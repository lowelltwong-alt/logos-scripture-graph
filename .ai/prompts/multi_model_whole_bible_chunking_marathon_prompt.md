# Multi-Model Whole-Bible Chunking — One Model, Book-at-a-Time

**You are ONE model in ONE folder.** Chunk the entire Bible alone. Save each book locally, then move to the next. **Do not** compare with other models during your run.

The shared template is a contract, not an answer key. It standardizes required fields,
sidecars, evidence logging, and non-authorizations. It must not standardize your chunk
boundaries. Make independent literary-form decisions after considering the substrate,
book genre, local markers, Strong's metadata as evidence-only, and the quality protocol.

## Your folder layout

```
M1_cursor/                    # example — your model_id names this folder
  book_chunks/
    Gen/chunks.jsonl          # save this book, then move on
    Exod/chunks.jsonl
    ...
  book_strategy/
    Gen.md
    Exod.md
    ...
  low_confidence_register.jsonl
  frontier_escalation_queue.jsonl
  atlas_candidate_feed.jsonl
  model_quality_summary.md
  marathon_progress.yaml
  layer_decision_log.jsonl
  whole_bible_chunk_map.jsonl # merged only after all 66 books (owner/script)
```

Use the assigned folder exactly. Current planned lanes are:

- `M1_cursor` — completed Cursor/Composer pass.
- `M2_claude_sonnet5` — Claude Sonnet 5 medium/high.
- `M3_claude_frontier` — Claude Opus 4.8 or Fable 5 high.
- `M4_codex_gpt55` — Codex GPT-5.5 high.
- `M5_gemini_thinking` — optional Gemini/outside-family pass.
- `M6_fable5` — Fable 5 comparison pass and harness critique.

## Workflow (one book per session)

1. Read `shared_research_baseline/research_baseline_manifest.yaml`; set `research_baseline_read: true` in `model_manifest.yaml`.
2. Read `.ai/control/t423_literary_marker_quality_protocol.yaml`.
3. Read **Rust observation substrate** under `build/observation_substrate/current/`.
4. Work **only** in your model folder (e.g. `M1_cursor/`).
5. Find next book:
   ```bash
   python scripts/t423_resume_book.py <your_model_folder> --json
   ```
6. Write `book_strategy/<Book>.md` before chunking that book. Name the literary strategy, markers considered, Strong's metadata considered evidence-only, expected low-confidence regions, and any chapter-only fallback reason.
   Include an independent boundary rationale. Do not copy example spans or template order as boundary authority.
   For future reruns, include these T467 sections: `literary_form_decision_matrix`, `larger_unit_preservation_check`, `list_register_function_check`, `epistle_unit_check_if_applicable`, `source_metadata_evidence_only_check`, `over_split_risk_check`, and `sidecar_specificity_plan`.
7. Chunk **that book only**; write all chunks to `book_chunks/<Book>/chunks.jsonl`. Use `literary_marker_aware_v2`: prefer scene, legal unit, stanza/acrostic, oracle/vision, discourse, greeting/thanksgiving/body/closing, list/genealogy, or paragraph/stanza evidence where the substrate supports it. Chapter-only is allowed only as a logged fallback, never as a silent default.
8. For every low-confidence or marker-sensitive chunk, append rows to all three sidecars:
   - `low_confidence_register.jsonl`
   - `frontier_escalation_queue.jsonl`
   - `atlas_candidate_feed.jsonl`
   These rows are non-authorizing and consideration-only; do not edit the governed stress atlas.
9. Validate the book:
   ```bash
   python scripts/validate_whole_bible_chunk_map.py book_chunks/<Book>/chunks.jsonl --model-id <M_id> --book <Book>
   python scripts/validate_t423_literary_quality_protocol.py --model-folder <your_model_folder> --book <Book> --require-artifacts
   ```
10. Mark book complete:
   ```bash
   python scripts/t423_resume_book.py <your_model_folder> --mark-complete <Book>
   ```
11. If session ends, stop. Next session resumes at the next incomplete book.
12. If a book was half-written, discard before re-chunk:
   ```bash
   python scripts/t423_resume_book.py <your_model_folder> --discard-incomplete <Book>
   ```

