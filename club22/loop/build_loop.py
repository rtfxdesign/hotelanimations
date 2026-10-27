"""22 Club spotlight -> vinyl -> back loop, v2. 1920x1080, 24 fps, 576 f (24.0 s), f575 -> f0 seamless.

usage: python build_loop.py LOGO_PNG VINYL_IMG OUT_DIR [FRAMES]
  LOGO_PNG   the 1920x1080 red-on-black mark (frame 0 is this image, pixel for pixel)
  VINYL_IMG  top-down photo of a record with a plain label on black (reference: 1536x1536,
             spindle hole at (756.3, 760.8), label r 207, record r 605 -- override with VINYL_* below)
  OUT_DIR    writes club22_loop_1080p24.mp4 (H.264), club22_loop_1080p24_prores.mov (ProRes 422 HQ),
             club22_loop_1080p24_hap.mov (HAP), contact_sheet.jpg
  FRAMES     optional, e.g. 0,100,300 -> PNG stills only, no encode
  --green    key-green ground (54,255,0) instead of black: no beam haze on the ground, dust only over
             the record, grain only on the mark/record; files get a _green suffix
Needs numpy, Pillow, ffmpeg on PATH. Deterministic (fixed seed).

The vinyl photo is split into a static light layer (masked blur of the vinyl area: the broad sheen)
and a detail layer (photo / light: grooves, dust). Detail rotates, light does not, so the sheen stays
put like a real lamp on a spinning record.

Timeline (frames):
  0-47     hold, mark on black (= source image)
  48-143   spotlight fades in from above, dust motes drift in the beam, mark warms to lit salmon
  144-239  record fades/grows in, mark shrinks onto the label and darkens to label ink
  240-431  spin: 40 f ramp up, cruise (~42 rpm), 40 f ramp down; exactly 6 revs so the mark ends upright
  432-527  record + label fade, mark back to red and full size, light fades
  528-575  hold, identical to f0
"""
import subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H, FPS, N = 1920, 1080, 24, 576
CX, CY = 960.0, 540.0
R_REC = 470.0
VINYL_CX, VINYL_CY, VINYL_R_LABEL, VINYL_R_REC = 756.3, 760.8, 207.0, 605.0
LOGO_SMALL = 0.40               # mark scale on the label (ink 520 px -> 208 px)
RED = np.array([199, 54, 46], np.float32)       # mark colour in the supplied still
LABEL_INK = np.array([92, 26, 22], np.float32)  # mark printed on the label (black in --green, per plate 4.webp)
T_HOLD, T_LIGHT, T_SHRINK, T_SPIN, T_OUT, T_END = 48, 144, 240, 432, 528, 576
SPIN_REVS, SPIN_ACC = 6, 40
GREEN = np.array([54, 255, 0], np.float32)
BRAND_RED = np.array([178, 47, 40], np.float32)  # key colour of the supplied greenscreen plates

def smooth(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)

def seg(f, a, b):
    return smooth((f - a) / (b - a))

def lerp(a, b, t):
    return a + (b - a) * t

def build_vinyl(path):
    """Returns (detail RGBA image, static light HxW float, record size px). Both centred on the record."""
    s = R_REC / VINYL_R_REC
    src = Image.open(path).convert("RGB")
    size = int(2 * R_REC) + 8
    # crop square around the hole, scale to output size
    half = (size / 2) / s
    box = (VINYL_CX - half, VINYL_CY - half, VINYL_CX + half, VINYL_CY + half)
    img = np.asarray(src.transform((size, size), Image.EXTENT, box, Image.BICUBIC), np.float32)
    c = size / 2
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    r = np.hypot(xx - c, yy - c)
    r_lab = VINYL_R_LABEL * s
    vin = ((r > r_lab + 3) & (r < R_REC - 2)).astype(np.float32)
    lum = img.mean(2)
    # masked (normalised) blur -> broad illumination of the vinyl only
    def blur(a, rad):  # 3x box blur ~ gaussian (Pillow cannot blur mode F)
        k = int(rad)
        for _ in range(3):
            for ax in (0, 1):
                p = np.pad(a, [(k + 1, k) if i == ax else (0, 0) for i in (0, 1)], mode="edge")
                cs = np.cumsum(p, axis=ax, dtype=np.float64)
                a = ((np.take(cs, range(2 * k + 1, cs.shape[ax]), axis=ax) - np.take(cs, range(0, cs.shape[ax] - 2 * k - 1), axis=ax)) / (2 * k + 1)).astype(np.float32)
        return a
    num, den = blur(lum * vin, 28), blur(vin, 28)
    light = np.where(den > 1e-3, num / np.maximum(den, 1e-3), 0) * vin
    light = np.maximum(light, 4.0)
    detail = img.copy()
    detail[vin > 0] = img[vin > 0] / light[vin > 0, None] * 14.0  # re-light at a flat 14 later scaled by light/14
    alpha = np.clip(R_REC - r + 0.5, 0, 1) * 255
    det = Image.fromarray(np.dstack([np.clip(detail, 0, 255), alpha]).astype(np.uint8), "RGBA")
    # light map as a full frame, and a mask of where it applies
    lf = np.zeros((H, W), np.float32); vm = np.zeros((H, W), np.float32)
    x0, y0 = int(CX - size / 2), int(CY - size / 2)
    lf[y0:y0 + size, x0:x0 + size] = light / 14.0
    vm[y0:y0 + size, x0:x0 + size] = vin
    return det, lf, vm, size, r_lab

