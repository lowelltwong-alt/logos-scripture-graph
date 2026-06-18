---
object_type: roadmap_note
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-18 during T364 as non-output-changing research work after T363 narrative/legal covenant dossiers."
reason_for_inclusion: "Explain the wisdom/dialogue/poetry dossier queue and its non-authorizing role before future Job, Proverbs, Ecclesiastes, Song, Lamentations, Psalm 119, graph, retrieval, evaluator, or chunking work resumes."
---

# T364 Wisdom Dialogue Poetry Dossiers

## Purpose

T364 creates a research-only queue for wisdom, dialogue, poetry, acrostic, refrain, speaker-boundary,
and lament review cases:

```text
.ai/control/wisdom_dialogue_poetry_dossier_queue.yaml
```

The goal is to preserve poetic, dialogue, acrostic, refrain, speaker, and wisdom-argument evidence
without letting those features decide wisdom theology, Job theodicy, Ecclesiastes framing, Song
allegorical/literal readings, speaker attribution, liturgical use, reviewed gold, or chunk
boundaries.

## Research Cases

The initial queue records:

- `Job.3-Job.42`: dialogue cycles, Elihu speeches, divine speeches, and restoration frame.
- `Prov.1-Prov.9`: wisdom speeches and instruction cycles.
- `Prov.31.10-Prov.31.31`: acrostic wisdom poem.
- `Eccl.1-Eccl.12`: refrain and argument cycles.
- `Song.1-Song.8`: speaker boundaries and genre-sensitive lyric units.
- `Lam.1-Lam.5`: acrostic lament units.
- `Ps.119`: acrostic Torah psalm.

## Non-Authorization

T364 does not authorize:

- wisdom theology system selection
- Job theodicy system selection
- Ecclesiastes pessimistic, optimistic, skeptical, or resolution frame
- Song allegorical, typological, or literal-only reading
- Song speaker assignment
- speaker attribution or speaker boundaries
- acrostic-as-boundary or refrain-as-boundary rules
- poetic parallelism as chunk-boundary authority
- liturgical use authority
- reviewed-gold promotion
- chunk boundaries
- route behavior
- evaluator changes
- graph edges
- retrieval truth
- output changes
- boundary import
- T345

Future output-changing use of any dossier still requires exact passage scope, owner review,
reviewed gold or equivalent governed evidence, non-target identity proof, validators/tests, and a
later implementation-authorizing decision.

## Validation

T364 adds:

- `scripts/validate_wisdom_dialogue_poetry_dossier_queue.py`
- `tests/test_wisdom_dialogue_poetry_dossier_queue.py`

The validator fails closed if the queue authorizes wisdom theology, speaker attribution, speaker
boundaries, output changes, chunk boundaries, route behavior, graph edges, retrieval truth, or
reviewed gold; loses required evidence channels; drops required dossiers; or omits
non-authorization guards.
