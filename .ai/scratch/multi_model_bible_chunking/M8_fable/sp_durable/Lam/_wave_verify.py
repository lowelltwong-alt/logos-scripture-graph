#!/usr/bin/env python3
"""Orchestrator wave verification: per-part tiling + full suite, compact JSON summary.
Usage: _wave_verify.py p01 p02 ... (parts must exist in writer_parts.json)"""
import json
import subprocess
import sys
from pathlib import Path

SP = Path(__file__).resolve().parent
TOOLS = SP / "tools"
parts_doc = json.loads((SP / "writer_parts.json").read_text(encoding="utf-8"))
spans = {p["part"]: (p["span"], p["verses"]) for p in parts_doc["writer_parts"]}

summary = {}
worst_rc = 0
for pid in sys.argv[1:]:
    span, expect_vv = spans[pid]
    f = SP / "writer" / f"writer_{pid}.jsonl"
    if not f.exists():
        summary[pid] = {"status": "MISSING"}
        worst_rc = 1
        continue
    rows = [json.loads(ln) for ln in f.read_text(encoding="utf-8").splitlines() if ln.strip()]
    til = subprocess.run([sys.executable, str(TOOLS / "check_tiling.py"), str(f), "--range", span],
                         capture_output=True, text=True, encoding="utf-8")
    sui = subprocess.run([sys.executable, str(TOOLS / "run_validator_suite.py"), str(f)],
                         capture_output=True, text=True, encoding="utf-8")
    # suite prints a JSON report; extract member statuses
    members = {}
    try:
        rep = json.loads(sui.stdout[sui.stdout.index("{"):])
        members = {k: (v.get("status", v) if isinstance(v, dict) else v)
                   for k, v in rep.items() if not k.startswith("_")}
    except Exception:
        members = {"parse": "UNPARSED", "tail": sui.stdout.strip()[-200:]}
    ok = til.returncode == 0 and sui.returncode == 0
    if not ok:
        worst_rc = 1
    summary[pid] = {"rows": len(rows), "expect_vv": expect_vv,
                    "tiling_exit": til.returncode, "suite_exit": sui.returncode,
                    "members": members, "status": "GREEN" if ok else "RED"}
print(json.dumps(summary, ensure_ascii=False, indent=1))
sys.exit(worst_rc)
