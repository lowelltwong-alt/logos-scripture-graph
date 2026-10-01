#!/usr/bin/env python3
"""Orchestrator: apply the two variation-sweep edit files to the combined
corpus under HARD GUARDS (Song _apply_edits lineage): the edit set must equal
the expected 31-row set exactly; every replacement may differ from its
original ONLY in boundary_rationale / strongest_rejected_alternative /
device_notes; span, refs, and every other field must be byte-identical."""
import json
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from pathlib import Path

SPBOOK = Path(__file__).resolve().parent.parent
EXPECTED_A = {"P09-001", "P09-002", "P09-004", "P09-005", "P09-006", "P09-007",
              "P10-001", "P10-004", "P10-005", "P10-009", "P10-010", "P10-011",
              "P10-012", "P10-013", "P10-014"}
EXPECTED_B = {"P11-001", "P11-003", "P11-004", "P11-005", "P11-007", "P11-009",
              "P11-010", "P11-011", "P11-013", "P11-014", "P11-015",
              "P14-001", "P14-004", "P14-005", "P14-008", "P14-014"}
MUTABLE = {"boundary_rationale", "strongest_rejected_alternative", "device_notes"}

combined = SPBOOK / "draft_rows_combined.jsonl"
rows = [json.loads(l) for l in combined.read_text(encoding="utf-8").splitlines() if l.strip()]
by_id = {r["decision_id"]: r for r in rows}

edits = {}
for name, expected in (("varsweep_A_edits.jsonl", EXPECTED_A),
                       ("varsweep_B_edits.jsonl", EXPECTED_B)):
    got = {}
    for l in (SPBOOK / "author" / name).read_text(encoding="utf-8").splitlines():
        if l.strip():
            e = json.loads(l)
            got[e["decision_id"]] = e
    assert set(got) == expected, f"{name}: edit set mismatch: {sorted(set(got) ^ expected)}"
    edits.update(got)

changed_fields = set()
n_changed = 0
for did, e in edits.items():
    orig = by_id[did]
    assert set(e.keys()) == set(orig.keys()), f"{did}: field-set mismatch"
    diff = {k for k in orig if e[k] != orig[k]}
    assert diff <= MUTABLE, f"{did}: immutable field(s) changed: {sorted(diff - MUTABLE)}"
    assert diff, f"{did}: edit row identical to original"
    changed_fields |= diff
    n_changed += 1
    by_id[did] = e

out_rows = [by_id[r["decision_id"]] for r in rows]      # preserve canonical order
with combined.open("w", encoding="utf-8", newline="\n") as fh:
    for r in out_rows:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
print(json.dumps({"rows_total": len(out_rows), "rows_replaced": n_changed,
                  "changed_fields_union": sorted(changed_fields),
                  "guards": "edit-set exact; immutable fields byte-identical",
                  "status": "APPLIED"}, indent=1))
