# Multi-Model Whole-Bible Chunking — Continuous Marathon Prompt

**Mode: set-and-forget.** Run straight through all **66 books** in one long session. Days are fine. Do not stop for owner gates.

## Your assignment

1. Read `shared_research_baseline/research_baseline_manifest.yaml` first; set `research_baseline_read: true` and record `research_baseline_manifest_sha256` in `model_manifest.yaml`.
2. Read **Rust observation substrate** under `build/observation_substrate/current/` (book + verse observations, span features, risk signals). Do **not** reread the whole raw USFM unless you log an exception in `layer_decision_log.jsonl`.
3. Work **only** in your model folder (e.g. `M1_cursor/`).
4. Chunk **100% of the WEB Bible** (all 66 canonical books) into proposed parent spans.
5. Append each chunk to `whole_bible_chunk_map.jsonl`.
6. Update `marathon_progress.yaml` after **each book** — mark `book_completion.<Book>.status: complete`.
7. Log every non-obvious boundary in `layer_decision_log.jsonl`.
8. Do **not** read other models' maps or `.ai/scratch/multi_model_bible_chunking/comparison/` until your marathon is complete.

## Isolation (mandatory)

- Do **not** read `.ai/context/agent_work/T417/model_layers/batch2/` (parallel ladder — separate experiment).
- Do **not** treat T417 strengthened packets as authority for your spans.
- Your map is scratch only; agreement with other models does not promote gold.

## Chunk map line format (JSONL)

```json
{
  "model_id": "M1_cursor",
  "book": "Gen",
  "span": "Gen.1.1-Gen.1.31",
  "chunk_index_in_book": 1,
  "literature_type_guess": "narrative",
  "boundary_evidence_refs": ["paragraph_marker", "observation_substrate:Gen.1.1"],
  "strong_or_hebrew_tags_used": false,
  "wj_or_red_letter_considered": false,
  "frontier_flag_considered": false,
  "confidence": "medium",
  "decision_id": "M1-GEN-001",
  "rationale": "Creation week narrative unit",
  "alternatives_rejected": ["split at Gen.1.2"],
  "might_be_wrong": "Genealogy boundary at ch2",
  "non_authorizing": true
}
```

For **Dan** and **Rev**, set `frontier_flag_considered: true` and note apocalyptic pressure in `layer_decision_log.jsonl`.

## Research you must apply

- Literature type (narrative, poetry, epistle, law, prophecy, wisdom, apocalyptic)
- Grammar/discourse and USFM paragraph markers (evidence only)
- Strong's G/H tags (evidence only, not theology authority)
- Words of Jesus / red-letter where relevant in Gospels
- Source metadata never becomes boundary authority alone
- Theology pressure from T411-style escalations = evidence only
- Textual variants / DSS / alternate readings = evidence only (see baseline manifest)

## Speed rule

**One continuous run through all 66 books.** Finish before comparing to other models.

Validate as you go:

```bash
python scripts/validate_whole_bible_chunk_map.py <your_model_folder> --model-id <M_id>
```

## When done

1. Write `model_summary.md`.
2. Set `marathon_progress.yaml` → `marathon_status: complete` and `books_completed: 66`.
3. Run full-bible validation:

```bash
python scripts/validate_whole_bible_chunk_map.py <your_model_folder> --require-full-bible
```

Owner or integrator runs compare when enough models finish:

```bash
python scripts/t423_marathon_status.py
python scripts/compare_multi_model_bible_chunk_maps.py
```

Use `--interim` only for early signal before 5 models complete.

## Non-authorizations

- No writes to `eval/chunking_gold/`, `data/candidate/chunks/`, or `pipelines/chunking/`
- Your map is scratch suggestion only
- Agreement with other models does not auto-promote to canon
