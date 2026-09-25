#!/usr/bin/env python3
"""Build the Airelles Le Grand Contrôle (Versailles) storyboard frames from the real assets.

Composites nine 1920x1080 frames — one per timing-doc beat, two for the salon
reveal — from files in a local pull of the Drive folder, plus a 3x3 contact
sheet. Frames that stand in for shots still to be generated or comped are
tagged in the corner. Nothing under PULL_ROOT is modified.

Usage:
    python versailles/storyboard/build_frames.py PULL_ROOT OUT_DIR

PULL_ROOT  local mirror of the Drive folder (contains Versali/)
OUT_DIR    where the PNG frames, *_small.jpg and contact_sheet.jpg go

What the Versali files actually contain (checked by eye 2026-09-25 — the
timing doc, pipeline doc and this task's brief all describe them wrong):
    965d5f9a  cake on gilt table under the GUILLOTINE, blade raised, salon   (RGB 1023x1537)
    fd1e32ee  cake on gilt table under the CHANDELIER, same salon            (RGB 1024x1536)
    cfb72e66  cake + CHANDELIER isolated, real alpha (max 254, no bg)        (RGBA 1024x1536)
    4ad9ad80  blade DOWN through the cake, slices plated round the table     (RGB 1023x1537)
    1651551468329.webp  Hall of Mirrors, wide                                (RGB 1170x780)
    images copy.jpg     AIRELLES / LE GRAND CONTRÔLE / CHÂTEAU DE VERSAILLES wordmark (447x447 JPG, cream bg)
    images.jpg          guillotine on white, NOT the wordmark                (554x554 JPG)

All hero plates are portrait 2:3. They are letterboxed at full height on a
sampled-and-darkened wall colour, never stretched or cropped, and tagged for
outpaint. The wordmark is a plain 2x Lanczos resize of the JPG, luma-keyed so
it sits on the parquet — a tagged placeholder until vector art arrives.

Requires Pillow. Layout constants are at the top; change W/H for other masters.
"""
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

W, H = 1920, 1080
BLACK = (0, 0, 0, 255)
PLATE_TAG = "PORTRAIT PLATE — outpaint to 16:9 pending (Seedream 4.5)"
LOGO_TAG = "WORDMARK = 447 px JPG AT 2x (Lanczos), luma-keyed — PLACEHOLDER UNTIL VECTOR"
WORDMARK_GOLD = (232, 208, 150, 255)   # warm gold-cream so it reads on the parquet
WORDMARK_W = 240      # on-canvas width: the clear parquet between the front feet is ~260 px
WORDMARK_TOP = 962    # sits on the parquet between the front feet (foot line ~1040)
ENDCARD_W = 760

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


def tag(im, text, colour=(255, 176, 32), row=0):
    """Corner tag; row=1 stacks a second tag under the first."""
    d = ImageDraw.Draw(im)
    f = font(30)
    tw = d.textlength(text, font=f)
    y = 24 + row * 60
    d.rectangle((24, y, 24 + tw + 28, y + 52), fill=(0, 0, 0, 220))
    d.text((38, y + 8), text, font=f, fill=colour)


def blank(colour=BLACK):
    return Image.new("RGBA", (W, H), colour)


def wall_colour(plate, dark=0.45):
    """Mean colour of the plate's outer columns, darkened — pillar fill for letterboxing."""
    edge = plate.width // 20
    strip = Image.new("RGB", (edge * 2, plate.height))
    strip.paste(plate.convert("RGB").crop((0, 0, edge, plate.height)), (0, 0))
    strip.paste(plate.convert("RGB").crop((plate.width - edge, 0, plate.width, plate.height)), (edge, 0))
    r, g, b = strip.resize((1, 1), Image.BOX).getpixel((0, 0))
    return (round(r * dark), round(g * dark), round(b * dark), 255)


