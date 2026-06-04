# ADR-0004: Deterministic agent handoff

## Status

Accepted

## Decision

Every task has exactly one active handoff path:

```text
.ai/handoffs/<task_id>/handoff.md
```

## Rationale

Multiple agents will work on the same repository. Chat transcripts are not a reliable coordination layer. Deterministic handoff files make progress, open questions, and next actions discoverable.

## Consequences

- Agents must create a handoff before substantial work.
- A task cannot be marked complete without a handoff.
- Roadmap changes must be reflected in `ROADMAP_STATE.yaml` and `.ai/control/roadmap_events.jsonl`.
- CI should eventually fail if active tasks lack handoffs.
