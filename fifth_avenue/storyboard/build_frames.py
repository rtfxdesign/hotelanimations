#!/usr/bin/env python3
"""Build the Fifth Avenue Hotel storyboard frames from the real assets.

Composites eight 1920x1080 frames (one per storyboard beat, plus one
alternate) from a local pull of the Drive folder, plus a contact sheet.
Frames that stand in for shots still to be generated, or that use a
placeholder mark, are tagged in the corner.

Usage:
    python fifth_avenue/storyboard/build_frames.py PULL_ROOT OUT_DIR

PULL_ROOT  local mirror of the Drive folder (tools/drive_pull.py); the film's
           files are under "5th ave hotel NYC/orig" and ".../upscaled"
OUT_DIR    where the PNG frames, *_small.jpg and contact_sheet.jpg go

Requires Pillow. psd-tools is optional: with it, the walkers plate is built
from turtlewalkers.psd (clean background layer + the four separated layers at
their PSD positions); without it, the 4:3 turtlewalkers.png is cropped to
cover 16:9 and the frame is tagged. Layout constants are at the top.

Beats follow theria_hotel_animations_timing_v1.md §2 (12.0 s, 24 fps).
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont

W, H = 1920, 1080
WHITE = (255, 255, 255, 255)

# --- Beats 1-3: the tortoise alone on white ---------------------------------
HERO_W = 860          # isolated tortoise width on the canvas (1.33x its plate size)
HERO_CX = 1100        # hero centre x (right of centre: the couple arrive at left)
HERO_FEET_Y = 650     # hero claw line
LOCKUP_W = 480        # gold lockup width under the plastron
LOCKUP_TOP = 700

# --- Beats 4-7: the walkers plate ------------------------------------------
# turtlewalkers.psd is 4346x2444 (16:9); layer origins from psd_layers_2026-09-25.md
PSD_W, PSD_H = 4346, 2444
LAYER_ORIGIN = {"woman": (742, 196), "man": (1754, 226), "leash": (1798, 1095), "turtle": (1934, 1272)}
LAYER_ORDER = ("woman", "man", "leash", "turtle")          # PSD stacking, bottom -> top
PLATE_S = W / PSD_W                                          # 0.4418: PSD px -> HD px
# Beat 5 end-frame offsets in PSD px (x only). Timing doc: man's foot ~15 px,
# tortoise "one body-width" -- a full body-width (1463 px) would carry the
# head out of frame right, so the board uses a quarter body-width.
WALK_END_DX = {"woman": 27, "man": 34, "turtle": 366}
ROUNDEL_W = 520       # end-card roundel width (downscale of the 894 px 2x file)

FONT = next((p for p in [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
] if Path(p).exists()), None)


def font(size):
    return ImageFont.truetype(FONT, size) if FONT else ImageFont.load_default()


def fit_cover(im, w=W, h=H):
    """Scale to cover w x h and crop the centre."""
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def alpha_crop(im):
    return im.crop(im.getchannel("A").getbbox())


def tag(im, text, colour=(255, 176, 32), max_chars=92):
    """Corner tag; long text wraps onto several lines so it stays readable."""
    words, lines, cur = text.split(), [], ""
    for wd in words:
        if cur and len(cur) + 1 + len(wd) > max_chars:
            lines.append(cur)
            cur = wd
        else:
            cur = f"{cur} {wd}".strip()
    lines.append(cur)
    d = ImageDraw.Draw(im)
    f = font(30)
    tw = max(d.textlength(l, font=f) for l in lines)
    d.rectangle((24, 24, 24 + tw + 28, 24 + 16 + 40 * len(lines)), fill=(0, 0, 0, 220))
    for i, l in enumerate(lines):
        d.text((38, 32 + 40 * i), l, font=f, fill=colour)


def blank():
    return Image.new("RGBA", (W, H), WHITE)


def scale_to_width(im, width):
    s = width / im.width
    return im.resize((width, round(im.height * s)), Image.LANCZOS)


def with_opacity(im, opacity):
    if opacity >= 1.0:
        return im
    im = im.copy()
    im.putalpha(im.getchannel("A").point(lambda v: int(v * opacity)))
    return im


def paste_hero(canvas, hero, width=HERO_W, cx=HERO_CX, feet=HERO_FEET_Y):
    g = scale_to_width(alpha_crop(hero), width)
    canvas.alpha_composite(g, (cx - g.width // 2, feet - g.height))
    return canvas


def paste_lockup(canvas, lockup, width=LOCKUP_W, cx=HERO_CX, top=LOCKUP_TOP, opacity=1.0):
    l = with_opacity(scale_to_width(lockup, width), opacity)
    canvas.alpha_composite(l, (cx - l.width // 2, top))
    return canvas


def key_gold(roundel):
    """Fallback placeholder: keep the gold pixels of the navy roundel, drop the disc.

    Only used if upscaled/fifthave_text.png (the same key, done in Photoshop)
    is missing from the pull. Gold = warm, bright, clearly above blue; the
    disc's anti-aliased rim is dropped by the alpha and brightness tests.
    """
    px = roundel.convert("RGBA").load()
    out = Image.new("RGBA", roundel.size, (0, 0, 0, 0))
    op = out.load()
    for y in range(roundel.height):
        for x in range(roundel.width):
            r, g, b, a = px[x, y]
            if a > 200 and r > 120 and r > b + 60 and g > b + 20:
                op[x, y] = (r, g, b, a)
    return alpha_crop(out)


def load_plate_layers(up):
    """Return (background RGBA at PSD size, {name: layer RGBA}) or (None, layers)."""
    layers = {n: Image.open(up / f"{n}.png").convert("RGBA") for n in LAYER_ORDER}
    try:
        from psd_tools import PSDImage
    except ImportError:
        return None, layers
    psd = PSDImage.open(up / "turtlewalkers.psd")
    bg = next(l for l in psd if l.name == "background").topil().convert("RGBA")
    return bg, layers


def build_plate(bg, layers, dx=None):
    """Composite the walkers plate at PSD size, optionally shifting layers in x."""
    dx = dx or {}
    plate = bg.copy()
    for n in LAYER_ORDER:
        x, y = LAYER_ORIGIN[n]
        layer = layers[n]
        if n == "leash" and "turtle" in dx:
            # the leash runs woman's hand (left end) -> collar (right end): stretch
            # it so the collar end follows the tortoise
            stretch = layer.width + dx["turtle"] - dx.get("woman", 0)
            layer = layer.resize((stretch, layer.height), Image.LANCZOS)
            x += dx.get("woman", 0)
        else:
            x += dx.get(n, 0)
        plate.alpha_composite(layer, (x, y))
    return fit_cover(plate)


def desaturate(im, amount=0.2):
    return ImageEnhance.Color(im.convert("RGB")).enhance(1 - amount).convert("RGBA")


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    pull, out = (Path(a).expanduser().resolve() for a in sys.argv[1:3])
    out.mkdir(parents=True, exist_ok=True)
    fa = pull / "5th ave hotel NYC"
    up = fa / "upscaled"

    hero = Image.open(up / "turtle02.png").convert("RGBA")           # isolated tortoise, 2803x1298
    roundel = Image.open(up / "fifthavenue.png").convert("RGBA")     # navy roundel, 894 px (2x of 447)
    text_png = up / "fifthave_text.png"
    if text_png.exists():
        lockup = alpha_crop(Image.open(text_png).convert("RGBA"))    # gold type keyed from the roundel
        lockup_src = "fifthave_text.png"
    else:
        lockup = key_gold(roundel)
        lockup_src = "gold keyed from fifthavenue.png"
    bg, layers = load_plate_layers(up)
    plate_note = ""
    if bg is not None:
        plate_hold = build_plate(bg, layers)
        plate_end = build_plate(bg, layers, WALK_END_DX)
    else:
        plate_hold = plate_end = fit_cover(Image.open(up / "turtlewalkers.png").convert("RGBA"))
        plate_note = " (psd-tools missing: 4:3 turtlewalkers.png cropped to 16:9, not the PSD)"

    frames = []

    # 01 -- Beat 1: the gold tortoise alone on white (specular sweep is a motion note only)
    f = paste_hero(blank(), hero)
    frames.append(("01_hold", f))

    # 01b -- ALT Beat 1: the plate's own tortoise layer as the hero, so the Beat 4
    # dissolve lands on the identical render (turtle02 and the plate tortoise differ)
    f = paste_hero(blank(), layers["turtle"])
    tag(f, "ALT BEAT 1 — plate tortoise layer (turtle.png) as hero: identical render to Beat 4-5, so the dissolve is a true match")
    frames.append(("01b_hold_ALT", f))

    # 02 -- Beat 2: gold lockup, no disc, under the plastron
    f = paste_lockup(paste_hero(blank(), hero), lockup)
    tag(f, f"PLACEHOLDER — vector lockup pending. Shown: {lockup_src} (gold type from the 2x 447 px roundel)")
    frames.append(("02_lockup", f))

    # 03 -- Beat 3: lockup on its way out (35 %, +3 % scale), tortoise unchanged
    f = paste_lockup(paste_hero(blank(), hero), lockup, width=round(LOCKUP_W * 1.03), opacity=0.35)
    tag(f, "PLACEHOLDER lockup at 35 %, +3 % scale — mid fade-out (f115 of f101-118)")
    frames.append(("03_lockup_out", f))

    # 04 -- Beat 4: cross-dissolve white -> park, tortoise as anchor, pull-out 1.33 -> 1.0
    tx, ty = LAYER_ORIGIN["turtle"]
    tw = round(layers["turtle"].width * PLATE_S)
    hero_at_plate = scale_to_width(alpha_crop(hero), tw)
    end_white = blank()
    end_white.alpha_composite(hero_at_plate, (round(tx * PLATE_S), round((ty + layers["turtle"].height) * PLATE_S) - hero_at_plate.height))
    f = Image.blend(end_white, plate_hold, 0.5)
    tag(f, "MID-DISSOLVE f152 — white to park, 50 %. Pull-out 1.33 -> 1.0 anchored on the tortoise. "
           "Ghosting shows turtle02 vs the plate tortoise: different render, see 01b ALT" + plate_note)
    frames.append(("04_reveal", f))

    # 05 -- Beat 5a: the walk, start frame = the full plate, layers at PSD positions
    f = plate_hold.copy()
    if plate_note:
        tag(f, "PLATE" + plate_note)
    frames.append(("05_walk_start", f))

    # 06 -- Beat 5b: the walk, end frame -- TO GENERATE; layers offset as the conform target
    f = plate_end.copy()
    tag(f, "TO GENERATE (KLING) — end frame of the 1/6-speed walk. Shown: PSD layers offset "
           "(man +15 px, woman +12 px, tortoise +162 px, leash stretched) as a conform target" + plate_note)
    frames.append(("06_walk_end_TOGEN", f))

    # 07 -- Beat 6: end card, plate frozen and 20 % desaturated, full navy roundel centre
    f = desaturate(plate_end, 0.2)
    r = scale_to_width(roundel, ROUNDEL_W)
    f.alpha_composite(r, ((W - r.width) // 2, (H - r.height) // 2))
    tag(f, "ROUNDEL = 447 px SOURCE MARK AT 2x (fifthavenue.png), PLACEHOLDER UNTIL VECTOR")
    frames.append(("07_endcard", f))

    for name, im in frames:
        im.convert("RGB").save(out / f"{name}.png", optimize=True)
        im.convert("RGB").resize((960, 540), Image.LANCZOS).save(out / f"{name}_small.jpg", quality=88)

    # contact sheet: 3 columns
    cols, tw_, th, gap = 3, 620, 349, 16
    rows = (len(frames) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw_ + (cols + 1) * gap, rows * (th + 40) + (rows + 1) * gap), (16, 16, 16))
    d = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(frames):
        r_, c = divmod(i, cols)
        x, y = gap + c * (tw_ + gap), gap + r_ * (th + 40 + gap)
        sheet.paste(im.convert("RGB").resize((tw_, th), Image.LANCZOS), (x, y))
        d.text((x, y + th + 8), name.replace("_", " "), font=font(22), fill=(255, 176, 32))
    sheet.save(out / "contact_sheet.jpg", quality=88)
    print(f"{len(frames)} frames -> {out}")


if __name__ == "__main__":
    main()
