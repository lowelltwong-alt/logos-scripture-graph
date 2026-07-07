#!/usr/bin/env python3
"""Validate the AI-agnostic Rust subagent charter and DAD report wiring."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
CHARTER = ROOT / ".ai" / "control" / "ai_agnostic_rust_subagent_charter.yaml"
AGENT_ROLES = ROOT / "config" / "agents" / "agent_roles.yaml"
MODEL_ROUTING = ROOT / "config" / "agents" / "model_routing.yaml"
CADENCE = ROOT / ".ai" / "control" / "multi_agent_review_cadence.yaml"
OUTBOX = ROOT / ".digital-asset" / "mail" / "outbox.jsonl"
CONTEXT_MAP = ROOT / ".digital-asset" / "context-map.json"
VALIDATE_ALL = ROOT / "scripts" / "validate_all.py"

REQUIRED_ROLES = {
    "rust_architecture_reviewer": "reasoner",
    "outside_rust_research_scout": "reasoner",
    "rust_engineer": "executor",
    "rust_qa_tester": "executor",
    "dad_lesson_reporter": "orchestrator",
}

REQUIRED_AUTHORITY_FALSE = {
    "authorizes_rust_observation_or_validation_work",
    "authorizes_reviewed_gold_promotion",
    "authorizes_child_spans",
    "authorizes_chunk_output_change",
    "authorizes_route_behavior_change",
    "authorizes_evaluator_change",
    "authorizes_graph_retrieval_vector_truth",
    "authorizes_embeddings_or_indexes",
    "authorizes_boundary_import",
    "authorizes_backend_or_profile_promotion",
    "authorizes_source_or_manuscript_rows",
    "authorizes_preferred_reading_or_source_tradition",
    "authorizes_canon_scope_change",
    "authorizes_theology_authority_change",
    "authorizes_dad_override_local_authority",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "model_vendor_lock_in",
    "rust_for_rust_sake",
    "rust_validator_as_governance_authority",
    "dad_override_local_authority",
    "reviewed_gold_promotion",
    "child_span_selection",
    "chunk_output_change",
    "route_behavior_change",
    "evaluator_change",
    "graph_retrieval_or_vector_truth",
    "embeddings_or_indexes",
    "boundary_import",
    "backend_or_profile_promotion",
    "preferred_reading_or_source_tradition",
    "canon_scope_change",
    "source_or_manuscript_row_population",
    "theology_authority",
}

REQUIRED_ROUTING = {
    "rust_architecture_review": "reasoner",
    "rust_external_research": "reasoner",
    "rust_bounded_implementation": "executor",
    "rust_parity_qa": "executor",
    "dad_lesson_reporting": "orchestrator",
}

ROLE_REQUIRED_FIELDS = {
    "capability_profile",
    "purpose",
    "required_inputs",
    "required_outputs",
    "stop_conditions",
    "must_not",
}

REGISTRY_REQUIRED_FIELDS = {
    "purpose",
    "ai_agnostic",
    "capability_profile",
    "canonical_cadence",
    "allowed_paths",
    "forbidden_actions",
    "required_outputs",
    "non_authorizations",
}

BANNED_ROLE_TEXT = {
    "preferred_model",
    "model_id",
    "claude",
    "openai",
    "gpt",
    "gemini",
    "cursor",
    "sonnet",
    "opus",
}


class RustSubagentCharterError(ValueError):
    """Raised when the Rust subagent charter is invalid."""


def _rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path, root: Path) -> dict[str, Any]:
    if not path.exists():
        raise RustSubagentCharterError(f"{_rel(path, root)}: missing")
    text = path.read_text(encoding="utf-8")
    data: dict[str, Any] = {}
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            header = yaml.safe_load(parts[1]) or {}
            body = yaml.safe_load(parts[2]) or {}
            if not isinstance(header, dict) or not isinstance(body, dict):
                raise RustSubagentCharterError(f"{_rel(path, root)}: expected YAML mappings")
            data.update(header)
            data.update(body)
            return data
    loaded = yaml.safe_load(text)
    if not isinstance(loaded, dict):
        raise RustSubagentCharterError(f"{_rel(path, root)}: expected YAML mapping")
    return loaded


def _read_json(path: Path, root: Path) -> dict[str, Any]:
    if not path.exists():
        raise RustSubagentCharterError(f"{_rel(path, root)}: missing")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RustSubagentCharterError(f"{_rel(path, root)}: expected JSON object")
    return data


def _read_jsonl(path: Path, root: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise RustSubagentCharterError(f"{_rel(path, root)}: missing")
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        if not isinstance(row, dict):
            raise RustSubagentCharterError(f"{_rel(path, root)}:{line_no}: expected JSON object")
        rows.append(row)
    return rows


def _require_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise RustSubagentCharterError(f"{label}: expected non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise RustSubagentCharterError(f"{label}: list must contain only non-empty strings")
    return list(value)


def _stringify(value: Any) -> str:
    return json.dumps(value, sort_keys=True, default=str).lower()


def _reject_vendor_lock(role_id: str, role_data: dict[str, Any], location: str) -> None:
    text = _stringify(role_data)
    found = sorted(token for token in BANNED_ROLE_TEXT if token in text)
    if found:
        raise RustSubagentCharterError(f"{location}:{role_id}: vendor/model-specific token(s): {found}")


def _validate_charter(charter: dict[str, Any], root: Path) -> None:
    if charter.get("object_type") != "ai_agnostic_rust_subagent_charter":
        raise RustSubagentCharterError("charter object_type mismatch")
    if charter.get("schema_version") != "ai_agnostic_rust_subagent_charter.v1":
        raise RustSubagentCharterError("charter schema_version mismatch")
    if charter.get("task_id") != "T458":
        raise RustSubagentCharterError("charter task_id must be T458")
    if charter.get("model_routing_policy") != "config/agents/model_routing.yaml":
        raise RustSubagentCharterError("charter model_routing_policy mismatch")
    if charter.get("role_registry") != "config/agents/agent_roles.yaml":
        raise RustSubagentCharterError("charter role_registry mismatch")

    principles = charter.get("principles")
    if not isinstance(principles, dict):
        raise RustSubagentCharterError("charter principles must be a mapping")
    for key in (
        "route_by_capability_profile_not_vendor_or_model_name",
        "rust_is_for_deterministic_leaf_work_when_worth_it",
        "python_pytest_remain_governance_orchestrator",
        "outside_research_is_candidate_input_only",
        "dad_reports_are_candidate_lessons_only",
    ):
        if principles.get(key) is not True:
            raise RustSubagentCharterError(f"charter principles.{key} must be true")

    authority = charter.get("authority")
    if not isinstance(authority, dict):
        raise RustSubagentCharterError("charter authority must be a mapping")
    for key in REQUIRED_AUTHORITY_FALSE:
        if authority.get(key) is not False:
            raise RustSubagentCharterError(f"charter authority.{key} must be false")

    non_auth = set(_require_list(charter.get("required_non_authorizations"), "required_non_authorizations"))
    missing = sorted(REQUIRED_NON_AUTHORIZATIONS - non_auth)
    if missing:
        raise RustSubagentCharterError(f"charter missing required_non_authorizations {missing}")

    roles = charter.get("roles")
    if not isinstance(roles, dict):
        raise RustSubagentCharterError("charter roles must be a mapping")
    missing_roles = sorted(set(REQUIRED_ROLES) - set(roles))
    if missing_roles:
        raise RustSubagentCharterError(f"charter missing roles {missing_roles}")
    for role_id, profile in REQUIRED_ROLES.items():
        role = roles.get(role_id)
        if not isinstance(role, dict):
            raise RustSubagentCharterError(f"charter role {role_id} must be a mapping")
        missing_fields = sorted(ROLE_REQUIRED_FIELDS - set(role))
        if missing_fields:
            raise RustSubagentCharterError(f"charter role {role_id} missing {missing_fields}")
        if role.get("capability_profile") != profile:
            raise RustSubagentCharterError(f"charter role {role_id} profile mismatch")
        if role.get("role_registry_key") != role_id:
            raise RustSubagentCharterError(f"charter role {role_id} registry key mismatch")
        _require_list(role.get("required_inputs"), f"charter role {role_id}.required_inputs")
        _require_list(role.get("required_outputs"), f"charter role {role_id}.required_outputs")
        _require_list(role.get("stop_conditions"), f"charter role {role_id}.stop_conditions")
        must_not = set(_require_list(role.get("must_not"), f"charter role {role_id}.must_not"))
        if "choose_vendor_or_model_name" not in must_not:
            raise RustSubagentCharterError(f"charter role {role_id} must deny vendor/model choice")
        _reject_vendor_lock(role_id, role, "charter")

    if charter.get("dad_context_map_entry") != "ctx-t458-ai-agnostic-rust-subagent-charter":
        raise RustSubagentCharterError("charter DAD context id mismatch")
    if charter.get("dad_outbox_message_id") != "msg-20260706-t458-ai-agnostic-rust-subagent-charter":
        raise RustSubagentCharterError("charter DAD outbox id mismatch")
    lesson_slot = charter.get("dad_lesson_slot")
    if lesson_slot != ".digital-asset/lessons/t458_ai_agnostic_rust_subagent_charter.yaml":
        raise RustSubagentCharterError("charter DAD lesson slot mismatch")
    if not (root / lesson_slot).is_file():
        raise RustSubagentCharterError("charter DAD lesson slot missing")


def _validate_agent_roles(registry: dict[str, Any]) -> None:
    roles = registry.get("roles")
    if not isinstance(roles, dict):
        raise RustSubagentCharterError("agent_roles roles must be a mapping")
    for role_id, profile in REQUIRED_ROLES.items():
        role = roles.get(role_id)
        if not isinstance(role, dict):
            raise RustSubagentCharterError(f"agent_roles missing {role_id}")
        missing_fields = sorted(REGISTRY_REQUIRED_FIELDS - set(role))
        if missing_fields:
            raise RustSubagentCharterError(f"agent_roles {role_id} missing {missing_fields}")
        if role.get("ai_agnostic") is not True:
            raise RustSubagentCharterError(f"agent_roles {role_id}.ai_agnostic must be true")
        if role.get("capability_profile") != profile:
            raise RustSubagentCharterError(f"agent_roles {role_id} profile mismatch")
        if role.get("canonical_cadence") != ".ai/control/ai_agnostic_rust_subagent_charter.yaml":
            raise RustSubagentCharterError(f"agent_roles {role_id} cadence mismatch")
        _require_list(role.get("allowed_paths"), f"agent_roles {role_id}.allowed_paths")
        forbidden = set(_require_list(role.get("forbidden_actions"), f"agent_roles {role_id}.forbidden_actions"))
        _require_list(role.get("required_outputs"), f"agent_roles {role_id}.required_outputs")
        _require_list(role.get("non_authorizations"), f"agent_roles {role_id}.non_authorizations")
        _reject_vendor_lock(role_id, role, "agent_roles")
        if role_id == "rust_engineer":
            required_forbidden = {"write data/raw/", "write data/canonical/", "write eval/chunking_gold/"}
            if not required_forbidden <= forbidden:
                raise RustSubagentCharterError("rust_engineer missing protected-surface forbidden actions")
        if role_id == "outside_rust_research_scout":
            allowed = set(role.get("allowed_paths", []))
            forbidden_paths = {"tools/", "scripts/", ".ai/control/"}
            if allowed & forbidden_paths:
                raise RustSubagentCharterError("outside_rust_research_scout must not write sensitive paths")
        if role_id == "dad_lesson_reporter":
            non_auth = set(role.get("non_authorizations", []))
            if "dad_override_local_authority" not in non_auth:
                raise RustSubagentCharterError("dad_lesson_reporter must deny DAD override")


def _validate_model_routing(routing: dict[str, Any]) -> None:
    profiles = routing.get("profiles")
    if not isinstance(profiles, dict):
        raise RustSubagentCharterError("model_routing profiles must be a mapping")
    missing_profiles = sorted(set(REQUIRED_ROLES.values()) - set(profiles))
    if missing_profiles:
        raise RustSubagentCharterError(f"model_routing missing profiles {missing_profiles}")
    task_routing = routing.get("task_routing")
    if not isinstance(task_routing, dict):
        raise RustSubagentCharterError("model_routing task_routing must be a mapping")
    for task, profile in REQUIRED_ROUTING.items():
        row = task_routing.get(task)
        if not isinstance(row, dict) or row.get("profile") != profile:
            raise RustSubagentCharterError(f"model_routing {task} must route to {profile}")


def _validate_cadence(cadence: dict[str, Any]) -> None:
    rust = cadence.get("rust_subagent_cadence")
    if not isinstance(rust, dict):
        raise RustSubagentCharterError("multi-agent cadence missing rust_subagent_cadence")
    if rust.get("control") != ".ai/control/ai_agnostic_rust_subagent_charter.yaml":
        raise RustSubagentCharterError("rust_subagent_cadence control mismatch")
    if rust.get("routing") != "capability_profile_not_model_name":
        raise RustSubagentCharterError("rust_subagent_cadence routing must be capability-profile based")
    roles = set(_require_list(rust.get("roles"), "rust_subagent_cadence.roles"))
    missing = sorted(set(REQUIRED_ROLES) - roles)
    if missing:
        raise RustSubagentCharterError(f"rust_subagent_cadence missing roles {missing}")
    does_not = set(_require_list(rust.get("does_not_authorize"), "rust_subagent_cadence.does_not_authorize"))
    for required in ("theology_authority_change", "dad_override_local_authority", "graph_retrieval_or_vector_truth"):
        if required not in does_not:
            raise RustSubagentCharterError(f"rust_subagent_cadence missing non-authorization {required}")
    _reject_vendor_lock("rust_subagent_cadence", rust, "multi_agent_review_cadence")


def _validate_dad(charter: dict[str, Any], root: Path) -> None:
    message_id = str(charter.get("dad_outbox_message_id"))
    context_id = str(charter.get("dad_context_map_entry"))
    lesson_slot = str(charter.get("dad_lesson_slot"))

    rows = _read_jsonl(root / OUTBOX.relative_to(ROOT), root)
    by_id = {row.get("message_id"): row for row in rows}
    row = by_id.get(message_id)
    if not isinstance(row, dict):
        raise RustSubagentCharterError("T458 DAD outbox row missing")
    if row.get("message_type") != "lesson_candidate":
        raise RustSubagentCharterError("T458 DAD message_type must be lesson_candidate")
    if row.get("task_id") != "T458":
        raise RustSubagentCharterError("T458 DAD row task_id mismatch")
    if row.get("trust_zone") != "candidate":
        raise RustSubagentCharterError("T458 DAD row must stay candidate")
    if row.get("requires_local_adoption") is not True or row.get("local_adoption_required") is not True:
        raise RustSubagentCharterError("T458 DAD row must require local adoption")
    if row.get("context_map_entry") != context_id or row.get("lesson_learned_slot") != lesson_slot:
        raise RustSubagentCharterError("T458 DAD row context/lesson mismatch")
    non_auth = set(_require_list(row.get("non_authorizations"), "T458 DAD row non_authorizations"))
    for required in ("dad_override_local_authority", "model_vendor_lock_in", "rust_validator_as_governance_authority"):
        if required not in non_auth:
            raise RustSubagentCharterError(f"T458 DAD row missing non-authorization {required}")
    if "scout" not in str(row.get("extra_context", "")).lower():
        raise RustSubagentCharterError("T458 DAD row extra_context must mention scout findings")

    context = _read_json(root / CONTEXT_MAP.relative_to(ROOT), root)
    contexts = context.get("contexts")
    if not isinstance(contexts, list):
        raise RustSubagentCharterError("DAD context map contexts must be a list")
    context_rows = {item.get("context_id"): item for item in contexts if isinstance(item, dict)}
    ctx = context_rows.get(context_id)
    if not isinstance(ctx, dict):
        raise RustSubagentCharterError("T458 DAD context entry missing")
    if ctx.get("task_id") != "T458" or ctx.get("outbox_message_id") != message_id:
        raise RustSubagentCharterError("T458 DAD context linkage mismatch")
    if ctx.get("lesson_learned_slot") != lesson_slot:
        raise RustSubagentCharterError("T458 DAD context lesson mismatch")

    lesson = _read_yaml(root / lesson_slot, root)
    if lesson.get("object_type") != "dad_lesson_learned_slot":
        raise RustSubagentCharterError("T458 DAD lesson object_type mismatch")
    if lesson.get("task_id") != "T458" or lesson.get("source_outbox_message_id") != message_id:
        raise RustSubagentCharterError("T458 DAD lesson linkage mismatch")
    lesson_non_auth = set(_require_list(lesson.get("non_authorizations"), "T458 DAD lesson non_authorizations"))
    if "dad_override_local_authority" not in lesson_non_auth:
        raise RustSubagentCharterError("T458 DAD lesson must deny DAD override")


def _validate_validate_all(root: Path) -> None:
    path = root / VALIDATE_ALL.relative_to(ROOT)
    if not path.exists():
        raise RustSubagentCharterError("scripts/validate_all.py missing")
    text = path.read_text(encoding="utf-8")
    if "validate_ai_agnostic_rust_subagents.py" not in text:
        raise RustSubagentCharterError("validate_all.py must include validate_ai_agnostic_rust_subagents.py")


def validate_ai_agnostic_rust_subagents(root: Path = ROOT) -> None:
    root = root.resolve()
    charter = _read_yaml(root / CHARTER.relative_to(ROOT), root)
    _validate_charter(charter, root)
    _validate_agent_roles(_read_yaml(root / AGENT_ROLES.relative_to(ROOT), root))
    _validate_model_routing(_read_yaml(root / MODEL_ROUTING.relative_to(ROOT), root))
    _validate_cadence(_read_yaml(root / CADENCE.relative_to(ROOT), root))
    _validate_dad(charter, root)
    _validate_validate_all(root)


def main() -> int:
    try:
        validate_ai_agnostic_rust_subagents()
    except (RustSubagentCharterError, OSError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"AI-agnostic Rust subagent charter validation failed: {exc}", file=sys.stderr)
        return 1
    print("AI-agnostic Rust subagent charter validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
