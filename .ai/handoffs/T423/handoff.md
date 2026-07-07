# T423 Handoff

## Task
T423 - Parallel Isolation And Literary Quality Hardening

## Agent
Codex

## Files read
- AI_FRONT_DOOR.md
- .ai/control/MASTER_CONTEXT.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/current_focus.yaml
- .ai/control/multi_model_whole_bible_chunking_fork.yaml
- .ai/prompts/multi_model_whole_bible_chunking_marathon_prompt.md
- .ai/scratch/multi_model_bible_chunking/models/_TEMPLATE/README.md
- .ai/scratch/multi_model_bible_chunking/models/_TEMPLATE/model_manifest.yaml
- scripts/validate_t423_parallel_isolation.py
- scripts/validate_whole_bible_chunk_map.py
- scripts/t423_resume_book.py
- tests/test_t423_chunk_map_compare.py
- tests/test_t423_pilot_e2e.py
- scripts/validate_task_scope.py
- scripts/validate_parallel_execution_safety.py

## Files changed
- .ai/tasks/T423.task.yaml
- .ai/handoffs/T423/handoff.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/multi_model_whole_bible_chunking_fork.yaml
- .ai/control/t423_literary_marker_quality_protocol.yaml
- .ai/prompts/multi_model_whole_bible_chunking_marathon_prompt.md
- .ai/scratch/multi_model_bible_chunking/manifest.yaml
- .ai/scratch/multi_model_bible_chunking/M1_cursor/model_manifest.yaml
- .ai/scratch/multi_model_bible_chunking/M2_claude_sonnet5/model_manifest.yaml
- .ai/scratch/multi_model_bible_chunking/M2_claude_sonnet5/marathon_progress.yaml
- .ai/scratch/multi_model_bible_chunking/M3_claude_frontier/model_manifest.yaml
- .ai/scratch/multi_model_bible_chunking/M3_claude_frontier/marathon_progress.yaml
- .ai/scratch/multi_model_bible_chunking/M4_codex_gpt55/model_manifest.yaml
- .ai/scratch/multi_model_bible_chunking/M4_codex_gpt55/marathon_progress.yaml
- .ai/scratch/multi_model_bible_chunking/M5_gemini_thinking/model_manifest.yaml
- .ai/scratch/multi_model_bible_chunking/M5_gemini_thinking/marathon_progress.yaml
- .ai/scratch/multi_model_bible_chunking/FORK_README.md
- .ai/scratch/multi_model_bible_chunking/MARATHON_PLAYBOOK.md
- .ai/scratch/multi_model_bible_chunking/comparison/model_agreement_matrix.yaml
- .ai/scratch/multi_model_bible_chunking/models/_TEMPLATE/README.md
- .ai/scratch/multi_model_bible_chunking/models/_TEMPLATE/model_manifest.yaml
- docs/roadmap/T423_MULTI_MODEL_WHOLE_BIBLE_CHUNKING_FORK.md
- .ai/prompts/multi_model_whole_bible_chunking_delta_compare_prompt.md
- scripts/t423_chunk_map_utils.py
- scripts/t423_resume_book.py
- scripts/validate_all.py
- scripts/validate_multi_model_whole_bible_chunking_fork.py
- scripts/validate_t423_parallel_isolation.py
- scripts/validate_t423_literary_quality_protocol.py
- scripts/validate_whole_bible_chunk_map.py
- tests/test_t423_chunk_map_compare.py
- tests/test_t423_parallel_isolation.py
- tests/test_t423_literary_quality_protocol.py
- tests/test_t423_pilot_e2e.py

## Decisions made
- Fixed `_normalize` so it removes only literal leading `./` prefixes and preserves `.ai/` roots.
- Added regression coverage for main-branch fail-closed behavior, scratch branch allowance, broad T417 batch2 root blocking, future `L4_*` / `L5_*` batch2 path blocking, and policy-listed comparison-path blocking.
- Added `literary_marker_aware_v2` as the required T423 quality protocol for every model slot.
- Required per-book strategy notes, low-confidence register rows, frontier escalation rows, and atlas candidate feed rows for low-confidence or marker-sensitive chunking.
- Wired `scripts/validate_t423_literary_quality_protocol.py` into `t423_resume_book.py --mark-complete`, `validate_all.py`, and the T423 fork validator.
- Made `frontier_flag_considered` a required chunk-map field.
- Renamed pending model lanes so the planned sequence is explicit:
  `M2_claude_sonnet5`, `M3_claude_frontier`, `M4_codex_gpt55`, and optional
  `M5_gemini_thinking`.
