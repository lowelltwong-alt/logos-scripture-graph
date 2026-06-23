#!/usr/bin/env python3
"""Validate the T391 manuscript source-catalog research packet."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
PACKET = ROOT / ".ai" / "control" / "manuscript_source_catalog_research_packet.yaml"
ROADMAP_DOC = ROOT / "docs" / "roadmap" / "T391_MANUSCRIPT_SOURCE_CATALOG_RESEARCH_PACKET.md"
TASK = ROOT / ".ai" / "tasks" / "T391.task.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T391" / "handoff.md"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
MAIN_TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"
ROADMAP_STATE = ROOT / "ROADMAP_STATE.yaml"
VALIDATE_ALL = ROOT / "scripts" / "validate_all.py"

REQUIRED_SOURCE_FAMILIES = {
    "dss_biblical_witness_catalogs",
    "nt_manuscript_catalogs",
    "major_codex_project_catalogs",
    "holding_institution_catalogs",
    "critical_apparatus_method_profiles",
}

REQUIRED_SOURCE_IDS = {
    "iaa_leon_levy_dss_digital_library",
    "iaa_dss_archive_browser",
    "iaa_dss_discovery_publication",
    "iaa_dss_content_categories",
    "israel_museum_great_isaiah_scroll",
    "israel_museum_great_isaiah_collection_record",
    "intf_ntvmr",
    "intf_liste",
    "intf_institute_profile",
    "intf_ecm",
    "intf_cbgm",
    "csntm_manuscripts_catalog",
    "csntm_p52",
    "manchester_rylands_p52",
    "codex_sinaiticus_project",
    "codex_sinaiticus_project_about",
    "vatican_library_codex_vaticanus",
    "british_library_codex_alexandrinus",
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

REQUIRED_NON_AUTHORIZATIONS = {
    "sqlite_database_creation",
    "metadata_row_population",
    "source_text_import",
    "transcription_storage",
    "bible_text_storage",
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
        "manuscript_source_catalog_research_packet.yaml",
        "T391 source-catalog research packet",
    ],
    MAIN_TOC: [
        "source-catalog-research",
        "manuscript_source_catalog_research_packet.yaml",
        "T391_MANUSCRIPT_SOURCE_CATALOG_RESEARCH_PACKET.md",
    ],
    ROADMAP_TOC: [
        "T391 | Manuscript source catalog research packet",
        "source-catalog-research",
        "scripts/validate_manuscript_source_catalog_research_packet.py",
    ],
    ROADMAP_STATE: [
        "T391",
        "Manuscript Source Catalog Research Packet",
        "manuscript_source_catalog_research_packet.yaml",
    ],
    VALIDATE_ALL: ["validate_manuscript_source_catalog_research_packet.py"],
}


class ManuscriptSourceCatalogResearchPacketError(ValueError):
    """Raised when the T391 research packet is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ManuscriptSourceCatalogResearchPacketError(f"{_rel(path)}: unreadable: {exc}") from exc


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
        raise ManuscriptSourceCatalogResearchPacketError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise ManuscriptSourceCatalogResearchPacketError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ManuscriptSourceCatalogResearchPacketError(f"{label} must be a mapping")
    return value


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ManuscriptSourceCatalogResearchPacketError(f"{label} must be a non-empty string")
    return value.strip()


def _require_string_list(value: Any, label: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not value and not allow_empty):
        raise ManuscriptSourceCatalogResearchPacketError(
            f"{label} must be a {'possibly empty ' if allow_empty else ''}list"
        )
    result: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ManuscriptSourceCatalogResearchPacketError(f"{label} must contain only non-empty strings")
        result.append(item.strip())
    return result


