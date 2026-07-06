# T423 Marathon Playbook — One Model, Book Segments, Batch Compare Last

## Owner workflow

1. **T412 gate:** `python scripts/validate_rust_observation_substrate.py`
2. **Pin substrate** (same build for all models): `python scripts/t423_pin_substrate.py M1_cursor`
3. **One model at a time** — each model gets its own git worktree branch (`scratch/t423-M1-cursor`, `scratch/t423-M2-claude-sonnet5`, etc.)
4. Model chunks **all 66 books alone**, saving each to `book_chunks/<Book>/chunks.jsonl`
5. **No real-time cross-model work** — never pair two models on the same book live
6. After **all** target models finish 66 books and merge maps, owner runs **batch** compare

## Per-model launch (repeat for M1, then M2, …)

```powershell
# PowerShell — one book per agent invocation
$model = ".ai/scratch/multi_model_bible_chunking/M1_cursor"
python scripts/t423_resume_book.py $model --json
# Agent chunks that book -> book_chunks/<Book>/chunks.jsonl
python scripts/validate_whole_bible_chunk_map.py $model --book <Book>
python scripts/t423_resume_book.py $model --mark-complete <Book>
```

```bash
# Bash loop (supervisor)
MODEL=".ai/scratch/multi_model_bible_chunking/M1_cursor"
while python scripts/t423_marathon_supervisor.py "$MODEL" --json | grep -q '"next_book":'; do
  BOOK=$(python scripts/t423_resume_book.py "$MODEL")
  echo "Chunk book: $BOOK (invoke agent here)"
  # after agent writes book_chunks/$BOOK/chunks.jsonl:
  python scripts/t423_resume_book.py "$MODEL" --mark-complete "$BOOK"
done
python scripts/t423_merge_book_chunks.py "$MODEL"
```

## Pilot gate (before full 66 on all models)

Pilot books: **Gen, Ps, Phlm, Jonah, Rev**

1. Run M1–M4 through pilot books only (validator blocks books outside pilot until `pilot_gate.status: go`)
2. Merge + batch compare pilot:
   ```bash
   python scripts/compare_multi_model_bible_chunk_maps.py --book Gen --book Ps --book Phlm --book Jonah --book Rev
   python scripts/evaluate_t423_revert_signal.py --pilot-only
   ```
3. Owner reviews `comparison/delta_summary.md`; sets `pilot_gate.status: go` in fork YAML if passing
4. Release full 66-book marathons

## Batch compare (after all models complete)

```bash
python scripts/t423_marathon_status.py
python scripts/t423_merge_book_chunks.py .ai/scratch/multi_model_bible_chunking/M1_cursor
# ... repeat merge for each model ...
python scripts/compare_multi_model_bible_chunk_maps.py
python scripts/evaluate_t423_revert_signal.py
```

Compare uses **verse-coverage** offline — not live pairing during chunking.

## Folder layout

```
.ai/scratch/multi_model_bible_chunking/
  M1_cursor/book_chunks/Gen/chunks.jsonl ...
  M2_claude_sonnet5/book_chunks/...
  comparison/          # written only by batch compare script
```

## Recommended model order

1. `M1_cursor` — completed Cursor/Composer 2.5 fast marathon.
2. `M2_claude_sonnet5` — Claude Sonnet 5 at medium/high effort for the next efficient high-quality pass.
3. `M3_claude_frontier` — Claude Opus 4.8 or Fable 5 at high effort for hard literary/theological cases.
4. `M4_codex_gpt55` — Codex GPT-5.5 high effort for structured contrast after the Claude-family passes.
5. `M5_gemini_thinking` — optional outside-family comparison if owner wants more variance before compare.

## Non-authorizations

- Agreement ledger does not promote gold (`promotion_authority: none`)
- Rust compare acceleration deferred to Phase 2
