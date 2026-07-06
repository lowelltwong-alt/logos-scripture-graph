# Book Strategy — Revelation (M2_claude_sonnet5)

- **strategy_id:** literary_marker_aware_v2 | **book:** Rev | **pilot_book:** true (T423 pilot set) | **frontier_book:** true (fork policy frontier_flag_books)

## Selected strategy
Structural chunking using only the text's own explicit, self-declared divisions: the seven
letters (2-3), the seven seals (6, plus the seventh in 8:1), the seven trumpets (8-9, plus the
seventh in 11:15-19), the seven bowls (16), and the text's own explicitly marked interludes (7,
10, 15). Every chunk is set to `medium_low` confidence (Revelation is both pilot-fragile and a
frontier book) and every chunk sets `frontier_flag_considered: true` per the fork policy's
mandatory rule.

## Critical governance note

This repository has an existing, separately-governed research/prep-only decision for Revelation
(REV-T344-E, recorded in `.ai/control/chunking_theological_decision_register.yaml` and related
control surfaces), which holds that Revelation implementation must wait until reviewed gold
exists and a later owner decision authorizes it. This scratch map does not implement Revelation
in any authoritative sense: it is a non-authorizing observation of structural/textual features
only, produced independently for T423 comparison purposes. Every chunk's rationale explicitly
disclaims any hermeneutical-school adoption (preterist/historicist/futurist/idealist), millennial
position, chronological/recapitulation theory, or symbolic identification (e.g., the identity of
the beasts, Babylon, or the 144,000 is never asserted).

## Literature type / mixed genre
narrative (apocalyptic vision sequence), with hymnic/poetic insets at ch.5, 7, and 15
(substrate-confirmed).

## Substrate markers considered
WJ/red-letter marker presence checked per chunk (ch.1-3, 16, 21-22); per CD-021/CD-022, cited as
evidence only — no chunk in this book treats WJ presence as resolving Revelation voice/speaker
identity, chronology, or any other authoritative claim. Poetry markers verified at ch.5, 7, 15.

## Strong's metadata — evidence only
Not used to resolve any interpretive question.

## Chapter-only fallback
Not used as a primary rationale anywhere; every boundary is justified by the text's own explicit
septet/interlude structure, even where it happens to coincide with a chapter line.

## Expected low-confidence / doctrinally sensitive regions
All 21 chunks are flagged, consistent with Revelation's status as both a pilot book and the fork
policy's other mandatory frontier book alongside Daniel.

## Frontier / atlas candidate expectations
All 21 chunks require `frontier_flag_considered: true` and appear in every sidecar file.
