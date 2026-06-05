# Task Handoff

## Task

- task_id: T311
- title: Fix psalms_fragmented evaluator grouping
- phase: phase_3
- status: complete

## Agent

- agent_name: codex-5
- mode: build
- stage: final
- updated_at: 2026-06-05T20:13:01+00:00
- handoff_id: 7caf9e1a2a2cfa32

## Files read

- AI_FRONT_DOOR.md
- .ai/control/MASTER_CONTEXT.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/DATA_MAP.md
- .ai/control/RAW_SOURCE_INVENTORY.md
- ROADMAP_STATE.yaml
- HANDOFF_PROTOCOL.md
- docs/architecture/ARCHITECTURE.md
- docs/chunking/CHUNKING_DESIGN.md
- config/agents/agent_roles.yaml
- config/chunking/book_genres.yaml
- pipelines/chunking/evaluate_chunks.py
- pipelines/chunking/leaderboard.py
- eval/LEADERBOARD.md
- eval/chunking_runs/*.json
- eval/chunking_runs/README.md
- tests/test_chunker_gold.py
- tests/test_chunker_smoke.py

## Files changed

- pipelines/chunking/evaluate_chunks.py
- pipelines/chunking/leaderboard.py
- tests/test_evaluate_chunks.py
- eval/chunking_runs/*.json
- eval/LEADERBOARD.md
- eval/chunking_runs/README.md
- .ai/context/agent_work/T311_psalms_fragmented_before_after.md
- .ai/tasks/T311.task.yaml
- .ai/handoffs/T311/handoff.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/DATA_MAP.md
- .ai/control/handoff_ledger.jsonl
- ROADMAP_STATE.yaml

## Decisions made

- Replaced chapter-only psalm fragmentation grouping with OSIS `(book, chapter)` grouping.
- Adopted split metrics: `psalms_fragmented` remains a backward-compatible alias for `literal_psalms_fragmented`, with `poetry_books_fragmented` retaining the broader poetry-book signal.
- Excluded Psalm 119 from fragmentation penalties and reported it explicitly as `psalm119_section_chunks`.
- Updated the leaderboard composite to prefer `literal_psalms_fragmented` and added the existing Gen 1 no-mid-sentence gate to eligibility.
- Rescored committed scorecards in place with `evaluator_metric_version = psalm-fragmentation-book-chapter-v2`.

## Validation run

- command: `python pipelines/chunking/evaluate_chunks.py A_genre_default=data/derived/chunks/variants/A_genre_default/chunks.jsonl B_genre_tight=data/derived/chunks/variants/B_genre_tight/chunks.jsonl C_naive_window=data/derived/chunks/variants/C_naive_window/chunks.jsonl D_claude_pass2=data/derived/chunks/variants/D_claude_pass2/chunks.jsonl --report build/t311/after_report.md --json build/t311/after_scores.json`
- result: passed; fixed metrics recomputed for all four variants
- command: `python pipelines/chunking/leaderboard.py`
- result: passed; default leaderboard regenerated with D_claude_pass2 rank 1 at composite 93.0
- command: `python scripts/validate_all.py`
- result: passed
- command: `python -m pytest -q`
- result: passed, 54 tests
- failures: none

## Known risks

- Existing historical scorecards were rescored in place so the committed leaderboard reflects the fixed evaluator; the original before values are preserved in the T311 analysis note.
- "Intentional" sectioning is explicitly recognized only for Psalm 119; no general curated intentional-section registry exists yet.
- The workspace contained pre-existing unrelated T310 changes at task start; T311 did not modify chunker/orchestrator/detector behavior or raw/canonical/chunk outputs.

## Open questions

- Whether future composites should also penalize `poetry_books_fragmented`; T311 leaves it visible but not part of the composite to avoid gaming the literal Psalm target.

## Next agent instruction

Continue T310/T309 work using the fixed evaluator surface; do not treat old `psalms_fragmented` scorecard values as comparable unless they have `evaluator_metric_version = psalm-fragmentation-book-chapter-v2`.
