# The Fifth Avenue Hotel — storyboard v1

| | |
|---|---|
| Film | 02 · The Fifth Avenue Hotel (client folder `5th ave hotel NYC/`) |
| TRT | **12.0 s = f288** per `theria_hotel_animations_timing_v1.md` §2 (the storyboards page says 11.0 s, six beats — see "Where the page differs") |
| fps | 24 (assumed in the timing doc, not confirmed by Allen) |
| Aspect / master | 16:9, 1920×1080 HD (Allen, 2026-09-25). The storyboards page header also lists 1:1 and 9:16 masters — not boarded here |
| Frames | `frames/NN_name.png` 1920×1080, `NN_name_small.jpg` 960×540, `contact_sheet.jpg`. Built by `build_frames.py PULL_ROOT OUT_DIR` (run 2026-09-25, 8 frames, clean) |
| Brief (source of truth for beats) | 1 start on the gold tortoise · 2 add the Fifth Ave logo in gold, no background, under its feet · 3 the logo disappears · 4 add the people walking the tortoise · 5 the people move very slowly |

**Assumptions made to build the board**
- The walkers plate is `upscaled/turtlewalkers.psd` (4346×2444, 16:9) flattened from its own layers: `background` + `woman`, `man`, `leash`, `turtle` at the PSD bbox origins. The background layer is a clean park (no figures, no holes), so layers can be moved. `turtlewalkers.png` is the old 4:3 plate and is only the fallback if psd-tools is absent.
- Plate → HD is a straight cover scale of 0.4418 (no crop). At HD the plate tortoise is 646 px wide at x 854–1501, y 562–935; the woman's head is at y 87 and the tortoise's claws at y 935, so the plate cannot be scaled up without cropping the figures.
- Beats 1–3 use the client's isolated tortoise (`turtle02.png`, from `orig/47da2bff…png`) at 860 px wide = 1.33× its size in the plate, right of centre, claws at y 650, so the gold lockup fits under it. Beat 4 therefore carries a 1.33 → 1.0 pull-out anchored on the tortoise. If Allen wants the timing doc's "not a pixel" literally, the hero must be 646 px wide with its claws at y 935 — and then there is no room for a lockup under its feet. Open question 1.
- Gold lockup = `upscaled/fifthave_text.png` (603×422 RGBA). It is already the gold type keyed out of the navy roundel — the same thing the brief asked for — but it comes from the 2× (894 px) enlargement of a 447 px web thumbnail. **Placeholder until vector.** The script keys the gold out of `fifthavenue.png` itself only if `fifthave_text.png` is missing. No logo was AI-enlarged.
- End card roundel = `upscaled/fifthavenue.png` (894 px, plain 2× of `orig/images.jpg`) shown at 520 px — a downscale, tagged placeholder.
- No motion exists yet for this film. Every "motion / camera" cell is the timing doc's note, not something that has been generated.

## Beats

