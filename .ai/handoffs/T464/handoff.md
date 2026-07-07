# Task Handoff

## Task

- task_id: T464
- title: Multi-Model Chunking Comparison And Decision Docket
- phase: phase_4
- status: complete

## Agent

- agent_name: Codex
- mode: comparison_artifact_generation_non_authorizing
- stage: final
- updated_at: 2026-07-07T01:45:00+00:00
- handoff_id: t464-multi-model-decision-docket

## Files read

- `AI_FRONT_DOOR.md`
- `.ai/control/MASTER_CONTEXT.md`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/tasks/T464.task.yaml`
- `.ai/control/multi_model_whole_bible_chunking_fork.yaml`
- `.ai/scratch/multi_model_bible_chunking/manifest.yaml`
- `.ai/scratch/multi_model_bible_chunking/M1_cursor/model_manifest.yaml`
- `.ai/scratch/multi_model_bible_chunking/M2_claude_sonnet5/model_manifest.yaml`
- `.ai/scratch/multi_model_bible_chunking/M3_claude_frontier/model_manifest.yaml`
- `.ai/scratch/multi_model_bible_chunking/M4_codex_gpt55/model_manifest.yaml`
- `.ai/scratch/multi_model_bible_chunking/M5_gemini_thinking/model_manifest.yaml`
- `.ai/scratch/multi_model_bible_chunking/M6_fable5/model_manifest.yaml`
- `.ai/scratch/multi_model_bible_chunking/comparison/delta_summary.md`
- `.ai/scratch/multi_model_bible_chunking/comparison/model_agreement_matrix.yaml`
- `.ai/scratch/multi_model_bible_chunking/comparison/frontier_review_queue.jsonl`

## Files changed

- `.ai/tasks/T464.task.yaml`
- `.ai/handoffs/T464/handoff.md`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/handoff_ledger.jsonl`
- `.ai/control/multi_model_whole_bible_chunking_fork.yaml`
- `.ai/prompts/multi_model_whole_bible_chunking_delta_compare_prompt.md`
- `.ai/scratch/multi_model_bible_chunking/comparison/agreement_chunks.jsonl`
- `.ai/scratch/multi_model_bible_chunking/comparison/disagreement_delta.jsonl`
- `.ai/scratch/multi_model_bible_chunking/comparison/frontier_review_queue.jsonl`
- `.ai/scratch/multi_model_bible_chunking/comparison/harness_improvement_queue.md`
- `.ai/scratch/multi_model_bible_chunking/comparison/model_agreement_matrix.yaml`
- `.ai/scratch/multi_model_bible_chunking/comparison/delta_focus_queue.yaml`
- `.ai/scratch/multi_model_bible_chunking/comparison/owner_decision_docket.yaml`
- `.ai/scratch/multi_model_bible_chunking/comparison/delta_summary.md`
- `docs/roadmap/T464_MULTI_MODEL_CHUNKING_DECISION_DOCKET.md`
- `scripts/compare_multi_model_bible_chunk_maps.py`
- `scripts/t423_chunk_map_utils.py`
- `scripts/validate_parallel_execution_safety.py`
- `scripts/validate_all.py`
- `scripts/validate_t464_multi_model_decision_docket.py`
- `tests/test_parallel_execution_safety.py`
- `tests/test_t423_chunk_map_compare.py`
- `tests/test_t464_multi_model_decision_docket.py`

## Decisions made

- T464 freezes the six completed scratch model lanes as comparison evidence: `M1_cursor`, `M2_claude_sonnet5`, `M3_claude_frontier`, `M4_codex_gpt55`, `M5_gemini_thinking`, and `M6_fable5`.
- Direct and module compare entrypoints are both supported.
- Comparison outputs are non-authorizing evidence only: agreement rows, disagreement deltas, owner docket, frontier queue, harness queue, and agreement matrix.
- `M4_codex_gpt55` plus `M6_fable5` agreement is recorded as a preferred evidence lens, never as authority.
- Known textual-variant/source-tradition hot zones, including Mark.16.1-Mark.16.20 and Mark.16.9-Mark.16.20, are routed to frontier review even if models agree.
- Mark 16 rows include expert lanes for major codex witness review, Codex Vaticanus layout/blank-space review, Codex Sinaiticus ending review, scribal layout and letters-per-column/column-space review, manuscript transmission history, and the longer-ending specialist packet.
- The full comparison produced a `FULL_FAIL` fork threshold signal: verse-coverage agreement is 6.17%, below the 50.00% full-run threshold. This is not a code failure; it is a decision signal that model outputs need reconciliation and harness improvement before any output-changing work.

## Validation run

- `python scripts/t423_marathon_status.py` - passed
- `python scripts/validate_multi_model_whole_bible_chunking_fork.py` - passed
- `python scripts/validate_t423_literary_quality_protocol.py --model-folder <each M1-M6 folder> --require-artifacts` - passed for all six model folders
- `python scripts/compare_multi_model_bible_chunk_maps.py --dry-run` - passed, 144 agreements, 1048 deltas, 6.17% verse-coverage agreement
- `python scripts/compare_multi_model_bible_chunk_maps.py` - passed and wrote comparison artifacts
- `python scripts/evaluate_t423_revert_signal.py --json` - returned `FULL_FAIL` as expected decision signal because 6.17% < 50.00%
- `python scripts/validate_t464_multi_model_decision_docket.py` - passed
- `python scripts/validate_parallel_execution_safety.py --task-id T464 --allow-current-task-dirty` - passed
- `python -m pytest tests/test_parallel_execution_safety.py tests/test_t464_multi_model_decision_docket.py tests/test_t423_chunk_map_compare.py -q` - 28 passed

## Known risks

- Agreement is low enough that T464 should not be used to promote chunks directly. It should be used to identify low-risk owner candidates, frontier review packets, and harness defects.
- High-disagreement books include many historical, epistle, and high-risk literature areas. They need reconciliation or rerun guidance before promotion.
- Mark 16 and other textual-variant hot zones must be handled with manuscript-source evidence, not with model consensus alone.
- Scratch outputs remain non-canonical and must not be treated as reviewed gold or governed chunk output.

## Open questions

- Which owner docket slice should become the first reconciliation batch: easy agreements first, Mark 16/textual variants first, or harness fixes before any owner decisions?
- Should the comparison metric be adjusted after harness improvements, since verse-coverage agreement exposes large strategy divergence across models?
- Which expert agent should own the first Mark 16 specialist packet: textual-criticism/codex lane, frontier theological/literary lane, or both in sequence?

## Next agent instruction

Review `.ai/scratch/multi_model_bible_chunking/comparison/owner_decision_docket.yaml` and choose a narrow T465 reconciliation route. Recommended first route: do not promote output; instead triage `harness_improvement_queue.md`, then open a frontier packet for Mark.16.9-Mark.16.20 that explicitly covers Codex Vaticanus blank-space/layout claims, Codex Sinaiticus ending evidence, scribal letters-per-column/column-space analysis, and longer-ending theological/literary implications.
