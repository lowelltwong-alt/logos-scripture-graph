---
object_type: roadmap_note
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-18 during T362 as non-output-changing research work after WJ marker inventory, WJ policy, John 3 docket, and epistle issue dossiers."
reason_for_inclusion: "Explain the Gospel/WJ discourse dossier queue and its non-authorizing role before future red-letter, speaker-boundary, discourse, graph, retrieval, evaluator, or chunking work resumes."
---

# T362 Gospel WJ Discourse Dossiers

## Purpose

T362 creates a research-only queue for WJ/red-letter and Gospel discourse review cases:

```text
.ai/control/gospel_wj_discourse_dossier_queue.yaml
```

The goal is to make future red-letter and speaker-boundary work faithful without letting source
metadata decide who is speaking, where a discourse begins or ends, or how chunks should change.
WJ/red-letter markers are preserved as evidence, but they are not speaker attribution, reviewed
gold, graph truth, retrieval truth, or chunk authority.

## Research Cases

The initial queue records:

- `John.3.1-John.3.36`: John 3 WJ speaker/narrator boundary, still owner-selection pending.
- `Matt.5.1-Matt.7.29`: Sermon on the Mount WJ discourse and child-boundary review.
- `John.13-John.17`: Farewell Discourse and prayer complex.
- `Matt.24-Matt.25`, `Mark.13`, `Luke.21`: Synoptic Olivet WJ discourse.
- `John.7.53-John.8.11`: textual-variant-sensitive WJ speech.
- `Rev.1-Rev.3`, `Rev.21-Rev.22`: Revelation WJ voice shifts.
- Acts and epistle WJ/dominical quotation markers outside the four Gospels.

## Source-Metadata Caution

The current WJ inventory records:

- WJ word tokens: 38,094
- WJ token runs: 675
- Books with WJ markers: Matthew, Mark, Luke, John, Acts, 1 Corinthians, 2 Corinthians,
  1 Timothy, and Revelation

Therefore:

- presence of WJ metadata is not Jesus speaker authority
- absence of WJ metadata is not narrator or non-Jesus authority
- WJ evidence outside the four Gospels must be remembered before graph, retrieval, or chunking use

## Non-Authorization

T362 does not authorize:

- Jesus speaker attribution
- speaker boundaries
- discourse boundaries
- reviewed-gold promotion
- chunk boundaries
- output changes
- route behavior
- evaluator changes
- graph edges
- retrieval truth
- source metadata authority
- boundary import
- Gospel/WJ implementation
- T345

Future output-changing use of any dossier still requires exact passage scope, owner review,
reviewed speaker/discourse gold or equivalent governed evidence, non-target identity proof,
validators/tests, and a later implementation-authorizing decision.

## Validation

T362 adds:

- `scripts/validate_gospel_wj_discourse_dossier_queue.py`
- `tests/test_gospel_wj_discourse_dossier_queue.py`

The validator fails closed if the queue authorizes speaker attribution or output changes, loses WJ
inventory counts, drops required dossiers, treats pending packets as approved, or omits
non-authorization guards.
