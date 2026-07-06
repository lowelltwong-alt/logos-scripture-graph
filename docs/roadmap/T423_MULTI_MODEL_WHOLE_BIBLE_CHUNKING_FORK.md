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
  M2_claude_sonnet5/book_chunks/...
  M3_claude_frontier/book_chunks/...
  M4_codex_gpt55/book_chunks/...
  M5_gemini_thinking/book_chunks/...   # optional outside-family pass
  comparison/                   # batch compare outputs only
  redteam/
  MARATHON_PLAYBOOK.md
```

## Recommended model lineup

1. `M1_cursor` — completed Cursor/Composer fast marathon.
2. `M2_claude_sonnet5` — Claude Sonnet 5 medium/high effort for the next efficient whole-Bible pass.
3. `M3_claude_frontier` — Claude Opus 4.8 or Fable 5 high effort for hard literary/theological cases.
4. `M4_codex_gpt55` — Codex GPT-5.5 high effort for structured contrast after the Claude-family passes.
5. `M5_gemini_thinking` — optional outside-family comparison if owner wants more variance before compare.

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
