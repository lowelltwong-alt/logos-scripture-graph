#!/usr/bin/env python3
"""Validate local DAD outbox candidate messages."""
from __future__ import annotations

import json
import sys
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
CANDIDATE_FIXTURE = ROOT / "tests" / "fixtures" / "dad" / "candidate_messages.jsonl"
RUNTIME_OUTBOX = ROOT / ".digital-asset" / "mail" / "outbox.jsonl"
CONTEXT_MAP = ROOT / ".digital-asset" / "context-map.json"
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

LESSON_REQUIRED_NON_AUTHORIZATIONS = {"dad_override_local_authority"}
CONTEXT_REQUIRED_NON_AUTHORIZATIONS = {"dad_override_local_authority"}


class DadOutboxError(ValueError):
    """Raised when DAD outbox messages are invalid."""


LESSON_MESSAGE_TYPES = {"lesson_candidate", "lesson_and_asset_candidate"}


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


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise DadOutboxError(f"{_rel(path)}: missing DAD context map")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise DadOutboxError(f"{_rel(path)}: invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise DadOutboxError(f"{_rel(path)}: expected a JSON object")
    return data


def _read_yaml_mapping(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise DadOutboxError(f"{_rel(path)}: missing DAD lesson slot")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise DadOutboxError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise DadOutboxError(f"{_rel(path)}: expected a YAML mapping")
    return data


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


def _resolve_dad_lesson_slot(value: str, label: str) -> Path:
    normalized = value.replace("\\", "/").strip()
    posix_path = PurePosixPath(normalized)
    if posix_path.is_absolute() or ".." in posix_path.parts:
        raise DadOutboxError(f"{label}: lesson_learned_slot must be a safe repo-relative path")
    if not normalized.startswith(".digital-asset/lessons/"):
        raise DadOutboxError(f"{label}: lesson_learned_slot must stay under .digital-asset/lessons/")
    if posix_path.suffix not in {".yaml", ".yml"}:
        raise DadOutboxError(f"{label}: lesson_learned_slot must be a YAML file")
    return ROOT / Path(*posix_path.parts)


def validate_dad_outbox(
    path: Path = CANDIDATE_FIXTURE,
    *,
    require_historical_contract: bool = True,
) -> list[dict[str, Any]]:
    rows = _read_jsonl(path)
    context_map = _read_json(CONTEXT_MAP)
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
        _validate_candidate_message(row, label)
        _validate_lesson_slot(row, label)
        _validate_context_map_entry(row, label, context_map)

    if require_historical_contract:
        _validate_t424_contract_message(path, by_id)

        front_door = FRONT_DOOR.read_text(encoding="utf-8")
        for needle in (".digital-asset/mail/", "lessons", "reusable assets", T424_MESSAGE_ID):
            if needle not in front_door:
                raise DadOutboxError(f"{_rel(FRONT_DOOR)}: missing DAD wiring string {needle!r}")

    return rows


def validate_runtime_outbox_if_present(path: Path = RUNTIME_OUTBOX) -> list[dict[str, Any]]:
    if not path.exists() or not path.read_text(encoding="utf-8").strip():
        return []
    return validate_dad_outbox(path, require_historical_contract=False)


def _validate_candidate_message(row: dict[str, Any], label: str) -> None:
    """Validate generic DAD candidate-message safety without assuming a task id."""
    if row.get("local_adoption_required") is not None and row.get("local_adoption_required") is not True:
        raise DadOutboxError(f"{label}: local_adoption_required must be true when present")
    message_type = row.get("message_type")
    if message_type in LESSON_MESSAGE_TYPES:
        _require_string(row, "task_id", label)
        non_authorizations = _require_string_list(row, "non_authorizations", label)
        if "dad_override_local_authority" not in set(non_authorizations):
            raise DadOutboxError(f"{label}: lesson messages must deny dad_override_local_authority")
    if "artifacts" in row:
        _require_string_list(row, "artifacts", label)
    if "asset_candidates" in row:
        _require_string_list(row, "asset_candidates", label)
    if "follow_up_messages_expected" in row:
        _require_string_list(row, "follow_up_messages_expected", label)


def _validate_lesson_slot(row: dict[str, Any], label: str) -> None:
    slot = row.get("lesson_learned_slot")
    if slot is None:
        return
    if not isinstance(slot, str) or not slot.strip():
        raise DadOutboxError(f"{label}: lesson_learned_slot must be a non-empty string when present")

    slot_path = _resolve_dad_lesson_slot(slot, label)
    data = _read_yaml_mapping(slot_path)
    if data.get("object_type") != "dad_lesson_learned_slot":
        raise DadOutboxError(f"{_rel(slot_path)}: object_type must be dad_lesson_learned_slot")
    if data.get("schema_version") != "dad_lesson_learned_slot.v0.1":
        raise DadOutboxError(f"{_rel(slot_path)}: schema_version must be dad_lesson_learned_slot.v0.1")
    if data.get("source_repo") != "logos-scripture-graph":
        raise DadOutboxError(f"{_rel(slot_path)}: source_repo must be logos-scripture-graph")
    if data.get("trust_zone") != "candidate":
        raise DadOutboxError(f"{_rel(slot_path)}: trust_zone must be candidate")
    if data.get("local_adoption_required") is not True:
        raise DadOutboxError(f"{_rel(slot_path)}: local_adoption_required must be true")
    if data.get("task_id") != row.get("task_id"):
        raise DadOutboxError(f"{_rel(slot_path)}: task_id must match outbox row")
    if data.get("source_outbox_message_id") != row.get("message_id"):
        raise DadOutboxError(f"{_rel(slot_path)}: source_outbox_message_id must match outbox row")
    if row.get("context_map_entry") and data.get("context_map_entry") != row.get("context_map_entry"):
        raise DadOutboxError(f"{_rel(slot_path)}: context_map_entry must match outbox row")
    if not isinstance(data.get("extra_context"), str) or not data["extra_context"].strip():
        raise DadOutboxError(f"{_rel(slot_path)}: extra_context must record why this lesson matters")

    non_authorizations = set(_require_string_list(data, "non_authorizations", _rel(slot_path)))
    missing_non_auth = sorted(LESSON_REQUIRED_NON_AUTHORIZATIONS - non_authorizations)
    if missing_non_auth:
        raise DadOutboxError(f"{_rel(slot_path)}: missing non_authorizations {missing_non_auth}")


def _validate_context_map_entry(row: dict[str, Any], label: str, context_map: dict[str, Any]) -> None:
    context_id = row.get("context_map_entry")
    if context_id is None:
        return
    if not isinstance(context_id, str) or not context_id.strip():
        raise DadOutboxError(f"{label}: context_map_entry must be a non-empty string when present")
    if context_map.get("schema_version") != "dad_context_map.v0.1":
        raise DadOutboxError(f"{_rel(CONTEXT_MAP)}: schema_version must be dad_context_map.v0.1")
    contexts = context_map.get("contexts")
    if not isinstance(contexts, list) or not contexts:
        raise DadOutboxError(f"{_rel(CONTEXT_MAP)}: contexts must be a non-empty list")
    by_context_id = {
        context.get("context_id"): context
        for context in contexts
        if isinstance(context, dict) and isinstance(context.get("context_id"), str)
    }
    context = by_context_id.get(context_id)
    if not isinstance(context, dict):
        raise DadOutboxError(f"{_rel(CONTEXT_MAP)}: missing context_map_entry {context_id}")
    if context.get("task_id") != row.get("task_id"):
        raise DadOutboxError(f"{_rel(CONTEXT_MAP)}:{context_id}: task_id must match outbox row")
    if context.get("outbox_message_id") != row.get("message_id"):
        raise DadOutboxError(f"{_rel(CONTEXT_MAP)}:{context_id}: outbox_message_id must match outbox row")
    if row.get("lesson_learned_slot") and context.get("lesson_learned_slot") != row.get("lesson_learned_slot"):
        raise DadOutboxError(f"{_rel(CONTEXT_MAP)}:{context_id}: lesson_learned_slot must match outbox row")
    if context.get("trust_zone") != "candidate":
        raise DadOutboxError(f"{_rel(CONTEXT_MAP)}:{context_id}: trust_zone must be candidate")
    if context.get("local_adoption_required") is not True:
        raise DadOutboxError(f"{_rel(CONTEXT_MAP)}:{context_id}: local_adoption_required must be true")
    if not isinstance(context.get("extra_context"), str) or not context["extra_context"].strip():
        raise DadOutboxError(f"{_rel(CONTEXT_MAP)}:{context_id}: extra_context must be non-empty")

    non_authorizations = set(
        _require_string_list(context, "non_authorizations", f"{_rel(CONTEXT_MAP)}:{context_id}")
    )
    missing_non_auth = sorted(CONTEXT_REQUIRED_NON_AUTHORIZATIONS - non_authorizations)
    if missing_non_auth:
        raise DadOutboxError(f"{_rel(CONTEXT_MAP)}:{context_id}: missing non_authorizations {missing_non_auth}")


def _validate_t424_contract_message(path: Path, by_id: dict[str, dict[str, Any]]) -> None:
    """Keep the T424 asset lesson contract explicit inside the broader outbox gate."""
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


def main() -> int:
    try:
        validate_dad_outbox(CANDIDATE_FIXTURE)
        validate_runtime_outbox_if_present()
    except DadOutboxError as exc:
        print(f"DAD outbox validation failed: {exc}", file=sys.stderr)
        return 1
    print("DAD outbox validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
