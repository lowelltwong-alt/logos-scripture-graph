#!/usr/bin/env python3
"""Validate mandatory preflight reading for chunking agents."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
RULE_REGISTRY = ROOT / "docs" / "methodology" / "LOGOS_CHUNKING_WORKFLOW_RULES_REGISTRY.md"
SUPPLY_CHAIN = ROOT / "docs" / "methodology" / "CHUNKING_SKILL_SUPPLY_CHAIN.md"
WORKFLOW_LESSONS = ROOT / "docs" / "methodology" / "WORKFLOW_LESSONS.md"
DECISION_REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
TRIAGE_MAP = ROOT / ".ai" / "control" / "bible_chunking_research_triage_map.yaml"
RESEARCH_REGISTRY = ROOT / ".ai" / "control" / "bible_wide_chunking_research_registry.yaml"
SOURCE_METADATA_ATLAS = ROOT / ".ai" / "control" / "source_metadata_research_atlas.yaml"
APOCALYPTIC_INTERTEXT_QUEUE = ROOT / ".ai" / "control" / "apocalyptic_prophetic_intertext_dossier_queue.yaml"
EPISTLE_ISSUE_QUEUE = ROOT / ".ai" / "control" / "epistle_argument_theological_issue_dossier_queue.yaml"
GOSPEL_WJ_QUEUE = ROOT / ".ai" / "control" / "gospel_wj_discourse_dossier_queue.yaml"
CAPITALIZATION_INVENTORY = ROOT / ".ai" / "control" / "divine_capitalization_inventory.yaml"
WJ_MARKER_INVENTORY = ROOT / ".ai" / "control" / "wj_marker_inventory.yaml"
WJ_SPEAKER_POLICY = ROOT / ".ai" / "control" / "wj_speaker_discourse_policy.yaml"
JOHN3_OWNER_DOCKET = ROOT / ".ai" / "control" / "john3_wj_owner_review_docket.yaml"

REQUIRED_TOP_LEVEL = {
    "object_type",
    "trust_zone",
    "lifecycle_status",
    "provenance_note",
    "reason_for_inclusion",
    "schema_version",
    "contract_id",
    "owner",
    "applies_to_work_types",
    "mandatory_reading",
    "midflight_lesson_capture",
    "non_authorizing_metadata_types",
    "metadata_authority_policy",
    "future_output_changing_use_requires",
    "validator",
}

REQUIRED_WORK_TYPES = {
    "ingest",
    "chunking",
    "review_packet",
    "evaluator",
    "route_or_orchestrator",
    "graph_or_edge_generation",
}

REQUIRED_RULE_IDS = {
    "CHUNK-METADATA-001",
    "CHUNK-MARKER-001",
    "CHUNK-WJ-001",
    "CHUNK-SEM-001",
}

REQUIRED_DECISION_IDS = {"CD-015", "CD-018", "CD-021", "CD-022", "CD-023", "CD-024", "CD-025", "CD-026", "CD-027", "CD-028"}

REQUIRED_TRIAGE_LANES = {"divine_name_title_capitalization", "gospel_discourse_wj"}

REQUIRED_WORKFLOW_LESSON_IDS = {
    "WORKFLOW-LESSON-004",
    "BIBLE-CHUNKING-WORKFLOW-LESSON-003",
    "BIBLE-CHUNKING-WORKFLOW-LESSON-004",
}

REQUIRED_METADATA_TYPES = {
    "internal_cross_references",
    "strongs_style_word_numbers",
    "hebrew_greek_lexeme_tags",
    "footnotes",
    "alternate_readings",
    "section_headings",
    "paragraph_markers",
    "poetry_markers",
    "words_of_jesus_markers",
    "speaker_labels",
    "edition_formatting",
    "divine_name_title_capitalization",
    "divine_pronoun_capitalization",
}

REQUIRED_AUTHORITY_FALSE = {
    "authorizes_scripture_truth",
    "authorizes_lexical_truth",
    "authorizes_intertext_truth",
    "authorizes_speaker_attribution",
    "authorizes_graph_edges",
    "authorizes_chunk_boundaries",
    "authorizes_output_change",
}

REQUIRED_FRONT_DOOR_STRINGS = {
    ".ai/control/chunking_agent_preflight.yaml",
    "CHUNK-METADATA-001",
    "Source metadata is evidence, not authority",
    "divine-name/title capitalization",
    "divine_capitalization_inventory.yaml",
    "wj_marker_inventory.yaml",
    "wj_speaker_discourse_policy.yaml",
    "john3_wj_owner_review_docket.yaml",
    "bible_wide_chunking_research_registry.yaml",
    "source_metadata_research_atlas.yaml",
    "apocalyptic_prophetic_intertext_dossier_queue.yaml",
    "epistle_argument_theological_issue_dossier_queue.yaml",
    "gospel_wj_discourse_dossier_queue.yaml",
}

REQUIRED_OUTPUT_CHANGE_REQUIREMENTS = {
    "owner_review",
    "exact_scope",
    "reviewed_gold_or_equivalent_governed_evidence",
    "decision_register_update",
    "executable_tests",
    "non_target_identity_proof",
}


class PreflightError(ValueError):
    """Raised when the chunking-agent preflight contract is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
        if text.startswith("---\n"):
            parts = text.split("---\n", 2)
            if len(parts) == 3:
                text = parts[1] + "\n" + parts[2]
        data = yaml.safe_load(text)
    except (OSError, yaml.YAMLError) as exc:
        raise PreflightError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise PreflightError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise PreflightError(f"{_rel(path)}: unreadable: {exc}") from exc


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    if not isinstance(actual, list):
        raise PreflightError(f"{label} must be a list")
    missing = sorted(required - {str(item) for item in actual})
    if missing:
        raise PreflightError(f"{label} missing {missing}")


