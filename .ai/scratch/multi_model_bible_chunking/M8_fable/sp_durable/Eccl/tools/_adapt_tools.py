#!/usr/bin/env python3
"""Phase-0 helper (orchestrator only): adapt the book-agnostic Prov r3 tools to
Eccl (lib import + book-token transform). Source is the DURABLE
sp_durable/Prov/tools set — the post-rev-round versions carrying patches
p1 (refs-mirror SKIP_KEYS schema fields), p2 (ngram7 structural-enum
exclusion), p3 (guarded scope-file output path). Book-specific tools
(citation_sweep, check_language_zones, check_marks, check_atomic_isolation,
TOOLKIT.md, eccl_lib, build_*, eccl_devices) are hand-written, not copied.
Transforms include the underscore-literal form (Prov_ -> Eccl_) that the
word-boundary regex missed in the Ps->Prov adaptation (recorded lesson).
After copying, grep the outputs for stale book-specific prose and fix by
hand — especially IDENTITY-ASSUMPTION prose: Eccl is NOT an identity book.
"""
import re
from pathlib import Path

SRC = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Prov\tools")
DST = Path(__file__).resolve().parent

MECHANICAL = [
    "check_web_quotes.py", "check_refs_mirror.py", "check_tiling.py",
    "check_universals.py", "ngram7.py",
    "normalize_hebrew_in_json.py", "sweep.py", "run_validator_suite.py",
    "collate.py",
]

for name in MECHANICAL:
    t = (SRC / name).read_text(encoding="utf-8")
    t = t.replace("prov_lib", "eccl_lib")
    t = t.replace("Prov_", "Eccl_")          # underscore forms escape \bProv\b
    t = re.sub(r"\bProv\b", "Eccl", t)
    t = re.sub(r"\bPROV\b", "ECCL", t)
    (DST / name).write_text(t, encoding="utf-8")
    print("adapted", name)
