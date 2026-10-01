#!/usr/bin/env python3
"""CWO-EZ-21, deterministic half (ezek_controlling_rulings_a1#e9 ruling S2-13), run as its own sweep. Exactly the nine ruled
old -> new pairs are applied, each to its named row and top-level field. Each pair must appear verbatim in the ruled remedy, and
its old substring must occur exactly once in that field, or nothing is written. Bytes are otherwise unchanged, and the manifest
records old and new field bytes per change. The author half (fifteen hits) is left for FIXUP-2; the manifest lists what the
predicate still finds after the sweep, and that list must equal the ruled author half. Spans, order and decision ids are asserted
unchanged (_sweep_common). Nothing here judges content.
Usage: _cwo21_ledger_id_tags.py --in repair/rows_v4_cwo20.jsonl --out repair/rows_v4_cwo21.jsonl   (both under SP/Ezek)
"""
import argparse
import json
import re
import sys
from collections import Counter

from _sweep_common import EZ, load_rows, summary, write_sweep

sys.stdout.reconfigure(encoding="utf-8")
RULINGS_E9 = EZ / "ezek_controlling_agent_rulings_e9.v1.json"
PAIRS = [("P01-003", "boundary_rationale", " (E-23)", ""), ("P01-003", "strongest_rejected_alternative", " (E-23)", ""),
         ("P01-003", "device_notes", " (E-23)", ""), ("P01-014", "boundary_rationale", " (E-23)", ""),
         ("P01-014", "strongest_rejected_alternative", " (E-23)", ""), ("P01-014", "device_notes", " per E-23", ""),
         ("P04-004", "device_notes", "(E-23, ", "("), ("P04-008", "strongest_rejected_alternative", " (E-23)", ""),
         ("P07-006", "device_notes", " (E-02)", "")]
ENN = re.compile(r"\bE-\d{2}\b")
CAMP = re.compile(r"\bcampaign\b", re.I)
AUTHOR_HALF = Counter({("P03-001", "E-02"): 1, ("P03-020", "E-02"): 1, ("P08-010", "E-02"): 1,
                       **{(r, "campaign"): 1 for r in ("P01-006", "P03-003", "P03-007", "P03-014", "P03-020", "P04-001", "P04-002",
                                                        "P04-004", "P04-007", "P08-002", "P09-002", "P09-007")}})


def leaves(o, path=""):
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from leaves(v, ("%s.%s" % (path, k)) if path else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from leaves(v, "%s[%d]" % (path, i))


def predicate_hits(rows):
    hits = []
    for r in rows:
        for p, s in leaves(r):
            hits += [{"row": r["decision_id"], "field": p, "match": m.group(0)} for m in ENN.finditer(s)]
            hits += [{"row": r["decision_id"], "field": p, "match": m.group(0)} for m in CAMP.finditer(s)]
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    in_p, out_p = EZ / a.inp, EZ / a.out
    e9 = json.loads(RULINGS_E9.read_text(encoding="utf-8"))
    ruled = next(c for c in e9["corpus_wide_orders"] if c["id"] == "CWO-EZ-21")
    for row, field, old, new in PAIRS:
        if ("%s %s '%s' -> '%s'" % (row, field, old, new)) not in ruled["remedy"]:
            raise SystemExit("ABORT: the pair %s %s %r -> %r is not in the ruled CWO-EZ-21 remedy" % (row, field, old, new))
    for row, _m in AUTHOR_HALF:
        if row not in ruled["remedy"]:
            raise SystemExit("ABORT: author-half row %s is not in the ruled remedy" % row)
    rows_in = load_rows(in_p)
    by_id = {r["decision_id"]: dict(r) for r in rows_in}
    changes = []
    for row, field, old, new in PAIRS:
        s = by_id[row][field]
        if not isinstance(s, str) or s.count(old) != 1:
            raise SystemExit("ABORT: %s %s carries %r %s times, not exactly once" % (row, field, old, s.count(old) if isinstance(s, str) else "n/a"))
        ns = s.replace(old, new, 1)
        changes.append({"row": row, "field": field, "removed": old, "inserted": new, "old": s, "new": ns})
        by_id[row][field] = ns
    rows_out = [by_id[r["decision_id"]] for r in rows_in]
    left = predicate_hits(rows_out)
    found = Counter((h["row"], "campaign" if h["match"].casefold() == "campaign" else h["match"]) for h in left)
    if found != AUTHOR_HALF:
        raise SystemExit("ABORT: after the nine pairs the predicate finds %s, not the ruled author half %s"
                         % (sorted(found.items()), sorted(AUTHOR_HALF.items())))
    mf = write_sweep("CWO-EZ-21 (ledger ids and campaign talk), deterministic half", in_p, out_p, rows_in, rows_out, changes, {
        "ruled_predicate": ruled["predicate"], "ruled_fields": ruled["fields"], "ruled_remedy": ruled["remedy"],
        "pairs_applied": len(changes), "routed_to_author_wave_fixup2": left,
        "assert_author_half_equals_ruling": True},
        ordered_by=("ezek_controlling_rulings_a1#e9", RULINGS_E9))
    print(json.dumps(summary(mf) | {"pairs_applied": len(changes)}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
