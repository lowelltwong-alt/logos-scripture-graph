# Task Handoff

## Task

- task_id: T520
- title: Publish scrubbed public showcase and contributor research map
- phase: phase_4
- status: in_progress

## Agent

- agent_name: cursor
- mode: build
- stage: final
- updated_at: 2026-07-20T23:30:00+00:00
- handoff_id: a1b2c3d4e5f60718

## Files read

- AI_FRONT_DOOR.md
- docs/public/LOGOS_SCRIPTURE_GRAPH_PUBLIC_SHOWCASE.md
- docs/public/CONTRIBUTOR_RESEARCH_MAP.md

## Files changed

- docs/public/LOGOS_SCRIPTURE_GRAPH_PUBLIC_SHOWCASE.md
- docs/public/CONTRIBUTOR_RESEARCH_MAP.md
- .ai/tasks/T520.task.yaml
- .ai/handoffs/T520/handoff.md

## Decisions made

- Public showcase uses Leipzig IIIF web derivatives (PDM 1.0), not local data/raw binaries.
- Local showcase JPEGs remain on preserve/t470-t478-nas-scholarship-mirror for later rights-gated admission.

## Validation run

- command: python scripts/validate_task_scope.py --task-id T520
- result: pending_push
- failures: none expected for docs-only scope

## Known risks

- Empty-task PRs previously fell through to T417 scope; T520 task file prevents that fallback.

## Open questions

- None for this docs-only surface.

## Next agent instruction

1. Merge PR #190 when CI is green.
2. Keep NAS/scholarship work on preserve/t470-t478-nas-scholarship-mirror until separately scoped.
3. Proceed to T475 shadow re-freeze after T519 merge (already on main).

---

## Handoff refresh: final

- agent_name: cursor
- mode: 
- updated_at: 2026-07-20T23:26:19+00:00
- handoff_id: 370180b842946033
