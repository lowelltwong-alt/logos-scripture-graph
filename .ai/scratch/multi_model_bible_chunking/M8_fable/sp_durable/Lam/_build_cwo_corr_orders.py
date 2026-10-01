#!/usr/bin/env python3
"""Build the BOUNDED CWO CORRECTION round from the post-wave re-scan residuals (E-18: an exact arm must return 0 over
the revised corpus; where it does not, the residual is cured and the arm re-run, never waived).

Input: the post-scan JSON over rows_v3 produced by the corrected _cwo_scan.py. Output: cwo/corr/orders_corr_01.json,
one slice carrying every row with a residual exact-arm item, each item quoting the boss's controlling predicate and the
scan's own evidence. Rows are the residual rows only; nothing else may be touched.
Usage: _build_cwo_corr_orders.py --post <scan_post.json> [--base rows_v3.jsonl]"""
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
A = sys.argv[1:]
def arg(k, d=None): return A[A.index(k) + 1] if k in A else d
POST = arg("--post"); BASE = arg("--base", "rows_v3.jsonl")
EXACT = ("CWO-1", "CWO-2", "CWO-4", "CWO-6", "CWO-10")
INSTR = {
    "CWO-2": ("Rewrite the flagged sentence so the listed word is gone, OR give the claim a same-sentence sweep citation "
              "bearing a DIGIT (the numeral, not a spelled-out number) and a unit word. An ordinal or positional use "
              "(the first half, the last verse, first appear) is not an exclusivity claim and is rewritten with a "
              "non-listed word rather than given a false sweep. Do not touch any verbatim quotation."),
    "CWO-4": ("device_notes must name the OUT-OF-SPAN verse the scan lists as well as an in-span verse. Verify the sweep "
              "yourself with sweep.py before writing the disclosure, and keep the count true."),
    "CWO-10": ("Add the ketiv/qere disclosure to the SAME FIELD as the splice: name that the verse is marked in the K/Q "
              "inventory and whether the spliced form stands at the variant. Check pmarks_Lam.json before writing it."),
}


def main():
    rows = {r["decision_id"]: r for r in (json.loads(l) for l in (HERE / BASE).read_text(encoding="utf-8-sig").splitlines() if l.strip())}
    scan = json.load(open(POST, encoding="utf-8"))["orders"]
    boss = json.load(open(HERE / "reviews" / "boss_lam_b1.json", encoding="utf-8-sig"))
    texts = {c["id"]: {k: c[k] for k in ("id", "arm", "predicate", "scope", "test") if k in c} for c in boss["corpus_wide_orders"]}
    per_row = defaultdict(list)
    for cwo in EXACT:
        for c in scan[cwo]["candidates"]:
            per_row[c["row"]].append({"cwo": cwo, "arm": "exact", "residual_evidence": {k: v for k, v in c.items() if k != "row"},
                                      "instruction": INSTR[cwo]})
    assert per_row, "no residuals: the correction round is unnecessary"
    ids = sorted(per_row, key=lambda r: rows[r]["chunk_index_in_book"])
    assert len(ids) <= 8, f"{len(ids)} rows: split the round"
    out_dir = HERE / "cwo" / "corr"; out_dir.mkdir(parents=True, exist_ok=True)
    sl = {"schema": "lam_cwo_corr_orders_slice.v1", "agent": "corr01", "attempt_id": "lam_cwo_corr_01_a1", "base": BASE,
          "output_file": "cwo/corr/corr_01.jsonl", "row_ids": ids,
          "law": "these are the exact-arm residuals of the corpus-wide-order wave, measured by re-running the same deterministic scan over the revised corpus; the arm is not satisfied until the re-scan returns 0",
          "orders": {rid: {"row_id": rid, "op": "replace", "current_row": rows[rid], "items": sorted(per_row[rid], key=lambda it: int(it["cwo"].split("-")[1])),
                           "cwo_texts": {it["cwo"]: texts[it["cwo"]] for it in per_row[rid]}} for rid in ids}}
    (out_dir / "orders_corr_01.json").write_text(json.dumps(sl, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    print(json.dumps({"rows": ids, "items": {rid: [it["cwo"] for it in per_row[rid]] for rid in ids},
                      "orders_file": str(out_dir / "orders_corr_01.json")}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
