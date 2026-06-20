# T382 No-Context Audit Surface

## Scope

T382 is a non-output-changing governance/preflight task. It adds a tagged chunking lesson index and
validator so future agents can discover reusable lessons by category, tag, use-when trigger,
related decision/task, downstream risk, non-authorization, and validator.

## Primary Artifacts

- `.ai/control/chunking_lesson_index.yaml`
- `scripts/validate_chunking_lesson_index.py`
- `tests/test_chunking_lesson_index.py`
- `docs/roadmap/T382_CHUNKING_LESSON_INDEX.md`
- `.ai/tasks/T382.task.yaml`
- `.ai/handoffs/T382/handoff.md`

## What Changed

- Added the machine-readable lesson index and lesson graph.
- Made the lesson index mandatory chunking-agent preflight reading.
- Added `WORKFLOW-LESSON-005` to the workflow lesson collector.
- Added `CD-058` to the chunking theological decision register.
- Added changed-path validation so lesson/preflight/methodology/register/audit/TOC changes require the index to update.
- Exposed the new surface through the AI front door, AI TOCs, readiness map, task scope, handoff, and project status.

## Non-Authorizations

T382 does not authorize:

- chunk output changes
- reviewed-gold promotion
- route behavior changes
- evaluator changes
- graph edge generation
- retrieval truth
- vector or embedding work
- boundary import
- theology claims from lesson tags
- owner decisions from the lesson index

## Next Gate

T376 owner lane selection remains the next human decision gate after T382. Do not select a lane or
begin output-changing chunk work from this audit surface.
