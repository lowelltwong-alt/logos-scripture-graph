#!/usr/bin/env python3
"""Phase-0 helper (orchestrator only): adapt the book-agnostic Isa r3 tools
to Jer (lib import + book-token transform). Source is the DURABLE
sp_durable/Isa/tools set - the POST-CYCLE versions carrying the p1-p4
lineage plus the Isa patches i1 (letter-name whitelists), i2 (koh-amar
classifier - book-specific, not copied), i3 (defective-spelling needle
lesson), i4 (ngram7 book/model_id mandated-fixed-value exclusions).
Book-specific tools (citation_sweep, check_language_zones, check_marks,
check_atomic_isolation, TOOLKIT.md, jer_lib, build_*, jer_devices) are
hand-written, not copied. Transforms cover BOTH underscore-literal forms
(Isa_ -> Jer_ AND _Isa -> _Jer) plus the word-boundary forms. After
copying, grep the outputs for stale book-specific prose and fix by hand -
especially OFFSET-ZONE prose: Jer carries ONE zone (chs 8-9 renumbering,
MT 8:23 = WEB 9:1) and NO split - jer_lib's SPLIT_MT = None keeps any
surviving split-aware arm inert, but stale Isa zone claims (63:19, ch 64,
1292/1291, 1QIsa, Isaiah) must not survive in prose."""
import re
from pathlib import Path

SRC = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Isa\tools")
DST = Path(__file__).resolve().parent

MECHANICAL = [
    "check_web_quotes.py", "check_refs_mirror.py", "check_tiling.py",
    "check_universals.py", "ngram7.py",
    "normalize_hebrew_in_json.py", "sweep.py", "run_validator_suite.py",
    "collate.py",
]

for name in MECHANICAL:
    t = (SRC / name).read_text(encoding="utf-8")
    t = t.replace("isa_lib", "jer_lib")
    t = t.replace("Isa_", "Jer_")          # trailing-underscore literal
    t = t.replace("_Isa", "_Jer")          # leading-underscore literal
    t = re.sub(r"\bIsa\b", "Jer", t)
    t = re.sub(r"\bISA\b", "JER", t)
    t = re.sub(r"\bisa\b", "jer", t)
    (DST / name).write_text(t, encoding="utf-8")
    print("adapted", name)
