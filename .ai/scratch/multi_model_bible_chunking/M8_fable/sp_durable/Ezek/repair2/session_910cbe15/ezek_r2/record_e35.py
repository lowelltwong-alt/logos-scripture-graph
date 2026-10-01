#!/usr/bin/env python3
"""Record E-35 (the inherited-base arithmetic class) and queue entry E13-94."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

CAMP = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
EZ = CAMP / "sp_durable" / "Ezek"
LJ = CAMP / "error_pattern_ledger.v1.jsonl"
LM = CAMP / "ERROR_PATTERN_LEDGER.v1.md"
Q = EZ / "ezek_controlling_agent_queue_e13.v1.jsonl"
NOW = datetime.now(timezone.utc).isoformat()
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731

row = {
    "id": "E-35",
    "kind": "error_pattern",
    "date": "2026-09-16",
    "headline": "a published count becomes the base for a later record's arithmetic and no layer re-measures "
                "it; the wrong answer can be right one layer down, which is what hides it",
    "severity": "medium",
    "severity_basis": (
        "no corpus damage: the nine ordered grade moves were each anchored per row and applied correctly, and "
        "the corpus count was right the whole time. What was wrong was the check meant to verify it - so the "
        "blast radius is a verification control that would have passed a corpus with five wrong grades in it, "
        "and would have failed the sound corpus it was actually run against."),
    "the_instance": {
        "layer_1": ("#e13's confidence_summary states high_rows_after: 27 while its own moves dict lists nine "
                    "high-downgrades against a measured 32 before - its own list gives 23. The same summary's "
                    "prose says '13 are adopted' where its own fields add 10 + 2 = 12 adopted against 13 "
                    "declined for 25 proposals."),
        "layer_2": ("#e13 then HELD one row (P08-012) by name rather than moving it blind, an audit moved it, "
                    "and the next ruling confirmed it - so the true count became 22."),
        "layer_3": ("#e15 inherited 27 as its base and reasoned '27 - 5 + 1 = 23, from the 27 #e13 left "
                    "(P08-012's move to medium was #e14's, already counted there)'. P08-012 could not have "
                    "been counted in the 27, because #e13 held it rather than moving it."),
        "what_hid_it": ("#e15's answer, 23, is exactly #e13's TRUE after-count. A reader checking 23 against "
                        "#e13 finds agreement. The number is correct as an answer to a question nobody was "
                        "asking, at a layer nobody was checking."),
        "how_it_surfaced": ("the ruling wrote 'verify by count at apply time' and I did. The gate refused: 22 "
                            "measured against 27 stated. That clause is the only reason this is a finding and "
                            "not a shipped grade."),
    },
    "why_the_obvious_cure_fails": (
        "'re-measure the base' is right and insufficient, because an author who states a base has usually just "
        "measured something - #e13 had measured 32 - and the derived figure inherits the feel of a "
        "measurement. The tier is the cure: a count computed this execution is MEASURED; a count read from a "
        "record is REPORTED, however recently it was written and however authoritative its author."),
    "cure": [
        "a count check asserts the DELTA the decision actually ordered, against a base re-measured in the same "
        "execution; a stated base is a cross-check that can disagree, never the operand",
        "when a stated base and a measured base disagree, the gate REFUSES and the run explains the chain end "
        "to end before anything is applied - neither silently adopting the measurement nor silently trusting "
        "the record, because the disagreement is itself the finding",
        "a published derived count carries the list it was derived from, so a later reader can recompute it "
        "instead of inheriting it",
        "a record that HOLDS an item for another authority says so at the point where the count is stated, "
        "because that is where the next reader will do arithmetic with it",
    ],
    "detection": ("recompute every published count from the record's own itemised list at the moment the count "
                  "is used as an operand, and compare three values: the stated count, the count implied by the "
                  "record's own list, and the count measured on the artifact"),
    "generalisation": ("this is the counting form of E-31 (an ordered clause reported as done) and E-32 (an "
                       "artifact built from part of an order): a summary figure standing in for the itemised "
                       "content it summarises. The itemised list is the record; the total is a convenience, "
                       "and a convenience is not evidence."),
    "tier": "MEASURED on the rows at both digests and on the rulings' own lists; the account of what hid it is "
            "INFERRED from the numbers coinciding",
    "provenance": {"book": "Ezek", "found_by": "orchestrator (claude-opus-5) at REPAIR-2 step 1",
                   "found_at": NOW},
}
with LJ.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(row, ensure_ascii=False) + "\n")

md = [
    "",
    "## E-35 - an inherited base: a published count used as an operand without re-measurement",
    "",
    "**The shape.** A record publishes a derived count. A later record uses that count as the base of new",
    "arithmetic. No layer recomputes it. The later record's answer can be *correct as an answer to an earlier",
    "question*, which is what keeps it from being noticed.",
    "",
    "**The instance, measured end to end.**",
    "",
    "| layer | states | its own list gives | truth on disk |",
    "|---|---|---|---|",
    "| #e13 confidence_summary | high_rows_after: 27 | 32 - 9 = **23** | 23 |",
    "| #e13 prose | \"13 are adopted\" | 10 + 2 = **12** (12 + 13 declined = 25, correct) | 12 |",
    "| #e15 Q3 | \"27 - 5 + 1 = 23, from the 27 #e13 left\" | 22 - 5 + 1 = **18** | 18 |",
    "",
    "Between #e13 and #e15 one row (P08-012) was *held* by name - \"no lane proposed on it and I do not move it",
    "blind\" - then moved by an audit and confirmed by the next ruling, taking the true count to 22. #e15's",
    "parenthetical, \"P08-012's move to medium was #e14's, already counted there\", is the load-bearing error: it",
    "could not have been counted in the 27, because #e13 held it rather than moving it.",
    "",
    "**What hid it.** #e15's answer, 23, is exactly #e13's *true* after-count. Anyone checking 23 against #e13",
    "finds agreement. The figure was right at a layer nobody was asking about and wrong at the layer it was used.",
    "",
    "**What surfaced it.** The ruling itself wrote *\"verify by count at apply time\"*, and the verification",
    "refused: 22 measured against 27 stated. Without that clause the nine moves would have applied silently and",
    "the base error would have travelled into the close.",
    "",
    "**Why the obvious cure is not enough.** \"Re-measure the base\" is correct and insufficient. An author who",
    "states a base has usually just measured *something* - #e13 had genuinely measured 32 - so the derived figure",
    "inherits the feel of a measurement. The durable distinction is the tier: a count computed **this execution**",
    "is MEASURED; a count read from a record is REPORTED, however recent its author and however authoritative",
    "the record.",
    "",
    "**Cure.**",
    "",
    "1. A count check asserts the **delta the decision ordered**, against a base re-measured in the same",
    "   execution. A stated base is a cross-check that is allowed to disagree - never the operand.",
    "2. When stated and measured bases disagree, the gate **refuses** and the run explains the chain before",
    "   anything is applied. Neither silently adopting the measurement nor silently trusting the record is",
    "   acceptable: the disagreement is itself the finding.",
    "3. A published derived count travels with the list it was derived from, so the next reader can recompute",
    "   rather than inherit.",
    "4. A record that HOLDS an item for another authority says so **where the count is stated**, because that is",
    "   where the next reader will do arithmetic with it.",
    "",
    "**Generalisation.** This is the counting form of E-31 and E-32: a summary figure standing in for the",
    "itemised content it summarises. The itemised list is the record; the total is a convenience, and a",
    "convenience is not evidence.",
    "",
]
with LM.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(md))

entry = {
    "id": "E13-94", "opened_at": NOW, "severity": "MEDIUM",
    "headline": ("REPAIR-2 STEP 1 APPLIED (9/9 parity, digest exact) AND ITS COUNT CHECK REFUSED FIRST: the "
                 "ruling's base of 27 high rows is 22 on disk. The nine moves are sound - every from-value "
                 "anchors - and the arithmetic above them is not. New ledger class E-35."),
    "raised_by": "orchestrator (claude-opus-5)", "status": "step 1 DONE; the finding is for #e16",
    "blocks_close": False, "tier": "MEASURED",
    "applied": {"sweep": "repair2_step1_confidence", "rows_touched": 9, "e18_parity_digits": "9/9",
                "preimage": "64d9eff05f0e49dc5dfa6aa74ebbbd81809cb8cb2fb8bc24013e03bb3fce0476",
                "postimage": "1238eb2443c2e2b02ffd15ccc26cd8bd6acef0aecd5646e24500ba8417799425",
                "moves": {"P04-008": "medium_low->medium", "P07-008": "medium_low->high",
                          "P09-001": "high->medium", "P03-014": "high->medium_low",
                          "P03-015": "high->medium_low", "P03-016": "medium->medium_low",
                          "P03-017": "high->medium_low", "P03-018": "high->medium_low",
                          "P03-019": "medium->medium_low"}},
    "the_count_chain": {
        "e13_summary_states": "high_rows_after: 27",
        "e13_own_moves_dict_gives": "32 measured before - 9 high-downgrades = 23",
        "e13_prose_states": "'13 are adopted'",
        "e13_own_fields_give": "adopted_as_proposed 10 + adopted_one_step_beyond 2 = 12; +13 declined = 25",
        "then": ("#e13 HELD P08-012 by name ('no lane proposed on it and I do not move it blind - the boss "
                 "audit re-weighs it'); the boss audit moved it high->medium; #e14 Q2 confirmed 'the 12 named "
                 "in #e13 plus P08-012 -> medium remain the mechanical list'. True count 22."),
        "e15_states": ("'27 - 5 + 1 = 23, from the 27 #e13 left (P08-012's move to medium was #e14's, already "
                       "counted there: verify by count at apply time)'"),
        "why_that_parenthetical_cannot_hold": "P08-012 could not be counted in the 27 because #e13 held it",
        "measured_truth": {"high_before": 22, "high_after": 18, "ordered_delta": -4, "delta_reproduced": True},
        "what_hid_it": "#e15's 23 is exactly #e13's TRUE after-count, so checking 23 against #e13 agrees",
        "the_corpus_is_sound": ("the wave applied exactly the authorised 13 moves (#e13's 12 + P08-012); "
                                "32 - 10 = 22 is correct. No row carries an unordered grade."),
    },
    "what_i_did_with_the_failing_check": (
        "I did not adjust the gate to pass. The gate now asserts the DELTA the ruling decided, re-measures the "
        "base in the same execution, and records the stated base as a disagreement with its full explanation. "
        "Asserting 23 would fail a sound corpus; dropping the check would lose the only thing that caught it."),
    "for_e16": ("confirm the corrected figures for the record - 22 high before step 1, 18 after - and whether "
                "#e13's confidence_summary should be re-versioned or annotated, since two rulings now cite a "
                "figure that its own list contradicts"),
    "ledger": {"new_class": "E-35"},
    "step_2_state": ("dispatched to two blind author lanes with the per-row ORDERS as data (the #e15 Q1 cure), "
                     "each carrying the register gate as a self-check; 16 rows, 44 order attachments. The nine "
                     "rows from step 1 carry a grade their prose does not yet state until step 2 lands - "
                     "disclosed in the step-1 receipt as an obligation, and the close gate cannot pass while "
                     "it holds."),
}
entry["ledger"]["jsonl_rows_after"] = len([1 for l in LJ.read_text(encoding="utf-8").splitlines() if l.strip()])
with Q.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(entry, ensure_ascii=False) + "\n")

print(json.dumps({"ledger_jsonl_rows": entry["ledger"]["jsonl_rows_after"],
                  "ledger_md_lines": len(LM.read_text(encoding="utf-8").splitlines()),
                  "queue_rows": len([1 for l in Q.read_text(encoding="utf-8").splitlines() if l.strip()]),
                  "ledger_md_sha256": sha(LM)}, indent=1))
