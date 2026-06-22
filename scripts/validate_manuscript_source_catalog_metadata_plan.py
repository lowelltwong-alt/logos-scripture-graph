#!/usr/bin/env python3
"""Validate the T390 manuscript source catalog metadata plan."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / ".ai" / "control" / "manuscript_source_catalog_metadata_plan.yaml"
ROADMAP_DOC = ROOT / "docs" / "roadmap" / "T390_MANUSCRIPT_SOURCE_CATALOG_METADATA_PLAN.md"
TASK = ROOT / ".ai" / "tasks" / "T390.task.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T390" / "handoff.md"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
MAIN_TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"
ROADMAP_STATE = ROOT / "ROADMAP_STATE.yaml"
VALIDATE_ALL = ROOT / "scripts" / "validate_all.py"

REQUIRED_TABLES = {
    "scripture_source_catalog",
    "scripture_holding_institution",
    "scripture_catalog_witness_record",
    "scripture_witness_identifier",
    "scripture_witness_date_claim",
    "scripture_witness_material_claim",
    "scripture_witness_coverage_claim",
    "scripture_witness_discovery_event",
    "evidence_source_catalog_method_profile",
    "evidence_source_trust_rule",
    "evidence_catalog_review_queue",
}

REQUIRED_FALSE_AUTHORITY = {
    "authorizes_sqlite_database_creation",
    "authorizes_metadata_row_population",
    "authorizes_source_text_import",
    "authorizes_transcription_storage",
    "authorizes_canonical_bible_text_change",
    "authorizes_canonical_passage_record_change",
    "authorizes_chunk_output_change",
    "authorizes_reviewed_gold_promotion",
    "authorizes_textual_critical_decision",
    "authorizes_preferred_reading",
    "authorizes_source_tradition_preference",
    "authorizes_canon_scope_change",
    "authorizes_boundary_import",
    "authorizes_commentary_or_patristic_import",
    "authorizes_doctrine_genealogy_import",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_embedding_or_vector_work",
    "authorizes_doctrinal_system",
    "authorizes_apologetic_conclusion_as_truth",
}

REQUIRED_SOURCE_FAMILIES = {
    "dss_biblical_witness_catalogs",
    "nt_manuscript_catalogs",
    "major_codex_project_catalogs",
    "holding_institution_catalogs",
    "critical_apparatus_method_profiles",
}

REQUIRED_SOURCE_ANCHORS = {
    "iaa_leon_levy_dss_digital_library",
    "iaa_dss_archive_browser",
    "iaa_dss_discovery_publication",
    "iaa_dss_content_categories",
    "israel_museum_great_isaiah_scroll",
    "intf_ntvmr",
    "intf_liste",
    "csntm_manuscripts_catalog",
    "csntm_p52",
    "manchester_rylands_p52",
    "codex_sinaiticus_project",
    "vatican_library_codex_vaticanus",
    "british_library_codex_alexandrinus",
}

REQUIRED_TRUST_RULES = {
    "official_holding_institution_over_secondary",
    "catalog_identifier_required",
    "date_range_not_point_date",
    "coverage_claim_requires_source_scope",
    "conflicting_catalog_claims_preserved",
    "no_transcription_text",
    "no_preferred_reading_from_catalog",
    "rights_status_before_ingest",
    "biblical_dss_only_in_scripture_graph",
}

REQUIRED_REVIEW_STATUSES = {
    "unreviewed_candidate",
    "source_catalog_located",
    "holding_institution_confirmed",
    "rights_reviewed",
    "metadata_reviewed",
    "method_reviewed",
    "owner_review_required",
    "deprecated",
}

REQUIRED_GOAL_IDS = {
    "T391_DSS_BIBLICAL_SOURCE_CATALOG_POPULATION",
    "T392_NT_PAPYRI_AND_MAJOR_CODICES_SOURCE_CATALOG_POPULATION",
    "T393_VARIANT_AND_COPY_ABUNDANCE_METHOD_PROFILE",
    "T394_DISCOVERY_TIMELINE_WHAT_WAS_KNOWN_WHEN",
    "BOUNDARY_PATRISTIC_RECEPTION_RECONSTRUCTION",
    "DOCTRINE_GENEALOGY_THEOLOGIAN_LINEAGE",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "sqlite_database_creation",
    "metadata_row_population",
    "source_text_import",
    "transcription_storage",
    "canonical_bible_text_change",
    "canonical_passage_record_change",
    "canonical_chunk_change",
    "reviewed_gold_promotion",
    "textual_critical_decision",
    "preferred_reading_selection",
    "source_tradition_preference",
    "canon_scope_change",
    "boundary_import",
    "commentary_or_patristic_import",
    "doctrine_genealogy_import",
    "commentary_as_scripture",
    "patristic_citation_as_scripture_authority",
    "graph_edge_generation",
    "retrieval_truth",
    "embedding_or_vector_work",
    "apologetic_conclusion_as_truth",
}

REQUIRED_WIRING = {
    FRONT_DOOR: [
        "manuscript_source_catalog_metadata_plan.yaml",
        "T390 manuscript source catalog metadata plan",
    ],
    MAIN_TOC: [
        "source-catalog",
        "manuscript_source_catalog_metadata_plan.yaml",
        "T390_MANUSCRIPT_SOURCE_CATALOG_METADATA_PLAN.md",
    ],
    ROADMAP_TOC: [
        "T390 | Manuscript source catalog metadata plan",
        "source-catalog",
        "scripts/validate_manuscript_source_catalog_metadata_plan.py",
    ],
    ROADMAP_STATE: [
        "T390",
        "Manuscript Source Catalog Metadata Plan",
        "manuscript_source_catalog_metadata_plan.yaml",
    ],
    VALIDATE_ALL: ["validate_manuscript_source_catalog_metadata_plan.py"],
}


class ManuscriptSourceCatalogPlanError(ValueError):
    """Raised when the T390 plan is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ManuscriptSourceCatalogPlanError(f"{_rel(path)}: unreadable: {exc}") from exc


