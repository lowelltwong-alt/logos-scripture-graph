#!/usr/bin/env python3
"""REPAIR-2 step-3 CANDIDATE GATE, v3.1 - corrects two defects BOTH blind author lanes hit in v3.

DEFECT 1 - TWO RULES THAT COULD NOT BOTH BE MET. v3 refused edits to fields no owed item named, yet marked a row
unclean for register flags ANYWHERE in it. Rows P02-003, P08-013 and P09-002 carry pre-existing register flags in
fields no step-3 item opens, so they could never be clean whatever an author wrote. Lane A stopped eight items on it
(its ESC-1); lane B left the rows out and escalated. Same shape as E-34's six-word cap against a required phrase -
this time in the orchestrator's own gate. v3.1 judges a row by the flags its proposal INTRODUCES, measured as a delta
against the live row: pre-existing register flags belong to step 5, never to the author who did not create them.

DEFECT 2 - ADVISORY HINTS MADE BINDING. v3 took each worklist item's field list as a hard scope, and those lists were
the orchestrator's guesses: lane A found four items whose claim sits in a field the list did not name (ESC-2). v3.1
scopes by ROW: every prose field and the refs of a row that owes an item may change; observed_substrate_signals only
on a row whose item names it. The field lists stay in the worklist as hints.

UNCHANGED: entry form on every new or changed refs entry (pinned vocabulary, no face qualifier yet, 1-6 word
annotation, faces, zone), and the WHOLE pinned suite on the candidate with no hard member allowed to gain a flag.
A selftest with fixtures that must fail - and the exact contradiction the lanes hit, which must now pass - gates
every verdict.

usage: python check_candidate_v3_1.py <proposal.json> --work <dir>
       python check_candidate_v3_1.py --selftest
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_candidate_v3 as V3                                                # noqa: E402

V2 = V3.V2
PROSE, REFS, SIG = V3.PROSE, V3.REFS, V3.SIG


def scope():
    wl = json.loads(V3.WORKLIST.read_text(encoding="utf-8"))
    rows, sig = set(), set()
    for i in wl["items"]:
        if i["status"] == "DISCHARGED":
            continue
        rows.add(i["row"])
        if any("signals" in f for f in i["fields"]):
            sig.add(i["row"])
    return {r: set(PROSE) | {REFS} | ({SIG} if r in sig else set()) for r in rows}


def _flags(row):
    flags = V2.CR.scan_row(row, "c")
    a = V2.CM.analyze_row(row)
    return ({(f["field"], f["class"], f["match"]) for f in flags},
            {(x.get("citation"), x.get("field")) for x in (a.get("items") or [])},
            {json.dumps(x, sort_keys=True, ensure_ascii=False) for x in (a.get("orphan_refs") or [])},
            {json.dumps(x, sort_keys=True, ensure_ascii=False) for x in (a.get("mirror_reading_disagreements") or [])})


def check_row(live_row, fields, allowed):
    probs = [{"field": f, "problem": "outside step-3 scope for this row"} for f in fields if f not in allowed]
    cand = dict(live_row)
    cand.update({f: v for f, v in fields.items() if f in allowed})
    if REFS in fields and REFS in allowed:
        old = list(live_row.get(REFS) or [])
        for e in fields[REFS]:
            if e not in old:
                probs.extend({"field": REFS, "entry": e, "problem": p} for p in V2.check_new_entry(e))
    lr, lu, lo, ld = _flags(live_row)
    cr, cu, co, cd = _flags(cand)
    new_reg, new_unm, new_orph, new_dis = cr - lr, cu - lu, co - lo, cd - ld
    return {"clean": not (probs or new_reg or new_unm or new_orph or new_dis), "form_problems": probs,
            "NEW_register_flags": sorted(new_reg), "NEW_unmirrored_citations": sorted(new_unm),
            "NEW_orphan_refs": sorted(new_orph), "NEW_mirror_disagreements": sorted(new_dis),
            "preexisting_register_flags_left_for_step_5": len(lr & cr),
            "register_flags_cleared": len(lr - cr)}


def selftest():
    live, sc = V2.live_rows(), scope()
    cases = []
    r = "P02-003"
    pre, _, _, _ = _flags(live[r])
    contradiction = check_row(live[r], {"device_notes": "The span carries no K/Q note and no paseq."}, sc.get(r, set()))
    cases.append(("THE CONTRADICTION BOTH LANES HIT: a clean edit on a row with pre-existing register flags elsewhere "
                  "is CLEAN", r in sc and bool(pre) and contradiction["clean"]))
    cases.append(("a proposal that INTRODUCES a register flag is unclean",
                  not check_row(live[r], {"device_notes": "disclosed under CUT-RULE limb (b)"}, sc[r])["clean"]))
    out_row = next(x for x in live if x not in sc)
    cases.append(("a row that owes no item is refused", not check_row(live[out_row], {"device_notes": "x"}, set())["clean"]))
    cases.append(("signals on a row whose items do not name signals are refused",
                  not check_row(live[r], {SIG: {}}, sc[r])["clean"]))
    q = list(live["P09-010"][REFS]) + ["oshb:Ezek.39.21 [WARRANT-onset:near] onset verse"]
    cases.append(("a face qualifier is still refused", any("step-4" in p["problem"] for p in
                                                           check_row(live["P09-010"], {REFS: q}, sc["P09-010"])["form_problems"])))
    cases.append(("any prose field of an owed row is in scope (the hints are advisory)",
                  PROSE[0] in sc[r] and PROSE[1] in sc[r] and PROSE[2] in sc[r]))
    failed = [n for n, ok in cases if not ok]
    print(json.dumps({"selftest_cases": len(cases), "failed": failed,
                      "p02_003_preexisting_register_flags": len(pre)}, indent=1))
    return 1 if failed else 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    if selftest():
        raise SystemExit("REFUSED: selftest failed; no verdict computed (E-36)")
    # the per-row arm is v3.1's; the whole-suite arm is v3's, reused unchanged by rebinding its row checker and scope
    V3.check_row = lambda live_row, fields, allowed: check_row(live_row, fields, allowed)
    V3.scope = scope
    V3.selftest = lambda: 0
    return V3.main()


if __name__ == "__main__":
    raise SystemExit(main())
