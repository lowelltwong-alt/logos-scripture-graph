# Post-Fix Audit — T423 Whole-Bible Multi-Model Chunking Fork

**Role:** Independent auditor. You are NOT a marathon chunker. Verify the Fable-review fixes landed.

**Output file (required):** `.ai/scratch/multi_model_bible_chunking/redteam/POSTFIX_AUDIT_REPORT.md`

---

## Independence rules

1. Read implementation critically — assume gaps remain until verified.
2. Do **not** chunk the Bible. Do **not** write canon/gold surfaces.
3. Verdict: **GO_MARATHON_PILOT** | **HOLD** | **ABANDON_FORK**

---

## Mandatory reads

1. `.ai/control/multi_model_whole_bible_chunking_fork.yaml` — `execution_mode`, `pilot_gate`, `book_chunks` layout
2. `.ai/scratch/multi_model_bible_chunking/MARATHON_PLAYBOOK.md`
3. `.ai/prompts/multi_model_whole_bible_chunking_marathon_prompt.md`
4. `scripts/t423_chunk_map_utils.py` — `compare_book_verse_coverage`
5. `scripts/compare_multi_model_bible_chunk_maps.py`
6. `scripts/t423_merge_book_chunks.py`, `scripts/t423_resume_book.py`, `scripts/t423_marathon_supervisor.py`
7. `scripts/evaluate_t423_revert_signal.py`
8. `scripts/validate_t423_pilot_gate.py`, `scripts/validate_t423_parallel_isolation.py`
9. `tests/test_t423_chunk_map_compare.py`

---

## Must verify

1. **One model at a time** — each model has its own folder; `book_chunks/<Book>/chunks.jsonl`; no real-time two-model pairing during chunking
2. Compare regression tests pass; different chunk counts with same boundaries yield high verse-coverage (not 0%)
3. No whole-book `split_count_mismatch` deltas in fixture compare
4. `evaluate_t423_revert_signal.py` uses verse-coverage, not legacy index metric
5. Resume: supervisor + `t423_resume_book.py` documented; `--discard-incomplete` works
6. `validate_t423_pilot_gate.py` blocks full 66 before `pilot_gate.status: go`
7. `validate_t423_parallel_isolation.py` enforces offline batch compare policy
8. Marathon prompt does not require single infinite session
9. All agreement/delta rows carry `promotion_authority: none`
10. Batch compare runs only after all models save 66 books locally

---

## Required report structure

```markdown
# Post-Fix Audit — T423

## Executive verdict
GO_MARATHON_PILOT | HOLD | ABANDON_FORK

## Findings table
| ID | Severity | Area | Issue | Fix |

## Workflow audit (one model, book segments, batch compare last)

## Compare algorithm audit (verse-coverage)

## Minimum fixes before pilot

## Non-authorizations confirmed
```

---

## Non-authorizations (auditor)

- Do not authorize gold, chunk output, or canon writes
- Do not start marathons in your audit session
