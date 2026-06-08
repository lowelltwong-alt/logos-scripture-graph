# Task Handoff

## Task

- task_id: T327A2
- title: Boundary Governance Stop Rules
- phase: phase_4
- status: complete

## Agent

- agent_name: Codex
- mode: plan
- stage: final
- updated_at: 2026-06-08T18:00:00+00:00
- handoff_id: t327a2-codex-20260608

## Files read

- AI_FRONT_DOOR.md
- AI_TABLE_OF_CONTENTS.md
- .ai/control/PROJECT_STATUS.md
- .ai/control/boundary_material_routing.yaml
- docs/roadmap/T327A1_THREE_REPO_ROUTING_GUARDRAILS.md
- tests/test_boundary_material_routing_policy.py

## Files changed

- AI_FRONT_DOOR.md
- AI_TABLE_OF_CONTENTS.md
- .ai/control/boundary_material_routing.yaml
- .ai/control/PROJECT_STATUS.md
- .ai/control/roadmap_events.jsonl
- docs/roadmap/T327A1_THREE_REPO_ROUTING_GUARDRAILS.md
- docs/roadmap/T327A2_BOUNDARY_GOVERNANCE_STOP_RULES.md
- .ai/tasks/T327A2.task.yaml
- .ai/handoffs/T327A2/handoff.md
- ROADMAP_STATE.yaml
- tests/test_boundary_material_routing_policy.py

## Decisions made

- Added `BOUNDARY-GOV-001 - Governance Is Constraint, Not Obstacle`.
- Added `BOUNDARY-GOV-002 - Owner-Reserved Authorization for Boundary-Originated Higher-Layer Changes`.
- Boundary-originated requests that conflict with governance-layer policy, canonical Scripture
  authority, repository-link contracts, routing policy, trust hierarchy, or canonical scope must
  stop and be reviewed in the higher-authority repository.
- Only Lowell Wong, as project owner, may authorize boundary-originated changes to those
  higher-authority surfaces.
- Contributor consensus, contributor volume, automated recommendation, agent routing, and
  boundary-layer operational need are not sufficient authority.
- T327B was not started.

## Validation run

- command: `python scripts/validate_all.py`
- result: passed, all validation gates passed.
- command: `python -m pytest -q`
- result: passed, `119 passed`.
- command: YAML parse checks
- result: passed.
- command: `git diff --check`
- result: passed.

## Known risks

- Child repo wording may need later synchronization if the governance registry changes.

## Open questions

- Whether future child-repo validators should consume governance registry policy directly.

## Next agent instruction

Run validation. Review and merge T327A.2 if green, then run T327B as a separate 66-book allow-list /
ingest-filter task.
