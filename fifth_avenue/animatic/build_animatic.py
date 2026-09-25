#!/usr/bin/env python3
"""The Fifth Avenue Hotel animatic v0.1 — 312 frames, 13.0 s at 24 fps, 16:9 HD, loops on frame 0.

Beats from theria_hotel_animations_timing_v1.md §2 as boarded in fifth_avenue/storyboard/STORYBOARD.md.
Reuses the storyboard builder's plate maths (PSD layers, hero positions, lockup, push-whip).
Generated clip: generation_kit/output/02_fifth_avenue/fa_1_t1.mp4 (Kling 3 from the walk start frame).

    python3 fifth_avenue/animatic/build_animatic.py PULL_ROOT OUT_DIR [--no-burnin]

Shot plan:
  B1 hold        f0-58     tortoise alone on white, up-left (loop frame)
  B2 lockup      f58-101   gold lockup wipes on L->R f58-82, holds
  B3 lockup out  f101-130  lockup 100->0 over f101-118 with +3 % scale
  B4 reveal      f130-173  white -> park (couple, no tortoise); tortoise slides to its plate position f130-168; leash f165-173
  B5 walk        f173-274  Kling FA-1 take 1, source f0-25 over 101 f (4x slow, frame-held); NLE does the optical-flow retime
  B6 whip        f274-282  park + couple push out frame-left with motion blur; tortoise stays
  B6b white      f282-288  tortoise alone at its plate position
  B7 return      f288-306  tortoise glides back up-left
  B8 loop        f306-312  = frame 0
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "fifth_avenue" / "storyboard"))
import build_frames as B  # noqa: E402

W, H, FPS, TOTAL = 1920, 1080, 24, 312
GEN = ROOT / "generation_kit" / "output" / "02_fifth_avenue"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SLOW = 4          # walk clip slow-down in the animatic
SHOTS = [("B1 hold", 0, 58), ("B2 lockup (AE wipe)", 58, 101), ("B3 lockup out (AE)", 101, 130), ("B4 reveal (AE dissolve + slide)", 130, 173),
         ("B5 walk (Kling FA-1, 4x slow)", 173, 274), ("B6 whip (AE)", 274, 282), ("B6b white", 282, 288), ("B7 return (AE)", 288, 306), ("B8 loop", 306, 312)]


def font(size):
    return ImageFont.truetype(FONT, size)


def fit(im):
    return im.convert("RGBA").resize((W, H), Image.LANCZOS) if im.size != (W, H) else im.convert("RGBA")


def lerpf(a, b, t):
    return a + (b - a) * t


class Clip:
    def __init__(self, out: Path):
        self.dir = out / "_clips" / "fa_1_t1"; self.cache = {}
        if not self.dir.exists() or not any(self.dir.glob("*.png")):
            self.dir.mkdir(parents=True, exist_ok=True)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(GEN / "fa_1_t1.mp4"), "-vsync", "0", str(self.dir / "f%03d.png")], check=True)
        self.n = len(list(self.dir.glob("*.png")))

    def frame(self, i):
        i = max(0, min(self.n - 1, int(round(i))))
        if i not in self.cache:
            self.cache[i] = fit(Image.open(self.dir / f"f{i + 1:03d}.png"))
        return self.cache[i]


def push_out(im, shift, blur=160, samples=16):
    """Push-whip with horizontal motion blur; shifts clamped to the frame (the storyboard helper is not)."""
    src = np.asarray(im.convert("RGB")).astype(np.float32)
    acc = np.zeros_like(src)
    for i in range(samples):
        s = int(max(0, min(W, shift + round((i / (samples - 1) - 0.5) * blur))))
        canvas = np.full_like(src, 255.0)
        if s < W:
            canvas[:, :W - s] = src[:, s:]
        acc += canvas
    return Image.fromarray((acc / samples).astype(np.uint8), "RGB").convert("RGBA")


def wipe_lr(layer, t, soft=60):
    """Reveal a layer left -> right: alpha multiplied by a soft horizontal ramp at fraction t."""
    m = Image.new("L", (layer.width, 1)); px = m.load()
    edge = t * (layer.width + soft) - soft
    for x in range(layer.width):
        px[x, 0] = int(255 * max(0.0, min(1.0, (edge + soft - x) / soft)))
    out = layer.copy(); out.putalpha(ImageChops.multiply(out.getchannel("A"), m.resize(layer.size)))
    return out


def burn(im, f, shot, extra=None):
    d = ImageDraw.Draw(im); ff = font(22)
    txt = f"THE FIFTH AVENUE HOTEL · ANIMATIC v0.1 · {shot} · f{f:03d} · {f / FPS:05.2f}s"
    tw = d.textlength(txt, font=ff)
    d.rectangle((16, 16, 16 + tw + 20, 52), fill=(0, 0, 0, 255)); d.text((26, 22), txt, font=ff, fill=(255, 176, 32))
    if extra:
        fe = font(26); tw = d.textlength(extra, font=fe)
        d.rectangle((W // 2 - tw // 2 - 20, H - 88, W // 2 + tw // 2 + 20, H - 40), fill=(0, 0, 0, 255)); d.text((W // 2 - tw // 2, H - 80), extra, font=fe, fill=(255, 176, 32))


def shot_name(f):
    return next(n for n, a, b in SHOTS if a <= f < b)


class Scene:
    def __init__(self, pull: Path, out: Path):
        up = pull / "5th ave hotel NYC" / "upscaled"
        self.lockup = B.alpha_crop(Image.open(up / "Asset 1@2x.png").convert("RGBA"))
        bg, layers = B.load_plate_layers(up)
        assert bg is not None, "psd-tools is needed for the walkers plate"
        self.park = B.build_plate(bg, layers, include=("woman", "man"))                     # no leash, no tortoise
        self.park_leash = B.build_plate(bg, layers, include=("woman", "man", "leash"))
        self.park_end = B.build_plate(bg, layers, B.WALK_END_DX, include=("woman", "man", "leash"))
        self.hero = B.scale_to_width(layers["turtle"], round(layers["turtle"].width * B.PLATE_S))
        self.pos_hold, self.pos_plate = B.hero_positions(self.hero)
        self.clip = Clip(out)
        self.frame01 = B.paste_hero(B.blank(), self.hero, self.pos_hold)
        self.whip_cache = {}

    def whip(self, f):
        if f not in self.whip_cache:
            t = (f - 274) / 8
            t = t * t if t < 0.25 else t                    # 2 f ease-in
            self.whip_cache[f] = push_out(self.park_end, round(W * min(1.0, t)))
        return self.whip_cache[f]

    def render(self, f, burnin=True):
        extra = None
        if f < 58:
            im = self.frame01.copy()
        elif f < 101:
            im = self.frame01.copy()
            l = B.scale_to_width(self.lockup, B.LOCKUP_W)
            l = wipe_lr(l, min(1.0, (f - 58) / 24))
            im.alpha_composite(l, (B.LOCKUP_CX - l.width // 2, B.LOCKUP_TOP))
            extra = "AE: letterforms wipe on L→R f58-82 behind a gold foil shimmer"
        elif f < 130:
            t = min(1.0, (f - 101) / 17)
            im = B.paste_lockup(self.frame01.copy(), self.lockup, width=round(B.LOCKUP_W * (1 + 0.03 * t)), opacity=1 - t) if t < 1 else self.frame01.copy()
        elif f < 173:
            td = (f - 130) / 43
            ts = B.smoothstep((f - 130) / 38)
            im = Image.blend(B.blank(), self.park, td)
            if f >= 165:
                tl = (f - 165) / 8
                im = Image.blend(im, Image.blend(B.blank(), self.park_leash, td), tl)
            pos = (B.lerp(self.pos_hold[0], self.pos_plate[0], ts), B.lerp(self.pos_hold[1], self.pos_plate[1], ts))
            B.paste_hero(im, self.hero, pos)
            extra = "AE: cross-dissolve white → park; tortoise slides (+147, +335) f130-168; leash fades up f165-173"
        elif f < 274:
            im = self.clip.frame((f - 173) / SLOW).copy()
            extra = f"Kling FA-1 take 1, source f0-25 held {SLOW}x; NLE: figures at 1/6 with optical flow, background 1:1"
        elif f < 282:
            im = self.whip(f).copy()
            B.paste_hero(im, self.hero, self.pos_plate)
            extra = "AE: park pre-comp pushes −1920 px in 8 f with directional blur; tortoise layer stays"
        elif f < 288:
            im = B.paste_hero(B.blank(), self.hero, self.pos_plate)
        elif f < 306:
            tr = B.smoothstep((f - 288) / 18)
            im = B.paste_hero(B.blank(), self.hero, (B.lerp(self.pos_plate[0], self.pos_hold[0], tr), B.lerp(self.pos_plate[1], self.pos_hold[1], tr)))
            extra = "AE: tortoise glides back (−147, −335), ease in-out"
        else:
            im = self.frame01.copy()
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
    print(f"hero {S.hero.size} hold {S.pos_hold} plate {S.pos_plate}; lockup {B.scale_to_width(S.lockup, B.LOCKUP_W).size} at cx {B.LOCKUP_CX} top {B.LOCKUP_TOP}")
    S.park.convert("RGB").save(out / "fa_park_couple_no_tortoise.png")
    S.park_leash.convert("RGB").save(out / "fa_park_couple_leash.png")
    S.hero.save(out / "fa_tortoise_hd_alpha.png")
    resume = "--resume" in sys.argv
    for f in range(TOTAL):
        if resume and (frames / f"fa_{f:04d}.png").exists():
            continue
        S.render(f, burnin).save(frames / f"fa_{f:04d}.png", compress_level=1)
        if f % 48 == 0:
            print(f"frame {f}/{TOTAL}  {shot_name(f)}", flush=True)
    a = S.render(0, False).tobytes(); b = S.render(TOTAL - 1, False).tobytes()
    print("loop frame identical:", a == b)
    mp4 = out / "fifth_avenue_animatic_v0.1.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(frames / "fa_%04d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium", "-movflags", "+faststart", str(mp4)], check=True)
    print("wrote", mp4)


if __name__ == "__main__":
    main()
