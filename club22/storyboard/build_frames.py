#!/usr/bin/env python3
"""Build the 22 Club storyboard frames — v2 (vector mark, black ground).

Six 1920x1080 frames, one per beat, plus a contact sheet. Everything sits on
black (Allen's call). The mark is the client's vector, rasterised to
assets/wordmarks/club22_wordmark.png (2023x3050 RGBA) and Lanczos-downsampled
(premultiplied) so its ink stands MARK_H px tall. The decks, spotlight and dust
are Pillow schematics tagged COMP / TO GENERATE, as in v1.

Usage:
    python club22/storyboard/build_frames.py PULL_ROOT OUT_DIR

PULL_ROOT  local mirror of the Drive folder ("22 club/22club_wordmark.ai" is
           the vector the raster was made from; it is only checked, not read)
OUT_DIR    where the PNG frames, *_small.jpg and contact_sheet.jpg go

Nothing under PULL_ROOT is modified. Requires Pillow only.

Timing: theria_hotel_animations_timing_v1.md section 8, quantised to the
124 BPM grid it asks for (24 fps, 290 frames, 11.613 f/beat). See STORYBOARD.md.
"""
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

W, H = 1920, 1080
BLACK = (0, 0, 0, 255)          # ground, and the colour of the cut-to-black tail
RED = (178, 47, 40)             # brand red, read from the vector raster (99.9 % of opaque px)
MARK_H = 520                    # ink height of the whole mark on the canvas
CX, CY = W // 2, H // 2

MARK_PATH = Path(__file__).resolve().parents[2] / "assets" / "wordmarks" / "club22_wordmark.png"
MARK_SIZE = (2023, 3050)
VECTOR_IN_PULL = Path("22 club") / "22club_wordmark.ai"

# Source-mark geometry: ink boxes (l, t, r, b), r/b exclusive, measured from the
# raster's alpha at build time and checked against these values. Rows 1884-1952
# are the clear band between the digits and the script; the digits are
# separated by a 15 px clear column (1014-1029) — that is the split line.
SRC_INK = (280, 262, 1783, 2595)        # whole mark
SRC_22 = (345, 262, 1699, 1884)         # the two digits
SRC_2L = (345, 262, 1014, 1884)         # left digit
SRC_2R = (1029, 262, 1699, 1884)        # right digit
SRC_CLUB = (280, 1952, 1783, 2595)      # the script

PLATTER_D = 320                 # platter diameter on canvas (px)
PLATTER_DX = 185                # platter centre offset from CX (decks drift apart as they fall)
ELEV = 0.5                      # sin(30 deg): ellipse height / width when seen from 30 deg above

AMBER = (255, 176, 32)
GREY_LINE = (70, 70, 75, 255)           # base line on black
GREY_DASH = (130, 130, 135, 255)        # platter footprints on black
GREY_TEXT = (175, 175, 170)             # annotations on black

FONT = next((p for p in [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
] if Path(p).exists()), None)


def font(size):
    return ImageFont.truetype(FONT, size) if FONT else ImageFont.load_default()


def tag(im, text, colour=AMBER, y=24):
    d = ImageDraw.Draw(im)
    size = 30
    f = font(size)
    tw = d.textlength(text, font=f)
    while tw > W - 48 - 28 and size > 18:      # shrink to fit the frame width
        size -= 1
        f = font(size)
        tw = d.textlength(text, font=f)
    d.rectangle((24, y, 24 + tw + 28, y + 52), fill=(28, 28, 30, 255))
    d.text((38, y + 8), text, font=f, fill=colour)


def footer(im, text):
    d = ImageDraw.Draw(im)
    f = font(26)
    tw = d.textlength(text, font=f)
    d.rectangle((24, H - 24 - 46, 24 + tw + 28, H - 24), fill=(28, 28, 30, 255))
    d.text((38, H - 24 - 38), text, font=f, fill=(220, 220, 220))


def blank():
    return Image.new("RGBA", (W, H), BLACK)


def runs(flags):
    """[(start, end)) runs of True in a sequence."""
    out, start = [], None
    for i, v in enumerate(flags):
        if v and start is None:
            start = i
        elif not v and start is not None:
            out.append((start, i))
            start = None
    if start is not None:
        out.append((start, len(flags)))
    return out


