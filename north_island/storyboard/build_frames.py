#!/usr/bin/env python3
"""Build the North Island (Seychelles) storyboard frames — v2.

Composites eight 1920x1080 frames (one per storyboard beat, two beats get an
extra frame) from the plates in a local pull of the Drive folder, plus a
contact sheet. Frames that stand in for shots still to be generated or comped
are tagged in the corner.

Boarded to theria_hotel_animations_timing_v1.md §5 (24 fps, 13.0 s, 6 shots,
final frame = frame 0 so the film loops). One master, 16:9 1920x1080.

Usage:
    python north_island/storyboard/build_frames.py PULL_ROOT OUT_DIR

PULL_ROOT  local mirror of the Drive folder (tools/drive_pull.py); the plates
           are read from PULL_ROOT/"North Island"/. Nothing under it is written.
OUT_DIR    where the PNG frames, *_small.jpg previews and contact_sheet.jpg go

Requires Pillow. Layout constants are at the top; change W/H for other masters.

v2 changes
- Water beats use northisland.png (3072x2048), the 2x re-render of the
  7e26a98a lock-up (same composition: mean abs diff 3.5/255 after resize,
  gold-mask IoU 0.89, identical bounding boxes). Sharper on the 1080p master.
- Lock-up plates (white + water) are FIT BY HEIGHT (1620x1080, centred), not
  cover-cropped: v1's cover crop cut the top-right turtle and the big turtle's
  rear flippers at the frame edge. White plate: pillars are white (invisible).
  Water plate: the outer 150 px each side are filled on the board by
  mirror-tiling a gold-free strip of the plate's own edge, as a stand-in for a
  generative expand of the raster in comp.
- Beach plate stays a cover crop biased down (loses 115 source rows of sky).
- Wordmark is baked into both lock-up plates; accepted. It is masked/held in
  comp over the Kling shots. No "regenerate clean" tags.
- Turtle count is five. The beach plate (three turtles) is used as-is on the
  landfall frames with a note that two more are comped from water-plate
  cut-outs.
"""
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps

W, H = 1920, 1080
REF_W, REF_H = 1536, 1024          # reference plate space for crop offsets
SMALL = (960, 540)

WHITE = "b261916d-7215-4f97-8607-d091aabe911a.png"   # 1536x1024, turtles + wordmark on white
WATER = "northisland.png"                            # 3072x2048, same lock-up over turquoise (2x)
WATER_1X = "7e26a98a-718f-43e1-8719-c7f930b25af3.png" # 1536x1024, the 1x original (not used in frames)
BEACH = "0873e031-511a-499b-a9d5-8a2b7a701d87.png"   # 1536x1024, three turtles on the sand
MARK = "download.jpg"                                # house mark, 225x121 (not used in frames)

PLATE_SIZE = {WHITE: (1536, 1024), WATER: (3072, 2048), BEACH: (1536, 1024)}

# Beach plate: top of the 16:9 cover-crop window in REFERENCE (1024-row) space.
# Cover scale is 1.25, so the window is 864 reference rows tall. The turtles
# sit in rows 96-979 with only sky above, so bias the crop down and lose sky.
BEACH_CROP_TOP = REF_H - 864 - 45   # 115

FONT = next((p for p in [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
] if Path(p).exists()), None)


def font(size):
    return ImageFont.truetype(FONT, size) if FONT else ImageFont.load_default()


def fit_cover(im, top_ref, w=W, h=H):
    """Scale to cover w x h and crop. `top_ref` is the crop's top edge in
    REFERENCE (1024-row) space, so the same number works for a 1x or 2x plate."""
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - w) // 2
    y = round(top_ref * (im.height / (REF_H * s)) * s)
    y = max(0, min(y, im.height - h))
    return im.crop((x, y, x + w, y + h))


def fit_height(im, fill=None, clean_rows=None, w=W, h=H):
    """Scale to h tall, centre horizontally. Pillars are `fill` (a colour) or,
    if None, built from the plate's own outer columns: `clean_rows` =
    (left_rows, right_rows) is how many rows from the top of each outer column
    are free of gold; that strip is mirror-tiled down the pillar. A board
    stand-in for a generative expand of the raster in comp. Returns (frame, pad)."""
    s = h / im.height
    im = im.resize((round(im.width * s), h), Image.LANCZOS)
    pad = (w - im.width) // 2
    if fill is not None:
        out = Image.new("RGBA", (w, h), fill)
    else:
        out = Image.new("RGBA", (w, h))
        lrows, rrows = clean_rows
        strips = [(im.crop((0, 0, pad, lrows)), 0),
                  (im.crop((im.width - (w - pad - im.width), 0, im.width, rrows)), pad + im.width)]
        for strip, x in strips:
            y, flip = 0, False
            while y < h:
                out.paste(ImageOps.flip(strip) if flip else strip, (x, y))
                y += strip.height
                flip = not flip
    out.paste(im, (pad, 0))
    return out, pad


