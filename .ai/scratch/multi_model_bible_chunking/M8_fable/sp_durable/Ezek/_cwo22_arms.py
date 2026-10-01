#!/usr/bin/env python3
"""Shared reading of the corpus-wide orders ruled by ezek_controlling_rulings_a1#e10 (CWO-EZ-22 and CWO-EZ-23).

Everything comes from the ruling file itself, so no pattern, count, row list or pair is retyped here (E-03):
  - CWO-EZ-22's six case-insensitive arms, parsed from the ruled predicate string;
  - the ruled content-field scope;
  - the measured counts and residual rows the ruling states in its remedy;
  - CWO-EZ-23's 33 old -> new pairs.
The module judges no content.
"""
import json
import re
from pathlib import Path

EZ = Path(__file__).resolve().parent
RULINGS_E10 = EZ / "ezek_controlling_agent_rulings_e10.v1.json"
HEAD22 = "six regular-expression arms, case-insensitive, over every content string leaf: "
CONTENT_STR_FIELDS = ("boundary_rationale", "strongest_rejected_alternative", "device_notes", "literature_type_guess")
CONTENT_LIST_FIELDS = ("boundary_evidence_refs", "observed_substrate_signals", "strong_or_hebrew_tags_used")
WAVE_PARTS = ("p01", "p02", "p03", "p04", "p07", "p08")
PAIR_PARTS = ("p05", "p06", "p09", "p10", "p11")
FIELD_IDX = re.compile(r"^(\w+)\[(\d+)\]$")


def ruled(cwo):
    doc = json.loads(RULINGS_E10.read_text(encoding="utf-8"))
    hits = [c for c in doc.get("corpus_wide_orders", []) if c.get("id") == cwo]
    if len(hits) != 1:
        raise SystemExit("ABORT: %d %s entries in %s" % (len(hits), cwo, RULINGS_E10.name))
    return hits[0]


def arms():
    pred = ruled("CWO-EZ-22")["predicate"]
    if not pred.startswith(HEAD22):
        raise SystemExit("ABORT: CWO-EZ-22's predicate does not open with the ruled head")
    parts = re.split(r" ; (?=R[1-6] )", pred[len(HEAD22):])
    out = []
    for i, part in enumerate(parts, 1):
        label = "R%d " % i
        if not part.startswith(label):
            raise SystemExit("ABORT: arm %d does not start with %r" % (i, label))
        out.append(("R%d" % i, re.compile(part[len(label):].strip(), re.I)))
    if len(out) != 6:
        raise SystemExit("ABORT: %d arms parsed, not 6" % len(out))
    return out


def ruled_counts():
    """The counts CWO-EZ-22's remedy states: over rows_v5 and after the CWO-EZ-23 pairs, with the residual rows listed."""
    rem = ruled("CWO-EZ-22")["remedy"]
    m1 = re.search(r"(\d+) hits on (\d+) rows \(R1 (\d+), R2 (\d+), R3 (\d+), R4 (\d+), R5 (\d+), R6 (\d+)\)", rem)
    m2 = re.search(r"after the pairs: (\d+) hits on (\d+) rows, all in the six wave parts \(([^)]*)\)", rem)
    if not m1 or not m2:
        raise SystemExit("ABORT: CWO-EZ-22's remedy does not state its measured counts in the expected form")
    rows_after = re.findall(r"P\d\d-\d{3}", m2.group(3))
    if len(rows_after) != int(m2.group(2)):
        raise SystemExit("ABORT: the remedy lists %d residual rows but states %s" % (len(rows_after), m2.group(2)))
    return {"v5": {"hits": int(m1.group(1)), "rows": int(m1.group(2)),
                   "by_arm": {"R%d" % k: int(m1.group(k + 2)) for k in range(1, 7)}},
            "after_pairs": {"hits": int(m2.group(1)), "rows": int(m2.group(2)), "row_ids": sorted(rows_after)}}


def pairs():
    ps = ruled("CWO-EZ-23")["pairs"]
    if [p["n"] for p in ps] != list(range(1, 34)):
        raise SystemExit("ABORT: CWO-EZ-23's pairs are not numbered 1..33")
    return ps


def get_field(row, field):
    m = FIELD_IDX.match(field)
    if m:
        lst = row.get(m.group(1))
        i = int(m.group(2))
        if not isinstance(lst, list) or i >= len(lst) or not isinstance(lst[i], str):
            raise SystemExit("ABORT: %s has no string at %s" % (row.get("decision_id"), field))
        return lst[i]
    v = row.get(field)
    if not isinstance(v, str):
        raise SystemExit("ABORT: %s.%s is not a string" % (row.get("decision_id"), field))
    return v


def set_field(row, field, value):
    m = FIELD_IDX.match(field)
    if m:
        lst = list(row[m.group(1)])
        lst[int(m.group(2))] = value
        row[m.group(1)] = lst
    else:
        row[field] = value


def content_leaves(row):
    for f in CONTENT_STR_FIELDS:
        v = row.get(f)
        if isinstance(v, str):
            yield f, v
    for f in CONTENT_LIST_FIELDS:
        for i, v in enumerate(row.get(f) or []):
            if isinstance(v, str):
                yield "%s[%d]" % (f, i), v


def hits(rows, arm_list):
    out = []
    for r in rows:
        for field, s in content_leaves(r):
            for name, rx in arm_list:
                for m in rx.finditer(s):
                    out.append({"row": r["decision_id"], "part": r["writer_part"], "field": field, "arm": name, "match": m.group(0),
                                "start": m.start(), "end": m.end(), "context": s[max(0, m.start() - 80):m.end() + 80]})
    return out


if __name__ == "__main__":
    raise SystemExit("shared module; run _cwo23_ruled_pairs.py or _cwo_coverage_e10_ezek.py")
