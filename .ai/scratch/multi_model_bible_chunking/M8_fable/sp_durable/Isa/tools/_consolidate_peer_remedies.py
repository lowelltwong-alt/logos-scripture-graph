"""Consolidate Isaiah peer rulings into the boss-round input (m8-mesh-r3).

Reads all 29 peer packets, splits upheld/refined remedies into:
  - boundary_proposals: remedies whose text proposes respan/merge/split/
    dissolve/boundary movement (peer proposals REQUIRE boss adoption);
  - ordinary_cures: in-field work orders for the author wave.
Also collects the 2 refutes and per-row severity_final. Writes
../peer_work_orders.json. Keyword bucketing is a triage aid; the orchestrator
reviews the boundary bucket before the boss launch.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SP_ISA = os.path.dirname(HERE)
REVIEWS = os.path.join(SP_ISA, "reviews")

BOUNDARY_RE = re.compile(
    r"respan|re-span|boundary (change|move|proposal|shift)|merge|split the row"
    r"|dissolve|absorb|extend the (row|span)|shrink the (row|span)|new row"
    r"|move the (seam|cut|boundary)|redraw|span change|re-cut the row",
    re.IGNORECASE)

rulings = []
for fn in sorted(os.listdir(REVIEWS)):
    if not fn.startswith("peer_"):
        continue
    with open(os.path.join(REVIEWS, fn), encoding="utf-8") as f:
        d = json.load(f)
    for r in d.get("rulings", []):
        r2 = dict(r)
        r2["packet"] = fn
        r2["attempt_id"] = d.get("attempt_id")
        rulings.append(r2)

boundary, ordinary, refutes = [], [], []
for r in rulings:
    if r["ruling"] == "refute":
        refutes.append(r)
        continue
    if r["ruling"] not in ("uphold", "refine"):
        continue
    text = (r.get("remedy") or "")
    if BOUNDARY_RE.search(text):
        boundary.append(r)
    else:
        ordinary.append(r)

sev = {}
for r in rulings:
    sev[r.get("severity_final")] = sev.get(r.get("severity_final"), 0) + 1

out = {
    "schema": "isa_peer_work_orders.v1",
    "totals": {"rulings": len(rulings), "boundary_proposals": len(boundary),
               "ordinary_cures": len(ordinary), "refutes": len(refutes),
               "severity_final": sev},
    "boundary_proposals": boundary,
    "refutes": refutes,
    "ordinary_cures": ordinary,
}
dst = os.path.join(SP_ISA, "peer_work_orders.json")
with open(dst, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("wrote", dst)
print(json.dumps(out["totals"], indent=1))
print("--- boundary bucket (row, packet, first 160 chars of remedy):")
for r in boundary:
    print(r["row_id"], r["packet"], "|", (r.get("remedy") or "")[:160].replace("\n", " "))
print("--- refutes:")
for r in refutes:
    print(r["row_id"], r["packet"], "|", (r.get("grounds") or "")[:160].replace("\n", " "))
