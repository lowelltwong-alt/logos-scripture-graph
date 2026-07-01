#!/usr/bin/env python3
"""Validate T417 batch2 draft review packets stay non-authorizing prep artifacts."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRAFT_DIR = ROOT / ".ai" / "context" / "agent_work" / "T417" / "review_packet_drafts"
TRACE = ROOT / ".ai" / "context" / "agent_work" / "T417" / "claim_traceability_batch2.jsonl"
STANDING_POLICY = ROOT / ".ai" / "control" / "standing_owner_escalation_policy.yaml"

DRAFTS = {
    "T402-LC-057": DRAFT_DIR / "phlm_opening_draft.md",
    "T402-LC-065": DRAFT_DIR / "jude_opening_draft.md",
    "T402-LC-032": DRAFT_DIR / "jonah_opening_draft.md",
}

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
    """Raised when batch2 draft packets leak authority or miss traceability."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def validate_drafts() -> list[str]:
    errors: list[str] = []
    if not STANDING_POLICY.is_file():
        errors.append(f"missing {_rel(STANDING_POLICY)}")

    for candidate_id, path in DRAFTS.items():
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

    if not TRACE.is_file():
        errors.append(f"missing {_rel(TRACE)}")
        return errors

    rows: list[dict] = []
    for line_no, line in enumerate(TRACE.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{_rel(TRACE)}:{line_no}: invalid JSON: {exc}")
            continue
        if not isinstance(row, dict):
            errors.append(f"{_rel(TRACE)}:{line_no}: row must be object")
            continue
        rows.append(row)

    by_candidate: dict[str, list[dict]] = {cid: [] for cid in DRAFTS}
    for row in rows:
        cid = row.get("candidate_id")
        if cid in by_candidate:
            by_candidate[cid].append(row)
        if row.get("non_authorizing") is not True:
            errors.append(f"claim row {row.get('claim_id')}: non_authorizing must be true")
        draft = row.get("draft_packet")
        if not isinstance(draft, str) or not draft.startswith(".ai/context/agent_work/T417/"):
            errors.append(f"claim row {row.get('claim_id')}: draft_packet must stay under T417 work dir")

    for cid, claim_rows in by_candidate.items():
        if not claim_rows:
            errors.append(f"{cid}: no claim traceability rows")
        if not any(r.get("theology_sensitive") for r in claim_rows):
            errors.append(f"{cid}: expected at least one theology_sensitive escalation claim row")

    return errors


def main() -> int:
    errors = validate_drafts()
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print("OK: T417 batch2 draft review packets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
