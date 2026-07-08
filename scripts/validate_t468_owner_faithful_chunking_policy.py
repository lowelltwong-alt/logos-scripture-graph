#!/usr/bin/env python3
"""Validate T468 owner faithful-route chunking policy."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = {
    "task": ".ai/tasks/T468.task.yaml",
    "control": ".ai/control/t468_owner_faithful_chunking_policy.yaml",
    "register": ".ai/control/chunking_theological_decision_register.yaml",
    "lesson_index": ".ai/control/chunking_lesson_index.yaml",
    "status": ".ai/control/PROJECT_STATUS.md",
    "focus": ".ai/control/current_focus.yaml",
    "handoff": ".ai/handoffs/T468/handoff.md",
    "roadmap": "docs/roadmap/T468_OWNER_FAITHFUL_CHUNKING_POLICY.md",
}

FORBIDDEN_AUTH_FIELDS = {
    "authorizes_target_selection",
    "authorizes_reviewed_gold",
    "authorizes_chunk_output",
    "authorizes_child_spans",
    "changes_route_behavior",
    "changes_evaluator_behavior",
    "creates_graph_truth",
    "creates_retrieval_truth",
    "creates_vector_truth",
    "runs_embeddings_or_builds_indexes",
    "imports_boundary_material",
    "selects_preferred_reading",
    "selects_source_tradition",
    "changes_canon_scope",
    "decides_variant_or_inspiration_status",
    "authorizes_theology_authority",
}

TASK_FORBIDDEN_AUTH_FIELDS = {
    "authorizes_target_selection",
    "authorizes_reviewed_gold",
    "authorizes_chunk_output",
    "authorizes_child_spans",
    "changes_route_behavior",
    "changes_evaluator_behavior",
    "creates_graph_or_retrieval_truth",
    "runs_embeddings_or_builds_indexes",
    "imports_boundary_material",
    "selects_preferred_reading_or_source_tradition",
    "changes_canon_scope",
    "authorizes_theology_authority",
    "decides_variant_or_inspiration_status",
    "writes_dad_reports",
}

REQUIRED_DECISION_IDS = {f"T468-D{i}" for i in range(1, 8)}

REQUIRED_HARD_EXCEPTIONS = {
    "mark_16_longer_ending",
    "john_7_53_8_11",
    "romans_16_doxology",
    "deut_32_8_9",
    "jeremiah_source_tradition_structure",
    "daniel_esther_additions_routing",
    "first_john_5_6_8",
    "dense_epistle_arguments_romans_corinthians_hebrews",
    "wj_speaker_heavy_gospel_spans",
    "revelation_and_daniel_vision_cycles",
}

REQUIRED_REGISTER_NON_AUTHS = {
    "target_selection",
    "chunk_output_change",
    "reviewed_gold_promotion",
    "child_span_creation",
    "route_or_evaluator_behavior",
    "graph_or_retrieval_truth",
    "vector_or_embedding_truth",
    "source_tradition_preference",
    "canon_scope_change",
    "variant_or_inspiration_decision",
    "theology_authority_change",
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


def _validate_false_flags(auth: dict[str, Any], fields: set[str], label: str, errors: list[str]) -> None:
    for field in sorted(fields):
        if auth.get(field) is not False:
            errors.append(f"{label}: {field} must be false")


def _find_decision(register: dict[str, Any], decision_id: str) -> dict[str, Any] | None:
    for decision in register.get("decisions", []):
        if isinstance(decision, dict) and decision.get("decision_id") == decision_id:
            return decision
    return None


def validate_t468_package(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    paths = {key: root / rel for key, rel in REQUIRED_FILES.items()}
    for key, path in paths.items():
        if not path.is_file():
            errors.append(f"missing required T468 file {REQUIRED_FILES[key]}")
    if errors:
        return errors

    task = _read_yaml(paths["task"])
    control = _read_yaml(paths["control"])
    register = _read_yaml(paths["register"])
    lesson_index = _read_yaml(paths["lesson_index"])
    focus = _read_yaml(paths["focus"])
    status_text = paths["status"].read_text(encoding="utf-8")
    handoff_text = paths["handoff"].read_text(encoding="utf-8")
    roadmap_text = paths["roadmap"].read_text(encoding="utf-8")

    _require(task.get("id") == "T468", "task id must be T468", errors)
    _require(control.get("object_type") == "t468_owner_faithful_chunking_policy", "control object_type mismatch", errors)
    _require(control.get("schema_version") == "t468_owner_faithful_chunking_policy.v1", "control schema_version mismatch", errors)
    _require(focus.get("current_task") == "T468", "current_focus current_task must be T468", errors)

    _validate_false_flags(task.get("authorization", {}), TASK_FORBIDDEN_AUTH_FIELDS, "task.authorization", errors)
    _validate_false_flags(control.get("authorization", {}), FORBIDDEN_AUTH_FIELDS, "control.authorization", errors)

    first = control.get("first_principle", {})
    _require(first.get("id") == "let_the_bible_interpret_the_bible", "first principle id mismatch", errors)
    _require("Bible" in str(first.get("rule", "")), "first principle rule must mention Bible", errors)
    _require("does not authorize" in str(first.get("guardrail", "")), "first principle must include non-authority guardrail", errors)

    candidate = control.get("candidate_acceptance", {})
    expected_counts = {
        "easy_majority_rows_total": 144,
        "easy_majority_rows_accepted_after_hard_exceptions": 143,
        "strict_frontier_triad_delta_agreement_total": 60,
        "strict_frontier_triad_delta_agreement_accepted_after_hard_exceptions": 50,
        "first_governed_review_batch_recommendation": 19,
    }
    for key, expected in expected_counts.items():
        _require(candidate.get(key) == expected, f"candidate_acceptance {key} must be {expected}", errors)
        _require(control.get("validation", {}).get(f"expected_{key}") == expected, f"validation expected_{key} must be {expected}", errors)
    _require(candidate.get("promotion_authority") == "none", "candidate promotion_authority must be none", errors)

    decisions = control.get("approved_decisions", [])
    _require(isinstance(decisions, list) and len(decisions) == 7, "approved_decisions must contain seven decisions", errors)
    decision_ids = {decision.get("decision_id") for decision in decisions if isinstance(decision, dict)}
    _require(decision_ids == REQUIRED_DECISION_IDS, "approved_decisions must contain T468-D1 through T468-D7", errors)
    for decision in decisions:
        if not isinstance(decision, dict):
            errors.append("approved decision must be a mapping")
            continue
        if decision.get("selected_route") != "faithful_route":
            errors.append(f"{decision.get('decision_id')}: selected_route must be faithful_route")

    control_text = paths["control"].read_text(encoding="utf-8")
    for needle in (
        "larger coherent biblical unit",
        "functional list",
        "poem, psalm, lament, song",
        "oracle, vision, symbolic-scene",
        "WJ/red-letter metadata is evidence only",
        "argument movement",
        "Defer output and require a transparent variant/source-tradition packet",
    ):
        if needle not in control_text:
            errors.append(f"control missing faithful-route phrase {needle!r}")

    hard = set(control.get("hard_exceptions_not_downgraded", []))
    _require(REQUIRED_HARD_EXCEPTIONS.issubset(hard), "hard exceptions list missing required cases", errors)

    register_decision = _find_decision(register, "CD-107")
    if register_decision is None:
        errors.append("decision register missing CD-107")
    else:
        _require("T468" in register_decision.get("task_ids", []), "CD-107 must cover T468", errors)
        _require(register_decision.get("classification") == "interpretive_boundary", "CD-107 classification must be interpretive_boundary", errors)
        _require(REQUIRED_REGISTER_NON_AUTHS.issubset(set(register_decision.get("non_authorizations", []))), "CD-107 missing required non-authorizations", errors)
        _require("faithful-route" in register_decision.get("decision", ""), "CD-107 decision must mention faithful-route", errors)

    required_task_ids = set(register.get("backfill_coverage", {}).get("required_task_ids", []))
    _require("T468" in required_task_ids, "backfill_coverage.required_task_ids must include T468", errors)

    lesson = None
    for item in lesson_index.get("lessons", []):
        if isinstance(item, dict) and item.get("lesson_id") == "LSN-052":
            lesson = item
            break
    if lesson is None:
        errors.append("lesson index missing LSN-052")
    else:
        _require("T468" in lesson.get("related_task_ids", []), "LSN-052 must cover T468", errors)
        _require("CD-107" in lesson.get("related_decision_ids", []), "LSN-052 must reference CD-107", errors)
        _require("faithful-route" in " ".join(lesson.get("tags", [])), "LSN-052 tags must include faithful-route", errors)
        _require("faithful_route_policy_as_reviewed_gold" in lesson.get("non_authorizations", []), "LSN-052 must forbid faithful policy as reviewed gold", errors)

    for text_label, text in (("status", status_text), ("handoff", handoff_text), ("roadmap", roadmap_text)):
        for needle in ("T468", "faithful", "non-authorizing", "reviewed gold", "chunk output"):
            if needle not in text:
                errors.append(f"{text_label} missing required text {needle!r}")
    _require("deferred_due_to_interface_drift" in control_text, "control must record DAD reporting deferral", errors)

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    errors = validate_t468_package(args.root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("T468 owner faithful-route chunking policy validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
