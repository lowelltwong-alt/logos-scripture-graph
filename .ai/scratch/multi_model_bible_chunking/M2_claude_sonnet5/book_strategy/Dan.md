# Book Strategy — Daniel (M2_claude_sonnet5)

- **strategy_id:** literary_marker_aware_v2 | **book:** Dan | **pilot_book:** true (T423 pilot set) | **frontier_book:** true (fork policy frontier_flag_books)

## Selected strategy
One chunk per chapter, matching Daniel's well-known bipartite structure: court narratives (1-6)
and apocalyptic visions (7-12). Every chunk sets `frontier_flag_considered: true` per the fork
policy's mandatory rule for Dan/Rev, and every chunk is forced to `medium_low` confidence because
Daniel is both pilot-fragile and (per the substrate) poetry/liturgy-marker-rich throughout,
consistent with the chapter-fallback rule.

## Literature type / mixed genre
narrative (court tales, 1-6, 9-10) and prophetic_oracle (apocalyptic visions, 7-8, 11-12).

## Substrate markers considered
All 12 chapters carry the poetry/liturgy marker flag; used directly to justify the confidence
downgrade rather than assumed.

## Strong's metadata — evidence only
Not used to resolve any interpretive question.

## Chapter-only fallback
Used deliberately for all 12 chunks, explicitly justified by the book's own well-established
narrative/vision chapter divisions, not a default.

## Expected low-confidence / doctrinally sensitive regions
All 12 chunks flagged, concentrated most heavily at the four-kingdom vision (2), the four-beasts
and 'son of man' vision (7, among the most historically significant apocalyptic texts in the
corpus), the ram-and-goat vision (8), the seventy-weeks prophecy (9), the detailed kings prophecy
(11), and the end-times/resurrection vision (12) — all carrying long, cross-tradition-disputed
interpretive histories, flagged for downstream awareness, never adjudicated here.

## Frontier / atlas candidate expectations
All 12 chunks require `frontier_flag_considered: true` per fork policy; all 12 also carry sidecar
rows given the pilot-fragile + marker-rich forced downgrade.
