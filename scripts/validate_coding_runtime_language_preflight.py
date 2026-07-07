#!/usr/bin/env python3
"""Validate coding-language preflight for high-resource deterministic code."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
PREFLIGHT = ROOT / ".ai" / "control" / "coding_runtime_language_preflight.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
VALIDATE_ALL = ROOT / "scripts" / "validate_all.py"
TASK_SCOPE = ROOT / "scripts" / "validate_task_scope.py"
ROADMAP_DOC = ROOT / "docs" / "roadmap" / "T424_RUST_ACCELERATED_VALIDATION_LAYER.md"

REQUIRED_TRIGGERS = {
    "estimated_runtime_seconds_60",
    "input_bytes_100mb",
    "records_100k",
    "memory_512mb",
    "repeated_gate_or_ci_hot_path",
    "deterministic_streaming_parse_hash_or_compare",
}

REQUIRED_DECISION_FIELDS = {
    "task_id",
    "touched_paths",
    "expected_input_size_or_record_count",
    "expected_runtime_or_memory_pressure",
    "rust_trigger_match",
    "chosen_language",
    "expected_rust_time_saved_or_reason_not_applicable",
    "interop_boundary",
    "python_fallback_or_wrapper_plan",
    "validation_plan",
    "maintenance_tradeoffs",
}

REQUIRED_RUST_DOMAINS = {
    "large_jsonl_or_ndjson_scans",
    "canonical_scope_or_reference_validation_over_generated_data",
    "whole_bible_or_corpus_observation_scans",
    "hash_checksum_or_manifest_walks_over_large_inputs",
    "large_chunk_map_or_model_output_comparison",
    "deterministic_token_marker_or_strong_occurrence_indexing",
}

REQUIRED_PYTHON_DOMAINS = {
    "governance_yaml_policy_validation",
    "task_scope_and_handoff_orchestration",
    "theology_policy_language_checks",
    "small_control_plane_validators",
    "wrapper_commands_that_dispatch_to_rust_or_existing_python",
    "tests_and_fixture_generation",
}

REQUIRED_MIGRATION_BOOLEANS = {
    "do_not_rewrite_all_pytest_in_rust": True,
    "preserve_existing_python_command_entry_points": True,
    "prefer_rust_fast_path_for_repeated_deterministic_validators": True,
    "keep_python_only_escape_hatch_for_parity_and_debugging": True,
    "require_modular_rust_check_report_boundaries": True,
    "require_validation_lifecycle_record_before_retiring_python_gate": True,
    "require_python_wrapper_to_fail_closed_on_rust_validation_failure": True,
}

REQUIRED_MIGRATION_PATTERNS = {
    "legacy_python_command_delegates_to_rust_wrapper",
    "python_wrapper_supports_require_rust_compare_python_python_fallback",
    "rust_module_run_check_returns_check_report",
    "combined_rust_command_preserves_per_check_failure_identity",
}

REQUIRED_MIGRATION_APPLIES_TO = {
    "validators_always_run_in_succession",
    "long_running_generated_data_checks",
    "whole_bible_chunk_map_checks",
    "canonical_sidecar_record_scans",
    "word_token_or_original_language_evidence_scans",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "rewrite_existing_python_by_default",
    "skip_python_governance_orchestration",
    "treat_rust_as_theology_authority",
    "chunk_output",
    "reviewed_gold",
    "child_spans",
    "route_or_evaluator_behavior",
    "graph_retrieval_or_vector_truth",
    "embeddings_or_indexes",
    "canon_scope_change",
}

REQUIRED_WIRING = {
    FRONT_DOOR: [
        "coding_runtime_language_preflight.yaml",
        "Rust-first",
        "high-resource deterministic code",
    ],
    VALIDATE_ALL: ["validate_coding_runtime_language_preflight.py"],
    TASK_SCOPE: ["runtime_language_preflight", "RUNTIME_PREFLIGHT_SURFACES"],
    ROADMAP_DOC: [
        "coding_runtime_language_preflight.yaml",
        "Rust-first",
        "Python/pytest remain authoritative",
        "Legacy Command Adoption Pattern",
    ],
}


class CodingRuntimeLanguagePreflightError(ValueError):
    """Raised when coding-language runtime preflight policy is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise CodingRuntimeLanguagePreflightError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise CodingRuntimeLanguagePreflightError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise CodingRuntimeLanguagePreflightError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise CodingRuntimeLanguagePreflightError(f"{label} must be a non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise CodingRuntimeLanguagePreflightError(f"{label} must contain only non-empty strings")
    return [str(item) for item in value]


def _require_bool(mapping: dict[str, Any], key: str, expected: bool, label: str) -> None:
    if mapping.get(key) is not expected:
        raise CodingRuntimeLanguagePreflightError(f"{label}.{key} must be {expected}")


def validate_coding_runtime_language_preflight(path: Path = PREFLIGHT) -> dict[str, Any]:
    data = _read_yaml(path)
    expected = {
        "object_type": "coding_runtime_language_preflight",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "coding_runtime_language_preflight.v1",
        "preflight_id": "repo_coding_runtime_language_preflight",
        "validator": "scripts/validate_coding_runtime_language_preflight.py",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise CodingRuntimeLanguagePreflightError(f"{_rel(path)}: {key} must be {value!r}")

    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise CodingRuntimeLanguagePreflightError(f"{_rel(path)}: authority must be a mapping")
    _require_bool(authority, "records_language_selection_policy", True, "authority")
    for key in (
        "authorizes_rewriting_existing_python_by_default",
        "authorizes_skipping_python_governance_orchestration",
        "authorizes_output_change",
        "authorizes_validation_bypass",
        "authorizes_theology_authority",
    ):
        _require_bool(authority, key, False, "authority")

    policy = data.get("policy")
    if not isinstance(policy, dict):
        raise CodingRuntimeLanguagePreflightError(f"{_rel(path)}: policy must be a mapping")
    for key in (
        "python_pytest_remain_governance_orchestrator",
        "rust_preferred_for_high_resource_deterministic_code",
        "rust_required_to_be_considered_before_new_heavy_code",
        "python_allowed_for_small_policy_and_orchestration_code",
        "interop_and_maintenance_tradeoffs_required",
        "fail_closed_on_rust_validation_failure",
    ):
        _require_bool(policy, key, True, "policy")

    triggers = data.get("rust_consideration_triggers")
    if not isinstance(triggers, list) or not triggers:
        raise CodingRuntimeLanguagePreflightError(f"{_rel(path)}: rust_consideration_triggers must be a non-empty list")
    by_id = {item.get("trigger_id"): item for item in triggers if isinstance(item, dict)}
    missing_triggers = sorted(REQUIRED_TRIGGERS - set(by_id))
    if missing_triggers:
        raise CodingRuntimeLanguagePreflightError(f"{_rel(path)}: missing triggers {missing_triggers}")
    for trigger_id, trigger in by_id.items():
        label = f"{_rel(path)}:{trigger_id}"
        if not isinstance(trigger.get("threshold"), str) or not trigger["threshold"].strip():
            raise CodingRuntimeLanguagePreflightError(f"{label}: threshold must be non-empty text")
        if trigger.get("rust_preflight_required") is not True:
            raise CodingRuntimeLanguagePreflightError(f"{label}: rust_preflight_required must be true")

    cutoffs = data.get("rust_preferred_cutoffs")
    if not isinstance(cutoffs, dict):
        raise CodingRuntimeLanguagePreflightError(f"{_rel(path)}: rust_preferred_cutoffs must be a mapping")
    if cutoffs.get("rust_preferred_when_estimated_savings_seconds_at_least") < 30:
        raise CodingRuntimeLanguagePreflightError(f"{_rel(path)}: Rust savings cutoff must be at least 30 seconds")
    if cutoffs.get("rust_preferred_when_estimated_speedup_ratio_at_least") < 1.25:
        raise CodingRuntimeLanguagePreflightError(f"{_rel(path)}: Rust speedup ratio cutoff must be at least 1.25")
    if cutoffs.get("rust_preferred_when_recurring_gate_runs_per_week_at_least") < 5:
        raise CodingRuntimeLanguagePreflightError(f"{_rel(path)}: recurring gate cutoff must be at least 5 runs/week")
    if cutoffs.get("python_default_allowed_when_estimated_runtime_seconds_below") > 30:
        raise CodingRuntimeLanguagePreflightError(f"{_rel(path)}: Python default runtime cutoff must be no more than 30 seconds")
    if cutoffs.get("python_default_allowed_when_input_bytes_below") > 10_485_760:
        raise CodingRuntimeLanguagePreflightError(f"{_rel(path)}: Python default byte cutoff must be no more than 10 MiB")
    if cutoffs.get("python_default_allowed_when_records_below") > 10_000:
        raise CodingRuntimeLanguagePreflightError(f"{_rel(path)}: Python default record cutoff must be no more than 10000")

    rust_domains = set(_require_string_list(data.get("rust_default_domains"), f"{_rel(path)}.rust_default_domains"))
    missing_rust_domains = sorted(REQUIRED_RUST_DOMAINS - rust_domains)
    if missing_rust_domains:
        raise CodingRuntimeLanguagePreflightError(f"{_rel(path)}: missing rust_default_domains {missing_rust_domains}")

    python_domains = set(_require_string_list(data.get("python_default_domains"), f"{_rel(path)}.python_default_domains"))
    missing_python_domains = sorted(REQUIRED_PYTHON_DOMAINS - python_domains)
    if missing_python_domains:
        raise CodingRuntimeLanguagePreflightError(f"{_rel(path)}: missing python_default_domains {missing_python_domains}")

    migration = data.get("python_test_and_validator_migration_strategy")
    if not isinstance(migration, dict):
        raise CodingRuntimeLanguagePreflightError(
            f"{_rel(path)}: python_test_and_validator_migration_strategy must be a mapping"
        )
    for key, expected in REQUIRED_MIGRATION_BOOLEANS.items():
        _require_bool(migration, key, expected, "python_test_and_validator_migration_strategy")
    patterns = set(
        _require_string_list(
            migration.get("adopted_patterns"),
            f"{_rel(path)}.python_test_and_validator_migration_strategy.adopted_patterns",
        )
    )
    missing_patterns = sorted(REQUIRED_MIGRATION_PATTERNS - patterns)
    if missing_patterns:
        raise CodingRuntimeLanguagePreflightError(f"{_rel(path)}: missing migration patterns {missing_patterns}")
    applies_to = set(
        _require_string_list(
            migration.get("applies_to"),
            f"{_rel(path)}.python_test_and_validator_migration_strategy.applies_to",
        )
    )
    missing_applies_to = sorted(REQUIRED_MIGRATION_APPLIES_TO - applies_to)
    if missing_applies_to:
        raise CodingRuntimeLanguagePreflightError(f"{_rel(path)}: missing migration applies_to {missing_applies_to}")

    decision_fields = set(
        _require_string_list(data.get("decision_record_required_fields"), f"{_rel(path)}.decision_record_required_fields")
    )
    missing_fields = sorted(REQUIRED_DECISION_FIELDS - decision_fields)
    if missing_fields:
        raise CodingRuntimeLanguagePreflightError(f"{_rel(path)}: missing decision fields {missing_fields}")

    task_guidance = data.get("task_contract_guidance")
    if not isinstance(task_guidance, dict):
        raise CodingRuntimeLanguagePreflightError(f"{_rel(path)}: task_contract_guidance must be a mapping")
    for key in ("required_when", "allowed_decisions"):
        _require_string_list(task_guidance.get(key), f"{_rel(path)}.task_contract_guidance.{key}")
    if task_guidance.get("recommended_field_name") != "runtime_language_preflight":
        raise CodingRuntimeLanguagePreflightError(
            f"{_rel(path)}: task_contract_guidance.recommended_field_name must be runtime_language_preflight"
        )
    if "language choice" not in str(task_guidance.get("handoff_requirement", "")):
        raise CodingRuntimeLanguagePreflightError(f"{_rel(path)}: handoff_requirement must mention language choice")

    non_auth = set(_require_string_list(data.get("non_authorizations"), f"{_rel(path)}.non_authorizations"))
    missing_non_auth = sorted(REQUIRED_NON_AUTHORIZATIONS - non_auth)
    if missing_non_auth:
        raise CodingRuntimeLanguagePreflightError(f"{_rel(path)}: missing non_authorizations {missing_non_auth}")

    for wired_path, needles in REQUIRED_WIRING.items():
        text = _read_text(wired_path)
        for needle in needles:
            if needle not in text:
                raise CodingRuntimeLanguagePreflightError(
                    f"{_rel(wired_path)}: missing coding-runtime preflight wiring string {needle!r}"
                )

    return data


def main() -> int:
    try:
        validate_coding_runtime_language_preflight()
    except CodingRuntimeLanguagePreflightError as exc:
        print(f"Coding runtime language preflight validation failed: {exc}", file=sys.stderr)
        return 1
    print("Coding runtime language preflight validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
