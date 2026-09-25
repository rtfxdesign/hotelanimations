# Passalacqua, Lago di Como — storyboard v1

| | |
|---|---|
| Film | 03 · Passalacqua — "three fish leave the crest" |
| Client / studio | Theria / Allen Grabo, RTFX Design |
| TRT | **13.0 s (f312)** per `theria_hotel_animations_timing_v1.md` §3. The earlier storyboard page says 12.5 s / 6 beats — boarded to the timing doc, page differences noted per beat. |
| Frame rate | 24 fps (frame numbers `f###`) |
| Master | 16:9, 1920×1080 board frames (the aspect is still "not decided" in the timing doc; logo-safe area = centre 80 %) |
| Frames | `frames/01_outlines.png` … `frames/08_endcard_COMP.png` (+ `ref_images-3_villa.png`), each with a `*_small.jpg` (960×540), and `frames/contact_sheet.jpg` |
| Built by | `build_frames.py PULL_ROOT OUT_DIR` — Pillow only, all frames from the four files in `Passalaqua/`; nothing under the pull directory was modified |
| Board date | 2026-09-25 |

**Assumptions**

1. The brief's "start with their logo of 3 outlines / add the logo underneath" is read as the timing doc reads it: fish mark first, wordmark second.
2. **The pull's file descriptions in the timing doc are wrong, and the board follows what the files actually contain** (verified by eye and by pixel stats):
   - `passalacqua.jpg` 410×319 — the printed mark (flat gold fish, wave rule, PASSALACQUA / LAGO DI COMO). The only flat source.
   - `images-3.jpg` 275×183 — **not** the mark: a small photo of a villa on Como (it looks like Villa del Balbianello, not Passalacqua).
   - `46e10c0f-….png` 1421×1107 — **not** the leap: the same lockup re-rendered on white with dimensional polished-gold fish (an AI render; its wordmark is redrawn, so only its fish are used here).
   - `b74514e7-….png` 1536×1024 — **not** a villa-only plate: this is the leap — three gold fish breaching in sync, villa behind. There is no fish-free lake plate anywhere in the pull.
3. Logo rule: the 410 px mark is never AI-enlarged. Beats 1–3 and the end card show it at a plain 2× Lanczos resize (820×638, 43 % of frame width, fish ≈154 px tall) tagged `PLACEHOLDER — 410 px source at plain 2x, vector crest pending`. That is the honest size, not the design intent — see open question 5.
4. Every wordmark appearance is an AE layer over the plate (pipeline doc §4), so no beat needs NBP. Gold fish = Flux (objects), lake/villa = Seedream (worlds), motion = Kling, end card = comp.
5. The gold fish in beats 3–5 are rectangular crops of `46e10c0f` with a cheap white-threshold alpha (not a key); edges are crunchy and are only for the board.

## Beats

