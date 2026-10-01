# Ezekiel — atlas candidate rows (close-gate item 22)

**What this is.** Ezekiel's contribution to the cross-book blast-radius atlas: 102 candidate rows in the shared
feed's own schema, plus a sidecar that keeps the atlas's three dimensions separated. Built 2026-09-21 by
`gen_atlas_rows.py` from records already pinned in this book's close.

**What this is not.** It is not a promotion, an authorization, or a merge. Nothing here has been added to
`M8_fable/atlas_candidate_feed.jsonl`. **Merging these rows into the shared feed is the owner's act**, as is
accepting or rejecting the seven concern-type names that are new to that feed. Every row carries
`non_authorizing` and `atlas_promotion_authority` saying so in the data itself, so the statement survives
separation from this README.

## AMENDED 2026-09-23 - v10 hold round, OW-30 (read this first; it supersedes the counts below)

The final corpus is now `Ezek/rows_v10_final.jsonl`. The v9 final review wave held eight rows; Fable's one
authorized ruling on them (`Ezek/fable_end_review/atlas_hold_ruling.v1.json`, owner ruling OW-30) resolved
them under its standing three-rule precedent, recorded in the ledger:

- **release** (P1 or P2): `M8-Ezek-035`, `-037`, `-038`, `-039`, `-049`, `-083`. Their feed rows now read
  `accepted_candidate` / `candidate_review_complete` with no hold. No corpus row changed for them.
- **drop_from_feed** (P2): `M8-Ezek-082` (writer row P07-003, Ezek.29.17-Ezek.29.21) is graded `high`, above
  medium_low, so it leaves the feed. Its class question goes to Ezekiel's Fable end packet.
- **keep_held** (P3): `M8-Ezek-113` (writer row P10-016, Ezek.40.28-Ezek.40.37). The corpus row is re-versioned
  to `final_deferred_review` / `deferred_human_or_external_ai` / `specialist_or_external_review`
  (manifest `Ezek/rows_v10_final.manifest.json`), and its feed row mirrors it as `held_lower_confidence`.

**The selection rule changed with it.** The feed now follows the corpus: a row is in the feed only if it is
graded `low` or `medium_low`, and it is held exactly when its corpus row carries `candidate_hold_state`.
A referral by the final review wave (STOP or GRADE_QUESTION) no longer adds or holds a row; it only raises
the row's score. The checker gained `feed_mirrors_the_corpus_hold` and the tamper `tamper_packet_state`, and
passes 16 of 16. The feed has 101 rows (11 low, 90 medium_low), 1 held. Where the sections below say 102 rows,
8 held rows or a referral-based selection, they describe the earlier builds and are kept as history.
These are the current bytes:

| File | Bytes | sha256 |
|---|---|---|
| `atlas_candidate_feed_rows.jsonl` | 129,383 | `15bcea3730bfc39a1214a5dbaf293342e0175c5f43b8a6e553b8de908bb32081` |
| `Ezek_atlas_dimensions.v1.jsonl` | 222,884 | `2060bd5a965a5a602079ad80ad5ff29e8261eb82023fc88160fb245a2669b7fc` |
| `gen_atlas_rows.py` | 16,652 | `b8fa0ea08b8c939fb3630bccd608ba7ad07dd9274015f44d67e4fb927917965e` |
| `check_atlas_rows.py` | 17,642 | `2ed2e31786a8a019ca9d26f86bad84751d9d7960aba82600321d9dd9837522c3` |
| `atlas_rows_check.v1.json` | 3,255 | `59b38fb385a013b2307e85c5c4e82fb5da4aa07f87886d09335f4db0d68059e6` |
| `gen_sidecars.py` | 7,945 | `21ca02dd72fe3f27d4024d58c01a0f1c9a6494e65ea3db648de7f98fbe959923` |
| `Ezek/sidecar_src_ezek.jsonl` | 127,327 | `3ad194a1077fb0a20c473666011148b1c02db21b5a889ef5a7b5b2571c900e2c` |
| `Ezek/rows_v10_final.jsonl` | 656,378 | `106f355324fb867055e4f1ec25cc30ced8607b69a7ce0489b9d953e30e18608b` |
| `Ezek/rows_v10_final.manifest.json` | 2,145 | `f8bd078b70cee18a9e54e02d1d3a5a7ba6b8aab3d1b0c48aa2e91d0f536be040` |
| `Ezek/fable_end_review/atlas_hold_ruling.v1.json` | 4,039 | `24f6f8b0f4b2c4527db95505c9cf44d7a547c68b725675d32aa437d8bc130e5c` |

