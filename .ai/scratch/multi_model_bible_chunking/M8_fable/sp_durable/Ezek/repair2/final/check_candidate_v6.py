#!/usr/bin/env python3
"""FINAL REMEDIATION CANDIDATE GATE, v6 - v5 unchanged except ONE scoped arm, for the rows #e17 re-tiled.

WHY. v5's claim accounting makes a removed anchor unclean unless the lane accounts for it. On the eight RETILE rows the
live prose is a SEED (the ruling's ground plus the retired rows' texts joined), which the order says to rewrite whole; the
seed is not a reviewed claim set, so enforcing accounting there would buy dozens of 'why' lines about text that argues seams
the row no longer has. On a RETILE row only, every removed anchor is REPORTED to the adjudicator under
'claim_removed_on_retile_seed' and does not make the row unclean. Every other arm - the per-row delta, the English form,
the entry form with clause 6 v2 qualifiers, and the WHOLE suite with no hard member allowed to gain a flag - binds the
RETILE rows exactly as it binds every other row, and every non-RETILE row is judged by v5 byte for byte.

A row is a RETILE row only if the worklist (--worklist, required) carries an item of class RETILE on it.

usage: python check_candidate_v6.py <proposal.json> --work <dir> --worklist <final_worklist.v2.json> [--discharge <path>]
       python check_candidate_v6.py --selftest --worklist <final_worklist.v2.json>
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
if "--worklist" not in sys.argv:
    raise SystemExit("REFUSED: v6 needs --worklist (the RETILE rows are read from it)")
sys.path.insert(0, str(EZ / "repair2" / "step5"))
import check_candidate_v5 as V5                                                # noqa: E402

WL = json.loads(Path(V5.WORKLIST).read_text(encoding="utf-8"))
RETILE_ROWS = {i["row"] for i in WL["items"] if i["class"] == "RETILE" and i["status"] != "DONE"}
_v5_check_row = V5.check_row


def check_row(live_row, fields, allowed):
    rid = live_row["decision_id"]
    if rid not in RETILE_ROWS:
        return _v5_check_row(live_row, fields, allowed)
    cand = dict(live_row)
    cand.update({f: v for f, v in fields.items() if f in allowed})
    removed = sorted(V5.anchors(live_row) - V5.anchors(cand))
    saved = V5.DISCHARGE
    acc = dict(saved.get("claim_accounting") or {})
    lane_acc = {a.get("anchor") for a in (acc.get(rid) or []) if isinstance(a, dict)}
    acc[rid] = list(acc.get(rid) or []) + [{"anchor": a, "why": "RETILE seed: reported, not enforced (v6)"} for a in removed if a not in lane_acc]
    V5.DISCHARGE = dict(saved, claim_accounting=acc)
    try:
        res = _v5_check_row(live_row, fields, allowed)
    finally:
        V5.DISCHARGE = saved
    res["claim_removed_on_retile_seed"] = [a for a in removed if a not in lane_acc]
    res["retile_row"] = True
    return res


V5.check_row = check_row


def selftest_v6():
    live = V5.V2.live_rows()
    sc = V5.scope()
    cases = []
    if not RETILE_ROWS:
        cases.append(("the worklist carries RETILE rows", False))
    else:
        rid = sorted(RETILE_ROWS)[0]
        stripped = {f: V5.A_CV.sub("that verse", V5.A_FACE.sub("that verse", live[rid][f])) for f in V5.PROSE if isinstance(live[rid].get(f), str)}
        V5.DISCHARGE = {}
        r = check_row(live[rid], stripped, sc[rid])
        cases.append(("RETILE row: removed anchors are reported, not unaccounted", bool(r["claim_removed_on_retile_seed"]) and not r["claim_removed_UNACCOUNTED"]))
        r = check_row(live[rid], {"device_notes": live[rid]["device_notes"] + " Held under CUT-RULE limb (b)."}, sc[rid])
        cases.append(("RETILE row: a rule id is still UNCLEAN (every other arm binds)", not r["clean"]))
        other = next(x for x in sorted(sc) if x not in RETILE_ROWS and any(V5.A_CV.search(live[x].get(f) or "") for f in V5.PROSE))
        stripped = {f: V5.A_CV.sub("that verse", V5.A_FACE.sub("that verse", live[other][f])) for f in V5.PROSE if isinstance(live[other].get(f), str)}
        r = check_row(live[other], stripped, sc[other])
        cases.append(("a non-RETILE row keeps v5's enforced accounting", bool(r["claim_removed_UNACCOUNTED"]) and not r["clean"]))
        cases.append(("the RETILE set is exactly the worklist's 8 rows", len(RETILE_ROWS) == 8))
    V5.DISCHARGE = {}
    failed = [n for n, ok in cases if not ok]
    print(json.dumps({"v6_selftest_cases": len(cases), "failed": failed, "retile_rows": sorted(RETILE_ROWS)}, indent=1))
    return 1 if failed else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(V5.selftest() or selftest_v6())
    if selftest_v6():
        raise SystemExit("REFUSED: v6 selftest failed; no verdict computed (E-36)")
    raise SystemExit(V5.main())
