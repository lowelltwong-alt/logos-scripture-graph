# Shared Research Baseline — Multi-Model Whole-Bible Chunking Fork

All models **M1–M10** must read `research_baseline_manifest.yaml` before starting their marathon.

## Same starting point

Every model gets the same:
- Raw WEB USFM (`data/raw/bible/eng-web/`)
- Rust observation substrate ledgers
- Chunking design, preflight, lesson index
- Stress atlas, T411 escalation discoveries
- Literature-type and marker rules (Strong's, wj, paragraph markers)

## Continuous marathon rule

Run **straight through all 66 books** in your model folder. Days-long runs are expected. Update `marathon_progress.yaml` after each book.

## Outputs (your folder only)

| File | Purpose |
|------|---------|
| `whole_bible_chunk_map.jsonl` | One JSON line per proposed chunk span |
| `marathon_progress.yaml` | Book completion tracker |
| `layer_decision_log.jsonl` | Transparent boundary decisions |
| `model_summary.md` | End-of-run summary |

## After all models finish

Comparison scripts populate `comparison/`:
- **Agreement** → easy/consensus chunks
- **Delta** → disagreement focus queue for governed work

## Non-authorizations

Scratch chunk maps are not canon. Revert to T410 baseline if fork fails.
