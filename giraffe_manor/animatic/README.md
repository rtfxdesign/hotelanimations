# Giraffe Manor — animatic v0.1

`giraffe_manor_animatic_v0.1.mp4` — 1920×1080, 24 fps, 16.0 s (384 frames), H.264 + AAC. Last frame equals the first (verified in the build). Birdsong bed at −14 dB with 0.5 s fades. Burn-in top-left: shot, frame, time.

Built by `build_animatic.py` from the v2 storyboard staging. Shots 6 (the turn) and 7 (heads in the windows) are placeholders with captions until the Kling clips exist: shot 6 is a crude shrink-and-drift on the comp, shot 7 is the client reference photo with a slow push-in.

| Shot | Frames | Source |
|---|---|---|
| 1 hold | 0–48 | hero still on cream (Kling micro-life from `kling_hero_blink_take2.mp4` replaces this in the comp) |
| 2 logo | 48–86 | vector wordmark fades up under the hooves |
| 3a/3b walker | 86–154 | `giraffe_walking.mov` colour-matched, 30→24 by time sampling, eased in to the stop position |
| 4 reveal | 154–178 | dissolve to the manor plate at 2.65× cover, 10 px blur |
| 5 pull-back | 178–216 | rack focus 10 f, then z 2.65 → 1.0 over 28 f |
| 6 turn | 216–269 | PLACEHOLDER |
| 7 windows | 269–322 | PLACEHOLDER (reference photo) |
| 8 payoff + mark | 322–351 | mark fades up bottom-right |
| 9 return | 351–373 | exposure lift then dissolve to the hero alone |
| 10 loop hold | 373–384 | = frame 0 |

Rebuild: `python giraffe_manor/animatic/build_animatic.py PULL_ROOT WALK_FRAMES_DIR OUT_DIR` (add `--no-burnin` for a clean pass).

## v0.2 (2026-09-25, after Sol round 1)

`giraffe_manor_animatic_v0.2.mp4` — same 384-frame structure. Shots 6–9 now use generated material:

| Shot | Frames | Source |
|---|---|---|
| S6 turn | 206–269 | `generation_kit/output/01_giraffe_manor/gm_2_t3.mp4` (Kling 3, first+last frame), all 121 frames retimed 2× into 63; 6-frame dissolve from the staged plate at f216. No in-place turn yet: the giraffes travel to the steps and end rear-facing. Roto/retime candidate. |
| S7 windows | 269–322 | hard cut to `gm_3b_t1.png` (in-place edit of the plate crop), still with a 4 % push. GM-4 (necks rise) pending. |
| S8, S9 | 322–373 | same plate; mark and return as v0.1 |

Build: `GM_S6_FRAMES=<dir of clip PNGs> GM_S7_PLATE=<gm_3b_t1.png> python3 build_animatic.py PULL_ROOT WALK_FRAMES_DIR OUT_DIR`. Without the two variables the v0.1 placeholders render.

## v0.3 (2026-09-25, after Sol round 3)

`giraffe_manor_animatic_v0.3.mp4` — shot 7 is now the generated GM-4 clip (Kling 3, first frame GM-3c necks lowered, last frame GM-3b heads in the windows): necks rise over f269–291, heads in from f291, and shots 8–9 continue on the same clip (source f53–103) so the payoff keeps breathing under the mark. Shot 6 unchanged from v0.2.

Build: `GM_S6_FRAMES=<GM-2 t3 PNGs> GM_S7_FRAMES=<GM-4 PNGs> python3 build_animatic.py PULL_ROOT WALK_FRAMES_DIR OUT_DIR`. `GM_S7_PLATE` remains as the still fallback when no clip is given.
