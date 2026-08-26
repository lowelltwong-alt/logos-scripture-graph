#!/usr/bin/env python3
"""Orchestrator: consolidate peer rulings into SP/Song/work_orders.json —
ordinary-cure author orders (partitioned by writer part), the TRUE boss
docket (escalations + boundary-change proposals inside remedies, which are
proposals only until boss adoption), boss-pending rows (excluded from author
phase 1), and the sample-defect orders not already covered by a ruling."""
import json
import re
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from pathlib import Path

SPBOOK = Path(__file__).resolve().parent.parent
R = SPBOOK / "reviews"

BOUNDARY = re.compile(r"\brespan\b|\bre-span\b|\bmerge\b|\bmerging\b|\bsplit\b|"
                      r"\bretire\b|\bextend(?:ing|ed)?\s+the\s+(?:span|row|unit)\b|"
                      r"\bmove\s+the\s+(?:boundary|seam)\b|\bboundary\s+change\b|"
                      r"\babsorb\b|\bnew\s+row\b", re.I)

orders = []
boss_docket = []
for f in sorted(R.glob("c0*_PEER*.json")):
    d = json.loads(f.read_text(encoding="utf-8-sig"))
    for x in d["rulings"]:
        entry = {
            "cluster": x.get("cluster"), "row_id": x["row_id"],
            "source": x.get("source"), "ruling": x["ruling"],
            "severity": x.get("severity_final"),
            "challenge_claim": x.get("challenge_claim"),
            "grounds": x.get("grounds"),
            "remedy": x.get("remedy"),
            "packet": f.name,
        }
        if x["ruling"] == "escalate":
            boss_docket.append({**entry, "docket_kind": "peer_escalation"})
        elif x["ruling"] in ("uphold", "refine"):
            rem = x.get("remedy") or ""
            if BOUNDARY.search(rem):
                boss_docket.append({**entry, "docket_kind": "boundary_proposal_in_remedy"})
            else:
                orders.append(entry)

boss_rows = sorted({b["row_id"] for b in boss_docket})
# the 8:5|8:6 escalation is a seam-pair: P02-017 is named inside the P02-018
# escalation grounds — pull any row ids the escalation text names
for b in boss_docket:
    for m in re.finditer(r"\bP0\d-\d{3}\b", (b.get("grounds") or "") + " " + (b.get("challenge_claim") or "")):
        if m.group(0) not in boss_rows:
            boss_rows.append(m.group(0))
boss_rows = sorted(boss_rows)

phase1 = [o for o in orders if o["row_id"] not in boss_rows]
held = [o for o in orders if o["row_id"] in boss_rows]
by_part = {}
for o in phase1:
    part = "p01" if o["row_id"].startswith("P01") else "p02"
    by_part.setdefault(part, []).append(o)

out = {
    "built": "post-peer consolidation (orchestrator triage)",
    "orders_phase1_total": len(phase1),
    "orders_by_part": {k: len(v) for k, v in by_part.items()},
    "boss_docket_total": len(boss_docket),
    "boss_pending_rows_excluded_from_phase1": boss_rows,
    "orders_held_pending_boss": [o["row_id"] for o in held],
    "phase1": by_part,
    "held_pending_boss": held,
    "boss_docket": boss_docket,
}
(SPBOOK / "work_orders.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({"phase1_orders": len(phase1),
                  "by_part": out["orders_by_part"],
                  "boss_docket": len(boss_docket),
                  "docket_rows": boss_rows,
                  "held_orders": [o["row_id"] for o in held],
                  "docket_kinds": [b["docket_kind"] + ":" + b["row_id"] for b in boss_docket]},
                 ensure_ascii=False, indent=1))
