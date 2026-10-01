"""PC-1 pattern census over a rows file. Usage: python tools/_pc1_census.py rows_v4.jsonl"""
import json, re, sys

pats = [r"(preceding|previous|next|following|earlier|adjacent|neighboring|opening|final)\s+row",
        r"row\s+(before|after)", r"this\s+part\b", r"this\s+part's",
        r"the\s+part's\s+own", r"its\s+assigned\s+span"]
rows = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8")]
hits = []
for r in rows:
    for f in ("boundary_rationale", "device_notes", "strongest_rejected_alternative"):
        t = str(r.get(f, ""))
        for p in pats:
            for m in re.finditer(p, t, re.I):
                hits.append((r["writer_decision_id"], f, m.group(0)))
print("total pattern hits:", len(hits))
for h in hits:
    print("-", h)
