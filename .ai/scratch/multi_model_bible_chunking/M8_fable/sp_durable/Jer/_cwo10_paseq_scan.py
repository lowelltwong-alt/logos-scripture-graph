#!/usr/bin/env python3
"""CWO-10 (spot-wave corpus-wide order, S5 finding on P05-014/P07-001/P07-012; E-18: executed as its OWN sweep): every row
whose WEB span covers a verse carrying a paseq seg (pmarks, MT keys via the crosswalk) must disclose the paseq (count-only,
single-witness) somewhere in its prose. Deterministic scan: rows with in-span paseq verses and NO 'paseq' token in any string
field = candidates (exact arm). Prints the COUNT + the row list; writes _cwo10_paseq_scan.json. Usage: _cwo10_paseq_scan.py rows.jsonl"""
import json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "tools"))
from jer_lib import expand_ref_token, web_to_mt, load_pmarks
pm = load_pmarks(); paseq = pm["paseq"]
rows = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8-sig") if l.strip()]
def prose(r):
    parts = []
    def walk(o):
        if isinstance(o, dict): [walk(v) for k, v in o.items() if k != "boundary_evidence_refs"]
        elif isinstance(o, list): [walk(v) for v in o]
        elif isinstance(o, str): parts.append(o)
    walk(r); return "\n".join(parts) + "\n" + "\n".join(r.get("boundary_evidence_refs", []))
cands, covered = [], 0
for r in rows:
    mt_hits = []
    for c, v in expand_ref_token(r["span"]):
        mt = web_to_mt(c, v)
        if mt and paseq.get(f"Jer.{mt[0]}.{mt[1]}"): mt_hits.append(f"Jer.{mt[0]}.{mt[1]}")
    if not mt_hits: continue
    covered += 1
    if not re.search(r"\bpaseq\b", prose(r), re.I):
        cands.append({"row_id": r["decision_id"], "span": r["span"], "in_span_paseq_mt_keys": mt_hits, "paseq_count": sum(paseq[k] for k in mt_hits)})
out = {"order": "CWO-10", "arm": "exact", "object": "rows whose span covers a paseq verse (MT keys via crosswalk) with no paseq disclosure in any prose field", "rows_covering_paseq_verses": covered, "candidates": len(cands), "rows": cands}
(HERE / "_cwo10_paseq_scan.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=1)); print([c["row_id"] for c in cands])
