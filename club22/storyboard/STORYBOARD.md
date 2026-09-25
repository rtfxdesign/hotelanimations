# 22 CLUB — storyboard v2

| | |
|---|---|
| Film | 22 Club (Theria slate, film 8 of 8) — "the numerals become the decks" |
| TRT | **12.10 s = 290 frames @ 24 fps**, cut to a 124 BPM grid (11.613 f/beat, 25 beats, 6.25 bars of 4). Picture cuts to black on beat 25 = f279; black held 11 f to f290 |
| Format | 16:9, 1920×1080 master, 24 fps. Frames in `frames/` (PNG) + `*_small.jpg` (960×540) + `contact_sheet.jpg` |
| Ground | **Black** (0,0,0) throughout — Allen's call. No ivory anywhere in this film |
| Mark | Client vector `22 club/22club_wordmark.ai`, rasterised to `assets/wordmarks/club22_wordmark.png` (2023×3050 RGBA). Used at ×0.223 so the ink stands 520 px tall, 335 px wide, top-left of ink at (793, 280). Brand red **178/47/40** (read from the file). No placeholders remain |
| Built by | `build_frames.py PULL_ROOT OUT_DIR` — Pillow only; the mark comes from the repo raster, the pull is only checked for the `.ai` source and never modified |
| Source of truth | Client brief (5 lines) → `theria_hotel_animations_timing_v1.md` §8 → v1 board → Allen's decisions (below) → this board |
| Changes v1 → v2 | Vector mark replaces the 364 px placeholder; ivory dropped, one ground; `01b` alternate frame removed; beat-6 composite is byte-for-byte the beat-1 composite; open-questions section closed out as decisions |

## Decisions taken

From Allen (applied, not re-opened):
1. **One master, 16:9, 1920×1080, 24 fps.** The v1 beat grid at 124 BPM stays exactly as it was (12.10 s / 290 f).
2. **Black ground.** Beat 1 is the red mark on black; the spotlight beat no longer has to "take the ground to black" — the ground already is, so the beam only brightens what it covers and the decks sit at 55 % outside the cone. Beat 5 no longer mixes the ground anywhere; the light lifts to nothing and black remains.
3. **Loop rule: last picture frame = first frame.** The beat-6 composite is the beat-1 composite reused (the build asserts the two are pixel-identical). f278 → f0 is a clean join.
4. **The vector mark is the mark.** Split read from the raster's alpha: digits rows 262–1884, left 2 cols 345–1014, right 2 cols 1029–1699 (15 px clear column between them), script rows 1952–2595 cols 280–1783. Three AE layers: `2 L`, `2 R`, `club`.

Judgement calls made here:
5. **The two 2s drift outward as they fall** — left −107 px, right +110 px — landing centred on 320 px platters at x = 775 / 1145 (±185 from centre). At 520 px mark height the digits' centres are only 153 px apart; two readable decks need the drift. The drift is eased in with the rotation (it is part of the fall, not a separate slide) and reversed on the way back up in beat 5. Alternative (140 px decks, no drift) rejected: too small to read as turntables at 1080p.
6. **Hinge line = the 2s' lowest ink row** (source row 1884, canvas y = 642). The vector's "2" has a calligraphic swash base, not the flat bar the timing doc assumed; there is no straight edge to rotate on, so each digit rotates about a horizontal axis through its lowest ink point and the platter rim, once built, hides the swash. Left digit rotates first, right +8 f.
7. **Spotlight and flip-back keep the timing doc's 6.2 s / 8.2 s hits**, snapped to beats 14 (f151) and 18 (f197) — the "2" of bars 4 and 5. Moving them to the downbeats would shorten the deck beat to 1.45 s; the syncopated hit is the better trade.
8. **Cut to black on beat 25 = f279**, black held 11 f to f290 so audio can ring out under black. The loop point is therefore the last *picture* frame (f278), not the last frame of the file — see risk 1.
9. **Spin at 33⅓ rpm from f130** (43 f/rev, timing doc), not locked to the 124 BPM bar. The vinyl flash reads as a record; the beat is carried by the light and the cuts.
10. **Perspective: 30° camera elevation**, platter ellipses at 0.5 × width, near rim on the hinge line, extending away from camera. The "club" script never moves; in beat 3 it reads as the mixer fascia between and below the decks.

