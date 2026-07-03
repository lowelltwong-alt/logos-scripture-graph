# Comparison — Agreement vs Delta

Run comparison **after** models complete marathons (or owner requests interim compare on completed books).

## Set-and-forget flow

1. Each model runs M1–M5 (or M6–M10) marathons independently → `whole_bible_chunk_map.jsonl`
2. Check readiness: `python scripts/t423_marathon_status.py`
3. Compare: `python scripts/compare_multi_model_bible_chunk_maps.py`
4. Governed T410 work reads `disagreement_delta.jsonl` only — not consensus spans

## Outputs

| File | Meaning |
|------|---------|
| `agreement_chunks.jsonl` | Spans where models agree → **easy/consensus chunks** (`promotion_authority: none`) |
| `disagreement_delta.jsonl` | Spans where models split differently → **focus here** |
| `delta_focus_queue.yaml` | Prioritized governed-work queue from disagreement |
| `model_agreement_matrix.yaml` | Per-book agreement rates |
| `delta_summary.md` | Human/AI audit summary |

## Rules

- **Minimum compare:** 3 complete models (`--interim`)
- **Default compare:** 5 complete models (initial target)
- **Maximum:** 10 models — add via `models/_TEMPLATE/` → `M6_*` … `M10_*`
- **Full consensus:** exact same span across **all** complete models (N)
- **Easy bucket:** exact same span across **≥ ceil(0.7 × N)** models (N=10 → 7 agreeing)
- **At N=3:** easy bucket requires 3/3 (same as full consensus)
- **Delta:** any boundary mismatch, split count difference, or span overlap disagreement
- **Governed work (T410):** targets `disagreement_delta.jsonl` only — not consensus spans

## Scripts

```bash
python scripts/t423_marathon_status.py
python scripts/compare_multi_model_bible_chunk_maps.py
python scripts/compare_multi_model_bible_chunk_maps.py --interim   # before 5 models done
python scripts/compare_multi_model_bible_chunk_maps.py --book Phlm --book Jude
```

## Non-authorizations

Agreement does not auto-promote to `eval/chunking_gold/` or chunk output.
