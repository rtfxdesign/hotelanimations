# Handoff: run the Theria generation kit through the Higgsfield MCP (local session)

Written 2026-09-25 by the cloud session on branch `claude/wizardly-edison-00x4h8` (PR #3). The cloud session has no Higgsfield credentials or connector. A local session with the Higgsfield MCP does the generation; everything else is prepared.

## What exists

- `generation_kit/PROMPTS.md` (+ `.html`, `.pdf`): every asset still to generate, film by film, with the frame to feed and the prompt. Human-readable source of truth.
- `generation_kit/jobs.json`: the same prompts as 34 machine-readable jobs. Each job has `id`, `film`, `phase` (A or B), `endpoint` (Higgsfield endpoint id), `inputs` (kit frames, or `out:JOB[:first_frame|last_frame]` for phase B), `args`, `prompt`, `takes`.
- `generation_kit/0N_<film>/`: the 35 input frames, committed on the branch (122 MB). A plain clone has them; no zips needed.
- `tools/higgsfield_run.py`: REST runner (needs `HF_KEY`). Use it if the MCP is unavailable; otherwise it is only a reference for the request shapes. `--dry-run` prints the full plan without network.
- `generation_kit/README_higgsfield.md`: model choices and phase rules.

## Model mapping (change only if the MCP exposes different endpoints)

| jobs.json endpoint | Purpose | Key args |
|---|---|---|
| `kling-video/v3.0/pro/image-to-video` | all I2V; `image_url` first frame, optional `last_image_url` | duration 5, sound off, cfg 0.5 |
| `alibaba/qwen-image-3/edit` | edits with 1–3 reference images | resolution 2k, aspect per job, prompt_extend false, enable_thinking false, negative_prompt |
| `alibaba/qwen-image-3/text-to-image` | pure T2I | same |

## Procedure

1. Run one cheap image job first (CL-2) to confirm the MCP, then the rest of phase A.
2. Takes: 1 each on the first pass, 2 for GM-2 and FA-1 (the risk shots). Do not raise takes without Allen's OK; spend is his call.
3. Save outputs as `generation_kit/output/<film>/<jobid lowercase, hyphen to underscore>_t<take>.<mp4|png>` and append to `generation_kit/output/ledger.json` (`{"JOB#take": {job, take, film, endpoint, request_id, status, url, file}}`). The cloud session's animatic tooling reads these paths.
4. Phase B after Allen picks takes: GM-1v (from GM-1s), GM-4 (first = last frame of chosen GM-2 take, last = GM-3), PA-4 (from PA-1), NI-2 (from NI-1), NI-4 (first = last frame of NI-3, last = first frame of NI-3), MI-1b/MI-1c (from MI-1a), NE-3 (from NE-2). Pull frames with `ffmpeg -sseof -0.2 -i in.mp4 -update 1 -frames:v 1 last.png`.
5. Not runnable by prompt alone: PA-3 (comp the three gold fish from `passalacqua.png` onto the PA-1 plate first). Logos never go through a model.
6. Inputs with alpha: flatten onto white before upload. `mi_ref_resort_16x9.png` is 4988 px and 26 MB; downscale to 4096 wide if the MCP rejects it.
7. When done: contact sheet of all outputs, list of failed or NSFW-flagged jobs, and commit `output/ledger.json` only (outputs stay out of git, `generation_kit/*/` is ignored). Upload outputs to the Drive folder `Theria` > `generated` only if Allen says so.

## Rules carried over

- No likeness of any real person (NE-2 rider is generic). No wordmark through a model. Never AI-enlarge a client logo.
- Ask before spending beyond the counts above, before deletes, and before any upload to Drive.
