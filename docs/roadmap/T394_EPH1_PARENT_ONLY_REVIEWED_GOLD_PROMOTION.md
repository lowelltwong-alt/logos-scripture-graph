---
object_type: roadmap_task_report
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-23 during T394 after Lowell explicitly authorized T393-A."
reason_for_inclusion: "Give auditors and future agents a human-readable explanation of the Eph.1.3-Eph.1.14 parent-only reviewed-gold promotion and its limits."
---

# T394 Eph.1.3-Eph.1.14 Parent-Only Reviewed-Gold Promotion

## Decision

Lowell authorized `T393-A` on 2026-06-23. The repo records that decision in:

- `.ai/control/t394_eph1_parent_only_reviewed_gold_promotion.yaml`
- `.ai/control/t393_eph1_reviewed_gold_promotion_decision_packet.yaml`
- `eval/chunking_gold/per_form/epistle_argument_gold_manifest.json`
- `.ai/control/chunking_theological_decision_register.yaml` entry `CD-071`
- `.ai/control/chunking_lesson_index.yaml` entry `LSN-025`

The exact promoted parent-only reviewed-gold span is:

```text
Eph.1.3-Eph.1.14
```

## Variant And Source-Tradition Dependency

The owner confirmation records:

- `exact_internal_variant_refs: []`
- parent boundary is current-repo variant-non-dependent
- reviewed-gold claim is current-repo variant-non-dependent
- source-tradition non-dependency is limited to current repo evidence

This does not claim universal textual-critical certainty. It does not select a preferred reading,
prefer a source tradition, change canon scope, or create boundary/source-tradition authority.

## Child Spans

Child spans are not necessary now for parent-only reviewed gold and are not authorized.

This is not a permanent denial of later child-span review. Any later child span requires separate
reviewed evidence, owner authorization, decision-register update, validators/tests, and audit
surface.

## Non-Authorizations

This task does not authorize:

- parent span as a chunk boundary
- child spans
- chunk output changes
- route or evaluator behavior changes
- graph edges, retrieval truth, embeddings, or vectors
- boundary import
- preferred readings or source-tradition preference
- canon-scope change
- source or manuscript row creation
- SQLite database creation
- theology authority or denominational systematic theology
- implementation

## Next Route

The next safe route is Goal 6:

```text
T397 - Route-Isolated Implementation Harness For Eph.1.3-Eph.1.14
```

That next route is harness-only and non-output-changing. Output-changing implementation still
requires a later exact owner authorization after Goal 6 proves non-target identity and same-baseline
constraints.

## Validation

- `python scripts/validate_t394_eph1_parent_only_reviewed_gold_promotion.py`
- `python scripts/validate_t393_eph1_reviewed_gold_promotion_decision_packet.py`
- `python scripts/validate_chunking_gold.py`
- `python scripts/validate_chunking_theological_decision_register.py`
- `python scripts/validate_chunking_lesson_index.py`
- `python scripts/validate_chunking_agent_preflight.py`
- `python scripts/validate_bible_chunking_readiness_map.py`
- `python scripts/validate_task_scope.py --task-id T394`
- `python scripts/agent/validate_handoffs.py`
- `python scripts/validate_all.py`
- `python -m pytest -q`
