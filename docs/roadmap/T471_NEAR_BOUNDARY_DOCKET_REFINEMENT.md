# T471 Near-Boundary Docket Refinement

T471 is the bridge from the raw T464/T465 comparison outputs into the first
owner-facing packet batch. It does not rerun model marathons and does not mutate
the frozen T464 comparison artifacts. It reads those ledgers and writes a
T471-owned refinement layer under `.ai/context/agent_work/T471/`.

## Purpose

The T464 compare produced 1,048 disagreement deltas and the T465 reconciliation
gate identified a 19-row M4/M6 candidate docket. T470 then required future work
to distinguish what is well-supported, how it was concluded, what is debated,
and what downstream implication follows.

T471 applies that rule:

- separate tiny near-boundary offsets from real literary/discourse disagreement,
- keep frontier and hard-exception rows visible,
- produce support/debate tables for the 19 M4/M6 candidates,
- name the first likely T472 owner-packet candidate,
- preserve every non-authorization.

## Outputs

- `near_boundary_delta_refinement.jsonl`: one T471 row per T464 delta.
- `owner_candidate_support_debate_docket.yaml`: the 19 T465 owner candidates
  with T470-style support/debate tables.
- `refinement_summary.md`: counts, recommended next route, and non-authorities.

## Recommended Next Route

Use `DELTA-2John-001` (`2John.1.1-2John.1.13`) as the first T472 packet
candidate because it is short, epistle-form driven, and aligned by the preferred
M4/M6 evidence lens. That recommendation is not owner selection, reviewed gold,
or chunk output.

## Non-Authorizations

T471 authorizes no target selection, reviewed gold, chunk output, child spans,
route/evaluator behavior, graph/retrieval/vector truth, source-tradition choice,
canon change, variant/inspiration decision, DAD reporting success gate, or
theology authority.
