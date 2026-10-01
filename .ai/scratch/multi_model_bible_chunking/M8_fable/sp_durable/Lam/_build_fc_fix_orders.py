#!/usr/bin/env python3
"""Build the bounded fix round ordered by the OW-6 stage-2 FINAL CHECKER (not by a postcheck).

_build_fix_orders.py reads a postcheck packet, whose residuals carry a row_id. A final-check packet names its
subject in row_or_artifact, which may hold a field name ("P03-006 device_notes"), two rows at once
("P02-004 device_notes; P02-008 device_notes"), or an artifact that is not a row at all. This builder handles that
shape, splits multi-row residuals into per-row orders, and IGNORES the non-corpus residuals - those are the
orchestrator's own to fix and several already are.

Each order carries the checker's words verbatim: the defective text, the byte evidence, and the cure it proposed.
The author cures the defect the checker actually found rather than a paraphrase of it, and cannot widen the edit,
because the guarded apply freezes span, unit_type, parent_collection, confidence, the frontier flag and review
status. Digits are the tool's COUNTS.
Usage: _build_fc_fix_orders.py [--final-check final_check_01.json] [--base rows_v9.jsonl]"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
A = sys.argv[1:]
def arg(k, d): return A[A.index(k) + 1] if k in A else d
FC = arg("--final-check", "final_check_01.json")
BASE = arg("--base", "rows_v9.jsonl")
ROW_RE = re.compile(r"\bP\d{2}-\d{3}\b")


def main():
    rows = {r["decision_id"]: r for r in
            (json.loads(l) for l in (HERE / BASE).read_text(encoding="utf-8-sig").splitlines() if l.strip())}
    fc = json.load(open(HERE / "final_check" / FC, encoding="utf-8-sig"))
    assert fc.get("verdict") == "not_fit_to_close", f"final-check verdict is {fc.get('verdict')}: no fix round needed"

    per_row, skipped = defaultdict(list), []
    for r in fc.get("residual", []):
        subject = str(r.get("row_or_artifact", "")).strip()
        # A residual is a ROW EDIT only when its subject BEGINS with a row id. Merely MENTIONING a row is not the
        # same as being about it: the CWO-1 residual names P02-006 as the evidence for a missing ORDER RULING, and
        # a naive search for row ids would hand a records defect to a corpus author, who would then edit a row that
        # is not what is wrong. Anchoring on the first token is what distinguishes subject from evidence.
        ids = ROW_RE.findall(subject) if ROW_RE.match(subject) else []
        if not ids:
            skipped.append({"row_or_artifact": subject[:90], "severity": r.get("severity"),
                            "why": "not a corpus row - orchestrator/record residual, cured outside this wave"})
            continue
        for rid in ids:
            assert rid in rows, f"residual names an unknown row: {rid}"
            per_row[rid].append({
                "e_class": r.get("class"), "severity": r.get("severity"), "origin": r.get("origin"),
                "field": next((f for f in ("boundary_rationale", "device_notes", "strongest_rejected_alternative")
                               if f in subject), None),
                "defective_text": r.get("defective_text"), "byte_evidence": r.get("evidence"),
                "proposed_cure": r.get("proposed_cure")})

    assert per_row, "no corpus-row residuals in the final check"
    ids = sorted(per_row, key=lambda r: rows[r]["chunk_index_in_book"])
    out_dir = HERE / "spot"
    out_dir.mkdir(exist_ok=True)
    slices = []
    for n in range(0, len(ids), 8):
        k = n // 8 + 2  # fix_01 already exists from the postcheck path; this round starts at 02
        ch = ids[n:n + 8]
        sl = {"schema": "lam_fc_fix_orders_slice.v1", "agent": f"f{k:02d}", "attempt_id": f"lam_fcfix_f{k:02d}_a1",
              "base": BASE, "source_final_check": FC, "output_file": f"spot/fix_{k:02d}.jsonl", "row_ids": ch,
              "law": "these residuals were found by the OW-6 stage-2 FINAL CHECKER against the assembled corpus, "
                     "after the postcheck passed. Cure exactly the defect it names, from its byte evidence, and "
                     "nothing else on the row. Where it proposed a cure, execute that cure unless the bytes show it "
                     "is wrong - in which case cure correctly and say why in your final message. Every edit is read "
                     "back against its verse before you deliver.",
              "orders": {rid: {"row_id": rid, "op": "replace", "current_row": rows[rid],
                               "residuals": per_row[rid]} for rid in ch}}
        (out_dir / f"orders_fix_{k:02d}.json").write_text(json.dumps(sl, ensure_ascii=False, indent=1),
                                                          encoding="utf-8", newline="\n")
        slices.append({"slice": sl["agent"], "attempt_id": sl["attempt_id"], "orders_file": f"spot/orders_fix_{k:02d}.json",
                       "output_file": sl["output_file"], "rows": ch,
                       "items": sum(len(per_row[r]) for r in ch),
                       "medium": sum(1 for r in ch for it in per_row[r] if it["severity"] == "medium"),
                       "low": sum(1 for r in ch for it in per_row[r] if it["severity"] == "low")})

    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({"base": BASE, "final_check": FC, "corpus_rows": len(ids),
                      "items": sum(len(v) for v in per_row.values()),
                      "slices": slices,
                      "non_corpus_residuals_not_in_this_wave": skipped}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
