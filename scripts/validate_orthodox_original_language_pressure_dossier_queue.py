#!/usr/bin/env python3
"""Validate the orthodox original-language pressure passage dossier queue."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / ".ai" / "control" / "orthodox_original_language_pressure_dossier_queue.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
ROADMAP = ROOT / "ROADMAP_STATE.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"

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
    "authorizes_original_language_truth",
    "authorizes_translation_preference",
    "authorizes_textual_critical_decision",
    "authorizes_canon_scope_change",
    "authorizes_boundary_import",
    "authorizes_nonorthodox_source_authority",
    "authorizes_extra_canonical_source_authority",
    "authorizes_doctrinal_system",
    "authorizes_chunk_boundaries",
    "authorizes_reviewed_gold",
    "authorizes_output_change",
    "authorizes_route_behavior",
    "authorizes_evaluator_change",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_embedding_or_vector_work",
    "authorizes_new_algorithm_work",
}

REQUIRED_EVIDENCE_CHANNELS = {
    "greek_lemma_morphology_syntax",
    "hebrew_lemma_morphology_syntax",
    "translation_divergence_pressure",
    "non_orthodox_prooftext_pressure",
    "extra_canonical_pressure",
    "divine_plurality_and_unity_language",
}

REQUIRED_REVIEW_OPTIONS = {
    "canonical_text_review",
    "greek_grammar_overlay_review",
    "hebrew_grammar_overlay_review",
    "morphology_syntax_review",
    "lexical_semantic_range_review",
    "translation_divergence_review",
    "non_orthodox_pressure_review",
    "ancient_jewish_context_review",
    "trinitarian_christological_boundary_review",
    "owner_review_before_any_authority_change",
}

REQUIRED_DOSSIERS = {
    "JOHN1_1_LOGOS_THEOS_GRAMMAR",
    "COL1_15_20_FIRSTBORN_ALL_THINGS",
    "TITUS2_13_2PET1_1_GOD_SAVIOR_GRAMMAR",
    "JOHN8_58_EGO_EIMI",
    "HEB1_SON_WORSHIP_AND_GOD_ADDRESS",
    "MATT28_19_TRIADIC_NAME",
    "GEN1_26_ELOHIM_US_IMAGE",
    "DEUT6_4_YHWH_ECHAD_UNITY",
    "PS110_1_YHWH_ADONI_MESSIANIC",
    "ISA43_44_ONE_GOD_LDS_POLYTHEISM",
    "ONECOR15_29_BAPTISM_FOR_DEAD",
    "ONEPET3_18_4_6_SPIRITS_PRISON_DEAD",
}

REQUIRED_DOSSIER_FIELDS = {
    "dossier_id",
    "title",
    "status",
    "priority",
    "exact_passage_scope",
    "primary_lanes",
    "pressure_sources",
    "evidence_channels",
    "original_language_focus",
    "grammar_overlay_needed",
    "boundary_questions",
    "orthodox_boundary",
    "theological_downstream_risks",
    "assumptions_avoided",
    "review_options_preserved",
    "reviewed_gold_dependency",
    "non_authorizations",
    "validator_or_test_plan",
    "non_target_identity_plan",
}

REQUIRED_GLOBAL_NON_AUTHORIZATIONS = {
    "pressure_queue_as_reviewed_gold",
    "original_language_as_automatic_truth",
    "grammar_overlay_as_chunk_boundary",
    "translation_divergence_as_translation_preference",
    "nonorthodox_source_as_authority",
    "extra_canonical_source_as_authority",
    "external_translation_import",
    "canon_scope_change",
    "boundary_import",
    "doctrinal_system_selection",
    "graph_edge_generation",
    "retrieval_truth",
    "route_behavior_change",
    "evaluator_change",
    "reviewed_gold_promotion",
    "chunk_output_change",
}

REQUIRED_VALIDATORS = {
    "scripts/validate_orthodox_original_language_pressure_dossier_queue.py",
    "tests/test_orthodox_original_language_pressure_dossier_queue.py",
    "scripts/validate_chunking_agent_preflight.py",
    "scripts/validate_bible_chunking_readiness_map.py",
    "scripts/validate_chunking_theological_decision_register.py",
    "scripts/validate_all.py",
}

ALLOWED_STATUSES = {"research_packet_pending", "research_only", "owner_review_pending"}


class OrthodoxLanguagePressureQueueError(ValueError):
    """Raised when the original-language pressure queue is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise OrthodoxLanguagePressureQueueError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        text = _read_text(path)
        if text.startswith("---\n"):
            parts = text.split("---\n", 2)
            if len(parts) == 3:
                text = parts[1] + "\n" + parts[2]
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise OrthodoxLanguagePressureQueueError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise OrthodoxLanguagePressureQueueError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_string(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise OrthodoxLanguagePressureQueueError(f"{label} must be a non-empty string")


def _require_string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise OrthodoxLanguagePressureQueueError(f"{label} must be a non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise OrthodoxLanguagePressureQueueError(f"{label} must contain only non-empty strings")
    return value


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    if not isinstance(actual, list):
        raise OrthodoxLanguagePressureQueueError(f"{label} must be a list")
    missing = sorted(required - {str(item) for item in actual})
    if missing:
        raise OrthodoxLanguagePressureQueueError(f"{label} missing {missing}")


def validate_orthodox_original_language_pressure_dossier_queue(path: Path = QUEUE) -> dict[str, Any]:
    data = _read_yaml(path)
    missing_top = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing_top:
        raise OrthodoxLanguagePressureQueueError(f"{_rel(path)}: missing top-level keys {missing_top}")

    if data["object_type"] != "orthodox_original_language_pressure_dossier_queue":
        raise OrthodoxLanguagePressureQueueError(f"{_rel(path)}: object_type is wrong")
    if data["trust_zone"] != "canonical":
        raise OrthodoxLanguagePressureQueueError(f"{_rel(path)}: trust_zone must be canonical")
    if data["lifecycle_status"] != "active":
        raise OrthodoxLanguagePressureQueueError(f"{_rel(path)}: lifecycle_status must be active")
    if data["schema_version"] != "orthodox_original_language_pressure_dossier_queue.v1":
        raise OrthodoxLanguagePressureQueueError(f"{_rel(path)}: schema_version is wrong")

    authority = data["authority"]
    if not isinstance(authority, dict):
        raise OrthodoxLanguagePressureQueueError(f"{_rel(path)}: authority must be a mapping")
    for key in ("records_original_language_pressure_queue", "records_non_orthodox_pressure_cases", "may_surface_for_review", "requires_owner_review_before_output"):
        if authority.get(key) is not True:
            raise OrthodoxLanguagePressureQueueError(f"{_rel(path)}: authority.{key} must be true")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise OrthodoxLanguagePressureQueueError(f"{_rel(path)}: authority.{key} must be false")

    scope = data["scope"]
    if not isinstance(scope, dict):
        raise OrthodoxLanguagePressureQueueError(f"{_rel(path)}: scope must be a mapping")
    if scope.get("corpus_scope") != "canonical_66":
        raise OrthodoxLanguagePressureQueueError(f"{_rel(path)}: scope.corpus_scope must be canonical_66")
    if scope.get("research_mode") != "non_output_changing":
        raise OrthodoxLanguagePressureQueueError(f"{_rel(path)}: scope.research_mode must be non_output_changing")
    lanes = set(_require_string_list(scope.get("lanes"), "scope.lanes"))
    for required_lane in ("source_metadata_research", "textual_variant_source_tradition", "epistle_argument", "gospel_discourse_wj"):
        if required_lane not in lanes:
            raise OrthodoxLanguagePressureQueueError(f"{_rel(path)}: scope.lanes missing {required_lane}")

    policy = data["preservation_policy"]
    if not isinstance(policy, dict):
        raise OrthodoxLanguagePressureQueueError(f"{_rel(path)}: preservation_policy must be a mapping")
    boundary = str(policy.get("orthodox_boundary", ""))
    for phrase in ("Nicene/Chalcedonian", "canonical Scripture", "LDS", "Watch Tower", "anti-Trinitarian"):
        if phrase not in boundary:
            raise OrthodoxLanguagePressureQueueError(f"{_rel(path)}: orthodox_boundary missing {phrase!r}")
    source_rule = str(policy.get("canonical_source_rule", ""))
    for phrase in ("canonical 66", "not imported", "not promoted"):
        if phrase not in source_rule:
            raise OrthodoxLanguagePressureQueueError(f"{_rel(path)}: canonical_source_rule missing {phrase!r}")
    language_rule = str(policy.get("source_language_rule", ""))
    for phrase in ("evidence", "do not", "chunk boundaries", "output changes"):
        if phrase not in language_rule:
            raise OrthodoxLanguagePressureQueueError(f"{_rel(path)}: source_language_rule missing {phrase!r}")
    _require_subset(REQUIRED_REVIEW_OPTIONS, policy.get("preserved_review_options"), "preserved_review_options")
    _require_string_list(policy.get("not_selected_by_queue"), "not_selected_by_queue")

    channels = data["evidence_channels"]
    if not isinstance(channels, list) or not channels:
        raise OrthodoxLanguagePressureQueueError(f"{_rel(path)}: evidence_channels must be a non-empty list")
    channel_ids: set[str] = set()
    for channel in channels:
        if not isinstance(channel, dict):
            raise OrthodoxLanguagePressureQueueError(f"{_rel(path)}: each evidence channel must be a mapping")
        channel_id = str(channel.get("channel_id", ""))
        _require_string(channel_id, "evidence_channels.channel_id")
        channel_ids.add(channel_id)
        _require_string(channel.get("use_when"), f"{channel_id}.use_when")
        _require_string(channel.get("non_authorization"), f"{channel_id}.non_authorization")
        lowered = str(channel["non_authorization"]).lower()
        if "evidence only" not in lowered or ("authorize" not in lowered and "authority" not in lowered):
            raise OrthodoxLanguagePressureQueueError(f"{channel_id}.non_authorization must deny authority")
    missing_channels = sorted(REQUIRED_EVIDENCE_CHANNELS - channel_ids)
    if missing_channels:
        raise OrthodoxLanguagePressureQueueError(f"{_rel(path)}: missing evidence channels {missing_channels}")

    _require_subset(REQUIRED_DOSSIER_FIELDS, data["required_future_dossier_fields"], "required_future_dossier_fields")
    _require_subset(REQUIRED_GLOBAL_NON_AUTHORIZATIONS, data["global_non_authorizations"], "global_non_authorizations")
    _require_subset(REQUIRED_VALIDATORS, data["validators"], "validators")

    dossiers = data["dossier_queue"]
    if not isinstance(dossiers, list) or not dossiers:
        raise OrthodoxLanguagePressureQueueError(f"{_rel(path)}: dossier_queue must be a non-empty list")
    dossier_ids: set[str] = set()
    priorities: list[int] = []
    for dossier in dossiers:
        if not isinstance(dossier, dict):
            raise OrthodoxLanguagePressureQueueError(f"{_rel(path)}: each dossier must be a mapping")
        dossier_id = str(dossier.get("dossier_id", ""))
        _require_string(dossier_id, "dossier_queue.dossier_id")
        if dossier_id in dossier_ids:
            raise OrthodoxLanguagePressureQueueError(f"{_rel(path)}: duplicate dossier_id {dossier_id}")
        dossier_ids.add(dossier_id)
        missing_fields = sorted(REQUIRED_DOSSIER_FIELDS - set(dossier))
        if missing_fields:
            raise OrthodoxLanguagePressureQueueError(f"{dossier_id} missing fields {missing_fields}")
        if dossier.get("status") not in ALLOWED_STATUSES:
            raise OrthodoxLanguagePressureQueueError(f"{dossier_id}.status is invalid")
        priority = dossier.get("priority")
        if not isinstance(priority, int):
            raise OrthodoxLanguagePressureQueueError(f"{dossier_id}.priority must be an integer")
        priorities.append(priority)
        _require_string(dossier.get("title"), f"{dossier_id}.title")
        _require_string_list(dossier.get("exact_passage_scope"), f"{dossier_id}.exact_passage_scope")
        _require_string_list(dossier.get("primary_lanes"), f"{dossier_id}.primary_lanes")
        _require_string_list(dossier.get("pressure_sources"), f"{dossier_id}.pressure_sources")
        dossier_channels = set(_require_string_list(dossier.get("evidence_channels"), f"{dossier_id}.evidence_channels"))
        unknown_channels = sorted(dossier_channels - channel_ids)
        if unknown_channels:
            raise OrthodoxLanguagePressureQueueError(f"{dossier_id}.evidence_channels unknown {unknown_channels}")
        _require_string(dossier.get("original_language_focus"), f"{dossier_id}.original_language_focus")
        if dossier.get("grammar_overlay_needed") is not True:
            raise OrthodoxLanguagePressureQueueError(f"{dossier_id}.grammar_overlay_needed must be true")
        for key in ("boundary_questions", "theological_downstream_risks", "assumptions_avoided"):
            _require_string_list(dossier.get(key), f"{dossier_id}.{key}")
        _require_string(dossier.get("orthodox_boundary"), f"{dossier_id}.orthodox_boundary")
        options = set(_require_string_list(dossier.get("review_options_preserved"), f"{dossier_id}.review_options_preserved"))
        unknown_options = sorted(options - set(policy["preserved_review_options"]))
        if unknown_options:
            raise OrthodoxLanguagePressureQueueError(f"{dossier_id}.review_options_preserved unknown {unknown_options}")
        _require_string(dossier.get("reviewed_gold_dependency"), f"{dossier_id}.reviewed_gold_dependency")
        for phrase in ("owner", "review", "grammar", "reviewed", "non-target", "graph", "retrieval", "route"):
            if phrase not in dossier["reviewed_gold_dependency"].lower():
                raise OrthodoxLanguagePressureQueueError(f"{dossier_id}.reviewed_gold_dependency missing {phrase!r}")
        non_auth = set(_require_string_list(dossier.get("non_authorizations"), f"{dossier_id}.non_authorizations"))
        for required in ("source_language_as_automatic_truth", "nonorthodox_source_authority", "chunk_boundary", "reviewed_gold", "output_change", "route_behavior", "graph_edge", "retrieval_truth", "boundary_import"):
            if required not in non_auth:
                raise OrthodoxLanguagePressureQueueError(f"{dossier_id}.non_authorizations missing {required}")
        _require_string(dossier.get("validator_or_test_plan"), f"{dossier_id}.validator_or_test_plan")
        _require_string(dossier.get("non_target_identity_plan"), f"{dossier_id}.non_target_identity_plan")
        if "unchanged identity" not in str(dossier["non_target_identity_plan"]):
            raise OrthodoxLanguagePressureQueueError(f"{dossier_id}.non_target_identity_plan must require unchanged identity")

    missing_dossiers = sorted(REQUIRED_DOSSIERS - dossier_ids)
    if missing_dossiers:
        raise OrthodoxLanguagePressureQueueError(f"{_rel(path)}: missing dossiers {missing_dossiers}")
    if priorities != sorted(priorities):
        raise OrthodoxLanguagePressureQueueError(f"{_rel(path)}: dossier priorities must be sorted")

    _validate_governed_links()
    return data


def _validate_governed_links() -> None:
    queue_rel = ".ai/control/orthodox_original_language_pressure_dossier_queue.yaml"

    preflight = _read_yaml(PREFLIGHT)
    reading_paths = {str(item.get("path")) for item in preflight.get("mandatory_reading", []) if isinstance(item, dict)}
    if queue_rel not in reading_paths:
        raise OrthodoxLanguagePressureQueueError(f"{_rel(PREFLIGHT)}: pressure queue must be mandatory reading")

    register_text = _read_text(REGISTER)
    for phrase in ("CD-043", "Original-language pressure passages require governed review before chunk authority", "T377"):
        if phrase not in register_text:
            raise OrthodoxLanguagePressureQueueError(f"{_rel(REGISTER)}: missing {phrase!r}")

    readiness_text = _read_text(READINESS)
    if queue_rel not in readiness_text:
        raise OrthodoxLanguagePressureQueueError(f"{_rel(READINESS)}: missing pressure queue surface")

    roadmap = _read_yaml(ROADMAP)
    phase_4 = roadmap.get("phases", {}).get("phase_4", {})
    tasks = {item.get("id"): item for item in phase_4.get("tasks", []) if isinstance(item, dict)}
    future = {item.get("id"): item for item in phase_4.get("future_sequence", []) if isinstance(item, dict)}
    task = tasks.get("T377") or future.get("T377")
    if not isinstance(task, dict) or task.get("status") != "complete":
        raise OrthodoxLanguagePressureQueueError(f"{_rel(ROADMAP)}: T377 must be recorded complete")
    if task.get("dossier_queue") != queue_rel:
        raise OrthodoxLanguagePressureQueueError(f"{_rel(ROADMAP)}: T377 dossier_queue is stale")
    if task.get("output_change_authorized") is not False:
        raise OrthodoxLanguagePressureQueueError(f"{_rel(ROADMAP)}: T377 output_change_authorized must be false")

    for path in (FRONT_DOOR, TOC, ROADMAP_TOC):
        text = _read_text(path)
        for phrase in (queue_rel, "original-language", "non-orthodox", "grammar"):
            if phrase not in text:
                raise OrthodoxLanguagePressureQueueError(f"{_rel(path)}: missing {phrase!r}")


def main() -> int:
    try:
        validate_orthodox_original_language_pressure_dossier_queue()
    except OrthodoxLanguagePressureQueueError as exc:
        print(f"Orthodox original-language pressure queue validation failed: {exc}", file=sys.stderr)
        return 1
    print("Orthodox original-language pressure queue validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