- Recorded the recommended lineup: completed Cursor/Composer fast pass, Claude Sonnet 5,
  Claude Opus 4.8 or Fable 5 high, Codex GPT-5.5 high, then optional Gemini/outside-family
  comparison.
- Kept atlas candidate rows consideration-only; they do not edit or promote the governed stress atlas.
- Kept T423 non-authorizing: no marathon start, reviewed gold, governed output, graph/retrieval/vector truth, route/evaluator change, or theology authority.

## Validation run
- `python -m pytest tests/test_t423_literary_quality_protocol.py tests/test_t423_parallel_isolation.py tests/test_t423_chunk_map_compare.py tests/test_t423_pilot_e2e.py -q` -> passed, 22 tests.
- `python scripts/validate_t423_literary_quality_protocol.py --policy-only` -> passed.
- `python scripts/validate_multi_model_whole_bible_chunking_fork.py` -> passed.
- `python scripts/validate_t423_pilot_gate.py` -> passed.
- `python scripts/validate_t423_parallel_isolation.py --policy-only` -> passed.
- `python scripts/validate_t423_parallel_isolation.py` on `main` -> expected fail-closed, exit 1.
- `python scripts/validate_task_scope.py --task-id T423` -> passed.
- `python scripts/validate_parallel_execution_safety.py --task-id T423 --allow-current-task-dirty` -> passed.
- `python scripts/validate_all.py` -> pending final rerun after handoff/status updates.
- `python -m pytest -q` -> pending final rerun.

## Known risks
- This patch hardens T423 protocol and validators only. It does not review or approve any completed scratch chunk map.
- Existing M1 chapter-only scratch work in a separate worktree should be treated as coarse baseline unless revised under `literary_marker_aware_v2`.
- T423 remains an experimental scratch fork; any scratch-to-governed promotion must follow the T410 owner-gated path.

## Open questions
- Whether to preserve M1_cursor v1 as a coarse baseline or restart it as M1_cursor_v2 after this protocol lands.

## Next agent instruction
Rerun focused T423 gates, `validate_all.py`, full pytest, `generate_data_map.py --check`, and `git diff --check`. Do not start T423 marathon work from this handoff.

---

## M4 Codex GPT-5.5 Marathon Addendum - 2026-07-04

## Task

- task_id: T423
- title: M4_codex_gpt55 whole-Bible scratch chunking marathon
- mode: build
- status: complete for M4 scratch lane

## Agent

- agent_name: Codex GPT-5.5
- model_lane: M4_codex_gpt55

## Files read

- AI_FRONT_DOOR.md
- .ai/control/MASTER_CONTEXT.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/multi_model_whole_bible_chunking_fork.yaml
- .ai/control/t423_literary_marker_quality_protocol.yaml
- .ai/scratch/multi_model_bible_chunking/FORK_README.md
- .ai/scratch/multi_model_bible_chunking/MARATHON_PLAYBOOK.md
- .ai/prompts/multi_model_whole_bible_chunking_marathon_prompt.md
- .ai/scratch/multi_model_bible_chunking/shared_research_baseline/research_baseline_manifest.yaml
- build/observation_substrate/current/scan_manifest.json
- build/observation_substrate/current/book_observations.jsonl
- build/observation_substrate/current/verse_observations.jsonl
- build/observation_substrate/current/span_observation_features.jsonl
- build/observation_substrate/current/risk_signal_index.jsonl
- data/raw/bible/eng-web/source_manifest.yaml
- .ai/control/RAW_SOURCE_INVENTORY.md
- config/ingest/usfm_marker_coverage.yaml
- config/chunking/book_genres.yaml
- scripts/validate_whole_bible_chunk_map.py
- scripts/validate_t423_literary_quality_protocol.py
- scripts/t423_resume_book.py
- scripts/t423_merge_book_chunks.py

## Files changed

- .ai/scratch/multi_model_bible_chunking/M4_codex_gpt55/model_manifest.yaml
- .ai/scratch/multi_model_bible_chunking/M4_codex_gpt55/marathon_progress.yaml
- .ai/scratch/multi_model_bible_chunking/M4_codex_gpt55/generate_m4_literary_chunks.py
- .ai/scratch/multi_model_bible_chunking/M4_codex_gpt55/book_strategy/*.md
- .ai/scratch/multi_model_bible_chunking/M4_codex_gpt55/book_chunks/*/chunks.jsonl
- .ai/scratch/multi_model_bible_chunking/M4_codex_gpt55/low_confidence_register.jsonl
- .ai/scratch/multi_model_bible_chunking/M4_codex_gpt55/frontier_escalation_queue.jsonl
- .ai/scratch/multi_model_bible_chunking/M4_codex_gpt55/atlas_candidate_feed.jsonl
- .ai/scratch/multi_model_bible_chunking/M4_codex_gpt55/layer_decision_log.jsonl
- .ai/scratch/multi_model_bible_chunking/M4_codex_gpt55/whole_bible_chunk_map.jsonl
- .ai/scratch/multi_model_bible_chunking/M4_codex_gpt55/model_quality_summary.md
- .ai/scratch/multi_model_bible_chunking/M4_codex_gpt55/model_summary.md
- .ai/scratch/multi_model_bible_chunking/M4_codex_gpt55/audit/preflight_clean_state.md
- .ai/handoffs/T423/handoff.md
- .ai/control/handoff_ledger.jsonl

