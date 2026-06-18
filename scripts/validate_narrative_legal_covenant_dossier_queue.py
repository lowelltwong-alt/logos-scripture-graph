#!/usr/bin/env python3
"""Validate the narrative/legal covenant dossier queue."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / ".ai" / "control" / "narrative_legal_covenant_dossier_queue.yaml"

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
    "authorizes_covenant_theology",
    "authorizes_law_gospel_framework",
    "authorizes_typology",
    "authorizes_harmonization",
    "authorizes_source_critical_partition",
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
    "local_scene_review",
    "parent_cycle_review",
    "parent_with_child_scene_review",
    "genealogy_or_list_review",
    "law_code_unit_review",
    "covenant_speech_review",
    "ritual_instruction_review",
    "royal_annal_formula_review",
    "embedded_document_or_decree_review",
    "gospel_narrative_scene_review",
}

REQUIRED_EVIDENCE_CHANNELS = {
    "narrative_scene_markers",
    "speech_and_dialogue_frame",
    "genealogy_list_formula",
    "legal_covenant_formula",
    "ritual_instruction_sequence",
    "royal_annal_or_regnal_formula",
    "embedded_document_or_decree",
    "source_metadata_formatting",
    "canonical_sequence_and_parallel_accounts",
    "theological_motif_repetition",
}

REQUIRED_DOSSIERS = {
    "GEN1_11_PRIMEVAL_NARRATIVE_GENEALOGY",
    "GEN12_50_PATRIARCHAL_COVENANT_CYCLES",
    "EXOD19_24_SINAI_COVENANT_NARRATIVE_LAW",
    "LEV1_7_SACRIFICE_RITUAL_LAW",
    "NUM22_24_BALAAM_ORACLE_NARRATIVE",
    "DEUT5_30_COVENANT_SPEECH_LAW",
    "JOSH13_21_LAND_ALLOTMENT_LISTS",
    "SAM_KINGS_ROYAL_COVENANT_ANNALS",
    "CHRONICLES_EZRA_NEHEMIAH_RESTORATION_LISTS",
    "MATT_LUKE_GENEALOGY_BIRTH_NARRATIVE",
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
    "narrative_dossier_as_reviewed_gold",
    "legal_dossier_as_reviewed_gold",
    "scene_label_as_chunk_boundary",
    "law_formula_as_covenant_system",
    "ritual_sequence_as_fulfillment_claim",
    "genealogy_as_identity_hierarchy",
    "list_formula_as_graph_edge",
    "royal_annal_as_theological_verdict",
    "embedded_document_as_source_partition",
    "parallel_account_as_harmonization_authority",
    "source_metadata_as_authority",
    "heading_as_chunk_boundary",
    "covenant_system_selection",
    "law_gospel_framework_selection",
    "typology_selection",
    "chronology_harmonization",
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
    "scripts/validate_narrative_legal_covenant_dossier_queue.py",
    "tests/test_narrative_legal_covenant_dossier_queue.py",
    "scripts/validate_bible_wide_chunking_research_registry.py",
    "scripts/validate_chunking_agent_preflight.py",
    "scripts/validate_bible_chunking_readiness_map.py",
    "scripts/validate_chunking_theological_decision_register.py",
    "scripts/validate_all.py",
}

ALLOWED_STATUSES = {"research_packet_pending", "research_only", "owner_review_pending"}
ALLOWED_LANES = {"narrative_pericope", "legal_covenant_formulae"}


class NarrativeLegalCovenantQueueError(ValueError):
    """Raised when the narrative/legal covenant queue is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise NarrativeLegalCovenantQueueError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise NarrativeLegalCovenantQueueError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_string(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise NarrativeLegalCovenantQueueError(f"{label} must be a non-empty string")


def _require_string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise NarrativeLegalCovenantQueueError(f"{label} must be a non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise NarrativeLegalCovenantQueueError(f"{label} must contain only non-empty strings")
    return value


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    if not isinstance(actual, list):
        raise NarrativeLegalCovenantQueueError(f"{label} must be a list")
    missing = sorted(required - {str(item) for item in actual})
    if missing:
        raise NarrativeLegalCovenantQueueError(f"{label} missing {missing}")


def _require_evidence_only(text: str, label: str) -> None:
    lowered = text.lower()
    if "evidence only" not in lowered:
        raise NarrativeLegalCovenantQueueError(f"{label} must say evidence only")
    if "authorize" not in lowered and "authority" not in lowered:
        raise NarrativeLegalCovenantQueueError(f"{label} must explicitly deny authority")


def validate_narrative_legal_covenant_dossier_queue(path: Path = QUEUE) -> dict[str, Any]:
    data = _read_yaml(path)
    missing_top = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing_top:
        raise NarrativeLegalCovenantQueueError(f"{_rel(path)}: missing top-level keys {missing_top}")

    if data["object_type"] != "narrative_legal_covenant_dossier_queue":
        raise NarrativeLegalCovenantQueueError(f"{_rel(path)}: object_type must be narrative_legal_covenant_dossier_queue")
    if data["trust_zone"] != "canonical":
        raise NarrativeLegalCovenantQueueError(f"{_rel(path)}: trust_zone must be canonical")
    if data["lifecycle_status"] != "active":
        raise NarrativeLegalCovenantQueueError(f"{_rel(path)}: lifecycle_status must be active")
    if data["schema_version"] != "narrative_legal_covenant_dossier_queue.v1":
        raise NarrativeLegalCovenantQueueError(f"{_rel(path)}: schema_version must be narrative_legal_covenant_dossier_queue.v1")

    authority = data["authority"]
    if not isinstance(authority, dict):
        raise NarrativeLegalCovenantQueueError(f"{_rel(path)}: authority must be a mapping")
    for key in ("records_narrative_legal_dossier_queue", "records_covenant_boundary_risks", "may_surface_for_review", "requires_owner_review_before_output"):
        if authority.get(key) is not True:
            raise NarrativeLegalCovenantQueueError(f"{_rel(path)}: authority.{key} must be true")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise NarrativeLegalCovenantQueueError(f"{_rel(path)}: authority.{key} must be false")

    scope = data["scope"]
    if not isinstance(scope, dict):
        raise NarrativeLegalCovenantQueueError(f"{_rel(path)}: scope must be a mapping")
    if scope.get("corpus_scope") != "canonical_66":
        raise NarrativeLegalCovenantQueueError(f"{_rel(path)}: scope.corpus_scope must be canonical_66")
    if scope.get("research_mode") != "non_output_changing":
        raise NarrativeLegalCovenantQueueError(f"{_rel(path)}: scope.research_mode must be non_output_changing")
    _require_subset(ALLOWED_LANES, scope.get("lanes"), "scope.lanes")
    for key, phrases in {
        "relation_to_t358": ("narrative_scene_pericope", "legal_covenant_formulae"),
        "relation_to_t359": ("evidence only", "authority"),
        "relation_to_t362": ("Complements", "without authorizing"),
    }.items():
        text = str(scope.get(key, ""))
        for phrase in phrases:
            if phrase not in text:
                raise NarrativeLegalCovenantQueueError(f"{_rel(path)}: scope.{key} missing {phrase!r}")

    policy = data["preservation_policy"]
    if not isinstance(policy, dict):
        raise NarrativeLegalCovenantQueueError(f"{_rel(path)}: preservation_policy must be a mapping")
    _require_subset(REQUIRED_REVIEW_OPTIONS, policy.get("preserved_review_options"), "preserved_review_options")
    _require_string_list(policy.get("not_selected_by_queue"), "not_selected_by_queue")
    boundary = str(policy.get("orthodox_boundary", ""))
    for phrase in ("Nicene/Chalcedonian", "refusing", "covenant"):
        if phrase not in boundary:
            raise NarrativeLegalCovenantQueueError(f"{_rel(path)}: orthodox_boundary missing {phrase!r}")

    channels = data["evidence_channels"]
    if not isinstance(channels, list) or not channels:
        raise NarrativeLegalCovenantQueueError(f"{_rel(path)}: evidence_channels must be a non-empty list")
    channel_ids: set[str] = set()
    for channel in channels:
        if not isinstance(channel, dict):
            raise NarrativeLegalCovenantQueueError(f"{_rel(path)}: each evidence channel must be a mapping")
        channel_id = str(channel.get("channel_id", ""))
        _require_string(channel_id, "evidence_channels.channel_id")
        channel_ids.add(channel_id)
        _require_string(channel.get("use_when"), f"{channel_id}.use_when")
        _require_string(channel.get("non_authorization"), f"{channel_id}.non_authorization")
        _require_evidence_only(channel["non_authorization"], f"{channel_id}.non_authorization")
    missing_channels = sorted(REQUIRED_EVIDENCE_CHANNELS - channel_ids)
    if missing_channels:
        raise NarrativeLegalCovenantQueueError(f"{_rel(path)}: missing evidence channels {missing_channels}")

    _require_subset(REQUIRED_DOSSIER_FIELDS, data["required_future_dossier_fields"], "required_future_dossier_fields")
    _require_subset(REQUIRED_GLOBAL_NON_AUTHORIZATIONS, data["global_non_authorizations"], "global_non_authorizations")
    _require_subset(REQUIRED_VALIDATORS, data["validators"], "validators")

    dossiers = data["dossier_queue"]
    if not isinstance(dossiers, list) or not dossiers:
        raise NarrativeLegalCovenantQueueError(f"{_rel(path)}: dossier_queue must be a non-empty list")
    dossier_ids: set[str] = set()
    priorities: list[int] = []
    for dossier in dossiers:
        if not isinstance(dossier, dict):
            raise NarrativeLegalCovenantQueueError(f"{_rel(path)}: each dossier must be a mapping")
        dossier_id = str(dossier.get("dossier_id", ""))
        _require_string(dossier_id, "dossier_queue.dossier_id")
        if dossier_id in dossier_ids:
            raise NarrativeLegalCovenantQueueError(f"{_rel(path)}: duplicate dossier_id {dossier_id}")
        dossier_ids.add(dossier_id)
        missing_fields = sorted(REQUIRED_DOSSIER_FIELDS - set(dossier))
        if missing_fields:
            raise NarrativeLegalCovenantQueueError(f"{dossier_id} missing fields {missing_fields}")
        if dossier.get("status") not in ALLOWED_STATUSES:
            raise NarrativeLegalCovenantQueueError(f"{dossier_id}.status is invalid")
        if dossier.get("primary_lane") not in ALLOWED_LANES:
            raise NarrativeLegalCovenantQueueError(f"{dossier_id}.primary_lane is invalid")
        priority = dossier.get("priority")
        if not isinstance(priority, int):
            raise NarrativeLegalCovenantQueueError(f"{dossier_id}.priority must be an integer")
        priorities.append(priority)
        _require_string(dossier.get("title"), f"{dossier_id}.title")
        _require_string_list(dossier.get("exact_passage_scope"), f"{dossier_id}.exact_passage_scope")
        dossier_channels = set(_require_string_list(dossier.get("evidence_channels"), f"{dossier_id}.evidence_channels"))
        unknown_channels = sorted(dossier_channels - channel_ids)
        if unknown_channels:
            raise NarrativeLegalCovenantQueueError(f"{dossier_id}.evidence_channels unknown {unknown_channels}")
        options = set(_require_string_list(dossier.get("review_options_preserved"), f"{dossier_id}.review_options_preserved"))
        unknown_options = sorted(options - set(policy["preserved_review_options"]))
        if unknown_options:
            raise NarrativeLegalCovenantQueueError(f"{dossier_id}.review_options_preserved unknown {unknown_options}")
        _require_string_list(dossier.get("boundary_questions"), f"{dossier_id}.boundary_questions")
        _require_string_list(dossier.get("theological_downstream_risks"), f"{dossier_id}.theological_downstream_risks")
        _require_string_list(dossier.get("assumptions_avoided"), f"{dossier_id}.assumptions_avoided")
        _require_string(dossier.get("reviewed_gold_dependency"), f"{dossier_id}.reviewed_gold_dependency")
        for phrase in ("owner", "review", "reviewed", "non-target", "graph", "retrieval", "route"):
            if phrase not in dossier["reviewed_gold_dependency"].lower():
                raise NarrativeLegalCovenantQueueError(f"{dossier_id}.reviewed_gold_dependency missing {phrase!r}")
        non_authorizations = set(_require_string_list(dossier.get("non_authorizations"), f"{dossier_id}.non_authorizations"))
        for required in ("chunk_boundary", "reviewed_gold", "output_change", "route_behavior", "graph_edge", "retrieval_truth"):
            if required not in non_authorizations:
                raise NarrativeLegalCovenantQueueError(f"{dossier_id}.non_authorizations missing {required}")
        _require_string(dossier.get("validator_or_test_plan"), f"{dossier_id}.validator_or_test_plan")
        _require_string(dossier.get("non_target_identity_plan"), f"{dossier_id}.non_target_identity_plan")
        if "unchanged identity" not in str(dossier["non_target_identity_plan"]):
            raise NarrativeLegalCovenantQueueError(f"{dossier_id}.non_target_identity_plan must require unchanged identity")

    missing_dossiers = sorted(REQUIRED_DOSSIERS - dossier_ids)
    if missing_dossiers:
        raise NarrativeLegalCovenantQueueError(f"{_rel(path)}: missing dossiers {missing_dossiers}")
    if priorities != sorted(priorities):
        raise NarrativeLegalCovenantQueueError(f"{_rel(path)}: dossier priorities must be sorted")

    return data


def main() -> int:
    try:
        validate_narrative_legal_covenant_dossier_queue()
    except NarrativeLegalCovenantQueueError as exc:
        print(f"Narrative/legal covenant dossier queue validation failed: {exc}", file=sys.stderr)
        return 1
    print("Narrative/legal covenant dossier queue validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
