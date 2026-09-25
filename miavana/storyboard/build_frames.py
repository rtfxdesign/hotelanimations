#!/usr/bin/env python3
"""Build the Miavana storyboard frames (v2) from the real assets.

Composites eight 1920x1080 frames (one per storyboard beat) from the Miavana
folder of a local pull of the Drive folder, plus a 4x2 contact sheet. Frames
that stand in for shots still to be generated are tagged in the corner.
Nothing under PULL_ROOT is modified; the one ffmpeg frame grab is written into
OUT_DIR/_work.

Usage:
    python miavana/storyboard/build_frames.py PULL_ROOT OUT_DIR

PULL_ROOT  local mirror of the Drive folder (tools/drive_pull.py); files are
           read from PULL_ROOT/Miavana/upscaled
OUT_DIR    where the PNG frames, *_small.jpg and contact_sheet.jpg go

v2 changes (client decisions, 2026-09-25):
  - MIAVANA line = the rasterised vector wordmark in assets/wordmarks/, fitted
    to the PSD wordmark bbox; ISLAND SANCTUARY and BY TIME+TIDE stay PSD layers
  - resort plate = resort_16x9.png (Allen's outpaint), scaled to cover HD
  - seated lemur stays on the M (PSD position); the first-A ALT frame is gone
  - frame 08 (loop point) is the same composite as frame 01, asserted
    pixel-identical before the annotations go on

Requires Pillow, numpy and ffmpeg on PATH. Layout comes from the PSD layer
bboxes in inventory/psd_layers_2026-09-25.md (canvas 2508x1411 -> 1920x1080).
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1920, 1080
PSD_W, PSD_H = 2508, 1411
S = W / PSD_W                       # 0.7655 - PSD canvas to HD
SAGE = (157, 200, 183, 255)         # sampled from miavana_0005_Layer-0.png

REPO = Path(__file__).resolve().parents[2]
WORDMARK = REPO / "assets" / "wordmarks" / "miavana_wordmark.png"   # 3919x604 RGBA, white letterforms
WORDMARK_BBOX = (145, 427, 2405, 628)   # PSD bbox of the raster `miavana` layer the vector replaces

# PSD layer bboxes (x0, y0) in 2508x1411 canvas space - inventory/psd_layers_2026-09-25.md
LAYERS = {
    "left_lemur": ("miavana_0000_left_lemur.png", (44, 230)),      # seated on the M
    "right_lemur": ("miavana_0001_right_lemur.png", (2208, 420)),  # hanging from the last A
    "islandsanctuary": ("miavana_0003_islandsanctuary.png", (439, 835)),
    "bytimeandtide": ("miavana_0004_bytimeandtide.png", (988, 1270)),
}
LEFT_HAND = (270, 450)              # PSD: tip of the seated lemur's reaching hand (catch point)
RIGHT_HANDS = (2286, 850)           # PSD: clasped hands of the hanging lemur (release point)
V_CENTRE_X = 145 + 1073             # PSD x of the V (arc apex sits over it)
CAP_TOP_Y = 427                     # PSD y of the wordmark cap height

RESORT = "resort_16x9.png"          # 4988x2806, Allen's 16:9 outpaint of the aerial
MANGO_CLIP = "a ring-tailed lemur produces a mango, throws it up and to the right.mp4"
MANGO_T = 2.0                       # seconds into the clip: mango held in both hands, unoccluded enough
MANGO_BOX = (358, 360, 483, 446)    # measured mango bbox in that 720x1280 frame
MANGO_W = 84                        # on-screen width at HD (crop is 125 px wide, so this is a down-scale)

FONT = next((p for p in [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
] if Path(p).exists()), None)


def font(size):
    return ImageFont.truetype(FONT, size) if FONT else ImageFont.load_default()


def hd(pt):
    """PSD canvas coordinate -> HD canvas coordinate."""
    return (round(pt[0] * S), round(pt[1] * S))


def scaled(im, s):
    return im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)


def fit_cover(im, w=W, h=H):
    """Scale to cover w x h and centre-crop the remainder (none for a true 16:9 source)."""
    s = max(w / im.width, h / im.height)
    im = scaled(im, s)
    x = (im.width - w) // 2
    y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def alpha_crop(im):
    return im.crop(im.getchannel("A").getbbox())


def with_opacity(im, opacity):
    if opacity >= 1.0:
        return im
    im = im.copy()
    im.putalpha(im.getchannel("A").point(lambda v: int(v * opacity)))
    return im


def tag(im, text, colour=(255, 176, 32), row=0):
    d = ImageDraw.Draw(im)
    f = font(30)
    tw = d.textlength(text, font=f)
    y = 24 + row * 60
    d.rectangle((24, y, 24 + tw + 28, y + 52), fill=(0, 0, 0, 220))
    d.text((38, y + 8), text, font=f, fill=colour)


def caption(im, text):
    """Beat / timecode strip along the bottom edge."""
    d = ImageDraw.Draw(im)
    f = font(26)
    tw = d.textlength(text, font=f)
    d.rectangle((24, H - 24 - 46, 24 + tw + 28, H - 24), fill=(0, 0, 0, 200))
    d.text((38, H - 24 - 38), text, font=f, fill=(235, 235, 235))


def blank():
    return Image.new("RGBA", (W, H), SAGE)


def dashed_curve(im, p0, p1, p2, colour=(255, 176, 32, 230), width=4, dash=18):
    """Dashed quadratic Bezier p0 -> p2 with control p1 (throw-arc annotation)."""
    d = ImageDraw.Draw(im)
    pts = []
    for i in range(121):
        t = i / 120
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        pts.append((x, y))
    on, run = True, 0.0
    for a, b in zip(pts, pts[1:]):
        seg = ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5
        if on:
            d.line([a, b], fill=colour, width=width)
        run += seg
        if run >= dash:
            on, run = not on, 0.0
    # arrow head at p2
    d.ellipse((p2[0] - 8, p2[1] - 8, p2[0] + 8, p2[1] + 8), fill=colour)


# --------------------------------------------------------------------------- assets

def load_layers(up):
    out = {}
    for key, (fn, origin) in LAYERS.items():
        out[key] = (Image.open(up / fn).convert("RGBA"), origin)
    return out


def load_wordmark():
    """Vector MIAVANA rasterisation, alpha-cropped and fitted to the PSD wordmark bbox at HD.

    Fitted by width (letter x-positions match the PSD raster to <0.1 % of the
    width, so the lemur seats on the M and the final A do not move); the
    0.6 % taller vector aspect is centred on the PSD bbox height.
    """
    x0, y0, x1, y1 = WORDMARK_BBOX
    bw, bh = round((x1 - x0) * S), round((y1 - y0) * S)
    g = alpha_crop(Image.open(WORDMARK).convert("RGBA"))
    g = scaled(g, bw / g.width)
    origin = (hd((x0, 0))[0], hd((0, y0))[1] + (bh - g.height) // 2)
    return g, origin


def paste_layer(canvas, layers, key, opacity=1.0):
    im, (x0, y0) = layers[key]
    im = with_opacity(scaled(im, S), opacity)
    canvas.alpha_composite(im, hd((x0, y0)))
    return canvas


def lockup(canvas, layers, wordmark_im, wordmark=1.0, lemurs=1.0):
    """The lock-up: vector MIAVANA + PSD ISLAND SANCTUARY / BY TIME+TIDE + PSD lemurs, placed by bbox."""
    g, origin = wordmark_im
    canvas.alpha_composite(with_opacity(g, wordmark), origin)
    for key in ("islandsanctuary", "bytimeandtide"):
        paste_layer(canvas, layers, key, opacity=wordmark)
    if lemurs > 0:
        paste_layer(canvas, layers, "left_lemur", opacity=lemurs)
        paste_layer(canvas, layers, "right_lemur", opacity=lemurs)
    return canvas


def grab_mango(up, work):
    """Extract one frame from the Kling mango clip and cut the mango out by colour."""
    work.mkdir(parents=True, exist_ok=True)
    frame = work / f"mango_t{MANGO_T:.1f}.png"
    if not frame.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(MANGO_T), "-i", str(up / MANGO_CLIP),
                        "-frames:v", "1", str(frame)], check=True)
    m = 8
    x0, y0, x1, y1 = MANGO_BOX
    crop = Image.open(frame).convert("RGB").crop((x0 - m, y0 - m, x1 + m, y1 + m))
    a = np.array(crop).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mask = ((r > 160) & (g > 80) & (b < 140) & (r - b > 80)).astype(np.uint8) * 255
    # close pin-holes without growing into the grey fingers, then feather
    mask = Image.fromarray(mask).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
    mask = mask.filter(ImageFilter.GaussianBlur(1.0))
    out = crop.convert("RGBA")
    out.putalpha(mask)
    out = alpha_crop(out)
    out.save(work / "mango_cutout.png")
    return out


def paste_mango(canvas, mango, centre, width=MANGO_W, angle=0):
    s = width / mango.width
    m = scaled(mango, s)
    if angle:
        m = m.rotate(angle, resample=Image.BICUBIC, expand=True)
    canvas.alpha_composite(m, (round(centre[0] - m.width / 2), round(centre[1] - m.height / 2)))
    return canvas


def paste_fit_bbox(canvas, cutout, top_left, height, align="centre"):
    """Scale an alpha cut-out to `height` px and place its top edge at top_left (HD)."""
    g = alpha_crop(cutout)
    g = scaled(g, height / g.height)
    x, y = top_left
    if align == "centre":
        x = x - g.width // 2
    canvas.alpha_composite(g, (round(x), round(y)))
    return canvas


# --------------------------------------------------------------------------- frames

def main():
    pull, out = (Path(a).expanduser().resolve() for a in sys.argv[1:3])
    out.mkdir(parents=True, exist_ok=True)
    up = pull / "Miavana" / "upscaled"
    work = out / "_work"

    layers = load_layers(up)
    wm = load_wordmark()
    mango = grab_mango(up, work)
    resort = fit_cover(Image.open(up / RESORT).convert("RGBA"))
    big_seated = Image.open(up / "lemur.png").convert("RGBA")
    big_hanging = Image.open(up / "Firefly_remove background 477817 (1).png").convert("RGBA")

    # screen positions of the two lemurs, straight from the PSD bboxes
    left_box = (hd((44, 230)), hd((270, 862)))          # (34,176)-(207,660)
    right_box = (hd((2208, 420)), hd((2364, 1023)))     # (1690,322)-(1810,783)
    release = hd(RIGHT_HANDS)
    catch = hd(LEFT_HAND)
    apex = (hd((V_CENTRE_X, 0))[0], hd((0, CAP_TOP_Y))[1] - 130)   # clears cap height over the V
    ctrl = (apex[0], 2 * apex[1] - (release[1] + catch[1]) / 2)     # Bezier control so the curve passes through apex
    mango_in_hand = (release[0] + 6, release[1] - 6)

    def loop_frame():
        """Beat 1 = beat 6: the lock-up with the mango in the hanging lemur's hands."""
        f = lockup(blank(), layers, wm)
        return paste_mango(f, mango, mango_in_hand)

    frames = []

    # 01 - Beat 1 (f0-58): the lock-up, mango already in the hanging lemur's hands
    first = loop_frame()
    f = first.copy()
    tag(f, "LOCK-UP: vector MIAVANA fitted to the PSD bbox; other two lines + lemurs = PSD layers")
    tag(f, "TO GENERATE (Flux) - mango prop (shown: crop from Kling clip, 720x1280)", row=1)
    caption(f, "BEAT 1  HOLD  00.0-02.4  f0-58")
    frames.append(("01_lockup", f))

    # 02 - Beat 2a (f58-72): wind-up. The hanging lemur needs one free arm - a Kling re-pose
    f = lockup(blank(), layers, wm)
    paste_mango(f, mango, (release[0] + 40, release[1] - 60), angle=-20)
    tag(f, "TO GENERATE (Kling) - wind-up pose: hanging lemur with one free arm, 12-frame anticipation hold")
    caption(f, "BEAT 2a  SETUP / WIND-UP  02.4-03.0  f58-72")
    frames.append(("02_windup_TOGEN", f))

    # 03 - Beat 2b (f72-92): the throw - Flux mango on a 2D arc over the breathing stills
    f = lockup(blank(), layers, wm)
    dashed_curve(f, release, ctrl, catch)
    paste_mango(f, mango, apex, angle=35)
    tag(f, "2D ARC (AE) - Flux mango prop tumbles along this Bezier over the breathing stills; no Kling for the throw")
    tag(f, "arc right-to-left, apex over the V, clears cap height, passes IN FRONT of the type", row=1)
    caption(f, "BEAT 2b  THE THROW  03.0-03.8  f72-92")
    frames.append(("03_throw_2D", f))

    # 04 - Beat 2c (f92-101): the catch, one-handed, by the seated lemur
    f = lockup(blank(), layers, wm)
    paste_mango(f, mango, (catch[0] + 10, catch[1] - 4), width=72)
    tag(f, "TO GENERATE (Kling) - catch pose: seated lemur, one hand out, head tracks the mango; body otherwise still")
    caption(f, "BEAT 2c  CATCH  03.8-04.2  f92-101")
    frames.append(("04_catch_TOGEN", f))

    # 05 - Beat 3 (f101-149): sage dissolves to the 16:9 resort plate, wordmark holding then fading
    f = Image.blend(blank(), resort.filter(ImageFilter.GaussianBlur(3)), 0.6)
    lockup(f, layers, wm, wordmark=0.55, lemurs=1.0)
    paste_mango(f, mango, (catch[0] + 10, catch[1] - 4), width=72)
    tag(f, "COMP - cross-dissolve mid-point over resort_16x9.png; letters under the lemurs resolve into palm trunks")
    caption(f, "BEAT 3  SAGE BECOMES ISLAND  04.2-06.2  f101-149")
    frames.append(("05_reveal_COMP", f))

    # 06 - Beat 4 (f149-230): lemurs in the palms, same screen positions as on the letterforms
    f = resort.copy()
    paste_fit_bbox(f, big_seated, ((left_box[0][0] + left_box[1][0]) // 2, left_box[0][1]),
                   left_box[1][1] - left_box[0][1])
    paste_fit_bbox(f, big_hanging, ((right_box[0][0] + right_box[1][0]) // 2, right_box[0][1]),
                   right_box[1][1] - right_box[0][1])
    low_apex = (apex[0], apex[1] + 90)     # second toss: shorter and lower than Beat 2b, thrown BACK
    low_ctrl = (low_apex[0], 2 * low_apex[1] - (release[1] + catch[1]) / 2)
    dashed_curve(f, catch, low_ctrl, release)   # left-to-right: mango returns to the hanging lemur for the loop
    paste_mango(f, mango, low_apex, width=66, angle=-35)
    tag(f, "TO GENERATE (NBP) - lemurs in real palm crowns at these positions (shown: lemur.png + Firefly cut-out)")
    tag(f, "second toss at 07.8 thrown BACK, left-to-right, apex 90 px lower - mango is home for the loop", row=1)
    caption(f, "BEAT 4  UP IN THE PALMS  06.2-09.6  f149-230  (slow aerial drift R-to-L, 6%)")
    frames.append(("06_palms_TOGEN", f))

    # 07 - Beat 5 (f230-274): resort dissolves out, sage returns, letters re-form under the lemurs
    f = Image.blend(blank(), resort.filter(ImageFilter.GaussianBlur(6)), 0.3)
    lockup(f, layers, wm, wordmark=0.75, lemurs=1.0)
    tag(f, "COMP - reverse cross-dissolve; lemurs land back in their Beat 1 positions")
    caption(f, "BEAT 5  BACK TO THE MARK  09.6-11.4  f230-274")
    frames.append(("07_return_COMP", f))

    # 08 - Beat 6 (f274-288): hold = beat 1, mango back in hand. Same composite as frame 01 -> clean loop
    last = loop_frame()
    assert np.array_equal(np.array(first), np.array(last)), "loop frame drifted from frame 01"
    f = last.copy()
    tag(f, "LOOP POINT - pixel-identical to frame 01 (asserted in build): mango back in hand, lemurs in place")
    caption(f, "BEAT 6  HOLD  11.4-12.0  f274-288  -> cuts to f0")
    frames.append(("08_hold_LOOP", f))

    for name, im in frames:
        im.convert("RGB").save(out / f"{name}.png", optimize=True)
        im.convert("RGB").resize((960, 540), Image.LANCZOS).save(out / f"{name}_small.jpg", quality=88)

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
    print(f"{len(frames)} frames -> {out}  (frame 08 == frame 01 before annotation: verified)")


if __name__ == "__main__":
    main()
