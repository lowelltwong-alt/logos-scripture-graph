# T412 Post-Merge Frontier Audit — Rust-First Observation Substrate

**Auditor:** Claude (frontier architecture audit)  
**Recorded by:** Codex (deterministic repo recording)  
**Date:** 2026-06-30  
**Merge commit audited:** `e90bc3d0022f612fb3c80775699e85d4b9f3d672` (PR #124)  
**Mode:** read-only audit; no repository writes by auditor

## Verdict

**APPROVE_T411_CURSOR** — two P2s are forward-only; none block T411.

Claude independently rebuilt and ran the Rust scanner on `main @ e90bc3d` (Rust 1.96.1) and reproduced the proof end-to-end. The substrate is safe and sufficient for Cursor to consume compressed ledger packs instead of whole-Bible raw rereads.

## P0 findings

None.

## P1 findings

None. The pre-merge P1 (unproven Rust) is closed by independent reproduction, not only the recorded proof.

## P2 findings (forward-only)

- **P2-1 — Rust crate had zero unit tests.** `cargo test` compiled cleanly but reported `running 0 tests`. Recommend Rust unit tests for core parsers (`markers_in_line`, `strong_ids_in_line`, `parse_number_after_marker`, `usfm_to_osis`, `feature_flags`/`is_risk_flag`). Correctness rested on Python generated-mode validation + synthetic pytest + real-output inspection (confirmed correct).
- **P2-2 — No-text enforced by key-name denylist + text-free-by-construction, not value inspection.** Empirically airtight (0 forbidden keys; anomaly `reason` is a hard-coded diagnostic label). Adequate; document the assumption (recorded in `rust_first_observation_substrate.yaml`).
- **P2-3 — Handoff test-count provenance.** `tests/test_rust_observation_substrate.py` has 9 tests; the T412 handoff cited "29 passed" for a broader combined pytest scope. Reconcile handoff wording for auditability.

## T411 gate clearance

- **cursor_may_proceed_after_substrate:** yes
- **conditions_before_cursor_run:**
  - Record this Claude post-merge clearance deterministically; update `T411.task.yaml` `claude_final_audit_gate` from T410 @ `3c2770f` to T412 post-merge @ `e90bc3d`.
  - Clean T411 task branch/worktree + pass `python scripts/validate_parallel_execution_safety.py --task-id T411 --require-task-branch`.
  - `python scripts/validate_t411_cursor_batch_artifacts.py` present and passing.
  - Owner launch of the batch (Cursor must not self-start).
  - Cursor regenerates (or consumes ignored) substrate and passes generated-mode validation + pack `--check` before batch work.
- **raw_usfm_exception_policy:** confirmed. Ledger-first default stands. Raw USFM read allowed only for an exact owner/Codex-supplied span exception or escalation packet, with bytes/chars/lines/hashes logged, `non_authorizing: true`, and Codex review before owner gate.

## Checklist summary

| Area | Result |
|------|--------|
| A. Authority leakage | No — all rows `non_authorizing:true` / `no_text:true`; CD-079 consistent |
| B. No-text integrity | Adequate — 0 forbidden text keys across ledgers |
| C. Strong's / risk semantics | Correct — 0 `has_strong_*` in `risk_signal_index.jsonl` |
| D. Ledger sufficiency for T411 | Yes for 2John, Phlm, Jonah greeting/opening spans |
| E. Frontier escalation | Still required for theology-sensitive claims; substrate approval does not waive |
| F. Governance / ops | `build/` and `target/` ignored; `validate_all` contract-only; 0 marker anomalies |
| G. T410 relationship | No new P0/P1 beyond T410 audit @ `3c2770f` |

## Spot-check evidence (auditor environment)

- `cargo test` → compiled; 0 tests at audit time (see P2-1).
- `cargo run … scan … --no-text` → 83 books, 38,058 verses, 83 source files.
- `validate_rust_observation_substrate.py --input …` → passed generated mode (66 canonical books, 1,402 spans).
- `build_cursor_observation_pack.py … --task-id T411 --check` → passed.
- `pytest tests/test_rust_observation_substrate.py -q` → 9 passed.
- Strong/risk sanity: 0 `has_strong_*` in risk index; 278,168 Strong occurrence rows.

## Non-authorizations (unchanged)

This audit authorizes none of: target selection, reviewed gold, child spans, chunk output, route/evaluator changes, graph/retrieval/vector truth, embeddings/indexes, boundary import, backend choice, profile promotion, source/manuscript rows, canon changes, or theology authority. It clears **only** the substrate-safety gate so the owner may launch the T411 ledger-first Cursor batch under the conditions above.
