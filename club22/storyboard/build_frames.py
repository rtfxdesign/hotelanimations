#!/usr/bin/env python3
"""Build the 22 Club storyboard frames.

Seven 1920x1080 frames (one per beat, plus a black-ground alternate for
beat 1) and a contact sheet. The only client asset is a 364x549 palette PNG
of the mark, so the mark is a Lanczos-resized placeholder (tagged) and every
other element is a Pillow schematic (tagged COMP / TO GENERATE).

Usage:
    python club22/storyboard/build_frames.py PULL_ROOT OUT_DIR

PULL_ROOT  local mirror of the Drive folder (contains "22 club/images.png")
OUT_DIR    where the PNG frames, *_small.jpg and contact_sheet.jpg go

Nothing under PULL_ROOT is modified. Requires Pillow.

Timing: theria_hotel_animations_timing_v1.md section 8, re-quantised to the
124 BPM grid it asks for (24 fps, 290 frames, 11.613 f/beat). See STORYBOARD.md.
"""
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1920, 1080
IVORY = (255, 255, 240, 255)
BLACK = (8, 8, 10, 255)
RED = (181, 54, 47)             # mean ink colour of the source mark
MARK_H = 520                    # ink height of the whole mark on the canvas
CX, CY = W // 2, H // 2

# Source-mark geometry (pixel rows/cols of ink in images.png, measured 2026-09-25)
SRC_INK = (114, 169, 250, 380)          # whole mark ink bbox (l, t, r, b), b/r exclusive
SRC_22 = (120, 169, 244, 315)           # the two digits
SRC_2L = (120, 169, 181, 315)           # left digit
SRC_2R = (183, 169, 244, 315)           # right digit
SRC_CLUB = (114, 321, 250, 380)         # the script

PLATTER_D = 320                 # platter diameter on canvas (px)
PLATTER_DX = 185                # platter centre offset from CX (decks drift apart as they fall)
ELEV = 0.5                      # sin(30 deg): ellipse height / width when seen from 30 deg above

FONT = next((p for p in [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
] if Path(p).exists()), None)


def font(size):
    return ImageFont.truetype(FONT, size) if FONT else ImageFont.load_default()


def tag(im, text, colour=(255, 176, 32), y=24):
    d = ImageDraw.Draw(im)
    size = 30
    f = font(size)
    tw = d.textlength(text, font=f)
    while tw > W - 48 - 28 and size > 18:      # shrink to fit the frame width
        size -= 1
        f = font(size)
        tw = d.textlength(text, font=f)
    d.rectangle((24, y, 24 + tw + 28, y + 52), fill=(0, 0, 0, 220))
    d.text((38, y + 8), text, font=f, fill=colour)


def footer(im, text):
    d = ImageDraw.Draw(im)
    f = font(26)
    tw = d.textlength(text, font=f)
    d.rectangle((24, H - 24 - 46, 24 + tw + 28, H - 24), fill=(0, 0, 0, 220))
    d.text((38, H - 24 - 38), text, font=f, fill=(220, 220, 220))


def blank(colour=IVORY):
    return Image.new("RGBA", (W, H), colour)


def key_white(im):
    """Palette/RGB mark on white -> RGBA: solid brand red, alpha from ink coverage.
    A plain colour key, not a redraw; anti-aliased edges keep their partial alpha."""
    rgb = im.convert("RGB")
    lum = rgb.convert("L")
    ink_lum = round(0.299 * RED[0] + 0.587 * RED[1] + 0.114 * RED[2])
    alpha = lum.point(lambda v: max(0, min(255, round((255 - v) * 255 / (255 - ink_lum)))))
    out = Image.new("RGBA", im.size, RED + (255,))
    out.putalpha(alpha)
    return out


