#!/usr/bin/env python3
"""Phase-0 helper (orchestrator only): adapt the book-agnostic Song r3 tools
to Isa (lib import + book-token transform). Source is the DURABLE
sp_durable/Song/tools set — the POST-CYCLE versions carrying patches
p1 (refs-mirror SKIP_KEYS schema fields), p2 (ngram7 structural-enum
exclusion), p3 (guarded scope-file output path), and p4 (ngram7
mandated-fixed-value exclusion: wj_or_red_letter_considered + review_status).
Book-specific tools (citation_sweep, check_language_zones, check_marks,
check_atomic_isolation, TOOLKIT.md, isa_lib, build_*, isa_devices) are
hand-written, not copied. Transforms cover BOTH underscore-literal forms
(Song_ -> Isa_ AND _Song -> _Isa — the Ps->Prov trailing-underscore lesson
and its Eccl->Song leading-underscore reverse) plus the lowercase
rule-name/word-boundary forms. After copying, grep the outputs for stale
book-specific prose and fix by hand — especially the OFFSET-ZONE prose:
Isa carries TWO zones with different shapes (ch 8-9 renumbering; the 63:19
SPLIT into WEB 63:19 + 64:1 — web_to_mt is NOT injective here, unlike every
prior book)."""
import re
from pathlib import Path

SRC = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Song\tools")
DST = Path(__file__).resolve().parent

MECHANICAL = [
    "check_web_quotes.py", "check_refs_mirror.py", "check_tiling.py",
    "check_universals.py", "ngram7.py",
    "normalize_hebrew_in_json.py", "sweep.py", "run_validator_suite.py",
    "collate.py",
]

for name in MECHANICAL:
    t = (SRC / name).read_text(encoding="utf-8")
    t = t.replace("song_lib", "isa_lib")
    t = t.replace("Song_", "Isa_")          # trailing-underscore literal
    t = t.replace("_Song", "_Isa")          # leading-underscore literal
    t = re.sub(r"\bSong\b", "Isa", t)
    t = re.sub(r"\bSONG\b", "ISA", t)
    t = re.sub(r"\bsong\b", "isa", t)
    (DST / name).write_text(t, encoding="utf-8")
    print("adapted", name)
