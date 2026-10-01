#!/usr/bin/env python3
"""One-shot orchestrator triage of the combined-corpus ngram7 RED."""
import collections
import json
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from pathlib import Path

SPBOOK = Path(__file__).resolve().parent.parent
r = json.loads((SPBOOK / "draft_rows_combined.jsonl.validator_report.json").read_text(encoding="utf-8"))
grams = r["ngram7"]["offending_7grams"]
print("total offending grams:", len(grams))
allrows = set()
for g in grams:
    allrows.update(g["row_ids"])
    print(f"{g['rows']:3d} rows | {g['gram']}")
print("distinct rows across all grams:", len(allrows))
print("by part:", dict(collections.Counter(x.split("-")[0] for x in sorted(allrows))))
