#!/usr/bin/env python3
"""Build the Passalacqua (Lago di Como) storyboard frames from the real assets.

Composites eight 1920x1080 frames (one per storyboard beat, timing doc v1
section 3, 13.0 s @ 24 fps) from the files in a local pull of the Drive
folder, plus a contact sheet. Frames that stand in for shots still to be
generated are tagged in the corner.

Usage:
    python passalacqua/storyboard/build_frames.py PULL_ROOT OUT_DIR

PULL_ROOT  local mirror of the Drive folder (contains `Passalaqua/`)
OUT_DIR    where the PNG frames, *_small.jpg and contact_sheet.jpg go

Requires Pillow only. Layout constants are at the top.

What the four source files actually are (checked by eye and by pixel stats
on 2026-09-25 -- the timing doc v1 has two of them swapped and one wrong):
  passalacqua.jpg  410x319  the printed mark: three flat gold fish over a wave
                            rule, PASSALACQUA / LAGO DI COMO. Only flat source.
  images-3.jpg     275x183  NOT the mark: a small photo of a villa on Como.
  46e10c0f-*.png   1421x1107  the SAME lockup re-rendered with dimensional,
                            polished-gold fish on white (AI render; wordmark
                            inside it is redrawn -- never use its type).
  b74514e7-*.png   1536x1024  three gold fish leaping out of the lake, villa
                            behind. The only lake plate; fish are baked in.
"""
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont

W, H = 1920, 1080
WHITE = (255, 255, 255, 255)

# --- the 410 px mark, placed at a plain 2x Lanczos (placeholder, never AI-enlarged)
MARK_SCALE = 2
MARK_LEFT, MARK_TOP = 550, 221          # 820x638 centred on the 1920x1080 frame
# row bands measured in the 410x319 source (ink threshold L<225), in source px
FISH_ROWS = (70, 147)                   # three flat fish
WAVE_ROWS = (147, 163)                  # wave rule under the tails
TYPE_ROWS = (163, 252)                  # PASSALACQUA + LAGO DI COMO
FLAT_FISH_BOX = (159, 74, 251, 147)     # bbox of the three flat fish (source px)

# --- the dimensional gold fish in 46e10c0f (1421x1107), measured the same way
GOLD_FISH_BOXES = [(532, 215, 653, 546), (655, 215, 777, 546), (778, 215, 900, 546)]
GOLD_BLOCK = (532, 215, 900, 546)       # all three, used for the fill beat

FONT = next((p for p in [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
] if Path(p).exists()), None)


def font(size):
    return ImageFont.truetype(FONT, size) if FONT else ImageFont.load_default()


def fit_cover(im, w=W, h=H, zoom=1.0):
    """Scale to cover w x h (times zoom) and crop the centre."""
    s = max(w / im.width, h / im.height) * zoom
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def tag(im, *lines, colour=(255, 176, 32)):
    """Corner tag, one or more lines (same look as the Giraffe Manor board)."""
    d = ImageDraw.Draw(im)
    f = font(30)
    tw = max(d.textlength(t, font=f) for t in lines)
    d.rectangle((24, 24, 24 + tw + 28, 24 + 52 * len(lines)), fill=(0, 0, 0, 220))
    for i, t in enumerate(lines):
        d.text((38, 32 + 52 * i), t, font=f, fill=colour)


def blank(colour=WHITE):
    return Image.new("RGBA", (W, H), colour)


def scaled(im, s):
    return im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)


def with_opacity(im, opacity):
    if opacity >= 1.0:
        return im
    im = im.copy()
    im.putalpha(im.getchannel("A").point(lambda v: int(v * opacity)))
    return im


def white_to_alpha(im, lo=228, hi=250):
    """Cheap white-threshold alpha for an object photographed on white.
    Not a proper key -- edges will be crunchy. Good enough for a board."""
    r, g, b = im.convert("RGB").split()
    mn = ImageChops.darker(ImageChops.darker(r, g), b)
    a = mn.point(lambda v: 255 if v <= lo else (0 if v >= hi else int(255 * (hi - v) / (hi - lo))))
    out = im.convert("RGBA")
    out.putalpha(a)
    return out


def mark_band(mark2x, rows, opacity=1.0):
    """A horizontal band of the 2x mark as an RGBA layer positioned on the frame."""
    y0, y1 = rows[0] * MARK_SCALE, rows[1] * MARK_SCALE
    band = mark2x.crop((0, y0, mark2x.width, y1)).convert("RGBA")
    return with_opacity(band, opacity), (MARK_LEFT, MARK_TOP + y0)


def paste_mark_bands(canvas, mark2x, *bands):
    for rows, opacity in bands:
        layer, pos = mark_band(mark2x, rows, opacity)
        canvas.alpha_composite(layer, pos)
    return canvas


def flat_fish_frame_box():
    """Where the three flat fish sit on the frame at 2x."""
    x0, y0, x1, y1 = FLAT_FISH_BOX
    return (MARK_LEFT + x0 * MARK_SCALE, MARK_TOP + y0 * MARK_SCALE,
            MARK_LEFT + x1 * MARK_SCALE, MARK_TOP + y1 * MARK_SCALE)