def _strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            return parts[1] + "\n" + parts[2]
    return text


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(_strip_frontmatter(_read_text(path)))
    except yaml.YAMLError as exc:
        raise ManuscriptSourceCatalogPlanError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise ManuscriptSourceCatalogPlanError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ManuscriptSourceCatalogPlanError(f"{label} must be a mapping")
    return value


def _require_string_list(value: Any, label: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not value and not allow_empty):
        raise ManuscriptSourceCatalogPlanError(
            f"{label} must be a {'possibly empty ' if allow_empty else ''}list"
        )
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise ManuscriptSourceCatalogPlanError(f"{label} must contain only non-empty strings")
    return [str(item) for item in value]


def _validate_metadata(data: dict[str, Any]) -> None:
    expected = {
        "object_type": "manuscript_source_catalog_metadata_plan",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "manuscript_source_catalog_metadata_plan.v1",
        "plan_id": "t390_manuscript_source_catalog_metadata_plan",
        "task_id": "T390",
        "status": "active_planning_only",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}: {key} must be {value!r}")
    for key in ("provenance_note", "reason_for_inclusion"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}: {key} must be a non-empty string")


def _validate_authority(data: dict[str, Any]) -> None:
    authority = _require_mapping(data.get("authority"), f"{_rel(PLAN)}: authority")
    for key in (
        "records_source_catalog_metadata_plan",
        "refines_t387_scaffold",
        "may_define_sqlite_table_candidates",
        "may_define_source_trust_rules",
        "may_define_future_population_goals",
    ):
        if authority.get(key) is not True:
            raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}: authority.{key} must be true")
    missing = sorted(REQUIRED_FALSE_AUTHORITY - set(authority))
    if missing:
        raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}: authority missing {missing}")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}: authority.{key} must be false")


