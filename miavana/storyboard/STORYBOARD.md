# MIAVANA — storyboard v1

| | |
|---|---|
| Film | 06 Miavana, Nosy Ankao, Madagascar (client: Theria; hotel group Time+Tide) |
| TRT | 12.0 s = 288 frames @ 24 fps (timing doc `theria_hotel_animations_timing_v1.md` §6) |
| Master | 16:9, 1920×1080, sage brand ground RGB 157/200/183 (sampled from the PSD background layer) |
| Frames | `miavana/storyboard/frames/` — one PNG per beat + `*_small.jpg` (960×540) + `contact_sheet.jpg`; rebuilt by `build_frames.py PULL_ROOT OUT_DIR` |
| Brief | "Start with the logo with the lemurs (better positions). Have the last one holding a mango throwing it to the other lemur. The hotel appears in the background and the lemurs are in the palm trees. Hotel disappears back to the logo and lemurs in places." |

**Assumptions**

- The lock-up is rebuilt from the PSD layer exports (`Miavana/upscaled/miavana_*.png`) placed by the bboxes in `inventory/psd_layers_2026-09-25.md`, scaled 2508→1920 (×0.7655). Nothing in the wordmark has been redrawn, re-kerned or AI-enlarged; the PSD is used **as-is** — seated lemur on the **M**, hanging lemur on the **final A**. The timing doc's "seated lemur on the first A" is shown once as an ALT frame, not adopted (see open question 1).
- "The last one" in the brief = the hanging lemur on the final A; it throws **right-to-left** to the seated lemur. Both the timing doc and the earlier storyboard page agree on this direction.
- Mango: no prop exists in the pull. The frames use a colour-keyed crop of one frame (`-ss 2.0`) of the Kling clip `a ring-tailed lemur produces a mango, throws it up and to the right.mp4` (720×1280), down-scaled to ~84 px. It is a placeholder for a Flux-generated prop; the clip proves the throw motion but is below HD.
- Resort plate: `resort.png` (3600×4802, 2× upscale of `Miavana_©_Dylane_Cabano_001-scaled.jpg`) is **portrait**. The board covers 16:9 with a crop centred at 62 % of the plate's height (villas, pools, palm band, beach edge); ~58 % of the plate's height is discarded. Outpaint vs. crop is not decided here.
- The PSD lemurs are ~480 px / ~460 px tall at HD (soft, from the 1254 px source). The palms beat uses the large cut-outs `lemur.png` (seated) and `Firefly_remove background 477817 (1).png` (hanging) scaled **down** to the same screen bboxes; those are stand-ins for NBP output, not finals.
- Screen positions (HD px) carried through every beat: seated lemur bbox (34,176)–(207,660); hanging lemur bbox (1690,322)–(1810,783); release point = hanging lemur's clasped hands (1750,651); catch point = seated lemur's reaching hand (207,344); throw apex (932,197), i.e. over the V and 130 px above cap height (y 327).
- Storyboard page (rendered text, "06 MIAVANA") has slightly different beat splits (throw 04.0–05.5, palms 08–10). This board follows the **timing doc**; the page's notes (12-frame anticipation hold, arc in front of the type, colour-match plate greens toward sage, easter-egg mango on loop 3) are kept as motion notes.

## Beats

