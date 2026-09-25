#!/usr/bin/env python3
"""Build the North Island (Seychelles) storyboard frames from the real assets.

Composites eight 1920x1080 frames (one per storyboard beat, two beats get an
extra frame) from the three 1536x1024 plates in a local pull of the Drive
folder, plus a contact sheet. Frames that stand in for shots still to be
generated or comped are tagged in the corner.

Boarded to theria_hotel_animations_timing_v1.md §5 (24 fps, 13.0 s, 6 shots,
final frame = frame 0 so the film loops).

Usage:
    python north_island/storyboard/build_frames.py PULL_ROOT OUT_DIR

PULL_ROOT  local mirror of the Drive folder (tools/drive_pull.py); the plates
           are read from PULL_ROOT/"North Island"/. Nothing under it is written.
OUT_DIR    where the PNG frames, *_small.jpg previews and contact_sheet.jpg go

Requires Pillow. Layout constants are at the top; change W/H for other masters.

Crop note: the plates are 3:2. Scaling to cover 16:9 keeps 864 of 1024 source
rows. On the two logo plates the turtles span rows 21-1004, so a centred crop
clips ~60 px off the top-right turtle and ~60 px off the big turtle's rear
flippers. The beach plate's turtles end at row 979 with only sky above, so its
crop is biased downward and loses nothing but sky. All three are tagged.
"""
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont

W, H = 1920, 1080
PLATE_W, PLATE_H = 1536, 1024
SMALL = (960, 540)

# Source-space top offset of the 16:9 crop window for each plate (see docstring).
# Cover scale is 1.25, so the window is 864 source rows tall.
CROP_TOP = {
    "logo": (PLATE_H - 864) // 2,   # 80: centred, balances the clipping top/bottom
    "beach": PLATE_H - 864 - 45,    # 115: keep the turtles (rows 96-979), lose sky
}

WHITE = "b261916d-7215-4f97-8607-d091aabe911a.png"   # turtles + wordmark on white
WATER = "7e26a98a-718f-43e1-8719-c7f930b25af3.png"   # same lock-up over turquoise
BEACH = "0873e031-511a-499b-a9d5-8a2b7a701d87.png"   # turtles on the sand
MARK = "download.jpg"                                # house mark, 225x121 (not used in frames)

FONT = next((p for p in [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
] if Path(p).exists()), None)


def font(size):
    return ImageFont.truetype(FONT, size) if FONT else ImageFont.load_default()


def fit_cover(im, w=W, h=H, top=None):
    """Scale to cover w x h and crop. `top` is the crop's top edge in SOURCE
    pixels; default centres the crop (same as the Giraffe Manor helper)."""
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - w) // 2
    y = (im.height - h) // 2 if top is None else round(top * s)
    y = max(0, min(y, im.height - h))
    return im.crop((x, y, x + w, y + h))


def tag(im, text, colour=(255, 176, 32), line=0):
    """Corner tag. `line` stacks a second/third tag under the first."""
    d = ImageDraw.Draw(im)
    f = font(30)
    tw = d.textlength(text, font=f)
    assert 24 + tw + 28 <= im.width - 24, f"tag overflows frame ({int(tw)} px): {text}"
    y = 24 + line * 60
    d.rectangle((24, y, 24 + tw + 28, y + 52), fill=(0, 0, 0, 220))
    d.text((38, y + 8), text, font=f, fill=colour)


