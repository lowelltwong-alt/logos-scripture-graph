# Wave 02 checkpoint

- **timestamp:** 2026-07-04T18:52:42.200638+00:00
- **wave id:** 2
- **books completed:** Josh, Judg, Ruth, 1Sam, 2Sam, 1Kgs, 2Kgs

## chunk counts per book
- Josh: 173
- Judg: 273
- Ruth: 42
- 1Sam: 354
- 2Sam: 342
- 1Kgs: 292
- 2Kgs: 298

## validators run
- `validate_whole_bible_chunk_map` per book: **PASS**
- `validate_t423_literary_quality_protocol --require-artifacts` per book: **PASS**

## sidecar row deltas
- low_confidence_register / frontier_escalation_queue / atlas_candidate_feed: **+111** (total 284)

## low-confidence / frontier / theology-pressure highlights
- Marker-rich poetry, law/genealogy spans, oracle/vision units, WJ discourse, and frontier books (Dan, Rev) logged to all three sidecars.

## WJ/red-letter summary (Gospels/Acts)
- N/A this wave (no Gospels/Acts).

## Strong's Greek/Hebrew evidence-only summary
- `strong_or_hebrew_tags_used` set from substrate `strong_ids` and wh/wg counts only; never boundary authority.

## raw-read exceptions
- None. All boundaries from pinned `build/observation_substrate/current/`.

## process issues or repairs
- Restart-from-zero archive before wave 1; independent strategy implementation.

## next wave
- Wave 3: 1Chr, 2Chr, Ezra, Neh, Esth, Job, Ps, Prov, Eccl, Song, Lam

## non-authorizations
- No compare, no canon output, no reviewed gold, no route/evaluator changes, no graph/retrieval/vector truth, no theology authority.
