# Acts — M3 frontier chunking strategy

**Strategy id:** `literary_marker_aware_v2` (frontier pass). **Literature type:** historical
narrative (`genre_acts`): the expansion of the church from Jerusalem to Rome, structured by
episodes, **speeches/sermons** (Pentecost 2; Stephen 7; Antioch 13; Areopagus 17; the defenses
22; 24; 26), missionary journeys, and the first-person **"we" sections** (16:10–17; 20:5–21:18;
27:1–28:16).

## Local marker signals (Rust substrate)
- `has_poetry_or_liturgy_marker` on the OT citations within sermons (ch2 Joel; ch7; ch13). `has_wj`
  where the risen/exalted Christ speaks (ch1; 9; 10; 18; 22; 26) — **evidence only**. `has_variant_reading`
  at ch8 (8:37) and ch15 — evidence only. `has_strong_g` — Strong's **Greek evidence only**.

## Boundary handling (independent rationale)
- Chunked by **episode / speech / journey unit**, with arcs (3:1–4:4 healing-and-sermon; 10:1–11:18
  the Cornelius/Gentile-Pentecost cycle). Major speeches are kept whole within their scenes.
- "We"-sections are noted as source-critical **evidence**, not used as boundary authority.

## Strong's / WJ handling (evidence only)
WJ (risen-Christ speech) and Strong's Greek are **evidence only**, never used to set a boundary or
decide theology.

## Low-confidence & frontier escalation triggers
- Pentecost and Peter's sermon (2, incl. 2:38 baptism/repentance), Stephen's speech (7), the
  **Ethiopian eunuch** (8, with the 8:37 textual variant), Saul's conversion (9), the **Cornelius /
  Gentile inclusion** cycle (10–11), the **Jerusalem Council** (15, Gentiles and the law; variant),
  the Areopagus address (17), and Paul's defenses/arrival at Rome (26; 28:26–27 citing Isa 6) are
  flagged — surfaced, interpretation not decided by the boundary.

## Why this is not silent chapter-only
Episode/speech/journey seams drive boundaries, several units cross chapters, and the theological
turning points (Gentile inclusion, the Council) are isolated and escalated.
