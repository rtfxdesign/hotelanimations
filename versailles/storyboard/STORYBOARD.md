# Airelles Le Grand Contrôle, Château de Versailles — storyboard v2

| | |
|---|---|
| Film | 04 — Airelles Le Grand Contrôle, Château de Versailles ("Let them eat cake") |
| Client / studio | Theria / Allen Grabo, RTFX Design |
| TRT | **15.6 s (f374)** — timing-doc beats 1–7 unchanged (0–13.6 s); the 1.4 s Hall of Mirrors end card is replaced by a 2.0 s return-to-frame-0 beat (13.6–15.6 s) |
| Frame rate | 24 fps |
| Master | one master, 16:9, 1920×1080 |
| Loop | **final frame f374 = frame 0.** `build_frames.py` asserts `01_black_open` and `09_loop` are pixel-identical below the tag band |
| Frames | `frames/*.png` (1920×1080), `frames/*_small.jpg` (960×540), `frames/contact_sheet.jpg` — built by `build_frames.py PULL_ROOT OUT_DIR` |
| Board date | 2026-09-25 (v2; v1 same day) |

## Decisions taken

Allen's decisions, applied as given:

1. **One master 16:9 1920×1080, 24 fps.** v1 shot timings kept; the film is extended only by what the loop needs (see 5).
2. **Black field for the open and the close.** The page's white field is dropped. Shot 1 is the `cfb72e66` cut-out on black; the film returns to that exact frame.
3. **The film loops — last frame = first frame.** The Hall of Mirrors end card (v1 `08_endcard`, timing-doc Shot 8) is gone; `1651551468329.webp` is no longer used. After the plated slices, the salon fades to black inward from the edges, the slices slide back into the whole cake and the guillotine dissolves back into the chandelier, landing on frame 0.
4. **Wordmark stays raster.** The 2× Lanczos, luma-keyed enlargement of `images copy.jpg` is the approved production asset — tagged "raster, approved" on the frames. No vector is coming and none is requested.
5. **Production plan = one clean 16:9 salon plate + layered objects** (cake, chandelier, guillotine, table, slices held in one position across Shots 2–8), per the v1 review note. This is stated in the beat table's Status column. The board frames themselves stay on the v1 plates (`fd1e32ee`, `965d5f9a`, `cfb72e66`, `4ad9ad80`) — they are the look reference for the rebuild, not the comp sources.

Judgement calls made on this board (not put back to the client):

6. **Blade drop = 8 frames + flash (timing doc)**, not the page's 4 frames + dust: 2 f pre-shake at f235, blade f238–246, 3-frame white flash on f246, 4 px camera shake settling by f254. The blade is an AE layer moved down over the clean salon — no video model for this shot (pipeline §7 expects the Kling prompt to be refused).
7. **Chandelier → guillotine morph is an AE comp** (Shot 4), never a video model. Crystals darken and elongate into uprights f149–180, boss stretches into the blade f170–200, rope and pulley draw on f195–211. Light drops 1.5 stops across the shot.
8. **The return beat is 2.0 s (13.6–15.6 s, f326–374), TRT 15.6 s.** The 1.4 s the end card had is too short for three overlapping actions after a 3.0 s plating beat: salon-to-black 1.0 s, slices back 1.0 s, guillotine→chandelier 0.8 s, then a 4-frame hold on frame 0 so the join is dead still. Nothing before 13.6 s moves.
9. **The return is the payoff run backwards, not a new idea.** Slices retrace their Shot 7 paths at 2× speed and the plates fade out as each portion arrives; the cut heals as the last slice lands; the guillotine fades and the chandelier fades up in its place (a dissolve, not a reverse morph — the room is already black, so the uprights just go). Quartet fades under the return; silence at the join.
10. **Shot 1 micro-motion (candle flicker, caustics, 1 % push-in) is AE layer work on the still, not Kling.** That keeps f0 pixel-exact to the still, so f374 can equal it. Kling O1 stays an option for Shot 2 (reveal) and Shot 7 (slice travel) only, where neither end has to match a loop frame.

Notes on the files (unchanged from v1 — the timing doc §4 list, pipeline doc §3 and the original brief describe four of the six Versali files wrong; the board uses what is in them):

| File | Actually contains |
|---|---|
| `965d5f9a-…png` 1023×1537 RGB | cake on gilt table under the **guillotine, blade raised**, salon |
| `fd1e32ee-…png` 1024×1536 RGB | cake on gilt table under the **chandelier**, salon |
| `cfb72e66-…png` 1024×1536 RGBA | cake + **chandelier**, isolated, real alpha (bbox 783×1527 at x 227); `(1).png` is a byte-identical duplicate |
| `4ad9ad80-…png` 1023×1537 RGB | **blade down** through the cake, slices already plated round the table |
| `images copy.jpg` 447×447 | the AIRELLES / LE GRAND CONTRÔLE / CHÂTEAU DE VERSAILLES wordmark (dark on cream) |
| `images.jpg` 554×554 | guillotine on white — not the wordmark |
| `1651551468329.webp` 1170×780 | Hall of Mirrors — no longer used |

