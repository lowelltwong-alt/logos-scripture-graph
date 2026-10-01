#!/usr/bin/env python3
"""FINALIZE pass (deterministic, orchestrator): rows_v4 -> rows_v5 with review_status set to
candidate_review_complete on every row (the Isa close convention; no other field touched); then the validator
suite over rows_v5 and the E-23 sweep (-> _e23_post.json). Pins rows_v4 by sha16 given on the command line.
Usage: _finalize.py <rows_v4_sha16>"""
import hashlib, json, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
raw = (HERE / "rows_v4.jsonl").read_bytes(); s16 = hashlib.sha256(raw).hexdigest()[:16]
assert len(sys.argv) > 1 and s16 == sys.argv[1], f"rows_v4 sha {s16} != {sys.argv[1:]}"
rows = [json.loads(l) for l in raw.decode("utf-8").splitlines() if l.strip()]
assert len(rows) == 275 and [r["chunk_index_in_book"] for r in rows] == list(range(1, 276))
changed = 0
for r in rows:
    if r["review_status"] != "candidate_review_complete": r["review_status"] = "candidate_review_complete"; changed += 1
out = HERE / "rows_v5.jsonl"
out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8", newline="\n")
sha5 = hashlib.sha256(out.read_bytes()).hexdigest()
suite = json.loads(subprocess.run([sys.executable, "tools/run_validator_suite.py", "rows_v5.jsonl"], capture_output=True, text=True, encoding="utf-8", cwd=str(HERE)).stdout)
e23 = json.loads(subprocess.run([sys.executable, "tools/_punct_boundary_sweep.py", "rows_v5.jsonl"], capture_output=True, text=True, encoding="utf-8", cwd=str(HERE)).stdout)
(HERE / "_e23_post.json").write_text(json.dumps(e23, ensure_ascii=False, indent=1), encoding="utf-8")
til = subprocess.run([sys.executable, "tools/check_tiling.py", "rows_v5.jsonl", "--range", "Jer.1.1-Jer.52.34"], capture_output=True, text=True, encoding="utf-8", cwd=str(HERE))
print(json.dumps({"rows": len(rows), "review_status_set": changed, "rows_v5_sha256": sha5, "suite": {k: suite.get(k) for k in ("hard_status", "nfd_hard_e01", "triage_flags", "per_check")}, "e23": {"rows_checked": e23.get("rows_checked"), "flag_count": e23.get("flag_count")}, "tiling": "GREEN" if til.returncode == 0 else "RED"}, ensure_ascii=False, indent=1))
