# Task Handoff

## Task

- task_id: T395
- title: SQLite Source Catalog Schema Shell
- phase: phase_5
- status: complete_source_catalog_seed_only

## Agent

- agent_name: Codex
- mode: build
- stage: start
- updated_at: 2026-06-23T01:27:45+00:00
- handoff_id: b0928fc3253e0359

## Files read

- AGENTS.md
- .ai/tasks/T390.task.yaml
- .ai/tasks/T391.task.yaml
- .ai/tasks/T395.task.yaml
- .ai/control/manuscript_source_catalog_metadata_plan.yaml
- .ai/control/manuscript_source_catalog_research_packet.yaml
- .ai/control/chunking_lesson_index.yaml
- .ai/control/chunking_theological_decision_register.yaml
- scripts/validate_all.py
- scripts/agent/force_handoff.py

## Files changed

- .ai/control/manuscript_source_catalog_sqlite_shell.yaml
- .ai/tasks/T395.task.yaml
- .ai/handoffs/T395/handoff.md
- data/candidate/source_catalog/manuscript_reliability/sqlite/schema.sql
- data/candidate/source_catalog/manuscript_reliability/sqlite/seed_rows.jsonl
- data/candidate/source_catalog/manuscript_reliability/sqlite/manifest.yaml
- docs/roadmap/T395_SQLITE_SOURCE_CATALOG_SCHEMA_SHELL.md
- scripts/validate_manuscript_source_catalog_sqlite_shell.py
- tests/test_manuscript_source_catalog_sqlite_shell.py
- AI_FRONT_DOOR.md
- AI_TABLE_OF_CONTENTS.md
- docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md
- ROADMAP_STATE.yaml
- .ai/control/PROJECT_STATUS.md
- .ai/control/chunking_theological_decision_register.yaml
- .ai/control/chunking_lesson_index.yaml
- .ai/control/roadmap_events.jsonl
- .ai/control/handoff_ledger.jsonl
- .ai/control/DATA_MAP.md
- scripts/validate_all.py

## Decisions made

- Created only a schema shell and source-catalog seed metadata, not a committed SQLite database file.
- Used `scripture_*` and `evidence_*` namespaces only. No `canonical_*`, `boundary_*`, or `doctrine_*` table/view was created.
- Seeded only four source-authority tables: `scripture_source_family`, `scripture_source_catalog`, `evidence_source_catalog_method_profile`, and `evidence_source_trust_rule`.
- Left witness, identifier, date, material, coverage, discovery, holding-institution, and review-queue tables empty.
- Required source URL, method, confidence, provenance, review status, source family, rights/access status, and non-authorizing scope label on every seed row.
- Preserved the boundary that this packet cannot import source text, transcriptions, Bible text, preferred readings, graph edges, vector/retrieval output, or apologetic conclusions as authority.
- Built T395 as a fresh branch from live `origin/main` after T391 was squash-merged.
- Fixed `scripts/validate_all.py` so local validation detects untracked `.ai/tasks/<task>.task.yaml` files before falling back to current-focus task scope.

## Validation run

- command: `python scripts\validate_manuscript_source_catalog_sqlite_shell.py`
- result: passed; 12 tables, 37 seeded source rows, 8 empty shell tables
- failures: none
- command: `python -m pytest -q tests\test_manuscript_source_catalog_sqlite_shell.py tests\test_chunking_lesson_index.py`
- result: passed; 13 passed in 1.22s
- failures: none
- command: `python scripts\validate_chunking_lesson_index.py --index .ai\control\chunking_lesson_index.yaml --changed-file .ai\control\chunking_lesson_index.yaml --index-updated true`
- result: passed
- failures: none
- command: `python scripts\validate_chunking_theological_decision_register.py --changed-file data/candidate/source_catalog/manuscript_reliability/sqlite/schema.sql --changed-file .ai/control/chunking_theological_decision_register.yaml --register-updated true`
- result: passed
- failures: none
- command: `python scripts\validate_task_scope.py --task-id T395 --base-ref origin/main`
- result: passed
- failures: none
- command: `python scripts\validate_all.py`
- result: passed; all validation gates passed
- failures: none
- command: `python -m pytest -q`
- result: passed; 580 passed in 500.08s
- failures: none

## Known risks

- This branch starts from live `origin/main` after T391. The earlier PR #110 was superseded because it merged into the old T391 branch instead of `main`.
- The T395 seed data records source metadata only. It does not populate real manuscript witness rows.
- No generated canonical JSONL artifacts are part of the T395 commit.

## Open questions

- After T391 and T395 are on live `origin/main`, should the first witness population task start with DSS biblical witnesses only, or with a tiny mixed smoke set across DSS plus NT papyri/codices?
- Should the eventual binary SQLite database be generated in CI/release artifacts rather than committed?

## Next agent instruction

After T391 and T395 are on live `origin/main`, create a small DSS biblical witness source-row population task. Begin with a premortem and red-team pass, then fix every P0/P1 risk before editing. Populate only row-level metadata anchored to official/academic source URLs, with method, confidence, provenance, review status, rights/access status, and non-authorizing labels. Do not import source text, transcriptions, Bible text, non-biblical Qumran content, preferred readings, graph/retrieval/vector output, or apologetic conclusions as authority.

---

## Handoff refresh: final

- agent_name: Codex
- mode: build
- updated_at: 2026-06-23T13:58:00+00:00
- handoff_id: t395-main-final
