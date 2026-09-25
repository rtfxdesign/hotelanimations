#!/usr/bin/env python3
"""Build the Passalacqua (Lago di Como) storyboard frames -- v2.

Composites eleven 1920x1080 frames (one per beat of timing doc v1 section 3
plus Allen's return beat and the loop frame; 15.0 s @ 24 fps) from the real
assets, plus a contact sheet. Frames that stand in for shots still to be
generated are tagged in the corner. Frame 11 is pixel-identical to frame 01
before tagging (the script asserts it) -- that is the loop.

Usage:
    python passalacqua/storyboard/build_frames.py PULL_ROOT OUT_DIR

PULL_ROOT  local mirror of the Drive folder (contains `Passalaqua/`)
OUT_DIR    where the PNG frames, *_small.jpg and contact_sheet.jpg go

Requires Pillow only. Layout constants are at the top.

Sources (all measured 2026-09-25, alpha threshold 20):
  assets/wordmarks/passalacqua_wordmark.png  4000x2200 RGBA, the vector crest
        rasterised: black line art, three fish / wave rule / PASSALACQUA /
        LAGO DI COMO. Row bands found in the alpha:
            fish        rows   76-1010   (cols 1474-2543; fish split at x=1821, 2184)
            wave rule   rows 1011-1151   (cols 1512-2467)
            PASSALACQUA rows 1390-1761   (cols  404-3607)
            LAGO DI COMO rows 1900-2009  (cols 1131-2880)
        The beat-1/2 artwork. Never AI-enlarged; placed at 0.393x (crest 760 px
        tall on the 1080 frame, fish 367 px = 34 % of frame height).
  Passalaqua/passalacqua.png  7872x4428 RGBA, Allen's render of the same crest
        with the three fish as dimensional gold, wave rule gold, words black.
        Layer bboxes from passalacqua.psd (psd-tools; `passalacqua copy.psd`
        is identical): fish (3278,760,4720,2056), waves (3280,2195,4592,2388),
        text (1412,2380,6489,3525). Alpha bands agree: fish rows 761-2055 in
        three columns 3279-3733 / 3773-4229 / 4266-4720. The fish are cropped
        from the PNG on their own alpha (no white-threshold key any more) for
        beats 3-5 and 8-9. Its wordmark is a different scale/cut of the type and
        is not used; its gold wave rule is not used (the rule stays line art).
  Passalaqua/passalacqua_words.png / _words@2x.png  wordmark only (1923x372 /
        3844x742). Not needed: the crest PNG already carries the type on
        separate row bands.
  Passalaqua/b74514e7-*.png  1536x1024  the leap: three gold fish breaching
        in sync, villa behind. Only lake plate; fish baked in.
  Passalaqua/46e10c0f-*.png  1421x1107  earlier lock-up render; superseded by
        passalacqua.png, not used.
  Passalaqua/images-3.jpg, passalacqua.jpg  small villa photo / 410 px mark;
        superseded, not used.
"""
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont

W, H = 1920, 1080
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)

# --- the vector crest (4000x2200) -- row bands and boxes in source px
FISH_ROWS = (76, 1010)
WAVE_ROWS = (1011, 1151)
WORD_ROWS = (1390, 1761)                 # PASSALACQUA
SUB_ROWS = (1900, 2009)                  # LAGO DI COMO
TYPE_ROWS = (1390, 2009)                 # both lines
CREST_BBOX = (404, 76, 3607, 2009)       # whole lock-up
FISH_BOX = (1474, 76, 2543, 1010)        # the three fish
FISH_SPLITS = (1821, 2184)               # empty columns between the fish
CREST_HEIGHT_ON_FRAME = 760              # lock-up height in the 1080 frame
CREST_SCALE = CREST_HEIGHT_ON_FRAME / (CREST_BBOX[3] - CREST_BBOX[1])   # 0.393

# --- the gold render (7872x4428) -- per-fish boxes (PSD 'fish' layer, alpha-tight)
GOLD_FISH_BOXES = [(3279, 761, 3733, 2055), (3773, 761, 4229, 2055), (4266, 761, 4720, 2055)]
GOLD_BLOCK = (3279, 761, 4720, 2055)

