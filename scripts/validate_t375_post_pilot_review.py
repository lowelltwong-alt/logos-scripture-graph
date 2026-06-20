#!/usr/bin/env python3
"""Validate the T375 post-pilot review record."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
REVIEW = ROOT / ".ai" / "control" / "t375_post_pilot_review.yaml"
T374_MANIFEST = ROOT / ".ai" / "control" / "t374_additive_parent_overlay_manifest.yaml"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
ROADMAP = ROOT / "ROADMAP_STATE.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
MAIN_TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"
ROADMAP_DOC = ROOT / "docs" / "roadmap" / "T375_POST_PILOT_REVIEW.md"
TASK = ROOT / ".ai" / "tasks" / "T375.task.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T375" / "handoff.md"
T374_AUDIT = ROOT / ".ai" / "audits" / "reports" / "20260620-T374-additive-parent-overlay.md"
T375_AUDIT = ROOT / ".ai" / "audits" / "reports" / "20260620-T375-post-pilot-review.md"

REVIEW_REL = ".ai/control/t375_post_pilot_review.yaml"
VALIDATOR_REL = "scripts/validate_t375_post_pilot_review.py"
DOC_REL = "docs/roadmap/T375_POST_PILOT_REVIEW.md"
AUDIT_REL = ".ai/audits/reports/20260620-T375-post-pilot-review.md"
OVERLAY_ID = (
    "chunk--eng-web--chunk-policy-v0.1.0--epistles-parent-overlay--"
    "1Cor.8.1--1Cor.10.33--T374-OVERLAP-B"
)


class T375ReviewError(ValueError):
    """Raised when the T375 review is stale or unsafe."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise T375ReviewError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise T375ReviewError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise T375ReviewError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    if not isinstance(actual, list):
        raise T375ReviewError(f"{label} must be a list")
    missing = sorted(required - {str(item) for item in actual})
    if missing:
        raise T375ReviewError(f"{label} missing {missing}")


