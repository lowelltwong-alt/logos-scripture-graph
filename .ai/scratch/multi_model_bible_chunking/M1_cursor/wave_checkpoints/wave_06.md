# Wave 06 checkpoint

- **timestamp:** 2026-07-04T18:01:05.661250+00:00
- **wave id:** 6
- **books completed:** Matt, Mark, Luke, John, Acts

## chunk counts per book
- Matt: 526
- Mark: 378
- Luke: 566
- John: 458
- Acts: 330

## validators run
- `validate_whole_bible_chunk_map` per book: **PASS**
- `validate_t423_literary_quality_protocol --require-artifacts` per book: **PASS**

## sidecar row deltas
- low_confidence_register / frontier_escalation_queue / atlas_candidate_feed: **+1033** (total 2069)

## low-confidence / frontier / theology-pressure highlights
- Marker-rich poetry, law/genealogy spans, oracle/vision units, WJ discourse, and frontier books (Dan, Rev) logged to all three sidecars.

## WJ/red-letter summary (Gospels/Acts)
- Books with WJ/red-letter consideration: Matt, Mark, Luke, John, Acts. `wj_or_red_letter_considered` set per-chunk when `wj` markers present.

## Strong's Greek/Hebrew evidence-only summary
- `strong_or_hebrew_tags_used` set from substrate `strong_ids` and wh/wg counts only; never boundary authority.

## raw-read exceptions
- None. All boundaries from pinned `build/observation_substrate/current/`.

## process issues or repairs
- Restart-from-zero archive before wave 1; book-family strategy templates in literary_marathon_chunker.py.

## next wave
- Wave 7: Rom, 1Cor, 2Cor, Gal, Eph, Phil, Col, 1Thess, 2Thess, 1Tim, 2Tim, Titus, Phlm, Heb, Jas, 1Pet, 2Pet, 1John, 2John, 3John, Jude, Rev

## non-authorizations
- No compare, no canon output, no reviewed gold, no route/evaluator changes, no graph/retrieval/vector truth, no theology authority.
