# T471 Near-Boundary Refinement Summary

T471 refines T464/T465 comparison evidence without mutating the frozen comparison outputs.

## Refined Delta Counts
- codex_fable_owner_ready_candidate: 19
- frontier_review_required: 951
- harness_fix_or_rerun_required: 78
- minor_near_boundary_offset: 0
- owner_decision_required: 0
- real_literary_disagreement: 0

## Recommended First T472 Candidate
- source_id: DELTA-2John-001
- span: 2John.1.1-2John.1.13
- status: owner-packet candidate evidence only

## How To Use This
- Use `minor_near_boundary_offset` rows for WindowDiff/near-boundary review before escalation.
- Use `codex_fable_owner_ready_candidate` rows to prepare owner packets, starting with the recommended first candidate.
- Keep `frontier_review_required` rows with Claude/frontier or specialist lanes.
- Keep `harness_fix_or_rerun_required` rows out of owner promotion until harness issues are addressed.

## Non-Authorizations
- No target selection.
- No reviewed gold.
- No chunk output.
- No child spans.
- No route/evaluator behavior changes.
- No graph/retrieval/vector truth.
- No source-tradition choice, canon change, variant/inspiration decision, or theology authority.