def letterbox(plate, fill=None):
    """Portrait plate at full canvas height, centred, pillars in `fill` (default: sampled wall)."""
    s = H / plate.height
    p = plate.convert("RGBA").resize((round(plate.width * s), H), Image.LANCZOS)
    canvas = blank(fill or wall_colour(plate))
    canvas.alpha_composite(p, ((W - p.width) // 2, 0))
    return canvas, ((W - p.width) // 2, p.width)


def stops(im, ev):
    """Exposure change in stops (negative = darker). Board approximation of the AE grade."""
    return ImageEnhance.Brightness(im.convert("RGB")).enhance(2 ** ev).convert("RGBA")


def wordmark_layer(jpg):
    """2x Lanczos of the JPG wordmark -> luma-keyed RGBA in WORDMARK_GOLD, cropped to the type.

    This is the one enlargement Allen allows (plain 2x resize, no AI). The JPG has
    dark type on a cream field; the key inverts luma so only the letterforms carry alpha.
    """
    big = jpg.convert("L").resize((jpg.width * 2, jpg.height * 2), Image.LANCZOS)
    big = big.crop((8, 8, big.width - 8, big.height - 8))   # JPG has a dark right/bottom edge
    a = ImageOps.invert(big).point(lambda v: 0 if v < 60 else min(255, int((v - 60) * 1.6)))
    layer = Image.new("RGBA", big.size, WORDMARK_GOLD)
    layer.putalpha(a)
    return layer.crop(a.getbbox())


def paste_wordmark(canvas, mark, width=WORDMARK_W, cx=W // 2, top=WORDMARK_TOP, opacity=1.0):
    s = width / mark.width
    m = mark.resize((width, round(mark.height * s)), Image.LANCZOS)
    if opacity < 1.0:
        m.putalpha(m.getchannel("A").point(lambda v: int(v * opacity)))
    canvas.alpha_composite(m, (cx - width // 2, top))
    return canvas


def radial_reveal(canvas, cx, cy, r_in, r_out):
    """Multiply the canvas by a soft radial mask: fully visible inside r_in, black beyond r_out."""
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    steps = 24
    for i in range(steps, -1, -1):
        r = r_in + (r_out - r_in) * i / steps
        v = round(255 * (1 - i / steps))
        d.ellipse((cx - r, cy - r * 0.8, cx + r, cy + r * 0.8), fill=v)
    mask = mask.filter(ImageFilter.GaussianBlur(30))
    out = blank()
    out.paste(canvas, (0, 0), mask)
    return out


def main():
    pull, out = (Path(a).expanduser().resolve() for a in sys.argv[1:3])
    out.mkdir(parents=True, exist_ok=True)
    v = pull / "Versali"
    chandelier_salon = Image.open(v / "fd1e32ee-80ef-4d63-9d10-59e07f81e997.png").convert("RGB")
    guillotine_salon = Image.open(v / "965d5f9a-d71a-4435-b487-cfabab3a0186.png").convert("RGB")
    elements = Image.open(v / "cfb72e66-8752-47fc-8f43-2f824eeb0f1d.png").convert("RGBA")
    plated = Image.open(v / "4ad9ad80-ccba-4b14-8cd7-b85c4eb54f27.png").convert("RGB")
    hall = Image.open(v / "1651551468329.webp").convert("RGB")
    mark = wordmark_layer(Image.open(v / "images copy.jpg"))

    # the three salon plates differ by 1 px in each axis; conform to the chandelier plate
    guillotine_salon = guillotine_salon.resize(chandelier_salon.size, Image.LANCZOS)
    plated = plated.resize(chandelier_salon.size, Image.LANCZOS)
    wall = wall_colour(chandelier_salon)   # one pillar colour for every salon frame

    frames = []

    # 01 — Shot 1 (00.0–02.2): cake + chandelier on black, nothing else. Real cut-out, real alpha.
    f, _ = letterbox(elements, fill=BLACK)
    tag(f, "ELEMENT cfb72e66 on black — READY (candle flicker + caustics = Kling O1 or AE)")
    frames.append(("01_black_open", f))

    # 02a — Shot 2 mid-reveal (~03.0): salon fading up from black, outward from the cake
    f, _ = letterbox(chandelier_salon, fill=BLACK)
    f = radial_reveal(f, W // 2, 620, 260, 700)
    tag(f, "COMP (AE) — salon fades up from centre outward, ~1.4 s. Shown: fd1e32ee under radial mask")
    frames.append(("02a_salon_reveal", f))

    # 02b — Shot 2 end (04.4): the salon whole
    f, _ = letterbox(chandelier_salon, fill=wall)
    tag(f, PLATE_TAG)
    tag(f, "PLATE fd1e32ee — READY", row=1)
    frames.append(("02b_salon", f))

    # 03 — Shot 3 (04.4–06.2): wordmark fades up on the parquet under the table
    f, _ = letterbox(chandelier_salon, fill=wall)
    paste_wordmark(f, mark)
    tag(f, PLATE_TAG)
    tag(f, LOGO_TAG, row=1)
    frames.append(("03_wordmark", f))

    # 04 — Shot 4 (06.2–08.8): the turn. Mid-morph = 50 % blend of the two salon plates,
    #      room already ~0.75 stop down (half of the 1.5-stop drop). Wordmark still up.
    f = Image.blend(chandelier_salon, guillotine_salon, 0.5)
    f, _ = letterbox(stops(f, -0.75), fill=wall_colour(chandelier_salon, 0.30))
    paste_wordmark(f, mark)
    tag(f, "COMP (AE) — chandelier→guillotine morph. Shown: 50 % blend fd1e32ee / 965d5f9a")
    tag(f, "NOTE: the two salon plates do NOT register (walls/doors ghost) — see STORYBOARD.md", row=1)
    frames.append(("04_morph_COMP", f))

    # 05 — Shot 5 (08.8–09.8): logo out, guillotine raised, room 1.5 stops down, total stillness
    f, _ = letterbox(stops(guillotine_salon, -1.0), fill=wall_colour(chandelier_salon, 0.20))
    tag(f, "PLATE 965d5f9a — READY. Grade = AE (doc: -1.5 stop; shown -1.0 so the board reads) + wordmark fade")
    tag(f, PLATE_TAG, row=1)
    frames.append(("05_still", f))

    # 06 — Shot 6 (09.8–10.6): the drop. Impact frame with the 3-frame white flash and 4 px shake.
    #      4ad9ad80 has the blade through the cake; its plated slices belong to Shot 7 — ignore here.
    f, _ = letterbox(stops(plated, -1.5), fill=BLACK)
    shaken = blank()
    shaken.alpha_composite(f, (4, -3))
    flash = Image.blend(shaken, blank((255, 255, 255, 255)), 0.35)
    tag(flash, "COMP (AE) — blade falls in 8 f, white flash f246, 4 px shake. Shown: 4ad9ad80 at impact")
    tag(flash, "NOTE: plated slices in this plate arrive in Shot 7, not here", row=1)
    frames.append(("06_drop_COMP", flash))

    # 07 — Shot 7 (10.6–13.6): cake apart, slices assemble to their plates, light back up 1 stop
    f, _ = letterbox(stops(plated, -0.5), fill=wall_colour(plated, 0.35))
    tag(f, "PLATE 4ad9ad80 — READY. Slices sliding out to plates = TO GENERATE (Kling O1) or AE")
    tag(f, PLATE_TAG, row=1)
    frames.append(("07_served", f))

    # 08 — Shot 8 (13.6–15.0): end card — Hall of Mirrors wide, wordmark centre
    f = fit_cover(hall).convert("RGBA")
    f = stops(f, -0.9)
    f = ImageEnhance.Color(f.convert("RGB")).enhance(0.85).convert("RGBA")
    m = mark.resize((ENDCARD_W, round(mark.height * ENDCARD_W / mark.width)), Image.LANCZOS)
    f.alpha_composite(m, ((W - ENDCARD_W) // 2, (H - m.height) // 2 + 40))
    tag(f, "HALL OF MIRRORS 1170 px source, 1.64x to cover — soft; Seedream re-render pending")
    tag(f, LOGO_TAG, row=1)
    frames.append(("08_endcard", f))

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