All hero plates are portrait 2:3, letterboxed at full height on a sampled-and-darkened wall colour, never stretched or cropped. Exposure changes are approximated with a brightness multiply; the real grade is AE. Nobody in frame, ever; the blade only meets cake.

---

## Beats

Frame numbers are `f###` at 24 fps. "Brief line" is the client brief line the beat serves.

| # | Brief line | IN – OUT (s) / frames | Frame | On screen | Motion / camera | Transition | Assets used | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | "Start with the cake on the table with the chandelier" | 00.0 – 02.2 / f0–53 (2.2 s) | `01_black_open.png` | Tiered blue cake on the gilt table, crystal chandelier directly above, everything else black. **This is frame 0 and the loop frame** | Locked off, 1 % push-in. Candle flames flicker; slow crystal caustics across the icing; chandelier may sway 1.5° on a slow sine | — | `cfb72e66-…png` (RGBA cut-out on black) | **READY.** Micro-motion = AE layers on the still (decision 10), so f0 stays exact. In the production build the same cut-out is the cake+chandelier layer for Shots 2–8 |
| 2a | "The background appears with the lavish finishing in the background" | 02.2 – ~03.6 / f53–86 (mid-reveal) | `02a_salon_reveal.png` | The salon fading up from black, outward from the cake; walls and parquet still dark at the edges | Radial reveal ~1.4 s from centre; three passes floor / walls / light ~400 ms apart; warm afternoon shaft lands across the floor last | reveal (from black) | `fd1e32ee-…png` under a radial luma mask | **COMP (AE)** — luma-matte reveal of the **clean salon plate** behind the held cake layer. Alt: Kling O1 Shot 2 prompt with `01` and `02b` as start/end frames |
| 2b | same | 02.2 – 04.4 / f53–106 (end state) | `02b_salon.png` | The salon whole: boiserie, gilding, drapes, window light, cake centre, chandelier above | Hold. Camera locked | — | `fd1e32ee-…png` | **READY as look reference.** Production = clean 16:9 salon plate (TO GENERATE, Seedream 4.5) + cake/chandelier layer; `fd1e32ee` is the reference image for that generation, not a comp source |
| 3 | "The logo for the hotel appears under the table" | 04.4 – 06.2 / f106–149 (1.8 s) | `03_wordmark.png` | AIRELLES lockup on the parquet between the table's front feet | Wordmark fade 0.7 s, hold 1.1 s. Screen-flat fade (timing doc); gold-cream so it reads on the parquet | — | `fd1e32ee-…png` + `images copy.jpg` (2× Lanczos, luma-keyed) | **COMP (AE)** — wordmark layer over the clean salon. Wordmark **raster, approved**. On the clean-salon build the table is a layer, so the floor clearance under it is set at build time; board it at 240 px wide as here |
| 4 | "The chandelier turns into a guillotine" | 06.2 – 08.8 / f149–211 (2.6 s) | `04_morph_COMP.png` | Mid-morph: the chandelier half-become guillotine; wordmark still on the floor; room ~¾ stop down | Morph, not cut (decision 7): crystals → uprights f149–180; boss → blade f170–200; rope and pulley draw on f195–211. Light drops 1.5 stops across the shot; the cake is oblivious | — | 50 % blend of `fd1e32ee-…png` and `965d5f9a-…png`, `images copy.jpg` | **COMP (AE), never a video model.** The blend ghosts because the two plates do not register — irrelevant in production, where the chandelier and guillotine are two layers over one clean salon and the morph is between those two layers |
| 5 | "The logo disappears" | 08.8 – 09.8 / f211–235 (1.0 s) | `05_still.png` | Guillotine raised over the cake, dark room, no logo. Total stillness f223–235 | Wordmark opacity → 0 over 0.5 s, then 12 frames of nothing. Quartet stops dead at 09.8 | — | `965d5f9a-…png` | **READY as look reference** (shown −1.0 stop; doc grade is −1.5). Production = clean salon + guillotine layer (isolated guillotine TO GENERATE, see Assets) + logo fade in AE |
| 6 | "The guillotine comes down fast and cuts the cake" | 09.8 – 10.6 / f235–254 (0.8 s) | `06_drop_COMP.png` | Impact frame: blade through all three tiers, 3-frame white flash, frame kicked 4 px | **8-frame drop + flash (decision 6):** pre-shake f235, blade f238–246, flash f246, 4 px shake settling by f254. No dust burst, no gore physics | hard | `4ad9ad80-…png` at −1.5 stop, +4/−3 px offset, 35 % white | **COMP (AE)** — blade is a layer moved 8 frames over the clean salon. Impact state needs a blade-through-cake element without plates (see Assets); `4ad9ad80` stands in on the board |
| 7 | "The cake it cut up into many pieces" | 10.6 – 13.6 / f254–326 (3.0 s) | `07_served.png` | Cake parted under the blade, slices on porcelain ringing the table; light back up 1 stop | 0.6 s of the cake falling into slices, then portions slide out to their plate positions and settle. Quartet back at 11.2 as if nothing happened | — | `4ad9ad80-…png` at −0.5 stop | **READY as end-state reference.** Slice travel = Kling O1 (pipeline §6 Shot 7 prompt, start `06` end `07`) or AE cut-outs sliding over the clean salon. Whichever is used, the end positions are keyed so Shot 8 can run them back |
| 8 | — (loop rule, replaces the timing-doc end card) | 13.6 – 15.6 / f326–374 (2.0 s) | `08_return_COMP.png` | Mid-return (~f350): the salon black at the edges and closing in, only the table still lit; slices trailing back toward the cake; the chandelier ghosting in over the guillotine; the cut cake starting to heal | **The return (decisions 8–9):** salon fades to black inward from the edges f326–350 (reverse of Shot 2); slices retrace their Shot 7 paths at 2× speed f338–362, plates fading as each portion lands, cut heals on the last; guillotine → chandelier dissolve f350–370, cake light back to Shot 1 level; hold f370–374. Quartet fades out under it; silence at the join | fade to black around the table; **loop** | `4ad9ad80-…png` (−0.5 stop, radial mask to black, slice bands smeared inward) + `cfb72e66-…png` ghosted at 50 % / 18 % | **COMP (AE)** — layer work on the clean salon: salon layer fades, slice cut-outs run backwards, guillotine layer out / chandelier layer in. The board frame is an honest composite of two plates that do not register (table ~15 % larger in `4ad9ad80`) — see Flagged risks |
| 9 | (loop point) | 15.4 – 15.6 / f370–374 (4 f hold, inside Shot 8) | `09_loop.png` | Identical to frame 0 | Dead still. **Final frame f374 = frame 0** | loop → Shot 1 | `cfb72e66-…png` | **READY** — same pixels as `01_black_open` (asserted by the build) |

