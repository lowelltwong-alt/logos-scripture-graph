#!/usr/bin/env python3
"""Create or refresh the deterministic handoff file for a task.

Usage:
  python scripts/agent/force_handoff.py --task-id T001 --agent claude --stage start
"""
from __future__ import annotations
import argparse, datetime as dt, hashlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HANDOFF_ROOT = ROOT / ".ai" / "handoffs"
LEDGER = ROOT / ".ai" / "control" / "handoff_ledger.jsonl"
TASK_ID_RE = re.compile(r"^T\d{3,}$")  # matches schemas/handoff.schema.json

TEMPLATE = """# Task Handoff

## Task

- task_id: {task_id}
- title: 
- phase: 
- status: 

## Agent

- agent_name: {agent}
- mode: {mode}
- stage: {stage}
- updated_at: {timestamp}
- handoff_id: {handoff_id}

## Files read

- 

## Files changed

- 

## Decisions made

- 

## Validation run

- command: 
- result: 
- failures: 

## Known risks

- 

## Open questions

- 

## Next agent instruction

Write the exact next step another agent should take.
"""


def compute_id(task_id: str, stage: str, agent: str) -> str:
    raw = f"handoff-v1|{task_id}|{stage}|{agent}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--agent", required=True)
    parser.add_argument("--stage", required=True, choices=["start", "update", "final", "review"])
    parser.add_argument("--mode", default="")
    args = parser.parse_args()

    if not TASK_ID_RE.match(args.task_id):
        print(
            f"ERROR: task-id '{args.task_id}' must match ^T\\d{{3,}}$ "
            "(e.g. T305). See schemas/handoff.schema.json.",
            file=sys.stderr,
        )
        return 2

    task_dir = HANDOFF_ROOT / args.task_id
    task_dir.mkdir(parents=True, exist_ok=True)
    path = task_dir / "handoff.md"
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    handoff_id = compute_id(args.task_id, args.stage, args.agent)

    if not path.exists():
        path.write_text(TEMPLATE.format(
            task_id=args.task_id,
            agent=args.agent,
            mode=args.mode,
            stage=args.stage,
            timestamp=now,
            handoff_id=handoff_id,
        ), encoding="utf-8")
    else:
        text = path.read_text(encoding="utf-8")
        marker = f"\n\n---\n\n## Handoff refresh: {args.stage}\n\n- agent_name: {args.agent}\n- mode: {args.mode}\n- updated_at: {now}\n- handoff_id: {handoff_id}\n"
        path.write_text(text.rstrip() + marker, encoding="utf-8")

    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "event": "handoff_created_or_refreshed",
        "task_id": args.task_id,
        "agent": args.agent,
        "stage": args.stage,
        "handoff_path": str(path.relative_to(ROOT)),
        "handoff_id": handoff_id,
        "timestamp": now,
    }
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
    print(path.relative_to(ROOT))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
