#!/usr/bin/env python3
"""CWO-EZ-09 (rulings R3(iii) and CWO-EZ-09): whole-chapter cap enforcement on the one row the orchestrator corrects
mechanically, as its own sweep.

P02-004 spans all of MT/WEB chapter 9 (identity numbering). E-02 requires confidence <= medium_low, the frontier flag,
and a cap disclosure that cites the chapter's verse count together with cap phrasing. The ruling keeps the span and
changes the confidence: medium -> medium_low, with the cap sentence appended to device_notes. Every precondition is
asserted before the edit: the whole-chapter span, the chapter's verse count read from verse_inventory.json, the current
confidence and the flag. P01-002 (ch 2) is NOT touched: R3 resolves it by a boundary amendment in the author wave, so
cap_sweep is expected to report that row alone until the author wave lands.

Usage: _cwo09_cap.py --in repair/rows_s4_cwo05.jsonl --out repair/rows_v2_swept.jsonl
"""
import argparse
import json
import os
import subprocess
import sys

from _sweep_common import EZ, load_rows, summary, write_sweep

sys.stdout.reconfigure(encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    in_p, out_p = EZ / a.inp, EZ / a.out
    inv = json.loads((EZ / "verse_inventory.json").read_text(encoding="utf-8"))
    per_ch = inv.get("per_chapter") or inv.get("chapters") or inv
    n9 = per_ch.get("9") if isinstance(per_ch, dict) else None
    n9 = n9 if isinstance(n9, int) else (n9 or {}).get("verses") if isinstance(n9, dict) else n9
    assert n9 == 11, "verse_inventory.json does not give chapter 9 as 11 verses (got %r)" % n9
    rows_in = load_rows(in_p)
    rows_out, changes = [], []
    for r in rows_in:
        nr = json.loads(json.dumps(r, ensure_ascii=False))
        if nr["decision_id"] == "P02-004":
            assert nr["span"] == "Ezek.9.1-Ezek.9.11", nr["span"]
            assert nr["confidence"] == "medium", nr["confidence"]
            assert nr["frontier_flag_considered"] is True
            nr["confidence"] = "medium_low"
            changes.append({"row": "P02-004", "field": "confidence", "old": "medium", "new": "medium_low", "why": "R3(iii), E-02"})
            sentence = (" Whole-chapter row covering all 11 verses of the chapter: confidence is capped at medium_low under "
                        "the whole-chapter cap.")
            nr["device_notes"] = nr["device_notes"].rstrip() + sentence
            changes.append({"row": "P02-004", "field": "device_notes", "appended": sentence.strip(), "why": "E-02 cap disclosure"})
        rows_out.append(nr)
    assert len(changes) == 2, "P02-004 not found"
    m = write_sweep("CWO-EZ-09", in_p, out_p, rows_in, rows_out, changes, {
        "predicate": "P02-004 (whole chapter 9); P01-002 left to the R3 boundary amendment in the author wave",
    })
    cs = subprocess.run([sys.executable, str(EZ / "tools" / "cap_sweep.py"), str(out_p)], capture_output=True, text=True,
                        encoding="utf-8", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    cap = json.loads(cs.stdout)
    print(json.dumps(summary(m) | {"cap_sweep_on_output": {"failures": cap["failures"], "status": cap["status"]}},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
