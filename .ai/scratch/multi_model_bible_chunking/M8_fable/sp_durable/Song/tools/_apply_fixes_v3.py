#!/usr/bin/env python3
"""Orchestrator: apply micro-fix edit files (all _op:replace) over rows_v2 ->
SP/Song/rows_v3.jsonl. Verifies targets exist, no duplicate edits, no
dropped fields, spans byte-identical to rows_v2 (micro-fixes never move
boundaries)."""
import json
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from pathlib import Path

SPBOOK = Path(__file__).resolve().parent.parent

rows = [json.loads(l) for l in (SPBOOK / "rows_v2.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
by_id = {r["writer_decision_id"]: i for i, r in enumerate(rows)}

applied = set()
for name in ("p01_fixes.jsonl", "p02_fixes.jsonl"):
    f = SPBOOK / "author" / name
    for l in f.read_text(encoding="utf-8").splitlines():
        if not l.strip():
            continue
        e = json.loads(l)
        op = e.pop("_op")
        assert op == "replace", f"unexpected op {op} in micro-fix ({name})"
        wid = e["writer_decision_id"]
        assert wid in by_id, f"fix targets unknown row {wid}"
        assert wid not in applied, f"duplicate fix for {wid}"
        assert e["span"] == rows[by_id[wid]]["span"], \
            f"{wid} micro-fix moved the span: {rows[by_id[wid]]['span']!r} -> {e['span']!r}"
        missing = set(rows[by_id[wid]].keys()) - set(e.keys())
        assert not missing, f"{wid} replacement drops fields: {missing}"
        applied.add(wid)
        rows[by_id[wid]] = e

out = SPBOOK / "rows_v3.jsonl"
with out.open("w", encoding="utf-8", newline="\n") as fh:
    for r in rows:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
print(json.dumps({"rows": len(rows), "fixed": sorted(applied),
                  "fixed_count": len(applied), "out": out.name}, indent=1))
