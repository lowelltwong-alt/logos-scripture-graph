# Job — M3 frontier chunking strategy

**Strategy id:** `literary_marker_aware_v2` (frontier pass, independent judgment)

## Primary literature type
Wisdom **dialogue in poetry** (`genre_wisdom`) inside a prose frame (1–2; 42:7–17). Chapters
3–42 are almost entirely poetic (q1/q2 nearly every verse, with `b` strophe breaks). The
governing structure is the **speech**: each named speaker's discourse is one unit.

## Local marker signals (Rust substrate)
- `has_poetry_or_liturgy_marker` + dense q1/q2 and `b` (strophe/blank) markers on ch3–42;
  prose frame (1–2; 42:7–17) has `p` not `q`.
- `has_footnote` textual notes — evidence only. `has_strong_h` — Strong's **evidence only**;
  rare-word lexis in Job is notoriously hard, so Strong's is explicitly not used for boundaries.

## Boundary handling (independent rationale)
- **Speaker-shift = boundary.** The three dialogue cycles are chunked by speech (Eliphaz,
  Bildad, Zophar, and Job's replies), several as multi-chapter arcs where one speech spans
  chapters (4–5; 6–7; 9–10; 12–14; 16–17; 23–24; 26–27; 29–31; 32–33; 36–37).
- **Set pieces isolated:** Job's opening lament (3), the hymn to wisdom (28), Job's final
  oath of innocence (29–31), the LORD's two whirlwind speeches (38:1–40:2; 40:6–41:34), and
  Job's two responses (40:3–5; 42:1–6).
- Speaker labels ("Then X answered") are discourse-marker **evidence**, not theology authority.

## Strong's / WJ handling
Strong's Hebrew = evidence only. `wj_or_red_letter` n/a (OT).

## Low-confidence & frontier escalation triggers
- Single-chapter marker-rich speeches are marked `medium_low` and surfaced to the sidecars for
  strophe review. ch19 (the "I know that my Redeemer lives" crux, 19:25) carries messianic
  pressure; the divine speeches (38–41, incl. Behemoth/Leviathan) carry interpretive/creational
  weight — surfaced, not encoded in the boundary.

## Why this is not silent chapter-only
Boundaries follow the dialogue's speaker shifts, with many multi-chapter speech arcs and
isolated poetic set-pieces — the opposite of a one-chunk-per-chapter map.
