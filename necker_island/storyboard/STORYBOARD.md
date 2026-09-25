# Necker Island, BVI — storyboard v1 (2026-09-25)

**Film 07 of 8** · client Theria · Allen Grabo / RTFX Design
**TRT 14.0 s (f336) @ 24 fps · 16:9 · 1920×1080 master** · 6 shots + 1 fallback frame
Frames: `necker_island/storyboard/frames/` (PNG 1920×1080, `*_small.jpg` 960×540, `contact_sheet.jpg`).
Build: `python3 necker_island/storyboard/build_frames.py PULL_ROOT OUT_DIR`

**Source of truth for beats:** the client brief (flamingo → takes flight → zoom out to island with kite-surfer → lemurs playing tennis). Cuts are boarded to `theria_hotel_animations_timing_v1.md` §7 (14.0 s). The earlier storyboard page ("07 NECKER ISLAND", TRT 13.0 s) is noted per beat where it differs.

**Assumptions**
- This is the flamingo concept from the brief. `Animation Virgin.docx` in the same folder is a **different film** (hand-drawn Virgin logo, red line through the decades, parachute drop onto Necker) and is **not boarded here** — see open question 1.
- The only usable art in the pull is the Virgin script mark (`07D6D2DD-….jpg`, 1320×1240, red on white, no alpha). Every other frame is a **Pillow-drawn schematic placeholder**: pale sky field, thirds grid, simple silhouettes and labelled boxes giving position and screen fraction. Nothing in these frames is a look reference — they are layout guides for the generation pass.
- Generation prompts for the four missing elements are already written in `theria_higgsfield_asset_pipeline_v1.md` §5.3 and are referenced by name, not rewritten. Kling motion prompts per shot are in the same doc §6 "Necker Island".
- Casting rule (brief + both docs): the kite-surfer is a **generic blonde man, small in frame, back to camera, no facial detail** — never a likeness of a named person. No real person's name goes into any prompt.
- Lemur stand-ins in S5 are the Miavana cut-outs `Miavana/upscaled/lemur2.png` and `lemur3.png` (RGBA, ~1050×2700), Lanczos-resized only. They are the wrong pose and hold nothing; they are there for species/scale and to remind that S5 must match Miavana's lemurs.
- Mark on the end card: plain Lanczos downscale of the 1320 px jpg with alpha lifted from luminance. Not AI-enlarged. Placeholder until the correct lock-up arrives; logo fade is an AE layer over the plate, never baked into a generation (pipeline doc §4).
- Frames show the *end state* of each shot unless noted.

## Beats

| # | Brief line served | IN–OUT (s) / frames @24 | Frame | On screen | Motion / camera | Transition | Assets used | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | "Art is a flamingo" | 00.0–02.4 · f0–58 (2.4 s) | `01_flamingo_hold_TOGEN.png` | Single flamingo standing on one leg, full profile, ≈70 % frame height, just left of centre, isolated on white / pale sky. Same open-on-white grammar as Films 01, 02, 05. | Locked off. Head preens at f20, settles f38. Nothing else moves. | — | none (schematic silhouette) | **TO GENERATE — Flux 2.0 Pro** "Flamingo, isolated" (§5.3). Motion: Kling Necker shot 1. *Page: 0:00–0:02, same beat.* |
| 2 | "The flamingo takes flight" | 02.4–04.6 · f58–110 (2.2 s) | `02_takeoff_TOGEN.png` | Takeoff: wings extended, body angled up and forward, climbing toward frame right; wings ≈ full frame width by the last beat. Still on the pale field — no background yet. | Crouch f58–66, first downstroke f68, three full wingbeats to f110. Camera tilts up with it, lagging slightly. | — | none (schematic silhouette) | **TO GENERATE — Flux pose 1 → Nano Banana Pro pose 2** (same bird, §5.3 "second pass"). Motion: Kling Necker shot 2. *Page: 0:02–0:04.5, "runs three steps"; timing doc has a crouch instead — boarded to the crouch.* |
| 3 | "It zooms out as an island comes into view" | 04.6–07.4 · f110–178 (2.8 s) | `03_pullback_island_TOGEN.png` | Flamingo now ≈8 % frame height, upper third, upper-right, still flying. Sea has filled in from the edges; island resolves centre in aerial three-quarter view (not top-down): white sand ring, palm interior, villa scatter, boats. | One continuous zoom-out, no cut. | — | none (schematic island plate) | **TO GENERATE — Seedream 4.5** "Island aerial" (§5.3). Motion: Kling Necker shot 3. *Page: 0:04.5–0:07, "bird holds screen-left third throughout" — timing doc sends it right in S2 and back left in S4, so boarded upper-right here.* |
| 4 | "…with Richard Branson kite surfing (change in the photo to a blonde man)" | 07.4–10.2 · f178–245 (2.8 s) | `04_kitesurfer_TOGEN.png` | Camera settled on the island wide. Kite-surfer crosses the bay **left → right in the lower third**: blonde, small, back to camera, board throwing spray, kite arcing above and behind. Flamingo crosses the **upper third right → left**. The two crossing paths are the composition. | Locked off; only the two subjects move. | — | none (schematic figure + kite) | **TO GENERATE — Seedream 4.5** "Kite-surfer" (§5.3). Motion: Kling Necker shot 4. Casting rule applies: generic blonde man, no likeness, no face. *Page: 0:07–0:09.5, rider "jumps"; timing doc is a straight crossing — boarded straight.* |
| 5 | "And Lemurs are playing Tennis with each other" | 10.2–13.0 · f245–312 (2.8 s) | `05_lemur_tennis_TOGEN.png` | Push in on the island's grass court. Two ring-tailed lemurs, one each side, rackets in hand, mid-rally. Palms and turquoise sea behind. Play it straight — proper form, no cartoon takes, no clothing. | Push in. Three hits at **10.8 / 11.6 / 12.4 s**, ball travel ≈14 frames per exchange. Rally audio arrives one beat before the court enters frame (page note, kept). | — | `Miavana/upscaled/lemur2.png`, `lemur3.png` as tagged stand-ins (wrong pose) | **TO GENERATE — Seedream 4.5, then Nano Banana Pro with the Miavana lemur references** so the coat matches Film 06 (§5.3). Motion: Kling Necker shot 5 — highest-risk generation in the reel. *Page: 0:09.5–0:11.5, same beat, 2.0 s.* |
| 5b | (fallback for 5) | 10.2–13.0 · f245–312 | `05b_tennis_AE_fallback.png` | Same court; ball on a 14-frame arc; plates swap on each hit (A ready / B follow-through). | Two static Seedream plates, ball keyed in After Effects, cut on each hit. | — | as above | **FALLBACK** per pipeline doc §6 ("board a fallback"). Only used if Kling cannot hold rackets. |
| 6 | (sign-off) | 13.0–14.0 · f312–336 (1.0 s) | `06_endcard.png` | Pull back out to the island wide, field whites out ≈70 %, Necker / Virgin lock-up fades up centre (≈27 % frame width). | Pull-back then hold; lock-up fade is an AE layer. | fade to out at 14.0 | `Necker Island/07D6D2DD-….jpg` Virgin mark, Lanczos resize only | Mark is a **placeholder** — confirm Necker lockup vs Virgin Limited Edition (open question 2). *Page: 0:11.5–0:13 (1.5 s), "flamingo drops out bottom-left, island holds a half-beat, whites out"; timing doc gives 1.0 s and a pull-back — boarded to the timing doc, flamingo exit not shown.* |

