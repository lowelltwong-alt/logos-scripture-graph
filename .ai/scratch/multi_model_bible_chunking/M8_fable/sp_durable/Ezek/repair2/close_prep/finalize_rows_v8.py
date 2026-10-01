#!/usr/bin/env python3
"""FINALIZE pass for Ezekiel's close (the Lamentations precedent: set review_status on every row, no other field touched).

WHY BEFORE THE CHECKERS. The OW-6 final check binds its verdict to one corpus sha256, and Lamentations' close tool
refuses a corpus whose rows are not all `candidate_review_complete`. Setting the status after the checkers would move
the sha they bound, so the pass runs first and the checkers judge the bytes that will be assembled (OW-26).

WHAT IT DOES. Reads the live corpus at its pinned sha, replaces the one serialised `"review_status": "pending"` in each
line with `"review_status": "candidate_review_complete"` - a byte-level replace, not a re-serialisation, so no key
order, escape or spacing can drift - and writes a NEW file. It never overwrites: an existing output with the same bytes
is reported and left; with different bytes it refuses. Then it re-parses both files and asserts every row is equal
field-for-field except review_status.

usage: finalize_rows_v8.py [--check]      --check builds in memory and compares against the written file
"""
import hashlib
import json
import sys
from pathlib import Path

EZ = Path(__file__).resolve().parents[2]
SRC = EZ / "repair" / "rows_v7_cwo24.jsonl"
SRC_PIN = "e24048cc869f1493ac5d65a7e37fd6457909d2848da31583e9d55211601611a7"
OUT = EZ / "rows_v8_final.jsonl"
OLD = b'"review_status": "pending"'
NEW = b'"review_status": "candidate_review_complete"'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def build():
    src = SRC.read_bytes()
    if sha(src) != SRC_PIN:
        raise SystemExit("REFUSED: the live corpus moved since it was pinned: %s" % sha(src))
    lines = src.split(b"\n")
    out = []
    for i, ln in enumerate(lines):
        if not ln.strip():
            out.append(ln)
            continue
        if ln.count(OLD) != 1:
            raise SystemExit("REFUSED: line %d carries the pending status %d times, not once" % (i + 1, ln.count(OLD)))
        out.append(ln.replace(OLD, NEW))
    return src, b"\n".join(out)


def main():
    src, new = build()
    if "--check" in sys.argv:
        print("MATCH" if OUT.is_file() and OUT.read_bytes() == new else "DIFFERS")
        return
    if OUT.exists():
        if OUT.read_bytes() != new:
            raise SystemExit("REFUSED: %s exists with different bytes; never overwritten" % OUT.name)
        print("%s already present with the same bytes - not rewritten" % OUT.name)
    else:
        OUT.write_bytes(new)
    a = [json.loads(l) for l in src.decode("utf-8").splitlines() if l.strip()]
    b = [json.loads(l) for l in OUT.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len(a) == len(b) == 138, (len(a), len(b))
    for x, y in zip(a, b):
        assert y["review_status"] == "candidate_review_complete"
        assert {k: v for k, v in x.items() if k != "review_status"} == {k: v for k, v in y.items() if k != "review_status"}
    assert [r["chunk_index_in_book"] for r in b] == list(range(1, len(b) + 1))
    print(json.dumps({"source": str(SRC.relative_to(EZ)), "source_sha256": SRC_PIN, "output": OUT.name,
                      "output_sha256": sha(OUT.read_bytes()), "rows": len(b),
                      "fields_changed": ["review_status: pending -> candidate_review_complete"],
                      "every_other_field_equal": True}, indent=1))


if __name__ == "__main__":
    main()
