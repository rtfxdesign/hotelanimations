#!/usr/bin/env python3
"""Build the Fifth Avenue Hotel storyboard frames (v2) from the real assets.

Composites ten 1920x1080 frames from a local pull of the Drive folder, plus a
contact sheet, and writes the flat gold type extracted from the vector lockup.
Frames that stand in for motion still to be generated or comped are tagged in
the corner; there are no placeholder marks in this board.

Usage:
    python fifth_avenue/storyboard/build_frames.py PULL_ROOT OUT_DIR

PULL_ROOT  local mirror of the Drive folder (tools/drive_pull.py); the film's
           files are under "5th ave hotel NYC/upscaled" and ".../audio"
OUT_DIR    where the PNG frames, *_small.jpg, contact_sheet.jpg and
           lockup_vector_goldtype.png go

Requires Pillow and numpy. psd-tools is optional: with it, the walkers plate is
built from turtlewalkers.psd (clean background layer + the separated layers at
their PSD positions); without it, the 4:3 turtlewalkers.png is cropped to cover
16:9 and the frame is tagged.

v2 (2026-09-25): hero = the plate's own tortoise layer at plate scale (no
pull-out; the Beat 4 dissolve is a true match). Gold lockup = Allen's rendered
"Asset 1@2x.png", low-centre under the tortoise, which sits offset up-left of
its plate position in Beats 1-3 and slides down-right into it through the
dissolve. End: the park push-whips out frame-left, tortoise alone on white,
return tween up-left, loop frame == frame 1. 13.0 s = f312 @ 24 fps.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1920, 1080
WHITE = (255, 255, 255, 255)

# --- The walkers plate (Beats 4-6) -----------------------------------------
# turtlewalkers.psd is 4346x2444 (16:9); layer origins from psd_layers_2026-09-25.md
PSD_W, PSD_H = 4346, 2444
LAYER_ORIGIN = {"woman": (742, 196), "man": (1754, 226), "leash": (1798, 1095), "turtle": (1934, 1272)}
LAYER_ORDER = ("woman", "man", "leash", "turtle")          # PSD stacking, bottom -> top
PLATE_S = H / PSD_H                                          # 0.4419: PSD px -> HD px (height governs the cover)
PLATE_X0 = (round(PSD_W * PLATE_S) - W) // 2                 # 0: fit_cover crops 1 px off the right
# Beat 5 end-frame offsets in PSD px (x only). Timing doc: man's foot ~15 px,
# tortoise "one body-width" -- a full body-width (1463 px) would carry the
# head out of frame right, so the board uses a quarter body-width.
WALK_END_DX = {"woman": 27, "man": 34, "turtle": 366}

# --- Beats 1-3: the plate tortoise alone on white, offset up-left -----------
# The tortoise is the plate's own layer at plate scale (646x373 at HD). At its
# plate position (x 855-1501, claws y 935) there are 145 px under its feet, so
# the lockup cannot go there: the tortoise sits up-left in Beats 1-3 and the
# lockup goes low-centre under its plastron. Through the Beat 4 dissolve the
# tortoise translates (no scale) into the plate position.
HERO_LEFT, HERO_FEET_Y = 708, 600     # sprite left edge, claw line (top = 227)
LOCKUP_W, LOCKUP_TOP = 460, 645       # Asset 1@2x at 460 px = 322 px tall -> bottom y 967 (inside the centre-80 % logo-safe area)
LOCKUP_CX = W // 2

# --- Timing (24 fps) --------------------------------------------------------
DISSOLVE = (130, 173)                 # Beat 4: white -> park
HERO_SLIDE = (130, 168)               # tortoise slide, ease in-out, lands 5 f before the dissolve completes
LEASH_IN = (165, 173)                 # leash fades up last, once the collar is in place
WHIP = (274, 282)                     # park + couple push out frame-left
RETURN = (288, 306)                   # tortoise glides back to the Beat 1 position

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


def smoothstep(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def lerp(a, b, t):
    return round(a + (b - a) * t)


def plate_px(x, y):
    """PSD px -> HD px, matching fit_cover(build_plate(...))."""
    return round(x * PLATE_S) - PLATE_X0, round(y * PLATE_S)


def hero_positions(hero_hd):
    """(Beat 1 top-left, plate top-left) of the HD tortoise sprite."""
    tx, ty = plate_px(*LAYER_ORIGIN["turtle"])
    return (HERO_LEFT, HERO_FEET_Y - hero_hd.height), (tx, ty)


def paste_hero(canvas, hero_hd, pos):
    canvas.alpha_composite(hero_hd, pos)
    return canvas


def paste_lockup(canvas, lockup, width=LOCKUP_W, cx=LOCKUP_CX, top=LOCKUP_TOP, opacity=1.0):
    l = with_opacity(scale_to_width(lockup, width), opacity)
    canvas.alpha_composite(l, (cx - l.width // 2, top))
    return canvas


def extract_gold_type(wordmark):
    """Flat gold type from the rasterised vector lockup, no disc, cropped.

    fifth_avenue_wordmark.png renders as a white square with a transparent disc
    and gold type. Keep only gold-ish pixels (red well above blue), weighted so
    anti-aliased edges keep a soft alpha; paint them the mark's flat gold; drop
    the 2 px registration ticks at the square's edges and inside the disc with
    a small morphological open; crop to the type's bounds.
    """
    a = np.asarray(wordmark.convert("RGBA")).astype(np.float32)
    r, b, al = a[..., 0], a[..., 2], a[..., 3]
    strong = (al > 250) & (r - b > 90)
    gold = a[strong][:, :3].mean(axis=0)
    goldness = np.clip((r - b - 25) / (gold[0] - gold[2] - 25), 0, 1) * (al / 255)
    alpha = Image.fromarray((goldness * 255).astype(np.uint8), "L")
    keep = alpha.point(lambda v: 255 if v > 64 else 0).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.MaxFilter(9))
    alpha = Image.fromarray(np.minimum(np.asarray(alpha), np.asarray(keep)), "L")
    out = Image.new("RGBA", wordmark.size, tuple(int(v) for v in gold) + (0,))
    out.putalpha(alpha)
    return alpha_crop(out), tuple(int(v) for v in gold)


def load_plate_layers(up):
    """Return (background RGBA at PSD size, {name: layer RGBA}) or (None, layers)."""
    layers = {n: Image.open(up / f"{n}.png").convert("RGBA") for n in LAYER_ORDER}
    try:
        import logging
        logging.getLogger("psd_tools").setLevel(logging.ERROR)   # silence 'Unknown metadata key caiM'
        from psd_tools import PSDImage
    except ImportError:
        return None, layers
    psd = PSDImage.open(up / "turtlewalkers.psd")
    bg = next(l for l in psd if l.name == "background").topil().convert("RGBA")
    return bg, layers


def build_plate(bg, layers, dx=None, include=LAYER_ORDER):
    """Composite the walkers plate at PSD size, optionally shifting layers in x."""
    dx = dx or {}
    plate = bg.copy()
    for n in LAYER_ORDER:
        if n not in include:
            continue
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


def push_out(im, shift, blur=160, samples=16):
    """Push-whip: the image shifted left by `shift` px over white, with horizontal motion blur."""
    src = np.asarray(im.convert("RGB")).astype(np.float32)
    acc = np.zeros_like(src)
    for i in range(samples):
        s = shift + round((i / (samples - 1) - 0.5) * blur)
        canvas = np.full_like(src, 255.0)
        if s < W:
            canvas[:, :W - s] = src[:, s:]
        acc += canvas
    return Image.fromarray((acc / samples).astype(np.uint8), "RGB").convert("RGBA")


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    pull, out = (Path(a).expanduser().resolve() for a in sys.argv[1:3])
    out.mkdir(parents=True, exist_ok=True)
    up = pull / "5th ave hotel NYC" / "upscaled"
    repo = Path(__file__).resolve().parents[2]

    # gold lockup: Allen's textured render of the vector type (no disc)
    lockup = alpha_crop(Image.open(up / "Asset 1@2x.png").convert("RGBA"))
    # flat gold type from the vector lockup, saved as an asset for any flat use
    goldtype, gold_rgb = extract_gold_type(Image.open(repo / "assets" / "wordmarks" / "fifth_avenue_wordmark.png"))
    goldtype.save(out / "lockup_vector_goldtype.png", optimize=True)
    print(f"vector gold type: {goldtype.size[0]}x{goldtype.size[1]} RGBA, flat gold {gold_rgb} -> lockup_vector_goldtype.png")

    bg, layers = load_plate_layers(up)
    plate_note = ""
    if bg is not None:
        plate_hold = build_plate(bg, layers)
        plate_end = build_plate(bg, layers, WALK_END_DX)
        plate_no_tortoise = build_plate(bg, layers, include=("woman", "man"))
    else:
        plate_hold = plate_end = plate_no_tortoise = fit_cover(Image.open(up / "turtlewalkers.png").convert("RGBA"))
        plate_note = " (psd-tools missing: 4:3 turtlewalkers.png cropped to 16:9, not the PSD)"

    # hero = the plate's own tortoise layer at plate scale: identical render to Beats 4-6
    hero_hd = scale_to_width(layers["turtle"], round(layers["turtle"].width * PLATE_S))
    pos_hold, pos_plate = hero_positions(hero_hd)
    print(f"hero {hero_hd.size[0]}x{hero_hd.size[1]}: Beat 1 top-left {pos_hold} (claws y {HERO_FEET_Y}); "
          f"plate top-left {pos_plate} (claws y {pos_plate[1] + hero_hd.height}); slide {tuple(b - a for a, b in zip(pos_hold, pos_plate))} px")

    def frame01():
        return paste_hero(blank(), hero_hd, pos_hold)

    frames = []

    # 01 -- Beat 1 (f0-58): the gold tortoise alone on white; specular sweep + head-lift are motion notes
    frames.append(("01_hold", frame01()))

    # 02 -- Beat 2 (f58-101): gold lockup, no disc, low-centre under the plastron
    frames.append(("02_lockup", paste_lockup(frame01(), lockup)))

    # 03 -- Beat 3 (f101-130): lockup on its way out (35 %, +3 % scale), tortoise unchanged
    f = paste_lockup(frame01(), lockup, width=round(LOCKUP_W * 1.03), opacity=0.35)
    tag(f, "MID FADE f115 (f101-118): lockup at 35 %, +3 % scale, tortoise unchanged")
    frames.append(("03_lockup_out", f))

    # 04 -- Beat 4 (f130-173): white -> park dissolve under the tortoise, which slides into its plate position
    fr = 152
    t_d = (fr - DISSOLVE[0]) / (DISSOLVE[1] - DISSOLVE[0])
    t_s = smoothstep((fr - HERO_SLIDE[0]) / (HERO_SLIDE[1] - HERO_SLIDE[0]))
    f = Image.blend(blank(), plate_no_tortoise, t_d)
    paste_hero(f, hero_hd, (lerp(pos_hold[0], pos_plate[0], t_s), lerp(pos_hold[1], pos_plate[1], t_s)))
    tag(f, f"MID-DISSOLVE f{fr}: park at {round(t_d * 100)} % under the tortoise, which slides down-right "
           f"(f{HERO_SLIDE[0]}-{HERO_SLIDE[1]}, ease in-out, {round(t_s * 100)} % here) into its plate position. "
           f"Leash fades up f{LEASH_IN[0]}-{LEASH_IN[1]} once the collar has landed" + plate_note)
    frames.append(("04_reveal", f))

    # 05 -- Beat 5a (f173): the walk, start frame = the full plate, layers at PSD positions
    f = plate_hold.copy()
    if plate_note:
        tag(f, "PLATE" + plate_note)
    frames.append(("05_walk_start", f))

    # 06 -- Beat 5b (f274): the walk, end frame -- TO GENERATE; layers offset as the conform target
    f = plate_end.copy()
    tag(f, "TO GENERATE (KLING) - end frame of the 1/6-speed walk. Shown: PSD layers offset "
           "(man +15 px, woman +12 px, tortoise +162 px, leash stretched) as a conform target" + plate_note)
    frames.append(("06_walk_end_TOGEN", f))

    # 07 -- Beat 6 (f274-282): the park + couple push-whip out frame-left; the tortoise layer stays put
    fr = 278
    t_w = (fr - WHIP[0]) / (WHIP[1] - WHIP[0])
    park = build_plate(bg, layers, WALK_END_DX, include=("woman", "man", "leash")) if bg is not None else plate_end
    f = push_out(park, round(W * t_w))
    paste_hero(f, hero_hd, pos_plate)
    tag(f, f"MID-WHIP f{fr} (f{WHIP[0]}-{WHIP[1]}): park, couple and leash push out frame-left with motion blur; "
           "the tortoise is a separate layer above and does not move" + plate_note)
    frames.append(("07_whip", f))

    # 08 -- Beat 6 (f282-288): white, tortoise alone at its plate position
    frames.append(("08_white_hold", paste_hero(blank(), hero_hd, pos_plate)))

    # 09 -- Return (f288-306): tortoise glides up-left to the Beat 1 position
    fr = 297
    t_r = smoothstep((fr - RETURN[0]) / (RETURN[1] - RETURN[0]))
    f = paste_hero(blank(), hero_hd, (lerp(pos_plate[0], pos_hold[0], t_r), lerp(pos_plate[1], pos_hold[1], t_r)))
    tag(f, f"MID-RETURN f{fr} (f{RETURN[0]}-{RETURN[1]}, ease in-out): tortoise glides up-left, no scale, to the Beat 1 position")
    frames.append(("09_return", f))

    # 10 -- Loop (f306-312): identical to frame 01
    loop = frame01()
    assert np.array_equal(np.asarray(loop), np.asarray(frames[0][1])), "loop frame differs from frame 01"
    frames.append(("10_loop", loop))

    for name, im in frames:
        im.convert("RGB").save(out / f"{name}.png", optimize=True)
        im.convert("RGB").resize((960, 540), Image.LANCZOS).save(out / f"{name}_small.jpg", quality=88)

    # contact sheet: 4 columns
    cols, tw_, th, gap = 4, 464, 261, 16
    rows = (len(frames) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw_ + (cols + 1) * gap, rows * (th + 40) + (rows + 1) * gap), (16, 16, 16))
    d = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(frames):
        r_, c = divmod(i, cols)
        x, y = gap + c * (tw_ + gap), gap + r_ * (th + 40 + gap)
        sheet.paste(im.convert("RGB").resize((tw_, th), Image.LANCZOS), (x, y))
        d.text((x, y + th + 8), name.replace("_", " "), font=font(22), fill=(255, 176, 32))
    sheet.save(out / "contact_sheet.jpg", quality=88)
    print(f"{len(frames)} frames -> {out}; loop frame 10 == frame 01 verified")


if __name__ == "__main__":
    main()
