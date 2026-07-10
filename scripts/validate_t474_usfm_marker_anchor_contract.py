#!/usr/bin/env python3
"""Validate the T474 explicit USFM marker-anchor code and fixture contract."""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = {
    "task": ".ai/tasks/T474.task.yaml",
    "control": ".ai/control/t474_usfm_marker_anchor_contract.yaml",
    "t473_control": ".ai/control/t473_semantic_harness_pilot.yaml",
    "owner_packet": ".ai/context/agent_work/T473/source_anchor_repair_owner_packet.yaml",
    "roadmap": "docs/roadmap/T474_EXPLICIT_USFM_MARKER_ANCHOR_REPAIR.md",
    "handoff": ".ai/handoffs/T474/handoff.md",
    "importer": "pipelines/ingest/usfm_importer.py",
    "event_schema": "schemas/usfm_event.schema.json",
    "boundary_schema": "schemas/boundary_claim.schema.json",
    "heading_schema": "schemas/section_heading.schema.json",
    "contract_tests": "tests/test_t474_usfm_marker_anchor_contract.py",
}

ANCHOR_KINDS = {
    "current_content",
    "next_content_start",
    "between_units",
    "chapter_context",
    "book_context",
    "unresolved",
}
BODY_DISPOSITIONS = {"append_current", "editorial_only", "none", "unresolved"}
ANCHOR_FIELDS = {
    "anchor_kind",
    "anchor_osis_ref",
    "prior_osis_ref",
    "next_osis_ref",
    "body_disposition",
    "anchor_resolved",
}
TASK_FALSE_FIELDS = {
    "regenerates_committed_canonical_data",
    "regenerates_committed_processed_data",
    "modifies_raw_sources",
    "modifies_reviewed_gold",
    "authorizes_target_selection",
    "authorizes_reviewed_gold",
    "authorizes_chunk_output",
    "authorizes_child_spans",
    "changes_chunker_or_form_consumer_behavior",
    "changes_route_behavior",
    "changes_evaluator_behavior",
    "creates_graph_or_retrieval_truth",
    "runs_embeddings_or_builds_indexes",
    "imports_boundary_material",
    "selects_preferred_reading_or_source_tradition",
    "changes_canon_scope",
    "authorizes_theology_authority",
    "decides_variant_or_inspiration_status",
}
CONTROL_FALSE_FIELDS = {
    "changes_committed_raw_data",
    "changes_committed_canonical_data",
    "changes_committed_processed_data",
    "changes_reviewed_gold",
    "authorizes_target_selection",
    "authorizes_reviewed_gold",
    "authorizes_chunk_output",
    "authorizes_child_spans",
    "changes_chunker_or_form_consumer_behavior",
    "changes_route_behavior",
    "changes_evaluator_behavior",
    "creates_graph_or_retrieval_truth",
    "runs_embeddings_or_builds_indexes",
    "imports_boundary_material",
    "selects_preferred_reading_or_source_tradition",
    "changes_canon_scope",
    "authorizes_theology_authority",
}


