#!/usr/bin/env python3
"""Validate a task-local execution overlay without polluting durable model routing."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
TASK_ROOT = ROOT / ".ai" / "tasks"

EXPECTED_BINDINGS = {
    "Sol": ("architecture_owner", "reasoner", "gpt-5.6-sol"),
    "Terra": ("shadow_regenerator_and_parity_specialist", "executor", "gpt-5.6-terra"),
    "Luna": ("bounded_delta_verifier", "executor", "gpt-5.6-luna"),
    "Claude": ("independent_auditor", "reasoner", "claude-opus-4.8"),
}
MODEL_IDS = {item[2] for item in EXPECTED_BINDINGS.values()}
DURABLE_BANNED_MODEL_IDS = {model_id for model_id in MODEL_IDS if model_id.startswith("gpt-5.6-")}
REQUIRED_STAGES = [
    "preflight_and_contract",
    "shadow_pair",
    "exact_inventory",
    "reconcile_and_freeze",
    "blind_audit",
    "evidence_ready_for_T476",
]
REQUIRED_CORRECTNESS = {
    "explicit_python_oracle",
    "full_parity_green",
    "fail_closed_exit",
    "deterministic_repeated_runs",
    "no_authority_leakage",
}
REQUIRED_VALUE = {
    "reproducible_wall_clock_or_memory_improvement",
    "simpler_or_safer_deployment",
    "stronger_fail_closed_correctness",
    "better_failure_isolation_and_diagnostics",
    "materially_lower_repeated_compute_cost",
}


class ExecutionOverlayError(ValueError):
    """Raised when a task-local execution overlay is unsafe or incomplete."""


def _read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ExecutionOverlayError(f"{path}: missing")
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            header = yaml.safe_load(parts[1]) or {}
            body = yaml.safe_load(parts[2]) or {}
            if not isinstance(header, dict) or not isinstance(body, dict):
                raise ExecutionOverlayError(f"{path}: expected YAML mappings")
            return {**header, **body}
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ExecutionOverlayError(f"{path}: expected YAML mapping")
    return data


def _mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ExecutionOverlayError(f"{label}: expected mapping")
    return value


def _string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ExecutionOverlayError(f"{label}: expected non-empty list")
    if not all(isinstance(item, str) and item for item in value):
        raise ExecutionOverlayError(f"{label}: expected non-empty strings")
    return list(value)


def validate_execution_overlay(root: Path, task_id: str) -> dict[str, Any]:
    task_path = root / ".ai" / "tasks" / f"{task_id}.task.yaml"
    task = _read_yaml(task_path)
    overlay = _mapping(task.get("execution_overlay"), f"{task_path}: execution_overlay")
    if overlay.get("schema_version") != "task_execution_overlay.v1":
        raise ExecutionOverlayError("execution_overlay.schema_version must be task_execution_overlay.v1")
    if overlay.get("task_id") != task_id:
        raise ExecutionOverlayError("execution_overlay.task_id must match task id")

    refs = _mapping(overlay.get("policy_refs"), "execution_overlay.policy_refs")
    for key in ("routing", "roles", "rust", "source_contract"):
        rel = refs.get(key)
        if not isinstance(rel, str) or not (root / rel).exists():
            raise ExecutionOverlayError(f"policy_refs.{key}: missing path {rel!r}")

    routing_path = root / str(refs["routing"])
    routing = _read_yaml(routing_path)
    profiles = _mapping(routing.get("profiles"), f"{routing_path}: profiles")
    binding = _mapping(overlay.get("task_local_roster_binding"), "task_local_roster_binding")
    if set(binding) != set(EXPECTED_BINDINGS):
        raise ExecutionOverlayError(
            f"task_local_roster_binding must contain exactly {sorted(EXPECTED_BINDINGS)}"
        )
    for alias, (role, profile, model_id) in EXPECTED_BINDINGS.items():
        row = _mapping(binding[alias], f"task_local_roster_binding.{alias}")
        if row.get("role") != role or row.get("profile") != profile or row.get("model_id") != model_id:
            raise ExecutionOverlayError(f"task_local_roster_binding.{alias}: role/profile/model mismatch")
        if profile not in profiles:
            raise ExecutionOverlayError(f"task_local_roster_binding.{alias}: unknown profile {profile}")
        if row.get("effort") not in {"low", "medium", "high", "xhigh"}:
            raise ExecutionOverlayError(f"task_local_roster_binding.{alias}: invalid effort")

    for rel in (str(refs["routing"]), str(refs["roles"]), str(refs["rust"])):
        text = (root / rel).read_text(encoding="utf-8").lower()
        leaked = sorted(model_id for model_id in DURABLE_BANNED_MODEL_IDS if model_id in text)
        if leaked:
            raise ExecutionOverlayError(f"{rel}: task-local model id leaked into durable policy: {leaked}")

    authority = _mapping(overlay.get("authority"), "execution_overlay.authority")
    for key in (
        "architecture_owner",
        "shadow_regenerator_and_parity_specialist",
        "bounded_delta_verifier",
        "independent_auditor",
        "reserved_to_owner",
        "universally_forbidden",
    ):
        _string_list(authority.get(key), f"execution_overlay.authority.{key}")
    if "committed_regeneration" not in authority["reserved_to_owner"]:
        raise ExecutionOverlayError("committed regeneration must remain reserved to owner")
    if "authority_promotion" not in authority["universally_forbidden"]:
        raise ExecutionOverlayError("authority promotion must be universally forbidden")

    roots = _mapping(overlay.get("roots"), "execution_overlay.roots")
    baseline = str(roots.get("baseline", "")).replace("\\", "/")
    candidate = str(roots.get("candidate", "")).replace("\\", "/")
    if not baseline.startswith("build/T475/") or not candidate.startswith("build/T475/"):
        raise ExecutionOverlayError("baseline and candidate must stay under build/T475/")
    if baseline == candidate:
        raise ExecutionOverlayError("baseline and candidate roots must be distinct")
    if roots.get("require_ignored_and_distinct") is not True or roots.get("forbid_symlink_escape") is not True:
        raise ExecutionOverlayError("shadow roots must be ignored, distinct, and symlink-contained")

    stages = overlay.get("stages")
    if not isinstance(stages, list) or [row.get("id") for row in stages if isinstance(row, dict)] != REQUIRED_STAGES:
        raise ExecutionOverlayError("execution stages or ordering changed")
    previous: str | None = None
    for row in stages:
        item = _mapping(row, "execution_overlay.stages[]")
        needs = item.get("needs")
        if not isinstance(needs, list):
            raise ExecutionOverlayError(f"stage {item.get('id')}: needs must be a list")
        expected = [] if previous is None else [previous]
        if needs != expected:
            raise ExecutionOverlayError(f"stage {item.get('id')}: must depend only on {expected}")
        previous = str(item["id"])

    rust = _mapping(overlay.get("rust_continuation_gate"), "rust_continuation_gate")
    if rust.get("new_rust_or_dependency_in_T475") != "forbidden":
        raise ExecutionOverlayError("T475 must not add Rust or dependencies before measurement")
    if set(_string_list(rust.get("correctness_required"), "rust.correctness_required")) != REQUIRED_CORRECTNESS:
        raise ExecutionOverlayError("Rust correctness gate is incomplete")
    if set(_string_list(rust.get("balanced_value_requires_one"), "rust.balanced_value_requires_one")) != REQUIRED_VALUE:
        raise ExecutionOverlayError("balanced-value options are incomplete")
    if rust.get("performance_alone_may_advance") is not False:
        raise ExecutionOverlayError("performance alone may not advance Rust")
    if rust.get("independent_audit_required") is not True:
        raise ExecutionOverlayError("independent audit must be required")
    benchmark = _mapping(rust.get("benchmark"), "rust.benchmark")
    if benchmark.get("repetitions_minimum", 0) < 3:
        raise ExecutionOverlayError("at least three benchmark repetitions are required")
    for key in ("pinned_inputs", "median_reported", "environment_recorded", "warmup_policy_recorded"):
        if benchmark.get(key) is not True:
            raise ExecutionOverlayError(f"rust.benchmark.{key} must be true")

    quality = _mapping(overlay.get("quality_first_context_policy"), "quality_first_context_policy")
    priority = _string_list(quality.get("priority"), "quality.priority")
    if priority[:4] != ["correctness", "completeness", "independence", "reproducibility"]:
        raise ExecutionOverlayError("quality priorities must lead with correctness, completeness, independence, reproducibility")
    for key in (
        "minimum_sufficient_context_per_role",
        "summaries_do_not_replace_machine_readable_ledgers",
    ):
        if quality.get(key) is not True:
            raise ExecutionOverlayError(f"quality.{key} must be true")
    if quality.get("silent_sampling_or_truncation") != "forbidden":
        raise ExecutionOverlayError("silent sampling/truncation must be forbidden")
    if quality.get("token_exhaustion_may_produce_pass") is not False:
        raise ExecutionOverlayError("token exhaustion may not produce a pass")

    audit = _mapping(overlay.get("independent_audit"), "independent_audit")
    if audit.get("roster_alias") != "Claude":
        raise ExecutionOverlayError("independent audit must resolve through the Claude task-local alias")
    for key in ("separate_invocation_and_context", "frozen_inputs_only", "findings_require_new_revision_and_new_audit"):
        if audit.get(key) is not True:
            raise ExecutionOverlayError(f"independent_audit.{key} must be true")
    if audit.get("may_edit_or_regenerate") is not False:
        raise ExecutionOverlayError("independent auditor may not edit or regenerate")
    if set(_string_list(audit.get("verdicts"), "independent_audit.verdicts")) != {
        "PASS", "HOLD_WITH_FINDINGS", "ESCALATE_OWNER"
    }:
        raise ExecutionOverlayError("independent audit verdicts changed")

    task_without_binding = json.loads(json.dumps(task))
    del task_without_binding["execution_overlay"]["task_local_roster_binding"]
    outside_text = json.dumps(task_without_binding, sort_keys=True).lower()
    leaked = sorted(model_id for model_id in MODEL_IDS if model_id in outside_text)
    if leaked:
        raise ExecutionOverlayError(f"model ids may occur only in task_local_roster_binding: {leaked}")

    return {"task_id": task_id, "aliases": sorted(binding), "stage_count": len(stages)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-id", required=True)
    args = parser.parse_args(argv)
    try:
        result = validate_execution_overlay(ROOT, args.task_id)
    except ExecutionOverlayError as exc:
        print(f"Task execution overlay validation failed: {exc}", file=sys.stderr)
        return 1
    print(f"Task execution overlay validation passed: {result['task_id']} ({result['stage_count']} stages).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
