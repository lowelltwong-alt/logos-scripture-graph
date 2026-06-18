#!/usr/bin/env python3
"""Validate the Gospel/WJ discourse dossier queue."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / ".ai" / "control" / "gospel_wj_discourse_dossier_queue.yaml"
WJ_INVENTORY = ROOT / ".ai" / "control" / "wj_marker_inventory.yaml"
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
    "observed_wj_metadata",
    "existing_packet_state",
    "wj_discourse_preservation_policy",
    "evidence_channels",
    "required_future_dossier_fields",
    "dossier_queue",
    "global_non_authorizations",
    "validators",
}

REQUIRED_FALSE_AUTHORITY = {
    "authorizes_scripture_truth",
    "authorizes_jesus_speaker_attribution",
    "authorizes_speaker_boundary",
    "authorizes_discourse_boundary",
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

REQUIRED_REVIEW_OPTIONS = {
    "jesus_speech",
    "narrator_commentary",
    "unresolved_for_chunking",
    "parent_only_discourse_review",
    "parent_with_child_discourse_review",
    "variant_policy_first",
    "revelation_research_first",
    "synoptic_parallel_review",
    "dominical_quotation_review",
}

REQUIRED_EVIDENCE_CHANNELS = {
    "wj_red_letter_metadata",
    "speaker_formula_and_narrative_frame",
    "discourse_connector_and_scene_flow",
    "paragraph_heading_or_formatting_metadata",
    "textual_variant_policy",
    "synoptic_parallel_or_intertext_context",
}

REQUIRED_DOSSIERS = {
    "JOHN3_WJ_SPEAKER_BOUNDARY",
    "MATT5_7_SERMON_ON_MOUNT_WJ_DISCOURSE",
    "JOHN13_17_FAREWELL_DISCOURSE",
    "SYNOPTIC_OLIVET_WJ_APOCALYPTIC_DISCOURSE",
    "JOHN7_53_8_11_VARIANT_WJ_SPEECH",
    "REVELATION_WJ_VOICE_SHIFTS",
    "ACTS_EPISTLE_WJ_DOMINICAL_QUOTES",
}

REQUIRED_PENDING_PACKETS = {
    "packet_john3_wj_speaker_boundary_review": {
        "case_id": "john3_wj_speaker_boundary",
        "passage": "John.3",
    },
    "packet_matt5_7_wj_discourse_review": {
        "case_id": "matt5_7_sermon_on_mount_wj_discourse",
        "passage": "Matt.5-Matt.7",
    },
    "packet_john7_53_8_11_textual_variant_review": {
        "case_id": "john7_53_8_11_pericope_adulterae",
        "passage": "John.7.53-John.8.11",
    },
}

REQUIRED_POLICY_CASES = {
    "observed_john13_17_wj_farewell_discourse_marker_focus": "john13_17_wj_farewell_discourse_marker_focus",
    "observed_synoptic_apocalyptic_wj_discourses": "synoptic_apocalyptic_wj_discourses",
}

REQUIRED_DOSSIER_FIELDS = {
    "dossier_id",
    "title",
    "status",
    "priority",
    "exact_passage_scope",
    "existing_review_dependency",
    "source_metadata_observed",
    "evidence_channels",
    "speaker_or_discourse_questions",
    "review_options_preserved",
    "theological_downstream_risks",
    "assumptions_avoided",
    "reviewed_gold_dependency",
    "non_authorizations",
    "validator_or_test_plan",
    "non_target_identity_plan",
}

REQUIRED_GLOBAL_NON_AUTHORIZATIONS = {
    "wj_dossier_as_reviewed_gold",
    "pending_packet_as_approval",
    "wj_marker_as_speaker_authority",
    "wj_marker_as_jesus_speaker_attribution",
    "wj_marker_as_speaker_boundary",
    "wj_marker_as_discourse_boundary",
    "wj_marker_as_chunk_boundary",
    "wj_marker_as_graph_edge",
    "wj_marker_as_retrieval_truth",
    "wj_marker_as_output_change",
    "formatting_as_speaker_authority",
    "punctuation_as_discourse_authority",
    "variant_wj_as_canonical_preference",
    "synoptic_parallel_as_harmonization_authority",
    "revelation_voice_identity_from_wj",
    "dominical_quotation_authority",
    "gospel_wj_implementation",
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
    "scripts/validate_gospel_wj_discourse_dossier_queue.py",
    "tests/test_gospel_wj_discourse_dossier_queue.py",
    "scripts/validate_wj_marker_inventory.py",
    "scripts/validate_wj_speaker_discourse_policy.py",
    "scripts/validate_john3_owner_review_docket.py",
    "scripts/validate_bible_wide_chunking_research_registry.py",
    "scripts/validate_chunking_agent_preflight.py",
    "scripts/validate_bible_chunking_readiness_map.py",
    "scripts/validate_chunking_theological_decision_register.py",
    "scripts/validate_all.py",
}

ALLOWED_STATUSES = {
    "owner_selection_pending",
    "existing_packet_pending",
    "speaker_review_required",
    "variant_policy_first",
    "revelation_research_first",
    "research_packet_pending",
}


class GospelWJDossierQueueError(ValueError):
    """Raised when the Gospel/WJ dossier queue is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise GospelWJDossierQueueError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise GospelWJDossierQueueError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise GospelWJDossierQueueError(f"{_rel(path)}: JSON unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise GospelWJDossierQueueError(f"{_rel(path)}: expected a JSON object")
    return data


def _require_string(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise GospelWJDossierQueueError(f"{label} must be a non-empty string")


def _require_string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise GospelWJDossierQueueError(f"{label} must be a non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise GospelWJDossierQueueError(f"{label} must contain only non-empty strings")
    return value


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    if not isinstance(actual, list):
        raise GospelWJDossierQueueError(f"{label} must be a list")
    missing = sorted(required - {str(item) for item in actual})
    if missing:
        raise GospelWJDossierQueueError(f"{label} missing {missing}")


def _require_evidence_only(text: str, label: str) -> None:
    lowered = text.lower()
    if "evidence only" not in lowered:
        raise GospelWJDossierQueueError(f"{label} must say evidence only")
    if "authorize" not in lowered and "authority" not in lowered:
        raise GospelWJDossierQueueError(f"{label} must explicitly deny authority")


def _index_entries_by_id() -> dict[str, dict[str, Any]]:
    index = _read_json(PACKET_INDEX)
    entries = index.get("entries")
    if not isinstance(entries, list) or not all(isinstance(entry, dict) for entry in entries):
        raise GospelWJDossierQueueError(f"{_rel(PACKET_INDEX)}: entries must be a list of objects")
    return {str(entry.get("entry_id")): entry for entry in entries}


def _validate_packet_state(packet_state: dict[str, Any]) -> None:
    if packet_state.get("packet_index") != "eval/chunking_gold/review_packets/review_packet_index.json":
        raise GospelWJDossierQueueError("existing_packet_state.packet_index path is wrong")
    index_by_id = _index_entries_by_id()
    pending_packets = packet_state.get("required_pending_packets")
    if not isinstance(pending_packets, list) or len(pending_packets) != len(REQUIRED_PENDING_PACKETS):
        raise GospelWJDossierQueueError("existing_packet_state.required_pending_packets has wrong length")
    packet_ids = {str(packet.get("entry_id")) for packet in pending_packets if isinstance(packet, dict)}
    missing_packets = sorted(set(REQUIRED_PENDING_PACKETS) - packet_ids)
    if missing_packets:
        raise GospelWJDossierQueueError(f"existing_packet_state missing packets {missing_packets}")
    for entry_id, expected in REQUIRED_PENDING_PACKETS.items():
        entry = index_by_id.get(entry_id)
        if entry is None:
            raise GospelWJDossierQueueError(f"{_rel(PACKET_INDEX)} missing {entry_id}")
        if entry.get("entry_type") != "review_packet":
            raise GospelWJDossierQueueError(f"{entry_id}.entry_type must be review_packet")
        if entry.get("case_id") != expected["case_id"]:
            raise GospelWJDossierQueueError(f"{entry_id}.case_id must be {expected['case_id']}")
        if entry.get("passage") != expected["passage"]:
            raise GospelWJDossierQueueError(f"{entry_id}.passage must be {expected['passage']}")
        if entry.get("status") != "pending_human_review":
            raise GospelWJDossierQueueError(f"{entry_id}.status must be pending_human_review")
        if entry.get("decision") != "pending":
            raise GospelWJDossierQueueError(f"{entry_id}.decision must be pending")
        for key in ("output_change_authorized", "implementation_allowed"):
            if entry.get(key) is not False:
                raise GospelWJDossierQueueError(f"{entry_id}.{key} must be false")

    policy_cases = packet_state.get("required_policy_cases")
    if not isinstance(policy_cases, list) or len(policy_cases) != len(REQUIRED_POLICY_CASES):
        raise GospelWJDossierQueueError("existing_packet_state.required_policy_cases has wrong length")
    policy_ids = {str(case.get("entry_id")) for case in policy_cases if isinstance(case, dict)}
    missing_policy = sorted(set(REQUIRED_POLICY_CASES) - policy_ids)
    if missing_policy:
        raise GospelWJDossierQueueError(f"existing_packet_state missing policy cases {missing_policy}")
    for entry_id, case_id in REQUIRED_POLICY_CASES.items():
        entry = index_by_id.get(entry_id)
        if entry is None:
            raise GospelWJDossierQueueError(f"{_rel(PACKET_INDEX)} missing {entry_id}")
        if entry.get("case_id") != case_id:
            raise GospelWJDossierQueueError(f"{entry_id}.case_id must be {case_id}")
        if entry.get("status") != "speaker_review_required":
            raise GospelWJDossierQueueError(f"{entry_id}.status must be speaker_review_required")
        for key in ("output_change_authorized", "implementation_allowed"):
            if entry.get(key) is not False:
                raise GospelWJDossierQueueError(f"{entry_id}.{key} must be false")


def _validate_wj_metadata(metadata: dict[str, Any]) -> None:
    inventory = _read_yaml(WJ_INVENTORY)
    summary = inventory.get("summary")
    if not isinstance(summary, dict):
        raise GospelWJDossierQueueError(f"{_rel(WJ_INVENTORY)}: summary must be a mapping")
    if metadata.get("source_inventory") != ".ai/control/wj_marker_inventory.yaml":
        raise GospelWJDossierQueueError("observed_wj_metadata.source_inventory path is wrong")
    for key in ("wj_word_tokens", "wj_token_runs", "books_with_wj", "books_outside_four_gospels_with_wj"):
        if metadata.get(key) != summary.get(key):
            raise GospelWJDossierQueueError(f"observed_wj_metadata.{key} must match WJ inventory")
    warning = str(metadata.get("warning", "")).lower()
    for phrase in ("evidence only", "presence", "absence", "speaker authority"):
        if phrase not in warning:
            raise GospelWJDossierQueueError(f"observed_wj_metadata.warning missing {phrase!r}")


def validate_gospel_wj_discourse_dossier_queue(path: Path = QUEUE) -> dict[str, Any]:
    data = _read_yaml(path)
    missing_top = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing_top:
        raise GospelWJDossierQueueError(f"{_rel(path)}: missing top-level keys {missing_top}")

    if data["object_type"] != "gospel_wj_discourse_dossier_queue":
        raise GospelWJDossierQueueError(f"{_rel(path)}: object_type must be gospel_wj_discourse_dossier_queue")
    if data["trust_zone"] != "canonical":
        raise GospelWJDossierQueueError(f"{_rel(path)}: trust_zone must be canonical")
    if data["lifecycle_status"] != "active":
        raise GospelWJDossierQueueError(f"{_rel(path)}: lifecycle_status must be active")
    if data["schema_version"] != "gospel_wj_discourse_dossier_queue.v1":
        raise GospelWJDossierQueueError(f"{_rel(path)}: schema_version must be gospel_wj_discourse_dossier_queue.v1")

    authority = data["authority"]
    if not isinstance(authority, dict):
        raise GospelWJDossierQueueError(f"{_rel(path)}: authority must be a mapping")
    for key in ("records_gospel_wj_dossier_queue", "records_wj_discourse_risks", "may_surface_for_review", "requires_owner_review_before_output"):
        if authority.get(key) is not True:
            raise GospelWJDossierQueueError(f"{_rel(path)}: authority.{key} must be true")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise GospelWJDossierQueueError(f"{_rel(path)}: authority.{key} must be false")

    scope = data["scope"]
    if not isinstance(scope, dict):
        raise GospelWJDossierQueueError(f"{_rel(path)}: scope must be a mapping")
    expected_scope = {
        "corpus_scope": "canonical_66",
        "lane": "gospel_discourse_wj",
        "research_mode": "non_output_changing",
    }
    for key, expected in expected_scope.items():
        if scope.get(key) != expected:
            raise GospelWJDossierQueueError(f"{_rel(path)}: scope.{key} must be {expected}")
    for key, phrases in {
        "relation_to_t354": ("WJ marker inventory", "evidence only"),
        "relation_to_t355": ("WJ speaker/discourse policy", "without selecting"),
        "relation_to_t356": ("owner_selection_pending", "not promoted"),
        "relation_to_t358": ("gospel_discourse_speaker_wj", "Bible-wide"),
        "relation_to_t360": ("Olivet", "Revelation", "hermeneutic neutrality"),
    }.items():
        text = str(scope.get(key, ""))
        for phrase in phrases:
            if phrase not in text:
                raise GospelWJDossierQueueError(f"{_rel(path)}: scope.{key} missing {phrase!r}")

    _validate_wj_metadata(data["observed_wj_metadata"])
    packet_state = data["existing_packet_state"]
    if not isinstance(packet_state, dict):
        raise GospelWJDossierQueueError(f"{_rel(path)}: existing_packet_state must be a mapping")
    _validate_packet_state(packet_state)

    policy = data["wj_discourse_preservation_policy"]
    if not isinstance(policy, dict):
        raise GospelWJDossierQueueError(f"{_rel(path)}: wj_discourse_preservation_policy must be a mapping")
    _require_subset(REQUIRED_REVIEW_OPTIONS, policy.get("preserved_review_options"), "preserved_review_options")
    _require_string_list(policy.get("not_selected_by_queue"), "not_selected_by_queue")
    boundary = str(policy.get("orthodox_boundary", ""))
    for phrase in ("Nicene/Chalcedonian", "refusing", "speaker identity"):
        if phrase not in boundary:
            raise GospelWJDossierQueueError(f"{_rel(path)}: orthodox_boundary missing {phrase!r}")

    channels = data["evidence_channels"]
    if not isinstance(channels, list) or not channels:
        raise GospelWJDossierQueueError(f"{_rel(path)}: evidence_channels must be a non-empty list")
    channel_ids: set[str] = set()
    for channel in channels:
        if not isinstance(channel, dict):
            raise GospelWJDossierQueueError(f"{_rel(path)}: each evidence channel must be a mapping")
        channel_id = str(channel.get("channel_id", ""))
        _require_string(channel_id, "evidence_channels.channel_id")
        channel_ids.add(channel_id)
        _require_string(channel.get("use_when"), f"{channel_id}.use_when")
        _require_string(channel.get("non_authorization"), f"{channel_id}.non_authorization")
        _require_evidence_only(channel["non_authorization"], f"{channel_id}.non_authorization")
    missing_channels = sorted(REQUIRED_EVIDENCE_CHANNELS - channel_ids)
    if missing_channels:
        raise GospelWJDossierQueueError(f"{_rel(path)}: missing evidence channels {missing_channels}")

    _require_subset(REQUIRED_DOSSIER_FIELDS, data["required_future_dossier_fields"], "required_future_dossier_fields")
    _require_subset(REQUIRED_GLOBAL_NON_AUTHORIZATIONS, data["global_non_authorizations"], "global_non_authorizations")
    _require_subset(REQUIRED_VALIDATORS, data["validators"], "validators")

    dossiers = data["dossier_queue"]
    if not isinstance(dossiers, list) or not dossiers:
        raise GospelWJDossierQueueError(f"{_rel(path)}: dossier_queue must be a non-empty list")
    dossier_ids: set[str] = set()
    priorities: list[int] = []
    for dossier in dossiers:
        if not isinstance(dossier, dict):
            raise GospelWJDossierQueueError(f"{_rel(path)}: each dossier must be a mapping")
        dossier_id = str(dossier.get("dossier_id", ""))
        _require_string(dossier_id, "dossier_queue.dossier_id")
        if dossier_id in dossier_ids:
            raise GospelWJDossierQueueError(f"{_rel(path)}: duplicate dossier_id {dossier_id}")
        dossier_ids.add(dossier_id)
        missing_fields = sorted(REQUIRED_DOSSIER_FIELDS - set(dossier))
        if missing_fields:
            raise GospelWJDossierQueueError(f"{dossier_id} missing fields {missing_fields}")
        if dossier.get("status") not in ALLOWED_STATUSES:
            raise GospelWJDossierQueueError(f"{dossier_id}.status is invalid")
        priority = dossier.get("priority")
        if not isinstance(priority, int):
            raise GospelWJDossierQueueError(f"{dossier_id}.priority must be an integer")
        priorities.append(priority)
        _require_string(dossier.get("title"), f"{dossier_id}.title")
        _require_string_list(dossier.get("exact_passage_scope"), f"{dossier_id}.exact_passage_scope")
        if not isinstance(dossier.get("source_metadata_observed"), dict):
            raise GospelWJDossierQueueError(f"{dossier_id}.source_metadata_observed must be a mapping")
        dossier_channels = set(_require_string_list(dossier.get("evidence_channels"), f"{dossier_id}.evidence_channels"))
        unknown_channels = sorted(dossier_channels - channel_ids)
        if unknown_channels:
            raise GospelWJDossierQueueError(f"{dossier_id}.evidence_channels unknown {unknown_channels}")
        _require_string_list(dossier.get("speaker_or_discourse_questions"), f"{dossier_id}.speaker_or_discourse_questions")
        options = set(_require_string_list(dossier.get("review_options_preserved"), f"{dossier_id}.review_options_preserved"))
        unknown_options = sorted(options - set(policy["preserved_review_options"]))
        if unknown_options:
            raise GospelWJDossierQueueError(f"{dossier_id}.review_options_preserved unknown {unknown_options}")
        _require_string_list(dossier.get("theological_downstream_risks"), f"{dossier_id}.theological_downstream_risks")
        _require_string_list(dossier.get("assumptions_avoided"), f"{dossier_id}.assumptions_avoided")
        _require_string(dossier.get("reviewed_gold_dependency"), f"{dossier_id}.reviewed_gold_dependency")
        for phrase in ("owner", "review", "reviewed", "graph", "retrieval", "route", "non-target"):
            if phrase not in dossier["reviewed_gold_dependency"].lower():
                raise GospelWJDossierQueueError(f"{dossier_id}.reviewed_gold_dependency missing {phrase!r}")
        non_authorizations = set(_require_string_list(dossier.get("non_authorizations"), f"{dossier_id}.non_authorizations"))
        for required in ("speaker_attribution", "speaker_boundary", "discourse_boundary", "reviewed_gold", "chunk_boundary", "route_behavior", "graph_edge", "retrieval_truth", "output_change"):
            if required not in non_authorizations:
                raise GospelWJDossierQueueError(f"{dossier_id}.non_authorizations missing {required}")
        _require_string(dossier.get("validator_or_test_plan"), f"{dossier_id}.validator_or_test_plan")
        _require_string(dossier.get("non_target_identity_plan"), f"{dossier_id}.non_target_identity_plan")
        if "unchanged identity" not in str(dossier["non_target_identity_plan"]):
            raise GospelWJDossierQueueError(f"{dossier_id}.non_target_identity_plan must require unchanged identity")

    missing_dossiers = sorted(REQUIRED_DOSSIERS - dossier_ids)
    if missing_dossiers:
        raise GospelWJDossierQueueError(f"{_rel(path)}: missing dossiers {missing_dossiers}")
    if priorities != sorted(priorities):
        raise GospelWJDossierQueueError(f"{_rel(path)}: dossier priorities must be sorted")

    return data


def main() -> int:
    try:
        validate_gospel_wj_discourse_dossier_queue()
    except GospelWJDossierQueueError as exc:
        print(f"Gospel/WJ discourse dossier queue validation failed: {exc}", file=sys.stderr)
        return 1
    print("Gospel/WJ discourse dossier queue validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
