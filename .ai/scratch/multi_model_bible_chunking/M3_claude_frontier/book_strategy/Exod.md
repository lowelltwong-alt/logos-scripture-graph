# Exodus — M3 frontier chunking strategy

**Strategy id:** `literary_marker_aware_v2` (frontier pass, independent judgment)

## Primary literature type
Mixed: narrative (1–18; 32–34), covenant/theophany (19–24), and legal + ritual/cultic
prescription (20:22–23:33 Book of the Covenant; 25–31 and 35–40 tabernacle). Substrate
`genre_narrative` with `has_poetry_or_liturgy_marker` concentrated at **ch15** (Song of
the Sea, q1=20/q2=28).

## Local marker signals (Rust substrate)
- `p` paragraph density marks legal/ritual sub-units (ch21 p=14, ch22 p=17, ch23 p=15).
- Poetry only at 15 (Song of the Sea / Miriam). Elsewhere prose.
- `has_footnote` frequent (esp. ch30 f=12, ch38 f=22 — textual/measurement notes) —
  evidence only. `has_strong_h` — Strong's Hebrew **evidence only**, not used for boundaries.

## Boundary handling (independent rationale)
- **Narrative:** scene/episode units, several crossing chapter lines (3:1–4:17 call arc;
  13:17–14:31 sea-crossing; 30:1–31:18; 35:1–36:7; 36:8–38:31 construction arc).
- **Plague cycle** (7:14–10:29) grouped into triads by scene rather than one-per-plague
  or one-per-chapter, following the narrative's own paneling.
- **Book of the Covenant** (20:22–23:33) segmented into legal code-units (altar/servant
  law; capital & injury; property/restitution; social-moral-religious; sabbath/festivals;
  angel-conquest) — legal form, not chapter, sets the boundary.
- **Tabernacle** prescriptions (25–31) and their execution (35–40) chunked by furnishing/
  ritual unit. The Decalogue (20:1–21) is kept as its own unit.
- The **Song of the Sea** (15:1–21) is kept intact as a poetic unit and flagged.

## Strong's / WJ handling
Strong's Hebrew = evidence only, not consulted for boundaries. `wj_or_red_letter` n/a (OT).

## Low-confidence & frontier escalation triggers
- The Song of the Sea (poetry) is flagged for stanza review.
- Long ritual/legal chapters carry `medium` confidence where the internal sub-unit seam
  is debatable; those are not sidecar-flagged unless poetic/pilot-fragile (Exodus is not
  a pilot-fragile book), keeping the low-confidence register focused on genuine risk.

## Why this is not silent chapter-only
Units are defined by scene, legal code-unit, and tabernacle furnishing — many span or
split chapters. Evidence refs cite the specific substrate/paragraph seam per unit.
