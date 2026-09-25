# The Fifth Avenue Hotel — edit sheet

Comp 1920×1080, 24 fps, 312 frames (13.0 s). Background white. Reference: `fifth_avenue_animatic_v0.1.mp4`.

The park is `turtlewalkers.psd` (4346×2444) with four layers: woman, man, leash, turtle. PSD pixels map to HD at 44.19 % (height fits; 1 px cropped on the right). The plate tortoise is the hero throughout: it is the same sprite at the same scale on white in beats 1–3 and on the park in beats 4–7. All positions are top-left corners of layers at 44.19 %.

## Shots

| Beat | Frames | What happens |
|---|---|---|
| 1 hold | 0–58 | gold tortoise alone on white, up-left (loop frame); specular sweep across the shell f10–50 |
| 2 lockup | 58–101 | gold lockup wipes on left to right under the plastron, holds |
| 3 lockup out | 101–130 | lockup fades with a 3 % scale-up |
| 4 reveal | 130–173 | white dissolves to the park; the tortoise slides down-right into its plate position; leash fades up last |
| 5 walk | 173–274 | the couple walk the tortoise, very slowly |
| 6 whip | 274–282 | park and couple push out frame-left; tortoise stays |
| 6b white | 282–288 | tortoise alone at its plate position |
| 7 return | 288–306 | tortoise glides back up-left |
| 8 loop | 306–312 | = frame 0 |

## Layers, bottom to top

| # | Layer | Source (assets/) | In–out | Transform | Keyframes and notes |
|---|---|---|---|---|---|
| 1 | White BG | solid white | 0–312 | | |
| 2 | Park background | `turtlewalkers.psd` layer `background` (or `fa_park_couple_no_tortoise.png`, the background + woman + man flattened at HD) | 130–282 | scale 44.19 %; top-left (0, 0) | opacity f130 0 → f173 100. Whip: position x 0 → −1920 over f274–282, 2-frame ease in, directional motion blur. Pre-comp layers 2–5 for the whip. |
| 3 | Woman | `woman.png` (1131×1804) | 130–282 | scale 44.19 %; top-left (328, 87) | same opacity as 2; walk: +12 px in x over the walk (f173–274); whip with the pre-comp. |
| 4 | Man | `man.png` (666×1579) | 130–282 | scale 44.19 %; top-left (775, 100) | as 3; walk +15 px. |
| 5 | Leash | `leash.png` (582×336) | 165–282 | scale 44.19 %; top-left (795, 484) | opacity f165 0 → f173 100. Walk: stretch the right end to follow the collar. Whip with the pre-comp. |
| 6 | Kling walk (optional, replaces 2–5 for the walk beat) | `fa_1_t1.mp4` | 173–274 | full frame | the clip is the whole plate walking at normal speed. Retime the figures to 1/6 with optical flow and keep the background at normal speed (or a second pass on the background alone). The animatic holds source f0–25 over the beat, 4× slow, frame-held. |
| 7 | Tortoise | `turtle.png` (1463×844) | 0–312 | scale 44.19 % (646×373 at HD); beat 1: top-left (708, 227), claws on y 600 | position (708, 227) → (855, 562) over f130–168, ease in-out, no scale; walk: +162 px in x over f173–274 (a quarter body-width); f288–306 back to (708, 227), ease in-out. Specular sweep f10–50 as a masked light layer. |
| 8 | Lockup | `Asset 1@2x.png` (2762×1933, textured gold render of the vector type; alpha-crop to 2761×1933) | 58–118 | scale 16.66 % (460 px wide, 322 tall); centred at x 960, top y 645 | wipe on left → right f58–82 (60 px soft edge) behind a gold foil shimmer; opacity f101 100 → f118 0 with scale 16.66 → 17.16 %. |

Loop check: f311 = f0 (tortoise at (708, 227) on white, nothing else).

Audio: nothing chosen. The Drive folder `5th ave hotel NYC/audio` has clock ticks, harp glisses and a horse-drawn carriage pass, none placed in the animatic.

Also in assets: `fa_tortoise_hd_alpha.png` (the tortoise sprite at HD scale), `fa_park_couple_leash.png` (background + woman + man + leash at HD), `fa_shot5_START_walk.png` and `fa_shot5_END_target_layers_offset.png` (the Kling start frame and the walk end target), `fifth_avenue_wordmark.png` (vector lockup rasterised) and `fifth_avenue_wordmark_goldtype.png` (flat gold type extracted from it).
