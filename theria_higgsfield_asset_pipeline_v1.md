# Theria — Higgsfield Asset & Generation Pipeline v1
Companion to `theria_hotel_animations_timing_v1.md`
Prepared 2026-09-09 · Allen Grabo / RTFX Design

**Untested.** Nothing below has been run. Model names, strengths and limits are from general knowledge as of mid-2026, not from a live check of your Higgsfield account, and I don't know your exact UI field names. Treat the routing as a starting hypothesis, run the three Tier-0 tests in §8 first, and correct this file from what actually comes back.

---

## 1. The shape of the pipeline

Every one of the eight films is a **transformation between two known still frames** — logo → creature, white → water, chandelier → guillotine, flat mark → spinning deck. That is the easiest thing to control and the hardest thing to get from a text prompt.

So: **do not text-to-video any of this.** Build it as

```
STILLS  →  KEYFRAME PAIRS  →  KLING start+end  →  NLE assembly
(NBP / Seedream / Flux)      (one clip per shot)   (Resolve/AE)
```

1. **Generate every keyframe as a still first**, at delivery resolution or above. Every shot boundary in the timing doc is a keyframe. There are ~50 across the eight films; roughly 30 already exist as the plates in your folders.
2. **Feed Kling a start frame and an end frame per shot.** If your Kling build exposes start+end keyframes, use it everywhere — it is the difference between "the giraffe turns around" and "something giraffe-shaped happens." Where only a start frame is available, keep the motion prompt to a single verb.
3. **Generate long, cut short.** Kling clips come out at fixed lengths (5 s / 10 s). Every shot in the timing doc is 0.6–4.2 s. Generate 5 s, take the best 1.5–3 s window, retime in the NLE. Budget 3–5 generations per shot to get one usable window.
4. **Assemble, retime and grade in the NLE.** All the timing-doc frame numbers are conform targets, not generation targets. Kling output frame rate will not match your 24 fps timeline — conform with optical flow, not frame blending.
5. **Do the impossible beats in comp, not in a model.** Specifically: the Versailles chandelier→guillotine morph, the 22 Club digit flip, and every logo fade. See §7.

---

## 2. Model routing

| Job | Model | Why |
|---|---|---|
| Compositing a **brand mark** into a scene; anything where type must stay legible | **Nano Banana Pro** | Best-in-class in-image text and multi-reference composition. It is the only one of the four I would trust near a wordmark |
| **Multi-image consistency** — same creature, same pose, across several plates | **Nano Banana Pro** | Takes several reference images and holds identity between them |
| **Photoreal hero plates at large size** — landscapes, interiors, water | **Seedream 4.5** | Native high-res output; least upscaling needed downstream |
| **Enlarging / re-rendering an existing 1–1.5K plate** to 4K | **Seedream 4.5** | Feed the existing plate as reference, re-render at target size rather than upscaling |
| **Outpainting** a portrait plate to 16:9 | **Seedream 4.5** or **Nano Banana Pro** | Both extend cleanly; NBP if there's type in frame |
| **Isolated objects on white** — gold props, turntable, guillotine, mango | **Flux 2.0 Pro** | Strongest material and specular rendering; gold and lacquer are its home turf |
| **All motion** | **Kling O1** | image-to-video, start+end frame |
| **Any logo enlargement** | **none of them** | vector trace — see §4 |

Rule of thumb: **Flux for the object, Seedream for the world, Nano Banana Pro for anything with type in it, Kling for the move.**

---

## 3. What you actually have — measured

Every file, its real pixel dimensions, and what it needs. Delivery target assumed **3840×2160**.

### Usable plates (need enlargement only)

