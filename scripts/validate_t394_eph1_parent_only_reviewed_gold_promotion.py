#!/usr/bin/env python3
"""Validate the T394 Eph.1.3-Eph.1.14 parent-only reviewed-gold promotion."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
PROMOTION = ROOT / ".ai" / "control" / "t394_eph1_parent_only_reviewed_gold_promotion.yaml"
PACKET = ROOT / ".ai" / "control" / "t393_eph1_reviewed_gold_promotion_decision_packet.yaml"
REVIEW_PACKET = ROOT / "eval" / "chunking_gold" / "review_packets" / "eph1_3_14_argument_review.md"
MANIFEST = ROOT / "eval" / "chunking_gold" / "per_form" / "epistle_argument_gold_manifest.json"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
LESSON_INDEX = ROOT / ".ai" / "control" / "chunking_lesson_index.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
ROADMAP = ROOT / "ROADMAP_STATE.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"
ROADMAP_DOC = ROOT / "docs" / "roadmap" / "T394_EPH1_PARENT_ONLY_REVIEWED_GOLD_PROMOTION.md"
TASK = ROOT / ".ai" / "tasks" / "T394.task.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T394" / "handoff.md"
AUDIT = ROOT / ".ai" / "audits" / "reports" / "20260623-T394-eph1-parent-only-reviewed-gold-promotion.md"
PROJECT_STATUS = ROOT / ".ai" / "control" / "PROJECT_STATUS.md"
CURRENT_FOCUS = ROOT / ".ai" / "control" / "current_focus.yaml"
VALIDATE_ALL = ROOT / "scripts" / "validate_all.py"

PROMOTION_REL = ".ai/control/t394_eph1_parent_only_reviewed_gold_promotion.yaml"
PACKET_REL = ".ai/control/t393_eph1_reviewed_gold_promotion_decision_packet.yaml"
MANIFEST_REL = "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json"
REVIEW_PACKET_REL = "eval/chunking_gold/review_packets/eph1_3_14_argument_review.md"
ROADMAP_DOC_REL = "docs/roadmap/T394_EPH1_PARENT_ONLY_REVIEWED_GOLD_PROMOTION.md"
VALIDATOR_REL = "scripts/validate_t394_eph1_parent_only_reviewed_gold_promotion.py"
TEST_REL = "tests/test_t394_eph1_parent_only_reviewed_gold_promotion.py"

REQUIRED_FALSE_AUTHORITY = {
    "authorizes_parent_span_as_chunk_boundary",
    "authorizes_child_spans",
    "authorizes_preferred_reading",
    "authorizes_source_tradition_preference",
    "authorizes_canon_scope_change",
    "authorizes_boundary_import",
    "authorizes_route_behavior",
    "authorizes_evaluator_change",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_embedding_or_vector_work",
    "authorizes_chunk_output_change",
    "authorizes_implementation",
    "authorizes_sqlite_database_creation",
    "authorizes_metadata_row_population",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "parent_span_as_chunk_boundary",
    "child_span_selection",
    "child_span_reviewed_gold_promotion",
    "permanent_child_span_denial",
    "preferred_reading_selection",
    "source_tradition_preference",
    "current_sidecar_silence_as_universal_variant_claim",
    "canon_scope_change",
    "boundary_import",
    "noncanonical_source_authority",
    "source_metadata_as_authority",
    "paragraph_marker_as_chunk_boundary",
    "strong_number_as_lexical_truth",
    "denominational_systematic_theology_as_chunk_authority",
    "liberal_critical_default",
    "anti_supernatural_default",
    "route_behavior_change",
    "evaluator_change",
    "graph_edge_generation",
    "retrieval_truth",
    "embedding_or_vector_work",
    "chunk_output_change",
    "implementation_authority",
    "sqlite_database_creation",
    "metadata_row_population",
    "source_or_manuscript_row_population",
}

FORBIDDEN_TRUE_FLAGS = {
    "parent_span_as_chunk_boundary_authorized",
    "child_spans_authorized",
    "output_change_authorized",
    "implementation_authorized",
    "route_behavior_authorized",
    "evaluator_change_authorized",
    "graph_edge_generation_allowed",
    "retrieval_truth_authorized",
    "embedding_or_vector_work_allowed",
    "chunk_output_change_authorized",
}


class T394PromotionError(ValueError):
    """Raised when T394 promotion state is unsafe or stale."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise T394PromotionError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise T394PromotionError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise T394PromotionError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise T394PromotionError(f"{_rel(path)}: JSON unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise T394PromotionError(f"{_rel(path)}: expected a JSON object")
    return data


