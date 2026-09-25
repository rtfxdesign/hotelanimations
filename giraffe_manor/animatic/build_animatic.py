#!/usr/bin/env python3
"""Giraffe Manor animatic v0.1 — 1920x1080, 24 fps, 16.0 s (384 frames), loops.

Renders every frame with Pillow from the same assets and staging as the v2
storyboard (giraffe_manor/storyboard/build_frames.py), then encodes with ffmpeg
and lays the birdsong bed under it. Shots that still need Kling (6: the turn,
7: heads in the windows) are animatic placeholders: a crude move on the comp
and the client reference photo, each with a burned-in caption.

Usage:
    python giraffe_manor/animatic/build_animatic.py PULL_ROOT WALK_FRAMES_DIR OUT_DIR [--no-burnin]

PULL_ROOT        local mirror of the Drive folder (tools/drive_pull.py)
WALK_FRAMES_DIR  w_0000.png .. w_0299.png: giraffe_walking.mov at 1920x1080 RGBA
                 (ffmpeg -i giraffe_walking.mov -vf scale=1920:1080,format=rgba w_%04d.png)
OUT_DIR          frames/ (PNG sequence) and giraffe_manor_animatic_v0.1.mp4 go here

Requires Pillow, ffmpeg on PATH.
"""
import math
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageStat

W, H, FPS = 1920, 1080, 24
CREAM = (255, 255, 240, 255)
HERO_H, HERO_CX, FEET_Y = 800, 760, 880
LOGO_W, LOGO_TOP, MARK_W = 640, 912, 400
WALKER_STOP_LEFT, WALKER_FEET_Y = 1060, 885
WALK_SRC_FPS = 30
REPO = Path(__file__).resolve().parents[2]
WORDMARK = REPO / "assets" / "wordmarks" / "giraffe_manor_wordmark.png"

# Shot boundaries in frames @24 (v2 board). Each entry: (name, in, out)
SHOTS = [
    ("S1 hold", 0, 48), ("S2 logo", 48, 86), ("S3a enter", 86, 120), ("S3b stop", 120, 154),
    ("S4 reveal", 154, 178), ("S5 pull-back", 178, 206), ("S6 turn (Kling t3 f58-120)", 206, 269),
    ("S7 windows (GM-3b plate, push-in)", 269, 322), ("S8 payoff + mark", 322, 351),
    ("S9 return", 351, 373), ("S10 loop hold", 373, 384),
]
TOTAL = 384

