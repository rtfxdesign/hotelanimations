"""22 Club spotlight -> vinyl -> back loop. 1920x1080, 24 fps, 288 f (12.0 s), f287 -> f0 seamless.

usage: python build_loop.py LOGO_PNG OUT_DIR [FRAMES]   (FRAMES e.g. 0,60,150 -> PNG stills only)
  LOGO_PNG  the 1920x1080 red-on-black mark (frame 0 is this image, pixel for pixel)
  OUT_DIR   writes club22_loop_1080p24.mp4 (H.264), club22_loop_1080p24_prores.mov (ProRes 422 HQ),
            club22_loop_1080p24_hap.mov (HAP), contact_sheet.jpg
Needs numpy, Pillow, ffmpeg on PATH. Deterministic (fixed seed).

Timeline (frames):
  0-23    hold, mark on black (= source image)
  24-71   spotlight cone fades in from above, mark brightens in the pool
  72-119  record fades/grows in, mark shrinks onto the label and goes red -> black on a red label
  120-215 spin: ramps up, cruises (~42 rpm), ramps down, exactly 3 revs so the mark ends upright
  216-263 record + label fade, mark goes back to red and expands to full size, spotlight fades
  264-287 hold, identical to f0
"""
import subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image

W, H, FPS, N = 1920, 1080, 24, 288
CX, CY = 960.0, 540.0
R_REC, R_LABEL = 470.0, 165.0
LOGO_SMALL = 0.40  # mark scale on the label (ink 520 px -> 208 px)

def smooth(t):
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)

def seg(f, a, b):
    return smooth((f - a) / (b - a))

def lerp(a, b, t):
    return a + (b - a) * t