### Flagged risks (two, each with the decision)

| # | Risk | Decision |
|---|---|---|
| 1 | **Loop vs. cut-to-black.** A player that loops the file will show an 11 f blink of black (f279–289) before the mark reappears at f0. | Keep the black tail — it is Allen's beat-25 cut and the audio needs it. For a seamless-loop deliverable (club screens), trim the export at f279: TRT 11.61 s = exactly 24 beats / 6 bars, and f278 → f0 already joins. Both cuts come from the same master; no re-animation. |
| 2 | **The digit gap is 3 px on the canvas** (15 px in the source): when the left 2 goes down first, its top edge sweeps back through the space directly beside the still-upright right 2. In a true 3D rotation the two layers can z-fight for ~8 f. | Rotate the digits about an axis 2 px *behind* their face (not on it) and put the left digit on a lower z-order for beats 2–5; the 8 f stagger means the right 2 is still upright and in front when the left passes it, which reads correctly from the 30° camera. Verified only as words; first thing to test in the AE block-through. |

## Beats

| # | Brief line served | IN–OUT (timing doc) | IN–OUT snapped to 124 BPM · frames @24 · lands on beat | Frame | On screen | Motion / camera | Transition | Assets used | Status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | "Start with the logo with the 22 club" | 0.00–2.00 s | **0.00–1.94 s · f0–46 · beats 1→5** (in on beat 1, out on bar-2 downbeat) | `01_hold.png` | The full mark, brand red, dead centre on black. Nothing else. | Locked off. Optional 2 % bass-pulse scale on "club" at tempo (timing doc) — not drawn. | — (out is the flip starting, no cut) | `club22_wordmark.png` ×0.223, whole mark | **READY** (AE, nothing to generate) |
| 2 | "The 22 turns on its back" | 2.00–4.40 s | **1.94–4.36 s · f46–105 · beats 5→10** (59 f, 2.46 s) | `02_flip_COMP.png` | Both 2s rotate 90° backwards about the hinge line (their lowest ink row), left first, right 8 f behind; they end as two flat shapes seen from 30° above, drifting outward (−107 / +110 px) onto the platter footprints. "club" does not move. Shown ≈ f80: left down, right at ~45°. | 3D layer rotation in AE, camera 30° elevation. 0.8 s per digit (19 f) with small overshoot and settle. Ease-in from still. Drift eased with the rotation. | — | mark split into `2 L`, `2 R`, `club` (source cols 345–1014 / 1029–1699, rows 262–1884; script rows 1952–2595) | **COMP (AE)** — digit flip. Layers exist; see risk 2 |
| 3 | "…becomes vinyl record player with spinning records" | 4.40–6.20 s | **4.36–6.29 s · f105–151 · beats 10→14** (46 f, 1.92 s) | `03_decks_TOGEN.png` | Spindle, platter rim, tonearm and a black vinyl with plain red label build onto each ellipse over 1.0 s (f105–129). Records start spinning at f130, up to speed in 0.5 s. "club" stays put and becomes the mixer fascia between/under the decks. Shown ≈ f140. | Static camera. Rotation: 33⅓ rpm = 1.8 s/rev = 43 f/rev. Flash on the vinyl once per rev. Tonearm pivots behind the far rim (decks sit 50 px apart). | — | Flux stills: "Turntable platter, isolated" + "Vinyl record, isolated, top-down" (pipeline §5.1) cut out and mapped onto the 30° ellipses in AE | **TO GENERATE (Flux 2.0 Pro)** — turntable, vinyl. Deck build itself is COMP (AE). |
| 4 | "A spot light appears" | 6.20–8.20 s | **6.29–8.21 s · f151–197 · beats 14→18** (46 f, 1.92 s) | `04_spotlight_COMP.png` | Hard-edged cone drops in from top-left at f151, hits the left deck at f158, sweeps right across both by f180. Decks at 55 % outside the cone, full inside. Dust in the beam. Vinyl catches the light each rotation. "club" half-lit in the spill. Shown ≈ f180. | Beam = AE cone geometry + noise-driven dust layer (pipeline §5.1 note). Track: filter opens here. | — | Flux "Spotlight cone + floor" still as lighting reference only; beam built in AE | **COMP (AE)** — spotlight. Reference still TO GENERATE (Flux), optional. |
| 5 | "The numbers turn back around" | 8.20–10.60 s | **8.21–10.65 s · f197–255 · beats 18→23** (58 f, 2.42 s) | `05_flipback_COMP.png` | Records fade, decks strip back to bare ellipses (0.8 s, f197–216), then both digits rotate up 90° **together** (0.8 s, f216–235) with the same overshoot, sliding back to their home x. Spotlight narrows and lifts to nothing by f255. Ground stays black. Shown ≈ f240 (digits at ~45°). | Reverse of beat 2 in AE, un-staggered. Track: drop lands on f197. | — | same as beats 2–3 | **COMP (AE)** — digit flip back + spotlight lift. |
| 6 | "…and then go back to normal" | 10.60–12.00 s (doc: 12.10 s) | **10.65–12.10 s · f255–290 · beats 23→25(+end)**; hard cut to black on beat 25 = f279 (11.61 s), black held 11 f to f290 | `06_return.png` (= `01_hold.png` composite, pixel-identical) | Full mark, dead centre, dead still, red on black. Same pixels as beat 1 = loop point (f278 → f0). | Locked off. | **hard cut to black on the final downbeat (beat 25)** | `club22_wordmark.png`, whole mark | **READY** as beat 1 |

