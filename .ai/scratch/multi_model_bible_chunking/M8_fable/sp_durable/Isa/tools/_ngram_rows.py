#!/usr/bin/env python3
"""One-shot: full affected-row lists for the two genuine convergence
families (parashah-disclosure sentence; set-aside connective)."""
import collections
import json
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from pathlib import Path

SPBOOK = Path(__file__).resolve().parent.parent
r = json.loads((SPBOOK / "draft_rows_combined.jsonl.validator_report.json").read_text(encoding="utf-8"))
para = set()
aside = set()
for g in r["ngram7"]["offending_7grams"]:
    if "parashah" in g["gram"] or "witness sits" in g["gram"] or "immediately before" in g["gram"]:
        para.update(g["row_ids"])
    elif "set aside" in g["gram"]:
        aside.update(g["row_ids"])
print(json.dumps({
    "parashah_family_rows": sorted(para),
    "parashah_by_part": dict(collections.Counter(x.split("-")[0] for x in para)),
    "aside_family_rows": sorted(aside),
    "aside_by_part": dict(collections.Counter(x.split("-")[0] for x in aside)),
    "union": len(para | aside)}, indent=1))
