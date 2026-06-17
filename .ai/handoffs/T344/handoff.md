# Task Handoff

## Task

- task_id: T344
- title: Select One Revelation Behavior Target
- phase: phase_4
- status: in_progress

## Agent

- agent_name: codex
- mode: plan
- stage: update
- updated_at: 2026-06-17T20:09:48+00:00
- handoff_id: bca0c1ed741f2be7

## Files read

- AI_FRONT_DOOR.md
- .ai/control/chunking_agent_preflight.yaml
- docs/methodology/WORKFLOW_LESSONS.md
- docs/methodology/LOGOS_CHUNKING_WORKFLOW_RULES_REGISTRY.md
- docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md
- .ai/control/chunking_theological_decision_register.yaml
- .ai/control/bible_chunking_readiness_map.yaml
- docs/roadmap/T343_REVELATION_REVIEW_PACKETS_AND_GOLD_CANDIDATES.md
- eval/chunking_gold/review_packets/rev12_14_symbolic_scenes_review.md
- ROADMAP_STATE.yaml
- .ai/audits/README.md
- .ai/audits/NO_CONTEXT_REVIEW_PROTOCOL.md
- .ai/control/audit_surface_map.yaml
- .ai/control/harness_upgrade_roadmap.yaml

## Files changed

- docs/roadmap/T344_REVELATION_OWNER_SELECTION_DOCKET.md
- .ai/tasks/T344.task.yaml
- .ai/handoffs/T344/handoff.md
- ROADMAP_STATE.yaml
- .ai/control/bible_chunking_readiness_map.yaml
- .ai/control/chunking_theological_decision_register.yaml
- .ai/control/current_focus.yaml
- .ai/control/PROJECT_STATUS.md
- .ai/control/roadmap_events.jsonl
- .ai/control/handoff_ledger.jsonl
- .ai/audits/README.md
- .ai/audits/NO_CONTEXT_REVIEW_PROTOCOL.md
- .ai/audits/templates/REVIEW_REPORT_TEMPLATE.md
- .ai/audits/reports/README.md
- .ai/control/audit_surface_map.yaml
- .ai/control/harness_upgrade_roadmap.yaml
- scripts/validate_audit_surface_map.py
- scripts/agent/no_context_audit_harness.py
- AI_TABLE_OF_CONTENTS.md
- AI_FRONT_DOOR.md
- docs/methodology/WORKFLOW_LESSONS.md
- docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md
- tests/test_t344_revelation_owner_selection.py
- tests/test_audit_surface_map.py
- tests/test_ai_roadmap_table_of_contents.py
- tests/test_bible_chunking_readiness_map.py
- tests/test_t337_selection_docs.py
- tests/test_t337a_psalm_review_packet.py
- tests/test_t342_revelation_candidate_selection.py

## Decisions made

- T344 is active as owner-selection only; owner selection remains pending.
- Five stable options were recorded: preserve current behavior, promote parent-only reviewed gold, promote parent plus exact child spans, mark characterization-only, or require more research.
- No option was selected by Codex.
- No Revelation implementation, reviewed gold, output change, route behavior, evaluator change, chunk regeneration, graph edge, embedding/index work, boundary import, source-metadata authority, T327G, or Psalm candidate promotion is authorized.
- Decision register entry CD-016 records that Revelation owner selection is required before reviewed gold or implementation.
- Added a no-context audit path and harness so an independent AI/human reviewer can reconstruct branch/PR intent, changed files, changelogs, decision surfaces, validation, future harness watch conditions, and stop conditions after commit/push without chat context.
- Added a future harness-upgrade roadmap with candidate harnesses for protected-path scope checks, owner-decision consistency, CI parity, review-packet authorization drift, source-metadata authority risk, route leakage, generated artifact reproducibility, cross-repo mirrors, lesson capture, theological label risk, and owner-selection-to-implementation gating.

## Validation run

- command: python scripts/validate_chunking_agent_preflight.py
- result: passed
- failures: none

- command: python scripts/validate_bible_chunking_readiness_map.py
- result: passed
- failures: none

- command: python scripts/validate_chunking_theological_decision_register.py
- result: passed
- failures: none

- command: python scripts/validate_audit_surface_map.py
- result: passed
- failures: none

- command: python -m pytest -q tests/test_t344_revelation_owner_selection.py tests/test_audit_surface_map.py tests/test_ai_roadmap_table_of_contents.py tests/test_bible_chunking_readiness_map.py tests/test_t337_selection_docs.py tests/test_t337a_psalm_review_packet.py tests/test_t342_revelation_candidate_selection.py
- result: 32 passed
- failures: none

- command: python scripts/validate_all.py
- result: all validation gates passed
- failures: none

- command: python -m pytest -q
- result: 273 passed
- failures: none

## Known risks

- A docket can be mistaken for reviewed gold; all authorization flags remain false to prevent that.
- Option C lists exact candidate child spans, but they remain unapproved until owner selection.
- Revelation boundaries can imply chronology, recapitulation, interlude status, symbolic identity, or eschatological school if labels are overread.
- Audit reports can recommend or block but must not be treated as owner authorization.

## Open questions

- Owner must select exactly one option: REV-T344-A, REV-T344-B, REV-T344-C, REV-T344-D, or REV-T344-E.
- If REV-T344-C is selected, owner must confirm whether every listed child span is approved exactly as written.
- Owner may need a later speaker/voice policy before Revelation implementation.

## Next agent instruction

Run the full validation gates, then present the owner with the five T344 options. For independent review, point the reviewer to `.ai/audits/README.md` or generate a brief with `python scripts/agent/no_context_audit_harness.py --task-id T344 --base-ref origin/main --print`. Ask the reviewer to check `.ai/control/harness_upgrade_roadmap.yaml` for any repeated issue that should become a harness. Do not start T345 or edit implementation/gold/output surfaces until Lowell Wong explicitly selects one option and the required governed evidence is updated.
