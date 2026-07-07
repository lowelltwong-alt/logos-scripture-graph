# Matthew — M3 frontier chunking strategy

**Strategy id:** `literary_marker_aware_v2` (frontier pass, independent judgment). **Literature
type:** Gospel (`genre_gospels`): narrative pericopes alternating with **five great discourses**,
each closed by "when Jesus had finished these words" (7:28; 11:1; 13:53; 19:1; 26:1).

## Local marker signals (Rust substrate)
- `has_wj` word-of-Jesus token counts are dense in the discourses (ch5 wj=124; ch13 wj=124;
  ch24 wj=110) — **evidence only**. `has_crossref`/`x` (OT citations) and `has_poetry_or_liturgy_marker`
  (the fulfillment quotations set as poetry). `has_strong_g` — Strong's **Greek evidence only**.

## Boundary handling (independent rationale)
- Chunked by **pericope and discourse unit**. The five discourses are treated as discourse units
  (the Sermon 5–7 split into its rhetorical movements; the others kept whole or lightly split).
  Narrative sections are chunked by scene/pericope, several crossing or splitting chapters.
- **Discourse boundaries follow the narrative frame** ("Jesus said…", the "when he had finished"
  formula), *not* the mere presence of red letters.

## Strong's / WJ handling (evidence only)
- **WJ/red-letter markers are evidence only**, never automatic speaker or theology authority: I do
  not set a boundary because a verse is red-lettered, and I do not infer christology from it.
- **Strong's Greek** is evidence only; never used to set a boundary or decide meaning.

## Low-confidence & frontier escalation triggers
- The discourses (esp. the Sermon 5–7, the Olivet discourse 24–25) flagged for WJ/discourse-boundary
  review. Theologically loaded pericopes — the virgin birth/Immanuel (1:18–25), Peter's confession
  and the keys (16:13–20), church discipline (18:15–20), the eschatological discourse (24–25), the
  crucifixion and cry of dereliction (27:32–66), and the **Great Commission's Trinitarian formula**
  (28:19) — flagged, interpretation surfaced not decided.

## Why this is not silent chapter-only
Boundaries follow pericope/discourse seams; most units split or cross chapters and the discourses
are treated as rhetorical units, with WJ used only as evidence.
