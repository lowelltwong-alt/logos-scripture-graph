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

## Merge-state principle

A roadmap merge records state; it does not by itself authorize implementation, output changes,
reviewed-gold promotion, boundary imports, or skill lifecycle promotion.

## Roadmap correction rule

If an agent determines the roadmap is wrong, it may propose a correction, but must include:

- reason
- affected tasks
- downstream impacts
- files changed
- migration path
- handoff explanation

## Unintended-consequence review rule

For high-leverage roadmap, authority, routing, evaluator, default-behavior, corpus-scope,
generated-artifact, automation, cross-repo, workflow-rule, or master-chunker changes, run the
unintended-consequence review in `docs/methodology/UNINTENDED_CONSEQUENCE_REVIEW.md` before merge.

The required question is:

```text
What could this change accidentally authorize, weaken, contaminate, overfit, globalize, or make harder to reverse?
```

## Workflow lesson rule

When a roadmap change exposes a reusable generated-artifact, boundary-intake, candidate-promotion,
or downstream-handoff rule, update `docs/methodology/WORKFLOW_LESSONS.md` or record why the lesson
collector did not need a change.
