# Giraffe Manor — Storyboard v2 for review
Film 01 of 8 · Theria hospitality slate · v2 boarded 2026-09-25 from the client brief (`Sample Hotel Animations_.docx`), Allen's decisions on v1, and the new assets in the Drive folder (vector wordmark, two Kling hero takes, birdsong ambience).

| | |
|---|---|
| Client brief | Start with image of the giraffe → the Giraffe Manor logo appears under its feet → another giraffe walks into frame → the logo disappears but the manor in the background appears → both giraffes turn and walk towards the manor and put their heads in the window |
| TRT | **16.0 s / 384 frames @ 24 fps** (f0–f383). v1's 14.0 s of picture is unchanged; 2.0 s added at the tail for the loop return |
| Master | One master: 16:9, 1920×1080, 24 fps |
| Loop | **The last frame equals the first.** f383 is pixel-identical to f0 (hero alone on cream, clean still, no logo). The film can be played on repeat with no cut |
| Frames | `frames/01_hold.png` … `frames/11_loop.png` (12 frames incl. `06b_zoomout`), contact sheet `frames/contact_sheet.jpg`. Built by `build_frames.py` from the pulled assets and `assets/wordmarks/giraffe_manor_wordmark.png`; nothing AI-enlarged; no placeholders remain |
| Status key | READY = built from an existing asset · COMP = After Effects / NLE work on existing assets · TO GENERATE = needs a Higgsfield pass (model named) |

## Decisions taken

From Allen (applied as given):

1. One master, 16:9 HD, 24 fps. The 30 fps Kling walk is conformed to 24 with optical flow.
2. Run time: v1 timings kept for beats 1–7 (14.0 s). Extended only for the loop: +1.2 s payoff hold with the mark, +0.9 s return dissolve, +0.5 s loop tail = **16.0 s**.
3. Loop rule: last frame = first frame. Implemented as a return dissolve (Beat 9) landing on the Shot 1 clean still, then a 12-frame hold that is pixel-identical to f0. `build_frames.py` asserts `11_loop == 01_hold`.
4. Vector wordmark is the approved mark (`assets/wordmarks/giraffe_manor_wordmark.png`, 3952×703 RGBA, "Giraffe Manor / Nairobi" with the patch block). It is now on every logo frame; the 288 px webp code path is gone.

Made on this board (state, not ask):

5. **Two giraffes, one colour.** The Kling walker is a darker, more saturated animal than the hero (mean RGB 153/96/60 vs 192/156/125). Plan: regenerate the walk with the hero still as the image reference (NBP for a matching side view, then Kling image-to-video). For the board the walker is colour-matched to the hero with a per-channel levels adjust in Pillow (mean and spread of the opaque pixels, gain capped at 1.35) and tagged **WALKER COLOUR-MATCHED FOR BOARD** on frames 03, 04, 06, 07. The match is board-only; it is not a grade for the film.
6. **Window payoff = exterior upstairs windows** (client reference `images-2.jpg`). The interior breakfast-window alternate is off the board.
7. **Guests stay in the manor plate.** `manor01_background.png` is used as is; no clean plate.
8. **End card folded into the return.** No separate black end. The small mark (400 px, bottom-right, on a translucent cream card so the brown mark reads over brick and ivy) fades up over the payoff hold and dissolves out with the payoff in the return.
9. **Shot 1 micro-life = Kling take2.** `kling_hero_blink_take2.mp4` (1920×1080, 24 fps, 4.04 s) is byte-identical to `frame1_to_frame2.mp4` (same md5): hero alone on cream with subtle life. Use frames 0–48 for Shot 1. `kling_hero_blink_take3.mp4` (4.0 s) is the hero with a Kling-drawn wordmark rising in from below, "Giraffe Manor" first then "Nairobi" and the patch: its pixels are not used (AI-drawn mark), but its timing is the reference for the Beat 2 logo build.
10. **Shot 1 push-in dropped.** v1 had a 1.5 % push over Shot 1; with the loop, any scale change across Shot 1 would have to be undone in the return. Shot 1 is locked off; life comes from take2.
11. **Loop frame is the clean still.** Take2's micro-life starts after f0, so f0 (and f383) is the hero before any blink or ear twitch. The Beat 2 logo, when it fades up, does not touch this frame.
12. **Ambience = birdsong.** `audio/birdsong01.wav` (179.3 s) and `birdsong02.wav` (49.8 s), both 44.1 kHz stereo PCM, are the Shot 1 ambience bed. 01 is the main bed (long enough to pick a clean 16 s section); 02 is the alternate. The bed loops with the picture: crossfade tail to head (0.5 s) across the loop point.
13. **3D wordmark noted, not used.** `upscaled/wordmark3d.obj` / `.usdz` (extrusion of the mark, with `.mtl`) is available for a dimensional logo reveal. The brief says the logo appears under the giraffe's feet; a flat mark does that, so the board keeps it flat. `upscaled/wordmark.psd` is the same mark flat on cream (reference only; the raster PNG with alpha is what the comp uses).

