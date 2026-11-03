#!/usr/bin/env python3
"""Keep the landed outputs that exist only in a lane's scratch directory, and name the durable roots that hold the others.

Input is a landed-manifest build's `not_matching` list. Each entry is matched BY DIGEST against the files of the scratch
roots given; a match is copied to <Book>/close/landed/<attempt>/<listed path> (write-once, digest checked), so the landed
builder then finds it. Durable roots (--durable) are hashed the same way to say which directories to name in LANDED_ROOTS.
Only an exact digest match counts; what matches nothing is printed for the close report, never invented. Book-agnostic (TE-7).

usage (from SP): python -B campaign/close_kit/retain_scratch_outputs.py --book BOOK --probe MANIFEST
                 --durable DIR [--durable ...] --scratch DIR [--scratch ...] [--dry-run]
"""
import argparse
import collections
import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SP = Path(__file__).resolve().parents[2]


def digests(root, want):
    for p in Path(root).rglob("*"):
        if p.is_file() and p.stat().st_size < 30_000_000:
            b = p.read_bytes()
            h = hashlib.sha256(b).hexdigest()
            if h in want:
                yield h, p, b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True)
    ap.add_argument("--probe", required=True)
    ap.add_argument("--durable", action="append", default=[])
    ap.add_argument("--scratch", action="append", default=[])
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    rows = json.loads(Path(a.probe).read_text(encoding="utf-8"))["not_matching"]
    want = {r["sha256"] for r in rows}
    durable, found = {}, {}
    for d in a.durable:
        for h, p, _ in digests(SP / d, want):
            durable.setdefault(h, p.parent.relative_to(SP).as_posix())
    left = want - set(durable)
    for s in a.scratch:
        for h, p, b in digests(s, left):
            found.setdefault(h, b)
    written, attempts, missing = 0, set(), []
    for r in rows:
        h = r["sha256"]
        if h in durable:
            continue
        if h not in found:
            missing.append({"attempt": r["attempt_id"], "path": r["listed_path"]})
            continue
        rel = Path(a.book) / "close" / "landed" / r["attempt_id"] / Path(r["listed_path"].replace("\\", "/"))
        attempts.add((Path(a.book) / "close" / "landed" / r["attempt_id"]).as_posix())
        target = SP / rel
        if target.exists() and target.read_bytes() != found[h]:
            raise SystemExit("REFUSED: %s exists with different bytes" % rel)
        if not a.dry_run and not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(found[h])
            written += 1
    roots = sorted(set(durable.values())) + sorted(attempts)
    print(json.dumps({"durable_rows": sum(r["sha256"] in durable for r in rows), "copied": written, "dry_run": a.dry_run,
                      "landed_roots": roots, "missing": missing,
                      "durable_by_dir": collections.Counter(durable.values()).most_common()}, ensure_ascii=False))


if __name__ == "__main__":
    main()