The earlier files are kept beside these as `<name>.pre_<sha12>`. Re-pointing tool:
`repair2/fixround_v10/repoint_generators_v10.py`; corpus builder `repair2/fixround_v10/build_rows_v10.py`.

## AMENDED 2026-09-23 - v9 fix round (read this before the tables below)

The generator and checker now read the final corpus, `Ezek/rows_v9_final.jsonl`, not the preimage
`Ezek/repair/rows_v7_cwo24.jsonl`. Both merged-close lanes found (low) that the rows asserted
`candidate_review_complete` while being built from an image in which every row was still `pending`.
Regenerating over v9 changed ONE row: `M8-Ezek-079` (writer row P06-015), field `observed_substrate_signals`,
which now copies the corrected signals of the corpus row (lane B's SIGNAL_OUT_OF_SPAN, cured by measurement in
`repair2/fixround_v9/signals_v9.report.json`). The other 101 rows are unchanged. The sidecar source regenerated
byte-identical. The tables below are the 2026-09-21 build and are kept as history; these are the current bytes:

| File | Bytes | sha256 |
|---|---|---|
| `atlas_candidate_feed_rows.jsonl` | 131,218 | `6adc037d01ce02d4991162959e1b364bfe771915760a7875e6eae0d2de4d0f38` |
| `Ezek_atlas_dimensions.v1.jsonl` | 225,713 | `54c766dbff939f921dca0fe1b3d7a4006ff7014a8524487c1521cfee0e34632d` |
| `gen_atlas_rows.py` | 15,855 | `9e91588fbd740a2ec3703d84b020905334195de1b987c14246196ff0270b19e6` |
| `check_atlas_rows.py` | 15,816 | `069f0e6a026228f287f6fded84446634eba085c47395174573d61bcb4c54b5ea` |
| `atlas_rows_check.v1.json` | 2,965 | `78545043f69dc015086d98062b40f1e654d8729f2e984256fb5d35afa592b178` |
| `Ezek/rows_v9_final.jsonl` | 656,268 | `a80b6e6712aa43bf3d8652255b4655a934af08a9cd3e036f9b320a37bbd1098c` |

The earlier files are kept beside these as `<name>.pre_<sha12>`. Re-pointing tool:
`repair2/fixround_v9/repoint_generators_v9.py`.

## Files

| File | Bytes | sha256 |
|---|---|---|
| `atlas_candidate_feed_rows.jsonl` | 131,302 | `b9de6b3c7905c790f950e7574a6f256a2c8377fb2816625683fc9d84ab348739` |
| `Ezek_atlas_dimensions.v1.jsonl` | 225,797 | `417fb54332990a913011bf03d507cfd0221d1e927e62c0daf10d095a566768c2` |
| `gen_atlas_rows.py` (retained generator) | 15,792 | `ce34aaa4ae791a31d7c87f1db7c2866bf25f87184deb34475bf75ec4a945107e` |
| `check_atlas_rows.py` (checker + negative control) | 15,768 | `2347dd8b8e94624e43e9a9e0881182ce978741e0c311b9b62d9728ac410160d3` |
| `atlas_rows_check.v1.json` | 2,965 | `d84658968d232d5a284aac7c1b152a530208b5da70f3a02dbeea748cfaaa3506` |

The generator is **retained**, not extended in place. Item 20 lost the v1 scholar-record generator's bytes by
extending it; the cure is written into the method record (v6 §10, obligation 13) and is followed here.

## Inputs, as pinned

