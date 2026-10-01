#!/usr/bin/env python3
"""CWO-EZ-05 (rulings R3(v) and CWO-EZ-05): mark and paseq claim verification against pmarks_Ezek.json, as its own sweep.

Mechanical corrections only, each asserted against the inventory before it is made:
  1. P01-009 cites paseq at MT 5:2, where the inventory has 5:1 (5:7 is right). The ref entry and the device_notes
     phrase move to 5:1. The inventory is asserted to hold 5:1 and not 5:2 before either edit.
  2. Every boundary_evidence_refs entry that citation_sweep reads as a parashah claim (its own MARK_WORD pattern) or as a
     paseq claim, and lacks 'single-witness', gains the disclosure: 'single witness' (space) becomes 'single-witness';
     otherwise ', single-witness' goes before the closing parenthesis, or ' (single-witness)' is appended. The hyphen
     matters because citation_sweep tests for 'single-witness' literally, while R1 wrote the words with a space.
Not changed here, but REPORTED to the author wave, per CWO-EZ-05: every pe/samekh claim contradicting the inventory
(mark_symmetry paragraph_mark_claim) and every false mark-absence claim (false_mark_absence_claim), taken from the
Tier-0 report with the inventory's own values. P06-008's paseq claim at 26:19 is resolved by the G7 merge.

Usage: _cwo05_marks_paseq.py --in repair/rows_s3_cwo02.jsonl --out repair/rows_s4_cwo05.jsonl
"""
import argparse
import json
import re
import sys

from _sweep_common import EZ, REPORT_V1, load_rows, summary, write_sweep

sys.stdout.reconfigure(encoding="utf-8")
MARK_WORD = re.compile(r"\b(petuchah|setumah)\b|\b(pe|samekh)\b(?!\w)", re.I)
PASEQ = re.compile(r"\bpaseq\b", re.I)
REF_HEAD = re.compile(r"^(?:web|oshb):Ezek\.\d+\.\d+(?:-(?:Ezek\.)?\d+(?:\.\d+)?)?(?:\s*=\s*(?:web|oshb):Ezek\.\d+\.\d+(?:-(?:Ezek\.)?\d+(?:\.\d+)?)?)?")


def add_single_witness(entry):
    if "single-witness" in entry:
        return entry
    if re.search(r"single witness", entry, re.I):
        return re.sub(r"single witness", "single-witness", entry, count=1, flags=re.I)
    if entry.rstrip().endswith(")"):
        s = entry.rstrip()
        return s[:-1] + ", single-witness)"
    return entry + " (single-witness)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    in_p, out_p = EZ / a.inp, EZ / a.out
    pm = json.loads((EZ / "pmarks_Ezek.json").read_text(encoding="utf-8"))
    paseq = set(pm["paseq"])
    assert "Ezek.5.1" in paseq and "Ezek.5.2" not in paseq and "Ezek.5.7" in paseq, "inventory no longer supports the 5:1 correction"
    rows_in = load_rows(in_p)
    rows_out, changes = [], []
    for r in rows_in:
        nr = json.loads(json.dumps(r, ensure_ascii=False))
        did = nr["decision_id"]
        if did == "P01-009":
            old = "oshb:Ezek.5.2 (paseq, single-witness, count-only)"
            idx = [i for i, x in enumerate(nr["boundary_evidence_refs"]) if x == old]
            assert len(idx) == 1, "P01-009 paseq ref not found exactly once"
            nr["boundary_evidence_refs"][idx[0]] = "oshb:Ezek.5.1 (paseq, single-witness, count-only)"
            changes.append({"row": did, "field": "boundary_evidence_refs", "index": idx[0], "old": old,
                            "new": nr["boundary_evidence_refs"][idx[0]], "why": "R3(v): inventory paseq at 5:1, none at 5:2"})
            assert nr["device_notes"].count("Paseq at 5:2 and 5:7") == 1, "P01-009 device_notes phrase not found exactly once"
            nr["device_notes"] = nr["device_notes"].replace("Paseq at 5:2 and 5:7", "Paseq at 5:1 and 5:7")
            changes.append({"row": did, "field": "device_notes", "old": "Paseq at 5:2 and 5:7", "new": "Paseq at 5:1 and 5:7",
                            "why": "R3(v)"})
        for i, x in enumerate(nr.get("boundary_evidence_refs", [])):
            head = REF_HEAD.match(x)
            tail = x[head.end():] if head else x
            if (MARK_WORD.search(tail) or PASEQ.search(tail)) and "single-witness" not in tail:
                new = add_single_witness(x)
                if new != x:
                    nr["boundary_evidence_refs"][i] = new
                    changes.append({"row": did, "field": "boundary_evidence_refs", "index": i, "old": x, "new": new,
                                    "why": "parashah/paseq ref disclosure 'single-witness' (CWO-EZ-05)"})
        rows_out.append(nr)
    rep = json.loads(REPORT_V1.read_text(encoding="utf-8"))
    reported = [dict(decision_id=f["decision_id"], rule=f["rule"],
                     **{k: f[k] for k in ("claimed", "verse_cited", "inventory_under_both_readings",
                                          "span_relevant_marks_mt_keys") if k in f})
                for f in rep["mark_symmetry"]["flags"] if f["rule"] in ("paragraph_mark_claim", "false_mark_absence_claim")]
    m = write_sweep("CWO-EZ-05", in_p, out_p, rows_in, rows_out, changes, {
        "predicate": "P01-009 paseq misreference; parashah/paseq refs lacking single-witness; contradicted mark claims reported",
        "inventory": {"path": "Ezek/pmarks_Ezek.json", "paseq_5_1": True, "paseq_5_2": False},
        "routed_to_author_wave_mark_claims_contradicting_inventory": reported,
        "routed_to_author_wave_note": "P06-008's paseq claim at MT 26:19 (none in the inventory) is resolved by the G7 merge",
    })
    print(json.dumps(summary(m), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
