# T383 No-Context Audit Surface

## Scope

T383 is a non-output-changing governance/preflight task. It records that context always matters
when reading the Bible and makes contextual reading a deterministic preflight requirement for
future chunking, review-packet, graph, retrieval, route, evaluator, and theology-risk work.

## Primary Artifacts

- `.ai/control/contextual_reading_policy.yaml`
- `scripts/validate_contextual_reading_policy.py`
- `tests/test_contextual_reading_policy.py`
- `docs/roadmap/T383_CONTEXTUAL_READING_POLICY.md`
- `.ai/tasks/T383.task.yaml`
- `.ai/handoffs/T383/handoff.md`

## What Changed

- Added layered context requirements: immediate, paragraph/section, chapter/book, canonical,
  original-language, historical/cultural, and source-metadata context.
- Added `LSN-011` to the lesson index and `WORKFLOW-LESSON-006` to workflow lessons.
- Added `CD-059` to the chunking theological decision register.
- Made contextual reading policy mandatory chunking-agent preflight reading.
- Added a validator and tests that fail if the policy loses required layers or starts authorizing
  history, chunks, graph/retrieval truth, or output.

## Non-Authorizations

T383 does not authorize:

- chunk output changes
- reviewed-gold promotion
- route behavior changes
- evaluator changes
- graph edge generation
- retrieval truth
- vector or embedding work
- boundary import
- doctrine from context labels
- history or culture as Scripture authority
- a separate history repo

## Next Gate

T376 owner lane selection remains the next human decision gate after T383.
