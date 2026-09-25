#!/usr/bin/env python3
"""22 Club animatic v0.1 — 290 frames, 12.08 s at 24 fps, 16:9 HD. Loop point f278 = f0; black tail f279-290 (beat 25 cut).

Beats from theria_hotel_animations_timing_v1.md §8 at 124 bpm as boarded in club22/storyboard/STORYBOARD.md.
Reuses the storyboard builder's Mark (vector raster, parts, hinge) and its schematic deck and spotlight.
The decks and vinyl are schematic here; the Flux stills (cl_1_t2 platter, cl_2_t1 vinyl, cl_3_t1 beam) are the
production elements and ride in the handoff assets. Audio: Sol's 124 bpm rhythm bed (placeholder).

    python3 club22/animatic/build_animatic.py PULL_ROOT OUT_DIR [--no-burnin]

Shot plan:
  B1 hold      f0-46     the mark, brand red on black (loop frame)
  B2 flip      f46-105   both 2s rotate back 90° about their base line, left first, right 8 f behind, drifting onto the platter marks
  B3 decks     f105-151  decks build on the flat digits over 24 f; records spin from f130
  B4 spot      f151-197  hard cone from top-left, hits the left deck f158, sweeps across both by f180
  B5 flipback  f197-255  decks strip back f197-216; both digits rise together f216-235; spot lifts by f255
  B6 return    f255-279  the mark; f278 = f0; hard cut to black f279-290
"""
from __future__ import annotations

import math
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("club22_build_frames", ROOT / "club22" / "storyboard" / "build_frames.py")
B = _ilu.module_from_spec(_spec); _spec.loader.exec_module(B)   # the storyboard builder, under its own module name

W, H, FPS, TOTAL, LOOP_AT = 1920, 1080, 24, 290, 279
GEN = ROOT / "generation_kit" / "output" / "08_club22"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SHOTS = [("B1 hold", 0, 46), ("B2 flip (AE 3D)", 46, 105), ("B3 decks (AE)", 105, 151), ("B4 spotlight (AE)", 151, 197),
         ("B5 flip back (AE)", 197, 255), ("B6 return", 255, 279), ("black tail (beat 25 cut)", 279, 290)]


def ease(t):
    t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)


def overshoot(t, amount=0.08):
    """Ease with a small overshoot and settle."""
    t = max(0.0, min(1.0, t))
    return 1 + amount * math.sin(math.pi * t) * (1 - t) if t > 0.6 else ease(t / 0.6) * (1 + amount * ease(t / 0.6) * 0.0)


def lerp(a, b, t):
    return a + (b - a) * t


def font(size):
    return ImageFont.truetype(FONT, size)


