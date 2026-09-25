#!/usr/bin/env python3
"""Assemble the After Effects handoff folders for the finished films.

    python3 tools/collect_ae_handoff.py PULL_ROOT OUT_DIR

PULL_ROOT  local mirror of the Theria Drive folder (has "Giraffe Manor/", "North Island/", "Passalaqua/")
OUT_DIR    where ae_handoff/<film>/ folders are written (assets + EDIT_SHEET.md + animatic)

Copies the plates, cut-outs, generated clips and wordmarks each comp needs, exports the derived
layers (crest bands, gold fish crops, held frames) and drops the edit sheet from docs/ae_handoff/
next to them. Files over 90 MB (the ProRes walk cycle) are not copied; the sheet says where they live.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter
import subprocess

ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / "generation_kit" / "output"
WM = ROOT / "assets" / "wordmarks"
SHEETS = ROOT / "docs" / "ae_handoff"
Image.MAX_IMAGE_PIXELS = None


def cp(src: Path, dst_dir: Path, name: str | None = None):
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / (name or src.name)
    if not dst.exists() or dst.stat().st_size != src.stat().st_size:
        shutil.copy2(src, dst)
    return dst


def last_frame(mp4: Path, dst: Path):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-sseof", "-0.2", "-i", str(mp4), "-update", "1", "-frames:v", "1", str(dst)], check=True)


def giraffe_manor(pull: Path, out: Path):
    a = out / "giraffe_manor" / "assets"
    gm = pull / "Giraffe Manor"
    cp(gm / "upscaled" / "ea5d5cfc-e93b-4d86-acf6-81bba6e7bd70.png", a, "gm_hero_cutout_alpha.png")
    cp(gm / "upscaled" / "manor01_background.png", a, "gm_manor_plate_no_giraffes.png")
    cp(WM / "giraffe_manor_wordmark.png", a)
    cp(gm / "audio" / "birdsong01.wav", a)
    for n in ("gm_2_t3.mp4", "gm_4_t1.mp4", "gm_1v_t1.mp4", "gm_3b_t1.png", "gm_3c_t1.png"):
        cp(GEN / "01_giraffe_manor" / n, a)
    cp(ROOT / "giraffe_manor" / "animatic" / "giraffe_manor_animatic_v0.3.mp4", out / "giraffe_manor")
    cp(SHEETS / "giraffe_manor_EDIT_SHEET.md", out / "giraffe_manor", "EDIT_SHEET.md")


def north_island(pull: Path, out: Path):
    a = out / "north_island" / "assets"
    ni = pull / "North Island"
    cp(ni / "b261916d-7215-4f97-8607-d091aabe911a.png", a, "ni_lockup_white_1536x1024.png")
    cp(GEN / "05_north_island" / "ni_1_comp.png", a, "ni_water_16x9_3641x2048.png")
    cp(ni / "0873e031-511a-499b-a9d5-8a2b7a701d87.png", a, "ni_beach_3_turtles_1536x1024.png")
    for n in ("ni_2_t1.mp4", "ni_3_t1.mp4", "ni_4_t1.mp4"):
        cp(GEN / "05_north_island" / n, a)
    cp(ROOT / "north_island" / "animatic" / "north_island_animatic_v0.1.mp4", out / "north_island")
    cp(SHEETS / "north_island_EDIT_SHEET.md", out / "north_island", "EDIT_SHEET.md")


def passalacqua(pull: Path, out: Path):
    a = out / "passalacqua" / "assets"
    a.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(ROOT / "passalacqua" / "storyboard"))
    import build_frames as B
    wm = Image.open(WM / "passalacqua_wordmark.png").convert("RGBA")
    for name, rows in (("pa_crest_fish_lineart.png", B.FISH_ROWS), ("pa_crest_wave_rule.png", B.WAVE_ROWS), ("pa_crest_type.png", B.TYPE_ROWS)):
        band = wm.crop((0, rows[0], wm.width, rows[1]))
        band.save(a / name)
        if "type" in name or "wave" in name:
            B.recolour(band, (255, 255, 255)).save(a / name.replace(".png", "_white.png"))
    gold = Image.open(pull / "Passalaqua" / "passalacqua.png").convert("RGBA")
    for i, box in enumerate(B.GOLD_FISH_BOXES):
        gold.crop(box).save(a / f"pa_gold_fish_{'LCR'[i]}.png")
    for n in ("pa_1_t1.png", "pa_2_t1.mp4", "pa_3_t1.mp4", "pa_4_t1.mp4", "pa_3_START_comp.png"):
        cp(GEN / "03_passalacqua" / n, a)
    last_frame(GEN / "03_passalacqua" / "pa_4_t1.mp4", a / "pa_4_last_frame.png")
    cp(WM / "passalacqua_wordmark.png", a)
    cp(ROOT / "passalacqua" / "animatic" / "passalacqua_animatic_v0.1.mp4", out / "passalacqua")
    cp(SHEETS / "passalacqua_EDIT_SHEET.md", out / "passalacqua", "EDIT_SHEET.md")


def main():
    pull, out = (Path(a).expanduser().resolve() for a in sys.argv[1:3])
    out.mkdir(parents=True, exist_ok=True)
    giraffe_manor(pull, out); north_island(pull, out); passalacqua(pull, out)
    cp(SHEETS / "README.md", out)
    total = 0
    for p in sorted(out.rglob("*")):
        if p.is_file():
            total += p.stat().st_size
            print(f"{p.stat().st_size / 1048576:7.1f} MB  {p.relative_to(out)}")
    print(f"total {total / 1048576:.0f} MB -> {out}")


if __name__ == "__main__":
    main()
