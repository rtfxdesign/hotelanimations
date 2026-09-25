## Read this first — decisions that cut across all eight films

Each film section below has its own frames, beat table, review notes and open questions. These are the calls that affect more than one film. Nothing below has been decided; the boards follow the timing doc where the documents disagree.

| # | Decision | Why it matters | Boards affected |
|---|---|---|---|
| 1 | **Run times: timing doc or storyboard page?** Timing doc: 14.0 / 12.0 / 13.0 / 15.0 / 13.0 / 12.0 / 14.0 / 12.1 s. Page: 12.0 / 11.0 / 12.5 / 14.0 / 13.0 / 12.0 / 13.0 / 12.0 s | Every frame range in every beat table moves | all except North Island and Miavana |
| 2 | **One master (16:9 HD) or three (1:1, 9:16, 16:9)?** The page header says three; the handoff says HD settled | Several payoff frames do not survive a 1:1 crop (Giraffe Manor 06–07, Fifth Avenue walk, Passalacqua leap) | all |
| 3 | **Frame rate 24 or 30.** Boards are at 24 (timing doc). The one Kling clip delivered so far is 30 | Conform of every Kling clip; the 22 Club beat grid | all |
| 4 | **Vector logos.** None exist for any hotel. Every logo on every board is a tagged raster placeholder (web thumbnails at 2×, or AI redraws that were not used) | Blocks every "logo appears / disappears" beat in all eight briefs | all |
| 5 | **Loop rule.** The page says every film ends on its opening frame. The timing doc ends Fifth Avenue, Passalacqua and Versailles on a different end card | Changes the last beat of three films | Fifth Avenue, Passalacqua, Versailles |
| 6 | **Source files are mislabelled in the timing and pipeline docs.** Versailles: chandelier / guillotine / isolated / plated are swapped across all four files. Passalacqua: the "leap" file is the lock-up render, the "villa" file is the leap, `images-3.jpg` is a villa photo not the mark, and the villa may be Balbianello, not Passalacqua. North Island: turtle count is 5 / 3 / 4 across plates, page and doc, and the two lock-up plates do not register. Fifth Avenue: the isolated tortoise and the plate's tortoise are different renders | The boards use what is actually in the files; the docs need correcting before generation | Versailles, Passalacqua, North Island, Fifth Avenue |
| 7 | **Licensed photo, generative extension.** Miavana `resort.png` is a 2× of the © Dylane Cabano aerial and is portrait; 16:9 needs an outpaint or a crop that loses 58 % of its height | Rights question before any model touches it | Miavana |
| 8 | **Which Necker concept is live** — the flamingo brief (boarded) or `Animation Virgin.docx` (not boarded). And which mark signs off | Whole film | Necker Island |
| 9 | **22 Club: ivory or black ground, and lock the track first.** Every frame number is at 124 BPM; any other tempo moves all of them | Beats 2–5 | 22 Club |

### One line per film

- **01 Giraffe Manor** — walk cycle exists on alpha at 4K. Revised staging: manor fades in at scale, camera pulls back. Decide the window payoff (exterior vs interior) and note the walker is a darker giraffe than the hero.
- **02 Fifth Avenue** — layers are separated and placed. The two tortoises don't match; use the plate's own tortoise as the hero (frame 01b). Lockup has no room under the feet at plate scale; boarded with a 1.33× pull-out.
- **03 Passalacqua** — no clean lake plate and no mark above 410 px exist. Confirm the villa is the right one before generating anything.
- **04 Versailles** — the two salon plates do not register, so the morph cannot be a blend of them. Recommend one clean empty salon plus cake / chandelier / guillotine as layers.
- **05 North Island** — wordmark is burned into two plates and is an AI serif, not the house mark. Regenerate clean and comp the type. Settle the turtle count.
- **06 Miavana** — seated lemur on the M (PSD, page) or first A (timing doc); both boarded. The 720×1280 Kling clips prove the throw but are below HD; cheapest route is a Flux mango on a 2D arc over breathing stills.
- **07 Necker Island** — nothing exists but the Virgin script. Schematic board with screen fractions; lemur tennis is the riskiest generation in the slate, AE fallback boarded.
- **08 22 Club** — the two 2s are too close together to become two readable decks without drifting apart as they fall. Ground colour decides the spotlight beat.

### How to use this page

Frames are 960×540 previews; the 1920×1080 PNGs and each film's `build_frames.py` are in the repo under `<film>/storyboard/`. Orange tags on a frame mean placeholder, comp, or to-generate; untagged frames are built from a supplied asset as-is. Nothing here is animated yet. Answers to the nine decisions above unlock the animatics.
