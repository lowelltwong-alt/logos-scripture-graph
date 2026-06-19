#!/usr/bin/env python3
"""Validate the T371-A parent-only reviewed-gold promotion record."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
PROMOTION = ROOT / ".ai" / "control" / "t371_parent_only_reviewed_gold_promotion.yaml"
PACKET = ROOT / ".ai" / "control" / "t371_variant_dependency_owner_decision_packet.yaml"
EVIDENCE = ROOT / "eval" / "chunking_gold" / "review_packets" / "1cor8_10_parent_only_evidence_packet.yaml"
MANIFEST = ROOT / "eval" / "chunking_gold" / "per_form" / "epistle_argument_gold_manifest.json"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
FORECAST = ROOT / ".ai" / "control" / "chunking_human_decision_forecast.yaml"
ROADMAP = ROOT / "ROADMAP_STATE.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"

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
}

REQUIRED_NON_AUTHORIZATIONS = {
    "preferred_reading_selection",
    "critical_text_default",
    "majority_text_default",
    "textus_receptus_default",
    "current_source_as_hidden_textual_policy",
    "source_tradition_preference",
    "canon_scope_change",
    "boundary_import",
    "noncanonical_source_authority",
    "parent_span_as_chunk_boundary",
    "child_span_selection",
    "argument_outline_as_child_boundary",
    "paragraph_marker_as_chunk_boundary",
    "source_metadata_as_authority",
    "cross_reference_as_graph_edge",
    "strong_number_as_lexical_truth",
    "capitalization_as_divine_identity",
    "route_behavior_change",
    "evaluator_change",
    "graph_edge_generation",
    "retrieval_truth",
    "embedding_or_vector_work",
    "chunk_output_change",
    "implementation_authority",
}


class T371PromotionError(ValueError):
    """Raised when T371-A promotion state is unsafe or stale."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise T371PromotionError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise T371PromotionError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise T371PromotionError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise T371PromotionError(f"{_rel(path)}: JSON unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise T371PromotionError(f"{_rel(path)}: expected a JSON object")
    return data


