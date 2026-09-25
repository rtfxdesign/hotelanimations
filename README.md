# hotelanimations
Theria Hotel Animations — working notes, inventory and tooling for the eight hotel films. Assets live in the Google Drive folder "Hotel Animations" (id `1ACTa41JOtVEZU7itaOsRUOOVOIfB4kv4`); this repo holds no media, only a manifest, measurements, previews and scripts.

Read in this order:
1. `HANDOFF_claude_code.md` — the 2026-09-25 Cowork handoff (context, rules, open questions).
2. `INVENTORY_2026-09-25.md` — measured inventory, corrections to the handoff, storyboard findings, next steps. Also as `docs/INVENTORY_2026-09-25.html` and `.pdf`.
3. `theria_hotel_animations_timing_v1.md` — shot timings (source of truth for cuts, see open question 6 in the inventory).
4. `theria_higgsfield_asset_pipeline_v1.md` — model routing and prompts (ignore its 4K lines; delivery is HD).

Layout:
- `drive/manifest.json` — every Drive file with id, size, modified time.
- `tools/drive_pull.py` — mirror the Drive folder locally (stdlib, cross-platform, resumable).
- `tools/measure.py` — pixel dims / alpha / video probe / sha256 for a tree (Pillow + ffprobe).
- `tools/r2_upload.py` — mirror a local tree into Cloudflare R2 (boto3; untested, needs `R2_*` env vars).
- `inventory/` — measurements, PSD layer maps, rendered storyboard text, previews.

Quick start:
```
python tools/drive_pull.py ./theria_pull --max-mb 400
python tools/measure.py ./theria_pull -o measurements.json --md measurements.md
```
