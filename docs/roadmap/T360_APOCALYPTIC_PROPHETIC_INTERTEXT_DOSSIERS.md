---
object_type: roadmap_note
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-18 during T360 as non-output-changing research work after the Bible-wide registry and source-metadata atlas merged."
reason_for_inclusion: "Explain the apocalyptic/prophetic intertext dossier queue and its non-authorizing role before future Revelation, Daniel, prophetic, graph, retrieval, or chunking work resumes."
---

# T360 Apocalyptic Prophetic Intertext Dossiers

## Purpose

T360 creates a research-only queue for intertext-sensitive apocalyptic and prophetic passages:

```text
.ai/control/apocalyptic_prophetic_intertext_dossier_queue.yaml
```

The goal is to prepare future Revelation, Daniel, prophetic, Gospel discourse, graph, retrieval,
and chunking review work without forcing a contested hermeneutic position. Revelation and related
passages can be read through several orthodox frameworks, including futurist, preterist,
historicist, idealist, premillennial, amillennial, postmillennial, typological, and
already/not-yet lenses. This queue preserves those possibilities instead of selecting one.

## Research Cases

The initial queue records these dossier candidates:

- Revelation and Daniel Son of Man imagery: `Rev.1.13`, `Rev.14.14`, `Dan.7.13-Dan.7.14`.
- Revelation and Psalm 2 rod-of-iron imagery: `Rev.2.27`, `Rev.19.15`, `Ps.2.9`.
- Revelation kingdom-priest language with Exodus/Isaiah background: `Rev.1.6`, `Exod.19.6`, `Isa.61.6`.
- Olivet discourse and Daniel abomination references: `Matt.24.15-Matt.24.31`, `Mark.13.14-Mark.13.27`, `Luke.21.20-Luke.21.28`, `Dan.9.27`, `Dan.11.31`, `Dan.12.11`.
- Cosmic signs and Day-of-the-Lord imagery: `Matt.24.29`, `Mark.13.24-Mark.13.25`, `Luke.21.25-Luke.21.26`, `Isa.13.10`, `Isa.34.4`, `Joel.2.30-Joel.2.31`, `Rev.6.12-Rev.6.17`.
- Ezekiel temple/city imagery and Revelation new creation: `Ezek.40-Ezek.48`, `Rev.21-Rev.22`.
- Zechariah pierced-one and mourning imagery: `Zech.12.10`, `John.19.37`, `Rev.1.7`.

These are not reviewed gold, not graph edges, not retrieval truth, and not implementation targets.

## Source-Metadata Caution

The canonical `eng-web` editorial cross-reference sidecar is useful but sparse for this lane:

- total editorial cross-reference records: 340
- Revelation-origin editorial cross-reference records: 5
- Daniel-origin editorial cross-reference records: 0
- Ezekiel-origin editorial cross-reference records: 0
- Zechariah-origin editorial cross-reference records: 0
- Isaiah-origin editorial cross-reference records: 0

Therefore:

- absence of a source cross-reference is not absence of a canonical intertext
- presence of a source cross-reference is not intertext authority
- source metadata remains evidence only

## Non-Authorization

T360 does not authorize:

- Revelation implementation
- Daniel/Revelation chronology
- hermeneutic system selection
- graph edges
- retrieval truth
- reviewed-gold promotion
- chunk boundaries
- output changes
- boundary import
- T345

Future output-changing use of any dossier still requires exact passage scope, owner review,
reviewed gold or equivalent governed evidence, non-target identity proof, validators/tests, and a
later implementation-authorizing decision.

## Validation

T360 adds:

- `scripts/validate_apocalyptic_prophetic_intertext_dossier_queue.py`
- `tests/test_apocalyptic_prophetic_intertext_dossier_queue.py`

The validator fails closed if the queue becomes authorizing, loses required hermeneutic options,
misstates observed cross-reference counts, drops required dossiers, or omits non-authorization
guards.
