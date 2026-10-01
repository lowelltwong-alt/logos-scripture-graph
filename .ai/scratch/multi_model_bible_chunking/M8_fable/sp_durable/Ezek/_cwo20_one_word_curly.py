#!/usr/bin/env python3
"""CWO-EZ-20 (ezek_controlling_rulings_a1#e9 ruling S2-12), run as its own deterministic sweep. In every string leaf of every
field (refs entries and tags included) that contains no 'web:' substring, each one-word span in curly double quotes
(U+201C ... U+201D, no whitespace inside) becomes single curly quotes (U+2018 ... U+2019); bytes are otherwise unchanged, and the
manifest records old and new bytes per changed leaf, with 60 characters of context per hit.

Classification per hit is NOT decided here. #e9 read all twelve live contexts and ruled every one a gloss or label, none a
WEB-wording claim. The sweep asserts that the hits it finds equal that ruled multiset, (row, span) by (row, span), and stamps
them 'gloss' on that ruling. Any other hit, or a missing one, writes nothing and returns to the controlling lane.
Spans, order and decision ids are asserted unchanged (_sweep_common).
Usage: _cwo20_one_word_curly.py --in repair/rows_v4_cwo19.jsonl --out repair/rows_v4_cwo20.jsonl   (both under SP/Ezek)
"""
import argparse
import json
import re
import sys
from collections import Counter

from _sweep_common import EZ, load_rows, summary, write_sweep

sys.stdout.reconfigure(encoding="utf-8")
RULINGS_E9 = EZ / "ezek_controlling_agent_rulings_e9.v1.json"
ONE_RE = re.compile("“([^“”\\s]+)”")
RULED_HITS = Counter({("P02-016", "“foxes”"): 1, ("P02-020", "“Daniel”"): 1, ("P08-007", "“because”"): 4,
                      ("P08-011", "“you,”"): 3, ("P08-012", "“for”"): 1, ("P08-013", "“for”"): 1,
                      ("P09-011", "“therefore,”"): 1})


def transform(o, path, rid, changes):
    if isinstance(o, str):
        if "web:" in o:
            return o
        hits = list(ONE_RE.finditer(o))
        if not hits:
            return o
        new = ONE_RE.sub(lambda m: "‘" + m.group(1) + "’", o)
        changes.append({"row": rid, "field": path, "old": o, "new": new, "spans": [m.group(0) for m in hits],
                        "contexts": [o[max(0, m.start() - 30):m.end() + 30] for m in hits],
                        "classification": ["gloss"] * len(hits)})
        return new
    if isinstance(o, list):
        return [transform(v, "%s[%d]" % (path, i), rid, changes) for i, v in enumerate(o)]
    if isinstance(o, dict):
        return {k: transform(v, ("%s.%s" % (path, k)) if path else k, rid, changes) for k, v in o.items()}
    return o


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    in_p, out_p = EZ / a.inp, EZ / a.out
    e9 = json.loads(RULINGS_E9.read_text(encoding="utf-8"))
    ruled = next(c for c in e9["corpus_wide_orders"] if c["id"] == "CWO-EZ-20")
    decision = next(r for r in e9["rulings"] if r["id"] == "S2-12")["decision"]
    if "U+201C" not in ruled["predicate"] or "U+2018" not in ruled["remedy"]:
        raise SystemExit("ABORT: the ruled CWO-EZ-20 predicate or remedy is not the one this tool implements")
    for (row, span) in RULED_HITS:
        if row not in decision or span not in decision:
            raise SystemExit("ABORT: %s %s is not in #e9 ruling S2-12's reading of the contexts" % (row, span))
    rows_in = load_rows(in_p)
    rows_out, changes = [], []
    for r in rows_in:
        rows_out.append(transform(r, "", r["decision_id"], changes))
    found = Counter((c["row"], s) for c in changes for s in c["spans"])
    if found != RULED_HITS:
        raise SystemExit("ABORT: hits found %s differ from the ruled hits %s; returns to the controlling lane"
                         % (sorted(found.items()), sorted(RULED_HITS.items())))
    mf = write_sweep("CWO-EZ-20 (one-word curly double-quoted spans with no web: ref)", in_p, out_p, rows_in, rows_out, changes, {
        "ruled_predicate": ruled["predicate"], "ruled_fields": ruled["fields"], "ruled_remedy": ruled["remedy"],
        "hit_count": sum(found.values()), "classification_source": "ezek_controlling_rulings_a1#e9 ruling S2-12 (all twelve contexts read: "
                                                                   "every span a gloss or label, none a WEB-wording claim)",
        "web_wording_claims_left_for_authors": [], "assert_hits_equal_ruled_hits": True},
        ordered_by=("ezek_controlling_rulings_a1#e9", RULINGS_E9))
    print(json.dumps(summary(mf) | {"hit_count": mf["hit_count"]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
