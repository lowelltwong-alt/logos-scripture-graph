# 2 Chronicles — M3 frontier chunking strategy

**Strategy id:** `literary_marker_aware_v2` (frontier pass, independent judgment)

## Primary literature type
Narrative (`genre_narrative`): Solomon's reign and temple (1–9) then the kings of Judah to
the exile and Cyrus decree (10–36). Substrate shows minor liturgical-refrain poetry (the
"for he is good; his loyal love endures forever" refrain at 5; 7) and `has_variant_reading`
at 20 and 36.

## Local marker signals (Rust substrate)
- Minor q at 5, 7 (refrain). `has_variant_reading` at 20, 36 — a textual-variant evidence
  flag, evidence only. `has_footnote` — evidence only. `has_strong_h` — Strong's evidence only.

## Boundary handling (independent rationale)
- **Solomon block** by scene (temple build arc 3:1–4:22; dedication prayer 6; response 7).
- **Kings of Judah** chunked by **reign**, arcing multi-chapter reigns (Rehoboam 10–12;
  Asa 14–16; Jehoshaphat 17–20; Hezekiah 29–31; Josiah 34–35) rather than one-per-chapter.

## Strong's / WJ handling
Strong's Hebrew = evidence only. Textual-variant flags = evidence only. `wj_or_red_letter` n/a.

## Low-confidence & frontier escalation triggers
- ch20 (Jehoshaphat's holy-war-by-praise, carrying `has_variant_reading`) flagged as a
  textual/interpretive review point. The liturgical refrains are noted here but left inside
  their scenes as single lines.

## Why this is not silent chapter-only
Reign-arcs and temple scenes drive boundaries; evidence/strategy cite the substrate variant
and paragraph markers per unit.
