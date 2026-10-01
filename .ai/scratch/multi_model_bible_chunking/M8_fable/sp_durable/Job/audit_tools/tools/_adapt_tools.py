#!/usr/bin/env python3
"""Staging helper (orchestrator only): adapt the book-agnostic mechanical
tools to the Job OW-2 AUDIT toolkit (lib import + book-token transform).
Source is the DURABLE sp_durable/Song/tools set — the newest lineage
(Ps -> Prov -> Eccl -> Song, carrying patches p1-p4). Only the AUDIT subset is
adapted: collate.py, sweep.py, normalize_hebrew_in_json.py,
check_web_quotes.py. Book-specific tools (job_lib, build_*) are hand-written.
Transforms include the underscore-literal form (Song_ -> Job_) that the
word-boundary regex misses (recorded lesson). After copying, the outputs are
grepped for stale Song-specific prose and fixed by hand where it would
mislead an auditor.
"""
import re
from pathlib import Path

SRC = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Song\tools")
DST = Path(__file__).resolve().parent

AUDIT_SUBSET = ["collate.py", "sweep.py", "normalize_hebrew_in_json.py", "check_web_quotes.py"]

for name in AUDIT_SUBSET:
    t = (SRC / name).read_text(encoding="utf-8")
    t = t.replace("song_lib", "job_lib")
    t = t.replace("Song_", "Job_")           # underscore forms escape \bSong\b
    t = re.sub(r"\bSong\b", "Job", t)
    t = re.sub(r"\bSONG\b", "JOB", t)
    (DST / name).write_text(t, encoding="utf-8", newline="\n")
    print("adapted", name)
