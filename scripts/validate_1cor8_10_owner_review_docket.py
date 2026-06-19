#!/usr/bin/env python3
"""Validate the 1 Corinthians 8-10 owner-review docket."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCKET = ROOT / ".ai" / "control" / "1cor8_10_epistle_owner_review_docket.yaml"
PACKET = ROOT / "eval" / "chunking_gold" / "review_packets" / "1cor8_10_food_offered_to_idols_review.md"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
READINESS_MAP = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"

REQUIRED_OPTIONS = {
    "1COR8-10-T369-A",
    "1COR8-10-T369-B",
    "1COR8-10-T369-C",
    "1COR8-10-T369-D",
    "1COR8-10-T369-E",
}

REQUIRED_FALSE_AUTHORITY = {
    "authorizes_parent_span_as_reviewed_gold",
    "authorizes_child_spans_as_reviewed_gold",
    "authorizes_argument_boundary",
    "authorizes_doctrinal_system",
    "authorizes_sacramental_system",
    "authorizes_ecclesial_system",
    "authorizes_textual_critical_decision",
    "authorizes_reviewed_gold",
    "authorizes_chunk_boundaries",
    "authorizes_route_behavior",
    "authorizes_evaluator_change",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_output_change",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "1cor8_10_parent_span_as_reviewed_gold",
    "1cor8_10_parent_span_as_chunk_boundary",
    "1cor8_10_child_span_approval",
    "argument_boundary_as_chunk_boundary",
    "conscience_label_as_doctrine",
    "weak_strong_label_as_theological_system",
    "christian_liberty_as_system",
    "table_language_as_sacramental_system",
    "ecclesial_boundary_as_chunk_authority",
    "cross_reference_as_graph_edge",
    "lexical_metadata_as_doctrine",
    "textual_variant_as_policy_decision",
    "route_behavior_change",
    "evaluator_change",
    "reviewed_gold_promotion",
    "graph_edge_generation",
    "retrieval_truth",
    "chunk_output_change",
}


class OneCorDocketError(ValueError):
    """Raised when the 1Cor.8-10 owner-review docket is stale or authorizing."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise OneCorDocketError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise OneCorDocketError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise OneCorDocketError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    if not isinstance(actual, list):
        raise OneCorDocketError(f"{label} must be a list")
    missing = sorted(required - {str(item) for item in actual})
    if missing:
        raise OneCorDocketError(f"{label} missing {missing}")


