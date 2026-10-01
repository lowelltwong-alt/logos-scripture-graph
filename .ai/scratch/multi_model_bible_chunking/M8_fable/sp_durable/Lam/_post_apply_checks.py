#!/usr/bin/env python3
"""Post-apply checks over a finalized corpus version (orchestrator, deterministic): the validator suite (report lands
beside the file), the E-23 punctuation-boundary sweep (-> _e23_post_<tag>.json), whole-book tiling, and the review_status
invariant (candidate_review_complete on every row). Usage: _post_apply_checks.py rows_v6.jsonl v6"""
import hashlib, json, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
name, tag = sys.argv[1], sys.argv[2]
raw = (HERE / name).read_bytes(); rows = [json.loads(l) for l in raw.decode("utf-8").splitlines() if l.strip()]
assert [r["chunk_index_in_book"] for r in rows] == list(range(1, len(rows) + 1))
rs = sum(1 for r in rows if r["review_status"] != "candidate_review_complete")
suite = json.loads(subprocess.run([sys.executable, "tools/run_validator_suite.py", name], capture_output=True, text=True, encoding="utf-8", cwd=str(HERE)).stdout)
e23 = json.loads(subprocess.run([sys.executable, "tools/_punct_boundary_sweep.py", name], capture_output=True, text=True, encoding="utf-8", cwd=str(HERE)).stdout)
(HERE / f"_e23_post_{tag}.json").write_text(json.dumps(e23, ensure_ascii=False, indent=1), encoding="utf-8")
til = subprocess.run([sys.executable, "tools/check_tiling.py", name, "--range", "Lam.1.1-Lam.5.22"], capture_output=True, text=True, encoding="utf-8", cwd=str(HERE))
out = {"corpus": name, "sha256": hashlib.sha256(raw).hexdigest(), "rows": len(rows), "review_status_not_complete": rs, "suite": {k: suite.get(k) for k in ("hard_status", "nfd_hard_e01", "triage_flags", "per_check")},
       "e23": {"rows_checked": e23.get("rows_checked"), "flag_count": e23.get("flag_count")}, "tiling": "GREEN" if til.returncode == 0 else "RED"}
sys.stdout.reconfigure(encoding="utf-8"); print(json.dumps(out, ensure_ascii=False, indent=1))
sys.exit(0 if (rs == 0 and suite.get("hard_status") == "GREEN" and til.returncode == 0) else 1)
