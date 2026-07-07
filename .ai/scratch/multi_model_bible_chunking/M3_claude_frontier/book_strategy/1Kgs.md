# 1 Kings — M3 frontier chunking strategy

**Strategy id:** `literary_marker_aware_v2` (frontier pass, independent judgment)

## Primary literature type
Narrative (`genre_narrative`): Solomon's reign (1–11), the divided kingdom (12–16), and the
Elijah cycle (17–19; 21–22). No poetry markers in the substrate (embedded prophetic sayings
are prose-set here).

## Local marker signals (Rust substrate)
- High `p` density on court and prophetic scenes (ch2 p=27, ch18 p=28, ch20 p=33, ch22 p=32).
- `has_footnote` textual notes — evidence only. `has_strong_h` — Strong's **evidence only**.

## Boundary handling (independent rationale)
- Boundaries are **regnal/episode units**, not merely chapters: the temple-and-palace
  construction is arced (6:1–7:51); the Solomon dedication (8) is its own unit; the Elijah
  cycle is chunked by scene (drought/Zarephath 17; Carmel 18; Horeb/Elisha 19).
- Regnal-summary chapters (14–16) are kept as king-list/episode units.

## Strong's / WJ handling
Strong's Hebrew = evidence only. `wj_or_red_letter` n/a (OT).

## Low-confidence & frontier escalation triggers
- ch13 (the man of God from Judah and the old prophet) flagged as a narrative/theological
  crux (obedience, deception, the prophetic word) — surfaced for review, not resolved by the
  boundary. No poetry flags (none present).

## Why this is not silent chapter-only
The temple construction is arced and the prophetic cycles are scene-chunked; each unit's
evidence ref names its episode/regnal seam rather than defaulting to the chapter.
