# Task Handoff

## Task

- task_id: T327A
- title: Forensic Canonical Corpus Scope Audit
- phase: phase_4
- status: complete

## Agent

- agent_name: Codex
- mode: plan
- stage: final
- updated_at: 2026-06-08T00:00:00+00:00
- handoff_id: t327a-codex-20260608

## Files read

- AI_FRONT_DOOR.md
- .ai/control/MASTER_CONTEXT.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/DATA_MAP.md
- .ai/control/RAW_SOURCE_INVENTORY.md
- HANDOFF_PROTOCOL.md
- docs/architecture/ARCHITECTURE.md
- docs/chunking/CHUNKING_DESIGN.md
- config/agents/agent_roles.yaml
- ROADMAP_STATE.yaml
- .ai/control/METHODOLOGY_UPDATE_RULES.md
- docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md
- data/raw/bible/eng-web/source_manifest.yaml
- data/raw/bible/eng-web/usfm/eng-web_usfm.zip
- data/processed/bible/eng-web/usfm/usfm_events.jsonl
- data/canonical/scripture/passages/passages.jsonl
- data/canonical/translations/eng-web/*.jsonl
- data/derived/chunks/variants/*/chunks.jsonl
- eval/LEADERBOARD.md
- eval/chunking_runs/*.json
- eval/chunking_gold/**
- tests/**
- git history and GitHub PR metadata for PRs #1, #3, #4, #6, #13, #17, and #22

## Files changed

- docs/roadmap/CANONICAL_66_BOOK_SCOPE_POLICY.md
- docs/roadmap/T327A_FORENSIC_CANONICAL_CORPUS_SCOPE_AUDIT.md
- tests/test_t327a_canonical_scope_audit.py
- docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md
- .ai/control/METHODOLOGY_UPDATE_RULES.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/roadmap_events.jsonl
- .ai/tasks/T327A.task.yaml
- .ai/handoffs/T327A/handoff.md
- ROADMAP_STATE.yaml

## Decisions made

- Methodology updated: yes.
- T327A records the owner decision that `logos-scripture-graph` canonical Scripture/chunking scope is the 66-book canon.
- Deuterocanonical/apocrypha/boundary texts must not enter canonical passages/chunks by default.
- Front matter and glossary are source/editorial artifacts, not Scripture content.
- Raw source archive provenance must be handled through source replacement, ingest filter, or migration planning rather than hand edits.
- Future use of excluded material belongs in `logos-boundary-literature` or another explicitly scoped boundary/tradition repo after separate source/license review.
- Current generated canonical passage and witness outputs contain 81 books and 6,955 excluded non-66 records.
- Current generated chunk variants contain excluded chunks and committed scorecards/leaderboard are wider-corpus lineage.
- T327A is audit/planning only. It does not implement removal, filtering, regeneration, scorecard changes, evaluator changes, or boundary-repo import.
- The standard `force_handoff.py` helper was attempted for T327A but rejects suffix task IDs (`^T\d{3,}$`), while the repo already uses suffix task IDs such as T316b/T316c. This handoff was created manually and validated through `validate_handoffs.py`.

## Validation run

- command: `python -m pytest -q tests/test_t327a_canonical_scope_audit.py`
- result: passed, `7 passed`.
- command: `python scripts/validate_all.py`
- result: passed, all validation gates passed.
- command: `python -m pytest -q`
- result: passed, `109 passed`.
- command: `git diff --name-only -- data/raw data/canonical data/processed data/derived/chunks pipelines/ingest pipelines/chunking/chunker.py pipelines/chunking/orchestrator.py pipelines/chunking/evaluate_chunks.py pipelines/chunking/leaderboard.py eval/chunking_runs eval/LEADERBOARD.md registry/chunking`
- result: no protected-path changes.
- failures: none.

## Known risks

- The current official D / Claude pass2 = 93.5 score is a T314 evaluator-policy baseline over the pre-corpus-scope-correction generated corpus.
- Filtering to 66 books will require regenerated canonical outputs, chunk outputs, scorecards, leaderboard, and updated score language.
- Existing gold/stress/index controls that mention `PrMan`, `Ps151`, AddDan/AddEsth, or other excluded material need cleanup in a later isolated task.
- The raw archive still contains excluded material; whether to retain it with an ingest filter or replace/migrate it remains a separate provenance decision.

## Open questions

- Should the raw WEB archive remain in `logos-scripture-graph` as immutable provenance with an explicit 66-book ingest filter, or should a source replacement/migration task remove it later?
- What source/license package should `logos-boundary-literature` use if excluded material is ever ingested there?
- What is the corpus-corrected D / Claude pass2 score after 66-book filtering and regenerated scorecards?
- Should `force_handoff.py` and `schemas/handoff.schema.json` be updated later to support suffix task IDs already present in the roadmap?

## Next agent instruction

Claude review T327A. If accepted, merge the audit and then plan T327B canonical 66-book allow-list / ingest filter. Do not continue T320/T325/T326 implementation work or implement removal until T327A is reviewed.
