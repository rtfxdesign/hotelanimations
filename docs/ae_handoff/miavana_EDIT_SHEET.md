# Miavana — edit sheet

Comp 1920×1080, 24 fps, 288 frames (12.0 s). Background: sage solid RGB 157,200,183. Reference: `miavana_animatic_v0.1.mp4`.

The lock-up is the vector MIAVANA wordmark plus the PSD layers (two text lines, two lemurs), placed from the PSD layer boxes. PSD canvas 2508×1411 maps to HD at 76.56 %. All positions below are top-left corners in the comp for layers at that 76.56 %.

## Shots

| Beat | Frames | What happens |
|---|---|---|
| 1 hold | 0–58 | lock-up, mango in the hanging lemur's hands (loop frame) |
| 2a wind-up | 58–72 | hanging lemur frees an arm and draws back |
| 2b throw | 72–92 | mango arcs right to left over the V, in front of the type |
| 2c catch | 92–101 | seated lemur catches one-handed |
| 3 reveal | 101–149 | sage dissolves to the aerial; wordmark holds about 1 s then fades |
| 4 palms | 149–230 | lemurs in the palms at the same screen positions; slow drift right to left; second toss thrown back |
| 5 return | 230–274 | aerial dissolves out, lock-up re-forms |
| 6 hold | 274–288 | = frame 0 |

## Layers, bottom to top

| # | Layer | Source (assets/) | In–out | Transform | Keyframes and notes |
|---|---|---|---|---|---|
| 1 | Sage BG | solid 157,200,183 | 0–288 | | |
| 2 | Aerial with lemurs | `mi_palms_lemurs_comp_4988x2806.png` (MI-4b lemurs keyed and comped on the resort plate at the lock-up positions) | 101–274 | scale 40.8 % (= 2035 px wide) so a 6 % drift fits; position slides from x centre +58 (f149) to −58 (f230), ease; y centred | opacity f101 0 → f149 100 (linear), f230 100 → f274 0. Under the dissolves the letters resolve into the palm trunks. Colour-match the greens toward the sage so the change reads as focus, not a cut. |
| 3 | Wordmark MIAVANA | `miavana_wordmark.png` (3919×604, white) | 0–125 and 230–288 | alpha-cropped and fitted 1730 px wide; top-left (111, 326) | opacity 100 → 0 over f101–125 (holds while the plate comes up); f230 0 → f274 100. |
| 4 | ISLAND SANCTUARY | `miavana_0003_islandsanctuary.png` (1684×101) | as layer 3 | scale 76.56 %; top-left (336, 639) | same opacity as layer 3. |
| 5 | BY TIME+TIDE | `miavana_0004_bytimeandtide.png` (588×58) | as layer 3 | scale 76.56 %; top-left (756, 972) | same opacity as layer 3. |
| 6 | Seated lemur | `miavana_0000_left_lemur.png` (226×632) | 0–149 and 230–288 | scale 76.56 %; top-left (34, 176) | still except a head-turn; hand reaches at the catch (f92–101). Replaced in beat 2 by the Kling clip below if that is preferred. |
| 7 | Hanging lemur | `miavana_0001_right_lemur.png` (156×603) | as layer 6 | scale 76.56 %; top-left (1690, 322) | breathing; one tail sway; arm frees f58–70 for the throw (2-key puppet or the Kling clip). |
| 8 | Mango | `mi_mango_cutout_alpha.png` (from the MI-1a still) | 0–101 and 230–288 | 84 px wide | in the hanging lemur's hands: centre (1756, 645). Throw f72–92 on a quadratic arc: release (1750, 651), apex over the V (932, 197), catch (207, 344); tumbling about 35°, in front of the type. Held by the seated lemur f92–101 at (217, 340). Return: the second toss in beat 4 goes back, apex 90 px lower, so the mango is home by f230. |
| 9 | Kling wind-up (optional) | `mi_2_t1.mp4` | 58–72 | full frame | the clip is the lock-up with the hanging lemur freeing an arm and raising a mango by its f98; the animatic retimes it 8.6× into the beat. Use it as reference or as the layer, with the lock-up layers off. |
| 10 | Kling catch (optional) | `mi_3_t1.mp4` | 72–101 | full frame, source f44 on f72, stretch 45 % | the clip's own mango flies in from the right and is caught at its f109. The animatic uses it; the final uses the 2D arc above. |

Loop check: f287 = f0.

Also in assets: `mi_seated_lemur_keyed_alpha.png`, `mi_hanging_lemur_keyed_alpha.png` (the MI-4b lemurs on alpha, with fronds), `resort_16x9.png` (the clean 4988 px aerial), `mi_1a_t1.png`, `mi_1b_t1.png` (mango in a lemur hand), `mi_1c_t1.png` (mango tumbling with motion blur).