def _load_yaml(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        text = parts[1] + "\n" + parts[2]
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected YAML mapping")
    return data


def _load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def _literal_assignment(source: str, name: str) -> Any:
    tree = ast.parse(source)
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(isinstance(target, ast.Name) and target.id == name for target in node.targets):
            return ast.literal_eval(node.value)
    raise ValueError(f"importer missing literal assignment {name}")


def _false_flags(block: dict[str, Any], fields: set[str], label: str, errors: list[str]) -> None:
    for field in sorted(fields):
        if block.get(field) is not False:
            errors.append(f"{label}.{field} must be false")


def validate_t474_package(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    paths = {key: root / rel for key, rel in REQUIRED_FILES.items()}
    for key, path in paths.items():
        if not path.exists():
            errors.append(f"missing {key}: {path.relative_to(root)}")
    if errors:
        return errors

    task = _load_yaml(paths["task"])
    control = _load_yaml(paths["control"])
    t473 = _load_yaml(paths["t473_control"])
    owner = _load_yaml(paths["owner_packet"])

    if task.get("id") != "T474":
        errors.append("task id must be T474")
    if task.get("mode") != "importer_code_and_fixture_repair_only":
        errors.append("task mode mismatch")
    if task.get("status") not in {"in_progress", "complete"}:
        errors.append("task status must be in_progress or complete")
    if task.get("owner_gate", {}).get("selected_option") != "T473-ANCHOR-A":
        errors.append("task must record T473-ANCHOR-A")
    authorization = task.get("authorization", {})
    if authorization.get("changes_importer_code") is not True:
        errors.append("task must authorize importer code")
    if authorization.get("adds_synthetic_fixtures") is not True:
        errors.append("task must authorize synthetic fixtures")
    _false_flags(authorization, TASK_FALSE_FIELDS, "task.authorization", errors)

    owner_selection = owner.get("owner_selection")
    if owner_selection != "T473-ANCHOR-A":
        errors.append("owner packet must select T473-ANCHOR-A")
    if owner.get("status") != "selected_for_T474_code_and_fixture_work_only":
        errors.append("owner packet status must remain T474-only")
    gate = owner.get("owner_gate_effect", {})
    for field in (
        "authorizes_canonical_regeneration_now",
        "authorizes_reviewed_gold_change_now",
        "authorizes_chunk_output_now",
    ):
        if gate.get(field) is not False:
            errors.append(f"owner packet {field} must be false")

    execution = t473.get("execution_state", {})
    if execution.get("t474_allowed") is not True:
        errors.append("T473 control must allow T474")
    if execution.get("pilot_execution_allowed") is not False:
        errors.append("T473 semantic pilot must remain blocked")

    if control.get("task_id") != "T474":
        errors.append("control task_id must be T474")
    if control.get("owner_gate", {}).get("selected_option") != "T473-ANCHOR-A":
        errors.append("control must record T473-ANCHOR-A")
    contract = control.get("marker_resolution_contract", {})
    if set(contract.get("required_anchor_kinds", [])) != ANCHOR_KINDS:
        errors.append("control anchor kinds mismatch")
    if set(contract.get("required_body_dispositions", [])) != BODY_DISPOSITIONS:
        errors.append("control body dispositions mismatch")
    if set(contract.get("required_fields", [])) != ANCHOR_FIELDS:
        errors.append("control required fields mismatch")
    state = control.get("execution_state", {})
    for field in ("importer_repair_complete", "synthetic_fixture_proof_complete"):
        if state.get(field) is not True:
            errors.append(f"control execution_state.{field} must be true")
    for field in (
        "committed_canonical_regeneration_performed",
        "committed_processed_regeneration_performed",
        "downstream_chunker_consumer_changed",
    ):
        if state.get(field) is not False:
            errors.append(f"control execution_state.{field} must be false")
    _false_flags(control.get("authorization", {}), CONTROL_FALSE_FIELDS, "control.authorization", errors)

    source = paths["importer"].read_text(encoding="utf-8")
    for signature in (
        "class MarkerResolution:",
        "def resolve_line_marker(",
        "def prepare_line_contexts(",
        "resolution.body_disposition == \"append_current\"",
        "**resolution.fields()",
    ):
        if signature not in source:
            errors.append(f"importer missing signature: {signature}")
    if "def extract_nonverse_inline_sidecars(" in source:
        errors.append("legacy non-verse canonical sidecar parser must remain removed")
    try:
        structural = set(_literal_assignment(source, "STRUCTURAL_MARKERS"))
        between = set(_literal_assignment(source, "BETWEEN_UNIT_MARKERS"))
        headings = set(_literal_assignment(source, "NEXT_CONTENT_HEADING_MARKERS"))
    except (SyntaxError, ValueError) as exc:
        errors.append(str(exc))
    else:
        if "qs" in structural:
            errors.append("inline qs must not remain a structural line marker")
        if between != {"b", "nb"}:
            errors.append("between-unit marker set must be b and nb")
        if not {"d", "sp", "s1", "ms1"} <= headings:
            errors.append("editorial following-content markers are incomplete")

    for key in ("event_schema", "boundary_schema", "heading_schema"):
        schema = _load_json(paths[key])
        properties = schema.get("properties", {})
        missing = ANCHOR_FIELDS - set(properties)
        if missing:
            errors.append(f"{key} missing anchor properties: {sorted(missing)}")
        required = set(schema.get("required", []))
        accidentally_required = ANCHOR_FIELDS & required
        if accidentally_required:
            errors.append(f"{key} anchor fields must remain optional in T474: {sorted(accidentally_required)}")
        if schema.get("additionalProperties") is not True:
            errors.append(f"{key} must retain additive compatibility")
    for key in ("boundary_schema", "heading_schema"):
        schema = _load_json(paths[key])
        if "source_event_id" not in schema.get("properties", {}):
            errors.append(f"{key} missing source_event_id")

    combined = "\n".join(
        paths[key].read_text(encoding="utf-8")
        for key in ("roadmap", "handoff")
    ).lower()
    for phrase in (
        "no committed",
        "reviewed gold",
        "chunk output",
        "source-tradition",
        "theology authority",
        "t475",
    ):
        if phrase not in combined:
            errors.append(f"T474 documentation missing non-authorization/route phrase: {phrase}")
    return errors


def main() -> int:
    errors = validate_t474_package(ROOT)
    if errors:
        print("T474 USFM MARKER-ANCHOR VALIDATION FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("T474 USFM marker-anchor contract validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
