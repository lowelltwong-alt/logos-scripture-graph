#!/usr/bin/env python3
"""Validate T417 draft review packets stay non-authorizing prep artifacts."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRAFT_DIR = ROOT / ".ai" / "context" / "agent_work" / "T417" / "review_packet_drafts"
WORK_DIR = ROOT / ".ai" / "context" / "agent_work" / "T417"
STANDING_POLICY = ROOT / ".ai" / "control" / "standing_owner_escalation_policy.yaml"

REQUIRED_MARKERS = (
    "draft_pending_standing_policy",
    "Implementation allowed: false",
    "Output change authorized: false",
    "Reviewed gold promoted: false",
    "standing_owner_escalation_policy.yaml",
    "No reviewed gold is promoted.",
)

FORBIDDEN_MARKERS = (
    "eval/chunking_gold/",
    "Strengthened packet: true",
    "authorizes_chunk_output",
    "reviewed_gold_promoted: true",
)


class T417DraftPacketError(ValueError):
    """Raised when draft packets leak authority or miss traceability."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _discover_drafts() -> dict[str, Path]:
    drafts: dict[str, Path] = {}
    for path in sorted(DRAFT_DIR.glob("*_draft.md")):
        text = path.read_text(encoding="utf-8")
        match = re.search(r"T402-LC-\d+", text)
        if match:
            drafts[match.group(0)] = path
    return drafts


def _discover_trace_files() -> dict[str, Path]:
    traces: dict[str, Path] = {}
    for path in sorted(WORK_DIR.glob("claim_traceability_batch*.jsonl")):
        batch_id = path.stem.replace("claim_traceability_", "")
        traces[batch_id] = path
    return traces


def validate_drafts() -> list[str]:
    errors: list[str] = []
    if not STANDING_POLICY.is_file():
        errors.append(f"missing {_rel(STANDING_POLICY)}")

    drafts = _discover_drafts()
    if not drafts:
        errors.append(f"no draft packets found under {_rel(DRAFT_DIR)}")

    for candidate_id, path in drafts.items():
        if not path.is_file():
            errors.append(f"missing draft for {candidate_id}: {_rel(path)}")
            continue
        text = path.read_text(encoding="utf-8")
        if candidate_id not in text:
            errors.append(f"{_rel(path)}: missing candidate id {candidate_id}")
        for marker in REQUIRED_MARKERS:
            if marker not in text:
                errors.append(f"{_rel(path)}: missing marker {marker!r}")
        for marker in FORBIDDEN_MARKERS:
            if marker in text:
                errors.append(f"{_rel(path)}: forbidden marker {marker!r}")

    by_candidate: dict[str, list[dict]] = {cid: [] for cid in drafts}
    trace_files = _discover_trace_files()
    if not trace_files:
        errors.append(f"missing claim_traceability_batch*.jsonl under {_rel(WORK_DIR)}")

    for batch_id, trace_path in trace_files.items():
        if not trace_path.is_file():
            errors.append(f"missing {_rel(trace_path)}")
            continue
        batch_candidate_ids: set[str] = set()
        for line_no, line in enumerate(trace_path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"{_rel(trace_path)}:{line_no}: invalid JSON: {exc}")
                continue
            if not isinstance(row, dict):
                errors.append(f"{_rel(trace_path)}:{line_no}: row must be object")
                continue
            cid = row.get("candidate_id")
            if not isinstance(cid, str):
                errors.append(f"{_rel(trace_path)}:{line_no}: candidate_id required")
                continue
            batch_candidate_ids.add(cid)
            if cid in by_candidate:
                by_candidate[cid].append(row)
            if cid not in drafts:
                errors.append(f"{_rel(trace_path)}:{line_no}: unknown candidate {cid}")
            if row.get("non_authorizing") is not True:
                errors.append(f"claim row {row.get('claim_id')}: non_authorizing must be true")
            draft = row.get("draft_packet")
            if not isinstance(draft, str) or not draft.startswith(".ai/context/agent_work/T417/"):
                errors.append(f"claim row {row.get('claim_id')}: draft_packet must stay under T417 work dir")

        for cid in batch_candidate_ids:
            if cid not in drafts:
                errors.append(f"{batch_id}: trace references missing draft for {cid}")

    for cid, claim_rows in by_candidate.items():
        if not claim_rows:
            errors.append(f"{cid}: no claim traceability rows")
        elif not any(r.get("theology_sensitive") for r in claim_rows):
            errors.append(f"{cid}: expected at least one theology_sensitive escalation claim row")

    return errors


def main() -> int:
    errors = validate_drafts()
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print("OK: T417 draft review packets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
