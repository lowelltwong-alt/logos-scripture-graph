#!/usr/bin/env python3
"""Orchestrator: assemble the combined Song draft corpus in canonical order
from the two writer deliverables, census it, verify id consistency and the
writer-dir hygiene inventory. (Phase-2 assembly step.)"""
import collections
import json
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from pathlib import Path

SPBOOK = Path(__file__).resolve().parent.parent
W = SPBOOK / "writer"

# hygiene inventory: only the two deliverables + suite reports may exist
allowed = {"p01_rows.jsonl", "p02_rows.jsonl",
           "p01_rows.jsonl.validator_report.json",
           "p02_rows.jsonl.validator_report.json"}
stray = [p.name for p in W.iterdir() if p.name not in allowed]
assert not stray, f"stray files in writer dir (do NOT delete; investigate): {stray}"

rows = []
for part in ("p01", "p02"):
    for l in (W / f"{part}_rows.jsonl").read_text(encoding="utf-8").splitlines():
        if l.strip():
            rows.append(json.loads(l))
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
print(json.dumps({"rows": len(rows), "per_part": dict(parts),
                  "unit_type": dict(ut.most_common()),
                  "confidence": dict(conf.most_common()),
                  "parents": dict(pc), "ids_consistent": ids_ok,
                  "ids_unique": ids_unique,
                  "combined": str(combined.name)}, ensure_ascii=False, indent=1))
