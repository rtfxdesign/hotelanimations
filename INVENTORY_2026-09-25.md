# Theria Hotel Animations — Measured Inventory and Drive Connection
Written 2026-09-25 by Claude Code (cloud session) for Allen Grabo / RTFX Design. Companion to `HANDOFF_claude_code.md`; this document supersedes its "Inventory" and "First commands to run" sections. Everything below was measured by running code on the actual files, except where marked **untested** or **probed remotely**.

## 1. The answer

- **The Drive folder is connected two ways.** The claude.ai Google Drive connector can list and read it (it is owned by allen.grabo@gmail.com and shared to rtfxdesign@gmail.com). Separately, the folder is shared as *anyone with the link: writer*, so plain HTTPS downloads work from any machine with no OAuth. `tools/drive_pull.py` uses that to mirror the whole tree from `drive/manifest.json` (121 files, 2.45 GB, every file's Drive id and byte size).
- **Everything was pulled and measured.** 111 files downloaded and hashed; 95 images/videos measured (pixel dims, mode, alpha extent, fps, codec, frames). The two 681 MB stock items were probed over HTTPS without downloading. Results: `inventory/measurements_2026-09-25.json` and `.md`, `inventory/psd_layers_2026-09-25.md`.
- **Cloudflare R2 was not possible from this session.** The Cloudflare connector needs authorising in claude.ai connector settings, and there are no R2 keys in the environment. `tools/r2_upload.py` is written and compiles, but is **untested** against a real bucket. To let a future session upload, add four variables to the cloud environment (Edit environment → API credentials / environment variables): `R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_BUCKET`. Do not paste them into chat.
- **The storyboards HTML was rendered** (headless Chromium) and its full text is in `inventory/storyboards_rendered_text_2026-09-25.txt`. It answers some open questions and raises two new ones (§3).

## 2. Corrections to the handoff, from measurement

| Handoff said | Measured | Consequence |
|---|---|---|
| Source plates are 1536×1024 | The **orig** plates are (5th Ave tortoise 1536×1024, North Island ×3, Passalacqua villa). But the **working** plates are larger: `manor01.png/.psd` 2752×1536, `turtlewalkers.psd` 4346×2444, `miavana.psd` 2508×1411, `fadein.png` 6048×2592 | For HD 1920×1080 nothing in `upscaled/` needs enlarging. The 2752×1536 manor plate is 143 % of HD width; the pipeline doc's "re-render at 4K" is dead for these |
| `giraffe_walking.mov` 327 MB, "ProRes?" and open question 5 "which is the master" | **ProRes 4444, 3840×2160, 30.00 fps, 300 frames, 10.0 s, `yuva444p12le` with a real alpha channel** (alpha min 0 / max 255; the opaque region is ≈1070×1540 px, i.e. an isolated giraffe on transparency). `giraffe_walking.mp4` is the same clip as H.264 4:2:0, no alpha, on a cream field | **The .mov is the master. Keep it.** The mp4 is a proxy. Kling handed back 4K/30, not 1080p |
| "Kling native output (typically 1080p) is delivery-res" | Three different Kling outputs in the folder: 3840×2160 @ 30 (giraffe walk), 1920×1080 @ 24 (`frame1_to_frame2.mp4`, 97 frames, 4.04 s), **720×1280 @ 24** (both Miavana lemur clips, 144 frames, 6.0 s) | Kling resolution/fps depends on the mode used. The Miavana clips are portrait and below HD; usable only as comped elements at ≤ 84 % scale, and they carry backgrounds (forest, grey) that need keying |
| `manor01_giraffe0*.png` at 129 / 397 KB "check they're full-res, not thumbnails" | 178×290 and 332×486, RGBA, cropped to bounds. Positions in the PSD: giraffe01 at (1262, 869), giraffe02 at (1578, 1049) on the 2752×1536 canvas | They are full plate resolution, not thumbnails. They are small because the giraffes are small in the plate (19 % and 32 % of frame height). Fine as background figures; not usable as a hero |
| `giraffemanor_wordmark_alpha.png` "origin unknown" | 2346×432 RGBA, opaque area 2224×245. Letterforms are a mixed-case serif **"Giraffe Manor / Nairobi"** with wood-grain texture inside the strokes. It is cut from `hf_20260909_034918_86df0845….png` (6048×2592, a Higgsfield render of that wordmark on cream) | **It is an AI-drawn wordmark, not the client's mark.** The client mark (`orig/Giraffe-Manor-Logo-46px.webp`, 288×46) is small-caps **GIRAFFEMANOR** with a lowercase "nairobi" and a giraffe-patch block. Different typeface, different case, different lock-up. Unusable as a brand asset. Same wordmark is baked into `frame02.png` |
| `hf_…86df0845….ai` 703 bytes "flag" | Opened as text: Photoshop "Pen Path Export 7.0", bounding box 0 0 6048 2592, **no path data at all** between setup and trailer | Empty. Delete or ignore. There is no vector logo anywhere in the folder |
| `fifthave_text.png` / `fifthavenue.png` "raster; same vector caveat" | 603×422 and 894×894. `fifthavenue.png` is exactly 2× the 447×447 `orig/images.jpg` roundel; at 100 % the gold letterforms are soft with invented texture | AI-enlarged from a web thumbnail. Unusable for an HD title card. Vector needed |
| `fadein.png` "?" | 6048×2592 (2.33:1), Seedream/NBP render: the manor with a giraffe eating leaves in the foreground and **guests at tables**. `fadein - resized….png` is the same at 3999×1714 | It is the Shot 4/5 reveal plate. The storyboards page asks for "a clean manor plate without guests" — this is not that |
| `resort.png` "presumably outpainted/enlarged" | 3600×4802 **portrait**, exactly 2.0× the licensed `Miavana_©_Dylane_Cabano_001-scaled.jpg` (1800×2401). Not outpainted | Still needs a 16:9 solution (outpaint or crop to 3600×2025). It is a licensed photo; outpainting it is a rights question |
| Miavana lemur positions "first A and last A" | `miavana.psd` has the seated lemur on the **M** (x 44–270) and the hanging lemur on the **final A** (x 2208–2364). The storyboards page also says M and final A | Handoff and timing doc say first A; PSD and storyboards say M. Pick one (§3) |
| Storyboards HTML "not read" | Rendered. Bundled single-page app, 16.2 MB (51 images as blobs), title "THÈRIA · AR ANIMATION PROGRAMME · HOSPITALITY SLATE / EIGHT HOTELS, EIGHT AWAKENINGS". The 3.3 MB copy in `Giraffe Manor/` has identical text, images at half size | See §3. The page's run times differ from the timing doc |

Other measured facts worth knowing:

- **Byte-identical duplicates** (sha256): `Giraffe Manor/upscaled/manor01.png` = `Giraffe Manor/hf_20260909_025934_a3e0463c….png`; the two `hf_…86df0845….png`; the two `273559596_…n.jpg` (320×320 Facebook thumbnails); the two `Versali/cfb72e66….png`.
- `Miavana/upscaled/miavana_text - crop 2026-09-25 00-56-17.png` is a **JPEG** with a .png extension (2508×1260, no alpha).
- `manor01_background.png` differs from `manor01.png` across the whole frame, not just where the giraffes were: it was re-encoded or re-rendered, not masked. Harmless, but do not expect a pixel match outside the fill.
- `turtlewalkers.png` (2896×2172, 4:3) is not a flatten of `turtlewalkers.psd` (4346×2444, 16:9). The PSD is the 16:9 version with the canvas widened and the couple/tortoise/leash separated.
- `frame1_to_frame2.mp4`: start frame matches `frame01.png` (mean diff 1.5/255); end frame matches `frame01` better than `frame02` in the wordmark band (7.9 vs 22.1). **Kling did not render the wordmark that was in the end frame.** This is the pipeline doc's §4 point demonstrated: logos must be AE layers, never in the generated frames.
- Miavana Kling clips: the mango throw is a lemur seated on a branch **in a forest** (not on sage); it produces a mango and tosses it up-right, arms follow through. The sway clip is the upside-down lemur on a **light grey** field. Neither is on alpha or sage; both need keying, and at 720 px wide both are soft.
- The 681 MB `836ec439….mov` (extracted from the zip) probed remotely: 4096×2160, 24 fps, 57 s, H.264 (yuvj420p). The zip is the same file compressed; keep one.

## 3. What the storyboards page says that the docs don't

Source: `inventory/storyboards_rendered_text_2026-09-25.txt` and `inventory/previews/storyboards_page_part0–3.jpg`.

1. **Masters: 1:1 + 9:16 + 16:9.** The page header states three master aspects and "TRIGGER: PRINTED MARK / QR" (scan-to-animate AR). The handoff says HD 1920×1080 is settled. If the page is current, 16:9 HD is one of three deliverables and every layout note in the timing doc needs checking against 1:1 and 9:16 crops (the timing doc's "logo-safe area = centre 80 %" was written for exactly this). **Needs a decision.**
2. **Run times differ from the timing doc.** Storyboards → timing doc: Giraffe Manor 12.0 → 14.0 s; Fifth Avenue 11.0 → 12.0; Passalacqua 12.5 → 13.0; Versailles 14.0 → 15.0; North Island 13.0 = 13.0; Miavana 12.0 = 12.0; Necker 13.0 → 14.0; 22 Club 12.0 → 12.1. The handoff names the timing doc as source of truth for cuts. Confirm that still holds.
3. **Giraffe Manor beat 6 is "cut inside"**: two heads through the breakfast window over a laid table (matches `orig` `images.jpg`, 547×365). The timing doc's Shot 7 lands on the exterior `images-2.jpg`. Different payoff frame.
4. **Miavana lemurs are on the M and the final A** (page and PSD agree). The mango "arcs over the letterforms… in front of the type, never behind it" and the catch is by the lemur on the M.
5. **"TO SOURCE" lists per film** (the page's own asset gaps): Giraffe Manor — vector wordmark, second giraffe cut-out in a different pose, clean manor plate without guests. Fifth Avenue — gold-on-transparent lockup, walking couple as separated layers (now done in `turtlewalkers.psd`). Passalacqua — vector crest with fish on separate paths, clean villa/lake plate. Versailles — logo files, clean salon plate without cake or chandelier. North Island — each turtle as its own layer (or 3D source), clean beach plate. Miavana — lemur cut-outs in throw/catch poses, mango, wordmark as vector. Necker — everything. 22 Club — vector mark with numerals and script on separate paths, turntable reference, licensed techno bed.
6. Necker sign-off: "confirm which mark signs off — Necker Island lockup or Virgin Limited Edition."

## 4. Measured inventory, per hotel

Full table with every file, hash and alpha bbox: `inventory/measurements_2026-09-25.md`. Below is the curated view. "Use" is my read; verify before relying on it.

### Giraffe Manor
| File | Dims | Type | Use |
|---|---|---|---|
| `upscaled/giraffe_walking.mov` | 3840×2160, 30 fps, 10.0 s | ProRes 4444 **with alpha** | **Master** walk cycle, isolated giraffe entering frame right, walking left (Shot 3) |
| `upscaled/giraffe_walking.mp4` | 3840×2160, 30 fps, 10.0 s | H.264, no alpha, cream bg | proxy of the above |
| `upscaled/frame1_to_frame2.mp4` | 1920×1080, 24 fps, 4.04 s | H.264 | Kling start/end test, hero giraffe; end frame lacks the wordmark |
| `upscaled/frame01.png` / `frame02.png` | 2844×1600 | RGB | Kling keyframe pair; frame02 has the AI wordmark baked in |
| `upscaled/ea5d5cfc….png` | 1024×1536, opaque 881×1487 | RGBA | original hero giraffe on alpha, portrait |
| `upscaled/manor01.psd` | 2752×1536 | 3 layers | plate + two giraffe cut-outs (positions in `psd_layers`) |
| `upscaled/manor01.png` / `manor01_background.png` | 2752×1536 | RGB / RGBA (fully opaque) | plate with / without giraffes; guests and staff in frame |
| `upscaled/fadein.png` | 6048×2592 | RGB | reveal plate, giraffe head eating leaves, guests in frame |
| `upscaled/giraffemanor_wordmark_alpha.png` | 2346×432 | RGBA | AI-drawn wordmark; **not the brand** |
| `upscaled/hf_…86df0845….ai` | 703 B | empty PS path export | discard |
| `hf_20260909_030041….png` | 5504×3072 | RGB | Higgsfield render (not inspected further) |
| `hf_20260909_025953….png` | 3504×2336 | RGB | Higgsfield render |
| `hf_20260909_025923….png` | 2752×1536 | RGB | Higgsfield render, sibling of manor01 |
| `hf_20260909_043233….png` | 1280×720 | RGB | small render |
| `closeup-shot-of-a-giraffe….jpeg`, `striking-giraffe-profile….jpg` | 6000×4000, 5600×3719 | JPEG | licensed stock stills |
| `orig/Giraffe-Manor-Logo-46px.webp` | 288×46 | WEBP RGBA | the only real brand mark; web thumbnail |
| `images.jpg`, `images-1.jpg`, `images-2.jpg` | 547×365, 666×460, 678×452 | JPEG | web reference (interior window heads, lawn, exterior windows) |

### 5th Avenue Hotel
| File | Dims | Type | Use |
|---|---|---|---|
| `upscaled/turtlewalkers.psd` | 4346×2444 (16:9) | 5 layers: background, man, turtle, leash, woman | **Master comp**, layers separated, zero motion |
| `upscaled/man.png` `woman.png` `turtle.png` `leash.png` | 666×1579, 1131×1804, 1463×844, 582×336 | RGBA, crop-to-bounds | layer exports; origins in `psd_layers` |
| `upscaled/turtlewalkers.png` | 2896×2172 (4:3) | RGB | 2× of the original painterly plate, pre-widening |
| `upscaled/turtle.psd` / `turtle02.png` | 3072×2048 canvas / 2803×1298 | RGBA | isolated gold tortoise, Shot 1 start frame |
| `upscaled/fifthave.psd` `fifthavenue.png` `fifthave_text.png` | 894×894, 894×894, 603×422 | RGBA | 2× of a 447 px roundel; soft; **not HD-usable** |
| `orig/47da2bff….png`, `orig/d9bdfd2c….png`, `orig/images.jpg` | 1536×1024, 1448×1086, 447×447 | | originals, unchanged |

### Miavana
| File | Dims | Type | Use |
|---|---|---|---|
| `upscaled/miavana.psd` | 2508×1411 | 6 layers | **lock-up master**: sage bg, MIAVANA, ISLAND SANCTUARY, BY TIME+TIDE, left lemur (on M), right lemur (on final A) |
| `upscaled/miavana_000N_*.png` | 226×632 … 2508×1411 | RGBA | the six layer exports; wordmark letterforms are clean |
| `upscaled/miavana copy.png` | 2508×1411 | RGB | flatten of the PSD |
| `upscaled/miavana_text.png` | 2508×2508 | RGB | square render of the lock-up (source of the crop) |
| `upscaled/…mango, throws it up and to the right.mp4` | 720×1280, 24 fps, 6.0 s | H.264, forest bg | **the throw exists**, but low-res, portrait, not on sage |
| `upscaled/…natural motion, slow sway.mp4` | 720×1280, 24 fps, 6.0 s | H.264, grey bg | hanging lemur sway |
| `upscaled/a ring-tailed lemur hanging upside-down… (2).png` | 3072×5504 | RGB | large render of the hanging lemur |
| `upscaled/…hanging upside-down….png`, `(1).png` | 768×1376 | RGB | small renders (Kling start frames?) |
| `upscaled/lemur.png` `lemur2.png` `lemur3.png` | 1796×3192 (opaque 1129×2932), 1035×2717, 1068×2689 | RGBA | large lemur cut-outs; these are the ones to re-stage onto the letterforms |
| `upscaled/Firefly_remove background 477817*.png` | 1535×2752, 768×1376 | RGBA | Firefly cut-outs of the hanging lemur |
| `upscaled/resort.png` | 3600×4802 portrait | RGB | 2× of the licensed aerial; needs 16:9 |
| `upscaled/playful-ringtailed-lemurs….mov` | 3840×2160, 30 fps, 10 s | H.264 | licensed stock |
| `upscaled/ring-tailed-lemur-grazing….mp4` | 1920×1080, 25 fps, 32.8 s | H.264 | licensed stock |
| `upscaled/ringtail-lemur-looking-around….mov` | 3840×2160, 29.97 fps, 6.0 s | H.264 | licensed stock |
| `upscaled/ring-tailed-lemurs-perched….zip` and `…/836ec439….mov` | 4096×2160, 24 fps, 57 s (probed remotely) | H.264 | licensed stock, twice (681 MB each) |
| root: three `ring-tailed-lemur-…-utc.jpg` | 4500×3000, 6000×4000, 2222×3332 | JPEG | licensed stock stills |
| `195288a0….png`, `Miavana_©_Dylane_Cabano_001-scaled.jpg` | 1254×1254, 1800×2401 | | originals |

### Untouched hotels (originals only, as the handoff says)
- **Versali**: three portrait plates 1023×1537 / 1024×1536 (cake+chandelier, cake+guillotine ×2 identical, cake sliced), `fd1e32ee` 1024×1536 elements on black, Hall of Mirrors webp 1170×780, wordmark jpgs 554×554 and 447×447.
- **Passalaqua**: `b74514e7` villa 1536×1024, `46e10c0f` fish leap 1421×1107, mark jpgs 410×319 and 275×183.
- **North Island**: three plates 1536×1024 (two with the wordmark burned in), `download.jpg` mark 225×121.
- **Necker Island**: Virgin mark jpg 1320×1240, five docx (speeches, itinerary, questions, `Animation Virgin.docx`), two PDFs (schedule 6 MB, "Iconic Leadership Summit 26" 62 MB). No flamingo, no island plate.
- **22 club**: `images.png` 364×549 palette PNG. Nothing else.

## 5. Open questions — updated

Answered by measurement:
- **Q5 (which giraffe file is the master):** the `.mov`. It is ProRes 4444 with alpha. The mp4 is a proxy.

Still open, carried forward:
1. **Frame rate.** Timing doc assumes 24. Kling gave 30 for the giraffe and 24 for the others. Delivery fps decides whether the 4K/30 walk gets conformed with optical flow.
2. **Assembly tool.** AE or Resolve. Not stated anywhere in the folder.
3. **Vector logos.** None exist in the folder for any of the eight hotels. Every wordmark currently on disk is a raster ≤ 554 px or an AI redraw. Has the ask gone to the clients?
4. **Which Necker concept** — flamingo brief or `Animation Virgin.docx` (the latter is a Virgin brand-history piece ending on Necker; different film).

New from this pass:
5. **Master aspects.** Storyboards page says 1:1 + 9:16 + 16:9. Handoff says HD 16:9 settled. Which?
6. **Run-time source of truth.** Storyboards page (12.0 / 11.0 / 12.5 / 14.0 / 13.0 / 12.0 / 13.0 / 12.0 s) or timing doc (14.0 / 12.0 / 13.0 / 15.0 / 13.0 / 12.0 / 14.0 / 12.1 s)?
7. **Giraffe Manor payoff.** Interior breakfast window (storyboards) or exterior upstairs windows (timing doc Shot 7)?
8. **Miavana lemur positions.** M + final A (PSD, storyboards) or first A + final A (handoff, timing doc)?
9. **`resort.png` outpaint.** It is a licensed photograph. Are the rights clear for generative extension, or should it be cropped to 3600×2025?

## 6. Recommended next steps

1. **Decide §5 items 5–8 first.** They change the Giraffe Manor end plate, the Miavana composition, and whether three masters are being cut.
2. **Giraffe Manor.** The walk (Shot 3) is done and on alpha. Next generation targets are Shot 6 (the turn, over-generate) and Shot 7. Use `manor01_background.png` as the Shot 4/5 plate only if guests in frame are acceptable; otherwise generate the clean plate the storyboards ask for. Stop using the AI wordmark; comp the real mark as an AE layer once vector arrives.
3. **Fifth Avenue.** Comp is ready in `turtlewalkers.psd`. Generate Shot 5 figure motion from the separated layers at normal speed, retime in the NLE. Title card waits on vector.
4. **Miavana.** Rebuild the lock-up with the large cut-outs (`lemur.png`, `lemur2.png`, `lemur3.png`) instead of the 600 px lemurs currently in `miavana.psd`. Regenerate the throw and the sway **on sage, landscape, at the highest Kling resolution available**; the existing 720×1280 clips prove the motion but will not hold up at HD. Then Shot 3, the letters-to-palms dissolve, from two NBP end plates built from the same composition.
5. **Housekeeping (ask before doing):** delete the four duplicate files, the empty `.ai`, one of the two 681 MB stock copies; rename the mislabelled JPEG.

## 7. How to use what was added to the repo

| Path | What |
|---|---|
| `drive/manifest.json` | every file in the Drive folder: path, id, bytes, modified time; folder ids |
| `tools/drive_pull.py DEST [--max-mb N] [--only SUBSTR] [--dry-run]` | mirror the folder locally over the public link; stdlib only; skips files already present at the right size. Ran here: 111 downloaded, 0 failed |
| `tools/measure.py ROOT -o out.json --md out.md` | dims / alpha bbox / video probe / sha256 for a tree. Needs Pillow; ffprobe for video. Ran here on the pull |
| `tools/r2_upload.py ROOT [--prefix P] [--dry-run]` | mirror a local tree into R2 via boto3 using the four `R2_*` env vars. **Untested** against R2 |
| `inventory/measurements_2026-09-25.{json,md}` | the measurements |
| `inventory/psd_layers_2026-09-25.md` | layer names, bboxes, sizes for all five PSDs |
| `inventory/storyboards_rendered_text_2026-09-25.txt` | full text of the storyboards page |
| `inventory/previews/` | 100 % crops of the logo rasters, frame grabs from the four generated clips, plate thumbnails, storyboards page screenshots |
| `docs/INVENTORY_2026-09-25.html`, `.pdf` | this document |

Works on Windows, macOS and Linux; paths are relative; nothing is hardcoded. Python 3.9+.

## 8. What was left out, and why

- **No R2 upload happened.** No credentials in this session and the Cloudflare connector is unauthorised. Script provided, untested.
- **The 681 MB zip was not downloaded**; its extracted `.mov` sibling was probed over HTTPS instead. Everything else was downloaded in full.
- **Nothing in the Drive folder was modified, renamed or deleted.** Duplicates and the empty `.ai` are listed, not removed.
- **The five Necker docx files and the two PDFs were downloaded but only `Animation Virgin.docx` and the client brief were read.** The speeches, itinerary and the 62 MB summit PDF look unrelated to the animation.
- **No generation, no comp, no retime was done.** This is measurement and reading only.
- **The `hf_20260909_*` renders in the Giraffe Manor root were measured but not inspected visually** beyond `86df0845` (the wordmark) and `025934` (= manor01).
- **PSD layer reads are bounding boxes only.** Blend modes, layer effects and smart-object contents were not checked (none appeared to exist, but psd-tools warned about an unknown `caiM` metadata key, which is Content Credentials, not layer data).
- **Storyboards page images were not extracted individually.** They are blob URLs inside the bundle; the four page screenshots cover them.
