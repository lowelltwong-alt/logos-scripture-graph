# Task Handoff

## Task

- task_id: T327B1
- title: Canonical Scope Validator Fail Closed
- phase: phase_4
- status: complete

## Agent

- agent_name: Codex
- mode: build
- stage: final
- updated_at: 2026-06-08T22:00:00+00:00
- handoff_id: t327b1-codex-20260608

## Files read

- AI_FRONT_DOOR.md
- .ai/control/MASTER_CONTEXT.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/DATA_MAP.md
- ROADMAP_STATE.yaml
- HANDOFF_PROTOCOL.md
- docs/architecture/ARCHITECTURE.md
- config/agents/agent_roles.yaml
- scripts/validate_canonical_66_scope.py
- pipelines/util/canonical_scope.py
- tests/test_t327b_canonical_66_ingest_filter.py
- docs/roadmap/T327B_CANONICAL_66_INGEST_FILTER.md
- docs/roadmap/CANONICAL_66_BOOK_SCOPE_POLICY.md

## Files changed

- pipelines/util/canonical_scope.py
- scripts/validate_canonical_66_scope.py
- tests/test_t327b_canonical_66_ingest_filter.py
- docs/roadmap/T327B1_CANONICAL_SCOPE_VALIDATOR_FAIL_CLOSED.md
- docs/roadmap/T327B_CANONICAL_66_INGEST_FILTER.md
- docs/roadmap/CANONICAL_66_BOOK_SCOPE_POLICY.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/roadmap_events.jsonl
- .ai/tasks/T327B1.task.yaml
- .ai/handoffs/T327B1/handoff.md
- ROADMAP_STATE.yaml

## Decisions made

- `CANON-SCOPE-VALIDATOR-001` is implemented for optional canonical JSONL validation.
- Canonical-output records with no resolvable book identity now fail validation instead of passing.
- Valid 66-book records still pass validation.
- Explicitly excluded records, including `GLO` and `FRT`, fail validation.
- Glossary/front-matter/concordance/source metadata remains preservable only as separately scoped
  non-scripture supporting/reference artifacts outside canonical Scripture outputs.
- T327C/D/E/F/G were not started.

## Validation run

- command: `python scripts/validate_canonical_66_scope.py`
- result: passed, canonical 66 scope config validation passed.
- command: `python -m pytest -q tests/test_t327b_canonical_66_ingest_filter.py`
- result: passed, `15 passed`.
- command: `python scripts/validate_all.py`
- result: passed, all validation gates passed.
- command: `python -m pytest -q`
- result: passed, `134 passed`.
- command: `git diff --check`
- result: passed.

## Known risks

- Existing generated canonical outputs remain pre-T327C and may still contain non-66/front/glossary
  records until the isolated regeneration task.
- T327C must be careful to pass the canonical-66 filter and then validate generated canonical
  outputs with this fail-closed behavior.
- This validator does not prove content authenticity when a record is falsely labeled with an
  allowed canonical book identity. Fake, substituted, or altered text labeled `Mark` is a
  source-integrity/provenance risk that must be handled through raw source manifest checksums,
  provenance, parser determinism, and raw immutability controls.

## Open questions

- Whether supporting/reference artifacts for glossary/front matter should get a separate
  non-scripture storage root and validator in a later task.

## Next agent instruction

Claude review next. Merge T327B.1 before T327C. T327C should use the canonical-66 filter and
fail-closed validator. Do not start T327D/E/F.