| # | Brief line served | IN – OUT (s) · frames @24 | Frame | On screen | Motion / camera | Transition | Assets used | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | "Start with their logo of 3 outlines of golden fishes" | 00.0 – 02.0 · f0–f48 | `01_outlines.png` | Three flat gold fish over the wave rule, white field, no type. | Fish draw on in sequence: left f0–14, centre f8–22, right f16–30. Then dead still. *(Page: "hairline engraving", paths write in L→R over 1.1 s — same idea, same order.)* | — (open) | `passalacqua.jpg` (rows 70–163 of the 410 px source, 2×) | **PLACEHOLDER** — needs the vector crest with the three fish and the wave rule on separate paths. Comp in AE. |
| 2 | "Add the logo underneath" | 02.0 – 03.6 · f48–f86 | `02_wordmark.png` | PASSALACQUA / LAGO DI COMO fades up beneath the wave rule; full printed crest. | Wordmark opacity 0→1, letter-spacing eases +8 % → +4 % as it fades. Hold 0.8 s. *(Page disagrees: "fade + 8 px rise; no tracking animation, the crest is fixed artwork" — see OQ 4.)* | — | `passalacqua.jpg` (full mark, 2×) | **PLACEHOLDER** — vector crest. Comp in AE (wordmark is a separate AE layer). |
| 3 | "The logo disappears as the fish become real golden fish — colored in" | 03.6 – 05.0 · f86–f120 | `03_fill.png` | Wordmark at 35 % and going; gold floods each fish bottom-to-top, scales catch light, eyes gain a specular. Frame shows the flood at ~55 %. | Wordmark opacity → 0 over 0.5 s (f86–98). From f100 gold gradient floods each body from the tail up, 900 ms per fish, staggered 120 ms (page timing). Wave rule stays. | — | `passalacqua.jpg` (2×, type at 35 %) + `46e10c0f-….png` (gold fish block, registered onto the flat fish, bottom-up mask) | **COMP** (fill wipe in AE) + **TO GENERATE (Flux)**: three isolated gold fish on white, flat-on, one per layer with alpha. `46e10c0f` is usable as the look reference for the filled state. |
| 4 | "The fish then become alive" | 05.0 – 06.6 · f120–f158 | `04_alive_TOGEN.png` | Three dimensional gold fish alone on white, turned slightly off-axis, cast shadows on the white, mid first tail beat. | Rotate flat-on → three-quarter, gain a cast shadow, first tail beat; the three are offset ~150 ms so they never move in lockstep. Board assumes a gentle ~30 % push-in as they come off the page (not in the timing doc). *(Page adds: gills work, fins flutter, "the wave rule thickens into actual water" — that is boarded in beat 5 instead.)* | — | `46e10c0f-….png` (three fish crops, white-threshold alpha, rotated −9° / +4° / −5°, synthetic shadows) | **TO GENERATE (Kling)** — start frame = beat 3 end, end frame = three-quarter fish with tail beat. Needs the Flux isolated fish first. |
| 5 | "Add the background of the villa" | 06.6 – 08.2 · f158–f197 | `05_lake_TOGEN.png` | White dissolving to the lake; water level rising into the bottom third; the three fish tipping over and dropping into it, splash rings on landing. | Cross-dissolve white → lake plate. Water rises to ~y 740 (bottom third). Fish pitch nose-down and drop, staggered; rings on entry. *(Page: lake "floods in behind them — mountains, cypress, the villa on its terrace".)* | cross-dissolve in | `b74514e7-….png` (55 % under white, blurred — the baked-in leaping fish are visible, tagged) + `46e10c0f-….png` fish crops | **TO GENERATE (Seedream)** clean lake + villa plate, no fish, 16:9, 3840×2160. **TO GENERATE (Kling)** drop-in with splashes. |
| 6a | "the fish jumping out of the water" | 08.2 – 10.2 · f197–f245 | `06_leap_TOGEN.png` | The leap, tight framing (plate at 112 %): centre fish breaching. | Three staggered arcs — centre breaches at 08.6, left at 09.4, right at 10.1; each airborne ~0.9 s with a full body arc and a water sheet off the tail. *(Page: "all three break the surface together", peak at 09.6, 240 fps water retimed 0.5× at apex — see OQ 3.)* | — | `b74514e7-….png` (fit-cover, zoom 1.12) | **TO GENERATE (Kling)** — `b74514e7` is the leap keyframe but shows all three in sync; the film must stagger them (three separate fish layers, or three Kling passes on the clean plate). |
| 6b | same beat, second half | 10.2 – 12.2 · f245–f293 | `07_pullback_TOGEN.png` | Same shot, camera 12 % wider, villa opened up, last (right) fish still airborne. | Camera pulls back 12 % across the whole 4.0 s shot (08.2 → 12.2). | — | `b74514e7-….png` (fit-cover, full) | **TO GENERATE (Kling)** — same clip as 6a; boarded as two frames only to show the pull-back. |
| 7 | end card (not in the brief; timing doc / page) | 12.2 – 13.0 · f293–f312 | `08_endcard_COMP.png` | Last fish re-enters; the splash rings settle into the wave rule of the crest; wordmark fades up reversed-out over the darkened lake. | Rings contract and flatten into the rule (the "signature move"; comp, not a model). Wordmark fade 0→1. *(Page ends differently: wordmark "re-forms in the white" — back to the crest on white, which also satisfies the global loop rule — see OQ 2.)* | fade out | `b74514e7-….png` (desaturated, darkened, blurred) + `passalacqua.jpg` (wave rule + wordmark at 2×, reversed to white) | **COMP (AE)** — pipeline doc: do the ripple→rule in comp, fall back to a straight fade if it fights. Needs the vector crest and the clean lake plate. |
| ref | — | — | `ref_images-3_villa.png` | The pull's fourth file, so nothing is unaccounted for. | — | — | `images-3.jpg` (275 px, fit-cover) | **REFERENCE ONLY** — not a beat. |