| Input | sha256 | Bytes |
|---|---|---|
| `Ezek/repair/rows_v7_cwo24.jsonl` (138 shipped units) | `e24048cc869f1493ac5d65a7e37fd6457909d2848da31583e9d55211601611a7` | 653,487 |
| `Ezek/author/final/s1_adjudication/adjudication.json` | `1f068df5f395117f84ddd232fa3be8291182a2ae67075678f375d3a5c4a102f8` | 137,354 |
| `…/s2_adjudication/adjudication.json` | `7cb64b936381444465a34947526f2805c15eb911e2ca1a3e5045bbd7c29c8cad` | 64,317 |
| `…/s3_adjudication/adjudication.json` | `356b816dfa665a43811bbf7fbb76d426bea9219cae8314e1d49f3d2719b93e5a` | 80,563 |
| `…/s4_adjudication/adjudication.json` | `b20fc08b3f9b4bfa65690b47e507a5c39540d7a635b64b1885b4c0f3c7641196` | 82,984 |
| `…/s5_adjudication/adjudication.json` | `ecf425272a058b694a940f38850d4e4a94e743d6e4e2b51b3354100fe966a0aa` | 60,844 |
| `…/s6_adjudication/adjudication.json` | `7012a9eb9051fb4c6192a51b93925b5452f66a4ccb5471b40b4590f951a34fd7` | 58,793 |
| `M8_fable/atlas_candidate_feed.jsonl` (target schema and vocabulary, 384 rows) | `4f8c74c7dd5c333701d3bb5ff2c99d6544249ddaaf2b0f1a8bf66df9b641e610` | 470,280 |

The shared feed is read **only** to take its schema and its controlled vocabularies. It is not modified.

## Selection rule, stated as a set

A shipped unit appears here if **either**

1. its recorded confidence is `low` or `medium_low`; **or**
2. the second independent reading refused to act on it (`STOP`) or questioned its recorded grade
   (`GRADE_QUESTION`) — **whatever grade it carries**.

102 of 138 units qualify. The checker verifies this as set equality, not as a count.

Clause 2 was not in the first draft, and measurement is what added it: the first run captured 7 of the 8 referred
rows. The eighth, `Ezek.29.17-Ezek.29.21`, is recorded `high` and was still refused by the second reading. A
confidence-only rule would have dropped exactly the row a reader had objected to. That row is why the feed now
contains one grade the shared feed has never carried; the checker requires any such grade to belong to a referred
row, so the loosening cannot spread.

## How the prose fields were made

`why_low_confidence` is **derived from each row's own record** — its `device_notes` and
`strongest_rejected_alternative` — not re-written from the document and not composed freshly. The sidecar's
`derivation` block names the fields each row drew on and counts what was carried and what was not, so the
derivation can be walked back per row. The checker enforces it: every fragment of `why_low_confidence` must occur
**verbatim** in that row's own two fields, or the check fails.

`possible_downstream_risk` is different and is labelled as such: it is **composed from measured structure**, not
from the row's prose — one clause per dependency class the row actually has (numbering zone, shared seam,
convention reach, shared frame, referral). The sentence that reaches the feed is repeated in the sidecar as
`dependency.composed_sentence_in_feed`, beside the measurements it was built from.

A sentence cannot travel if it contains Hebrew codepoints, a double quotation mark, or an internal campaign token
(warrant tags, tier numbers, packet or slice item ids, ruling codes, filenames). Separately, each field is capped
— 2 sentences from `device_notes`, 1 from `strongest_rejected_alternative`. **Measured across the 102 rows: 299
sentences carried, 70 genuinely unquotable (across 50 rows), 469 usable but past the cap, and 0 rows needing a
composed fallback.** The two counts are kept apart because collapsing them would suggest the whole remainder was
unquotable, when in fact most of it is simply not carried here. **These fields are a capped summary of each row's
reason, not the reason in full** — the full reason is in the row and in the scholar record.

**Consequence, deliberate: this deliverable quotes no witness.** No OSHB text and no WEB text is transcribed
here, in any field, so no attribution or licence obligation travels with these two files. The obligation still
attaches to the underlying rows and to the scholar record, which do quote and do carry their attribution. Do not
back-fill quotations into these rows without carrying the attribution with them.

## The sidecar, and why it exists separately