def gold_block_registered(gold, scale=1.0):
    """The three gold fish from 46e10c0f scaled to sit exactly on the flat fish."""
    fx0, fy0, fx1, fy1 = flat_fish_frame_box()
    block = gold.crop(GOLD_BLOCK)
    s = (fy1 - fy0) / block.height * scale
    block = scaled(block, s)
    cx, cy = (fx0 + fx1) // 2, (fy0 + fy1) // 2
    return block, (cx - block.width // 2, cy - block.height // 2)


def gold_fish_layers(gold, height, rotations=(0, 0, 0)):
    """Individual gold fish, white-to-alpha, scaled to `height`, optionally rotated."""
    out = []
    for box, rot in zip(GOLD_FISH_BOXES, rotations):
        f = white_to_alpha(gold.crop(box))
        f = scaled(f, height / f.height)
        if rot:
            f = f.rotate(rot, resample=Image.BICUBIC, expand=True)
        out.append(f)
    return out


def cast_shadow(canvas, layer, pos, dy=18, blur=14, alpha=70):
    sh = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    sh.putalpha(layer.getchannel("A").point(lambda v: int(v * alpha / 255)))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(sh, (pos[0] + 6, pos[1] + dy))


def ripple_rings(canvas, cx, cy, n=4, rx0=90, ry0=22, step=1.45, alpha=150):
    d = ImageDraw.Draw(canvas)
    rx, ry = rx0, ry0
    for i in range(n):
        a = int(alpha * (1 - i / n))
        d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), outline=(255, 255, 255, a), width=3)
        rx, ry = rx * step, ry * step