## Beats

| # | Brief line | IN – OUT (frames) | Frame | On screen | Motion / camera | Transition | Assets used | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | Start with image of the giraffe | 00.0 – 02.0 (f0–48) | `01_hold` | Hero giraffe alone on the cream field, centre-left, full body, facing camera-left. **f0 is the loop frame** | Locked off, no push-in. Micro-life from take2: ear, tail, one slow blink, none of it before f12 | — (f0 = f383) | `upscaled/kling_hero_blink_take2.mp4` frames 0–48, conformed to the board staging (hero 800 px tall, hooves y=880, centre x=760; take2 frames the hero a little more central, so reposition the clip in AE). Board frame built from `upscaled/ea5d5cfc-….png` (1024×1536 RGBA). Cream (255,255,240) | READY (Kling take2) — conform position in AE |
| 2 | The Giraffe Manor logo appears under its feet | 02.0 – 03.6 (f48–86) | `02_logo` | Vector wordmark, 640 px wide, on the ground line under the hooves | Rise-and-fade per take3's timing: "Giraffe Manor" first (opacity 0 → 100, y +24 → 0 px over 0.6 s), "Nairobi" and the patch block follow 0.3 s later. Hold 0.7 s | fade | `assets/wordmarks/giraffe_manor_wordmark.png` (3952×703 RGBA, from `upscaled/wordmark.ai`). Timing ref: `kling_hero_blink_take3.mp4` | COMP (AE layer over the vector) |
| 3a | Another giraffe walks into frame | 03.6 – 05.0 (f86–120) | `03_enter` | Second giraffe enters from frame right at full walk, same colouring as the hero | Walk cycle, ~1.4 s per stride pair. Logo stays put; newcomer walks behind it | — | `upscaled/giraffe_walking.mov` (ProRes 4444 with alpha, 4K/30) conformed to 24 and scaled 50 %; frame at t=0.0. Board: colour-matched | READY (existing Kling clip, colour-matched for board) → **regenerate from hero ref** (NBP side view → Kling i2v) |
| 3b | (same) | 05.0 – 06.4 (f120–154) | `04_stop` | Newcomer stops with its shoulder just clear of the hero's rump. Logo eases to 35 % | Walk decelerates to a stop over the last 4 strides | — | same clip, frame at t=2.8; stop position bbox-left x=1060 | READY / COMP — the clip does not itself stop: freeze or ease the last cycle in the NLE |
| 4 | The logo disappears but the manor in the background appears | 06.4 – 07.4 (f154–178) | `05_reveal` | Logo out; cream dissolves to the manor **at scale**: the plate arrives at 2.65× its cover size, so the terrace, steps and ground floor fill the frame behind the giraffes and they read as standing at the foot of the house | Logo opacity → 0 over 0.6 s. Background arrives at ~10 px blur. Giraffes hold at their Shot 3 size and position | cross-dissolve | `upscaled/manor01_background.png` (2752×1536, giraffes painted out, guests kept) at 2.65× cover, pivot chosen so the hooves stay on y=880 | COMP (AE). Approved staging; the 2.65× enlargement is only on screen during the dissolve and the first frames of the pull-back |
| 5 | (same) | 07.4 – 08.6 (f178–206) | `06_manor` → `06b_zoomout` | Manor resolves sharp, then the camera **zooms out**. Giraffes are locked to the plate and shrink with it | Rack focus soft → sharp over 0.4 s, then a continuous pull-back from 2.65× toward 1.0× (ease-in-out). Both giraffes scale from 800 px to ~300 px tall as the whole house comes into view | continuous | same plate; giraffes placed in plate pixels (hero hooves at plate 1744,1400; walker at 2050,1400) so the pull-back is one transform | COMP (AE): one camera move on a pre-comp |
| 6 | Both giraffes turn and walk towards the manor | 08.6 – 11.2 (f206–269) | `07_turn_TOGEN` | Pull-back lands on the full plate: both giraffes on the lawn where the plate's own giraffes stood. From here they turn away and walk up to the house | The risk shot: a 180° turn. If the pull-back is still finishing, overlap it 0.4 s into this shot | — | `07_turn_TOGEN.png` is the actual composite (plate 1.0× + both giraffes at plate scale), not a reference | **TO GENERATE (Kling)** — start frame = `07_turn_TOGEN.png` (rebuild it once the walker is regenerated), prompt in pipeline doc §6 Shot 6. Over-generate; fallback is the whip-pan cheat |
| 7 | …and put their heads in the window | 11.2 – 13.4 (f269–322) | `08_window_TOGEN` | Necks rise, both heads enter the upstairs windows. Land on the reference composition | Slow and calm | — | Shown: client reference `images-2.jpg` (exterior, 678 px). The end plate is generated to match it | **TO GENERATE**: end plate first (Seedream, same house, upstairs windows, both giraffes in the hero's colouring), then Kling start→end from Shot 6's last frame |
| 8 | (payoff hold + mark) | 13.4 – 14.6 (f322–350) | `09_payoff_mark` | Hold on the payoff. Wordmark small, bottom-right (400 px on a cream card), fades up | Mark opacity 0 → 100 over 0.4 s, hold | — | Shot 7 last frame + vector wordmark | COMP (AE) |
| 9 | (loop return) | 14.6 – 15.5 (f350–372) | `10_return_COMP` (shown at 50 %) | Payoff and mark dissolve back to the cream field with the hero alone, in her Shot 1 position | Payoff lifts toward cream first (exposure +0.6 over the first 8 frames) so the dissolve is not a hard brick-to-cream jump, then a cross-dissolve to the Shot 1 clean still. Mark rides the payoff layer and goes with it | cross-dissolve, 0.9 s | Shot 7 last frame; `01_hold` (= take2 f0) | COMP (AE) |
| 10 | (loop tail) | 15.5 – 16.0 (f372–384) | `11_loop` | Hero alone on cream. **f383 is pixel-identical to f0** | Nothing moves | cut to f0 on loop | same still as Beat 1 | READY (`build_frames.py` asserts the identity) |

**Audio.** Birdsong ambience (`audio/birdsong01.wav`, 179.3 s, main; `birdsong02.wav`, 49.8 s, alternate; both 44.1 kHz stereo) from 00.0 under Shot 1 and throughout; one low woodwind swell 06.4 → 08.6 under the reveal (not sourced); ambience alone from 13.4. The bed loops with the picture: 16.0 s section, 0.5 s crossfade tail → head at the loop point. Kling audio tracks are muted.

## Risks (two, with the decision taken)

1. **The return dissolve is a big tonal jump** (dark brick and ivy → flat cream). Decision: the payoff lifts toward cream for 8 frames before the 0.9 s cross-dissolve, and the mark goes out with the payoff layer rather than on its own. If it still reads as a hard cut in the animatic, lengthen the dissolve to 1.2 s and take the 0.3 s from the Beat 8 hold; the TRT stays 16.0 s.
2. **The loop frame depends on Shot 1's source.** If Shot 1 is take2, f0 must be take2's first frame after it is repositioned to the board staging, and the return must land on that exact frame, not on the upscaled still. Decision: the AE comp uses take2 f0 (frozen) as both the Beat 10 hold and the return's landing frame, so the identity holds by construction. The board's `01_hold`/`11_loop` stand for that frame.

## Assets still needed

- Walker regenerated to match the hero (NBP side-view reference from `ea5d5cfc-….png` → Kling i2v walk, right-to-left, alpha via the same matte pass as `giraffe_walking.mov`). Replaces the board's colour-matched stand-in on frames 03–07.
- Shot 6 Kling clip (turn and walk away), from `07_turn_TOGEN.png` as start frame (rebuild after the walker regen).
- Shot 7 end plate (both heads in the upstairs windows, matching `images-2.jpg`; Seedream), then the Kling clip.
- Woodwind swell for the reveal (not sourced; birdsong is in hand).

## What this board does not cover

- No motion was rendered; frames are stills. The animatic (24 fps, 16.0 s, looping) is the next step.
- Shot 1 micro-life and the Beat 2 logo rise are described from the Kling takes, not drawn.
- The return dissolve is shown as a single 50 % blend; its exposure lift is described only.
- The colour of the regenerated walker is not shown; the board's walker is a levels match, not a grade.
