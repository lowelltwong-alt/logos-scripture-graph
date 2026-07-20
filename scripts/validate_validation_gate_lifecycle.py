#!/usr/bin/env python3
"""Validate lifecycle metadata for expensive or superseded validation gates."""
from __future__ import annotations

import sys
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
LIFECYCLE = ROOT / ".ai" / "control" / "validation_gate_lifecycle.yaml"
EXPANSION_CANDIDATES = ROOT / ".ai" / "control" / "validation_lifecycle_expansion_candidates.yaml"

ALLOWED_STATUSES = {"active", "active_generated_data", "shadow", "superseded", "retired"}
ALLOWED_MISSING_INPUT_BEHAVIOR = {
    "skip_when_ignored_generated_data_absent",
    "require_before_release",
    "not_applicable",
}
REQUIRED_AUTHORITY_FALSE = {
    "may_authorize_ad_hoc_validator_skip",
    "may_authorize_deleting_validator_without_replacement",
    "may_override_task_scope",
    "may_override_local_governance",
    "may_authorize_chunk_output",
    "may_authorize_reviewed_gold",
    "may_authorize_graph_or_retrieval_truth",
    "may_authorize_theology_authority",
}
REQUIRED_GENERATED_DATA_GATES = {
    "validate_source_metadata_research_atlas",
    "validate_apocalyptic_prophetic_intertext_dossier_queue",
    "validate_bible_verse_passage_coverage_inventory",
    "validate_1cor8_10_parent_evidence_packet",
    "validate_divine_capitalization_inventory",
    "validate_wj_marker_inventory",
    "validate_fast_canonical_qa",
    "validate_fast_word_token_signals",
    "validate_fast_canonical_scope",
    "validate_fast_jsonl_canonical",
    "build_t433_phlm_alignment_pilot_currentness",
    "build_t439_phlm_alignment_bridge_expansion_currentness",
}
REQUIRED_GLOBAL_NON_AUTHS = {
    "validation_speed_as_correctness",
    "rust_validator_as_governance_authority",
    "ad_hoc_skip_without_lifecycle_record",
    "delete_slow_gate_without_replacement_or_owner_gate",
    "dad_override_local_authority",
    "chunk_output",
    "reviewed_gold",
    "graph_retrieval_or_vector_truth",
    "theology_authority",
}
REQUIRED_EXPANSION_SURFACES = {
    "validation_gates",
    "generated_artifacts",
    "ai_prompt_packs",
    "scratch_outputs",
    "rust_leaf_tools",
    "data_sources_and_downloads",
    "schemas_and_contracts",
    "dad_messages_and_lessons",
}
REQUIRED_EXPANSION_NON_AUTHS = {
    "lifecycle_state_as_content_authority",
    "dad_override_local_authority",
    "lifecycle_retirement_without_replacement_or_owner_gate",
    "scratch_output_as_canon",
    "rust_speed_as_correctness",
    "theology_authority",
}


