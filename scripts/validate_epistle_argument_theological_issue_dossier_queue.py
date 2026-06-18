#!/usr/bin/env python3
"""Validate the epistle argument theological issue dossier queue."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / ".ai" / "control" / "epistle_argument_theological_issue_dossier_queue.yaml"
PACKET_INDEX = ROOT / "eval" / "chunking_gold" / "review_packets" / "review_packet_index.json"

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
    "existing_packet_state",
    "interpretive_preservation_policy",
    "evidence_channels",
    "required_future_dossier_fields",
    "dossier_queue",
    "global_non_authorizations",
    "validators",
}

REQUIRED_FALSE_AUTHORITY = {
    "authorizes_scripture_truth",
    "authorizes_doctrinal_system",
    "authorizes_argument_boundaries",
    "authorizes_chunk_boundaries",
    "authorizes_reviewed_gold",
    "authorizes_output_change",
    "authorizes_route_behavior",
    "authorizes_evaluator_change",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_embedding_or_vector_work",
    "authorizes_source_metadata_truth",
    "authorizes_boundary_import",
    "authorizes_new_algorithm_work",
}

REQUIRED_PRESERVED_OPTIONS = {
    "reformed_or_augustinian_election_readings",
    "arminian_or_wesleyan_election_readings",
    "corporate_election_readings",
    "individual_election_readings",
    "covenant_continuity_readings",
    "covenant_discontinuity_readings",
    "classic_law_gospel_readings",
    "new_perspective_sensitive_readings",
    "perseverance_of_saints_readings",
    "apostasy_warning_readings",
    "high_sacramental_readings",
    "memorial_or_conscience_readings",
    "faith_works_harmony_readings",
    "justification_distinction_readings",
    "union_with_christ_readings",
}

REQUIRED_EVIDENCE_CHANNELS = {
    "argument_connector_flow",
    "quotation_or_catena_structure",
    "paragraph_or_section_metadata",
    "original_language_sentence_or_clause_metadata",
    "editorial_cross_reference_metadata",
    "lexical_or_strongs_metadata",
    "discourse_participant_or_pronoun_reference",
    "sacramental_or_ecclesial_language",
}

REQUIRED_DOSSIERS = {
    "EPH1_BLESSING_ELECTION_SEALING",
    "ROM9_11_ISRAEL_ELECTION_MERCY",
    "HEB7_10_PRIESTHOOD_COVENANT_SACRIFICE",
    "1COR8_10_CONSCIENCE_IDOL_FOOD_TABLE",
    "GAL3_4_LAW_PROMISE_SEED_SONS",
    "ROM7_8_FLESH_SPIRIT_ASSURANCE",
    "JAMES2_FAITH_WORKS_JUSTIFICATION",
    "1PET3_SPIRITS_BAPTISM_SALVATION",
    "1JOHN1_2_ASSURANCE_CONFESSION",
    "JUDE_NONCANONICAL_REFERENCES_JUDGMENT",
}

REQUIRED_T352_PACKETS = {
    "packet_eph1_3_14_argument_review": {
        "case_id": "eph1_3_14_greek_sentence",
        "passage": "Eph.1.3-Eph.1.14",
    },
    "packet_rom9_11_argument_review": {
        "case_id": "rom9_11_argument",
        "passage": "Rom.9-Rom.11",
    },
    "packet_heb7_10_priesthood_argument_review": {
        "case_id": "heb7_10_priesthood_argument",
        "passage": "Heb.7-Heb.10",
    },
    "packet_1cor8_10_food_offered_to_idols_review": {
        "case_id": "1cor8_10_food_offered_to_idols",
        "passage": "1Cor.8-1Cor.10",
    },
}

REQUIRED_DOSSIER_FIELDS = {
    "dossier_id",
    "title",
    "status",
    "priority",
    "exact_passage_scope",
    "existing_review_packet_dependency",
    "source_metadata_observed",
    "evidence_channels",
    "argument_boundary_questions",
    "orthodox_options_preserved",
    "theological_downstream_risks",
    "assumptions_avoided",
    "reviewed_gold_dependency",
    "non_authorizations",
    "validator_or_test_plan",
    "non_target_identity_plan",
}

REQUIRED_GLOBAL_NON_AUTHORIZATIONS = {
    "epistle_dossier_as_reviewed_gold",
    "pending_packet_as_approval",
    "argument_outline_as_doctrine",
    "argument_boundary_as_chunk_boundary",
    "theological_label_as_retrieval_truth",
    "editorial_crossref_as_graph_edge",
    "lexical_metadata_as_doctrine",
    "capitalization_as_divine_identity",
    "source_metadata_as_authority",
    "confessional_system_selection",
    "soteriology_system_selection",
    "covenant_system_selection",
    "sacramental_system_selection",
    "perseverance_system_selection",
    "epistle_implementation",
    "route_behavior_change",
    "evaluator_change",
    "reviewed_gold_promotion",
    "chunk_output_change",
    "graph_edge_generation",
    "retrieval_truth",
    "boundary_import",
    "t345",
}

REQUIRED_VALIDATORS = {
    "scripts/validate_epistle_argument_theological_issue_dossier_queue.py",
    "tests/test_epistle_argument_theological_issue_dossier_queue.py",
    "scripts/validate_epistle_argument_review_packets.py",
    "scripts/validate_bible_wide_chunking_research_registry.py",
    "scripts/validate_chunking_agent_preflight.py",
    "scripts/validate_bible_chunking_readiness_map.py",
    "scripts/validate_chunking_theological_decision_register.py",
    "scripts/validate_all.py",
}

ALLOWED_STATUSES = {"existing_packet_pending", "research_packet_pending", "research_only", "owner_review_pending"}


class EpistleIssueQueueError(ValueError):
    """Raised when the epistle issue dossier queue is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise EpistleIssueQueueError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise EpistleIssueQueueError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EpistleIssueQueueError(f"{_rel(path)}: JSON unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise EpistleIssueQueueError(f"{_rel(path)}: expected a JSON object")
    return data


def _require_string(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise EpistleIssueQueueError(f"{label} must be a non-empty string")


def _require_string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise EpistleIssueQueueError(f"{label} must be a non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise EpistleIssueQueueError(f"{label} must contain only non-empty strings")
    return value


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    if not isinstance(actual, list):
        raise EpistleIssueQueueError(f"{label} must be a list")
    missing = sorted(required - {str(item) for item in actual})
    if missing:
        raise EpistleIssueQueueError(f"{label} missing {missing}")


def _require_evidence_only(text: str, label: str) -> None:
    lowered = text.lower()
    if "evidence only" not in lowered:
        raise EpistleIssueQueueError(f"{label} must say evidence only")
    if "authorize" not in lowered and "authority" not in lowered:
        raise EpistleIssueQueueError(f"{label} must explicitly deny authority")


def _index_entries_by_id() -> dict[str, dict[str, Any]]:
    index = _read_json(PACKET_INDEX)
    entries = index.get("entries")
    if not isinstance(entries, list) or not all(isinstance(entry, dict) for entry in entries):
        raise EpistleIssueQueueError(f"{_rel(PACKET_INDEX)}: entries must be a list of objects")
    return {str(entry.get("entry_id")): entry for entry in entries}


def _validate_existing_packet_state(packet_state: dict[str, Any]) -> None:
    if packet_state.get("t352_packet_count") != 4:
        raise EpistleIssueQueueError("existing_packet_state.t352_packet_count must be 4")
    for key in ("reviewed_gold_promoted", "output_change_authorized", "implementation_allowed"):
        if packet_state.get(key) is not False:
            raise EpistleIssueQueueError(f"existing_packet_state.{key} must be false")
    if packet_state.get("packet_status_required") != "pending_human_review":
        raise EpistleIssueQueueError("existing_packet_state.packet_status_required must be pending_human_review")
    if packet_state.get("packet_index") != "eval/chunking_gold/review_packets/review_packet_index.json":
        raise EpistleIssueQueueError("existing_packet_state.packet_index path is wrong")

    packets = packet_state.get("packets")
    if not isinstance(packets, list) or len(packets) != 4:
        raise EpistleIssueQueueError("existing_packet_state.packets must contain four packets")
    packet_ids = {str(packet.get("entry_id")) for packet in packets if isinstance(packet, dict)}
    missing_packets = sorted(set(REQUIRED_T352_PACKETS) - packet_ids)
    if missing_packets:
        raise EpistleIssueQueueError(f"existing_packet_state missing packets {missing_packets}")

    index_by_id = _index_entries_by_id()
    for entry_id, expected in REQUIRED_T352_PACKETS.items():
        entry = index_by_id.get(entry_id)
        if entry is None:
            raise EpistleIssueQueueError(f"{_rel(PACKET_INDEX)} missing {entry_id}")
        if entry.get("entry_type") != "review_packet":
            raise EpistleIssueQueueError(f"{entry_id}.entry_type must be review_packet")
        if entry.get("case_id") != expected["case_id"]:
            raise EpistleIssueQueueError(f"{entry_id}.case_id must be {expected['case_id']}")
        if entry.get("passage") != expected["passage"]:
            raise EpistleIssueQueueError(f"{entry_id}.passage must be {expected['passage']}")
        if entry.get("status") != "pending_human_review":
            raise EpistleIssueQueueError(f"{entry_id}.status must be pending_human_review")
        if entry.get("decision") != "pending":
            raise EpistleIssueQueueError(f"{entry_id}.decision must be pending")
        for key in ("output_change_authorized", "implementation_allowed"):
            if entry.get(key) is not False:
                raise EpistleIssueQueueError(f"{entry_id}.{key} must be false")


def validate_epistle_argument_theological_issue_dossier_queue(path: Path = QUEUE) -> dict[str, Any]:
    data = _read_yaml(path)
    missing_top = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing_top:
        raise EpistleIssueQueueError(f"{_rel(path)}: missing top-level keys {missing_top}")

    if data["object_type"] != "epistle_argument_theological_issue_dossier_queue":
        raise EpistleIssueQueueError(f"{_rel(path)}: object_type must be epistle_argument_theological_issue_dossier_queue")
    if data["trust_zone"] != "canonical":
        raise EpistleIssueQueueError(f"{_rel(path)}: trust_zone must be canonical")
    if data["lifecycle_status"] != "active":
        raise EpistleIssueQueueError(f"{_rel(path)}: lifecycle_status must be active")
    if data["schema_version"] != "epistle_argument_theological_issue_dossier_queue.v1":
        raise EpistleIssueQueueError(f"{_rel(path)}: schema_version must be epistle_argument_theological_issue_dossier_queue.v1")

    authority = data["authority"]
    if not isinstance(authority, dict):
        raise EpistleIssueQueueError(f"{_rel(path)}: authority must be a mapping")
    for key in (
        "records_epistle_argument_dossier_queue",
        "records_theological_downstream_risks",
        "may_surface_for_review",
        "requires_owner_review_before_output",
    ):
        if authority.get(key) is not True:
            raise EpistleIssueQueueError(f"{_rel(path)}: authority.{key} must be true")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise EpistleIssueQueueError(f"{_rel(path)}: authority.{key} must be false")

    scope = data["scope"]
    if not isinstance(scope, dict):
        raise EpistleIssueQueueError(f"{_rel(path)}: scope must be a mapping")
    expected_scope = {
        "corpus_scope": "canonical_66",
        "testament_scope": "NT",
        "lane": "epistle_argument",
        "research_mode": "non_output_changing",
    }
    for key, expected in expected_scope.items():
        if scope.get(key) != expected:
            raise EpistleIssueQueueError(f"{_rel(path)}: scope.{key} must be {expected}")
    for key, phrases in {
        "relation_to_t352": ("T352", "pending", "reviewed gold"),
        "relation_to_t358": ("discourse_argument_flow", "Bible-wide"),
        "relation_to_t359": ("evidence only", "metadata", "authority"),
        "relation_to_t360": ("Parallel", "must not import", "Revelation"),
    }.items():
        text = str(scope.get(key, ""))
        for phrase in phrases:
            if phrase not in text:
                raise EpistleIssueQueueError(f"{_rel(path)}: scope.{key} missing {phrase!r}")

    packet_state = data["existing_packet_state"]
    if not isinstance(packet_state, dict):
        raise EpistleIssueQueueError(f"{_rel(path)}: existing_packet_state must be a mapping")
    _validate_existing_packet_state(packet_state)

    policy = data["interpretive_preservation_policy"]
    if not isinstance(policy, dict):
        raise EpistleIssueQueueError(f"{_rel(path)}: interpretive_preservation_policy must be a mapping")
    _require_subset(REQUIRED_PRESERVED_OPTIONS, policy.get("preserved_orthodox_options"), "preserved_orthodox_options")
    _require_string_list(policy.get("not_selected_by_queue"), "not_selected_by_queue")
    boundary = str(policy.get("orthodox_boundary", ""))
    for phrase in ("Nicene/Chalcedonian", "refusing", "confessional system"):
        if phrase not in boundary:
            raise EpistleIssueQueueError(f"{_rel(path)}: orthodox_boundary missing {phrase!r}")

    channels = data["evidence_channels"]
    if not isinstance(channels, list) or not channels:
        raise EpistleIssueQueueError(f"{_rel(path)}: evidence_channels must be a non-empty list")
    channel_ids: set[str] = set()
    for channel in channels:
        if not isinstance(channel, dict):
            raise EpistleIssueQueueError(f"{_rel(path)}: each evidence channel must be a mapping")
        channel_id = str(channel.get("channel_id", ""))
        _require_string(channel_id, "evidence_channels.channel_id")
        channel_ids.add(channel_id)
        _require_string(channel.get("use_when"), f"{channel_id}.use_when")
        _require_string(channel.get("non_authorization"), f"{channel_id}.non_authorization")
        _require_evidence_only(channel["non_authorization"], f"{channel_id}.non_authorization")
    missing_channels = sorted(REQUIRED_EVIDENCE_CHANNELS - channel_ids)
    if missing_channels:
        raise EpistleIssueQueueError(f"{_rel(path)}: missing evidence channels {missing_channels}")

    _require_subset(REQUIRED_DOSSIER_FIELDS, data["required_future_dossier_fields"], "required_future_dossier_fields")
    _require_subset(REQUIRED_GLOBAL_NON_AUTHORIZATIONS, data["global_non_authorizations"], "global_non_authorizations")
    _require_subset(REQUIRED_VALIDATORS, data["validators"], "validators")

    dossiers = data["dossier_queue"]
    if not isinstance(dossiers, list) or not dossiers:
        raise EpistleIssueQueueError(f"{_rel(path)}: dossier_queue must be a non-empty list")
    dossier_ids: set[str] = set()
    priorities: list[int] = []
    for dossier in dossiers:
        if not isinstance(dossier, dict):
            raise EpistleIssueQueueError(f"{_rel(path)}: each dossier must be a mapping")
        dossier_id = str(dossier.get("dossier_id", ""))
        _require_string(dossier_id, "dossier_queue.dossier_id")
        if dossier_id in dossier_ids:
            raise EpistleIssueQueueError(f"{_rel(path)}: duplicate dossier_id {dossier_id}")
        dossier_ids.add(dossier_id)
        missing_fields = sorted(REQUIRED_DOSSIER_FIELDS - set(dossier))
        if missing_fields:
            raise EpistleIssueQueueError(f"{dossier_id} missing fields {missing_fields}")
        if dossier.get("status") not in ALLOWED_STATUSES:
            raise EpistleIssueQueueError(f"{dossier_id}.status is invalid")
        priority = dossier.get("priority")
        if not isinstance(priority, int):
            raise EpistleIssueQueueError(f"{dossier_id}.priority must be an integer")
        priorities.append(priority)
        _require_string(dossier.get("title"), f"{dossier_id}.title")
        _require_string_list(dossier.get("exact_passage_scope"), f"{dossier_id}.exact_passage_scope")
        source_metadata = dossier.get("source_metadata_observed")
        if not isinstance(source_metadata, dict):
            raise EpistleIssueQueueError(f"{dossier_id}.source_metadata_observed must be a mapping")
        dossier_channels = set(_require_string_list(dossier.get("evidence_channels"), f"{dossier_id}.evidence_channels"))
        unknown_channels = sorted(dossier_channels - channel_ids)
        if unknown_channels:
            raise EpistleIssueQueueError(f"{dossier_id}.evidence_channels unknown {unknown_channels}")
        _require_string_list(dossier.get("argument_boundary_questions"), f"{dossier_id}.argument_boundary_questions")
        options = set(_require_string_list(dossier.get("orthodox_options_preserved"), f"{dossier_id}.orthodox_options_preserved"))
        unknown_options = sorted(options - set(policy["preserved_orthodox_options"]))
        if unknown_options:
            raise EpistleIssueQueueError(f"{dossier_id}.orthodox_options_preserved unknown {unknown_options}")
        _require_string_list(dossier.get("theological_downstream_risks"), f"{dossier_id}.theological_downstream_risks")
        _require_string_list(dossier.get("assumptions_avoided"), f"{dossier_id}.assumptions_avoided")
        _require_string(dossier.get("reviewed_gold_dependency"), f"{dossier_id}.reviewed_gold_dependency")
        for phrase in ("human review", "owner", "reviewed gold", "route", "graph", "retrieval", "non-target"):
            if phrase not in dossier["reviewed_gold_dependency"].lower():
                raise EpistleIssueQueueError(f"{dossier_id}.reviewed_gold_dependency missing {phrase!r}")
        non_authorizations = set(_require_string_list(dossier.get("non_authorizations"), f"{dossier_id}.non_authorizations"))
        for required in ("argument_boundary", "doctrine_label", "reviewed_gold", "chunk_boundary", "route_behavior", "graph_edge", "retrieval_truth", "output_change"):
            if required not in non_authorizations:
                raise EpistleIssueQueueError(f"{dossier_id}.non_authorizations missing {required}")
        if dossier.get("status") == "existing_packet_pending":
            dependency = dossier.get("existing_review_packet_dependency")
            if dependency not in REQUIRED_T352_PACKETS:
                raise EpistleIssueQueueError(f"{dossier_id}.existing_review_packet_dependency must point to a T352 packet")
        _require_string(dossier.get("validator_or_test_plan"), f"{dossier_id}.validator_or_test_plan")
        _require_string(dossier.get("non_target_identity_plan"), f"{dossier_id}.non_target_identity_plan")
        if "unchanged identity" not in str(dossier["non_target_identity_plan"]):
            raise EpistleIssueQueueError(f"{dossier_id}.non_target_identity_plan must require unchanged identity")
    missing_dossiers = sorted(REQUIRED_DOSSIERS - dossier_ids)
    if missing_dossiers:
        raise EpistleIssueQueueError(f"{_rel(path)}: missing dossiers {missing_dossiers}")
    if priorities != sorted(priorities):
        raise EpistleIssueQueueError(f"{_rel(path)}: dossier priorities must be sorted")

    return data


def main() -> int:
    try:
        validate_epistle_argument_theological_issue_dossier_queue()
    except EpistleIssueQueueError as exc:
        print(f"Epistle argument theological issue dossier queue validation failed: {exc}", file=sys.stderr)
        return 1
    print("Epistle argument theological issue dossier queue validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
