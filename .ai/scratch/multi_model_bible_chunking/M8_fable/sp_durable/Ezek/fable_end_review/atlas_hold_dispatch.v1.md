# Fable ruling: Ezekiel atlas-feed holds (8 rows)

Use no tools and read no files; everything you need is below. Reply with the JSON object only.

## The rule
A book's rows in the shared atlas feed must be exactly its low/medium_low chunks, and each must mirror its chunk's span, confidence, review status and hold state (checks/validate_book_review_coverage.py). Ezekiel's v9 corpus marks every row final (candidate_review_complete, hold null). Eight feed rows break the rule: seven are held (final_deferred_review, deferred_human_or_external_ai) while their chunk is final, and one (M8-Ezek-082) is held but graded high, so it is outside the low/medium_low set.

## Context
Every holding reason below was set by the book's final review wave (author/final). The later fix rounds (repair, repair2 v8, v9) changed some rows. By owner ruling OW-28, you will review every low/medium_low row of every book at campaign end; this book's end packet already carries its open questions (docket keys given). Releasing a hold therefore does not drop a question from your end review; it only stops the feed claiming the chunk is unfinished.

## Options
- release: the feed row becomes candidate_review_complete, hold null, accepted_candidate, matching the corpus. No corpus change.
- keep_held: the corpus row changes to final_deferred_review / deferred_human_or_external_ai (as Gen, Deut and Judg did for 4 rows), with its review packet held_lower_confidence. This needs a v10 corpus and two new blind delta re-check lanes before the book can close.
- For M8-Ezek-082 only: drop_from_feed (the feed stays low/medium_low only; its question goes into your end packet; no corpus change) or regrade_medium_low (the corpus grade becomes medium_low with a stated ground, so the row belongs in the feed and in the low-confidence register and frontier queue; v10 plus two lanes).

