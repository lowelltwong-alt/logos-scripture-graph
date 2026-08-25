#!/usr/bin/env python3
"""Orchestrator: consolidate peer rulings into (a) the author work-order
roster (upheld/refined rulings with remedies), (b) the boss docket
(boundary/unit_type-change proposals, either/or remedies, escalations,
cross-cluster policy questions), (c) the new-findings list. Deterministic
extraction; writes SP/Eccl/work_orders.json."""
import json
import re
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from pathlib import Path
from collections import Counter

SPBOOK = Path(__file__).resolve().parent.parent
REV = SPBOOK / "reviews"

BOUNDARY = re.compile(r"respan|retire|split|merg|re-?cut|atomic row|retype|"
                      r"unit_type change|either supply|either provide|or convert|"
                      r"or retype|or split|boundary change", re.I)

orders = []
boss_docket = []
new_findings = []
counts = Counter()
for f in sorted(REV.glob("c*_PEER*.json")):
    p = json.loads(f.read_text(encoding="utf-8"))
    for r in p.get("rulings", []):
        counts[r.get("ruling", "?")] += 1
        entry = {
            "cluster": r.get("cluster") or (p.get("clusters") or ["?"])[0],
            "row_id": r.get("row_id"), "source": r.get("source"),
            "ruling": r.get("ruling"), "severity": r.get("severity_final"),
            "remedy": r.get("remedy"), "packet": f.name,
        }
        if r.get("ruling") == "escalate":
            boss_docket.append({**entry, "docket_class": "peer_escalation"})
        elif r.get("ruling") in ("uphold", "refine") and r.get("remedy"):
            if BOUNDARY.search(str(r.get("remedy", ""))):
                boss_docket.append({**entry, "docket_class": "boundary_flavored_remedy"})
            else:
                orders.append(entry)
        elif r.get("ruling") in ("uphold", "refine"):
            orders.append({**entry, "remedy": r.get("remedy") or "MISSING_REMEDY"})
    for s in p.get("supported_sample", []):
        if s.get("result") == "defect_found":
            new_findings.append({"packet": f.name, **s})

# cross-cluster policy items the orchestrator poses to the boss
boss_docket.append({
    "docket_class": "cross_cluster_policy",
    "row_id": None, "cluster": "c05+c09",
    "question": ("Does a cohesion driver that matches only at SKELETON tier "
                 "(e.g. the 7:2/7:4 bet-avel bracket, prefixed-bet at one end) "
                 "satisfy the owner's 'byte-grounded cohesion NAMED' bar for "
                 "saying_cluster rows once the tier is honestly disclosed, or "
                 "does the bar require byte-tier identity / multiple "
                 "independent drivers? Rule the controlling standard and apply "
                 "it decision-locally to the standing cluster rows "
                 "(p02-013 7:2-4, p02-014 7:5-6, P03-015 10:10-11)."),
})

by_part = Counter((o["row_id"] or "?")[:3].lower() for o in orders)
out = {
    "built": "post-peer consolidation, 2026-08-19",
    "ruling_counts": dict(counts),
    "author_orders": orders,
    "author_orders_by_part": dict(by_part),
    "boss_docket": boss_docket,
    "new_findings": new_findings,
}
(SPBOOK / "work_orders.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({"ruling_counts": dict(counts),
                  "author_orders": len(orders),
                  "by_part": dict(by_part),
                  "boss_docket": len(boss_docket),
                  "boss_items": [{k: (str(v)[:100] if v else v) for k, v in d.items()
                                  if k in ("docket_class", "row_id", "cluster")}
                                 for d in boss_docket],
                  "new_findings": len(new_findings),
                  "missing_remedies": sum(1 for o in orders if o.get("remedy") == "MISSING_REMEDY")},
                 ensure_ascii=False, indent=1))
