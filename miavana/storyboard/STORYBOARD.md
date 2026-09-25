# MIAVANA — storyboard v2

| | |
|---|---|
| Film | 06 Miavana, Nosy Ankao, Madagascar (client: Theria; hotel group Time+Tide) |
| TRT | 12.0 s = 288 frames @ 24 fps (timing doc `theria_hotel_animations_timing_v1.md` §6; v1 timings kept) |
| Master | One master, 16:9, 1920×1080, 24 fps; sage brand ground RGB 157/200/183 (PSD background layer) |
| Loop | Last frame = first frame. Frame 08 is built from the same composite as frame 01 and asserted pixel-identical in `build_frames.py` |
| Frames | `miavana/storyboard/frames/` — one PNG per beat + `*_small.jpg` (960×540) + `contact_sheet.jpg` (4×2); rebuilt by `build_frames.py PULL_ROOT OUT_DIR` |
| Brief | "Start with the logo with the lemurs (better positions). Have the last one holding a mango throwing it to the other lemur. The hotel appears in the background and the lemurs are in the palm trees. Hotel disappears back to the logo and lemurs in places." |

## Decisions taken

- **Seated lemur stays on the M** (PSD position). The timing doc's first-A placement is dropped: it put the tail into ISLAND SANCTUARY and would have meant re-seating the lemur against the mark. The v1 ALT frame is removed.
- **MIAVANA line = the vector wordmark**, rasterised to `assets/wordmarks/miavana_wordmark.png` (3919×604 RGBA, white). It is alpha-cropped and fitted **by width** to the PSD `miavana` layer bbox (2260×201 on the 2508 canvas → 1730×154 at HD, origin (111,327)). Letter x-positions match the PSD raster to <0.1 % of the width, so the seat on the M and the hang on the final A do not move; the vector's 0.6 % taller aspect is centred on the bbox height. ISLAND SANCTUARY and BY TIME+TIDE remain the PSD layer exports (no vector for those two lines).
- **Resort plate = `resort_16x9.png`** (4988×2806, Allen's 16:9 outpaint). Scaled to cover 1920×1080 with no crop. Used for beats 3, 4 and 5. Licensing: the plate may be used freely; no rights note carried.
- **Throw = 2D.** The Flux mango prop is animated along the drawn Bezier in After Effects over the breathing lemur stills. Kling is used **only** for two lemur poses: the hanging lemur's wind-up (one free arm) and the seated lemur's one-handed catch. No Kling throw clip at HD is needed.
- **Mango at the loop point: in hand.** Beat 6 = beat 1, mango in the hanging lemur's clasped hands, so f288 cuts to f0 with no visible change. The storyboard page's "mango is gone" gag is not used.
- Throw direction right-to-left ("the last one" = the hanging lemur on the final A), release from its clasped hands (1750,651), catch at the seated lemur's hand (207,344), apex over the V at (932,197), 130 px above cap height. Unchanged from v1.
- Timings follow the **timing doc**; the storyboard page's motion notes (12-frame anticipation hold, arc in front of the type, plate greens matched toward sage) are kept.

Screen positions (HD px) carried through every beat: seated lemur bbox (34,176)–(207,660); hanging lemur bbox (1690,322)–(1810,783). The PSD lemurs are ~480 px / ~460 px tall at HD (soft, from the 1254 px source); the palms beat uses the large cut-outs `lemur.png` and `Firefly_remove background 477817 (1).png` scaled down to the same bboxes as stand-ins for NBP output.

## Beats

| # | Brief line | IN–OUT (s) · frames | Frame | On screen | Motion / camera | Transition | Assets used | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | "Start with the logo with the lemurs (better positions)" | 00.0–02.4 · f0–58 | `01_lockup.png` | Sage lock-up: vector MIAVANA / ISLAND SANCTUARY / BY TIME+TIDE, seated lemur on the M, hanging lemur by its tail from the final A, mango already in its clasped hands | Still. Breathing on both, one tail sway on the hanging lemur, one head-turn. Mango visible from f0 so it registers before it moves | — | `assets/wordmarks/miavana_wordmark.png` (fitted to PSD bbox 145,427→2405,628), `miavana_0003_islandsanctuary.png`, `miavana_0004_bytimeandtide.png`, `miavana_0000_left_lemur.png`, `miavana_0001_right_lemur.png`, sage from `miavana_0005_Layer-0.png`; mango crop from `a ring-tailed lemur produces a mango, throws it up and to the right.mp4` @2.0 s | COMP (lock-up READY) · mango TO GENERATE — **Flux** prop |
| 2a | "the last one holding a mango" | 02.4–03.0 · f58–72 | `02_windup_TOGEN.png` | Hanging lemur weighs the mango, cocks one arm | Wind-up f58–70, 12-frame anticipation hold — the comedy is in the pause. Seated lemur only turns its head | — | as beat 1; mango offset up-right of the hands | TO GENERATE — **Kling** wind-up pose (hanging lemur with one free arm; the PSD still has both hands clasped) |
| 2b | "throwing it to the other lemur" | 03.0–03.8 · f72–92 | `03_throw_2D.png` | Mango mid-arc over the V, in front of the type; dashed arc from release (1750,651) to catch (207,344) | Release f72, 20-frame arc, apex (932,197) clearing cap height, mango tumbling ~35°; seated lemur's head tracks it | — | as beat 1 | **2D (AE)** — Flux mango on the Bezier over breathing stills; no Kling |
| 2c | (catch) | 03.8–04.2 · f92–101 | `04_catch_TOGEN.png` | Mango in the seated lemur's outstretched hand | One-handed catch, body otherwise still; soft "thup" at 04.0 | — | as beat 1 | TO GENERATE — **Kling** catch pose (seated lemur, one hand out) |
| 3 | "The hotel appears in the background" | 04.2–06.2 · f101–149 | `05_reveal_COMP.png` | Sage dissolving to the 16:9 aerial plate; wordmark holds ~1.0 s at reduced strength then fades; lemurs hold position | Cross-dissolve; the letters under the lemurs resolve into palm trunks as they go. Colour-match the plate greens toward the sage ground so the change reads as focus, not a cut | cross-dissolve | `resort_16x9.png` (cover, no crop; blurred 3 px at the mid-point), lock-up at 55 %, lemur layers, mango | COMP |
| 4 | "the lemurs are in the palm trees" | 06.2–09.6 · f149–230 | `06_palms_TOGEN.png` | Full 16:9 plate; both lemurs in real palm crowns at the same screen positions they had on the letterforms; second toss mid-arc, going **back** left-to-right | Slow aerial drift right-to-left, 6 % of frame over 3.4 s. Second toss at 07.8: seated lemur throws it back, shorter and lower (apex 90 px below the first); hanging lemur catches at 08.0 ("thup") and keeps it | — | `resort_16x9.png`, `lemur.png` (seated, scaled to the 484 px bbox), `Firefly_remove background 477817 (1).png` (hanging, scaled to the 462 px bbox), mango crop | TO GENERATE — **NBP** plate (lemurs sat in real palm crowns at these bboxes, type-free); toss **2D** as beat 2b |
| 5 | "Hotel disappears back to the logo" | 09.6–11.4 · f230–274 | `07_return_COMP.png` | Plate dissolving out, sage returning, letters re-forming under the lemurs | Reverse of beat 3; lemurs land in their beat 1 positions | cross-dissolve | `resort_16x9.png` at 30 % (blurred 6 px), lock-up at 75 %, lemur layers | COMP |
| 6 | "lemurs in places" (hold / loop) | 11.4–12.0 · f274–288 | `08_hold_LOOP.png` | Lock-up at full strength, lemurs in beat 1 positions, mango back in the hanging lemur's hands | Still; f288 cuts to f0 | — (loop) | as beat 1 — same composite, pixel-identical to `01_lockup.png` under the annotations | READY (loop verified in build); mango TO GENERATE — **Flux** |

Audio (timing doc): Malagasy forest at dawn, valiha or light marimba; two soft catches at 04.0 and 08.0. Storyboard page: "keep it dry, never cartoonish".

## Flagged risks

1. **Mango continuity across the loop.** The mango leaves the hanging lemur's hands at f72, is caught at f101, is tossed again at 07.8 in the palms, and must be back in the hanging lemur's hands at f274. Nothing in the brief returns it. Decision: the second toss in beat 4 is the seated lemur throwing it **back** (left-to-right, same arc reversed); the hanging lemur catches it at 08.0 and holds it through beats 5–6. This keeps the loop clean without an extra shot; the beat-4 arc annotation reads either direction, and the NBP brief for the palms plate does not change.
2. **Vector aspect vs. PSD bbox.** The vector wordmark is 0.6 % taller than the PSD raster at the same width. Fitted by width and centred on the bbox height, the cap line moves <1 px at HD and the letter x-positions are unchanged, so the lemur seats hold. Decision: accept; do not stretch the vector to the PSD height.

## Assets still needed

- **Mango prop (Flux)**: clean alpha, ~120 px at HD, lit to match the lemur stills; one hero frame plus a 35° tumbled frame for the arc (the board uses a colour-keyed crop from the 720×1280 Kling clip as a placeholder).
- **HD lemur poses (Kling)**: hanging lemur wind-up with one free arm (beat 2a) and seated lemur one-handed catch (beat 2c), at the PSD lemurs' scale on sage, plus breathing/tail-sway loops for the holds.
- **Palms plate (NBP)**: `resort_16x9.png` with both lemurs composited into real palm crowns at bboxes (34,176)–(207,660) and (1690,322)–(1810,783), type-free, for beat 4.
- Audio: forest bed, valiha/marimba figure, two catch foleys.

## What this board does not cover

- No motion is proven at HD: the Kling references are 720×1280. The dashed arcs are annotations, not the final AE curves.
- The "letters resolve into palm trunks" idea (beat 3) is described only; no morph frame was built. With the vector mark in hand it is now buildable, but it waits for the NBP palms plate.
- The palms frame places the big cut-outs at the letterform positions on the plate; they are not yet in the palm crowns — that is the NBP job.
- Colour-matching the plate greens to sage, the 6 % aerial drift, and the easter-egg mango on the third loop are not previewed.
- No audio, no end-card variant with a smaller mark, and no vertical (9:16) safe-area pass — one 16:9 master only.
- `build_frames.py` writes one ffmpeg frame grab and the mango cut-out into `frames/_work/`; nothing under the pull directory is touched.