| File | Size | Gap to 4K | Action |
|---|---|---|---|
| `Giraffe Manor/ea5d5cfc…png` | 1024×1536 | 2.5× + wrong orientation | Seedream re-render at 4K, then outpaint to 16:9 |
| `5th ave/47da2bff…png` | 1536×1024 | 2.5× | Seedream re-render 3840×2560, crop |
| `5th ave/d9bdfd2c…png` | 1448×1086 | 2.65× | Seedream re-render |
| `Passalaqua/46e10c0f…png` | 1421×1107 | 2.7× | Seedream re-render |
| `Passalaqua/b74514e7…png` | 1536×1024 | 2.5× | Seedream re-render |
| `North Island/0873e031…png` | 1536×1024 | 2.5× | Seedream re-render |
| `North Island/7e26a98a…png` | 1536×1024 | 2.5× | **NBP** — has the wordmark in it |
| `North Island/b261916d…png` | 1536×1024 | 2.5× | **NBP** — has the wordmark in it |
| `Versali/965d5f9a…png` (cake+chandelier) | 1023×1537 | 2.5× + **portrait** | Seedream re-render, then outpaint L/R to 16:9 |
| `Versali/cfb72e66…png` (cake+guillotine) | 1024×1536 | same | same — and it must outpaint to the *same* room as the one above |
| `Versali/4ad9ad80…png` (cake sliced) | 1023×1537 | same | same |
| `Versali/fd1e32ee…png` (elements on black) | 1024×1536 | 2.5× | Flux — it's an isolated-object plate |
| `Versali/1651551468329.webp` (Hall of Mirrors) | 1170×780 | 3.3× | Seedream re-render |
| `Miavana/195288a0…png` (clean sage lock-up) | 1254×1254 | square, 3× | **NBP** — type |
| `Miavana/…Dylane_Cabano_001-scaled.jpg` | 1800×2401 | portrait, real photograph | Do **not** re-render — this is a licensed photo. Upscale conventionally (Topaz / Resolve super-scale) and outpaint only if you have the rights |

**The three Versailles portrait plates are the biggest single job.** They are 2:3, the film is 16:9, and the room has to match across all three or the morph will crawl. Outpaint all three from the same reference in one session, same seed if the model exposes one.

### Logos — all too small, none should be AI-enlarged

| File | Size | Verdict |
|---|---|---|
| `Giraffe Manor/Giraffe-Manor-Logo-46px.webp` | **288×46** | web thumbnail. Unusable |
| `North Island/download.jpg` | **225×121** | unusable |
| `Passalaqua/images-3.jpg` | 275×183 | unusable |
| `Passalaqua/passalacqua.jpg` | 410×319 | unusable |
| `22 club/images.png` | 364×549 | unusable |
| `5th ave/images.jpg` | 447×447 | unusable |
| `Miavana/images-2.jpg` | 447×447 | unusable (clean 1254 version exists) |
| `Versali/images.jpg` | 554×554 | unusable |
| `Necker/07D6D2DD…jpg` (Virgin) | 1320×1240 | borderline — a hard red-on-white script, traces cleanly |

### Missing entirely

| Film | Missing | Model |
|---|---|---|
| Miavana | mango prop | Flux |
| Necker | flamingo (isolated) | Flux |
| Necker | island aerial | Seedream |
| Necker | kite-surfer | Seedream |
| Necker | two lemurs playing tennis | Seedream, then NBP for consistency with the Miavana lemurs |
| 22 Club | turntable / platter / vinyl | Flux |
| 22 Club | spotlight cone + dusty club floor | Flux or comp it in AE |

---

## 4. Logos: trace them, don't generate them

**Do not put a client's wordmark through a generative model.** Not Nano Banana Pro, not anything. These models re-draw letterforms; they will not reproduce the Giraffe Manor giraffe-patch counter or the Passalacqua fish tails exactly, and "almost the logo" is the one thing a hotel brand team will reject on sight.

The boring answer is the right one:

1. Ask the client for **vector artwork** — AI/EPS/SVG. Every one of these eight properties has it. One email saves a day of tracing. Do this first.
2. If it doesn't come back, **trace by hand** in Illustrator against the raster at high zoom. The Giraffe Manor mark at 288×46 will need eyeballing from the live website's SVG rather than that file.
3. Only then bring the vector into Nano Banana Pro **as a reference for placement**, or — better — never put it through a model at all: composite the vector over the generated plate in After Effects, where you control its position, scale and opacity to the frame.

That last point changes the pipeline for the better. **Every logo appearance in all eight films should be an AE layer over a generated plate, not something baked into a generated image.** It makes every "logo fades in / logo fades out" beat free, exact and revisable, and it removes the single largest source of client rejection.

