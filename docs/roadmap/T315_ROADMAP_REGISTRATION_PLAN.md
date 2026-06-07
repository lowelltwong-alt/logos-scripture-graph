# T315 Roadmap Registration Plan

Status: broad future roadmap-state registration deferred.

## Confirmed

- `ROADMAP_STATE.yaml` uses task entries with `required_handoff` paths.
- `scripts/agent/validate_handoffs.py` validates every `required_handoff` path referenced in
  `ROADMAP_STATE.yaml`.
- T315 has an active handoff at `.ai/handoffs/T315/handoff.md`.
- Future tasks T313, T316, T320, T321, T330, and T340 do not all have complete handoff packets yet.

## Decision

T315 registers only the current T315 task in `ROADMAP_STATE.yaml`, because that task has a real
handoff. T315 does not broadly add future task entries. Adding many future tasks with required
handoff references would either fail validation or require creating placeholder handoffs for tasks
that have not started. That would make the state file look more settled than the roadmap actually is.

Instead, T315 registers the future lanes in this plan and in project status/handoff prose.

## Proposed Future Registration

When the owner wants machine-readable registration, add entries with real handoffs:

| Task | Proposed phase | Proposed status | Primary lane |
| --- | --- | --- | --- |
| T313 | phase_3 or phase_4 | planned | evaluator |
| T314 | phase_3 | complete | evaluator |
| T315 | phase_3 | complete | methodology/governance |
| T316 | phase_4 | planned | gold/stress atlas |
| T320 | phase_8 | planned | entity layer |
| T321 | phase_8 or upstream sibling lane | planned | boundary texts / heterodoxy controls |
| T330 | phase_8 | planned | concept graph |
| T340 | phase_8 | planned | retrieval/rendering |

## Required Follow-Up For Registration

For each task:

- create `.ai/tasks/<task_id>.task.yaml`;
- create or start `.ai/handoffs/<task_id>/handoff.md`;
- add a `ROADMAP_STATE.yaml` entry with a matching `required_handoff`;
- append `.ai/control/roadmap_events.jsonl`;
- run `python scripts/agent/validate_handoffs.py`;
- run `python scripts/validate_all.py`.

## Unknown

- Whether T321 belongs in this Bible repository or should be a separate boundary-literature lane
  under upstream governance.
- Whether T320/T330/T340 should live in phase_8 or get dedicated future phases once schemas are
  approved.
