# 1 Samuel — M3 frontier chunking strategy

**Strategy id:** `literary_marker_aware_v2` (frontier pass, independent judgment)

## Primary literature type
Narrative (`genre_narrative`): the Samuel–Saul–David transition, with an embedded psalm
(**Hannah's Song**, 2:1–10) and short poetic refrains (the women's "Saul has slain his
thousands", 18:7; 21:11; 29:5).

## Local marker signals (Rust substrate)
- Poetry (`has_poetry_or_liturgy_marker` + q1=14/q2=21/b=4) at **ch2**; minor single-line
  q at 18, 21, 29 (the refrain). High `p` density on long battle/court scenes (14, 17, 28).
- `has_footnote` textual notes — evidence only. `has_strong_h` — Strong's **evidence only**.

## Boundary handling (independent rationale)
- **Hannah's Song** split out (2:1–10) as a poetic unit; the surrounding birth/Eli
  narrative in its own scenes.
- Narrative by scene, with arcs where a single episode spans chapters (5:1–6:21 ark among
  the Philistines; 9:1–10:27 Saul anointed).
- David-and-Saul cycle by episode (Goliath 17; sparing Saul 24 and 26; Nabal/Abigail 25).

## Strong's / WJ handling
Strong's Hebrew = evidence only. `wj_or_red_letter` n/a (OT).

## Low-confidence & frontier escalation triggers
- Hannah's Song (2:1–10) flagged for stanza review.
- ch28 (the medium at Endor / Samuel's apparition) flagged as a theological crux — surfaced
  in the sidecars, not resolved by the boundary. The women's-song refrains are noted here but
  left within their scenes as single lines.

## Why this is not silent chapter-only
Scene and episode form drive boundaries; the psalm is isolated and two episodes are arcs.
Evidence/strategy cite the substrate poetry and paragraph markers.