def _validate_static(review: dict[str, Any]) -> None:
    expected = {
        "object_type": "t375_post_pilot_review",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "t375_post_pilot_review.v1",
        "review_id": "t375_1cor8_10_post_pilot_review",
        "task_id": "T375",
        "status": "complete_review_only_child_spans_not_necessary_now",
    }
    for key, value in expected.items():
        if review.get(key) != value:
            raise T375ReviewError(f"{REVIEW_REL}: {key} must be {value!r}")

    scope = review.get("scope")
    if not isinstance(scope, dict):
        raise T375ReviewError(f"{REVIEW_REL}: scope must be a mapping")
    expected_scope = {
        "lane": "epistle_argument",
        "selected_target": "1cor8_10_food_offered_to_idols",
        "selected_passage": "1Cor.8-1Cor.10",
        "selected_parent": "1Cor.8.1-1Cor.10.33",
        "prior_reviewed_gold_case_id": "1cor8_10_parent_only_reviewed_gold",
        "prior_implementation_task": "T374",
        "implementation_manifest": ".ai/control/t374_additive_parent_overlay_manifest.yaml",
        "prior_decision_register_entry": "CD-056",
        "decision_register_entry": "CD-057",
    }
    for key, value in expected_scope.items():
        if scope.get(key) != value:
            raise T375ReviewError(f"{REVIEW_REL}: scope.{key} must be {value!r}")
    if scope.get("selected_children") != []:
        raise T375ReviewError(f"{REVIEW_REL}: scope.selected_children must be []")

    authority = review.get("authority")
    if not isinstance(authority, dict):
        raise T375ReviewError(f"{REVIEW_REL}: authority must be a mapping")
    for required_true in (
        "records_post_pilot_review",
        "records_same_baseline_review",
        "records_no_context_audit_review",
        "records_child_necessity_review",
    ):
        if authority.get(required_true) is not True:
            raise T375ReviewError(f"{REVIEW_REL}: authority.{required_true} must be true")
    for required_false in (
        "authorizes_child_spans",
        "authorizes_child_span_reviewed_gold",
        "authorizes_new_chunk_output",
        "authorizes_route_behavior_change",
        "authorizes_evaluator_change",
        "authorizes_graph_edges",
        "authorizes_retrieval_truth",
        "authorizes_embedding_or_vector_work",
        "authorizes_preferred_reading",
        "authorizes_source_tradition_preference",
        "authorizes_boundary_import",
        "authorizes_broader_epistle_generalization",
        "authorizes_whole_bible_output_pass",
    ):
        if authority.get(required_false) is not False:
            raise T375ReviewError(f"{REVIEW_REL}: authority.{required_false} must be false")

    same_baseline = review.get("same_baseline_review")
    if not isinstance(same_baseline, dict):
        raise T375ReviewError(f"{REVIEW_REL}: same_baseline_review must be a mapping")
    expected_same = {
        "source_manifest": ".ai/control/t374_additive_parent_overlay_manifest.yaml",
        "evaluator": "pipelines/chunking/evaluate_chunks.py",
        "evaluator_formula_changed": False,
        "leaderboard_updated": False,
        "improvement_claim_allowed": False,
        "finding": "no_safety_regression_no_improvement_claim",
        "baseline_chunk_count": 1136,
        "candidate_chunk_count": 1137,
        "added_overlay_count": 1,
        "baseline_prefix_matches_pre_t374_bytes": True,
        "non_target_output_diff_detected": False,
        "baseline_chunk_sha256": "eda6232b2cb7f0ab4c8dacac10ed672c247a1e41ccb1f807ace05d0ca9eec619",
        "candidate_chunk_sha256": "681a0840edd8513daeb204579ed0a1b0b0f818c910abfc83a7890317c3b481e7",
    }
    for key, value in expected_same.items():
        if same_baseline.get(key) != value:
            raise T375ReviewError(f"{REVIEW_REL}: same_baseline_review.{key} must be {value!r}")

    audit = review.get("no_context_audit_review")
    if not isinstance(audit, dict):
        raise T375ReviewError(f"{REVIEW_REL}: no_context_audit_review must be a mapping")
    if audit.get("finding") != "audit_trail_sufficient_for_external_no_context_review":
        raise T375ReviewError(f"{REVIEW_REL}: audit finding is stale")
    _require_subset(
        {
            "exact_owner_selection",
            "implementation_manifest",
            "output_hashes",
            "baseline_prefix_identity",
            "same_baseline_metrics",
            "non_authorizations",
            "decision_register_links",
            "next_route_statement",
        },
        audit.get("required_context_present"),
        "no_context_audit_review.required_context_present",
    )

    child = review.get("child_necessity_review")
    if not isinstance(child, dict):
        raise T375ReviewError(f"{REVIEW_REL}: child_necessity_review must be a mapping")
    if child.get("finding") != "child_spans_not_necessary_now":
        raise T375ReviewError(f"{REVIEW_REL}: child_necessity_review.finding must keep children unnecessary now")
    if child.get("current_child_span_authority") != "none":
        raise T375ReviewError(f"{REVIEW_REL}: child span authority must be none")
    if child.get("selected_children") != []:
        raise T375ReviewError(f"{REVIEW_REL}: child selected_children must be []")
    candidates = child.get("child_span_candidates_not_promoted")
    if not isinstance(candidates, list) or len(candidates) != 6:
        raise T375ReviewError(f"{REVIEW_REL}: expected six non-promoted child candidates")
    _require_subset(
        {
            "exact_child_spans",
            "governed_child_evidence",
            "theological_risk_review",
            "owner_promotion",
            "decision_register_update",
            "validators_and_tests",
            "non_target_identity_proof",
            "same_baseline_evaluation",
        },
        child.get("later_child_span_gate_must_include"),
        "child_necessity_review.later_child_span_gate_must_include",
    )

    next_route = review.get("next_route")
    if not isinstance(next_route, dict):
        raise T375ReviewError(f"{REVIEW_REL}: next_route must be a mapping")
    if next_route.get("task_id") != "T376" or next_route.get("owner_decision_required") is not True:
        raise T375ReviewError(f"{REVIEW_REL}: next route must be T376 owner decision")
    _require_subset(
        {
            "child_span_selection",
            "automatic_child_spans_after_parent_pilot",
            "treating_t374_overlay_as_truth_bearing_hierarchy",
            "graph_edge_generation",
            "retrieval_truth",
            "evaluator_change",
            "whole_bible_output_pass",
        },
        review.get("non_authorizations"),
        "non_authorizations",
    )