def build_record(rng):
    """Vinyl RGBA at 2x supersample, then downsampled. Returns float arrays (rgb, alpha) 1024x1024 at scale 1."""
    S = 2
    size = int(R_REC * 2 * S) + 8
    c = size / 2
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    r = np.hypot(xx - c, yy - c) / S
    th = np.arctan2(yy - c, xx - c)
    # grooves: fine rings with slow radial variation, plus a few track gaps
    groove = 0.5 + 0.5 * np.sin(r * 2 * np.pi / 1.6)
    band = np.zeros_like(r)
    for gap in (230, 300, 360, 420):
        band += np.exp(-((r - gap) / 2.5) ** 2)
    base = 14 + 6 * groove - 8 * band
    # angular wobble so rotation is visible on the grooves themselves
    base += 3 * np.sin(th * 3 + r * 0.05) * (r > R_LABEL + 10)
    # dust and scratches (rotate with the record)
    dust = np.zeros_like(r)
    pts = rng.integers(0, size, size=(900, 2))
    dust[pts[:, 1], pts[:, 0]] = rng.uniform(40, 120, 900)
    v = base + dust
    rgb = np.stack([v, v, v * 1.02], -1)
    # label, rim, spindle hole
    lab = r <= R_LABEL
    rgb[lab] = (199, 54, 46)
    rgb[(r > R_LABEL) & (r < R_LABEL + 6)] = (8, 8, 8)
    rim = (r > R_REC - 10) & (r <= R_REC)
    rgb[rim] = 26
    rgb[r < 6] = 0
    alpha = np.clip(R_REC - r + 0.5, 0, 1)
    img = np.dstack([np.clip(rgb, 0, 255), alpha * 255]).astype(np.uint8)
    im = Image.fromarray(img, "RGBA").resize((size // S, size // S), Image.LANCZOS)
    return im

def sheen_map():
    """Static anisotropic highlight on vinyl (does not rotate, like a real light on a spinning record)."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    th = np.arctan2(yy - CY, xx - CX)
    r = np.hypot(xx - CX, yy - CY)
    s = np.exp(-((np.angle(np.exp(1j * (th + 2.2)))) / 0.35) ** 2) + np.exp(-((np.angle(np.exp(1j * (th - 0.94)))) / 0.35) ** 2)
    s *= np.clip((r - R_LABEL) / 40, 0, 1) * np.clip((R_REC - 12 - r) / 40, 0, 1)
    return (s * 70).astype(np.float32)

def spot_maps():
    """Cone haze from a source above frame, and a pool on the mark."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    sx, sy = CX, -260.0
    half = 0.30  # half-angle in radians
    ang = np.arctan2(xx - sx, yy - sy)
    d = np.hypot(xx - sx, yy - sy)
    cone = np.clip(1 - np.abs(ang) / half, 0, 1) ** 0.9
    cone *= np.clip(d / 500, 0, 1) * np.exp(-((yy - 700) / 1100) ** 2)
    floor = np.exp(-(((xx - CX) / 620) ** 2 + ((yy - 980) / 120) ** 2))
    cone = cone + 0.8 * floor
    pool = np.exp(-(((xx - CX) / 520) ** 2 + ((yy - CY - 40) / 470) ** 2))
    return (cone * 62).astype(np.float32), pool.astype(np.float32)

def main(logo_png, out_dir, only=None):
    """only: list of frame numbers -> write PNG stills for those frames instead of encoding."""
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(22)
    src = np.asarray(Image.open(logo_png).convert("RGB")).astype(np.float32)
    assert src.shape == (H, W, 3), src.shape
    red = np.array([199, 54, 46], np.float32)
    a_full = np.clip(src[..., 0] / red[0], 0, 1)  # mark alpha from the red channel
    logo_a = Image.fromarray((a_full * 255).astype(np.uint8), "L")
    record = build_record(rng)
    sheen = sheen_map()
    cone, pool = spot_maps()
    grain_seeds = rng.integers(0, 2**31, N)

    # spin angle: trapezoid velocity over f120-215, total 1080 deg
    acc, total = 20, 96
    vmax = 1080.0 / (total - acc)
    def angle(f):
        t = f - 120
        if t <= 0: return 0.0
        if t >= total: return 1080.0
        if t < acc: return 0.5 * vmax / acc * t * t
        if t <= total - acc: return 0.5 * vmax * acc + vmax * (t - acc)
        u = total - t
        return 1080.0 - 0.5 * vmax / acc * u * u

    ff = None if only else subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le", str(out / "club22_loop_1080p24_prores.mov")],
        stdin=subprocess.PIPE)
    sheet = []
    for f in (only or range(N)):
        light = seg(f, 24, 71) * (1 - seg(f, 216, 263))
        shrink = seg(f, 72, 119) * (1 - seg(f, 216, 263))
        rec_a = seg(f, 72, 119) * (1 - seg(f, 216, 255))
        rot = angle(f)

        frame = np.zeros((H, W, 3), np.float32)
        frame += cone[..., None] * light
        if rec_a > 0:
            rs = lerp(0.82, 1.0, rec_a)
            sz = int(record.width * rs)
            rim = record.rotate(-rot, resample=Image.BICUBIC).resize((sz, sz), Image.BICUBIC)
            layer = np.zeros((H, W, 4), np.float32)
            x0, y0 = int(CX - sz / 2), int(CY - sz / 2)
            layer[y0:y0 + sz, x0:x0 + sz] = np.asarray(rim, np.float32)
            ra = layer[..., 3:4] / 255 * rec_a
            is_lab = (layer[..., :1] > 150)
            vinyl = layer[..., :3] * (1 + light * pool[..., None] * np.where(is_lab, 0.08, 0.9))
            vinyl += sheen[..., None] * (1 - is_lab) * light * (layer[..., 3:4] / 255)
            frame = frame * (1 - ra) + vinyl * ra

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
        ink = red * (1 - rec_a) + np.array([12, 6, 6], np.float32) * rec_a
        lit = ink * (1 + 0.28 * light * pool[..., None])
        frame = frame * (1 - ma) + lit * ma

        # light grain only while the light is on, so f0 and f287 stay exactly the source image
        if light > 0:
            g = np.random.default_rng(int(grain_seeds[f])).normal(0, 2.2, (H, W, 1)).astype(np.float32)
            frame += g * light
        if light == 0 and rec_a == 0 and s == 1.0:
            frame = src.copy()
        out8 = np.clip(frame + 0.5, 0, 255).astype(np.uint8)
        if only:
            Image.fromarray(out8).save(out / f"still_f{f:03d}.png"); continue
        ff.stdin.write(out8.tobytes())
        if f % 24 == 0:
            sheet.append(Image.fromarray(out8).resize((480, 270)))
    if only: return
    ff.stdin.close(); ff.wait()
    assert ff.returncode == 0

    pr = str(out / "club22_loop_1080p24_prores.mov")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", pr, "-c:v", "libx264", "-crf", "14", "-preset", "slow",
                    "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out / "club22_loop_1080p24.mp4")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", pr, "-c:v", "hap", "-format", "hap",
                    str(out / "club22_loop_1080p24_hap.mov")], check=True)
    cs = Image.new("RGB", (480 * 4, 270 * 3))
    for i, im in enumerate(sheet):
        cs.paste(im, ((i % 4) * 480, (i // 4) * 270))
    cs.save(out / "contact_sheet.jpg", quality=88)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else None)
