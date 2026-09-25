#!/usr/bin/env python3
"""Pull the Theria "Hotel Animations" Google Drive folder to a local directory.

Reads drive/manifest.json (path -> Drive file id) and downloads each file over
the public share link. The folder is shared "anyone with the link", so no
OAuth is needed. Existing files whose byte size matches the manifest are
skipped, so re-runs are cheap.

Usage:
    python tools/drive_pull.py DEST_DIR [--max-mb N] [--only SUBSTRING] [--dry-run]

Examples:
    python tools/drive_pull.py ~/theria_pull --max-mb 400
    python tools/drive_pull.py D:/theria --only "Giraffe Manor/upscaled"

Stdlib only. Honours HTTPS_PROXY / SSL_CERT_FILE via urllib defaults.
"""
import argparse
import json
import os
import shutil
import ssl
import sys
import urllib.request
from pathlib import Path

DOWNLOAD_URL = "https://drive.usercontent.google.com/download?id={id}&export=download&confirm=t"
CHUNK = 1 << 20


def ssl_context():
    bundle = os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE")
    if bundle and Path(bundle).is_file():
        return ssl.create_default_context(cafile=bundle)
    return ssl.create_default_context()


def download(file_id: str, dest: Path, expected: int, ctx) -> int:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    req = urllib.request.Request(DOWNLOAD_URL.format(id=file_id), headers={"User-Agent": "curl/8"})
    with urllib.request.urlopen(req, context=ctx, timeout=120) as r, open(tmp, "wb") as out:
        ctype = r.headers.get("Content-Type", "")
        if ctype.startswith("text/html"):
            raise RuntimeError("got an HTML page instead of the file (sharing changed, or quota)")
        shutil.copyfileobj(r, out, CHUNK)
    got = tmp.stat().st_size
    if expected and got != expected:
        tmp.unlink(missing_ok=True)
        raise RuntimeError(f"size mismatch: expected {expected}, got {got}")
    tmp.replace(dest)
    return got


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dest")
    ap.add_argument("--manifest", default=str(Path(__file__).resolve().parent.parent / "drive" / "manifest.json"))
    ap.add_argument("--max-mb", type=float, default=None, help="skip files larger than this many MB")
    ap.add_argument("--only", default=None, help="only paths containing this substring")
    ap.add_argument("--skip-ds-store", action="store_true", default=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    manifest = json.loads(Path(a.manifest).read_text(encoding="utf-8"))
    dest_root = Path(a.dest).expanduser().resolve()
    ctx = ssl_context()
    ok = skipped = failed = 0
    for f in manifest["files"]:
        rel, fid, size = f["path"], f["id"], int(f["size"])
        if a.only and a.only not in rel:
            continue
        if a.skip_ds_store and rel.endswith(".DS_Store"):
            continue
        if a.max_mb is not None and size > a.max_mb * 1e6:
            print(f"SKIP  {size/1e6:8.1f} MB  {rel}  (over --max-mb)")
            skipped += 1
            continue
        dest = dest_root / Path(rel)
        if dest.is_file() and dest.stat().st_size == size:
            skipped += 1
            continue
        if a.dry_run:
            print(f"WOULD {size/1e6:8.1f} MB  {rel}")
            continue
        try:
            got = download(fid, dest, size, ctx)
            print(f"OK    {got/1e6:8.1f} MB  {rel}")
            ok += 1
        except Exception as e:  # noqa: BLE001
            print(f"FAIL  {size/1e6:8.1f} MB  {rel}  -> {e}", file=sys.stderr)
            failed += 1
    print(f"\ndownloaded {ok}, skipped {skipped}, failed {failed} -> {dest_root}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
