# Lamentations — M3 frontier chunking strategy

**Strategy id:** `literary_marker_aware_v2` (frontier pass, independent judgment)

## Primary literature type
Acrostic **laments** (`genre_psalms`): five poems over fallen Jerusalem. Chapters 1, 2, 4 are
22-line alphabetic acrostics; chapter 3 is a triple acrostic (66 verses, three lines per
letter); chapter 5 is a 22-line prayer that is **not** acrostic.

## Local marker signals (Rust substrate)
- Dense q1/q2 with heavy `b` strophe breaks (b≈21–22 per chapter), matching the acrostic strophe
  structure. `has_footnote` — evidence only. `has_strong_h` — Strong's Hebrew **evidence only**.

## Boundary handling (independent rationale)
- **The acrostic poem is the unit:** each chapter is one complete acrostic lament and is chunked
  whole, because the alphabetic structure defines the poem's extent. Splitting mid-acrostic would
  break the alphabetic frame.
- ch3 (triple acrostic) contains the hope-centre (3:22–24, "great is your faithfulness"); kept
  whole as one poem and flagged.

## Strong's / WJ handling
Strong's Hebrew = evidence only. `wj_or_red_letter` n/a (OT).

## Low-confidence & frontier escalation triggers
- All five poems flagged `medium_low`: each whole-poem/whole-chapter unit is confident, but per
  protocol it coincides with the chapter and its internal acrostic strophes are not sub-chunked —
  surfaced for strophe/acrostic review. ch3's hope-centre is noted for theological review.

## Why this is not silent chapter-only
The acrostic form is the reason each chapter is one unit; this is a documented literary-form
judgment (with strophe-review sidecars), not a lazy chapter default.