| # | Brief line | IN–OUT (s) · frames @24 | Frame | On screen | Motion / camera | Transition | Assets used | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | Start with image of the gold tortoise | 00.0–02.4 · f0–58 (58 f) | `01_hold.png` | Gold tortoise in profile facing camera-right, alone on white, right of centre (cx 1100), 860 px wide, claws at y 650 | Dead still. Specular highlight travels across the shell L→R f10–f50; one slow head-lift at f44 | — (cold open on white) | `upscaled/turtle02.png` (2803×1298 RGBA; = `orig/47da2bff-cdd3-4463-a32e-4320ffb9b8b0.png` isolated at 2×) | READY from assets (still). Specular sweep = AE comp (light sweep over the alpha). Head-lift = TO GENERATE, Kling O1 from this frame, single-verb prompt |
| 1 ALT | same | same | `01b_hold_ALT.png` | Same layout using the plate's own tortoise layer as hero (different pose: head higher, collar on, 1463×844) | as Beat 1 | — | `upscaled/turtle.png` (= `turtle` layer of `turtlewalkers.psd`) | READY from assets. **Recommended** unless the plate is regenerated around `turtle02` — it makes Beat 4 a true match (see review note 1) |
| 2 | Add the Fifth Ave logo in gold, no background, under its feet | 02.4–04.2 · f58–101 (43 f) | `02_lockup.png` | Gold "THE FIFTH AVENUE HOTEL" lockup, disc removed, 480 px wide centred under the plastron (top y 700, bottom y 1036) | Letterforms wipe on L→R over 1.0 s behind a soft gold gradient (foil shimmer), then hold. Tortoise unchanged | — | `upscaled/turtle02.png`, `upscaled/fifthave_text.png` **(PLACEHOLDER — vector lockup pending)** | COMP (AE layer over the still). Vector trace / client vector needed — no generative model near the mark |
| 3 | The logo disappears | 04.2–05.4 · f101–130 (29 f) | `03_lockup_out.png` | Same, lockup at 35 % opacity and +3 % scale (mid fade, ≈f115) | Lockup opacity 100→0 over 0.7 s (f101–118) with 3 % scale-up as it goes. Tortoise unchanged, white stays white | — | `upscaled/turtle02.png`, `upscaled/fifthave_text.png` (placeholder) | COMP (AE) |
| 4 | Add the people walking the tortoise | 05.4–07.2 · f130–173 (43 f) | `04_reveal.png` | Mid-dissolve (≈f152): white field and the couple/park at 50 %; the tortoise is the anchor | Cross-dissolve white → plate over 1.8 s, plus the 1.33→1.0 pull-out that lands the hero on the plate tortoise (646 px, x 854–1501, claws y 935). The frame shows the ghost of `turtle02` over the plate tortoise: they are different renders | cross-dissolve | `upscaled/turtle02.png` scaled to the plate footprint, `upscaled/turtlewalkers.psd` (`background` layer) + `woman.png`, `man.png`, `leash.png`, `turtle.png` at PSD origins | COMP (AE). Blocked by the hero mismatch: either take 01b ALT, or regenerate the plate around `turtle02` — NBP (multi-reference consistency; keep the pose) — and re-separate |
| 5a | Have the people moving very slowly | 07.2–11.4 · f173–274 (101 f) — start | `05_walk_start.png` | The full plate: Gilded-Age couple (parasol, top hat) walking the gold tortoise on a leash, painterly park | This is the Kling **start frame**. Everything at ≈1/6 normal speed; leaves and light in the background at normal speed | — | `upscaled/turtlewalkers.psd` (`background`) + `woman.png` @(742,196), `man.png` @(1754,226), `leash.png` @(1798,1095), `turtle.png` @(1934,1272) | READY from assets (flattened by `build_frames.py`, identical to the PSD comp) |
| 5b | same | 07.2–11.4 · f173–274 — end | `06_walk_end_TOGEN.png` | Conform target for the end of the walk: man +15 px (foot), woman +12 px, tortoise +162 px (¼ body-width), leash stretched to follow the collar. Parasol rotation (~8°) not shown — the parasol is inside the `woman` layer | Kling O1 image-to-video, start = 05, end = 06. Generate 5 s at normal walk speed, take the best window, retime to 1/6 in the NLE with optical flow. Background leaves/light at normal speed = a second Kling pass on the `background` layer only (or AE particles), comped under the figures | — | as 5a, layers offset in x | **TO GENERATE — Kling O1** (figures) + Kling/AE (background). The end frame itself is a comp, not a generation |
| 6 | (sign-off; not in the brief) | 11.4–12.0 · f274–288 (14 f) | `07_endcard.png` | Plate frozen at the 06 position, desaturated 20 %; full navy roundel fades up dead centre, 520 px | Roundel opacity 0→100 over the 0.6 s. No move on the plate | fade (out to black/white is not specified in the timing doc) | 06 comp + `upscaled/fifthavenue.png` **(447 px source at 2×, PLACEHOLDER UNTIL VECTOR)** | COMP (AE). Vector roundel needed |

Frame counts: the doc's IN/OUT frames sum to f288 = 12.0 s. Beat 1 is 2.4 s = 57.6 f (rounded to f58 in the doc).

## Where the storyboards page (TRT 11.0 s, six beats) differs from the timing doc

Boarded to the timing doc. The page is `inventory/storyboards_rendered_text_2026-09-25.txt`, "02 THE FIFTH AVENUE HOTEL · GILDED PATIENCE".

