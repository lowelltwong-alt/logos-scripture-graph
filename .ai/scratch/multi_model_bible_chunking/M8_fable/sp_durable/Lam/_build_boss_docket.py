#!/usr/bin/env python3
"""Deterministic boss-docket builder — Lam boss round (m8-mesh-r3; the Jer _build_boss_docket.py shape with a mechanical
item selection instead of a hand list). Consumes remedy_docket.v1.json + draft_rows_combined.jsonl and emits
boss_docket.json (master) + boss_docket_bN.json (per-agent slices, <=8 items each). Item selection (mechanical, recorded):
(a) every uphold/refine remedy whose remedy or grounds carries a boundary marker (PROPOSAL / respan / re-span / merge /
split / retire / new row / boundary change / move the seam) -> a boss adoption item, seam pairs (two rows naming the same
seam) folded into ONE paired item; (b) every peer escalation; (c) every corpus-wide-order candidate -> one CWO
adjudication item (the explicit corpus_wide_orders list, E-18); (d) every sample-lane defect -> a record item; (e) the
round's calibration record. Each item embeds the docket entry, the affected rows and their book-order neighbours.
An optional boss_docket_overrides.json ({"add": [row ids], "drop": [row ids], "pairs": [[rowA, rowB], ...]}) lets the
orchestrator add/drop items with a recorded reason. Usage: _build_boss_docket.py [--per-agent 8]"""
import json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
A = sys.argv[1:]; PER = int(A[A.index("--per-agent") + 1]) if "--per-agent" in A else 8
d = json.load(open(HERE / "remedy_docket.v1.json", encoding="utf-8")); dk = d["docket"]
rows = [json.loads(l) for l in open(HERE / "draft_rows_combined.jsonl", encoding="utf-8") if l.strip()]
by_id = {r["decision_id"]: r for r in rows}; order = [r["decision_id"] for r in rows]; idx = {rid: i for i, rid in enumerate(order)}
ov = json.load(open(HERE / "boss_docket_overrides.json", encoding="utf-8")) if (HERE / "boss_docket_overrides.json").exists() else {"add": [], "drop": [], "pairs": [], "reason": None}
MARK = re.compile(r"\bPROPOSAL\b|\bre-?span\b|\bmerge\b|\bsplit\b|\bretire\b|\bnew row\b|\bboundary change\b|\bmove the seam\b|\bboss adoption\b|\bexplicit boss\b", re.I)
def neigh(rid):
    i = idx[rid]; return [by_id[order[j]] for j in (i - 1, i + 1) if 0 <= j < len(order)]
items = []
prop_rows = [rid for rid, e in dk.items() if e["ruling"] in ("uphold", "refine") and MARK.search((e.get("remedy") or "") + " " + (e.get("grounds") or ""))]
prop_rows = [r for r in prop_rows if r not in ov.get("drop", [])] + [r for r in ov.get("add", []) if r in dk and r not in prop_rows]
paired = set()
for a, b in ov.get("pairs", []):
    if a in prop_rows and b in prop_rows:
        items.append({"kind": "boundary_proposal_pair", "rows": [a, b], "question": f"adopt or decline the seam proposal shared by {a} and {b}", "docket": {a: dk[a], b: dk[b]}, "affected_rows": {r: by_id[r] for r in (a, b)}, "neighbours": {r: neigh(r) for r in (a, b)}}); paired |= {a, b}
for rid in sorted(prop_rows, key=lambda r: idx[r]):
    if rid in paired: continue
    items.append({"kind": "boundary_proposal", "rows": [rid], "question": f"adopt or decline the boundary/respan proposal on {rid}", "docket": {rid: dk[rid]}, "affected_rows": {rid: by_id[rid]}, "neighbours": {rid: neigh(rid)}})
for e in d.get("escalations", []):
    rid = e["row_id"]; items.append({"kind": "escalation", "rows": [rid], "question": f"rule the peer escalation on {rid} (owner-level policy reading contested)", "docket": {rid: dk.get(rid)}, "escalation": e, "affected_rows": {rid: by_id[rid]}, "neighbours": {rid: neigh(rid)}})
if d.get("cwo_candidates_for_orchestrator_adjudication") or d.get("corpus_wide_orders"):
    items.append({"kind": "corpus_wide_orders", "rows": ["corpus_wide"], "question": "adjudicate the explicit corpus_wide_orders list (E-18): confirm/decline every candidate as a numbered CWO with an exact or heuristic arm and its test", "seeded": d.get("corpus_wide_orders", []), "candidates": d.get("cwo_candidates_for_orchestrator_adjudication", [])})
for sd in d.get("sample_lane_defects", []):
    rid = sd["row_id"]; items.append({"kind": "sample_defect_record", "rows": [rid], "question": f"record the sample-lane defect on the supported row {rid} as a work order", "sample_defect": sd, "affected_rows": {rid: by_id[rid]}, "neighbours": {rid: neigh(rid)}})
items.append({"kind": "calibration_record", "rows": ["record"], "question": "record the round's calibration: rulings by verdict, lens divergence, severity histogram", "totals": d["totals"]})
slices = [items[i:i + PER] for i in range(0, len(items), PER)]
for n, sl in enumerate(slices, 1):
    for k, it in enumerate(sl, 1): it["item_id"] = it["id"] = f"B{n}-{k}"   # ruling ids == item ids, in slice order (the _boss_verify.py contract)
master = {"schema": "lam_boss_docket.v1", "selection_basis": "mechanical (see the builder docstring)", "overrides": ov, "items_total": len(items), "kinds": {k: sum(1 for it in items if it["kind"] == k) for k in sorted({it["kind"] for it in items})}, "agents": {}, "items": items}
for n, sl in enumerate(slices, 1):
    ag = f"b{n}"; doc = {"schema": "lam_boss_docket_slice.v1", "agent": ag, "attempt_id": f"lam_boss_{ag}_a1", "output_file": f"reviews/boss_lam_{ag}.json", "item_ids": [it["id"] for it in sl], "items": sl}
    (HERE / f"boss_docket_{ag}.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    master["agents"][ag] = {"items": [it["id"] for it in sl], "output_file": doc["output_file"]}
(HERE / "boss_docket.json").write_text(json.dumps(master, ensure_ascii=False, indent=1), encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8"); print(json.dumps({k: v for k, v in master.items() if k != "items"}, ensure_ascii=False, indent=1))
