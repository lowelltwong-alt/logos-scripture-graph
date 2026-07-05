#!/usr/bin/env python3
"""Validate the T451 Bible edge candidate-type catalog."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTROL = ROOT / ".ai" / "control" / "bible_edge_candidate_type_catalog.yaml"
PREDICATE_REGISTRY = ROOT / "config" / "governance" / "predicate_registry.yaml"
T450_CONTROL = ROOT / ".ai" / "control" / "bible_edge_taxonomy_research_program.yaml"
ROADMAP = ROOT / "docs" / "roadmap" / "T451_BIBLE_EDGE_CANDIDATE_TYPE_CATALOG.md"
MODEL_PROMPT = ROOT / ".ai" / "prompts" / "bible_edge_taxonomy_model_review_prompt.md"
FRONTIER_PROMPT = ROOT / ".ai" / "prompts" / "bible_edge_taxonomy_frontier_audit_prompt.md"
HANDOFF = ROOT / ".ai" / "handoffs" / "T451" / "handoff.md"
DAD_CONTEXT = ROOT / ".digital-asset" / "context-map.json"
DAD_LESSON = ROOT / ".digital-asset" / "lessons" / "t451_bible_edge_candidate_type_catalog.yaml"
DAD_OUTBOX = ROOT / ".digital-asset" / "mail" / "outbox.jsonl"

REQUIRED_FAMILIES = {
    "structural_source_occurrence",
    "editorial_metadata",
    "textual_intertextual",
    "covenant_law_sacrifice_calendar",
    "prophecy_apocalyptic_typology",
    "orthodox_creedal_doctrinal",
    "historical_geographic",
    "literary_discourse_genre",
    "linguistic_original_language",
    "textual_criticism_manuscript",
    "apologetic_polemic",
    "pastoral_doctrinal",
}

REQUIRED_EDGE_TYPES = {
    "explicit_quotation_candidate",
    "allusion_or_echo_candidate",
    "ot_in_nt_usage_candidate",
    "covenant_formula_evidence",
    "law_code_unit_evidence",
    "sacrifice_offering_type_evidence",
    "feast_calendar_worship_unit",
    "priesthood_temple_sanctuary_role",
    "oracle_formula_evidence",
    "vision_sequence_evidence",
    "fulfillment_claim_candidate",
    "typology_candidate",
    "messianic_sensitive_language",
    "divine_title_watchpoint",
    "christological_pressure_passage",
    "trinitarian_relation_pressure",
    "creedal_boundary_guard",
    "historical_context_evidence",
    "place_name_occurrence_observed",
    "site_or_route_identification_candidate",
    "regnal_or_genealogical_chronology_evidence",
    "person_kinship_office_role_evidence",
    "narrative_scene_unit",
    "speech_dialogue_frame",
    "epistle_argument_flow",
    "poetic_parallelism_unit",
    "wj_discourse_evidence",
    "lemma_morphology_evidence",
    "phrase_clause_syntax_evidence",
    "translation_divergence_pressure",
    "lxx_hebrew_nt_relation",
    "root_or_semantic_range_warning",
    "variant_marker_evidence",
    "source_tradition_difference",
    "variant_sensitive_block",
    "manuscript_witness_metadata",
    "attestation_candidate",
    "apologetic_pressure_label",
    "polemic_against_false_worship_candidate",
    "reliability_claim_candidate",
    "translation_polemics_watchpoint",
    "early_creedal_pattern_candidate",
    "pastoral_theme_candidate",
    "doctrinal_risk_tag",
    "orthodox_options_preserved",
}

AUTHORITY_FALSE_KEYS = {
    "expands_predicate_registry",
    "registers_predicates",
    "generates_graph_edges",
    "creates_candidate_edge_rows",
    "creates_reviewed_semantic_edges",
    "creates_retrieval_truth",
    "creates_vector_truth",
    "runs_embeddings_or_builds_indexes",
    "imports_boundary_material",
    "changes_chunk_output",
    "promotes_reviewed_gold",
    "changes_route_or_evaluator_behavior",
    "selects_preferred_reading_or_source_tradition",
    "selects_canon_scope",
    "selects_theological_system",
    "authorizes_theology_authority",
    "authorizes_apologetic_or_polemic_conclusion",
}

GLOBAL_NEVER_AUTO = {
    "graph_edge_generation",
    "predicate_registry_expansion",
    "theology_authority",
    "retrieval_truth",
    "vector_truth",
    "chunk_boundary",
    "reviewed_gold",
    "source_tradition_preference",
    "canon_scope_change",
    "apologetic_conclusion_as_truth",
}

FRONTIER_FAMILIES = {
    "prophecy_apocalyptic_typology",
    "orthodox_creedal_doctrinal",
    "linguistic_original_language",
    "textual_criticism_manuscript",
    "apologetic_polemic",
}

AUTHORITY_DENIAL_TERMS = (
    "authority",
    "truth",
    "claim",
    "preference",
    "conclusion",
    "graph",
    "retrieval",
    "vector",
    "chunk",
    "reviewed",
    "boundary",
    "theology",
    "doctrine",
    "system_selection",
    "preferred",
    "source_tradition",
    "canon",
    "proof",
    "caricature",
    "refutation",
)

REQUIRED_PROMPT_PHRASES = {
    "Do not",
    "expand the predicate registry",
    "generate graph edges",
    "decide theology",
}


class T451CatalogError(ValueError):
    """Raised when the T451 catalog contract is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise T451CatalogError(f"{_rel(path)} is missing")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise T451CatalogError(f"{_rel(path)} is invalid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise T451CatalogError(f"{_rel(path)} must be a YAML mapping")
    return data


def _string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise T451CatalogError(f"{label} must be a non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise T451CatalogError(f"{label} must contain only non-empty strings")
    return [str(item) for item in value]


def validate_catalog(data: dict[str, Any]) -> dict[str, Any]:
    if data.get("schema_version") != "bible_edge_candidate_type_catalog.v1":
        raise T451CatalogError("schema_version must be bible_edge_candidate_type_catalog.v1")
    if data.get("object_type") != "bible_edge_candidate_type_catalog":
        raise T451CatalogError("object_type must be bible_edge_candidate_type_catalog")
    if data.get("task_id") != "T451":
        raise T451CatalogError("task_id must be T451")
    if data.get("planning_only") is not True or data.get("non_authorizing") is not True:
        raise T451CatalogError("catalog must be planning_only and non_authorizing")

    registry_snapshot = data.get("current_registered_predicates")
    if not isinstance(registry_snapshot, dict):
        raise T451CatalogError("current_registered_predicates must be a mapping")
    if registry_snapshot.get("registry_path") != _rel(PREDICATE_REGISTRY):
        raise T451CatalogError("current_registered_predicates.registry_path must point to the predicate registry")
    registry = _read_yaml(PREDICATE_REGISTRY)
    registry_predicates = registry.get("predicates")
    if not isinstance(registry_predicates, dict) or not registry_predicates:
        raise T451CatalogError("predicate registry must define predicates")
    registered_names = set(registry_predicates)
    snapshot_names = set(_string_list(registry_snapshot.get("predicates"), "current_registered_predicates.predicates"))
    missing_snapshot = sorted(registered_names - snapshot_names)
    extra_snapshot = sorted(snapshot_names - registered_names)
    if missing_snapshot or extra_snapshot:
        raise T451CatalogError(
            "current_registered_predicates.predicates must match "
            f"{_rel(PREDICATE_REGISTRY)}; missing={missing_snapshot}, extra={extra_snapshot}"
        )

    boundary = data.get("authority_boundary")
    if not isinstance(boundary, dict):
        raise T451CatalogError("authority_boundary must be a mapping")
    for key in AUTHORITY_FALSE_KEYS:
        if boundary.get(key) is not False:
            raise T451CatalogError(f"authority_boundary.{key} must be false")

    floor = data.get("global_evidence_floor")
    if not isinstance(floor, dict):
        raise T451CatalogError("global_evidence_floor must be a mapping")
    never_auto = set(_string_list(floor.get("universal_never_auto_create"), "global_evidence_floor.universal_never_auto_create"))
    missing_never = sorted(GLOBAL_NEVER_AUTO - never_auto)
    if missing_never:
        raise T451CatalogError(f"global never-auto-create list missing {missing_never}")
    evidence_only = "\n".join(_string_list(floor.get("evidence_only_inputs"), "global_evidence_floor.evidence_only_inputs"))
    for term in ("Strong's numbers", "WJ/red-letter", "editorial cross-references", "manuscript", "model agreement"):
        if term not in evidence_only:
            raise T451CatalogError(f"evidence_only_inputs missing {term!r}")

    families = data.get("candidate_edge_families")
    if not isinstance(families, list) or not families:
        raise T451CatalogError("candidate_edge_families must be a non-empty list")
    family_ids = {family.get("family_id") for family in families if isinstance(family, dict)}
    missing_families = sorted(REQUIRED_FAMILIES - family_ids)
    if missing_families:
        raise T451CatalogError(f"missing family ids: {missing_families}")

    escalation = data.get("frontier_escalation_required_for")
    if not isinstance(escalation, dict):
        raise T451CatalogError("frontier_escalation_required_for must be a mapping")
    frontier_families = set(_string_list(escalation.get("families"), "frontier_escalation_required_for.families"))
    missing_frontier = sorted(FRONTIER_FAMILIES - frontier_families)
    if missing_frontier:
        raise T451CatalogError(f"frontier escalation families missing {missing_frontier}")
    triggers = "\n".join(_string_list(escalation.get("triggers"), "frontier_escalation_required_for.triggers"))
    for trigger in ("WJ_or_speaker_boundary", "Christology_or_Trinity_pressure", "textual_variant_or_source_tradition_pressure", "original_language_claim_controls_meaning"):
        if trigger not in triggers:
            raise T451CatalogError(f"frontier escalation triggers missing {trigger}")

    edge_types = data.get("candidate_edge_types")
    if not isinstance(edge_types, list) or len(edge_types) < 40:
        raise T451CatalogError("candidate_edge_types must contain at least 40 entries")
    edge_ids = {edge.get("edge_type_id") for edge in edge_types if isinstance(edge, dict)}
    missing_edges = sorted(REQUIRED_EDGE_TYPES - edge_ids)
    if missing_edges:
        raise T451CatalogError(f"missing required edge type ids: {missing_edges}")

    for index, edge in enumerate(edge_types, start=1):
        if not isinstance(edge, dict):
            raise T451CatalogError(f"candidate_edge_types[{index}] must be a mapping")
        edge_id = edge.get("edge_type_id")
        for key in (
            "family_id",
            "label",
            "candidate_status",
            "default_assertion_path",
            "intended_future_predicate",
            "description",
            "evidence_channels",
            "evidence_floor",
            "escalation_triggers",
            "never_auto_create",
        ):
            if key not in edge:
                raise T451CatalogError(f"{edge_id} missing {key}")
        if edge["family_id"] not in family_ids:
            raise T451CatalogError(f"{edge_id} references unknown family {edge['family_id']}")
        if edge["candidate_status"] != "candidate_type_only":
            raise T451CatalogError(f"{edge_id} must remain candidate_type_only")
        if edge["default_assertion_path"] not in {"structural_deterministic", "reviewed_semantic", "model_inferred_candidate"}:
            raise T451CatalogError(f"{edge_id} has invalid default_assertion_path")
        _string_list(edge["evidence_channels"], f"{edge_id}.evidence_channels")
        _string_list(edge["evidence_floor"], f"{edge_id}.evidence_floor")
        _string_list(edge["escalation_triggers"], f"{edge_id}.escalation_triggers")
        edge_never = set(_string_list(edge["never_auto_create"], f"{edge_id}.never_auto_create"))
        if not edge_never:
            raise T451CatalogError(f"{edge_id}.never_auto_create must not be empty")
        denies_authority_leakage = any(
            any(term in item for term in AUTHORITY_DENIAL_TERMS)
            for item in edge_never
        )
        if not denies_authority_leakage:
            raise T451CatalogError(f"{edge_id} must explicitly deny authority leakage")

    future = data.get("future_work_queue")
    if not isinstance(future, list) or not future:
        raise T451CatalogError("future_work_queue must be a non-empty list")
    future_ids = {entry.get("task_id") for entry in future if isinstance(entry, dict)}
    for task_id in ("T452", "T453", "T454", "T455"):
        if task_id not in future_ids:
            raise T451CatalogError(f"future_work_queue missing {task_id}")

    dad = data.get("dad_coordination")
    if not isinstance(dad, dict):
        raise T451CatalogError("dad_coordination must be a mapping")
    for key in ("context_map_entry", "outbox_message_id", "lesson_learned_slot"):
        if not isinstance(dad.get(key), str) or not dad[key].strip():
            raise T451CatalogError(f"dad_coordination.{key} must be a non-empty string")

    return data


def validate_text_surfaces() -> None:
    for path in (T450_CONTROL, ROADMAP, MODEL_PROMPT, FRONTIER_PROMPT, HANDOFF):
        if not path.exists():
            raise T451CatalogError(f"{_rel(path)} is missing")
    for path in (ROADMAP, MODEL_PROMPT, FRONTIER_PROMPT):
        text = path.read_text(encoding="utf-8")
        for phrase in REQUIRED_PROMPT_PHRASES if path.name.endswith("_prompt.md") else ("planning-only", "predicate", "graph", "theology"):
            if phrase not in text:
                raise T451CatalogError(f"{_rel(path)} missing required phrase {phrase!r}")


def validate_dad_surfaces(data: dict[str, Any]) -> None:
    dad = data["dad_coordination"]
    for path in (DAD_CONTEXT, DAD_LESSON, DAD_OUTBOX):
        if not path.exists():
            raise T451CatalogError(f"{_rel(path)} is missing")
    context_text = DAD_CONTEXT.read_text(encoding="utf-8")
    lesson_text = DAD_LESSON.read_text(encoding="utf-8")
    outbox_text = DAD_OUTBOX.read_text(encoding="utf-8")
    for value in (dad["context_map_entry"], dad["outbox_message_id"], dad["lesson_learned_slot"]):
        if value not in f"{context_text}\n{lesson_text}\n{outbox_text}":
            raise T451CatalogError(f"DAD coordination value {value!r} not found in DAD surfaces")


def validate_t451_catalog(path: Path = CONTROL) -> dict[str, Any]:
    data = validate_catalog(_read_yaml(path))
    validate_text_surfaces()
    validate_dad_surfaces(data)
    return data


def main() -> int:
    try:
        data = validate_t451_catalog()
    except T451CatalogError as exc:
        print(f"T451 Bible edge candidate-type catalog validation failed: {exc}", file=sys.stderr)
        return 1
    print(f"T451 Bible edge candidate-type catalog OK ({len(data['candidate_edge_types'])} candidate edge types).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
