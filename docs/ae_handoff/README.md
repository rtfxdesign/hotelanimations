# Theria hotel animations: After Effects handoff

Six films are ready to build. Each folder has everything the comp needs, an edit sheet, and the animatic (the timed rough cut) to match.

```
giraffe_manor/   EDIT_SHEET.md  giraffe_manor_animatic_v0.3.mp4  assets/
north_island/    EDIT_SHEET.md  north_island_animatic_v0.1.mp4   assets/
passalacqua/     EDIT_SHEET.md  passalacqua_animatic_v0.1.mp4    assets/
miavana/         EDIT_SHEET.md  miavana_animatic_v0.1.mp4        assets/
necker_island/   EDIT_SHEET.md  necker_island_animatic_v0.1.mp4  assets/
fifth_avenue/    EDIT_SHEET.md  fifth_avenue_animatic_v0.1.mp4   assets/
```

Every comp: 1920×1080, 24 fps, square pixels. The last frame must equal the first frame, pixel for pixel; the films loop.

How to read an edit sheet: one row per layer, bottom to top. Frames are comp frames at 24 fps (f0 = first frame). "in/out" is where the layer is visible. Positions are pixels in the 1920×1080 comp unless the row says "in plate px", which means the layer is parented to the plate and positioned in the plate's own pixels. Scale is the layer's Transform scale. Keyframes are written `f48 0 → f67 100` and are eased unless marked linear.

Generated clips are 5 s Kling renders at 24 fps, 121 frames, H.264. "stretch 52 %" means the layer's Stretch value in AE (the clip plays faster). Where a sheet says "source f92 at comp f197" the clip's frame 92 lands on comp frame 197.

The animatic is the reference: it was built from the same numbers, so if a layer looks different from the animatic at the same frame, the sheet has been misread or has a mistake. Say which and it gets fixed.

Wordmarks come only from the `*_wordmark.png` files (RGBA, rendered from the client vectors). Never key a logo from a white-background image. Never scale a logo up with AI tools.

What is not in the folders: the Giraffe Manor walk cycle (`giraffe_walking.mov`, 327 MB ProRes 4444 with alpha) lives in the Drive folder Giraffe Manor/upscaled. Everything else is here.

Questions go to Allen. Built by RTFX Design, 2026-09-25.
