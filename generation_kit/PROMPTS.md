# Theria — generation kit
Everything still to generate, film by film. Each item: the frame(s) in this folder to feed the model, the prompt, and what must not change. Model-agnostic: use image-to-video for anything marked I2V, text-to-image or image-edit for T2I / EDIT. 2026-09-25.

## Global settings

- Output 16:9. Stills at 2K or better (the plates are 2752 px wide; the film masters at 1920×1080). Video at 1080p or better; 24 fps if the model offers it, otherwise 30 and I conform.
- Video clips: generate 5 s (or the model's shortest length ≥ the shot), 3–5 takes each. The shots are 1.5–3 s; I take the best window.
- Camera locked off unless the prompt says otherwise. No camera language means no camera move.
- **Negative, every still:** `text, letters, watermark, signature, logo, extra limbs, deformed anatomy, plastic, CGI look, oversaturated, harsh flash, tilted horizon, people` (drop `people` where the prompt asks for a person).
- **Negative, every video:** `morphing, warping limbs, flickering, sudden zoom, camera shake, extra animals appearing, style change, text`.
- Never put a wordmark through a model. Every logo is an AE layer over the generated plate.
- Frame names: `START` = feed as the first frame; `END` = feed as the last frame where the model takes one; `EDIT` = the image to edit in place; `ref` = reference for look or identity only.

---

## 01 Giraffe Manor

**GM-1 · Walker regenerated to match the hero** (I2V, or T2I then I2V)
Frames: `gm_ref_hero_cutout_alpha.png` (identity reference), `gm_ref_hero_on_cream.png` (staging). Optional motion reference: the existing `Giraffe Manor/upscaled/giraffe_walking.mp4`.
Still first, if the model needs one:

> A single adult reticulated giraffe, pale sandy coat with soft tan patches, exactly the same animal as the reference, mid-stride walking left, full body including all four hooves, isolated on a flat ivory field (255,255,240), soft even studio light, no cast shadow beyond a faint contact shadow. Photoreal wildlife photography.

Video:

> The giraffe walks calmly from right to left at a natural walking pace, four full strides, head level, tail swaying slightly. Flat ivory background throughout. Camera locked off. Nothing else in frame.

Keep fixed: coat colour and pattern of the reference; ivory background; full body in frame.

**GM-2 · Shot 6, the turn** (I2V, start frame supplied)
Frames: `gm_shot6_START_both_on_lawn.png` (board start), `gm_shot6_START_animatic_f216.png` (same composite at the animatic frame; use either), `gm_shot6_placeholder_END_f268.png` (only shows where they should end up in frame, not a real end pose).

> Both giraffes turn away from the camera together, slowly, and walk up the lawn toward the ivy-covered stone house, getting smaller as they go. Natural giraffe walking gait, necks swaying. The people on the terrace stay still. Camera locked off, no zoom.

Keep fixed: the house, the terrace, the guests. The risk shot: over-generate; the fallback is a whip-pan cut.

**GM-3 · Shot 7 end plate, heads in the windows** (T2I with reference)
Frames: `gm_shot7_ref_client_photo_heads_in_windows.jpg` (client photo, the target composition), `gm_ref_manor_plate_no_giraffes.png` (the house, for continuity of stone and ivy).

> Two giraffes standing at the ivy-covered stone wall of an old manor house, seen from behind and slightly below, necks raised, both heads reaching into the open upstairs windows. Warm late-afternoon light, stone mullioned windows, dense ivy. Photoreal, 16:9, the giraffes fill the centre of frame.

Then **GM-4 · Shot 7 motion** (I2V from the last frame of GM-2 to the GM-3 plate, or from GM-3 alone):

> The two giraffes raise their necks and push their heads gently through the upstairs windows. Slow and calm. Camera locked off.

Keep fixed: same two giraffes as GM-1/hero; window positions match the client photo.

---

## 02 The Fifth Avenue Hotel

**FA-1 · Shot 5, the walk** (I2V, start frame supplied)
Frames: `fa_shot5_START_walk.png`, `fa_shot5_END_target_layers_offset.png` (conform target only; shows roughly how far they travel).

> A Gilded Age couple in period dress, the woman with a lace parasol, walk slowly forward beside a golden tortoise on a leash through a sunlit park. Painterly, oil-painting texture preserved. Normal walking speed, natural gait, the parasol turns slightly, the leash sways. Leaves and light move naturally. Camera locked off.

Generate at normal speed; I retime the figures to one-sixth in the NLE with the background at 100 %. Do not ask the model for slow motion.
Keep fixed: the painting's brushwork look; the tortoise's gold; the frame composition.

---

## 03 Passalacqua

**PA-1 · Clean lake and villa plate, no fish** (T2I with reference)
Frames: `pa_ref_lake_villa_with_fish.png` (the look, minus the fish).

> A calm alpine lake in front of a grand Italian lakeside villa on a wooded promontory, mountains behind, morning light, still water with soft reflections. No fish, no boats, no people. Photoreal, 16:9, horizon on the upper third, open water across the lower third.

Keep fixed: the villa, the light and colour of the reference.

**PA-2 · Fish become alive** (I2V, start frame supplied)
Frames: `pa_shot4_START_gold_fish_on_white.png`.

> Three solid gold fish sculptures, standing vertically side by side on white, come alive: they rotate slightly toward the viewer, gain a soft cast shadow, and take their first tail beat, each a beat apart. Pure white background. Camera locked off.

**PA-3 · Fish drop into rising water** (I2V; start = PA-1 plate with the three gold fish comped, `pa_shot5_approx_fish_drop_into_water.png` shows the intent)

> Clear lake water rises into the lower third of the frame and three golden fish drop into it one after another, small splash rings where they land. The villa on the shore stays still. Camera locked off.

**PA-4 · The leap** (I2V; start = PA-1 plate; `pa_shot6_leap_reference.png` is the target look)

> Three golden fish leap out of the lake one after another in high arcs, centre first, then left, then right, water sheeting off their bodies, droplets catching the light. Slow pull-back of about ten percent to reveal the villa on the shoreline.

Keep fixed: three fish, gold, staggered, never in sync.

---

## 04 Airelles Le Grand Contrôle, Versailles

The film is built as one clean salon plate with the cake, chandelier, guillotine and slices as separate layers. Four stills, then everything else is After Effects.

**VE-1 · Clean empty salon, 16:9** (T2I with reference)
Frames: `ve_ref_salon_cake_chandelier_portrait.png`, `ve_ref_salon_cake_guillotine_portrait.png` (the room; ignore the objects), `ve_shot2_letterboxed_16x9_reference.png` (framing).

> An empty eighteenth-century French salon: gilded boiserie panelling, parquet floor, tall windows with warm afternoon light falling across the floor, no furniture in the centre of the room, no people, no chandelier, no table. Photoreal interior photography, 16:9, camera at table height looking straight down the room.

Keep fixed: the panelling and window light of the references; clear floor in the centre for the table.

**VE-2 · Guillotine, isolated, blade separable** (T2I)
Frames: `ve_ref_salon_cake_guillotine_portrait.png` (the guillotine's look).

> A tall wooden guillotine with an angled steel blade raised to the top, rope and pulley, photographed straight on, isolated on pure white, soft studio light, one contact shadow. Then a second image of the same guillotine with the blade at the bottom.

Two stills, identical frame, blade up and blade down; I cut the blade out from the pair.

**VE-3 · Cake and chandelier as separate elements** (EDIT or T2I)
Frames: `ve_ref_cake_chandelier_cutout_alpha.png` (both objects on alpha; split them).

> Same tiered pale-blue cake with gold cameo medallions on the gilt console table, isolated on white. / Same crystal chandelier with lit candles, isolated on white.

Keep fixed: identical to the reference; only the separation changes.

**VE-4 · Sliced and plated** (T2I with reference)
Frames: `ve_ref_cake_sliced_plated_portrait.png`.

> The same cake cut into sixteen neat slices arranged on small porcelain plates in a ring around the gilt table, on pure white, soft studio light, one contact shadow.

---

## 05 North Island

**NI-1 · Water plate extended to 16:9** (EDIT: outpaint)
Frames: `ni_ref_water_lockup_3x2_to_extend.png` (3072×2048). Extend 150 px of water on each side at the plate's scale; `ni_shot3_START_swim_16x9_fit.png` shows the target framing.

> Extend the turquoise shallow water with sun caustics to the left and right edges. Do not change or add any turtles or text.

**NI-2 · The turtles swim** (I2V, start = NI-1)

> The five golden turtles begin to swim, front flippers stroking one after another, drifting slowly to the right by about a tenth of the frame. Sun caustics move across their shells and the sand. The lettering does not move. Seen from directly above. Camera locked off.

**NI-3 · Onto the sand** (I2V, start frame supplied)
Frames: `ni_shot5_START_crawl_on_sand.png`.

> Golden turtles crawl slowly up the white sand beach from the water's edge, heavy deliberate flipper movement, leaving faint drag tracks. Palms and green hillside behind stay still. Camera locked off.

**NI-4 · Back to the sea** (I2V, start = last frame of NI-3)

> The turtles turn around one after another and crawl back down the beach into the shallow turquoise water. Camera locked off.

Keep fixed across NI-2..4: five turtles, same gold; `ni_ref_lockup_on_white.png` is the identity reference.

---

## 06 Miavana

**MI-1 · Mango prop** (T2I, three stills)

> A single ripe mango, blushed red-orange fading to yellow-green, slight natural bloom on the skin, one small stem scar, photographed at eye level on pure white, soft even studio light, one contact shadow. Sharp, photoreal, natural fruit colour, no gloss.

Then the same mango: one held (slight finger indentation), one mid-air with slight motion blur.

**MI-2 · Wind-up pose** (I2V, start frame supplied)
Frames: `mi_shot1_START_lockup.png`. `mi_ref_lemur_cutout_alpha.png` is the identity reference.

> The ring-tailed lemur hanging by its feet from the last letter frees one arm, weighs a mango in its hand and draws the arm back to throw. Twelve frames of stillness before the throw. Flat sage-green background, the white lettering and the seated lemur do not move. Camera locked off.

**MI-3 · Catch pose** (I2V, same start frame)

> The ring-tailed lemur seated on the first letter reaches out one hand and catches a mango arriving from the right, its head tracking it; the body otherwise still. Flat sage-green background, lettering does not move. Camera locked off.

The arc between MI-2 and MI-3 is 2D in AE with the MI-1 mango; no video model for the throw.

**MI-4 · Lemurs in real palm crowns** (EDIT on the resort plate)
Frames: `mi_shot4_START_palms_positions.png` (where the two lemurs must sit), `mi_ref_resort_16x9.png` (clean plate).

> Place two ring-tailed lemurs in the crowns of the tall palms at these two positions, one seated, one hanging by its feet, at dusk light matching the plate. Nothing else in the plate changes.

Keep fixed: lemur screen positions match the lettering positions in `mi_shot1_START_lockup.png`; this continuity is the whole trick.

---

## 07 Necker Island

**NE-1 · Takeoff** (I2V, start frame supplied)
Frames: `ne_shot1_START_flamingo_on_white.png`; `ne_ref_flamingo_flight_4k.jpg` for the wing pose.

> The flamingo with the black bow tie crouches, then launches into flight with three strong wingbeats, climbing toward the upper right and exiting frame top-right. Pure white background throughout. Camera locked off, no tilt.

Keep fixed: the bow tie; the drawn look of the cut-out.

**NE-2 · Kite-surfer plate with a generic rider** (EDIT)
Frames: `ne_shot4_EDIT_kite_plate_4k.jpg`.

> Replace the rider with a different person: a blonde man, small in frame, seen from behind, riding the board across the bay left to right, no face visible, same board and spray. Bring the kite into frame above him. Keep the beach, sea, light and sun flare exactly as they are.

Rule: no likeness of any real person. Then **NE-3 · motion** (I2V from NE-2):

> The kite-surfer crosses the bay from left to right throwing spray, the kite arcing above. A flamingo flies across the upper third from right to left. Camera locked off.

**NE-4 · Lemurs playing tennis** (EDIT, two stills)
Frames: `ne_shot5_EDIT_tennis_court_4k.jpg` (remove the player first), `ne_ref_lemur_01_4k.jpg` (a real Necker lemur; the species to match is the Miavana ring-tail, `mi_ref_lemur_cutout_alpha.png`).

> Remove the tennis player. Then place two ring-tailed lemurs on opposite sides of the net, each holding a wooden tennis racket, mid-rally: one crouched ready, one following through. Natural lemur anatomy, no clothing, no cartoon styling. Same court, same light.

Two stills (A: left lemur ready, B: right lemur following through) are enough; the ball is animated in AE. If a video model is tried: `Two ring-tailed lemurs rally a tennis ball back and forth three times, natural movement, rackets held properly. Camera locked off.`

**NE-5 · Landing** (I2V, reverse of NE-1)

> The flamingo with the black bow tie glides in from the upper left, flares its wings, lands on one leg and settles into a standing profile pose. Pure white background. Camera locked off.

The last frame is replaced by the cut-out still in comp, so it need not match exactly.

---

## 08 22 Club

All three are objects for After Effects; the digit flip, spotlight and platter build are comp. `cl_ref_mark_on_black.png` is the mark for scale and colour only, never an input.

**CL-1 · Turntable platter** (T2I)

> Single vintage direct-drive turntable platter from a low three-quarter angle, brushed aluminium rim, black rubber slipmat, chrome centre spindle, matte black tonearm with counterweight resting at the side. Studio product photography on pure black, single soft key from upper left, warm specular highlights on the metal. No text, no branding, no record on the platter.

**CL-2 · Vinyl record, top-down** (T2I)

> A single black 12-inch vinyl record perfectly top-down, deep matte black grooves catching a narrow crescent of warm light, plain deep-red centre label with no text, tiny dust motes. Pure black background, no reflection.

**CL-3 · Spotlight cone reference** (T2I, lighting reference only; the beam is built in AE)

> A hard-edged theatrical spotlight beam descending from upper left into total darkness, volumetric shaft heavy with drifting dust, landing as a sharp bright ellipse on a dark polished floor. Nothing else in frame, deep blacks, no lens flare.

---

## Not in this kit (nothing to generate)

Giraffe Manor shot 1 micro-life (Kling take exists), the walk cycle as-is (exists, colour-matched for the board), all logo beats (AE), the Fifth Avenue lockup (vector + rendered gold type exist), the Passalacqua gold fish (exist in `passalacqua.png`), the Versailles blade drop and morph (AE), the Miavana throw arc (AE), the Necker pull-back (AE scale on the 5k aerial), the whole of 22 Club except the three objects above.
