# T423 — Multi-Model Whole-Bible Chunking Fork (Experimental)

## Why this fork exists

Speed up chunking by running **3–10 AI models** in **separate scratch folders** (initial target **5**). Each model chunks the **entire Bible alone**, saving **one book at a time** to `book_chunks/<Book>/chunks.jsonl`. **No real-time cross-model compare.** After all models finish 66 books locally, owner runs **batch verse-coverage compare**:

- **Agreement** → easy/consensus chunks (low governed effort)
- **Delta** → disagreement focus queue (where T410 work concentrates)

If the fork fails → **revert to** `.ai/control/parallel_chunking_research_program.yaml`.

## Scratch layout

```
.ai/scratch/multi_model_bible_chunking/
  manifest.yaml
  shared_research_baseline/
  M1_cursor/book_chunks/Gen/chunks.jsonl ...
  M2_codex/book_chunks/...
  comparison/                   # batch compare outputs only
  redteam/
  MARATHON_PLAYBOOK.md
```

## Pilot gate

Five pilot books (Gen, Ps, Phlm, Jonah, Rev) before full 66 on all models. Owner sets `pilot_gate.status: go` after batch pilot compare passes.

## Marathon flow (one model, book segments)

See `MARATHON_PLAYBOOK.md` and `.ai/prompts/multi_model_whole_bible_chunking_marathon_prompt.md`.

```bash
python scripts/t423_resume_book.py .ai/scratch/multi_model_bible_chunking/M1_cursor
python scripts/t423_merge_book_chunks.py .ai/scratch/multi_model_bible_chunking/M1_cursor
python scripts/compare_multi_model_bible_chunk_maps.py   # after ALL models complete
python scripts/evaluate_t423_revert_signal.py
```

## Post-fix audit

`.ai/prompts/multi_model_whole_bible_chunking_postfix_audit_prompt.md`

## Rust acceleration (Phase 2 — deferred)

Boundary-candidate index + Rust compare with Python parity tests. Python verse-coverage compare is canonical for now.

## Parallel work

T417 batch2 scratch ladder continues separately under `.ai/context/agent_work/T417/model_layers/`.

## Non-authorizations

Scratch chunk maps are not canon. Agreement does not auto-promote gold or output.
