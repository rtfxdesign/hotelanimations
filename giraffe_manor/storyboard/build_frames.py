#!/usr/bin/env python3
"""Build the Giraffe Manor storyboard frames (v2) from the real assets.

Composites twelve 1920x1080 frames (one per storyboard beat, plus 06b, the
loop return and the loop frame) from files in a local pull of the Drive
folder, the approved vector wordmark, and three walk-cycle frames, plus a
3-column contact sheet.
Frames that stand in for shots still to be generated are tagged in the corner.

v2 changes: vector wordmark (no placeholders), walker colour-matched to the
hero for the board, exterior-window payoff only, and a loop return so the
last frame of the film equals the first (11_loop is pixel-identical to
01_hold; the script asserts it).

Usage:
    python giraffe_manor/storyboard/build_frames.py PULL_ROOT WALK_FRAMES_DIR OUT_DIR [WORDMARK_PNG]

PULL_ROOT       local mirror of the Drive folder (tools/drive_pull.py)
WALK_FRAMES_DIR folder with walk_t0.0.png, walk_t1.4.png, walk_t2.8.png
                (1920x1080 RGBA frames from giraffe_walking.mov at those times)
OUT_DIR         where the PNG frames and contact sheet go
WORDMARK_PNG    rasterised vector mark, RGBA (default: assets/wordmarks/
                giraffe_manor_wordmark.png in this repo)

Requires Pillow only. Layout constants are at the top; change W/H for other masters.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageStat

W, H = 1920, 1080
CREAM = (255, 255, 240, 255)
HERO_H = 800          # hero giraffe opaque height on the canvas
HERO_CX = 760         # hero centre x
FEET_Y = 880          # hero hoof line
LOGO_W = 640          # vector wordmark width under the hooves (3952x703 source -> 640x114)
LOGO_TOP = 912
MARK_W = 400          # small end mark, bottom-right, during the return dissolve
WALKER_STOP_LEFT = 1060   # second giraffe bbox-left when it stops
WALKER_FEET_Y = 885
DEFAULT_WORDMARK = Path(__file__).resolve().parents[2] / "assets" / "wordmarks" / "giraffe_manor_wordmark.png"

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
    d = ImageDraw.Draw(im)
    f = font(30)
    tw = d.textlength(text, font=f)
    y = 24 + row * 62
    d.rectangle((24, y, 24 + tw + 28, y + 52), fill=(0, 0, 0, 220))
    d.text((38, y + 8), text, font=f, fill=colour)


def blank():
    return Image.new("RGBA", (W, H), CREAM)


def colour_match(src, ref, max_gain=1.35):
    """Per-channel levels so src's opaque pixels take ref's mean and spread.

    A board-only stand-in for regenerating the walker from the hero: the Kling
    walker is a darker, more saturated animal than the hero still. Gains are
    capped so the pale patches do not blow out on the cream field.
    """
    def stat(im):
        mask = im.getchannel("A").point(lambda v: 255 if v > 200 else 0)
        s = ImageStat.Stat(im.convert("RGB"), mask=mask)
        return s.mean, s.stddev
    sm, ss = stat(src)
    rm, rs = stat(ref)
    bands = []
    for c, band in enumerate(src.convert("RGB").split()):
        g = min(max_gain, rs[c] / ss[c])
        o = rm[c] - sm[c] * g
        bands.append(band.point(lambda v, g=g, o=o: max(0, min(255, round(v * g + o)))))
    out = Image.merge("RGB", bands).convert("RGBA")
    out.putalpha(src.getchannel("A"))
    return out


def paste_hero(canvas, hero, scale=1.0, cx=HERO_CX, feet=FEET_Y):
    g = alpha_crop(hero)
    s = HERO_H / g.height * scale
    g = g.resize((round(g.width * s), round(g.height * s)), Image.LANCZOS)
    canvas.alpha_composite(g, (cx - g.width // 2, feet - g.height))
    return canvas


def paste_walker(canvas, walker, left, feet=WALKER_FEET_Y, scale=1.0):
    g = alpha_crop(walker)
    if scale != 1.0:
        g = g.resize((round(g.width * scale), round(g.height * scale)), Image.LANCZOS)
    canvas.alpha_composite(g, (left, feet - g.height))
    return canvas


def paste_logo(canvas, logo, width=LOGO_W, cx=HERO_CX, top=LOGO_TOP, opacity=1.0):
    s = width / logo.width
    l = logo.resize((width, round(logo.height * s)), Image.LANCZOS)
    if opacity < 1.0:
        a = l.getchannel("A").point(lambda v: int(v * opacity))
        l.putalpha(a)
    canvas.alpha_composite(l, (cx - width // 2, top))
    return canvas


def paste_end_mark(canvas, logo, width=MARK_W, margin=60, opacity=1.0):
    """Small mark bottom-right on a cream card, so the brown mark reads over the photo."""
    s = width / logo.width
    lw, lh = width, round(logo.height * s)
    pad = 22
    card = Image.new("RGBA", (lw + 2 * pad, lh + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(card).rounded_rectangle((0, 0, card.width - 1, card.height - 1), radius=14,
                                           fill=(255, 255, 240, 225))
    card.alpha_composite(logo.resize((lw, lh), Image.LANCZOS), (pad, pad))
    if opacity < 1.0:
        card.putalpha(card.getchannel("A").point(lambda v: int(v * opacity)))
    canvas.alpha_composite(card, (W - margin - card.width, H - margin - card.height))
    return canvas


def main():
    pull, walkdir, out = (Path(a).expanduser().resolve() for a in sys.argv[1:4])
    wordmark = Path(sys.argv[4]).expanduser().resolve() if len(sys.argv) > 4 else DEFAULT_WORDMARK
    out.mkdir(parents=True, exist_ok=True)
    gm = pull / "Giraffe Manor"
    hero = Image.open(gm / "upscaled" / "ea5d5cfc-e93b-4d86-acf6-81bba6e7bd70.png").convert("RGBA")
    logo = Image.open(wordmark).convert("RGBA")
    ref_ext = fit_cover(Image.open(gm / "images-2.jpg").convert("RGBA"))
    walk_raw = {t: Image.open(walkdir / f"walk_t{t}.png").convert("RGBA") for t in ("0.0", "1.4", "2.8")}
    walk = {t: colour_match(im, hero) for t, im in walk_raw.items()}
    WALKER_TAG = "WALKER COLOUR-MATCHED FOR BOARD — regenerate the walk from the hero as reference"

    frames = []

    # 01 — Beat 1: the giraffe, alone on cream. Also the loop frame (see 11).
    hold = paste_hero(blank(), hero)
    frames.append(("01_hold", hold.copy()))

    # 02 — Beat 2: the vector wordmark appears under its feet
    f = paste_logo(paste_hero(blank(), hero), logo)
    frames.append(("02_logo", f))

    # 03 — Beat 3a: second giraffe entering from frame right (walk cycle, real alpha)
    f = paste_logo(paste_hero(blank(), hero), logo)
    paste_walker(f, walk["0.0"], left=1500)
    tag(f, WALKER_TAG)
    frames.append(("03_enter", f))

    # 04 — Beat 3b: it stops beside the first; logo at 35 %
    f = paste_logo(paste_hero(blank(), hero), logo, opacity=0.35)
    paste_walker(f, walk["2.8"], left=WALKER_STOP_LEFT)
    tag(f, WALKER_TAG)
    frames.append(("04_stop", f))

    # Plate-locked staging for beats 4-6 (approved). The manor plate arrives at
    # the zoom where its own giraffes match ours (z=2.65 x cover), then the
    # camera zooms out to the full plate (z=1.0). Giraffes are positioned in
    # PLATE pixels so they scale and move with the zoom. Pivot chosen so feet
    # sit at y=880 at z=2.65 and the plate exactly covers the frame at z=1.0.
    plate_src = Image.open(gm / "upscaled" / "manor01_background.png").convert("RGBA")
    S0 = H / plate_src.height                       # cover scale, 0.703
    X0 = (W - plate_src.width * S0) / 2             # -7 px
    PIV = (2140, 1490)                              # plate px
    HERO_P = (1744, 1400)                           # hero feet, plate px (foot of the steps)
    WALK_P = (2050, 1400)                           # walker feet, plate px
    G_H_PLATE = HERO_H / (S0 * 2.65)                # giraffe height in plate px (~429)

    def plate_at(z, blur=0):
        s = S0 * z
        im = plate_src.resize((round(plate_src.width * s), round(plate_src.height * s)), Image.LANCZOS)
        if blur:
            im = im.filter(ImageFilter.GaussianBlur(blur))
        ox = round(PIV[0] * S0 + X0 - PIV[0] * s)
        oy = round(PIV[1] * S0 - PIV[1] * s)
        canvas = blank()
        canvas.alpha_composite(im, (ox, oy))
        return canvas, (lambda px, py: (round(ox + px * s), round(oy + py * s))), s

    def stage(z, blur=0, blend_cream=0.0):
        canvas, to_canvas, s = plate_at(z, blur)
        if blend_cream:
            canvas = Image.blend(blank(), canvas, 1 - blend_cream)
        gh = G_H_PLATE * s
        hx, hy = to_canvas(*HERO_P)
        g = alpha_crop(hero); k = gh / g.height
        g = g.resize((round(g.width * k), round(g.height * k)), Image.LANCZOS)
        canvas.alpha_composite(g, (hx - g.width // 2, hy - g.height))
        wx, wy = to_canvas(*WALK_P)
        wk = alpha_crop(walk["2.8"]); k = gh / wk.height
        wk = wk.resize((round(wk.width * k), round(wk.height * k)), Image.LANCZOS)
        canvas.alpha_composite(wk, (wx - wk.width // 2, wy - wk.height))
        return canvas

    # 05 — Beat 4a: logo gone, cream dissolving to the manor, at scale, soft
    f = stage(2.65, blur=10, blend_cream=0.45)
    frames.append(("05_reveal", f))

    # 06 — Beat 4b: manor sharp behind both, still at scale (terrace + ground floor)
    f = stage(2.65)
    tag(f, "PLATE AT 2.65x COVER — giraffes at true scale to the manor's own giraffes")
    tag(f, WALKER_TAG, row=1)
    frames.append(("06_manor", f))

    # 06b — camera zooms out; giraffes shrink with the plate
    f = stage(1.6)
    tag(f, "ZOOM OUT IN PROGRESS (COMP) — camera pulls back, giraffes locked to the plate")
    frames.append(("06b_zoomout", f))

    # 07 — Beat 5a: full plate; both turn and walk toward the manor — TO GENERATE from this frame
    f = stage(1.0)
    tag(f, "TO GENERATE (KLING) — start frame: both turn away and walk up to the house")
    tag(f, WALKER_TAG, row=1)
    frames.append(("07_turn_TOGEN", f))

    # 08 — Beat 5b: heads in the upstairs windows — TO GENERATE; client reference photo of the target
    f = ref_ext.copy()
    tag(f, "TO GENERATE (KLING) — heads through the upstairs windows. Shown: client reference images-2.jpg (678 px)")
    frames.append(("08_window_TOGEN", f))

    # 09 — Beat 6: hold on the payoff, small mark bottom-right (the end card now lives here)
    payoff = paste_end_mark(ref_ext.copy(), logo)
    frames.append(("09_payoff_mark", payoff.copy()))

    # 10 — Beat 7 (loop return): payoff + mark dissolve back to the cream field, hero alone
    f = Image.blend(payoff, hold, 0.5)
    tag(f, "RETURN DISSOLVE (COMP), shown at 50 % — payoff and mark dissolve to the hero alone; lands on 01_hold")
    frames.append(("10_return_COMP", f))

    # 11 — Loop frame: pixel-identical to 01_hold, so the last frame equals the first
    frames.append(("11_loop", hold.copy()))
    assert frames[-1][1].tobytes() == frames[0][1].tobytes(), "11_loop must equal 01_hold"

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
    print(f"{len(frames)} frames -> {out}  (11_loop == 01_hold verified)")


if __name__ == "__main__":
    main()
