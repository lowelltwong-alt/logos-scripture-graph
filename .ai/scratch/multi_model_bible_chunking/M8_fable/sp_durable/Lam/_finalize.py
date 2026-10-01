#!/usr/bin/env python3
"""FINALIZE pass (deterministic, orchestrator): rows_v4 -> rows_v5 with review_status set to
candidate_review_complete on every row (the Isa close convention; no other field touched); then the validator
suite over rows_v5 and the E-23 sweep (-> _e23_post.json). Pins rows_v4 by sha16 given on the command line.
Usage: _finalize.py <src_sha16> [--src rows_v4.jsonl --dst rows_v5.jsonl]  (Lam build; row count read from the file)"""
import hashlib, json, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
A = sys.argv[1:]; SRC = A[A.index("--src") + 1] if "--src" in A else "rows_v4.jsonl"; DST = A[A.index("--dst") + 1] if "--dst" in A else "rows_v5.jsonl"
raw = (HERE / SRC).read_bytes(); s16 = hashlib.sha256(raw).hexdigest()[:16]
assert s16 == A[0], f"{SRC} sha {s16} != {A[0]}"
rows = [json.loads(l) for l in raw.decode("utf-8").splitlines() if l.strip()]
assert [r["chunk_index_in_book"] for r in rows] == list(range(1, len(rows) + 1))
changed = 0
for r in rows:
    if r["review_status"] != "candidate_review_complete": r["review_status"] = "candidate_review_complete"; changed += 1
out = HERE / DST
out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8", newline="\n")
sha5 = hashlib.sha256(out.read_bytes()).hexdigest()
suite = json.loads(subprocess.run([sys.executable, "tools/run_validator_suite.py", DST], capture_output=True, text=True, encoding="utf-8", cwd=str(HERE)).stdout)
e23 = json.loads(subprocess.run([sys.executable, "tools/_punct_boundary_sweep.py", DST], capture_output=True, text=True, encoding="utf-8", cwd=str(HERE)).stdout)
(HERE / "_e23_post.json").write_text(json.dumps(e23, ensure_ascii=False, indent=1), encoding="utf-8")
til = subprocess.run([sys.executable, "tools/check_tiling.py", DST, "--range", "Lam.1.1-Lam.5.22"], capture_output=True, text=True, encoding="utf-8", cwd=str(HERE))
print(json.dumps({"rows": len(rows), "review_status_set": changed, "rows_v5_sha256": sha5, "suite": {k: suite.get(k) for k in ("hard_status", "nfd_hard_e01", "triage_flags", "per_check")}, "e23": {"rows_checked": e23.get("rows_checked"), "flag_count": e23.get("flag_count")}, "tiling": "GREEN" if til.returncode == 0 else "RED"}, ensure_ascii=False, indent=1))
