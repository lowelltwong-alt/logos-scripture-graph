#!/usr/bin/env python3
"""Combine the eleven Ezekiel writer parts into one draft corpus and PROVE whole-book tiling.

Per-part tiling was proven at landing. That does not prove the book: two parts can each tile their own range
perfectly and still leave a gap or an overlap between them if a range in writer_parts.json were wrong. So this
re-derives the whole WEB verse sequence 1:1 -> 48:35 from verse_inventory.json and checks the COMBINED rows against
it - every verse exactly once.

It never mutates a part draft. It refuses to combine while any part is missing, and names the missing parts.
chunk_index_in_book is renumbered globally in part order; decision_id is left untouched, since PNN-xxx is already
unique per part and every review packet will cite it.

Usage: _combine_writer_parts.py [--out writer/draft_rows_combined.jsonl]
"""
import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SP = Path(__file__).resolve().parent


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="writer/draft_rows_combined.jsonl")
    a = ap.parse_args()

    parts = json.loads((SP / "writer_parts.json").read_text(encoding="utf-8"))["rows"]
    inv = {int(k): v for k, v in
           json.loads((SP / "verse_inventory.json").read_text(encoding="utf-8"))["chapters"].items()}
    book = [(c, v) for c in sorted(inv) for v in range(1, inv[c] + 1)]

    missing = [p["part_id"] for p in parts if not (SP / "writer" / ("draft_%s.jsonl" % p["part_id"])).is_file()]
    if missing:
        print(json.dumps({"verdict": "REFUSED", "why": "parts not yet durable", "missing": missing},
                         ensure_ascii=False, indent=1))
        return 1

    rows, inputs = [], {}
    for p in parts:
        f = SP / "writer" / ("draft_%s.jsonl" % p["part_id"])
        inputs[f.name] = sha(f)
        rows += [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]

    problems = []
    ids = [r.get("decision_id") for r in rows]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        problems.append("duplicate decision_id: %s" % dup[:10])

    seen = {}
    for r in rows:
        m = re.match(r"Ezek\.(\d+)\.(\d+)-Ezek\.(\d+)\.(\d+)$", r.get("span", ""))
        if not m:
            problems.append("%s: unparseable span" % r.get("decision_id"))
            continue
        c1, v1, c2, v2 = (int(x) for x in m.groups())
        for c in range(c1, c2 + 1):
            for v in range((v1 if c == c1 else 1), (v2 if c == c2 else inv[c]) + 1):
                if (c, v) in seen:
                    problems.append("OVERLAP at Ezek.%d.%d (%s and %s)" % (c, v, seen[(c, v)], r["decision_id"]))
                seen[(c, v)] = r["decision_id"]
    gaps = [x for x in book if x not in seen]
    extra = [x for x in seen if x not in set(book)]
    if gaps:
        problems.append("GAP: %d verses uncovered, first %s" % (len(gaps), gaps[:5]))
    if extra:
        problems.append("OVERRUN: %d verses outside the book, first %s" % (len(extra), extra[:5]))

    # rows must also be in canonical order once combined
    starts = []
    for r in rows:
        m = re.match(r"Ezek\.(\d+)\.(\d+)-", r.get("span", ""))
        if m:
            starts.append((int(m.group(1)), int(m.group(2))))
    if starts != sorted(starts):
        problems.append("combined rows are not in canonical order")

    if problems:
        print(json.dumps({"verdict": "RED", "problems": problems[:30], "inputs": inputs},
                         ensure_ascii=False, indent=1))
        return 1

    for i, r in enumerate(rows, 1):
        r["chunk_index_in_book"] = i
    out = SP / a.out
    out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8", newline="\n")
    conf = {}
    for r in rows:
        conf[r.get("confidence")] = conf.get(r.get("confidence"), 0) + 1
    report = {
        "schema": "m8_combined_writer_rows.v1", "book": "Ezek", "built": datetime.now(timezone.utc).isoformat(),
        "rows": len(rows), "verses_covered": len(seen), "book_verses": len(book),
        "whole_book_tiling": "EXACT - every verse 1:1 -> 48:35 exactly once",
        "canonical_order": True, "confidence_spread": conf,
        "inputs": inputs, "output": a.out, "output_sha256": sha(out),
        "limit": "a deterministic combine proves coverage and order, not the quality of any seam",
    }
    (SP / "writer" / "draft_rows_combined.report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    report["verdict"] = "GREEN"
    print(json.dumps(report, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