Sound (timing doc): lake ambience + distant church bell from 00.0; three water-breaks at 08.6 / 09.4 / 10.1; strings resolve on the end card. *(Page: room tone → single water drop at the moment of colouring → lake; strings enter on the jump.)*

## Open questions for Allen

1. **Is this the right villa?** `b74514e7` (the leap plate) and `images-3.jpg` both look like Villa del Balbianello at Lenno, not Passalacqua at Moltrasio. If the client will notice (they will), the clean lake plate should be generated from a real Passalacqua facade reference — do we have one?
2. **How does it end?** Timing doc: wordmark over the lake, fade. Page: ripples → wave rule → wordmark re-forms *in the white*, i.e. back to the beat-2 crest, which is also what the global "each film ends on its own opening frame" rule wants. Board follows the timing doc; page version is one extra dissolve.
3. **Leap: staggered (timing doc) or together (page)?** The only plate has them in sync. Staggered means three fish layers or three Kling passes over the clean plate; together means one pass but loses the three water-breaks in the audio.
4. **Wordmark tracking ease (+8 % → +4 %, timing doc) or fixed artwork (page)?** The page's argument — "this is the frame that must read as the printed mark" — is the brand-safe one.
5. **Crest size and the coloured-in look.** At the permitted 2× the placeholder fish are 154 px tall on a 1080 frame; once the vector arrives, propose fish ≈ 35 % of frame height for beats 1–4. And: `46e10c0f` is an AI re-render of the client's mark — is that dimensional-gold look approved as "the fish coloured in", or must the filled fish keep the client's exact silhouette?

## Assets still needed

| Asset | For beats | Model / source | Notes |
|---|---|---|---|
| Vector crest (AI/EPS/SVG) with three fish, wave rule, PASSALACQUA, LAGO DI COMO on separate paths | 1, 2, 3, 7 | client — ask first; trace by hand if it does not come | needed for the draw-on and the fill wipe; nothing on hand is above 410 px in the flat style |
| Three isolated gold fish on white with alpha, flat-on (matching the crest silhouette) and three-quarter | 3, 4, 5 | Flux (or a proper key of `46e10c0f`, which is already on clean white) | one file per fish |
| Clean lake + villa plate, no fish, 16:9, target 3840×2160 | 5, 6, 7 | Seedream | the on-hand plate has the fish baked in; ideally the real Passalacqua (OQ 1) |
| Kling clips: fill → alive (beats 3–4), drop-in (5), staggered leap with 12 % pull-back (6) | 3–6 | Kling, start/end keyframes from the frames above | prompts drafted in `theria_higgsfield_asset_pipeline_v1.md` §6 "Passalacqua" |
| `46e10c0f` / `b74514e7` at 4K | 3–7 | pipeline doc routes both to Seedream re-render (2.7× / 2.5×) | only needed if the plates survive into the final; if the clean plate and Flux fish are generated at 4K they replace both |
| Audio bed + three water-breaks + bell/strings | all | — | not boarded |

## What this board does not cover

- Aspect ratio: 16:9 assumed; the 1:1 and 9:16 crops are not checked (the crest at 2× sits inside the centre-80 % safe area, the leap does not).
- The draw-on itself (beat 1) and the fill wipe (beat 3) at frame level — both need the vector paths; the frames show start/mid states only.
- Splash / water-sheet simulation, the 240 fps retime at the apex, grade, and audio.
- Reconciling the page (12.5 s, 6 beats) with the timing doc (13.0 s, 7 beats) beyond the notes above — the board follows the timing doc.
- Whether the film loops (global rule) — depends on OQ 2.
- Kling's actual clip lengths / keyframe support; the two-frame split of beat 6 is a board convenience, not a cut.
- Any keying: the gold fish crops here are white-threshold alpha for layout only.
