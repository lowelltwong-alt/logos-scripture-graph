#!/usr/bin/env python3
"""Expected-manifest stray sweep for SP/REPAIR (E-21 standing wave-close gate; allowlist-based;
interpreter pycache excluded). Prints CLEAN or STRAYS_FOUND with the paths."""
import fnmatch
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REP = HERE.parent / "REPAIR"
ALLOW = [
    "*/orders_rep_*.json", "*/repair_*_[0-9][0-9].jsonl", "*/repair_*_r[2-9]*.jsonl", "*/REPAIR_BRIEF_*.md",
    "*/semcheck_*.json", "*/semcheck_slices/slice_*.json", "SEMCHECK_BRIEF.md",
    "*/repair_attempt_receipts.jsonl", "*/semcheck_attempt_receipts.jsonl",
]
strays = []
n = 0
for p in sorted(REP.rglob("*")):
    if p.is_dir() or "__pycache__" in p.parts:
        continue
    n += 1
    rel = p.relative_to(REP).as_posix()
    if not any(fnmatch.fnmatch(rel, pat) for pat in ALLOW):
        strays.append({"path": rel, "bytes": p.stat().st_size})
print(json.dumps({"sweep": "CLEAN" if not strays else "STRAYS_FOUND", "files_checked": n, "strays": strays}, indent=1))
raise SystemExit(1 if strays else 0)
