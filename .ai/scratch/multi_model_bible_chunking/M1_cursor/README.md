# M1 Cursor — Whole-Bible Chunk Marathon

**Model:** Cursor (Composer) | **Status:** `pending_marathon_start`

## Run

1. Read `../shared_research_baseline/research_baseline_manifest.yaml`
2. Follow `.ai/prompts/multi_model_whole_bible_chunking_marathon_prompt.md`
3. Chunk all 66 books continuously into `whole_bible_chunk_map.jsonl`
4. Update `marathon_progress.yaml` after each book

## Files

| File | Status |
|------|--------|
| `model_manifest.yaml` | scaffold |
| `whole_bible_chunk_map.jsonl` | empty — append per chunk |
| `marathon_progress.yaml` | book tracker |
| `layer_decision_log.jsonl` | decision transparency |
| `model_summary.md` | write at end |

Do not read other model folders until your marathon is complete.
