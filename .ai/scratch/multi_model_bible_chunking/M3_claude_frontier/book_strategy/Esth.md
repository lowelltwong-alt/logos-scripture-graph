# Esther — M3 frontier chunking strategy

**Strategy id:** `literary_marker_aware_v2` (frontier pass, independent judgment)

## Primary literature type
Narrative (`genre_narrative`): a tightly plotted court drama in ten scenes, ending with the
etiology of Purim. No poetry markers; the divine name is famously absent (evidence, not a
theological conclusion).

## Local marker signals (Rust substrate)
- `p` density marks the banquet/court dialogue turns (ch5, ch6, ch7 p≈8–9). `has_footnote`
  textual notes — evidence only. `has_strong_h` — Strong's **evidence only**.

## Boundary handling (independent rationale)
- The dramatic scenes align with chapters here (Vashti; Esther chosen; Haman's plot; Esther's
  resolve; the banquets; Mordecai honored; Haman exposed; counter-decree; deliverance/Purim;
  epilogue) — documented as scene units, not chapter fallback. The tight reversal-plot makes
  the scene seams and chapter seams coincide.

## Strong's / WJ handling
Strong's Hebrew = evidence only. `wj_or_red_letter` n/a (OT).

## Low-confidence & frontier escalation triggers
- ch9 (the Jews' armed defense and the institution of Purim) flagged as an ethical/etiological
  review point — surfaced for review, not resolved by the boundary.

## Why this is not silent chapter-only
Each unit's evidence ref names its dramatic scene and the reversal-plot beat, documenting why
scene and chapter coincide rather than defaulting silently.