FONT = next((p for p in [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
] if Path(p).exists()), None)


def font(size):
    return ImageFont.truetype(FONT, size) if FONT else ImageFont.load_default()


def fit_cover(im, w=W, h=H, zoom=1.0):
    """Scale to cover w x h (times zoom) and crop the centre."""
    s = max(w / im.width, h / im.height) * zoom
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def tag(im, *lines, colour=(255, 176, 32)):
    """Corner tag, one or more lines (same look as the Giraffe Manor board)."""
    d = ImageDraw.Draw(im)
    f = font(30)
    tw = max(d.textlength(t, font=f) for t in lines)
    d.rectangle((24, 24, 24 + tw + 28, 24 + 52 * len(lines)), fill=(0, 0, 0, 220))
    for i, t in enumerate(lines):
        d.text((38, 32 + 52 * i), t, font=f, fill=colour)


def blank(colour=WHITE):
    return Image.new("RGBA", (W, H), colour)


def scaled(im, s):
    return im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)


def with_opacity(im, opacity):
    if opacity >= 1.0:
        return im
    im = im.copy()
    im.putalpha(im.getchannel("A").point(lambda v: int(v * opacity)))
    return im


def recolour(im, rgb):
    """Keep the alpha, replace the colour (black line art -> white over the lake)."""
    out = Image.new("RGBA", im.size, rgb + (255,))
    out.putalpha(im.getchannel("A"))
    return out


