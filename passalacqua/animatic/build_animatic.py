#!/usr/bin/env python3
"""Passalacqua animatic v0.1 — 360 frames, 15.0 s at 24 fps, 16:9 HD, loops on frame 0.

Timing from theria_hotel_animations_timing_v1.md §3 plus the return beats, as boarded in
passalacqua/storyboard/STORYBOARD.md. Reuses the storyboard builder's crest maths.
Generated clips (generation_kit/output/03_passalacqua/):
  PA-2 alive  pa_2_t1.mp4 (Kling 3 from the gold fish on white)
  PA-3 drop   pa_3_t1.mp4 (Kling 3 from the PA-1 clean lake + fish comp)
  PA-4 leap   pa_4_t1.mp4 (Kling 3 from the PA-1 clean lake)

    python3 passalacqua/animatic/build_animatic.py PULL_ROOT OUT_DIR [--no-burnin]

Shot plan:
  B1 crest     f0-48     line-art fish + wave rule on white (loop frame)
  B2 wordmark  f48-86    type 0->1 over f48-67, hold
  B3 fill      f86-120   type 1->0 f86-98; gold wipes up each fish L/C/R from f100, 16 f each, 3 f stagger
  B4 alive     f120-158  6 f dissolve into PA-2 f0, then PA-2 1:1
  B5 lake      f158-197  12 f dissolve PA-2 -> PA-3 f0, PA-3 f0-120 retimed 3x into the beat
  B6 leap      f197-293  PA-4 f0-120 retimed 1.26x
  B7 end card  f293-312  PA-4 last frame darkened; rings; rule + type reversed out, 0->1 over 12 f
  B8 settle    f312-336  lake -> white; fish rise to crest positions; type white -> black
  B9 flatten   f336-355  gold drains head-down R/C/L; type 1->0 f343-355
  B10 loop     f355-360  = frame 0
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "passalacqua" / "storyboard"))
import build_frames as B  # noqa: E402  (the storyboard builder: Crest, gold fish helpers, rings)

W, H, FPS, TOTAL = 1920, 1080, 24, 360
GEN = ROOT / "generation_kit" / "output" / "03_passalacqua"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SHOTS = [("B1 crest", 0, 48), ("B2 wordmark", 48, 86), ("B3 fill (AE)", 86, 120), ("B4 alive (Kling PA-2)", 120, 158),
         ("B5 lake (Kling PA-3, 3x)", 158, 197), ("B6 leap (Kling PA-4, 1.26x)", 197, 293), ("B7 end card (AE)", 293, 312),
         ("B8 settle (AE)", 312, 336), ("B9 flatten (AE)", 336, 355), ("B10 loop", 355, 360)]


def ease(t):
    t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)


def lerp(a, b, t):
    return a + (b - a) * t


def font(size):
    return ImageFont.truetype(FONT, size)


def fit(im):
    return im.convert("RGBA").resize((W, H), Image.LANCZOS) if im.size != (W, H) else im.convert("RGBA")


class Clips:
    def __init__(self, out: Path):
        self.dir = out / "_clips"; self.cache = {}; self.n = {}
        for name in ("pa_2_t1", "pa_3_t1", "pa_4_t1"):
            d = self.dir / name
            if not d.exists() or not any(d.glob("*.png")):
                d.mkdir(parents=True, exist_ok=True)
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(GEN / f"{name}.mp4"), "-vsync", "0", str(d / "f%03d.png")], check=True)
            self.n[name] = len(list(d.glob("*.png")))

    def frame(self, name, i):
        i = max(0, min(self.n[name] - 1, int(round(i))))
        if (name, i) not in self.cache:
            self.cache[(name, i)] = fit(Image.open(self.dir / name / f"f{i + 1:03d}.png"))
        return self.cache[(name, i)]


def burn(im, f, shot, extra=None):
    d = ImageDraw.Draw(im); ff = font(22)
    txt = f"PASSALACQUA · ANIMATIC v0.1 · {shot} · f{f:03d} · {f / FPS:05.2f}s"
    tw = d.textlength(txt, font=ff)
    d.rectangle((16, 16, 16 + tw + 20, 52), fill=(0, 0, 0, 255)); d.text((26, 22), txt, font=ff, fill=(255, 176, 32))
    if extra:
        fe = font(26); tw = d.textlength(extra, font=fe)
        d.rectangle((W // 2 - tw // 2 - 20, H - 88, W // 2 + tw // 2 + 20, H - 40), fill=(0, 0, 0, 255)); d.text((W // 2 - tw // 2, H - 80), extra, font=fe, fill=(255, 176, 32))


def shot_name(f):
    return next(n for n, a, b in SHOTS if a <= f < b)


class Scene:
    def __init__(self, pull: Path, out: Path):
        src = pull / "Passalaqua"
        self.crest = B.Crest(ROOT / "assets" / "wordmarks" / "passalacqua_wordmark.png")
        self.gold = Image.open(src / "passalacqua.png").convert("RGBA")
        self.C = Clips(out)
        self.art = self.crest.paste_bands(B.blank(), (B.FISH_ROWS, 1.0), (B.WAVE_ROWS, 1.0))
        self.wave_c = self.crest.wave_centre()

    def crest_frame(self, type_op, gold_keep=(0.0, 0.0, 0.0), fish_from_top=False):
        """Line art + wave rule, type at `type_op`, gold fish partially filled (fraction per fish, from the tail up)."""
        f = self.crest.paste_bands(B.blank(), (B.FISH_ROWS, 1.0), (B.WAVE_ROWS, 1.0))
        if type_op > 0:
            self.crest.paste_bands(f, (B.TYPE_ROWS, type_op))
        for i, k in enumerate(gold_keep):
            if k <= 0:
                continue
            layer, pos = B.gold_fish_registered(self.gold, self.crest, i)
            if k >= 1:
                f.alpha_composite(layer, pos)
            elif fish_from_top:
                f.alpha_composite(B.vertical_mask(layer, 1 - k, 1.0), pos)     # drained from the head down: keep the lower part
            else:
                f.alpha_composite(B.vertical_mask(layer, 1 - k, 1.0), pos)     # filled from the tail up: keep the lower part
        return f

    def end_card(self, t_in, base):
        dark = ImageEnhance.Color(base.convert("RGB").filter(ImageFilter.GaussianBlur(3))).enhance(0.5).convert("RGBA")
        dark.alpha_composite(Image.new("RGBA", (W, H), (0, 10, 25, int(150 * t_in))))
        cx, cy = self.wave_c
        B.ripple_rings(dark, cx, cy, n=5, rx0=190 * (0.6 + 0.4 * t_in), ry0=28 * (0.6 + 0.4 * t_in), step=1.4, alpha=int(170 * t_in))
        for rows in (B.WAVE_ROWS, B.TYPE_ROWS):
            layer, pos = self.crest.band(rows, t_in, rgb=(255, 255, 255))
            dark.alpha_composite(layer, pos)
        return dark

    def render(self, f, burnin=True):
        C = self.C; extra = None
        if f < 48:
            im = self.art.copy()
        elif f < 86:
            im = self.crest_frame(ease((f - 48) / 19))
        elif f < 120:
            top = 1 - ease((f - 86) / 12)
            keep = tuple(ease((f - (100 + 3 * i)) / 16) for i in range(3))
            im = self.crest_frame(top, keep)
            extra = "AE: gold wipes up each fish from the tail, L/C/R, 3-frame stagger"
        elif f < 158:
            im = C.frame("pa_2_t1", f - 120).copy()
            if f < 126:
                im = Image.blend(self.crest_frame(0, (1, 1, 1)), im, ease((f - 120) / 6))
            extra = "Kling PA-2 1:1"
        elif f < 197:
            i = (f - 158) * (C.n["pa_3_t1"] - 1) / 38
            im = C.frame("pa_3_t1", i).copy()
            if f < 170:
                im = Image.blend(C.frame("pa_2_t1", 37), im, ease((f - 158) / 12))
            extra = "Kling PA-3 retimed 3x (fish drop right, left, centre)"
        elif f < 293:
            i = (f - 197) * (C.n["pa_4_t1"] - 1) / 95
            im = C.frame("pa_4_t1", i).copy()
            extra = "Kling PA-4 retimed 1.26x; fish read live and large — comp scale/gold pass later"
        elif f < 312:
            im = self.end_card(ease((f - 293) / 12), C.frame("pa_4_t1", C.n["pa_4_t1"] - 1))
            extra = "AE: rings spread, rule + type reversed out at crest positions"
        elif f < 336:
            t = ease((f - 312) / 24)
            base = Image.blend(self.end_card(1.0, C.frame("pa_4_t1", C.n["pa_4_t1"] - 1)), B.blank(), t)
            self.crest.paste_bands(base, (B.WAVE_ROWS, t), (B.TYPE_ROWS, t))
            for i, (rot, dy) in enumerate(((-6, 90), (3, 60), (-4, 110))):
                layer, pos = B.gold_fish_registered(self.gold, self.crest, i, scale=lerp(1.12, 1.0, t), rot=rot * (1 - t))
                pos = (pos[0], pos[1] + round(dy * (1 - t)))
                B.cast_shadow(base, layer, pos, dy=10, blur=12, alpha=int(35 * (1 - t)))
                base.alpha_composite(layer, pos)
            im = base
            extra = "AE: lake → white, fish rise to crest positions, type crosses white → black"
        elif f < 355:
            keep = tuple(1 - ease((f - (336 + 3 * (2 - i))) / 12) for i in range(3))   # R first, then C, then L
            im = self.crest_frame(1 - ease((f - 343) / 12), keep, fish_from_top=True)
            extra = "AE: gold drains head-down R/C/L; type fades"
        else:
            im = self.art.copy()
        im = im.convert("RGBA")
        if burnin:
            burn(im, f, shot_name(f), extra)
        return im.convert("RGB")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    burnin = "--no-burnin" not in sys.argv
    pull, out = (Path(a).expanduser().resolve() for a in args[:2])
    frames = out / "frames"; frames.mkdir(parents=True, exist_ok=True)
    S = Scene(pull, out)
    for f in range(TOTAL):
        S.render(f, burnin).save(frames / f"pa_{f:04d}.png", compress_level=1)
        if f % 48 == 0:
            print(f"frame {f}/{TOTAL}  {shot_name(f)}", flush=True)
    a = S.render(0, False).tobytes(); b = S.render(TOTAL - 1, False).tobytes()
    print("loop frame identical:", a == b)
    mp4 = out / "passalacqua_animatic_v0.1.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(frames / "pa_%04d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium", "-movflags", "+faststart", str(mp4)], check=True)
    print("wrote", mp4)


if __name__ == "__main__":
    main()
