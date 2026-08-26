#!/usr/bin/env python3
"""Phase-0 helper (orchestrator only): adapt the book-agnostic Eccl r3 tools to
Song (lib import + book-token transform). Source is the DURABLE
sp_durable/Eccl/tools set — the POST-CYCLE versions carrying patches
p1 (refs-mirror SKIP_KEYS schema fields), p2 (ngram7 structural-enum
exclusion), p3 (guarded scope-file output path), and p4 (ngram7
mandated-fixed-value exclusion: wj_or_red_letter_considered + review_status).
Book-specific tools (citation_sweep, check_language_zones, check_marks,
check_atomic_isolation, TOOLKIT.md, song_lib, build_*, song_devices) are
hand-written, not copied. Transforms include the underscore-literal form
(Eccl_ -> Song_) that the word-boundary regex missed in the Ps->Prov
adaptation (recorded lesson). After copying, grep the outputs for stale
book-specific prose and fix by hand — especially the OFFSET-ZONE prose:
Song's seam is WEB 6:13 = MT 7:1 (a DIFFERENT shape from Eccl's ch 4/5
split — the extra verse sits at the WEB chapter END, not the MT one).
"""
import re
from pathlib import Path

SRC = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Eccl\tools")
DST = Path(__file__).resolve().parent

MECHANICAL = [
    "check_web_quotes.py", "check_refs_mirror.py", "check_tiling.py",
    "check_universals.py", "ngram7.py",
    "normalize_hebrew_in_json.py", "sweep.py", "run_validator_suite.py",
    "collate.py",
]

for name in MECHANICAL:
    t = (SRC / name).read_text(encoding="utf-8")
    t = t.replace("eccl_lib", "song_lib")
    t = t.replace("Eccl_", "Song_")          # underscore forms escape \bEccl\b
    t = re.sub(r"\bEccl\b", "Song", t)
    t = re.sub(r"\bECCL\b", "SONG", t)
    (DST / name).write_text(t, encoding="utf-8")
    print("adapted", name)
