# Song of Songs — M3 frontier chunking strategy

**Strategy id:** `literary_marker_aware_v2` (frontier pass, independent judgment)

## Primary literature type
Love **poetry** (`genre_psalms`) built from dialogue between the bride, the beloved, and the
daughters of Jerusalem. The substrate carries `has_speaker_label` (`sp` markers) throughout —
**speaker attribution is the central structural and interpretive difficulty** of the book.

## Local marker signals (Rust substrate)
- `sp` speaker-label markers on every chapter (ch1 sp=10, ch8 sp=6). Dense q1/q2 poetry, `b`
  strophe breaks. `has_footnote` — evidence only. `has_strong_h` — Strong's Hebrew **evidence only**.

## Boundary handling (independent rationale)
- Chunked by **poetic unit / speaker exchange**, following speaker shifts and scene changes
  rather than chapters; most units cross chapter lines (1:9–2:7; 4:16–5:1; 5:2–6:3; 7:10–8:4).
- Speaker labels (`sp`) are treated as **editorial evidence** for the exchange structure, not as
  authoritative attribution; where speaker assignment is disputed the unit is flagged.

## Strong's / WJ handling
Strong's Hebrew = evidence only. Speaker labels = editorial evidence, not authority.

## Low-confidence & frontier escalation triggers
- Most units are flagged `medium_low` for **speaker-boundary review**, since the identity and
  extent of each speaker's part is genuinely contested. The literal/allegorical reading question
  is noted as evidence and surfaced in the sidecars, never used to move a boundary.

## Why this is not silent chapter-only
Boundaries follow speaker/scene shifts and cross chapters; each unit's evidence ref names its
exchange and the speaker seam it depends on.
