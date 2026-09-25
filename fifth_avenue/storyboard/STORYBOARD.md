# The Fifth Avenue Hotel — storyboard v2

| | |
|---|---|
| Film | 02 · The Fifth Avenue Hotel (client folder `5th ave hotel NYC/`) |
| TRT | **13.0 s = f312** at 24 fps: the v1 12.0 s (f288) untouched, plus a 1.0 s return beat (f288–312) so the film loops. Last frame (f311) is identical to f0 |
| fps / master | 24 fps · one master, 16:9, 1920×1080 (Allen, 2026-09-25) |
| Loop rule | Last frame = first frame. The couple exit frame-left, the park whips to white, the tortoise glides back to its Beat 1 position, hold = frame 01. For a seamless player loop drop the final frame (f311) on assembly; left in, it is one duplicate frame inside a 2.4 s hold |
| Frames | `frames/NN_name.png` 1920×1080, `NN_name_small.jpg` 960×540, `contact_sheet.jpg`, plus `lockup_vector_goldtype.png` (flat gold type from the vector). Built by `build_frames.py PULL_ROOT OUT_DIR` (run 2026-09-25, 10 frames, clean; the script asserts frame 10 == frame 01) |
| Brief (source of truth for beats) | 1 start on the gold tortoise · 2 add the Fifth Ave logo in gold, no background, under its feet · 3 the logo disappears · 4 add the people walking the tortoise · 5 the people move very slowly |

## Decisions taken

