# Luke — M3 frontier chunking strategy

**Strategy id:** `literary_marker_aware_v2` (frontier pass). **Literature type:** Gospel
(`genre_gospels`) with a formal prologue (1:1–4), an infancy narrative rich in **canticles**
(Magnificat, Benedictus, Gloria, Nunc Dimittis), a large central **travel narrative** (9:51–19:27)
holding many unique parables, and a passion/resurrection with the Emmaus road.

## Local marker signals (Rust substrate)
- `has_poetry_or_liturgy_marker` + q1/q2 in the infancy canticles (ch1–2) and OT citations. `has_wj`
  dense in the travel narrative (ch11 wj=102; ch12 wj=122) — **evidence only**. `has_strong_g` —
  Strong's **Greek evidence only**.

## Boundary handling (independent rationale)
- Chunked by **pericope / canticle / parable-block**. The four canticles are isolated within their
  birth scenes; the travel narrative is chunked by teaching/parable block; the Sermon on the Plain
  (6:17–49) and the Olivet discourse (21:5–38) are units.

## Strong's / WJ handling (evidence only)
WJ/red-letter and Strong's Greek are **evidence only**; discourse seams follow the narrative frame,
not the red letters.

## Low-confidence & frontier escalation triggers
- The **canticles** (Magnificat 1:46–55; Benedictus 1:68–79; Gloria 2:14; Nunc Dimittis 2:29–32)
  flagged as embedded poetry; the **Nazareth sermon** (4:16–30, citing Isa 61) flagged for messianic
  self-application; the parables of grace (15) and the resurrection/ascension (24) flagged. Surfaced,
  not decided.

## Why this is not silent chapter-only
Canticles, parable-blocks, and travel-narrative pericopes drive the boundaries — the canticles are
isolated and many units cross chapters.
