#!/usr/bin/env python3
"""Install a landed lane's other deliverables: each must match the digest the lane reported, and each target is write-once.

The result file names every deliverable with its sha256 (the shape every close lane returns). A name in --map that the
result does not list is refused; a target that exists with other bytes is refused, and nothing is written unless every
item passes. Book-agnostic (TE-7).

usage (from SP): python -B campaign/close_kit/install_close_outputs.py --result <landed result json> --out <lane OUT>
                 --map NAME=SP_RELATIVE_TARGET [--map ...] [--dry-run]
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SP = Path(__file__).resolve().parents[2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--result", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--map", action="append", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    listed = {d["name"]: d["sha256"] for d in json.loads(Path(a.result).read_text(encoding="utf-8"))["deliverables"]}
    plan = []
    for item in a.map:
        name, _, rel = item.partition("=")
        if name not in listed or not rel:
            raise SystemExit("REFUSED: %s is not a deliverable of this result" % name)
        data = (Path(a.out) / name).read_bytes()
        if hashlib.sha256(data).hexdigest() != listed[name]:
            raise SystemExit("REFUSED: %s does not match the digest the lane reported" % name)
        target = SP / rel
        if target.exists() and target.read_bytes() != data:
            raise SystemExit("REFUSED: %s exists with different bytes" % rel)
        plan.append((target, data, rel))
    for target, data, rel in plan:
        if not a.dry_run and not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    print(json.dumps({"installed": len(plan), "dry_run": a.dry_run, "targets": [p[2] for p in plan]}))


if __name__ == "__main__":
    main()
