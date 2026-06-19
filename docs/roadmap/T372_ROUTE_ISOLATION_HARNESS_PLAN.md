---
object_type: roadmap_task_note
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-19 during T372 after T371-A parent-only reviewed-gold promotion."
reason_for_inclusion: "Give auditors and future agents a human-readable summary of the route-isolation and non-target identity plan before any implementation work."
---

# T372 Route-Isolation Harness Plan

## Result

T372 adds a non-output-changing harness plan for the 1 Corinthians 8-10 epistle argument lane.
The machine-readable record is:

- `.ai/control/t372_route_isolation_harness_plan.yaml`

It uses the T371-A parent-only reviewed-gold case only as input context:

- parent span: `1Cor.8.1-1Cor.10.33`
- reviewed-gold manifest: `eval/chunking_gold/per_form/epistle_argument_gold_manifest.json`
- promotion record: `.ai/control/t371_parent_only_reviewed_gold_promotion.yaml`

## What The Plan Requires Later

Before any T374 implementation or output-changing PR, a future agent must prove:

- exact T373 owner implementation authorization exists
- child spans are still disallowed unless the owner explicitly selects them
- parent-only gold is not silently treated as an output chunk boundary
- route behavior stays isolated to the exact owner-authorized target
- non-target chunk output identity is proven
- same-baseline evaluation is planned before any improvement claim
- source metadata stays evidence only

## Non-Authorizations

T372 does not authorize implementation, route behavior, evaluator behavior, graph edges, retrieval truth, embeddings, vectors, generated chunks, parent span as chunk boundary, child spans, preferred readings, source-tradition preference, boundary import, or output changes.

## Next Gate

The next route is:

```text
T373 - Owner Implementation Authorization Gate
```

Stop at T373 before any implementation or output-changing work.
