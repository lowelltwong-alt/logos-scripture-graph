# Jeremiah — M3 frontier chunking strategy

**Strategy id:** `literary_marker_aware_v2` (frontier pass, independent judgment)

## Primary literature type
Prophetic oracle + biographical narrative (`genre_prophets`), mixing poetry (2–6; 8–20; 30–31;
46–51) and prose (7; 26–29; 34–45; 52). Includes Jeremiah's personal **confessions/laments**
(e.g. 11–12; 15; 17; 18; 20), the **Book of Consolation** (30–33) with the **new covenant**
(31:31–34), oracles against the nations (46–51), and a historical appendix (52).

## Local marker signals (Rust substrate)
- `has_poetry_or_liturgy_marker` + q1/q2 dense in the poetic oracles; prose narrative in the
  Baruch/last-days material. `has_footnote` — evidence only. `has_strong_h` — Strong's evidence only.
  (The book's MT/LXX order-and-length differences are a known textual issue — evidence only.)

## Boundary handling (independent rationale)
- Chunked by **oracle / sermon / narrative unit**, with arcs where a movement spans chapters
  (2:1–3:5; 4:5–6:30 foe from the north; 7:1–8:3 temple sermon; 11:1–12:17; 19:1–20:18;
  30:1–31:40 consolation; 50:1–51:64 Babylon). The confessions are kept within their oracle units.

## Strong's / WJ handling
Strong's Hebrew = evidence only. `wj_or_red_letter` n/a (OT). MT/LXX differences = evidence only.

## Low-confidence & frontier escalation triggers
- The **righteous Branch** oracles (23:5–6; 33:14–16) flagged for messianic pressure; the **new
  covenant** (31:31–34) flagged for its heavy NT/theological use (Heb 8); the harshest **lament**
  (20:14–18) flagged. All surfaced in sidecars, not encoded in the boundary.

## Why this is not silent chapter-only
Boundaries follow oracle/sermon/narrative seams with many multi-chapter arcs; the confessions
and the Book of Consolation are treated as literary movements, not chapters.
