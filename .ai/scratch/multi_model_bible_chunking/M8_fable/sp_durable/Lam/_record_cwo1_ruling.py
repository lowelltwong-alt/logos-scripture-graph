#!/usr/bin/env python3
"""Fix-round item (3): record the CWO-1 ruling, the scanner change it authorised, and the ONE condition of it that
was never executed.

THE STAGE-2 CHECKER'S RESIDUAL said the CWO-1 amendment had no record and asked for the ruling "by exact path", or
else for its own ruling to be adopted. Both halves of that are now answerable:

  THE RULING EXISTS. It is B3-1 in SP/Lam/reviews/boss_lam_b3.json, issued by the third boss attempt
  (lam_boss_b3_a1, claude-fable-5-1). The checker was never given that path, so it could not see it, and it said
  plainly that if the boss had ruled, its ruling stands and the checker's own is withdrawn. It does, and it is.
  The scanner's implementation matches B3-1's predicate: mark-layer tokens barred under every prefix; the letter
  homonyms samekh and pe permitted only inside the acrostic namespace and only without a mark-context co-token.

  WHAT WAS MISSING IS THE RECORD, and one substantive thing besides. The scanner narrowing is not among the five
  entries of the scan-correction record, the cycle log carries no entry for the escalation or its ruling, and -
  found while writing this - B3-1's own PRICE was never paid. The ruling says: "The price at the one site where the
  collision is live is an explicit never-conflated sentence in P02-006's device_notes." P02-006 carries no such
  sentence. Its device_notes speaks of "SAMEKH marks" at Lam.3.42 and Lam.3.45 while its key carries the samekh
  LETTER, which is exactly the collision the sentence was meant to disarm, standing undisclosed on the row.

That last item is a boss ruling accepted and then not executed. It is more serious than the missing paperwork,
because the narrowing of a corpus-wide order was granted ON that condition. This tool records it and amends the
live fix-round orders so the row is cured in this wave rather than after it.
Usage: _record_cwo1_ruling.py [--apply]"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCR = HERE / "cwo" / "scan_correction_record.v1.json"
ORDERS = HERE / "spot" / "orders_fix_02.json"
LOG = HERE / "freeze" / "CYCLE_STATE.md"
BOSS = HERE / "reviews" / "boss_lam_b3.json"
NL = "\n"

SIXTH = {
    "n": 6,
    "what": "CWO-1's token predicate was narrowed in _cwo_scan.py: cwo1_verdict(key) implements B3-1's three rules "
            "(R1 mark-layer token under any prefix; R2 letter/mark homonym outside the acrostic namespace; R3 "
            "letter/mark homonym paired with mark wording) in place of the issued flat token list.",
    "why": "NOT a scanner defect and NOT the orchestrator's judgement: this change executes boss ruling B3-1 "
           "(2026-09-07, SP/Lam/reviews/boss_lam_b3.json), which narrowed CWO-1 after the second-generation catch "
           "found that the same string names a tier-1 acrostic LETTER and a tier-3 parashah MARK, and the "
           "campaign's own hazard law forbids conflating those layers.",
    "authority": "boss ruling B3-1 by lam_boss_b3_a1 (claude-fable-5-1); the issued order stands unedited in "
                 "reviews/boss_lam_b1.json",
    "how_it_differs_from_corrections_1_to_5": "those five were corrections to a scanner that was misreading its own "
                                              "order; this one implements a change to the ORDER itself, made by the "
                                              "boss, and is recorded here because a reader comparing scans across "
                                              "the wave must see every reason the tool's verdicts moved",
    "self_test": "29 vectors in _cwo_scan.py exercise R1/R2/R3 and their negatives",
    "recorded_late": True,
    "recorded_late_note": "this entry was written during the OW-6 fix round after the stage-2 final checker found "
                          "the scan-correction record listed five corrections and not this one",
}

CONDITION_ITEM = {
    "e_class": "boss ruling B3-1 condition not executed",
    "severity": "medium",
    "origin": "orchestrator, during fix-round item 3 - NOT raised by the stage-2 checker, which lacked the ruling's path",
    "field": "device_notes",
    "defective_text": "(absence) - device_notes names the SAMEKH marks at Lam.3.42 and Lam.3.45 while the row's key "
                      "observed_substrate_signals carries acrostic.triplet_nun_samekh_pe_partial, the samekh "
                      "LETTER; no sentence distinguishes the two layers",
    "byte_evidence": "boss ruling B3-1 (reviews/boss_lam_b3.json) narrowed CWO-1 and set its price: 'The price at "
                     "the one site where the collision is live is an explicit never-conflated sentence in P02-006's "
                     "device_notes.' The narrowing was implemented in the scanner and the row shipped in rows_v9 "
                     "without the sentence. The row's own device_notes uses the word 'SAMEKH' for the mark layer.",
    "proposed_cure": "Add ONE sentence to device_notes stating that the samekh in this row's acrostic key is the "
                     "Hebrew LETTER naming the triplet's position in the alphabetic spine (tier-1, from the verse "
                     "bytes) and is never the SAMEKH parashah mark cited in this same field (tier-3, single-witness "
                     "from the seg inventory), and that the two are not conflated. Change nothing else: no span, no "
                     "label, no key, and do not alter the existing mark citations.",
}


def main():
    apply = "--apply" in sys.argv
    boss = json.load(open(BOSS, encoding="utf-8-sig"))
    ruling = next((r for r in boss.get("rulings", []) if r.get("id") == "B3-1"), None)
    assert ruling, "B3-1 not found in the boss packet"

    scr = json.load(open(SCR, encoding="utf-8-sig"))
    already = any(c.get("n") == 6 for c in scr.get("corrections", []))
    orders = json.load(open(ORDERS, encoding="utf-8-sig"))
    p2 = orders["orders"].get("P02-006")
    assert p2, "P02-006 is not in the live fix orders"
    cond_present = any(i.get("e_class", "").startswith("boss ruling B3-1") for i in p2["residuals"])

    plan = {"ruling_found_at": str(BOSS), "ruling_id": "B3-1",
            "boss_attempt": boss.get("attempt_id"), "boss_model": boss.get("model"),
            "checker_ruling_withdrawn_by_its_own_terms": True,
            "scan_correction_entries_now": len(scr.get("corrections", [])),
            "would_add_sixth_entry": not already,
            "condition_of_B3-1": "an explicit never-conflated sentence in P02-006 device_notes",
            "condition_executed_in_rows_v9": False,
            "would_amend_live_orders": not cond_present,
            "dry_run": not apply}
    sys.stdout.reconfigure(encoding="utf-8")
    if not apply:
        print(json.dumps(plan, indent=1))
        return 0

    now = datetime.now(timezone.utc).isoformat()
    if not already:
        scr.setdefault("corrections", []).append(SIXTH)
        scr["amended_at"] = now
        scr["amendment_note"] = ("a sixth entry was appended during the OW-6 fix round: it records a change to the "
                                 "ORDER made by boss ruling B3-1, not a correction of the scanner's own reading. "
                                 "Entries 1-5 are unedited.")
        SCR.write_text(json.dumps(scr, ensure_ascii=False, indent=1), encoding="utf-8", newline=NL)

    if not cond_present:
        p2["residuals"].append(CONDITION_ITEM)
        orders["amended_at"] = now
        orders["amendment_note"] = ("P02-006 gained one item AFTER this slice was launched: boss ruling B3-1's "
                                    "condition was found unexecuted while recording the ruling. The row set is "
                                    "unchanged, so ordered/emitted parity is unaffected; the author was notified. "
                                    "The amendment is recorded here so the orders file remains the record of what "
                                    "was actually ordered.")
        ORDERS.write_text(json.dumps(orders, ensure_ascii=False, indent=1), encoding="utf-8", newline=NL)

    entry = ["",
             f"## CWO-1 RULING RECORDED {datetime.now(timezone.utc).strftime('%Y-%m-%d')} (session dce0b6e2) - fix-round item 3",
             "- the second-generation catch escalated a conflict between CWO-1's token ban and the tier-1 acrostic",
             "  LETTER name in P02-006's key. The escalation and its ruling had no cycle-log entry until now.",
             f"- RULING B3-1 EXISTS: reviews/boss_lam_b3.json (sha256 {hashlib.sha256(BOSS.read_bytes()).hexdigest()[:16]}...),",
             "  issued by lam_boss_b3_a1 (claude-fable-5-1). It NARROWS CWO-1 rather than rewriting it; the issued",
             "  order stands unedited in reviews/boss_lam_b1.json. The stage-2 final checker offered its own ruling",
             "  only in case none had been written, and withdrew it by its own terms once the boss ruling was found.",
             "- the scanner change implementing B3-1 is now the sixth entry of cwo/scan_correction_record.v1.json,",
             "  distinguished there from corrections 1-5, which fixed the scanner's reading of its own order.",
             "- FOUND WHILE RECORDING THIS: B3-1's condition was never executed. The ruling granted the narrowing at",
             "  a price - an explicit never-conflated sentence in P02-006's device_notes - and rows_v9 carries no",
             "  such sentence, while that same field calls Lam.3.42 and Lam.3.45 SAMEKH marks. A corpus-wide order",
             "  was narrowed on a condition that was then not met. The live fix-round orders for P02-006 were",
             "  amended to cure it in this wave and the author was notified; the amendment is recorded in",
             "  spot/orders_fix_02.json so that file stays the record of what was ordered.",
             ""]
    pre = LOG.read_bytes()
    body = pre if pre.endswith(b"\n") else pre + b"\n"
    LOG.write_bytes(body + NL.join(entry).encode("utf-8"))
    assert LOG.read_bytes().startswith(body), "log preimage not intact"

    print(json.dumps({"status": "RECORDED", "sixth_scan_entry_added": not already,
                      "orders_amended": not cond_present,
                      "scan_record_sha16": hashlib.sha256(SCR.read_bytes()).hexdigest()[:16],
                      "orders_sha16": hashlib.sha256(ORDERS.read_bytes()).hexdigest()[:16],
                      "log_appended": True}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
