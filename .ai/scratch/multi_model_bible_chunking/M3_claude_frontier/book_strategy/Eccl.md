# Ecclesiastes — M3 frontier chunking strategy

**Strategy id:** `literary_marker_aware_v2` (frontier pass, independent judgment)

## Primary literature type
Wisdom reflection (`genre_wisdom`): Qoheleth's first-person meditation, mixing prose reasoning
with poetic set-pieces (the "a time for everything" poem 3:1–8; the aging poem 11:7–12:8), an
editorial prologue (1:1–11) and epilogue (12:9–14). The "vanity/vapor" (hevel) refrain recurs.

## Local marker signals (Rust substrate)
- Poetry (`has_poetry_or_liturgy_marker` + q1/q2) at 3 and 9–12; prose (`p`) elsewhere.
  `has_footnote` — evidence only. `has_strong_h` — Strong's Hebrew **evidence only**.

## Boundary handling (independent rationale)
- Chunked by **argument/reflection unit**, several as arcs (1:12–2:26 the quest; 3:16–4:16;
  5:8–6:12; 9:13–10:20; 11:7–12:8 the aging poem). The prologue and epilogue are isolated.
- The two poems (3:1–15 with the times-poem; 11:7–12:8) are kept intact.

## Strong's / WJ handling
Strong's Hebrew = evidence only. `wj_or_red_letter` n/a (OT).

## Low-confidence & frontier escalation triggers
- The times-poem (3:1–15) and the aging poem (11:7–12:8) flagged for poetic-unit review. The
  hevel/"vanity" refrain and the book's theological tension (its qualified this-worldly wisdom)
  are noted as evidence, surfaced in the sidecars, not encoded in the boundary.

## Why this is not silent chapter-only
Reflection-arcs and isolated poems drive boundaries; the prologue/epilogue are separated.
Evidence/strategy cite the substrate poetry and paragraph markers.
