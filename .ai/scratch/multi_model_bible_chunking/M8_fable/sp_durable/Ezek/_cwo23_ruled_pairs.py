#!/usr/bin/env python3
"""CWO-EZ-23 (ezek_controlling_rulings_a1#e10, rulings S3-16 and S3-ROUTING (1)-(2)), run as its own sweep over the chain head
rows_v5_fixup2.jsonl (sha256 41b19ad9...).

What it does:
  - applies exactly the 33 ruled old -> new byte pairs, read from the ruling's corpus_wide_orders entry (never retyped);
  - applies each pair to its named row and field: a top-level string field, or one boundary_evidence_refs entry by index;
  - requires each pair's old bytes to occur exactly once in that field of the input and at the moment it is applied, or writes nothing;
  - leaves bytes otherwise unchanged, and records old and new field bytes per pair in the manifest.

After the pairs, the CWO-EZ-22 predicate (the six ruled arms over the content fields) must find exactly the residual #e10 states: its
count of hits, on its listed rows, all in p01, p02, p03, p04, p07 and p08, and none in p05, p06, p09, p10 or p11. Otherwise nothing is
written, and the difference returns to the controlling lane. Spans, order and decision ids are asserted unchanged (_sweep_common).
Nothing here judges content.

Usage: _cwo23_ruled_pairs.py --in repair/rows_v5_fixup2.jsonl --out repair/rows_v5_cwo23.jsonl   (both under SP/Ezek)
"""
import argparse
import copy
import json
import sys
from collections import Counter

from _cwo22_arms import PAIR_PARTS, RULINGS_E10, WAVE_PARTS, arms, get_field, hits, pairs, ruled, ruled_counts, set_field
from _sweep_common import EZ, load_rows, sha, summary, write_sweep

sys.stdout.reconfigure(encoding="utf-8")
HEAD_SHA = "41b19ad9874dbb56d53b5317572fff6f90879b9b297021e7afc3300dead3c8f2"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    in_p, out_p = EZ / a.inp, EZ / a.out
    if sha(in_p) != HEAD_SHA:
        raise SystemExit("ABORT: the input is not the chain head #e10 names (41b19ad9)")
    ps, rc, arm_list, spec = pairs(), ruled_counts(), arms(), ruled("CWO-EZ-23")
    rows_in = load_rows(in_p)
    by_id = {r["decision_id"]: copy.deepcopy(r) for r in rows_in}
    orig = {r["decision_id"]: r for r in rows_in}
    for p in ps:
        if p["row"] not in orig:
            raise SystemExit("ABORT: pair %d names a row not in the input: %s" % (p["n"], p["row"]))
        n0 = get_field(orig[p["row"]], p["field"]).count(p["old"])
        if n0 != 1:
            raise SystemExit("ABORT: pair %d's old bytes occur %d times in %s %s of the input, not exactly once" % (p["n"], n0, p["row"], p["field"]))
    changes = []
    for p in ps:
        row = by_id[p["row"]]
        s = get_field(row, p["field"])
        if s.count(p["old"]) != 1:
            raise SystemExit("ABORT: pair %d's old bytes occur %d times in %s %s when applied" % (p["n"], s.count(p["old"]), p["row"], p["field"]))
        ns = s.replace(p["old"], p["new"], 1)
        set_field(row, p["field"], ns)
        changes.append({"pair": p["n"], "row": p["row"], "field": p["field"], "removed": p["old"], "inserted": p["new"], "old": s, "new": ns})
    rows_out = [by_id[r["decision_id"]] for r in rows_in]
    v5_hits, left = hits(rows_in, arm_list), hits(rows_out, arm_list)
    v5_by_arm = dict(Counter(h["arm"] for h in v5_hits))
    left_rows = sorted({h["row"] for h in left})
    problems = []
    if len(v5_hits) != rc["v5"]["hits"] or len({h["row"] for h in v5_hits}) != rc["v5"]["rows"] or v5_by_arm != rc["v5"]["by_arm"]:
        problems.append("over the input the arms find %d hits on %d rows %s; the ruling states %s"
                        % (len(v5_hits), len({h["row"] for h in v5_hits}), v5_by_arm, rc["v5"]))
    if len(left) != rc["after_pairs"]["hits"] or left_rows != rc["after_pairs"]["row_ids"]:
        problems.append("after the pairs the arms find %d hits on rows %s; the ruling states %d hits on %s"
                        % (len(left), left_rows, rc["after_pairs"]["hits"], rc["after_pairs"]["row_ids"]))
    stray = sorted({h["row"] for h in left if h["part"] in PAIR_PARTS or h["part"] not in WAVE_PARTS})
    if stray:
        problems.append("after the pairs hits remain outside the six wave parts: %s" % stray)
    if problems:
        raise SystemExit("ABORT (returns to the controlling lane; nothing written): " + " | ".join(problems))
    mf = write_sweep("CWO-EZ-23 (33 ruled byte pairs removing rule names as warrants)", in_p, out_p, rows_in, rows_out, changes, {
        "ruled_predicate": spec["predicate"], "ruled_fields": spec["fields"], "ruled_remedy": spec["remedy"],
        "pairs_applied": len(changes), "pairs_refused": 0,
        "cwo_ez_22_over_input": {"hits": len(v5_hits), "rows": len({h["row"] for h in v5_hits}), "by_arm": v5_by_arm},
        "routed_to_author_wave_fixup3": [{k: h[k] for k in ("row", "part", "field", "arm", "match")} for h in left],
        "assert_residual_equals_ruling": True},
        ordered_by=("ezek_controlling_rulings_a1#e10", RULINGS_E10))
    print(json.dumps(summary(mf) | {"pairs_applied": len(changes), "cwo_ez_22_input_hits": len(v5_hits), "residual_hits": len(left),
                                    "residual_rows": len(left_rows)}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
