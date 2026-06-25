---
object_type: roadmap_report
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-25 by Codex during T402 after the owner asked whether whole-Bible low-complexity candidates could be reviewed before more chunking."
reason_for_inclusion: "Make the whole-Bible low-complexity runway visible to humans and future AI agents while preserving the non-output-changing, non-authorizing boundary."
---

# T402 Low-Complexity Chunking Runway

## Status

T402 is review/research only and non-output-changing.

It adds a governed all-66-book candidate queue and post-pilot review for the completed
`Eph.1.3-Eph.1.14` output pilot. It does not promote reviewed gold, implement chunks, add child
spans, change route or evaluator behavior, create graph/retrieval/vector truth, import boundary
or source-tradition authority, change canon scope, or authorize theology authority.

## Core Rule

Low-complexity status means review eligibility only. It never means AI may chunk automatically.

## What T402 Adds

- `.ai/control/t402_eph1_post_pilot_review.yaml`
- `.ai/control/whole_bible_low_complexity_chunking_candidate_queue.yaml`
- `scripts/validate_t402_low_complexity_chunking_runway.py`
- `tests/test_t402_low_complexity_chunking_runway.py`
- `.ai/tasks/T402.task.yaml`
- `.ai/audits/reports/20260625-T402-low-complexity-runway.md`
- `.ai/handoffs/T402/handoff.md`

## Eph.1 Post-Pilot Finding

The T401 exact output pilot remains stable for the exact parent-only overlay:
`Eph.1.3-Eph.1.14`.

The post-pilot review records that child spans are not necessary now. That is not permanent
child-span denial and not child-span authority. Any later child span still needs exact reviewed
evidence, owner promotion, register updates, validators, tests, and route-isolated proof.

## Terminology

- `unit`: any text span under chunking review.
- `parent`: the main governed chunk span.
- `child`: a smaller span inside a parent, only when separately reviewed and authorized.
- `overlay`: an additive chunk view that preserves existing baseline records.
- `lane`: a chunking problem family such as epistle argument, narrative, poetry, or apocalyptic.
- `route`: the exact algorithm path authorized for one exact target.
- `depth`: numeric hierarchy level if a later authorized design needs nesting.

Avoid `grandparent` and `great-grandparent` terms for now. If larger structure is needed later,
use `section_overlay`, `book_structure_overlay`, or numeric `depth` with explicit review.

## Candidate Queue

The queue contains one candidate per canonical book. Every candidate records a proposed parent
span, lane, status, why it may or may not be low-complexity, contextual dependencies, source
metadata evidence-only notes, variant/source-tradition flags, theological risk flags, original
language review needs, owner-decision needs, recommended next action, and non-authorizations.

Status buckets:

- `ready_for_review_packet`
- `needs_context_research`
- `needs_original_language_review`
- `variant_sensitive_hold`
- `theological_risk_hold`
- `not_low_complexity`
- `owner_decision_required`
- `do_not_chunk_now`

## Recommended Next Step

Choose one exact `ready_for_review_packet` candidate for lightweight review-packet strengthening.
That future work remains review-only until a separate owner promotion gate.

## Validation

Run:

```bash
python scripts/validate_t402_low_complexity_chunking_runway.py
python -m pytest tests/test_t402_low_complexity_chunking_runway.py -q
python scripts/validate_all.py
python -m pytest -q
```

Before running full pytest, read `.ai/control/test_runtime_preflight.yaml`; full pytest may need a
long timeout or split execution.