TAG_MAX_W = 1180   # keeps tags clear of the turtles (top-right turtle starts x>=1400 on the fit-height lock-up)


def tag(im, text, colour=(255, 176, 32), line=0):
    """Corner tag, top-left. `line` stacks a second/third tag under the first;
    three lines end at y=196, above the small top-left turtle (y>=250 on the
    fit-height lock-up)."""
    assert line <= 2, "max three tag lines (would cover the small turtle)"
    d = ImageDraw.Draw(im)
    f = font(26)
    tw = d.textlength(text, font=f)
    assert 24 + tw + 28 <= TAG_MAX_W, f"tag too wide ({int(tw)} px, max text ~{TAG_MAX_W - 52}): {text}"
    y = 24 + line * 60
    d.rectangle((24, y, 24 + tw + 28, y + 52), fill=(0, 0, 0, 220))
    d.text((38, y + 10), text, font=f, fill=colour)


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
        assert im.size == PLATE_SIZE[name], f"{name}: expected {PLATE_SIZE[name]}, got {im.size}"
        return im

    white, pad = fit_height(load(WHITE), fill=(255, 255, 255, 255))
    # outer 150 px columns of the scaled water plate are gold-free for the top
    # 230 rows (left: small turtle starts y~250) / 380 rows (right: the "d" and
    # "ES" of the wordmark start y~400).
    water, pad_w = fit_height(load(WATER), clean_rows=(230, 380))
    assert pad == pad_w == 150, (pad, pad_w)
    beach = fit_cover(load(BEACH), top_ref=BEACH_CROP_TOP)
    for name in (WATER_1X, MARK):
        assert (ni / name).exists(), f"{name} missing from pull"

    WM_TAG = "WORDMARK BAKED IN (accepted) — mask/hold it in comp over Kling"
    FIT_TAG = "LOCK-UP FIT-HEIGHT 1620x1080 — no turtle clipped; white pillars"
    EXT_TAG = "WATER +150 px each side: tiled from plate here; gen-expand raster in comp"

    frames = []

    # 01 — Shot 1 (f0-53): the lock-up on white, dead still. b261916d exactly.
    f = white.copy()
    tag(f, "READY — b261916d as shot; shell highlight sweep f24-48 in AE")
    tag(f, WM_TAG, line=1)
    tag(f, FIT_TAG, line=2)
    frames.append(("01_hold", f))

    # 02 — Shot 2 (f53-96): white becomes water. Shown as a 50 % blend of the
    # two lock-up plates; the real move is a bottom-up flood over 1.2 s.
    f = blend(white, water, 0.5)
    tag(f, "COMP (AE) — water floods BOTTOM-UP 1.2 s; 50% b261916d/northisland")
    tag(f, "PLATES NOT PIXEL-LOCKED — turtles/type drift 5-11 px; comp as layers", line=1)
    frames.append(("02_flood_COMP", f))

    # 03 — Shot 3 (f96-168): they start to swim. Kling from northisland.png.
    f = water.copy()
    tag(f, "TO GENERATE (KLING) — flippers, drift right ~15%; start northisland.png")
    tag(f, WM_TAG, line=1)
    tag(f, EXT_TAG, line=2)
    frames.append(("03_swim_TOGEN", f))

    # 04 — Shot 4a (f168-197): water shallows out to sand, beach fades up.
    f = blend(water, beach, 0.5)
    tag(f, "COMP + KLING — turquoise to sand 1.2 s; 50% northisland/0873e031")
    tag(f, "5 TURTLES — beach plate has 3; +2 comped from water-plate cut-outs", line=1)
    frames.append(("04_landfall_COMP", f))

    # 05 — Shot 4b (f197-226): landed. 0873e031 as-is (three turtles).
    f = beach.copy()
    tag(f, "TO GENERATE (KLING) — swim to heavy crawl f190; plate 0873e031 as-is")
    tag(f, "+2 turtles comped from water-plate cut-outs (5 on the sand)", line=1)
    tag(f, "3:2 COVER-CROP biased down — loses 115 px of sky only", line=2)
    frames.append(("05_sand", f))

    # 06 — Shot 5 (f226-274): turn and return. Beach dissolving back to water.
    f = blend(beach, water, 0.5)
    tag(f, "TO GENERATE (KLING) + COMP — turn back, sand to turquoise")
    tag(f, "shown 50% 0873e031/northisland; end in lock-up positions for loop", line=1)
    frames.append(("06_return_COMP", f))

    # 07 — Shot 6a (f274-298): back to blue, back to white. Water drains to white top-down.
    f = blend(water, white, 0.5)
    tag(f, "COMP (AE) — water to white TOP-DOWN 1.0 s; wordmark held throughout")
    tag(f, "shown 50% northisland/b261916d", line=1)
    frames.append(("07_whiteout_COMP", f))

    # 08 — Shot 6b (f312): final frame = frame 0. Same pixels as 01.
    f = white.copy()
    tag(f, "LOOP POINT — final frame f312 = frame 0 (same pixels as 01_hold)")
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