def _validate_manifest_alignment(review: dict[str, Any]) -> None:
    manifest = _read_yaml(T374_MANIFEST)
    output = manifest.get("output_change", {})
    overlay = manifest.get("overlay_record", {})
    same = review["same_baseline_review"]
    if output.get("baseline_chunk_count") != same["baseline_chunk_count"]:
        raise T375ReviewError("T375 baseline count does not match T374 manifest")
    if output.get("candidate_chunk_count") != same["candidate_chunk_count"]:
        raise T375ReviewError("T375 candidate count does not match T374 manifest")
    if output.get("added_overlay_count") != same["added_overlay_count"]:
        raise T375ReviewError("T375 added overlay count does not match T374 manifest")
    if output.get("baseline_prefix_matches_pre_t374_bytes") is not True:
        raise T375ReviewError("T374 manifest no longer proves baseline prefix identity")
    if output.get("non_target_output_diff_detected") is not False:
        raise T375ReviewError("T374 manifest reports non-target output diff")
    if overlay.get("id") != OVERLAY_ID:
        raise T375ReviewError("T374 overlay id is stale")
    if overlay.get("selected_children") != []:
        raise T375ReviewError("T374 overlay must remain parent-only")
    if overlay.get("child_span_authorized") is not False:
        raise T375ReviewError("T374 overlay must not authorize child spans")


def _validate_links() -> None:
    linked_requirements = (
        (REGISTER, ("CD-057", "T375 post-pilot review keeps child spans unnecessary now", REVIEW_REL)),
        (PREFLIGHT, ("CD-057", REVIEW_REL, "child spans are not necessary now")),
        (READINESS, ("task_id: T376", REVIEW_REL, "child_spans_not_necessary_now")),
        (ROADMAP, ("id: T375", "complete_review_only_child_spans_not_necessary_now", REVIEW_REL, "id: T376")),
        (FRONT_DOOR, (REVIEW_REL, VALIDATOR_REL, "T376 owner lane selection")),
        (MAIN_TOC, (REVIEW_REL, VALIDATOR_REL, "post-pilot-review")),
        (ROADMAP_TOC, (REVIEW_REL, DOC_REL, "T375 | Post-pilot review")),
        (ROADMAP_DOC, (REVIEW_REL, "child spans are not necessary now", "T376")),
        (TASK, ("id: T375", "complete_review_only_child_spans_not_necessary_now", REVIEW_REL)),
        (HANDOFF, ("task_id: T375", "CD-057", "T376 owner lane selection")),
        (T374_AUDIT, ("T374 Additive Parent Overlay", "T375 is the next route")),
        (T375_AUDIT, ("T375 Post-Pilot", REVIEW_REL, "child spans are not necessary now")),
    )
    for path, phrases in linked_requirements:
        text = _read_text(path)
        for phrase in phrases:
            if phrase not in text:
                raise T375ReviewError(f"{_rel(path)}: missing {phrase!r}")


def validate_t375_post_pilot_review(path: Path = REVIEW) -> dict[str, Any]:
    review = _read_yaml(path)
    _validate_static(review)
    _validate_manifest_alignment(review)
    _validate_links()
    return review


def main() -> int:
    try:
        validate_t375_post_pilot_review()
    except T375ReviewError as exc:
        print(f"T375 post-pilot review validation failed: {exc}", file=sys.stderr)
        return 1
    print("T375 post-pilot review validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
