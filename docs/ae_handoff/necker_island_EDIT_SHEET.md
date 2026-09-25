# Necker Island — edit sheet

Comp 1920×1080, 24 fps, 372 frames (15.5 s). Background white. Reference: `necker_island_animatic_v0.1.mp4`.

No wordmark layer: the brief's mark is Virgin's script, small, lower right, on the whiteout only (f318–336). It is not in the assets; use the client's file.

## Shots

| Shot | Frames | What happens |
|---|---|---|
| 1 hold | 0–58 | the cut-out flamingo (bow tie) alone on white |
| 2 takeoff | 58–110 | crouch, three wingbeats, exits top right |
| 3 pull-back | 110–178 | the aerial resolves from white as the camera pulls back 2.2× → 1×; flamingo small, flying right |
| 4 kite | 178–245 | beach level: rider crosses left to right in the lower third, flamingo crosses right to left in the upper third |
| 5 tennis | 245–312 | two lemurs rally on the real court; push in 1× → 1.15×; hits at 10.8, 11.6, 12.4 s |
| 6 whiteout | 312–336 | aerial shrinks 1× → 0.55× under a white ramp; mark lower right |
| 7 landing | 336–372 | flamingo glides in from upper left, lands, settles into the opening pose |
| loop | 371 = 0 | |

## Layers, bottom to top

| # | Layer | Source (assets/) | In–out | Transform | Keyframes and notes |
|---|---|---|---|---|---|
| 1 | White BG | solid white | 0–372 | | |
| 2 | Flamingo still | `flamingo.png` (915×1666 RGBA) | 0–62 and 366–372 | 777 px tall (72 % of frame); anchor bottom-centre; feet at y 940; centre x 920 | still; head preen f20–38 optional. `ne_shot1_START_flamingo_on_white.png` is this placement rendered flat. |
| 3 | Takeoff clip | `ne_1_t1.mp4` | 58–110 | full frame; stretch 43 % (121 into 52) | opacity f58 0 → f62 100 over the still. The clip's background drifts light grey: key it or lift to white. |
| 4 | Aerial, pull-back | `ne_aerial_16x9_3840x2160.png` | 110–178 | scale f110 110 % (= 2.2× of fit) → f178 50 % (fit), ease; centred | white ramp above it: white solid opacity f110 85 → f140 0. |
| 5 | Flamingo small | `flamingo.png` | 110–178 | 86 px tall (8 %); position (1290, 375) → (1600, 295) | stand-in for a flying bird; the final wants a flight-pose crop (`necker_flamingos_08.jpg` in Drive, single clean bird top-left) or a Kling flier. |
| 6 | Kite clip | `ne_3_t1.mp4` | 178–245 | full frame; stretch 55 % (121 into 67) | hard cut in. The clip's flamingo grows toward camera late; if that reads, cut the bird out and drive it as a separate layer. |
| 7 | Tennis A | `ne_4a_t1.png` | 245–312 | scale f245 100 % → f312 115 %, ease; centred | shows f245–259, f278–298. |
| 8 | Tennis B | `ne_4b_t1.png` | 245–312 | same push-in | shows f259–278, f298–312; 4-frame dissolves at each hit. Ball is an AE shape on 14-frame arcs between the rackets with a hit mark at 10.8, 11.6, 12.4 s. |
| 9 | Aerial, whiteout | `ne_aerial_16x9_3840x2160.png` | 312–336 | scale f312 50 % → f336 27.5 %, ease; centred | white solid above: opacity f312 0 → f336 100. Flamingo small banking back: (1600, 295) → (1440, 375). Virgin mark lower right on f318, off with the white. |
| 10 | Landing clip | `ne_5_t1.mp4` | 336–372 | full frame; source f20 on f336, stretch 45 % | opacity f366 100 → f371 0 over the still. The clip ends in the S1 pose on white. |

Loop check: f371 = f0.

Also in assets: `ne_2_t1.png` (kite plate with the generic rider, the kite clip's first frame), `ne_ref_flamingo_cutout_alpha.png` (the cut-out, alpha-cropped).
