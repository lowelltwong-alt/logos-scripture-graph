# Book Strategy — Leviticus (M2_claude_sonnet5)

- **strategy_id:** literary_marker_aware_v2 | **book:** Lev | **pilot_book:** false

## Selected strategy
Per-topic legal-unit chunking. Leviticus substrate: 27 chapters, 859 verses, genre_law, only ch.10 poetry-marked. Each offering type and legal topic in Leviticus is a self-contained "torah" (instruction) unit, so many chunks legitimately coincide with a single chapter — this reflects the text's own structure (one law-topic per chapter), not a silent chapter-only default. A few naturally continuous blocks (ch.6-7 priestly manual; ch.13-14 skin-disease law; ch.21-22 priestly standards) are grouped as single chunks since splitting them at chapter lines would sever one legal argument.

## Literature type / mixed genre
Almost entirely law_code, with narrative interludes at the ordination (ch.8-9), Nadab/Abihu's death (ch.10, substrate-confirmed poetic fragment at 10:3), and the blasphemer case (24:10-23).

## Substrate markers considered
Marker-rich flag (`has_poetry_or_liturgy_marker`) present only at ch.10 (Moses' brief poetic utterance after Nadab/Abihu's death); this is the only Leviticus chunk carrying the low-confidence poetic-inset flag by that signal. Footnotes present throughout but not used as boundary authority.

## Strong's metadata — evidence only
Leviticus carries substantial Hebrew Strong's tags for offering/purity terminology; not cited as lexical-truth or doctrinal authority in any chunk.

## Chapter-only fallback
Used deliberately and transparently for most offering-law and purity-law chapters, since each chapter is a genuinely self-contained legal topic in this book's own literary structure. Flagged medium_low/sensitive wherever the content (not the boundary) carries significant covenant-theology, atonement-theology, or contemporary ethical weight (ch.10, 11, 16, 18, 20, 26), per the book_specific_hints Torah risk list (ritual_procedure, covenant_context).

## Expected low-confidence / doctrinally sensitive regions
Nadab/Abihu (10), clean/unclean animals (11, matches existing T402-LC-003 candidate), Day of Atonement (16), sexual purity laws (18, 20), and covenant blessings/curses (26).

## Frontier / atlas candidate expectations
Roughly 7 rows expected.
