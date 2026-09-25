#!/usr/bin/env python3
"""Run the Theria generation kit through the Higgsfield API.

Reads generation_kit/jobs.json, uploads the input frames, submits each job,
polls, and downloads the outputs to generation_kit/output/<film>/.

Credentials come from the environment only (never from arguments or files):
    HF_KEY="<key id>:<key secret>"        (same variable the official client reads)
or  HF_API_KEY / HF_API_SECRET

Usage
    python3 tools/higgsfield_run.py --dry-run                 # validate + print the plan, no network
    python3 tools/higgsfield_run.py --phase A                 # run every phase-A job
    python3 tools/higgsfield_run.py --only GM-2,FA-1 --takes 3
    python3 tools/higgsfield_run.py --phase B                 # jobs that take phase-A outputs as input
    python3 tools/higgsfield_run.py --resume                  # re-poll anything the ledger shows unfinished
    python3 tools/higgsfield_run.py --pick GM-2=2 --phase B   # use take 2 of GM-2 as the upstream for phase B

Standard library only (urllib, json, hashlib). Pillow is used to flatten alpha
and shrink oversized inputs; ffmpeg is used to pull first/last frames from
upstream video outputs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import subprocess
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

API = "https://api.higgsfield.ai"
ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "generation_kit"
OUT = KIT / "output"
AUX = KIT / "_aux"
LEDGER = OUT / "ledger.json"
UPLOADS = KIT / ".uploads.json"
UPLOAD_TTL_S = 6 * 3600          # re-upload after this; inputs are tagged retention=temporary
MAX_INPUT_PX = 4096              # longest side sent to the API
MAX_INPUT_BYTES = 18 * 1024 * 1024

VIDEO_ENDPOINTS = ("kling-video/", "seedance", "minimax/", "wan/", "ltx")


# ----------------------------------------------------------------------------- credentials
def credentials() -> str:
    key = os.getenv("HF_KEY")
    if not key:
        a, b = os.getenv("HF_API_KEY"), os.getenv("HF_API_SECRET")
        if a and b:
            key = f"{a}:{b}"
    if not key or ":" not in key:
        sys.exit("No Higgsfield credentials. Set HF_KEY=\"<key id>:<key secret>\" in the environment "
                 "(or HF_API_KEY and HF_API_SECRET). Never pass them on the command line.")
    return key


def api(method: str, path: str, body: dict | None = None, key: str | None = None) -> dict:
    url = path if path.startswith("http") else API + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    if key:
        req.add_header("Authorization", f"Key {key}")
    backoff = 2.0
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read().decode() or "{}")
        except urllib.error.HTTPError as e:
            text = e.read().decode(errors="replace")
            if e.code in (429, 500, 502, 503, 504) and attempt < 5:
                time.sleep(backoff + random.random()); backoff *= 2
                continue
            raise RuntimeError(f"{method} {url} -> HTTP {e.code}: {text[:400]}") from None
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < 5:
                time.sleep(backoff + random.random()); backoff *= 2
                continue
            raise RuntimeError(f"{method} {url} -> {e}") from None
    raise RuntimeError("unreachable")


# ----------------------------------------------------------------------------- inputs
def prepared_input(src: Path) -> Path:
    """Flatten alpha onto white, cap the longest side, cap the byte size. Returns a file to upload."""
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    im = Image.open(src)
    needs = im.mode in ("RGBA", "LA", "P") or max(im.size) > MAX_INPUT_PX or src.stat().st_size > MAX_INPUT_BYTES
    if not needs:
        return src
    AUX.mkdir(parents=True, exist_ok=True)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        bg.alpha_composite(im)
        im = bg.convert("RGB")
    else:
        im = im.convert("RGB")
    if max(im.size) > MAX_INPUT_PX:
        s = MAX_INPUT_PX / max(im.size)
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    dst = AUX / f"{src.stem}_upload.png"
    im.save(dst, "PNG", optimize=True)
    if dst.stat().st_size > MAX_INPUT_BYTES:
        dst = AUX / f"{src.stem}_upload.jpg"
        im.save(dst, "JPEG", quality=94, subsampling=0)
    return dst


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(p: Path, default):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default


def save_json(p: Path, obj) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=1, ensure_ascii=False), encoding="utf-8")
    tmp.replace(p)


def upload(path: Path, key: str, cache: dict) -> str:
    """Upload once per content hash; return the public URL the API can read."""
    prepared = prepared_input(path)
    digest = sha256(prepared)
    hit = cache.get(digest)
    if hit and time.time() - hit["at"] < UPLOAD_TTL_S:
        return hit["url"]
    ctype = "image/png" if prepared.suffix.lower() == ".png" else "image/jpeg"
    if prepared.suffix.lower() == ".mp4":
        ctype = "video/mp4"
    info = api("POST", "/files/generate-upload-url", {"content_type": ctype}, key)
    req = urllib.request.Request(info["upload_url"], data=prepared.read_bytes(), method="PUT")
    for k, v in info.get("upload_headers", {}).items():
        req.add_header(k, v)           # no Higgsfield credentials go to the storage URL
    with urllib.request.urlopen(req, timeout=600) as r:
        if r.status not in (200, 201, 204):
            raise RuntimeError(f"upload of {path.name} returned {r.status}")
    cache[digest] = {"url": info["public_url"], "at": time.time(), "file": str(path.relative_to(ROOT))}
    save_json(UPLOADS, cache)
    return info["public_url"]


# ----------------------------------------------------------------------------- upstream outputs
def output_file(ledger: dict, job_id: str, take: int) -> Path:
    rec = ledger.get(f"{job_id}#{take}")
    if not rec or rec.get("status") != "completed" or not rec.get("file"):
        raise RuntimeError(f"{job_id} take {take} has no completed output in the ledger; run it first")
    return ROOT / rec["file"]


def frame_of(video: Path, which: str) -> Path:
    AUX.mkdir(parents=True, exist_ok=True)
    dst = AUX / f"{video.stem}_{which}.png"
    if dst.exists() and dst.stat().st_mtime >= video.stat().st_mtime:
        return dst
    if which == "first_frame":
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-frames:v", "1", str(dst)]
    else:
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-sseof", "-0.2", "-i", str(video), "-update", "1", "-frames:v", "1", str(dst)]
    subprocess.run(cmd, check=True)
    return dst


def resolve_input(spec: str, ledger: dict, picks: dict) -> Path:
    """'01_giraffe_manor/x.png' -> kit file; 'out:GM-2' -> that job's output; 'out:GM-2:last_frame' -> a frame of it."""
    if spec.startswith("out:"):
        parts = spec.split(":")
        job_id = parts[1]
        take = int(picks.get(job_id, 1))
        f = output_file(ledger, job_id, take)
        if len(parts) > 2:
            return frame_of(f, parts[2])
        return f
    if spec.startswith("aux:"):
        return make_aux(spec[4:])
    p = KIT / spec
    if not p.exists():
        raise FileNotFoundError(p)
    return p


