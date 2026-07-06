# Book Strategy — Proverbs (M2_claude_sonnet5)

- **strategy_id:** literary_marker_aware_v2 | **book:** Prov | **pilot_book:** false

## Selected strategy
Discourse-unit chunking for ch.1-9 (each an extended wisdom speech, most matching one chapter),
text-marked collection chunking for the remainder (the book itself explicitly labels its
sub-collections at 22:17, 24:23, 25:1, 30:1, 31:1). The large atomized-proverb collections
(10:1-15:33, 16:1-22:16, 25:1-29:27) are kept as single large blocks since individual proverbs are
mostly independent couplets not naturally grouped except by the book's own chapter/collection
markers; a different model might subdivide these by catchword or theme, noted as a plausible
finer split rather than treated as settled.

## Literature type / mixed genre
wisdom_dialogue throughout (discourse, personified-wisdom speech, and atomized proverb
collections).

## Substrate markers considered
All 31 chapters carry the poetry/liturgy marker flag; Proverbs is not a pilot-fragile book, so
the chapter-fallback confidence rule applies only where a chunk is both an exact single-chapter
match AND marker-rich — several of the discourse chapters (1-9) are affected and correctly
carry medium/medium_low confidence.

## Strong's metadata — evidence only
Not used to resolve any interpretive question.

## Chapter-only fallback
Not used as a default; boundaries follow the book's own discourse and collection-marker
structure, which sometimes coincides with chapter lines and sometimes spans or subdivides them
(e.g., ch.6 split into two discourses; 22:17-24:34 spans and subdivides chapter lines to follow
the text's own collection markers).

## Expected low-confidence / doctrinally sensitive regions
Wisdom's pre-creation speech (8:22-31), which has a documented history of Christological reading
in some traditions, flagged for downstream awareness, not asserted.

## Frontier / atlas candidate expectations
One row expected (ch.8).
