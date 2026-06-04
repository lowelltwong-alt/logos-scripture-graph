# Roadmap Change Workflow

Roadmap changes are controlled changes.

## When to update roadmap state

Update `ROADMAP_STATE.yaml` when:

- task status changes
- owner changes
- task scope changes
- phase sequencing changes
- new task is added
- task is blocked
- acceptance criteria change

## Required event log

Append one JSON line to `.ai/control/roadmap_events.jsonl`:

```json
{"event":"task_status_changed","task_id":"T001","from":"planned","to":"in_progress","agent":"claude","reason":"started chunking policy review","timestamp":"2026-05-28T00:00:00Z"}
```

## Roadmap correction rule

If an agent determines the roadmap is wrong, it may propose a correction, but must include:

- reason
- affected tasks
- downstream impacts
- files changed
- migration path
- handoff explanation