def make_aux(name: str) -> Path:
    from PIL import Image
    AUX.mkdir(parents=True, exist_ok=True)
    p = AUX / name
    if p.exists():
        return p
    if name == "white_16x9.png":
        Image.new("RGB", (1920, 1080), (255, 255, 255)).save(p)
    elif name == "black_16x9.png":
        Image.new("RGB", (1920, 1080), (0, 0, 0)).save(p)
    else:
        raise ValueError(f"unknown aux frame {name}")
    return p


# ----------------------------------------------------------------------------- jobs
def is_video(endpoint: str) -> bool:
    return endpoint.startswith(VIDEO_ENDPOINTS)


def build_body(job: dict, ledger: dict, picks: dict, key: str | None, cache: dict, dry: bool) -> dict:
    body = dict(job.get("args", {}))
    body["prompt"] = job["prompt"]
    for field, spec in job.get("inputs", {}).items():
        if isinstance(spec, list):
            paths = [resolve_input(s, ledger, picks) for s in spec]
            body[field] = [str(p) if dry else upload(p, key, cache) for p in paths]
        else:
            p = resolve_input(spec, ledger, picks)
            body[field] = str(p) if dry else upload(p, key, cache)
    return body


def submit(job: dict, take: int, body: dict, key: str) -> dict:
    backoff = 5.0
    while True:
        try:
            return api("POST", "/" + job["endpoint"], body, key)
        except RuntimeError as e:
            if "concurrent requests" in str(e) and backoff < 120:
                time.sleep(backoff + random.random() * 2); backoff *= 1.6
                continue
            raise


