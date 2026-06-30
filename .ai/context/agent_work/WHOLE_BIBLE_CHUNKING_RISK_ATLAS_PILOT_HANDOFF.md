# Whole-Bible Chunking Risk Atlas (Pilot) - Handoff

**Status:** research_only_non_authorizing
**Contract scope:** planning_only
**Governance authority:** false
**Agent:** Cursor
**Date:** 2026-06-29
**Repository:** logos-scripture-graph-repo

## Task

Research-only pilot atlas: raw-source marker glossary, Strong's handling notes, Torah
(Genesis-Deuteronomy) chunking risk classification, scaling method for remaining 61 books.

## Mode

Read-only research synthesis into `.ai/context/agent_work/` - no control-plane promotion.

## Branch and worktree

| Field | Value |
| --- | --- |
| Branch | `codex/t406-cursor-artifact-hardening` (current) |
| Prior T406 handoff | `.ai/handoffs/T406/` exists from the same T406 batch |

## Files read

1. `AGENTS.md` (governance conventions)
2. `AI_FRONT_DOOR.md`
3. `.ai/control/MASTER_CONTEXT.md` (read-only)
4. `.ai/control/PROJECT_STATUS.md` (targeted)
5. `.ai/control/RAW_SOURCE_INVENTORY.md`
6. `config/ingest/usfm_marker_coverage.yaml`
7. `.ai/control/chunking_agent_preflight.yaml` (targeted sections)
8. `.ai/control/contextual_reading_policy.yaml`
9. `.ai/control/original_language_phrase_context_policy.yaml`
10. `.ai/control/chunking_lesson_index.yaml` (referenced via preflight)
11. `.ai/control/chunking_theological_decision_register.yaml` (referenced via preflight)
12. `.ai/control/bible_chunking_readiness_map.yaml` (referenced)
13. `.ai/control/whole_bible_low_complexity_chunking_candidate_queue.yaml` (Torah T402 rows)
14. `.ai/control/bible_wide_chunking_research_registry.yaml` (Gen-Deut)
15. `.ai/control/bible_chunking_research_triage_map.yaml`
16. `.ai/control/t398_bible_wide_phase_one_research_synthesis.yaml`
17. `.ai/control/t399_focused_bible_wide_research_queue.yaml` (referenced)
18. `docs/chunking/CHUNKING_DESIGN.md`
19. `docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md` (referenced)
20. `.ai/control/bible_verse_passage_readiness_matrix.yaml` (Torah block)
21. `.ai/control/bible_verse_passage_gap_register.yaml` (gap samples)
22. `.ai/control/source_metadata_research_atlas.yaml`
23. `.ai/context/README.md`

## Files changed

| Action | Path |
| --- | --- |
| Added/hardened | `.ai/context/agent_work/WHOLE_BIBLE_CHUNKING_RISK_ATLAS_PILOT.md` |
| Added/hardened | `.ai/context/agent_work/WHOLE_BIBLE_CHUNKING_RISK_ATLAS_PILOT_HANDOFF.md` |
| Added | `.ai/tasks/T406.task.yaml` |
| Hardened | `.ai/handoffs/T406/handoff.md` |
| Hardened | `.ai/handoffs/T406/candidate_prep/t402_lc_064_3john_opening_greeting_candidate_prep.md` |

## Files not changed (confirmed)

- `.ai/control/**` (including `MASTER_CONTEXT.md`)
- `data/raw/`, `data/canonical/`, `data/processed/`, `data/derived/`
- `eval/chunking_gold/**`
- Chunk pipelines, routes, evaluators, retrieval/graph surfaces

## Non-authorizations confirmed

- No chunking implementation target selected
- No chunk output, reviewed gold, child spans, route/evaluator changes
- No graph/retrieval/vector truth, embeddings, indexes, boundary import
- No backend choice, retrieval-profile promotion, manuscript rows
- No authoritative theology claims
- Atlas not promoted to `.ai/control/`

## Method limits added by Codex review hardening

- The atlas is governed-surface synthesis plus the 2026-06-04 raw-source inventory scan.
- Cursor did not read the full raw USFM archive character by character during the pilot.
- The 83-file / 38,058-verse count is the raw WEB archive superset; `canonical_66` remains 31,103
  verses.
- Torah risk labels are T358/T386/T402/gap-register cross-walks, not per-verse raw verification.
- Book-level labels are triage judgments, not governed classifications.

## Stop conditions checked

| Condition | Result |
| --- | --- |
| Implementation target selection | NONE |
| Control-plane or data-plane edits | NONE |
| Expansion beyond Torah pilot | STOPPED per plan |
| Metadata as boundary authority | AVOIDED in atlas language |

## Validation

| Command | Timeout ceiling (ms) | Result |
| --- | ---: | --- |
| `python scripts/validate_task_scope.py --task-id T406` | 900000 | PASSED |
| `python scripts/agent/validate_handoffs.py` | 900000 | PASSED - 111 referenced handoff path(s) |
| `python scripts/validate_cursor_low_risk_chunking_handoff.py` | 900000 | PASSED |
| `python scripts/validate_t402_low_complexity_chunking_runway.py` | 900000 | PASSED |
| `python -m pytest tests/test_cursor_low_risk_chunking_handoff.py tests/test_t402_low_complexity_chunking_runway.py -q` | 900000 | 13 passed in 6.07s |
| `python scripts/validate_all.py` | 900000 | PASSED - all validation gates passed |
| `python -m pytest -q` | 1800000 | 636 passed in 472.29s |
| `python scripts/generate_data_map.py --check` | 900000 | PASSED - `DATA_MAP.md` is current |
| `git diff --check` | - | PASSED |

**Note:** The prior task-scope failure was expected scope noise because the untracked T406 paths
were being checked against T404. Codex added `.ai/tasks/T406.task.yaml` so these paths can validate
under T406.

## Codex review questions

1. Does the glossary correctly describe eng-web markers without treating them as boundary authority?
2. Are Torah risk assignments evidence-backed and separated (book vs example span)?
3. Does the atlas stay in `agent_work/` without smuggling control-plane authority?
4. Are stop conditions and non-authorizations explicit?
5. Is the scaling method bounded (no whole-Bible single edit)?

## Recommended next actions

1. Codex reviews diff before merge.
2. Owner may authorize T408 strengthening for T402-LC-064 or a separate T409 raw-source
   observation pass.
3. No commit/push unless Lowell explicitly instructs.

## Pilot deliverable

Primary atlas: `.ai/context/agent_work/WHOLE_BIBLE_CHUNKING_RISK_ATLAS_PILOT.md`