class Mark:
    """The mark and its parts, Lanczos-resized so the whole mark's ink is MARK_H tall."""

    def __init__(self, src):
        self.src = key_white(src)
        self.s = MARK_H / (SRC_INK[3] - SRC_INK[1])
        ink_w = round((SRC_INK[2] - SRC_INK[0]) * self.s)
        # canvas position of the source ink-bbox origin so the whole mark is centred
        self.ox = CX - ink_w // 2 - round(SRC_INK[0] * self.s)
        self.oy = CY - MARK_H // 2 - round(SRC_INK[1] * self.s)

    def part(self, box):
        l, t, r, b = box
        crop = self.src.crop(box)
        im = crop.resize((round((r - l) * self.s), round((b - t) * self.s)), Image.LANCZOS)
        return im, (self.ox + round(l * self.s), self.oy + round(t * self.s))

    def paste(self, canvas, box, opacity=1.0, dx=0, squash=1.0):
        """Paste a part at its home position. squash < 1 scales height about the
        part's base line (schematic of the digit rotating backwards)."""
        im, (x, y) = self.part(box)
        base = y + im.height
        if squash != 1.0:
            im = im.resize((im.width, max(1, round(im.height * squash))), Image.LANCZOS)
            y = base - im.height
        if opacity < 1.0:
            im.putalpha(im.getchannel("A").point(lambda v: int(v * opacity)))
        canvas.alpha_composite(im, (x + dx, y))
        return canvas

    @property
    def base_y(self):
        return self.oy + round(SRC_22[3] * self.s)

    def digit_dx(self, side):
        """dx that moves a digit's centre onto its platter centre."""
        box = SRC_2L if side == "L" else SRC_2R
        home = self.ox + round((box[0] + box[2]) / 2 * self.s)
        target = CX - PLATTER_DX if side == "L" else CX + PLATTER_DX
        return target - home


def paste_mark(canvas, mark, opacity=1.0):
    return mark.paste(canvas, SRC_INK, opacity=opacity)


def platter_box(cx, base_y, d=PLATTER_D, k=1.0):
    """Ellipse bbox for a platter of diameter d whose near edge sits on base_y,
    seen from 30 deg above (height = ELEV * d). k scales it (label, vinyl)."""
    w, h = d * k, d * ELEV * k
    cy = base_y - d * ELEV / 2
    return (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)


def dashed_ellipse(d, box, fill, width=3, n=48):
    l, t, r, b = box
    cx, cy, rx, ry = (l + r) / 2, (t + b) / 2, (r - l) / 2, (b - t) / 2
    for i in range(0, n, 2):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        pts = [(cx + rx * math.cos(a), cy + ry * math.sin(a))
               for a in (a0 + (a1 - a0) * j / 4 for j in range(5))]
        d.line(pts, fill=fill, width=width)


