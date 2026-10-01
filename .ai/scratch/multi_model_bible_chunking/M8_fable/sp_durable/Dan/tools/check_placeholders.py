#!/usr/bin/env python3
"""Unfilled-template placeholder check (HARD suite member "placeholders"), Dan.

Controlling ruling S1-02 (dan_controlling_rulings_a1#e3, 2026-09-29): S1 found W6-001.strongest_rejected_alternative
carrying two unfilled "%s" placeholders, and no suite member caught it. This member walks EVERY string value at any
depth of every row, all fields (boundary_evidence_refs and parent_collection included), and is RED on any match of the
CWO-DAN-01 predicate (Python re, no flags):
    %(?:\\([A-Za-z_]\\w*\\))?[-+ #0]*\\d*(?:\\.\\d+)?[sdrifx]|\\{(?:[A-Za-z_]\\w*|\\d+)?(?:![rsa])?(?::[^{}\\s]*)?\\}
It adds a gate and weakens none. Prints one JSON object with a coverage report.

Usage: check_placeholders.py rows.jsonl [more files]   |   check_placeholders.py --selftest
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PRED = re.compile(r"%(?:\([A-Za-z_]\w*\))?[-+ #0]*\d*(?:\.\d+)?[sdrifx]"
                  r"|\{(?:[A-Za-z_]\w*|\d+)?(?:![rsa])?(?::[^{}\s]*)?\}")


def rows_from(p: Path):
    text = p.read_text(encoding="utf-8-sig")
    if p.suffix == ".jsonl":
        return [json.loads(l) for l in text.splitlines() if l.strip()]
    data = json.loads(text)
    if isinstance(data, dict):
        return data.get("decisions", [v for v in data.values() if isinstance(v, dict)])
    return data


def strings(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from strings(v, f"{path}.{k}" if path else str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from strings(v, f"{path}[{i}]")
    elif isinstance(o, str):
        yield path, o


def scan(rows):
    hits, nstr, nrows = [], 0, 0
    for n, row in enumerate(rows):
        if not isinstance(row, dict):
            continue
        nrows += 1
        rid = row.get("decision_id") or row.get("chunk_id") or f"#{n}"
        for field, s in strings(row):
            nstr += 1
            for m in PRED.finditer(s):
                hits.append({"row": rid, "field": field, "match": m.group(0), "at": m.start()})
    return hits, nstr, nrows


def selftest() -> int:
    # W6-001.strongest_rejected_alternative verbatim as installed 2026-09-29 (413 chars), per the S1-02 order.
    w6_001 = ("Two candidates were weighed. A one-verse heading at 10:1 (the third-person summary) with the first-person "
              "mourning opening at 10:2 was declined: oshb:Dan.10.2 begins %s (OSHB/WLC), %s (WEB), which points back "
              "to the time 10:1 has just named, so the heading and the fast read as one setting (INFERRED). Running the "
              "unit on to 10:9 was also declined, because the new day and place at 10:4 begin the sighting itself.")
    must_fail = [w6_001, "{name}", "%(x)s", "{0}", "{}"]
    must_pass = ["50%", "a 100 % count", "בִּשְׁנַת "
                 "שָׁלוֹשׁ", "{ a b }"]
    bad = [s for s in must_fail if not PRED.search(s)] + [s for s in must_pass if PRED.search(s)]
    w6 = PRED.findall(must_fail[0])
    ok = not bad and w6 == ["%s", "%s"] and len(w6_001) == 413
    print(json.dumps({"selftest": "PASS" if ok else "FAIL", "must_fail": len(must_fail), "must_pass": len(must_pass),
                      "misbehaving": bad, "w6_matches": w6}, ensure_ascii=False))
    return 0 if ok else 1


def main() -> int:
    if "--selftest" in sys.argv:
        return selftest()
    files = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not files:
        print(json.dumps({"usage": "check_placeholders.py rows.jsonl [...] | --selftest", "status": "ERROR"}))
        return 2
    rows = [r for f in files for r in rows_from(Path(f))]
    hits, nstr, nrows = scan(rows)
    by_row: dict[str, int] = {}
    for h in hits:
        by_row[h["row"]] = by_row.get(h["row"], 0) + 1
    print(json.dumps({"rows": nrows, "strings_scanned": nstr, "hit_count": len(hits), "hits_by_row": by_row,
                      "hits": hits[:50], "status": "RED" if hits else "GREEN"}, ensure_ascii=False, indent=1))
    return 1 if hits else 0


if __name__ == "__main__":
    raise SystemExit(main())
