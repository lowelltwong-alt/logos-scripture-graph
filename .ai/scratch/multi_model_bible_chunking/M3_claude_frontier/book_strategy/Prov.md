# Proverbs — M3 frontier chunking strategy

**Strategy id:** `literary_marker_aware_v2` (frontier pass, independent judgment)

## Primary literature type
Wisdom **poetry** (`genre_wisdom`): extended instruction poems and Lady-Wisdom speeches (1–9),
then editorial sentence-collections marked by their own superscriptions (Solomon 10:1–22:16;
sayings of the wise 22:17–24:34; Hezekiah's Solomon collection 25–29; Agur 30; Lemuel 31:1–9;
the acrostic woman of valor 31:10–31).

## Local marker signals (Rust substrate)
- q1/q2 poetry on every chapter; `b` strophe breaks heavier in 22–24 and 30. `has_footnote` —
  evidence only. `has_strong_h` — Strong's Hebrew **evidence only**.

## Boundary handling (independent rationale)
- **Chapters 1–9** chunked by **instruction poem / Wisdom speech** (motto 1:1–7; the ten
  instructions and interludes; Lady Wisdom 8; the two banquets 9).
- **Sentence collections (10–29)** chunked by the editorial **collection headings**, and within
  the long Solomonic collections by **chapter as a proverb-cluster**. This is a logged, flagged
  decision: individual proverbs are atomic couplets with no verse-level literary seam finer than
  the chapter, so each cluster is marked `medium_low` and surfaced for thematic-clustering review
  rather than asserted as a confident boundary.
- ch22 split at 22:16/22:17 (collection seam); the "sayings of the wise" (22:17–24:22; 24:23–34)
  as their own units; Agur (30), Lemuel (31:1–9), and the acrostic (31:10–31) isolated.

## Strong's / WJ handling
Strong's Hebrew = evidence only. `wj_or_red_letter` n/a (OT).

## Low-confidence & frontier escalation triggers
- All proverb-cluster chapters flagged (`proverb_cluster_thematic_review`).
- ch8 (Lady Wisdom, 8:22–31 "the LORD possessed/created me") flagged for **Christological
  pressure** — the Arian/Nicene debate point — surfaced, not decided by the boundary.
- 31:10–31 flagged for its acrostic structure.

## Why this is not silent chapter-only
Chapters 1–9 are poem-chunked and the collections follow the book's own editorial headings;
where chapter=cluster in the sentence collections, it is explicitly flagged and explained.
