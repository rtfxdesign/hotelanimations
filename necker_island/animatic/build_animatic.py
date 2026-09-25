#!/usr/bin/env python3
"""Necker Island animatic v0.1 — 372 frames, 15.5 s at 24 fps, 16:9 HD, loops on frame 0.

Beats from theria_hotel_animations_timing_v1.md §7 as boarded in necker_island/storyboard/STORYBOARD.md.
Generated material (generation_kit/output/07_necker_island/):
  NE-1 takeoff  ne_1_t1.mp4   (Kling 3 from the flamingo-on-white still)
  NE-2 plate    ne_2_t1.png   (kite plate with a generic rider)
  NE-3 crossing ne_3_t1.mp4   (Kling 3 from NE-2)
  NE-4a/b       ne_4a_t1.png, ne_4b_t1.png (lemurs playing tennis, two poses)
  NE-5 landing  ne_5_t1.mp4   (Kling 3, white frame -> flamingo still)
Plates: generation_kit/07_necker_island/ne_shot1_START_flamingo_on_white.png (the cut-out at its S1 placement),
        ne_shot3_aerial_16x9.png (the 3/4 aerial, 3840x2160).

    python3 necker_island/animatic/build_animatic.py PULL_ROOT OUT_DIR [--no-burnin]

Shot plan:
  S1 hold       f0-58     flamingo still (loop frame)
  S2 takeoff    f58-110   NE-1 f0-120 retimed 2.3x, 4 f dissolve in
  S3 pull-back  f110-178  aerial 2.2x -> 1.0x, white 85 % -> 0 by f140, flamingo small crossing right
  S4 kite       f178-245  NE-3 f0-120 retimed 1.8x (hard cut)
  S5 tennis     f245-312  NE-4a/b alternating at the hits (f259, f278, f298), push-in 1.0 -> 1.15
  S6 whiteout   f312-336  aerial 1.0x -> 0.55x, white 0 -> 100
  S7 landing    f336-372  NE-5 f20-100 retimed 2.2x, last 6 f dissolve to the still
  loop          f371 = f0
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
W, H, FPS, TOTAL = 1920, 1080, 24, 372
GEN = ROOT / "generation_kit" / "output" / "07_necker_island"
KIT = ROOT / "generation_kit" / "07_necker_island"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SHOTS = [("S1 hold", 0, 58), ("S2 takeoff (Kling NE-1, 2.3x)", 58, 110), ("S3 pull-back (AE)", 110, 178), ("S4 kite (Kling NE-3, 1.8x)", 178, 245),
         ("S5 tennis (NE-4a/b stills, AE ball)", 245, 312), ("S6 whiteout (AE)", 312, 336), ("S7 landing (Kling NE-5, 2.2x)", 336, 372)]
HITS = (259, 278, 298)


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
        for name in ("ne_1_t1", "ne_3_t1", "ne_5_t1"):
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
    txt = f"NECKER ISLAND · ANIMATIC v0.1 · {shot} · f{f:03d} · {f / FPS:05.2f}s"
    tw = d.textlength(txt, font=ff)
    d.rectangle((16, 16, 16 + tw + 20, 52), fill=(0, 0, 0, 255)); d.text((26, 22), txt, font=ff, fill=(255, 176, 32))
    if extra:
        fe = font(26); tw = d.textlength(extra, font=fe)
        d.rectangle((W // 2 - tw // 2 - 20, H - 88, W // 2 + tw // 2 + 20, H - 40), fill=(0, 0, 0, 255)); d.text((W // 2 - tw // 2, H - 80), extra, font=fe, fill=(255, 176, 32))


def shot_name(f):
    return next(n for n, a, b in SHOTS if a <= f < b)


class Scene:
    def __init__(self, pull: Path, out: Path):
        self.C = Clips(out)
        self.still = fit(Image.open(KIT / "ne_shot1_START_flamingo_on_white.png"))
        self.aerial = Image.open(KIT / "ne_shot3_aerial_16x9.png").convert("RGBA")
        self.bird = Image.open(KIT / "ne_ref_flamingo_cutout_alpha.png").convert("RGBA")
        self.bird = self.bird.crop(self.bird.getchannel("A").getbbox())
        k = 0.08 * H / self.bird.height; self.bird_small = self.bird.resize((round(self.bird.width * k), round(self.bird.height * k)), Image.LANCZOS)
        self.court_a = fit(Image.open(GEN / "ne_4a_t1.png")); self.court_b = fit(Image.open(GEN / "ne_4b_t1.png"))
        self.white = Image.new("RGBA", (W, H), (255, 255, 255, 255))
        self._az = {}

    def aerial_at(self, z):
        key = round(z, 3)
        if key not in self._az:
            im = self.aerial.resize((round(W * z), round(H * z)), Image.LANCZOS)
            if z >= 1:
                im = im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width - W) // 2 + W, (im.height - H) // 2 + H))
            else:                                   # smaller than frame: centred on white
                canvas = self.white.copy(); canvas.alpha_composite(im, ((W - im.width) // 2, (H - im.height) // 2)); im = canvas
            self._az = {key: im}
        return self._az[key]

    def court(self, f, which):
        z = lerp(1.0, 1.15, ease((f - 245) / 67)); src = self.court_a if which == "a" else self.court_b
        im = src.resize((round(W * z), round(H * z)), Image.LANCZOS)
        return im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width - W) // 2 + W, (im.height - H) // 2 + H))

    def render(self, f, burnin=True):
        C = self.C; extra = None
        if f < 58:
            im = self.still.copy()
        elif f < 110:
            im = C.frame("ne_1_t1", (f - 58) * (C.n["ne_1_t1"] - 1) / 51).copy()
            if f < 62:
                im = Image.blend(self.still, im, ease((f - 58) / 4))
            extra = "Kling NE-1 retimed 2.3x. AE: key or lift the grey background to white"
        elif f < 178:
            t = ease((f - 110) / 68)
            z = lerp(2.2, 1.0, t)
            im = self.aerial_at(z).copy()
            wt = 0.85 * (1 - ease((f - 110) / 30))
            if wt > 0:
                im = Image.blend(im, self.white, wt)
            bx = round(lerp(1250, 1560, t)); by = round(lerp(330, 250, t))
            im.alpha_composite(self.bird_small, (bx, by))
            extra = "AE: plate 2.2x → 1.0x, white ramp off by f140; flamingo 8 % crossing right (cut-out stand-in)"
        elif f < 245:
            im = C.frame("ne_3_t1", (f - 178) * (C.n["ne_3_t1"] - 1) / 66).copy()
            extra = "Kling NE-3 retimed 1.8x: rider L→R, flamingo R→L"
        elif f < 312:
            which = "a"
            for h in HITS:
                if f >= h:
                    which = "b" if which == "a" else "a"
            im = self.court(f, which)
            for h in HITS:
                if h <= f < h + 4:
                    prev = "a" if which == "b" else "b"
                    im = Image.blend(self.court(f, prev), im, ease((f - h) / 4))
            extra = "NE-4a/b stills alternate at the hits (10.8 / 11.6 / 12.4 s), push-in 1.15x. AE: ball + hit marks"
        elif f < 336:
            t = ease((f - 312) / 24)
            im = Image.blend(self.aerial_at(lerp(1.0, 0.55, t)), self.white, t)
            if t < 1:
                bx = round(lerp(1560, 1400, t)); by = round(lerp(250, 330, t))
                im.alpha_composite(self.bird_small, (bx, by))
            extra = "AE: plate 1.0x → 0.55x under a white ramp; Virgin mark lower-right f318"
        else:
            i = 20 + (f - 336) * 80 / 35
            im = C.frame("ne_5_t1", i).copy()
            if f >= 366:
                im = Image.blend(im, self.still, ease((f - 366) / 5))
            extra = "Kling NE-5 f20-100 retimed 2.2x; last 6 f dissolve to the S1 still"
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
        S.render(f, burnin).save(frames / f"ne_{f:04d}.png", compress_level=1)
        if f % 48 == 0:
            print(f"frame {f}/{TOTAL}  {shot_name(f)}", flush=True)
    a = S.render(0, False).tobytes(); b = S.render(TOTAL - 1, False).tobytes()
    print("loop frame identical:", a == b)
    mp4 = out / "necker_island_animatic_v0.1.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(frames / "ne_%04d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium", "-movflags", "+faststart", str(mp4)], check=True)
    print("wrote", mp4)


if __name__ == "__main__":
    main()
