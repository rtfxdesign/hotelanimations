# Giraffe Manor — Storyboard v1 for review
Film 01 of 8 · Theria hospitality slate · boarded 2026-09-25 from the client brief (`Sample Hotel Animations_.docx`) and the real assets in the Drive folder.

| | |
|---|---|
| Client brief | Start with image of the giraffe → the Giraffe Manor logo appears under its feet → another giraffe walks into frame → the logo disappears but the manor in the background appears → both giraffes turn and walk towards the manor and put their heads in the window |
| TRT | **14.0 s / 336 frames @ 24 fps** (timing doc v1). The earlier storyboard page ran it at 12.0 s; see open question 1 |
| Master | 16:9, 1920×1080 (HD confirmed 2026-09-25). The storyboard page also lists 1:1 and 9:16 masters; see open question 2 |
| Frames | `frames/01_hold.png` … `frames/09_endcard.png` (11 frames incl. `06b_zoomout` and the `08b` alternate), contact sheet `frames/contact_sheet.jpg`. Built by `build_frames.py` from the pulled assets; nothing AI-enlarged |
| Status key | READY = built from an existing asset · COMP = After Effects / NLE work on existing assets · TO GENERATE = needs a Higgsfield pass (model named) |

## Beats

| # | Brief line | IN – OUT (frames) | Frame | On screen | Motion / camera | Transition | Assets used | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | Start with image of the giraffe | 00.0 – 02.0 (f0–48) | `01_hold` | Hero giraffe alone on the cream field, centre-left, full body, facing camera-left | Locked off. Micro-life only: ear twitch f12, tail flick f30, one slow blink f40. 1.5 % push-in over the shot | — | `upscaled/ea5d5cfc-….png` (1024×1536 RGBA, opaque 881×1487) scaled to 800 px tall; cream (255,255,240) sampled from the Kling test frames | COMP (still + micro-life) or Kling Shot 1 prompt from pipeline doc §6 |
| 2 | The Giraffe Manor logo appears under its feet | 02.0 – 03.6 (f48–86) | `02_logo` | Wordmark fades up on the ground line directly under the hooves | Scale 96 → 100 % ease-out, opacity 0 → 100 over 0.8 s, hold 0.8 s | fade | `orig/Giraffe-Manor-Logo-46px.webp` (288×46) at 2× as a **placeholder**. The AI-drawn `giraffemanor_wordmark_alpha.png` is not used: wrong typeface and case | COMP (AE layer) — **blocked on vector logo** |
| 3a | Another giraffe walks into frame | 03.6 – 05.0 (f86–120) | `03_enter` | Second giraffe enters from frame right at full walk | Walk cycle, ~1.4 s per stride pair. Logo stays put; newcomer walks behind it | — | `upscaled/giraffe_walking.mov` (ProRes 4444 with alpha, 4K/30) conformed to 24 and scaled 50 %; frame at t=0.0 | READY (existing Kling clip) — conform 30→24 with optical flow |
| 3b | (same) | 05.0 – 06.4 (f120–154) | `04_stop` | Newcomer stops with its shoulder just clear of the hero's rump. Logo eases to 35 % | Walk decelerates to a stop over the last 4 strides | — | same clip, frame at t=2.8; stop position bbox-left x=1060 | READY / COMP — the clip does not itself stop: freeze or ease the last cycle in the NLE |
| 4 | The logo disappears but the manor in the background appears | 06.4 – 07.4 (f154–178) | `05_reveal` | Logo out; cream dissolves to the manor **at scale**: the plate arrives at 2.65× its cover size, so the terrace, steps and ground floor fill the frame behind the giraffes and they read as standing at the foot of the house, not towering over it | Logo opacity → 0 over 0.6 s. Background arrives at ~10 px blur. Giraffes hold at their Shot 3 size and position | cross-dissolve | `upscaled/manor01_background.png` (2752×1536, giraffes painted out) at 2.65× cover, pivot chosen so the hooves stay on y=880 | COMP (AE). The 2.65× enlargement is only on screen during the dissolve and the first frames of the pull-back |
| 5 | (same) | 07.4 – 08.6 (f178–206) | `06_manor` → `06b_zoomout` | Manor resolves sharp, then the camera **zooms out**. Giraffes are locked to the plate and shrink with it | Rack focus soft → sharp over 0.4 s, then a continuous pull-back from 2.65× toward 1.0× (ease-in-out). Both giraffes scale down from 800 px to ~300 px tall as the whole house comes into view | continuous | same plate; giraffes placed in plate pixels (hero hooves at plate 1744,1400; walker at 2050,1400) so the pull-back is one transform | COMP (AE): one camera move on a pre-comp |
| 6 | Both giraffes turn and walk towards the manor | 08.6 – 11.2 (f206–269) | `07_turn_TOGEN` | Pull-back lands on the full plate: both giraffes on the lawn where the plate's own giraffes stood. From here they turn away and walk up to the house | The risk shot: a 180° turn. If the pull-back is still finishing, overlap it 0.4 s into this shot | — | `07_turn_TOGEN.png` is the actual composite (plate 1.0× + both giraffes at plate scale), not a reference | **TO GENERATE (Kling)** — start frame = `07_turn_TOGEN.png`, prompt in pipeline doc §6 Shot 6. Over-generate; fallback is the whip-pan cheat |
| 7 | …and put their heads in the window | 11.2 – 13.4 (f269–322) | `08_window_TOGEN` (exterior) · `08b_window_interior_ALT` | Necks rise, both heads enter the windows. Land on the reference composition | Slow and calm | — | Placeholders show the client reference photos `images-2.jpg` (exterior, 678 px) and `images.jpg` (interior breakfast room, 547 px) | **TO GENERATE (Kling)**, end plate first (Seedream), see open question 3 |
| 8 | (end card, not in brief) | 13.4 – 14.0 (f322–336) | `09_endcard` | Wordmark small, bottom-right, 60 % of Shot 2 size, over the payoff frame darkened; hold to black | fade to black f336 | fade | logo placeholder as above | COMP (AE) |

