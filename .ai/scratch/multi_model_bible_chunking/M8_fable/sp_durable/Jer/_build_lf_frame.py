#!/usr/bin/env python3
"""B-8 LF-SUPPORT AUDIT LANE (default from Isa on): rebuild the LF-support frame from the Jer LF primary packets
(sp_durable/Jer/reviews/rev_LF_cNN.json, verdict == support), drop rows retired by the author apply, and draw the
deterministic sample (every 5th of the id-sorted frame, the Isa rule) -> SP/Jer/lf_support_sample.json.
Digits are the tool's COUNTS. Audited AS SHIPPED at the spot wave (rows_v3 after the CWO apply)."""
import glob, json, os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
REV = M8 / "sp_durable" / "Jer" / "reviews"
RETIRED = {"P06-012", "P14-008"}
support, challenge = [], []
pk = sorted(REV.glob("rev_LF_c*.json"))
for f in pk:
    d = json.load(open(f, encoding="utf-8"))
    for it in d["items"]:
        (support if it.get("verdict") == "support" else challenge).append(it["row_id"])
frame = sorted(set(support) - RETIRED)
sample = frame[::5]
out = {"schema": "jer_lf_support_sample.v1", "frame_object": "rows LF verdict=support (35 LF primary packets, 276 pre-apply rows), retired rows dropped",
       "lf_packets": len(pk), "support_verdicts": len(support), "challenge_verdicts": len(challenge), "retired_dropped": sorted(set(support) & RETIRED),
       "frame_size": len(frame), "rule": "every 5th of id-sorted frame", "sample_size": len(sample), "sample": sample, "frame": frame}
(HERE / "lf_support_sample.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({k: v for k, v in out.items() if k not in ("frame", "sample")}, ensure_ascii=False, indent=1)); print("sample:", sample)