def measure(alpha):
    """Ink boxes from the alpha channel: whole mark, digit row, each digit, script."""
    w, h = alpha.size
    ink = alpha.getbbox()
    row_runs = runs([alpha.crop((0, y, w, y + 1)).getbbox() is not None for y in range(h)])
    assert len(row_runs) == 2, f"expected digits + script as two row bands, got {row_runs}"
    (dt, db), (ct, cb) = row_runs
    digits = alpha.crop((0, dt, w, db))
    col_runs = runs([digits.crop((x, 0, x + 1, db - dt)).getbbox() is not None for x in range(w)])
    assert len(col_runs) == 2, f"expected two digit columns, got {col_runs}"
    (ll, lr), (rl, rr) = col_runs
    script = alpha.crop((0, ct, w, cb))
    cl, _, cr, _ = script.getbbox()
    return {
        "INK": ink,
        "22": (ll, dt, rr, db),
        "2L": (ll, dt, lr, db),
        "2R": (rl, dt, rr, db),
        "CLUB": (cl, ct, cr, cb),
    }


class Mark:
    """The vector mark (RGBA raster) and its parts, premultiplied-Lanczos-resized
    so the whole mark's ink is MARK_H tall and centred on the canvas."""

    def __init__(self, path):
        im = Image.open(path).convert("RGBA")
        assert im.size == MARK_SIZE, f"unexpected mark size {im.size}; boxes assume {MARK_SIZE}"
        self.boxes = measure(im.getchannel("A"))
        print("mark ink boxes (l, t, r, b) measured from alpha:")
        for k, v in self.boxes.items():
            print(f"  {k:5s} {v}")
        expected = {"INK": SRC_INK, "22": SRC_22, "2L": SRC_2L, "2R": SRC_2R, "CLUB": SRC_CLUB}
        for k, v in expected.items():
            assert self.boxes[k] == v, f"box {k} measured {self.boxes[k]} != documented {v}"
        self.src = im.convert("RGBa")           # premultiply so Lanczos edges do not fringe dark
        self.s = MARK_H / (SRC_INK[3] - SRC_INK[1])
        ink_w = round((SRC_INK[2] - SRC_INK[0]) * self.s)
        # canvas position of the source ink-bbox origin so the whole mark is centred
        self.ox = CX - ink_w // 2 - round(SRC_INK[0] * self.s)
        self.oy = CY - MARK_H // 2 - round(SRC_INK[1] * self.s)

    def part(self, box):
        l, t, r, b = box
        crop = self.src.crop(box)
        im = crop.resize((round((r - l) * self.s), round((b - t) * self.s)), Image.LANCZOS).convert("RGBA")
        return im, (self.ox + round(l * self.s), self.oy + round(t * self.s))

    def paste(self, canvas, box, opacity=1.0, dx=0, squash=1.0):
        """Paste a part at its home position. squash < 1 scales height about the
        part's base line (schematic of the digit rotating backwards)."""
        im, (x, y) = self.part(box)
        base = y + im.height
        if squash != 1.0:
            im = im.convert("RGBa").resize((im.width, max(1, round(im.height * squash))), Image.LANCZOS).convert("RGBA")
            y = base - im.height
        if opacity < 1.0:
            im.putalpha(im.getchannel("A").point(lambda v: int(v * opacity)))
        canvas.alpha_composite(im, (x + dx, y))
        return canvas

    @property
    def base_y(self):
        """Canvas row of the digits' lowest ink = the hinge line for the flip."""
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
    # tonearm: pivot back-right behind the platter, head on the outer groove
    l, t, r, b = platter_box(cx, base_y)
    pivot = (r - 34, t - 22)                 # behind the far rim, not beside it (decks sit 50 px apart)
    head = (cx + PLATTER_D * 0.3, (t + b) / 2 + 4)
    d.ellipse((pivot[0] - 16, pivot[1] - 10, pivot[0] + 16, pivot[1] + 10), fill=(g(90), g(90), g(94), 255))
    d.line([pivot, head], fill=(g(120), g(120), g(124), 255), width=7)
    d.rectangle((head[0] - 14, head[1] - 6, head[0] + 14, head[1] + 6), fill=(g(120), g(120), g(124), 255))
    if spin:  # rotation arrow along the rim
        arc = platter_box(cx, base_y, k=1.12)
        d.arc(arc, 200, 300, fill=AMBER + (255,), width=4)
        ax, ay = arc[0] + (arc[2] - arc[0]) * (0.5 + 0.5 * math.cos(math.radians(300))), \
            arc[1] + (arc[3] - arc[1]) * (0.5 + 0.5 * math.sin(math.radians(300)))
        d.polygon([(ax, ay), (ax - 22, ay - 4), (ax - 10, ay + 16)], fill=AMBER + (255,))
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


