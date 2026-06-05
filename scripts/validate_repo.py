#!/usr/bin/env python3
"""Minimal repository validation.

This is intentionally dependency-light. It checks control-surface files and raw-source policy.
"""
from __future__ import annotations
from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = [
    "AI_FRONT_DOOR.md",
    "AI_TABLE_OF_CONTENTS.md",
    "ROADMAP.md",
    "ROADMAP_STATE.yaml",
    "HANDOFF_PROTOCOL.md",
    "docs/chunking/CHUNKING_DESIGN.md",
    "config/chunking/chunking_policy.yaml",
    "schemas/chunk.schema.json",
    ".ai/control/MASTER_CONTEXT.md",
    ".ai/control/MASTER_CONTEXT.lock.yaml",
    ".ai/control/PROJECT_CONTEXT.md",
    ".ai/control/PROJECT_STATUS.md",
    ".ai/control/current_focus.yaml",
    "config/governance/repository_link_contract.yaml",
    "config/agents/agent_hostile_policy.yaml",
]


def validate_json_files() -> list[str]:
    failures = []
    for path in ROOT.glob("schemas/*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            failures.append(f"Invalid JSON {path.relative_to(ROOT)}: {e}")
    return failures


def validate_required_files() -> list[str]:
    return [f"Missing required file: {p}" for p in REQUIRED if not (ROOT / p).exists()]


def validate_raw_policy() -> list[str]:
    failures = []
    for p in (ROOT / "data" / "raw").rglob("*"):
        if p.is_file() and p.name.startswith("processed_"):
            failures.append(f"Processed-looking file in raw vault: {p.relative_to(ROOT)}")
    return failures


def main() -> int:
    failures = []
    failures += validate_required_files()
    failures += validate_json_files()
    failures += validate_raw_policy()
    if failures:
        print("REPO VALIDATION FAILED")
        for f in failures:
            print(f"- {f}")
        return 1
    print("Repo validation passed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