`Ezek_atlas_dimensions.v1.jsonl` is keyed 1:1 to the feed rows by `chunk_decision_id` and splits each row into
the three blocks that the method record (§15) forbids merging, plus the derivation record:

- **`measured`** — facts read off the records: `confidence_recorded`, `unit_type`, `parent_collection`, `signals`,
  `in_numbering_divergence_zone`, `own_notes_state_no_onset_formula`, `own_notes_disclose_mark_absence`, and a
  `second_reading` sub-block (addressed in the final wave, items closed `NO_DEFECT`, whether the reader refused to
  act, whether the recorded grade was questioned).
- **`dependency`** — structural reach: `classes`, `neighbour_spans` in the shipped ordering,
  `units_sharing_this_frame`, and the `composed_sentence_in_feed` built from them. Blast radius, which is **not**
  difficulty.
- **`judged`** — `atlas_hardness` with its `score`, explicitly labelled `tier: JUDGED_BY_RULE`, with
  `not_a_measurement` and the full `rule` printed in every row.
- **`derivation`** — which of the row's own fields `why_low_confidence` drew on, how many sentences were carried,
  how many were unquotable, how many fell past the cap, and whether the composed fallback was used.

It is a sidecar rather than four more columns because widening a shared registry's schema is not this
generation's authority. If the owner wants these dimensions in the feed itself, that is a schema change to
propose, not a change to make while shipping a book.

**The judged rule, in full:** +2 recorded `low`, +1 recorded `medium_low`, +2 in the dual-numbering zone, +2
refused or grade-questioned by the second reading, +1 no onset formula found, +1 at least one review item closed
`NO_DEFECT`; `high` at ≥4, `medium` at ≥2, else `low`. Measured distribution: high 6, medium 48, low 48. This is
a rule applied to measurements, not itself a measurement, and it has never been checked against any external
difficulty judgement.

## Distribution, measured

- Concern types: `formula_absent_onset` 25, `frame_edge` 23, `scope_hinge` 22, `mark_layer_absence` 15,
  `reading_rests_on_prose` 13, `numbering_zone_seam` 2, `compression_zone` 2.
- Held for referral: 8 rows, each carrying `candidate_hold_state`, `chunk_review_status =
  final_deferred_review`, and `suggested_reviewer = deferred_human_or_external_ai`. These are the second
  reading's own refusals and grade questions; they are handed on, not resolved here.

## Verification

```bash
cd sp_durable/Ezek/deliverables && python check_atlas_rows.py && python check_atlas_rows.py --selftest
```

Run 2026-09-21: **15 of 15 checks PASS**, VERDICT PASS (`atlas_rows_check.v1.json`), and the rebuild is
byte-identical (`gen_atlas_rows.py --check` → DETERMINISTIC: MATCH). Two further results are reported as
disclosures rather than as pass/fail, because a new book legitimately brings them: the seven new concern-type
names, and the shared feed's own two row shapes.

**Negative control — the gate can fail.** The selftest tampers with a copy seven ways and requires the right
check to catch each: prose rewritten instead of derived, planted Hebrew, a planted packet id, a span that is not
a shipped row, a held row silently un-held, one row dropped, and a judged rating merged into a feed row. All
seven CAUGHT. Method record v6 obligation 12 requires this; a gate never shown failing is not evidence.

The checker imports nothing from the generator. Re-using the generator's helpers would prove only
self-consistency, so the dependency facts and the selection rule are re-measured independently inside the
checker.

## Not verified / limits

- **Seven concern-type names are new** to the shared feed's vocabulary. The checker reports them as a disclosure
  rather than a failure, because a new book legitimately brings new classes — but they are unreviewed, and
  accepting the vocabulary is the owner's decision at merge.
- **The shared feed is itself heterogeneous** (measured: 253 rows with 16 fields, 131 with 12). These rows use
  the 16-field union. Whether the 12-field rows should be back-filled is not addressed here.
- **Judged hardness is unvalidated** against anything outside this campaign, and against no other book's rows.
- **No cross-book comparison** is attempted: Ezekiel's ratings are not calibrated against the 384 existing rows,
  so `high` here does not claim to mean `high` there.
- The 8 held rows remain open; nothing here closes them.
