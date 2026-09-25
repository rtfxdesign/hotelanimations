#!/usr/bin/env python3
"""Build the Necker Island storyboard frames.

This is the film with almost no art: the only usable asset is the Virgin
script mark. Every other frame is a clean schematic placeholder drawn with
Pillow (pale sky field, simple silhouettes, labelled boxes, screen fractions
from the timing doc) and tagged TO GENERATE with the model named in the
pipeline doc §5.3. Nothing here is a final look — it is a layout guide.

Usage:
    python necker_island/storyboard/build_frames.py PULL_ROOT OUT_DIR

PULL_ROOT  local mirror of the Drive folder (tools/drive_pull.py); read-only
OUT_DIR    where the PNG frames, *_small.jpg and contact_sheet.jpg go

Helpers (font, fit_cover, alpha_crop, tag, paste_logo) are copied from
giraffe_manor/storyboard/build_frames.py so the two boards read the same.
Requires Pillow.
"""
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1920, 1080
FPS = 24
SKY_TOP = (214, 232, 244, 255)      # pale sky field, top
SKY_BOT = (240, 246, 250, 255)      # pale sky field, bottom (near white)
SEA_DEEP = (28, 92, 150, 255)
SEA_SHALLOW = (92, 205, 214, 255)
SAND = (243, 232, 200, 255)
PALM = (56, 122, 64, 255)
COURT = (88, 150, 78, 255)
FLAMINGO = (238, 110, 140, 255)
INK = (40, 40, 40, 255)
GUIDE = (0, 0, 0, 40)
NOTE = (30, 30, 30, 255)

FONT = next((p for p in [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
] if Path(p).exists()), None)


# ---------------------------------------------------------------- helpers (from giraffe_manor)
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


def tag(im, text, colour=(255, 176, 32)):
    d = ImageDraw.Draw(im)
    f = font(30)
    tw = d.textlength(text, font=f)
    d.rectangle((24, 24, 24 + tw + 28, 24 + 52), fill=(0, 0, 0, 220))
    d.text((38, 32), text, font=f, fill=colour)


