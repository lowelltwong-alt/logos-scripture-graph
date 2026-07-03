# Comparison — Batch Offline Agreement vs Delta

**Only after** each model has saved all 66 books locally under `book_chunks/<Book>/chunks.jsonl` and merged maps.

**No real-time compare** during chunking — one model at a time.

## Batch flow

1. Each model finishes alone → `book_chunks/` per book → `t423_merge_book_chunks.py` → `whole_bible_chunk_map.jsonl`
2. Check readiness: `python scripts/t423_marathon_status.py`
3. Owner runs batch compare: `python scripts/compare_multi_model_bible_chunk_maps.py`
4. Revert signal: `python scripts/evaluate_t423_revert_signal.py`
5. Governed T410 work reads `disagreement_delta.jsonl` only

## Headline metric

**Verse-coverage agreement rate** (`overall_verse_coverage_agreement_rate`) — not chunk-index alignment.

## Outputs

| File | Meaning |
|------|---------|
| `agreement_chunks.jsonl` | Consensus spans (`promotion_authority: none`) |
| `disagreement_delta.jsonl` | Boundary disagreements → **focus here** |
| `delta_focus_queue.yaml` | Prioritized governed-work queue |
| `model_agreement_matrix.yaml` | Per-book verse-coverage rates |
| `delta_summary.md` | Human/AI audit summary |

## Rules

- **Minimum compare:** 3 complete models (`--interim`)
- **Default compare:** 5 complete models
- **Easy bucket:** ≥ ceil(0.7 × N) models exact same span
- **Delta kinds:** `boundary_shift`, `literature_routing_disagreement`, `coverage_gap` — not whole-book `split_count_mismatch`

## Scripts

```bash
python scripts/t423_marathon_status.py
python scripts/compare_multi_model_bible_chunk_maps.py
python scripts/evaluate_t423_revert_signal.py --pilot-only
python scripts/compare_multi_model_bible_chunk_maps.py --book Phlm --book Jude --book Jonah
```

## Non-authorizations

Agreement does not auto-promote to `eval/chunking_gold/` or chunk output.
