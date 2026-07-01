#!/usr/bin/env python3
"""Validate multi-agent review cadence charter and cross-links."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
CADENCE = ROOT / ".ai" / "control" / "multi_agent_review_cadence.yaml"
LEDGER = ROOT / ".ai" / "control" / "agent_review_ledger.jsonl"
PROCESSOR = ROOT / ".ai" / "control" / "autonomous_corpus_processor.yaml"
PROGRAM = ROOT / ".ai" / "control" / "parallel_chunking_research_program.yaml"
TASK = ROOT / ".ai" / "tasks" / "T420.task.yaml"
CODEX_PROMPT = ROOT / ".ai/prompts/codex_daily_prep_review_prompt.md"
CLAUDE_PROMPT = ROOT / ".ai/prompts/claude_weekly_architecture_chunking_audit_prompt.md"
ROADMAP = ROOT / "docs/roadmap/T420_MULTI_AGENT_REVIEW_CADENCE.md"


class MultiAgentReviewCadenceError(ValueError):
    """Raised when cadence charter state is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise MultiAgentReviewCadenceError(f"{_rel(path)}: expected YAML mapping")
    return data


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _validate_cadence(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("task_id") != "T420":
        errors.append("cadence task_id must be T420")
    if data.get("review_ledger") != ".ai/control/agent_review_ledger.jsonl":
        errors.append("review_ledger path mismatch")
    for tier in ("cursor_tier", "codex_tier", "claude_tier", "owner_tier"):
        if not isinstance(data.get(tier), dict):
            errors.append(f"missing {tier}")
    codex = data.get("codex_tier", {})
    if codex.get("frequency") != "daily_recommended":
        errors.append("codex_tier.frequency must be daily_recommended")
    claude = data.get("claude_tier", {})
    if claude.get("frequency") != "weekly_recommended":
        errors.append("claude_tier.frequency must be weekly_recommended")
    verdicts = claude.get("verdict_enums", [])
    for required in ("APPROVE_WEEKLY", "HOLD_WITH_FINDINGS", "ESCALATE_OWNER"):
        if required not in verdicts:
            errors.append(f"claude_tier missing verdict {required}")
    authority = data.get("authority", {})
    if authority.get("authorizes_chunk_output_change"):
        errors.append("cadence must not authorize chunk output")
    return errors


def _validate_prompts() -> list[str]:
    errors: list[str] = []
    if not CODEX_PROMPT.is_file():
        errors.append(f"missing {_rel(CODEX_PROMPT)}")
    else:
        text = _read_text(CODEX_PROMPT)
        for phrase in ("APPROVE_PREP", "HOLD_WITH_FINDINGS"):
            if phrase not in text:
                errors.append(f"codex prompt missing {phrase}")
    if not CLAUDE_PROMPT.is_file():
        errors.append(f"missing {_rel(CLAUDE_PROMPT)}")
    else:
        text = _read_text(CLAUDE_PROMPT)
        for phrase in ("APPROVE_WEEKLY", "HOLD_WITH_FINDINGS", "ESCALATE_OWNER"):
            if phrase not in text:
                errors.append(f"claude prompt missing {phrase}")
    return errors


def _validate_cross_links() -> list[str]:
    errors: list[str] = []
    if not PROCESSOR.is_file():
        errors.append(f"missing {_rel(PROCESSOR)}")
    else:
        proc = _read_yaml(PROCESSOR)
        if proc.get("canonical_cadence") != ".ai/control/multi_agent_review_cadence.yaml":
            errors.append("processor must reference multi_agent_review_cadence.yaml")
    if not PROGRAM.is_file():
        errors.append(f"missing {_rel(PROGRAM)}")
    else:
        prog = _read_yaml(PROGRAM)
        cadence = prog.get("review_cadence", {})
        if cadence.get("canonical_control") != ".ai/control/multi_agent_review_cadence.yaml":
            errors.append("parallel program must reference cadence control")
    if not TASK.is_file():
        errors.append(f"missing {_rel(TASK)}")
    else:
        task = yaml.safe_load(_read_text(TASK))
        if not isinstance(task, dict) or task.get("cadence_control") != ".ai/control/multi_agent_review_cadence.yaml":
            errors.append("T420 task must reference cadence control")
    if not ROADMAP.is_file():
        errors.append(f"missing {_rel(ROADMAP)}")
    if not LEDGER.is_file():
        errors.append(f"missing {_rel(LEDGER)}")
    return errors


def _load_ledger() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    text = LEDGER.read_text(encoding="utf-8").strip()
    if not text:
        return rows
    for line_no, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise MultiAgentReviewCadenceError(f"ledger line {line_no}: invalid JSON: {exc}") from exc
        if not isinstance(row, dict):
            raise MultiAgentReviewCadenceError(f"ledger line {line_no}: expected object")
        rows.append(row)
    return rows


def _validate_staleness(rows: list[dict[str, Any]]) -> list[str]:
    warnings: list[str] = []
    now = datetime.now(timezone.utc)
    codex_rows = [r for r in rows if r.get("review_tier") == "codex_daily"]
    claude_rows = [r for r in rows if r.get("review_tier") == "claude_weekly"]
    if codex_rows:
        last = max(codex_rows, key=lambda r: r.get("date", ""))
        try:
            last_dt = datetime.strptime(str(last["date"]), "%Y-%m-%d").replace(tzinfo=timezone.utc)
            if now - last_dt > timedelta(hours=24):
                warnings.append("advisory: no codex_daily ledger entry within 24h")
        except ValueError:
            warnings.append("advisory: codex_daily ledger date not parseable")
    if claude_rows:
        last = max(claude_rows, key=lambda r: r.get("date", ""))
        try:
            last_dt = datetime.strptime(str(last["date"]), "%Y-%m-%d").replace(tzinfo=timezone.utc)
            if now - last_dt > timedelta(days=7):
                warnings.append("advisory: no claude_weekly ledger entry within 7d")
        except ValueError:
            warnings.append("advisory: claude_weekly ledger date not parseable")
    return warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-staleness", action="store_true", help="Warn if reviews are stale")
    args = parser.parse_args()
    try:
        if not CADENCE.is_file():
            raise MultiAgentReviewCadenceError(f"missing {_rel(CADENCE)}")
        data = _read_yaml(CADENCE)
        errors = _validate_cadence(data)
        errors.extend(_validate_prompts())
        errors.extend(_validate_cross_links())
        rows = _load_ledger()
        if args.check_staleness:
            warnings = _validate_staleness(rows)
            for warning in warnings:
                print(f"WARNING: {warning}", file=sys.stderr)
        if errors:
            raise MultiAgentReviewCadenceError("; ".join(errors))
        print("multi-agent review cadence: OK")
        return 0
    except MultiAgentReviewCadenceError as exc:
        print(f"multi-agent review cadence: FAIL — {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
