# Task Handoff

## Task

- task_id: T412
- title: Rust-First Whole-Bible Observation Substrate
- phase: phase_4
- status: complete_merged

## Agent

- agent_name: Codex
- mode: implementation
- stage: final
- updated_at: 2026-06-30T23:27:47Z
- handoff_id: t412-rust-first-final-proof

## Files read

- AI_FRONT_DOOR.md
- .ai/control/MASTER_CONTEXT.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/DATA_MAP.md
- .ai/control/RAW_SOURCE_INVENTORY.md
- .ai/control/test_runtime_preflight.yaml
- .ai/control/parallel_chunking_research_program.yaml
- .ai/control/rust_first_observation_substrate.yaml
- .ai/tasks/T411.task.yaml
- .ai/tasks/T412.task.yaml
- config/ingest/usfm_marker_coverage.yaml
- config/canon/canonical_66_books.yaml
- config/chunking/book_genres.yaml
- tools/usfm_observation_scanner/Cargo.toml
- tools/usfm_observation_scanner/src/main.rs
- scripts/validate_rust_observation_substrate.py
- scripts/build_cursor_observation_pack.py
- tests/test_rust_observation_substrate.py
- Claude T412 review attachment at C:/Users/lowel/.codex/attachments/e1cbc02f-1f2e-4ba9-a1d8-8e9735bb53a6/pasted-text.txt

## Files changed

- .gitignore
- .ai/control/rust_first_observation_substrate.yaml
- .ai/control/parallel_chunking_research_program.yaml
- .ai/control/chunking_theological_decision_register.yaml
- .ai/control/chunking_lesson_index.yaml
- .ai/control/PROJECT_STATUS.md
- .ai/control/current_focus.yaml
- .ai/control/handoff_ledger.jsonl
- .ai/tasks/T412.task.yaml
- .ai/tasks/T411.task.yaml
- .ai/handoffs/T412/handoff.md
- AI_FRONT_DOOR.md
- AI_TABLE_OF_CONTENTS.md
- ROADMAP_STATE.yaml
- docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md
- docs/roadmap/T410_RESEARCH_TO_CHUNKING_PHASE_ONE_ROADMAP.md
- docs/roadmap/T411_CURSOR_READINESS_WITH_CLAUDE_GATE.md
- docs/roadmap/T412_RUST_FIRST_OBSERVATION_SUBSTRATE.md
- tools/usfm_observation_scanner/Cargo.toml
- tools/usfm_observation_scanner/Cargo.lock
- tools/usfm_observation_scanner/src/main.rs
- scripts/validate_rust_observation_substrate.py
- scripts/build_cursor_observation_pack.py
- scripts/validate_all.py
- scripts/validate_parallel_chunking_prompt_pack.py
- scripts/validate_t411_cursor_batch_artifacts.py
- tests/test_rust_observation_substrate.py
- tests/test_t411_cursor_batch_artifacts.py

Generated but not committed:

- build/observation_substrate/current/
- tools/usfm_observation_scanner/target/

## Decisions made

- Closed Claude P1 by installing Rust stable plus the GNU Windows toolchain, compiling the scanner, running it against the real WEB USFM zip, and validating generated ledgers.
- Closed Claude P2-1 by keeping `has_strong_h` and `has_strong_g` as evidence feature flags and Strong occurrence rows only; Strong's presence alone no longer creates risk signals.
- Closed Claude P2-2 by ignoring `tools/usfm_observation_scanner/target/` and declaring `.gitignore` in T412 scope.
- Addressed Claude P3 cleanup by removing dead Rust code, requiring `hex` and `sha2` in the contract validator, and documenting the key-name/scanner-contract no-text assumption.
- Added `CD-079` to the chunking theological decision register so T410/T411/T412 roadmap and observation-substrate surfaces remain explicitly non-authorizing and cannot smuggle theology, boundary, reviewed-gold, output, route/evaluator, graph/retrieval/vector, source-tradition, or canon authority.
- Kept generated ledgers ignored under `build/observation_substrate/current/`; they are proof artifacts and can be regenerated from committed source.
- Kept T411/Cursor stopped. The substrate and T411 pack checks now pass, but Cursor still requires a clean T411 branch/worktree preflight and owner launch before running.

## Validation run

