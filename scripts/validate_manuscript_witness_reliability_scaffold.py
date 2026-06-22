#!/usr/bin/env python3
"""Validate the T387 manuscript witness reliability scaffold."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
SCAFFOLD = ROOT / ".ai" / "control" / "manuscript_witness_reliability_scaffold.yaml"
ROADMAP_DOC = ROOT / "docs" / "roadmap" / "T387_MANUSCRIPT_WITNESS_RELIABILITY_SCAFFOLD.md"
TASK = ROOT / ".ai" / "tasks" / "T387.task.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T387" / "handoff.md"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
MAIN_TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"
ROADMAP_STATE = ROOT / "ROADMAP_STATE.yaml"
VALIDATE_ALL = ROOT / "scripts" / "validate_all.py"

REQUIRED_TABLES = {
    "scripture_witness_source",
    "scripture_manuscript_witness",
    "scripture_textual_variant_unit",
    "scripture_variant_attestation",
    "scripture_discovery_timeline_event",
    "evidence_reliability_claim",
}

REQUIRED_FALSE_AUTHORITY = {
    "authorizes_source_text_import",
    "authorizes_canonical_bible_text_change",
    "authorizes_canonical_passage_record_change",
    "authorizes_chunk_output_change",
    "authorizes_reviewed_gold_promotion",
    "authorizes_textual_critical_decision",
    "authorizes_preferred_reading",
    "authorizes_source_tradition_preference",
    "authorizes_canon_scope_change",
    "authorizes_boundary_import",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_embedding_or_vector_work",
    "authorizes_doctrinal_system",
    "authorizes_apologetic_conclusion_as_truth",
}

REQUIRED_SOURCE_ANCHORS = {
    "iaa_leon_levy_dss_digital_library",
    "iaa_dss_discovery_publication",
    "israel_museum_great_isaiah_scroll",
    "intf_institute_profile",
    "intf_ecm_method_profile",
    "manchester_rylands_p52",
    "csntm_p52",
    "codex_sinaiticus_project",
}

REQUIRED_BACKLOG = {
    "dss_biblical_witness_spine",
    "nt_papyri_and_major_codices_spine",
    "copy_abundance_variant_detection_method",
    "discovery_timeline_what_was_known_when",
    "early_creed_oral_tradition_bridge",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "source_text_import",
    "canonical_bible_text_change",
    "canonical_passage_record_change",
    "canonical_chunk_change",
    "reviewed_gold_promotion",
    "textual_critical_decision",
    "preferred_reading_selection",
    "source_tradition_preference",
    "canon_scope_change",
    "boundary_import",
    "commentary_as_scripture",
    "patristic_citation_as_scripture_authority",
    "graph_edge_generation",
    "retrieval_truth",
    "embedding_or_vector_work",
    "apologetic_conclusion_as_truth",
}

REQUIRED_WIRING = {
    FRONT_DOOR: [
        "manuscript_witness_reliability_scaffold.yaml",
        "T387 manuscript witness reliability scaffold",
    ],
    MAIN_TOC: [
        "manuscript-witness",
        "manuscript_witness_reliability_scaffold.yaml",
        "T387_MANUSCRIPT_WITNESS_RELIABILITY_SCAFFOLD.md",
    ],
    ROADMAP_TOC: [
        "T387 | Manuscript witness reliability scaffold",
        "manuscript-witness",
        "scripts/validate_manuscript_witness_reliability_scaffold.py",
    ],
    ROADMAP_STATE: [
        "T387",
        "Manuscript Witness Reliability Scaffold",
        "manuscript_witness_reliability_scaffold.yaml",
    ],
    VALIDATE_ALL: ["validate_manuscript_witness_reliability_scaffold.py"],
}


class ManuscriptWitnessReliabilityError(ValueError):
    """Raised when the T387 scaffold is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ManuscriptWitnessReliabilityError(f"{_rel(path)}: unreadable: {exc}") from exc


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
        raise ManuscriptWitnessReliabilityError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise ManuscriptWitnessReliabilityError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ManuscriptWitnessReliabilityError(f"{label} must be a mapping")
    return value


