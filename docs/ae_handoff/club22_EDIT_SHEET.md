# 22 Club — edit sheet

Comp 1920×1080, 24 fps, 290 frames (12.08 s) at 124 bpm (one beat = 11.6 frames). Background black. Reference: `club22_animatic_v0.1.mp4`.

The mark is the client vector rasterised at 2023×3050 (`club22_wordmark.png`), brand red RGB 178,47,40, placed so its ink is 520 px tall and centred. It is used in three parts: left 2, right 2, and the "club" script, exported as separate files at canvas scale. Two cuts come from one master: the full file with the black tail (beat-25 cut, keeps the audio), and a seamless loop trimmed at f279 (f278 = f0).

## Shots

| Beat | Frames | Beats | What happens |
|---|---|---|---|
| 1 hold | 0–46 | 1 → 5 | the mark, dead centre on black; optional 2 % bass pulse on "club" at tempo |
| 2 flip | 46–105 | 5 → 10 | both 2s rotate 90° backwards about their base line, left first, right 8 f behind; they drift outward onto the platter footprints |
| 3 decks | 105–151 | 10 → 14 | platter, vinyl, tonearm build on each flat digit over 24 f; records spin from f130 |
| 4 spotlight | 151–197 | 14 → 18 | hard cone from top-left; hits the left deck f158, sweeps right across both by f180; dust in the beam |
| 5 flip back | 197–255 | 18 → 23 | decks strip back to bare ellipses f197–216; both digits rise together f216–235; spot lifts to nothing by f255 |
| 6 return | 255–279 | 23 → 25 | the mark, dead still; hard cut to black on beat 25 (f279) |
| tail | 279–290 | | black |

## Layers, bottom to top

| # | Layer | Source (assets/) | In–out | Transform | Keyframes and notes |
|---|---|---|---|---|---|
| 1 | Black BG | solid black | 0–290 | | |
| 2 | Spotlight | AE cone: apex (−80, −160), hard-edged, warm white RGB 255,240,210; noise-driven dust; `cl_3_t1.png` is the lighting reference | 151–255 | pool ellipse from (left deck only) at f158 to (both decks) at f180: centre x 775 → 960, width 560 → 930, height 270 | strength f151 0 → f158 100; f197 45 → f255 0, narrowing and lifting. Decks 55 % outside the pool, full inside; "club" 65 % in the spill. |
| 3 | Deck L, Deck R | `cl_1_t2.png` (platter + tonearm on black), `cl_2_t1.png` (vinyl top-down on black), keyed from black or masked | 105–216 | platter 320 px wide, seen from 30° above (ellipse 320×160); near edge on the hinge line y 642; centres x 775 (L) and 1145 (R) | build on: opacity f105 0 → f129 100. Vinyl spins 33⅓ rpm = 43 f per rev from f130, one flash per rev. Strip back: f197 100 → f216 0. Tonearm pivots behind the far rim (decks sit 50 px apart). |
| 4 | Digit 2 L | `cl_mark_2L.png` (149×362) | 0–129 and 197–290 | home top-left (808, 280); 3D layer; anchor on its lowest ink row (hinge, y 642); camera 30° elevation | flip: X rotation 0 → 90° over f46–65 (0.8 s) with a small overshoot and settle, drift x −107 px eased with it; hides under the deck f105–129 (opacity 100 → 0). Back: opacity 0 → 100 f197–216 flat, then rotation 90° → 0 and drift → 0 over f216–235 with the same overshoot. |
| 5 | Digit 2 R | `cl_mark_2R.png` (149×362) | as 4 | home top-left (960, 280); same hinge | as layer 4 but flip starts f54 (8 f behind) and drift +110 px; rises together with L on f216–235. Put L on a lower z-order for beats 2–5 and rotate about an axis 2 px behind the face so the two do not z-fight as the left passes the still-upright right. |
| 6 | "club" script | `cl_mark_club.png` (335×143) | 0–290 | top-left (793, 657) | never moves. Becomes the mixer fascia between and under the decks; half-lit in the spill f151–255. |
| 7 | Whole mark (alternative to 4–6 for beats 1 and 6) | `cl_mark_whole.png` (335×520) | 0–46 and 255–279 | top-left (793, 280) | pixel-identical composite of 4–6 at home; use either. |
| 8 | Audio | `club22_rhythm_124bpm.wav` (Sol's placeholder bed, 12.08 s) | 0–290 | | −6 dB in the animatic. Track cues: filter opens on the spotlight (f151), the drop lands on f197, cut on beat 25 (f279). Replace with the real track. |

Loop check: f278 = f0 for the seamless-loop cut. The full cut ends on black.

Also in assets: `club22_wordmark.png` (the vector raster), `cl_3_t1.png` (spotlight reference still).
