# 22 Club — spotlight / vinyl loop

`build_loop.py` renders a 24.0 s (576 f @ 24 fps, 1920×1080) seamless loop: the mark is lit by a wide spotlight with drifting dust, shrinks onto the label of a photographed record, spins exactly 6 revolutions and stops upright, then the record fades and the mark expands back to full size. f575 is pixel-identical to f0 (checked on the ProRes decode: max diff 0).

```
python build_loop.py 22club_1920x1080.png vinyl_topdown.webp OUT_DIR          # mp4 + ProRes 422 HQ + HAP + contact sheet
python build_loop.py 22club_1920x1080.png vinyl_topdown.webp OUT_DIR 0,60,160 # PNG stills only
```

Input: the 1920×1080 red-on-black mark (red 199/54/46, the colour in the supplied still, not the 178/47/40 brand red in `../storyboard`). Output media is not committed (repo holds no media). Needs numpy, Pillow, ffmpeg. Full render ≈ 7 min. Vinyl photo geometry (hole centre, label/record radii) is set in `VINYL_*` at the top of the script; the photo's broad sheen is held static while grooves and dust rotate.

| Frames | Beat |
|---|---|
| 0–47 | hold |
| 48–143 | spotlight + dust in |
| 144–239 | record in, mark shrinks onto label |
| 240–431 | spin (40 f ramps, ~42 rpm cruise, 2160° total) |
| 432–527 | record out, mark back to red and full size, light out |
| 528–575 | hold (= f0) |

## Greenscreen (`--green`)

`python build_loop.py 22club_1920x1080.png vinyl_topdown.webp OUT_DIR --green` writes the same files with a `_green` suffix. Ground is flat key green 54/255/0 (sampled from the supplied plates). The spotlight lights only the mark and the record: no beam haze on the ground, dust motes only over the record, grain only on the objects. The mark uses the brand red 178/47/40 (as on the green plates) and is black on the label. f575 = f0 (max diff 0 on the ProRes decode); background pixels decode as 53/254/0.
