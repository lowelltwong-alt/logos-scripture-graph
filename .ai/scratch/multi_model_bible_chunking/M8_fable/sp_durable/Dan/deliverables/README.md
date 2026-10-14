# Daniel: atlas candidate rows, dimensions record and low-confidence sidecar

Close-gate item 22 for the book of Daniel (Hebrew and Aramaic). Everything here is a **candidate**: it authorizes
nothing, promotes nothing, and changes no row. Merging into the shared atlas feed is the owner's act.

Every number below is produced by the tools named and is reproduced by re-running them. None was counted by hand.

## Files

| File | What it is |
|---|---|
| `gen_atlas_rows.py` | builds the two atlas files from pinned inputs; `--check` prints `DETERMINISTIC: MATCH` |
| `atlas_candidate_feed_rows.jsonl` | 49 rows in the 16 fields of the shared feed |
| `Dan_atlas_dimensions.v1.jsonl` | 1 header, 75 unit records, 348 open-question records, 260 linkage records |
| `check_atlas_rows.py` | independent checker with tamper self-test; writes `atlas_rows_check.v1.json` |
| `atlas_rows_check.v1.json` | the check record: 23 checks, 14 tampers, the generator's own check |
| `gen_sidecars.py` | builds the sidecar and its derivation record; `--check` prints `MATCH` as its last line |
| `Dan_sidecar_derivation.v1.jsonl` | for each sidecar row, where each field came from and at what tier |
| `../sidecar_src_dan.jsonl` | 49 sidecar rows, keyed by `writer_decision_id` |

Run order: `gen_atlas_rows.py`, then `gen_sidecars.py`, then `check_atlas_rows.py`. Each takes `--dan-root`
(inputs; default the parent of the script's directory) and `--out-root` (outputs; default the same). No tool reads a
clock, draws a random number or scans a directory. Each holds its input digests as constants and refuses if an input
has moved.

## What is measured

- **Selection.** 75 final rows; 49 are graded `medium_low` (47) or `low` (2). Those 49 are the feed rows and the
  sidecar rows. No Daniel row is held: every feed row has `candidate_hold_state` null, the corpus row's own
  `review_status`, and `review_packet_final_state` `accepted_candidate`.
- **Contested between the blind lanes.** For 20 of 75 units the two blind primary lanes gave different verdicts
  (support against challenge). The reconciling reader's own flag (28 of 75) is kept beside it and labelled REPORTED.
  All lanes ran on one model family, so agreement between them is one voice and not corroboration.
- **Severities landed.** Per unit, counts of high, medium and low findings from the blind lanes' challenges, the
  later review rounds and the final audit (book totals: 2 high, 21 medium, 110 low). The reconciling reader restates
  the blind lanes' findings and is not counted again.
- **Device evidence on both faces of the seam.** For each unit's onset and close: whether a section mark follows the
  last verse of the unit before, or a counted device stands at it (left face), and whether a counted device stands at
  the unit's first verse (right face). 43 onsets carry evidence on both faces, 31 do not, 1 is the book's edge.
  Presence is not strength: several counted devices are weak connectives.
- **Answerable from the witnesses.** One of three values. `a_witness_limit_is_stated` (2 units): an open question
  naming the unit says the witnesses cannot settle it. `seam_evidence_present_in_the_witness_layers` (43).
  `left_out` (30): nothing here derives an answer, so the rating is left out rather than guessed.
- **Numbering.** Row spans use the English witness's numbering; the device inventory and the mark layer use the
  Hebrew witness's. Two units hold a verse whose chapter differs between the two (`Dan.4.1-Dan.4.3`,
  `Dan.5.31-Dan.6.3`); 15 units lie where the numberings differ at all. The generator converts by the inventory's
  own numbering sentence; the checker re-derives the same spans by aligning the two witnesses verse by verse.

## What is judged, and kept apart

The `judged` block of each unit record holds a hardness rating assigned by a stated rule over the measured fields
(13 high, 49 medium, 13 low). It is labelled `JUDGED_BY_RULE` and says that no one re-read the passage to produce
it. It does not travel in the feed. **No risk rating is derived**: no packet rates risk for a unit, and the record
says so in `risk_rating_left_out`.

## Open questions and blast radius

348 open-question records: the 46 routed end-review items, 217 entries that the landed review packets list as
unresolved, and 85 that the twelve controlling rulings list as unresolved. For the last two kinds the record says
only that the author raised the entry as unresolved; whether a later round settled it is not derived here.

Each carries a blast-radius class, assigned by rule: `campaign_wide` 60, `one_book` 235, `several_units` 26,
`one_unit` 27. A question with any convention word, or a routed item whose id names no unit, is never filed
narrower than `one_book`. The four routed items filed `one_unit` each carry a unit in their id.

## Linkages and divergent treatment

260 pairs of units are named together by a review item, an open question or a controlling ruling. A linkage asserts
co-mention only, and every source is re-opened by the checker. Harvest is by unit id: a cross-reference written only
as chapter and verse is not harvested.

231 linked pairs differ in recorded confidence or unit type. Each carries a statement, assigned by rule:

- 156 `real_distinction`, the difference stands after a controlling ruling or routed item that names both units;
- 33 `real_distinction`, the two units are of different recorded kinds and are graded alike;
- 36 `real_distinction`, grades differ, no source naming both uses a word of divergence, and the final audit
  confirmed each row (REPORTED);
- **6 `possible_inconsistency_unruled`**: a source naming both uses a word of divergence and no ruling of six units
  or fewer names both. Five lie in `Dan.10.4` to `Dan.11.6`, one at `Dan.12.5-Dan.12.13`. These are candidates for
  the end review, not findings: the rule matches a word, it does not read the passages.

## Prose in the feed and sidecar

`why_low_confidence` is the row's own sentences, transcribed. A sentence is dropped if it carries a Hebrew-block
character, a quotation mark, an internal code or process talk. At most two sentences come from the row's device
notes and one from its recorded alternative. All 49 are unique; none needed a composed fallback.
`why_frontier_review_needed` is the first other usable sentence of the recorded alternative (42 rows) or of the
boundary rationale (7 rows). `possible_downstream_risk` is composed from measured dependency facts.
Sentences are split at full stops and semicolons, so a few begin mid-clause.

## Limits

- The shared feed file was not a pinned input of this build and was not read. Its 16 field names and the reviewer
  and action vocabulary are held as constants taken from the form of the earlier book's tool; the owner should
  compare them with the shared feed before merging.
- Blast-radius classes, statements and hardness are rule output over word matches. A rule can misfile.
- The checker shares no code with the generator, but one builder on one model family wrote both. It is not an
  independent review.
- No witness text is carried in any file here; the two witnesses' licence terms were not examined in this build.
- Nothing from any other book is carried: no finding, sentence, id, count or rating.
