"""Add one lane row to a book's close table by copying an existing row with named overrides.

usage: add_close_lane.py --table <Book>/close/close_lanes.v1.json --expect-before SHA --lane NEW --like OLD --set FILE [--dry-run]
Run from SP. FILE is a JSON object of the keys to override. Refuses a lane that exists, a stale digest, and an override key the
copied row does not hold. Replaces the table atomically."""
import argparse
import hashlib
import json
import os
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--table", required=True)
    ap.add_argument("--expect-before", required=True)
    ap.add_argument("--lane", required=True)
    ap.add_argument("--like", required=True)
    ap.add_argument("--set", required=True, dest="setf")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    p = Path(a.table)
    raw = p.read_bytes()
    if hashlib.sha256(raw).hexdigest() != a.expect_before:
        raise SystemExit("REFUSED: table digest is not the pinned one")
    t = json.loads(raw.decode("utf-8"))
    if a.lane in t["lanes"]:
        raise SystemExit("REFUSED: lane exists: %s" % a.lane)
    row = dict(t["lanes"][a.like])
    over = json.load(open(a.setf, encoding="utf-8"))
    bad = [k for k in over if k not in row]
    if bad:
        raise SystemExit("REFUSED: keys not on the copied row: %s" % bad)
    row.update(over)
    t["lanes"][a.lane] = row
    body = json.dumps(t, ensure_ascii=False, indent=1) + "\n"
    if a.dry_run:
        print("DRY", a.lane, "lanes", len(t["lanes"]), sorted(over))
        return
    tmp = p.with_suffix(".tmp")
    tmp.write_bytes(body.encode("utf-8"))
    os.replace(tmp, p)
    print("OK", a.lane, hashlib.sha256(p.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
