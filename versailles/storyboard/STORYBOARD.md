# Airelles Le Grand Contrôle, Château de Versailles — storyboard v1

| | |
|---|---|
| Film | 04 — Airelles Le Grand Contrôle, Château de Versailles ("Let them eat cake") |
| Client / studio | Theria / Allen Grabo, RTFX Design |
| TRT | **15.0 s (f360)** per `theria_hotel_animations_timing_v1.md` §4, 8 shots |
| Frame rate | 24 fps |
| Master | 16:9, 1920×1080 (frames built at this size; deliverable master resolution still open per timing-doc global assumptions) |
| Frames | `frames/*.png` (1920×1080), `frames/*_small.jpg` (960×540), `frames/contact_sheet.jpg` — built by `build_frames.py PULL_ROOT OUT_DIR` |
| Board date | 2026-09-25 |

**Assumptions**

1. Boarded to the timing doc (15.0 s, 8 shots, black-field open, end card). Where the earlier storyboard page (TRT 14.0 s, 7 beats, white-field open, no end card) differs, it is called out in the row and in "Where the page differs" below.
2. **The asset descriptions in the timing doc (§4 asset list), the pipeline doc (§3 table) and this task's brief are wrong for four of the six Versali files.** Checked by eye; the board uses what is actually in the files:

| File | Actually contains | Docs say |
|---|---|---|
| `965d5f9a-d71a-4435-b487-cfabab3a0186.png` 1023×1537 RGB | cake on gilt table under the **guillotine, blade raised**, salon | cake + chandelier |
| `fd1e32ee-80ef-4d63-9d10-59e07f81e997.png` 1024×1536 RGB | cake on gilt table under the **chandelier**, salon (no alpha, not on black) | elements on black |
| `cfb72e66-8752-47fc-8f43-2f824eeb0f1d.png` 1024×1536 RGBA | cake + **chandelier**, isolated, real alpha (max 254 everywhere; bbox 783×1527 at x 227) | cake + guillotine |
| `4ad9ad80-ccba-4b14-8cd7-b85c4eb54f27.png` 1023×1537 RGB | **blade down** through the cake, slices already plated round the table | cake sliced, guillotine above |
| `images.jpg` 554×554 | **guillotine on white** (not the wordmark) | wordmark |
| `images copy.jpg` 447×447 | AIRELLES / LE GRAND CONTRÔLE / CHÂTEAU DE VERSAILLES wordmark, dark type on cream, JPG | wordmark |
| `cfb72e66-… (1).png` | byte-identical duplicate of `cfb72e66` (same md5) | — |

3. All three salon plates and the cut-out are portrait 2:3. They are letterboxed at full height, centred, pillars filled with a sampled-and-darkened wall colour — never stretched or cropped — and tagged **PORTRAIT PLATE — outpaint to 16:9 pending (Seedream 4.5)**. Shot 1 is an element on black, so its pillars are black by design.
4. The wordmark is a plain 2× Lanczos resize of the 447 px JPG, luma-keyed (dark type → gold-cream alpha) so it can sit on the parquet. Tagged placeholder; no AI enlargement. Vector art replaces it 1:1.
5. Exposure changes written in the timing doc ("light drops 1.5 stops") are approximated with a brightness multiply for the board; the real grade is AE.
6. Nobody in frame, ever. The blade only meets cake. No frame in this board shows or implies a figure.

---

## Beats

Frame numbers are `f###` at 24 fps from the timing doc. "Brief line" is the client brief line the beat serves.