def draw_deck(canvas, cx, base_y, lit=1.0, spin=True, opacity=1.0):
    """Schematic turntable: platter ring, black vinyl, red label, spindle, tonearm."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    g = lambda v: int(v * lit)
    d.ellipse(platter_box(cx, base_y + 10), fill=(g(70), g(70), g(75), 255))          # plinth shadow
    d.ellipse(platter_box(cx, base_y), fill=(g(150), g(150), g(155), 255),
              outline=(g(210), g(210), g(215), 255), width=3)                           # aluminium rim
    d.ellipse(platter_box(cx, base_y, k=0.9), fill=(g(22), g(22), g(24), 255))         # vinyl
    for k in (0.82, 0.7, 0.58, 0.46):                                                   # grooves
        d.ellipse(platter_box(cx, base_y, k=k), outline=(g(48), g(48), g(52), 255), width=1)
    d.ellipse(platter_box(cx, base_y, k=0.3), fill=(g(RED[0]), g(RED[1]), g(RED[2]), 255))  # label
    d.ellipse(platter_box(cx, base_y, k=0.035), fill=(g(230), g(230), g(235), 255))     # spindle
    # tonearm: pivot back-right, head on the outer groove
    l, t, r, b = platter_box(cx, base_y)
    pivot = (r + 40, t + 10)
    head = (cx + PLATTER_D * 0.36, (t + b) / 2 + 8)
    d.ellipse((pivot[0] - 16, pivot[1] - 10, pivot[0] + 16, pivot[1] + 10), fill=(g(60), g(60), g(64), 255))
    d.line([pivot, head], fill=(g(40), g(40), g(44), 255), width=7)
    d.rectangle((head[0] - 14, head[1] - 6, head[0] + 14, head[1] + 6), fill=(g(40), g(40), g(44), 255))
    if spin:  # rotation arrow along the rim
        arc = platter_box(cx, base_y, k=1.12)
        d.arc(arc, 200, 300, fill=(255, 176, 32, 255), width=4)
        ax, ay = arc[0] + (arc[2] - arc[0]) * (0.5 + 0.5 * math.cos(math.radians(300))), \
            arc[1] + (arc[3] - arc[1]) * (0.5 + 0.5 * math.sin(math.radians(300)))
        d.polygon([(ax, ay), (ax - 22, ay - 4), (ax - 10, ay + 16)], fill=(255, 176, 32, 255))
    if opacity < 1.0:
        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * opacity)))
    canvas.alpha_composite(layer)
    return canvas


def spotlight(canvas, apex, pool_box, strength=1.0, dust=True, seed=22):
    """Hard-edged cone from apex to an elliptical pool; brightens what is under it."""
    l, t, r, b = pool_box
    pcx, pcy, rx, ry = (l + r) / 2, (t + b) / 2, (r - l) / 2, (b - t) / 2
    # tangent-ish points on the pool ellipse, left and right
    ang = math.atan2(pcy - apex[1], pcx - apex[0])
    a0, a1 = ang + math.pi / 2, ang - math.pi / 2
    p0 = (pcx + rx * math.cos(a0), pcy + ry * math.sin(a0))
    p1 = (pcx + rx * math.cos(a1), pcy + ry * math.sin(a1))
    beam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(beam)
    d.polygon([apex, p0, p1], fill=(255, 236, 200, int(70 * strength)))
    d.ellipse(pool_box, fill=(255, 240, 210, int(110 * strength)))
    beam = beam.filter(ImageFilter.GaussianBlur(2))
    canvas.alpha_composite(beam)
    edge = ImageDraw.Draw(canvas)
    edge.line([apex, p0], fill=(255, 240, 210, int(120 * strength)), width=2)
    edge.line([apex, p1], fill=(255, 240, 210, int(120 * strength)), width=2)
    if dust:
        rnd = random.Random(seed)
        dd = ImageDraw.Draw(canvas)
        for _ in range(int(260 * strength)):
            u, v = rnd.random(), rnd.random() ** 0.6
            x = apex[0] + (p0[0] + (p1[0] - p0[0]) * u - apex[0]) * v
            y = apex[1] + (p0[1] + (p1[1] - p0[1]) * u - apex[1]) * v
            rr = rnd.choice((1, 1, 2))
            dd.ellipse((x - rr, y - rr, x + rr, y + rr), fill=(255, 245, 225, rnd.randint(90, 200)))
    return canvas


def arrow(canvas, p0, p1, colour=(255, 176, 32, 255), width=5):
    d = ImageDraw.Draw(canvas)
    d.line([p0, p1], fill=colour, width=width)
    a = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    for s in (1, -1):
        d.line([p1, (p1[0] - 26 * math.cos(a + s * 0.45), p1[1] - 26 * math.sin(a + s * 0.45))],
               fill=colour, width=width)


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    pull, out = (Path(a).expanduser().resolve() for a in sys.argv[1:3])
    out.mkdir(parents=True, exist_ok=True)
    src = Image.open(pull / "22 club" / "images.png")
    assert src.size == (364, 549), f"unexpected source size {src.size}; geometry constants assume 364x549"
    mark = Mark(src)
    base = mark.base_y
    PLACEHOLDER = "PLACEHOLDER — 364 px source, Lanczos x%.2f, vector pending" % mark.s
    lcx, rcx = CX - PLATTER_DX, CX + PLATTER_DX

    frames = []

    # 01 — Beat 1: the mark, cold, on ivory
    f = paste_mark(blank(), mark)
    tag(f, PLACEHOLDER)
    footer(f, "BEAT 01 HOLD · f0–46 · 0.00–1.94 s · beats 1–5 @124 · still")
    frames.append(("01_hold_ivory", f))

    # 01b — Beat 1 alternate: same, on black (the timing doc's preference for a club)
    f = paste_mark(blank(BLACK), mark)
    tag(f, PLACEHOLDER)
    tag(f, "ALT GROUND — black. Same beat, Allen to pick ivory or black", y=84)
    footer(f, "BEAT 01 HOLD (ALT) · f0–46 · 0.00–1.94 s · beats 1–5 @124 · still")
    frames.append(("01b_hold_black_ALT", f))

    # 02 — Beat 2: the flip. Shown at ~f80: left digit already on its back, right mid-fall.
    f = blank()
    d = ImageDraw.Draw(f)
    d.line([(CX - 560, base), (CX + 560, base)], fill=(200, 200, 185, 255), width=2)     # base line
    dashed_ellipse(d, platter_box(lcx, base), (170, 170, 160, 255))                       # left footprint
    dashed_ellipse(d, platter_box(rcx, base), (215, 215, 205, 255))                       # right footprint (coming)
    mark.paste(f, SRC_2L, dx=mark.digit_dx("L"), squash=ELEV)                            # flat, seen from 30 deg above
    mark.paste(f, SRC_2R, dx=mark.digit_dx("R") // 2, squash=0.75)                       # ~45 deg, 8 f behind
    mark.paste(f, SRC_CLUB)                                                              # script stays put
    arrow(f, (rcx - 60, base - 330), (rcx + 40, base - 210))                             # falls backwards
    d = ImageDraw.Draw(f)
    d.text((lcx - 60, base + 14), "30° above", font=font(24), fill=(120, 120, 110))
    d.text((rcx - 40, base - 380), "+8 f", font=font(24), fill=(120, 120, 110))
    tag(f, "COMP (AE) — digit flip: 3D layer, 90° about the base line, left first, +8 f stagger")
    tag(f, PLACEHOLDER, y=84)
    footer(f, "BEAT 02 TURN · f46–105 · 1.94–4.36 s · beats 5–10 @124 · shown ≈ f80")
    frames.append(("02_flip_COMP", f))

    # 03 — Beat 3: they become decks. Shown at ~f140: platters built, records spinning.
    f = blank()
    d = ImageDraw.Draw(f)
    d.line([(CX - 560, base), (CX + 560, base)], fill=(200, 200, 185, 255), width=2)
    draw_deck(f, lcx, base)
    draw_deck(f, rcx, base)
    mark.paste(f, SRC_CLUB)
    d = ImageDraw.Draw(f)
    cb = mark.part(SRC_CLUB)[1]
    cw, ch = mark.part(SRC_CLUB)[0].size
    d.rectangle((cb[0] - 60, cb[1] - 16, cb[0] + cw + 60, cb[1] + ch + 16), outline=(170, 170, 160, 255), width=2)
    d.text((cb[0] + cw + 72, cb[1] + ch // 2 - 12), "mixer fascia (script stays put)", font=font(22), fill=(120, 120, 110))
    tag(f, "TO GENERATE (Flux 2.0 Pro) — turntable, vinyl (pipeline §5.1)  ·  COMP (AE) — build decks onto the fallen digits")
    tag(f, "SCHEMATIC — 33⅓ rpm from f130 (timing doc), spin locked to 124 BPM per storyboard page", y=84)
    footer(f, "BEAT 03 TRANSFORM · f105–151 · 4.36–6.29 s · beats 10–14 @124 · shown ≈ f140")
    frames.append(("03_decks_TOGEN", f))

    # 04 — Beat 4: spotlight. Shown at ~f180: cone has swept right and covers both decks.
    f = blank(BLACK)
    draw_deck(f, lcx, base, lit=0.55)
    draw_deck(f, rcx, base, lit=0.55)
    pool = (lcx - PLATTER_D * 0.75, base - PLATTER_D * 0.62, rcx + PLATTER_D * 0.75, base + 70)
    spotlight(f, (-80, -160), pool)
    draw_deck(f, lcx, base, lit=1.0, opacity=0.55)      # decks catch the light inside the pool
    draw_deck(f, rcx, base, lit=1.0, opacity=0.55)
    mark.paste(f, SRC_CLUB, opacity=0.65)                # script in the pool's spill, half-lit
    arrow(f, (lcx - 40, base - 420), (rcx + 40, base - 420), colour=(255, 240, 210, 255))
    d = ImageDraw.Draw(f)
    d.text((CX - 150, base - 470), "sweep L→R, f151 (in) → f158 hits left deck → f180", font=font(22), fill=(230, 230, 220))
    tag(f, "COMP (AE) — spotlight: hard-edged cone from top-left, dust layer, ground to black outside the cone")
    tag(f, "Flux 'spotlight cone + floor' still = lighting reference only (pipeline §5.1 note)", y=84)
    footer(f, "BEAT 04 DROP · f151–197 · 6.29–8.21 s · beats 14–18 @124 · shown ≈ f180")
    frames.append(("04_spotlight_COMP", f))

    # 05 — Beat 5: the flip back. Shown at ~f240: decks stripped, both digits rising together, light lifting.
    f = Image.blend(blank(BLACK), blank(), 0.7)          # ground on its way back to ivory
    d = ImageDraw.Draw(f)
    d.line([(CX - 560, base), (CX + 560, base)], fill=(110, 110, 100, 255), width=2)
    dashed_ellipse(d, platter_box(lcx, base), (70, 70, 64, 255), width=4)
    dashed_ellipse(d, platter_box(rcx, base), (70, 70, 64, 255), width=4)
    pool = (CX - PLATTER_D * 0.9, base - PLATTER_D * 0.9, CX + PLATTER_D * 0.9, base - 40)
    spotlight(f, (-80, -160), pool, strength=0.45, dust=False)
    mark.paste(f, SRC_2L, dx=mark.digit_dx("L") // 2, squash=0.75)   # both at ~45 deg, together
    mark.paste(f, SRC_2R, dx=mark.digit_dx("R") // 2, squash=0.75)
    mark.paste(f, SRC_CLUB)
    arrow(f, (lcx + 80, base - 160), (lcx + 20, base - 330))
    arrow(f, (rcx - 20, base - 160), (rcx - 80, base - 330))
    d = ImageDraw.Draw(f)
    d.text((CX - 120, base - 400), "rise together, same overshoot", font=font(22), fill=(60, 60, 55))
    tag(f, "COMP (AE) — digit flip back: records fade, decks strip to bare ellipses, both digits rotate up together")
    tag(f, "COMP (AE) — spotlight narrows and lifts; ground returning to ivory", y=84)
    footer(f, "BEAT 05 RETURN · f197–255 · 8.21–10.65 s · beats 18–23 @124 · shown ≈ f240")
    frames.append(("05_flipback_COMP", f))

    # 06 — Beat 6: back to normal = beat 1, dead still, then hard cut to black on beat 25.
    f = paste_mark(blank(), mark)
    tag(f, PLACEHOLDER)
    tag(f, "= BEAT 01 frame (loop point). Hard cut to black on beat 25 = f279, black held to f290", y=84)
    footer(f, "BEAT 06 SIGN-OFF · f255–290 · 10.65–12.10 s · beats 23–25 @124 · still")
    frames.append(("06_return", f))

    for name, im in frames:
        im.convert("RGB").save(out / f"{name}.png", optimize=True)
        im.convert("RGB").resize((960, 540), Image.LANCZOS).save(out / f"{name}_small.jpg", quality=88)

    # contact sheet: 4 columns
    cols, tw, th, gap = 4, 470, 264, 16
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
