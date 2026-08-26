#!/usr/bin/env python3
"""Orchestrator: apply author phase-1 edit files (all _op:replace) over the
Song draft corpus -> SP/Song/rows_v1.jsonl. Verifies every edit targets an
existing writer_decision_id, no duplicate edits, no dropped fields, and that
no boss-pending row was touched."""
import json
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from pathlib import Path

SPBOOK = Path(__file__).resolve().parent.parent
BOSS_PENDING = {"P02-006", "P02-013", "P02-015", "P02-016", "P02-017", "P02-018"}

rows = [json.loads(l) for l in (SPBOOK / "draft_rows_combined.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
by_id = {r["writer_decision_id"]: i for i, r in enumerate(rows)}
assert len(by_id) == len(rows), "duplicate ids in draft corpus"

applied = {}
ops = {"replace": 0, "retire": 0, "add": 0}
for part in ("p01", "p02"):
    f = SPBOOK / "author" / f"{part}_edits.jsonl"
    for l in f.read_text(encoding="utf-8").splitlines():
        if not l.strip():
            continue
        e = json.loads(l)
        op = e.pop("_op")
        ops[op] += 1
        assert op == "replace", f"unexpected op {op} in phase 1 ({part})"
        wid = e["writer_decision_id"]
        assert wid in by_id, f"edit targets unknown row {wid}"
        assert wid not in applied, f"duplicate edit for {wid}"
        assert wid not in BOSS_PENDING, f"phase-1 edit touched boss-pending row {wid}"
        missing = set(rows[by_id[wid]].keys()) - set(e.keys())
        assert not missing, f"{wid} replacement drops fields: {missing}"
        applied[wid] = True
        rows[by_id[wid]] = e

out = SPBOOK / "rows_v1.jsonl"
with out.open("w", encoding="utf-8", newline="\n") as fh:
    for r in rows:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
print(json.dumps({"rows": len(rows), "ops": ops, "replaced_unique": len(applied),
                  "out": out.name}, indent=1))