def poll(status_url: str, key: str, label: str) -> dict:
    wait = 2.0
    t0 = time.time()
    while True:
        st = api("GET", status_url, None, key)
        s = st.get("status")
        if s in ("completed", "failed", "nsfw", "canceled"):
            return st
        if time.time() - t0 > 40 * 60:
            raise RuntimeError(f"{label}: still {s} after 40 min; leaving it in the ledger for --resume")
        time.sleep(wait + random.random())
        wait = min(10.0, wait * 1.4)


def download(url: str, dst: Path) -> Path:
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_suffix(dst.suffix + ".part")
    with urllib.request.urlopen(url, timeout=900) as r, open(tmp, "wb") as f:
        for chunk in iter(lambda: r.read(1 << 20), b""):
            f.write(chunk)
    tmp.replace(dst)
    return dst


def result_url(st: dict) -> tuple[str, str]:
    if st.get("video") and st["video"].get("url"):
        return st["video"]["url"], ".mp4"
    if st.get("images"):
        u = st["images"][0]["url"]
        ext = ".jpg" if u.lower().split("?")[0].endswith((".jpg", ".jpeg")) else ".png"
        return u, ext
    raise RuntimeError(f"completed but no media in status: {json.dumps(st)[:300]}")


def run_take(job: dict, take: int, body: dict, key: str, ledger: dict, lock) -> dict:
    lid = f"{job['id']}#{take}"
    rec = {"job": job["id"], "take": take, "film": job["film"], "endpoint": job["endpoint"],
           "body": {k: v for k, v in body.items()}, "submitted": time.time()}
    acc = submit(job, take, body, key)
    rec.update(request_id=acc["request_id"], status_url=acc["status_url"], status=acc.get("status", "queued"))
    with lock:
        ledger[lid] = rec; save_json(LEDGER, ledger)
    print(f"  {lid}: submitted {rec['request_id']}", flush=True)
    st = poll(acc["status_url"], key, lid)
    rec["status"] = st["status"]
    rec["finished"] = time.time()
    if st["status"] == "completed":
        url, ext = result_url(st)
        dst = OUT / job["film"] / f"{job['id'].replace('-', '_').lower()}_t{take}{ext}"
        download(url, dst)
        rec["url"] = url
        rec["file"] = str(dst.relative_to(ROOT))
        print(f"  {lid}: completed -> {rec['file']} ({dst.stat().st_size/1048576:.1f} MiB, {rec['finished']-rec['submitted']:.0f} s)", flush=True)
    else:
        rec["error"] = st.get("error")
        print(f"  {lid}: {st['status']} {st.get('error') or ''}", flush=True)
    with lock:
        ledger[lid] = rec; save_json(LEDGER, ledger)
    return rec


def resume(ledger: dict, key: str, jobs_by_id: dict) -> None:
    pending = [(lid, r) for lid, r in ledger.items() if r.get("status") not in ("completed", "failed", "nsfw", "canceled")]
    if not pending:
        print("nothing pending in the ledger"); return
    for lid, rec in pending:
        job = jobs_by_id[rec["job"]]
        st = poll(rec["status_url"], key, lid)
        rec["status"] = st["status"]; rec["finished"] = time.time()
        if st["status"] == "completed":
            url, ext = result_url(st)
            dst = OUT / job["film"] / f"{job['id'].replace('-', '_').lower()}_t{rec['take']}{ext}"
            download(url, dst); rec["url"] = url; rec["file"] = str(dst.relative_to(ROOT))
        else:
            rec["error"] = st.get("error")
        print(f"  {lid}: {rec['status']} {rec.get('file', rec.get('error') or '')}")
        save_json(LEDGER, ledger)


