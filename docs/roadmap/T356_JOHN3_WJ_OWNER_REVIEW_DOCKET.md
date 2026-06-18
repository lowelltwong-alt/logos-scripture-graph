---
object_type: roadmap_owner_review_docket
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-18 during T356 after T355 selected John 3 as the first exact WJ speaker/discourse owner-review target."
reason_for_inclusion: "Give the owner a precise John 3 decision surface before any reviewed-gold promotion, chunk implementation, graph edge, retrieval truth, or output change."
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
owner_selection_status: pending
selected_option: pending
implementation_allowed: false
output_change_authorized: false
reviewed_gold_promoted: false
```

T356 does not approve a John 3 parent span, child spans, Jesus speaker attribution, narrator
boundary, reviewed gold, route behavior, graph edges, retrieval truth, or generated chunk output.

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

Only one option may be selected in a later owner-decision task.

| Option id | Selection | Future effect if selected | Implementation now? |
| --- | --- | --- | --- |
| `JOHN3-T356-A` | Preserve current overlapping Gospel chunks. | No reviewed gold is promoted; John 3 remains pending. | No |
| `JOHN3-T356-B` | Approve parent-only `John.3.1-John.3.36` as a review target. | A later task may prepare parent-only reviewed-gold/equivalent governed evidence. | No |
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

If you are ready to approve a first John 3 behavior target, `JOHN3-T356-B` is the lowest-risk
implementation-useful option because it approves only the parent scope and leaves internal
speaker/discourse boundaries unresolved. `JOHN3-T356-C` is more useful for future retrieval, but it
requires an explicit decision about the `John.3.9-John.3.21` disputed zone. If that disputed zone is
not ready, choose `JOHN3-T356-E`.

## Required Updates After Owner Selection

Any later owner selection must update:

- `.ai/control/john3_wj_owner_review_docket.yaml`;
- this docket;
- `.ai/control/chunking_theological_decision_register.yaml`;
- `.ai/control/bible_chunking_readiness_map.yaml`;
- relevant task, handoff, and roadmap state surfaces.

If an option can lead to implementation, a later task must add reviewed-gold/equivalent governed
evidence, executable checks, same-baseline evaluation, non-target identity proof, and a separate
implementation authorization.

## Non-Authorizations

This docket does not authorize:

- John 3 parent span approval;
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
  reviewer: null
  date: null
  owner_selection_status: pending
  selected_option: pending
  selected_parent: null
  selected_children: []
  selected_jesus_speech_span: null
  rationale: null
  implementation_allowed: false
  output_change_authorized: false
  reviewed_gold_promoted: false
  notes: >
    T356 records owner-review options only. No John 3 parent span, child span,
    Jesus speaker attribution, narrator boundary, reviewed gold, route behavior,
    graph edge, retrieval truth, generated chunk, or output change is authorized.
```