FONT = next((p for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
                         "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                         "C:/Windows/Fonts/consolab.ttf", "/System/Library/Fonts/Menlo.ttc"] if Path(p).exists()), None)


def font(size):
    return ImageFont.truetype(FONT, size) if FONT else ImageFont.load_default()


def ease(t):  # smoothstep
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def ease_out(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def lerp(a, b, t):
    return a + (b - a) * t


def blank():
    return Image.new("RGBA", (W, H), CREAM)


def alpha_crop(im):
    return im.crop(im.getchannel("A").getbbox())


def fit_cover(im, w=W, h=H):
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def with_opacity(im, a):
    if a >= 1.0:
        return im
    out = im.copy()
    out.putalpha(out.getchannel("A").point(lambda v: int(v * a)))
    return out


def colour_match(src, ref, max_gain=1.35):
    def stat(im):
        mask = im.getchannel("A").point(lambda v: 255 if v > 200 else 0)
        s = ImageStat.Stat(im.convert("RGB"), mask=mask)
        return s.mean, s.stddev
    sm, ss = stat(src)
    rm, rs = stat(ref)
    bands = []
    for c, band in enumerate(src.convert("RGB").split()):
        g = min(max_gain, rs[c] / ss[c])
        o = rm[c] - sm[c] * g
        bands.append(band.point(lambda v, g=g, o=o: max(0, min(255, round(v * g + o)))))
    out = Image.merge("RGB", bands).convert("RGBA")
    out.putalpha(src.getchannel("A"))
    return out


class Assets:
    def __init__(self, pull: Path, walkdir: Path):
        gm = pull / "Giraffe Manor"
        self.hero = alpha_crop(Image.open(gm / "upscaled" / "ea5d5cfc-e93b-4d86-acf6-81bba6e7bd70.png").convert("RGBA"))
        k = HERO_H / self.hero.height
        self.hero = self.hero.resize((round(self.hero.width * k), round(self.hero.height * k)), Image.LANCZOS)
        self.logo = Image.open(WORDMARK).convert("RGBA")
        s = LOGO_W / self.logo.width
        self.logo_small = self.logo.resize((LOGO_W, round(self.logo.height * s)), Image.LANCZOS)
        self.plate = Image.open(gm / "upscaled" / "manor01_background.png").convert("RGBA")
        self.ref_ext = fit_cover(Image.open(gm / "images-2.jpg").convert("RGBA"))
        self.walkdir = walkdir
        self.walk_cache = {}
        # colour-match parameters from the first walk frame against the hero
        first = Image.open(walkdir / "w_0000.png").convert("RGBA")
        self.match_ref = colour_match(first, self.hero)
        self._match_from = first
        self.plate_scaled = {}

    def walk(self, src_index: int):
        src_index = max(0, min(299, src_index))
        if src_index not in self.walk_cache:
            im = Image.open(self.walkdir / f"w_{src_index:04d}.png").convert("RGBA")
            self.walk_cache[src_index] = alpha_crop(colour_match(im, self.hero))
            if len(self.walk_cache) > 40:
                self.walk_cache.pop(next(iter(self.walk_cache)))
        return self.walk_cache[src_index]

    # plate-locked staging (same maths as the board)
    S0 = None

    def plate_at(self, z, blur=0):
        S0 = H / self.plate.height
        X0 = (W - self.plate.width * S0) / 2
        PIV = (2140, 1490)
        s = S0 * z
        key = (round(s, 4), blur)
        if key not in self.plate_scaled:
            im = self.plate.resize((round(self.plate.width * s), round(self.plate.height * s)), Image.LANCZOS)
            if blur:
                im = im.filter(ImageFilter.GaussianBlur(blur))
            self.plate_scaled = {key: im}          # keep one; z changes every frame during the pull-back
        im = self.plate_scaled[key]
        ox = round(PIV[0] * S0 + X0 - PIV[0] * s)
        oy = round(PIV[1] * S0 - PIV[1] * s)
        canvas = blank()
        canvas.alpha_composite(im, (ox, oy))
        return canvas, (lambda px, py: (round(ox + px * s), round(oy + py * s))), s

    def stage(self, z, walker_img, blur=0, blend_cream=0.0, hero_shift=(0, 0), walker_shift=(0, 0), giraffe_scale=1.0):
        S0 = H / self.plate.height
        HERO_P, WALK_P = (1744, 1400), (2050, 1400)
        G_H_PLATE = HERO_H / (S0 * 2.65)
        canvas, to_canvas, s = self.plate_at(z, blur)
        if blend_cream:
            canvas = Image.blend(blank(), canvas, 1 - blend_cream)
        gh = G_H_PLATE * s * giraffe_scale
        hx, hy = to_canvas(*HERO_P)
        k = gh / self.hero.height
        g = self.hero.resize((round(self.hero.width * k), round(self.hero.height * k)), Image.LANCZOS)
        canvas.alpha_composite(g, (hx - g.width // 2 + hero_shift[0], hy - g.height + hero_shift[1]))
        wx, wy = to_canvas(*WALK_P)
        k = gh / walker_img.height
        wk = walker_img.resize((round(walker_img.width * k), round(walker_img.height * k)), Image.LANCZOS)
        canvas.alpha_composite(wk, (wx - wk.width // 2 + walker_shift[0], wy - wk.height + walker_shift[1]))
        return canvas


def paste_hero(canvas, hero):
    canvas.alpha_composite(hero, (HERO_CX - hero.width // 2, FEET_Y - hero.height))


def paste_logo(canvas, logo_small, opacity=1.0, scale=1.0):
    l = logo_small
    if scale != 1.0:
        l = l.resize((round(l.width * scale), round(l.height * scale)), Image.LANCZOS)
    l = with_opacity(l, opacity)
    canvas.alpha_composite(l, (HERO_CX - l.width // 2, LOGO_TOP + (logo_small.height - l.height) // 2))


def end_mark(canvas, logo, opacity):
    s = MARK_W / logo.width
    lw, lh = MARK_W, round(logo.height * s)
    pad = 22
    card = Image.new("RGBA", (lw + 2 * pad, lh + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(card).rounded_rectangle((0, 0, card.width - 1, card.height - 1), radius=14, fill=(255, 255, 240, 225))
    card.alpha_composite(logo.resize((lw, lh), Image.LANCZOS), (pad, pad))
    canvas.alpha_composite(with_opacity(card, opacity), (W - 60 - card.width, H - 60 - card.height))


def burn(canvas, f, shot, extra=None):
    d = ImageDraw.Draw(canvas)
    ff = font(22)
    txt = f"GIRAFFE MANOR · ANIMATIC v0.2 · {shot} · f{f:03d} · {f / FPS:05.2f}s"
    tw = d.textlength(txt, font=ff)
    d.rectangle((16, 16, 16 + tw + 20, 16 + 36), fill=(0, 0, 0, 200))
    d.text((26, 22), txt, font=ff, fill=(255, 176, 32))
    if extra:
        fe = font(30)
        tw = d.textlength(extra, font=fe)
        d.rectangle((W // 2 - tw // 2 - 20, H - 96, W // 2 + tw // 2 + 20, H - 44), fill=(0, 0, 0, 200))
        d.text((W // 2 - tw // 2, H - 88), extra, font=fe, fill=(255, 176, 32))


def shot_name(f):
    for name, a, b in SHOTS:
        if a <= f < b:
            return name
    return SHOTS[-1][0]


GEN_S6 = Path(os.environ["GM_S6_FRAMES"]) if os.environ.get("GM_S6_FRAMES") else None   # dir of 63 PNGs, Kling GM-2 take, f58..f120
GEN_S7 = Path(os.environ["GM_S7_PLATE"]) if os.environ.get("GM_S7_PLATE") else None    # GM-3b still, any 16:9 size
_s6_cache = {}
_s7_cache = {}


def s6_frame(i):
    """Frame i (0..62) of the generated turn, fitted to 1920x1080 RGBA."""
    if i not in _s6_cache:
        files = sorted(GEN_S6.glob("*.png"))
        im = Image.open(files[min(i, len(files) - 1)]).convert("RGBA")
        if im.size != (W, H):
            im = im.resize((W, H), Image.LANCZOS)
        _s6_cache[i] = im
    return _s6_cache[i]


def s7_plate(z):
    """GM-3b payoff plate at push-in factor z, centre-cropped to 1920x1080 RGBA."""
    key = round(z, 4)
    if key not in _s7_cache:
        if "base" not in _s7_cache:
            _s7_cache["base"] = Image.open(GEN_S7).convert("RGBA").resize((W, H), Image.LANCZOS)
        b = _s7_cache["base"]
        im = b.resize((round(W * z), round(H * z)), Image.LANCZOS)
        im = im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width - W) // 2 + W, (im.height - H) // 2 + H))
        _s7_cache[key] = im
    return _s7_cache[key]


def render_frame(A: Assets, f: int, burnin=True):
    hero_alone = blank(); paste_hero(hero_alone, A.hero)   # the loop frame
    extra = None

    def cream_frame(ff):
        """S1..S3: cream field, hero still, logo, walker entering and stopping."""
        c = blank()
        paste_hero(c, A.hero)
        if ff >= 86:
            t = ease_out((ff - 86) / 68)
            left = round(lerp(1940, WALKER_STOP_LEFT, t))
            src = round((ff - 86) / FPS * WALK_SRC_FPS)
            wk = A.walk(src)
            c.alpha_composite(wk, (left, WALKER_FEET_Y - wk.height))
        # logo on top (the walker passes behind it): fades up f48-67, holds, eases to 35 % over f120-154
        if 48 <= ff < 120:
            t = ease_out((ff - 48) / 19)
            paste_logo(c, A.logo_small, opacity=t, scale=lerp(0.96, 1.0, t))
        elif 120 <= ff < 154:
            t = (ff - 120) / 34
            paste_logo(c, A.logo_small, opacity=lerp(1.0, 0.35, ease(t)))
        return c

    if f < 154:
        canvas = cream_frame(f)
        frozen_walker = None
    if f >= 154:
        # walker frozen on the frame it stopped on (src index at f=154)
        frozen_walker = A.walk(round((154 - 86) / FPS * WALK_SRC_FPS))

    if 154 <= f < 178:
        # ---- S4: the last S3 frame (walker stopped, logo at 35 %) dissolves to the manor at z=2.65, soft.
        # The logo lives only in the S3 frame, so it fades out with the dissolve.
        t = (f - 154) / 24
        staged = A.stage(2.65, frozen_walker, blur=10)
        canvas = Image.blend(cream_frame(153), staged, ease(t))
    elif 178 <= f < 216:
        # ---- S5: rack focus f178-188 (blur 10 -> 0), then pull-back z 2.65 -> 1.0 over f188-216 (overlaps S6 by 10 f)
        if f < 188:
            blur = round(lerp(10, 0, (f - 178) / 10))
            canvas = A.stage(2.65, frozen_walker, blur=blur)
        else:
            z = lerp(2.65, 1.0, ease((f - 188) / 28))
            canvas = A.stage(z, frozen_walker)
    elif 216 <= f < 269 and GEN_S6 is not None:
        # ---- S6: the generated turn (Kling GM-2 take 3, source f58-120 = 63 frames), 6-frame dissolve in from the staged plate
        gen = s6_frame(f - 216)
        if f < 222:
            canvas = Image.blend(A.stage(1.0, frozen_walker), gen, ease((f - 216) / 6))
        else:
            canvas = gen
        extra = "SHOT 6 — Kling GM-2 t3, f58-120; turn is partial, roto candidate"
    elif 216 <= f < 269:
        # ---- S6 placeholder: giraffes shrink and drift up toward the house (they do not turn; that is Kling's job)
        t = ease((f - 216) / 53)
        gs = lerp(1.0, 0.62, t)
        shift = (round(lerp(0, -40, t)), round(lerp(0, -150, t)))
        canvas = A.stage(1.0, frozen_walker, hero_shift=shift, walker_shift=shift, giraffe_scale=gs)
        extra = "SHOT 6 PLACEHOLDER — Kling: both turn and walk up to the house"
    elif 269 <= f < 322 and GEN_S7 is not None:
        # ---- S7: cut to the GM-3b payoff plate (12 f dissolve from the last S6 frame), 4 % push-in over the shot.
        # The necks-rise motion (GM-4) is not generated yet; this is a still with a push.
        t = ease((f - 269) / 53)
        ref = s7_plate(lerp(1.0, 1.04, t))
        if f < 281:
            prev = s6_frame(62) if GEN_S6 is not None else A.stage(1.0, frozen_walker, hero_shift=(-40, -150), walker_shift=(-40, -150), giraffe_scale=0.62)
            canvas = Image.blend(prev, ref, ease((f - 269) / 12))
        else:
            canvas = ref
        extra = "SHOT 7 — GM-3b plate, still + push-in; GM-4 motion pending"
    elif 269 <= f < 322:
        # ---- S7 placeholder: dissolve (12 f) to the client reference of the payoff, slow push-in
        t = ease((f - 269) / 53)
        z = lerp(1.0, 1.04, t)
        ref = A.ref_ext.resize((round(W * z), round(H * z)), Image.LANCZOS)
        ref = ref.crop(((ref.width - W) // 2, (ref.height - H) // 2, (ref.width - W) // 2 + W, (ref.height - H) // 2 + H))
        if f < 281:
            prev = A.stage(1.0, frozen_walker, hero_shift=(-40, -150), walker_shift=(-40, -150), giraffe_scale=0.62)
            canvas = Image.blend(prev, ref, ease((f - 269) / 12))
        else:
            canvas = ref
        extra = "SHOT 7 PLACEHOLDER — Kling: heads through the upstairs windows (client reference photo)"
    elif 322 <= f < 351:
        # ---- S8: payoff hold, small mark fades up bottom-right over 0.5 s
        canvas = s7_plate(1.04).copy() if GEN_S7 is not None else A.ref_ext.copy()
        end_mark(canvas, A.logo, ease(min(1, (f - 322) / 12)))
    elif 351 <= f < 373:
        # ---- S9: exposure lift (8 f) then dissolve to the hero alone
        payoff = s7_plate(1.04).copy() if GEN_S7 is not None else A.ref_ext.copy(); end_mark(payoff, A.logo, 1.0)
        t = (f - 351) / 22
        lift = Image.blend(payoff, blank(), 0.25 * ease(min(1, (f - 351) / 8)))
        canvas = Image.blend(lift, hero_alone, ease(t))
    elif f >= 373:
        canvas = hero_alone.copy()

    if burnin:
        burn(canvas, f, shot_name(f), extra)
    return canvas.convert("RGB")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    burnin = "--no-burnin" not in sys.argv
    pull, walkdir, out = (Path(a).expanduser().resolve() for a in args[:3])
    frames_dir = out / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    A = Assets(pull, walkdir)
    for f in range(TOTAL):
        render_frame(A, f, burnin).save(frames_dir / f"gm_{f:04d}.png", compress_level=1)
        if f % 48 == 0:
            print(f"frame {f}/{TOTAL}  {shot_name(f)}", flush=True)
    # loop check: last frame equals first frame apart from the burn-in
    a = render_frame(A, 0, False).tobytes(); b = render_frame(A, TOTAL - 1, False).tobytes()
    print("loop frame identical:", a == b)
    mp4 = out / ("giraffe_manor_animatic_v0.2.mp4" if (GEN_S6 or GEN_S7) else "giraffe_manor_animatic_v0.1.mp4")
    bed = pull / "Giraffe Manor" / "audio" / "birdsong01.wav"
    cmd = ["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(frames_dir / "gm_%04d.png")]
    if bed.exists():
        cmd += ["-i", str(bed), "-filter_complex", f"[1:a]atrim=0:{TOTAL / FPS},afade=t=in:d=0.5,afade=t=out:st={TOTAL / FPS - 0.5}:d=0.5,volume=-14dB[a]", "-map", "0:v", "-map", "[a]", "-c:a", "aac", "-b:a", "160k"]
    cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium", "-movflags", "+faststart", "-shortest", str(mp4)]
    subprocess.run(cmd, check=True)
    print("wrote", mp4)


if __name__ == "__main__":
    main()