**Audio (timing doc):** wing beats close then distant, wind and water, three tennis pocks. No music until the end card.

**Page vs timing doc, summary:** page TRT 13.0 s → timing doc 14.0 s (S2 +0.1, S3 +0.3, S4 +0.3, S5 +0.8, S6 −0.5). Beat order and content are the same; the differences are S2 "runs three steps" vs crouch, S4 rider "jumps" vs straight crossing, S3 bird screen-left vs right, and S6 whiteout-only vs pull-back + fade. Timing doc wins per the handoff.

## Open questions for Allen

1. **Which Necker concept is live?** The brief (flamingo → island → kite-surfer → lemur tennis, boarded here) or `Animation Virgin.docx` (hand-drawn Virgin logo / red line through the decades / parachute onto Necker). They are different films; only the flamingo one is boarded.
2. **Which mark signs off** — a Necker Island lock-up, or Virgin Limited Edition? Only the plain Virgin script (jpg, no alpha) was supplied; the end card uses it as a placeholder.
3. **Are the timing-doc cuts still the source of truth** (14.0 s) over the storyboard page (13.0 s)? Boarded to 14.0; the four content differences are listed above.
4. **S5 tennis: generate it in Kling, or go straight to the comp fallback** (two static plates + AE ball)? The pipeline doc calls it the highest-risk generation in the reel; the fallback costs less than three Kling attempts.
5. **Flamingo path across S2–S4:** timing doc sends it right in S2 then back right-to-left in S4; the page holds it screen-left throughout. Confirm the crossing-paths version (boarded).

## Assets still needed

- Flamingo, standing, isolated on white (Flux 2.0 Pro, §5.3) — plus takeoff pose, same bird (NBP referencing pose 1).
- Necker aerial plate, three-quarter view, ~300 m (Seedream 4.5, §5.3). If a real Necker aerial exists client-side it beats a generated island — the page mentions "Great House on the ridge, reef line, sailboats".
- Kite-surfer plate, generic blonde man, back to camera (Seedream 4.5, §5.3).
- Two lemurs playing tennis (Seedream 4.5 → NBP with Miavana refs, §5.3); for the fallback, two separate static plates (ready / follow-through).
- Kling segments for shots 1–5 (pipeline doc §6, Necker table).
- Correct end-card mark as vector or transparent PNG (Necker lock-up or Virgin Limited Edition).
- Audio: wingbeats, wind/water bed, three tennis pocks, end-card music sting.

## What this board does not cover

- No look, colour or lighting reference — every frame except the mark is a schematic. Do not show these to the client as visuals.
- The flamingo's exit is not boarded (page has it leaving bottom-left before the end card; timing doc does not mention it).
- Not boarded: the second concept in `Animation Virgin.docx`. Not read: the five speech/itinerary/questions docx files and the two PDFs (schedule, 62 MB summit deck) — they look unrelated to the animation, as the inventory already noted.
- No in-between frames for S2's three wingbeats or S5's three hits; only end states plus the hit times.
- No AE comp, no Kling runs, no generated art — nothing here touches the pull directory or any model.
