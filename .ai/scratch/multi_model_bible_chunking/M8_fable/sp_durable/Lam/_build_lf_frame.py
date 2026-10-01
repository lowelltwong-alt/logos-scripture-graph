#!/usr/bin/env python3
"""B-8 LF-SUPPORT AUDIT LANE (default from Isa on): rebuild the LF-support frame from the Lam LF primary packets
(reviews/rev_LF_cNN.json, verdict == support), drop rows retired by the author apply (_apply_author_report.json), and
draw the deterministic sample (every Nth of the id-sorted frame; N given, default 2 for the 26-row book) ->
lf_support_sample.json. Digits are the tool's COUNTS. Audited AS SHIPPED at the spot wave. Usage: _build_lf_frame.py [--every 2]"""
import glob, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
A = sys.argv[1:]; EVERY = int(A[A.index("--every") + 1]) if "--every" in A else 2
sup = set()
for f in sorted(glob.glob(str(HERE / "reviews" / "rev_LF_c[0-9][0-9].json"))):
    for it in json.load(open(f, encoding="utf-8-sig"))["items"]:
        if it.get("verdict") == "support": sup.add(it["row_id"])
retired = set()
rep = HERE / "_apply_author_report.json"
if rep.exists(): retired = set(json.load(open(rep, encoding="utf-8")).get("retired", []))
frame = sorted(r for r in sup if r not in retired)
sample = frame[::EVERY]
out = {"schema": "lam_lf_support_sample.v1", "frame_rule": "LF primary verdict == support, retired rows dropped, id-sorted", "frame": frame, "frame_size": len(frame), "retired_dropped": sorted(sup & retired),
       "sample_rule": f"every {EVERY}th of the id-sorted frame from index 0", "sample": sample, "sample_size": len(sample)}
(HERE / "lf_support_sample.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({k: v for k, v in out.items() if k not in ("frame",)}, indent=1))
