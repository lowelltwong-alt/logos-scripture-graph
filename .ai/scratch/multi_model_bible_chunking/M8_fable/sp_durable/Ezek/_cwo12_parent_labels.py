#!/usr/bin/env python3
"""CWO-EZ-12 (ezek_controlling_rulings_a1#e3, ruling PC-1), run as its own deterministic sweep over the applied rows.
parent_collection is canonicalised to ONE label per parent, keyed on the row's P<n> prefix, exactly as ruled (the
strategy's section-5 table verbatim). The sweep records old -> new per row, aborts when any row's prefix is not P1-P8,
and asserts that no row's parent id changes. Spans, order and decision ids are asserted unchanged (_sweep_common).
Usage: _cwo12_parent_labels.py --in <rows> --out <swept rows>   (both under SP/Ezek)
"""
import argparse
import json
import re
import sys

from _sweep_common import EZ, load_rows, summary, write_sweep

sys.stdout.reconfigure(encoding="utf-8")
RULINGS_E3 = EZ / "ezek_controlling_agent_rulings_e3.v1.json"
CANON = {"P1": "P1 (inaugural vision and commission)", "P2": "P2 (sign-acts and the first judgment oracles)",
         "P3": "P3 (the temple vision)", "P4": "P4 (the undated oracle collection)",
         "P5": "P5 (the dated disputation-to-siege collection)", "P6": "P6 (oracles against the nations)",
         "P7": "P7 (restoration oracles and visions)", "P8": "P8 (the temple vision and the land)"}
PREFIX = re.compile(r"^\s*(P[1-8])(?![0-9])")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    in_p, out_p = EZ / a.inp, EZ / a.out
    e3 = json.loads(RULINGS_E3.read_text(encoding="utf-8"))
    ruled = next(c for c in e3["corpus_wide_orders"] if c["id"] == "CWO-EZ-12")
    for pid, label in CANON.items():
        if label.split(" ", 1)[1].strip("()") not in ruled["order"]:
            raise SystemExit("ABORT: the label for %s is not the one CWO-EZ-12 rules" % pid)
    rows_in = load_rows(in_p)
    rows_out, changes = [], []
    for r in rows_in:
        m = PREFIX.match(str(r.get("parent_collection", "")))
        if not m:
            raise SystemExit("ABORT: %s has no P1-P8 prefix in parent_collection %r" % (r["decision_id"], r.get("parent_collection")))
        nr = dict(r, parent_collection=CANON[m.group(1)])
        if nr["parent_collection"] != r["parent_collection"]:
            changes.append({"row": r["decision_id"], "field": "parent_collection", "old": r["parent_collection"], "new": nr["parent_collection"]})
        assert PREFIX.match(nr["parent_collection"]).group(1) == m.group(1), "a parent id changed"
        rows_out.append(nr)
    distinct = sorted({r["parent_collection"] for r in rows_out})
    mf = write_sweep("CWO-EZ-12 (canonical parent labels)", in_p, out_p, rows_in, rows_out, changes, {
        "narrowed_predicate_label": ruled["predicate"],
        "labels_before": sorted({r["parent_collection"] for r in rows_in}), "labels_after": distinct,
        "assert_one_label_per_parent": len(distinct) == len({PREFIX.match(x).group(1) for x in distinct}),
        "assert_no_parent_id_changed": True},
        shape_keys=("decision_id", "span", "chunk_index_in_book", "writer_part"),
        ordered_by=("ezek_controlling_rulings_a1#e3", RULINGS_E3))
    print(json.dumps(summary(mf) | {"labels_before": len(mf["labels_before"]), "labels_after": len(distinct)}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
