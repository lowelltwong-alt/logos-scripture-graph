# Task Handoff

## Task

- task_id: T388
- title: Legacy Branch Discovery Audit
- phase: phase_7
- status: complete_non_authorizing_audit

## Agent

- agent_name: codex
- mode: plan
- stage: final
- updated_at: 2026-06-22T19:00:00+00:00
- handoff_id: 633b3d0b174194c3

## Files read

- AGENTS.md
- AI_FRONT_DOOR.md
- .ai/control/MASTER_CONTEXT.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/DATA_MAP.md
- ROADMAP.md
- ROADMAP_STATE.yaml
- HANDOFF_PROTOCOL.md
- docs/architecture/ARCHITECTURE.md
- .ai/audits/reports/README.md
- .ai/audits/templates/REVIEW_REPORT_TEMPLATE.md
- .ai/tasks/_TEMPLATE.task.yaml
- .ai/handoffs/_TEMPLATE.handoff.md
- .ai/control/boundary_material_routing.yaml
- .ai/control/chunking_lesson_index.yaml
- .ai/control/boundary_source_intake_plan.yaml
- docs/roadmap/T327F_BOUNDARY_SOURCE_INTAKE_PLANNING.md
- docs/roadmap/T387_MANUSCRIPT_WITNESS_RELIABILITY_SCAFFOLD.md
- git log/diff summaries for feat/scale-connection-discovery-codex-5-5
- git log/diff summaries for t320-t325-boundary-entity-commentary-planning-pack
- selected stale branch docs from T321, T323, T325, and T326

## Files changed

- .ai/tasks/T388.task.yaml
- .ai/handoffs/T388/handoff.md
- .ai/audits/reports/20260622-T388-legacy-branch-discovery-audit.md
- .ai/audits/reports/README.md
- .ai/control/chunking_lesson_index.yaml
- .ai/control/PROJECT_STATUS.md
- .ai/control/current_focus.yaml
- .ai/control/roadmap_events.jsonl
- ROADMAP_STATE.yaml

## Decisions made

- Do not merge feat/scale-connection-discovery-codex-5-5 directly; preserve it only as historical candidate-discovery signal.
- Do not merge t320-t325-boundary-entity-commentary-planning-pack directly; preserve it only as historical planning signal until this audit reaches main.
- Future agents should rediscover the scale branch signal during T308-style candidate adjudication/rerun planning, not by reviving stale candidate files.
- Future agents should rediscover the T320/T325 branch signal during Boundary Literature/commentary/source-marker planning, after reading current T327F/T382/T383/T386/T387 controls.
- LSN-017 records the reusable branch-cleanup lesson: old branches can be rediscovery prompts, not merge authority.

## Validation run

- command: python scripts/validate_chunking_lesson_index.py
- result: passed
- failures: none
- command: python scripts/validate_task_scope.py --task-id T388
- result: passed
- failures: none
- command: python scripts/agent/validate_handoffs.py
- result: passed for 94 referenced handoff path(s)
- failures: none
- command: python scripts/validate_all.py
- result: passed
- failures: none
- command: python -m pytest -q
- result: passed, 542 tests in 409.43s
- failures: none

## Known risks

- The local-only T320/T325 branch remains the only full pointer to its stale files until this audit PR is merged.
- Deleting stale branches before this audit reaches main would make rediscovery depend on chat or reflog memory, so cleanup should finish after merge.

## Open questions

- None for this audit. Any future use of candidate data, graph edges, boundary corpora, or governance changes requires a separate authorized task.

## Next agent instruction

- After this audit PR is merged, delete the stale scale-discovery branch locally/remotely if still present, then delete local t320-t325-boundary-entity-commentary-planning-pack after confirming the audit note is on main.

---

## Handoff refresh: final

- agent_name: codex
- mode: plan
- updated_at: 2026-06-22T19:02:49+00:00
- handoff_id: 16e98db827efa3bb

---

## Handoff refresh: final

- agent_name: codex
- mode: plan
- updated_at: 2026-06-22T19:07:47+00:00
- handoff_id: 16e98db827efa3bb