**Audio** (timing doc): Kenyan highland ambience from 00.0; one low woodwind swell 06.4 → 08.6 under the reveal; ambience alone from 13.4. Not sourced.

## Review notes (what to look at)

1. **Giraffe identity.** The Kling walker (`giraffe_walking.mov`) is a darker, more orange animal than the pale hero still. Frames 04–06 show them side by side. Either regenerate the walk from the hero as reference (NBP for consistency, then Kling) or accept two different giraffes.
2. **Staging scale, frames 05–07 (revised after Allen's note).** The manor now fades in at scale and the camera pulls back, so the giraffes never appear oversized against the house. Cost: the plate is enlarged 2.65× at the reveal, so it is soft for about a second while blurred anyway. If that bothers you, the fix is a second manor plate shot from the foot of the steps (Seedream, same house) for the reveal, cross-dissolving to the wide during the pull-back. Also visible at 2.65×: guests and staff on the terrace behind the giraffes.
3. **Logo.** Every wordmark on the board is the 288 px web mark at 2×. It is legible on the board and unusable in the film. Nothing else in the folder is the real mark.
4. **Guests in the plate.** `manor01_background.png` still has staff and guests at the tables. The earlier storyboard page asked for a clean plate; the brief does not. Decide.

## Open questions for Allen

1. TRT 14.0 s (timing doc) or 12.0 s (storyboard page)? The board is cut at 14.0.
2. One master (16:9 HD) or three (1:1, 9:16, 16:9)? Frames 01–04 survive a 1:1 crop; frame 06 does not.
3. Payoff: exterior upstairs windows (`images-2.jpg`, timing doc) or interior breakfast window (`images.jpg`, storyboard page)? Both are boarded as 08 / 08b.
4. Guests in the manor plate: keep or regenerate clean?
5. Frame rate 24 (board) or 30 (Kling walk native)?

## Assets still needed

- Vector Giraffe Manor wordmark (AI/EPS/SVG) — blocks Beats 2 and 8.
- Shot 6 Kling clip (turn and walk away), from `06_manor` as start frame.
- Shot 7 end plate (heads in windows, matching the chosen reference) then the Kling clip.
- Optional: clean manor plate without guests; a walker regenerated to match the hero's colouring.

## What this board does not cover

- No motion was rendered; frames are stills. The animatic is the next step once the questions above are answered.
- Audio not sourced.
- 1:1 and 9:16 reframes not drawn.
- Shot 1 micro-life and Shot 2 logo animation are described, not shown.
