#!/usr/bin/env python3
"""Build the Necker Island storyboard frames — v2, built from the real photo set.

v1 was a schematic (no art existed). Allen has since uploaded the Necker photo
set and a flamingo cut-out, so every frame here is now a real plate or the real
cut-out, with only the things that genuinely do not exist yet tagged
TO GENERATE / TO BE REPLACED and the model named.

Usage:
    python necker_island/storyboard/build_frames.py PULL_ROOT OUT_DIR

PULL_ROOT  local mirror of the Drive folder (tools/drive_pull.py); read-only.
           Photos live in PULL_ROOT/"Necker Island"/ under the local names
           (drive/manifest.json maps them to the Drive titles).
OUT_DIR    where the PNG frames, *_small.jpg and contact_sheet.jpg go

Loop rule (Allen): last frame = first frame (flamingo alone on white). Beats
1–6 keep the v1 timings (14.0 s); a 1.5 s landing beat is added so the film
returns to its opening pose. TRT 15.5 s = f372 @ 24 fps.

Photos are 5–9k px / ~20 MB each: they are opened with Image.draft so the JPEG
decoder only produces what the board needs. Source dims are measured and
printed. Helpers (font, fit_cover, alpha_crop, tag, paste_logo, thirds, note,
footer, arrow) keep their v1 / giraffe_manor names. Requires Pillow + numpy.
"""
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

Image.MAX_IMAGE_PIXELS = None

W, H = 1920, 1080
FPS = 24
WHITE = (255, 255, 255, 255)
INK = (40, 40, 40, 255)
GUIDE = (0, 0, 0, 40)
NOTE = (30, 30, 30, 255)
ARC = (200, 60, 90, 255)          # flamingo motion arcs
RED = (225, 40, 40, 255)          # replace / remove boxes
AMBER = (255, 176, 32)            # tag text
BALL = (220, 240, 60, 255)

FONT = next((p for p in [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
] if Path(p).exists()), None)

# Source-fraction boxes measured on the photos (x0, y0, x1, y1 as fractions of the source).
RIDER_BOX = (0.19, 0.36, 0.42, 0.88)          # necker_kitesurfing_01: the real rider + board
PLAYER_BOX = (0.40, 0.26, 0.56, 0.80)         # necker_tennis_03: the real player (+ her shadow)
FLIGHT_BIRD = (0.189, 0.067, 0.322, 0.208)    # necker_flamingos_08: single clean bird, top-left of the flock
FLIGHT_REF = (0.15, 0.03, 0.42, 0.30)         # necker_flamingos_08: two-bird reference crop
KITER_REF = (0.76, 0.57, 0.97, 0.74)          # necker_watersports_aerial_02: distant kiter in the bay
LEMUR_A = (0.22, 0.18, 0.69, 1.00)            # necker_lemur_01: ring-tail on the branch
LEMUR_B = (0.10, 0.23, 0.52, 0.73)            # necker_lemur_08: black-and-white ruffed on the rock


# ---------------------------------------------------------------- helpers (v1 / giraffe_manor names)
def font(size):
    return ImageFont.truetype(FONT, size) if FONT else ImageFont.load_default()


def load(nk, name, min_w=2400):
    """Open a big JPEG at the smallest draft scale that still gives min_w px width. Prints the dims."""
    im = Image.open(nk / name)
    src = im.size
    im.draft("RGB", (min_w, round(min_w * src[1] / src[0])))
    im = im.convert("RGB")
    print(f"  {name:48s} {src[0]}x{src[1]}  (loaded {im.width}x{im.height})")
    return im


def fit_cover(im, w=W, h=H, focus=(0.5, 0.5)):
    """Scale to cover w x h and crop. Returns (RGBA canvas, mapper) where mapper(fx, fy)
    turns a source-fraction point into canvas pixels, so boxes measured on the photo land."""
    s = max(w / im.width, h / im.height)
    sw, sh = round(im.width * s), round(im.height * s)
    ox, oy = round((sw - w) * focus[0]), round((sh - h) * focus[1])
    out = im.resize((sw, sh), Image.LANCZOS).crop((ox, oy, ox + w, oy + h)).convert("RGBA")

    def m(fx, fy):
        return (round(fx * sw - ox), round(fy * sh - oy))
    return out, m