Consequence: the North Island plates `7e26a98a` and `b261916d` already have the wordmark burned in. Either get clean versions generated without type (Seedream, prompt the scene only) and re-composite, or accept them as-is and lose the ability to animate the wordmark separately. **Recommend regenerating clean.**

---

## 5. Asset production queue — prompts

Global settings for all still generation:
- Aspect **16:9**, largest resolution the model offers, target 3840×2160
- Negative / avoid, everywhere: `text, watermark, signature, logo, letters, extra limbs, deformed anatomy, plastic, CGI look, oversaturated, harsh flash, tilted horizon`
- Isolated objects: pure white `#FFFFFF` background, soft studio key, one clean contact shadow

### 5.1 — 22 Club (Flux 2.0 Pro)

**Turntable platter, isolated**
> Single vintage direct-drive turntable platter photographed from a low three-quarter angle, brushed aluminium rim, black rubber slipmat, chrome centre spindle, matte black tonearm with counterweight resting at the side. Studio product photography on pure white seamless, single soft key from upper left, one crisp contact shadow, warm specular highlights on the metal. No text, no branding, no record on the platter.

**Vinyl record, isolated, top-down**
> A single black 12-inch vinyl record photographed perfectly top-down, deep matte black grooves catching a narrow crescent of warm light, plain deep-red centre label with no text on it, tiny dust motes on the surface. Pure white background, no shadow, no reflection. No text of any kind.

**Spotlight cone + floor**
> A hard-edged theatrical spotlight beam descending from upper left into total darkness, volumetric shaft heavy with drifting dust, landing as a sharp bright ellipse on a dark polished concrete floor. Nothing else in frame. Deep blacks, no fill light, no lens flare, no people.

Note: the beam is much easier to build in After Effects (cone geometry + Optical Flares + a noise-driven dust layer) than to matte out of a generated still. Generate it as reference for the lighting direction, then build the real one.

### 5.2 — Miavana mango (Flux 2.0 Pro)

> A single ripe mango, blushed red-orange fading to yellow-green, slight natural bloom on the skin, one small stem scar. Photographed at eye level on pure white seamless, soft even studio light, one contact shadow. Sharp, photoreal, natural fruit colour, no gloss spray, no text.

Generate three: one clean, one held (with a slight indentation), one mid-air with motion blur. The mid-air is the one Kling will need at both ends of the throw.

### 5.3 — Necker Island (the four-element build)

**Flamingo, isolated — Flux 2.0 Pro**
> A single adult Caribbean flamingo standing on one leg in full profile, deep coral-pink plumage, black-tipped down-curved beak, neck in a relaxed S-curve. Full body including both feet, isolated on pure white seamless, soft overcast studio light, natural feather detail, one soft contact shadow. Photoreal wildlife photography. No background, no water, no text.

Then a second pass for the takeoff pose, same bird:
> Same flamingo, wings fully extended in the first downstroke of takeoff, body angled forward and upward, one foot still touching the ground, primary feathers spread. Isolated on pure white, same lighting.

Feed the first image in as a reference so the plumage matches. **Nano Banana Pro handles this consistency better than Flux** — generate pose 1 in Flux for material quality, then pose 2 in NBP referencing it.

**Island aerial — Seedream 4.5**
> Aerial three-quarter view of a small private Caribbean island from about 300 metres, turquoise shallows ringing white sand beaches, dense green palm interior, a low scatter of thatched villas among the trees, deep blue open ocean beyond, a few small boats at anchor. Late afternoon light, long soft shadows, clear sky with scattered cloud. Photoreal drone photography, sharp horizon, no text.

**Kite-surfer — Seedream 4.5**
> A lone kite-surfer crossing a turquoise bay left to right, seen from a distance so the figure is small in frame, back to camera, blonde hair, board throwing a long white spray trail, a large bright kite arcing high above and behind. Bright tropical afternoon, island coastline in the background. Photoreal action photography, no facial detail, no text.

Deliberately anonymous: small in frame, back to camera, no face. Do not prompt any real person's name or likeness.

