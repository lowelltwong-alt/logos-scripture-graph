#!/usr/bin/env python3
"""Append a JSONL roadmap event.

Example:
  python scripts/agent/record_roadmap_event.py --event task_status_changed --task-id T001 --agent claude --reason "started work"
"""
from __future__ import annotations
import argparse, datetime as dt, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOG = ROOT / ".ai" / "control" / "roadmap_events.jsonl"

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--event", required=True)
    p.add_argument("--task-id", required=True)
    p.add_argument("--agent", required=True)
    p.add_argument("--reason", required=True)
    p.add_argument("--from-status", default=None)
    p.add_argument("--to-status", default=None)
    args = p.parse_args()
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    LOG.parent.mkdir(parents=True, exist_ok=True)
    obj = {
        "event": args.event,
        "task_id": args.task_id,
        "agent": args.agent,
        "reason": args.reason,
        "from": args.from_status,
        "to": args.to_status,
        "timestamp": now,
    }
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")
    print(json.dumps(obj, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
