#!/usr/bin/env python3
"""Build 1920x1080 replacement frames for storyboard beats from generated outputs.

Writes docs/frame_overrides/<film>__<frame_stem>.jpg and docs/frame_overrides.json,
which tools/build_storyboard_site.py reads to swap board frames for generated ones.
Re-run after each generation round; only beats with an approved output are listed.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image

Image.MAX_IMAGE_PIXELS = None
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "frame_overrides"
GEN = ROOT / "generation_kit" / "output"
KIT = ROOT / "generation_kit"
W, H = 1920, 1080


def fit_16x9(im: Image.Image) -> Image.Image:
    """Centre-crop to 16:9 then resize to 1920x1080."""
    im = im.convert("RGB")
    tw = im.height * 16 / 9
    if abs(tw - im.width) > 1:
        if im.width > tw:
            x = round((im.width - tw) / 2); im = im.crop((x, 0, round(x + tw), im.height))
        else:
            th = im.width * 9 / 16; y = round((im.height - th) / 2); im = im.crop((0, y, im.width, round(y + th)))
    return im.resize((W, H), Image.LANCZOS)


def video_frame(mp4: Path, n: int) -> Image.Image:
    tmp = OUT / "_frame.png"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf", f"select=eq(n\\,{n})", "-vframes", "1", str(tmp)], check=True)
    im = Image.open(tmp).convert("RGB"); tmp.unlink(); return im


def versailles_salon() -> Image.Image:
    """VE-1 clean salon with the real cake+chandelier cut-out (alpha) standing centre."""
    plate = fit_16x9(Image.open(GEN / "04_versailles" / "ve_1_t1.png"))
    cut = Image.open(KIT / "04_versailles" / "ve_ref_cake_chandelier_cutout_alpha.png").convert("RGBA")
    bb = cut.getchannel("A").getbbox(); cut = cut.crop(bb)
    target_h = 990; s = target_h / cut.height
    cut = cut.resize((round(cut.width * s), target_h), Image.LANCZOS)
    plate = plate.convert("RGBA")
    plate.alpha_composite(cut, (W // 2 - cut.width // 2, 1040 - target_h))
    return plate.convert("RGB")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    items = {
        # film/frame_stem : (image, note)
        "giraffe_manor/07_turn_TOGEN": (fit_16x9(Image.open(GEN / "01_giraffe_manor" / "gm_2_rear_end.png")), "generated end plate, round 0"),
        "giraffe_manor/08_window_TOGEN": (fit_16x9(Image.open(GEN / "01_giraffe_manor" / "gm_3_t1.png")), "generated plate, round 0 (house continuity being redone)"),
        "fifth_avenue/06_walk_end_TOGEN": (fit_16x9(video_frame(GEN / "02_fifth_avenue" / "fa_1_t1.mp4", 120)), "generated clip, take 1, last frame"),
        "passalacqua/07_pullback_TOGEN": (fit_16x9(Image.open(GEN / "03_passalacqua" / "pa_1_t1.png")), "generated clean lake plate, round 0"),
        "versailles/02b_salon": (versailles_salon(), "generated clean salon plate + real cake cut-out"),
        "miavana/06_palms_TOGEN": (fit_16x9(Image.open(GEN / "06_miavana" / "mi_4_t1.png")), "generated plate with lemurs, round 0"),
        "club22/03_decks_TOGEN": (fit_16x9(video_frame(GEN / "08_club22" / "club22_seamless_loop_v0.1.mp4", 148)), "generated vinyl, comp draft"),
        "club22/04_spotlight_COMP": (fit_16x9(video_frame(GEN / "08_club22" / "club22_seamless_loop_v0.1.mp4", 185)), "generated vinyl, comp draft"),
    }
    index = {}
    for key, (im, note) in items.items():
        name = key.replace("/", "__") + ".jpg"
        im.save(OUT / name, "JPEG", quality=90, subsampling=0)
        index[key] = {"file": f"docs/frame_overrides/{name}", "note": note}
        print(f"{key:36s} -> {name}")
    (ROOT / "docs" / "frame_overrides.json").write_text(json.dumps(index, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
