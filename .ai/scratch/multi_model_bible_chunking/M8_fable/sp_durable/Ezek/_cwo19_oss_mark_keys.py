#!/usr/bin/env python3
"""CWO-EZ-19 (ezek_controlling_rulings_a1#e9 ruling S2-04), run as its own deterministic sweep. Every element of
observed_substrate_signals that matches the ruled predicate closure\\.(?:parashah_\\w+|pe|samekh)\\b is removed from the list;
bytes are otherwise unchanged, and the manifest records each row's old and new list. The ruled predicate is read from the landed
rulings and must equal this tool's; the rows touched must equal the seven rows the ruled remedy names, or nothing is written.
Spans, order and decision ids are asserted unchanged (_sweep_common). Nothing here judges content.
Usage: _cwo19_oss_mark_keys.py --in repair/rows_v4_fixup1.jsonl --out repair/rows_v4_cwo19.jsonl   (both under SP/Ezek)
"""
import argparse
import json
import re
import sys

from _sweep_common import EZ, load_rows, summary, write_sweep

sys.stdout.reconfigure(encoding="utf-8")
RULINGS_E9 = EZ / "ezek_controlling_agent_rulings_e9.v1.json"
PREDICATE = r"closure\.(?:parashah_\w+|pe|samekh)\b"
RE = re.compile(PREDICATE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    in_p, out_p = EZ / a.inp, EZ / a.out
    e9 = json.loads(RULINGS_E9.read_text(encoding="utf-8"))
    ruled = next(c for c in e9["corpus_wide_orders"] if c["id"] == "CWO-EZ-19")
    if PREDICATE not in ruled["predicate"]:
        raise SystemExit("ABORT: this tool's predicate is not the one CWO-EZ-19 rules")
    ruled_rows = sorted(set(re.findall(r"P\d\d-\d{3}", ruled["remedy"])))
    rows_in = load_rows(in_p)
    rows_out, changes = [], []
    for r in rows_in:
        oss = r.get("observed_substrate_signals")
        if not isinstance(oss, list) or not all(isinstance(k, str) for k in oss):
            raise SystemExit("ABORT: %s observed_substrate_signals is not a list of strings" % r["decision_id"])
        keep = [k for k in oss if not RE.search(k)]
        if keep != oss:
            removed = [(i, k) for i, k in enumerate(oss) if RE.search(k)]
            changes.append({"row": r["decision_id"], "field": "observed_substrate_signals",
                            "removed": [{"index": i, "element": k} for i, k in removed],
                            "old": oss, "new": keep})
        rows_out.append(dict(r, observed_substrate_signals=keep))
    touched = sorted({c["row"] for c in changes})
    if touched != ruled_rows:
        raise SystemExit("ABORT: rows touched %s differ from the ruled rows %s; returns to the controlling lane" % (touched, ruled_rows))
    mf = write_sweep("CWO-EZ-19 (oss keys that encode a parashah mark)", in_p, out_p, rows_in, rows_out, changes, {
        "ruled_predicate": ruled["predicate"], "ruled_fields": ruled["fields"], "ruled_remedy": ruled["remedy"],
        "elements_removed": sum(len(c["removed"]) for c in changes),
        "assert_rows_equal_ruled_rows": True},
        ordered_by=("ezek_controlling_rulings_a1#e9", RULINGS_E9))
    print(json.dumps(summary(mf) | {"elements_removed": mf["elements_removed"], "rows": touched}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
