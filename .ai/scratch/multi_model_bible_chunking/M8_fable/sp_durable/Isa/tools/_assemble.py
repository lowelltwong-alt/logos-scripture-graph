#!/usr/bin/env python3
"""Orchestrator: assemble the combined Isa draft corpus in canonical order
from the 18 writer deliverables, census it, verify id consistency, renumber
chunk_index_in_book canonically (the brief told writers assembly renumbers),
machine-check the R2 frame-seam non-straddle rule, and verify the writer-dir
hygiene inventory. (Phase-2 assembly step.)"""
import collections
import json
import re
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from isa_lib import LAST_VERSE, expand_ref_token

SPBOOK = Path(__file__).resolve().parent.parent
W = SPBOOK / "writer"
PARTS = [f"p{i:02d}" for i in range(1, 19)]

# hygiene inventory: only the 18 deliverables + suite reports may exist
allowed = set()
for p in PARTS:
    allowed.add(f"{p}_rows.jsonl")
    allowed.add(f"{p}_rows.jsonl.validator_report.json")
stray = [p.name for p in W.iterdir() if p.name not in allowed]
assert not stray, f"stray files in writer dir (do NOT delete; investigate): {stray}"

rows = []
per_part_verses = {}
for part in PARTS:
    n = 0
    for l in (W / f"{part}_rows.jsonl").read_text(encoding="utf-8").splitlines():
        if l.strip():
            r = json.loads(l)
            rows.append(r)
            n += len(expand_ref_token(r["span"]))
    per_part_verses[part] = n

# canonical order = span start (WEB); verify it matches part order + renumber
def span_start(r):
    m = re.match(r"^Isa\.(\d+)\.(\d+)-", r["span"])
    return (int(m.group(1)), int(m.group(2)))

assert rows == sorted(rows, key=span_start), "parts are not span-ordered"
for i, r in enumerate(rows, 1):
    r["chunk_index_in_book"] = i

# R2 frame-seam non-straddle machine check
FRAME_STARTS = {(1, 1), (1, 2), (13, 1), (28, 1), (36, 1), (40, 1), (49, 1), (56, 1)}
frame_of = {}
bounds = sorted(FRAME_STARTS)
for r in rows:
    s = span_start(r)
    m = re.match(r"^Isa\.\d+\.\d+-Isa\.(\d+)\.(\d+)$", r["span"])
    e = (int(m.group(1)), int(m.group(2)))
    fs = max(b for b in bounds if b <= s)
    fe = max(b for b in bounds if b <= e)
    assert fs == fe, f"{r['decision_id']} straddles a frame seam: {r['span']}"

combined = SPBOOK / "draft_rows_combined.jsonl"
with combined.open("w", encoding="utf-8", newline="\n") as fh:
    for r in rows:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")

ut = collections.Counter(r["unit_type"] for r in rows)
conf = collections.Counter(r["confidence"] for r in rows)
pc = collections.Counter(r["parent_collection"].split()[0] for r in rows)
parts = collections.Counter(r["writer_part"] for r in rows)
ids_ok = all(r["decision_id"] == r["writer_decision_id"] for r in rows)
ids_unique = len({r["writer_decision_id"] for r in rows}) == len(rows)
ids_upper = all(re.match(r"^P\d{2}-\d{3}$", r["decision_id"]) for r in rows)
print(json.dumps({"rows": len(rows), "verses_total": sum(per_part_verses.values()),
                  "per_part_rows": dict(parts),
                  "per_part_verses": per_part_verses,
                  "unit_type": dict(ut.most_common()),
                  "confidence": dict(conf.most_common()),
                  "parents": dict(pc), "ids_consistent": ids_ok,
                  "ids_unique": ids_unique, "ids_format_ok": ids_upper,
                  "frame_straddle": "none (machine-checked)",
                  "combined": str(combined.name)}, ensure_ascii=False, indent=1))
