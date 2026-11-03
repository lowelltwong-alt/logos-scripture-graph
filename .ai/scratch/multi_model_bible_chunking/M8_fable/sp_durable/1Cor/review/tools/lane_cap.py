"""Lane cap (OW-31 / OW-32: three lanes or fewer per book in flight), counted BEFORE a launch.

in_flight(book_dir) reads every *attempt_receipts*.jsonl under the book directory and returns the execution ids that have
a launch row and no closing row. A closing row is any row whose record_kind is in CLOSING and whose execution_id or
amends_execution_id names the execution. A completion notification not yet recorded still counts as in flight, so the
orchestrator must record a landing before the next launch (fail closed).

Prevention for the 2026-10-20 finding: the cap lived only in the post-launch recorders, which run after the Agent call;
FIXUP-2 W1/W4 launched with W6/W3 still writing (four in flight), and Phase 0 T1-e2/T3-e2/C1/C2 ran four on 2026-10-15.
usage: lane_cap.py --book-dir DIR   (prints the in-flight list; exit 3 when three or more are in flight)
"""
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
CAP = 3
CLOSING = {"completion", "interruption", "abandon", "abandoned", "landing", "failed", "superseded"}


def in_flight(book_dir):
    launched, closed = [], set()
    for f in sorted(Path(book_dir).rglob("*attempt_receipts*.jsonl")):
        if ".pre_" in f.name:
            continue
        for line in f.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            k = r.get("record_kind")
            if k == "launch" and r.get("execution_id"):
                launched.append(r["execution_id"])
            elif k in CLOSING:
                for key in ("execution_id", "amends_execution_id"):
                    if r.get(key):
                        closed.add(r[key])
    return [x for x in launched if x not in closed]


if __name__ == "__main__":
    d = sys.argv[sys.argv.index("--book-dir") + 1]
    live = in_flight(d)
    print(json.dumps({"in_flight": live, "count": len(live), "cap": CAP}))
    sys.exit(3 if len(live) >= CAP else 0)