def paste_logo(canvas, logo, width, cx, top, opacity=1.0):
    """Plain Lanczos resize of the mark — never AI-enlarged."""
    s = width / logo.width
    l = logo.resize((width, round(logo.height * s)), Image.LANCZOS)
    if opacity < 1.0:
        a = l.getchannel("A").point(lambda v: int(v * opacity))
        l.putalpha(a)
    canvas.alpha_composite(l, (cx - width // 2, top))
    return canvas


# ---------------------------------------------------------------- schematic drawing
def sky():
    """Pale sky field with a vertical gradient."""
    im = Image.new("RGBA", (W, H), SKY_BOT)
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / (H - 1)
        c = tuple(round(SKY_TOP[i] * (1 - t) + SKY_BOT[i] * t) for i in range(3)) + (255,)
        d.line((0, y, W, y), fill=c)
    return im


def thirds(im):
    d = ImageDraw.Draw(im)
    for k in (1, 2):
        d.line((W * k // 3, 0, W * k // 3, H), fill=GUIDE, width=2)
        d.line((0, H * k // 3, W, H * k // 3), fill=GUIDE, width=2)


def note(im, xy, text, size=26, fill=NOTE, anchor="la"):
    d = ImageDraw.Draw(im)
    d.text(xy, text, font=font(size), fill=fill, anchor=anchor)


def label_box(im, box, text, size=24, fill=(0, 0, 0, 0), outline=INK):
    d = ImageDraw.Draw(im)
    d.rectangle(box, fill=fill, outline=outline, width=3)
    d.text(((box[0] + box[2]) // 2, (box[1] + box[3]) // 2), text, font=font(size),
           fill=outline, anchor="mm", align="center")


def footer(im, shot, t_in, t_out, text):
    """Bottom strip: shot number, timing, what the shot is."""
    d = ImageDraw.Draw(im)
    d.rectangle((0, H - 58, W, H), fill=(0, 0, 0, 190))
    f_in, f_out = round(t_in * FPS), round(t_out * FPS)
    d.text((24, H - 46), f"S{shot}  {t_in:04.1f}–{t_out:04.1f} s  (f{f_in}–{f_out}, {t_out - t_in:.1f} s)  ·  {text}",
           font=font(26), fill=(230, 230, 230))


def arrow(im, p0, p1, colour=INK, width=5, head=22):
    d = ImageDraw.Draw(im)
    d.line((p0, p1), fill=colour, width=width)
    a = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    for s in (-1, 1):
        d.line((p1, (p1[0] - head * math.cos(a + s * 0.5), p1[1] - head * math.sin(a + s * 0.5))),
               fill=colour, width=width)


def flamingo(im, cx, feet_y, height, wings=False, facing=1, colour=FLAMINGO):
    """Very simple flamingo silhouette. facing=1 looks frame-right, -1 frame-left."""
    d = ImageDraw.Draw(im)
    u = height / 100.0                       # 100 units tall, feet to head top
    bw, bh = 34 * u, 20 * u                  # body ellipse
    body_cy = feet_y - 52 * u
    far = tuple(max(0, c - 40) for c in colour[:3]) + (255,)
    if wings:                                # far wing, behind the body
        d.polygon([(cx + facing * 2 * u, body_cy - 2 * u), (cx - facing * 26 * u, body_cy - 30 * u),
                   (cx - facing * 40 * u, body_cy - 16 * u), (cx - facing * 10 * u, body_cy + 4 * u)], fill=far)
    leg_x = cx - 2 * u * facing
    d.line((leg_x, feet_y, leg_x, body_cy + 4 * u), fill=colour, width=max(2, round(1.6 * u)))
    d.ellipse((cx - bw / 2, body_cy - bh / 2, cx + bw / 2, body_cy + bh / 2), fill=colour)
    if wings:                                # near wing, swept up and back
        d.polygon([(cx + facing * 6 * u, body_cy - 6 * u), (cx - facing * 28 * u, body_cy - 44 * u),
                   (cx - facing * 46 * u, body_cy - 34 * u), (cx - facing * 14 * u, body_cy)], fill=colour)
    # S-neck as a chain of short segments
    pts = []
    for i in range(0, 21):
        t = i / 20
        x = cx + facing * (12 * u + 8 * u * math.sin(t * math.pi))
        y = body_cy - 6 * u - t * 40 * u
        pts.append((x, y))
    d.line(pts, fill=colour, width=max(2, round(4 * u)), joint="curve")
    hx, hy = pts[-1]
    d.ellipse((hx - 5 * u, hy - 4 * u, hx + 5 * u, hy + 4 * u), fill=colour)
    d.polygon([(hx + facing * 4 * u, hy - 1 * u), (hx + facing * 12 * u, hy + 6 * u),
               (hx + facing * 3 * u, hy + 3 * u)], fill=(40, 30, 30, 255))


def island_plate(zoom=1.0, cx=W // 2, cy=int(H * 0.56)):
    """Aerial three-quarter island on sea. zoom < 1 = further away."""
    im = sky()
    d = ImageDraw.Draw(im)
    horizon = int(H * 0.30)
    # sea, deep to shallow toward the horizon (haze)
    for y in range(horizon, H):
        t = (y - horizon) / (H - horizon)
        c = tuple(round(SEA_DEEP[i] * (0.55 + 0.45 * t) + 255 * (0.45 - 0.45 * t)) for i in range(3)) + (255,)
        d.line((0, y, W, y), fill=c)
    d.line((0, horizon, W, horizon), fill=(255, 255, 255, 120), width=2)
    rx, ry = 560 * zoom, 190 * zoom
    d.ellipse((cx - rx * 1.35, cy - ry * 1.35, cx + rx * 1.35, cy + ry * 1.35), fill=SEA_SHALLOW)  # shallows
    d.ellipse((cx - rx * 1.08, cy - ry * 1.08, cx + rx * 1.08, cy + ry * 1.08), fill=SAND)         # beach
    d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=PALM)                                       # palm interior
    for i in range(7):                                                                              # villas
        a = i / 7 * 2 * math.pi
        vx, vy = cx + math.cos(a) * rx * 0.55, cy + math.sin(a) * ry * 0.55
        s = 11 * zoom
        d.rectangle((vx - s, vy - s * 0.6, vx + s, vy + s * 0.6), fill=SAND)
    for bx, by in ((cx - rx * 1.6, cy + ry * 0.9), (cx + rx * 1.7, cy - ry * 0.4)):                # boats
        d.ellipse((bx - 6 * zoom, by - 3 * zoom, bx + 6 * zoom, by + 3 * zoom), fill=(250, 250, 250, 255))
    return im


def court(im, box, colour=COURT):
    """Grass court in simple perspective (trapezoid), white lines."""
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = box
    inset = (x1 - x0) * 0.12
    quad = [(x0 + inset, y0), (x1 - inset, y0), (x1, y1), (x0, y1)]
    d.polygon(quad, fill=colour)
    d.line(quad + [quad[0]], fill=(255, 255, 255, 255), width=4)
    ym = (y0 + y1) / 2
    lx = x0 + inset * (1 - (ym - y0) / (y1 - y0))
    d.line(((lx, ym), (x1 + x0 - lx, ym)), fill=(240, 240, 240, 255), width=5)  # net
    for t in (0.25, 0.75):
        yy = y0 + (y1 - y0) * t
        ix = x0 + inset * (1 - t)
        d.line(((ix + (x1 - x0 - 2 * ix + 2 * x0) * 0.18, yy), (x1 + x0 - ix - (x1 - x0 - 2 * ix + 2 * x0) * 0.18, yy)),
               fill=(255, 255, 255, 255), width=3)


def kitesurfer(im, x, y, size=1.0):
    """Small figure, back to camera, blonde, board + spray, kite high above and behind."""
    d = ImageDraw.Draw(im)
    u = 10 * size
    # spray trail behind (to the left)
    d.polygon([(x - 2 * u, y + 1.5 * u), (x - 22 * u, y + 0.2 * u), (x - 22 * u, y + 3.5 * u)],
              fill=(255, 255, 255, 200))
    d.line((x - 4 * u, y + 1.6 * u, x + 4 * u, y + 1.4 * u), fill=(30, 30, 30, 255), width=round(1.2 * u))  # board
    d.line((x, y + 1.4 * u, x, y - 4 * u), fill=(30, 40, 60, 255), width=round(1.4 * u))                     # body
    d.ellipse((x - 1.1 * u, y - 6.3 * u, x + 1.1 * u, y - 4.1 * u), fill=(226, 196, 96, 255))               # blonde head
    kx, ky = x - 18 * u, y - 40 * u
    d.line((x, y - 3.5 * u, kx, ky), fill=(120, 120, 120, 255), width=2)                                     # lines
    d.chord((kx - 14 * u, ky - 8 * u, kx + 14 * u, ky + 8 * u), 180, 360, fill=(240, 90, 60, 255))           # kite


def lemur_standin(canvas, lem, feet, height, flip=False):
    g = alpha_crop(lem)
    s = height / g.height
    g = g.resize((round(g.width * s), round(g.height * s)), Image.LANCZOS)
    if flip:
        g = g.transpose(Image.FLIP_LEFT_RIGHT)
    canvas.alpha_composite(g, (feet[0] - g.width // 2, feet[1] - g.height))
    return g.width, g.height


def racket(im, grip, head, colour=(120, 80, 40, 255)):
    d = ImageDraw.Draw(im)
    d.line((grip, head), fill=colour, width=6)
    r = 22
    d.ellipse((head[0] - r, head[1] - r * 1.25, head[0] + r, head[1] + r * 1.25), outline=colour, width=6)


def ball(im, xy, r=9):
    ImageDraw.Draw(im).ellipse((xy[0] - r, xy[1] - r, xy[0] + r, xy[1] + r), fill=(220, 240, 60, 255), outline=INK)


# ---------------------------------------------------------------- frames
def main():
    pull, out = (Path(a).expanduser().resolve() for a in sys.argv[1:3])
    out.mkdir(parents=True, exist_ok=True)
    nk = pull / "Necker Island"
    mark = Image.open(nk / "07D6D2DD-B1C4-4F3A-A698-BEFC90F1162C.jpg").convert("RGB")
    # red-on-white jpg → alpha from luminance so it can sit on any field (plain Lanczos only, no AI enlarge)
    mark_rgba = mark.convert("RGBA")
    mark_rgba.putalpha(mark.convert("L").point(lambda v: 255 if v < 180 else round((255 - v) * 255 / 75)))  # solid red opaque, edges soft
    lem_a = Image.open(pull / "Miavana" / "upscaled" / "lemur2.png").convert("RGBA")
    lem_b = Image.open(pull / "Miavana" / "upscaled" / "lemur3.png").convert("RGBA")

    frames = []

    # 01 — S1 00.0–02.4: single flamingo, standing, on pale sky / white
    f = sky()
    thirds(f)
    flamingo(f, cx=W // 2 - 40, feet_y=int(H * 0.86), height=int(H * 0.70))
    note(f, (W // 2 + 250, int(H * 0.40)), "FLAMINGO ≈70 % frame height\nstanding, one leg, profile\nstill; preen f20, settle f38", 26)
    tag(f, "TO GENERATE (Flux 2.0 Pro) — flamingo standing, isolated, see pipeline doc §5.3")
    footer(f, 1, 0.0, 2.4, "flamingo hold, isolated on white / pale sky")
    frames.append(("01_flamingo_hold_TOGEN", f))

    # 02 — S2 02.4–04.6: takeoff, climbing toward frame right, camera tilts up lagging
    f = sky()
    thirds(f)
    flamingo(f, cx=int(W * 0.58), feet_y=int(H * 0.72), height=int(H * 0.62), wings=True)
    arrow(f, (int(W * 0.10), int(H * 0.86)), (int(W * 0.30), int(H * 0.40)), colour=(200, 60, 90, 255))
    note(f, (int(W * 0.08), int(H * 0.62)), "crouch f58–66, first downstroke f68,\nthree full wingbeats to f110\nclimbs toward frame RIGHT; camera tilts up, lags", 26)
    note(f, (int(W * 0.76), int(H * 0.14)), "wings ≈ full frame width\nby last beat", 24)
    tag(f, "TO GENERATE (Flux → NBP pose 2, Kling motion) — flamingo takeoff, see pipeline doc §5.3")
    footer(f, 2, 2.4, 4.6, "takeoff — three wingbeats, camera tilts up with it")
    frames.append(("02_takeoff_TOGEN", f))

    # 03 — S3 04.6–07.4: continuous zoom-out, sea fills from edges, island resolves centre, flamingo ≈8 % upper third
    f = island_plate(zoom=0.85)
    thirds(f)
    fl_h = int(H * 0.08)
    flamingo(f, cx=int(W * 0.70), feet_y=int(H * 0.12) + fl_h, height=fl_h, wings=True)
    d = ImageDraw.Draw(f)
    d.rectangle((int(W * 0.70) - 90, int(H * 0.12) - 10, int(W * 0.70) + 90, int(H * 0.12) + fl_h + 10), outline=INK, width=2)
    note(f, (int(W * 0.70) + 100, int(H * 0.12)), "flamingo ≈8 % frame height,\nupper third, still flying", 24)
    note(f, (60, int(H * 0.36)), "ISLAND: aerial 3/4 view (not top-down),\nresolves centre as sea fills in from edges\n— continuous zoom-out, no cut", 26, fill=(255, 255, 255, 255))
    tag(f, "TO GENERATE (Seedream 4.5 island aerial + Kling zoom-out) — see pipeline doc §5.3")
    footer(f, 3, 4.6, 7.4, "pull back to the island — flamingo shrinks to ~8 %")
    frames.append(("03_pullback_island_TOGEN", f))

    # 04 — S4 07.4–10.2: camera settles; kite-surfer L→R lower third, flamingo R→L upper third
    f = island_plate(zoom=0.85)
    thirds(f)
    kitesurfer(f, x=int(W * 0.50), y=int(H * 0.82), size=1.0)
    arrow(f, (int(W * 0.22), int(H * 0.90)), (int(W * 0.78), int(H * 0.90)), colour=(255, 255, 255, 255))
    note(f, (int(W * 0.22), int(H * 0.91)), "KITE-SURFER: crosses bay left → right, lower third; blonde, small, back to camera, no face; spray trail", 24, fill=(255, 255, 255, 255))
    flamingo(f, cx=int(W * 0.42), feet_y=int(H * 0.14) + fl_h, height=fl_h, wings=True, facing=-1)
    arrow(f, (int(W * 0.68), int(H * 0.12)), (int(W * 0.30), int(H * 0.12)), colour=(200, 60, 90, 255))
    note(f, (int(W * 0.70), int(H * 0.10)), "flamingo continues right → left,\nupper third (crossing paths = the shot)", 24)
    tag(f, "TO GENERATE (Seedream 4.5 kite-surfer + Kling) — generic blonde man, NOT a likeness, see pipeline doc §5.3")
    footer(f, 4, 7.4, 10.2, "kite-surfer crosses lower third; flamingo crosses upper third opposite way")
    frames.append(("04_kitesurfer_TOGEN", f))

    # 05 — S5 10.2–13.0: push in on the court; two ring-tails rallying, hits at 10.8 / 11.6 / 12.4
    def tennis_scene():
        f = sky()
        d = ImageDraw.Draw(f)
        for y in range(int(H * 0.28), H):                                  # sea band behind court
            t = (y - H * 0.28) / (H * 0.72)
            d.line((0, y, W, y), fill=tuple(round(SEA_SHALLOW[i] * (1 - t) + PALM[i] * t) for i in range(3)) + (255,))
        for px in range(120, W, 260):                                       # palm line
            d.line((px, int(H * 0.30), px, int(H * 0.44)), fill=(70, 50, 30, 255), width=8)
            d.ellipse((px - 60, int(H * 0.22), px + 60, int(H * 0.34)), fill=PALM)
        thirds(f)
        court(f, (int(W * 0.14), int(H * 0.46), int(W * 0.86), int(H * 0.94)))
        lemur_standin(f, lem_a, feet=(int(W * 0.22), int(H * 0.92)), height=int(H * 0.44))
        lemur_standin(f, lem_b, feet=(int(W * 0.78), int(H * 0.80)), height=int(H * 0.34), flip=True)
        racket(f, (int(W * 0.255), int(H * 0.58)), (int(W * 0.31), int(H * 0.47)))
        racket(f, (int(W * 0.745), int(H * 0.53)), (int(W * 0.69), int(H * 0.44)))
        label_box(f, (int(W * 0.27), int(H * 0.78), int(W * 0.49), int(H * 0.86)), "LEMUR A — Miavana lemur2.png\nSTAND-IN, wrong pose, no racket", 20, fill=(255, 255, 255, 200))
        label_box(f, (int(W * 0.51), int(H * 0.66), int(W * 0.73), int(H * 0.74)), "LEMUR B — Miavana lemur3.png\nSTAND-IN, wrong pose, no racket", 20, fill=(255, 255, 255, 200))
        return f

    f = tennis_scene()
    for bx, by, t in ((int(W * 0.40), int(H * 0.52), "hit 10.8"), (int(W * 0.52), int(H * 0.46), "net"), (int(W * 0.64), int(H * 0.52), "hit 11.6")):
        ball(f, (bx, by))
        note(f, (bx, by - 20), t, 22, anchor="mb")
    note(f, (int(W * 0.50), int(H * 0.56)), "rally: hits at 10.8 / 11.6 / 12.4 s, ~14 f ball travel per exchange\nplay it straight — proper form, no cartoon takes", 24, anchor="ma")
    tag(f, "TO GENERATE (Seedream 4.5 → NBP w/ Miavana refs, Kling) — lemurs playing tennis, see pipeline doc §5.3")
    footer(f, 5, 10.2, 13.0, "push in on the court — two ring-tails rallying, three hits")
    frames.append(("05_lemur_tennis_TOGEN", f))

    # 05b — fallback for S5 (pipeline doc §6): two static plates, ball animated in AE
    f = Image.alpha_composite(tennis_scene(), Image.new("RGBA", (W, H), (255, 255, 255, 70)))
    d = ImageDraw.Draw(f)
    pts = [(int(W * 0.30) + i * (int(W * 0.40) // 12), int(H * 0.56) - int(160 * math.sin(i / 12 * math.pi))) for i in range(13)]
    d.line(pts, fill=(200, 60, 90, 255), width=4, joint="curve")
    for i in (0, 6, 12):
        ball(f, pts[i])
    note(f, (int(W * 0.50), int(H * 0.60)), "FALLBACK: two static Seedream plates (A ready / B follow-through),\nball on a 14-frame arc keyed in AE, cut on each hit; swap plates per hit", 24, anchor="ma")
    tag(f, "FALLBACK FOR S5 — static plates + AE ball (pipeline doc §6). Use if Kling cannot hold rackets")
    footer(f, 5, 10.2, 13.0, "FALLBACK — static lemur plates, ball animated in comp")
    frames.append(("05b_tennis_AE_fallback", f))

    # 06 — S6 13.0–14.0: pull back to island wide; Necker / Virgin lock-up fades up
    f = island_plate(zoom=0.55, cy=int(H * 0.60))
    f = Image.alpha_composite(f, Image.new("RGBA", (W, H), (255, 255, 255, 175)))
    paste_logo(f, mark_rgba, width=520, cx=W // 2, top=int(H * 0.50) - 244)
    note(f, (W // 2, int(H * 0.50) + 270), "lock-up fades up over the island wide (whited ~70 % so the red reads); fade out at 14.0", 24, anchor="ma")
    tag(f, "Virgin mark (1320 px jpg, Lanczos resize) — confirm Necker lockup vs Virgin Limited Edition")
    footer(f, 6, 13.0, 14.0, "end card — pull back out to island wide, lock-up fades up, fade")
    frames.append(("06_endcard", f))

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