## Decisions made

- Ran the M4 marathon independently from the Rust no-text observation substrate, with raw USFM exception reads kept at 0.
- Set `research_baseline_read: true` and recorded the shared baseline manifest SHA-256 in the M4 manifest.
- Pinned the current substrate fingerprint in the M4 manifest and preserved it through reset/finalization.
- Restarted the active M4 lane from 0 completed books; no old active chunks or sidecar residue remained after reset.
- Generated one book strategy before each book's chunks, then validated and marked each book complete before continuing.
- Used `literary_marker_aware_v2` with paragraph, poetry, list/genealogy, speaker, WJ, footnote/cross-reference, oracle/vision, and chapter-boundary evidence treated as non-authorizing.
- Merged only M4's own book chunks into `whole_bible_chunk_map.jsonl`; comparison was not run.

## Validation run

- `python scripts/validate_rust_observation_substrate.py --input build/observation_substrate/current` -> passed.
- Per-book `python -m scripts.validate_whole_bible_chunk_map ... --model-id M4_codex_gpt55 --book <Book>` -> passed for all 66 books.
- Per-book `python scripts/validate_t423_literary_quality_protocol.py --model-folder .ai/scratch/multi_model_bible_chunking/M4_codex_gpt55 --book <Book> --require-artifacts` -> passed for all 66 books.
- `python scripts/t423_merge_book_chunks.py .ai/scratch/multi_model_bible_chunking/M4_codex_gpt55` -> merged 1,319 chunks from 66 books.
- `python scripts/validate_whole_bible_chunk_map.py .ai/scratch/multi_model_bible_chunking/M4_codex_gpt55 --model-id M4_codex_gpt55 --require-full-bible` -> passed.
- `python scripts/validate_t423_literary_quality_protocol.py --model-folder .ai/scratch/multi_model_bible_chunking/M4_codex_gpt55 --require-artifacts` -> passed.
- Custom substrate coverage check -> 31,103/31,103 canonical verses covered exactly once; Dan/Rev frontier flag missing count 0.
- `python scripts/validate_all.py` -> failed only after many passing gates because task-scope/parallel-safety dirty paths pre-existed outside M4 and `validate_t423_pilot_gate.py` still has `pilot_gate.status: pending` while the owner instruction requested a full M4 66-book run.
- `python -m pytest -q` -> 732 passed, 1 failed (`tests/test_control_plane.py::test_validate_all_suite`) due the same `validate_all.py` failures.

## Known risks

- Full repo dirty state was not limited to `M4_codex_gpt55/` before this run; M4 changes were kept isolated, but repo-wide scope gates still see other task/model setup paths.
- One early broad search accidentally printed M2 Genesis hits because a Windows glob exclusion did not apply as intended. The M4 map was generated mechanically from the substrate and did not reuse those boundaries.
- The run intentionally follows the owner's full-66 M4 instruction even though the fork YAML pilot gate remains `pending`; the pilot gate validator therefore fails until the control-plane gate is reconciled.
- The M4 map is scratch only and non-authorizing; it does not promote reviewed gold, canon chunk output, child spans, graph/retrieval truth, source-tradition preference, or theology authority.

## Open questions

- Should the owner update or waive the T423 pilot gate for already-started full-model marathons, or should validators add an explicit owner-override field for this full M4 run?
- Should the M4-local generator be kept as audit evidence, or archived after comparison so it is not mistaken for governed pipeline code?

## Next agent instruction

Do not run comparison yet. First reconcile the T423 pilot gate/status with the owner's full-66 marathon instruction, then rerun `validate_all.py` and `python -m pytest -q`. After at least the required model set is complete and the owner releases comparison, merge completed model maps and run the batch compare scripts.

---

## Handoff refresh: final

- agent_name: Codex GPT-5.5
- mode: build
- updated_at: 2026-07-04T19:05:15+00:00
- handoff_id: 6e70f8c540cace59
