---
object_type: roadmap_note
trust_zone: canonical
lifecycle_status: active
provenance_note: "Created 2026-06-18 during T366 as non-output-changing research work after T365 prophetic/oracle/vision dossiers."
reason_for_inclusion: "Explain the textual-variant/source-tradition dossier queue and its non-authorizing role before future Mark 16, John 7:53-8:11, omitted-verse, source-tradition, boundary-routing, graph, retrieval, evaluator, or chunking work resumes."
---

# T366 Textual Variant Source Tradition Dossiers

## Purpose

T366 creates a research-only queue for textual-variant, source-tradition, omitted-verse,
canon-scope, boundary-routing, and noncanonical-reference review cases:

```text
.ai/control/textual_variant_source_tradition_dossier_queue.yaml
```

The goal is to preserve variant markers, footnotes, empty witnesses, source-tradition differences,
boundary-material routing questions, doctrinal sensitivity, and source metadata without letting
those features decide textual-critical policy, canon scope, source-tradition preference,
noncanonical authority, reviewed gold, graph edges, retrieval truth, or chunk boundaries.

## Research Cases

The initial queue records:

- `Mark.16.1-Mark.16.20` and `Mark.16.9-Mark.16.20`: Mark longer-ending textual-variant boundary.
- `John.7.53-John.8.11`: pericope adulterae textual-variant boundary.
- `Acts.8.37`, `Acts.15.34`, and `Acts.24.7`: empty witnesses and omitted-verse records.
- `Rom.16.25-Rom.16.27`: Romans doxology placement or omission evidence.
- `Deut.32.8-Deut.32.9`: sons of God / Israel source-tradition issue.
- `Jer.1-Jer.52`: Jeremiah MT/LXX order and length source-tradition issue.
- `Jude.5-Jude.15`: noncanonical reference and source-sensitive examples.
- `Dan` and `Esth`: additions as boundary-material routing cases.
- `1John.5.6-1John.5.8`: Comma Johanneum doctrinally sensitive variant.

## Non-Authorization

T366 does not authorize:

- textual-critical preferred reading selection
- canon-scope expansion or contraction
- source-tradition preference
- boundary import
- noncanonical source authority
- longer-ending inclusion or exclusion policy
- pericope adulterae inclusion, exclusion, or placement policy
- Comma Johanneum proof-text policy
- Deuteronomy 32 divine-council or angelology policy
- Jeremiah MT/LXX order or length preference
- Romans doxology placement policy
- Jude boundary-source authority
- Daniel or Esther additions import
- variant markers, footnotes, WJ/red-letter markers, or empty witnesses as chunk-boundary authority
- source metadata, cross-references, or lexical markers as graph or retrieval truth
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
reviewed gold or equivalent governed evidence, textual policy if needed, non-target identity proof,
validators/tests, and a later implementation-authorizing decision.

## Unintended Consequence Review

Confirmed risks:

- None of the T366 surfaces change raw data, canonical data, generated chunks, evaluator scoring,
  route behavior, reviewed gold, graph edges, retrieval output, or vector/index output.

Plausible risks:

- The phrase "longer ending" could be read as an inclusion or exclusion decision.
- John 7:53-8:11 could be treated as a WJ/red-letter or Gospel narrative decision before variant
  policy is reviewed.
- Omitted or empty witnesses could accidentally become chunk splits or retrieval gaps.
- Jude noncanonical references could become boundary import or graph-edge authority.
- Deuteronomy 32 and 1 John 5:7 could be overread as doctrinal proof-text decisions.

Mitigation:

- The queue and CD-032 deny textual-critical, canon-scope, source-tradition, boundary-import,
  noncanonical-source, doctrine, graph, retrieval, reviewed-gold, route, evaluator, output, and
  chunk-boundary authority.
- Future implementation still requires exact owner-reviewed gold or equivalent governed evidence.

Owner decisions needed:

- None for this non-output-changing research queue.
- A later owner decision is required before any textual-variant/source-tradition output-changing
  work, canon-scope change, source-tradition preference, boundary import, or reviewed-gold
  promotion.

## Validation

T366 adds:

- `scripts/validate_textual_variant_source_tradition_dossier_queue.py`
- `tests/test_textual_variant_source_tradition_dossier_queue.py`

The validator fails closed if the queue authorizes textual-critical decisions, canon-scope changes,
source-tradition preference, noncanonical source authority, output changes, chunk boundaries, route
behavior, graph edges, retrieval truth, reviewed gold, boundary import, or algorithm work; loses
required evidence channels; drops required dossiers; or omits non-authorization guards.
