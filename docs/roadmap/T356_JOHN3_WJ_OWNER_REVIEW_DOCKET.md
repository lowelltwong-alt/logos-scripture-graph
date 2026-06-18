---
object_type: roadmap_owner_review_docket
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-18 during T356 after T355 selected John 3 as the first exact WJ speaker/discourse owner-review target; updated during T367 after the owner selected JOHN3-T356-B."
reason_for_inclusion: "Give the owner a precise John 3 decision surface and record the parent-only review target selection before any reviewed-gold promotion, chunk implementation, graph edge, retrieval truth, or output change."
---

# T356 John 3 WJ Owner Review Docket

## Status

T356 creates a non-output-changing owner-review docket for:

```text
John.3.1-John.3.36
john3_wj_speaker_boundary
```

Machine-readable docket:

```text
.ai/control/john3_wj_owner_review_docket.yaml
```

Existing review packet:

```text
eval/chunking_gold/review_packets/john3_wj_speaker_boundary_review.md
```

Owner selection status:

```yaml
owner_selection_status: selected
selected_option: JOHN3-T356-B
selected_parent: John.3.1-John.3.36
selected_children: []
implementation_allowed: false
output_change_authorized: false
reviewed_gold_promoted: false
```

T367 records the owner selection of `JOHN3-T356-B`: `John.3.1-John.3.36` is approved as a
parent-only review target. This does not approve the parent span as reviewed gold or a chunk
boundary, child spans, Jesus speaker attribution, narrator boundary, route behavior, graph edges,
retrieval truth, or generated chunk output.

## Faithful Selection Rule

The owner decision must preserve John 3 speaker/discourse transparency without turning red-letter
formatting into authority.

Do not let the selected option decide automatically:

- whether `John.3.10-John.3.21` is Jesus speech, narrator/commentary, or unresolved for chunking;
- whether WJ/red-letter starts and stops are speaker boundaries;
- whether punctuation or paragraphing settles discourse boundaries;
- whether a chapter boundary is a discourse boundary;
- whether John 3 child spans become a global Gospel discourse rule.

## Owner Selection Options

Only one option may be selected.

| Option id | Selection | Future effect if selected | Implementation now? |
| --- | --- | --- | --- |
| `JOHN3-T356-A` | Preserve current overlapping Gospel chunks. | No reviewed gold is promoted; John 3 remains pending. | No |
| `JOHN3-T356-B` | Approve parent-only `John.3.1-John.3.36` as a review target. | Selected in T367; a later task may prepare parent-only reviewed-gold/equivalent governed evidence. | No |
| `JOHN3-T356-C` | Approve parent plus exact child-boundary review target. | A later task may prepare exact parent/child reviewed-gold/equivalent evidence after the disputed zone is explicitly handled. | No |
| `JOHN3-T356-D` | Approve one narrower Jesus-speech span only. | A later task must record the exact selected Jesus-speech span and keep other John 3 material unresolved. | No |
| `JOHN3-T356-E` | Require more research before John 3 gold or implementation. | John 3 remains research/prep only. | No |

## Candidate Child Spans For Option C

These spans are candidates only. They are not approved unless the owner later selects
`JOHN3-T356-C` and explicitly handles the disputed speaker/discourse zone.

| Candidate span | Review label | Guardrail |
| --- | --- | --- |
| `John.3.1-John.3.2` | Narrative setup and Nicodemus arrival | Narrative label does not authorize a theological or discourse boundary by itself. |
| `John.3.3-John.3.8` | Initial Jesus/Nicodemus exchange with WJ evidence | WJ evidence remains diagnostic and not speaker authority. |
| `John.3.9-John.3.21` | Disputed speaker/discourse zone | Owner must explicitly decide Jesus speech, narrator/commentary, or unresolved-for-chunking status. |
| `John.3.22-John.3.36` | John's witness after the Nicodemus scene | Following witness material must not be merged or split by WJ metadata alone. |

## Recommendation

Most faithful next action: owner review, not implementation.

The owner selected `JOHN3-T356-B` in T367. This is the lowest-risk implementation-useful review
target because it preserves the parent scope while leaving internal speaker/discourse boundaries
unresolved. `JOHN3-T356-C` would be more useful for future retrieval, but it would require an
explicit decision about the `John.3.9-John.3.21` disputed zone.

## Required Updates After Owner Selection

T367 updated:

- `.ai/control/john3_wj_owner_review_docket.yaml`;
- this docket;
- `.ai/control/chunking_theological_decision_register.yaml`;
- `.ai/control/bible_chunking_readiness_map.yaml`;
- relevant task, handoff, and roadmap state surfaces.

If this option later leads to implementation, a later task must add reviewed-gold/equivalent governed
evidence, executable checks, same-baseline evaluation, non-target identity proof, and a separate
implementation authorization.

## Non-Authorizations

This docket does not authorize:

- John 3 parent span as reviewed gold or chunk boundary;
- John 3 child span approval;
- Jesus speaker attribution;
- narrator boundary decisions;
- WJ/red-letter marker authority;
- reviewed-gold promotion;
- graph edges;
- retrieval truth;
- generated chunk regeneration;
- route behavior;
- output changes;
- raw or canonical data mutation.

## Owner Decision Box

```yaml
john3_owner_review:
  reviewer: Lowell Wong
  date: "2026-06-18"
  owner_selection_status: selected
  selected_option: JOHN3-T356-B
  selected_parent: John.3.1-John.3.36
  selected_children: []
  selected_jesus_speech_span: null
  rationale: >
    Owner selected the parent-only review target while refusing to decide child spans,
    Jesus/narrator boundaries, reviewed-gold status, route behavior, graph/retrieval truth,
    or output changes.
  implementation_allowed: false
  output_change_authorized: false
  reviewed_gold_promoted: false
  notes: >
    T367 records JOHN3-T356-B as a parent-only review target. No John 3 child span,
    Jesus speaker attribution, narrator boundary, reviewed gold, route behavior,
    graph edge, retrieval truth, generated chunk, or output change is authorized.
```
