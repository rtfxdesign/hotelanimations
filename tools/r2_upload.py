#!/usr/bin/env python3
"""Mirror a local pull of the Drive folder into a Cloudflare R2 bucket.

UNTESTED against R2 as of 2026-09-25: this session had no R2 credentials.
The code is a plain S3-compatible upload via boto3, which is how R2 is
normally driven. Run it once with --dry-run, then for real.

Credentials come from environment variables only (never from the command line):
    R2_ACCOUNT_ID         Cloudflare account id (the hex string in the R2 dashboard URL)
    R2_ACCESS_KEY_ID      from an R2 API token with Object Read & Write on the bucket
    R2_SECRET_ACCESS_KEY  same token
    R2_BUCKET             bucket name, e.g. theria-hotel-animations

Usage:
    pip install boto3
    python tools/r2_upload.py LOCAL_ROOT [--prefix hotel-animations/] [--dry-run] [--max-mb N]

Keys mirror the Drive paths under --prefix, e.g.
    hotel-animations/Giraffe Manor/upscaled/giraffe_walking.mov
Existing objects with the same size are skipped, so re-runs only send changes.
"""
import argparse
import mimetypes
import os
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root")
    ap.add_argument("--prefix", default="hotel-animations/")
    ap.add_argument("--max-mb", type=float, default=None)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    missing = [k for k in ("R2_ACCOUNT_ID", "R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY", "R2_BUCKET") if not os.environ.get(k)]
    if missing:
        print("missing environment variables: " + ", ".join(missing), file=sys.stderr)
        return 2
    try:
        import boto3
        from boto3.s3.transfer import TransferConfig
    except ImportError:
        print("pip install boto3", file=sys.stderr)
        return 2

    s3 = boto3.client(
        "s3",
        endpoint_url=f"https://{os.environ['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com",
        aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
        region_name="auto",
    )
    bucket = os.environ["R2_BUCKET"]
    cfg = TransferConfig(multipart_threshold=64 * 1024 * 1024, multipart_chunksize=64 * 1024 * 1024)
    root = Path(a.root).expanduser().resolve()
    sent = skipped = 0
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.name.startswith(".") or p.suffix == ".part":
            continue
        size = p.stat().st_size
        if a.max_mb is not None and size > a.max_mb * 1e6:
            continue
        key = a.prefix + p.relative_to(root).as_posix()
        try:
            head = s3.head_object(Bucket=bucket, Key=key)
            if head.get("ContentLength") == size:
                skipped += 1
                continue
        except Exception:  # noqa: BLE001 — 404 means upload it
            pass
        if a.dry_run:
            print(f"WOULD {size/1e6:8.1f} MB  {key}")
            continue
        ctype = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
        s3.upload_file(str(p), bucket, key, ExtraArgs={"ContentType": ctype}, Config=cfg)
        print(f"OK    {size/1e6:8.1f} MB  {key}")
        sent += 1
    print(f"\nuploaded {sent}, skipped {skipped} -> r2://{bucket}/{a.prefix}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
