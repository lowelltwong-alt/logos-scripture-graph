# Sol T475 Acceptance Report

## Verdict

READY_FOR_INDEPENDENT_AUDIT

Post-T519 shadow re-freeze is deterministic, exact, no-text, and reusable.
P1 editorial-heading footnote loss is resolved. T476 remains blocked until the
independent Claude audit passes.

## Findings

### Resolved: P1 Editorial Footnote Sidecars

Zero footnote removals. `footnotes.jsonl` is unchanged at 1130 rows, including
the three WEB Psalm descriptive-heading footnotes restored by T519
(`…:2347:0001`, `…:4961:0001`, `…:8067:0001`).

### Resolved: P2 Fixture Coverage

T519 added editorial-inline sidecar fixture coverage before this re-freeze.

## Confirmed Intended Effects

- Footnotes: removed=0, unchanged=1130.
- Word tokens: removed=2 (known bogus Psalm 119 heading-derived tokens),
  unchanged=677686.
- Translation witnesses: modified=48,
  removed=0, added=0.
- Totals: {"added": 0, "modified": 102793, "modified_file": 1, "removed": 2, "unchanged": 741402}.
- Three alternating trials are deterministic.
- Baseline median runtime: 45.220773 s.
- Candidate median runtime: 49.522366 s.
- No chunker ran and no chunk output exists.

## Balanced-Value Gate

Outcome: hold_and_defer_rust.

Candidate median is not faster than baseline in this re-freeze. Speed alone
never advances the gate. Correctness/parity (zero footnote removals with the
intended token cleanup retained) plus failure-isolation in the bounded Python
comparator satisfy the non-speed half of the gate.

## Required Next Route

1. Independent Claude audit via `.ai/prompts/t475_independent_audit_prompt.md`
   against this frozen bundle.
2. Begin T476 only after that audit passes.
3. Do not regenerate committed canonical data in this task.

## Non-Authorizations

This report does not authorize committed regeneration, reviewed gold, chunk
output, source-tradition preference, canon change, route/evaluator behavior,
graph/retrieval/vector truth, or theology authority.

Frozen at: 2026-07-21T00:35:03.800899+00:00
