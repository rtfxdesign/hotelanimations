# Round 0 review (Sol's existing outputs, commit 97ca55c)

Contact sheets in `review/r0/`. Verdicts: KEEP = use as is, KEEP+COMP = use with cleanup in comp, RERUN = new request in round 1, REJECT = do not use.

| Output | Verdict | Notes |
|---|---|---|
| GM-2 t1, t2 (Kling 3) | RERUN | Giraffes walk sideways along the lower terrace, overlap, never turn or recede. Round 1 adds `gm_2_rear_end.png` as the last frame so the model has a target. |
| gm_2_rear_end (GPT Image) | KEEP | Two giraffes from behind on the centre steps, plate otherwise held. Becomes GM-2's end frame. |
| GM-3 t1 (GPT Image) | KEEP+COMP as fallback, RERUN as GM-3b | Composition and giraffe pose are right, but the house is rebuilt: window grid, terrace and ivy differ from the plate, so a continuous shot 6 to 7 would morph the building. GM-3b edits the real plate crop in place; if that fails, isolated giraffes on green and I comp. Coat is darker orange than the hero; colour-match in comp. |
| FA-1 t1, t2 (Kling 3) | KEEP, pick t1 | Both hold the painterly look and the composition. t1: cleaner tortoise front legs, parasol and leash consistent through f120. t2: man's cane and hand drift at f80–120. Retime figures to 1/6 with roto in AE; background at 100 %. |
| PA-1 t1 (GPT Image) | KEEP | Villa, promontory and light preserved, fish removed cleanly. 1672×941: I will Lanczos to 1920 for the animatic; ask for a 2K regen only if the pull-back shows softness. |
| VE-1 t1 (GPT Image) | KEEP | Faithful panelling and window light, clear centre floor. Same resolution note. |
| MI-4 t1 (GPT Image) | KEEP for animatic, MI-4b for final | Lemurs sit at the right palms and poses (seated left, hanging right) and read at frame scale. Plate is a 1672 px regeneration with warmer colour; for the final I comp isolated lemurs (MI-4b) onto the 4988 px source. |
| CL-1 t1 (FLUX) | REJECT | Whole branded deck with lettering. Rerun with a stricter prompt. |
| CL-2 t1 (FLUX) | KEEP+COMP | Usable vinyl; fix the oval with a 3 % horizontal scale, desaturate the label toward the brand red, flatten the textured black. |
| mango_prop.png | REJECT | 128 px flat cartoon, not a generation. Allen has a realistic mango generation to commit. |
| Sol's preview cuts | reference only | giraffe_manor_v0.2, fifth_avenue_v0.1, passalacqua_v0.1, miavana_v0.1, club22 loops are useful drafts of the edit structure. Not masters; the cloud animatic builder stays the master. |

Provisional picks written to `picks.json` (FA-1=1, PA-1=1, VE-1=1, MI-4=1, CL-2=1) pending Allen.

Policy from Allen, 2026-09-25: Sol may use whichever model serves the shot; rotoscoping in After Effects is acceptable, so prefer clean separable elements over perfect in-plate integration.

## Addendum (Allen, 12:35 UTC)

`passalacqua_v0.1.mp4` f311: wordmark over the lake is a luma-keyed white-background raster; letter counters (O, D, A, Q) are filled white. See `r0/pa_f311_logo_zoom.png`. Fix: use `assets/wordmarks/passalacqua_wordmark.png` (RGBA from the vector). Rule restated to Sol on PR #3. Applies to all films.