Where this board still differs from the earlier storyboard page ("08 22 CLUB", TRT 12.0 s, 6 beats) — unchanged from v1, boarded to the timing doc in every case: 12.10 s at 124 BPM (not 12.0 s); "club" stays put as the mixer fascia (does not slide away); 33⅓ rpm spin (not BPM-locked); single L→R spotlight sweep dropping in over 7 f (not a one-frame snap); same-speed un-staggered rise and a hard cut on the final downbeat (not "20 % faster" with audio running a bar past picture).

## Assets still needed

| Asset | For | Route | Notes |
|---|---|---|---|
| Turntable platter, isolated, low three-quarter | beat 3 | Flux 2.0 Pro, pipeline §5.1 prompt 1 | Needs to read at 30° elevation; two copies. Brushed rim, black slipmat, chrome spindle, matte tonearm. |
| Vinyl record, top-down, plain red label | beats 3–5 | Flux 2.0 Pro, pipeline §5.1 prompt 2 | Label in brand red 178/47/40. Mapped to the ellipse in AE; rotation done in AE. |
| Spotlight: AE build (cone geometry + Optical Flares + noise-driven dust) | beats 4–5 | AE, by us | The Flux "spotlight cone + floor" still (§5.1 prompt 3) is a lighting reference only, optional. |
| Techno bed, 124 BPM, ≥ 13 s, **licensed** | all | Allen / client | Locks the frame grid. Any other tempo moves every IN–OUT in the table (at 122 BPM the film is 12.30 s / 295 f). Filter opens f151, drop f197. |

Nothing else is outstanding on the mark: the vector is in the pull (`22club_wordmark.ai`) and the raster in `assets/wordmarks/` is the working file. `Asset 1.png` / `Asset 1@2x.png` (541×840) are PNG exports of the same vector, kept for reference only.

## What this board does not cover

- **No motion was tested.** Every frame is a still at one representative frame number; the digit flip is drawn as a vertical squash, not a true 3D projection. The overshoot, the 8 f stagger, the eased drift and the tonearm move only exist as words. Risk 2 (digit z-order during the stagger) is untested.
- **No real deck, vinyl, spotlight or dust artwork.** Beats 2–5 are Pillow schematics tagged COMP / TO GENERATE. Nothing was generated; the pipeline §5.1 prompts were not run or rewritten.
- **Audio.** No track chosen; filter/drop automation is specified only as "filter opens f151, drop f197". The 124 BPM grid is fixed by decision but still needs a track that is actually 124.
- **Any format other than 16:9 @ 24 fps.** Allen fixed one master. A 9:16 or square cut-down would restack the decks and the whole flip geometry changes; not boarded.
- **Type, taglines, URLs, end-card legal.** Logo only, as on every film in the slate.
- **Sound design of the flip** (mechanical clunk, needle drop) — not specified anywhere upstream, not added here.
- **Colour management.** Brand red is taken as the sRGB value in the raster (178/47/40). If the vector carries a spot/CMYK definition, match to that in AE, not to this number.
