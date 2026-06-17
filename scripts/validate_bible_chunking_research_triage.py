#!/usr/bin/env python3
"""Validate the Bible-wide chunking research triage map."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
TRIAGE_MAP = ROOT / ".ai" / "control" / "bible_chunking_research_triage_map.yaml"

ALLOWED_STATUSES = {
    "review_packet_ready",
    "research_first",
    "governed_hold",
    "implementation_blocked",
}

REQUIRED_LANES = {
    "psalms_poetry",
    "revelation_apocalyptic",
    "epistle_argument",
    "narrative_pericope",
    "legal_covenant",
    "wisdom_dialogue",
    "prophetic_oracle",
    "gospel_discourse_wj",
    "textual_variant_source_tradition",
    "divine_name_title_capitalization",
    "bible_wide_orchestration",
}

REQUIRED_TOP_LEVEL = {
    "object_type",
    "trust_zone",
    "lifecycle_status",
    "provenance_note",
    "reason_for_inclusion",
    "schema_version",
    "map_id",
    "owner",
    "authority",
    "triage_rule",
    "allowed_triage_statuses",
    "global_non_authorizations",
    "evidence_rules",
    "lanes",
    "recommended_sequence_after_triage",
}

REQUIRED_LANE_FIELDS = {
    "lane_id",
    "canonical_scope",
    "triage_status",
    "current_evidence",
    "why_not_chunk_now",
    "review_packet_candidates",
    "research_questions",
    "downstream_theological_risks",
    "next_action",
    "output_change_authorized",
    "implementation_authorized",
    "reviewed_gold_promoted",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "raw_or_canonical_mutation",
    "generated_chunk_regeneration",
    "chunk_output_change",
    "reviewed_gold_promotion",
    "graph_edge_generation",
    "embedding_or_vector_work",
    "boundary_import",
    "t345_revelation_implementation",
}


class TriageMapError(ValueError):
    """Raised when the Bible-wide research triage map is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
        if text.startswith("---\n"):
            parts = text.split("---\n", 2)
            if len(parts) == 3:
                text = parts[1] + "\n" + parts[2]
        data = yaml.safe_load(text)
    except (OSError, yaml.YAMLError) as exc:
        raise TriageMapError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise TriageMapError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_string(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise TriageMapError(f"{label} must be a non-empty string")


def _require_string_list(value: Any, label: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not value and not allow_empty):
        raise TriageMapError(f"{label} must be a {'possibly empty ' if allow_empty else ''}list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise TriageMapError(f"{label} must contain only non-empty strings")
    return value


def validate_triage_map(path: Path = TRIAGE_MAP) -> dict[str, Any]:
    data = _read_yaml(path)
    missing = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing:
        raise TriageMapError(f"{_rel(path)}: missing top-level keys {missing}")

    if data["object_type"] != "bible_chunking_research_triage_map":
        raise TriageMapError(f"{_rel(path)}: object_type must be bible_chunking_research_triage_map")
    if data["trust_zone"] != "canonical":
        raise TriageMapError(f"{_rel(path)}: trust_zone must be canonical")
    if data["lifecycle_status"] != "active":
        raise TriageMapError(f"{_rel(path)}: lifecycle_status must be active")

    authority = data["authority"]
    if not isinstance(authority, dict):
        raise TriageMapError(f"{_rel(path)}: authority must be a mapping")
    if authority.get("records_research_triage") is not True:
        raise TriageMapError(f"{_rel(path)}: authority.records_research_triage must be true")
    for forbidden in (
        "authorizes_chunk_output_change",
        "authorizes_new_algorithm_work",
        "authorizes_reviewed_gold_promotion",
        "authorizes_revelation_implementation",
        "authorizes_graph_or_vector_work",
        "authorizes_boundary_import",
    ):
        if authority.get(forbidden) is not False:
            raise TriageMapError(f"{_rel(path)}: authority.{forbidden} must be false")

    if set(data["allowed_triage_statuses"]) != ALLOWED_STATUSES:
        raise TriageMapError(f"{_rel(path)}: allowed_triage_statuses must match {sorted(ALLOWED_STATUSES)}")
    non_authorizations = set(_require_string_list(data["global_non_authorizations"], "global_non_authorizations"))
    missing_non_authorizations = sorted(REQUIRED_NON_AUTHORIZATIONS - non_authorizations)
    if missing_non_authorizations:
        raise TriageMapError(f"{_rel(path)}: global_non_authorizations missing {missing_non_authorizations}")

    evidence_rules = data["evidence_rules"]
    if not isinstance(evidence_rules, dict):
        raise TriageMapError(f"{_rel(path)}: evidence_rules must be a mapping")
    for required_rule in (
        "source_metadata",
        "cross_references",
        "original_language",
        "speaker_markers",
        "divine_name_capitalization",
    ):
        _require_string(evidence_rules.get(required_rule), f"evidence_rules.{required_rule}")
        if "authority" not in evidence_rules[required_rule].lower():
            raise TriageMapError(f"evidence_rules.{required_rule} must explicitly limit authority")
    divine_rule = evidence_rules["divine_name_capitalization"].lower()
    for term in ("god/god", "spirit/spirit", "father/father", "word/word"):
        if term not in divine_rule:
            raise TriageMapError(f"evidence_rules.divine_name_capitalization missing {term}")
    for required_word in ("graph", "trinitarian", "chunk"):
        if required_word not in divine_rule:
            raise TriageMapError(
                "evidence_rules.divine_name_capitalization must block graph, Trinitarian, and chunk authority"
            )

    lanes = data["lanes"]
    if not isinstance(lanes, list) or not lanes:
        raise TriageMapError(f"{_rel(path)}: lanes must be a non-empty list")
    by_lane: dict[str, dict[str, Any]] = {}
    for lane in lanes:
        if not isinstance(lane, dict):
            raise TriageMapError(f"{_rel(path)}: each lane must be a mapping")
        missing_lane = sorted(REQUIRED_LANE_FIELDS - set(lane))
        lane_id = str(lane.get("lane_id", "<missing>"))
        if missing_lane:
            raise TriageMapError(f"{_rel(path)}:{lane_id}: missing keys {missing_lane}")
        if lane_id in by_lane:
            raise TriageMapError(f"{_rel(path)}:{lane_id}: duplicate lane_id")
        by_lane[lane_id] = lane
        _require_string(lane["canonical_scope"], f"lanes.{lane_id}.canonical_scope")
        _require_string(lane["current_evidence"], f"lanes.{lane_id}.current_evidence")
        _require_string(lane["why_not_chunk_now"], f"lanes.{lane_id}.why_not_chunk_now")
        _require_string(lane["next_action"], f"lanes.{lane_id}.next_action")
        _require_string_list(lane["review_packet_candidates"], f"lanes.{lane_id}.review_packet_candidates", allow_empty=True)
        _require_string_list(lane["research_questions"], f"lanes.{lane_id}.research_questions")
        _require_string_list(lane["downstream_theological_risks"], f"lanes.{lane_id}.downstream_theological_risks")
        if lane["triage_status"] not in ALLOWED_STATUSES:
            raise TriageMapError(f"{_rel(path)}:{lane_id}: invalid triage_status {lane['triage_status']!r}")
        for flag in ("output_change_authorized", "implementation_authorized", "reviewed_gold_promoted"):
            if lane.get(flag) is not False:
                raise TriageMapError(f"{_rel(path)}:{lane_id}: {flag} must be false")

    missing_lanes = sorted(REQUIRED_LANES - set(by_lane))
    if missing_lanes:
        raise TriageMapError(f"{_rel(path)}: missing required lanes {missing_lanes}")
    if by_lane["revelation_apocalyptic"]["triage_status"] != "research_first":
        raise TriageMapError("revelation_apocalyptic must remain research_first")
    if by_lane["epistle_argument"]["triage_status"] != "review_packet_ready":
        raise TriageMapError("epistle_argument must remain review_packet_ready unless the owner changes the route")
    if by_lane["divine_name_title_capitalization"]["triage_status"] != "research_first":
        raise TriageMapError("divine_name_title_capitalization must remain research_first")
    if by_lane["bible_wide_orchestration"]["triage_status"] != "implementation_blocked":
        raise TriageMapError("bible_wide_orchestration must remain implementation_blocked")

    sequence = data["recommended_sequence_after_triage"]
    if not isinstance(sequence, dict):
        raise TriageMapError(f"{_rel(path)}: recommended_sequence_after_triage must be a mapping")
    _require_string(sequence.get("immediate_next"), "recommended_sequence_after_triage.immediate_next")
    _require_string_list(
        sequence.get("blocked_until_later_owner_decision"),
        "recommended_sequence_after_triage.blocked_until_later_owner_decision",
    )
    if "review_packet_ready" not in sequence["immediate_next"]:
        raise TriageMapError("recommended_sequence_after_triage.immediate_next must route through review_packet_ready")

    return data


def main() -> int:
    try:
        validate_triage_map()
    except TriageMapError as exc:
        print(f"Bible chunking research triage validation failed: {exc}", file=sys.stderr)
        return 1
    print("Bible chunking research triage validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