class ValidationGateLifecycleError(ValueError):
    """Raised when validation lifecycle metadata is missing or unsafe."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ValidationGateLifecycleError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise ValidationGateLifecycleError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationGateLifecycleError(f"{label} must be a non-empty string")
    return value.strip()


def _require_string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ValidationGateLifecycleError(f"{label} must be a non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise ValidationGateLifecycleError(f"{label} must contain only non-empty strings")
    return [str(item).strip() for item in value]


def _canonical_relative_path(value: str) -> bool:
    path = PurePosixPath(value)
    return (
        not path.is_absolute()
        and path.parts[:2] == ("data", "canonical")
        and ".." not in path.parts
        and "\\" not in value
    )


def _validate_authority(data: dict[str, Any], path: Path) -> None:
    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise ValidationGateLifecycleError(f"{_rel(path)}: authority must be a mapping")
    if authority.get("records_validation_lifecycle_policy") is not True:
        raise ValidationGateLifecycleError(f"{_rel(path)}: authority.records_validation_lifecycle_policy must be true")
    if authority.get("may_classify_gate_runtime_dependency") is not True:
        raise ValidationGateLifecycleError(f"{_rel(path)}: authority.may_classify_gate_runtime_dependency must be true")
    for key in REQUIRED_AUTHORITY_FALSE:
        if authority.get(key) is not False:
            raise ValidationGateLifecycleError(f"{_rel(path)}: authority.{key} must be false")


def _validate_gate(gate: dict[str, Any], seen_ids: set[str], path: Path) -> str:
    gate_id = _require_string(gate.get("gate_id"), "tracked_gates.gate_id")
    if gate_id in seen_ids:
        raise ValidationGateLifecycleError(f"{_rel(path)}: duplicate gate_id {gate_id}")
    seen_ids.add(gate_id)
    command = _require_string(gate.get("command"), f"{gate_id}.command")
    command_path = (ROOT / command).resolve()
    if not command_path.is_relative_to((ROOT / "scripts").resolve()):
        raise ValidationGateLifecycleError(f"{gate_id}.command must be under scripts/")
    if not command_path.is_file():
        raise ValidationGateLifecycleError(f"{gate_id}.command target does not exist: {command}")
    args = gate.get("args", [])
    if not isinstance(args, list) or not all(isinstance(item, str) and item.strip() for item in args):
        raise ValidationGateLifecycleError(f"{gate_id}.args must contain only non-empty strings")
    if any("\n" in item or "\r" in item for item in args):
        raise ValidationGateLifecycleError(f"{gate_id}.args must not contain line breaks")
    status = _require_string(gate.get("status"), f"{gate_id}.status")
    if status not in ALLOWED_STATUSES:
        raise ValidationGateLifecycleError(f"{gate_id}.status must be one of {sorted(ALLOWED_STATUSES)}")
    _require_string(gate.get("owner_task"), f"{gate_id}.owner_task")
    _require_string(gate.get("purpose"), f"{gate_id}.purpose")
    _require_string(gate.get("retirement_criteria"), f"{gate_id}.retirement_criteria")
    non_auths = set(_require_string_list(gate.get("non_authorizations"), f"{gate_id}.non_authorizations"))
    if "theology_authority" not in non_auths and "rust_validator_as_governance_authority" not in non_auths:
        raise ValidationGateLifecycleError(
            f"{gate_id}.non_authorizations must deny theology authority or Rust-as-governance authority"
        )

    required_inputs = gate.get("required_inputs")
    if status == "active_generated_data":
        paths = _require_string_list(required_inputs, f"{gate_id}.required_inputs")
        if not all(_canonical_relative_path(item) for item in paths):
            raise ValidationGateLifecycleError(
                f"{gate_id}.required_inputs must contain only repository-relative generated canonical data"
            )
        missing_behavior = _require_string(gate.get("missing_input_behavior"), f"{gate_id}.missing_input_behavior")
        if missing_behavior not in ALLOWED_MISSING_INPUT_BEHAVIOR:
            raise ValidationGateLifecycleError(
                f"{gate_id}.missing_input_behavior must be one of {sorted(ALLOWED_MISSING_INPUT_BEHAVIOR)}"
            )
    elif gate.get("missing_input_behavior") not in {None, "not_applicable"}:
        raise ValidationGateLifecycleError(f"{gate_id}.missing_input_behavior must be not_applicable outside generated-data gates")

    if status in {"superseded", "retired"}:
        replacement = gate.get("replacement_gate")
        if not isinstance(replacement, str) or not replacement.strip():
            raise ValidationGateLifecycleError(f"{gate_id}.replacement_gate is required when status is {status}")
        criteria = str(gate.get("retirement_criteria", "")).lower()
        for phrase in ("replacement", "owner"):
            if phrase not in criteria:
                raise ValidationGateLifecycleError(f"{gate_id}.retirement_criteria must mention {phrase}")

    return gate_id


def validate_validation_gate_lifecycle(path: Path = LIFECYCLE) -> dict[str, Any]:
    data = _read_yaml(path)
    if data.get("object_type") != "validation_gate_lifecycle":
        raise ValidationGateLifecycleError(f"{_rel(path)}: object_type must be validation_gate_lifecycle")
    if data.get("schema_version") != "validation_gate_lifecycle.v1":
        raise ValidationGateLifecycleError(f"{_rel(path)}: schema_version must be validation_gate_lifecycle.v1")
    if data.get("trust_zone") != "governance_control":
        raise ValidationGateLifecycleError(f"{_rel(path)}: trust_zone must be governance_control")
    if data.get("lifecycle_status") != "active":
        raise ValidationGateLifecycleError(f"{_rel(path)}: lifecycle_status must be active")
    _validate_authority(data, path)

    policy = data.get("policy")
    if not isinstance(policy, dict):
        raise ValidationGateLifecycleError(f"{_rel(path)}: policy must be a mapping")
    if policy.get("default_gate_state") != "active":
        raise ValidationGateLifecycleError(f"{_rel(path)}: policy.default_gate_state must be active")
    for key in ("generated_data_missing_behavior", "retirement_requires", "cleanup_rule"):
        if key not in policy:
            raise ValidationGateLifecycleError(f"{_rel(path)}: policy missing {key}")
    _require_string_list(policy["retirement_requires"], "policy.retirement_requires")
    _require_string(policy["generated_data_missing_behavior"], "policy.generated_data_missing_behavior")
    _require_string(policy["cleanup_rule"], "policy.cleanup_rule")

    global_non_auths = set(_require_string_list(data.get("global_non_authorizations"), "global_non_authorizations"))
    missing_non_auths = sorted(REQUIRED_GLOBAL_NON_AUTHS - global_non_auths)
    if missing_non_auths:
        raise ValidationGateLifecycleError(f"{_rel(path)}: global_non_authorizations missing {missing_non_auths}")

    gates = data.get("tracked_gates")
    if not isinstance(gates, list) or not gates:
        raise ValidationGateLifecycleError(f"{_rel(path)}: tracked_gates must be a non-empty list")
    seen: set[str] = set()
    for gate in gates:
        if not isinstance(gate, dict):
            raise ValidationGateLifecycleError(f"{_rel(path)}: each tracked gate must be a mapping")
        _validate_gate(gate, seen, path)
    missing_gates = sorted(REQUIRED_GENERATED_DATA_GATES - seen)
    if missing_gates:
        raise ValidationGateLifecycleError(f"{_rel(path)}: missing required generated-data gate(s) {missing_gates}")
    return data


def validate_lifecycle_expansion_candidates(path: Path = EXPANSION_CANDIDATES) -> dict[str, Any]:
    data = _read_yaml(path)
    if data.get("object_type") != "validation_lifecycle_expansion_candidates":
        raise ValidationGateLifecycleError(
            f"{_rel(path)}: object_type must be validation_lifecycle_expansion_candidates"
        )
    if data.get("schema_version") != "validation_lifecycle_expansion_candidates.v1":
        raise ValidationGateLifecycleError(
            f"{_rel(path)}: schema_version must be validation_lifecycle_expansion_candidates.v1"
        )
    if data.get("trust_zone") != "governance_control":
        raise ValidationGateLifecycleError(f"{_rel(path)}: trust_zone must be governance_control")
    references = data.get("external_research_references")
    if not isinstance(references, list) or len(references) < 2:
        raise ValidationGateLifecycleError(f"{_rel(path)}: external_research_references must include at least two entries")
    for index, reference in enumerate(references, start=1):
        if not isinstance(reference, dict):
            raise ValidationGateLifecycleError(f"{_rel(path)}: external reference {index} must be a mapping")
        _require_string(reference.get("name"), f"external_research_references[{index}].name")
        url = _require_string(reference.get("url"), f"external_research_references[{index}].url")
        if not url.startswith("https://"):
            raise ValidationGateLifecycleError(f"external_research_references[{index}].url must be https")
        _require_string(reference.get("lesson_used"), f"external_research_references[{index}].lesson_used")

    surfaces = data.get("recommended_lifecycle_surfaces")
    if not isinstance(surfaces, list) or not surfaces:
        raise ValidationGateLifecycleError(f"{_rel(path)}: recommended_lifecycle_surfaces must be a non-empty list")
    seen: set[str] = set()
    for surface in surfaces:
        if not isinstance(surface, dict):
            raise ValidationGateLifecycleError(f"{_rel(path)}: each recommended surface must be a mapping")
        surface_id = _require_string(surface.get("surface_id"), "recommended_lifecycle_surfaces.surface_id")
        if surface_id in seen:
            raise ValidationGateLifecycleError(f"{_rel(path)}: duplicate surface_id {surface_id}")
        seen.add(surface_id)
        if surface.get("priority") not in {"immediate", "high", "medium", "low"}:
            raise ValidationGateLifecycleError(f"{surface_id}.priority is invalid")
        _require_string(surface.get("why"), f"{surface_id}.why")
        _require_string(surface.get("dad_asset_candidate"), f"{surface_id}.dad_asset_candidate")
        states = _require_string_list(surface.get("suggested_states"), f"{surface_id}.suggested_states")
        if len(states) < 3:
            raise ValidationGateLifecycleError(f"{surface_id}.suggested_states must include at least three states")
    missing_surfaces = sorted(REQUIRED_EXPANSION_SURFACES - seen)
    if missing_surfaces:
        raise ValidationGateLifecycleError(f"{_rel(path)}: missing recommended surfaces {missing_surfaces}")

    non_auths = set(_require_string_list(data.get("global_non_authorizations"), "global_non_authorizations"))
    missing_non_auths = sorted(REQUIRED_EXPANSION_NON_AUTHS - non_auths)
    if missing_non_auths:
        raise ValidationGateLifecycleError(
            f"{_rel(path)}: global_non_authorizations missing {missing_non_auths}"
        )
    return data


def main() -> int:
    try:
        validate_validation_gate_lifecycle()
        validate_lifecycle_expansion_candidates()
    except ValidationGateLifecycleError as exc:
        print(f"Validation gate lifecycle validation failed: {exc}", file=sys.stderr)
        return 1
    print("Validation gate lifecycle validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
