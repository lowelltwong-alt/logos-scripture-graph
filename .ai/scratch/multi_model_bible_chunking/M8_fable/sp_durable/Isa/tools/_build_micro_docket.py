"""Consolidate spot-wave findings into the micro-round docket. Run from SP/Isa."""
import json, glob, collections

docket = []
for f in sorted(glob.glob("reviews/spot_s*.json")):
    p = json.load(open(f, encoding="utf-8"))
    lane = p.get("lane") or f
    for fd in p.get("findings", []):
        rows = fd.get("row_id") or fd.get("row_ids") or fd.get("rows") or "?"
        if isinstance(rows, str):
            rows = [rows]
        docket.append({
            "lane": str(lane)[:28], "rows": rows,
            "sev": str(fd.get("severity", "?")),
            "cls": str(fd.get("E-class") or fd.get("e_class") or fd.get("class") or "?"),
            "text": str(fd.get("summary") or fd.get("defect") or fd.get("exact_defective_text") or "")[:110],
            "cure": str(fd.get("proposed_cure") or fd.get("cure") or "")[:160],
        })
by_row = collections.defaultdict(list)
for d in docket:
    for r in d["rows"]:
        by_row[r].append(d)
out = {"schema": "isa_micro_docket.v1", "total_findings": len(docket),
       "distinct_rows": len(by_row),
       "by_row": {r: by_row[r] for r in sorted(by_row)}}
with open("micro_docket.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("findings:", len(docket), "| distinct rows:", len(by_row))
for r in sorted(by_row):
    for d in by_row[r]:
        print(r, "|", d["sev"][:6].ljust(6), "|", d["cls"][:16].ljust(16), "|", (d["cure"] or d["text"])[:120])