def main():
    pull, out = (Path(a).expanduser().resolve() for a in sys.argv[1:3])
    out.mkdir(parents=True, exist_ok=True)
    src = pull / "Passalaqua"
    mark = Image.open(src / "passalacqua.jpg").convert("RGBA")
    mark2x = scaled(mark, MARK_SCALE)                      # 820x638, plain Lanczos
    gold = Image.open(src / "46e10c0f-f505-41f9-a395-57fca38d4551.png").convert("RGBA")
    leap = Image.open(src / "b74514e7-03e1-4fab-98a6-e903c4f48506.png").convert("RGBA")
    villa_ref = Image.open(src / "images-3.jpg").convert("RGBA")

    PH = "PLACEHOLDER — 410 px source at plain 2x, vector crest pending"
    frames = []

    # 01 — Beat 1 (00.0–02.0): three flat fish + wave rule on white, no type
    f = paste_mark_bands(blank(), mark2x, (FISH_ROWS, 1.0), (WAVE_ROWS, 1.0))
    tag(f, PH, "Beat 1: fish draw on L→C→R f0–f30, then dead still")
    frames.append(("01_outlines", f))

    # 02 — Beat 2 (02.0–03.6): wordmark fades up beneath the wave rule
    f = paste_mark_bands(blank(), mark2x, (FISH_ROWS, 1.0), (WAVE_ROWS, 1.0), (TYPE_ROWS, 1.0))
    tag(f, PH, "Beat 2: PASSALACQUA / LAGO DI COMO fades up, tracking +8% → +4%")
    frames.append(("02_wordmark", f))

    # 03 — Beat 3 (03.6–05.0): type out, gold floods each fish bottom-to-top (shown at ~55 %)
    f = paste_mark_bands(blank(), mark2x, (FISH_ROWS, 1.0), (WAVE_ROWS, 1.0), (TYPE_ROWS, 0.35))
    block, pos = gold_block_registered(gold)
    fill = Image.new("L", block.size, 0)
    ImageDraw.Draw(fill).rectangle((0, int(block.height * 0.45), block.width, block.height), fill=255)
    fill = fill.filter(ImageFilter.GaussianBlur(6))
    block.putalpha(ImageChops.multiply(block.getchannel("A"), fill))
    f.alpha_composite(block, pos)
    tag(f, "COMP — gold flood = 46e10c0f fish over the flat mark, bottom-up wipe (shown 55 %)",
        "TO GENERATE (Flux) — three isolated gold fish on white, one per layer, flat-on")
    frames.append(("03_fill", f))

    # 04 — Beat 4 (05.0–06.6): fish become real — rotate to 3/4, cast shadow, first tail beat
    f = blank()
    fx0, fy0, fx1, fy1 = flat_fish_frame_box()
    h = int((fy1 - fy0) * 1.3)                      # gentle push-in as they come off the page
    cy = (fy0 + fy1) // 2
    layers = gold_fish_layers(gold, h, rotations=(-9, 4, -5))
    xs = [W // 2 - 190, W // 2, W // 2 + 190]
    for layer, cx, dy in zip(layers, xs, (14, -10, 6)):
        pos = (cx - layer.width // 2, cy - layer.height // 2 + dy)
        cast_shadow(f, layer, pos)
        f.alpha_composite(layer, pos)
    tag(f, "TO GENERATE (Kling) — flat-on → three-quarter, cast shadow, first tail beat, offset x3",
        "Shown: 46e10c0f fish crops, white-threshold alpha, rotated; push-in ~30 % assumed")
    frames.append(("04_alive_TOGEN", f))

    # 05 — Beat 5 (06.6–08.2): white dissolves to the lake; water rises; fish drop in
    lake = fit_cover(leap).filter(ImageFilter.GaussianBlur(8))
    f = Image.blend(blank(), lake, 0.55)
    water = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(water).rectangle((0, 740, W, H), fill=(40, 90, 120, 110))
    layers = gold_fish_layers(gold, int((fy1 - fy0) * 1.6), rotations=(-30, -22, -34))
    xs = [W // 2 - 300, W // 2, W // 2 + 300]
    for layer, cx, dy in zip(layers, xs, (40, 0, 70)):
        f.alpha_composite(layer, (cx - layer.width // 2, 560 + dy))
    f.alpha_composite(water)
    for cx in xs:
        ripple_rings(f, cx, 800, n=3, rx0=110, ry0=26, alpha=120)
    tag(f, "TO GENERATE (Seedream) — clean lake + villa plate, NO fish (b74514e7 has them baked in)",
        "TO GENERATE (Kling) — fish drop into rising water, splash rings. Shown: b74514e7 55 % under white")
    frames.append(("05_lake_TOGEN", f))

    # 06 — Beat 6a (08.2–10.2): the leap, tight — centre fish breaches first
    f = fit_cover(leap, zoom=1.12)
    tag(f, "TO GENERATE (Kling) — staggered breaches 08.6 / 09.4 / 10.1, ~0.9 s airborne each",
        "Shown: b74514e7 at 112 % — all three in sync here; the film must NOT be")
    frames.append(("06_leap_TOGEN", f))

    # 07 — Beat 6b (10.2–12.2): same shot, camera pulled back 12 % to open up the villa
    f = fit_cover(leap)
    tag(f, "TO GENERATE (Kling) — end of the 12 % pull-back, last (right) fish still airborne",
        "Shown: b74514e7 full frame — this plate IS the leap keyframe, no clean villa behind it")
    frames.append(("07_pullback_TOGEN", f))

    # 08 — Beat 7 (12.2–13.0): end card — ripples settle into the wave rule, wordmark over the lake
    f = ImageEnhance.Color(fit_cover(leap).filter(ImageFilter.GaussianBlur(6)).convert("RGB")).enhance(0.5).convert("RGBA")
    f.alpha_composite(Image.new("RGBA", (W, H), (0, 10, 25, 150)))
    wave, _ = mark_band(mark2x, WAVE_ROWS)
    wave = white_to_alpha(wave, lo=200, hi=245)
    wave_y = 560
    # rings concentric with the wave rule: the innermost ring is the rule's width, the rest spread out
    ripple_rings(f, W // 2, wave_y + wave.height // 2, n=5, rx0=95, ry0=14, step=1.5, alpha=170)
    f.alpha_composite(wave, (MARK_LEFT, wave_y))
    typ, _ = mark_band(mark2x, TYPE_ROWS)
    inv = ImageChops.invert(typ.convert("L"))            # black type → white type over the lake
    typ_w = Image.new("RGBA", typ.size, (255, 255, 255, 255))
    typ_w.putalpha(inv)
    f.alpha_composite(typ_w, (MARK_LEFT, 600))
    tag(f, "COMP (AE) — splash rings settle into the wave rule; wordmark fades up reversed-out",
        PH + "; needs the clean fish-free lake plate")
    frames.append(("08_endcard_COMP", f))

    # 08b — reference: what the client's small villa photo actually shows (not the mark)
    f = fit_cover(villa_ref)
    tag(f, "REFERENCE ONLY — images-3.jpg (275 px) is a villa photo, not the mark; confirm it is Passalacqua",
        "Not a beat. Kept so the pull's fourth file is accounted for")
    frames.append(("ref_images-3_villa", f))

    for name, im in frames:
        im.convert("RGB").save(out / f"{name}.png", optimize=True)
        im.convert("RGB").resize((960, 540), Image.LANCZOS).save(out / f"{name}_small.jpg", quality=88)

    # contact sheet: 3 columns
    cols, tw, th, gap = 3, 620, 349, 16
    rows = (len(frames) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * gap, rows * (th + 40) + (rows + 1) * gap), (16, 16, 16))
    d = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(frames):
        r, c = divmod(i, cols)
        x, y = gap + c * (tw + gap), gap + r * (th + 40 + gap)
        sheet.paste(im.convert("RGB").resize((tw, th), Image.LANCZOS), (x, y))
        d.text((x, y + th + 8), name.replace("_", " "), font=font(22), fill=(255, 176, 32))
    sheet.save(out / "contact_sheet.jpg", quality=88)
    print(f"{len(frames)} frames -> {out}")


if __name__ == "__main__":
    main()
