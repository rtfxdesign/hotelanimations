# Theria — Hotel Animation Timings v1
Shot-by-shot expansion of the 8 hero animations
Prepared 2026-09-09 · Allen Grabo / RTFX Design

---

## Global assumptions (change these once and the whole sheet shifts)

| Parameter | Value | Note |
|---|---|---|
| Frame rate | **24 fps** | frame numbers given as `f###`; at 30 fps multiply by 1.25 |
| Duration band | **10–15 s** | each sequence below states its own total |
| Aspect | **not decided** | see "Open questions" — every layout note below assumes 16:9 |
| Colour | logo-safe area = centre 80% | so the same master crops to 1:1 and 9:16 |
| Audio | 1 stinger + 1 bed per film | 22 Club is the exception (music-led) |
| Loop | each film ends on its own opening frame ±1 tone | so they can run on a lobby loop back-to-back |

Timing convention: `IN – OUT (duration)`. Overlaps are deliberate — a cross-dissolve is written on both shots.

Production note: every sequence is built as **stills → animated segments**, not full CG. The files already in each folder are the keyframes; the work is the in-between. Where a keyframe does not exist yet it is flagged **[ASSET MISSING]**.

---

## 1. Giraffe Manor — 14.0 s (f336)

**Assets on hand** (`…\Giraffe Manor\`)
- `ea5d5cfc-e93b-4d86-acf6-81bba6e7bd70.png` — hero giraffe, isolated on white, full body, three-quarter facing camera-left
- `Giraffe-Manor-Logo-46px.webp` — burnt-orange wordmark + giraffe-patch square
- `images-1.jpg` — manor exterior, lawn, herd on the steps (wide)
- `images-2.jpg` — two giraffes standing at the upstairs stone windows (the money shot)
- `images.jpg` — two heads through the dining-room windows, interior

| # | IN – OUT | Dur | On screen | Motion / camera | Transition |
|---|---|---|---|---|---|
| 1 | 00.0 – 02.0 (f0–48) | 2.0 s | Hero giraffe, pure white field, standing centre-left | Locked off. Micro-life only: ear twitch f12, tail flick f30, one slow blink f40. 1.5% push-in across the whole shot | — |
| 2 | 02.0 – 03.6 (f48–86) | 1.6 s | Wordmark fades up on the ground line directly under the hooves | Logo scales 96% → 100% with an ease-out; opacity 0 → 100 over 0.8 s, then hold 0.8 s | fade |
| 3 | 03.6 – 06.4 (f86–154) | 2.8 s | Second giraffe enters from frame right | Full walk cycle, 4 strides, ~1.4 s per stride pair. It stops with its shoulder just clear of the first giraffe's rump. Logo stays put — the newcomer walks *behind* it | — |
| 4 | 06.4 – 07.4 (f154–178) | 1.0 s | Logo out, manor in | Logo opacity 100 → 0 over 0.6 s. On the same frame the white field starts dissolving up to the `images-1.jpg` lawn, held soft/defocused | cross-dissolve begins |
| 5 | 07.4 – 08.6 (f178–206) | 1.2 s | Manor resolves behind both giraffes | Background rack-focuses from f/1.4-soft to sharp. Slight parallax: background drifts 2% left, giraffes hold | dissolve completes f206 |
| 6 | 08.6 – 11.2 (f206–269) | 2.6 s | Both giraffes turn and walk away toward the manor | They turn over ~0.8 s, then walk upstage. Scale down to 62%. Camera pushes in 8% behind them so the manor grows faster than they shrink | — |
| 7 | 11.2 – 13.4 (f269–322) | 2.2 s | Arrival at the stone façade — match to `images-2.jpg` | Necks rise, both heads enter the upstairs windows. Land the last frame on the `images-2.jpg` composition exactly | — |
| 8 | 13.4 – 14.0 (f322–336) | 0.6 s | End card | Wordmark fades up small, bottom-right, 60% of its Shot 2 size. Hold to black | fade to black f336 |

**Audio** — Kenyan highland ambience (birds, distant wind) from 00.0. Single low woodwind swell 06.4 → 08.6 under the reveal. Ambience alone from 13.4.

**Risk** — Shot 6 is the hard one: a 180° turn on a quadruped from a static plate. Budget the most iterations here, or cheat it with a whip-pan at 09.4 and cut to the backs-turned walk.

---

## 2. The Fifth Avenue Hotel — 12.0 s (f288)

**Assets on hand** (`…\5th ave hotel NYC\`)
- `47da2bff-…png` — gold tortoise, isolated on white, in profile facing camera-right
- `d9bdfd2c-…png` — the painted plate: Gilded-Age couple walking the gold tortoise on a leash, park setting
- `images.jpg` — navy roundel logo, "THE FIFTH AVENUE HOTEL" in gold

Brief says the logo appears **in gold with no background**, so the roundel's navy disc is stripped — wordmark only, gold on white.

| # | IN – OUT | Dur | On screen | Motion / camera | Transition |
|---|---|---|---|---|---|
| 1 | 00.0 – 02.4 (f0–58) | 2.4 s | Gold tortoise, profile, white field | Dead still except a specular highlight travelling across the shell, left → right, f10–f50. One slow head-lift at f44 | — |
| 2 | 02.4 – 04.2 (f58–101) | 1.8 s | Gold wordmark (disc removed) fades up under the plastron | Letterforms wipe on left-to-right over 1.0 s behind a soft gold gradient, then hold | — |
| 3 | 04.2 – 05.4 (f101–130) | 1.2 s | Logo out | Opacity 100 → 0 over 0.7 s, with a 3% scale-up as it goes. Tortoise unchanged | — |
| 4 | 05.4 – 07.2 (f130–173) | 1.8 s | The couple materialise; white becomes park | Cross-dissolve from white to the `d9bdfd2c` plate. The tortoise is the anchor — it must not move a pixel through the dissolve, so the plate is pre-aligned to the isolate | cross-dissolve |
| 5 | 07.2 – 11.4 (f173–274) | 4.2 s | The walk | This is the whole joke, so it gets the longest hold. Everything moves at roughly **1/6 normal speed**: the woman's parasol rotates ~8°, the man's forward foot travels ~15 px, the tortoise advances one body-width. Leash tension shifts. Leaves drift at *normal* speed in the background — the contrast is what sells the slowness | — |
| 6 | 11.4 – 12.0 (f274–288) | 0.6 s | End card | Full navy roundel logo fades up centre over the frozen plate, which desaturates 20% | fade |

**Audio** — a single sustained cello note under the whole film, one lazy footfall + leash creak at 08.2 and 10.6. No music sting; the silence is the gag.

---

## 3. Passalacqua — 13.0 s (f312)

**Assets on hand** (`…\Passalaqua\`)
- `passalacqua.jpg` / `images-3.jpg` — the mark: three gold fish above a wave rule, "PASSALACQUA / LAGO DI COMO"
- `46e10c0f-…png` — three real gold fish leaping out of Lake Como, villa behind
- `b74514e7-…png` — the villa on the lake, blue-graded

Note the brief reads "start with the logo of 3 fishes / add the logo underneath" — read as: **fish mark first, wordmark second**.

| # | IN – OUT | Dur | On screen | Motion / camera | Transition |
|---|---|---|---|---|---|
| 1 | 00.0 – 02.0 (f0–48) | 2.0 s | Three flat gold fish outlines + wave rule, white field, no type | Fish draw on in sequence: left f0–f14, centre f8–f22, right f16–f30. Then dead still | — |
| 2 | 02.0 – 03.6 (f48–86) | 1.6 s | "PASSALACQUA / LAGO DI COMO" fades up beneath the wave rule | Letter-spacing eases from +8% to +4% as it fades in. Hold 0.8 s | — |
| 3 | 03.6 – 05.0 (f86–120) | 1.4 s | Type out, fish start to fill | Wordmark opacity to 0 over 0.5 s. From f100 the fish take on volume: gold gradient floods each body bottom-to-top, scales catch light, eyes gain a specular | — |
| 4 | 05.0 – 06.6 (f120–158) | 1.6 s | Fish become real | They rotate from flat-on to three-quarter, gain a cast shadow on the white, and take the first tail beat. Slight overlap/offset between the three — do not animate them in sync | — |
| 5 | 06.6 – 08.2 (f158–197) | 1.6 s | Lake and villa arrive | White dissolves to the `46e10c0f` plate. Water level rises into the bottom third of the frame; the fish drop into it, splash rings on landing | cross-dissolve |
| 6 | 08.2 – 12.2 (f197–293) | 4.0 s | The leap | Three staggered arcs: centre fish breaches at 08.6, left at 09.4, right at 10.1. Each is airborne ~0.9 s with a full body arc and a water-sheet trailing off the tail. Camera pulls back 12% across the shot to open up the villa | — |
| 7 | 12.2 – 13.0 (f293–312) | 0.8 s | End card | Last fish re-enters the water; the ripples settle into the wave rule of the logo, wordmark fades up over the lake | fade |

**Audio** — lake ambience and a distant church bell from 00.0. Three water-breaks at 08.6 / 09.4 / 10.1. Strings resolve on the end card.

**Nice-to-have** — Shot 7's "ripples become the wave rule" is the best idea in the set. If it fights you, fall back to a straight fade.

---

## 4. Airelles Le Grand Contrôle, Château de Versailles — 15.0 s (f360)

Longest of the eight — it has seven beats and the payoff is a hard cut on action.

**Assets on hand** (`…\Versali\`)
- `965d5f9a-…png` — cake on gilt table under the crystal chandelier, salon interior
- `cfb72e66-…png` — cake on gilt table under the **guillotine**, same salon
- `4ad9ad80-…png` — cake sliced, plated portions ringing the table, guillotine above
- `fd1e32ee-…png` — cake + chandelier isolated on black (clean elements)
- `1651551468329.webp` — Hall of Mirrors, wide
- `images.jpg` / `images copy.jpg` — AIRELLES / LE GRAND CONTRÔLE / CHÂTEAU DE VERSAILLES wordmark
- guillotine isolated on white (in `4ad9ad80`-set) — usable as a clean element

| # | IN – OUT | Dur | On screen | Motion / camera | Transition |
|---|---|---|---|---|---|
| 1 | 00.0 – 02.2 (f0–53) | 2.2 s | Cake on the gilt table, chandelier above, everything else black | Candle flames flicker; crystals throw slow caustics across the icing. 1% push-in | — |
| 2 | 02.2 – 04.4 (f53–106) | 2.2 s | The salon builds up around it | Boiserie, parquet, drapes and window light fade up from black outward from the centre, ~1.4 s. Warm afternoon shaft lands across the floor | reveal |
| 3 | 04.4 – 06.2 (f106–149) | 1.8 s | Wordmark fades up beneath the table | AIRELLES set in the clear parquet space below the table legs. Fade 0.7 s, hold 1.1 s | — |
| 4 | 06.2 – 08.8 (f149–211) | 2.6 s | **The turn.** Chandelier becomes guillotine | Do it as a morph, not a cut: crystals darken and elongate into timber uprights f149–f180; the central candle-boss stretches into the blade f170–f200; the rope and pulley draw on last f195–f211. Room light drops 1.5 stops across the shot. Nobody in frame reacts — the cake is oblivious | — |
| 5 | 08.8 – 09.8 (f211–235) | 1.0 s | Logo out | Wordmark opacity to 0 over 0.5 s. Beat of total stillness f223–f235 — hold on this, the silence is what makes the next beat land | — |
| 6 | 09.8 – 10.6 (f235–254) | 0.8 s | **The drop** | Blade falls in **8 frames** (f238–f246). Add 2 frames of pre-shake at f235 and a 3-frame white flash-frame on impact at f246. Camera shakes 4 px, settles by f254 | hard |
| 7 | 10.6 – 13.6 (f254–326) | 3.0 s | Cake apart | 0.6 s of the cake falling into slices, then the plated arrangement of `4ad9ad80` assembles: portions slide out to their plate positions and settle, ringing the table. Light comes back up 1 stop | — |
| 8 | 13.6 – 15.0 (f326–360) | 1.4 s | End card | Pull back / cross-dissolve to the Hall of Mirrors wide; wordmark fades up centre | dissolve |

**Audio** — string quartet, period, playing through beats 1–5. It **stops dead** at 09.8. Rope-and-timber creak, one blade whoosh, one impact thud at 10.6. Quartet returns at 11.2 on the cake-serving beat as if nothing happened.

**Tone check** — it reads as a dessert-service gag as long as the room stays empty and the blade only ever meets cake. Do not put a figure anywhere near the frame.

---

## 5. North Island, Seychelles — 13.0 s (f312)

The brief's arc is white → water → beach → water → white, so the film loops perfectly.

**Assets on hand** (`…\North Island\`)
- `b261916d-…png` — gold turtle mark + "north island / SEYCHELLES" on white (the start and end frame)
- `7e26a98a-…png` — same lock-up over turquoise shallows, turtles swimming
- `0873e031-…png` — turtles on the sand, beach and forested island behind
- `download.jpg` — the house mark: concentric-circle turtle + wordmark, black on white

| # | IN – OUT | Dur | On screen | Motion / camera | Transition |
|---|---|---|---|---|---|
| 1 | 00.0 – 02.2 (f0–53) | 2.2 s | Gold turtles + wordmark on white — `b261916d` exactly | Completely still. One highlight sweep across the big turtle's shell f24–f48 | — |
| 2 | 02.2 – 04.0 (f53–96) | 1.8 s | White becomes water | Turquoise floods in from the bottom edge upward over 1.2 s, caustics resolving as it rises. Wordmark stays locked and unmoved — it is now floating on the surface. Land on `7e26a98a` | — |
| 3 | 04.0 – 07.0 (f96–168) | 3.0 s | They start to swim | Front flippers begin at f96, staggered by 6 frames per turtle. Slow forward drift toward frame right, ~15% of frame width across the shot. Caustics move over the shells. Wordmark begins a slow fade at f150 | — |
| 4 | 07.0 – 09.4 (f168–226) | 2.4 s | Landfall | Water shallows out — colour ramps turquoise → pale sand across 1.2 s. Turtles' flipper cycle changes from swim to a heavier crawl at f190. Beach and island fade up behind. Land on `0873e031` | — |
| 5 | 09.4 – 11.4 (f226–274) | 2.0 s | Turn and return | The three turtles turn back toward the water (staggered, 0.5 s apart) and start out. Sand ramps back to turquoise | — |
| 6 | 11.4 – 13.0 (f274–312) | 1.6 s | Back to blue, back to white | Water desaturates to white from the top down over 1.0 s, turtles settle into their Shot 1 positions, wordmark fades back up. **Final frame = frame 0** | loop point |

**Audio** — surf and reef ambience, gently panned; it rises through the water beats and drops to near-silence at 12.4 so the loop join is inaudible.

---

## 6. Miavana — 12.0 s (f288)

**Assets on hand** (`…\Miavana\`)
- `images-2.jpg` — MIAVANA / ISLAND SANCTUARY / BY TIME+TIDE lock-up on sage green, with a lemur seated on the M and one hanging from the final A
- `195288a0-…png` — the clean lock-up on sage, no lemurs
- `Miavana_©_Dylane_Cabano_001-scaled.jpg` — the resort from the air, beach and palms at dusk
- `images-1.jpg` — ring-tailed lemur seated on a branch, tail hanging
- `images-4.jpg` — two ring-tails climbing/hanging in branches

**[ASSET MISSING]** — no mango. Needs one prop element, or lift a fruit from stock and gold/colour-match it.

Brief says "better positions" for the lemurs, so: seated lemur moves to the **first A**, hanging lemur to the **final A** — the two arches read as branches, and the throw then crosses the whole wordmark.

| # | IN – OUT | Dur | On screen | Motion / camera | Transition |
|---|---|---|---|---|---|
| 1 | 00.0 – 02.4 (f0–58) | 2.4 s | Sage lock-up, lemur seated on the first A, second lemur hanging by one arm from the last A, mango in its free hand | Still, with breathing and one tail sway on the hanging lemur. The mango is visible from frame 0 — the audience needs to see it before it moves | — |
| 2 | 02.4 – 04.2 (f58–101) | 1.8 s | **The throw** | Wind-up f58–f70, release f72, mango arcs right-to-left across the top of the wordmark f72–f92 (20 frames, apex over the V), catch f92–f101. Receiving lemur's head tracks it the whole way | — |
| 3 | 04.2 – 06.2 (f101–149) | 2.0 s | Sage becomes island | Green dissolves to the aerial resort plate; the wordmark holds on top for 1.0 s then fades. Letters that the lemurs were sitting on resolve into palm trunks as they go | cross-dissolve |
| 4 | 06.2 – 09.6 (f149–230) | 3.4 s | Lemurs in the palms | Both are now in real palm crowns at the same screen positions they occupied on the letters — that continuity is the whole trick. Slow aerial drift right-to-left, 6% of frame. One more mango toss at 07.8, shorter and lower this time | — |
| 5 | 09.6 – 11.4 (f230–274) | 1.8 s | Back to the mark | Resort dissolves out, sage returns, letters re-form under the lemurs. They land in their Shot 1 positions | cross-dissolve |
| 6 | 11.4 – 12.0 (f274–288) | 0.6 s | Hold | Wordmark and BY TIME+TIDE at full strength. Mango back in hand — loops clean | — |

**Audio** — Malagasy forest at dawn, valiha or light marimba figure. Two soft "thup" catches at 04.0 and 08.0.

---

## 7. Necker Island — 14.0 s (f336)

**Assets on hand** (`…\Necker Island\`)
- `07D6D2DD-…jpg` — the Virgin script logo, red on white

**[ASSET MISSING] — this is the thin one.** No flamingo art, no island plate, no kite-surf plate, no lemur/tennis element. Four hero elements to originate before this can be boarded properly.

Casting note carried through from the brief: the kite-surfer is **a blonde man, not a likeness of a named person**. Keep him small in frame, back-to-camera, no facial detail — safer and cheaper.

There is also a **second, unrelated Necker concept already in that folder** — `Animation Virgin.docx` — a hand-drawn-logo / red-line-through-the-decades piece ending on a parachute drop onto Necker. It is a different film. Flag it before anyone starts work so the two do not get merged by accident.

| # | IN – OUT | Dur | On screen | Motion / camera | Transition |
|---|---|---|---|---|---|
| 1 | 00.0 – 02.4 (f0–58) | 2.4 s | Single flamingo, standing, isolated on white or pale sky | Still, one-legged. Head preens at f20, settles f38 | — |
| 2 | 02.4 – 04.6 (f58–110) | 2.2 s | **Takeoff** | Crouch f58–f66, first downstroke f68, three full wingbeats to f110. It climbs and moves toward frame right; camera tilts up with it, lagging slightly | — |
| 3 | 04.6 – 07.4 (f110–178) | 2.8 s | Pull back to the island | Continuous zoom-out — flamingo shrinks to ~8% of frame height, still flying. Sea fills in from the edges, then the island resolves centre. Aerial three-quarter view, not top-down | — |
| 4 | 07.4 – 10.2 (f178–245) | 2.8 s | Kite-surfer | Camera settles. Blonde figure crosses the bay left-to-right in the lower third, kite arcing above. Spray trail. The flamingo continues across the upper third in the opposite direction — the two crossing paths are the composition | — |
| 5 | 10.2 – 13.0 (f245–312) | 2.8 s | Lemurs playing tennis | Push in on the island's court. Two ring-tails, one each side, rallying. Three hits: 10.8, 11.6, 12.4. Ball travel ~14 frames per exchange. Play it straight — no cartoon takes | — |
| 6 | 13.0 – 14.0 (f312–336) | 1.0 s | End card | Pull back out to the island wide; Necker / Virgin lock-up fades up | fade |

**Audio** — wing beats (close, then distant), wind and water, three tennis pocks. No music until the end card.

---

## 8. 22 Club — 12.0 s (f288)

**Assets on hand** (`…\22 club\`)
- `images.png` — the mark: red "22" over a scripted "club", white ground. 5.5 KB — **too small to animate from. Get vector or a large raster.**

**[ASSET MISSING]** — turntable/platter element, records, spotlight cone.

The gag: the two 2s rotate 90° onto their backs and read as two spinning platters. The digit "2" has a flat base bar, so once it is on its back that bar becomes the platter edge — build the rotation around that.

| # | IN – OUT | Dur | On screen | Motion / camera | Transition |
|---|---|---|---|---|---|
| 1 | 00.0 – 02.0 (f0–48) | 2.0 s | The mark, red on white — or red on black if the film is going in a club, which it should | Still. Optional faint bass-pulse scale on "club", 2% at the track's tempo | — |
| 2 | 02.0 – 04.4 (f48–106) | 2.4 s | **The flip** | Each 2 rotates 90° backward on its own base line, staggered 8 frames apart (left first). Perspective goes with it — they end as two ellipses seen from about 30° above. 0.8 s per digit with a small overshoot and settle | — |
| 3 | 04.4 – 06.2 (f106–149) | 1.8 s | They become decks | Spindle, platter ridges, tonearm and a black vinyl disc build onto each ellipse over 1.0 s. Records start spinning at f130, up to 33⅓ within 0.5 s. The "club" script stays put and becomes the front fascia of the mixer between them | — |
| 4 | 06.2 – 08.2 (f149–197) | 2.0 s | **Spotlight** | Hard-edged cone drops in from top-left at f149, hits the left deck f158, then sweeps right across both by f180. Ground goes to black outside the cone. Dust in the beam. Vinyl catches the light on every rotation — the flash rate should read as the 1.8 s/rev of a 33⅓ record | — |
| 5 | 08.2 – 10.6 (f197–254) | 2.4 s | **The flip back** | Records fade, decks strip back to bare ellipses over 0.8 s, then both digits rotate up 90° — this time **together**, not staggered, 0.8 s, with the same overshoot. Spotlight narrows and lifts away as they come up | — |
| 6 | 10.6 – 12.0 (f254–288) | 1.4 s | Back to normal | Full mark, dead centre, dead still. Light returns to a flat field. Last 6 frames hard-cut to black on the final downbeat | hard cut |

**Audio — the lead element here, cut picture to music, not the other way round.** Sexy techno, roughly 122–124 BPM. That puts a beat every 0.484 s, so the structural hits want to land on: 02.0 (flip), 06.2 (spotlight), 08.2 (flip back), 12.0 (cut). Build a 12.0 s edit at 124 BPM = 24.8 beats — round the tempo to **124 BPM and let the film run 12.10 s (f290)** so it ends exactly on beat 25. Filter sweep under the spotlight; drop on the flip-back.

---

## Summary

| Film | Duration | Frames @24 | Assets ready? | Hardest shot |
|---|---|---|---|---|
| Giraffe Manor | 14.0 s | 336 | ✅ all 5 | Shot 6 — the 180° turn |
| Fifth Avenue | 12.0 s | 288 | ✅ all 3 | Shot 5 — believable ultra-slow humans |
| Passalacqua | 13.0 s | 312 | ✅ all 4 | Shot 7 — ripples into the wave rule |
| Versailles | 15.0 s | 360 | ✅ all 7 | Shot 4 — chandelier→guillotine morph |
| North Island | 13.0 s | 312 | ✅ all 4 | Shot 6 — the loop join |
| Miavana | 12.0 s | 288 | ⚠️ no mango | Shot 3 — letters → palm trunks |
| Necker Island | 14.0 s | 336 | ❌ 4 elements missing | all of it |
| 22 Club | 12.1 s | 290 | ❌ logo too small + 3 elements | Shot 2 — the flip, in perspective |

Total run time if cut as one reel: **105.1 s**.

---

## Open questions — need your call

1. **Aspect ratio.** Everything above is laid out for 16:9. If these are going to Instagram as 9:16, the Versailles Hall-of-Mirrors end card and the North Island beach wide both need re-framing, and the Miavana throw arc gets shorter. Tell me the target and I will re-cut the layout notes.
2. **Delivery frame rate.** 24 fps assumed. If it is 30, every frame number multiplies by 1.25 and the 22 Club beat grid changes.
3. **22 Club logo.** The only file is 5.5 KB. Vector or a ≥2000 px raster, please, before anyone touches it.
4. **Necker Island.** Four hero elements do not exist yet (flamingo, island, kite-surfer, tennis lemurs). Also confirm which of the two Necker concepts is live — this one, or the `Animation Virgin.docx` red-line piece already in that folder.
5. **Miavana mango.** Source it or cut the throw and just have them swap places.

## What this document does not cover

- **Image-generation prompts.** These are shot descriptions, not prompt strings. If the pipeline is image-to-video (Veo / Kling / Runway), say so and I will write per-shot prompts with the seed images named.
- **Music selection or licensing.** Audio notes are directional only. 22 Club is the one film where the track has to be locked before the edit.
- **Client copy / end-card legal.** No taglines, URLs or credits are placed. Every end card above is logo-only.
- **The Theria Google Drive folder.** It mounted empty in this session, so nothing from it fed into these boards.
- **Nothing was rendered or tested.** This is a paper edit — all timings are untested and will move once the first shots come back.
