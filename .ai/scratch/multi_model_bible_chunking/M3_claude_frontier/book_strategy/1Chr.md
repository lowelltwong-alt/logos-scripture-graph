# 1 Chronicles — M3 frontier chunking strategy

**Strategy id:** `literary_marker_aware_v2` (frontier pass, independent judgment)

## Primary literature type
Genealogical **lists** (1–9) followed by the David narrative (10–29), with an embedded
psalm of thanksgiving (16:8–36, a composite of Pss 105/96/106).

## Local marker signals (Rust substrate)
- Poetry (`has_poetry_or_liturgy_marker` + q1=27/q2=37/b=3) at **ch16**. Genealogy chapters
  are list-form (low `p`). `has_footnote` textual notes — evidence only. `has_strong_h` —
  Strong's **evidence only**.

## Boundary handling (independent rationale)
- **Genealogies** (1–9) chunked by clan/tribal-block list unit (one per chapter here because
  each chapter is a discrete tribal register).
- **David psalm** (16:7–43) split out as a poetic liturgical unit from the ark procession
  (15:1–16:6).
- David narrative by scene/theme, with list arcs for the cultic organization (23–26) and
  officers (27); the covenant (17) kept whole and flagged for messianic weight.

## Strong's / WJ handling
Strong's Hebrew = evidence only. `wj_or_red_letter` n/a (OT).

## Low-confidence & frontier escalation triggers
- ch16:7–43 (David's psalm) flagged for stanza/parallel-psalm review. The Davidic covenant
  (17) flagged for messianic/theological review — surfaced, not encoded in the boundary.

## Why this is not silent chapter-only
The psalm is isolated and several narrative/list sections are arced; each genealogy unit's
evidence ref names its tribal register rather than defaulting silently to the chapter.
