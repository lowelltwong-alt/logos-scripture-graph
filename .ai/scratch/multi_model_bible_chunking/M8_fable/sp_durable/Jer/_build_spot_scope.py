#!/usr/bin/env python3
"""Build SP/Jer/spot_scope.json for the ONE Jeremiah spot wave (7 lanes) from state: boss-adopted sites
(_apply_author_jer.py SPAN_TARGETS/RETIRES/NEW_ROWS), the one-zone rows (rows_v3 spans touching WEB ch 9),
warrant-touched rows (author apply changed_fields_union with boundary_rationale / strongest_rejected_alternative
/ span changed, plus CWO apply rows) weighted by the peer REFINE set (_refine_rows.json), the B-8 sample
(lf_support_sample.json), and the E-23 flags (_e23_rev.json). Groups rows into scope items of <=6 rows so
every lane has <=8 decisions (items). Digits are the tool's COUNTS. Usage: _build_spot_scope.py"""
import json, re
from pathlib import Path
HERE = Path(__file__).resolve().parent
SC = HERE.parent.parent
rows = [json.loads(l) for l in (HERE / "rows_v3.jsonl").read_text(encoding="utf-8-sig").splitlines() if l.strip()]
ids = [r["decision_id"] for r in rows]
SPAN = re.compile(r"^Jer\.(\d+)\.(\d+)-Jer\.(\d+)\.(\d+)$")
def touches_zone(span):
    m = SPAN.match(span); c1, v1, c2, v2 = map(int, m.groups())
    return any(c == 9 for c in range(c1, c2 + 1))
zone = [r["decision_id"] for r in rows if touches_zone(r["span"])]
au = json.load(open(HERE / "_apply_author_report.json", encoding="utf-8"))
cw = json.load(open(HERE / "_apply_cwo_report.json", encoding="utf-8"))
warrant_fields = {"boundary_rationale", "strongest_rejected_alternative", "span", "unit_type", "confidence"}
au_touched = sorted(r for r, f in au["changed_fields_union"].items() if set(f) & warrant_fields and r in ids)
cw_touched = sorted(r for r, f in cw["changed_fields_union"].items() if set(f) & warrant_fields and r in ids)
refine = set(json.load(open(SC / "_refine_rows.json", encoding="utf-8"))["rows"])
touched = sorted(set(au_touched) | set(cw_touched))
weighted = sorted(touched, key=lambda r: (r not in refine, r))   # REFINE rows first (B3-6)
boss_sites = ["P02-017", "P02-017b", "P03-007", "P03-008", "P06-011", "P10-012", "P10-013", "P14-007", "P18-005", "P18-006", "P18-008", "P18-009"]
def partners(rid):
    if rid not in ids: return []
    i = ids.index(rid); return [x for x in (ids[i - 1] if i > 0 else None, ids[i + 1] if i + 1 < len(ids) else None) if x]
seam_items = []
for s in boss_sites:
    if s in ids:
        seam_items.append({"item": f"seam {s}", "rows": sorted(set([s] + partners(s)), key=ids.index)})
lf = json.load(open(HERE / "lf_support_sample.json", encoding="utf-8"))["sample"]
lf = [r for r in lf if r in ids]
e23 = json.load(open(HERE / "_e23_rev.json", encoding="utf-8"))
e23_rows = sorted({f.get("decision_id") or f.get("row_id") for f in e23.get("flags", []) if (f.get("decision_id") or f.get("row_id")) in ids}, key=ids.index)
def chunk(lst, n):
    return [lst[i:i + n] for i in range(0, len(lst), n)]
half = len(weighted) // 2 + len(weighted) % 2
s3 = weighted[:half]; s4 = weighted[half:]
def items(name, lst, size=6):
    return [{"item": f"{name} group {i + 1}", "rows": g} for i, g in enumerate(chunk(sorted(lst, key=ids.index), size))]
scope = {"schema": "jer_spot_scope.v1", "corpus": "rows_v3.jsonl", "rows_in_corpus": len(rows),
         "lanes": {
             "S1": {"model": "sonnet", "lane": "seam/boss", "items": seam_items[:8], "note": f"{len(seam_items)} boss-adopted sites with neighbours (top 8 by canonical order)"},
             "S2": {"model": "sonnet", "lane": "one-zone", "items": items("zone", zone, 3), "note": f"{len(zone)} rows touch WEB ch 9"},
             "S3": {"model": "opus", "lane": "second-generation (REFINE-weighted, half A)", "items": items("sg", s3, 6)[:8]},
             "S4": {"model": "opus", "lane": "second-generation (REFINE-weighted, half B)", "items": items("sg", s4, 6)[:8]},
             "S5": {"model": "opus", "lane": "B-8 LF-support audit (sample half A)", "items": items("lf", lf[:20], 3)[:8]},
             "S6": {"model": "opus", "lane": "B-8 LF-support audit (sample half B)", "items": items("lf", lf[20:], 3)[:8]},
             "S7": {"model": "opus", "lane": "E-23 punctuation-boundary", "items": items("e23", e23_rows, 4)[:8], "note": f"{len(e23_rows)} rows flagged by the E-23 sweep"}},
         "digits": {"boss_sites": len(seam_items), "zone_rows": len(zone), "warrant_touched_rows": len(touched), "refine_rows_in_touched": len([r for r in touched if r in refine]),
                    "lf_sample": len(lf), "e23_rows": len(e23_rows), "author_touched": len(au_touched), "cwo_touched": len(cw_touched)}}
for k, v in scope["lanes"].items():
    v["rows_total"] = len({r for it in v["items"] for r in it["rows"]}); v["decisions"] = len(v["items"])
(HERE / "spot_scope.json").write_text(json.dumps(scope, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({"digits": scope["digits"], "lanes": {k: {"decisions": v["decisions"], "rows": v["rows_total"]} for k, v in scope["lanes"].items()}}, indent=1))