def _validate_docket(data: dict[str, Any], path: Path) -> None:
    if data.get("object_type") != "epistle_argument_owner_review_docket":
        raise OneCorDocketError(f"{_rel(path)}: object_type must be epistle_argument_owner_review_docket")
    if data.get("trust_zone") != "canonical":
        raise OneCorDocketError(f"{_rel(path)}: trust_zone must be canonical")
    if data.get("lifecycle_status") != "active":
        raise OneCorDocketError(f"{_rel(path)}: lifecycle_status must be active")
    if data.get("schema_version") != "epistle_argument_owner_review_docket.v1":
        raise OneCorDocketError(f"{_rel(path)}: schema_version must be epistle_argument_owner_review_docket.v1")

    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise OneCorDocketError(f"{_rel(path)}: authority must be a mapping")
    if authority.get("records_owner_review_options") is not True:
        raise OneCorDocketError(f"{_rel(path)}: authority.records_owner_review_options must be true")
    if authority.get("records_owner_review_selection") is not True:
        raise OneCorDocketError(f"{_rel(path)}: authority.records_owner_review_selection must be true")
    if authority.get("may_surface_for_review") is not True:
        raise OneCorDocketError(f"{_rel(path)}: authority.may_surface_for_review must be true")
    if authority.get("authorizes_parent_only_review_target") is not True:
        raise OneCorDocketError(f"{_rel(path)}: authority.authorizes_parent_only_review_target must be true")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise OneCorDocketError(f"{_rel(path)}: authority.{key} must be false")

    target = data.get("target")
    if not isinstance(target, dict):
        raise OneCorDocketError(f"{_rel(path)}: target must be a mapping")
    expected_target = {
        "target_id": "1cor8_10_food_offered_to_idols",
        "passage": "1Cor.8-1Cor.10",
        "exact_parent_candidate": "1Cor.8.1-1Cor.10.33",
        "review_packet": "eval/chunking_gold/review_packets/1cor8_10_food_offered_to_idols_review.md",
        "prior_packet_task": "T352",
        "prior_issue_dossier_task": "T361",
        "prior_owner_decision_task": "T367",
        "strengthening_task": "T368",
        "status": "parent_only_review_target_selected",
    }
    for key, value in expected_target.items():
        if target.get(key) != value:
            raise OneCorDocketError(f"{_rel(path)}: target.{key} must be {value}")

    selection = data.get("owner_selection")
    if not isinstance(selection, dict):
        raise OneCorDocketError(f"{_rel(path)}: owner_selection must be a mapping")
    if selection.get("owner_selection_status") != "selected":
        raise OneCorDocketError(f"{_rel(path)}: owner_selection.owner_selection_status must be selected")
    if selection.get("selection_mode") != "projected_owner_pattern":
        raise OneCorDocketError(f"{_rel(path)}: owner_selection.selection_mode must be projected_owner_pattern")
    if selection.get("projection_policy") != ".ai/control/owner_decision_projection_policy.yaml":
        raise OneCorDocketError(f"{_rel(path)}: owner_selection.projection_policy is stale")
    if selection.get("projection_id") != "ODP-20260618-1COR8-10-PARENT":
        raise OneCorDocketError(f"{_rel(path)}: owner_selection.projection_id is stale")
    if selection.get("conflict_scan_result") != "no_conflict_detected":
        raise OneCorDocketError(f"{_rel(path)}: owner_selection.conflict_scan_result must be no_conflict_detected")
    if selection.get("selected_option") != "1COR8-10-T369-B":
        raise OneCorDocketError(f"{_rel(path)}: owner_selection.selected_option must be 1COR8-10-T369-B")
    if selection.get("selected_parent") != "1Cor.8.1-1Cor.10.33":
        raise OneCorDocketError(f"{_rel(path)}: owner_selection.selected_parent is wrong")
    if selection.get("selected_children") != []:
        raise OneCorDocketError(f"{_rel(path)}: owner_selection.selected_children must be []")
    for key in ("implementation_allowed", "output_change_authorized", "reviewed_gold_promoted"):
        if selection.get(key) is not False:
            raise OneCorDocketError(f"{_rel(path)}: owner_selection.{key} must be false")

    options = data.get("options")
    if not isinstance(options, list):
        raise OneCorDocketError(f"{_rel(path)}: options must be a list")
    option_ids = {str(item.get("option_id")) for item in options if isinstance(item, dict)}
    missing_options = sorted(REQUIRED_OPTIONS - option_ids)
    if missing_options:
        raise OneCorDocketError(f"{_rel(path)}: missing owner options {missing_options}")
    for option in options:
        if not isinstance(option, dict):
            raise OneCorDocketError(f"{_rel(path)}: every option must be a mapping")
        if option.get("implementation_allowed_now") is not False:
            raise OneCorDocketError(f"{_rel(path)}: {option.get('option_id')}.implementation_allowed_now must be false")

    option_c = next(item for item in options if item.get("option_id") == "1COR8-10-T369-C")
    spans = [item.get("span") for item in option_c.get("child_span_candidates", []) if isinstance(item, dict)]
    for required_span in (
        "1Cor.8.1-1Cor.8.13",
        "1Cor.9.1-1Cor.9.18",
        "1Cor.9.19-1Cor.9.27",
        "1Cor.10.1-1Cor.10.13",
        "1Cor.10.14-1Cor.10.22",
        "1Cor.10.23-1Cor.10.33",
    ):
        if required_span not in spans:
            raise OneCorDocketError(f"{_rel(path)}: option C missing child span {required_span}")

    _require_subset(REQUIRED_NON_AUTHORIZATIONS, data.get("non_authorizations"), "non_authorizations")


def _validate_packet_links() -> None:
    text = _read_text(PACKET)
    for phrase in (
        "T368 strengthened packet: true",
        "Owner-review docket: `.ai/control/1cor8_10_epistle_owner_review_docket.yaml`",
        "T370 parent-only evidence packet: `eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml`",
        "Decision-register anchors: `CD-034`, `CD-035`, `CD-036`, `CD-037`, `CD-042`",
        "No reviewed gold is promoted by the T370 evidence packet.",
        "1Cor.9.20",
        "1Cor.10.9",
        "Deut.25.4",
        "Exod.32.6",
        "Ps.24.1",
        "G1108",
        "G4893",
        "G1494",
        "G1497",
        "G1849",
        "G5132",
        "G4221",
        "G1140",
        "G2842",
        "Only `1COR8-10-T369-B` is selected, by projected owner pattern, as a parent-only review target.",
        "No child span, reviewed gold, route behavior, graph/retrieval truth, textual-critical policy",
    ):
        if phrase not in text:
            raise OneCorDocketError(f"{_rel(PACKET)}: missing strengthened-packet phrase {phrase!r}")
    for forbidden in (
        "Status: `reviewed_gold`",
        "Implementation allowed: true",
        "Output change authorized: true",
        "Reviewed gold promoted: true",
        "approved for implementation",
    ):
        if forbidden in text:
            raise OneCorDocketError(f"{_rel(PACKET)}: contains forbidden phrase {forbidden!r}")


