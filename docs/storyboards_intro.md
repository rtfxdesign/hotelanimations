## Decisions taken (v2, 2026-09-25)

Allen ruled on the nine cross-slate questions from v1; the rest are judgement calls made in the boards and stated per film. Nothing below is open.

| # | Decision | How the boards apply it |
|---|---|---|
| 1 | Run times: whatever is convenient | Timing-doc run times kept; each film gains a short return beat where the loop needed one, and the new TRT is stated in its header |
| 2 | One master, 16:9 | 1920×1080 only. No 1:1 or 9:16 reframes |
| 3 | 24 fps | All frame numbers at 24. The 4K/30 giraffe walk gets an optical-flow conform |
| 4 | Vector wordmarks for most hotels; rasters fine for the rest | Vectors received for Giraffe Manor, Fifth Avenue, Miavana, Passalacqua and 22 Club, rasterized at `assets/wordmarks/`. Versailles, North Island and Necker use their rasters, tagged "approved raster". No placeholders remain |
| 5 | Loop rule matters; add tween frames | Every film now ends on a frame pixel-identical to its first. Fifth Avenue, Passalacqua, Versailles, Giraffe Manor and Necker gained explicit return beats |
| 6 | Rename files if needed | Drive is untouched. The Necker uploads and two Kling clips have clean local names in `drive/manifest.json` with the original Drive title recorded alongside |
| 7 | Ignore licensing | Miavana uses Allen's new 16:9 outpaint of the aerial (`resort_16x9.png`) |
| 8 | Ignore Animation Virgin; use the client brief | Necker is boarded from the brief only, now with the real photo set and the bow-tied flamingo cut-out |
| 9 | Black background | 22 Club opens and closes on black. Versailles opens and closes on its black-field cake |

Judgement calls made without asking: both Giraffe Manor giraffes are colour-matched (the walk will be regenerated from the hero as reference); the Giraffe Manor payoff is the exterior upstairs windows; Fifth Avenue's hero is the plate's own tortoise; Miavana's seated lemur stays on the M; North Island keeps five turtles; Passalacqua's fish breach staggered; Versailles drops the Hall of Mirrors end card in favour of the loop.

## What changed in the Drive folder since v1

- Vectors: `wordmark.ai` (Giraffe Manor, plus a PSD and a 3D extrusion), `fifthave_wordmark.ai` (plus rendered gold type and a 3D extrusion), `miavana_wordmark.ai`, `passalacqua_wordmark.ai` (plus a gold-fish render and layered PSDs), `22club_wordmark.ai`.
- Plates: `resort_16x9.png` (Miavana, outpainted 16:9), `northisland.png` (clean 2× water plate), `flamingo.png` (Necker cut-out on alpha, bow tie).
- Necker photo set: 22 hotel photographs (flamingos, lemurs, tennis court, kite and foil surfing, aerials, villas) plus press kit, brochure and rate card.
- Audio: birdsong ×2 (Giraffe Manor); clocks, harp glisses and a carriage pass-by (Fifth Avenue).
- Kling: two new hero micro-life takes for Giraffe Manor Shot 1.

### How to use this page

Frames are 960×540 previews; the 1920×1080 PNGs and each film's `build_frames.py` are in the repo under `<film>/storyboard/`. Orange tags on a frame mean comp or to-generate; untagged frames are built from a supplied asset as-is. Nothing here is animated yet. The next step after sign-off is the Giraffe Manor animatic.