**Lemurs playing tennis — Seedream 4.5, then NBP**
> Two ring-tailed lemurs on opposite sides of a grass tennis court on a tropical island, each holding a wooden tennis racket, mid-rally, one crouched ready and one following through. Palm trees and turquoise sea behind the court. Warm afternoon light, photoreal wildlife photography, natural lemur anatomy and proportions, no cartoon styling, no clothing, no text.

Then run it through **Nano Banana Pro with the Miavana lemur references** so the same species and coat read across both films — the two hotels are in the same reel and a viewer will notice.

---

## 6. Per-film Kling segments

Format: `[start frame] → [end frame]` then the motion prompt. Generate 5 s, harvest the window the timing doc calls for. Keep camera language out of the prompt where the timing doc calls for a locked-off shot — Kling adds drift if you leave the door open.

Global negative for all video generation: `morphing faces, warping limbs, flickering, text distortion, sudden zoom, camera shake, extra animals appearing, style change mid-shot`

### Giraffe Manor
| Shot | Frames | Prompt |
|---|---|---|
| 1 | hero still → hero still | `Static shot. The giraffe stands still. Only its ear twitches once and its tail flicks. Camera locked off. Background stays pure white.` |
| 3 | hero alone → hero + second giraffe | `A second giraffe walks slowly into frame from the right and stops beside the first. Natural giraffe walking gait. Camera locked off. Pure white background throughout.` |
| 4–5 | two on white → two on manor lawn | `The white background dissolves away and a green lawn with an ivy-covered stone manor house resolves behind the two giraffes. The giraffes do not move. Slow, gentle transition.` |
| 6 | two facing camera → two walking away | `Both giraffes turn away from camera and walk slowly toward the manor house in the background, getting smaller. Camera pushes in slightly behind them.` |
| 7 | walking away → heads at windows | `The two giraffes reach the stone wall of the house, raise their necks and put their heads through the upstairs windows. Slow and calm.` |

Shot 6 is the one to over-generate. If ten attempts won't turn them cleanly, cheat it: hold on the static pair, whip-pan, and cut to a Seedream-generated backs-turned plate.

### Fifth Avenue
| Shot | Frames | Prompt |
|---|---|---|
| 1 | tortoise → tortoise | `Static shot. The gold tortoise does not move. A highlight slides slowly across its shell from left to right. The head lifts very slightly once. Locked-off camera, pure white background.` |
| 4 | tortoise on white → couple in park | `The white background dissolves into a sunlit park with trees and grass, and a Victorian couple in period dress appears walking behind the tortoise. The tortoise stays exactly in place.` |
| 5 | painted plate → painted plate | `Extreme slow motion. The couple walk forward almost imperceptibly slowly, the parasol rotates a few degrees, the leash sways. The tortoise takes one very slow step. Leaves drift at normal speed in the background. Painterly, oil-painting look preserved.` |

Shot 5 is the whole film. The trick is that the background must move at normal speed while the figures crawl — if Kling slows everything uniformly the gag dies. Fallback: generate the figures at normal speed and retime them in the NLE with optical flow, leaving the background at 100%.

### Passalacqua
| Shot | Frames | Prompt |
|---|---|---|
| 3–4 | flat gold fish outlines → dimensional gold fish | `Three flat golden fish symbols slowly gain volume and become solid three-dimensional golden fish. They rotate slightly toward the viewer and begin to move their tails. Pure white background.` |
| 5 | fish on white → fish over lake | `The white background dissolves into a blue alpine lake with mountains and a villa on the shore. Water rises into the lower third of the frame and the three golden fish drop into it with small splashes.` |
| 6 | fish in water → fish mid-leap | `Three golden fish leap out of the lake one after another in high arcs, water sheeting off their bodies, droplets catching the light. The camera pulls back slowly to reveal the villa on the shoreline.` |

### Versailles
| Shot | Frames | Prompt |
|---|---|---|
| 2 | cake on black → cake in full salon | `A lavish gilded eighteenth-century salon fades up around the cake, panelling and parquet and tall windows resolving from darkness. Warm afternoon light falls across the floor. The cake does not move.` |
| 4 | cake + chandelier → cake + guillotine | **do this in comp, not in Kling — see §7** |
| 6 | guillotine raised → blade down | `The blade drops straight down very fast and stops. Nothing else in the room moves. Single hard motion, no camera move.` |
| 7 | whole cake → sliced and plated | `The cake separates into slices which slide outward onto plates arranged around the table. Smooth, elegant, no debris, no crumbs flying.` |
| 8 | salon → Hall of Mirrors | `Slow pull back and dissolve into a long mirrored hall with crystal chandeliers receding into the distance.` |

