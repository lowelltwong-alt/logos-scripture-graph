"""B-8 cure: deterministic supported-row sample from the LF-SUPPORT column.

Frame = every row LF marked support across reviews/c*_LF.json (expected 155).
Draw every 5th of the id-sorted frame (n=31, 20.0%) — a size that sustains a
reliability statement. Writes lf_support_sample.json. Run from SP/Isa.
"""
import json, glob

support = set()
for f in sorted(glob.glob("reviews/c*_LF.json")):
    pkt = json.load(open(f, encoding="utf-8"))
    items = pkt.get("items") or pkt.get("reviews") or pkt.get("rows") or []
    if isinstance(items, dict):
        items = [dict(v, row_id=k) for k, v in items.items()]
    for it in items:
        rid = it.get("row_id") or it.get("writer_decision_id") or it.get("decision_id")
        verdict = (it.get("verdict") or it.get("ruling") or "").lower()
        if rid and verdict == "support":
            support.add(rid)
frame = sorted(support)
sample = frame[::5]
out = {"schema": "isa_lf_support_sample.v1", "frame_object": "rows LF verdict=support",
       "frame_size": len(frame), "rule": "every 5th of id-sorted frame",
       "sample_size": len(sample), "sample": sample}
with open("lf_support_sample.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print(json.dumps({k: out[k] for k in ("frame_size", "sample_size")}, indent=1))
print("first/last:", sample[:3], sample[-3:] if sample else [])