# ---------------------------------------------------------------- the crest
class Crest:
    """The vector crest scaled once and positioned so the lock-up is centred."""

    def __init__(self, path):
        src = Image.open(path).convert("RGBA")
        self.s = CREST_SCALE
        self.im = scaled(src, self.s)
        x0, y0, x1, y1 = CREST_BBOX
        self.ox = round(W / 2 - (x0 + x1) / 2 * self.s)
        self.oy = round(H / 2 - (y0 + y1) / 2 * self.s)

    def band(self, rows, opacity=1.0, rgb=None):
        y0, y1 = round(rows[0] * self.s), round(rows[1] * self.s)
        layer = self.im.crop((0, y0, self.im.width, y1))
        if rgb is not None:
            layer = recolour(layer, rgb)
        return with_opacity(layer, opacity), (self.ox, self.oy + y0)

    def paste_bands(self, canvas, *bands):
        for rows, opacity in bands:
            layer, pos = self.band(rows, opacity)
            canvas.alpha_composite(layer, pos)
        return canvas

    def fish_box(self):
        x0, y0, x1, y1 = FISH_BOX
        return (self.ox + round(x0 * self.s), self.oy + round(y0 * self.s),
                self.ox + round(x1 * self.s), self.oy + round(y1 * self.s))

    def fish_boxes(self):
        """The three fish as frame boxes, split at the empty columns."""
        xs = (FISH_BOX[0],) + FISH_SPLITS + (FISH_BOX[2],)
        return [(self.ox + round(xs[i] * self.s), self.oy + round(FISH_ROWS[0] * self.s),
                 self.ox + round(xs[i + 1] * self.s), self.oy + round(FISH_ROWS[1] * self.s))
                for i in range(3)]

    def fish_layer(self, i):
        x0, y0, x1, y1 = self.fish_boxes()[i]
        return self.im.crop((x0 - self.ox, y0 - self.oy, x1 - self.ox, y1 - self.oy)), (x0, y0)

    def wave_centre(self):
        return (W // 2, self.oy + round((WAVE_ROWS[0] + WAVE_ROWS[1]) / 2 * self.s))


# ---------------------------------------------------------------- the gold fish
def gold_block_registered(gold, crest, scale=1.0):
    """The three gold fish scaled to sit exactly on the line-art fish."""
    fx0, fy0, fx1, fy1 = crest.fish_box()
    block = gold.crop(GOLD_BLOCK)
    block = scaled(block, (fy1 - fy0) / block.height * scale)
    cx, cy = (fx0 + fx1) // 2, (fy0 + fy1) // 2
    return block, (cx - block.width // 2, cy - block.height // 2)


def gold_fish_registered(gold, crest, i, scale=1.0, rot=0):
    """One gold fish scaled/positioned onto its line-art counterpart, optionally rotated."""
    fx0, fy0, fx1, fy1 = crest.fish_boxes()[i]
    f = gold.crop(GOLD_FISH_BOXES[i])
    f = scaled(f, (fy1 - fy0) / f.height * scale)
    if rot:
        f = f.rotate(rot, resample=Image.BICUBIC, expand=True)
    cx, cy = (fx0 + fx1) // 2, (fy0 + fy1) // 2
    return f, (cx - f.width // 2, cy - f.height // 2)


def gold_fish_free(gold, i, height, rot=0):
    """A gold fish on its own alpha at an arbitrary height (drop-in / rise)."""
    f = gold.crop(GOLD_FISH_BOXES[i])
    f = scaled(f, height / f.height)
    if rot:
        f = f.rotate(rot, resample=Image.BICUBIC, expand=True)
    return f


def vertical_mask(layer, keep_from, keep_to, blur=6):
    """Alpha-multiply a layer so only rows keep_from..keep_to (fractions) remain."""
    m = Image.new("L", layer.size, 0)
    ImageDraw.Draw(m).rectangle((0, int(layer.height * keep_from), layer.width,
                                 int(layer.height * keep_to)), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(blur))
    out = layer.copy()
    out.putalpha(ImageChops.multiply(out.getchannel("A"), m))
    return out


def cast_shadow(canvas, layer, pos, dy=18, blur=14, alpha=70):
    sh = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    sh.putalpha(layer.getchannel("A").point(lambda v: int(v * alpha / 255)))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(sh, (pos[0] + 6, pos[1] + dy))


def ripple_rings(canvas, cx, cy, n=4, rx0=90, ry0=22, step=1.45, alpha=150, rgb=(255, 255, 255), width=3):
    d = ImageDraw.Draw(canvas)
    rx, ry = rx0, ry0
    for i in range(n):
        a = int(alpha * (1 - i / n))
        d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), outline=rgb + (a,), width=width)
        rx, ry = rx * step, ry * step


# ---------------------------------------------------------------- frames
def main():
    pull, out = (Path(a).expanduser().resolve() for a in sys.argv[1:3])
    out.mkdir(parents=True, exist_ok=True)
    src = pull / "Passalaqua"
    here = Path(__file__).resolve().parent
    crest = Crest(here.parents[1] / "assets" / "wordmarks" / "passalacqua_wordmark.png")
    gold = Image.open(src / "passalacqua.png").convert("RGBA")
    leap = Image.open(src / "b74514e7-03e1-4fab-98a6-e903c4f48506.png").convert("RGBA")

    fx0, fy0, fx1, fy1 = crest.fish_box()
    fish_h = fy1 - fy0
    wave_cx, wave_cy = crest.wave_centre()
    frames = []

    # 01 -- Beat 1 (00.0-02.0): the line-art fish + wave rule on white, dead still. THE LOOP FRAME.
    art01 = crest.paste_bands(blank(), (FISH_ROWS, 1.0), (WAVE_ROWS, 1.0))
    loop_bytes = art01.tobytes()
    f = art01.copy()
    tag(f, "Beat 1 (f0-48) - vector crest, fish + wave rule, no type. Dead still: this is frame 0 = frame 360",
        "Draw-on dropped (loop rule) - the fish arrive via the return beat's gold drain instead")
    frames.append(("01_crest_still", f))

    # 02 -- Beat 2 (02.0-03.6): wordmark fades up beneath the wave rule (fixed artwork, no tracking)
    f = crest.paste_bands(blank(), (FISH_ROWS, 1.0), (WAVE_ROWS, 1.0), (TYPE_ROWS, 1.0))
    tag(f, "Beat 2 (f48-86) - PASSALACQUA / LAGO DI COMO fades up 0->1 over 0.8 s, then holds 0.8 s",
        "Wordmark is fixed artwork: opacity only, no tracking animation, no rise")
    frames.append(("02_wordmark", f))

    # 03 -- Beat 3 (03.6-05.0): type out, gold floods each fish bottom-to-top (shown at ~55 %)
    f = crest.paste_bands(blank(), (FISH_ROWS, 1.0), (WAVE_ROWS, 1.0), (TYPE_ROWS, 0.35))
    block, pos = gold_block_registered(gold, crest)
    f.alpha_composite(vertical_mask(block, 0.45, 1.0), pos)
    tag(f, "Beat 3 (f86-120) - COMP: gold fish (passalacqua.png) over the line art, bottom-up wipe, shown 55 %",
        "Wordmark 1->0 f86-98. Fill L/C/R staggered 120 ms from f100. Wave rule stays line art")
    frames.append(("03_fill_COMP", f))

    # 04 -- Beat 4 (05.0-06.6): fish become real -- rotate to 3/4, cast shadow, first tail beat
    f = blank()
    crest.paste_bands(f, (WAVE_ROWS, 1.0))
    for i, (rot, dy) in enumerate(((-9, 8), (4, -12), (-5, 2))):
        layer, pos = gold_fish_registered(gold, crest, i, scale=1.15, rot=rot)
        pos = (pos[0] + (i - 1) * 14, pos[1] + dy - 12)
        cast_shadow(f, layer, pos)
        f.alpha_composite(layer, pos)
    tag(f, "Beat 4 (f120-158) - TO GENERATE (Kling): flat-on -> three-quarter, cast shadow, first tail beat, offset x3",
        "Shown: gold fish crops rotated -9 / +4 / -5 deg, push-in 15 %, shadows fall on the rule. Rule holds for beat 5")
    frames.append(("04_alive_TOGEN", f))

    # 05 -- Beat 5 (06.6-08.2): white dissolves to the lake; water rises; fish drop in
    lake = fit_cover(leap).filter(ImageFilter.GaussianBlur(8))
    f = Image.blend(blank(), lake, 0.55)
    water = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(water).rectangle((0, 740, W, H), fill=(40, 90, 120, 110))
    xs = [W // 2 - 300, W // 2, W // 2 + 300]
    for i, (cx, rot, dy) in enumerate(zip(xs, (-30, -22, -34), (40, 0, 70))):
        layer = gold_fish_free(gold, i, int(fish_h * 1.6), rot)
        f.alpha_composite(layer, (cx - layer.width // 2, 560 + dy))
    f.alpha_composite(water)
    for cx in xs:
        ripple_rings(f, cx, 800, n=3, rx0=110, ry0=26, alpha=120)
    tag(f, "Beat 5 (f158-197) - TO GENERATE (Seedream): clean lake + villa plate, NO fish (b74514e7 has them baked in)",
        "TO GENERATE (Kling): the wave rule thickens into water, fish drop in, splash rings. Shown: b74514e7 55 % under white")
    frames.append(("05_lake_TOGEN", f))

    # 06 -- Beat 6a (08.2-10.2): the leap, tight -- centre fish breaches first
    f = fit_cover(leap, zoom=1.12)
    tag(f, "Beat 6a (f197-245) - TO GENERATE (Kling): staggered breaches C 08.6 / L 09.4 / R 10.1, ~0.9 s airborne each",
        "Shown: b74514e7 at 112 % - all three in sync here; the film must NOT be (three fish layers)")
    frames.append(("06_leap_TOGEN", f))

    # 07 -- Beat 6b (10.2-12.2): same shot, camera pulled back 12 % to open up the villa
    f = fit_cover(leap)
    tag(f, "Beat 6b (f245-293) - TO GENERATE (Kling): end of the 12 % pull-back, right fish still airborne",
        "Shown: b74514e7 full frame - this plate IS the leap keyframe, no clean villa behind it")
    frames.append(("07_pullback_TOGEN", f))

    # 08 -- Beat 7 (12.2-13.0): end card -- last fish re-enters, rings spread, rule + wordmark reversed out
    dark = ImageEnhance.Color(fit_cover(leap).filter(ImageFilter.GaussianBlur(6)).convert("RGB")).enhance(0.5).convert("RGBA")
    dark.alpha_composite(Image.new("RGBA", (W, H), (0, 10, 25, 150)))
    f = dark.copy()
    ripple_rings(f, wave_cx, wave_cy, n=5, rx0=190, ry0=28, step=1.4, alpha=170)
    for rows in (WAVE_ROWS, TYPE_ROWS):
        layer, pos = crest.band(rows, 1.0, rgb=(255, 255, 255))
        f.alpha_composite(layer, pos)
    tag(f, "Beat 7 (f293-312) - COMP (AE): the right fish's rings spread; wave rule + wordmark fade up reversed-out",
        "Rule and type sit at their exact crest positions so the return beat can hold them. Needs the clean lake plate")
    frames.append(("08_endcard_COMP", f))

    # 09 -- Beat 8 return A (13.0-14.0): lake -> white, rings contract into the rule, fish rise back, type goes black
    f = Image.blend(blank(), dark, 0.18)
    ripple_rings(f, wave_cx, wave_cy, n=4, rx0=150, ry0=22, step=1.35, alpha=140, rgb=(20, 30, 45))
    crest.paste_bands(f, (WAVE_ROWS, 0.9), (TYPE_ROWS, 0.9))
    for i, (rot, dy) in enumerate(((-6, 70), (3, 40), (-4, 95))):
        layer, pos = gold_fish_registered(gold, crest, i, scale=1.12, rot=rot)
        pos = (pos[0], pos[1] + dy)
        cast_shadow(f, layer, pos, dy=10, blur=12, alpha=35)
        f.alpha_composite(layer, pos)
    tag(f, "Beat 8 (f312-336) return A - COMP (AE): lake dissolves to white f312-330, rings contract into the wave rule",
        "Fish rise out of the rule back to crest position (reverse of beat 5), type crosses white -> black. Shown ~f326")
    frames.append(("09_return_settle_COMP", f))

    # 10 -- Beat 9 return B (14.0-14.8): gold drains top-to-bottom R->C->L to line art; wordmark fades out
    f = crest.paste_bands(blank(), (FISH_ROWS, 1.0), (WAVE_ROWS, 1.0), (TYPE_ROWS, 0.4))
    for i, keep_from in ((0, 0.0), (1, 0.55)):          # left still gold, centre half drained, right done
        layer, pos = gold_fish_registered(gold, crest, i)
        f.alpha_composite(vertical_mask(layer, keep_from, 1.0), pos)
    tag(f, "Beat 9 (f336-355) return B - COMP (AE): gold drains top-down, right first, 500 ms each, 100 ms stagger",
        "Reverse of beat 3. Wordmark 1->0 f343-355. Shown ~f346: R = line art, C half, L still gold")
    frames.append(("10_return_flatten_COMP", f))

    # 11 -- Beat 10 (14.8-15.0): loop frame -- identical to 01 before tagging
    art11 = crest.paste_bands(blank(), (FISH_ROWS, 1.0), (WAVE_ROWS, 1.0))
    assert art11.tobytes() == loop_bytes, "loop frame drifted from frame 01"
    f = art11
    tag(f, "Beat 10 (f355-360) - LOOP FRAME: fish + wave rule on white, dead still. Pixel-identical to 01 (asserted)",
        "f360 cuts to f0 with no change on screen; the 2.0 s hold of beat 1 absorbs the join")
    frames.append(("11_loop_frame", f))

    for name, im in frames:
        im.convert("RGB").save(out / f"{name}.png", optimize=True)
        im.convert("RGB").resize((960, 540), Image.LANCZOS).save(out / f"{name}_small.jpg", quality=88)

    # contact sheet: 4 columns
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
    print(f"{len(frames)} frames -> {out}  (crest scale {crest.s:.3f}, fish {fish_h}px = {fish_h / H:.0%} of frame height)")


if __name__ == "__main__":
    main()