def _validate_placement_and_boundary(data: dict[str, Any]) -> None:
    placement = _require_mapping(data.get("placement_decision"), f"{_rel(PLAN)}: placement_decision")
    if placement.get("owning_repo") != "logos-scripture-graph":
        raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}: owning_repo must be logos-scripture-graph")
    for key, needle in (
        ("boundary_repo_scope", "logos-boundary-literature"),
        ("doctrine_repo_scope", "logos-doctrine-genealogy"),
        ("governance_repo_scope", "logos-governance-architecture"),
    ):
        if needle not in str(placement.get(key, "")):
            raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}: {key} must mention {needle}")
    split_rule = str(placement.get("split_rule", "")).lower()
    for phrase in ("commentary", "patristic", "theologian", "non-biblical qumran", "scripture graph"):
        if phrase not in split_rule:
            raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}: split_rule missing {phrase!r}")

    boundary = _require_mapping(data.get("data_boundary"), f"{_rel(PLAN)}: data_boundary")
    if set(_require_string_list(boundary.get("allowed_prefixes"), "allowed_prefixes")) != {"scripture_", "evidence_"}:
        raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}: allowed prefixes must be scripture_ and evidence_")
    forbidden = set(_require_string_list(boundary.get("forbidden_prefixes"), "forbidden_prefixes"))
    if not {"canonical_", "boundary_", "doctrine_"} <= forbidden:
        raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}: canonical_, boundary_, and doctrine_ prefixes must be forbidden")
    if "Never create a canonical_* table or view" not in str(boundary.get("forbidden_table_or_view_rule", "")):
        raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}: forbidden_table_or_view_rule must forbid canonical_*")


def _validate_sqlite_entity_plan(data: dict[str, Any]) -> None:
    entity_plan = _require_mapping(data.get("sqlite_entity_plan"), f"{_rel(PLAN)}: sqlite_entity_plan")
    tables = entity_plan.get("tables")
    if not isinstance(tables, list) or not tables:
        raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}: sqlite_entity_plan.tables must be a non-empty list")
    table_names = {item.get("table_name") for item in tables if isinstance(item, dict)}
    if table_names != REQUIRED_TABLES:
        raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}: tables must be {sorted(REQUIRED_TABLES)}")
    for table in tables:
        if not isinstance(table, dict):
            raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}: each table must be a mapping")
        name = str(table.get("table_name"))
        if not (name.startswith("scripture_") or name.startswith("evidence_")):
            raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}:{name}: table must use scripture_ or evidence_")
        if name.startswith("canonical_"):
            raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}:{name}: forbidden canonical_ table")
        for flag in ("stores_scripture_text", "stores_transcription_text", "stores_boundary_text"):
            if table.get(flag) is not False:
                raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}:{name}: {flag} must be false")
        required_fields = _require_string_list(table.get("required_fields"), f"{name}.required_fields")
        fields = set(required_fields)
        for required in ("source_url", "provenance_note", "confidence", "review_status"):
            if required not in fields:
                raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}:{name}: required_fields missing {required}")


def _validate_source_families_and_anchors(data: dict[str, Any]) -> None:
    families = data.get("source_families")
    if not isinstance(families, list) or not families:
        raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}: source_families must be a non-empty list")
    family_ids = {item.get("family_id") for item in families if isinstance(item, dict)}
    if family_ids != REQUIRED_SOURCE_FAMILIES:
        raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}: source_families must be {sorted(REQUIRED_SOURCE_FAMILIES)}")
    for family in families:
        if not isinstance(family, dict):
            raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}: each source family must be a mapping")
        if family.get("correct_repo") != "logos-scripture-graph":
            raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}:{family.get('family_id')}: correct_repo must be Scripture Graph")
        for key in ("allowed_scope", "routes_elsewhere"):
            if not isinstance(family.get(key), str) or not family[key].strip():
                raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}:{family.get('family_id')}: {key} required")

    anchors = data.get("source_anchors")
    if not isinstance(anchors, list) or not anchors:
        raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}: source_anchors must be a non-empty list")
    anchor_ids = {item.get("anchor_id") for item in anchors if isinstance(item, dict)}
    if anchor_ids != REQUIRED_SOURCE_ANCHORS:
        raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}: source_anchors must be {sorted(REQUIRED_SOURCE_ANCHORS)}")
    for anchor in anchors:
        if not isinstance(anchor, dict):
            raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}: each source anchor must be a mapping")
        label = str(anchor.get("anchor_id"))
        if anchor.get("source_family") not in REQUIRED_SOURCE_FAMILIES:
            raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}:{label}: invalid source_family")
        for key in ("source_url", "source_type", "confirmed_metadata_use", "plan_use", "not_authorized"):
            if not isinstance(anchor.get(key), str) or not anchor[key].strip():
                raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}:{label}: {key} must be a non-empty string")
        if not anchor["source_url"].startswith("https://"):
            raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}:{label}: source_url must be https")


