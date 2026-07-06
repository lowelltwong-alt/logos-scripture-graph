# Romans — M3 frontier chunking strategy

**Strategy id:** `literary_marker_aware_v2` (frontier pass). **Literature type:** epistle
(`genre_epistles`): Paul's most sustained theological **argument**, moving thesis → universal sin →
justification → sanctification → Israel → paraenesis → closing.

## Local marker signals (Rust substrate)
- `has_poetry_or_liturgy_marker` marks OT citations (esp. ch3; 9–11 with `x` up to 24 crossrefs) —
  evidence only. `has_strong_g` — Strong's **Greek evidence only**. `has_crossref`/`x` — evidence only.

## Boundary handling (independent rationale)
- Chunked by **rhetorical/argument unit**: greeting (1:1–7); thanksgiving+thesis (1:8–17); the
  argument in its steps (1:18–3:20 sin; 3:21–31 justification; 4 Abraham; 5 Adam/Christ; 6 baptism;
  7 law; 8 the Spirit; 9–11 Israel by movement); paraenesis (12–13; 14:1–15:13); travel/closing
  (15:14–16:27). Several units are arcs (9:30–10:21; 14:1–15:13).

## Strong's / WJ handling (evidence only)
Strong's Greek and OT-citation markers are **evidence only**; never used to set a boundary or decide
doctrine. `wj_or_red_letter` n/a.

## Low-confidence & frontier escalation triggers (dense theological pressure)
- The **thesis** (1:16–17), **justification/propitiation** (3:21–31, esp. 3:25 hilastērion),
  **Adam/original sin/imputation** (5:12–21), **no condemnation & predestination** (8:1, 28–30),
  **election** (9:6–24), and **"all Israel saved"** (11:25–32) are flagged — surfaced, interpretation
  not decided. The closing **doxology's placement** (16:25–27) is flagged as a textual issue.

## Why this is not silent chapter-only
Boundaries follow Paul's argument steps, several crossing chapters; the epistolary frame (greeting,
thanksgiving, paraenesis, closing) and the doctrinal cruxes are explicitly isolated.
