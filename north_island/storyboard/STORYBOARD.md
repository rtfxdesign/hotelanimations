# North Island, Seychelles — storyboard v2

| | |
|---|---|
| Film | 05 North Island (Theria slate, 8 films) |
| TRT | **13.0 s** = 312 frames @ **24 fps** (per `theria_hotel_animations_timing_v1.md` §5; v1 timings kept) |
| Master | **One master, 16:9, 1920×1080** |
| Shots | 6 in the timing doc, boarded as 8 frames (shots 4 and 6 get two frames each) |
| Loop | final frame f312 = frame 0. `build_frames.py` asserts 01 and 08 are pixel-identical below the tag band |
| Frames | `frames/NN_name.png` (1920×1080) + `NN_name_small.jpg` (960×540) + `contact_sheet.jpg`. Rebuild: `python3 north_island/storyboard/build_frames.py PULL_ROOT north_island/storyboard/frames` |
| Beat source | client brief lines (6) → timing doc §5 (source of truth for IN/OUT) → storyboard page "05 NORTH ISLAND" (page differences from v1 are resolved below) |

## Decisions taken

From Allen (applied):
- One master 16:9 1920×1080, 24 fps. v1 timings kept unchanged.
- Loop rule: last frame = first frame. Pixel-identical check kept in the build.
- No vector for this hotel; rasters are fine. The wordmark burned into `b261916d` and `northisland.png` is accepted as-is. It is baked in and will be **masked/held in comp** — a still patch of the plate's wordmark is held over the Kling shots and travels with the plate dissolves.

Judgement calls (made here, stated so they can be overruled):
1. **Turtle count = 5** (the lock-up plates). The beach plate `0873e031` with three turtles is used **as-is** for the landfall beat (04, 05); the two missing turtles (the top-right pair) are comped onto the sand from cut-outs of the water plate. Shot 5's "the three turtles" in the timing doc becomes five.
2. **Water wipe direction**: bottom-up flood on beat 2 (timing doc, 1.2 s), top-down drain on beat 6 (timing doc, 1.0 s). The page's radial-from-corners wipe with refraction is dropped; the wordmark stays locked, no displacement pass.
3. **`northisland.png` replaces `7e26a98a` on every water beat** (02, 03, 04, 06, 07). Diff after resizing to 1536×1024: mean abs difference 3.5/255, 1.8 % of pixels differ by more than 16, gold-mask IoU 0.89, identical gold bounding boxes — same composition, residual is edge/resampling detail. Being 2×, it scales to 1080p at 0.527 instead of 1.055, so it is sharper. `7e26a98a` is now reference only.
4. **Lock-up plates are fit by height, not cover-cropped.** v1's cover crop cut ~60 source px off the top-right turtle and the big turtle's rear flippers at the frame edge. v2 scales `b261916d` and `northisland.png` to 1620×1080, centred: nothing is clipped. On white the 150 px pillars are white and invisible. On water the pillars must be extended in comp (generative expand of the raster, 150 px each side — caustics only, no gold in the fill). On the board the pillars are a mirror-tiled gold-free strip of the plate's own edge, tagged. The beach plate is a scene, not a lock-up, so it keeps the v1 cover crop biased down (loses 115 source rows of sky, nothing else).
5. **Wordmark behaviour across the film**: held over shot 3 (masked still patch over Kling), dissolves out with the water→sand cross-dissolve at f168–197 (the beach plate has no wordmark), comes back with the sand→water dissolve at f226–274, and holds through the whiteout to the loop. The v1 "fade at f150 / fade back up" is dropped — one less thing to animate, and it needs no clean plate.
6. **Beat 5 exit**: turtles turn back on the same plate (timing doc). The page's "mirror the plate" is dropped — it flips the island and the lodge.
7. **Beat 3 motion**: timing-doc version (staggered flippers, ~15 % drift right, formation holds). The page's break-formation/wakes idea is not boarded.

Where the page and timing doc differed in v1 (beat boundaries, beat 2/6 mechanics, turtle count, beat 3/4/5 mechanics, sound), the timing doc wins throughout.

**Build assumptions**
- Blend frames (02, 04, 06, 07) are plain 50 % `Image.blend` of two plates: they show *which two states* the beat moves between, not the wipe itself.
- `b261916d` and `northisland.png` are two separate generations, not one composition re-lit: turtles and wordmark sit 5–11 px (1536-space) apart, gold-mask IoU 0.39. Shot 2 and shot 6 therefore cannot be a straight luma wipe between the two files — comp the turtles + wordmark as one cut-out layer set (from `northisland.png`, the sharper source) over a white plate and a water plate, then wipe the grounds.
- `download.jpg` (house mark, 225×121) is **not used in any frame**. Nothing was AI-enlarged. No client logo was touched.
- Nothing under the pull directory was modified.

## Beats

