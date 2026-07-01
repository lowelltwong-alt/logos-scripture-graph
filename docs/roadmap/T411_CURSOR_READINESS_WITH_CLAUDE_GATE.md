# T411 Cursor Readiness With Claude Final-Audit Gate

T411 prepares the first Cursor short-book research/review-prep batch after T410. It does not start Cursor, create output, promote reviewed gold, add child spans, or change route/evaluator behavior. After T412, T411 is also ledger-first: Cursor must consume the Rust observation substrate pack by default instead of rereading the whole raw Bible.

## Claude Gate

Claude's final T410 audit against `main @ 3c2770f` found no P0/P1 blockers for T411 setup. Claude's **T412 post-merge audit** against `main @ e90bc3d` issued **APPROVE_T411_CURSOR** with no P0/P1 (`.ai/audits/reports/20260630-T412-post-merge-claude-audit.md`). Cursor still must not run until **owner launch** and:

- `.ai/tasks/T411.task.yaml` exists and declares the exact task branch.
- `.ai/handoffs/T411/handoff.md` exists.
- the first candidate batch is owner/Codex supplied, not Cursor selected.
- `scripts/validate_t411_cursor_batch_artifacts.py` exists and passes setup mode.
- T412 Rust-first observation substrate validates with `python scripts/validate_rust_observation_substrate.py --input build/observation_substrate/current`.
- `python scripts/build_cursor_observation_pack.py --input build/observation_substrate/current --task-id T411 --check` passes.
- a clean T411 branch/worktree passes `python scripts/validate_parallel_execution_safety.py --task-id T411 --require-task-branch`.

Claude's forward P2-a is closed by the emitted-artifact validator. P2-b, cross-task status consistency, is logged as future broader validator work. P2-c is addressed by adding duplicate-worktree test coverage to the live-safety validator tests.

## First Batch

| Candidate | Parent Span | Lane | Risk Notes |
| --- | --- | --- | --- |
| `T402-LC-063` | `2John.1.1-2John.1.3` | epistle opening/greeting | "elect lady" identity and ecclesiology remain non-authorizing |
| `T402-LC-057` | `Phlm.1.1-Phlm.1.7` | epistle opening/greeting/thanksgiving | slavery and social ethics application remain non-authorizing |
| `T402-LC-032` | `Jonah.1.1-Jonah.1.3` | Hebrew narrative scene/notice | typology and prophetic theology remain non-authorizing |

## Cursor Contract

Cursor may write only:

- `.ai/context/agent_work/T411/`
- `.ai/handoffs/T411/`

Every future Cursor packet must expose:

- `source_size_manifest.jsonl`
- `confidence_register.jsonl`
- `audit_log.jsonl`
- `claim_traceability_matrix.md`
- `cursor_notes_to_codex.md`
- `escalation_packets/` when low confidence, theology sensitivity, or escalation triggers appear

All source metadata, Strong's tags, paragraph markers, headings, and raw-source observations are evidence-only. No Cursor artifact can authorize target selection, reviewed gold, child spans, chunk output, route/evaluator behavior, graph/retrieval/vector truth, embeddings/indexes, source rows, canon changes, source-tradition preference, or theology authority.

Cursor may inspect raw USFM only for an exact supplied span exception or an escalation packet, and must log bytes/chars/lines/hashes and limitations. Whole-Bible raw rereads by Cursor are blocked by T412.

## Validation

```bash
python scripts/validate_parallel_execution_safety.py --task-id T411 --allow-current-task-dirty --require-task-branch
python scripts/validate_rust_observation_substrate.py --input build/observation_substrate/current
python scripts/build_cursor_observation_pack.py --input build/observation_substrate/current --task-id T411 --check
python scripts/validate_t411_cursor_batch_artifacts.py
python -m pytest tests/test_t411_cursor_batch_artifacts.py -q
python -m pytest tests/test_parallel_execution_safety.py -q
python scripts/validate_task_scope.py --task-id T411
python scripts/agent/validate_handoffs.py
python scripts/validate_all.py
python -m pytest -q
python scripts/generate_data_map.py --check
git diff --check
```

Use the repo's long timeout ceiling for `validate_all.py` and full pytest.
