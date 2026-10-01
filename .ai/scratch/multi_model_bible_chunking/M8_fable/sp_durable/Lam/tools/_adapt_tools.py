#!/usr/bin/env python3
"""Phase-0 helper (orchestrator only): adapt the book-agnostic r3 mechanical tools from the DURABLE
sp_durable/Jer/tools set (post-cycle, carrying the Isa i1-i4 lineage + the Jer E-01/E-02/E-15/E-16
upgrades) to Lam (lib import + book-token transform, BOTH underscore-literal forms + word-boundary
forms). Book-specific tools (citation_sweep, check_language_zones, check_marks, check_atomic_isolation,
cap_sweep, check_register, _punct_boundary_sweep, TOOLKIT.md, lam_lib, build_*, lam_devices) are
hand-adapted, not blindly copied. After copying, grep the outputs for stale Jer prose (zone, island,
8:23, 9:1, 1364, Jeremiah) and fix by hand."""
import re
from pathlib import Path
SRC = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Jer\tools")
DST = Path(__file__).resolve().parent
MECHANICAL = ["check_web_quotes.py", "check_refs_mirror.py", "check_tiling.py", "check_universals.py", "ngram7.py",
              "normalize_hebrew_in_json.py", "sweep.py", "run_validator_suite.py", "collate.py"]
for name in MECHANICAL:
    t = (SRC / name).read_text(encoding="utf-8-sig")
    t = t.replace("jer_lib", "lam_lib").replace("Jer_", "Lam_").replace("_Jer", "_Lam")
    t = re.sub(r"\bJer\b", "Lam", t); t = re.sub(r"\bJER\b", "LAM", t); t = re.sub(r"\bjer\b", "lam", t)
    (DST / name).write_text(t, encoding="utf-8")
    print("adapted", name)