| # | Brief line | IN–OUT (s) · frames | Frame | On screen | Motion / camera | Transition | Assets used | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | "Start with the logo with the lemurs (better positions)" | 00.0–02.4 · f0–58 | `01_lockup.png` | Sage lock-up: MIAVANA / ISLAND SANCTUARY / BY TIME+TIDE, seated lemur on the M, hanging lemur by its tail from the final A, mango already visible in its clasped hands | Still. Breathing on both, one tail sway on the hanging lemur, one head-turn. Mango visible from f0 so the audience registers it before it moves | — | `miavana_0002_miavana.png`, `miavana_0003_islandsanctuary.png`, `miavana_0004_bytimeandtide.png`, `miavana_0000_left_lemur.png`, `miavana_0001_right_lemur.png`, sage from `miavana_0005_Layer-0.png`; mango crop from `a ring-tailed lemur produces a mango, throws it up and to the right.mp4` @2.0 s | COMP (lock-up READY as PSD comp) · mango TO GENERATE — **Flux** prop |
| 1 ALT | same | same | `01alt_lockup_firstA_ALT.png` | As beat 1 but the seated lemur moved onto the **first A** (PSD x 798, feet on the apex at x 885) — the timing doc position | same | — | same layers, `left_lemur` layer offset +754 px in PSD space | ALT — for Allen's call. Note: the tail (632 px layer) now drops ~27 PSD px into ISLAND SANCTUARY; needs a lifted seat or trimmed tail if chosen |
| 2a | "the last one holding a mango" | 02.4–03.0 · f58–72 | `02_windup_TOGEN.png` | Hanging lemur produces / weighs the mango, cocks one arm | Wind-up f58–70. 12-frame anticipation hold — the comedy is in the pause. Seated lemur only turns its head | — | as beat 1; mango offset up-right of the hands | TO GENERATE — **Kling** (hanging lemur re-posed with one free arm; the supplied still has both hands clasped). Existing 720×1280 Kling clips prove the motion, below HD |
| 2b | "throwing it to the other lemur" | 03.0–03.8 · f72–92 | `03_throw_TOGEN.png` | Mango mid-arc over the V, in front of the type; dashed arc drawn from release (1750,651) to catch (207,344) | Release f72, 20-frame arc, apex over the V clearing cap height, mango tumbling; receiving lemur's head tracks it | — | as beat 1 | TO GENERATE — **Flux** mango prop; **Kling** throw at HD (or 2D-animate the Flux prop along this arc in After Effects) |
| 2c | (catch) | 03.8–04.2 · f92–101 | `04_catch_TOGEN.png` | Mango in the seated lemur's outstretched hand | One-handed catch, lemur otherwise still; soft "thup" at 04.0 | — | as beat 1 | TO GENERATE — **Kling** (or 2D on the still) |
| 3 | "The hotel appears in the background" | 04.2–06.2 · f101–149 | `05_reveal_COMP.png` | Sage dissolving to the aerial resort plate; wordmark holds ~1.0 s at reduced strength then fades; lemurs hold position | Cross-dissolve; the letters under the lemurs resolve into palm trunks as they go. Colour-match the plate greens toward the sage ground so the change reads as focus, not a cut | cross-dissolve | `resort.png` (16:9 cover crop, anchor 0.62), lock-up layers at 55 %, lemur layers, mango | COMP · plate PORTRAIT — outpaint or crop decision pending |
| 4 | "the lemurs are in the palm trees" | 06.2–09.6 · f149–230 | `06_palms_TOGEN.png` | Resort plate full; both lemurs in real palm crowns at the same screen positions they had on the letterforms; second, lower toss mid-arc | Slow aerial drift right-to-left, 6 % of frame over 3.4 s. Second toss at 07.8 shorter and lower (apex ~90 px below the first); "thup" at 08.0 | — | `resort.png`, `lemur.png` (seated, scaled down to the 484 px bbox), `Firefly_remove background 477817 (1).png` (hanging, scaled to the 462 px bbox), mango crop | TO GENERATE — **NBP** (lemurs sat in real palm crowns at these positions on the plate; type-free); toss motion **Kling** or 2D |
| 5 | "Hotel disappears back to the logo" | 09.6–11.4 · f230–274 | `07_return_COMP.png` | Resort dissolving out, sage returning, letters re-forming under the lemurs | Reverse of beat 3; lemurs land in their beat 1 positions | cross-dissolve | `resort.png` at 30 % (blurred), lock-up layers at 75 %, lemur layers | COMP |
| 6 | "lemurs in places" (hold / loop) | 11.4–12.0 · f274–288 | `08_hold.png` | Full-strength lock-up, lemurs in beat 1 positions, mango back in the hanging lemur's hands | Still; loop point back to f0 | — (loop) | as beat 1 | READY as PSD comp; mango TO GENERATE — **Flux** |

Audio (timing doc): Malagasy forest at dawn, valiha or light marimba; two soft catches at 04.0 and 08.0. Storyboard page: "keep it dry, never cartoonish".

## Open questions for Allen

1. **Seated lemur: M or first A?** The PSD, the flattened `miavana copy.png`, `images-2.jpg` and the earlier storyboard page all put it on the M; the timing doc says first A ("the two arches read as branches"). Board is built on the M; `01alt_lockup_firstA_ALT.png` shows the alternative. If the first A wins, the tail collides with ISLAND SANCTUARY and the lemur needs re-seating (lifted or shorter tail) — that means touching the wordmark layout, so it needs the vector mark.
2. **`resort.png` rights and format.** It is a 2× upscale of `Miavana_©_Dylane_Cabano_001-scaled.jpg` — is the licence confirmed for a broadcast/social animation, and do we (a) outpaint the sides to 16:9 (NBP/Flux, risks inventing resort architecture) or (b) accept the tight cover crop shown (loses sky, sandbar and most of the lagoon)?
3. **Mango at the loop point.** Timing doc: "mango back in hand — loops clean." Storyboard page: "the mango is gone. Nobody mentions it." Board follows the timing doc. Which?
4. **Throw at HD: Kling re-run or 2D?** The two existing Kling clips are 720×1280 portrait with forest backgrounds (no alpha). Either re-run Kling on the sage lock-up at HD with the hanging pose, or animate the Flux mango along the drawn arc in AE with the stills breathing. The 2D route needs no new lemur generation for beats 2a–2c except one free-arm pose.
5. **Vector wordmark.** Still not in the pull — the PSD type layers are raster (2260 px wide). Needed before any re-kerning, the ALT position, or the "letters become palm trunks" morph in beat 3.

## Assets still needed

- Mango prop (Flux), clean alpha, ~120 px at HD, lit to match the lemur stills; a second frame with it tumbled 35° for the arc.
- Hanging lemur with one free arm raised (wind-up pose) at the PSD lemur's scale — NBP or Kling still.
- NBP plate: `resort.png` crop with both lemurs composited into real palm crowns at bboxes (34,176)–(207,660) and (1690,322)–(1810,783).
- Decision-dependent: 16:9 outpaint of `resort.png`; vector `MIAVANA` wordmark.
- Kling motion at HD (throw, catch, breathing/tail sway) if the 2D route is not taken.
- Audio: forest bed, valiha/marimba figure, two catch foleys.

## What this board does not cover

- No motion is proven at HD: every Kling reference is 720×1280. The dashed arcs are annotations, not animation curves.
- The "letters resolve into palm trunks" idea (beat 3) is described only; no morph frame was built, since it needs the vector mark and the NBP plate.
- The palms frame places the big cut-outs at the letterform positions on the plate; they are not in the palm crowns (floating over jungle at left, over a palm at right) — that is exactly the NBP job.
- Colour-matching the plate greens to sage, the 6 % aerial drift, and the easter-egg mango on the third loop are not previewed.
- No audio, no end-card variant with a smaller mark, and no vertical (9:16) safe-area pass.
- `build_frames.py` writes one ffmpeg frame grab and the mango cut-out into `frames/_work/`; nothing under the pull directory is touched.
