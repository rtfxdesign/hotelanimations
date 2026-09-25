# Theria Hotel Animations — Handoff to Claude Code
Written 2026-09-25 from the Cowork session. Read this first, then the two companion docs in this folder.

## Working rules (Allen's)
Correct beats fast. Lead with the answer. Verify by running — say "untested" if you didn't. Document as you go (what, where, what was run). End every piece of work with what was left out and why. Cross-platform, no hardcoded paths. Boring over clever; concrete over abstract. **Ask before anything irreversible** (delete, overwrite, send, spend). Never AI-enlarge a client logo — vector only.

## Project root
`K:\My Drive\dj_allen\theria\Hotel Animations\`  (Google Drive, Windows desktop "hapexamendios")
One subfolder per hotel. Convention Allen has started: `orig/` = source files as received, `upscaled/` = enlarged and layer-separated working files (PNG layers + the PSD they came from).

## Companion docs (same folder)
- `theria_hotel_animations_timing_v1.md` — shot-by-shot timings, 24 fps, all 8 films. **Source of truth for cuts.**
- `theria_higgsfield_asset_pipeline_v1.md` — model routing, prompts, per-shot Kling segments. **One correction, see below.**
- `Theria Hotel Animation Storyboards.html` (16 MB) — Allen's storyboard page. Not read by this session; open it.
- `Sample Hotel Animations_.docx` — the original client brief (the 8 numbered lists).

## CORRECTION: delivery target is HD, not 4K
Allen confirmed 2026-09-25: **target is HD — 1920×1080.** The pipeline doc assumed 3840×2160 throughout. Consequences:
- The 1536×1024 source plates are already 80% of HD width. A 1.25× enlargement is all they need. Most of §3's "re-render at 4K" is now unnecessary — a conventional upscale (Topaz / Photoshop Super Resolution) is enough and safer.
- Portrait plates (Giraffe hero 1024×1536, the three Versailles plates 1023×1537) still need **outpainting to 16:9**. That job survives; the scale part of it doesn't.
- Kling native output (typically 1080p) is delivery-res. No video upscale step.
- Logos still need vector. HD doesn't change that.
- Ignore every "target 3840×2160" line in the pipeline doc. Everything else in it stands.

## Tools / pipeline (stated by Allen)
- Generation: **Higgsfield** — unlimited on Seedream 4.5, Nano Banana Pro, Flux 2.0 Pro, Kling 01. Routing: Flux for the object, Seedream for the world, NBP for anything with type in it, Kling for the move.
- Layer separation is being done in Photoshop (PSDs present).
- Assembly presumed After Effects / Resolve — not confirmed. Ask.
- Frame rate 24 fps assumed in the timing doc — not confirmed. Ask.
- Aspect 16:9 assumed — HD confirms 1920×1080, so 16:9 is now settled.

## Inventory as of 2026-09-25 (from directory listing — sizes only; pixel dims NOT measured, do that first)
Files in the three active hotels. Skipped: `.DS_Store`, `desktop.ini`.

### Giraffe Manor — furthest along
`upscaled/`
| File | Size | What it is (inferred from name — verify) |
|---|---|---|
| `manor01.psd` | 26 MB | master comp of the manor plate |
| `manor01.png` | 11 MB | flattened manor plate |
| `manor01_background.png` | 10 MB | manor with giraffes removed |
| `manor01_giraffe01.png`, `manor01_giraffe02.png` | 129 KB / 397 KB | the two giraffes cut out. Small — check they're full-res, not thumbnails |
| `giraffemanor_wordmark_alpha.png` | 596 KB | wordmark on alpha. Raster — origin unknown; if it came from the 288×46 webp it's unusable. Check |
| `hf_…86df0845….ai` | **703 bytes** | an .ai that small is empty or a placeholder. Not a real vector logo. Flag |
| `frame01.png`, `frame02.png` | 575 / 694 KB | keyframes — likely Kling start/end pair |
| `giraffe_walking.mov` | 327 MB | Kling output, ProRes? |
| `giraffe_walking.mp4` | 18 MB | same, H.264 |
| `fadein.png` | 36 MB | ? |
| `ea5d5cfc….png` | 1.7 MB | original hero giraffe (1024×1536) |

Root of `Giraffe Manor/`: six `hf_20260909_*.png` Higgsfield outputs (0.3–42 MB), `fadein - resized….png`, two stock giraffe photos (`closeup-shot…jpeg` 15 MB, `striking-giraffe-profile….jpg` 3 MB), a Facebook-sourced `273559596…jpg` (13 KB, twice), `Hotel Animation Storyboards-selection.png`, and a 3.3 MB copy of the storyboards HTML. `orig/` holds only the 46 px logo webp.

### Fifth Avenue
`upscaled/` — layers separated, no motion yet
| File | Size |
|---|---|
| `turtlewalkers.psd` | 93 MB — master |
| `turtlewalkers.png` | 12 MB — flattened |
| `turtle.psd` / `turtle.png` / `turtle02.png` | 17 MB / 2.8 MB / 6.2 MB |
| `man.png`, `woman.png`, `leash.png` | 1.1 MB / 4.9 MB / 158 KB |
| `fifthave.psd`, `fifthavenue.png`, `fifthave_text.png` | 11.5 MB / 987 KB / 440 KB — logo work. Raster; same vector caveat |

`orig/` — the three source files unchanged.

### Miavana
`upscaled/` — most generation activity, least organised
| File | Size |
|---|---|
| `miavana.psd` | 3.6 MB — master lock-up |
| `miavana_0000_left_lemur.png` … `miavana_0005_Layer-0.png` | 19–171 KB — PS layer export: left lemur, right lemur, MIAVANA, ISLAND SANCTUARY, BY TIME+TIDE, background |
| `miavana_text.png`, `miavana_text - crop….png`, `miavana copy.png` | 6.2 MB / 163 KB / 502 KB |
| `lemur.png`, `lemur2.png`, `lemur3.png` | 4.5–4.8 MB — cut-out lemurs |
| `a ring-tailed lemur hanging upside-down by its tail*.png` ×3 | 1.9 / 17 / 1.9 MB — generated |
| `…hanging upside-down by its tail, natural motion, slow sway.mp4` | 1.5 MB — Kling |
| `…produces a mango, throws it up and to the right.mp4` | 1.5 MB — Kling. **The throw exists.** |
| `Firefly_remove background 477817*.png` ×2 | 434 KB / 1.2 MB |
| `resort.png` | 33 MB — resort plate, presumably outpainted/enlarged |
| Stock video: `playful-ringtailed-lemurs….mov` 79 MB, `ring-tailed-lemur-grazing….mp4` 38 MB, `ringtail-lemur-looking-around….mov` 32 MB, `ring-tailed-lemurs-perched….zip` 681 MB + its extracted `.mov` 681 MB | licensed stock — reference/plates |
| Stock stills: `ring-tailed-lemur-perched-on-a-wooden-surface….jpg` 3.4 MB | |

Root of `Miavana/`: three more stock lemur JPGs (3.7–8.7 MB) plus the original five files.

### Untouched since 2026-09-09
22 Club, Necker Island, North Island, Passalaqua, Versali — originals only. Nothing to do here yet.

## First commands to run (untested — write them, run them, fix them)
1. Measure every PNG/JPG in the three `upscaled/` folders: width × height × mode (PIL). The inventory above has none of that.
2. `ffprobe` the four MP4/MOVs that are generated (not stock): resolution, fps, duration, codec. Confirm Kling is handing back 1080p and what fps — this decides the conform.
3. Open `hf_…86df0845….ai` in a text editor. 703 bytes. Confirm it's empty.
4. Check `giraffemanor_wordmark_alpha.png` and `fifthave_text.png` at 100%. If the letterforms are soft or hallucinated, they were AI-enlarged and need replacing with vector.
5. Check that the `manor01_giraffe0*.png` cutouts are full plate resolution (129 KB is suspicious for a 1080p-plus alpha PNG).

## Immediate next steps, in order
**Giraffe Manor** (timing doc §1): keyframes and a walk cycle already exist. Review `giraffe_walking.mp4` against Shot 3. Then generate Shots 6 (the 180° turn — the risk shot, over-generate) and 7. Shots 2, 4 and 8 are AE comp (logo layers + dissolve to `manor01_background`).
**Fifth Avenue** (§2): all layers separated, zero motion. Next: Kling Shot 5 — the ultra-slow walk. Per the pipeline doc, generate the figures at normal speed and retime in the NLE with the background at 100%; do not ask Kling for slow motion. `turtle.png` is the Shot 1 start frame.
**Miavana** (§6): the mango throw and the sway exist as Kling clips. Next: rebuild the lock-up with lemurs on the **first A and last A** (Allen's "better positions"), then Shot 3 — the dissolve where letterform arches become palm trunks. Build both end plates from the same composition in NBP so positions match, then Kling only the dissolve.

## Open questions for Allen (carry forward)
1. Frame rate — 24 or 30?
2. Assembly tool — AE, Resolve, other?
3. Have vector logos been requested from the clients? The `.ai` in Giraffe Manor is 703 bytes.
4. Which Necker concept is live — the flamingo brief, or `Animation Virgin.docx`?
5. `giraffe_walking.mov` at 327 MB — keep as master, or is the mp4 the master?

## What this handoff does not contain
- No pixel dimensions, fps or codec data — the Cowork session could not shell into this folder (mount failed) and staging 300 MB of files for a measurement was stopped in favour of this handoff. Step 1–2 above replaces it.
- The storyboards HTML (16 MB) was never opened here. It may already answer some of the above.
- Nothing in this folder was modified by the Cowork session. Only the two `.md` docs were written into it, on 2026-09-25.
