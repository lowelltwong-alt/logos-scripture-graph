#!/usr/bin/env python3
"""Validate the apocalyptic/prophetic intertext dossier queue."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / ".ai" / "control" / "apocalyptic_prophetic_intertext_dossier_queue.yaml"
CROSSREFS = ROOT / "data" / "canonical" / "translations" / "eng-web" / "editorial_cross_references.jsonl"

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
    "observed_source_metadata_limits",
    "hermeneutic_preservation_policy",
    "evidence_channels",
    "required_future_dossier_fields",
    "dossier_queue",
    "global_non_authorizations",
    "validators",
}

REQUIRED_FALSE_AUTHORITY = {
    "authorizes_scripture_truth",
    "authorizes_lexical_truth",
    "authorizes_intertext_truth",
    "authorizes_speaker_attribution",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_chunk_boundaries",
    "authorizes_reviewed_gold",
    "authorizes_output_change",
    "authorizes_boundary_import",
    "authorizes_new_algorithm_work",
}

REQUIRED_HERMENEUTIC_OPTIONS = {
    "futurist",
    "preterist",
    "historicist",
    "idealist",
    "premillennial",
    "amillennial",
    "postmillennial",
    "already_not_yet",
}

REQUIRED_EVIDENCE_CHANNELS = {
    "explicit_canonical_quotation",
    "editorial_cross_reference_metadata",
    "repeated_phrase_or_title",
    "shared_symbol_or_vision_structure",
    "wj_or_voice_metadata",
    "divine_title_capitalization",
}

REQUIRED_DOSSIERS = {
    "REV_DAN_SON_OF_MAN",
    "REV_PS2_ROD_OF_IRON",
    "REV_EXOD_ISA_KINGDOM_PRIESTS",
    "OLIVET_DANIEL_ABOMINATION",
    "COSMIC_SIGNS_DAY_OF_THE_LORD",
    "EZEKIEL_TEMPLE_CITY_REVELATION_NEW_CREATION",
    "ZECHARIAH_PIERCED_MOURNING_AND_REVELATION",
}

REQUIRED_PACKET_FIELDS = {
    "dossier_id",
    "exact_passage_scope",
    "source_passages",
    "candidate_intertexts",
    "evidence_channels",
    "source_metadata_observed",
    "hermeneutic_options_preserved",
    "theological_downstream_risks",
    "assumptions_avoided",
    "reviewed_gold_dependency",
    "non_authorizations",
    "validator_or_test_plan",
    "non_target_identity_plan",
}

REQUIRED_GLOBAL_NON_AUTHORIZATIONS = {
    "intertext_dossier_as_truth",
    "editorial_crossref_as_graph_edge",
    "lexical_rarity_as_intertext_truth",
    "shared_symbol_as_identity_claim",
    "wj_marker_as_speaker_attribution",
    "capitalization_as_divine_identity",
    "heading_as_chunk_boundary",
    "hermeneutic_system_selection",
    "revelation_implementation",
    "daniel_revelation_chronology",
    "reviewed_gold_promotion",
    "chunk_output_change",
    "graph_edge_generation",
    "retrieval_truth",
    "boundary_import",
    "t345",
}

REQUIRED_VALIDATORS = {
    "scripts/validate_apocalyptic_prophetic_intertext_dossier_queue.py",
    "tests/test_apocalyptic_prophetic_intertext_dossier_queue.py",
    "scripts/validate_bible_wide_chunking_research_registry.py",
    "scripts/validate_source_metadata_research_atlas.py",
    "scripts/validate_chunking_agent_preflight.py",
    "scripts/validate_all.py",
}

ALLOWED_STATUSES = {"research_packet_pending", "owner_review_pending", "research_only"}


class ApocalypticIntertextQueueError(ValueError):
    """Raised when the apocalyptic/prophetic intertext dossier queue is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ApocalypticIntertextQueueError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise ApocalypticIntertextQueueError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_string(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ApocalypticIntertextQueueError(f"{label} must be a non-empty string")


def _require_string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ApocalypticIntertextQueueError(f"{label} must be a non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise ApocalypticIntertextQueueError(f"{label} must contain only non-empty strings")
    return value


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    if not isinstance(actual, list):
        raise ApocalypticIntertextQueueError(f"{label} must be a list")
    missing = sorted(required - {str(item) for item in actual})
    if missing:
        raise ApocalypticIntertextQueueError(f"{label} missing {missing}")


def _require_evidence_only(text: str, label: str) -> None:
    lowered = text.lower()
    if "evidence only" not in lowered:
        raise ApocalypticIntertextQueueError(f"{label} must say evidence only")
    if "authorize" not in lowered and "authority" not in lowered:
        raise ApocalypticIntertextQueueError(f"{label} must explicitly deny authority")


def _crossref_origin_counts() -> Counter[str]:
    counts: Counter[str] = Counter()
    try:
        with CROSSREFS.open("r", encoding="utf-8") as handle:
            for line in handle:
                record = json.loads(line)
                book = str(record.get("book") or record.get("osis_book") or "")
                if book:
                    counts[book] += 1
    except OSError as exc:
        raise ApocalypticIntertextQueueError(f"{_rel(CROSSREFS)}: unreadable: {exc}") from exc
    return counts


def validate_apocalyptic_prophetic_intertext_dossier_queue(path: Path = QUEUE) -> dict[str, Any]:
    data = _read_yaml(path)
    missing_top = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing_top:
        raise ApocalypticIntertextQueueError(f"{_rel(path)}: missing top-level keys {missing_top}")

    if data["object_type"] != "apocalyptic_prophetic_intertext_dossier_queue":
        raise ApocalypticIntertextQueueError(f"{_rel(path)}: object_type must be apocalyptic_prophetic_intertext_dossier_queue")
    if data["trust_zone"] != "canonical":
        raise ApocalypticIntertextQueueError(f"{_rel(path)}: trust_zone must be canonical")
    if data["lifecycle_status"] != "active":
        raise ApocalypticIntertextQueueError(f"{_rel(path)}: lifecycle_status must be active")
    if data["schema_version"] != "apocalyptic_prophetic_intertext_dossier_queue.v1":
        raise ApocalypticIntertextQueueError(f"{_rel(path)}: schema_version must be apocalyptic_prophetic_intertext_dossier_queue.v1")

    authority = data["authority"]
    if not isinstance(authority, dict):
        raise ApocalypticIntertextQueueError(f"{_rel(path)}: authority must be a mapping")
    for key in ("records_intertext_dossier_queue", "records_hermeneutic_risks", "may_surface_for_review"):
        if authority.get(key) is not True:
            raise ApocalypticIntertextQueueError(f"{_rel(path)}: authority.{key} must be true")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise ApocalypticIntertextQueueError(f"{_rel(path)}: authority.{key} must be false")

    scope = data["scope"]
    if not isinstance(scope, dict):
        raise ApocalypticIntertextQueueError(f"{_rel(path)}: scope must be a mapping")
    if scope.get("corpus_scope") != "canonical_66":
        raise ApocalypticIntertextQueueError(f"{_rel(path)}: scope.corpus_scope must be canonical_66")
    if scope.get("research_mode") != "non_output_changing":
        raise ApocalypticIntertextQueueError(f"{_rel(path)}: scope.research_mode must be non_output_changing")
    for phrase in ("Companion dossier queue", "apocalyptic_symbol_intertext", "prophetic_oracle_vision"):
        if phrase not in str(scope.get("relation_to_t358", "")):
            raise ApocalypticIntertextQueueError(f"{_rel(path)}: scope.relation_to_t358 missing {phrase!r}")
    if "evidence only" not in str(scope.get("relation_to_t359", "")).lower():
        raise ApocalypticIntertextQueueError(f"{_rel(path)}: scope.relation_to_t359 must keep metadata evidence only")

    limits = data["observed_source_metadata_limits"]
    if not isinstance(limits, dict):
        raise ApocalypticIntertextQueueError(f"{_rel(path)}: observed_source_metadata_limits must be a mapping")
    counts = _crossref_origin_counts()
    expected_counts = {
        "canonical_cross_reference_records": sum(counts.values()),
        "revelation_origin_cross_reference_records": counts["Rev"],
        "daniel_origin_cross_reference_records": counts["Dan"],
        "ezekiel_origin_cross_reference_records": counts["Ezek"],
        "zechariah_origin_cross_reference_records": counts["Zech"],
        "isaiah_origin_cross_reference_records": counts["Isa"],
    }
    for key, expected in expected_counts.items():
        if limits.get(key) != expected:
            raise ApocalypticIntertextQueueError(f"{_rel(path)}: {key} must be {expected}")
    for phrase in ("sparse", "absence", "not", "intertext authority"):
        if phrase not in str(limits.get("warning", "")).lower():
            raise ApocalypticIntertextQueueError(f"{_rel(path)}: metadata warning missing {phrase!r}")

    policy = data["hermeneutic_preservation_policy"]
    if not isinstance(policy, dict):
        raise ApocalypticIntertextQueueError(f"{_rel(path)}: hermeneutic_preservation_policy must be a mapping")
    _require_subset(REQUIRED_HERMENEUTIC_OPTIONS, policy.get("preserved_orthodox_options"), "preserved_orthodox_options")
    _require_string_list(policy.get("not_selected_by_queue"), "not_selected_by_queue")
    boundary = str(policy.get("orthodox_boundary", ""))
    for phrase in ("Nicene/Chalcedonian", "refusing", "eschatological"):
        if phrase not in boundary:
            raise ApocalypticIntertextQueueError(f"{_rel(path)}: orthodox_boundary missing {phrase!r}")

    channels = data["evidence_channels"]
    if not isinstance(channels, list) or not channels:
        raise ApocalypticIntertextQueueError(f"{_rel(path)}: evidence_channels must be a non-empty list")
    channel_ids: set[str] = set()
    for channel in channels:
        if not isinstance(channel, dict):
            raise ApocalypticIntertextQueueError(f"{_rel(path)}: each evidence channel must be a mapping")
        channel_id = str(channel.get("channel_id", ""))
        _require_string(channel_id, "evidence_channels.channel_id")
        channel_ids.add(channel_id)
        _require_string(channel.get("use_when"), f"{channel_id}.use_when")
        _require_string(channel.get("non_authorization"), f"{channel_id}.non_authorization")
        _require_evidence_only(channel["non_authorization"], f"{channel_id}.non_authorization")
    missing_channels = sorted(REQUIRED_EVIDENCE_CHANNELS - channel_ids)
    if missing_channels:
        raise ApocalypticIntertextQueueError(f"{_rel(path)}: missing evidence channels {missing_channels}")

    _require_subset(REQUIRED_PACKET_FIELDS, data["required_future_dossier_fields"], "required_future_dossier_fields")
    _require_subset(REQUIRED_GLOBAL_NON_AUTHORIZATIONS, data["global_non_authorizations"], "global_non_authorizations")
    _require_subset(REQUIRED_VALIDATORS, data["validators"], "validators")

    dossiers = data["dossier_queue"]
    if not isinstance(dossiers, list) or not dossiers:
        raise ApocalypticIntertextQueueError(f"{_rel(path)}: dossier_queue must be a non-empty list")
    dossier_ids: set[str] = set()
    priorities: list[int] = []
    for dossier in dossiers:
        if not isinstance(dossier, dict):
            raise ApocalypticIntertextQueueError(f"{_rel(path)}: each dossier must be a mapping")
        missing_fields = sorted(REQUIRED_PACKET_FIELDS - set(dossier))
        dossier_id = str(dossier.get("dossier_id", ""))
        _require_string(dossier_id, "dossier_queue.dossier_id")
        if missing_fields:
            raise ApocalypticIntertextQueueError(f"{dossier_id} missing fields {missing_fields}")
        if dossier_id in dossier_ids:
            raise ApocalypticIntertextQueueError(f"{_rel(path)}: duplicate dossier_id {dossier_id}")
        dossier_ids.add(dossier_id)
        if dossier.get("status") not in ALLOWED_STATUSES:
            raise ApocalypticIntertextQueueError(f"{dossier_id}.status is invalid")
        priority = dossier.get("priority")
        if not isinstance(priority, int):
            raise ApocalypticIntertextQueueError(f"{dossier_id}.priority must be an integer")
        priorities.append(priority)
        _require_string(dossier.get("title"), f"{dossier_id}.title")
        _require_string_list(dossier.get("exact_passage_scope"), f"{dossier_id}.exact_passage_scope")
        _require_string_list(dossier.get("source_passages"), f"{dossier_id}.source_passages")
        _require_string_list(dossier.get("candidate_intertexts"), f"{dossier_id}.candidate_intertexts")
        dossier_channels = set(_require_string_list(dossier.get("evidence_channels"), f"{dossier_id}.evidence_channels"))
        unknown_channels = sorted(dossier_channels - channel_ids)
        if unknown_channels:
            raise ApocalypticIntertextQueueError(f"{dossier_id}.evidence_channels unknown {unknown_channels}")
        if not isinstance(dossier.get("source_metadata_observed"), dict):
            raise ApocalypticIntertextQueueError(f"{dossier_id}.source_metadata_observed must be a mapping")
        _require_string_list(dossier.get("hermeneutic_options_preserved"), f"{dossier_id}.hermeneutic_options_preserved")
        _require_string_list(dossier.get("theological_downstream_risks"), f"{dossier_id}.theological_downstream_risks")
        _require_string_list(dossier.get("assumptions_avoided"), f"{dossier_id}.assumptions_avoided")
        _require_string(dossier.get("reviewed_gold_dependency"), f"{dossier_id}.reviewed_gold_dependency")
        for phrase in ("review", "owner", "chunk", "graph", "retrieval", "route"):
            if phrase not in dossier["reviewed_gold_dependency"].lower():
                raise ApocalypticIntertextQueueError(f"{dossier_id}.reviewed_gold_dependency missing {phrase!r}")
        non_authorizations = set(_require_string_list(dossier.get("non_authorizations"), f"{dossier_id}.non_authorizations"))
        for required in ("chunk_boundary", "reviewed_gold", "output_change"):
            if required not in non_authorizations:
                raise ApocalypticIntertextQueueError(f"{dossier_id}.non_authorizations missing {required}")
    missing_dossiers = sorted(REQUIRED_DOSSIERS - dossier_ids)
    if missing_dossiers:
        raise ApocalypticIntertextQueueError(f"{_rel(path)}: missing dossiers {missing_dossiers}")
    if priorities != sorted(priorities):
        raise ApocalypticIntertextQueueError(f"{_rel(path)}: dossier priorities must be sorted")

    return data


def main() -> int:
    try:
        validate_apocalyptic_prophetic_intertext_dossier_queue()
    except ApocalypticIntertextQueueError as exc:
        print(f"Apocalyptic/prophetic intertext dossier queue validation failed: {exc}", file=sys.stderr)
        return 1
    print("Apocalyptic/prophetic intertext dossier queue validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
