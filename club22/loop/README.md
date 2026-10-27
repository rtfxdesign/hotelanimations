# 22 Club — spotlight / vinyl loop

`build_loop.py` renders a 12.0 s (288 f @ 24 fps, 1920×1080) seamless loop: the mark is lit by a spotlight, shrinks onto a vinyl label, spins exactly 3 revolutions and stops upright, then the record fades and the mark expands back to full size. f287 is pixel-identical to f0 (checked on the ProRes decode: max diff 0).

```
python build_loop.py path/to/22club_1920x1080.png OUT_DIR          # mp4 + ProRes 422 HQ + HAP + contact sheet
python build_loop.py path/to/22club_1920x1080.png OUT_DIR 0,60,160 # PNG stills only
```

Input: the 1920×1080 red-on-black mark (red 199/54/46, the colour in the supplied still, not the 178/47/40 brand red in `../storyboard`). Output media is not committed (repo holds no media). Needs numpy, Pillow, ffmpeg. Full render ≈ 3 min.

| Frames | Beat |
|---|---|
| 0–23 | hold |
| 24–71 | spotlight in |
| 72–119 | record in, mark shrinks onto label, red → black |
| 120–215 | spin (trapezoid ramp, ~42 rpm cruise, 1080° total) |
| 216–263 | record out, mark back to red and full size, light out |
| 264–287 | hold (= f0) |
