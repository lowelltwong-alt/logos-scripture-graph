#!/usr/bin/env python3
"""Validate the prophetic/oracle/vision dossier queue."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / ".ai" / "control" / "prophetic_oracle_vision_dossier_queue.yaml"

REQUIRED_TOP_LEVEL = {
    "object_type",
    "trust_zone",
    "lifecycle_status",
    "provenance_note",
    "reason_for_inclusion",
    "schema_version",
    "queue_id",
    "owner",
    "authority",
    "scope",
    "preservation_policy",
    "evidence_channels",
    "required_future_dossier_fields",
    "dossier_queue",
    "global_non_authorizations",
    "validators",
}

REQUIRED_FALSE_AUTHORITY = {
    "authorizes_scripture_truth",
    "authorizes_fulfillment_theology",
    "authorizes_eschatological_system",
    "authorizes_covenant_system",
    "authorizes_israel_church_relation",
    "authorizes_messianic_identification",
    "authorizes_temple_theology",
    "authorizes_chunk_boundaries",
    "authorizes_reviewed_gold",
    "authorizes_output_change",
    "authorizes_route_behavior",
    "authorizes_evaluator_change",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_embedding_or_vector_work",
    "authorizes_source_metadata_truth",
    "authorizes_intertext_truth",
    "authorizes_boundary_import",
    "authorizes_new_algorithm_work",
}

REQUIRED_REVIEW_OPTIONS = {
    "local_oracle_review",
    "parent_oracle_cycle_review",
    "vision_report_review",
    "symbolic_action_review",
    "judgment_hope_pair_review",
    "servant_song_review",
    "temple_vision_review",
    "day_of_yahweh_review",
    "prophetic_book_frame_review",
}

REQUIRED_EVIDENCE_CHANNELS = {
    "oracle_formula",
    "prophetic_speech_frame",
    "vision_report",
    "symbolic_action",
    "judgment_hope_turn",
    "servant_or_messianic_language",
    "temple_zion_land_imagery",
    "day_of_yahweh_review",
    "source_metadata_formatting",
    "canonical_intertext_echo",
}

REQUIRED_DOSSIERS = {
    "ISA40_55_SERVANT_COMFORT_ORACLES",
    "JER30_33_RESTORATION_NEW_COVENANT",
    "EZEK40_48_TEMPLE_CITY_VISION",
    "EZEK36_37_RESTORATION_SPIRIT_DRY_BONES",
    "DAN7_12_PROPHETIC_APOCALYPTIC_VISIONS",
    "HOSEA1_3_SIGN_ACT_COVENANT_METAPHOR",
    "JOEL2_DAY_OF_YAHWEH_SPIRIT",
    "ZECH1_6_NIGHT_VISIONS",
}

REQUIRED_DOSSIER_FIELDS = {
    "dossier_id",
    "title",
    "status",
    "priority",
    "exact_passage_scope",
    "primary_lane",
    "evidence_channels",
    "boundary_questions",
    "review_options_preserved",
    "theological_downstream_risks",
    "assumptions_avoided",
    "reviewed_gold_dependency",
    "non_authorizations",
    "validator_or_test_plan",
    "non_target_identity_plan",
}

REQUIRED_GLOBAL_NON_AUTHORIZATIONS = {
    "prophetic_dossier_as_reviewed_gold",
    "oracle_formula_as_chunk_boundary",
    "vision_report_as_chronology",
    "symbolic_action_as_theology",
    "judgment_hope_turn_as_covenant_system",
    "servant_language_as_messianic_identity",
    "temple_vision_as_temple_theology",
    "day_of_yahweh_as_timeline",
    "canonical_echo_as_graph_edge",
    "source_metadata_as_authority",
    "fulfillment_theology_selection",
    "eschatological_system_selection",
    "covenant_system_selection",
    "israel_church_relation_selection",
    "reviewed_gold_promotion",
    "chunk_output_change",
    "route_behavior_change",
    "evaluator_change",
    "graph_edge_generation",
    "retrieval_truth",
    "boundary_import",
    "t345",
}

REQUIRED_VALIDATORS = {
    "scripts/validate_prophetic_oracle_vision_dossier_queue.py",
    "tests/test_prophetic_oracle_vision_dossier_queue.py",
    "scripts/validate_bible_wide_chunking_research_registry.py",
    "scripts/validate_chunking_agent_preflight.py",
    "scripts/validate_bible_chunking_readiness_map.py",
    "scripts/validate_chunking_theological_decision_register.py",
    "scripts/validate_all.py",
}

ALLOWED_STATUSES = {"research_packet_pending", "research_only", "owner_review_pending"}
ALLOWED_LANES = {"prophetic_oracle", "prophetic_oracle_vision"}


class PropheticOracleVisionQueueError(ValueError):
    """Raised when the prophetic/oracle/vision queue is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise PropheticOracleVisionQueueError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise PropheticOracleVisionQueueError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_string(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise PropheticOracleVisionQueueError(f"{label} must be a non-empty string")


def _require_string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise PropheticOracleVisionQueueError(f"{label} must be a non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise PropheticOracleVisionQueueError(f"{label} must contain only non-empty strings")
    return value


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    if not isinstance(actual, list):
        raise PropheticOracleVisionQueueError(f"{label} must be a list")
    missing = sorted(required - {str(item) for item in actual})
    if missing:
        raise PropheticOracleVisionQueueError(f"{label} missing {missing}")


def _require_evidence_only(text: str, label: str) -> None:
    lowered = text.lower()
    if "evidence only" not in lowered:
        raise PropheticOracleVisionQueueError(f"{label} must say evidence only")
    if "authorize" not in lowered and "authority" not in lowered:
        raise PropheticOracleVisionQueueError(f"{label} must explicitly deny authority")


def validate_prophetic_oracle_vision_dossier_queue(path: Path = QUEUE) -> dict[str, Any]:
    data = _read_yaml(path)
    missing_top = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing_top:
        raise PropheticOracleVisionQueueError(f"{_rel(path)}: missing top-level keys {missing_top}")

    if data["object_type"] != "prophetic_oracle_vision_dossier_queue":
        raise PropheticOracleVisionQueueError(f"{_rel(path)}: object_type must be prophetic_oracle_vision_dossier_queue")
    if data["trust_zone"] != "canonical":
        raise PropheticOracleVisionQueueError(f"{_rel(path)}: trust_zone must be canonical")
    if data["lifecycle_status"] != "active":
        raise PropheticOracleVisionQueueError(f"{_rel(path)}: lifecycle_status must be active")
    if data["schema_version"] != "prophetic_oracle_vision_dossier_queue.v1":
        raise PropheticOracleVisionQueueError(f"{_rel(path)}: schema_version must be prophetic_oracle_vision_dossier_queue.v1")

    authority = data["authority"]
    if not isinstance(authority, dict):
        raise PropheticOracleVisionQueueError(f"{_rel(path)}: authority must be a mapping")
    for key in ("records_prophetic_oracle_vision_dossier_queue", "records_prophetic_boundary_risks", "may_surface_for_review", "requires_owner_review_before_output"):
        if authority.get(key) is not True:
            raise PropheticOracleVisionQueueError(f"{_rel(path)}: authority.{key} must be true")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise PropheticOracleVisionQueueError(f"{_rel(path)}: authority.{key} must be false")

    scope = data["scope"]
    if not isinstance(scope, dict):
        raise PropheticOracleVisionQueueError(f"{_rel(path)}: scope must be a mapping")
    if scope.get("corpus_scope") != "canonical_66":
        raise PropheticOracleVisionQueueError(f"{_rel(path)}: scope.corpus_scope must be canonical_66")
    if scope.get("research_mode") != "non_output_changing":
        raise PropheticOracleVisionQueueError(f"{_rel(path)}: scope.research_mode must be non_output_changing")
    _require_subset(ALLOWED_LANES, scope.get("lanes"), "scope.lanes")

    policy = data["preservation_policy"]
    if not isinstance(policy, dict):
        raise PropheticOracleVisionQueueError(f"{_rel(path)}: preservation_policy must be a mapping")
    _require_subset(REQUIRED_REVIEW_OPTIONS, policy.get("preserved_review_options"), "preserved_review_options")
    _require_string_list(policy.get("not_selected_by_queue"), "not_selected_by_queue")
    boundary = str(policy.get("orthodox_boundary", ""))
    for phrase in ("Nicene/Chalcedonian", "refusing", "fulfillment", "temple"):
        if phrase not in boundary:
            raise PropheticOracleVisionQueueError(f"{_rel(path)}: orthodox_boundary missing {phrase!r}")

    channels = data["evidence_channels"]
    if not isinstance(channels, list) or not channels:
        raise PropheticOracleVisionQueueError(f"{_rel(path)}: evidence_channels must be a non-empty list")
    channel_ids: set[str] = set()
    for channel in channels:
        if not isinstance(channel, dict):
            raise PropheticOracleVisionQueueError(f"{_rel(path)}: each evidence channel must be a mapping")
        channel_id = str(channel.get("channel_id", ""))
        _require_string(channel_id, "evidence_channels.channel_id")
        channel_ids.add(channel_id)
        _require_string(channel.get("use_when"), f"{channel_id}.use_when")
        _require_string(channel.get("non_authorization"), f"{channel_id}.non_authorization")
        _require_evidence_only(channel["non_authorization"], f"{channel_id}.non_authorization")
    missing_channels = sorted(REQUIRED_EVIDENCE_CHANNELS - channel_ids)
    if missing_channels:
        raise PropheticOracleVisionQueueError(f"{_rel(path)}: missing evidence channels {missing_channels}")

    _require_subset(REQUIRED_DOSSIER_FIELDS, data["required_future_dossier_fields"], "required_future_dossier_fields")
    _require_subset(REQUIRED_GLOBAL_NON_AUTHORIZATIONS, data["global_non_authorizations"], "global_non_authorizations")
    _require_subset(REQUIRED_VALIDATORS, data["validators"], "validators")

    dossiers = data["dossier_queue"]
    if not isinstance(dossiers, list) or not dossiers:
        raise PropheticOracleVisionQueueError(f"{_rel(path)}: dossier_queue must be a non-empty list")
    dossier_ids: set[str] = set()
    priorities: list[int] = []
    for dossier in dossiers:
        if not isinstance(dossier, dict):
            raise PropheticOracleVisionQueueError(f"{_rel(path)}: each dossier must be a mapping")
        dossier_id = str(dossier.get("dossier_id", ""))
        _require_string(dossier_id, "dossier_queue.dossier_id")
        if dossier_id in dossier_ids:
            raise PropheticOracleVisionQueueError(f"{_rel(path)}: duplicate dossier_id {dossier_id}")
        dossier_ids.add(dossier_id)
        missing_fields = sorted(REQUIRED_DOSSIER_FIELDS - set(dossier))
        if missing_fields:
            raise PropheticOracleVisionQueueError(f"{dossier_id} missing fields {missing_fields}")
        if dossier.get("status") not in ALLOWED_STATUSES:
            raise PropheticOracleVisionQueueError(f"{dossier_id}.status is invalid")
        if dossier.get("primary_lane") not in ALLOWED_LANES:
            raise PropheticOracleVisionQueueError(f"{dossier_id}.primary_lane is invalid")
        priority = dossier.get("priority")
        if not isinstance(priority, int):
            raise PropheticOracleVisionQueueError(f"{dossier_id}.priority must be an integer")
        priorities.append(priority)
        _require_string(dossier.get("title"), f"{dossier_id}.title")
        _require_string_list(dossier.get("exact_passage_scope"), f"{dossier_id}.exact_passage_scope")
        dossier_channels = set(_require_string_list(dossier.get("evidence_channels"), f"{dossier_id}.evidence_channels"))
        unknown_channels = sorted(dossier_channels - channel_ids)
        if unknown_channels:
            raise PropheticOracleVisionQueueError(f"{dossier_id}.evidence_channels unknown {unknown_channels}")
        options = set(_require_string_list(dossier.get("review_options_preserved"), f"{dossier_id}.review_options_preserved"))
        unknown_options = sorted(options - set(policy["preserved_review_options"]))
        if unknown_options:
            raise PropheticOracleVisionQueueError(f"{dossier_id}.review_options_preserved unknown {unknown_options}")
        for key in ("boundary_questions", "theological_downstream_risks", "assumptions_avoided"):
            _require_string_list(dossier.get(key), f"{dossier_id}.{key}")
        _require_string(dossier.get("reviewed_gold_dependency"), f"{dossier_id}.reviewed_gold_dependency")
        for phrase in ("owner", "review", "reviewed", "non-target", "graph", "retrieval", "route"):
            if phrase not in dossier["reviewed_gold_dependency"].lower():
                raise PropheticOracleVisionQueueError(f"{dossier_id}.reviewed_gold_dependency missing {phrase!r}")
        non_authorizations = set(_require_string_list(dossier.get("non_authorizations"), f"{dossier_id}.non_authorizations"))
        for required in ("chunk_boundary", "reviewed_gold", "output_change", "route_behavior", "graph_edge", "retrieval_truth"):
            if required not in non_authorizations:
                raise PropheticOracleVisionQueueError(f"{dossier_id}.non_authorizations missing {required}")
        _require_string(dossier.get("validator_or_test_plan"), f"{dossier_id}.validator_or_test_plan")
        _require_string(dossier.get("non_target_identity_plan"), f"{dossier_id}.non_target_identity_plan")
        if "unchanged identity" not in str(dossier["non_target_identity_plan"]):
            raise PropheticOracleVisionQueueError(f"{dossier_id}.non_target_identity_plan must require unchanged identity")

    missing_dossiers = sorted(REQUIRED_DOSSIERS - dossier_ids)
    if missing_dossiers:
        raise PropheticOracleVisionQueueError(f"{_rel(path)}: missing dossiers {missing_dossiers}")
    if priorities != sorted(priorities):
        raise PropheticOracleVisionQueueError(f"{_rel(path)}: dossier priorities must be sorted")

    return data


def main() -> int:
    try:
        validate_prophetic_oracle_vision_dossier_queue()
    except PropheticOracleVisionQueueError as exc:
        print(f"Prophetic/oracle/vision dossier queue validation failed: {exc}", file=sys.stderr)
        return 1
    print("Prophetic/oracle/vision dossier queue validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
