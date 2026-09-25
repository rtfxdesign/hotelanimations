#!/usr/bin/env python3
"""North Island animatic v0.1 — 312 frames, 13.0 s at 24 fps, one 16:9 HD master, loops on frame 0.

Timing from theria_hotel_animations_timing_v1.md §5 (as boarded in north_island/storyboard/STORYBOARD.md).
Generated clips from Sol rounds 2-3 (generation_kit/output/05_north_island/):
  NI-2 swim   ni_2_t1.mp4  (Kling 3 from ni_1_comp.png, the 16:9 extension of northisland.png)
  NI-3 crawl  ni_3_t1.mp4  (Kling 3 from the board's 5-turtle beach comp)
  NI-4 return ni_4_t1.mp4  (Kling 3, NI-3 last frame -> NI-3 first frame)

    python3 north_island/animatic/build_animatic.py PULL_ROOT OUT_DIR [--no-burnin]

Shot plan (frame = animatic frame):
  S1 hold      f0-53    white lock-up plate, still (specular sweep is AE)
  S2 flood     f53-96   luma wipe bottom->top f53-82 white plate -> water plate (= NI-2 frame 0), hold
  S3 swim      f96-168  NI-2 f0-71 at 1:1
  S4a landfall f168-197 dissolve NI-2 f71 -> NI-3 f92 (the sand beat uses the tail of NI-3)
  S4b sand     f197-226 NI-3 f92-120 at 1:1
  S5 return    f226-274 NI-4 f0-120 retimed into 48 (2.5x); last 16 f dissolve to the water plate
  S6a whiteout f274-298 luma wipe top->bottom water plate -> white plate
  S6b loop     f298-312 white plate = frame 0
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS, TOTAL = 1920, 1080, 24, 312
ROOT = Path(__file__).resolve().parents[2]
GEN = ROOT / "generation_kit" / "output" / "05_north_island"
WHITE = "b261916d-7215-4f97-8607-d091aabe911a.png"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SHOTS = [("S1 hold", 0, 53), ("S2 flood (AE wipe)", 53, 96), ("S3 swim (Kling NI-2)", 96, 168),
         ("S4a landfall (dissolve)", 168, 197), ("S4b sand (Kling NI-3)", 197, 226),
         ("S5 return (Kling NI-4, 2.5x)", 226, 274), ("S6a whiteout (AE wipe)", 274, 298), ("S6b loop", 298, 312)]


def ease(t):
    t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)


def font(size):
    return ImageFont.truetype(FONT, size)


def fit_height(im, fill=(255, 255, 255)):
    s = H / im.height
    im = im.resize((round(im.width * s), H), Image.LANCZOS)
    out = Image.new("RGB", (W, H), fill); out.paste(im, ((W - im.width) // 2, 0)); return out


def fit(im):
    return im.convert("RGB").resize((W, H), Image.LANCZOS) if im.size != (W, H) else im.convert("RGB")


class Clips:
    def __init__(self, out: Path):
        self.dir = out / "_clips"; self.cache = {}
        for name in ("ni_2_t1", "ni_3_t1", "ni_4_t1"):
            d = self.dir / name
            if not d.exists() or not any(d.glob("*.png")):
                d.mkdir(parents=True, exist_ok=True)
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(GEN / f"{name}.mp4"), "-vsync", "0", str(d / "f%03d.png")], check=True)
        self.n = {name: len(list((self.dir / name).glob("*.png"))) for name in ("ni_2_t1", "ni_3_t1", "ni_4_t1")}

    def frame(self, name, i):
        i = max(0, min(self.n[name] - 1, i))
        key = (name, i)
        if key not in self.cache:
            self.cache[key] = fit(Image.open(self.dir / name / f"f{i + 1:03d}.png"))
        return self.cache[key]


def wipe(a, b, t, top_down=False, soft=90):
    """Luma wipe a -> b with a soft edge; t=0 all a, t=1 all b. Bottom->top by default."""
    m = Image.new("L", (1, H))
    px = m.load()
    edge = (1 - t) * (H + soft) - soft / 2 if not top_down else t * (H + soft) - soft / 2
    for y in range(H):
        d = (y - edge) if not top_down else (edge - y)
        px[0, y] = int(255 * max(0.0, min(1.0, (d + soft / 2) / soft)))
    return Image.composite(b, a, m.resize((W, H)))


def burn(im, f, shot, extra=None):
    d = ImageDraw.Draw(im); ff = font(22)
    txt = f"NORTH ISLAND · ANIMATIC v0.1 · {shot} · f{f:03d} · {f / FPS:05.2f}s"
    tw = d.textlength(txt, font=ff)
    d.rectangle((16, 16, 16 + tw + 20, 52), fill=(0, 0, 0)); d.text((26, 22), txt, font=ff, fill=(255, 176, 32))
    if extra:
        fe = font(26); tw = d.textlength(extra, font=fe)
        d.rectangle((W // 2 - tw // 2 - 20, H - 88, W // 2 + tw // 2 + 20, H - 40), fill=(0, 0, 0)); d.text((W // 2 - tw // 2, H - 80), extra, font=fe, fill=(255, 176, 32))


def shot_name(f):
    return next(n for n, a, b in SHOTS if a <= f < b)


def render(f, P, C, burnin):
    white, water = P
    extra = None
    if f < 53:
        im = white.copy()
    elif f < 96:
        im = wipe(white, water, ease((f - 53) / 29)) if f < 82 else water.copy()
        extra = "AE: wipe bottom→top; turtles + wordmark held as one cut-out layer over both plates"
    elif f < 168:
        im = C.frame("ni_2_t1", f - 96).copy()
        extra = "Kling NI-2, 1:1; wordmark = AE layer over the plate (baked lettering drifts)"
    elif f < 197:
        t = ease((f - 168) / 29)
        im = Image.blend(C.frame("ni_2_t1", 71), C.frame("ni_3_t1", 92), t)
        extra = "AE: colour ramp turquoise→sand under the dissolve"
    elif f < 226:
        im = C.frame("ni_3_t1", 92 + (f - 197)).copy()
        extra = "Kling NI-3 f92-120, 1:1"
    elif f < 274:
        i = round((f - 226) * (C.n["ni_4_t1"] - 1) / 47)
        im = C.frame("ni_4_t1", i)
        if f >= 258:
            im = Image.blend(im, water, ease((f - 258) / 16))
        else:
            im = im.copy()
        extra = "Kling NI-4 retimed 2.5x; last 16 f dissolve to the water plate (AE: sand→turquoise ramp)"
    elif f < 298:
        im = wipe(water, white, ease((f - 274) / 24), top_down=True)
        extra = "AE: wipe top→bottom; turtles settle to lock-up positions"
    else:
        im = white.copy()
    if burnin:
        burn(im, f, shot_name(f), extra)
    return im


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    burnin = "--no-burnin" not in sys.argv
    pull, out = (Path(a).expanduser().resolve() for a in args[:2])
    frames = out / "frames"; frames.mkdir(parents=True, exist_ok=True)
    C = Clips(out)
    white = fit_height(Image.open(pull / "North Island" / WHITE).convert("RGB"))
    water = C.frame("ni_2_t1", 0)          # = ni_1_comp fitted, exactly what the swim starts from
    P = (white, water)
    for f in range(TOTAL):
        render(f, P, C, burnin).save(frames / f"ni_{f:04d}.png", compress_level=1)
        if f % 48 == 0:
            print(f"frame {f}/{TOTAL}  {shot_name(f)}", flush=True)
    a = render(0, P, C, False).tobytes(); b = render(TOTAL - 1, P, C, False).tobytes()
    print("loop frame identical:", a == b)
    mp4 = out / "north_island_animatic_v0.1.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(frames / "ni_%04d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium", "-movflags", "+faststart", str(mp4)], check=True)
    print("wrote", mp4)


if __name__ == "__main__":
    main()
