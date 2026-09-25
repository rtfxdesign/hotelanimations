# Running the kit on Higgsfield

`jobs.json` maps every prompt in `PROMPTS.md` to a Higgsfield endpoint. `tools/higgsfield_run.py` uploads the frames, submits, polls and downloads into `generation_kit/output/<film>/` with a ledger at `output/ledger.json`.

Models (chosen 2026-09-25 from the Higgsfield catalogue):

| Kind | Endpoint | Used for |
|---|---|---|
| Video, image to video, optional last frame | `kling-video/v3.0/pro/image-to-video` | every I2V item, 5 s, sound off |
| Image edit with 1–3 references | `alibaba/qwen-image-3/edit` | clean plates, isolations, outpaint, lemur placements |
| Text to image | `alibaba/qwen-image-3/text-to-image` | mango, 22 Club objects |

Phases: A = inputs are kit frames. B = inputs are phase-A outputs (`out:JOB`, `out:JOB:first_frame`, `out:JOB:last_frame`). Takes default to 1 for a QC pass; raise with `--takes`.

```
export HF_KEY="<key id>:<key secret>"      # from console.higgsfield.ai, never on the command line
python3 tools/higgsfield_run.py --dry-run --phase A
python3 tools/higgsfield_run.py --phase A
python3 tools/higgsfield_run.py --phase B --pick GM-2=2   # after choosing takes
python3 tools/higgsfield_run.py --resume                  # re-poll anything unfinished
```

Not run by the script: PA-3 (needs the PA-1 plate with the three gold fish comped first), the Passalacqua and Versailles AE beats, all logos.
