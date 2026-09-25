# Passalacqua — edit sheet

Comp 1920×1080, 24 fps, 360 frames (15.0 s). Background white. Reference: `passalacqua_animatic_v0.1.mp4`.

The crest is the client vector, rasterised at 4000×2200 (`passalacqua_wordmark.png`). It is used in three horizontal bands, exported as separate files at full resolution and placed at 39.32 % with their top-left corners at the positions below. The three gold fish are crops of Allen's render `passalacqua.png` and register exactly onto the line-art fish at 28.36 %.

## Shots

| Beat | Frames | What happens |
|---|---|---|
| 1 crest | 0–48 | line-art fish and wave rule on white, still (loop frame) |
| 2 wordmark | 48–86 | type fades up, holds |
| 3 fill | 86–120 | type fades out; gold floods each fish from the tail up, left, centre, right |
| 4 alive | 120–158 | Kling clip: the gold fish come alive on white |
| 5 lake | 158–197 | dissolve to the lake; Kling clip: fish drop in |
| 6 leap | 197–293 | Kling clip: three leaps |
| 7 end card | 293–312 | lake darkens; rings; rule and type reversed out |
| 8 settle | 312–336 | lake to white; gold fish rise back to the crest; type crosses white to black |
| 9 flatten | 336–355 | gold drains head-down, right, centre, left; type fades |
| 10 loop | 355–360 | hold; f359 = f0 |

## Layers, bottom to top

| # | Layer | Source (assets/) | In–out | Transform | Keyframes and notes |
|---|---|---|---|---|---|
| 1 | White BG | solid white | 0–360 | | |
| 2 | Alive clip | `pa_2_t1.mp4` | 120–158 | full frame; source f0 on f120, normal speed | opacity f120 0 → f126 100. |
| 3 | Drop clip | `pa_3_t1.mp4` | 158–197 | full frame; stretch 32.2 % (121 into 39) | opacity f158 0 → f170 100. Fish drop right f165, left f179, centre f186 (comp frames). |
| 4 | Leap clip | `pa_4_t1.mp4` | 197–293 | full frame; stretch 79.3 % (121 into 96) | hard cut in. The fish read as live fish, larger than the villa scale: a scale and gold pass in comp is the fix, not a regen. |
| 5 | Held lake | `pa_4_last_frame.png` | 293–336 | full frame | saturation 50 %; overlay dark solid RGB 0,10,25 opacity f293 0 → f305 59, hold. Rings spread from the wave-rule centre (960, 555) f293–312 (AE shape layer, 5 ellipses). |
| 6 | White return | solid white | 312–360 | | opacity f312 0 → f336 100. |
| 7 | Wave rule, line art | `pa_crest_wave_rule.png` | 0–360 | scale 39.32 %; top-left (171, 527) | still (the rule is line art throughout). Under the lake beats it is covered. |
| 8 | Fish, line art | `pa_crest_fish_lineart.png` | 0–360 | scale 39.32 %; top-left (171, 160) | still. |
| 9 | Gold fish L / C / R | `pa_gold_fish_L.png`, `_C.png`, `_R.png` (each 454×1294) | 100–126 and 312–355 | scale 28.36 %; top-left L (755, 160), C (894, 160), R (1036, 160) | beat 3: each reveals from the bottom (tail) up over 16 f, L from f100, C f103, R f106. Beat 8: start at scale 112 %, rotation L −6°, C +3°, R −4°, offset down L 90, C 60, R 110 px, with a soft shadow; ease to registered position, 100 %, 0° by f336. Beat 9: each wipes off from the top (head) down over 12 f, R from f336, C f339, L f342. |
| 10 | Type, black | `pa_crest_type.png` | 48–98 and 312–355 | scale 39.32 %; top-left (171, 677) | opacity f48 0 → f67 100, f86 100 → f98 0; f312 0 → f336 100; f343 100 → f355 0. |
| 11 | Type + rule, white | `pa_crest_type_white.png`, `pa_crest_wave_rule_white.png` | 293–336 | same positions as layers 10 and 7 | opacity f293 0 → f305 100; f312 100 → f336 0 (crossing to the black type as the field goes white). |

Loop check: f359 must equal f0 (layers 7 and 8 only).

Also in assets: `pa_1_t1.png` (generated clean lake, no fish), `pa_3_START_comp.png` (the drop clip's start frame), `passalacqua_wordmark.png` (the full crest).
