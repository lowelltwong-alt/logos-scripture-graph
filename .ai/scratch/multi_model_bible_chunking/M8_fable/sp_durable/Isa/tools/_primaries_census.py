#!/usr/bin/env python3
"""Batch census for dual-blind primary packets (orchestrator tool).

Usage: _primaries_census.py c01 c02 ...  — checks, for each named cluster:
both cNN_LF.json and cNN_OL.json exist, parse, carry the right attempt ids,
review EXACTLY the cluster plan's row_ids (rows_reviewed and items agree),
severity present only on challenges, and summary arithmetic matches items.
Prints per-packet lines + aggregate tallies. Exit 1 on any hard defect.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SP_ISA = Path(__file__).resolve().parent.parent
PLAN = json.loads((SP_ISA / "review_clusters.json").read_text(encoding="utf-8"))
CLUSTERS = {c["id"]: c for c in PLAN["clusters"]}


def check(cid: str, role: str) -> tuple[list[str], dict]:
    defects: list[str] = []
    f = SP_ISA / "reviews" / f"{cid}_{role}.json"
    if not f.exists():
        return [f"{cid}_{role}: MISSING"], {}
    d = json.loads(f.read_text(encoding="utf-8"))
    want_rows = CLUSTERS[cid]["row_ids"]
    if d.get("attempt_id") != f"primary_isa_{cid}_{role}_r1":
        defects.append(f"{cid}_{role}: attempt_id {d.get('attempt_id')}")
    if d.get("role") != f"primary_{role}":
        defects.append(f"{cid}_{role}: role {d.get('role')}")
    if d.get("cluster") != cid:
        defects.append(f"{cid}_{role}: cluster {d.get('cluster')}")
    if sorted(d.get("rows_reviewed", [])) != sorted(want_rows):
        defects.append(f"{cid}_{role}: rows_reviewed mismatch vs plan")
    item_rows = [it.get("row_id") for it in d.get("items", [])]
    if sorted(item_rows) != sorted(want_rows):
        defects.append(f"{cid}_{role}: items rows {item_rows} != plan")
    sup = sum(1 for it in d["items"] if it.get("verdict") == "support")
    cha = sum(1 for it in d["items"] if it.get("verdict") == "challenge")
    bysev = {"high": 0, "medium": 0, "low": 0}
    for it in d["items"]:
        v, s = it.get("verdict"), it.get("severity")
        if v == "challenge":
            if s not in bysev:
                defects.append(f"{cid}_{role}: {it.get('row_id')} bad severity {s}")
            else:
                bysev[s] += 1
        elif s:
            defects.append(f"{cid}_{role}: {it.get('row_id')} severity on support")
        if v not in ("support", "challenge"):
            defects.append(f"{cid}_{role}: {it.get('row_id')} bad verdict {v}")
    summ = d.get("summary", {})
    if summ.get("supports") != sup or summ.get("challenges") != cha:
        defects.append(f"{cid}_{role}: summary counts disagree with items")
    got_sev = {k: v for k, v in (summ.get("by_severity") or {}).items() if v}
    if got_sev != {k: v for k, v in bysev.items() if v}:
        defects.append(f"{cid}_{role}: by_severity disagrees with items")
    return defects, {"sup": sup, "cha": cha, **bysev}


def main() -> int:
    cids = sys.argv[1:]
    all_defects: list[str] = []
    agg = {"sup": 0, "cha": 0, "high": 0, "medium": 0, "low": 0}
    per_row_challenges: dict[str, list[str]] = {}
    for cid in cids:
        for role in ("LF", "OL"):
            defects, stats = check(cid, role)
            all_defects.extend(defects)
            if stats:
                for k in agg:
                    agg[k] += stats[k]
                print(f"{cid}_{role}: sup={stats['sup']} cha={stats['cha']} "
                      f"h/m/l={stats['high']}/{stats['medium']}/{stats['low']}")
    # challenged-row inventory for the peer phase (union across roles)
    for cid in cids:
        for role in ("LF", "OL"):
            f = SP_ISA / "reviews" / f"{cid}_{role}.json"
            if not f.exists():
                continue
            d = json.loads(f.read_text(encoding="utf-8"))
            for it in d.get("items", []):
                if it.get("verdict") == "challenge":
                    per_row_challenges.setdefault(it["row_id"], []).append(
                        f"{role}:{it.get('severity')}")
    n_rows = sum(len(CLUSTERS[c]["row_ids"]) for c in cids)
    challenged = {k: v for k, v in sorted(per_row_challenges.items())}
    both = [r for r, v in challenged.items()
            if any(x.startswith("LF") for x in v) and any(x.startswith("OL") for x in v)]
    print(json.dumps({
        "clusters": len(cids), "rows": n_rows, "packets": len(cids) * 2,
        "aggregate": agg,
        "rows_challenged_any": len(challenged),
        "rows_challenged_both_roles": len(both),
        "both_roles_rows": both,
        "defects": all_defects,
        "status": "RED" if all_defects else "GREEN",
    }, indent=1))
    return 1 if all_defects else 0


if __name__ == "__main__":
    raise SystemExit(main())
