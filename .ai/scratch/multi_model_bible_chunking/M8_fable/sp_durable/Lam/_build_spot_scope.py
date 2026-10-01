#!/usr/bin/env python3
"""Build SP/Lam/spot_scope.json for the ONE Lamentations spot wave (5 lanes per SPOT_BRIEF.md) from state: boss-adopted
sites (author_overrides.json span_targets/retires/new_rows), every cross-part / poem seam pair, the acrostic rows (chs 1-4)
+ the ch-5 rows, warrant-touched rows (_apply_author_report.json changed_fields_union with boundary_rationale /
strongest_rejected_alternative / span changed, plus the CWO apply rows where present) weighted by the peer REFINE set
(remedy_docket.v1.json), the B-8 sample (lf_support_sample.json), and the E-23 flags (the _e23 file given). Groups rows
into scope items of <=6 rows so every lane has <=8 decisions. Digits are the tool's COUNTS.
Usage: _build_spot_scope.py --corpus rows_v3.jsonl --e23 _e23_rev.json"""
import json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
A = sys.argv[1:]; CORPUS = A[A.index("--corpus") + 1] if "--corpus" in A else "rows_v3.jsonl"; E23 = A[A.index("--e23") + 1] if "--e23" in A else "_e23_rev.json"
rows = [json.loads(l) for l in (HERE / CORPUS).read_text(encoding="utf-8-sig").splitlines() if l.strip()]
ids = [r["decision_id"] for r in rows]; idx = {rid: i for i, rid in enumerate(ids)}
SPAN = re.compile(r"^Lam\.(\d+)\.(\d+)-Lam\.(\d+)\.(\d+)$")
def ch(r): m = SPAN.match(r["span"]); return int(m.group(1)), int(m.group(3))
ov = json.load(open(HERE / "author_overrides.json", encoding="utf-8")) if (HERE / "author_overrides.json").exists() else {}
boss_sites = sorted(set(ov.get("span_targets", {})) | set(ov.get("retires", {})) | set(ov.get("new_rows", {})))
apply = json.load(open(HERE / "_apply_author_report.json", encoding="utf-8")) if (HERE / "_apply_author_report.json").exists() else {"changed_fields_union": {}}
touched = sorted(r for r, c in apply.get("changed_fields_union", {}).items() if any(k in c for k in ("boundary_rationale", "strongest_rejected_alternative", "span", "device_notes")) and r in idx)
cwo_rep = HERE / "_apply_cwo_report.json"
if cwo_rep.exists(): touched = sorted(set(touched) | {r for r in json.load(open(cwo_rep, encoding="utf-8")).get("changed_fields_union", {}) if r in idx})
dk = json.load(open(HERE / "remedy_docket.v1.json", encoding="utf-8"))["docket"]
refine = sorted(r for r, e in dk.items() if e["ruling"] == "refine" and r in idx)
lf = json.load(open(HERE / "lf_support_sample.json", encoding="utf-8")); sample = [r for r in lf["sample"] if r in idx]
e23 = json.load(open(HERE / E23, encoding="utf-8-sig")); e23_rows = sorted({f.get("row_id") or f.get("decision_id") for f in e23.get("flags", []) if (f.get("row_id") or f.get("decision_id")) in idx})
# seam pairs: every adjacent pair across a poem seam or a writer-part seam, plus boss sites with their neighbours
def neigh(rid): i = idx[rid]; return [ids[j] for j in (i - 1, i + 1) if 0 <= j < len(ids)]
poem_pairs = []
for i in range(len(rows) - 1):
    a, b = rows[i], rows[i + 1]
    if ch(a)[1] != ch(b)[0] or a["writer_part"] != b["writer_part"]: poem_pairs.append([a["decision_id"], b["decision_id"]])
s1_items = [{"item": f"boss site {r} + neighbours", "rows": sorted({r, *neigh(r)}, key=lambda x: idx[x])} for r in boss_sites] + [{"item": f"seam pair {a}|{b}", "rows": [a, b]} for a, b in poem_pairs]
acro = [r["decision_id"] for r in rows if ch(r)[0] <= 4]; ch5 = [r["decision_id"] for r in rows if ch(r)[0] == 5]
def chunk(lst, n): return [lst[i:i + n] for i in range(0, len(lst), n)]
s2_items = [{"item": f"acrostic rows group {k + 1}", "rows": g} for k, g in enumerate(chunk(acro, 6))] + ([{"item": "ch-5 discourse-seam rows", "rows": ch5}] if ch5 else [])
weighted = sorted(set(touched) | set(refine), key=lambda x: idx[x])
s3_items = [{"item": f"warrant-touched rows group {k + 1} (REFINE-weighted)", "rows": g} for k, g in enumerate(chunk(weighted, 6))]
s4_items = [{"item": f"B-8 LF-support sample group {k + 1}", "rows": g} for k, g in enumerate(chunk(sample, 6))]
s5_items = [{"item": f"E-23 flagged rows group {k + 1}", "rows": g} for k, g in enumerate(chunk(e23_rows, 6))] or [{"item": "E-23: zero flags over the corpus - confirm the sweep's null result over every seam argument", "rows": ids[:6]}]
lanes = {"S1": {"lane": "seam/boss lane", "model": "sonnet", "items": s1_items}, "S2": {"lane": "acrostic-boundary lane", "model": "sonnet", "items": s2_items},
         "S3": {"lane": "second-generation lane (REFINE-weighted)", "model": "opus", "items": s3_items}, "S4": {"lane": "B-8 LF-support audit lane", "model": "opus", "items": s4_items}, "S5": {"lane": "E-23 punctuation lane", "model": "opus", "items": s5_items}}
for sn, l in lanes.items():
    assert len(l["items"]) <= 8, f"{sn} has {len(l['items'])} decisions (> 8)"
    l["decisions"] = len(l["items"]); l["rows_total"] = len({r for it in l["items"] for r in it["rows"]})
out = {"schema": "lam_spot_scope.v1", "corpus": CORPUS, "sources": {"boss_sites": boss_sites, "poem_or_part_seam_pairs": poem_pairs, "warrant_touched": touched, "refine_rows": refine, "lf_sample": sample, "e23_rows": e23_rows}, "lanes": lanes}
(HERE / "spot_scope.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({sn: {"decisions": l["decisions"], "rows": l["rows_total"], "model": l["model"]} for sn, l in lanes.items()}, indent=1))