| # | Brief line | IN – OUT (s) / frames | Frame | On screen | Motion / camera | Transition | Assets used | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | "Start with the cake on the table with the chandelier" | 00.0 – 02.2 / f0–53 (2.2 s) | `01_black_open.png` | Tiered blue cake on the gilt table, crystal chandelier directly above, everything else black | Locked off, 1 % push-in. Candle flames flicker; slow crystal caustics across the icing. Chandelier may sway 1.5° on a slow sine (page note) | — | `cfb72e66-8752-47fc-8f43-2f824eeb0f1d.png` (RGBA cut-out on black) | **READY** as a still. Micro-motion = Kling O1 (image-to-video, "cake does not move") or AE flicker/caustic layers. Page says **white** field; doc says black — see Q1 |
| 2a | "The background appears with the lavish finishing in the background" | 02.2 – ~03.6 / f53–86 (mid-reveal) | `02a_salon_reveal.png` | The salon fading up from black, outward from the cake; walls and parquet still dark at the edges | Radial reveal ~1.4 s from centre. Warm afternoon shaft lands across the floor last. Page: three passes floor / walls / light 400 ms apart, cast shadows last | reveal (from black) | `fd1e32ee-80ef-4d63-9d10-59e07f81e997.png` under a radial luma mask | **COMP (AE)** — luma-matte reveal over the plate. Alt: Kling O1 Shot 2 prompt (pipeline §6) with `01` and `02b` as start/end frames |
| 2b | same | 02.2 – 04.4 / f53–106 (end state) | `02b_salon.png` | The salon whole: boiserie, gilding, drapes, window light, cake centre, chandelier above | Hold. Camera locked | — | `fd1e32ee-80ef-4d63-9d10-59e07f81e997.png` | **READY** plate. Portrait — outpaint to 16:9 (Seedream 4.5) |
| 3 | "The logo for the hotel appears under the table" | 04.4 – 06.2 / f106–149 (1.8 s) | `03_wordmark.png` | AIRELLES lockup on the parquet between the table's front feet | Wordmark fade 0.7 s, hold 1.1 s. Page wants it gold, inlaid, perspective-matched to the floor plane; doc reads screen-flat | — | `fd1e32ee-…png` + `images copy.jpg` (2× Lanczos, luma-keyed placeholder) | **COMP (AE)** logo layer over the plate. Wordmark **placeholder until vector**. Clear parquet under this table is only ~260 px wide at 1080p — see Q3 |
| 4 | "The chandelier turns into a guillotine" | 06.2 – 08.8 / f149–211 (2.6 s) | `04_morph_COMP.png` | Mid-morph: the chandelier half-become guillotine; wordmark still on the floor; room ~¾ stop down | Morph, not cut: crystals darken and elongate into timber uprights f149–180; central boss stretches into the blade f170–200; rope and pulley draw on last f195–211. Room light drops 1.5 stops across the shot. Cake oblivious. Page: 2.4 s ease-in-out, keep the chain as the hoist rope, light cools 400 K | — | 50 % blend of `fd1e32ee-…png` and `965d5f9a-…png`, `images copy.jpg` | **COMP (AE)** — pipeline §7: never a video model. **The two salon plates do not register** (doors, panels and window ghost in the blend; cake sits at slightly different positions) — see Q2. The blend is shown honestly, not aligned |
| 5 | "The logo disappears" | 08.8 – 09.8 / f211–235 (1.0 s) | `05_still.png` | Guillotine raised over the cake, dark room, no logo. Total stillness f223–235 | Wordmark opacity → 0 over 0.5 s, then 12 frames of nothing. Quartet stops dead at 09.8. Page adds "the blade rises the last few inches" and one rope creak | — | `965d5f9a-d71a-4435-b487-cfabab3a0186.png` | **READY** plate (shown at −1.0 stop so the board reads; doc grade is −1.5). Logo fade + grade = AE |
| 6 | "The guillotine comes down fast and cuts the cake" | 09.8 – 10.6 / f235–254 (0.8 s) | `06_drop_COMP.png` | Impact frame: blade through all three tiers, 3-frame white flash, frame kicked 4 px | 2 frames pre-shake f235, blade falls in **8 frames** f238–246, white flash-frame f246, camera shake 4 px settling by f254. Page: 4 frames of blade, motion-blurred, crumb/sugar-dust on the second frame after contact, no gore physics | hard | `4ad9ad80-ccba-4b14-8cd7-b85c4eb54f27.png` at −1.5 stop, +4/−3 px offset, 35 % white | **COMP (AE)** — blade is a layer moved 8 frames. Pipeline §6 also lists a Kling prompt for this shot but §7 warns "blade falling" may trip filters; board it as comp. **Caveat:** the only blade-down plate already has the plated slices around the table (Shot 7's end state) — a clean "blade through cake, no plates" frame does not exist. See Assets still needed |
| 7 | "The cake it cut up into many pieces" | 10.6 – 13.6 / f254–326 (3.0 s) | `07_served.png` | Cake parted under the blade, slices on porcelain ringing the table; light back up 1 stop | 0.6 s of the cake falling into slices, then portions slide out to their plate positions and settle. Page: plates pop in on 3-frame intervals in a spiral, "sixteen ways". Quartet back at 11.2 as if nothing happened | — | `4ad9ad80-ccba-4b14-8cd7-b85c4eb54f27.png` at −0.5 stop | **READY** plate as end state. Slice travel = **TO GENERATE (Kling O1**, pipeline §6 Shot 7 prompt, start `06` end `07`) or AE cut-outs sliding. Portrait — outpaint pending |
| 8 | — (timing-doc addition, not in brief) | 13.6 – 15.0 / f326–360 (1.4 s) | `08_endcard.png` | Hall of Mirrors wide, darkened; wordmark centre | Pull back / cross-dissolve from the salon to the hall; wordmark fades up centre | dissolve in; fade to black f360 | `1651551468329.webp` (cover-fit 1.64×), `images copy.jpg` (placeholder) | **READY** as a still but soft: 1170 px source at 1920 (Seedream re-render pending). Page has **no end card** — it whips back to white and loops. See Q1 |

### Where the earlier storyboard page differs from the timing doc (page text in `inventory/storyboards_rendered_text_2026-09-25.txt`, "04 AIRELLES")

| | Page (TRT 14.0 s, 7 beats) | Timing doc (15.0 s, 8 shots) — boarded |
|---|---|---|
| Open field | white | **black** |
| Beat times | 0–2 / 2–4 / 4–6 / 6–9 / 9–10.5 / 10.5–11.2 / 11.2–14 | 0–2.2 / 2.2–4.4 / 4.4–6.2 / 6.2–8.8 / 8.8–9.8 / 9.8–10.6 / 10.6–13.6 / 13.6–15 |
| Morph | 2.4 s, light cools 400 K, chain becomes hoist rope | 2.6 s, light drops 1.5 stops |
| Tension beat | includes "blade rises the last few inches" + one rope creak | pure stillness; audio stops dead |
| Drop | 4 frames of blade, dust burst | 8 frames, pre-shake, white flash-frame, 4 px camera shake |
| Payoff | spiral plating on 3-frame intervals, "sixteen ways", whip back to white, loops | slices slide to plates, light up 1 stop, then Hall of Mirrors end card |
| Music | harpsichord, keeps playing through the drop | string quartet, stops dead at 09.8, returns 11.2 |
| Logo | gold, inlaid into the floor, perspective-matched | set in the clear parquet below the table legs |

---

## Open questions for Allen

1. **Black or white field, and does it loop?** Doc opens on black and ends on a Hall of Mirrors card; the page opens on white and whips back to white so it loops (the global rule says each film ends on its own opening frame). The `cfb72e66` cut-out works on either. Pick one — it changes Shots 1, 2 and 8.
2. **The two salon plates do not register** (see `04_morph_COMP.png`: doors, panelling and window ghost; the cake shifts). Outpainting three mismatched plates will not fix this. Recommend the page's own TO SOURCE route: one clean empty salon plate (Seedream 4.5, 16:9, no cake, no chandelier), then cake, chandelier and guillotine as separate layers held in one position across Shots 2–7. That also makes the morph, the logo, the blade drop and the plating all AE layer work on a single background. OK to go that way?
3. **Wordmark placement.** In the portrait plate the clear parquet between the front feet is ~260 px at 1080p, so the lockup is small (`03_wordmark.png`). Either the outpaint/clean plate gives more floor below the table, or the lockup sits in front of the feet / on the apron. Also: screen-flat fade (doc) or gold floor inlay in perspective (page)?
4. **Blade drop: 8 frames + flash frame (doc) or 4 frames + dust (page)?** And confirm the drop is AE (a blade layer moved down) rather than the Kling Shot 6 segment listed in pipeline §6 — §7 of the same doc expects that prompt to be refused.
5. **Shot 7 payoff:** is `4ad9ad80` (blade already down, slices already ringing the table, more like 12 slices than the page's sixteen) the accepted end state, and do the slices travel by Kling (pipeline §6 prompt) or as AE cut-outs?

## Assets still needed

- **Vector wordmark** (AI/EPS/SVG/PDF) — the only logo file is a 447 px JPG on cream; the board's 2× placeholder is tagged on every frame it appears.
- **Clean empty salon plate**, 16:9, no cake, no chandelier, no guillotine (Seedream 4.5, ≥3840 wide) — the page's TO SOURCE item; needed if Q2 goes the layered route, and it makes the three portrait outpaints unnecessary.
- Otherwise: **16:9 outpaints of `fd1e32ee`, `965d5f9a`, `4ad9ad80`** from one reference, same seed (pipeline §3). They must also be brought into register with each other, which the outpaint alone will not do.
- **Isolated guillotine with alpha** at plate scale — `images.jpg` is a 554 px guillotine on white (too small, different model); Flux 2.0 Pro per pipeline §3, or key it out of `965d5f9a` (rope and open timber will be fiddly).
- **Isolated cake alone and chandelier alone** — `cfb72e66` has both in one alpha; they do not overlap, so a horizontal split above the cake's finial separates them for free. Note in the file, not yet done.
- **Blade-through-cake frame with no plated slices** (Shot 6 impact, Shot 7 start) — does not exist; generate (Seedream / NBP from `4ad9ad80` with plates removed) or build in AE from the cake cut-out.
- **Hall of Mirrors at master resolution** — the webp is 1170×780 with a timestamp filename; confirm it is licensed or re-render (Seedream). Only needed if the end card survives Q1.
- **Audio**: period string quartet bed (or harpsichord, per Q1/page), rope-and-timber creak, blade whoosh, impact thud.

## What this board does not cover

- In-between motion: candle flicker, caustics, the morph itself, the blade travel, slice travel — every frame here is a keyframe or a tagged stand-in, per the stills → animated segments approach.
- The morph design (which crystal becomes which upright, where the chain becomes rope) — that is an AE animatic, not a board.
- Colour grade, the 1.5-stop / 1-stop light changes (approximated), and the 400 K cool-down.
- Audio timing beyond what the timing doc states.
- 1:1 and 9:16 crops (logo-safe centre 80 % rule not checked on these portrait plates).
- The loop point, until Q1 is answered.
- Kling prompt wording — taken as given from pipeline §6 and not tested; no generation was run (no network).
- Anything under the pull directory was read only; nothing there was modified, including the duplicate `cfb72e66 (1).png`.