def _string_list(value: Any, label: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not allow_empty and not value):
        raise T394PromotionError(f"{label} must be a {'possibly empty ' if allow_empty else ''}list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise T394PromotionError(f"{label} must contain only non-empty strings")
    return value


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    missing = sorted(required - set(_string_list(actual, label)))
    if missing:
        raise T394PromotionError(f"{label} missing {missing}")


def _reject_true_flag(value: Any, forbidden_keys: set[str], label: str) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in forbidden_keys and child is True:
                raise T394PromotionError(f"{label}.{key} must not be true")
            _reject_true_flag(child, forbidden_keys, f"{label}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _reject_true_flag(child, forbidden_keys, f"{label}[{index}]")


def _validate_promotion_record(path: Path) -> dict[str, Any]:
    data = _read_yaml(path)
    expected = {
        "object_type": "parent_only_reviewed_gold_promotion_record",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "parent_only_reviewed_gold_promotion_record.v1",
        "record_id": "t394_eph1_3_14_parent_only_reviewed_gold_promotion",
        "task_id": "T394",
        "owner": "Lowell Wong",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise T394PromotionError(f"{_rel(path)}: {key} must be {value!r}")

    owner = data.get("owner_decision")
    if not isinstance(owner, dict):
        raise T394PromotionError(f"{_rel(path)}: owner_decision must be a mapping")
    expected_owner = {
        "selected_option": "T393-A",
        "decision_packet": PACKET_REL,
        "selected_parent": "Eph.1.3-Eph.1.14",
        "boundary_dependency_or_non_dependency": "current_repo_variant_non_dependent",
        "reviewed_gold_dependency_or_non_dependency": "current_repo_variant_non_dependent",
        "source_tradition_dependency_or_non_dependency": "current_repo_source_tradition_non_dependent",
        "child_span_necessity_or_denial": "child_spans_not_necessary_now_and_not_authorized",
        "parent_only_promotion_authorized_or_held": "authorized_parent_only_reviewed_gold",
        "decision_register_update": "CD-071",
    }
    for key, value in expected_owner.items():
        if owner.get(key) != value:
            raise T394PromotionError(f"{_rel(path)}: owner_decision.{key} must be {value!r}")
    if "Authorize T393-A" not in str(owner.get("exact_owner_confirmation", "")):
        raise T394PromotionError(f"{_rel(path)}: exact_owner_confirmation is stale")
    if owner.get("selected_children") != []:
        raise T394PromotionError(f"{_rel(path)}: selected_children must remain []")
    if owner.get("exact_internal_variant_refs") != []:
        raise T394PromotionError(f"{_rel(path)}: exact_internal_variant_refs must remain []")

    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise T394PromotionError(f"{_rel(path)}: authority must be a mapping")
    for key in (
        "records_owner_selection",
        "authorizes_current_repo_variant_non_dependency_finding_for_exact_parent_only_promotion",
        "authorizes_current_repo_source_tradition_non_dependency_finding_for_exact_parent_only_promotion",
        "authorizes_parent_only_reviewed_gold_promotion",
    ):
        if authority.get(key) is not True:
            raise T394PromotionError(f"{_rel(path)}: authority.{key} must be true")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise T394PromotionError(f"{_rel(path)}: authority.{key} must be false")

    scope = data.get("scope")
    if not isinstance(scope, dict):
        raise T394PromotionError(f"{_rel(path)}: scope must be a mapping")
    expected_scope = {
        "selected_parent": "Eph.1.3-Eph.1.14",
        "review_packet": REVIEW_PACKET_REL,
        "promotion_decision_packet": PACKET_REL,
        "reviewed_gold_manifest": MANIFEST_REL,
        "reviewed_gold_case_id": "eph1_3_14_parent_only_reviewed_gold",
    }
    for key, value in expected_scope.items():
        if scope.get(key) != value:
            raise T394PromotionError(f"{_rel(path)}: scope.{key} must be {value!r}")
    if scope.get("selected_children") != []:
        raise T394PromotionError(f"{_rel(path)}: scope.selected_children must remain []")

    finding = data.get("variant_and_source_tradition_findings")
    if not isinstance(finding, dict):
        raise T394PromotionError(f"{_rel(path)}: variant_and_source_tradition_findings must be a mapping")
    if finding.get("exact_internal_variant_refs") != []:
        raise T394PromotionError(f"{_rel(path)}: exact_internal_variant_refs must remain []")
    if finding.get("internal_target_variant_observed_in_current_sidecars") is not False:
        raise T394PromotionError(f"{_rel(path)}: internal target variant flag must be false")
    for key, value in {
        "finding": "current_repo_non_dependent_for_parent_boundary_and_parent_only_reviewed_gold_claim",
        "source_tradition_finding": "current_repo_source_tradition_non_dependent_for_parent_boundary_and_parent_only_reviewed_gold_claim",
    }.items():
        if finding.get(key) != value:
            raise T394PromotionError(f"{_rel(path)}: {key} is stale")
    limit_text = " ".join(_string_list(finding.get("limits"), "variant limits"))
    for phrase in ("current repo evidence", "does not claim universal textual-critical certainty", "does not select a preferred reading", "does not prefer a source tradition"):
        if phrase not in limit_text:
            raise T394PromotionError(f"{_rel(path)}: variant/source-tradition limits missing {phrase!r}")

    child = data.get("child_span_finding")
    if not isinstance(child, dict):
        raise T394PromotionError(f"{_rel(path)}: child_span_finding must be a mapping")
    if child.get("child_spans_necessary_now") is not False:
        raise T394PromotionError(f"{_rel(path)}: child spans must not be necessary now")
    if child.get("child_spans_authorized") is not False:
        raise T394PromotionError(f"{_rel(path)}: child spans must not be authorized")
    if child.get("permanent_child_span_denial") is not False:
        raise T394PromotionError(f"{_rel(path)}: permanent child-span denial must be false")

    promotion = data.get("promotion_scope")
    if not isinstance(promotion, dict):
        raise T394PromotionError(f"{_rel(path)}: promotion_scope must be a mapping")
    if promotion.get("promoted_as_reviewed_gold") is not True:
        raise T394PromotionError(f"{_rel(path)}: promoted_as_reviewed_gold must be true")
    if promotion.get("next_allowed_task") != "T397":
        raise T394PromotionError(f"{_rel(path)}: next_allowed_task must be T397")
    for key in FORBIDDEN_TRUE_FLAGS:
        if promotion.get(key) is not False and key in promotion:
            raise T394PromotionError(f"{_rel(path)}: promotion_scope.{key} must be false")

    _require_subset(REQUIRED_NON_AUTHORIZATIONS, data.get("non_authorizations"), "non_authorizations")
    _reject_true_flag(data, FORBIDDEN_TRUE_FLAGS, "promotion_record")
    return data


def _validate_t393_packet() -> None:
    packet = _read_yaml(PACKET)
    if packet.get("status") != "resolved_by_t393_a":
        raise T394PromotionError(f"{_rel(PACKET)}: status must be resolved_by_t393_a")
    selection = packet.get("owner_selection", {})
    expected = {
        "owner_selection_status": "selected",
        "selected_option": "T393-A",
        "selected_parent": "Eph.1.3-Eph.1.14",
        "selected_children": [],
        "reviewed_gold_promoted": False,
        "recommendation_is_owner_selection": False,
        "owner_response_record": PROMOTION_REL,
    }
    for key, value in expected.items():
        if selection.get(key) != value:
            raise T394PromotionError(f"{_rel(PACKET)}: owner_selection.{key} must be {value!r}")
    response = packet.get("owner_response", {})
    for key, value in {
        "response_status": "selected",
        "task_id": "T394",
        "selected_option": "T393-A",
        "owner_response_record": PROMOTION_REL,
        "exact_parent": "Eph.1.3-Eph.1.14",
        "boundary_dependency_or_non_dependency": "current_repo_variant_non_dependent",
        "reviewed_gold_dependency_or_non_dependency": "current_repo_variant_non_dependent",
        "source_tradition_dependency_or_non_dependency": "current_repo_source_tradition_non_dependent",
        "child_span_necessity_or_denial": "child_spans_not_necessary_now_and_not_authorized",
        "parent_only_reviewed_gold_authorized_or_held": "authorized_parent_only_reviewed_gold",
        "decision_register_update": "CD-071",
    }.items():
        if response.get(key) != value:
            raise T394PromotionError(f"{_rel(PACKET)}: owner_response.{key} must be {value!r}")
    if response.get("selected_children") != [] or response.get("exact_internal_variant_refs") != []:
        raise T394PromotionError(f"{_rel(PACKET)}: T393 response children/variants must be []")


def _validate_manifest() -> None:
    data = _read_json(MANIFEST)
    if data.get("manifest_id") != "epistle-argument-gold-v0":
        raise T394PromotionError(f"{_rel(MANIFEST)}: manifest_id is stale")
    cases = data.get("reviewed_gold")
    if not isinstance(cases, list):
        raise T394PromotionError(f"{_rel(MANIFEST)}: reviewed_gold must be a list")
    by_case = {item.get("case_id"): item for item in cases if isinstance(item, dict)}
    case = by_case.get("eph1_3_14_parent_only_reviewed_gold")
    if not isinstance(case, dict):
        raise T394PromotionError(f"{_rel(MANIFEST)}: missing Ephesians T394 reviewed-gold case")
    if case.get("status") != "reviewed_gold":
        raise T394PromotionError(f"{_rel(MANIFEST)}: T394 case must be reviewed_gold")
    if case.get("osis_span") != "Eph.1.3-Eph.1.14":
        raise T394PromotionError(f"{_rel(MANIFEST)}: T394 case span is wrong")
    owner = case.get("owner_decision", {})
    expected_owner = {
        "task_id": "T394",
        "record": PROMOTION_REL,
        "decision_packet": PACKET_REL,
        "selected_option": "T393-A",
        "decision": "promote_parent_only_reviewed_gold",
        "reviewed_gold_promoted": True,
        "implementation_allowed": False,
        "output_change_authorized": False,
    }
    for key, value in expected_owner.items():
        if owner.get(key) != value:
            raise T394PromotionError(f"{_rel(MANIFEST)}: owner_decision.{key} must be {value!r}")
    if owner.get("variant_refs") != []:
        raise T394PromotionError(f"{_rel(MANIFEST)}: variant_refs must remain []")
    expected = case.get("expected", {})
    if expected.get("parent_only_reviewed_gold") is not True:
        raise T394PromotionError(f"{_rel(MANIFEST)}: parent_only_reviewed_gold must be true")
    if expected.get("selected_children") != []:
        raise T394PromotionError(f"{_rel(MANIFEST)}: selected_children must be []")
    if case.get("variant_non_dependency") != []:
        raise T394PromotionError(f"{_rel(MANIFEST)}: variant_non_dependency must remain []")
    child = case.get("child_span_decision", {})
    if child.get("child_spans_necessary_now") is not False or child.get("child_spans_authorized") is not False:
        raise T394PromotionError(f"{_rel(MANIFEST)}: child spans must be denied")
    _reject_true_flag(case, FORBIDDEN_TRUE_FLAGS, "manifest_case")


def _validate_links() -> None:
    linked_requirements = (
        (REVIEW_PACKET, ("Eph.1.3-Eph.1.14", "Reviewed gold promoted: false")),
        (REGISTER, ("CD-071", PROMOTION_REL, MANIFEST_REL, "T393-A")),
        (LESSON_INDEX, ("LSN-025", "Parent-only reviewed gold is not implementation authority", PROMOTION_REL)),
        (PREFLIGHT, (PROMOTION_REL, "CD-071", "LSN-025")),
        (READINESS, ("task_id: T394", PROMOTION_REL, "reviewed_gold_promoted: true", "next_task: T397")),
        (ROADMAP, ("id: T394", "complete_parent_only_reviewed_gold_promoted", PROMOTION_REL)),
        (FRONT_DOOR, (PROMOTION_REL, "T394", "Goal 6 route-isolated harness")),
        (TOC, ("t394", PROMOTION_REL, "eph1_3_14_parent_only_reviewed_gold")),
        (ROADMAP_TOC, ("T394 | Eph.1.3-Eph.1.14 parent-only reviewed-gold promotion", ROADMAP_DOC_REL)),
        (ROADMAP_DOC, ("T394 Eph.1.3-Eph.1.14 Parent-Only Reviewed-Gold Promotion", "T397 - Route-Isolated Implementation Harness")),
        (TASK, ("id: T394", "CD-071", "LSN-025")),
        (HANDOFF, ("task_id: T394", "T393-A", PROMOTION_REL)),
        (AUDIT, ("T394", "reviewed gold", "Not authorized")),
        (PROJECT_STATUS, ("T394 Eph.1.3-Eph.1.14 parent-only reviewed-gold promotion", "T397")),
        (CURRENT_FOCUS, ("current_task: T394", PROMOTION_REL)),
        (VALIDATE_ALL, ("validate_t394_eph1_parent_only_reviewed_gold_promotion.py",)),
    )
    for path, phrases in linked_requirements:
        text = _read_text(path)
        for phrase in phrases:
            if phrase not in text:
                raise T394PromotionError(f"{_rel(path)}: missing {phrase!r}")


def validate_t394_eph1_parent_only_reviewed_gold_promotion(path: Path = PROMOTION) -> dict[str, Any]:
    data = _validate_promotion_record(path)
    _validate_t393_packet()
    _validate_manifest()
    _validate_links()
    return data


def main() -> int:
    try:
        validate_t394_eph1_parent_only_reviewed_gold_promotion()
    except T394PromotionError as exc:
        print(f"T394 Eph.1.3-Eph.1.14 promotion validation failed: {exc}", file=sys.stderr)
        return 1
    print("T394 Eph.1.3-Eph.1.14 parent-only reviewed-gold promotion validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