def burn(im, f, shot, extra=None):
    d = ImageDraw.Draw(im); ff = font(22)
    txt = f"22 CLUB · ANIMATIC v0.1 · {shot} · f{f:03d} · {f / FPS:05.2f}s · beat {1 + f / FPS * 124 / 60:.1f}"
    tw = d.textlength(txt, font=ff)
    d.rectangle((16, 16, 16 + tw + 20, 52), fill=(0, 0, 0, 255)); d.text((26, 22), txt, font=ff, fill=(255, 176, 32))
    if extra:
        fe = font(26); tw = d.textlength(extra, font=fe)
        d.rectangle((W // 2 - tw // 2 - 20, H - 88, W // 2 + tw // 2 + 20, H - 40), fill=(0, 0, 0, 255)); d.text((W // 2 - tw // 2, H - 80), extra, font=fe, fill=(255, 176, 32))


def shot_name(f):
    return next(n for n, a, b in SHOTS if a <= f < b)


class Scene:
    def __init__(self, out: Path):
        self.mark = B.Mark(B.MARK_PATH)
        self.base = self.mark.base_y
        self.lcx, self.rcx = B.CX - B.PLATTER_DX, B.CX + B.PLATTER_DX
        self.dl, self.dr = self.mark.digit_dx("L"), self.mark.digit_dx("R")
        el = out / "_elements"; el.mkdir(parents=True, exist_ok=True)
        for name, box in (("cl_mark_2L", B.SRC_2L), ("cl_mark_2R", B.SRC_2R), ("cl_mark_club", B.SRC_CLUB), ("cl_mark_whole", B.SRC_INK)):
            im, pos = self.mark.part(box); im.save(el / f"{name}.png")
            print(f"{name}: {im.size} at {pos}")
        self.hold = B.paste_mark(B.blank(), self.mark)

    def digits(self, f, tl, tr):
        """tl, tr in 0..1 = how far each digit has rotated back (0 upright, 1 flat)."""
        canvas = B.blank()
        for box, t, dx in ((B.SRC_2L, tl, self.dl), (B.SRC_2R, tr, self.dr)):
            sq = lerp(1.0, B.ELEV, t)
            self.mark.paste(canvas, box, dx=round(dx * t), squash=sq)
        self.mark.paste(canvas, B.SRC_CLUB)
        return canvas

    def render(self, f, burnin=True):
        extra = None
        if f < 46 or (255 <= f < LOOP_AT):
            im = self.hold.copy()
        elif f < 105:
            tl = ease((f - 46) / 19); tr = ease((f - 54) / 19)
            im = self.digits(f, tl, tr)
            extra = "AE: 3D layers rotate 90° back about the hinge (lowest ink row), camera 30° up; left first, right +8 f"
        elif f < 151:
            t = ease((f - 105) / 24)
            im = self.digits(f, 1.0, 1.0)
            decks = B.blank()
            B.draw_deck(decks, self.lcx, self.base, spin=False); B.draw_deck(decks, self.rcx, self.base, spin=False)
            self.mark.paste(decks, B.SRC_CLUB)
            im = Image.blend(im, decks, t)
            if f >= 130:
                ang = (f - 130) * 360 / 43
                d = ImageDraw.Draw(im)
                for cx in (self.lcx, self.rcx):
                    l, tt, r, b = B.platter_box(cx, self.base, k=0.9)
                    pcx, pcy, rx, ry = (l + r) / 2, (tt + b) / 2, (r - l) / 2, (b - tt) / 2
                    a = math.radians(ang)
                    d.line([(pcx, pcy), (pcx + rx * 0.95 * math.cos(a), pcy + ry * 0.95 * math.sin(a))], fill=(60, 60, 64, 255), width=2)
            extra = "AE: platter, vinyl, tonearm build on each digit's footprint (Flux stills as elements); 33⅓ rpm = 43 f/rev from f130"
        elif f < 197:
            im = B.blank()
            B.draw_deck(im, self.lcx, self.base, lit=0.55, spin=False); B.draw_deck(im, self.rcx, self.base, lit=0.55, spin=False)
            s = ease((f - 151) / 7)
            reach = ease((f - 158) / 22)
            pool = (self.lcx - B.PLATTER_D * 0.75, self.base - B.PLATTER_D * 0.62, lerp(self.lcx, self.rcx, reach) + B.PLATTER_D * 0.75, self.base + 70)
            B.spotlight(im, (-80, -160), pool, strength=s, dust=True, seed=f)
            lit = B.blank(); B.draw_deck(lit, self.lcx, self.base, lit=1.0, spin=False); B.draw_deck(lit, self.rcx, self.base, lit=1.0, spin=False, opacity=reach)
            lit.putalpha(lit.getchannel("A").point(lambda v: int(v * 0.55 * s)))
            im.alpha_composite(lit)
            self.mark.paste(im, B.SRC_CLUB, opacity=lerp(1.0, 0.65, s))
            extra = "AE: cone geometry + noise dust; decks 55 % outside the pool, full inside; vinyl flashes once per rev"
        elif f < 255:
            t_strip = ease((f - 197) / 19)
            t_up = ease((f - 216) / 19)
            im = self.digits(f, 1 - t_up, 1 - t_up)
            if t_strip < 1:
                decks = B.blank(); B.draw_deck(decks, self.lcx, self.base, spin=False); B.draw_deck(decks, self.rcx, self.base, spin=False); self.mark.paste(decks, B.SRC_CLUB)
                im = Image.blend(decks, im, t_strip)
            s = 0.45 * (1 - ease((f - 197) / 58))
            if s > 0.01:
                pool = (B.CX - B.PLATTER_D * 0.9, self.base - B.PLATTER_D * 0.9, B.CX + B.PLATTER_D * 0.9, self.base - 40)
                B.spotlight(im, (-80, -160), pool, strength=s, dust=False)
            extra = "AE: decks strip back f197-216, digits rise together f216-235, spot lifts by f255"
        else:
            im = B.blank()
        im = im.convert("RGBA")
        if burnin:
            burn(im, f, shot_name(f), extra)
        return im.convert("RGB")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    burnin = "--no-burnin" not in sys.argv
    pull, out = (Path(a).expanduser().resolve() for a in args[:2])
    frames = out / "frames"; frames.mkdir(parents=True, exist_ok=True)
    S = Scene(out)
    resume = "--resume" in sys.argv
    for f in range(TOTAL):
        if resume and (frames / f"cl_{f:04d}.png").exists():
            continue
        S.render(f, burnin).save(frames / f"cl_{f:04d}.png", compress_level=1)
        if f % 48 == 0:
            print(f"frame {f}/{TOTAL}  {shot_name(f)}", flush=True)
    a = S.render(0, False).tobytes(); b = S.render(LOOP_AT - 1, False).tobytes()
    print(f"loop frame f{LOOP_AT - 1} identical to f0:", a == b)
    mp4 = out / "club22_animatic_v0.1.mp4"
    bed = GEN / "club22_rhythm_124bpm.wav"
    cmd = ["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(frames / "cl_%04d.png")]
    if bed.exists():
        cmd += ["-i", str(bed), "-filter_complex", f"[1:a]atrim=0:{TOTAL / FPS},volume=-6dB[a]", "-map", "0:v", "-map", "[a]", "-c:a", "aac", "-b:a", "160k"]
    cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium", "-movflags", "+faststart", "-shortest", str(mp4)]
    subprocess.run(cmd, check=True)
    print("wrote", mp4)


if __name__ == "__main__":
    main()
