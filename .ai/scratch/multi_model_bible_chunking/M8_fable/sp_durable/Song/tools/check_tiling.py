#!/usr/bin/env python3
"""Exact-tiling checker: decisions must cover a WEB verse range exactly —
no gaps, no overlaps, no out-of-range verses, canonical order. (WEB numbering;
spans are always WEB.)

Usage: check_tiling.py FILE --range Song.1.1-Song.2.20
FILE = part file ({"decisions":[...]}), rows JSONL, or list JSON. Spans read
from each decision's "span" field ("Song.C.V-Song.C.V" or single verse;
a leading "web:" prefix is tolerated).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from song_lib import expand_ref_token


def rows_from(p: Path):
    text = p.read_text(encoding="utf-8-sig")
    if p.suffix == ".jsonl":
        return [json.loads(l) for l in text.splitlines() if l.strip()]
    data = json.loads(text)
    if isinstance(data, dict):
        return data.get("decisions", [v for v in data.values() if isinstance(v, dict)])
    return data


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file", type=Path)
    ap.add_argument("--range", required=True, dest="rng")
    args = ap.parse_args()
    want = expand_ref_token(args.rng.replace("web:", ""))
    if not want:
        print(json.dumps({"status": "RED", "error": f"bad range {args.rng!r}"}))
        return 1
    problems = []
    seen: list[tuple[int, int]] = []
    prev_last = None
    for row in rows_from(args.file):
        did = row.get("decision_id", "?")
        span = str(row.get("span", "")).replace("web:", "")
        pairs = expand_ref_token(span)
        if not pairs:
            problems.append(f"{did}: unparseable span {span!r}")
            continue
        if prev_last is not None and pairs[0] <= prev_last:
            problems.append(f"{did}: out of canonical order or overlaps previous "
                            f"(starts {pairs[0]}, previous ended {prev_last})")
        prev_last = pairs[-1]
        seen.extend(pairs)
    dup = sorted({p for p in seen if seen.count(p) > 1})
    missing = sorted(set(want) - set(seen))
    outside = sorted(set(seen) - set(want))
    for label, items in (("overlap", dup), ("gap", missing), ("outside_range", outside)):
        for c, v in items[:20]:
            problems.append(f"{label}: Song.{c}.{v}")
    print(json.dumps({"file": args.file.name, "range": args.rng,
                      "verses_expected": len(want), "verses_covered": len(set(seen)),
                      "decisions": len([1 for _ in rows_from(args.file)]),
                      "problems": problems,
                      "status": "GREEN" if not problems else "RED"}, indent=1))
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