Repeat until all **66 books** are complete.

## When all 66 books are done

```bash
python scripts/t423_merge_book_chunks.py <your_model_folder>
python scripts/validate_whole_bible_chunk_map.py <your_model_folder> --require-full-bible
```

Write `model_summary.md` and set `marathon_status: complete`.

**Do not run compare.** Owner runs batch verse-coverage compare only after **all** target models finish locally.

## Isolation (mandatory)

- Do **not** read other models' `book_chunks/` or `whole_bible_chunk_map.jsonl`.
- Do **not** read `.ai/scratch/multi_model_bible_chunking/comparison/`.
- Do **not** read `.ai/context/agent_work/T417/model_layers/batch2/`.
- Use an isolated git worktree per model slot (`scratch/t423-M1-cursor`, etc.).

## Chunk line format (JSONL in `book_chunks/<Book>/chunks.jsonl`)

This is a schema example only, not a recommended Genesis boundary.

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
  "non_authorizing": true
}
```

For **Dan** and **Rev**, set `frontier_flag_considered: true`.

## Literary-marker quality protocol (mandatory)

All models use `literary_marker_aware_v2`.

Do **not** produce a quiet one-chunk-per-chapter map when the substrate shows finer literary signals. Use chapter fallback only when no finer signal is available or when speed requires a coarse scratch placeholder; in that case set confidence to `medium_low` or `low`, explain the fallback in `book_strategy/<Book>.md`, and write sidecar rows.

Triggers for low-confidence/escalation sidecars include:

- poetry/liturgy markers such as `q1`, `q2`, `d`, `b`, Selah/performance markers, songs, hymns, blessings, doxologies, superscriptions, acrostics, or stanza risk
- law, covenant code, ritual procedure, list, genealogy, land allotment, or census material
- mixed book genre versus pericope genre, such as narrative books containing law or poetry
- speaker shifts, direct speech, WJ/red-letter spans, oracle/vision units, apocalyptic scenes, or frontier books
- source-tradition/textual-variant pressure, footnote/cross-reference pressure, or known stress-atlas overlap
- chapter-only fallback on a marker-rich chapter

Each `atlas_candidate_feed.jsonl` row must explain why the chunk might belong in future stress-atlas review. It does **not** promote the issue into the governed atlas.

Each `frontier_escalation_queue.jsonl` row must explain why Codex/Claude/frontier review should scrutinize the chunk.

For Psalms, Job, Proverbs, Ecclesiastes, Song, Lamentations, Daniel, Revelation, Philemon, and Jonah, write a more careful book strategy before chunking. For Ps 119, do not use one chapter chunk; use acrostic/stanza evidence.

## T467 harness hardening for future reruns

T465 found a recurring over-splitting pattern: some lanes split smaller local units where other lanes preserved larger literary units. Future model reruns and new model slots must apply `T467_literary_coherence_v1`:

- Preserve larger coherent units for genealogy, census, tribal allotment, legal list, ritual procedure, temple-service register, royal/administrative register, battle report, and covenant renewal unless the unit changes function.
- Before splitting a list/register/legal/allotment/admin/battle unit, name its function and the exact function change that justifies the split.
- For epistles, check greeting, thanksgiving/prayer, body argument, exhortation or paraenesis, household/church order, travel or mission notes, final greetings, doxology, and benediction where present.
- Strong's, lemma, morphology, WJ/red-letter, headings, footnotes, and cross-references are evidence only. They do not become boundary authority, source-language truth, or theology authority.
- Low-confidence, frontier, and atlas sidecars must name the concrete issue: over-split risk, larger-unit conflict, list/register uncertainty, epistle-unit uncertainty, speaker/variant pressure, or source-metadata-only limitation.
- If your model chooses a smaller split where a larger coherent unit is plausible, log the reason in `book_strategy/<Book>.md` and the relevant sidecar row.

## Non-authorizations

- No real-time pairing with another model on the same verses
- No writes to `eval/chunking_gold/`, `data/candidate/chunks/`, or `pipelines/chunking/`
- Your map is scratch only; batch agreement does not auto-promote to canon