def _validate_trust_and_anti_guessing(data: dict[str, Any]) -> None:
    rules = data.get("source_trust_rules")
    if not isinstance(rules, list) or not rules:
        raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}: source_trust_rules must be a non-empty list")
    rule_ids = {item.get("rule_id") for item in rules if isinstance(item, dict)}
    if rule_ids != REQUIRED_TRUST_RULES:
        raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}: source_trust_rules must be {sorted(REQUIRED_TRUST_RULES)}")
    for rule in rules:
        if not isinstance(rule.get("rule"), str) or not rule["rule"].strip():
            raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}:{rule.get('rule_id')}: rule must be a non-empty string")

    controls = _require_string_list(data.get("anti_guessing_rules"), "anti_guessing_rules")
    joined = "\n".join(controls).lower()
    for phrase in (
        "oldest",
        "model memory",
        "copy abundance",
        "discovery timing",
        "do not store scripture text",
        "commentary",
        "canonical_*",
        "preferred readings",
        "apologetic conclusions",
    ):
        if phrase not in joined:
            raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}: anti_guessing_rules missing {phrase!r}")

    statuses = set(_require_string_list(data.get("review_status_values"), "review_status_values"))
    if statuses != REQUIRED_REVIEW_STATUSES:
        raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}: review_status_values must be {sorted(REQUIRED_REVIEW_STATUSES)}")


def _validate_future_goal_prompts(data: dict[str, Any]) -> None:
    prompts = data.get("future_goal_prompts")
    if not isinstance(prompts, list) or not prompts:
        raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}: future_goal_prompts must be a non-empty list")
    goal_ids = {item.get("goal_id") for item in prompts if isinstance(item, dict)}
    if goal_ids != REQUIRED_GOAL_IDS:
        raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}: future_goal_prompts must be {sorted(REQUIRED_GOAL_IDS)}")
    joined = "\n".join(str(item.get("prompt", "")) for item in prompts if isinstance(item, dict)).lower()
    for phrase in (
        "logos-boundary-literature",
        "logos-doctrine-genealogy",
        "no transcription text",
        "do not import manuscript text",
        "scripture references only",
    ):
        if phrase not in joined:
            raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}: future_goal_prompts missing {phrase!r}")


def _validate_non_authorizations(data: dict[str, Any]) -> None:
    non_auth = set(_require_string_list(data.get("non_authorizations"), "non_authorizations"))
    missing = sorted(REQUIRED_NON_AUTHORIZATIONS - non_auth)
    if missing:
        raise ManuscriptSourceCatalogPlanError(f"{_rel(PLAN)}: non_authorizations missing {missing}")


def _validate_wiring() -> None:
    for path, needles in REQUIRED_WIRING.items():
        text = _read_text(path)
        for needle in needles:
            if needle not in text:
                raise ManuscriptSourceCatalogPlanError(f"{_rel(path)}: missing wiring string {needle!r}")
    for path in (ROADMAP_DOC, TASK, HANDOFF):
        if not path.exists():
            raise ManuscriptSourceCatalogPlanError(f"{_rel(path)}: required T390 surface is missing")


def validate_manuscript_source_catalog_metadata_plan(*, check_wiring: bool = True) -> dict[str, Any]:
    data = _read_yaml(PLAN)
    _validate_metadata(data)
    _validate_authority(data)
    _validate_placement_and_boundary(data)
    _validate_sqlite_entity_plan(data)
    _validate_source_families_and_anchors(data)
    _validate_trust_and_anti_guessing(data)
    _validate_future_goal_prompts(data)
    _validate_non_authorizations(data)
    if check_wiring:
        _validate_wiring()
    return {
        "plan_id": data["plan_id"],
        "table_count": len(data["sqlite_entity_plan"]["tables"]),
        "source_family_count": len(data["source_families"]),
        "source_anchor_count": len(data["source_anchors"]),
        "trust_rule_count": len(data["source_trust_rules"]),
        "future_goal_count": len(data["future_goal_prompts"]),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-wiring", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = validate_manuscript_source_catalog_metadata_plan(check_wiring=not args.skip_wiring)
    except ManuscriptSourceCatalogPlanError as exc:
        print(f"T390 manuscript source catalog metadata plan validation failed: {exc}", file=sys.stderr)
        return 1
    print(
        "T390 manuscript source catalog metadata plan validation passed "
        f"({result['table_count']} planned tables, {result['source_anchor_count']} source anchors)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