def _string_list(value: Any, label: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not allow_empty and not value):
        raise T371PromotionError(f"{label} must be a {'possibly empty ' if allow_empty else ''}list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise T371PromotionError(f"{label} must contain only non-empty strings")
    return value


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    missing = sorted(required - set(_string_list(actual, label)))
    if missing:
        raise T371PromotionError(f"{label} missing {missing}")


def _reject_true_flag(value: Any, forbidden_keys: set[str], label: str) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in forbidden_keys and child is True:
                raise T371PromotionError(f"{label}.{key} must not be true")
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
        "record_id": "t371_1cor8_10_parent_only_reviewed_gold_promotion",
        "task_id": "T371",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise T371PromotionError(f"{_rel(path)}: {key} must be {value!r}")

    owner = data.get("owner_decision")
    if not isinstance(owner, dict):
        raise T371PromotionError(f"{_rel(path)}: owner_decision must be a mapping")
    expected_owner = {
        "selected_option": "T371-A",
        "decision_packet": ".ai/control/t371_variant_dependency_owner_decision_packet.yaml",
        "selected_parent": "1Cor.8.1-1Cor.10.33",
        "boundary_dependency_or_non_dependency": "variant_non_dependent",
        "reviewed_gold_dependency_or_non_dependency": "variant_non_dependent",
        "parent_only_promotion_authorized_or_held": "authorized_parent_only_reviewed_gold",
        "decision_register_update": "CD-047",
    }
    for key, value in expected_owner.items():
        if owner.get(key) != value:
            raise T371PromotionError(f"{_rel(path)}: owner_decision.{key} must be {value!r}")
    if owner.get("selected_children") != []:
        raise T371PromotionError(f"{_rel(path)}: selected_children must remain []")
    if set(owner.get("exact_variant_refs", [])) != {"1Cor.9.20", "1Cor.10.9"}:
        raise T371PromotionError(f"{_rel(path)}: exact_variant_refs must be 1Cor.9.20 and 1Cor.10.9")
    if "lets go path t371-a confirmed" not in str(owner.get("exact_owner_confirmation", "")):
        raise T371PromotionError(f"{_rel(path)}: exact_owner_confirmation is stale")

    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise T371PromotionError(f"{_rel(path)}: authority must be a mapping")
    for key in (
        "records_owner_selection",
        "authorizes_variant_non_dependency_finding_for_exact_parent_only_promotion",
        "authorizes_parent_only_reviewed_gold_promotion",
    ):
        if authority.get(key) is not True:
            raise T371PromotionError(f"{_rel(path)}: authority.{key} must be true")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise T371PromotionError(f"{_rel(path)}: authority.{key} must be false")

    scope = data.get("scope")
    if not isinstance(scope, dict):
        raise T371PromotionError(f"{_rel(path)}: scope must be a mapping")
    expected_scope = {
        "selected_parent": "1Cor.8.1-1Cor.10.33",
        "reviewed_gold_manifest": "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json",
        "reviewed_gold_case_id": "1cor8_10_parent_only_reviewed_gold",
        "evidence_packet": "eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml",
    }
    for key, value in expected_scope.items():
        if scope.get(key) != value:
            raise T371PromotionError(f"{_rel(path)}: scope.{key} must be {value!r}")
    if scope.get("selected_children") != []:
        raise T371PromotionError(f"{_rel(path)}: scope.selected_children must remain []")

    findings = data.get("variant_non_dependency_findings")
    if not isinstance(findings, list):
        raise T371PromotionError(f"{_rel(path)}: variant_non_dependency_findings must be a list")
    by_ref = {item.get("ref"): item for item in findings if isinstance(item, dict)}
    if set(by_ref) != {"1Cor.9.20", "1Cor.10.9"}:
        raise T371PromotionError(f"{_rel(path)}: findings must cover exact T371 refs")
    for ref, item in by_ref.items():
        if item.get("finding") != "non_dependent_for_parent_boundary_and_parent_only_reviewed_gold_claim":
            raise T371PromotionError(f"{_rel(path)}: {ref}.finding is stale")
        if "Does not" not in str(item.get("limit", "")):
            raise T371PromotionError(f"{_rel(path)}: {ref}.limit must preserve non-authorizations")

    promotion = data.get("promotion_scope")
    if not isinstance(promotion, dict):
        raise T371PromotionError(f"{_rel(path)}: promotion_scope must be a mapping")
    if promotion.get("promoted_as_reviewed_gold") is not True:
        raise T371PromotionError(f"{_rel(path)}: promotion_scope.promoted_as_reviewed_gold must be true")
    for key in (
        "parent_span_as_chunk_boundary_authorized",
        "child_spans_authorized",
        "output_change_authorized",
        "implementation_authorized",
        "route_behavior_authorized",
        "evaluator_change_authorized",
        "graph_edge_generation_allowed",
        "retrieval_truth_authorized",
    ):
        if promotion.get(key) is not False:
            raise T371PromotionError(f"{_rel(path)}: promotion_scope.{key} must be false")
    if promotion.get("next_allowed_task") != "T372":
        raise T371PromotionError(f"{_rel(path)}: next_allowed_task must be T372")
    if promotion.get("later_owner_gate_required_before_output") != "T373":
        raise T371PromotionError(f"{_rel(path)}: later owner gate must be T373")

    _require_subset(REQUIRED_NON_AUTHORIZATIONS, data.get("non_authorizations"), "non_authorizations")
    return data


def _validate_manifest() -> None:
    data = _read_json(MANIFEST)
    if data.get("manifest_id") != "epistle-argument-gold-v0":
        raise T371PromotionError(f"{_rel(MANIFEST)}: manifest_id is stale")
    if data.get("target_form") != "epistle_argument":
        raise T371PromotionError(f"{_rel(MANIFEST)}: target_form must be epistle_argument")
    cases = data.get("reviewed_gold")
    if not isinstance(cases, list):
        raise T371PromotionError(f"{_rel(MANIFEST)}: reviewed_gold must be a list")
    by_case = {item.get("case_id"): item for item in cases if isinstance(item, dict)}
    case = by_case.get("1cor8_10_parent_only_reviewed_gold")
    if not isinstance(case, dict):
        raise T371PromotionError(f"{_rel(MANIFEST)}: missing 1cor8_10 parent-only case")
    if case.get("status") != "reviewed_gold":
        raise T371PromotionError(f"{_rel(MANIFEST)}: T371 case must be reviewed_gold")
    if case.get("osis_span") != "1Cor.8.1-1Cor.10.33":
        raise T371PromotionError(f"{_rel(MANIFEST)}: T371 case span is wrong")
    owner = case.get("owner_decision", {})
    if owner.get("selected_option") != "T371-A" or owner.get("record") != ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml":
        raise T371PromotionError(f"{_rel(MANIFEST)}: owner_decision must link T371-A record")
    expected = case.get("expected", {})
    if expected.get("selected_children") != []:
        raise T371PromotionError(f"{_rel(MANIFEST)}: expected.selected_children must be []")
    if expected.get("parent_only_reviewed_gold") is not True:
        raise T371PromotionError(f"{_rel(MANIFEST)}: parent_only_reviewed_gold must be true")
    for key in (
        "parent_span_as_chunk_boundary_authorized",
        "route_behavior_authorized",
        "evaluator_change_authorized",
        "graph_edge_generation_allowed",
        "retrieval_truth_authorized",
        "chunk_output_change_authorized",
        "implementation_authorized",
    ):
        if expected.get(key) is not False:
            raise T371PromotionError(f"{_rel(MANIFEST)}: expected.{key} must be false")
    refs = {item.get("ref") for item in case.get("variant_non_dependency", []) if isinstance(item, dict)}
    if refs != {"1Cor.9.20", "1Cor.10.9"}:
        raise T371PromotionError(f"{_rel(MANIFEST)}: variant_non_dependency refs are stale")
    _reject_true_flag(
        case,
        {
            "output_change_authorized",
            "implementation_authorized",
            "route_behavior_authorized",
            "evaluator_change_authorized",
            "graph_edge_generation_allowed",
            "retrieval_truth_authorized",
            "chunk_output_change_authorized",
            "parent_span_as_chunk_boundary_authorized",
        },
        "manifest_case",
    )


def _validate_links() -> None:
    promotion_rel = ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml"
    manifest_rel = "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json"
    for path in (
        PACKET,
        EVIDENCE,
        MANIFEST,
        REGISTER,
        PREFLIGHT,
        READINESS,
        FORECAST,
        ROADMAP,
        FRONT_DOOR,
        TOC,
        ROADMAP_TOC,
    ):
        if not path.exists():
            raise T371PromotionError(f"{_rel(path)}: missing linked surface")

    packet = _read_yaml(PACKET)
    if packet.get("status") != "resolved_by_t371_a":
        raise T371PromotionError(f"{_rel(PACKET)}: packet must be resolved_by_t371_a")
    response = packet.get("owner_response", {})
    if response.get("owner_response_record") != promotion_rel:
        raise T371PromotionError(f"{_rel(PACKET)}: owner_response_record must link promotion")
    if response.get("selected_option") != "T371-A":
        raise T371PromotionError(f"{_rel(PACKET)}: selected option must be T371-A")

    evidence_text = _read_text(EVIDENCE)
    for phrase in ("review_status: ready_for_owner_promotion_review", "reviewed_gold_promoted: false"):
        if phrase not in evidence_text:
            raise T371PromotionError(f"{_rel(EVIDENCE)}: evidence packet must remain historical and non-promoting")

    for path, phrases in (
        (REGISTER, ("CD-047", promotion_rel, manifest_rel, "T371-A")),
        (PREFLIGHT, (promotion_rel, manifest_rel, "CD-047")),
        (READINESS, (promotion_rel, manifest_rel, "T372", "reviewed_gold_promoted: true")),
        (FORECAST, ("HDF-003", promotion_rel, "T372")),
        (FRONT_DOOR, (promotion_rel, manifest_rel, "T371-A")),
        (TOC, (promotion_rel, manifest_rel, "t371-a")),
        (ROADMAP_TOC, ("T371", promotion_rel, manifest_rel)),
    ):
        text = _read_text(path)
        for phrase in phrases:
            if phrase not in text:
                raise T371PromotionError(f"{_rel(path)}: missing {phrase!r}")

    roadmap = _read_yaml(ROADMAP)
    future = roadmap.get("phases", {}).get("phase_4", {}).get("future_sequence", [])
    by_id = {item.get("id"): item for item in future if isinstance(item, dict)}
    t371 = by_id.get("T371")
    if not isinstance(t371, dict) or t371.get("status") != "complete":
        raise T371PromotionError(f"{_rel(ROADMAP)}: T371 must be complete")
    if t371.get("selected_option") != "T371-A":
        raise T371PromotionError(f"{_rel(ROADMAP)}: T371 selected_option must be T371-A")
    if t371.get("reviewed_gold_manifest") != manifest_rel:
        raise T371PromotionError(f"{_rel(ROADMAP)}: T371 reviewed_gold_manifest is stale")
    t372 = by_id.get("T372")
    if not isinstance(t372, dict) or t372.get("starts_only_if") != "T371_A_parent_only_reviewed_gold_promoted":
        raise T371PromotionError(f"{_rel(ROADMAP)}: T372 starts_only_if is stale")
    if t372.get("output_change_authorized") is not False:
        raise T371PromotionError(f"{_rel(ROADMAP)}: T372 must remain non-output-changing")


def validate_t371_parent_only_reviewed_gold_promotion(path: Path = PROMOTION) -> dict[str, Any]:
    data = _validate_promotion_record(path)
    _validate_manifest()
    _validate_links()
    return data


def main() -> int:
    try:
        validate_t371_parent_only_reviewed_gold_promotion()
    except T371PromotionError as exc:
        print(f"T371 parent-only reviewed-gold promotion validation failed: {exc}", file=sys.stderr)
        return 1
    print("T371 parent-only reviewed-gold promotion validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