def _validate_governed_links() -> None:
    register_text = _read_text(REGISTER)
    for phrase in (
        "CD-037",
        "CD-041",
        "CD-042",
        "1 Corinthians 8-10 strengthened packet remains non-authorizing",
        "1 Corinthians 8-10 parent-only review target selected by projected owner pattern",
        "1 Corinthians 8-10 parent-only evidence packet remains non-authorizing",
        "T369",
        "T370",
    ):
        if phrase not in register_text:
            raise OneCorDocketError(f"{_rel(REGISTER)}: missing {phrase!r}")

    preflight = _read_yaml(PREFLIGHT)
    reading_paths = {
        str(item.get("path"))
        for item in preflight.get("mandatory_reading", [])
        if isinstance(item, dict)
    }
    if ".ai/control/1cor8_10_epistle_owner_review_docket.yaml" not in reading_paths:
        raise OneCorDocketError(f"{_rel(PREFLIGHT)}: 1Cor.8-10 docket must be mandatory reading")

    readiness = _read_yaml(READINESS_MAP)
    next_route = readiness.get("next_route")
    if not isinstance(next_route, dict):
        raise OneCorDocketError(f"{_rel(READINESS_MAP)}: next_route must be a mapping")
    if next_route.get("task_id") != "T372":
        raise OneCorDocketError(f"{_rel(READINESS_MAP)}: next_route.task_id must be T372 after T371-A")
    if next_route.get("starts_only_if") != "T371_A_parent_only_reviewed_gold_promoted":
        raise OneCorDocketError(
            f"{_rel(READINESS_MAP)}: next_route.starts_only_if must be T371_A_parent_only_reviewed_gold_promoted"
        )
    if (
        next_route.get("evidence_packet")
        != "eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml"
    ):
        raise OneCorDocketError(f"{_rel(READINESS_MAP)}: next_route.evidence_packet is stale")
    if next_route.get("owner_review_docket") != ".ai/control/1cor8_10_epistle_owner_review_docket.yaml":
        raise OneCorDocketError(f"{_rel(READINESS_MAP)}: next_route.owner_review_docket is stale")
    if next_route.get("promotion_record") != ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml":
        raise OneCorDocketError(f"{_rel(READINESS_MAP)}: next_route.promotion_record is stale")
    if next_route.get("reviewed_gold_manifest") != "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json":
        raise OneCorDocketError(f"{_rel(READINESS_MAP)}: next_route.reviewed_gold_manifest is stale")
    if next_route.get("owner_decision_required") is not False:
        raise OneCorDocketError(f"{_rel(READINESS_MAP)}: next_route.owner_decision_required must be false")
    if next_route.get("harness_only") is not True:
        raise OneCorDocketError(f"{_rel(READINESS_MAP)}: next_route.harness_only must be true")
    if next_route.get("reviewed_gold_promoted") is not True:
        raise OneCorDocketError(f"{_rel(READINESS_MAP)}: next_route.reviewed_gold_promoted must be true")
    for key in (
        "output_change_authorized",
        "implementation_authorized",
        "route_behavior_authorized",
        "evaluator_change_authorized",
        "graph_edge_generation_allowed",
        "retrieval_truth_authorized",
    ):
        if next_route.get(key) is not False:
            raise OneCorDocketError(f"{_rel(READINESS_MAP)}: next_route.{key} must be false")


def validate_1cor8_10_owner_review_docket(path: Path = DOCKET) -> dict[str, Any]:
    data = _read_yaml(path)
    _validate_docket(data, path)
    _validate_packet_links()
    _validate_governed_links()
    return data


def main() -> int:
    try:
        validate_1cor8_10_owner_review_docket()
    except OneCorDocketError as exc:
        print(f"1Cor.8-10 owner-review docket validation failed: {exc}", file=sys.stderr)
        return 1
    print("1Cor.8-10 owner-review docket validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
