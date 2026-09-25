# North Island — edit sheet

Comp 1920×1080, 24 fps, 312 frames (13.0 s). Background white. Reference: `north_island_animatic_v0.1.mp4`.

The wordmark and the five gold turtles are baked into both plates and into the clips (accepted). No separate logo layer in this version. The lettering drifts slightly inside the swim clip; if that reads, mask the lettering region from the water plate and hold it over the clip.

## Shots

| Shot | Frames | What happens |
|---|---|---|
| 1 hold | 0–53 | lock-up on white, still |
| 2 flood | 53–96 | water floods up from the bottom edge (f53–82), then holds |
| 3 swim | 96–168 | Kling clip: turtles swim, drift right |
| 4a landfall | 168–197 | dissolve to the beach clip |
| 4b sand | 197–226 | Kling clip: turtles crawl up the sand |
| 5 return | 226–274 | Kling clip: turtles turn and go back to the water |
| 6a whiteout | 274–298 | water goes white from the top down |
| 6b loop | 298–312 | hold; f311 = f0 |

## Layers, bottom to top

| # | Layer | Source (assets/) | In–out | Transform | Keyframes and notes |
|---|---|---|---|---|---|
| 1 | White BG | solid white | 0–312 | | |
| 2 | Lock-up white | `ni_lockup_white_1536x1024.png` | 0–312 | scale 105.47 % (fit to height); centred (960, 540); white pillars each side | still |
| 3 | Water plate A | `ni_water_16x9_3641x2048.png` | 53–96 | scale 52.73 %; centred | revealed bottom → top over f53–82 with a soft edge (about 90 px): a Linear Wipe on a white cover above it, or a mask on this layer. Ease. |
| 4 | Swim clip | `ni_2_t1.mp4` | 96–197 | full frame; source f0 on f96, normal speed | hard cut in (its first frame is the water plate). |
| 5 | Sand clip | `ni_3_t1.mp4` | 168–226 | full frame; source f92 on comp f197 (start the layer at f105) | opacity f168 0 → f197 100 over the swim clip. Add a turquoise → sand colour ramp under the dissolve if it helps. |
| 6 | Return clip | `ni_4_t1.mp4` | 226–274 | full frame; stretch 39.67 % (121 into 48) | hard cut in (its first frame is the sand clip's last). |
| 7 | Water plate B | `ni_water_16x9_3641x2048.png` | 258–298 | as layer 3 | opacity f258 0 → f274 100 over the return clip's tail. |
| 8 | Whiteout cover | white | 274–298 | | covers from the top down over f274–298, soft edge 90 px, ease. At f298 the frame is layer 2 alone. |

Loop check: f311 must equal f0.

Also in assets: `ni_beach_3_turtles_1536x1024.png`, the original beach plate (three turtles), the Kling sand clip's source.