| # | Brief line | IN–OUT (s) / frames @24 | Frame | On screen | Motion / camera | Transition | Assets used | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | "Start with the gold turtle logo" | 0.0–2.2 / f0–53 (2.2 s) | `01_hold` | Five gold turtles + "north island / SEYCHELLES" on white, dead still. Lock-up 1620 px wide, centred, white pillars | Locked off. One specular sweep across the big turtle's shell f24–48 (AE, on the plate) | — | `b261916d-7215-4f97-8607-d091aabe911a.png` (fit-height) | **READY** as a board frame and as the final plate (wordmark baked in, accepted) |
| 2 | "Have the background change to water" | 2.2–4.0 / f53–96 (1.8 s) | `02_flood_COMP` | White ground becomes turquoise shallows; turtles and wordmark do not move | Turquoise floods from the bottom edge upward over 1.2 s (f53–82), caustics resolve as it rises; hold on the water plate to f96. Plates are not pixel-locked (5–11 px drift), so the turtles + wordmark are one cut-out layer set held over both grounds | luma wipe **bottom→top** (AE) | `b261916d-…png` → `northisland.png` (shown as 50 % blend) | **COMP (AE)** |
| 3 | "Have the gold turtles start to swim" | 4.0–7.0 / f96–168 (3.0 s) | `03_swim_TOGEN` | Turtles in the shallows begin to swim; wordmark holds | Front flippers start f96, staggered 6 frames per turtle; slow drift toward frame right ~15 % of frame width over the shot; caustics move across the shells. Wordmark = masked still patch held over the Kling output | — | `northisland.png` as Kling start frame (with the 150 px comp extension each side) | **TO GENERATE — Kling** (image-to-video). Wordmark region masked back to the plate in comp |
| 4a | "Have them land on a beach" | 7.0–8.2 / f168–197 (1.2 s) | `04_landfall_COMP` | Water shallows out; sand, beach and island fade up behind; wordmark goes with the water | Colour ramps turquoise → pale sand over 1.2 s; beach plate fades up under the Kling shot-3 tail | cross-dissolve (AE) | `northisland.png` → `0873e031-511a-499b-a9d5-8a2b7a701d87.png` (50 % blend) | **COMP (AE)**. Beach plate used as-is (3 turtles); **+2 turtles comped from `northisland.png` cut-outs** so five land |
| 4b | (same) | 8.2–9.4 / f197–226 (1.2 s) | `05_sand` | Five turtles on white sand, bay and lodge behind | Flipper cycle changes from swim to a heavy crawl at f190; slow each ~30 % as it takes the sand | — | `0873e031-…png` (Kling start frame, cover crop biased down) + 2 turtle cut-outs | **TO GENERATE — Kling** from the 5-turtle comp of the beach plate |
| 5 | "Then back to sea" | 9.4–11.4 / f226–274 (2.0 s) | `06_return_COMP` | Turtles turn back to the water; sand ramps back to turquoise; wordmark returns with the water | Five turtles turn, staggered 0.5 s apart, and head out; colour ramp sand → turquoise under them; same plate, no mirror | cross-dissolve (AE) | `0873e031-…png` → `northisland.png` (50 % blend) | **TO GENERATE — Kling** (turn) **+ COMP (AE)** ramp. Turtles must end in their lock-up positions |
| 6a | "back to blue, back to white" | 11.4–12.4 / f274–298 (1.0 s) | `07_whiteout_COMP` | Water desaturates to white from the top down; turtles settle into shot-1 positions; wordmark holds | Top-down luma wipe over 1.0 s; turtle/wordmark cut-out layer set held over both grounds | luma wipe **top→bottom** (AE) | `northisland.png` → `b261916d-…png` (50 % blend) | **COMP (AE)** |
| 6b | (loop) | 12.4–13.0 / f298–312 (0.6 s) | `08_loop` | Identical to frame 0 | Hold. **Final frame = frame 0** | loop point | `b261916d-…png` | **READY** (same pixels as `01_hold`) |

## Flagged risks

1. **Landfall turtle reconciliation (04/05).** The three beach turtles are at a different scale and lighting (low sun, long shadows) from the water plate's top-down gold. Two cut-outs pasted from `northisland.png` will need a relight/shadow pass to sit on the sand, and the two extra turtles have no beach-plate positions to inherit. Decision: comp them upper-right of the three, matching the lock-up's layout, and let the Kling shot-4b generation start from that 5-turtle comp rather than the raw plate. If Kling cannot hold five, fall back to three on the sand with the top-right pair still swimming in the shallows behind — the count stays five in frame.
2. **Water pillars (03, and the water state of 02/04/06/07).** Fit-height leaves 150 px each side of the water plate to extend. Decision: generative expand of the raster in Photoshop (caustics only; mask the gold out of the sample), done once on `northisland.png` before it goes to Kling, so shot 3 is generated at the full 16:9 frame and the extension never has to track. The board's tiled stand-in is not final.

## Assets still needed

- `northisland.png` extended to 16:9 (3413×1920 at 2×, or 1920×1080 at master) — generative expand of the water, gold masked out of the sample. Feeds shot 3 Kling and the 02/06/07 comps.
- Turtle + wordmark cut-outs from `northisland.png` (one layer per turtle, one for the wordmark) — for the shot 2/6 grounds wipe, the staggered swim start, the settle-back in shot 6 and the +2 turtles on the sand.
- Beach plate 5-turtle comp (`0873e031` + 2 cut-outs, relit) — Kling start frame for shot 4b.
- Kling clips: shot 3 swim/drift (start `northisland.png` 16:9), shot 4b crawl (start 5-turtle beach comp), shot 5 turn. No North Island prompts exist in the pipeline doc yet.
- Audio bed (surf/reef) rising through the water beats, dropping to near-silence at 12.4; loop-safe.

## What this board does not cover

- No wipe/caustic previs: 02, 04, 06, 07 are flat 50 % blends of two plates.
- No per-turtle motion, stagger or the 15 % drift; no shot-1 highlight sweep.
- The +2 turtles on the sand are noted on 04/05, not comped on the board frames.
- The water pillars on the board are a tiled stand-in, not the comp extension.
- No Kling prompts, seeds or fallbacks. No audio. No 1:1 / 9:16 re-frames (single 16:9 master).
- Frames are built from the 1536×1024 white/beach plates scaled ×1.055 / ×1.25 and the 3072×2048 water plate scaled ×0.527 — review frames, not final plates.
