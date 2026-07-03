# Multi-Model Whole-Bible Chunking — One Model, Book-at-a-Time

**You are ONE model in ONE folder.** Chunk the entire Bible alone. Save each book locally, then move to the next. **Do not** compare with other models during your run.

## Your folder layout

```
M1_cursor/                    # example — your model_id names this folder
  book_chunks/
    Gen/chunks.jsonl          # save this book, then move on
    Exod/chunks.jsonl
    ...
  marathon_progress.yaml
  layer_decision_log.jsonl
  whole_bible_chunk_map.jsonl # merged only after all 66 books (owner/script)
```

## Workflow (one book per session)

1. Read `shared_research_baseline/research_baseline_manifest.yaml`; set `research_baseline_read: true` in `model_manifest.yaml`.
2. Read **Rust observation substrate** under `build/observation_substrate/current/`.
3. Work **only** in your model folder (e.g. `M1_cursor/`).
4. Find next book:
   ```bash
   python scripts/t423_resume_book.py <your_model_folder> --json
   ```
5. Chunk **that book only**; write all chunks to `book_chunks/<Book>/chunks.jsonl`.
6. Validate the book:
   ```bash
   python scripts/validate_whole_bible_chunk_map.py book_chunks/<Book>/chunks.jsonl --model-id <M_id> --book <Book>
   ```
7. Mark book complete:
   ```bash
   python scripts/t423_resume_book.py <your_model_folder> --mark-complete <Book>
   ```
8. If session ends, stop. Next session resumes at the next incomplete book.
9. If a book was half-written, discard before re-chunk:
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

## Non-authorizations

- No real-time pairing with another model on the same verses
- No writes to `eval/chunking_gold/`, `data/candidate/chunks/`, or `pipelines/chunking/`
- Your map is scratch only; batch agreement does not auto-promote to canon
