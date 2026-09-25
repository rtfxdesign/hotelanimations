#!/usr/bin/env python3
"""Measure every image / video / PSD under a directory tree.

Images (PNG/JPG/WEBP/PSD): width, height, mode, alpha, alpha bounding box
(for cut-outs: how much of the canvas is actually opaque), sha256.
Video (MP4/MOV): codec, width, height, fps, frames, duration, pix_fmt, sha256.
Requires: Pillow. ffprobe on PATH for video (skipped if absent).

Usage:
    python tools/measure.py ROOT_DIR -o measurements.json [--md report.md]
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

Image.MAX_IMAGE_PIXELS = None
IMG = {".png", ".jpg", ".jpeg", ".webp", ".psd"}
VID = {".mp4", ".mov"}


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def measure_image(p: Path) -> dict:
    d = {}
    with Image.open(p) as im:
        d.update(format=im.format, width=im.width, height=im.height, mode=im.mode)
        if im.format == "PSD":
            try:
                d["psd_layers"] = len(getattr(im, "layers", []) or [])
            except Exception:  # noqa: BLE001
                pass
        if "A" in im.getbands():
            a = im.getchannel("A")
            bbox = a.getbbox()
            d["alpha"] = True
            if bbox:
                d["alpha_bbox"] = list(bbox)
                d["opaque_w"] = bbox[2] - bbox[0]
                d["opaque_h"] = bbox[3] - bbox[1]
                lo, hi = a.getextrema()
                d["alpha_min_max"] = [lo, hi]
            else:
                d["alpha_bbox"] = None
        else:
            d["alpha"] = False
        info = im.info
        if "dpi" in info:
            d["dpi"] = [round(x) for x in info["dpi"]]
    return d


def measure_video(p: Path) -> dict:
    if not shutil.which("ffprobe"):
        return {"error": "ffprobe not on PATH"}
    cmd = ["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(p)]
    j = json.loads(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)
    out = {"streams": []}
    for s in j.get("streams", []):
        e = {"type": s.get("codec_type"), "codec": s.get("codec_name")}
        if s.get("codec_type") == "video":
            num, den = (s.get("r_frame_rate") or "0/1").split("/")
            fps = float(num) / float(den) if float(den) else 0
            e.update(width=s.get("width"), height=s.get("height"), fps=round(fps, 3),
                     frames=int(s["nb_frames"]) if s.get("nb_frames", "N/A") != "N/A" else None,
                     pix_fmt=s.get("pix_fmt"), profile=s.get("profile"), bit_rate=s.get("bit_rate"))
        out["streams"].append(e)
    f = j.get("format", {})
    out["duration_s"] = round(float(f.get("duration", 0)), 3)
    out["container"] = f.get("format_name")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--md", default=None, help="also write a markdown table")
    a = ap.parse_args()
    root = Path(a.root).expanduser().resolve()
    rows = []
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.name.startswith("."):
            continue
        ext = p.suffix.lower()
        if ext not in IMG | VID:
            continue
        rel = p.relative_to(root).as_posix()
        row = {"path": rel, "bytes": p.stat().st_size, "sha256": sha256(p)}
        try:
            row.update(measure_image(p) if ext in IMG else measure_video(p))
        except Exception as e:  # noqa: BLE001
            row["error"] = f"{type(e).__name__}: {e}"
        rows.append(row)
        print(rel, {k: v for k, v in row.items() if k in ("width", "height", "mode", "streams", "error")}, file=sys.stderr)
    Path(a.out).write_text(json.dumps(rows, indent=1), encoding="utf-8")
    if a.md:
        lines = ["| path | MB | dims | mode / codec | fps | dur s | opaque bbox (cut-outs) |", "|---|---|---|---|---|---|---|"]
        for r in rows:
            if "streams" in r:
                v = next((s for s in r["streams"] if s["type"] == "video"), {})
                lines.append(f"| {r['path']} | {r['bytes']/1e6:.1f} | {v.get('width')}×{v.get('height')} | {v.get('codec')} {v.get('pix_fmt') or ''} | {v.get('fps')} | {r['duration_s']} | {v.get('frames')} frames |")
            elif "error" in r:
                lines.append(f"| {r['path']} | {r['bytes']/1e6:.1f} | ERROR | {r['error']} | | | |")
            else:
                bb = f"{r['opaque_w']}×{r['opaque_h']} at {r['alpha_bbox'][:2]}" if r.get("alpha_bbox") else ("no alpha" if not r.get("alpha") else "fully transparent")
                lines.append(f"| {r['path']} | {r['bytes']/1e6:.1f} | {r['width']}×{r['height']} | {r['format']} {r['mode']} | | | {bb} |")
        Path(a.md).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(rows)} files measured -> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
