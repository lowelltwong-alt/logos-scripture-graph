#!/usr/bin/env python3
"""Validate the Bible-wide chunking research registry."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / ".ai" / "control" / "bible_wide_chunking_research_registry.yaml"

CANONICAL_66 = [
    "Gen", "Exod", "Lev", "Num", "Deut", "Josh", "Judg", "Ruth", "1Sam", "2Sam",
    "1Kgs", "2Kgs", "1Chr", "2Chr", "Ezra", "Neh", "Esth", "Job", "Ps", "Prov",
    "Eccl", "Song", "Isa", "Jer", "Lam", "Ezek", "Dan", "Hos", "Joel", "Amos",
    "Obad", "Jonah", "Mic", "Nah", "Hab", "Zeph", "Hag", "Zech", "Mal", "Matt",
    "Mark", "Luke", "John", "Acts", "Rom", "1Cor", "2Cor", "Gal", "Eph", "Phil",
    "Col", "1Thess", "2Thess", "1Tim", "2Tim", "Titus", "Phlm", "Heb", "Jas",
    "1Pet", "2Pet", "1John", "2John", "3John", "Jude", "Rev",
]

REQUIRED_TOP_LEVEL = {
    "object_type",
    "trust_zone",
    "lifecycle_status",
    "provenance_note",
    "reason_for_inclusion",
    "schema_version",
    "registry_id",
    "owner",
    "authority",
    "scope",
    "global_non_authorizations",
    "research_dimensions",
    "required_future_research_packet_fields",
    "book_research_queue",
}

REQUIRED_FALSE_AUTHORITY = {
    "authorizes_chunk_output_change",
    "authorizes_new_algorithm_work",
    "authorizes_reviewed_gold_promotion",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_embedding_or_vector_work",
    "authorizes_source_metadata_truth",
    "authorizes_speaker_attribution",
    "authorizes_boundary_import",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "raw_or_canonical_mutation",
    "generated_chunk_regeneration",
    "chunk_output_change",
    "reviewed_gold_promotion",
    "graph_edge_generation",
    "retrieval_truth",
    "embedding_or_vector_work",
    "source_metadata_authority",
    "speaker_attribution",
    "boundary_import",
    "revelation_implementation",
    "epistle_implementation",
    "wj_implementation",
    "t345",
}

REQUIRED_DIMENSIONS = {
    "genre_form_boundary",
    "discourse_argument_flow",
    "narrative_scene_pericope",
    "legal_covenant_formulae",
    "poetry_parallelism_stanza",
    "prophetic_oracle_vision",
    "apocalyptic_symbol_intertext",
    "gospel_discourse_speaker_wj",
    "source_metadata_features",
    "divine_name_title_capitalization",
    "textual_variant_source_tradition",
}

REQUIRED_PACKET_FIELDS = {
    "exact_passage_scope",
    "genre_or_lane",
    "source_metadata_observed",
    "cross_reference_or_intertext_observed",
    "theological_downstream_risks",
    "assumptions_avoided",
    "reviewed_gold_dependency",
    "non_authorizations",
    "validators_or_tests_needed",
}

REQUIRED_BOOK_FIELDS = {
    "book_id",
    "canonical_order",
    "testament",
    "primary_lane",
    "secondary_lanes",
    "research_status",
    "use_when",
    "representative_boundary_questions",
    "theological_downstream_risks",
    "metadata_watchpoints",
    "future_review_packet_candidates",
    "output_change_authorized",
    "implementation_authorized",
    "reviewed_gold_promoted",
}

ALLOWED_STATUSES = {
    "seeded_needs_research",
    "research_first",
    "review_packet_pending",
    "owner_decision_pending",
    "governed_hold_existing_gold",
}


class ResearchRegistryError(ValueError):
    """Raised when the Bible-wide research registry is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ResearchRegistryError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise ResearchRegistryError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_string(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ResearchRegistryError(f"{label} must be a non-empty string")


def _require_string_list(value: Any, label: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not value and not allow_empty):
        raise ResearchRegistryError(f"{label} must be a {'possibly empty ' if allow_empty else ''}list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise ResearchRegistryError(f"{label} must contain only non-empty strings")
    return value


def _require_contains(text: str, needles: tuple[str, ...], label: str) -> None:
    lowered = text.lower()
    missing = [needle for needle in needles if needle.lower() not in lowered]
    if missing:
        raise ResearchRegistryError(f"{label} missing required phrase(s): {missing}")


def validate_research_registry(path: Path = REGISTRY) -> dict[str, Any]:
    data = _read_yaml(path)
    missing_top = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing_top:
        raise ResearchRegistryError(f"{_rel(path)}: missing top-level keys {missing_top}")

    if data["object_type"] != "bible_wide_chunking_research_registry":
        raise ResearchRegistryError(f"{_rel(path)}: object_type must be bible_wide_chunking_research_registry")
    if data["trust_zone"] != "canonical":
        raise ResearchRegistryError(f"{_rel(path)}: trust_zone must be canonical")
    if data["lifecycle_status"] != "active":
        raise ResearchRegistryError(f"{_rel(path)}: lifecycle_status must be active")
    if data["schema_version"] != "bible_wide_chunking_research_registry.v1":
        raise ResearchRegistryError(f"{_rel(path)}: schema_version must be bible_wide_chunking_research_registry.v1")

    authority = data["authority"]
    if not isinstance(authority, dict):
        raise ResearchRegistryError(f"{_rel(path)}: authority must be a mapping")
    if authority.get("records_research_queue") is not True:
        raise ResearchRegistryError(f"{_rel(path)}: authority.records_research_queue must be true")
    if authority.get("records_book_level_watchpoints") is not True:
        raise ResearchRegistryError(f"{_rel(path)}: authority.records_book_level_watchpoints must be true")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise ResearchRegistryError(f"{_rel(path)}: authority.{key} must be false")

    scope = data["scope"]
    if not isinstance(scope, dict):
        raise ResearchRegistryError(f"{_rel(path)}: scope must be a mapping")
    if scope.get("corpus_scope") != "canonical_66":
        raise ResearchRegistryError(f"{_rel(path)}: scope.corpus_scope must be canonical_66")
    if scope.get("book_count") != 66:
        raise ResearchRegistryError(f"{_rel(path)}: scope.book_count must be 66")
    if scope.get("research_mode") != "non_output_changing":
        raise ResearchRegistryError(f"{_rel(path)}: scope.research_mode must be non_output_changing")
    _require_contains(
        str(scope.get("relationship_to_t356", "")),
        ("parallel", "does not select", "does not supersede"),
        "scope.relationship_to_t356",
    )

    non_authorizations = set(_require_string_list(data["global_non_authorizations"], "global_non_authorizations"))
    missing_non_authorizations = sorted(REQUIRED_NON_AUTHORIZATIONS - non_authorizations)
    if missing_non_authorizations:
        raise ResearchRegistryError(f"{_rel(path)}: global_non_authorizations missing {missing_non_authorizations}")

    dimensions = data["research_dimensions"]
    if not isinstance(dimensions, list) or not dimensions:
        raise ResearchRegistryError(f"{_rel(path)}: research_dimensions must be a non-empty list")
    dimension_ids: set[str] = set()
    for dimension in dimensions:
        if not isinstance(dimension, dict):
            raise ResearchRegistryError(f"{_rel(path)}: each research dimension must be a mapping")
        dimension_id = str(dimension.get("dimension_id", ""))
        _require_string(dimension_id, "research_dimensions.dimension_id")
        dimension_ids.add(dimension_id)
        _require_string_list(dimension.get("tags"), f"research_dimensions.{dimension_id}.tags")
        _require_string(dimension.get("use_when"), f"research_dimensions.{dimension_id}.use_when")
        _require_string(dimension.get("non_authorization"), f"research_dimensions.{dimension_id}.non_authorization")
        non_authorization = dimension["non_authorization"].lower()
        has_negative_authority = (
            "evidence only" in non_authorization
            or ("not" in non_authorization and any(term in non_authorization for term in ("author", "automatic")))
            or (any(term in non_authorization for term in ("require", "requires", "before")) and "reviewed" in non_authorization)
        )
        if not has_negative_authority:
            raise ResearchRegistryError(
                f"research_dimensions.{dimension_id}.non_authorization must explicitly negate authority"
            )
        if dimension_id == "source_metadata_features":
            if dimension.get("companion_atlas") != ".ai/control/source_metadata_research_atlas.yaml":
                raise ResearchRegistryError(
                    "research_dimensions.source_metadata_features.companion_atlas must point to source metadata atlas"
                )
        if dimension_id == "discourse_argument_flow":
            if dimension.get("companion_dossier_queue") != ".ai/control/epistle_argument_theological_issue_dossier_queue.yaml":
                raise ResearchRegistryError(
                    "research_dimensions.discourse_argument_flow.companion_dossier_queue must point to epistle issue queue"
                )
        if dimension_id in {"narrative_scene_pericope", "legal_covenant_formulae"}:
            if dimension.get("companion_dossier_queue") != ".ai/control/narrative_legal_covenant_dossier_queue.yaml":
                raise ResearchRegistryError(
                    f"research_dimensions.{dimension_id}.companion_dossier_queue must point to narrative/legal queue"
                )
        if dimension_id == "poetry_parallelism_stanza":
            if dimension.get("companion_dossier_queue") != ".ai/control/wisdom_dialogue_poetry_dossier_queue.yaml":
                raise ResearchRegistryError(
                    "research_dimensions.poetry_parallelism_stanza.companion_dossier_queue must point to wisdom/dialogue/poetry queue"
                )
        if dimension_id in {"prophetic_oracle_vision", "apocalyptic_symbol_intertext"}:
            if dimension.get("companion_dossier_queue") != ".ai/control/apocalyptic_prophetic_intertext_dossier_queue.yaml":
                raise ResearchRegistryError(
                    f"research_dimensions.{dimension_id}.companion_dossier_queue must point to apocalyptic/prophetic queue"
                )
        if dimension_id == "prophetic_oracle_vision":
            if dimension.get("companion_oracle_dossier_queue") != ".ai/control/prophetic_oracle_vision_dossier_queue.yaml":
                raise ResearchRegistryError(
                    "research_dimensions.prophetic_oracle_vision.companion_oracle_dossier_queue must point to prophetic/oracle/vision queue"
                )
        if dimension_id == "gospel_discourse_speaker_wj":
            if dimension.get("companion_dossier_queue") != ".ai/control/gospel_wj_discourse_dossier_queue.yaml":
                raise ResearchRegistryError(
                    "research_dimensions.gospel_discourse_speaker_wj.companion_dossier_queue must point to Gospel/WJ queue"
                )
        if dimension_id == "textual_variant_source_tradition":
            if dimension.get("companion_dossier_queue") != ".ai/control/textual_variant_source_tradition_dossier_queue.yaml":
                raise ResearchRegistryError(
                    "research_dimensions.textual_variant_source_tradition.companion_dossier_queue must point to textual-variant/source-tradition queue"
                )
    missing_dimensions = sorted(REQUIRED_DIMENSIONS - dimension_ids)
    if missing_dimensions:
        raise ResearchRegistryError(f"{_rel(path)}: missing research dimensions {missing_dimensions}")

    packet_fields = set(_require_string_list(data["required_future_research_packet_fields"], "required_future_research_packet_fields"))
    missing_packet_fields = sorted(REQUIRED_PACKET_FIELDS - packet_fields)
    if missing_packet_fields:
        raise ResearchRegistryError(
            f"{_rel(path)}: required_future_research_packet_fields missing {missing_packet_fields}"
        )

    queue = data["book_research_queue"]
    if not isinstance(queue, list):
        raise ResearchRegistryError(f"{_rel(path)}: book_research_queue must be a list")
    if len(queue) != 66:
        raise ResearchRegistryError(f"{_rel(path)}: book_research_queue must contain 66 books")
    by_book: dict[str, dict[str, Any]] = {}
    orders: list[int] = []
    for entry in queue:
        if not isinstance(entry, dict):
            raise ResearchRegistryError(f"{_rel(path)}: each book entry must be a mapping")
        missing = sorted(REQUIRED_BOOK_FIELDS - set(entry))
        book_id = str(entry.get("book_id", "<missing>"))
        if missing:
            raise ResearchRegistryError(f"{_rel(path)}:{book_id}: missing keys {missing}")
        if book_id in by_book:
            raise ResearchRegistryError(f"{_rel(path)}:{book_id}: duplicate book_id")
        by_book[book_id] = entry
        order = entry["canonical_order"]
        if not isinstance(order, int):
            raise ResearchRegistryError(f"{_rel(path)}:{book_id}: canonical_order must be an integer")
        orders.append(order)
        if entry["research_status"] not in ALLOWED_STATUSES:
            raise ResearchRegistryError(f"{_rel(path)}:{book_id}: invalid research_status {entry['research_status']!r}")
        if entry["testament"] not in {"OT", "NT"}:
            raise ResearchRegistryError(f"{_rel(path)}:{book_id}: testament must be OT or NT")
        _require_string(entry["primary_lane"], f"{book_id}.primary_lane")
        _require_string(entry["use_when"], f"{book_id}.use_when")
        for key in (
            "secondary_lanes",
            "representative_boundary_questions",
            "theological_downstream_risks",
            "metadata_watchpoints",
            "future_review_packet_candidates",
        ):
            _require_string_list(entry[key], f"{book_id}.{key}")
        for key in ("output_change_authorized", "implementation_authorized", "reviewed_gold_promoted"):
            if entry[key] is not False:
                raise ResearchRegistryError(f"{_rel(path)}:{book_id}: {key} must be false")

    if list(by_book) != CANONICAL_66:
        raise ResearchRegistryError(f"{_rel(path)}: book order must match canonical 66")
    if orders != list(range(1, 67)):
        raise ResearchRegistryError(f"{_rel(path)}: canonical_order values must be 1..66")

    required_sensitive_checks = {
        "John": ("wj", "narrator", "speaker", "christology"),
        "Rev": ("futurist", "preterist", "historicist", "idealist", "premillennial", "amillennial"),
        "Dan": ("apocalyptic", "futurist", "historicist", "preterist", "idealist"),
        "Ps": ("existing reviewed", "messianic", "lament"),
        "Rom": ("calvinist", "arminian", "soteriology"),
        "Song": ("allegorical", "speaker"),
        "Jude": ("noncanonical", "boundary"),
    }
    for book_id, phrases in required_sensitive_checks.items():
        text = " ".join(
            str(value)
            for key, value in by_book[book_id].items()
            if isinstance(value, (str, list))
        )
        _require_contains(text, phrases, f"{book_id} sensitive research entry")

    return data


def main() -> int:
    try:
        validate_research_registry()
    except ResearchRegistryError as exc:
        print(f"Bible-wide chunking research registry validation failed: {exc}", file=sys.stderr)
        return 1
    print("Bible-wide chunking research registry validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
