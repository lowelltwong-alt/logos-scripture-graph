#!/usr/bin/env python3
"""CWO-EZ-04 supplement (the same order: 'quote the Qere with its note bytes exactly'), as its own sweep.

Found after D3. 66 of the 134 stored K/Q notes keep a non-canonical mark order. Rows that quote the Qere of such a note
in canonical (NFD) order carry the right reading in bytes that differ from the note's. The CWO-EZ-04 runs could not see
them, because they judged Qere presence with the NFD-based Qere tier that D3 corrected. This sweep re-splices each such
quote to the note's raw bytes, separators stripped. The two forms are canonically equivalent, so the content is
identical.

Guards, so nothing but a Qere quote changes:
  - only Qere readings whose raw bytes differ from their NFD form (non-canonical notes) are considered;
  - the canonical form must occur in the string as a whole Hebrew run, or as a run's leading or trailing word,
    never inside a longer word;
  - the canonical form must NOT be byte-present in any verse text: a byte-true verse quote is never touched.
After the sweep, every Qere reading of a non-canonical note must appear in canonical order nowhere outside a verse quote.

Usage: _cwo04b_qere_note_bytes.py --in repair/rows_v2_swept_r2.jsonl --out repair/rows_v2_swept_r3.jsonl
"""
import argparse
import json
import re
import sys
import unicodedata

from _sweep_common import EZ, load_rows, summary, write_sweep

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(EZ / "tools"))
from ezek_lib import kq_split_bytes  # noqa: E402

RUN = re.compile(r"[֑-״]+(?:[ ־][֑-״]+)*")
SKIP = {"decision_id", "writer_decision_id", "span", "book", "writer_part", "parent_collection", "confidence", "unit_type",
        "model_id", "writer_attempt_id", "review_status"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    in_p, out_p = EZ / a.inp, EZ / a.out
    oshb = dict(l.split("\t", 1) for l in (EZ / "Ezek_oshb.txt").read_text(encoding="utf-8").splitlines() if "\t" in l)
    all_verses = "\n".join(oshb.values())
    pm = json.loads((EZ / "pmarks_Ezek.json").read_text(encoding="utf-8"))
    targets = {}
    for ref, notes in pm["kq"].items():
        for n in notes:
            _k, q, method = kq_split_bytes(n, oshb.get(ref, ""))
            q = q.replace("/", "")
            canon = unicodedata.normalize("NFD", q)
            if q and canon != q and canon not in all_verses:
                targets[canon] = (q, ref)
    rows_in = load_rows(in_p)
    rows_out, changes = [], []

    def fix(s, did, path):
        out, last = [], 0
        for m in RUN.finditer(s):
            run = m.group(0)
            words = run.split(" ")
            new_words = list(words)
            hit = False
            for canon, (raw, ref) in targets.items():
                cw = canon.split(" ")
                n = len(cw)
                for i in range(len(new_words) - n + 1):
                    if new_words[i:i + n] == cw and (i == 0 or i + n == len(new_words) or n == len(new_words)):
                        new_words[i:i + n] = raw.split(" ")
                        changes.append({"row": did, "field": path, "old": canon, "new": raw, "verse": ref,
                                        "why": "Qere quoted in canonical order; re-spliced to the note's raw bytes"})
                        hit = True
                        break
            if hit:
                out.append(s[last:m.start()])
                out.append(" ".join(new_words))
                last = m.end()
        if not out:
            return s
        out.append(s[last:])
        return "".join(out)

    for r in rows_in:
        nr = {}
        for k, v in r.items():
            if k in SKIP:
                nr[k] = v
            elif isinstance(v, str):
                nr[k] = fix(v, r["decision_id"], k)
            elif isinstance(v, list):
                nr[k] = [fix(x, r["decision_id"], "%s[%d]" % (k, i)) if isinstance(x, str) else x for i, x in enumerate(v)]
            else:
                nr[k] = v
        rows_out.append(nr)
    residual = []
    for r in rows_out:
        blob = json.dumps(r, ensure_ascii=False)
        residual += [(r["decision_id"], ref) for canon, (_raw, ref) in targets.items() if canon in blob]
    m = write_sweep("CWO-EZ-04 (supplement: Qere note bytes)", in_p, out_p, rows_in, rows_out, changes, {
        "predicate": "Qere readings of non-canonical notes quoted in canonical order, outside any verse text",
        "non_canonical_qere_readings_considered": len(targets),
        "assert_no_canonical_form_remains": not residual,
        "residual": residual,
    })
    print(json.dumps(summary(m) | {"non_canonical_qere_readings_considered": len(targets),
                                   "assert_no_canonical_form_remains": not residual, "residual": residual[:10]},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