Scope: rule only on the hold (and on 082's grade, as its options name). Other grades and wording are for your campaign-end review.

## Facts (facts_sha256 a87ca428e7b82c8a4e9f0d898dbc8122f2097db5afa1a6fc2fd62640e7cf389f)
```json
[
 {
  "atlas_id": "M8-Ezek-035",
  "row": "P03-001",
  "span": "Ezek.15.1-Ezek.15.8",
  "grade": "medium_low",
  "corpus_status": [
   "candidate_review_complete",
   null
  ],
  "held_by": "author/final s5 F-414",
  "held_because": "GRADE_QUESTION: the medium_low grade had no stated ground.",
  "now_measured": "grade unchanged: medium_low",
  "docket_v9": {
   "A0": "cured_v9: O-63/X-9 grade without a stated ground (F-414)",
   "B7": "carried_low: CONFCAL"
  },
  "delta_lanes": "Both v9 blind delta lanes list P03-001's grade for the campaign-end Fable review."
 },
 {
  "atlas_id": "M8-Ezek-037",
  "row": "P03-003",
  "span": "Ezek.16.15-Ezek.16.19",
  "grade": "medium_low",
  "corpus_status": [
   "candidate_review_complete",
   null
  ],
  "held_by": "author/final s3 F-199",
  "held_because": "STOP: signal wordevent.strict_onset contradicted the prose; signals were outside that pass's writable scope.",
  "now_measured": "flagged signal absent from the v9 row",
  "docket_v9": {}
 },
 {
  "atlas_id": "M8-Ezek-038",
  "row": "P03-004",
  "span": "Ezek.16.20-Ezek.16.23",
  "grade": "medium_low",
  "corpus_status": [
   "candidate_review_complete",
   null
  ],
  "held_by": "author/final s5 F-200",
  "held_because": "STOP: same defect as F-199 (wordevent.strict_onset; no word-event formula opens 16:20).",
  "now_measured": "flagged signal absent from the v9 row",
  "docket_v9": {}
 },
 {
  "atlas_id": "M8-Ezek-039",
  "row": "P03-005",
  "span": "Ezek.16.24-Ezek.16.34",
  "grade": "medium_low",
  "corpus_status": [
   "candidate_review_complete",
   null
  ],
  "held_by": "author/final s3 F-201",
  "held_because": "STOP: same bar as F-199 (wordevent.strict_onset, oath.as_i_live).",
  "now_measured": "flagged signals absent from the v9 row",
  "docket_v9": {}
 },
 {
  "atlas_id": "M8-Ezek-049",
  "row": "P03-021",
  "span": "Ezek.18.21-Ezek.18.32",
  "grade": "medium_low",
  "corpus_status": [
   "candidate_review_complete",
   null
  ],
  "held_by": "author/final s2 F-279",
  "held_because": "STOP: signal closure.formula_final did not fit the span; signals were outside that pass's writable scope.",
  "now_measured": "flagged signal absent from the v9 row",
  "docket_v9": {}
 },
 {
  "atlas_id": "M8-Ezek-082",
  "row": "P07-003",
  "span": "Ezek.29.17-Ezek.29.21",
  "grade": "high",
  "corpus_status": [
   "candidate_review_complete",
   null
  ],
  "held_by": "author/final s6 F-494",
  "held_because": "STOP: a class question on the classified signal utterance.mid_unit; no edit could discharge it in that pass.",
  "now_measured": "flagged signal still present: utterance.mid_unit",
  "docket_v9": {
   "B19": "carried_low: EMPTY_EVIDENCE"
  }
 },
 {
  "atlas_id": "M8-Ezek-083",
  "row": "P07-004",
  "span": "Ezek.30.1-Ezek.30.12",
  "grade": "medium_low",
  "corpus_status": [
   "candidate_review_complete",
   null
  ],
  "held_by": "author/final s6 F-495",
  "held_because": "STOP: as F-494, on utterance.mid_unit and recognition.mid_unit.",
  "now_measured": "flagged signals still present: utterance.mid_unit, recognition.mid_unit",
  "docket_v9": {
   "B19": "carried_low: EMPTY_EVIDENCE"
  }
 },
 {
  "atlas_id": "M8-Ezek-113",
  "row": "P10-016",
  "span": "Ezek.40.28-Ezek.40.37",
  "grade": "low",
  "corpus_status": [
   "candidate_review_complete",
   null
  ],
  "held_by": "author/final s1 F-337",
  "held_because": "STOP: evidence clause 'the gate circuit is one list the plan never cuts inside' is false; the plan cuts inside chapter 40.",
  "now_measured": "clause still present in the v9 row",
  "docket_v9": {
   "A3": "cured_v9: F-337 partly cured",
   "B3": "carried_low: COUNT_TEXT"
  },
  "delta_lanes": "Both v9 blind delta lanes found the clause still present and still false (lane A R1, lane B N1); both still judged the book fit_to_close."
 }
]
```

## Reply (JSON only; each reason at most two sentences)
```json
{
 "schema": "ezek_atlas_hold_ruling.v1",
 "facts_sha256": "a87ca428e7b82c8a4e9f0d898dbc8122f2097db5afa1a6fc2fd62640e7cf389f",
 "rulings": {
  "M8-Ezek-035": {
   "decision": "release|keep_held",
   "reason": "..."
  },
  "M8-Ezek-037": {
   "decision": "release|keep_held",
   "reason": "..."
  },
  "M8-Ezek-038": {
   "decision": "release|keep_held",
   "reason": "..."
  },
  "M8-Ezek-039": {
   "decision": "release|keep_held",
   "reason": "..."
  },
  "M8-Ezek-049": {
   "decision": "release|keep_held",
   "reason": "..."
  },
  "M8-Ezek-082": {
   "decision": "drop_from_feed|regrade_medium_low",
   "reason": "..."
  },
  "M8-Ezek-083": {
   "decision": "release|keep_held",
   "reason": "..."
  },
  "M8-Ezek-113": {
   "decision": "release|keep_held",
   "reason": "..."
  }
 }
}
```

## Precedent (added at dispatch, outside facts_sha256)
The owner wants any ruling that should apply to later books recorded once, so that it is not asked again. Add one more top-level key to your reply: "precedent". It is a list of at most three objects, {"applies_when": "...", "decision": "...", "rule": "one sentence"}. State each rule generally enough to apply to any book's held atlas rows at close. Return an empty list if your rulings are specific to these Ezekiel rows.