- command: `cargo test --manifest-path tools/usfm_observation_scanner/Cargo.toml`
- result: passed with `stable-x86_64-pc-windows-gnu`
- failures: none
- command: `cargo run --manifest-path tools/usfm_observation_scanner/Cargo.toml -- scan --source data/raw/bible/eng-web/usfm/eng-web_usfm.zip --canon config/canon/canonical_66_books.yaml --marker-coverage config/ingest/usfm_marker_coverage.yaml --book-genres config/chunking/book_genres.yaml --out build/observation_substrate/current --no-text`
- result: passed; wrote 83 book rows, 38,058 verse rows, and 83 source file observations
- failures: none
- command: `python scripts/validate_rust_observation_substrate.py --input build/observation_substrate/current`
- result: passed generated mode: 83 books, 66 canonical books, 38,058 verses, 1,402 spans
- failures: none
- command: `python scripts/build_cursor_observation_pack.py --input build/observation_substrate/current --task-id T411 --check`
- result: passed for selected books 2John, Jonah, and Phlm; no output authority
- failures: none
- command: Strong/risk sanity check over generated ledgers
- result: 278,168 Strong occurrence rows; `has_strong_h` and `has_strong_g` absent from `risk_signal_index.jsonl`
- failures: none
- command: `python -m pytest tests/test_rust_observation_substrate.py tests/test_parallel_chunking_prompt_pack.py tests/test_t411_cursor_batch_artifacts.py -q`
- result: 29 passed combined across the three files (`tests/test_rust_observation_substrate.py` alone has 9 tests)
- failures: none
- command: `python scripts/validate_parallel_execution_safety.py --task-id T412 --allow-current-task-dirty --require-task-branch`
- result: passed
- failures: none
- command: `python scripts/validate_task_scope.py --task-id T412`
- result: passed
- failures: none
- command: `python scripts/validate_parallel_chunking_prompt_pack.py`
- result: passed
- failures: none
- command: `python scripts/validate_t411_cursor_batch_artifacts.py`
- result: passed
- failures: none
- command: `python scripts/validate_chunking_theological_decision_register.py --base-ref origin/main --register-updated true`
- result: passed for CD-079 content before commit amend
- failures: none
- command: `python scripts/validate_all.py`
- result: all validation gates passed
- failures: none
- command: `python -m pytest -q`
- result: 675 passed in 540.27s
- failures: none
- command: `python scripts/generate_data_map.py --check`
- result: DATA_MAP.md is current
- failures: none
- command: `git diff --check`
- result: passed with existing CRLF warning for `.ai/control/handoff_ledger.jsonl`
- failures: none

## Known risks

- Rust stable and WinLibs/MinGW were installed locally so the scanner can be proved on this Windows machine. The committed scanner remains an isolated crate under `tools/usfm_observation_scanner/`.
- Generated ledgers are intentionally ignored. Future agents must regenerate and validate them before Cursor consumes them in a fresh worktree.
- T411 may now be tempting to start, but it must still wait for a clean T411 branch/worktree preflight and owner launch.

## Open questions

- None for substrate safety. T411 awaits owner launch after governance recording and clean T411 preflight.

## Next agent instruction

T412 is merged @ `e90bc3d`. Claude post-merge audit recorded **APPROVE_T411_CURSOR** in `.ai/audits/reports/20260630-T412-post-merge-claude-audit.md`. Start T411 only after owner launch from a clean T411 branch/worktree with:

```bash
python scripts/validate_parallel_execution_safety.py --task-id T411 --require-task-branch
python scripts/validate_rust_observation_substrate.py --input build/observation_substrate/current
python scripts/build_cursor_observation_pack.py --input build/observation_substrate/current --task-id T411 --check
```

Do not run Cursor, promote reviewed gold, create chunks, add child spans, change route/evaluator behavior, create graph/retrieval/vector truth, run embeddings/indexes, import boundaries, choose a backend, promote a profile, create source rows, change canon scope, or authorize theology authority without owner launch and the later exact owner gate.

---

## Claude post-merge audit (T411 substrate gate)

- auditor: Claude (frontier architecture audit)
- recorded_at: 2026-06-30
- merge_ref: e90bc3d0022f612fb3c80775699e85d4b9f3d672
- audit_report: .ai/audits/reports/20260630-T412-post-merge-claude-audit.md
- verdict: APPROVE_T411_CURSOR
- p0_p1: none
- p2_forward_only:
  - P2-1 Rust parser unit tests (addressed post-audit with `#[cfg(test)]` module in `main.rs`)
  - P2-2 no-text key-name assumption documented in `rust_first_observation_substrate.yaml`
  - P2-3 handoff pytest scope clarified above
- t411_gate: substrate safety cleared; owner launch + clean T411 preflight still required before Cursor run

---

## Handoff refresh: final

- agent_name: Codex
- mode:
- updated_at: 2026-06-30T23:28:27+00:00
- handoff_id: 744cd29ffbba7d4b
