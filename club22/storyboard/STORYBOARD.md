# 22 CLUB — storyboard v1

| | |
|---|---|
| Film | 22 Club (Theria slate, film 8 of 8) — "the numerals become the decks" |
| TRT | **12.10 s = 290 frames @ 24 fps**, cut to a 124 BPM grid (11.613 f/beat, 25 beats, 6.25 bars of 4) |
| Format | 16:9, 1920×1080 master. Frames in `frames/` (PNG) + `*_small.jpg` (960×540) + `contact_sheet.jpg` |
| Built by | `build_frames.py PULL_ROOT OUT_DIR` — Pillow only, nothing under the pull is touched |
| Source of truth | Client brief (5 lines) → `theria_hotel_animations_timing_v1.md` §8 (shot list) → this board. The earlier rendered storyboard page ("08 22 CLUB", TRT 12.0 s) is referenced where it differs. |

**Assumptions**
- 24 fps and 16:9 (both still open in the timing doc's own questions). At 30 fps every frame number here ×1.25.
- The timing doc gives shot boundaries in round seconds (2.0 / 4.4 / 6.2 / 8.2 / 10.6 / 12.0) *and* says cut to the 124 BPM grid. I snapped each boundary to its nearest beat onset; the shift is never more than 0.07 s. Both values are in the table.
- Beat numbering is 1-based from the first frame (beat 1 = f0). Beat 5 = bar 2 downbeat, beat 13 = bar 4, beat 17 = bar 5, beat 21 = bar 6, beat 25 = bar 7 downbeat (f279).
- The mark: the only file is `22 club/images.png`, 364×549 palette PNG, white ground, no alpha. Ink bbox 136×211 px. It is used at ×2.46 (Lanczos) so the mark's ink stands 520 px tall on the 1080 canvas. **That is a tagged placeholder, not an approved enlargement** — the vector (or a ≥2000 px raster) replaces it 1:1 in position. The white was colour-keyed to alpha so the same file sits on black; the red is the measured mean ink colour (181, 54, 47).
- Platters are drawn 320 px in diameter, seen from 30° above (ellipse height = 0.5 × width, per the timing doc), near edge on the digits' base line, extending *away* from camera. The two 2s are only 155 px apart at this scale, so the decks drift outward to ±185 px from centre as the digits fall. See review note 2.
- Ground: ivory (255,255,240) for beats 1–3 and 6, black outside the spotlight cone in beat 4, mixing back in beat 5 — per the timing doc. Black-ground alternate for beat 1 supplied.

## Beats

| # | Brief line served | IN–OUT (timing doc) | IN–OUT snapped to 124 BPM · frames @24 · lands on beat | Frame | On screen | Motion / camera | Transition | Assets used | Status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | "Start with the logo with the 22 club" | 0.00–2.00 s | **0.00–1.94 s · f0–46 · beats 1→5** (in on beat 1, out on bar-2 downbeat) | `01_hold_ivory.png` / `01b_hold_black_ALT.png` | The full mark, red, dead centre on ivory (alt: on black). Nothing else. | Locked off. Optional 2 % bass-pulse scale on "club" at tempo (timing doc) — not drawn. | — (out is the flip starting, no cut) | `22 club/images.png` at ×2.46 Lanczos | **PLACEHOLDER** — vector pending. Otherwise READY (AE, nothing to generate) |
| 2 | "The 22 turns on its back" | 2.00–4.40 s | **1.94–4.36 s · f46–105 · beats 5→10** (59 f, 2.46 s) | `02_flip_COMP.png` | Both 2s rotate 90° backwards about their own base line, left first, right 8 f behind; they end as two flat shapes seen from ~30° above, drifting outward onto the platter footprints. "club" does not move. Shown ≈ f80: left down, right at ~45°. | 3D layer rotation in AE, camera 30° elevation. 0.8 s per digit (19 f) with small overshoot and settle. Ease-in from still. | — | mark split into `2 L`, `2 R`, `club` (source px cols 120–180 / 183–243 / rows 321–379) | **COMP (AE)** — digit flip. Needs vector with numerals and script on separate paths. |
| 3 | "…becomes vinyl record player with spinning records" | 4.40–6.20 s | **4.36–6.29 s · f105–151 · beats 10→14** (46 f, 1.92 s) | `03_decks_TOGEN.png` | Spindle, platter rim, tonearm and a black vinyl with plain red label build onto each ellipse over 1.0 s (f105–129). Records start spinning at f130, up to speed in 0.5 s. "club" stays put and becomes the mixer fascia between/under the decks. Shown ≈ f140. | Static camera. Rotation: 33⅓ rpm = 1.8 s/rev = 43 f/rev (timing doc). Flash on the vinyl once per rev. | — | Flux stills: "Turntable platter, isolated" + "Vinyl record, isolated, top-down" (pipeline §5.1) cut out and mapped onto the 30° ellipses in AE | **TO GENERATE (Flux 2.0 Pro)** — turntable, vinyl. Deck build itself is COMP (AE). |
| 4 | "A spot light appears" | 6.20–8.20 s | **6.29–8.21 s · f151–197 · beats 14→18** (46 f, 1.92 s) | `04_spotlight_COMP.png` | Hard-edged cone drops in from top-left at f151, hits the left deck at f158, sweeps right across both by f180. Ground goes to black outside the cone. Dust in the beam. Vinyl catches the light each rotation. "club" half-lit in the spill. Shown ≈ f180. | Beam = AE cone geometry + noise-driven dust layer (pipeline §5.1 note). Track: filter opens / drop lands here. | — | Flux "Spotlight cone + floor" still as lighting reference only; beam built in AE | **COMP (AE)** — spotlight. Reference still TO GENERATE (Flux), optional. |
| 5 | "The numbers turn back around" | 8.20–10.60 s | **8.21–10.65 s · f197–255 · beats 18→23** (58 f, 2.42 s) | `05_flipback_COMP.png` | Records fade, decks strip back to bare ellipses (0.8 s, f197–216), then both digits rotate up 90° **together** (0.8 s, f216–235) with the same overshoot, sliding back to their home x. Spotlight narrows and lifts away as they rise; ground mixes back toward ivory. Shown ≈ f240 (digits at ~45°). | Reverse of beat 2 in AE, un-staggered. | — | same as beats 2–3 | **COMP (AE)** — digit flip back + spotlight lift. |
| 6 | "…and then go back to normal" | 10.60–12.00 s (doc: 12.10 s) | **10.65–12.10 s · f255–290 · beats 23→25(+end)**; hard cut to black on beat 25 = f279 (11.61 s), black held 11 f to f290 | `06_return.png` (= beat 1) | Full mark, dead centre, dead still, flat ivory light. Same pixel position as beat 1 = loop point. | Locked off. | **hard cut to black on the final downbeat (beat 25)** | `22 club/images.png` placeholder | **PLACEHOLDER / READY** as beat 1 |

Where this board differs from the earlier storyboard page ("08 22 CLUB", TRT 12.0 s, 6 beats):
- Page runs 12.0 s with beats at 0/2/4/6/9/11/12; the timing doc (and this board) runs 12.10 s at 124 BPM with the spotlight at 6.29 s and the flip-back at 8.21 s. Page gives the spotlight 3 s, timing doc 2 s — boarded to the doc.
- Page: "club" script *slides down out of the way* in beat 2 and the ground goes to ink as the digits land. Timing doc: "club" stays put and becomes the mixer fascia; ground only goes black under the spotlight. Boarded to the doc.
- Page: spin locked to the track's BPM, one deck half a beat behind; tonearm swings in from the right; red label at centre. Timing doc: 33⅓ rpm from f130. Boarded to the doc's 33⅓; both noted on frame 03's tag. Red label kept (it is also in the Flux prompt).
- Page: spotlight snaps on in one frame, sweeps left-right-left. Timing doc: drops in over 7 f, single sweep L→R. Boarded to the doc.
- Page: beat 5 is "reverse the beat 2 curve exactly, 20 % faster" and the numerals stay "still lit, still moving slightly"; beat 6 has the audio run one bar past picture. Timing doc: same-speed rise, dead still on return, hard cut to black on the final downbeat. Boarded to the doc.

## Open questions for Allen

1. **Ground: ivory or black?** The brief says nothing; the timing doc says "red on black if the film is going in a club, which it should"; the page and the rest of the slate are ivory. Frames `01_hold_ivory` and `01b_hold_black_ALT` show both. Black makes the spotlight beat (4) trivial and the loop cleaner; ivory keeps the slate grammar.
2. **Music track.** The whole edit is quantised to 124 BPM. Which sexy-techno bed, and is it licensed? Any tempo other than 124 moves every IN–OUT in the table (at 122 BPM the film is 12.30 s / 295 f). Timing doc: this is the one film where the track must be locked *before* the edit.
3. **Platter size vs. digit spacing.** Two 320 px decks cannot sit where the two 2s stand (155 px apart) — the digits have to drift ~110 px outward each as they fall (as boarded), or the decks have to be ~140 px across (too small to read). Which? Alternative: keep them tight and let the decks overlap like a DJ's two-deck setup seen in perspective.
4. **Beats 4 and 5 land on the "2" of their bars** (beats 14 and 18) if the doc's 6.2 s / 8.2 s hits are kept. Moving them to the downbeats — beat 13 (5.81 s, f139) and beat 17 (7.74 s, f186) — makes the drop hit harder but shortens the deck beat to 1.45 s. Your call; the table changes by one column.
5. **Vector artwork.** Numerals and script on separate paths, plus the exact red. Until it arrives nothing in beats 2–5 can be built for real. (Also: which "2" glyph face is the brand's — the source has a flat base bar on each 2 that the flip is built around.)

## Assets still needed

| Asset | For | Route | Notes |
|---|---|---|---|
| 22 club mark, vector (AI/EPS/SVG), numerals + script as separate paths | every beat | client | The 364×549 PNG is a placeholder at ×2.46. Do not upscale with a model (pipeline §4). |
| Turntable platter, isolated, low three-quarter | beat 3 | Flux 2.0 Pro, pipeline §5.1 prompt 1 | Needs to read at 30° elevation; two copies. |
| Vinyl record, top-down, plain red label | beats 3–4 | Flux 2.0 Pro, pipeline §5.1 prompt 2 | Mapped to the ellipse in AE; rotation done in AE. |
| Spotlight cone + dusty floor still | beat 4 (reference only) | Flux 2.0 Pro, pipeline §5.1 prompt 3 | Beam itself built in AE. Optional. |
| Techno bed, 124 BPM, ≥13 s, licensed | all | Allen / client | Locks the frame grid. |

## What this board does not cover

- **No motion was tested.** Every frame is a still at one representative frame number; the digit flip is drawn as a vertical squash, not a true 3D projection. The overshoot, the 8 f stagger and the tonearm move only exist as words.
- **No real deck, vinyl, spotlight or dust artwork.** Beats 2–5 are Pillow schematics tagged COMP / TO GENERATE. Nothing was generated; the pipeline §5.1 prompts were not run or rewritten.
- **The mark is a Lanczos resize of a 364 px PNG**, colour-keyed to alpha. It is not the logo at delivery quality and it must not be shown to the client as such.
- **Audio.** No track chosen, no filter/drop automation specified beyond "filter opens under the spotlight, drop on the flip-back" (timing doc). The 124 BPM grid is an assumption until the track is locked.
- **Aspect ratio and frame rate** other than 16:9 @ 24 fps. 9:16 would restack the decks vertically and the whole flip geometry changes.
- **Type, taglines, URLs, end-card legal.** Logo only, as on every film in the slate.
- **Sound-design of the flip** (mechanical clunk, needle drop) — not specified anywhere upstream, not added here.
