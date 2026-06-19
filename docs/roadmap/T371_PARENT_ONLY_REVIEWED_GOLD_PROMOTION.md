---
object_type: roadmap_task_note
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-19 during T371 after the maintainer confirmed path T371-A."
reason_for_inclusion: "Give auditors and future agents a human-readable explanation of the T371-A parent-only reviewed-gold promotion and its limits."
---

# T371 Parent-Only Reviewed-Gold Promotion

## Decision

Lowell confirmed `T371-A` on 2026-06-19. The repo records that decision in:

- `.ai/control/t371_parent_only_reviewed_gold_promotion.yaml`
- `eval/chunking_gold/per_form/epistle_argument_gold_manifest.json`
- `.ai/control/chunking_theological_decision_register.yaml` entry `CD-047`

The exact promoted parent-only reviewed-gold span is:

```text
1Cor.8.1-1Cor.10.33
```

## Variant Dependency

The decision is variant-non-dependent only with respect to:

- `1Cor.9.20`
- `1Cor.10.9`

That means the parent boundary and parent-only reviewed-gold claim do not depend on choosing those readings. It does not select a preferred reading, source-tradition preference, critical-text default, majority-text default, Textus Receptus default, or current-source textual policy.

## Non-Authorizations

This task does not authorize:

- child spans
- parent span as a chunk boundary
- route or evaluator behavior changes
- graph edges, retrieval truth, embeddings, or vectors
- preferred readings or source-tradition preference
- sacramental, ecclesial, Christian-liberty, law/gospel, covenant, or denominational system selection
- implementation
- chunk output changes

## Next Route

The next safe route is:

```text
T372 - Route-Isolated Implementation Harness And Non-Target Identity Plan
```

`T372` is harness-only and non-output-changing. `T373` remains the owner gate before any exact implementation or output-changing work.
