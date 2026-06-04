#!/usr/bin/env python3
"""Validate the AI control plane: master context lock, front-door routing, handoffs.

CI gate — exit 0 = green, exit 1 = red.
Run: python scripts/validate_control_plane.py
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MASTER_CONTEXT = ROOT / ".ai" / "control" / "MASTER_CONTEXT.md"
MASTER_LOCK = ROOT / ".ai" / "control" / "MASTER_CONTEXT.lock.yaml"
PROJECT_STATUS = ROOT / ".ai" / "control" / "PROJECT_STATUS.md"
CURRENT_FOCUS = ROOT / ".ai" / "control" / "current_focus.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
README = ROOT / "README.md"
HANDOFF_PROTOCOL = ROOT / "HANDOFF_PROTOCOL.md"
CLAUDE_MD = ROOT / "CLAUDE.md"
AGENTS_MD = ROOT / "AGENTS.md"
ROADMAP_STATE = ROOT / "ROADMAP_STATE.yaml"

DATA_MAP = ROOT / ".ai" / "control" / "DATA_MAP.md"
ROUTING_GUIDE = ROOT / ".ai" / "handoffs" / "AGENT_ROUTING_GUIDE.md"

REQUIRED_CONTROL_FILES = [
    MASTER_CONTEXT,
    MASTER_LOCK,
    PROJECT_STATUS,
    CURRENT_FOCUS,
    DATA_MAP,
    ROUTING_GUIDE,
    ROOT / ".ai" / "context" / "README.md",
    ROOT / ".ai" / "context" / "agent_work",
    ROOT / ".ai" / "context" / "recommendations",
]

MASTER_REQUIRED_SECTIONS = [
    "GOVERNANCE: HUMAN-ONLY FILE",
    "## Non-negotiable architectural decisions",
    "## Identity chain",
    "## Explicit rejections",
]

FRONT_DOOR_REQUIRED_REFS = [
    "AI_FRONT_DOOR.md",
    ".ai/control/MASTER_CONTEXT.md",
    ".ai/control/PROJECT_STATUS.md",
    ".ai/control/DATA_MAP.md",
    "AGENT_ROUTING_GUIDE.md",
    "HANDOFF_PROTOCOL.md",
    "validate_control_plane.py",
    "MASTER_CONTEXT.md",
]

README_REQUIRED_REFS = [
    "AI_FRONT_DOOR.md",
    "MASTER_CONTEXT.md",
    "PROJECT_STATUS.md",
    "validate_control_plane.py",
]

MASTER_REQUIRED_PHRASES = [
    "AI agents: READ ONLY",
    "propose_master_context_change.py",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_text(encoding="utf-8").encode("utf-8"))
    return digest.hexdigest()


def parse_lock(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def validate_required_files() -> list[str]:
    failures = []
    for path in REQUIRED_CONTROL_FILES:
        if not path.exists():
            failures.append(f"Missing control-plane path: {path.relative_to(ROOT)}")
    return failures


def validate_master_context_sections() -> list[str]:
    if not MASTER_CONTEXT.exists():
        return ["MASTER_CONTEXT.md missing"]
    text = MASTER_CONTEXT.read_text(encoding="utf-8")
    failures = []
    for section in MASTER_REQUIRED_SECTIONS:
        if section not in text:
            failures.append(f"MASTER_CONTEXT.md missing section/phrase: {section}")
    for phrase in MASTER_REQUIRED_PHRASES:
        if phrase not in text:
            failures.append(f"MASTER_CONTEXT.md missing governance phrase: {phrase}")
    return failures


def validate_master_context_lock() -> list[str]:
    failures = []
    if not MASTER_CONTEXT.exists() or not MASTER_LOCK.exists():
        return failures
    lock = parse_lock(MASTER_LOCK)
    expected = lock.get("sha256", "")
    if not expected or expected == "PLACEHOLDER":
        failures.append(
            "MASTER_CONTEXT.lock.yaml has PLACEHOLDER sha256 — run: "
            "python scripts/agent/approve_master_context.py --approved-by human"
        )
        return failures
    actual = sha256_file(MASTER_CONTEXT)
    if actual.lower() != expected.lower():
        failures.append(
            "MASTER_CONTEXT.md changed without human lock update — "
            f"lock={expected[:16]}... actual={actual[:16]}... "
            "Human must review and run approve_master_context.py"
        )
    if lock.get("approved_by", "").lower() in {"", "null", "ai", "agent", "codex", "claude"}:
        failures.append("MASTER_CONTEXT.lock.yaml approved_by must be a human identifier, not an AI agent name alone")
    return failures


def validate_front_door_routing() -> list[str]:
    failures = []
    checks = [
        (FRONT_DOOR, FRONT_DOOR_REQUIRED_REFS, "AI_FRONT_DOOR.md"),
        (README, README_REQUIRED_REFS, "README.md"),
    ]
    for path, refs, label in checks:
        if not path.exists():
            failures.append(f"Missing {label}")
            continue
        text = path.read_text(encoding="utf-8")
        for ref in refs:
            if ref not in text:
                failures.append(f"{label} must reference: {ref}")
    for doc, label in [(CLAUDE_MD, "CLAUDE.md"), (AGENTS_MD, "AGENTS.md"), (HANDOFF_PROTOCOL, "HANDOFF_PROTOCOL.md")]:
        if not doc.exists():
            failures.append(f"Missing {label}")
            continue
        text = doc.read_text(encoding="utf-8")
        if "AI_FRONT_DOOR.md" not in text:
            failures.append(f"{label} must reference AI_FRONT_DOOR.md")
        if "MASTER_CONTEXT" not in text:
            failures.append(f"{label} must reference MASTER_CONTEXT")
    if PROJECT_STATUS.exists():
        text = PROJECT_STATUS.read_text(encoding="utf-8")
        if "MASTER_CONTEXT" not in text:
            failures.append("PROJECT_STATUS.md must reference MASTER_CONTEXT.md")
    return failures


def validate_current_focus() -> list[str]:
    failures = []
    if not CURRENT_FOCUS.exists():
        return ["Missing current_focus.yaml"]
    text = CURRENT_FOCUS.read_text(encoding="utf-8")
    for key in ("current_task:", "current_phase:", "primary_handoff:"):
        if key not in text:
            failures.append(f"current_focus.yaml missing {key}")
    match = re.search(r"primary_handoff:\s*(\S+)", text)
    if match:
        handoff = ROOT / match.group(1)
        if not handoff.exists():
            failures.append(f"current_focus primary_handoff not found: {match.group(1)}")
    return failures


def _iter_task_blocks(text: str):
    """Yield (task_id, fields) per task block in ROADMAP_STATE.yaml.

    Robust against task ordering: each `- id:` starts a new block and fields are
    only associated within that block (fixes CP-2 fail-open regex). Uses PyYAML
    when available; otherwise a deterministic structural scan.
    """
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(text) or {}
        for phase in (data.get("phases") or {}).values():
            for task in (phase or {}).get("tasks") or []:
                if not isinstance(task, dict) or "id" not in task:
                    continue
                yield str(task["id"]), {k: str(v) for k, v in task.items()}
        return
    except ImportError:
        pass

    current_id = None
    fields: dict[str, str] = {}
    id_re = re.compile(r"^\s*-\s*id:\s*(\S+)\s*$")
    kv_re = re.compile(r"^\s*([A-Za-z_]+):\s*(.+?)\s*$")
    for line in text.splitlines():
        m = id_re.match(line)
        if m:
            if current_id is not None:
                yield current_id, fields
            current_id, fields = m.group(1), {}
            continue
        if current_id is not None:
            kv = kv_re.match(line)
            if kv and kv.group(1) != "id":
                fields.setdefault(kv.group(1), kv.group(2).strip().strip('"').strip("'"))
    if current_id is not None:
        yield current_id, fields


def validate_active_task_handoff() -> list[str]:
    """Active in_progress tasks in ROADMAP_STATE must have a real next-agent instruction."""
    if not ROADMAP_STATE.exists():
        return ["Missing ROADMAP_STATE.yaml"]
    text = ROADMAP_STATE.read_text(encoding="utf-8")
    failures = []
    for task_id, fields in _iter_task_blocks(text):
        if fields.get("status") != "in_progress":
            continue
        handoff_rel = fields.get("required_handoff")
        if not handoff_rel:
            failures.append(f"Active task {task_id} has no required_handoff")
            continue
        handoff_path = ROOT / handoff_rel
        if not handoff_path.exists():
            failures.append(f"Active task {task_id} missing handoff: {handoff_rel}")
            continue
        handoff_text = handoff_path.read_text(encoding="utf-8")
        if "## Next agent instruction" not in handoff_text:
            failures.append(f"{handoff_rel}: missing Next agent instruction section")
        else:
            section = handoff_text.split("## Next agent instruction", 1)[1].strip()
            if len(section) < 40:
                failures.append(f"{handoff_rel}: Next agent instruction too short for active task {task_id}")
    return failures


def main() -> int:
    failures: list[str] = []
    failures += validate_required_files()
    failures += validate_master_context_sections()
    failures += validate_master_context_lock()
    failures += validate_front_door_routing()
    failures += validate_current_focus()
    failures += validate_active_task_handoff()

    if failures:
        print("CONTROL PLANE VALIDATION FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Control plane validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
