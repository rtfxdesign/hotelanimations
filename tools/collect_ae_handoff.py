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


def jsx(out: Path, film: str):
    """Copy the film's After Effects builder script next to its assets folder, when one exists."""
    j = SHEETS / "jsx" / f"build_{film}.jsx"
    if j.exists():
        cp(j, out / film)


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
    jsx(out, "giraffe_manor")


def key_white(im: Image.Image, span: int = 40) -> Image.Image:
    """Object on an off-white field -> RGBA, field level measured from the border."""
    import numpy as np
    a = np.array(im.convert("RGB")).astype(np.float32)
    lum = a.min(axis=2)
    border = np.concatenate([lum[:8].ravel(), lum[-8:].ravel(), lum[:, :8].ravel(), lum[:, -8:].ravel()])
    field = float(np.median(border))
    alpha = np.clip((field - 6 - lum) / span, 0, 1)
    return Image.fromarray(np.dstack([a, alpha * 255]).astype(np.uint8), "RGBA")


def north_island(pull: Path, out: Path):
    a = out / "north_island" / "assets"
    ni = pull / "North Island"
    cp(ni / "b261916d-7215-4f97-8607-d091aabe911a.png", a, "ni_lockup_white_1536x1024.png")
    a.mkdir(parents=True, exist_ok=True)
    key_white(Image.open(ni / "b261916d-7215-4f97-8607-d091aabe911a.png")).save(a / "ni_lockup_turtles_wordmark_alpha.png")
    cp(GEN / "05_north_island" / "ni_1_comp.png", a, "ni_water_16x9_3641x2048.png")
    cp(ni / "0873e031-511a-499b-a9d5-8a2b7a701d87.png", a, "ni_beach_3_turtles_1536x1024.png")
    for n in ("ni_2_t1.mp4", "ni_3_t1.mp4", "ni_4_t1.mp4"):
        cp(GEN / "05_north_island" / n, a)
    cp(ROOT / "north_island" / "animatic" / "north_island_animatic_v0.1.mp4", out / "north_island")
    cp(SHEETS / "north_island_EDIT_SHEET.md", out / "north_island", "EDIT_SHEET.md")
    jsx(out, "north_island")


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
    jsx(out, "passalacqua")


def miavana(pull: Path, out: Path):
    a = out / "miavana" / "assets"
    up = pull / "Miavana" / "upscaled"
    for n in ("miavana_0000_left_lemur.png", "miavana_0001_right_lemur.png", "miavana_0003_islandsanctuary.png", "miavana_0004_bytimeandtide.png", "resort_16x9.png"):
        cp(up / n, a)
    cp(WM / "miavana_wordmark.png", a)
    import importlib.util as ilu
    spec = ilu.spec_from_file_location("miavana_build_frames", ROOT / "miavana" / "storyboard" / "build_frames.py")
    mb = ilu.module_from_spec(spec); spec.loader.exec_module(mb)
    fitted, origin = mb.load_wordmark()
    fitted.save(a / "mi_wordmark_fitted_alpha.png")                # 1730 px wide, top-left (111, 326) at 100 %
    cp(GEN / "06_miavana" / "mi_4_comp_5k.png", a, "mi_palms_lemurs_comp_4988x2806.png")
    cp(GEN / "06_miavana" / "mi_4b_seated_alpha.png", a, "mi_seated_lemur_keyed_alpha.png")
    cp(GEN / "06_miavana" / "mi_4b_hanging_alpha.png", a, "mi_hanging_lemur_keyed_alpha.png")
    for n in ("mi_1a_t1.png", "mi_1b_t1.png", "mi_1c_t1.png", "mi_2_t1.mp4", "mi_3_t1.mp4"):
        cp(GEN / "06_miavana" / n, a)
    mango = ROOT / "miavana" / "animatic" / "mi_mango_cutout_alpha.png"
    if mango.exists():
        cp(mango, a)
    cp(ROOT / "miavana" / "animatic" / "miavana_animatic_v0.1.mp4", out / "miavana")
    cp(SHEETS / "miavana_EDIT_SHEET.md", out / "miavana", "EDIT_SHEET.md")
    jsx(out, "miavana")


