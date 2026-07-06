#!/usr/bin/env python3
"""Validate the T438 original-language alignment bridge goal gate."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTROL = ROOT / ".ai" / "control" / "t438_alignment_bridge_goal.yaml"
SUBSTRATE = ROOT / ".ai" / "control" / "original_language_evidence_substrate.yaml"
TASK = ROOT / ".ai" / "tasks" / "T438.task.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T438" / "handoff.md"
DAD_PREFLIGHT = ROOT / ".ai" / "context" / "agent_work" / "T438" / "dad_preflight.md"
ROADMAP = ROOT / "docs" / "roadmap" / "T438_ALIGNMENT_BRIDGE_GOAL.md"
GOAL_OPTIONS = ROOT / "docs" / "roadmap" / "T430_ORIGINAL_LANGUAGE_GOAL_OPTIONS.md"
VALIDATE_ALL = ROOT / "scripts" / "validate_all.py"

PRODUCTION_ROOTS = (
    ROOT / "data" / "candidate" / "original_language_evidence" / "source_tokens",
    ROOT / "data" / "candidate" / "original_language_evidence" / "strong_alignment",
    ROOT / "data" / "candidate" / "original_language_evidence" / "lemma_morphology",
    ROOT / "data" / "candidate" / "original_language_evidence" / "textual_variants",
    ROOT / "data" / "candidate" / "original_language_evidence" / "witness_support",
    ROOT / "data" / "candidate" / "original_language_evidence" / "editorial_layers",
)

FALSE_AUTHORITY = {
    "authorizes_source_language_truth",
    "authorizes_lexical_truth",
    "authorizes_word_level_alignment_truth",
    "authorizes_strongs_as_source_text",
    "authorizes_lemma_or_morphology_population",
    "authorizes_preferred_reading",
    "authorizes_source_tradition_preference",
    "authorizes_textual_critical_decision",
    "authorizes_manuscript_witness_support",
    "authorizes_canon_scope_change",
    "authorizes_translation_judgment",
    "authorizes_chunk_boundary",
    "creates_reviewed_gold",
    "creates_chunk_output",
    "changes_route_behavior",
    "changes_evaluator_behavior",
    "creates_graph_or_retrieval_truth",
    "runs_embeddings_or_builds_indexes",
    "authorizes_theology_authority",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "source_language_truth",
    "lexical_truth",
    "word_level_alignment_truth",
    "strongs_number_as_source_text",
    "local_lemma_population_without_span_local_proof",
    "morphology_population_without_span_local_proof",
    "preferred_reading",
    "source_tradition_preference",
    "translation_judgment",
    "translation_faithfulness_score",
    "graph_edge",
    "retrieval_truth",
    "theology_authority",
}

EXPECTED_SEQUENCE = ["T439", "T440", "T441", "T442"]


class T438AlignmentBridgeGoalError(ValueError):
    """Raised when the T438 alignment bridge goal gate is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise T438AlignmentBridgeGoalError(f"{_rel(path)} unreadable YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise T438AlignmentBridgeGoalError(f"{_rel(path)} must be a YAML mapping")
    return data


def _require_false(mapping: dict[str, Any], keys: set[str], label: str) -> None:
    for key in sorted(keys):
        if mapping.get(key) is not False:
            raise T438AlignmentBridgeGoalError(f"{label}.{key} must be false")


def _validate_no_production_outputs(root: Path) -> None:
    for directory in PRODUCTION_ROOTS:
        path = root / directory.relative_to(ROOT)
        if path.exists() and any(path.rglob("*")):
            raise T438AlignmentBridgeGoalError(f"{_rel(path)} must stay empty until a later production task")


def validate_t438_alignment_bridge_goal(root: Path = ROOT) -> dict[str, Any]:
    for path in (CONTROL, SUBSTRATE, TASK, HANDOFF, DAD_PREFLIGHT, ROADMAP, GOAL_OPTIONS):
        local = root / path.relative_to(ROOT)
        if not local.exists():
            raise T438AlignmentBridgeGoalError(f"{_rel(local)} is missing")

    control = _read_yaml(root / CONTROL.relative_to(ROOT))
    if control.get("object_type") != "t438_alignment_bridge_goal":
        raise T438AlignmentBridgeGoalError("T438 control object_type is wrong")
    if control.get("schema_version") != "t438_alignment_bridge_goal.v1":
        raise T438AlignmentBridgeGoalError("T438 control schema_version is wrong")
    if control.get("status") != "planning_control_gate":
        raise T438AlignmentBridgeGoalError("T438 status must remain planning_control_gate")

    goal = control.get("goal_selection")
    if not isinstance(goal, dict):
        raise T438AlignmentBridgeGoalError("goal_selection must be a mapping")
    if goal.get("primary_goal_option_id") != "option_1_alignment_bridge":
        raise T438AlignmentBridgeGoalError("primary goal must be option_1_alignment_bridge")
    if goal.get("status") != "recommended_next_implementation_lane":
        raise T438AlignmentBridgeGoalError("goal_selection.status must be recommended_next_implementation_lane")

    parallel = control.get("parallel_goal_option")
    if not isinstance(parallel, dict) or parallel.get("option_id") != "option_2_manuscript_custody_chain":
        raise T438AlignmentBridgeGoalError("parallel goal must be option_2_manuscript_custody_chain")
    if parallel.get("status") != "catalog_only_parallel_research":
        raise T438AlignmentBridgeGoalError("parallel manuscript work must remain catalog-only")

    bridge = control.get("alignment_bridge_contract")
    if not isinstance(bridge, dict):
        raise T438AlignmentBridgeGoalError("alignment_bridge_contract must be a mapping")
    input_policy = bridge.get("input_policy")
    if not isinstance(input_policy, dict):
        raise T438AlignmentBridgeGoalError("alignment_bridge_contract.input_policy must be a mapping")
    if input_policy.get("raw_archive_direct_consumption_allowed") is not False:
        raise T438AlignmentBridgeGoalError("raw archive direct consumption must be false")
    if input_policy.get("strongs_numbers_are_source_text") is not False:
        raise T438AlignmentBridgeGoalError("Strong's numbers must not be source text")
    if input_policy.get("source_metadata_is_authority") is not False:
        raise T438AlignmentBridgeGoalError("source metadata must not be authority")

    candidate_policy = bridge.get("candidate_row_policy")
    if not isinstance(candidate_policy, dict):
        raise T438AlignmentBridgeGoalError("candidate_row_policy must be a mapping")
    for key in (
        "alignment_truth_authorized",
        "translation_faithfulness_judgment_authorized",
    ):
        if candidate_policy.get(key) is not False:
            raise T438AlignmentBridgeGoalError(f"candidate_row_policy.{key} must be false")
    for key in (
        "local_lemma_or_morphology_population_requires_span_local_proof",
        "strong_lookup_hint_population_requires_source_specific_policy",
    ):
        if candidate_policy.get(key) is not True:
            raise T438AlignmentBridgeGoalError(f"candidate_row_policy.{key} must be true")

    rust = control.get("rust_fit_matrix")
    if not isinstance(rust, dict):
        raise T438AlignmentBridgeGoalError("rust_fit_matrix must be a mapping")
    rust_slices = {
        str(item.get("slice"))
        for item in rust.get("good_rust_candidates", [])
        if isinstance(item, dict)
    }
    for required in (
        "canonical_source_view_token_shape_scan",
        "source_to_web_ref_coverage_join",
        "jsonl_schema_shape_fast_scan",
        "no_text_alignment_candidate_index",
    ):
        if required not in rust_slices:
            raise T438AlignmentBridgeGoalError(f"missing Rust-fit slice {required}")
    keep_python = {str(item).lower() for item in rust.get("keep_python_governed", [])}
    if not any("theology" in item for item in keep_python):
        raise T438AlignmentBridgeGoalError("rust_fit_matrix must keep theology/translation policy Python-governed")

    sequence = control.get("next_task_sequence")
    if not isinstance(sequence, list):
        raise T438AlignmentBridgeGoalError("next_task_sequence must be a list")
    if [str(item.get("task_id")) for item in sequence if isinstance(item, dict)] != EXPECTED_SEQUENCE:
        raise T438AlignmentBridgeGoalError(f"next_task_sequence must be {EXPECTED_SEQUENCE}")
    t441 = next(item for item in sequence if isinstance(item, dict) and item.get("task_id") == "T441")
    if "rust" not in str(t441.get("mode", "")).lower():
        raise T438AlignmentBridgeGoalError("T441 must be the Rust leaf-tool stage")

    authority = control.get("authority")
    if not isinstance(authority, dict):
        raise T438AlignmentBridgeGoalError("authority must be a mapping")
    if authority.get("records_goal_selection") is not True:
        raise T438AlignmentBridgeGoalError("authority.records_goal_selection must be true")
    _require_false(authority, FALSE_AUTHORITY, "authority")

    non_auth = control.get("non_authorizations")
    if not isinstance(non_auth, list):
        raise T438AlignmentBridgeGoalError("non_authorizations must be a list")
    missing = sorted(REQUIRED_NON_AUTHORIZATIONS - {str(item) for item in non_auth})
    if missing:
        raise T438AlignmentBridgeGoalError(f"non_authorizations missing {missing}")

    task = _read_yaml(root / TASK.relative_to(ROOT))
    if task.get("id") != "T438":
        raise T438AlignmentBridgeGoalError("T438 task id is wrong")
    if task.get("rust_policy", {}).get("rust_added_in_t438") is not False:
        raise T438AlignmentBridgeGoalError("T438 must not add Rust")
    if task.get("rust_policy", {}).get("rust_preferred_for_future_leaf_tools") is not True:
        raise T438AlignmentBridgeGoalError("T438 must prefer Rust for future deterministic leaf tools")
    task_auth = task.get("authorization")
    if not isinstance(task_auth, dict):
        raise T438AlignmentBridgeGoalError("T438 task authorization must be a mapping")
    for key, value in task_auth.items():
        if key.startswith(("opens_", "creates_", "changes_", "runs_", "authorizes_", "selects_")) and key != "records_goal_selection":
            if value is not False:
                raise T438AlignmentBridgeGoalError(f"T438 task authorization {key} must be false")

    substrate = _read_yaml(root / SUBSTRATE.relative_to(ROOT))
    pilots = substrate.get("pilot_lanes")
    if not isinstance(pilots, list):
        raise T438AlignmentBridgeGoalError("substrate.pilot_lanes must be a list")
    t438_pilots = [pilot for pilot in pilots if isinstance(pilot, dict) and pilot.get("task_id") == "T438"]
    if len(t438_pilots) != 1:
        raise T438AlignmentBridgeGoalError("T430 substrate must reference exactly one T438 pilot lane")
    if "alignment bridge" not in str(t438_pilots[0].get("rule", "")).lower():
        raise T438AlignmentBridgeGoalError("T438 substrate lane must describe the alignment bridge")

    validate_all_text = (root / VALIDATE_ALL.relative_to(ROOT)).read_text(encoding="utf-8")
    if "validate_t438_alignment_bridge_goal.py" not in validate_all_text:
        raise T438AlignmentBridgeGoalError("validate_all.py must run the T438 validator")

    roadmap_text = (root / ROADMAP.relative_to(ROOT)).read_text(encoding="utf-8").lower()
    for phrase in (
        "greek/hebrew-to-english alignment bridge",
        "manuscript custody-chain",
        "rust speed is not authority",
        "do not treat strong's numbers as greek/hebrew source text",
    ):
        if phrase not in roadmap_text:
            raise T438AlignmentBridgeGoalError(f"{_rel(ROADMAP)} missing phrase {phrase!r}")

    dad_text = (root / DAD_PREFLIGHT.relative_to(ROOT)).read_text(encoding="utf-8").lower()
    for phrase in ("separate goal selection", "parser semantics", "rust acceleration"):
        if phrase not in dad_text:
            raise T438AlignmentBridgeGoalError(f"{_rel(DAD_PREFLIGHT)} missing phrase {phrase!r}")

    _validate_no_production_outputs(root)
    return control


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    try:
        validate_t438_alignment_bridge_goal(args.root.resolve())
    except T438AlignmentBridgeGoalError as exc:
        print(f"T438 alignment bridge goal validation failed: {exc}", file=sys.stderr)
        return 1
    print("T438 alignment bridge goal validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
