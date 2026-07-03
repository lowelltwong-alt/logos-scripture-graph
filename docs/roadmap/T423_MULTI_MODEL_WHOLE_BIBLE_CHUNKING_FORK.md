# T423 — Multi-Model Whole-Bible Chunking Fork (Experimental)

## Why this fork exists

Speed up chunking by running **3–10 AI models** in **separate scratch folders** (initial target **5**), each doing a **continuous whole-Bible marathon** (days acceptable) from the **same research baseline**. Then:

- **Agreement** → easy/consensus chunks (low governed effort)
- **Delta** → disagreement focus queue (where T410 work concentrates)

If the fork fails → **revert to** `.ai/control/parallel_chunking_research_program.yaml` (original batch ladder).

## Scratch layout

```
.ai/scratch/multi_model_bible_chunking/
  manifest.yaml
  shared_research_baseline/     # same starting research for all models
  M1_cursor/                    # independent chunk map
  M2_codex/
  M3_claude/
  M4_gemini/
  M5_composer_alt/              # optional 5th
  comparison/                   # agreement vs delta (after marathons)
  redteam/                      # pre-mortem reports
```

## Policy

`.ai/control/multi_model_whole_bible_chunking_fork.yaml`

## Marathon prompt

`.ai/prompts/multi_model_whole_bible_chunking_marathon_prompt.md`

## Red-team before marathons

`.ai/prompts/multi_model_whole_bible_chunking_redteam_premortem_prompt.md`

Red-team report: `.ai/scratch/multi_model_bible_chunking/redteam/REDTEAM_PREMORTEM_REPORT.md` (HOLD → fixes applied).

## Set-and-forget marathon flow

1. Init progress: `python scripts/t423_init_marathon_progress.py M1_cursor`
2. Run marathon prompt per model folder (all 66 books, substrate-first)
3. Status: `python scripts/t423_marathon_status.py`
4. Compare: `python scripts/compare_multi_model_bible_chunk_maps.py`

## Rust substrate (required)

Read `build/observation_substrate/current/` before chunking. Future Rust compare acceleration planned; Python compare is canonical for now.

## Parallel work

T417 batch2 scratch ladder continues separately under `.ai/context/agent_work/T417/model_layers/`.

## Non-authorizations

Scratch chunk maps are not canon. Agreement does not auto-promote gold or output.
