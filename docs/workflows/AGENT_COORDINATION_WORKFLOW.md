# Agent Coordination Workflow

## Step 1: Enter through front door

Every agent reads `AI_FRONT_DOOR.md`.

## Step 2: Claim or create task

Use `ROADMAP_STATE.yaml` to find a planned task. If no task exists, create `.ai/tasks/<task_id>.task.yaml` from template and add it to roadmap state.

## Step 3: Create deterministic handoff

```bash
python scripts/agent/force_handoff.py --task-id <ID> --agent <NAME> --stage start
```

## Step 4: Work within scope

Agents may only modify files allowed by the task. Architecture changes require an ADR.

## Step 5: Validate

Run:

```bash
python scripts/validate_repo.py
python scripts/agent/validate_handoffs.py
```

## Step 6: Final handoff

```bash
python scripts/agent/force_handoff.py --task-id <ID> --agent <NAME> --stage final
```

Then edit `.ai/handoffs/<ID>/handoff.md` with exact work performed.

## Step 7: Roadmap event

If task status or roadmap changed, append a JSON line to `.ai/control/roadmap_events.jsonl`.
