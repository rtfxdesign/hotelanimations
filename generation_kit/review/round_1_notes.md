# Round 1 review (Sol, commit 80798a3)

Sheets in `review/r1/`.

| Output | Verdict | Notes |
|---|---|---|
| GM-2 t3, t4 (Kling 3, first+last frame) | KEEP t3, partial | The end frame works: from f58 both giraffes are on the centre steps, rear-facing, walking up, and they shrink toward the house. f0–58 is still lateral travel, not a turn in place. Source f58–120 (63 frames) is cut into animatic v0.2 as shot 6 with a 6-frame dissolve in from the staged plate. The missing turn is a roto/retime candidate, not another prompt. t4 is equivalent; t3 has the cleaner final position. |
| GM-3b t1 (GPT Image 2.5, in-place edit on the plate crop) | KEEP | The house, ivy, windows and terrace hold; the model upscaled the crop to 2688×1520. Drift: the guests moved and two figures appeared leaning out of the target windows. Giraffe coat is the darker orange again; colour-match in comp. Used as the shot 7 plate in v0.2 with a 4 % push. |
| MI-4b t1 (GPT Image 2.5, lemurs on green) | KEEP | Clean key. Cut-outs `mi_4b_seated_alpha.png`, `mi_4b_hanging_alpha.png` (with their fronds). Comped onto the 4988 px plate at the lockup positions: `mi_4_comp_5k.png`, preview `r1/mi4_comp_preview.jpg`. At those edge positions they sit on their own fronds, not the plate's palms, exactly as the board showed. If Allen prefers real palm crowns, positions move inboard and the lockup continuity trick is dropped. |
| CL-1 t2 (FLUX.2 pro) | KEEP+COMP | Isolated platter and tonearm, no lettering, no deck. Cartridge rests on the slipmat; lift the arm in comp. |
| mi_realistic_mango_storyboard_crop.png | REJECT as asset | 132×95 crop of the Kling clip with fingertips. Not the standalone mango. Allen's realistic mango generation is still not in git; MI-1a runs in round 2 unless it turns up. |

Animatic: `giraffe_manor/animatic/giraffe_manor_animatic_v0.2.mp4` uses GM-2 t3 (shot 6) and GM-3b (shots 7–9). Shot 7 is a still with a push until GM-4 exists; GM-3c (necks lowered) is the start frame for it.