### North Island
| Shot | Frames | Prompt |
|---|---|---|
| 2 | turtles on white → turtles in shallows | `The white background floods with clear turquoise water rising from the bottom of the frame, light caustics rippling across the surface. The golden turtles stay exactly in place.` |
| 3 | turtles in shallows → turtles drifted right | `The golden turtles begin swimming, front flippers stroking one after another, drifting slowly toward the right of frame. Caustic light moves across their shells. Seen from directly above.` |
| 4 | turtles swimming → turtles on sand | `The water shallows out and becomes white sand beach with palms and a green hillside behind. The turtles' swimming becomes a slow heavy crawl across the sand.` |
| 5 | turtles on sand → turtles at waterline | `The turtles turn around one after another and crawl back toward the sea. The sand gives way to turquoise water.` |
| 6 | turtles in water → turtles on white | `The turquoise water drains away to pure white from the top of the frame down. The turtles settle into stillness.` |

Shot 6's end frame must be **frame 0 of shot 1**, pixel-identical, or the loop will pop.

### Miavana
| Shot | Frames | Prompt |
|---|---|---|
| 2 | lemur holding mango → other lemur holding mango | `The hanging lemur winds up and throws a mango in a high arc across the frame to the second lemur, which catches it. Natural lemur movement, both animals keep their grip. Flat sage-green background, nothing else changes.` |
| 3 | lemurs on lettering → lemurs in palms | `The flat green background dissolves into an aerial view of a tropical island resort at dusk, and the two lemurs are now sitting in real palm trees in the same positions. Smooth transition, lemurs do not move.` |
| 4 | lemurs in palms → lemurs in palms | `The two lemurs sit in the palm crowns, tails swaying. One tosses the mango to the other. The aerial view drifts slowly from right to left.` |
| 5 | lemurs in palms → lemurs on lettering | `The island dissolves back to flat sage green and the lemurs settle into their original positions.` |

Shot 3 is the one worth the effort: the two letterform arches becoming two palm trunks at the same screen positions. Build both end plates in Nano Banana Pro from the same composition so the positions line up exactly, then let Kling only handle the dissolve.

### Necker Island
| Shot | Frames | Prompt |
|---|---|---|
| 1 | flamingo standing → flamingo standing | `Static shot. The flamingo stands on one leg. It preens once and settles. Nothing else moves.` |
| 2 | standing → wings extended | `The flamingo crouches, then launches into flight with three strong wingbeats, climbing toward the upper right of frame. The camera tilts up to follow it.` |
| 3 | flamingo close → island wide | `Continuous zoom out. The flying flamingo becomes small in frame as an aerial view of a tropical island and turquoise sea opens up beneath it.` |
| 4 | island wide → island wide | `A kite-surfer crosses the bay from left to right in the lower third of the frame, throwing spray, kite arcing above. The flamingo continues flying across the upper third in the opposite direction.` |
| 5 | island wide → tennis court close | `Push in on a grass tennis court on the island. Two ring-tailed lemurs rally a tennis ball back and forth three times. Natural animal movement.` |

Shot 5 is the highest-risk generation in the whole reel — animals holding and swinging objects is where every current video model falls apart. Board a fallback: two static Seedream plates and a ball animated in AE.

### 22 Club
| Shot | Prompt |
|---|---|
| 2, 3, 5 | **do these in comp, not in Kling — see §7** |
| 4 | `A hard-edged spotlight beam drops in from the upper left and sweeps right across two turntables in a dark room, dust drifting in the light. The records keep spinning.` |

---

## 7. Three beats that must not go through a video model