1. **Hero = the plate's own tortoise** (`upscaled/turtle.png`, the `turtle` layer of `turtlewalkers.psd`, v1 frame 01b) at plate scale: 646×373 px at HD. Beats 1–6 all show the same render at the same scale, so the Beat 4 dissolve is a true match. `turtle02.png` is no longer used.
2. **The 1.33× pull-out is dropped.** No scale change anywhere in the film.
3. **Lockup low-centre, tortoise offset up-left in Beats 1–3.** At its plate position the tortoise's claws sit at y 935, leaving 145 px under its feet — the lockup cannot go there at any legible size. So in Beats 1–3 the tortoise sits at x 708–1354, claws y 600 (147 px left and 335 px above its plate position) and the lockup sits low-centre under its plastron: 460 px wide, centred x 960, y 645–967, inside the timing doc's centre-80 % logo-safe area. Through the Beat 4 dissolve the tortoise translates (+147, +335) — no scale — into the plate position (x 855–1501, claws y 935), ease in-out over f130–168, landing 5 f before the park is fully up; the leash fades up last (f165–173) once the collar is in place. The whip and return beat at the end undo that move, so the loop closes on frame 01.
4. **Gold lockup on screen = `Asset 1@2x.png`** (Allen's textured-gold render of the vector type, 2762×1933 RGBA, no disc). Its gold matches the tortoise. The flat vector type is extracted from `assets/wordmarks/fifth_avenue_wordmark.png` by the script (`lockup_vector_goldtype.png`, 2685×1876, flat gold #E0BD84 = the same gold the `.obj` material uses) and copied to `assets/wordmarks/fifth_avenue_wordmark_goldtype.png`. It is not on screen in this cut: the end/loop needs no flat mark (see 6). No placeholder marks remain.
5. **Beat 3** keeps the timing doc's out (0.7 s, +3 % scale), white stays white — the tortoise is about to slide, and a warming gradient under the type would fight the dissolve that follows.
6. **End (Beats 6–8), per Allen:** the couple exit frame-left, the park whips to white, the tortoise is alone. The exit *is* the whip: park + couple + leash are one pre-comp that push-whips out frame-left over 8 f (f274–282) with motion blur; the tortoise is a separate layer above it and does not move. Then 6 f of white with the tortoise still at its plate position, an 18 f ease in-out glide up-left to the Beat 1 position (f288–306), and a 6 f hold that is frame 01 (f306–312). The storyboards page's "gold lockup returns bottom-centre" is not used: on loop the lockup comes back 2.4 s later anyway, and a second mark inside 3 s would double-brand; the page's "park holds empty a half-beat" goes with it (see flagged risk 1). The v1 navy-roundel end card is gone.
7. **Beat 5 tortoise travel** stays at a quarter body-width (+162 px HD) — the doc's full body-width takes the head off frame right.
8. **Sound bed** is now the client's own files (`5th ave hotel NYC/audio/`), placed below. The timing doc's cello/footfall/leash-creak is superseded.

**Flagged risks (2)**

1. *"Couple exits frame left at the crawl" cannot be walked.* With a locked camera the couple stand up-stream (left) of the tortoise and everyone faces right; the man's right edge is at x ≈1085, so at the crawl (≈39 px/s) an on-foot exit takes ≈28 s, and a camera track right would take the tortoise out with them. **Decision:** the couple leave frame-left inside the push-whip (0.33 s), still mid-stride at the crawl when it takes them. If Allen wants a slower leave, the same pre-comp can push out over 24 f instead of 8 with no other change (`WHIP` in the script).
2. *The tortoise moves twice* (Beat 4 slide, Beat 7 return), against the timing doc's "not a pixel". It is translate-only, same render, same scale, so the match holds; the move exists only because the lockup has to fit under the tortoise's feet. **Decision:** keep it. The zero-move alternative is the tortoise pinned at its plate position for all 13 s with the lockup to its left (x ≈250–730, y ≈610–930, beside rather than under) — a two-constant change in the script (`HERO_LEFT/HERO_FEET_Y` = the plate position, `LOCKUP_CX/LOCKUP_TOP`), and Beats 7–8 then collapse to a single hold.

## Beats

| # | Brief line | IN–OUT (s) · frames @24 | Frame | On screen | Motion / camera | Transition | Assets used | Status · model |
|---|---|---|---|---|---|---|---|---|
| 1 | Start with image of the gold tortoise | 00.00–02.42 · f0–58 (58 f) | `01_hold.png` | Gold tortoise in profile facing camera-right, collar on, alone on white, offset up-left: x 708–1354, claws y 600. Nothing else | Dead still. Specular highlight travels across the shell L→R f10–f50; one slow head-lift at f44 | — (cold open on white; on loop it is the frame the return beat lands on) | `upscaled/turtle.png` (1463×844 RGBA = `turtle` layer of `turtlewalkers.psd`) at 646 px | READY from assets (still). Specular sweep = AE light sweep masked by the alpha. Head-lift = TO GENERATE, Kling O1 from this frame, single verb, on white so it keys back |
| 2 | Add the Fifth Ave logo in gold, no background, under its feet | 02.42–04.21 · f58–101 (43 f) | `02_lockup.png` | Textured-gold "THE FIFTH AVENUE HOTEL" lockup, no disc, low-centre under the plastron: 460 px wide, x 730–1190, y 645–967. Tortoise as Beat 1 | Letterforms wipe on L→R over 1.0 s (f58–82) behind a soft gold gradient (foil shimmer), then hold. Tortoise unchanged | — | `upscaled/turtle.png`, `upscaled/Asset 1@2x.png` (2762×1933 RGBA, Allen's textured gold render of the vector type) | COMP (AE layer over the still). No generative model near the mark |
| 3 | The logo disappears | 04.21–05.42 · f101–130 (29 f) | `03_lockup_out.png` | Same, lockup at 35 % opacity and +3 % scale (mid fade, f115) | Lockup opacity 100→0 over 0.7 s (f101–118) with 3 % scale-up as it goes. Tortoise unchanged, white stays white | — | as Beat 2 | COMP (AE) |
| 4 | Add the people walking the tortoise | 05.42–07.21 · f130–173 (43 f) | `04_reveal.png` | Mid-dissolve f152: park, couple and leash-less man at 51 % under the tortoise, which is 62 % of the way down-right into its plate position | Cross-dissolve white → park (background + woman + man) over 1.8 s. Tortoise layer translates (+147, +335) px, ease in-out, f130–168 — no scale. Leash fades up f165–173 after the collar has landed. Nothing else moves | cross-dissolve | `upscaled/turtle.png` (same sprite, same scale), `upscaled/turtlewalkers.psd` (`background` layer) + `woman.png`, `man.png`, `leash.png` at PSD origins | COMP (AE). Nothing to generate |
| 5a | Have the people moving very slowly | 07.21–11.42 · f173–274 (101 f) — start | `05_walk_start.png` | The full plate: Gilded-Age couple (parasol, top hat) walking the gold tortoise on a leash, painterly park; tortoise at x 855–1501, claws y 935 | This is the Kling **start frame**. Everything at ≈1/6 normal speed; leaves and light in the background at normal speed. Camera locked | — | `upscaled/turtlewalkers.psd` (`background`) + `woman.png` @(742,196), `man.png` @(1754,226), `leash.png` @(1798,1095), `turtle.png` @(1934,1272) | READY from assets (flattened by `build_frames.py`, identical to the PSD comp) |
| 5b | same | 07.21–11.42 · f173–274 — end | `06_walk_end_TOGEN.png` | Conform target for the end of the walk: man +15 px (foot), woman +12 px, tortoise +162 px (¼ body-width), leash stretched to follow the collar. Parasol rotation (~8°) not shown — the parasol is inside the `woman` layer | Kling O1 image-to-video, start = 05, end = 06. Generate 5 s at normal walk speed, take the best window, retime to 1/6 in the NLE with optical flow. Background leaves/light at normal speed = a second Kling pass on the `background` layer only (or AE particles), comped under the figures | — | as 5a, layers offset in x | **TO GENERATE — Kling O1** (figures) + Kling/AE (background). The end frame itself is a comp |
| 6 | (end, per Allen: couple exit frame-left, park whips to white) | 11.42–12.00 · f274–288 (14 f) | `07_whip.png` (mid-whip f278), `08_white_hold.png` (f282–288) | 07: park, couple and leash streaked out to the left with the white already across the right half; tortoise sharp and unmoved at x 855–1501. 08: white, tortoise alone at its plate position | Push-whip: the park pre-comp (background + woman + man + leash, at the Beat 5 end position) translates −1920 px in x over 8 f (f274–282), 2 f ease-in, directional motion blur; the tortoise layer above is static. Then 6 f hold on white | push-whip to white (the couple's frame-left exit) | 06 comp minus the tortoise layer; `upscaled/turtle.png` | COMP (AE). No generation. Whip audio cut on f282 |
| 7 | (return, for the loop) | 12.00–12.75 · f288–306 (18 f) | `09_return.png` (mid-return f297) | Tortoise alone on white, half-way between its plate position and the Beat 1 position | Tortoise translates (−147, −335) px, ease in-out, no scale, over 0.75 s. Nothing else on screen | — | `upscaled/turtle.png` | COMP (AE). No generation |
| 8 | (loop hold = frame 01) | 12.75–13.00 · f306–312 (6 f) | `10_loop.png` | Identical to `01_hold.png` (asserted pixel-equal by the script) | Dead still; the hold continues as Beat 1 on loop | hard loop to f0 | as Beat 1 | READY |

Frame counts: v1's f0–288 are unchanged (2.42 / 1.79 / 1.21 / 1.79 / 4.21 / 0.58 s); the return beat adds f288–312 = 1.0 s. Beat 1 is 2.4 s = 57.6 f, rounded to f58 as in the timing doc.

## Sound bed (client files, `5th ave hotel NYC/audio/`, all 44.1 kHz stereo WAV)

| Film beat | File | Duration | Placement |
|---|---|---|---|
| Beats 1–3 hold (f0–130) | `Clock 1.wav` | 7.20 s | From f0 under the hold, steady tick (≈−31 dBFS RMS throughout); fade out through the dissolve f130–173 — the file runs out at 7.2 s = f173 exactly. Alternates: `Clock 2.wav` 4.24 s, `Clock 3.wav` 3.84 s; `CLOCK_MantelClockWestminsterTick_SDLX.wav` 43.67 s (Westminster mantel clock, a longer bed if the hold ever extends) |
| Beat 2 lockup arrive (f58) | `HarpGliss_BW.25573.wav` | 3.79 s | Hit on f58 with the wipe-on; rings through Beat 3 to f149. Alternates: `Harp Gliss.wav` 7.17 s (longer tail), `14476 gliss up harp magic spell.wav` 5.13 s; `Mountain Audio - Harp Intro.wav` 10.00 s is a phrase, not a hit — only if the open needs music under the clock |
| Beats 4–6 walk (f130–282) | `Horse Drawn Carriage Pass By With People.wav` | 43.00 s | Use the file window 18.9–25.3 s (file time = film time + 13.5 s): fade in over the dissolve f130–173, so the pass-by's loudest stretch (file 22–26 s, ≈−23 dBFS) sits under f204–282 and peaks as the whip hits; hard cut on f282 with the whip. The file's first 18 s are the approach (−51 → −29 dBFS) |
| Beats 7–8 (f282–312) | — | | Silence after the whip; the clock re-enters at f0 on loop, so the audio loop seam is the clock's first tick |

Sound runs at normal speed under the 1/6-speed figures (storyboards page). Levels and the mix are not boarded.

## Assets still needed

| Asset | For | Route |
|---|---|---|
| Walk clip, figures: start = `05_walk_start.png`, end = `06_walk_end_TOGEN.png` | Beat 5 | Kling O1, start+end frame, 5 s at normal speed, retime to 1/6 in the NLE (optical flow). Budget 3–5 generations |
| Background-only motion (leaves drift, dappled light) | Beat 5 | Kling O1 on the PSD `background` layer alone, or AE particles/light. Normal speed under the slowed figures |
| Head-lift on the tortoise (f44) | Beat 1 | Kling O1 from `01_hold.png`, single verb; on white so it keys back to alpha. The same clip's first frame must match `turtle.png` — if it drifts, use the head-lift only on a soft matte over the neck |
| Specular sweep across the shell | Beat 1 | AE light sweep masked by the tortoise alpha. No generation |
| Foil-shimmer wipe-on, fade-out, dissolve, tortoise slide, leash fade, push-whip, return glide | Beats 2–4, 6–7 | AE only. Positions and frame ranges are the constants at the top of `build_frames.py` |
| Sound edit | all | The three placements above, plus levels; the loop seam is the clock |
| *Available, not used:* `upscaled/Asset 1.obj` + `.mtl` (3D extrusion of the type, 20,544 vertices, 25 groups, flat gold Kd 0.875/0.738/0.516) and `Asset 1.usdz` (448 MB, not pulled) | a dimensional lockup reveal if Beat 2 ever goes 3D | C4D/Blender or AE Advanced 3D; this board keeps the mark flat-lit as `Asset 1@2x.png` |
| *Available, not used:* `upscaled/fifthave_wordmark.ai` (vector source), `assets/wordmarks/fifth_avenue_wordmark_goldtype.png` (flat gold type, this build) | any flat use: 1:1 / 9:16 masters, a static end card if the film is ever played un-looped | Vector, no generation |

## What this board does not cover

- No motion has been generated or previewed; every frame is a still comp and the motion column is intent (v1 timings, Allen's end).
- Parasol rotation, leash slack/tension and the man's stride are not shown in `06` — the parasol and hands are inside the `woman`/`man` layers and the leash is stretched linearly. Kling owns those.
- `04` shows a plain blend and the tortoise at its eased position; the storyboards page's "brushwork resolving" treatment on the dissolve is not boarded.
- `07` simulates the push-whip with a horizontal blur in Pillow; the AE version should use real directional motion blur and a 2 f ease-in.
- Colour grade, sound levels/mix, and the storyboards page's "gold lockup returns bottom-centre" end (dropped, decision 6).
- The 1:1 and 9:16 masters the storyboards page lists. The Beat 1–3 composition (tortoise up-left, lockup low-centre) will need re-blocking for 9:16, and the plate's cover crop changes.
- `05`/`06` are the PSD flattened in Pillow (normal blend, 100 %, as the PSD is set), resampled as a whole plate; the hero in `01`–`04`/`07`–`10` is the `turtle` layer resampled alone at the same scale. In AE keep the tortoise inside the same pre-comp scale so the two are pixel-identical. If `turtlewalkers.psd` changes, re-run the script.