# ----------------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--jobs", default=str(KIT / "jobs.json"))
    ap.add_argument("--phase", help="A or B (default: all phases whose inputs resolve)")
    ap.add_argument("--only", help="comma-separated job ids")
    ap.add_argument("--takes", type=int, help="override takes for every selected job")
    ap.add_argument("--pick", action="append", default=[], help="JOB=TAKE: which take feeds downstream jobs (default 1)")
    ap.add_argument("--concurrency", type=int, default=3, help="parallel requests in flight (account limit applies)")
    ap.add_argument("--dry-run", action="store_true", help="validate inputs and print the plan; no network, no spend")
    ap.add_argument("--resume", action="store_true", help="re-poll unfinished requests from the ledger")
    ap.add_argument("--force", action="store_true", help="re-run takes that already completed")
    a = ap.parse_args()

    jobs = json.loads(Path(a.jobs).read_text(encoding="utf-8"))["jobs"]
    jobs_by_id = {j["id"]: j for j in jobs}
    ledger = load_json(LEDGER, {})
    picks = dict(p.split("=", 1) for p in a.pick)

    if a.resume:
        resume(ledger, credentials(), jobs_by_id); return 0

    sel = jobs
    if a.phase:
        sel = [j for j in sel if j.get("phase", "A").upper() == a.phase.upper()]
    if a.only:
        want = {s.strip() for s in a.only.split(",")}
        missing = want - set(jobs_by_id)
        if missing:
            sys.exit(f"unknown job ids: {sorted(missing)}")
        sel = [j for j in sel if j["id"] in want]
    if not sel:
        sys.exit("no jobs selected")

    key = None if a.dry_run else credentials()
    cache = load_json(UPLOADS, {})
    plan = []
    for j in sel:
        takes = a.takes or j.get("takes", 1)
        try:
            body = build_body(j, ledger, picks, key, cache, a.dry_run)
        except (FileNotFoundError, RuntimeError) as e:
            print(f"SKIP {j['id']}: {e}")
            continue
        for t in range(1, takes + 1):
            lid = f"{j['id']}#{t}"
            if not a.force and ledger.get(lid, {}).get("status") == "completed":
                print(f"have {lid}: {ledger[lid]['file']}")
                continue
            plan.append((j, t, body))

    n_vid = sum(1 for j, _, _ in plan if is_video(j["endpoint"]))
    n_img = len(plan) - n_vid
    print(f"\n{len(plan)} requests to submit: {n_vid} video, {n_img} image\n")
    for j, t, body in plan:
        ins = {k: v for k, v in body.items() if k.endswith("url") or k.endswith("urls")}
        extra = {k: v for k, v in body.items() if k not in ins and k != "prompt"}
        print(f"{j['id']}#{t}  {j['endpoint']}  {extra}")
        for k, v in ins.items():
            print(f"    {k}: {v}")
        print(f"    prompt: {body['prompt'][:110]}{'…' if len(body['prompt']) > 110 else ''}")
    if a.dry_run:
        print("\ndry run: nothing submitted, nothing spent")
        return 0

    import threading
    lock = threading.Lock()
    done, failed = 0, 0
    with ThreadPoolExecutor(max_workers=a.concurrency) as ex:
        futs = {ex.submit(run_take, j, t, body, key, ledger, lock): (j, t) for j, t, body in plan}
        for fut in as_completed(futs):
            j, t = futs[fut]
            try:
                rec = fut.result()
                done += rec.get("status") == "completed"
                failed += rec.get("status") != "completed"
            except Exception as e:  # keep the rest running
                failed += 1
                print(f"  {j['id']}#{t}: ERROR {e}", flush=True)
    print(f"\ncompleted {done}, not completed {failed}. Ledger: {LEDGER.relative_to(ROOT)}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