def _validate_metadata(data: dict[str, Any]) -> None:
    expected = {
        "object_type": "manuscript_source_catalog_research_packet",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "manuscript_source_catalog_research_packet.v1",
        "packet_id": "t391_manuscript_source_catalog_research_packet",
        "task_id": "T391",
        "status": "active_research_packet_only",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise ManuscriptSourceCatalogResearchPacketError(f"{_rel(PACKET)}: {key} must be {value!r}")
    for key in ("provenance_note", "reason_for_inclusion", "source_access_date"):
        _require_string(data.get(key), f"{_rel(PACKET)}.{key}")


def _validate_authority(data: dict[str, Any]) -> None:
    authority = _require_mapping(data.get("authority"), f"{_rel(PACKET)}.authority")
    for key in (
        "records_curated_source_list",
        "records_source_family_taxonomy",
        "records_confirmed_source_metadata_claims",
        "records_candidate_claims_and_blockers",
        "refines_t390_metadata_plan",
        "may_define_next_goal_prompt",
    ):
        if authority.get(key) is not True:
            raise ManuscriptSourceCatalogResearchPacketError(f"{_rel(PACKET)}: authority.{key} must be true")
    missing = sorted(REQUIRED_FALSE_AUTHORITY - set(authority))
    if missing:
        raise ManuscriptSourceCatalogResearchPacketError(f"{_rel(PACKET)}: authority missing {missing}")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise ManuscriptSourceCatalogResearchPacketError(f"{_rel(PACKET)}: authority.{key} must be false")


def _validate_placement(data: dict[str, Any]) -> None:
    placement = _require_mapping(data.get("placement_decision"), f"{_rel(PACKET)}.placement_decision")
    if placement.get("owning_repo") != "logos-scripture-graph":
        raise ManuscriptSourceCatalogResearchPacketError(f"{_rel(PACKET)}: owning_repo must be logos-scripture-graph")
    split_rule = str(placement.get("split_rule", "")).lower()
    for phrase in ("source metadata", "must not store", "bible text", "commentary text", "creed wording"):
        if phrase not in split_rule:
            raise ManuscriptSourceCatalogResearchPacketError(f"{_rel(PACKET)}: split_rule missing {phrase!r}")
    for key, target in (
        ("boundary_repo_scope", "logos-boundary-literature"),
        ("doctrine_repo_scope", "logos-doctrine-genealogy"),
    ):
        if target not in str(placement.get(key, "")):
            raise ManuscriptSourceCatalogResearchPacketError(f"{_rel(PACKET)}: {key} must mention {target}")


def _validate_source_families(data: dict[str, Any]) -> set[str]:
    families = data.get("source_family_taxonomy")
    if not isinstance(families, list) or not families:
        raise ManuscriptSourceCatalogResearchPacketError(f"{_rel(PACKET)}: source_family_taxonomy must be a list")
    family_ids = {item.get("family_id") for item in families if isinstance(item, dict)}
    if family_ids != REQUIRED_SOURCE_FAMILIES:
        raise ManuscriptSourceCatalogResearchPacketError(
            f"{_rel(PACKET)}: source_family_taxonomy must be {sorted(REQUIRED_SOURCE_FAMILIES)}"
        )
    for family in families:
        if not isinstance(family, dict):
            raise ManuscriptSourceCatalogResearchPacketError(f"{_rel(PACKET)}: each source family must be a mapping")
        label = f"{_rel(PACKET)}:{family.get('family_id')}"
        if family.get("correct_repo") != "logos-scripture-graph":
            raise ManuscriptSourceCatalogResearchPacketError(f"{label}: correct_repo must be logos-scripture-graph")
        for key in (
            "description",
            "confirmed_fact_boundary",
            "candidate_claim_boundary",
            "routes_elsewhere",
            "review_status",
        ):
            _require_string(family.get(key), f"{label}.{key}")
        _require_string_list(family.get("required_cross_checks"), f"{label}.required_cross_checks")
    return family_ids


def _validate_sources(data: dict[str, Any], family_ids: set[str]) -> set[str]:
    sources = data.get("curated_sources")
    if not isinstance(sources, list) or not sources:
        raise ManuscriptSourceCatalogResearchPacketError(f"{_rel(PACKET)}: curated_sources must be a list")
    source_ids = {item.get("source_id") for item in sources if isinstance(item, dict)}
    if source_ids != REQUIRED_SOURCE_IDS:
        raise ManuscriptSourceCatalogResearchPacketError(
            f"{_rel(PACKET)}: curated_sources must be {sorted(REQUIRED_SOURCE_IDS)}"
        )
    for source in sources:
        if not isinstance(source, dict):
            raise ManuscriptSourceCatalogResearchPacketError(f"{_rel(PACKET)}: each source must be a mapping")
        label = f"{_rel(PACKET)}:{source.get('source_id')}"
        if source.get("source_family") not in family_ids:
            raise ManuscriptSourceCatalogResearchPacketError(f"{label}: invalid source_family")
        for key in (
            "source_title",
            "source_url",
            "maintainer_or_institution",
            "source_type",
            "source_anchor_role",
            "confirmed_fact_summary",
            "method",
            "confidence",
            "provenance_note",
            "review_status",
            "source_limits",
        ):
            _require_string(source.get(key), f"{label}.{key}")
        if not str(source["source_url"]).startswith("https://"):
            raise ManuscriptSourceCatalogResearchPacketError(f"{label}: source_url must use https")
    return source_ids


def _validate_claims(
    claims: Any,
    *,
    section: str,
    source_ids: set[str],
    min_count: int,
) -> int:
    if not isinstance(claims, list) or len(claims) < min_count:
        raise ManuscriptSourceCatalogResearchPacketError(
            f"{_rel(PACKET)}:{section}.confirmed_facts must contain at least {min_count} claims"
        )
    for claim in claims:
        if not isinstance(claim, dict):
            raise ManuscriptSourceCatalogResearchPacketError(f"{_rel(PACKET)}:{section}: each claim must be a mapping")
        label = f"{_rel(PACKET)}:{claim.get('claim_id')}"
        for key in ("claim_id", "claim", "method", "confidence", "provenance_note", "review_status"):
            _require_string(claim.get(key), f"{label}.{key}")
        claim_sources = set(_require_string_list(claim.get("source_ids"), f"{label}.source_ids"))
        unknown = sorted(claim_sources - source_ids)
        if unknown:
            raise ManuscriptSourceCatalogResearchPacketError(f"{label}: unknown source_ids {unknown}")
    return len(claims)


def _validate_candidate_claims(value: Any, section: str) -> None:
    if not isinstance(value, list) or not value:
        raise ManuscriptSourceCatalogResearchPacketError(f"{_rel(PACKET)}:{section}.candidate_claims must be a list")
    for claim in value:
        if not isinstance(claim, dict):
            raise ManuscriptSourceCatalogResearchPacketError(
                f"{_rel(PACKET)}:{section}.candidate_claims entries must be mappings"
            )
        label = f"{_rel(PACKET)}:{claim.get('claim_id')}"
        for key in (
            "claim_id",
            "claim",
            "current_status",
            "required_source_review",
            "confidence",
            "provenance_note",
            "review_status",
        ):
            _require_string(claim.get(key), f"{label}.{key}")


def _validate_blocked_claims(value: Any, section: str) -> None:
    if not isinstance(value, list) or not value:
        raise ManuscriptSourceCatalogResearchPacketError(f"{_rel(PACKET)}:{section}.blocked_claims must be a list")
    for claim in value:
        if not isinstance(claim, dict):
            raise ManuscriptSourceCatalogResearchPacketError(
                f"{_rel(PACKET)}:{section}.blocked_claims entries must be mappings"
            )
        for key in ("blocked_claim", "review_status"):
            _require_string(claim.get(key), f"{section}.{key}")
        if not (claim.get("reason_blocked") or claim.get("why_blocked")):
            raise ManuscriptSourceCatalogResearchPacketError(f"{section}: blocked claim must explain why blocked")
        if not (claim.get("required_next_action") or claim.get("next_action")):
            raise ManuscriptSourceCatalogResearchPacketError(f"{section}: blocked claim must include next action")


def _validate_packets(data: dict[str, Any], source_ids: set[str]) -> tuple[int, int]:
    dss = _require_mapping(data.get("dss_biblical_witness_packet"), f"{_rel(PACKET)}.dss_biblical_witness_packet")
    nt = _require_mapping(data.get("nt_papyri_codices_packet"), f"{_rel(PACKET)}.nt_papyri_codices_packet")
    for section, packet in (("dss_biblical_witness_packet", dss), ("nt_papyri_codices_packet", nt)):
        _require_string(packet.get("packet_scope"), f"{section}.packet_scope")
        unknown = sorted(set(_require_string_list(packet.get("source_ids"), f"{section}.source_ids")) - source_ids)
        if unknown:
            raise ManuscriptSourceCatalogResearchPacketError(f"{section}: unknown source_ids {unknown}")
        _validate_candidate_claims(packet.get("candidate_claims"), section)
        _validate_blocked_claims(packet.get("blocked_claims"), section)

    dss_count = _validate_claims(
        dss.get("confirmed_facts"),
        section="dss_biblical_witness_packet",
        source_ids=source_ids,
        min_count=6,
    )
    nt_count = _validate_claims(
        nt.get("confirmed_facts"),
        section="nt_papyri_codices_packet",
        source_ids=source_ids,
        min_count=10,
    )
    return dss_count, nt_count


def _validate_timeline_and_open_questions(data: dict[str, Any], source_ids: set[str]) -> int:
    anchors = data.get("discovery_timeline_source_anchors")
    if not isinstance(anchors, list) or len(anchors) < 5:
        raise ManuscriptSourceCatalogResearchPacketError(
            f"{_rel(PACKET)}: discovery_timeline_source_anchors must contain at least five anchors"
        )
    for anchor in anchors:
        if not isinstance(anchor, dict):
            raise ManuscriptSourceCatalogResearchPacketError(f"{_rel(PACKET)}: each timeline anchor must be a mapping")
        label = f"{_rel(PACKET)}:{anchor.get('event_anchor_id')}"
        for key in (
            "event_anchor_id",
            "timeline_scope",
            "what_became_known",
            "what_not_proven",
            "method",
            "confidence",
            "provenance_note",
            "review_status",
        ):
            _require_string(anchor.get(key), f"{label}.{key}")
        unknown = sorted(set(_require_string_list(anchor.get("source_ids"), f"{label}.source_ids")) - source_ids)
        if unknown:
            raise ManuscriptSourceCatalogResearchPacketError(f"{label}: unknown source_ids {unknown}")

    questions = data.get("open_questions_and_blocked_claims")
    if not isinstance(questions, list) or len(questions) < 6:
        raise ManuscriptSourceCatalogResearchPacketError(
            f"{_rel(PACKET)}: open_questions_and_blocked_claims must contain at least six items"
        )
    for question in questions:
        if not isinstance(question, dict):
            raise ManuscriptSourceCatalogResearchPacketError(
                f"{_rel(PACKET)}: open_questions_and_blocked_claims entries must be mappings"
            )
        for key in ("question_id", "blocked_claim", "why_blocked", "next_action", "review_status"):
            _require_string(question.get(key), f"open_questions_and_blocked_claims.{key}")
    return len(anchors)


def _validate_handoff_and_next_goal(data: dict[str, Any]) -> None:
    handoff = _require_mapping(data.get("handoff_and_validation"), f"{_rel(PACKET)}.handoff_and_validation")
    if handoff.get("required_handoff") != ".ai/handoffs/T391/handoff.md":
        raise ManuscriptSourceCatalogResearchPacketError(f"{_rel(PACKET)}: wrong required handoff")
    if handoff.get("required_task") != ".ai/tasks/T391.task.yaml":
        raise ManuscriptSourceCatalogResearchPacketError(f"{_rel(PACKET)}: wrong required task")
    for key in ("validator", "tests"):
        _require_string(handoff.get(key), f"handoff_and_validation.{key}")
    commands = _require_string_list(handoff.get("validation_commands"), "handoff_and_validation.validation_commands")
    for needle in (
        "python scripts/validate_manuscript_source_catalog_research_packet.py",
        "python scripts/validate_all.py",
        "python -m pytest -q",
    ):
        if needle not in commands:
            raise ManuscriptSourceCatalogResearchPacketError(f"{_rel(PACKET)}: validation_commands missing {needle}")

    next_goal = _require_mapping(data.get("next_goal_prompt"), f"{_rel(PACKET)}.next_goal_prompt")
    if next_goal.get("goal_id") != "NEXT_UNUSED_SQLITE_SOURCE_CATALOG_SCHEMA_SHELL_AND_SOURCE_ROWS":
        raise ManuscriptSourceCatalogResearchPacketError(f"{_rel(PACKET)}: unexpected next goal id")
    prompt = _require_string(next_goal.get("prompt"), "next_goal_prompt.prompt").lower()
    for phrase in (
        "sqlite source-catalog schema shell",
        "do not populate witness rows",
        "do not import source text",
        "do not store manuscript transcription",
        "no canonical_* table or view",
    ):
        if phrase not in prompt:
            raise ManuscriptSourceCatalogResearchPacketError(f"{_rel(PACKET)}: next goal prompt missing {phrase!r}")


def _validate_non_authorizations(data: dict[str, Any]) -> None:
    non_auth = set(_require_string_list(data.get("non_authorizations"), "non_authorizations"))
    missing = sorted(REQUIRED_NON_AUTHORIZATIONS - non_auth)
    if missing:
        raise ManuscriptSourceCatalogResearchPacketError(f"{_rel(PACKET)}: non_authorizations missing {missing}")
    text = _read_text(PACKET)
    for forbidden in (
        "stores_transcription_text: true",
        "stores_scripture_text: true",
        "authorizes_preferred_reading: true",
        "authorizes_apologetic_conclusion_as_truth: true",
        "table_name: canonical_",
    ):
        if forbidden in text:
            raise ManuscriptSourceCatalogResearchPacketError(f"{_rel(PACKET)}: forbidden string {forbidden!r}")


def _validate_wiring() -> None:
    for path, needles in REQUIRED_WIRING.items():
        text = _read_text(path)
        for needle in needles:
            if needle not in text:
                raise ManuscriptSourceCatalogResearchPacketError(f"{_rel(path)}: missing wiring string {needle!r}")
    for path in (ROADMAP_DOC, TASK, HANDOFF):
        if not path.exists():
            raise ManuscriptSourceCatalogResearchPacketError(f"{_rel(path)}: required T391 surface is missing")


def validate_manuscript_source_catalog_research_packet(*, check_wiring: bool = True) -> dict[str, Any]:
    data = _read_yaml(PACKET)
    _validate_metadata(data)
    _validate_authority(data)
    _validate_placement(data)
    family_ids = _validate_source_families(data)
    source_ids = _validate_sources(data, family_ids)
    dss_count, nt_count = _validate_packets(data, source_ids)
    timeline_count = _validate_timeline_and_open_questions(data, source_ids)
    _validate_handoff_and_next_goal(data)
    _validate_non_authorizations(data)
    if check_wiring:
        _validate_wiring()
    return {
        "packet_id": data["packet_id"],
        "source_family_count": len(family_ids),
        "source_count": len(source_ids),
        "dss_confirmed_fact_count": dss_count,
        "nt_confirmed_fact_count": nt_count,
        "timeline_anchor_count": timeline_count,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-wiring", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = validate_manuscript_source_catalog_research_packet(check_wiring=not args.skip_wiring)
    except ManuscriptSourceCatalogResearchPacketError as exc:
        print(f"T391 manuscript source-catalog research packet validation failed: {exc}", file=sys.stderr)
        return 1
    print(
        "T391 manuscript source-catalog research packet validation passed "
        f"({result['source_count']} sources, {result['dss_confirmed_fact_count']} DSS facts, "
        f"{result['nt_confirmed_fact_count']} NT facts)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

