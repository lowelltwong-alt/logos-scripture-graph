#!/usr/bin/env python3
"""REPAIR-2 step 1: the nine grade moves #e15 ordered, applied mechanically.

THE RULING'S OWN SEQUENCING: "each move is applied mechanically FIRST (as #e13's order of execution has it) and
its ground is written into the row's prose in the same batch, so no row again carries a grade its own text does
not state."

WHY I APPLY THE GRADES AND AN AUTHOR WRITES THE GROUNDS. The grade is a value from a four-item scale that the
ruling states per row - mechanical, and mine to apply. The GROUND is prose, in a register that now has three new
checker arms, and prose is where I have failed twice in this book: my substitution broke nine sentences and my
"register GREEN" reported the checker's patterns as the rule. So the ground prose goes into step 2's author
batch, which the sequence puts immediately next, with the ruling's own measured findings as its source.

The interval matters and is disclosed: between this step and step 2 the nine rows carry a grade their text does
not yet state. That is a state inside REPAIR-2, never a shipped one, and the close gate cannot pass while it
holds - which is why step 2 follows immediately and why this script records the obligation in its receipt.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ezek_aw"))
import guarded_apply as GA                                                     # noqa: E402

EZ = GA.EZ
PRE = "64d9eff05f0e49dc5dfa6aa74ebbbd81809cb8cb2fb8bc24013e03bb3fce0476"

# from #e15 q3.confidence_moves_by_this_ruling, verbatim
MOVES = {
    "P04-008": ("medium_low", "medium"),
    "P07-008": ("medium_low", "high"),
    "P09-001": ("high", "medium"),
    "P03-014": ("high", "medium_low"),
    "P03-015": ("high", "medium_low"),
    "P03-016": ("medium", "medium_low"),
    "P03-017": ("high", "medium_low"),
    "P03-018": ("high", "medium_low"),
    "P03-019": ("medium", "medium_low"),
}
GROUND_OWED = {
    "P04-008": "the ruled value was one step low under the unified rival predicate; the wave applied #e13's "
               "value correctly and the repair itself stands",
    "P07-008": "both seams two-faced and top grade (32:16 verse-final utterance + PE / 32:17 dateline and "
               "hayah-form word-event; 32:32 verse-final utterance + PE / 33:1 strict word-event); no licensed "
               "or two-faced rival; the genre hold is excluded from the grade by the scale itself, and the "
               "16-verse length is the unit the division names",
    "P09-001": "the 37:10/37:11 rival is LICENSED - a vision-internal default onset with a mark behind it - and "
               "live, 37:1-10 being a complete scene and 37:11-14 its interpretation; a licensed rival bars the "
               "top grade",
    "P03-014": "every interior seam of the ch-18 unit is a discourse turn without a formula device on either "
               "face, marked only by samekh; the one formula-marked interior seam is paragraph-final because no "
               "fresh onset follows",
    "P03-015": "same class: the ch-18 tiling cuts one word-event unit at case turns that carry no formula "
               "device on either face",
    "P03-016": "same class; a shared seam weighs the same from both rows",
    "P03-017": "same class; the division names the ch-18 question and the 18:21-32 turn",
    "P03-018": "same class",
    "P03-019": "same class",
}

rows = {r["decision_id"]: r for r in GA.load_rows()}
edits, problems = [], []
for rid, (want_before, want_after) in MOVES.items():
    cur = rows.get(rid, {}).get("confidence")
    if cur is None:
        problems.append((rid, "no such row"))
        continue
    if cur != want_before:
        problems.append((rid, "current grade is %r, the ruling's from-value is %r" % (cur, want_before)))
        continue
    edits.append({"row_id": rid, "field": "confidence", "op": "set_confidence",
                  "expected_before": cur, "value": want_after, "sweep": "confidence",
                  "ground_owed_in_step_2": GROUND_OWED[rid]})

print(json.dumps({"moves_ordered": len(MOVES), "anchored": len(edits),
                  "refused": problems}, indent=1))
if problems:
    raise SystemExit("REFUSED: a from-value does not match the live grade; nothing applied. The ruling's "
                     "from-values are checked against the corpus, not assumed.")

# THE COUNT CHECK THE RULING ASKS FOR AT APPLY TIME - and it FAILS ON ITS BASE, which is the finding.
# The ruling writes: high_rows_after = "27 - 5 (P09-001, P03-014, P03-015, P03-017, P03-018) + 1 (P07-008)
# = 23, from the 27 #e13 left (P08-012's move to medium was #e14's, already counted there: verify by count at
# apply time)". Measured on disk the base is 22, not 27, so the true after-count is 18.
#
# THE CHAIN, measured end to end, because a base that is off by five is either a corpus defect or a ruling
# defect and only measurement says which:
#   pre-wave (25cdba56) carried 32 high. #e13's confidence_rulings hold exactly 12 adoptions, 9 of them out of
#   high, so #e13's own moves dict gives 32 - 9 = 23 - yet its summary states high_rows_after: 27. That is the
#   first error, internal to #e13 and against its own list. (Its prose "13 are adopted" likewise contradicts its
#   own summary, which adds 10 + 2 = 12 adopted against 13 declined for the 25 proposals.)
#   #e13 then HELD P08-012 by name - "no lane proposed on it and I do not move it blind - the boss audit
#   re-weighs it" - the boss audit moved it high -> medium, and #e14 confirmed "the 12 named in #e13 plus
#   P08-012 -> medium remain the mechanical list". So the wave's 13 moves are exactly the authorised 13 and
#   32 - 10 = 22 is CORRECT. The corpus is sound; the arithmetic above it is not.
#   #e15 inherited 27 and reasoned that P08-012 was "already counted there". It could not have been, because
#   #e13 held it. And #e15's answer, 23, happens to equal #e13's TRUE after-count - which is why the slip
#   survived four rounds of review.
#
# SO THIS GATE ASSERTS THE DELTA, WHICH IS WHAT THE RULING DECIDED, and records the base as a measured
# discrepancy. The nine moves are the decision; "23" was arithmetic on a stale base. Asserting 23 would make
# the build fail on a sound corpus; dropping the check would lose the only thing that caught the slip.
ORDERED_DELTA = sum((1 if b == "high" else 0) - (1 if a == "high" else 0) for a, b in MOVES.values())
highs_before = sum(1 for r in rows.values() if r.get("confidence") == "high")
highs_after = highs_before + ORDERED_DELTA
measured_after = sum(1 for rid, r in rows.items()
                     if (MOVES[rid][1] if rid in MOVES else r.get("confidence")) == "high")
count_check = {
    "high_rows_before_MEASURED": highs_before,
    "high_rows_after_MEASURED": measured_after,
    "delta_the_ruling_ordered": ORDERED_DELTA,
    "delta_agrees": measured_after == highs_after,
    "the_rulings_stated_base": 27,
    "the_rulings_stated_after": 23,
    "base_discrepancy": 27 - highs_before,
    "why": ("#e13's summary states high_rows_after 27 where its own 9 high-downgrades give 23; #e13 then HELD "
            "P08-012, which the boss audit moved and #e14 confirmed, taking the true count to 22. #e15 "
            "inherited 27 and treated P08-012 as already counted in it, which it could not be. The wave's 13 "
            "moves are exactly the authorised 13 - the corpus is sound and the arithmetic above it is not."),
    "tier": "MEASURED on the rows at both digests and on the rulings' own lists",
}
print(json.dumps(count_check, indent=1))
if not count_check["delta_agrees"]:
    raise SystemExit("REFUSED: the ordered delta does not reproduce; nothing applied.")

sim = GA.simulate_plan([("confidence", edits)], PRE)
print(json.dumps({"simulation_ok": sim["ok"], "final": sim.get("final_digest_if_applied")}, indent=1))
if not sim["ok"]:
    raise SystemExit("REFUSED")
if "--apply" not in sys.argv:
    print("\n(simulation only; pass --apply)")
    raise SystemExit(0)

rec = GA.apply_edits(edits, PRE, "repair2_step1_confidence", ordered_count=len(edits), apply=True)
rec["batch"] = "REPAIR-2 step 1: the nine grade moves ordered by #e15 q3"
rec["from_values_verified_against_the_corpus"] = True
rec["count_check"] = count_check
rec["grounds_owed"] = GROUND_OWED
rec["obligation_recorded"] = ("between this step and step 2 these nine rows carry a grade their text does not "
                              "yet state. That is a state inside REPAIR-2, never a shipped one, and the close "
                              "gate cannot pass while it holds.")
with (EZ / "author" / "ezek_author_wave_sweep_receipts.jsonl").open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
print(json.dumps({k: rec[k] for k in ("sweep", "e18_parity_digits", "rows_touched", "preimage_sha256",
                                      "postimage_sha256_measured_from_disk")}, indent=1))
