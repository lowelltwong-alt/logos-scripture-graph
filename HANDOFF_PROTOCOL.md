# Deterministic Handoff Protocol

The handoff protocol prevents agent drift. Every task must leave a resumable state packet.

## Required reading before any handoff work

1. `AI_FRONT_DOOR.md`
2. `.ai/control/MASTER_CONTEXT.md` (read only)
3. `.ai/control/PROJECT_STATUS.md`

## Handoff location

```text
.ai/handoffs/<task_id>/handoff.md
```

This path is deterministic. There is exactly one active handoff per task.

## Create or refresh a handoff

```bash
python scripts/agent/force_handoff.py --task-id T001 --agent claude --stage start
python scripts/agent/force_handoff.py --task-id T001 --agent claude --stage final
```

## Handoff sections

Every handoff must contain:

1. `Task`
2. `Agent`
3. `Mode`
4. `Files read`
5. `Files changed`
6. `Decisions made`
7. `Validation run`
8. `Known risks`
9. `Open questions`
10. `Next agent instruction`

## After every handoff update

1. Update `.ai/control/PROJECT_STATUS.md`
2. Run validation:

```bash
python scripts/validate_all.py
python -m pytest -q
```

CI enforces these gates on every push/PR.

## Master context changes

Architectural decisions that change master principles must **not** be written only in handoffs.

- Propose: `python scripts/agent/propose_master_context_change.py --agent <name> --summary "..." --body "..."`
- Human promotes to `.ai/control/MASTER_CONTEXT.md` and runs `approve_master_context.py`

## Roadmap update rules

If the task changes scope, status, owner, or sequencing:

1. Update `ROADMAP_STATE.yaml`.
2. Append an event to `.ai/control/roadmap_events.jsonl`.
3. Explain the change in the handoff.

## Handoff validity

A handoff is invalid if:

- task id does not match folder path
- mode is missing
- files changed are omitted
- validation status is omitted
- next agent instruction is blank
- task is marked complete in `ROADMAP_STATE.yaml` without a handoff
- `validate_control_plane.py` fails

## Why this matters

A multi-agent repo fails when the plan lives in chat transcripts. This protocol forces the plan, progress, and next action into files that any agent can read deterministically.