| Beat | Timing doc (boarded) | Storyboards page |
|---|---|---|
| all | 12.0 s: 2.4 / 1.8 / 1.2 / 1.8 / 4.2 / 0.6 | 11.0 s: 2.0 / 2.0 / 1.5 / 2.0 / 2.5 / 1.0 |
| 1 | specular L→R f10–50, head-lift f44 | highlight sweep 1.6 s, "no other movement" (no head-lift) |
| 2 | wipe on over 1.0 s behind a gold gradient | foil-shimmer wipe, 600 ms |
| 3 | type out 0.7 s, +3 % scale; tortoise unchanged, white stays | type out 500 ms; the white ground **warms to a park-light gradient** under it |
| 4 | 1.8 s cross-dissolve, plate pre-aligned to the isolate | 1.2 s dissolve "as a painting arrives — brushwork resolving" |
| 5 | 4.2 s hold, ≈1/6 speed, parasol ~8°, foot ~15 px, tortoise one body-width; leaves at normal speed | 2.5 s, "procession crosses frame left at a crawl, one step per second", ≈15 % speed; leaves/light normal speed |
| 6 | **navy roundel** fades up centre over the frozen plate, desaturated 20 % | couple **exit**, park holds empty a half-beat, **gold lockup** returns bottom-centre, then whip to white over 300 ms (loop) |

Sound also differs (doc: one cello note, footfall + leash creak at 08.2 and 10.6; page: parlour clock, distant carriage, one harp string). Not boarded.

## Open questions for Allen

1. **Hero scale vs "not a pixel".** Beats 1–3 are boarded at 1.33× the plate tortoise with a pull-out through the dissolve, because at plate scale the tortoise's claws sit at y 935 and there is no room for the lockup under its feet. Accept the pull-out, or move the lockup (beside the tortoise / lower third) and keep the tortoise fixed from frame 1?
2. **Which tortoise is the hero?** `turtle02.png` (the client's isolate — head low, no collar) and the plate's `turtle` layer (head raised, collar on) are different renders; a straight dissolve between them will crawl. Take 01b ALT (plate tortoise as hero), or regenerate the plate around `turtle02` with NBP and re-separate?
3. **End card.** Timing doc: navy roundel over the frozen plate. Page: couple exit, gold lockup bottom-centre, whip to white. Which one — and does the roundel version end on black, white, or loop?
4. **Beat 5 tortoise travel.** The doc's "one body-width" (646 px at HD) takes the tortoise's head off frame right (its nose is already at x 1501). Boarded as a quarter body-width. OK?
5. **Vector.** Has the client been asked for the lockup as AI/EPS/SVG? Both marks in this board are placeholders from a 447 px web thumbnail; the storyboards page also asks for the gold-on-transparent lockup as a source file.

## Assets still needed

| Asset | For | Route |
|---|---|---|
| Vector lockup — gold type only (no disc) **and** the navy roundel | Beats 2, 3, 6 | Client vector, else hand-trace in Illustrator. Not a generative model. Comp as an AE layer |
| Walk clip, figures: start = `05_walk_start.png`, end = `06_walk_end_TOGEN.png` | Beat 5 | Kling O1, start+end frame, 5 s at normal speed, retime to 1/6 in the NLE (optical flow). Budget 3–5 generations |
| Background-only motion (leaves drift, dappled light) | Beat 5 | Kling O1 on the PSD `background` layer alone, or AE particles/light. Must run at normal speed under the slowed figures |
| Head-lift on the isolated tortoise (f44) | Beat 1 | Kling O1 from `01_hold.png`, single verb; on white so it keys back to alpha |
| Specular sweep across the shell | Beat 1 | AE (light sweep masked by the tortoise alpha). No generation |
| *Optional, if open question 2 goes that way:* park plate regenerated around `turtle02` in the same pose, then re-separated | Beat 4–6 | NBP (multi-reference: `turtle02.png` + `turtlewalkers.png`), then Photoshop layer separation |

## What this board does not cover

- No motion has been generated or previewed; every frame is a still comp and the motion column is the timing doc's intent.
- Parasol rotation, leash slack/tension physics and the man's stride are not shown in `06` — the parasol and the hands are inside the `woman`/`man` layers, and the leash is stretched linearly, not re-drawn. Kling owns those.
- The mid-dissolve (`04`) shows a plain 50 % blend, not the pull-out in progress and not the page's "brushwork resolving" treatment.
- End card fade-out / loop behaviour, sound, and colour grade.
- The 1:1 and 9:16 masters the storyboards page lists; the timing doc's "logo-safe area = centre 80 %" was not checked against those crops.
- The `05`/`06` plate is the PSD flattened in Pillow (normal blend, 100 % opacity, which is how the PSD is set) — not a Photoshop export; if `turtlewalkers.psd` changes, re-run the script.
