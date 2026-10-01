#!/usr/bin/env python3
"""Record boss ruling B3-2, surface its owner packet, and build the per-ruling EXECUTION LEDGER.

WHAT THE SECOND FINAL CHECK FOUND: ruling B3-2 - the reasoning record, adopted with conditions under the owner's
escalation authority - was neither executed nor recorded. Its own terms say it is "in force for every brief issued
in the Lamentations cycle from this ruling forward and for every following book until the owner rules", and that
"the owner packet travels with the next owner touchpoint and no later than the Lamentations close packet". Neither
happened. Roughly thirteen attempts launched after the ruling without the record it ordered, and the owner packet
sat in a review file nobody surfaced.

The pattern behind this and behind the B3-1 companion edits is the same, and it is worth naming: a boss ruling is
not a verdict, it is a set of CONSEQUENCES, and this campaign had no place where a ruling's consequences were listed
one by one with an executed/declined mark against each. B3-1's condition was half-executed for the same reason. So
this tool does two things: it records B3-2, and it builds the execution ledger the checker asked for, seeded with
every consequence of both rulings and its true state.

The ledger is the durable control. The record entry is just the disclosure.
Usage: _record_b3_rulings.py [--apply]"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOSS = HERE / "reviews" / "boss_lam_b3.json"
LEDGER = HERE / "reviews" / "ruling_execution_ledger.v1.json"
LOG = HERE / "freeze" / "CYCLE_STATE.md"
NL = "\n"


def main():
    apply = "--apply" in sys.argv
    b3 = json.load(open(BOSS, encoding="utf-8-sig"))
    r1 = next(r for r in b3["rulings"] if r["id"] == "B3-1")
    r2 = next(r for r in b3["rulings"] if r["id"] == "B3-2")
    ce = r1["consequence"]["companion_edits_P02-006"]

    entries = [
        {"ruling": "B3-1", "n": 1, "consequence": "scanner enforces the narrowed CWO-1 predicate (29 test vectors)",
         "state": "EXECUTED", "evidence": "_cwo_scan.py cwo1_verdict(); cwo/scan_correction_record.v1.json entry 6",
         "executed_late": True},
        {"ruling": "B3-1", "n": 2, "consequence": "CWO-1 stands unedited in boss_lam_b1.json",
         "state": "EXECUTED", "evidence": "reviews/boss_lam_b1.json unmodified", "executed_late": False},
        {"ruling": "B3-1", "n": 3, "consequence": ce[0], "state": "EXECUTED",
         "evidence": "rows_v11 P02-006 observed_substrate_signals carries acrostic.triplet_nun_samekh_pe_partial",
         "executed_late": False},
        {"ruling": "B3-1", "n": 4, "consequence": ce[1], "state": "EXECUTED",
         "evidence": "rows_v11 P02-006 device_notes reads 'the pe triplet is entered but not completed here'",
         "executed_late": False},
        {"ruling": "B3-1", "n": 5, "consequence": ce[2], "state": "ORDERED - NOT YET EXECUTED",
         "evidence": "the neighbouring-unit phrase still stands in rows_v11; ordered in spot/orders_fix_04.json",
         "executed_late": None,
         "why_missed": "the ruling states its condition twice - a one-line summary and a five-item companion-edit "
                       "list. Three rounds acted on the summary; nobody opened the list."},
        {"ruling": "B3-1", "n": 6, "consequence": ce[3], "state": "PARTIALLY EXECUTED",
         "evidence": "the never-conflated clause and tier caveat stand in rows_v11; the close-seam clause naming "
                     "the Lam.3.48 mark does not. Ordered in spot/orders_fix_04.json.",
         "executed_late": None,
         "orchestrator_precheck": "pmarks_Lam.json gives SAMEKH at Lam.3.48, so the ruling's claim holds; the "
                                  "author is nonetheless ordered to verify it independently and to refuse to write "
                                  "the clause if the inventory disagrees"},
        {"ruling": "B3-1", "n": 7, "consequence": ce[4], "state": "EXECUTED",
         "evidence": "no span, confidence or tiling change on P02-006 across rows_v9..rows_v11; tiling 154/154 GREEN",
         "executed_late": False},
        {"ruling": "B3-1", "n": 8, "consequence": "history rule: CWO-1 reports carry the narrowed-predicate label",
         "state": "PARTIALLY EXECUTED",
         "evidence": "the label is in _cwo_scan.py (CWO1_LABEL) but the parity records and the scanner's JSON "
                     "reports do not carry it; raised as a low residual by final check 02",
         "executed_late": None},
        {"ruling": "B3-2", "n": 1, "consequence": "the reasoning record is in force for every brief issued from "
                                                  "this ruling forward, until the owner rules",
         "state": "NOT EXECUTED",
         "evidence": "0 hits for a record clause across the four briefs issued after the ruling; at least thirteen "
                     "attempts launched without it (three sidecars, two postchecks, fix f01, four stage-1 "
                     "auditors, two stage-2 checks, f02, f03)",
         "executed_late": None,
         "orchestrator_note": "not retroactive by the ruling's own terms; it binds the NEXT launch onward"},
        {"ruling": "B3-2", "n": 2, "consequence": "the owner packet travels with the next owner touchpoint and no "
                                                  "later than the Lamentations close packet",
         "state": "SURFACED " + datetime.now(timezone.utc).strftime("%Y-%m-%d"),
         "evidence": "carried to the owner in the session's close report alongside the stage-2 checker's own "
                     "escalation, which asks the same question independently",
         "executed_late": True,
         "orchestrator_note": "the packet sat unsurfaced in reviews/boss_lam_b3.json. Two independent Fable lanes "
                              "reached the same recommendation - the boss when it adopted the record, and the "
                              "stage-2 checker when it escalated - which is worth the owner knowing."},
        {"ruling": "B3-2", "n": 3, "consequence": "the owner's correction is applied forward and recorded verbatim, "
                                                  "append-only",
         "state": "PENDING - awaiting the owner's answer", "evidence": "no owner answer recorded in the ledger or "
                                                                      "the cycle log", "executed_late": None},
    ]

    led = {"schema": "m8_ruling_execution_ledger.v1", "book": "Lam",
           "built": datetime.now(timezone.utc).isoformat(),
           "why_this_exists": "a boss ruling is not a verdict but a set of CONSEQUENCES, and this campaign had no "
                              "place where each consequence carried an executed/declined mark. B3-1's condition was "
                              "half-executed and B3-2 was not executed at all, both for that reason. Ordered by the "
                              "second OW-6 stage-2 final check.",
           "source_ruling_file": str(BOSS), "source_sha256": hashlib.sha256(BOSS.read_bytes()).hexdigest(),
           "entries": entries,
           "digits": {"total": len(entries),
                      "executed": sum(1 for e in entries if e["state"].startswith("EXECUTED")),
                      "partial": sum(1 for e in entries if e["state"].startswith("PARTIALLY")),
                      "ordered_not_executed": sum(1 for e in entries if e["state"].startswith("ORDERED")),
                      "not_executed": sum(1 for e in entries if e["state"].startswith("NOT")),
                      "surfaced": sum(1 for e in entries if e["state"].startswith("SURFACED")),
                      "pending_owner": sum(1 for e in entries if e["state"].startswith("PENDING"))},
           "law": "no ruling of this campaign is closed until every consequence here carries EXECUTED or DECLINED "
                  "with a reason. A close that leaves one at ORDERED or PARTIALLY is not a close.",
           "authority": "orchestrator record of boss rulings; the rulings themselves are unedited"}

    sys.stdout.reconfigure(encoding="utf-8")
    if not apply:
        print(json.dumps({"dry_run": True, "entries": len(entries), "digits": led["digits"]}, indent=1))
        return 0

    LEDGER.write_text(json.dumps(led, ensure_ascii=False, indent=1), encoding="utf-8", newline=NL)

    entry = ["",
             f"## BOSS RULINGS B3-1 / B3-2 EXECUTION LEDGER {datetime.now(timezone.utc).strftime('%Y-%m-%d')} (session dce0b6e2)",
             "- the second OW-6 stage-2 final check found ruling B3-2 (the reasoning record, adopted with conditions",
             "  under the owner's escalation authority) neither executed nor recorded, and B3-1's companion edits",
             "  half-executed. Both have the same cause: a ruling is a set of CONSEQUENCES and nothing tracked them",
             "  one by one.",
             "- reviews/ruling_execution_ledger.v1.json now lists every consequence of both rulings with its state:",
             f"    executed {led['digits']['executed']}, partially executed {led['digits']['partial']}, "
             f"ordered-not-executed {led['digits']['ordered_not_executed']}, not executed {led['digits']['not_executed']},",
             f"    surfaced {led['digits']['surfaced']}, pending the owner {led['digits']['pending_owner']}.",
             "- LAW ADDED: no ruling is closed until every consequence carries EXECUTED or DECLINED with a reason. A",
             "  close that leaves one at ORDERED or PARTIALLY is not a close.",
             "- B3-2's OWNER PACKET IS SURFACED TO THE OWNER TODAY, in the session's close report. It asks the same",
             "  question the stage-2 checker escalated independently: ratify the self-authored reasoning record as",
             "  the durable substitute for chain of thought, and re-scope OW-6/OW-6c accordingly. Two separate Fable",
             "  lanes reached that recommendation without conferring.",
             "- B3-2's record clause is NOT retroactive by the ruling's own terms; it binds the next launch onward.",
             ""]
    pre = LOG.read_bytes()
    body = pre if pre.endswith(b"\n") else pre + b"\n"
    LOG.write_bytes(body + NL.join(entry).encode("utf-8"))
    assert LOG.read_bytes().startswith(body), "log preimage not intact"

    print(json.dumps({"status": "RECORDED", "ledger": str(LEDGER), "digits": led["digits"],
                      "ledger_sha16": hashlib.sha256(LEDGER.read_bytes()).hexdigest()[:16]}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