def arrow(canvas, p0, p1, colour=AMBER + (255,), width=5):
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
    vec = pull / VECTOR_IN_PULL
    print(f"vector source in pull: {vec} -> {'present, %d bytes' % vec.stat().st_size if vec.exists() else 'NOT FOUND (raster still used)'}")
    mark = Mark(MARK_PATH)
    base = mark.base_y
    lcx, rcx = CX - PLATTER_DX, CX + PLATTER_DX
    drift_l, drift_r = mark.digit_dx("L"), mark.digit_dx("R")
    print(f"mark scale x{mark.s:.4f}; ink {round((SRC_INK[2]-SRC_INK[0])*mark.s)}x{MARK_H} px at "
          f"({mark.ox + round(SRC_INK[0]*mark.s)}, {mark.oy + round(SRC_INK[1]*mark.s)}); hinge row y={base}; "
          f"digit drift L {drift_l:+d} px, R {drift_r:+d} px onto platters at x={lcx}/{rcx}")
    MARK_TAG = f"VECTOR MARK — club22_wordmark.png 2023×3050 at ×{mark.s:.3f} (premultiplied Lanczos), brand red {RED[0]}/{RED[1]}/{RED[2]}"

    frames = []

    # 01 — Beat 1: the mark, cold, red on black. This composite is reused verbatim for beat 6.
    hold = paste_mark(blank(), mark)

    f = hold.copy()
    tag(f, MARK_TAG)
    footer(f, "BEAT 01 HOLD · f0–46 · 0.00–1.94 s · beats 1–5 @124 · still")
    frames.append(("01_hold", f))

    # 02 — Beat 2: the flip. Shown at ~f80: left digit already on its back, right mid-fall.
    f = blank()
    d = ImageDraw.Draw(f)
    d.line([(CX - 560, base), (CX + 560, base)], fill=GREY_LINE, width=2)               # hinge / base line
    dashed_ellipse(d, platter_box(lcx, base), GREY_DASH)                                 # left footprint
    dashed_ellipse(d, platter_box(rcx, base), (80, 80, 85, 255))                         # right footprint (coming)
    mark.paste(f, SRC_2L, dx=drift_l, squash=ELEV)                                       # flat, seen from 30 deg above
    mark.paste(f, SRC_2R, dx=drift_r // 2, squash=0.75)                                  # ~45 deg, 8 f behind
    mark.paste(f, SRC_CLUB)                                                              # script stays put
    arrow(f, (rcx - 60, base - 330), (rcx + 40, base - 210))                             # falls backwards
    d = ImageDraw.Draw(f)
    d.text((lcx - 60, base + 14), "30° above", font=font(24), fill=GREY_TEXT)
    d.text((rcx - 40, base - 380), "+8 f", font=font(24), fill=GREY_TEXT)
    d.text((CX - 560, H - 130), f"hinge = the 2s' lowest ink row (the swash base, y={base})  ·  digits drift outward {abs(drift_l)} / {drift_r} px onto the platter centres", font=font(22), fill=GREY_TEXT)
    tag(f, "COMP (AE) — digit flip: 3D layer, 90° about the base line, left first, +8 f stagger; digits drift outward onto the platter centres")
    footer(f, "BEAT 02 TURN · f46–105 · 1.94–4.36 s · beats 5–10 @124 · shown ≈ f80")
    frames.append(("02_flip_COMP", f))

    # 03 — Beat 3: they become decks. Shown at ~f140: platters built, records spinning.
    f = blank()
    d = ImageDraw.Draw(f)
    d.line([(CX - 560, base), (CX + 560, base)], fill=GREY_LINE, width=2)
    draw_deck(f, lcx, base)
    draw_deck(f, rcx, base)
    mark.paste(f, SRC_CLUB)
    d = ImageDraw.Draw(f)
    cim, cb = mark.part(SRC_CLUB)
    cw, ch = cim.size
    d.rectangle((cb[0] - 60, cb[1] - 16, cb[0] + cw + 60, cb[1] + ch + 16), outline=GREY_DASH, width=2)
    d.text((cb[0] + cw + 72, cb[1] + ch // 2 - 12), "mixer fascia (script stays put)", font=font(22), fill=GREY_TEXT)
    tag(f, "TO GENERATE (Flux 2.0 Pro) — turntable, vinyl (pipeline §5.1)  ·  COMP (AE) — build decks onto the fallen digits")
    tag(f, "SCHEMATIC — 33⅓ rpm from f130 = 43 f/rev (timing doc)", y=84)
    footer(f, "BEAT 03 TRANSFORM · f105–151 · 4.36–6.29 s · beats 10–14 @124 · shown ≈ f140")
    frames.append(("03_decks_TOGEN", f))

    # 04 — Beat 4: spotlight. Shown at ~f180: cone has swept right and covers both decks.
    f = blank()
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
    tag(f, "COMP (AE) — spotlight: hard-edged cone from top-left, dust layer; decks at 55 % outside the cone (ground is already black)")
    tag(f, "Flux 'spotlight cone + floor' still = lighting reference only (pipeline §5.1 note)", y=84)
    footer(f, "BEAT 04 DROP · f151–197 · 6.29–8.21 s · beats 14–18 @124 · shown ≈ f180")
    frames.append(("04_spotlight_COMP", f))

    # 05 — Beat 5: the flip back. Shown at ~f240: decks stripped, both digits rising together, light lifting.
    f = blank()
    d = ImageDraw.Draw(f)
    d.line([(CX - 560, base), (CX + 560, base)], fill=GREY_LINE, width=2)
    dashed_ellipse(d, platter_box(lcx, base), (80, 80, 85, 255), width=4)
    dashed_ellipse(d, platter_box(rcx, base), (80, 80, 85, 255), width=4)
    pool = (CX - PLATTER_D * 0.9, base - PLATTER_D * 0.9, CX + PLATTER_D * 0.9, base - 40)
    spotlight(f, (-80, -160), pool, strength=0.45, dust=False)
    mark.paste(f, SRC_2L, dx=drift_l // 2, squash=0.75)   # both at ~45 deg, together
    mark.paste(f, SRC_2R, dx=drift_r // 2, squash=0.75)
    mark.paste(f, SRC_CLUB)
    arrow(f, (lcx + 80, base - 160), (lcx + 20, base - 330))
    arrow(f, (rcx - 20, base - 160), (rcx - 80, base - 330))
    d = ImageDraw.Draw(f)
    d.text((CX - 120, base - 400), "rise together, same overshoot", font=font(22), fill=GREY_TEXT)
    tag(f, "COMP (AE) — digit flip back: records fade, decks strip to bare ellipses, both digits rotate up together, sliding home")
    tag(f, "COMP (AE) — spotlight narrows and lifts to nothing by f255; ground stays black", y=84)
    footer(f, "BEAT 05 RETURN · f197–255 · 8.21–10.65 s · beats 18–23 @124 · shown ≈ f240")
    frames.append(("05_flipback_COMP", f))

    # 06 — Beat 6: back to normal = beat 1, pixel-identical (loop point), then hard cut to black on beat 25.
    f = hold.copy()
    tag(f, "= BEAT 01 composite, pixel-identical (loop point f278 → f0)")
    tag(f, "Hard cut to black on beat 25 = f279 (11.61 s); black held 11 f to f290", y=84)
    footer(f, "BEAT 06 SIGN-OFF · f255–290 · 10.65–12.10 s · beats 23–25 @124 · still, cut f279")
    frames.append(("06_return", f))

    # loop check: the untagged beat-1 and beat-6 composites are the same object copied, and the
    # mark placed fresh a second time lands on the same pixels (paste is deterministic).
    again = paste_mark(blank(), mark)
    assert ImageChops.difference(hold, again).getbbox() is None, "beat 6 composite differs from beat 1"
    print("loop check: beat 6 composite == beat 1 composite, pixel-identical")

    for name, im in frames:
        im.convert("RGB").save(out / f"{name}.png", optimize=True)
        im.convert("RGB").resize((960, 540), Image.LANCZOS).save(out / f"{name}_small.jpg", quality=88)

    # contact sheet: 3 columns x 2 rows, on black, thin border so black frames keep their edges
    cols, tw, th, gap = 3, 620, 349, 18
    rows = (len(frames) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * gap, rows * (th + 44) + (rows + 1) * gap), (0, 0, 0))
    d = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(frames):
        r, c = divmod(i, cols)
        x, y = gap + c * (tw + gap), gap + r * (th + 44 + gap)
        sheet.paste(im.convert("RGB").resize((tw, th), Image.LANCZOS), (x, y))
        d.rectangle((x - 1, y - 1, x + tw, y + th), outline=(60, 60, 64), width=1)
        d.text((x, y + th + 10), name.replace("_", " "), font=font(24), fill=AMBER)
    sheet.save(out / "contact_sheet.jpg", quality=88)
    print(f"{len(frames)} frames -> {out}")


if __name__ == "__main__":
    main()
