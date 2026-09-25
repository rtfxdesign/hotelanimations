# North Island, Seychelles — storyboard

| | |
|---|---|
| Film | 05 North Island (Theria slate, 8 films) |
| TRT | **13.0 s** = 312 frames @ **24 fps** (per `theria_hotel_animations_timing_v1.md` §5) |
| Master | 16:9, 1920×1080 (aspect is still "not decided" in the timing doc's global assumptions — see open question 2) |
| Shots | 6 in the timing doc, boarded as 8 frames (shots 4 and 6 get two frames each) |
| Loop | final frame f312 = frame 0. `build_frames.py` asserts 01 and 08 are pixel-identical below the tag band |
| Frames | `frames/NN_name.png` (1920×1080) + `NN_name_small.jpg` (960×540) + `contact_sheet.jpg`. Rebuild: `python3 north_island/storyboard/build_frames.py PULL_ROOT north_island/storyboard/frames` |
| Beat source | client brief lines (6) → timing doc §5 (source of truth for IN/OUT) → storyboard page "05 NORTH ISLAND" (differences noted below) |

**Assumptions**
- The three 1536×1024 (3:2) plates are scaled ×1.25 to cover 1920×1080 and cropped; 864 of 1024 source rows survive. On the two lock-up plates the turtles span rows 21–1004, so a centred crop clips ~60 px (source) off the top-right turtle and ~60 px off the big turtle's rear flippers. Both are tagged in-frame. The beach plate's crop is biased down (top = row 115) and loses only sky.
- `b261916d` and `7e26a98a` have the **wordmark burned in**. The board uses them as-is; the pipeline doc (§4, and test 3 in §8) recommends **regenerating both clean in Nano Banana Pro (no type)** so the wordmark becomes an After Effects layer. Every "wordmark fades" note below depends on that.
- Blend frames (02, 04, 06, 07) are plain 50 % `Image.blend` of two plates: they show *which two states* the beat moves between, not the wipe itself.
- `b261916d` and `7e26a98a` are two separate generations, not one composition re-lit: the turtles and wordmark sit 5–11 px (source) apart and the gold silhouettes differ ~9 % in area. Shot 2 and shot 6 therefore cannot be a clean dissolve between the two files as delivered — the fix is the same clean-plate regeneration: one turtle/wordmark layer set over a white plate and a water plate.
- `download.jpg` (house mark, 225×121) is **not used in any frame**. It was not enlarged; nothing was AI-enlarged. No client logo was touched.
- Nothing under the pull directory was modified.

## Beats

| # | Brief line | IN–OUT (s) / frames @24 | Frame | On screen | Motion / camera | Transition | Assets used | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | "Start with the gold turtle logo" | 0.0–2.2 / f0–53 (2.2 s) | `01_hold` | Five gold turtles + "north island / SEYCHELLES" on white, dead still | Locked off. One specular sweep across the big turtle's shell f24–48 (AE, on the plate) | — | `b261916d-7215-4f97-8607-d091aabe911a.png` | **READY** as a board frame. Final plate: NBP 4K re-render/outpaint of the same composition **without type** (has wordmark) |
| 2 | "Have the background change to water" | 2.2–4.0 / f53–96 (1.8 s) | `02_flood_COMP` | White ground becomes turquoise shallows; turtles and wordmark do not move | Turquoise floods from the bottom edge upward over 1.2 s (f53–82), caustics resolve as it rises; hold on `7e26a98a` to f96. **The two plates are not pixel-locked** (measured: gold-mask IoU 0.40, turtles and type drift 5–11 px source = 6–14 px at 1080p, big turtle 9 px vertical) — a straight wipe between them will hop. Comp the turtles + wordmark once as layers over a clean water plate | luma wipe bottom→top (AE) | `b261916d-…png` → `7e26a98a-718f-43e1-8719-c7f930b25af3.png` (shown as 50 % blend) | **COMP (AE)** — needs both plates clean (NBP) so the wordmark can sit on its own layer with refraction |
| 3 | "Have the gold turtles start to swim" | 4.0–7.0 / f96–168 (3.0 s) | `03_swim_TOGEN` | Turtles in the shallows begin to swim | Front flippers start f96, staggered 6 frames per turtle; slow drift toward frame right ~15 % of frame width over the shot; caustics move across the shells. Wordmark starts a slow fade at f150 | — | `7e26a98a-…png` as Kling start frame | **TO GENERATE — Kling** (image-to-video from the **clean** NBP plate; a burned-in wordmark will not survive Kling — cf. Giraffe Manor `frame1_to_frame2.mp4`). Wordmark fade = AE layer |
| 4a | "Have them land on a beach" | 7.0–8.2 / f168–197 (1.2 s) | `04_landfall_COMP` | Water shallows out; sand, beach and island fade up behind | Colour ramps turquoise → pale sand over 1.2 s; beach plate fades up | cross-dissolve (AE) | `7e26a98a-…png` → `0873e031-511a-499b-a9d5-8a2b7a701d87.png` (50 % blend) | **COMP (AE)** over the Kling shot-3 tail. Turtle positions do **not** match between plates (5 in water, 3 on sand) — see open question 1 |
| 4b | (same) | 8.2–9.4 / f197–226 (1.2 s) | `05_sand` | Turtles on white sand, bay and lodge behind | Flipper cycle changes from swim to a heavy crawl at f190; slow each ~30 % as it takes the sand | — | `0873e031-…png` (Kling start frame) | **TO GENERATE — Kling**. Plate: Seedream 4K re-render (clean, no type) per pipeline §3; page also asks for a beach plate **without turtles** |
| 5 | "Then back to sea" | 9.4–11.4 / f226–274 (2.0 s) | `06_return_COMP` | Turtles turn back to the water; sand ramps back to turquoise | Three turtles turn, staggered 0.5 s apart, and head out; colour ramp sand → turquoise under them | cross-dissolve (AE) | `0873e031-…png` → `7e26a98a-…png` (50 % blend) | **TO GENERATE — Kling** (turn) **+ COMP (AE)** ramp. Turtles must end in their `7e26a98a` positions |
| 6a | "back to blue, back to white" | 11.4–12.4 / f274–298 (1.0 s) | `07_whiteout_COMP` | Water desaturates to white from the top down; turtles settle into shot-1 positions; wordmark fades back up | Top-down luma wipe over 1.0 s, wordmark opacity 0 → 100 | luma wipe top→bottom (AE) | `7e26a98a-…png` → `b261916d-…png` (50 % blend) | **COMP (AE)** |
| 6b | (loop) | 12.4–13.0 / f298–312 (0.6 s) | `08_loop` | Identical to frame 0 | Hold. **Final frame = frame 0** | loop point | `b261916d-…png` | **READY** (same pixels as `01_hold`) |

## Where the storyboard page (TRT 13.0 s) differs from the timing doc

Boarded to the timing doc. The page text (`inventory/storyboards_rendered_text_2026-09-25.txt`, "05 NORTH ISLAND") differs in:

1. **Beat boundaries** — page: 0–2 / 2–4 / 4–7 / 7–10 / 10–12 / 12–13. Timing doc: 0–2.2 / 2.2–4.0 / 4.0–7.0 / 7.0–9.4 / 9.4–11.4 / 11.4–13.0. Same TRT, landfall is 0.6 s shorter and the sign-off 0.6 s longer in the doc.
2. **Beat 2 mechanics** — page: radial wipe from the four corners, 1.4 s, refraction distortion on the wordmark. Doc: bottom-up flood, 1.2 s, wordmark locked. Beat 6 mirrors this (page: "drains the way it came in"; doc: top-down).
3. **Turtle count** — page says **four**; the two lock-up plates have **five**; the beach plate has **three**; the doc's shot 5 says "the three turtles".
4. **Beat 3** — page: turtles break the logo formation into a loose line, big one leading, logo shape survives to ~0:05.5, wakes behind them. Doc: drift right ~15 %, staggered flippers, no formation change.
5. **Beat 4** — page: "camera surfaces and swings level", drag tracks in the sand. Doc: no camera move, beach fades up behind.
6. **Beat 5** — page: "mirror the plate so the exit reads opposite the entrance", a wave takes the tracks. Doc: turtles turn back on the same plate.
7. **Sound** — page: underwater pressure → surf → silence. Doc: surf/reef ambience rising through the water beats, dropping to near-silence at 12.4.

## Open questions for Allen

1. **How many turtles?** Lock-up plates: 5. Beach plate: 3. Page: 4. Doc shot 5: 3. If 5 is canon, do the two top-right turtles stay in the water on the beach beat, or does the beach plate get regenerated with all five?
2. **16:9 crop vs outpaint.** A cover crop of the 3:2 lock-up clips the top-right turtle and the big turtle's flippers (~60 px source each, tagged on 01/03/08). Outpaint both lock-up plates to 16:9 in NBP (recommended — same pass as removing the type), or shrink the lock-up and pillarbox (works on white, not on water)? And is 9:16 still on the table — it changes this film's layout completely.
3. **Which wordmark is canon?** The plates carry a textured gold serif "north island / SEYCHELLES"; the house mark in `download.jpg` is a thin black serif with concentric-circle turtles. Is the gold-rendered type approved, or must the client's vector wordmark be the AE layer (pipeline §4 says never generate a wordmark)?
4. **Beat 2/6 wipe direction** — bottom-up / top-down (doc) or radial from the corners with refraction (page)? Affects the comp and whether the wordmark needs a displacement pass.
5. **Beat 5 exit** — turn the turtles back on the same plate (doc) or mirror the plate (page)? Mirroring flips the island's geography and the lodge; check the client won't mind.

## Assets still needed

- Vector wordmark and house mark from the client (`download.jpg` is 225×121 — reference only, never to be enlarged).
- `b261916d` and `7e26a98a` regenerated **clean (no type)**, 16:9, ≥3840×2160 — Nano Banana Pro, same composition (pipeline §8 test 3 is exactly this file).
- `0873e031` re-rendered at 4K in Seedream 4.5; plus a **beach plate with no turtles** (page TO SOURCE) for the landfall comp.
- Each gold turtle as its own alpha layer (or the 3D source) — needed for the staggered swim start, the settle-back in shot 6 and any 5→3 turtle reconciliation.
- Kling clips: shot 3 swim/drift, shot 4b crawl, shot 5 turn. No North Island prompts exist in the pipeline doc yet.
- Audio bed (surf/reef) and the loop-safe fade at 12.4.

## What this board does not cover

- No wipe/caustic/refraction previs: 02, 04, 06, 07 are flat 50 % blends of two plates.
- No per-turtle motion, stagger or the 15 % drift; no shot-1 highlight sweep; no wordmark fade (impossible while it is burned in).
- No Kling prompts, seeds or fallbacks. No audio. No 1:1 / 9:16 re-frames (the logo-safe centre-80 % rule is not checked).
- No turtle-count reconciliation between the water and beach plates.
- Frames are built from the 1536×1024 originals scaled ×1.25 — they are review frames, not final plates.
