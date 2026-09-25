# Giraffe Manor — edit sheet

Comp 1920×1080, 24 fps, 384 frames (16.0 s). Background: cream solid RGB 255,255,240, full length. Reference: `giraffe_manor_animatic_v0.3.mp4`.

## Shots

| Shot | Frames | What happens |
|---|---|---|
| 1 hold | 0–48 | hero giraffe alone on cream |
| 2 logo | 48–86 | wordmark fades up under the hooves |
| 3 enter | 86–154 | second giraffe walks in from the right and stops beside the hero; logo eases to 35 % |
| 4 reveal | 154–178 | dissolve to the manor plate, seen large (265 %) and soft, giraffes standing in front of the terrace |
| 5 pull-back | 178–216 | rack focus f178–188, then the plate scales 265 % → 100 % over f188–216 |
| 6 turn | 216–269 | Kling clip: the giraffes walk up the centre steps and end rear-facing |
| 7 windows | 269–322 | Kling clip: necks rise, heads into the upstairs windows |
| 8 payoff | 322–351 | hold on the windows; small mark fades up bottom-right |
| 9 return | 351–373 | dissolve back to the hero alone on cream |
| 10 loop | 373–384 | hold; f383 = f0 |

## Layers, bottom to top

| # | Layer | Source (assets/) | In–out | Transform | Keyframes and notes |
|---|---|---|---|---|---|
| 1 | Cream BG | solid 255,255,240 | 0–384 | | |
| 2 | Hero on cream | `gm_hero_cutout_alpha.png` (1024×1536, opaque bbox x 49–930, y 18–1505) | 0–384 | anchor (489.5, 1505) = bottom-centre of the giraffe; position (760, 880); scale 53.8 % (800 px tall) | Still. Covered by the plate from f178 to f351; revealed again by the shot-9 dissolve. |
| 3 | Walker on cream | `giraffe_walking.mov` from Drive (3840×2160 ProRes 4444 alpha, 30 fps, 10 s) | 86–154 | scale 50 %. At 50 % the giraffe is about 775 px tall; its feet sit at y ≈ 885. Position keyframes move the giraffe's left edge from x 1940 (f86) to x 1060 (f154), ease out. Source starts at its frame 0 on f86, plays at normal speed. | Colour-match the walker to the hero (it is warmer and darker; the animatic used a per-channel levels match, gain capped 1.35). The clip stops on source frame 85 at f154. |
| 4 | Logo small | `giraffe_manor_wordmark.png` (3952×703) | 48–178 | scale 16.2 % (640 px wide); position (760, 969) | opacity f48 0 → f67 100; scale f48 15.5 % → f67 16.2 %; opacity f120 100 → f154 35 → f178 0. |
| 5 | Manor plate | `gm_manor_plate_no_giraffes.png` (2752×1536) | 154–222 | anchor (2140, 1490) in plate px; position (1497.5, 1047.7); scale f154–188 186.3 % (= 70.31 % × 2.65), f188 → f216 ease to 70.31 % | opacity f154 0 → f178 100. Gaussian blur f154–178 about 20, → 0 at f188 (rack focus). |
| 6 | Hero on plate | `gm_hero_cutout_alpha.png` | 154–222 | parent = layer 5. anchor as layer 2; position (1744, 1400) in plate px (feet); scale 28.85 % relative to parent (429 plate px tall) | opacity same as layer 5. |
| 7 | Walker on plate, frozen | `giraffe_walking.mov` frozen on source frame 85 (time remap, hold) | 154–222 | parent = layer 5. position (2050, 1400) in plate px (feet); scale so the giraffe is 429 plate px tall (about 27.7 % relative to parent) | opacity same as layer 5. |
| 8 | Shot 6 clip | `gm_2_t3.mp4` | 216–269 | full frame; stretch 52.07 % (121 source frames into 63) | opacity f216 0 → f222 100 (dissolve from the staged plate). The in-place turn at the start is not in the clip: the giraffes travel to the steps; roto or retime as needed. |
| 9 | Shot 7–9 clip | `gm_4_t1.mp4` | 269–373 | full frame; source f0 on f269, normal speed | hard cut in. opacity f351 100 → f373 0 (dissolve to the hero on cream). Optional: 25 % white lift over f351–359. |
| 10 | End card | cream solid 255,255,240, 444×115, rounded 14 px, 88 % opacity, bottom-right with 60 px margins (centre 1638, 962) | 322–373 | | opacity f322 0 → f334 100; f351 100 → f373 0. |
| 11 | End mark | `giraffe_manor_wordmark.png` | 322–373 | scale 10.1 % (400 px wide); centred on the card | same opacity as layer 10. |
| 12 | Audio | `birdsong01.wav` | 0–384 | | level −14 dB, 0.5 s fade in and out. |

Loop check: f383 must equal f0 (hero on cream, nothing else). Layers 4–11 are all out by f373.

Also in assets, not needed for the animatic version: `gm_1v_t1.mp4` (a generated walk on ivory, alternative walker, needs keying), `gm_3b_t1.png` and `gm_3c_t1.png` (the window payoff stills used as the shot-7 clip's end and start frames).
