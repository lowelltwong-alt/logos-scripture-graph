# M2 Claude Sonnet 5 — Quality Summary (literary_marker_aware_v2)

**Strategy:** `literary_marker_aware_v2` | **Books:** 66/66 | **Chunks:** 1,135

## Quality-protocol compliance

- `book_strategy/<Book>.md` written for all 66 books before their chunks, each covering: selected
  strategy, literature type/mixed genre, substrate markers considered, Strong's-metadata-as-
  evidence-only statement, chapter-only-fallback rationale where used, expected low-confidence
  regions, and frontier/atlas expectations.
- `low_confidence_register.jsonl`, `frontier_escalation_queue.jsonl`, and
  `atlas_candidate_feed.jsonl` each carry 580 rows, one triple per flagged chunk, satisfying the
  protocol's requirement that any `medium_low`/`low`-confidence chunk (including every chapter-
  fallback-forced one) appear in all three sidecars.
- `scripts/validate_t423_literary_quality_protocol.py --model-folder ... --require-artifacts` run
  after every book and again across the full set: **OK** (one real defect caught and fixed during
  Job in Wave 3 — 12 chunks had been missing the chapter-fallback confidence downgrade; corrected
  and re-validated before proceeding).

## Chapter-only-fallback discipline

The chapter-fallback rule (any chunk whose span exactly matches a full chapter that is
poetry/liturgy-marker-rich, or that belongs to a pilot-fragile book, must be `medium_low`/`low`)
was applied consistently across all 66 books. This affected entire books most heavily where
one-chapter-per-chunk is also the correct literary unit and the book is marker-dense throughout:
Psalms (150/150 chunks forced), Daniel (12/12, also frontier-flagged), Revelation (21/21, also
frontier-flagged), and substantial portions of Job, Isaiah, Hebrews, and the Minor Prophets.

## Independence from existing governed surfaces

Several spans in this map overlap with candidates, review packets, or reviewed-gold decisions
that already exist elsewhere in this repository under separate governed tasks (e.g., Gen.5
matches an existing T402 candidate boundary; Ps.78 and Ps.89 have existing reviewed-gold child-
span decisions; Eph.1.3-14, Rom.9-11, Heb.7-10, and 1Cor.8-10 have existing epistle-argument
review-packet treatment; Phlm, 2John.1.1-3, and Jonah have existing T402/T411/T417 candidate or
disposition records; John.3 has an existing T355/T411 owner-review docket for its speaker-boundary
question). In every such case, this scratch map's chunk was defined independently — same-contract-
different-judgment per the quality protocol's `model_independence` rule — and the per-chunk
rationale explicitly states that no existing governed decision is being referenced, replicated,
or contradicted. This preserves the fork's comparison value: agreement or disagreement with other
models (or with prior governed decisions) on these spans is informative precisely because this
map's answer was not copied from them.

## Honest limitations

- Torah/narrative/epistle chunking used hand-authored literary judgment informed by real substrate
  data, not an exhaustive verse-by-verse close reading of the raw USFM text.
- Psalms (150 psalms) used real per-psalm substrate facts (verse count, superscription presence,
  Selah presence) rather than an individually-verified genre classification for every psalm;
  roughly 30 well-known psalms received specific genre/intertext notes at high confidence, the
  remainder received a generic, honest "one self-contained psalm" note.
- Large atomized-proverb blocks in Proverbs (10:1-15:33, 16:1-22:16, 25:1-29:27) were kept as
  single large chunks rather than further subdivided by catchword/theme; this is explicitly noted
  as a plausible finer split a different model might make.
- Revelation and Daniel chunking is structural-only by design; every rationale disclaims any
  hermeneutical-school, millennial, chronological, or symbolic-identification claim.

## Non-authorizations restated

`non_authorizing: true` on every row; `promotion_authority: none` and
`atlas_promotion_authority: none` throughout. This summary and the underlying chunk map do not
constitute reviewed gold, canon output, or any output-changing authority.
