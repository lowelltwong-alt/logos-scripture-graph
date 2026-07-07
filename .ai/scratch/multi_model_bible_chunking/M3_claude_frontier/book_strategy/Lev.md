# Leviticus — M3 frontier chunking strategy

**Strategy id:** `literary_marker_aware_v2` (frontier pass, independent judgment)

## Primary literature type
Legal/ritual prescription (`genre_law`). Almost entirely priestly instruction with a
short narrative frame (8–10, ordination and Nadab/Abihu). Minimal poetry (only a short
divine saying at 10:3, q1/q2=1).

## Local marker signals (Rust substrate)
- High `p` density on the Holiness Code (ch18 p=21, ch19 p=33, ch20 p=18) marks
  apodictic law sub-units. `has_footnote` on measurement/textual notes — evidence only.
- `has_strong_h` — Strong's Hebrew **evidence only**, not used to set boundaries.

## Boundary handling (independent rationale)
- **Sacrificial law** (1–7) chunked by offering type, with the layperson block (1–5)
  and the priestly "law of the offering" block (6:8–7:38) as arcs.
- **Ordination narrative** (8–10) by scene; ch10 split at 10:11/10:12 so the divine
  saying and the eating-of-offerings ruling are cleanly separated.
- **Purity laws** (11–15) by topic (foods, childbirth, skin disease, house, discharges).
- **Day of Atonement** (16) kept whole and flagged for typological (Hebrews) review.
- **Holiness Code** (17–26) by legal topic; 27 (vows/tithes) as an appendix unit.

## Strong's / WJ handling
Strong's Hebrew = evidence only. `wj_or_red_letter` n/a (OT).

## Low-confidence & frontier escalation triggers
- Day of Atonement (16) and the sexual-ethics units (18; 20) are flagged `medium_low`
  because they carry heavy downstream theological/typological and contemporary-ethics
  review load, even though the boundary itself is clear. Theology is surfaced to
  sidecars, never used to move the boundary.

## Why this is not silent chapter-only
Offering-type, purity-topic, and legal-topic units drive the boundaries; several are
arcs (4:1–5:13; 6:8–7:38; 21:1–22:33) and one chapter is split (10).
