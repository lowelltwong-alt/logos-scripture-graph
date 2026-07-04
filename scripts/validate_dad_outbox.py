#!/usr/bin/env python3
"""Validate local DAD outbox candidate messages."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
OUTBOX = ROOT / ".digital-asset" / "mail" / "outbox.jsonl"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
T424_MESSAGE_ID = "msg-20260703-t424-rust-validation-layer"

REQUIRED_T424_ARTIFACTS = {
    ".ai/control/coding_runtime_language_preflight.yaml",
    "tools/logos_fast_validators/",
    "scripts/validate_coding_runtime_language_preflight.py",
    "scripts/validate_fast_jsonl.py",
    "scripts/validate_fast_canonical_scope.py",
    "docs/roadmap/T424_RUST_ACCELERATED_VALIDATION_LAYER.md",
}

REQUIRED_T424_ASSETS = {
    "asset-candidate:rust-fast-validator-leaf-cli",
    "asset-candidate:rust-first-coding-runtime-preflight",
    "asset-candidate:python-wrapper-rust-fallback-pattern",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "dad_override_local_authority",
    "theology_authority",
    "chunk_output",
    "reviewed_gold",
    "route_or_evaluator_behavior",
    "graph_retrieval_or_vector_truth",
}


class DadOutboxError(ValueError):
    """Raised when DAD outbox messages are invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise DadOutboxError(f"{_rel(path)}: missing DAD outbox")
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise DadOutboxError(f"{_rel(path)}:{line_no}: invalid JSON: {exc}") from exc
            if not isinstance(row, dict):
                raise DadOutboxError(f"{_rel(path)}:{line_no}: row must be a JSON object")
            rows.append(row)
    if not rows:
        raise DadOutboxError(f"{_rel(path)}: must contain at least one outbound message")
    return rows


def _require_string(row: dict[str, Any], key: str, label: str) -> str:
    value = row.get(key)
    if not isinstance(value, str) or not value.strip():
        raise DadOutboxError(f"{label}: {key} must be a non-empty string")
    return value.strip()


def _require_string_list(row: dict[str, Any], key: str, label: str) -> list[str]:
    value = row.get(key)
    if not isinstance(value, list) or not value:
        raise DadOutboxError(f"{label}: {key} must be a non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise DadOutboxError(f"{label}: {key} must contain only non-empty strings")
    return [str(item) for item in value]


def validate_dad_outbox(path: Path = OUTBOX) -> list[dict[str, Any]]:
    rows = _read_jsonl(path)
    seen: set[str] = set()
    by_id: dict[str, dict[str, Any]] = {}
    for row in rows:
        message_id = _require_string(row, "message_id", _rel(path))
        if message_id in seen:
            raise DadOutboxError(f"{_rel(path)}: duplicate message_id {message_id}")
        seen.add(message_id)
        by_id[message_id] = row
        label = f"{_rel(path)}:{message_id}"
        if row.get("direction") != "outbound":
            raise DadOutboxError(f"{label}: direction must be outbound")
        if row.get("from_repo") != "logos-scripture-graph":
            raise DadOutboxError(f"{label}: from_repo must be logos-scripture-graph")
        if row.get("to_hub") != "dad://hub/Digital-Assett-Directory":
            raise DadOutboxError(f"{label}: to_hub must be dad://hub/Digital-Assett-Directory")
        if row.get("trust_zone") != "candidate":
            raise DadOutboxError(f"{label}: trust_zone must be candidate")
        if row.get("requires_local_adoption") is not True:
            raise DadOutboxError(f"{label}: requires_local_adoption must be true")
        _require_string(row, "message_type", label)
        _require_string(row, "subject", label)
        _require_string(row, "summary", label)

    t424 = by_id.get(T424_MESSAGE_ID)
    if not t424:
        raise DadOutboxError(f"{_rel(path)}: missing required T424 DAD message {T424_MESSAGE_ID}")
    label = f"{_rel(path)}:{T424_MESSAGE_ID}"
    if t424.get("message_type") != "lesson_and_asset_candidate":
        raise DadOutboxError(f"{label}: message_type must be lesson_and_asset_candidate")
    if t424.get("task_id") != "T424":
        raise DadOutboxError(f"{label}: task_id must be T424")
    if t424.get("status") != "sent_candidate":
        raise DadOutboxError(f"{label}: status must be sent_candidate")
    if t424.get("local_adoption_required") is not True:
        raise DadOutboxError(f"{label}: local_adoption_required must be true")
    if t424.get("lesson_learned_slot") != ".digital-asset/lessons/t424_rust_validation_layer.yaml":
        raise DadOutboxError(f"{label}: lesson_learned_slot must point to the T424 lesson")
    if t424.get("context_map_entry") != "ctx-t424-rust-validation-layer":
        raise DadOutboxError(f"{label}: context_map_entry must be ctx-t424-rust-validation-layer")
    missing_artifacts = sorted(REQUIRED_T424_ARTIFACTS - set(_require_string_list(t424, "artifacts", label)))
    if missing_artifacts:
        raise DadOutboxError(f"{label}: missing artifacts {missing_artifacts}")
    missing_assets = sorted(REQUIRED_T424_ASSETS - set(_require_string_list(t424, "asset_candidates", label)))
    if missing_assets:
        raise DadOutboxError(f"{label}: missing asset_candidates {missing_assets}")
    missing_non_auth = sorted(REQUIRED_NON_AUTHORIZATIONS - set(_require_string_list(t424, "non_authorizations", label)))
    if missing_non_auth:
        raise DadOutboxError(f"{label}: missing non_authorizations {missing_non_auth}")

    front_door = FRONT_DOOR.read_text(encoding="utf-8")
    for needle in (".digital-asset/mail/", "lessons", "reusable assets", T424_MESSAGE_ID):
        if needle not in front_door:
            raise DadOutboxError(f"{_rel(FRONT_DOOR)}: missing DAD wiring string {needle!r}")

    return rows


def main() -> int:
    try:
        validate_dad_outbox()
    except DadOutboxError as exc:
        print(f"DAD outbox validation failed: {exc}", file=sys.stderr)
        return 1
    print("DAD outbox validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