def validate_preflight(path: Path = PREFLIGHT) -> dict[str, Any]:
    data = _read_yaml(path)
    missing_top = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing_top:
        raise PreflightError(f"{_rel(path)}: missing top-level keys {missing_top}")

    if data["object_type"] != "chunking_agent_preflight_contract":
        raise PreflightError(f"{_rel(path)}: object_type must be chunking_agent_preflight_contract")
    if data["trust_zone"] != "canonical":
        raise PreflightError(f"{_rel(path)}: trust_zone must be canonical")
    if data["lifecycle_status"] != "active":
        raise PreflightError(f"{_rel(path)}: lifecycle_status must be active")
    if data["validator"] != "scripts/validate_chunking_agent_preflight.py":
        raise PreflightError(f"{_rel(path)}: validator path is wrong")

    _require_subset(REQUIRED_WORK_TYPES, data["applies_to_work_types"], "applies_to_work_types")
    _require_subset(
        REQUIRED_METADATA_TYPES,
        data["non_authorizing_metadata_types"],
        "non_authorizing_metadata_types",
    )
    _require_subset(
        REQUIRED_OUTPUT_CHANGE_REQUIREMENTS,
        data["future_output_changing_use_requires"],
        "future_output_changing_use_requires",
    )

    policy = data["metadata_authority_policy"]
    if not isinstance(policy, dict):
        raise PreflightError(f"{_rel(path)}: metadata_authority_policy must be a mapping")
    if policy.get("may_preserve_as_evidence") is not True:
        raise PreflightError(f"{_rel(path)}: metadata must be preservable as evidence")
    if policy.get("may_surface_for_review") is not True:
        raise PreflightError(f"{_rel(path)}: metadata must be surfaceable for review")
    for key in REQUIRED_AUTHORITY_FALSE:
        if policy.get(key) is not False:
            raise PreflightError(f"{_rel(path)}: metadata_authority_policy.{key} must be false")

    lessons = data["midflight_lesson_capture"]
    if not isinstance(lessons, dict):
        raise PreflightError(f"{_rel(path)}: midflight_lesson_capture must be a mapping")
    if lessons.get("status") != "required":
        raise PreflightError(f"{_rel(path)}: midflight_lesson_capture.status must be required")
    for key in ("trigger", "postflight_question"):
        if not isinstance(lessons.get(key), str) or not lessons[key].strip():
            raise PreflightError(f"{_rel(path)}: midflight_lesson_capture.{key} is required")
    _require_subset(
        {
            "update_preflight_if_future_agents_must_read_it_first",
            "update_workflow_if_future_agents_must_do_it_midflight_or_postflight",
            "update_methodology_or_rules_registry_if_it_is_a_reusable_rule",
            "update_decision_register_if_it_has_possible_theological_downstream_effect",
            "add_or_update_validator_or_test_if_machine_checkable",
            "record_no_change_rationale_in_handoff_if_no_surface_changed",
        },
        lessons.get("required_action_before_task_close"),
        "midflight_lesson_capture.required_action_before_task_close",
    )
    _require_subset(
        {
            ".ai/control/chunking_agent_preflight.yaml",
            ".ai/workflows/chunking-skill-supply-chain.workflow.md",
            "docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md",
            "docs/methodology/WORKFLOW_LESSONS.md",
            "docs/methodology/LOGOS_CHUNKING_WORKFLOW_RULES_REGISTRY.md",
            ".ai/control/chunking_theological_decision_register.yaml",
            ".ai/handoffs/<task_id>/handoff.md",
        },
        lessons.get("required_surfaces"),
        "midflight_lesson_capture.required_surfaces",
    )

    reading = data["mandatory_reading"]
    if not isinstance(reading, list) or not reading:
        raise PreflightError(f"{_rel(path)}: mandatory_reading must be a non-empty list")
    reading_by_path = {}
    for item in reading:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            raise PreflightError(f"{_rel(path)}: each mandatory_reading entry must have a path")
        reading_by_path[item["path"]] = item
        target = ROOT / item["path"]
        if not target.exists():
            raise PreflightError(f"{_rel(path)}: mandatory_reading target missing: {item['path']}")

    for required_path in (
        "AI_FRONT_DOOR.md",
        ".ai/control/RAW_SOURCE_INVENTORY.md",
        "config/ingest/usfm_marker_coverage.yaml",
        "docs/methodology/LOGOS_CHUNKING_WORKFLOW_RULES_REGISTRY.md",
        "docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md",
        "docs/methodology/WORKFLOW_LESSONS.md",
        ".ai/control/chunking_theological_decision_register.yaml",
        ".ai/control/bible_chunking_research_triage_map.yaml",
        ".ai/control/bible_wide_chunking_research_registry.yaml",
        ".ai/control/source_metadata_research_atlas.yaml",
        ".ai/control/apocalyptic_prophetic_intertext_dossier_queue.yaml",
        ".ai/control/epistle_argument_theological_issue_dossier_queue.yaml",
        ".ai/control/gospel_wj_discourse_dossier_queue.yaml",
        ".ai/control/divine_capitalization_inventory.yaml",
        ".ai/control/wj_marker_inventory.yaml",
        ".ai/control/wj_speaker_discourse_policy.yaml",
        ".ai/control/john3_wj_owner_review_docket.yaml",
    ):
        if required_path not in reading_by_path:
            raise PreflightError(f"{_rel(path)}: mandatory_reading missing {required_path}")

    registry_entry = reading_by_path["docs/methodology/LOGOS_CHUNKING_WORKFLOW_RULES_REGISTRY.md"]
    _require_subset(REQUIRED_RULE_IDS, registry_entry.get("required_rule_ids"), "required_rule_ids")
    decision_entry = reading_by_path[".ai/control/chunking_theological_decision_register.yaml"]
    _require_subset(REQUIRED_DECISION_IDS, decision_entry.get("required_decision_ids"), "required_decision_ids")
    triage_entry = reading_by_path[".ai/control/bible_chunking_research_triage_map.yaml"]
    _require_subset(REQUIRED_TRIAGE_LANES, triage_entry.get("required_lane_ids"), "required_lane_ids")
    lessons_entry = reading_by_path["docs/methodology/WORKFLOW_LESSONS.md"]
    _require_subset(
        REQUIRED_WORKFLOW_LESSON_IDS,
        lessons_entry.get("required_sections"),
        "workflow_lesson_required_sections",
    )

    registry_text = _read_text(RULE_REGISTRY)
    for rule_id in REQUIRED_RULE_IDS:
        if rule_id not in registry_text:
            raise PreflightError(f"{_rel(RULE_REGISTRY)}: missing {rule_id}")
    for phrase in (
        "Source metadata may be preserved",
        "internal cross-references",
        "Strong's-style",
        "graph-edge authority",
        "chunk-boundary authority",
    ):
        if phrase not in registry_text:
            raise PreflightError(f"{_rel(RULE_REGISTRY)}: missing metadata rule phrase {phrase!r}")

    supply_text = _read_text(SUPPLY_CHAIN)
    if "10o. Chunking-agent preflight and source-metadata rule" not in supply_text:
        raise PreflightError(f"{_rel(SUPPLY_CHAIN)}: missing 10o preflight rule")
    lessons_text = _read_text(WORKFLOW_LESSONS)
    for lesson_id in REQUIRED_WORKFLOW_LESSON_IDS:
        if lesson_id not in lessons_text:
            raise PreflightError(f"{_rel(WORKFLOW_LESSONS)}: missing {lesson_id}")
    register_text = _read_text(DECISION_REGISTER)
    for decision_id in REQUIRED_DECISION_IDS:
        if decision_id not in register_text:
            raise PreflightError(f"{_rel(DECISION_REGISTER)}: missing {decision_id}")
    triage_text = _read_text(TRIAGE_MAP)
    for phrase in (
        "divine_name_title_capitalization",
        "gospel_discourse_wj",
        "God/god",
        "Spirit/spirit",
        "Word/word",
        "graph edges",
    ):
        if phrase not in triage_text:
            raise PreflightError(f"{_rel(TRIAGE_MAP)}: missing divine capitalization phrase {phrase!r}")
    research_registry_text = _read_text(RESEARCH_REGISTRY)
    for phrase in (
        "object_type: bible_wide_chunking_research_registry",
        "book_count: 66",
        "John.3",
        "Rev.12.1-Rev.14.20",
        "source_metadata_features",
        "divine_name_title_capitalization",
        "authorizes_chunk_output_change: false",
        "reviewed_gold_promoted: false",
    ):
        if phrase not in research_registry_text:
            raise PreflightError(f"{_rel(RESEARCH_REGISTRY)}: missing registry phrase {phrase!r}")
    source_metadata_atlas_text = _read_text(SOURCE_METADATA_ATLAS)
    for phrase in (
        "object_type: source_metadata_research_atlas",
        "editorial_cross_references",
        "strongs_style_word_numbers",
        "wj_red_letter_markers",
        "divine_name_title_capitalization",
        "authorizes_graph_edges: false",
        "metadata_as_chunk_boundary",
    ):
        if phrase not in source_metadata_atlas_text:
            raise PreflightError(f"{_rel(SOURCE_METADATA_ATLAS)}: missing atlas phrase {phrase!r}")
    apocalyptic_queue_text = _read_text(APOCALYPTIC_INTERTEXT_QUEUE)
    for phrase in (
        "object_type: apocalyptic_prophetic_intertext_dossier_queue",
        "REV_DAN_SON_OF_MAN",
        "OLIVET_DANIEL_ABOMINATION",
        "EZEKIEL_TEMPLE_CITY_REVELATION_NEW_CREATION",
        "futurist",
        "preterist",
        "premillennial",
        "authorizes_graph_edges: false",
        "hermeneutic_system_selection",
    ):
        if phrase not in apocalyptic_queue_text:
            raise PreflightError(f"{_rel(APOCALYPTIC_INTERTEXT_QUEUE)}: missing queue phrase {phrase!r}")
    epistle_issue_queue_text = _read_text(EPISTLE_ISSUE_QUEUE)
    for phrase in (
        "object_type: epistle_argument_theological_issue_dossier_queue",
        "ROM9_11_ISRAEL_ELECTION_MERCY",
        "HEB7_10_PRIESTHOOD_COVENANT_SACRIFICE",
        "JAMES2_FAITH_WORKS_JUSTIFICATION",
        "reformed_or_augustinian_election_readings",
        "arminian_or_wesleyan_election_readings",
        "authorizes_doctrinal_system: false",
        "epistle_dossier_as_reviewed_gold",
    ):
        if phrase not in epistle_issue_queue_text:
            raise PreflightError(f"{_rel(EPISTLE_ISSUE_QUEUE)}: missing queue phrase {phrase!r}")
    gospel_wj_queue_text = _read_text(GOSPEL_WJ_QUEUE)
    for phrase in (
        "object_type: gospel_wj_discourse_dossier_queue",
        "JOHN3_WJ_SPEAKER_BOUNDARY",
        "MATT5_7_SERMON_ON_MOUNT_WJ_DISCOURSE",
        "REVELATION_WJ_VOICE_SHIFTS",
        "ACTS_EPISTLE_WJ_DOMINICAL_QUOTES",
        "authorizes_jesus_speaker_attribution: false",
        "authorizes_chunk_boundaries: false",
        "wj_dossier_as_reviewed_gold",
    ):
        if phrase not in gospel_wj_queue_text:
            raise PreflightError(f"{_rel(GOSPEL_WJ_QUEUE)}: missing queue phrase {phrase!r}")
    inventory_text = _read_text(CAPITALIZATION_INVENTORY)
    for phrase in (
        "object_type: divine_capitalization_inventory",
        "God/god",
        "Spirit/spirit",
        "Father/father",
        "Word/word",
        "authorizes_graph_edges: false",
        "authorizes_chunk_boundaries: false",
    ):
        if phrase not in inventory_text:
            raise PreflightError(f"{_rel(CAPITALIZATION_INVENTORY)}: missing inventory phrase {phrase!r}")
    wj_inventory_text = _read_text(WJ_MARKER_INVENTORY)
    for phrase in (
        "object_type: wj_marker_inventory",
        "authorizes_speaker_boundary: false",
        "authorizes_chunk_boundaries: false",
        "authorizes_graph_edges: false",
        "books_outside_four_gospels_with_wj",
        "John.3.10",
        "Rev.1.17",
    ):
        if phrase not in wj_inventory_text:
            raise PreflightError(f"{_rel(WJ_MARKER_INVENTORY)}: missing inventory phrase {phrase!r}")
    wj_policy_text = _read_text(WJ_SPEAKER_POLICY)
    for phrase in (
        "object_type: wj_speaker_discourse_policy",
        "WJ-SPK-001",
        "target_id: john3_wj_speaker_boundary",
        "passage: John.3.1-John.3.36",
        "authorizes_speaker_boundary: false",
        "authorizes_discourse_boundary: false",
        "authorizes_chunk_boundaries: false",
        "reviewed_gold_promoted: false",
    ):
        if phrase not in wj_policy_text:
            raise PreflightError(f"{_rel(WJ_SPEAKER_POLICY)}: missing policy phrase {phrase!r}")
    john3_docket_text = _read_text(JOHN3_OWNER_DOCKET)
    for phrase in (
        "object_type: john3_wj_owner_review_docket",
        "target_id: john3_wj_speaker_boundary",
        "passage: John.3.1-John.3.36",
        "owner_selection_status: pending",
        "selected_option: pending",
        "JOHN3-T356-B",
        "authorizes_chunk_boundaries: false",
        "reviewed_gold_promoted: false",
    ):
        if phrase not in john3_docket_text:
            raise PreflightError(f"{_rel(JOHN3_OWNER_DOCKET)}: missing docket phrase {phrase!r}")

    front_door_text = _read_text(FRONT_DOOR)
    for phrase in REQUIRED_FRONT_DOOR_STRINGS:
        if phrase not in front_door_text:
            raise PreflightError(f"{_rel(FRONT_DOOR)}: missing required preflight phrase {phrase!r}")
    workflow_text = _read_text(ROOT / ".ai" / "workflows" / "chunking-skill-supply-chain.workflow.md")
    for phrase in (
        "Midflight Lesson Capture",
        "What did this task teach",
        "update `.ai/control/chunking_agent_preflight.yaml`",
    ):
        if phrase not in workflow_text:
            raise PreflightError(f".ai/workflows/chunking-skill-supply-chain.workflow.md: missing {phrase!r}")

    return data


def main() -> int:
    try:
        validate_preflight()
    except PreflightError as exc:
        print(f"Chunking-agent preflight validation failed: {exc}", file=sys.stderr)
        return 1
    print("Chunking-agent preflight validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
