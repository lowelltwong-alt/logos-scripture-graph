---
object_type: roadmap_report
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-29 by Codex during T404 as the human-readable companion to the Cursor low-risk chunking handoff."
reason_for_inclusion: "Explain how Cursor may help with low-level compute-intensive chunking prep while remaining review-only and non-authorizing."
---

# T404 Cursor Low-Risk Chunking Handoff

## Status

T404 is non-output-changing control-plane work.

It gives Cursor a deterministic handoff contract, project rule, and slash-command prompts for
low-risk chunking prep after T402. Cursor may help with compute-heavy review preparation, queue
inspection, metrics, and handoff packaging, but it may not choose targets, promote reviewed gold,
change chunks, change routes, change evaluator behavior, generate graph/retrieval/vector truth,
import boundary material, add source rows, choose a backend, promote profiles, or claim theology
authority.

## Low-Risk Definition

Low risk means all of these are true:

- the candidate is explicitly supplied by Lowell or Codex;
- the candidate exists in `.ai/control/whole_bible_low_complexity_chunking_candidate_queue.yaml`;
- the candidate status is exactly `ready_for_review_packet`;
- no variant/source-tradition, theological-risk, WJ/speaker, original-language-review, child-span,
  route, evaluator, graph/retrieval/vector, boundary-import, source-row, canon-scope, or theology
  stop condition is present;
- the work is review-only or candidate-only and leaves raw/canonical/processed/derived/eval-gold
  and runtime behavior untouched.

Cursor must stop if it has to pick the target itself.

## Research Completion Verdict

The low-risk research is complete at T402 triage depth: the queue covers all 66 canonical books and
records 38 `ready_for_review_packet` candidates.

It is not complete at review-packet, reviewed-gold, child-span, output, route/evaluator,
graph/retrieval/vector, boundary-import, source-row, backend/profile, canon-scope, or
theology-authority depth. That next work is staged in
`.ai/control/low_risk_chunking_multi_pass_plan.yaml`.

## Cursor Modes

Use Cursor Plan mode first for preflight, exact target confirmation, risk classification, and a
validation plan. Use Cursor Agent mode only after the scope is explicit and only for task-scoped
review-only artifacts. Use Ask mode when authority or target scope is unclear.

Project slash commands are provided under `.cursor/commands/`:

- `/chunking-preflight`
- `/low-risk-chunking-candidate`
- `/codex-review-packet`

The repo-local Cursor rule is `.cursor/rules/logos-scripture-low-risk-chunking.mdc`.

## Algorithms

1. Run `/chunking-preflight` in Plan mode and read the mandatory files in
   `.ai/control/cursor_low_risk_chunking_handoff.yaml`.
2. Confirm the exact target was supplied by Lowell or Codex.
3. Verify the target's T402 queue status is `ready_for_review_packet`.
4. Reject any stop condition before edits.
5. If allowed, run only read-only metrics, focused validators, or task-scoped review-only notes.
6. Prepare `/codex-review-packet` output with files read, files changed, commands, validation,
   timeout ceilings, stop conditions checked, and exact Codex review questions.

## Future Pass

T406 is placed on the future roadmap as a Cursor-assisted low-risk candidate research batch. It may
prepare at most three exact owner-or-Codex supplied `ready_for_review_packet` targets for Codex
review. T406 remains review-packet prep only and authorizes no implementation.

## Validation

Run:

```bash
python scripts/validate_cursor_low_risk_chunking_handoff.py
python -m pytest tests/test_cursor_low_risk_chunking_handoff.py -q
python scripts/validate_task_scope.py --task-id T404
python scripts/validate_all.py
python -m pytest -q
```

Before repo-wide validation or full pytest, read `.ai/control/test_runtime_preflight.yaml` and use
the recorded timeout ceilings on the first run.
