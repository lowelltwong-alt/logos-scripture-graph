# Multi-Model Whole-Bible Chunking Fork (Scratch Pad)

**Fork ID:** `whole_bible_multi_model_chunking_v1`  
**Policy:** `.ai/control/multi_model_whole_bible_chunking_fork.yaml`  
**Status:** experimental — revert to T410 baseline if fork fails

## What this is

3–10 AI models each chunk the **entire raw Bible** independently in **separate folders** (start with 5; scale to 10 if useful). All start from the **same research baseline** (literature types, grammar, Strong's, Greek/Hebrew tags, Jesus words/red-letter, observation substrate, lessons already discovered).

Later we **compare** outputs:
- **Agreement** → easy chunks (low-friction candidates)
- **Disagreement** → where governed T410/T402 work should focus

## Folder layout

```
.ai/scratch/multi_model_bible_chunking/
  manifest.yaml
  shared_research_baseline/     ← same starting research for every model
  comparison/                   ← agreement vs disagreement (built after models run)
  M1_cursor/                    ← Cursor/Composer pass 1
  M2_codex/                     ← Codex pass
  M3_claude/                    ← Claude pass
  M4_gemini/                    ← Gemini pass
  M5_composer/                  ← optional 5th independent pass
```

## Per-model outputs (required)

Each model folder must contain:

| File | Purpose |
|------|---------|
| `model_manifest.yaml` | Model id, status, timestamps |
| `whole_bible_chunk_map.jsonl` | One JSON object per proposed chunk span |
| `layer_decision_log.jsonl` | Transparent boundary decisions |
| `marathon_progress.yaml` | Per-book completion for set-and-forget marathon |
| `model_summary.md` | Human-readable rollup |

## Non-authorizations

Scratch maps are **not** reviewed gold, **not** `data/canonical/` chunks, **not** `eval/chunking_gold/`. Promotion requires separate governed PR.

## Parallel work

Batch2 multi-model ladder (`.ai/context/agent_work/T417/model_layers/batch2/`) continues alongside this fork.
