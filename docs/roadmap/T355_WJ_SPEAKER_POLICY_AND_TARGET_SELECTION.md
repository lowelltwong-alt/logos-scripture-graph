---
object_type: roadmap_task_report
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-18 during T355 after T354 proved the current canonical source preserves WJ/red-letter evidence and the maintainer asked whether red-letter passages can be chunked faithfully."
reason_for_inclusion: "Record the non-output-changing WJ speaker/discourse policy and the first exact owner-review target before any Gospel speaker-boundary or discourse chunking work."
---

# T355 WJ Speaker/Discourse Policy And Target Selection

## Purpose

T355 turns the red-letter / words-of-Jesus lesson into a first-class policy surface:

```text
.ai/control/wj_speaker_discourse_policy.yaml
```

The policy says WJ/red-letter markers, punctuation, paragraphing, sectioning, and narrative frame
evidence may be preserved and surfaced for review, but cannot by themselves decide speaker
attribution, speaker boundaries, discourse boundaries, graph edges, chunk boundaries, retrieval
truth, reviewed gold, or output changes.

## Selected First Review Target

T355 selects the existing pending John 3 review case as the next exact owner-review target:

```text
John.3.1-John.3.36
john3_wj_speaker_boundary
eval/chunking_gold/review_packets/john3_wj_speaker_boundary_review.md
```

This selection is review-only. It does not decide whether `John.3.10-John.3.21` is Jesus speech,
narrator/commentary, or unresolved for chunking. It also does not approve parent spans, child spans,
reviewed gold, graph edges, retrieval truth, route behavior, or generated chunk output.

## Candidate Queue

After John 3, the policy keeps these WJ/speaker/discourse cases visible without authorizing
implementation:

- `Matt.5.1-Matt.7.29` / Sermon on the Mount;
- `John.13-John.17` / Farewell Discourse and prayer complex;
- `Matt.24-Matt.25` / Olivet Discourse;
- `John.7.53-John.8.11` / WJ inside a major textual-variant case;
- Revelation WJ voice-shift cases under continuing Revelation research/prep only.

## Validation

Validated by:

```text
python scripts/validate_wj_speaker_discourse_policy.py
python scripts/validate_chunking_agent_preflight.py
python scripts/validate_bible_chunking_readiness_map.py
python scripts/validate_chunking_theological_decision_register.py
```

The validator fails if the policy becomes authorizing, loses the John 3 selected target, drops the
candidate queue, or is no longer mandatory preflight/readiness/register context.

## No Output Change

T355 does not modify raw data, canonical data, generated chunks, evaluators, route behavior, graph
edges, embeddings, retrieval indexes, review packets, or reviewed gold.
