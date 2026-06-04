#!/usr/bin/env python3
"""Validate required handoff files referenced in ROADMAP_STATE.yaml.

This intentionally uses a simple line-based scan so it can run before dependencies are installed.
For richer validation, install PyYAML and extend this script.
"""
from __future__ import annotations
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[2]
STATE = ROOT / "ROADMAP_STATE.yaml"

REQUIRED_SECTIONS = [
    "## Task", "## Agent", "## Files read", "## Files changed",
    "## Decisions made", "## Validation run", "## Known risks",
    "## Open questions", "## Next agent instruction"
]

def extract_handoff_paths(text: str) -> list[str]:
    return re.findall(r"required_handoff:\s*([^\n]+)", text)

def main() -> int:
    if not STATE.exists():
        print("Missing ROADMAP_STATE.yaml", file=sys.stderr)
        return 1
    paths = extract_handoff_paths(STATE.read_text(encoding="utf-8"))
    failures = []
    for raw in paths:
        rel = raw.strip().strip('"').strip("'")
        path = ROOT / rel
        if not path.exists():
            failures.append(f"Missing handoff: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        for section in REQUIRED_SECTIONS:
            if section not in text:
                failures.append(f"{rel}: missing section {section}")
    if failures:
        print("HANDOFF VALIDATION FAILED")
        for f in failures:
            print(f"- {f}")
        return 1
    print(f"Handoff validation passed for {len(paths)} referenced handoff path(s).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
