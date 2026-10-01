#!/usr/bin/env python3
"""Build the BOUNDED FIX ROUND from a postcheck's residuals (the not_fit path).

A not_fit verdict is a normal outcome: it orders a bounded cure round over exactly the residual rows, and a FRESH
postcheck afterwards. This builder carries each residual verbatim - its class, severity, origin lane, the exact
defective text, the byte evidence and the reviewer's one-sentence proposed cure - so the fix author cures the defect
the reviewer actually found rather than a paraphrase of it.

Slices are <=8 rows. Digits are the tool's COUNTS.
Usage: _build_fix_orders.py --postcheck postcheck_01.json --base rows_v8.jsonl"""
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
A = sys.argv[1:]
def arg(k, d=None): return A[A.index(k) + 1] if k in A else d
PC = arg("--postcheck", "postcheck_01.json"); BASE = arg("--base", "rows_v8.jsonl")


def main():
    rows = {r["decision_id"]: r for r in (json.loads(l) for l in (HERE / BASE).read_text(encoding="utf-8-sig").splitlines() if l.strip())}
    pc = json.load(open(HERE / "postcheck" / PC, encoding="utf-8-sig"))
    assert pc.get("verdict") == "not_fit", f"postcheck verdict is {pc.get('verdict')}: no fix round is needed"
    per_row = defaultdict(list)
    for r in pc.get("residual", []):
        rid = r.get("row_id")
        assert rid in rows, f"residual names an unknown row: {rid}"
        per_row[rid].append({k: r.get(k) for k in ("e_class", "severity", "origin", "defective_text", "byte_evidence", "proposed_cure")})
    assert per_row, "no residuals"
    ids = sorted(per_row, key=lambda r: rows[r]["chunk_index_in_book"])
    out_dir = HERE / "spot"; out_dir.mkdir(exist_ok=True)
    slices = []
    for n in range(0, len(ids), 8):
        k = n // 8 + 1
        ch = ids[n:n + 8]
        sl = {"schema": "lam_fix_orders_slice.v1", "agent": f"f{k:02d}", "attempt_id": f"lam_fix_f{k:02d}_a1", "base": BASE,
              "source_postcheck": PC, "output_file": f"spot/fix_{k:02d}.jsonl", "row_ids": ch,
              "law": "these are the residuals a postcheck found AFTER the cure round: defects that survived a cure, or that a cure installed. Cure the defect the reviewer found, from its byte evidence, and nothing else on the row.",
              "orders": {rid: {"row_id": rid, "op": "replace", "current_row": rows[rid], "residuals": per_row[rid]} for rid in ch}}
        (out_dir / f"orders_fix_{k:02d}.json").write_text(json.dumps(sl, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
        slices.append({"slice": sl["agent"], "attempt_id": sl["attempt_id"], "rows": ch,
                       "items": sum(len(per_row[r]) for r in ch),
                       "medium": sum(1 for r in ch for it in per_row[r] if it["severity"] == "medium"),
                       "low": sum(1 for r in ch for it in per_row[r] if it["severity"] == "low")})
    print(json.dumps({"base": BASE, "postcheck": PC, "rows": len(ids), "items": sum(len(v) for v in per_row.values()),
                      "blocking_rows": pc.get("blocking", []), "slices": slices}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
