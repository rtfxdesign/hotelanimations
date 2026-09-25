# Theria hotel animations: After Effects handoff

All eight films are ready to build. Each folder has everything the comp needs, an edit sheet, and the animatic (the timed rough cut) to match.

```
giraffe_manor/   EDIT_SHEET.md  giraffe_manor_animatic_v0.3.mp4  assets/
north_island/    EDIT_SHEET.md  north_island_animatic_v0.1.mp4   assets/
passalacqua/     EDIT_SHEET.md  passalacqua_animatic_v0.1.mp4    assets/
miavana/         EDIT_SHEET.md  miavana_animatic_v0.1.mp4        assets/
necker_island/   EDIT_SHEET.md  necker_island_animatic_v0.1.mp4  assets/
fifth_avenue/    EDIT_SHEET.md  fifth_avenue_animatic_v0.1.mp4   assets/
versailles/      EDIT_SHEET.md  versailles_animatic_v0.1.mp4     assets/
club22/          EDIT_SHEET.md  club22_animatic_v0.1.mp4         assets/
```

Every comp: 1920×1080, 24 fps, square pixels. The last frame must equal the first frame, pixel for pixel; the films loop.

Every folder has a `build_<film>.jsx`, so After Effects can build the comp itself: with the folder unzipped so `assets/` sits next to the script, open After Effects, File > Scripts > Run Script File, pick the `.jsx`. It imports the assets into a folder, makes the comp, adds every layer with its timing, transform, parenting, effects and keyframes, and drops shot markers on the timeline. Anything it cannot find in `assets/` (the walk cycle, the audio bed) it asks you to locate, and Cancel skips that layer. Then check the comp against the animatic at a few frames and refine. The scripts have not been run in After Effects by us; report the first error and it gets fixed.

How to read an edit sheet: one row per layer, bottom to top. Frames are comp frames at 24 fps (f0 = first frame). "in/out" is where the layer is visible. Positions are pixels in the 1920×1080 comp unless the row says "in plate px", which means the layer is parented to the plate and positioned in the plate's own pixels. Scale is the layer's Transform scale. Keyframes are written `f48 0 → f67 100` and are eased unless marked linear.

Generated clips are 5 s Kling renders at 24 fps, 121 frames, H.264. "stretch 52 %" means the layer's Stretch value in AE (the clip plays faster). Where a sheet says "source f92 at comp f197" the clip's frame 92 lands on comp frame 197.

The animatic is the reference: it was built from the same numbers, so if a layer looks different from the animatic at the same frame, the sheet has been misread or has a mistake. Say which and it gets fixed.

Wordmarks come only from the `*_wordmark.png` files (RGBA, rendered from the client vectors). Never key a logo from a white-background image. Never scale a logo up with AI tools.

What is not in the zips: the Giraffe Manor walk cycle (`giraffe_walking.mov`, 327 MB ProRes 4444 with alpha, Drive: Giraffe Manor/upscaled), the Fifth Avenue walkers PSD (`turtlewalkers.psd`, 93 MB, Drive: 5th ave hotel NYC/upscaled; its layers are in the zip as PNGs) and the audio beds (Drive, per film). Everything else is here.

Questions go to Allen. Built by RTFX Design, 2026-09-25.
