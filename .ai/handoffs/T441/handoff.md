# T441 Handoff

Task id: T441
Agent name: Codex
Mode: Rust no-text coverage/index leaf tool, non-authorizing

## Summary

T441 adds a Rust binary inside the existing original-language observation scanner crate. The binary emits no-text generated coverage ledgers for T439 Philemon and T436/T440 Jonah fixtures, while Python remains the authority validator.

## Files Read

- `AI_FRONT_DOOR.md`
- `.ai/control/MASTER_CONTEXT.md`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/original_language_evidence_substrate.yaml`
- `.ai/control/t439_phlm_alignment_bridge_expansion.yaml`
- `.ai/control/t440_jonah_hebrew_parser_contract.yaml`
- `scripts/validate_t435_original_language_observation_scanner.py`
- `scripts/validate_t439_phlm_alignment_bridge_expansion.py`
- `scripts/validate_t440_jonah_hebrew_parser_contract.py`
- `tools/original_language_observation_scanner/src/main.rs`
- DAD Rust guidance under `C:/Users/lowel/OneDrive/Desktop/Git Projects/04_Digital_Assett_Directory`

## Files Changed

- `.ai/control/t441_rust_alignment_coverage_index.yaml`
- `.ai/tasks/T441.task.yaml`
- `.ai/handoffs/T441/handoff.md`
- `.ai/context/agent_work/T441/dad_preflight.md`
- `docs/roadmap/T441_RUST_ALIGNMENT_COVERAGE_INDEX.md`
- `tools/original_language_observation_scanner/src/bin/t441_alignment_coverage.rs`
- `scripts/validate_t441_rust_alignment_coverage_index.py`
- `tests/test_t441_rust_alignment_coverage_index.py`
- `.ai/control/original_language_evidence_substrate.yaml`
- `.ai/control/current_focus.yaml`
- `.ai/control/PROJECT_STATUS.md`
- `.ai/control/DATA_MAP.md`
- `.ai/control/chunking_theological_decision_register.yaml`
- `.ai/control/handoff_ledger.jsonl`
- `.digital-asset/mail/outbox.jsonl`
- `scripts/validate_all.py`

## Decisions Made

- Keep T441 in the existing Rust scanner crate, with a separate binary to avoid destabilizing the T435 command.
- Treat "index" as a generated no-text coverage ledger, not retrieval/vector indexing.
- Preserve T439 low-confidence verse-level bridge semantics and T440 Jonah parser semantics.
- Keep full Rust generated validation out of routine `validate_all.py`; contract mode is fast.

## Validation Performed

- `cargo test --manifest-path tools/original_language_observation_scanner/Cargo.toml --bins` -> passed (existing T435 binary tests plus T441 binary tests).
- `cargo run --manifest-path tools/original_language_observation_scanner/Cargo.toml --bin t441_alignment_coverage -- --t439-root data/candidate/original_language_evidence/pilots/T439_phlm_alignment_bridge_expansion --t436-root data/candidate/original_language_evidence/pilots/T436_jonah_hebrew_observation_parity --t440-control .ai/control/t440_jonah_hebrew_parser_contract.yaml --out build/original_language_observation/T441/alignment_coverage --no-authority --no-text` -> passed; wrote 3 source rows, 121 coverage rows, and 9 guardrail rows to ignored build output.
- `python scripts/validate_t441_rust_alignment_coverage_index.py --input build/original_language_observation/T441/alignment_coverage` -> passed.
- `python -m pytest tests/test_t441_rust_alignment_coverage_index.py -q` -> 6 passed.
- `python scripts/validate_t439_phlm_alignment_bridge_expansion.py` -> passed.
- `python scripts/validate_t440_jonah_hebrew_parser_contract.py` -> passed.
- `python scripts/validate_t430_original_language_evidence_substrate.py` -> passed.
- `python scripts/validate_task_scope.py --task-id T441 --base-ref origin/codex/t440-jonah-hebrew-parser-contract` -> passed.
- `python scripts/agent/validate_handoffs.py` -> passed.
- `python scripts/validate_chunking_theological_decision_register.py --base-ref origin/codex/t440-jonah-hebrew-parser-contract` -> passed.
- `python scripts/generate_data_map.py --check` -> passed.
- `git diff --check` -> passed with only line-ending warnings on existing control/generated files.
- `python scripts/validate_all.py` -> passed after adding the untracked Rust `src/bin/` directory itself to T441 allowed paths.
- `python -m pytest -q` -> 786 passed in 668.40s.

## Risks Introduced

- Future agents could overread coverage rows as alignment truth. The validator and control surfaces explicitly reject that.

## Unresolved Questions

- Whether T442 should open a production candidate-root decision packet or first add another no-text pilot over a second Greek/Hebrew book.

## Exact Next Action

Open the stacked T441 PR against `codex/t440-jonah-hebrew-parser-contract`, then after review prepare T442 as an owner-gated production candidate-root decision packet or one more no-text pilot if coverage risk remains.
