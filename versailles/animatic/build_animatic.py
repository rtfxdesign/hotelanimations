#!/usr/bin/env python3
"""Airelles Le Grand Contrôle (Versailles) animatic v0.1 — 374 frames, 15.6 s at 24 fps, 16:9 HD, loops on frame 0.

Beats from theria_hotel_animations_timing_v1.md §4 plus the return beat, as boarded in versailles/storyboard/STORYBOARD.md.
Built the way the production comp is built: the clean salon plate with the cake, chandelier, guillotine and plated slices
as separate keyed layers, so every beat is a layer move, opacity or grade. Elements from Sol round 2
(generation_kit/output/04_versailles/): VE-1 clean salon, VE-2a/2b guillotine blade up/down, VE-3a cake on its table,
VE-3b chandelier, VE-4 plated slices. The wordmark is the approved raster (Versali/images copy.jpg, 2x Lanczos, luma-keyed).

    python3 versailles/animatic/build_animatic.py PULL_ROOT OUT_DIR [--no-burnin]

Shot plan:
  S1 open      f0-53     cake + chandelier on black (loop frame)
  S2 reveal    f53-106   salon reveals radially from the cake behind the held objects
  S3 wordmark  f106-149  AIRELLES lockup fades up on the parquet under the table
  S4 morph     f149-211  chandelier -> guillotine (dissolve stands in for the morph); room down 1.5 stops
  S5 still     f211-235  wordmark out; 12 frames of nothing
  S6 drop      f235-254  pre-shake, blade down over 8 f (2a -> 2b), 3-frame flash, 4 px kick settling
  S7 served    f254-326  cake -> plated slices; light back up 1 stop
  S8 return    f326-374  salon closes to black from the edges; slices -> cake; guillotine -> chandelier; hold = frame 0
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("versailles_build_frames", ROOT / "versailles" / "storyboard" / "build_frames.py")
B = _ilu.module_from_spec(_spec); _spec.loader.exec_module(B)   # the storyboard builder, under its own module name

W, H, FPS, TOTAL = 1920, 1080, 24, 374
GEN = ROOT / "generation_kit" / "output" / "04_versailles"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SHOTS = [("S1 open", 0, 53), ("S2 reveal (AE radial matte)", 53, 106), ("S3 wordmark", 106, 149), ("S4 morph (AE; dissolve stands in)", 149, 211),
         ("S5 still", 211, 235), ("S6 drop (AE)", 235, 254), ("S7 served (AE)", 254, 326), ("S8 return (AE)", 326, 374)]
# layer placement on the 1920x1080 canvas
GUILL_H, GUILL_BOTTOM = 1040, 1050
CAKE_H, CAKE_BOTTOM = 620, 1042
CHAND_H, CHAND_TOP = 300, 8
PLATED_H = 700


def ease(t):
    t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)


def lerp(a, b, t):
    return a + (b - a) * t


def font(size):
    return ImageFont.truetype(FONT, size)


def key_white(im: Image.Image, span=40) -> Image.Image:
    """Object on an off-white field -> RGBA, alpha-cropped. The field level is measured from the border
    so a render whose 'white' is 240 keys as cleanly as one at 255; the soft edge keeps the contact shadow."""
    a = np.array(im.convert("RGB")).astype(np.float32)
    lum = a.min(axis=2)
    border = np.concatenate([lum[:8].ravel(), lum[-8:].ravel(), lum[:, :8].ravel(), lum[:, -8:].ravel()])
    field = float(np.median(border))
    alpha = np.clip((field - 6 - lum) / span, 0, 1)
    out = Image.fromarray(np.dstack([a, alpha * 255]).astype(np.uint8), "RGBA")
    return out.crop(out.getchannel("A").getbbox())


def fit_h(im, h):
    s = h / im.height; return im.resize((round(im.width * s), h), Image.LANCZOS)


def with_op(im, op):
    if op >= 1:
        return im
    im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * op))); return im


def burn(im, f, shot, extra=None):
    d = ImageDraw.Draw(im); ff = font(22)
    txt = f"VERSAILLES · ANIMATIC v0.1 · {shot} · f{f:03d} · {f / FPS:05.2f}s"
    tw = d.textlength(txt, font=ff)
    d.rectangle((16, 16, 16 + tw + 20, 52), fill=(0, 0, 0, 255)); d.text((26, 22), txt, font=ff, fill=(255, 176, 32))
    if extra:
        fe = font(26); tw = d.textlength(extra, font=fe)
        d.rectangle((W // 2 - tw // 2 - 20, H - 88, W // 2 + tw // 2 + 20, H - 40), fill=(0, 0, 0, 255)); d.text((W // 2 - tw // 2, H - 80), extra, font=fe, fill=(255, 176, 32))


def shot_name(f):
    return next(n for n, a, b in SHOTS if a <= f < b)


class Scene:
    def __init__(self, pull: Path, out: Path):
        self.salon = Image.open(GEN / "ve_1_t1.png").convert("RGBA").resize((W, H), Image.LANCZOS)
        self.cake = fit_h(key_white(Image.open(GEN / "ve_3a_t1.png")), CAKE_H)
        self.chand = fit_h(key_white(Image.open(GEN / "ve_3b_t1.png")), CHAND_H)
        self.g_up = fit_h(key_white(Image.open(GEN / "ve_2a_t1.png")), GUILL_H)
        self.g_down = fit_h(key_white(Image.open(GEN / "ve_2b_t1.png")), GUILL_H)
        self.plated = fit_h(key_white(Image.open(GEN / "ve_4_t1.png")), PLATED_H)
        self.mark = B.wordmark_layer(Image.open(pull / "Versali" / "images copy.jpg"))
        self.elements = out / "_elements"; self.elements.mkdir(parents=True, exist_ok=True)
        for n, im in (("ve_cake_table_alpha", self.cake), ("ve_chandelier_alpha", self.chand), ("ve_guillotine_up_alpha", self.g_up),
                      ("ve_guillotine_down_alpha", self.g_down), ("ve_plated_alpha", self.plated), ("ve_wordmark_gold_alpha", self.mark)):
            im.save(self.elements / f"{n}.png")
        self._salon_cache = {}

    def salon_at(self, ev, radius):
        """Clean salon graded by `ev` stops, revealed inside a soft radial matte of `radius` px (0 = black)."""
        key = (round(ev, 2), int(radius))
        if key in self._salon_cache:
            return self._salon_cache[key]
        if radius <= 0:
            im = B.blank()
        else:
            im = B.stops(self.salon, ev) if ev else self.salon.copy()
            if radius < 1600:
                im = B.radial_reveal(im, W // 2, 620, radius * 0.45, radius)
        self._salon_cache = {key: im}
        return im

    def compose(self, ev=0.0, radius=0, cake=1.0, plated=0.0, chand=1.0, guill=0.0, blade_down=0.0, mark=0.0, shake=(0, 0), flash=0.0):
        f = self.salon_at(ev, radius).copy()
        if mark > 0:
            B.paste_wordmark(f, self.mark, opacity=mark)
        g = 2 ** ev if ev else 1.0
        def grade(im):
            return ImageEnhance.Brightness(im.convert("RGB")).enhance(g).convert("RGBA") if ev else im
        def paste(im, op, cx, bottom=None, top=None):
            if op <= 0:
                return
            im = grade(im)
            layer = with_op(im, op)
            y = bottom - layer.height if bottom is not None else top
            f.alpha_composite(layer.convert("RGBA") if layer.mode != "RGBA" else layer, (cx - layer.width // 2 + shake[0], y + shake[1]))
        # alpha lost by grade(): restore
        def paste_a(im, op, cx, bottom=None, top=None):
            if op <= 0:
                return
            src = im
            gr = grade(src); gr.putalpha(src.getchannel("A"))
            layer = with_op(gr, op)
            y = bottom - layer.height if bottom is not None else top
            f.alpha_composite(layer, (cx - layer.width // 2 + shake[0], y + shake[1]))
        paste_a(self.g_up, guill * (1 - blade_down), W // 2, bottom=GUILL_BOTTOM)
        paste_a(self.g_down, guill * blade_down, W // 2, bottom=GUILL_BOTTOM)
        paste_a(self.cake, cake, W // 2, bottom=CAKE_BOTTOM)
        paste_a(self.plated, plated, W // 2, bottom=CAKE_BOTTOM + 30)
        paste_a(self.chand, chand, W // 2, top=CHAND_TOP)
        if flash > 0:
            f = Image.blend(f, Image.new("RGBA", (W, H), (255, 255, 255, 255)), flash)
        return f

    def render(self, f, burnin=True):
        extra = None
        if f < 53:
            im = self.compose()
        elif f < 106:
            r = lerp(200, 1700, ease((f - 53) / 33)) if f < 86 else 1700
            im = self.compose(radius=r)
            extra = "AE: radial luma matte reveals the clean salon behind the held cake + chandelier layers"
        elif f < 149:
            im = self.compose(radius=1700, mark=ease((f - 106) / 17))
        elif f < 211:
            t = ease((f - 149) / 51)
            im = self.compose(ev=-1.5 * t, radius=1700, chand=1 - t, guill=t, mark=1.0)
            extra = "AE: chandelier → guillotine morph (crystals → uprights, boss → blade, rope draws on); a dissolve stands in"
        elif f < 235:
            im = self.compose(ev=-1.5, radius=1700, chand=0, guill=1, mark=1 - ease((f - 211) / 12))
        elif f < 254:
            sh = (0, 0); fl = 0.0; bd = 0.0
            if f < 238:
                sh = ((f % 2) * 2 - 1, 0)
            elif f < 246:
                bd = ease((f - 238) / 8)
            else:
                bd = 1.0
                if f < 249:
                    fl = 0.35
                k = 1 - (f - 246) / 8
                sh = (round(4 * k), round(-3 * k))
            im = self.compose(ev=-1.5, radius=1700, chand=0, guill=1, blade_down=bd, shake=sh, flash=fl)
            extra = "AE: blade layer drops 8 f, 3-frame flash, 4 px kick. Blade-down still stands in for the impact state"
        elif f < 326:
            t = ease((f - 254) / 14)
            ev = lerp(-1.5, -0.5, ease((f - 254) / 16))
            im = self.compose(ev=ev, radius=1700, chand=0, guill=1, blade_down=1, cake=1 - t, plated=t)
            extra = "AE: cake falls into slices, portions slide out to their plates; the plated still stands in"
        else:
            t_close = ease((f - 326) / 24)
            r = lerp(1700, 0, t_close)
            t_sl = ease((f - 338) / 24)
            t_g = ease((f - 350) / 20)
            ev = lerp(-0.5, 0.0, t_g)
            im = self.compose(ev=ev, radius=r, chand=t_g, guill=1 - t_g, blade_down=1 - t_sl, cake=t_sl, plated=1 - t_sl)
            extra = "AE: salon closes to black, slices retrace to the cake, guillotine → chandelier; f373 = f0"
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
    print("elements:", {n: im.size for n, im in (("cake", S.cake), ("chand", S.chand), ("g_up", S.g_up), ("g_down", S.g_down), ("plated", S.plated), ("mark", S.mark))})
    resume = "--resume" in sys.argv
    for f in range(TOTAL):
        if resume and (frames / f"ve_{f:04d}.png").exists():
            continue
        S.render(f, burnin).save(frames / f"ve_{f:04d}.png", compress_level=1)
        if f % 48 == 0:
            print(f"frame {f}/{TOTAL}  {shot_name(f)}", flush=True)
    a = S.render(0, False).tobytes(); b = S.render(TOTAL - 1, False).tobytes()
    print("loop frame identical:", a == b)
    mp4 = out / "versailles_animatic_v0.1.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(frames / "ve_%04d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium", "-movflags", "+faststart", str(mp4)], check=True)
    print("wrote", mp4)


if __name__ == "__main__":
    main()