**Versailles — chandelier → guillotine (Shot 4).** Two problems. First, a model will re-invent both objects mid-morph. Second, "guillotine" and "blade falling" will trip safety filters on at least one of these four models, and you'll burn a session finding out which. You already have both end states as clean plates (`965d5f9a` and `cfb72e66`) plus an isolated guillotine and an isolated chandelier. Morph them in After Effects — a shape-driven cross-dissolve with a luma-matte wipe travelling down the ropes reads far better than anything a video model will hand you, and it's revisable in minutes. If a filter does refuse a prompt, don't reword it into something vaguer; move that beat to comp.

**22 Club — the digit flip (Shots 2, 3, 5).** This is a geometric rotation of a vector logo in 3D space with a perspective change. It is a ten-minute job in After Effects with a 3D layer and a camera, and it is exactly what a diffusion model cannot do — it will warp the letterforms. Generate the *turntable* in Flux, rotate the *digits* in AE, comp them together.

**Every logo fade in all eight films.** Covered in §4. AE layers over generated plates. Never baked in.

Roughly a third of the reel is comp work, not generation. Plan the schedule that way.

---

## 8. Run these three tests before committing to anything

Each is cheap and each answers a question that changes the plan.

1. **Seedream outpaint test.** Take `Versali/965d5f9a…png` (portrait, 1023×1537), re-render at max resolution and outpaint left and right to 16:9. Does the salon extend believably, and does the marble tabletop stay level? If no, all three Versailles plates need regenerating from scratch in 16:9 instead — a much bigger job, and you want to know now.
2. **Kling turn test.** Giraffe Manor Shot 6, the 180° turn, from the existing 1024×1536 plate. Five generations. If none of them turn the animals cleanly, the whip-pan fallback goes into the board now rather than in week three.
3. **Nano Banana Pro type test.** Feed it `North Island/b261916d…png` and ask for the same composition at 4K **without the wordmark**. If the type comes out cleanly removed and the turtles survive, the clean-plate strategy in §4 works everywhere. If it hallucinates letterforms back in, you're compositing over the burned-in version and losing the type animation.

Log what each one returns and correct §2 from it.

---

## 9. Sequencing

| Order | Work | Blocked by |
|---|---|---|
| 1 | Email all eight clients for **vector logos** | nothing — do it today |
| 2 | Run the three Tier-0 tests (§8) | nothing |
| 3 | Re-render the 13 existing plates to 4K (Seedream / NBP) | test 1 and 3 |
| 4 | Outpaint the three Versailles plates to 16:9 | test 1 |
| 5 | Generate the 7 missing elements (§5) | nothing |
| 6 | Trace any logo that doesn't come back as vector | step 1 |
| 7 | Kling pass, film by film, easiest first: North Island → Passalacqua → Fifth Avenue → Miavana → Giraffe Manor → Necker | steps 3–5 |
| 8 | Comp beats in AE: Versailles morph, 22 Club flip, all logo layers | step 6 |
| 9 | Assemble, retime to the timing doc, grade, sound | everything |

Necker and 22 Club are last because they are the two with nothing on the shelf.

---

## 10. What this does not cover

- **Higgsfield's actual interface.** I don't know your field names, credit costs, queue behaviour, or which of the four models your account exposes at which resolutions. Every "largest resolution the model offers" above is a placeholder for a number you'll have to read off the UI.
- **Verification of any model claim.** The routing in §2 is reasoned from general model characteristics as of mid-2026, not measured. §8 exists because of that.
- **Aspect ratio.** Still assumed 16:9 and still unanswered from the last round. Every outpaint instruction above changes if these are 9:16.
- **Kling's exact clip lengths, frame rate and whether your build exposes start+end keyframes.** The whole §6 approach depends on that last one. Check it before generating anything.
- **Upscaler comparison.** I've routed enlargement through re-rendering in Seedream rather than a dedicated upscaler. If you have Topaz or Magnific in the stack, a straight upscale may beat a re-render on the plates you want unchanged — particularly the licensed Miavana photograph, which should not go near a generative model at all.
- **Prompt tuning per model.** The prompts in §5 are written model-neutral. Flux responds to denser material and lighting language; Nano Banana Pro responds to plain instructions and reference images; Seedream sits between. Expect to rewrite each one once you see what comes back.
- **Nothing was generated or tested.** Paper plan.