---

## Flagged risks (with decisions)

1. **`4ad9ad80` and `cfb72e66` do not register**, so the return cannot be a dissolve between the two plates — the table is ~15 % larger and lower in the plated plate and the cake sits at a different scale (`08_return_COMP` shows the honest blend; compare the two table edges). **Decision:** the return, like Shots 2–7, is built on the clean-salon layer stack, where the cake, table and chandelier cut-outs never move; the slices are cut-outs keyed from the Shot 7 end positions and run back. The plated plate is a look reference only. No outpaint of `4ad9ad80` is ordered.
2. **The loop join depends on f0 and f374 being the same pixels, but Shot 1 has micro-motion** (flicker, caustics, 1 % push-in). If Shot 1 came out of Kling its first frame would drift from the still and the join would pop. **Decision:** Shot 1 micro-motion is AE layers on the `cfb72e66` still, the push-in is a scale keyframe that resets at the join (1 % over 2.2 s reads as a breath, not a jump), and the flicker/caustic layers are seeded to start at zero. The build already asserts the two board frames match; the AE comp should be checked the same way (difference matte on f0 vs f374).

---

## Assets still needed

- **Clean empty salon plate**, 16:9, ≥ 3840 wide, no cake, no chandelier, no guillotine (Seedream 4.5, `fd1e32ee` as the reference) — the background for every shot from 2a to 8. This replaces the three portrait outpaints v1 listed; none is now needed.
- **Isolated guillotine with alpha** at plate scale, matching the model in `965d5f9a` — Flux 2.0 Pro per pipeline §3, or keyed out of `965d5f9a` (rope and open timber will be fiddly). Blade must be a separate layer, or separable, for the 8-frame drop.
- **Isolated cake alone and chandelier alone** — `cfb72e66` has both in one alpha; they do not overlap, so a horizontal split above the cake's finial separates them for free. Not yet done.
- **Blade-through-cake element with no plated slices** (Shot 6 impact, Shot 7 start, Shot 8 end of the heal) — does not exist; generate from `4ad9ad80` with plates removed (Seedream / NBP) or build in AE from the cake cut-out.
- **Slice cut-outs** (12 portions on porcelain) keyed from `4ad9ad80`, or generated as one element set — needed for Shot 7 travel if done in AE, and for Shot 8's return either way (a Kling Shot 7 does not give reversible layers).
- **Audio**: period string quartet bed, rope-and-timber creak, blade whoosh, impact thud; quartet out under the return.
- Nothing further for the wordmark (raster approved) and nothing for the Hall of Mirrors (end card dropped).

## What this board does not cover

- In-between motion: candle flicker, caustics, the morph itself, the blade travel, slice travel out and back — every frame here is a keyframe or a tagged stand-in.
- The morph design (which crystal becomes which upright, where the chain becomes rope) — AE animatic, not board.
- Colour grade, the 1.5-stop / 1-stop light changes (approximated), and any cool-down of the light through Shots 4–5.
- Audio timing beyond what the timing doc states and the fade under the return.
- 1:1 and 9:16 crops — one 16:9 master only, per Allen.
- The generation of the clean salon plate and the isolated elements listed above — no generation was run.
- Anything under the pull directory was read only; nothing there was modified, including the duplicate `cfb72e66 (1).png`.
