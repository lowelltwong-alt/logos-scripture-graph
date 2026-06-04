# Agent Coordination Guide

This file gives non-Claude agents the same operating contract as `CLAUDE.md`.

## Required entry files

All agents begin at:

1. `AI_FRONT_DOOR.md`
2. `.ai/control/MASTER_CONTEXT.md` (read only — human-gated)
3. `.ai/control/PROJECT_STATUS.md`

## Standard agent outputs

Each agent produces:

```text
.ai/handoffs/<task_id>/handoff.md
```

Updates after tasks:

```text
.ai/control/PROJECT_STATUS.md
.ai/context/agent_work/   (optional session notes)
```

Master context proposals (never direct edits):

```text
.ai/context/recommendations/   via propose_master_context_change.py
```

Each handoff must include:

- task id
- agent name
- mode
- files read
- files changed
- decisions made
- validation performed
- risks introduced
- unresolved questions
- exact next action for the next agent

## Validation gates (required)

```bash
python scripts/validate_all.py
python -m pytest -q
```

## Agent roles

Canonical role definitions live in:

```text
config/agents/agent_roles.yaml
```

## Forced handoff rule

A task is not considered complete unless a handoff exists and validates.

Run:

```bash
python scripts/agent/force_handoff.py --task-id <TASK_ID> --agent <AGENT_NAME> --stage start
python scripts/agent/force_handoff.py --task-id <TASK_ID> --agent <AGENT_NAME> --stage final
python scripts/agent/validate_handoffs.py
```
