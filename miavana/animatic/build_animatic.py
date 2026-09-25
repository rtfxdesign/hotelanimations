#!/usr/bin/env python3
"""Miavana animatic v0.1 — 288 frames, 12.0 s at 24 fps, 16:9 HD, loops on frame 0.

Beats from theria_hotel_animations_timing_v1.md §6 as boarded in miavana/storyboard/STORYBOARD.md.
Reuses the storyboard builder for the lock-up (vector MIAVANA + PSD layers + PSD lemurs).
Generated material (generation_kit/output/06_miavana/):
  MI-1a mango still      mi_1a_t1.png  (keyed from white here)
  MI-2 wind-up clip      mi_2_t1.mp4   (Kling 3 from the lock-up)
  MI-3 catch clip        mi_3_t1.mp4   (Kling 3 from the lock-up)
  MI-4 palms plate       mi_4_comp_5k.png (MI-4b lemurs keyed and comped on the 4988 px resort plate)

    python3 miavana/animatic/build_animatic.py PULL_ROOT OUT_DIR [--no-burnin]

Shot plan:
  B1 hold      f0-58     lock-up (MI-2 frame 0) with the MI-1a mango in the hanging lemur's hands (loop frame)
  B2a wind-up  f58-72    MI-2 f0-120 retimed 8.6x (the clip is far longer than the beat)
  B2b/c throw+catch f72-101  6 f dissolve to MI-3, then MI-3 f44-109 retimed 2.2x (Kling's mango flies in and is caught)
  B3 reveal    f101-149  dissolve lock-up -> palms plate
  B4 palms     f149-230  palms plate, 6 % drift right-to-left
  B5 return    f230-274  dissolve palms plate -> lock-up (loop composite)
  B6 hold      f274-288  = frame 0
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "miavana" / "storyboard"))
import build_frames as B  # noqa: E402

W, H, FPS, TOTAL = 1920, 1080, 24, 288
GEN = ROOT / "generation_kit" / "output" / "06_miavana"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SHOTS = [("B1 hold", 0, 58), ("B2a wind-up (Kling MI-2, 8.6x)", 58, 72), ("B2b/c throw + catch (Kling MI-3, 2.2x)", 72, 101),
         ("B3 reveal (AE dissolve)", 101, 149), ("B4 palms (drift)", 149, 230), ("B5 return (AE dissolve)", 230, 274), ("B6 hold / loop", 274, 288)]


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
        for name in ("mi_2_t1", "mi_3_t1"):
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


def key_white(im: Image.Image) -> Image.Image:
    """Mango on white -> RGBA cut-out (soft luma key on the white field)."""
    a = np.array(im.convert("RGB")).astype(np.float32)
    lum = a.min(axis=2)
    alpha = np.clip((240 - lum) / 30, 0, 1)
    out = np.dstack([a, alpha * 255]).astype(np.uint8)
    o = Image.fromarray(out, "RGBA"); return o.crop(o.getchannel("A").getbbox())


def burn(im, f, shot, extra=None):
    d = ImageDraw.Draw(im); ff = font(22)
    txt = f"MIAVANA · ANIMATIC v0.1 · {shot} · f{f:03d} · {f / FPS:05.2f}s"
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
        self.mango = key_white(Image.open(GEN / "mi_1a_t1.png"))
        release = B.hd(B.RIGHT_HANDS)
        self.mango_pos = (release[0] + 6, release[1] - 6)
        base = self.C.frame("mi_2_t1", 0).copy()
        B.paste_mango(base, self.mango, self.mango_pos, width=B.MANGO_W)
        self.loop = base                                       # frame 0 = frame 287
        self.plate = Image.open(GEN / "mi_4_comp_5k.png").convert("RGBA")
        self.zoom = 1.06
        zw, zh = round(W * self.zoom), round(H * self.zoom)
        self.plate_z = self.plate.resize((zw, zh), Image.LANCZOS)
        self.plate_fit = fit(self.plate)

    def palms(self, t):
        """6 % drift right-to-left over the beat: the zoomed plate slides from x=0 to x=-(zw-W)."""
        zw = self.plate_z.width; x = -round((zw - W) * t)
        return self.plate_z.crop((-x, (self.plate_z.height - H) // 2, -x + W, (self.plate_z.height - H) // 2 + H))

    def render(self, f, burnin=True):
        C = self.C; extra = None
        if f < 58:
            im = self.loop.copy()
        elif f < 72:
            im = C.frame("mi_2_t1", (f - 58) * (C.n["mi_2_t1"] - 1) / 13).copy()
            extra = "Kling MI-2 retimed 8.6x (121 f into 14): wind-up. AE: 12-frame anticipation hold"
        elif f < 101:
            i = 44 + (f - 72) * (109 - 44) / 28
            im = C.frame("mi_3_t1", i).copy()
            if f < 78:
                im = Image.blend(C.frame("mi_2_t1", C.n["mi_2_t1"] - 1), im, ease((f - 72) / 6))
            extra = "Kling MI-3 f44-109 retimed 2.2x: mango in from the right, seated lemur catches. AE: 2D arc from the hanging lemur instead"
        elif f < 149:
            t = ease((f - 101) / 48)
            im = Image.blend(C.frame("mi_3_t1", 109), self.palms(0.0), t)
            extra = "AE: cross-dissolve; letters under the lemurs resolve into the palms"
        elif f < 230:
            im = self.palms(ease((f - 149) / 81))
            extra = "palms plate (MI-4b lemurs keyed onto the 5k aerial), 6 % drift R→L. AE: second toss, mango 2D"
        elif f < 274:
            t = ease((f - 230) / 44)
            im = Image.blend(self.palms(1.0), self.loop, t)
            extra = "AE: reverse dissolve back to the lock-up"
        else:
            im = self.loop.copy()
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
    S.mango.save(out / "mi_mango_cutout_alpha.png")
    for f in range(TOTAL):
        S.render(f, burnin).save(frames / f"mi_{f:04d}.png", compress_level=1)
        if f % 48 == 0:
            print(f"frame {f}/{TOTAL}  {shot_name(f)}", flush=True)
    a = S.render(0, False).tobytes(); b = S.render(TOTAL - 1, False).tobytes()
    print("loop frame identical:", a == b)
    mp4 = out / "miavana_animatic_v0.1.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(frames / "mi_%04d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium", "-movflags", "+faststart", str(mp4)], check=True)
    print("wrote", mp4)


if __name__ == "__main__":
    main()
