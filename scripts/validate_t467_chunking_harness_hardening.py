#!/usr/bin/env python3
"""Validate T467 chunking harness hardening package."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = {
    "task": ".ai/tasks/T467.task.yaml",
    "control": ".ai/control/t467_chunking_harness_hardening.yaml",
    "protocol": ".ai/control/t423_literary_marker_quality_protocol.yaml",
    "fork": ".ai/control/multi_model_whole_bible_chunking_fork.yaml",
    "prompt": ".ai/prompts/multi_model_whole_bible_chunking_marathon_prompt.md",
    "template": ".ai/scratch/multi_model_bible_chunking/models/_TEMPLATE/model_manifest.yaml",
    "notes": ".ai/context/agent_work/T467/harness_hardening_notes.md",
    "handoff": ".ai/handoffs/T467/handoff.md",
    "roadmap": "docs/roadmap/T467_CHUNKING_HARNESS_HARDENING.md",
}

FORBIDDEN_AUTH_FIELDS = {
    "authorizes_reviewed_gold",
    "authorizes_chunk_output",
    "authorizes_child_spans",
    "authorizes_target_selection",
    "changes_route_behavior",
    "changes_evaluator_behavior",
    "creates_graph_truth",
    "creates_retrieval_truth",
    "creates_vector_truth",
    "selects_preferred_reading",
    "selects_source_tradition",
    "changes_canon_scope",
    "authorizes_theology_authority",
}

REQUIRED_STRATEGY_SECTIONS = {
    "literary_form_decision_matrix",
    "larger_unit_preservation_check",
    "list_register_function_check",
    "epistle_unit_check_if_applicable",
    "source_metadata_evidence_only_check",
    "over_split_risk_check",
    "sidecar_specificity_plan",
}

REQUIRED_LIST_FORMS = {
    "genealogy",
    "census",
    "tribal_allotment",
    "legal_list",
    "ritual_procedure",
    "temple_service_register",
    "royal_or_administrative_register",
    "battle_report",
    "covenant_renewal",
}

REQUIRED_EPISTLE_UNITS = {
    "greeting",
    "thanksgiving_or_prayer",
    "body_argument",
    "exhortation_or_paraenesis",
    "travel_or_mission_notes",
    "final_greetings",
    "doxology",
    "benediction",
}


def _strip_front_matter(text: str) -> str:
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            return parts[1] + "\n" + parts[2]
    return text


def _read_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(_strip_front_matter(path.read_text(encoding="utf-8")))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected YAML mapping")
    return data


def _require(condition: bool, error: str, errors: list[str]) -> None:
    if not condition:
        errors.append(error)


def _validate_no_authority(auth: dict[str, Any], label: str, errors: list[str]) -> None:
    for field in FORBIDDEN_AUTH_FIELDS:
        if auth.get(field) is not False:
            errors.append(f"{label}: {field} must be false")


def validate_t467_package(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    paths = {key: root / rel for key, rel in REQUIRED_FILES.items()}
    for key, path in paths.items():
        if not path.is_file():
            errors.append(f"missing required T467 file {REQUIRED_FILES[key]}")
    if errors:
        return errors

    task = _read_yaml(paths["task"])
    control = _read_yaml(paths["control"])
    protocol = _read_yaml(paths["protocol"])
    fork = _read_yaml(paths["fork"])
    template = _read_yaml(paths["template"])
    prompt_text = paths["prompt"].read_text(encoding="utf-8")
    notes_text = paths["notes"].read_text(encoding="utf-8")
    roadmap_text = paths["roadmap"].read_text(encoding="utf-8")

    _require(task.get("id") == "T467", "task id must be T467", errors)
    _require(control.get("object_type") == "t467_chunking_harness_hardening", "control object_type mismatch", errors)
    _require(control.get("policy_revision") == "T467_literary_coherence_v1", "control policy_revision mismatch", errors)
    _require(control.get("does_not_retroactively_invalidate_completed_models") is True, "control must preserve completed model evidence", errors)
    _validate_no_authority(control.get("authorization", {}), "control.authorization", errors)

    task_auth = task.get("authorization", {})
    for field in (
        "authorizes_target_selection",
        "authorizes_reviewed_gold",
        "authorizes_chunk_output",
        "authorizes_child_spans",
        "changes_route_behavior",
        "changes_evaluator_behavior",
        "runs_embeddings_or_builds_indexes",
        "changes_canon_scope",
        "authorizes_theology_authority",
        "writes_dad_reports",
    ):
        if task_auth.get(field) is not False:
            errors.append(f"task.authorization: {field} must be false")

    rules = control.get("hardening_rules", {})
    list_guard = rules.get("list_register_guard", {})
    epistle_guard = rules.get("epistle_closing_guard", {})
    source_guard = rules.get("source_metadata_guard", {})
    sidecar = rules.get("sidecar_specificity", {})
    _require(REQUIRED_LIST_FORMS.issubset(set(list_guard.get("affected_forms", []))), "control missing list/register affected forms", errors)
    _require(REQUIRED_EPISTLE_UNITS.issubset(set(epistle_guard.get("required_strategy_checks", []))), "control missing epistle checks", errors)
    _require("evidence only" in str(source_guard.get("rule", "")), "source metadata guard must say evidence only", errors)
    _require("concrete issue" in str(sidecar.get("rule", "")), "sidecar specificity must require concrete issue", errors)
    _require(REQUIRED_STRATEGY_SECTIONS.issubset(set(control.get("book_strategy_required_sections_for_future_reruns", []))), "control missing required book strategy sections", errors)

    protocol_overlay = protocol.get("t467_literary_coherence_overlay", {})
    _require(protocol_overlay.get("status") == "required_for_future_reruns", "protocol overlay status mismatch", errors)
    _require(REQUIRED_LIST_FORMS.issubset(set(protocol_overlay.get("do_not_over_split_forms", []))), "protocol missing do_not_over_split forms", errors)
    _require(REQUIRED_EPISTLE_UNITS.issubset(set(protocol_overlay.get("epistle_unit_checklist", []))), "protocol missing epistle checklist units", errors)
    _require(REQUIRED_STRATEGY_SECTIONS.issubset(set(protocol_overlay.get("required_book_strategy_sections", []))), "protocol missing T467 strategy sections", errors)
    _require(REQUIRED_STRATEGY_SECTIONS.issubset(set(protocol.get("book_strategy_note_must_cover", []))), "protocol book_strategy_note_must_cover missing T467 sections", errors)

    quality = fork.get("literary_marker_quality_protocol", {})
    _require(quality.get("active_policy_overlay") == "T467_literary_coherence_v1", "fork must declare active T467 overlay", errors)
    _require(quality.get("hardening_control") == ".ai/control/t467_chunking_harness_hardening.yaml", "fork must point to T467 control", errors)

    template_quality = template.get("quality_protocol", {})
    _require(template_quality.get("hardening_overlay") == "T467_literary_coherence_v1", "template must declare T467 hardening overlay", errors)
    _require(template_quality.get("source_metadata_boundary_authority") is False, "template source metadata authority must be false", errors)
    _require(template_quality.get("larger_unit_preservation_required") is True, "template larger unit preservation required", errors)
    _require(template_quality.get("sidecar_specificity_required") is True, "template sidecar specificity required", errors)

    for text_label, text in (("prompt", prompt_text), ("notes", notes_text), ("roadmap", roadmap_text)):
        for needle in (
            "T467_literary_coherence_v1",
            "larger",
            "list",
            "epistle",
            "Strong",
            "evidence only",
            "No",
        ):
            if needle not in text:
                errors.append(f"{text_label} missing required text {needle!r}")
    if ".digital-asset/" in "\n".join(str(path) for path in paths.values()):
        errors.append("T467 package must not require DAD paths")
    if "deferred_due_to_interface_drift" not in notes_text:
        errors.append("T467 notes must record DAD reporting deferral")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    errors = validate_t467_package(args.root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("T467 chunking harness hardening validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