def necker_island(pull: Path, out: Path):
    a = out / "necker_island" / "assets"
    kit = ROOT / "generation_kit" / "07_necker_island"
    cp(pull / "Necker Island" / "flamingo.png", a)
    cp(kit / "ne_shot1_START_flamingo_on_white.png", a)
    cp(kit / "ne_shot3_aerial_16x9.png", a, "ne_aerial_16x9_3840x2160.png")
    cp(kit / "ne_ref_flamingo_cutout_alpha.png", a)
    for n in ("ne_1_t1.mp4", "ne_2_t1.png", "ne_3_t1.mp4", "ne_4a_t1.png", "ne_4b_t1.png", "ne_5_t1.mp4"):
        cp(GEN / "07_necker_island" / n, a)
    cp(ROOT / "necker_island" / "animatic" / "necker_island_animatic_v0.1.mp4", out / "necker_island")
    cp(SHEETS / "necker_island_EDIT_SHEET.md", out / "necker_island", "EDIT_SHEET.md")
    jsx(out, "necker_island")


def fifth_avenue(pull: Path, out: Path):
    a = out / "fifth_avenue" / "assets"
    up = pull / "5th ave hotel NYC" / "upscaled"
    for n in ("turtlewalkers.psd", "woman.png", "man.png", "leash.png", "turtle.png", "Asset 1@2x.png"):
        cp(up / n, a)
    for n in ("fifth_avenue_wordmark.png", "fifth_avenue_wordmark_goldtype.png"):
        cp(WM / n, a)
    kit = ROOT / "generation_kit" / "02_fifth_avenue"
    cp(kit / "fa_shot5_START_walk.png", a); cp(kit / "fa_shot5_END_target_layers_offset.png", a)
    cp(GEN / "02_fifth_avenue" / "fa_1_t1.mp4", a)
    an = ROOT / "fifth_avenue" / "animatic"
    for n in ("fa_park_couple_no_tortoise.png", "fa_park_couple_leash.png", "fa_tortoise_hd_alpha.png"):
        if (an / n).exists():
            cp(an / n, a)
    cp(an / "fifth_avenue_animatic_v0.1.mp4", out / "fifth_avenue")
    cp(SHEETS / "fifth_avenue_EDIT_SHEET.md", out / "fifth_avenue", "EDIT_SHEET.md")
    jsx(out, "fifth_avenue")


def versailles(pull: Path, out: Path):
    a = out / "versailles" / "assets"
    v = pull / "Versali"
    cp(v / "cfb72e66-8752-47fc-8f43-2f824eeb0f1d.png", a, "cfb72e66_cake_chandelier_cutout_alpha.png")
    cp(v / "images copy.jpg", a)
    for n in ("ve_1_t1.png", "ve_2a_t1.png", "ve_2b_t1.png", "ve_3a_t1.png", "ve_3b_t1.png", "ve_4_t1.png"):
        cp(GEN / "04_versailles" / n, a)
    an = ROOT / "versailles" / "animatic"
    for p in sorted((an / "_elements").glob("*.png")) if (an / "_elements").exists() else []:
        cp(p, a)
    cp(an / "versailles_animatic_v0.1.mp4", out / "versailles")
    cp(SHEETS / "versailles_EDIT_SHEET.md", out / "versailles", "EDIT_SHEET.md")
    jsx(out, "versailles")


def club22(pull: Path, out: Path):
    a = out / "club22" / "assets"
    cp(WM / "club22_wordmark.png", a)
    for n in ("cl_1_t2.png", "cl_2_t1.png", "cl_3_t1.png", "club22_rhythm_124bpm.wav"):
        cp(GEN / "08_club22" / n, a)
    an = ROOT / "club22" / "animatic"
    for p in sorted((an / "_elements").glob("*.png")) if (an / "_elements").exists() else []:
        cp(p, a)
    cp(an / "club22_animatic_v0.1.mp4", out / "club22")
    cp(SHEETS / "club22_EDIT_SHEET.md", out / "club22", "EDIT_SHEET.md")
    jsx(out, "club22")


def main():
    pull, out = (Path(a).expanduser().resolve() for a in sys.argv[1:3])
    out.mkdir(parents=True, exist_ok=True)
    giraffe_manor(pull, out); north_island(pull, out); passalacqua(pull, out); miavana(pull, out); necker_island(pull, out); fifth_avenue(pull, out)
    versailles(pull, out); club22(pull, out)
    cp(SHEETS / "README.md", out)
    total = 0
    for p in sorted(out.rglob("*")):
        if p.is_file():
            total += p.stat().st_size
            print(f"{p.stat().st_size / 1048576:7.1f} MB  {p.relative_to(out)}")
    print(f"total {total / 1048576:.0f} MB -> {out}")


if __name__ == "__main__":
    main()
