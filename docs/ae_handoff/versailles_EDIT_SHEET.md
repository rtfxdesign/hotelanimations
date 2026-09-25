# Airelles Le Grand Contrôle, Versailles — edit sheet

Comp 1920×1080, 24 fps, 374 frames (15.6 s). Background black. Reference: `versailles_animatic_v0.1.mp4`.

This film is a layer build: one clean salon plate, and the cake, chandelier, guillotine and plated slices as separate keyed layers over it. Every beat is a matte, an opacity, a grade or a layer move. The keyed elements in `assets/` were cut from Sol's generated stills on their off-white fields; re-key from the originals (also included) if the edges need work. The wordmark is the approved raster (`images copy.jpg`, 2× Lanczos, luma-keyed to gold-cream).

## Shots

| Shot | Frames | What happens |
|---|---|---|
| 1 open | 0–53 | cake on its gilt table, chandelier above, everything else black (loop frame); candle flicker, slow crystal caustics, 1 % push-in |
| 2 reveal | 53–106 | the salon reveals radially from the cake, floor then walls then the window light, over about 1.4 s |
| 3 wordmark | 106–149 | AIRELLES lockup fades up on the parquet under the table, holds |
| 4 morph | 149–211 | chandelier morphs into the guillotine; room drops 1.5 stops |
| 5 still | 211–235 | wordmark out; 12 frames of nothing |
| 6 drop | 235–254 | pre-shake, blade down in 8 f, 3-frame flash, 4 px kick settling |
| 7 served | 254–326 | cake falls into slices, portions slide out to plates round the table; light up 1 stop |
| 8 return | 326–374 | salon closes to black from the edges; slices retrace to the cake; guillotine dissolves back to the chandelier; hold = frame 0 |

## Layers, bottom to top

| # | Layer | Source (assets/) | In–out | Transform | Keyframes and notes |
|---|---|---|---|---|---|
| 1 | Black BG | solid black | 0–374 | | |
| 2 | Clean salon | `ve_1_t1.png` (1672×941, generated) | 53–350 | scale 114.8 % (fits 1920×1080); centred | radial luma matte centred (960, 620): radius f53 200 px → f86 1700 px (fully open), soft edge about 45 % of the radius; reverse f326 1700 → f350 0. Grade: f149 0 → f211 −1.5 stops; f254 −1.5 → f270 −0.5; f350 −0.5 → f370 0. |
| 3 | Wordmark | `ve_wordmark_gold_alpha.png` (640×187, gold-cream RGB 232,208,150) | 106–223 | 240 px wide; centred at x 960, top y 962 (on the parquet between the table's front feet) | opacity f106 0 → f123 100; f211 100 → f223 0. Screen-flat fade, no tracking. |
| 4 | Guillotine, blade up | `ve_guillotine_up_alpha.png` (776×1040) | 149–370 | bottom-centre at (960, 1050) | opacity f149 0 → f200 100 (the morph target; in the final the chandelier's crystals become the uprights f149–180, the boss becomes the blade f170–200, the rope and pulley draw on f195–211). Out: f350 100 → f370 0. Same grade as layer 2. |
| 5 | Guillotine, blade down | `ve_guillotine_down_alpha.png` (776×1040) | 238–362 | as layer 4 | stands in for the impact state: opacity f238 0 → f246 100, f338 100 → f362 0. In the final the blade is its own layer cut from this still and moved down over f238–246. |
| 6 | Cake on table | `ve_cake_table_alpha.png` (463×620) | 0–374 | bottom-centre at (960, 1042) | opacity f254 100 → f268 0 (falls into slices); f338 0 → f362 100 (heals). Grade with layer 2. Candle and caustic micro-motion as masked layers on the still so f0 stays exact. |
| 7 | Plated slices | `ve_plated_alpha.png` (700×700) | 254–362 | bottom-centre at (960, 1072) | opacity f254 0 → f268 100; f338 100 → f362 0. In the final the slices are separate cut-outs sliding out to their plate positions over 0.6 s and back at 2× speed on the return. |
| 8 | Chandelier | `ve_chandelier_alpha.png` (224×300) | 0–200 and 350–374 | top-centre at (960, 8) | opacity f149 100 → f200 0; f350 0 → f370 100. May sway 1.5° on a slow sine. Grade with layer 2. |
| 9 | Flash | white solid | 246–249 | | opacity 35 % for 3 frames at the impact. Whole comp kicked (+4, −3) px at f246 settling to 0 by f254; 1 px jitter f235–238. |

Loop check: f373 = f0 (layers 6 and 8 at full, everything else out, grade 0).

Sound: the quartet stops dead at 09.8 s (f235) and is back at 11.2 s (f269) as if nothing happened; silence across the loop join. No music file in the assets.

Also in assets: the originals `ve_2a_t1.png`, `ve_2b_t1.png`, `ve_3a_t1.png`, `ve_3b_t1.png`, `ve_4_t1.png` (1744×2336 and 2048², on white), `cfb72e66_cake_chandelier_cutout_alpha.png` (the client's own cake + chandelier cut-out, 1024×1536, the look reference for layers 6 and 8), and `images copy.jpg` (the wordmark raster).
