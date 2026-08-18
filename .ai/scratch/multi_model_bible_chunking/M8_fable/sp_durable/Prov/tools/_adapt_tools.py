#!/usr/bin/env python3
"""Phase-0 helper (orchestrator only): adapt the book-agnostic Ps r3 tools to
Prov (lib import + book-token transform). Source is SP/Ps/tools — the
REV-ROUND-UPGRADED versions (prev/ holds pre-upgrade; NOT used). Book-specific
tools (citation_sweep, check_language_zones, check_marks, TOOLKIT.md,
prov_lib, build_*, prov_devices) are hand-written, not copied. After copying,
grep the outputs for stale psalm-specific prose and fix by hand."""
import re
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent.parent / "Ps" / "tools"
DST = Path(__file__).resolve().parent

MECHANICAL = [
    "check_web_quotes.py", "check_refs_mirror.py", "check_tiling.py",
    "check_universals.py", "ngram7.py",
    "normalize_hebrew_in_json.py", "sweep.py", "run_validator_suite.py",
    "collate.py",
]

for name in MECHANICAL:
    t = (SRC / name).read_text(encoding="utf-8")
    t = t.replace("ps_lib", "prov_lib")
    t = re.sub(r"\bPs\b", "Prov", t)
    t = re.sub(r"\bPS\b", "PROV", t)
    (DST / name).write_text(t, encoding="utf-8")
    print("adapted", name)