def blend(a, b, t):
    """t=0 -> a, t=1 -> b. Both already 1920x1080 RGBA."""
    return Image.blend(a, b, t)


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    pull, out = (Path(a).expanduser().resolve() for a in sys.argv[1:3])
    out.mkdir(parents=True, exist_ok=True)
    ni = pull / "North Island"

    def load(name):
        im = Image.open(ni / name).convert("RGBA")
        assert im.size == (PLATE_W, PLATE_H), f"{name}: expected {PLATE_W}x{PLATE_H}, got {im.size}"
        return im

    white = fit_cover(load(WHITE), top=CROP_TOP["logo"])
    water = fit_cover(load(WATER), top=CROP_TOP["logo"])
    beach = fit_cover(load(BEACH), top=CROP_TOP["beach"])
    assert (ni / MARK).exists(), f"house mark {MARK} missing from pull"

    CROP_TAG = "3:2 COVER-CROP clips top-right turtle + big turtle flippers (~60 px) — outpaint to 16:9 (NBP)"
    WM_TAG = "WORDMARK IS BURNED INTO THE PLATE — regenerate clean (NBP), wordmark as AE layer"

    frames = []

    # 01 — Shot 1 (f0-53): the lock-up on white, dead still. b261916d exactly.
    f = white.copy()
    tag(f, "READY — b261916d as shot; only a shell highlight sweep f24-48 (AE)")
    tag(f, WM_TAG, line=1)
    tag(f, CROP_TAG, line=2)
    frames.append(("01_hold", f))

    # 02 — Shot 2 (f53-96): white becomes water. Shown as a 50 % blend of the
    # two lock-up plates; the real move is a bottom-up flood over 1.2 s.
    f = blend(white, water, 0.5)
    tag(f, "COMP (AE) — turquoise floods bottom-up 1.2 s; shown: 50% blend b261916d/7e26a98a")
    tag(f, "Turtles + wordmark must stay pixel-locked between the two plates (they do)", line=1)
    frames.append(("02_flood_COMP", f))

    # 03 — Shot 3 (f96-168): they start to swim. Kling from 7e26a98a.
    f = water.copy()
    tag(f, "TO GENERATE (KLING) — flippers, drift right ~15% of frame; shown: 7e26a98a start frame")
    tag(f, "WORDMARK will not survive Kling — fade it as an AE layer from f150 (needs clean plate)", line=1)
    frames.append(("03_swim_TOGEN", f))

    # 04 — Shot 4a (f168-197): water shallows out to sand, beach fades up.
    f = blend(water, beach, 0.5)
    tag(f, "COMP + KLING — turquoise ramps to sand 1.2 s, island fades up; shown: 50% blend 7e26a98a/0873e031")
    tag(f, "NOTE: 5 turtles in the water plate, 3 on the beach plate — positions do not match", line=1)
    frames.append(("04_landfall_COMP", f))

    # 05 — Shot 4b (f197-226): landed. 0873e031 exactly.
    f = beach.copy()
    tag(f, "TO GENERATE (KLING) — flipper cycle changes to a heavy crawl f190; shown: 0873e031 landing plate")
    tag(f, "3:2 PLATE COVER-CROPPED — crop biased down, loses 115 px of sky only", line=1)
    frames.append(("05_sand", f))

    # 06 — Shot 5 (f226-274): turn and return. Beach dissolving back to water.
    f = blend(beach, water, 0.5)
    tag(f, "TO GENERATE (KLING) + COMP — turtles turn back, sand to turquoise; 50% blend 0873e031/7e26a98a")
    tag(f, "Turtles must arrive back in their 7e26a98a positions for the loop", line=1)
    frames.append(("06_return_COMP", f))

    # 07 — Shot 6a (f274-298): back to blue, back to white. Water drains to white top-down.
    f = blend(water, white, 0.5)
    tag(f, "COMP (AE) — water to white top-down 1.0 s, wordmark fades back up; 50% blend 7e26a98a/b261916d")
    frames.append(("07_whiteout_COMP", f))

    # 08 — Shot 6b (f312): final frame = frame 0. Same pixels as 01.
    f = white.copy()
    tag(f, "LOOP POINT — final frame f312 = frame 0 (identical pixels to 01_hold)")
    frames.append(("08_loop", f))

    for name, im in frames:
        im.convert("RGB").save(out / f"{name}.png", optimize=True)
        im.convert("RGB").resize(SMALL, Image.LANCZOS).save(out / f"{name}_small.jpg", quality=88)

    # contact sheet: 4 columns x 2 rows
    cols, tw, th, gap = 4, 620, 349, 16
    rows = (len(frames) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * gap, rows * (th + 40) + (rows + 1) * gap), (16, 16, 16))
    d = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(frames):
        r, c = divmod(i, cols)
        x, y = gap + c * (tw + gap), gap + r * (th + 40 + gap)
        sheet.paste(im.convert("RGB").resize((tw, th), Image.LANCZOS), (x, y))
        d.text((x, y + th + 8), name.replace("_", " "), font=font(22), fill=(255, 176, 32))
    sheet.save(out / "contact_sheet.jpg", quality=88)

    # loop check: first and last frame must be identical below the tag band (y >= 220)
    band = (0, 220, W, H)
    diff = ImageChops.difference(frames[0][1].convert("RGB").crop(band),
                                 frames[-1][1].convert("RGB").crop(band)).getbbox()
    print(f"{len(frames)} frames -> {out}")
    print("loop check 01_hold vs 08_loop (below tag band):", "IDENTICAL" if diff is None else f"DIFFER at {diff}")
    assert diff is None, "loop frames differ"


if __name__ == "__main__":
    main()