def _require_string_list(value: Any, label: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not allow_empty and not value):
        raise ManuscriptWitnessReliabilityError(f"{label} must be a {'possibly empty ' if allow_empty else ''}list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise ManuscriptWitnessReliabilityError(f"{label} must contain only non-empty strings")
    return [str(item) for item in value]


def _validate_metadata(data: dict[str, Any]) -> None:
    expected = {
        "object_type": "manuscript_witness_reliability_scaffold",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "manuscript_witness_reliability_scaffold.v1",
        "scaffold_id": "t387_manuscript_witness_reliability_scaffold",
        "task_id": "T387",
        "status": "active_planning_only",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise ManuscriptWitnessReliabilityError(f"{_rel(SCAFFOLD)}: {key} must be {value!r}")
    for key in ("provenance_note", "reason_for_inclusion"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ManuscriptWitnessReliabilityError(f"{_rel(SCAFFOLD)}: {key} must be a non-empty string")


def _validate_authority(data: dict[str, Any]) -> None:
    authority = _require_mapping(data.get("authority"), f"{_rel(SCAFFOLD)}: authority")
    if authority.get("records_manuscript_witness_reliability_scaffold") is not True:
        raise ManuscriptWitnessReliabilityError(f"{_rel(SCAFFOLD)}: authority.records_manuscript_witness_reliability_scaffold must be true")
    missing = sorted(REQUIRED_FALSE_AUTHORITY - set(authority))
    if missing:
        raise ManuscriptWitnessReliabilityError(f"{_rel(SCAFFOLD)}: authority missing {missing}")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise ManuscriptWitnessReliabilityError(f"{_rel(SCAFFOLD)}: authority.{key} must be false")


def _validate_placement(data: dict[str, Any]) -> None:
    placement = _require_mapping(data.get("placement_decision"), f"{_rel(SCAFFOLD)}: placement_decision")
    if placement.get("owning_repo") != "logos-scripture-graph":
        raise ManuscriptWitnessReliabilityError(f"{_rel(SCAFFOLD)}: placement_decision.owning_repo must be logos-scripture-graph")
    if "logos-boundary-literature" not in str(placement.get("boundary_repo_scope", "")):
        raise ManuscriptWitnessReliabilityError(f"{_rel(SCAFFOLD)}: boundary repo scope must be explicit")
    if "logos-governance-architecture" not in str(placement.get("governance_repo_scope", "")):
        raise ManuscriptWitnessReliabilityError(f"{_rel(SCAFFOLD)}: governance repo scope must be explicit")
    split_rule = str(placement.get("split_rule", ""))
    if "noncanonical" not in split_rule or "canonical Scripture records" not in split_rule:
        raise ManuscriptWitnessReliabilityError(f"{_rel(SCAFFOLD)}: split_rule must preserve noncanonical/canonical separation")


def _validate_database_plan(data: dict[str, Any]) -> None:
    plan = _require_mapping(data.get("database_namespace_plan"), f"{_rel(SCAFFOLD)}: database_namespace_plan")
    if set(_require_string_list(plan.get("allowed_prefixes"), "allowed_prefixes")) != {"scripture_", "evidence_"}:
        raise ManuscriptWitnessReliabilityError(f"{_rel(SCAFFOLD)}: allowed prefixes must be scripture_ and evidence_")
    forbidden = set(_require_string_list(plan.get("forbidden_prefixes"), "forbidden_prefixes"))
    if "canonical_" not in forbidden:
        raise ManuscriptWitnessReliabilityError(f"{_rel(SCAFFOLD)}: canonical_ prefix must be forbidden")
    tables = plan.get("tables")
    if not isinstance(tables, list) or not tables:
        raise ManuscriptWitnessReliabilityError(f"{_rel(SCAFFOLD)}: tables must be a non-empty list")
    table_names = {item.get("table_name") for item in tables if isinstance(item, dict)}
    if table_names != REQUIRED_TABLES:
        raise ManuscriptWitnessReliabilityError(f"{_rel(SCAFFOLD)}: tables must be {sorted(REQUIRED_TABLES)}")
    for table in tables:
        if not isinstance(table, dict):
            raise ManuscriptWitnessReliabilityError(f"{_rel(SCAFFOLD)}: each table must be a mapping")
        name = str(table.get("table_name"))
        if not (name.startswith("scripture_") or name.startswith("evidence_")):
            raise ManuscriptWitnessReliabilityError(f"{_rel(SCAFFOLD)}: table {name} must use scripture_ or evidence_")
        if name.startswith("canonical_"):
            raise ManuscriptWitnessReliabilityError(f"{_rel(SCAFFOLD)}: table {name} uses forbidden canonical_ prefix")
        if table.get("stores_scripture_text") is not False:
            raise ManuscriptWitnessReliabilityError(f"{_rel(SCAFFOLD)}:{name}: stores_scripture_text must be false")
        if table.get("stores_boundary_text") is not False:
            raise ManuscriptWitnessReliabilityError(f"{_rel(SCAFFOLD)}:{name}: stores_boundary_text must be false")
        required_fields = _require_string_list(table.get("required_fields"), f"{name}.required_fields")
        fields_joined = " ".join(required_fields)
        for required in ("provenance", "review_status"):
            if required not in fields_joined:
                raise ManuscriptWitnessReliabilityError(f"{_rel(SCAFFOLD)}:{name}: required_fields must include {required}")


def _validate_guardrails(data: dict[str, Any]) -> None:
    guardrails = _require_mapping(data.get("guardrails"), f"{_rel(SCAFFOLD)}: guardrails")
    controls = _require_string_list(guardrails.get("anti_guessing_controls"), "anti_guessing_controls")
    joined = "\n".join(controls).lower()
    for phrase in (
        "no ai-inferred manuscript date",
        "oldest",
        "copy abundance",
        "discovery timeline",
        "do not store scripture text",
        "noncanonical qumran",
    ):
        if phrase not in joined:
            raise ManuscriptWitnessReliabilityError(f"{_rel(SCAFFOLD)}: anti_guessing_controls missing {phrase!r}")
    required_sources = set(_require_string_list(guardrails.get("source_required_for"), "source_required_for"))
    for field in ("manuscript_date_range", "textual_variant_attestation", "copy_abundance_claim"):
        if field not in required_sources:
            raise ManuscriptWitnessReliabilityError(f"{_rel(SCAFFOLD)}: source_required_for missing {field}")


def _validate_sources_and_backlog(data: dict[str, Any]) -> None:
    anchors = data.get("source_anchors")
    if not isinstance(anchors, list) or not anchors:
        raise ManuscriptWitnessReliabilityError(f"{_rel(SCAFFOLD)}: source_anchors must be a non-empty list")
    anchor_ids = {item.get("anchor_id") for item in anchors if isinstance(item, dict)}
    if anchor_ids != REQUIRED_SOURCE_ANCHORS:
        raise ManuscriptWitnessReliabilityError(f"{_rel(SCAFFOLD)}: source_anchors must be {sorted(REQUIRED_SOURCE_ANCHORS)}")
    for anchor in anchors:
        if not isinstance(anchor, dict):
            raise ManuscriptWitnessReliabilityError(f"{_rel(SCAFFOLD)}: each source anchor must be a mapping")
        label = str(anchor.get("anchor_id"))
        for key in ("source_url", "source_type", "confirmed_fact_summary", "scaffold_use", "not_authorized"):
            if not isinstance(anchor.get(key), str) or not anchor[key].strip():
                raise ManuscriptWitnessReliabilityError(f"{_rel(SCAFFOLD)}:{label}: {key} must be a non-empty string")
        if not anchor["source_url"].startswith("https://"):
            raise ManuscriptWitnessReliabilityError(f"{_rel(SCAFFOLD)}:{label}: source_url must be https")
    backlog = data.get("initial_research_backlog")
    if not isinstance(backlog, list) or not backlog:
        raise ManuscriptWitnessReliabilityError(f"{_rel(SCAFFOLD)}: initial_research_backlog must be a non-empty list")
    backlog_ids = {item.get("backlog_id") for item in backlog if isinstance(item, dict)}
    if backlog_ids != REQUIRED_BACKLOG:
        raise ManuscriptWitnessReliabilityError(f"{_rel(SCAFFOLD)}: initial_research_backlog must be {sorted(REQUIRED_BACKLOG)}")
    bridge = next(item for item in backlog if item.get("backlog_id") == "early_creed_oral_tradition_bridge")
    if bridge.get("correct_repo") != "logos-boundary-literature":
        raise ManuscriptWitnessReliabilityError(f"{_rel(SCAFFOLD)}: early creed/oral tradition bridge must route to Boundary Literature")


def _validate_non_authorizations(data: dict[str, Any]) -> None:
    non_auth = set(_require_string_list(data.get("non_authorizations"), "non_authorizations"))
    missing = sorted(REQUIRED_NON_AUTHORIZATIONS - non_auth)
    if missing:
        raise ManuscriptWitnessReliabilityError(f"{_rel(SCAFFOLD)}: non_authorizations missing {missing}")


def _validate_wiring() -> None:
    for path, needles in REQUIRED_WIRING.items():
        text = _read_text(path)
        for needle in needles:
            if needle not in text:
                raise ManuscriptWitnessReliabilityError(f"{_rel(path)}: missing wiring string {needle!r}")
    for path in (ROADMAP_DOC, TASK, HANDOFF):
        if not path.exists():
            raise ManuscriptWitnessReliabilityError(f"{_rel(path)}: required T387 surface is missing")


def validate_manuscript_witness_reliability_scaffold(*, check_wiring: bool = True) -> dict[str, Any]:
    data = _read_yaml(SCAFFOLD)
    _validate_metadata(data)
    _validate_authority(data)
    _validate_placement(data)
    _validate_database_plan(data)
    _validate_guardrails(data)
    _validate_sources_and_backlog(data)
    _validate_non_authorizations(data)
    if check_wiring:
        _validate_wiring()
    return {
        "scaffold_id": data["scaffold_id"],
        "table_count": len(data["database_namespace_plan"]["tables"]),
        "source_anchor_count": len(data["source_anchors"]),
        "backlog_count": len(data["initial_research_backlog"]),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-wiring", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = validate_manuscript_witness_reliability_scaffold(check_wiring=not args.skip_wiring)
    except ManuscriptWitnessReliabilityError as exc:
        print(f"T387 manuscript witness reliability validation failed: {exc}", file=sys.stderr)
        return 1
    print(
        "T387 manuscript witness reliability validation passed "
        f"({result['table_count']} planned tables, {result['source_anchor_count']} source anchors)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