def alpha_crop(im, thresh=16):
    return im.crop(im.getchannel("A").point(lambda v: 255 if v > thresh else 0).getbbox())


def fit_font(d, text, max_w, size, min_size=20):
    f = font(size)
    while d.textlength(text, font=f) > max_w and size > min_size:
        size -= 1
        f = font(size)
    return f, size


def tag(im, text, colour=AMBER):
    d = ImageDraw.Draw(im)
    f, size = fit_font(d, text, W - 80, 30, 22)
    tw = d.textlength(text, font=f)
    d.rectangle((24, 24, 24 + tw + 28, 24 + 52), fill=(0, 0, 0, 220))
    d.text((38, 24 + (52 - size) // 2 - 2), text, font=f, fill=colour)


def paste_logo(canvas, logo, width, cx, top, opacity=1.0):
    """Plain Lanczos resize of the mark — never AI-enlarged."""
    s = width / logo.width
    l = logo.resize((width, round(logo.height * s)), Image.LANCZOS)
    if opacity < 1.0:
        l.putalpha(l.getchannel("A").point(lambda v: int(v * opacity)))
    canvas.alpha_composite(l, (cx - width // 2, top))
    return canvas


def thirds(im):
    d = ImageDraw.Draw(im)
    for k in (1, 2):
        d.line((W * k // 3, 0, W * k // 3, H), fill=GUIDE, width=2)
        d.line((0, H * k // 3, W, H * k // 3), fill=GUIDE, width=2)


def note(im, xy, text, size=26, fill=NOTE, anchor="la", plate=None, pad=10):
    """Text, optionally on a translucent plate so it reads over a photo. Multiline anchors end in 'a'."""
    d = ImageDraw.Draw(im)
    f = font(size)
    if plate is not None:
        x0, y0, x1, y1 = d.multiline_textbbox(xy, text, font=f, anchor=anchor)
        d.rounded_rectangle((x0 - pad, y0 - pad, x1 + pad, y1 + pad), radius=8, fill=plate)
    d.multiline_text(xy, text, font=f, fill=fill, anchor=anchor,
                     align={"l": "left", "m": "center", "r": "right"}[anchor[0]])


def footer(im, shot, t_in, t_out, text):
    """Bottom strip: shot number, timing, what the shot is."""
    f_in, f_out = round(t_in * FPS), round(t_out * FPS)
    footer_raw(im, f"S{shot}  {t_in:04.1f}–{t_out:04.1f} s  (f{f_in}–{f_out}, {t_out - t_in:.1f} s)  ·  {text}")


def footer_raw(im, text):
    d = ImageDraw.Draw(im)
    d.rectangle((0, H - 58, W, H), fill=(0, 0, 0, 190))
    d.text((24, H - 46), text, font=font(26), fill=(230, 230, 230))


def arrow(im, p0, p1, colour=INK, width=5, head=22):
    d = ImageDraw.Draw(im)
    d.line((p0, p1), fill=colour, width=width)
    a = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    for s in (-1, 1):
        d.line((p1, (p1[0] - head * math.cos(a + s * 0.5), p1[1] - head * math.sin(a + s * 0.5))),
               fill=colour, width=width)


def arc_arrow(im, pts, colour=ARC, width=5):
    """Curved motion path through pts (list of points), arrow head on the last segment."""
    d = ImageDraw.Draw(im)
    d.line(pts, fill=colour, width=width, joint="curve")
    arrow(im, pts[-2], pts[-1], colour=colour, width=width)


def box_tag(im, box, text, colour=RED, size=24):
    """Labelled rectangle over a region of the plate (replace / remove / generate)."""
    d = ImageDraw.Draw(im)
    d.rectangle(box, outline=colour, width=4)
    f = font(size)
    tw = d.textlength(text, font=f)
    x, y = box[0], box[1] - size - 14
    if y < 90:                                          # keep clear of the tag strip
        y = box[3] + 6
    d.rectangle((x, y, x + tw + 16, y + size + 10), fill=colour)
    d.text((x + 8, y + 4), text, font=f, fill=WHITE)


def crop_frac(im, box):
    return im.crop((round(box[0] * im.width), round(box[1] * im.height),
                    round(box[2] * im.width), round(box[3] * im.height)))


def inset(canvas, im, box, caption, size=20):
    """Pinned reference thumbnail with a white border and a caption plate below it."""
    x0, y0, x1, y1 = box
    cap_h = size + 16
    t = im.convert("RGB")
    s = min((x1 - x0) / t.width, (y1 - y0 - cap_h - 8) / t.height)      # thumb + caption stay inside the box
    t = t.resize((round(t.width * s), round(t.height * s)), Image.LANCZOS)
    x0 = x1 - t.width                                                     # right-aligned in the box
    d = ImageDraw.Draw(canvas)
    d.rectangle((x0 - 4, y0 - 4, x1 + 4, y0 + t.height + 4 + cap_h), fill=WHITE)
    canvas.paste(t, (x0, y0))
    d.rectangle((x0 - 4, y0 + t.height + 4, x1 + 4, y0 + t.height + 4 + cap_h), fill=(0, 0, 0, 220))
    f, _ = fit_font(d, caption, t.width - 4, size, 14)
    d.text((x0 + 4, y0 + t.height + 10), caption, font=f, fill=AMBER)


def place(canvas, im, height, cx, cy, angle=0, opacity=1.0, flip=False):
    """Lanczos-resize an RGBA element to `height`, optional flip / rotate / opacity, centre it on (cx, cy)."""
    s = height / im.height
    e = im.resize((max(1, round(im.width * s)), height), Image.LANCZOS)
    if flip:
        e = e.transpose(Image.FLIP_LEFT_RIGHT)
    if angle:
        e = e.rotate(angle, resample=Image.BICUBIC, expand=True)
    if opacity < 1.0:
        e.putalpha(e.getchannel("A").point(lambda v: int(v * opacity)))
    canvas.alpha_composite(e, (round(cx - e.width / 2), round(cy - e.height / 2)))
    return e.size


def place_feet(canvas, im, height, cx, feet_y, opacity=1.0):
    """Standing cut-out: centred on cx with its feet on feet_y. Returns the pasted box."""
    s = height / im.height
    e = im.resize((round(im.width * s), height), Image.LANCZOS)
    if opacity < 1.0:
        e.putalpha(e.getchannel("A").point(lambda v: int(v * opacity)))
    xy = (cx - e.width // 2, feet_y - e.height)
    canvas.alpha_composite(e, xy)
    return (*xy, xy[0] + e.width, xy[1] + e.height)


def key_sky(crop, width=640, lo=22, span=36):
    """Pull a bird off a clear-sky crop: alpha = colour distance from the border's median sky.
    Downscaled first so JPEG grain averages out. Good enough for a board element, not a final matte."""
    c = crop.resize((width, round(crop.height * width / crop.width)), Image.LANCZOS).convert("RGB")
    a = np.asarray(c).astype(float)
    sky = np.median(np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]]), axis=0)
    dist = np.sqrt(((a - sky) ** 2).sum(axis=2))
    alpha = np.clip((dist - lo) / span, 0, 1) * 255
    return alpha_crop(Image.fromarray(np.dstack([a, alpha]).astype(np.uint8), "RGBA"))


def pinned(canvas, photo, box, height, cx, feet_y, label):
    """Photo crop as a soft-cornered pinned stand-in, feet on feet_y, labelled underneath."""
    c = crop_frac(photo, box)
    c = c.resize((round(c.width * height / c.height), height), Image.LANCZOS).convert("RGBA")
    m = Image.new("L", c.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, c.width - 1, c.height - 1), radius=28, fill=255)
    c.putalpha(m)
    x, y = cx - c.width // 2, feet_y - c.height
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle((x - 5, y - 5, x + c.width + 5, y + c.height + 5), radius=32, fill=WHITE)
    canvas.alpha_composite(c, (x, y))
    note(canvas, (cx, feet_y + 12), label, 20, fill=WHITE, anchor="ma", plate=(0, 0, 0, 210), pad=8)
    return (x, y, x + c.width, y + c.height)


def zoomed(plate, zoom, white, size=(300, 169)):
    """Motion-strip thumb: the plate as the camera would see it at `zoom` (>1 = closer), blended to white."""
    cw, ch = round(W / zoom), round(H / zoom)
    x, y = (W - cw) // 2, (H - ch) // 2
    t = plate.crop((x, y, x + cw, y + ch)).resize(size, Image.LANCZOS)
    return Image.blend(t, Image.new("RGBA", size, WHITE), white)


def strip(canvas, thumbs, x, y, title):
    """Row of motion thumbs with a title and per-thumb captions, on a dark plate."""
    tw, th, gap = thumbs[0][0].width, thumbs[0][0].height, 12
    d = ImageDraw.Draw(canvas)
    d.rectangle((x - 12, y - 40, x + len(thumbs) * (tw + gap), y + th + 40), fill=(0, 0, 0, 200))
    d.text((x, y - 34), title, font=font(22), fill=AMBER)
    for i, (t, cap) in enumerate(thumbs):
        canvas.paste(t.convert("RGB"), (x + i * (tw + gap), y))
        d.rectangle((x + i * (tw + gap), y, x + i * (tw + gap) + tw - 1, y + th - 1), outline=(140, 140, 140, 255), width=1)
        f, _ = fit_font(d, cap, tw, 20, 14)
        d.text((x + i * (tw + gap), y + th + 8), cap, font=f, fill=(230, 230, 230))


def white_field():
    return Image.new("RGBA", (W, H), WHITE)


# ---------------------------------------------------------------- frames
def main():
    pull, out = (Path(a).expanduser().resolve() for a in sys.argv[1:3])
    out.mkdir(parents=True, exist_ok=True)
    nk = pull / "Necker Island"

    print("Source dims:")
    cutout = Image.open(nk / "flamingo.png").convert("RGBA")
    print(f"  {'flamingo.png':48s} {cutout.width}x{cutout.height}  RGBA cut-out, alpha bbox {cutout.getchannel('A').getbbox()}")
    cutout = alpha_crop(cutout, thresh=128)
    aerial = load(nk, "necker_aerial_01.jpg")
    ws_aerial = load(nk, "necker_watersports_aerial_02.jpg")
    kite = load(nk, "necker_kitesurfing_01.jpg")
    court = load(nk, "necker_tennis_03.jpg")
    court_top = load(nk, "necker_tennis_01.jpg", min_w=1200)
    flock_sky = load(nk, "necker_flamingos_08.jpg")
    lemur_a = load(nk, "necker_lemur_01.jpg", min_w=1600)
    lemur_b = load(nk, "necker_lemur_08.jpg", min_w=1600)
    # measured only (reference in the .md, not composited): the other flamingo / aerial / kite / lemur photos
    for name in ("necker_flamingos_02.jpg", "necker_flamingos_10.jpg", "necker_elders_temple_flamingos.jpg",
                 "necker_bali_hi_complex_flamingo_pond_02.jpg", "necker_bali_hi_aerial_05.jpg",
                 "necker_foil_surfing_06.jpg", "necker_foil_surfing_closeup_02.jpg", "necker_lemurs_3.jpg"):
        im = Image.open(nk / name)
        print(f"  {name:48s} {im.width}x{im.height}  (reference only)")
    mark = Image.open(nk / "07D6D2DD-B1C4-4F3A-A698-BEFC90F1162C.jpg").convert("RGB")
    print(f"  {'07D6D2DD-….jpg (Virgin script mark)':48s} {mark.width}x{mark.height}")
    mark_rgba = mark.convert("RGBA")
    mark_rgba.putalpha(mark.convert("L").point(lambda v: 255 if v < 180 else round((255 - v) * 255 / 75)))

    # a real Necker flamingo in flight, keyed off the sky photo — heading frame-right, gliding slightly down
    flier = key_sky(crop_frac(flock_sky, FLIGHT_BIRD))

    # the opening placement, reused verbatim for the loop frame
    STAND_H, STAND_CX, STAND_FEET = int(H * 0.72), W // 2 - 40, int(H * 0.87)

    frames = []

    # 01 — S1 00.0–02.4: the art. Cut-out flamingo, bow tie and all, alone on white.
    def opening(tag_text):
        f = white_field()
        thirds(f)
        place_feet(f, cutout, STAND_H, STAND_CX, STAND_FEET)
        note(f, (W - 48, int(H * 0.30)),
             "THE ART — flamingo.png cut-out as supplied\n≈72 % frame height, feet on 0.87 H, just left of centre\n"
             "locked off; head preens f20, settles f38\nbow tie stays (it is the character)", 24, anchor="ra")
        tag(f, tag_text)
        return f

    f = opening("ART SUPPLIED — flamingo.png (915×1666 RGBA), Lanczos resize only, no generation")
    footer(f, 1, 0.0, 2.4, "flamingo hold — the cut-out, alone on white")
    frames.append(("01_flamingo_hold", f))

    # 02 — S2 02.4–04.6: takeoff. Cut-out leans and lifts along an arc toward upper right; real flier at the end.
    f = white_field()
    thirds(f)
    p0 = (STAND_CX, STAND_FEET - STAND_H // 2)
    path = [p0, (int(W * 0.50), int(H * 0.46)), (int(W * 0.60), int(H * 0.34)), (int(W * 0.72), int(H * 0.24)), (int(W * 0.84), int(H * 0.17))]
    place_feet(f, cutout, STAND_H, STAND_CX, STAND_FEET, opacity=0.18)                               # f58 crouch
    place(f, cutout, int(H * 0.62), int(W * 0.50), int(H * 0.50), angle=14, opacity=0.35)           # f68 first downstroke
    place(f, flier, int(H * 0.30), int(W * 0.66), int(H * 0.32), angle=22, opacity=0.6)              # f84 second beat
    place(f, flier, int(H * 0.34), int(W * 0.84), int(H * 0.18), angle=18)                           # f110 out of the top-right
    arc_arrow(f, path)
    note(f, (48, 100),
         "crouch f58–66, first downstroke f68,\nthree full wingbeats to f110\n"
         "climbs toward frame RIGHT and exits top-right;\ncamera tilts up with it, lagging a few frames\n"
         "ghosts = the cut-out; last two poses = a real Necker\nflamingo in flight (keyed from necker_flamingos_08)", 24)
    inset(f, crop_frac(flock_sky, FLIGHT_REF), (W - 470, H - 58 - 300, W - 40, H - 58 - 20),
          "flight ref — necker_flamingos_08.jpg")
    tag(f, "TO GENERATE (Kling) — takeoff from the cut-out; wing pose per necker_flamingos_08; ends as the flier above")
    footer(f, 2, 2.4, 4.6, "takeoff — three wingbeats, camera tilts up with it")
    frames.append(("02_takeoff_TOGEN", f))

    # 03 — S3 04.6–07.4: the white field dissolves and the camera pulls back to the real 3/4 aerial.
    plate, mp = fit_cover(aerial)
    f = plate.copy()
    thirds(f)
    fl_h = int(H * 0.085)
    bx, by = int(W * 0.72), int(H * 0.16)
    bw, bh = place(f, flier, fl_h, bx, by, angle=12)
    ImageDraw.Draw(f).rectangle((bx - bw // 2 - 14, by - bh // 2 - 14, bx + bw // 2 + 14, by + bh // 2 + 14), outline=WHITE, width=2)
    note(f, (bx + bw // 2 + 26, by - 30), "flamingo ≈8 % frame height,\nupper third, still flying right", 22,
         fill=WHITE, plate=(0, 0, 0, 170))
    note(f, (48, int(H * 0.30)),
         "REAL PLATE — necker_aerial_01.jpg, 3/4 aerial from the south-west\n"
         "(turbines on the ridge, Great House centre, both beaches, boats)\n"
         "pull-back = AE scale 2.2× → 1.0× on the 5k plate (2.7× headroom at HD),\n"
         "white field ramps off f110–f140 as the island resolves centre — no cut", 24,
         fill=WHITE, plate=(0, 0, 0, 170))
    strip(f, [(zoomed(plate, 2.2, 0.85), "f110 · 2.2× · white 85 %"), (zoomed(plate, 1.5, 0.40), "f140 · 1.5× · white 40 %"),
              (zoomed(plate, 1.0, 0.0), "f178 · 1.0× · clear (this frame)")], 48, H - 58 - 40 - 169, "PULL-BACK, in-betweens")
    tag(f, "PLATE READY — necker_aerial_01.jpg (photo) · zoom-out is a comp move · flamingo TO GENERATE (Kling, continues S2)")
    footer(f, 3, 4.6, 7.4, "pull back to the island — real aerial, flamingo shrinks to ~8 %")
    frames.append(("03_pullback_aerial", f))

    # 04 — S4 07.4–10.2: cut down to sea level. Kite-surfer crosses lower third L→R, flamingo crosses above R→L.
    f, mk = fit_cover(kite)
    thirds(f)
    r0, r1 = mk(RIDER_BOX[0], RIDER_BOX[1]), mk(RIDER_BOX[2], RIDER_BOX[3])
    box_tag(f, (*r0, *r1), "RIDER TO BE REPLACED (Seedream/NBP) — generic blonde man, back to camera", size=22)
    d = ImageDraw.Draw(f)
    kx, ky = int(W * 0.16), int(H * 0.10)
    d.chord((kx - 150, ky - 70, kx + 150, ky + 70), 180, 360, outline=WHITE, width=3)
    note(f, (kx, ky + 12), "KITE — bring it into frame (photo has it cropped)", 20, fill=WHITE, anchor="ma", plate=(0, 0, 0, 170))
    arrow(f, (int(W * 0.20), int(H * 0.93)), (int(W * 0.80), int(H * 0.93)), colour=WHITE)
    note(f, (int(W * 0.44), int(H * 0.79)),
         "KITE-SURFER crosses the bay left → right, lower third, riding not jumping\nsmall, blonde, back to camera, no face; spray trail",
         22, fill=WHITE, anchor="ma", plate=(0, 0, 0, 170))
    fbx, fby = int(W * 0.52), int(H * 0.14)
    place(f, flier, fl_h, fbx, fby, flip=True, angle=-8)
    arrow(f, (int(W * 0.72), int(H * 0.11)), (int(W * 0.34), int(H * 0.11)), colour=ARC)
    note(f, (W - 48, int(H * 0.13)), "flamingo continues right → left,\nupper third — the crossing paths are the shot", 22,
         fill=WHITE, anchor="ra", plate=(0, 0, 0, 170))
    note(f, (48, int(H * 0.40)),
         "PLATE — necker_kitesurfing_01.jpg, framing only\n(beach-level, sun high, Necker's east beach behind)\n"
         "locked off; only rider and bird move", 24, fill=WHITE, plate=(0, 0, 0, 170))
    inset(f, crop_frac(ws_aerial, KITER_REF), (W - 470, H - 58 - 240, W - 40, H - 58 - 20),
          "scale ref — necker_watersports_aerial_02.jpg (kiter, back to camera)")
    tag(f, "RIDER TO BE REPLACED (Seedream/NBP) — generic blonde man, back to camera · plate necker_kitesurfing_01.jpg, framing only")
    footer(f, 4, 7.4, 10.2, "kite-surfer crosses lower third; flamingo crosses upper third opposite way")
    frames.append(("04_kitesurfer_RIDER_TBR", f))

    # 05 — S5 10.2–13.0: the real court, player removed, two lemurs rallying.
    f, mc = fit_cover(court)
    thirds(f)
    p0, p1 = mc(PLAYER_BOX[0], PLAYER_BOX[1]), mc(PLAYER_BOX[2], PLAYER_BOX[3])
    box_tag(f, (*p0, *p1), "PLAYER TO BE REMOVED — clean-plate the court (NBP inpaint)", size=22)
    pinned(f, lemur_a, LEMUR_A, int(H * 0.40), int(W * 0.24), int(H * 0.85),
           "LEMUR A stand-in — necker_lemur_01.jpg crop (ring-tail)\nwrong pose, scale + species only")
    pinned(f, lemur_b, LEMUR_B, int(H * 0.17), int(W * 0.76), int(H * 0.47),
           "LEMUR B stand-in — necker_lemur_08.jpg crop (b/w ruffed)\ngenerate as a ring-tail to match A")
    pts = [(int(W * 0.30) + i * (int(W * 0.31) // 12), int(H * 0.56) - int(130 * math.sin(i / 12 * math.pi))) for i in range(13)]
    d = ImageDraw.Draw(f)
    d.line(pts, fill=ARC, width=4, joint="curve")
    for i, lbl in ((0, "hit 10.8"), (6, "net"), (12, "hit 11.6")):
        x, y = pts[i]
        d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=BALL, outline=INK)
        note(f, (x, y - 16), lbl, 20, fill=WHITE, anchor="mb", plate=(0, 0, 0, 170), pad=5)
    note(f, (int(W * 0.50), int(H * 0.64)),
         "rally: hits at 10.8 / 11.6 / 12.4 s, ≈14 f ball travel per exchange\nplay it straight — rackets held properly, no cartoon takes",
         22, fill=WHITE, anchor="ma", plate=(0, 0, 0, 170))
    note(f, (48, int(H * 0.30)),
         "PLATE — necker_tennis_03.jpg (real court: astroturf,\nshade sail, umbrellas, palms) · push in 1.0× → 1.15×\n"
         "over the shot on the 6.7k plate", 24, fill=WHITE, plate=(0, 0, 0, 170))
    inset(f, court_top, (W - 400, H - 58 - 300, W - 40, H - 58 - 20), "court location — necker_tennis_01.jpg (top-down)")
    tag(f, "TO GENERATE (Seedream→NBP) — lemurs with rackets, mid-rally · court plate necker_tennis_03.jpg, cleaned · motion Kling")
    footer(f, 5, 10.2, 13.0, "push in on the court — two ring-tails rallying, three hits")
    frames.append(("05_lemur_tennis_TOGEN", f))

    # 06 — S6 13.0–14.0: return, part 1. Camera keeps pulling back, island whites out, flamingo turns for home. Mark small.
    f = Image.alpha_composite(zoomed(plate, 0.72, 0.0, (W, H)), Image.new("RGBA", (W, H), (255, 255, 255, 165)))
    thirds(f)
    place(f, flier, int(H * 0.13), int(W * 0.40), int(H * 0.22), flip=True, angle=-30)
    arc_arrow(f, [(int(W * 0.62), int(H * 0.10)), (int(W * 0.50), int(H * 0.15)), (int(W * 0.42), int(H * 0.24)), (int(W * 0.38), int(H * 0.36))])
    note(f, (int(W * 0.40), int(H * 0.40)), "flamingo banks back toward camera\nand starts to descend (still small)", 22, anchor="ma")
    paste_logo(f, mark_rgba, width=180, cx=W - 40 - 90, top=H - 58 - 40 - 170)
    note(f, (W - 40, H - 58 - 40 - 240), "sign-off — Virgin script jpg, 180 px,\nLanczos; on f318, off with the white", 20, anchor="ra")
    strip(f, [(zoomed(plate, 1.0, 0.0), "f312 · 1.0× · clear"), (zoomed(plate, 0.72, 0.65), "f324 · 0.72× · white 65 % ← this"),
              (zoomed(plate, 0.55, 1.0), "f336 · 0.55× · white 100 %")], 48, H - 58 - 40 - 169, "WHITE-OUT, in-betweens")
    note(f, (48, 96),
         "RETURN — the pull-back keeps going (AE scale 1.0× → 0.55×)\nwhile the white field ramps back up f312–f336;\n"
         "the island 'goes back into the art'. Same plate as S3.", 24)
    tag(f, "RETURN — island whites out (AE plate scale + white ramp, no generation) · flamingo TO GENERATE (Kling, turns for home)")
    footer(f, 6, 13.0, 14.0, "return — pull back continues, island whites out, mark small")
    frames.append(("06_return_whiteout", f))

    # 07 — S7 14.0–15.5: return, part 2. Flamingo lands from upper left back into the opening pose.
    f = white_field()
    thirds(f)
    land = [(int(W * 0.10), int(H * 0.12)), (int(W * 0.22), int(H * 0.22)), (int(W * 0.33), int(H * 0.36)), (int(W * 0.42), int(H * 0.52)), (STAND_CX - 40, STAND_FEET - STAND_H // 2 + 40)]
    place(f, flier, int(H * 0.26), int(W * 0.16), int(H * 0.16), flip=True, angle=-28, opacity=0.35)   # f336 gliding in
    place(f, flier, int(H * 0.36), int(W * 0.33), int(H * 0.36), flip=True, angle=-12, opacity=0.5)    # f348 flaring, legs drop
    place(f, cutout, int(H * 0.62), int(W * 0.40), int(H * 0.57), angle=-14, opacity=0.28)            # f358 touchdown
    place_feet(f, cutout, STAND_H, STAND_CX, STAND_FEET)                                               # f372 = f0
    arc_arrow(f, land)
    note(f, (W - 48, int(H * 0.60)),
         "descends from upper LEFT (mirror of the takeoff exit, right)\nglide f336–348, flare + legs down f348–358,\n"
         "touchdown f358, wings fold, settles into the\nopening pose by f372 — which IS frame 0\n"
         "generation must END on the cut-out exactly:\nlast frame is the still, not a near-match", 24, anchor="ra")
    tag(f, "TO GENERATE (Kling) — landing, reverse of the takeoff · last frame must match the cut-out placement exactly")
    footer(f, 7, 14.0, 15.5, "landing — back into the opening pose")
    frames.append(("07_return_landing_TOGEN", f))

    # 08 — loop frame: f372 = f0. Byte-identical composition to 01.
    f = opening("LOOP FRAME — f372 = f0, identical to 01_flamingo_hold (same cut-out, same placement)")
    footer_raw(f, "S8  15.5 s (f372) = 00.0 s (f0)  ·  loop point — flamingo alone on white, exactly as 01")
    frames.append(("08_loop_equals_01", f))

    for name, im in frames:
        im.convert("RGB").save(out / f"{name}.png", optimize=True)
        im.convert("RGB").resize((960, 540), Image.LANCZOS).save(out / f"{name}_small.jpg", quality=88)

    # contact sheet: 4 columns
    cols, tw, th, gap = 4, 460, 259, 16
    rows = (len(frames) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * gap, rows * (th + 40) + (rows + 1) * gap), (16, 16, 16))
    d = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(frames):
        r, c = divmod(i, cols)
        x, y = gap + c * (tw + gap), gap + r * (th + 40 + gap)
        sheet.paste(im.convert("RGB").resize((tw, th), Image.LANCZOS), (x, y))
        d.text((x, y + th + 8), name.replace("_", " "), font=font(22), fill=AMBER)
    sheet.save(out / "contact_sheet.jpg", quality=88)
    print(f"{len(frames)} frames -> {out}")


if __name__ == "__main__":
    main()