def spot_maps():
    """Wide soft beam from just above frame centre (ref: 3.jpg), brightest at the top."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    sx, sy = CX, -300.0
    half = 0.50
    ang = np.arctan2(xx - sx, yy - sy)
    d = np.hypot(xx - sx, yy - sy)
    edge = np.clip((half - np.abs(ang)) / 0.16, 0, 1)
    cone = edge * edge * (3 - 2 * edge)
    cone *= np.clip((d - 260) / 120, 0, 1) * (0.35 + 0.65 * np.exp(-((yy + 40) / 520) ** 2))
    cone *= 1 - 0.25 * np.clip(np.abs(ang) / half, 0, 1) ** 2
    pool = np.exp(-(((xx - CX) / 560) ** 2 + ((yy - CY + 40) / 520) ** 2))
    return (cone * 70).astype(np.float32), cone.astype(np.float32), pool.astype(np.float32)

class Motes:
    def __init__(self, rng, n=320):
        self.x = rng.uniform(300, 1620, n); self.y = rng.uniform(-40, H + 40, n)
        self.vx = rng.normal(0, 0.18, n); self.vy = rng.uniform(-0.5, -0.1, n)
        self.ph = rng.uniform(0, 2 * np.pi, n); self.sz = rng.choice([1.0, 1.4, 2.0, 2.8], n, p=[.45, .3, .18, .07])
        self.b = rng.uniform(70, 200, n)
    def draw(self, f):
        im = Image.new("L", (W, H), 0); d = ImageDraw.Draw(im)
        x = (self.x + self.vx * f + 6 * np.sin(f / 40 + self.ph)) % W
        y = (self.y + self.vy * f + 40) % (H + 80) - 40
        for xi, yi, s, b in zip(x, y, self.sz, self.b):
            d.ellipse((xi - s, yi - s, xi + s, yi + s), fill=int(b))
        return np.asarray(im.filter(ImageFilter.GaussianBlur(0.8)), np.float32)

def main(logo_png, vinyl_img, out_dir, only=None, green=False):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    sfx = "_green" if green else ""
    rng = np.random.default_rng(22)
    src = np.asarray(Image.open(logo_png).convert("RGB")).astype(np.float32)
    assert src.shape == (H, W, 3), src.shape
    a_full = np.clip(src[..., 0] / RED[0], 0, 1)  # mark alpha from the red channel
    MARK = BRAND_RED if green else RED  # green plates (5/6.png) carry the brand red
    logo_a = Image.fromarray((a_full * 255).astype(np.uint8), "L")
    det, vlight, vmask, size, r_lab = build_vinyl(vinyl_img)
    beam, cone, pool = spot_maps()
    motes = Motes(rng)
    grain_seeds = rng.integers(0, 2**31, N)

    total = T_SPIN - T_SHRINK
    vmax = 360.0 * SPIN_REVS / (total - SPIN_ACC)
    def angle(f):
        t = f - T_SHRINK
        if t <= 0: return 0.0
        if t >= total: return 360.0 * SPIN_REVS
        if t < SPIN_ACC: return 0.5 * vmax / SPIN_ACC * t * t
        if t <= total - SPIN_ACC: return 0.5 * vmax * SPIN_ACC + vmax * (t - SPIN_ACC)
        u = total - t
        return 360.0 * SPIN_REVS - 0.5 * vmax / SPIN_ACC * u * u

    ff = None if only else subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le", str(out / f"club22_loop_1080p24{sfx}_prores.mov")],
        stdin=subprocess.PIPE)
    sheet = []
    for f in (only or range(N)):
        light = seg(f, T_HOLD, T_LIGHT) * (1 - seg(f, T_SPIN, T_OUT))
        shrink = seg(f, T_LIGHT, T_SHRINK) * (1 - seg(f, T_SPIN, T_OUT))
        rec_a = seg(f, T_LIGHT, T_SHRINK) * (1 - seg(f, T_SPIN, T_OUT - 16))
        rot = angle(f)

        frame = np.zeros((H, W, 3), np.float32)  # premultiplied over black; cov = object coverage
        cov = np.zeros((H, W, 1), np.float32)
        dust = motes.draw(f) * cone * light if light > 0 else None
        if light > 0 and not green:
            frame += beam[..., None] * light
            frame += dust[..., None]
        if rec_a > 0:
            rs = lerp(0.85, 1.0, rec_a)
            sz = int(size * rs)
            rim = det.rotate(-rot, resample=Image.BICUBIC).resize((sz, sz), Image.BICUBIC)
            layer = np.zeros((H, W, 4), np.float32)
            x0, y0 = int(CX - sz / 2), int(CY - sz / 2)
            layer[y0:y0 + sz, x0:x0 + sz] = np.asarray(rim, np.float32)
            if rs != 1.0:  # light map follows the record's scale-in
                lm = np.asarray(Image.fromarray(vlight, "F").resize((int(W * rs), int(H * rs)), Image.BILINEAR), np.float32)
                mm = np.asarray(Image.fromarray(vmask, "F").resize((int(W * rs), int(H * rs)), Image.BILINEAR), np.float32)
                L = np.zeros((H, W), np.float32); M = np.zeros((H, W), np.float32)
                ox, oy = (W - lm.shape[1]) // 2, (H - lm.shape[0]) // 2
                L[oy:oy + lm.shape[0], ox:ox + lm.shape[1]] = lm; M[oy:oy + lm.shape[0], ox:ox + lm.shape[1]] = mm
            else:
                L, M = vlight, vmask
            # vinyl: detail x static light (dimmed to 35 % without the spot); label: lit by the pool
            lamp = 0.35 + 0.65 * light
            gain = M * L * lamp + (1 - M) * (0.55 + 0.45 * light * pool)
            vinyl = layer[..., :3] * gain[..., None]
            ra = layer[..., 3:4] / 255 * rec_a
            frame = frame * (1 - ra) + vinyl * ra
            cov = cov * (1 - ra) + ra
            if green and light > 0:  # dust only where the record is
                frame += dust[..., None] * ra

        # mark: scale about centre, rotate with the record
        s = lerp(1.0, LOGO_SMALL, shrink)
        m = logo_a.rotate(-rot, resample=Image.BICUBIC, center=(CX, CY)) if rot % 360 else logo_a
        if s != 1.0:
            sw, sh = int(round(W * s)), int(round(H * s))
            m = m.resize((sw, sh), Image.LANCZOS)
            canvas = Image.new("L", (W, H), 0)
            canvas.paste(m, (int(round(CX - sw / 2)), int(round(CY - sh / 2))))
            m = canvas
        ma = np.asarray(m, np.float32)[..., None] / 255
        ink = MARK * (1 - rec_a) + (np.array([10, 9, 9], np.float32) if green else LABEL_INK) * rec_a
        lit = ink * (1 + 0.18 * light * pool[..., None]) + np.array([42, 70, 70], np.float32) * (light * (1 - rec_a)) * pool[..., None]
        frame = frame * (1 - ma) + lit * ma
        cov = cov * (1 - ma) + ma

        # grain only while the light is on, so the holds stay exactly the source image
        if light > 0:
            g = np.random.default_rng(int(grain_seeds[f])).normal(0, 2.0, (H, W, 1)).astype(np.float32)
            frame += g * light * (cov if green else 1)
        if light == 0 and rec_a == 0 and s == 1.0:
            frame = src.copy() if not green else MARK * a_full[..., None] + GREEN * (1 - a_full[..., None])
        elif green:
            frame = frame + GREEN * (1 - cov)
        out8 = np.clip(frame + 0.5, 0, 255).astype(np.uint8)
        if only:
            Image.fromarray(out8).save(out / f"still_f{f:03d}.png"); continue
        ff.stdin.write(out8.tobytes())
        if f % 48 == 0:
            sheet.append(Image.fromarray(out8).resize((480, 270)))
    if only: return
    ff.stdin.close(); ff.wait()
    assert ff.returncode == 0

    pr = str(out / f"club22_loop_1080p24{sfx}_prores.mov")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", pr, "-c:v", "libx264", "-crf", "14", "-preset", "slow",
                    "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out / f"club22_loop_1080p24{sfx}.mp4")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", pr, "-c:v", "hap", "-format", "hap",
                    str(out / f"club22_loop_1080p24{sfx}_hap.mov")], check=True)
    cs = Image.new("RGB", (480 * 4, 270 * 3))
    for i, im in enumerate(sheet):
        cs.paste(im, ((i % 4) * 480, (i // 4) * 270))
    cs.save(out / f"contact_sheet{sfx}.jpg", quality=88)

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--green"]
    main(args[0], args[1], args[2], [int(x) for x in args[3].split(",")] if len(args) > 3 else None, "--green" in sys.argv)
