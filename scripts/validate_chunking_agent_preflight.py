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
NARRATIVE_LEGAL_QUEUE = ROOT / ".ai" / "control" / "narrative_legal_covenant_dossier_queue.yaml"
WISDOM_POETRY_QUEUE = ROOT / ".ai" / "control" / "wisdom_dialogue_poetry_dossier_queue.yaml"
PROPHETIC_ORACLE_QUEUE = ROOT / ".ai" / "control" / "prophetic_oracle_vision_dossier_queue.yaml"
TEXTUAL_VARIANT_QUEUE = ROOT / ".ai" / "control" / "textual_variant_source_tradition_dossier_queue.yaml"
ORTHODOX_LANGUAGE_PRESSURE_QUEUE = ROOT / ".ai" / "control" / "orthodox_original_language_pressure_dossier_queue.yaml"
ORTHODOX_FIREWALL = ROOT / ".ai" / "control" / "orthodox_hermeneutic_firewall_docket.yaml"
TEXTUAL_CRITICAL_DOCKET = ROOT / ".ai" / "control" / "textual_critical_policy_docket.yaml"
TEXTUAL_CRITICAL_OPTIONS = ROOT / ".ai" / "control" / "textual_critical_policy_owner_options.yaml"
TEXTUAL_CRITICAL_CASE_POLICY = ROOT / ".ai" / "control" / "textual_critical_case_policy.yaml"
T371_DECISION_PACKET = ROOT / ".ai" / "control" / "t371_variant_dependency_owner_decision_packet.yaml"
T371_PROMOTION_RECORD = ROOT / ".ai" / "control" / "t371_parent_only_reviewed_gold_promotion.yaml"
T372_HARNESS_PLAN = ROOT / ".ai" / "control" / "t372_route_isolation_harness_plan.yaml"
ONECOR_OWNER_DOCKET = ROOT / ".ai" / "control" / "1cor8_10_epistle_owner_review_docket.yaml"
ONECOR_EVIDENCE_PACKET = ROOT / "eval" / "chunking_gold" / "review_packets" / "1cor8_10_parent_only_evidence_packet.yaml"
EPISTLE_ARGUMENT_GOLD_MANIFEST = ROOT / "eval" / "chunking_gold" / "per_form" / "epistle_argument_gold_manifest.json"
HUMAN_DECISION_FORECAST = ROOT / ".ai" / "control" / "chunking_human_decision_forecast.yaml"
GOVERNANCE_MEMORY_DURABILITY = ROOT / ".ai" / "control" / "governance_memory_durability_policy.yaml"
OWNER_DECISION_PROJECTION = ROOT / ".ai" / "control" / "owner_decision_projection_policy.yaml"
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

REQUIRED_DECISION_IDS = {"CD-015", "CD-018", "CD-021", "CD-022", "CD-023", "CD-024", "CD-025", "CD-026", "CD-027", "CD-028", "CD-029", "CD-030", "CD-031", "CD-032", "CD-033", "CD-034", "CD-035", "CD-036", "CD-037", "CD-038", "CD-039", "CD-040", "CD-041", "CD-042", "CD-043", "CD-044", "CD-045", "CD-046", "CD-047", "CD-048"}

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
    "narrative_legal_covenant_dossier_queue.yaml",
    "wisdom_dialogue_poetry_dossier_queue.yaml",
    "prophetic_oracle_vision_dossier_queue.yaml",
    "textual_variant_source_tradition_dossier_queue.yaml",
    "orthodox_original_language_pressure_dossier_queue.yaml",
    "orthodox_hermeneutic_firewall_docket.yaml",
    "textual_critical_policy_docket.yaml",
    "textual_critical_policy_owner_options.yaml",
    "textual_critical_case_policy.yaml",
    "t371_variant_dependency_owner_decision_packet.yaml",
    "t371_parent_only_reviewed_gold_promotion.yaml",
    "t372_route_isolation_harness_plan.yaml",
    "validate_t372_route_isolation_harness_plan.py",
    "epistle_argument_gold_manifest.json",
    "1cor8_10_epistle_owner_review_docket.yaml",
    "1cor8_10_parent_only_evidence_packet.yaml",
    "validate_1cor8_10_parent_evidence_packet.py",
    "chunking_human_decision_forecast.yaml",
    "governance_memory_durability_policy.yaml",
    "owner_decision_projection_policy.yaml",
    "conflicting prior owner decisions",
    "projected owner pattern",
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
        ".ai/control/narrative_legal_covenant_dossier_queue.yaml",
        ".ai/control/wisdom_dialogue_poetry_dossier_queue.yaml",
        ".ai/control/prophetic_oracle_vision_dossier_queue.yaml",
        ".ai/control/textual_variant_source_tradition_dossier_queue.yaml",
        ".ai/control/orthodox_original_language_pressure_dossier_queue.yaml",
        ".ai/control/orthodox_hermeneutic_firewall_docket.yaml",
        ".ai/control/textual_critical_policy_docket.yaml",
        ".ai/control/textual_critical_policy_owner_options.yaml",
        ".ai/control/textual_critical_case_policy.yaml",
        ".ai/control/t371_variant_dependency_owner_decision_packet.yaml",
        ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml",
        ".ai/control/t372_route_isolation_harness_plan.yaml",
        ".ai/control/1cor8_10_epistle_owner_review_docket.yaml",
        "eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml",
        "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json",
        ".ai/control/chunking_human_decision_forecast.yaml",
        ".ai/control/governance_memory_durability_policy.yaml",
        ".ai/control/owner_decision_projection_policy.yaml",
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
    narrative_legal_queue_text = _read_text(NARRATIVE_LEGAL_QUEUE)
    for phrase in (
        "object_type: narrative_legal_covenant_dossier_queue",
        "GEN1_11_PRIMEVAL_NARRATIVE_GENEALOGY",
        "EXOD19_24_SINAI_COVENANT_NARRATIVE_LAW",
        "LEV1_7_SACRIFICE_RITUAL_LAW",
        "JOSH13_21_LAND_ALLOTMENT_LISTS",
        "MATT_LUKE_GENEALOGY_BIRTH_NARRATIVE",
        "authorizes_covenant_theology: false",
        "authorizes_chunk_boundaries: false",
        "narrative_dossier_as_reviewed_gold",
    ):
        if phrase not in narrative_legal_queue_text:
            raise PreflightError(f"{_rel(NARRATIVE_LEGAL_QUEUE)}: missing queue phrase {phrase!r}")
    wisdom_poetry_queue_text = _read_text(WISDOM_POETRY_QUEUE)
    for phrase in (
        "object_type: wisdom_dialogue_poetry_dossier_queue",
        "JOB_DIALOGUE_CYCLES_AND_DIVINE_SPEECHES",
        "PROV31_ACROSTIC_WISDOM_POEM",
        "SONG_SPEAKER_BOUNDARY_AND_GENRE",
        "LAMENTATIONS_ACROSTIC_LAMENT_UNITS",
        "PS119_ACROSTIC_TORAH_PSALM",
        "authorizes_speaker_boundary: false",
        "authorizes_chunk_boundaries: false",
        "wisdom_dossier_as_reviewed_gold",
    ):
        if phrase not in wisdom_poetry_queue_text:
            raise PreflightError(f"{_rel(WISDOM_POETRY_QUEUE)}: missing queue phrase {phrase!r}")
    prophetic_oracle_queue_text = _read_text(PROPHETIC_ORACLE_QUEUE)
    for phrase in (
        "object_type: prophetic_oracle_vision_dossier_queue",
        "ISA40_55_SERVANT_COMFORT_ORACLES",
        "JER30_33_RESTORATION_NEW_COVENANT",
        "EZEK40_48_TEMPLE_CITY_VISION",
        "DAN7_12_PROPHETIC_APOCALYPTIC_VISIONS",
        "ZECH1_6_NIGHT_VISIONS",
        "authorizes_fulfillment_theology: false",
        "authorizes_chunk_boundaries: false",
        "prophetic_dossier_as_reviewed_gold",
    ):
        if phrase not in prophetic_oracle_queue_text:
            raise PreflightError(f"{_rel(PROPHETIC_ORACLE_QUEUE)}: missing queue phrase {phrase!r}")
    textual_variant_queue_text = _read_text(TEXTUAL_VARIANT_QUEUE)
    for phrase in (
        "object_type: textual_variant_source_tradition_dossier_queue",
        "MARK16_LONGER_ENDING",
        "JOHN7_53_8_11_PERICOPE_ADULTERAE",
        "DEUT32_8_9_SONS_OF_GOD_VARIANT",
        "JUDE_NONCANONICAL_REFERENCE_SENSITIVITY",
        "ONEJOHN5_7_COMMA_JOHANNEUM",
        "authorizes_textual_critical_decision: false",
        "authorizes_boundary_import: false",
        "textual_variant_dossier_as_reviewed_gold",
    ):
        if phrase not in textual_variant_queue_text:
            raise PreflightError(f"{_rel(TEXTUAL_VARIANT_QUEUE)}: missing queue phrase {phrase!r}")
    orthodox_language_pressure_queue_text = _read_text(ORTHODOX_LANGUAGE_PRESSURE_QUEUE)
    for phrase in (
        "object_type: orthodox_original_language_pressure_dossier_queue",
        "JOHN1_1_LOGOS_THEOS_GRAMMAR",
        "COL1_15_20_FIRSTBORN_ALL_THINGS",
        "GEN1_26_ELOHIM_US_IMAGE",
        "ISA43_44_ONE_GOD_LDS_POLYTHEISM",
        "authorizes_nonorthodox_source_authority: false",
        "authorizes_extra_canonical_source_authority: false",
        "original_language_as_automatic_truth",
    ):
        if phrase not in orthodox_language_pressure_queue_text:
            raise PreflightError(f"{_rel(ORTHODOX_LANGUAGE_PRESSURE_QUEUE)}: missing queue phrase {phrase!r}")
    orthodox_firewall_text = _read_text(ORTHODOX_FIREWALL)
    for phrase in (
        "object_type: orthodox_hermeneutic_firewall_docket",
        "Nicene/Chalcedonian orthodox Christianity",
        "Canonical Scripture",
        "authorizes_liberal_critical_default: false",
        "authorizes_anti_supernatural_default: false",
        "authorizes_denominational_system_as_chunk_authority: false",
        "FIREWALL-ORTH-005",
    ):
        if phrase not in orthodox_firewall_text:
            raise PreflightError(f"{_rel(ORTHODOX_FIREWALL)}: missing firewall phrase {phrase!r}")
    textual_critical_text = _read_text(TEXTUAL_CRITICAL_DOCKET)
    for phrase in (
        "object_type: textual_critical_policy_docket",
        "requires_policy_before_variant_sensitive_promotion: true",
        "textual_critical_policy_selected: true",
        "selected_policy: TCP-T378-B",
        "selected_policy_record: .ai/control/textual_critical_case_policy.yaml",
        "owner_confirmation_required_per_variant_sensitive_promotion: true",
        "authorizes_textual_critical_decision: false",
        "authorizes_canon_scope_change: false",
        "variant_packet_as_reviewed_gold",
    ):
        if phrase not in textual_critical_text:
            raise PreflightError(f"{_rel(TEXTUAL_CRITICAL_DOCKET)}: missing textual-critical phrase {phrase!r}")
    textual_critical_options_text = _read_text(TEXTUAL_CRITICAL_OPTIONS)
    for phrase in (
        "object_type: textual_critical_policy_owner_options_docket",
        "TCP-T378-B",
        "case-by-case",
        "1Cor.9.20",
        "1Cor.10.9",
        "blocks_t371_until_selected: false",
        "selection_record: .ai/control/textual_critical_case_policy.yaml",
        "authorizes_preferred_reading: false",
        "authorizes_reviewed_gold: false",
    ):
        if phrase not in textual_critical_options_text:
            raise PreflightError(f"{_rel(TEXTUAL_CRITICAL_OPTIONS)}: missing textual-critical options phrase {phrase!r}")
    textual_critical_case_policy_text = _read_text(TEXTUAL_CRITICAL_CASE_POLICY)
    for phrase in (
        "object_type: textual_critical_case_policy",
        "selected_option: TCP-T378-B",
        "case-by-case owner policy",
        "required_before_each_variant_sensitive_promotion",
        "boundary_dependency_or_non_dependency",
        "reviewed_gold_dependency_or_non_dependency",
        "owner_confirmation",
        "ODP-005",
        "authorizes_preferred_reading: false",
        "authorizes_reviewed_gold: false",
        "authorizes_chunk_output_change: false",
    ):
        if phrase not in textual_critical_case_policy_text:
            raise PreflightError(f"{_rel(TEXTUAL_CRITICAL_CASE_POLICY)}: missing case-policy phrase {phrase!r}")
    t371_packet_text = _read_text(T371_DECISION_PACKET)
    for phrase in (
        "object_type: variant_dependency_owner_decision_packet",
        "target_owner_task: T371",
        "status: resolved_by_t371_a",
        "1Cor.9.20",
        "1Cor.10.9",
        "T371-A",
        "T371-B",
        "owner_response_record: .ai/control/t371_parent_only_reviewed_gold_promotion.yaml",
        "authorizes_variant_non_dependency_finding: false",
        "authorizes_reviewed_gold_promotion: false",
        "authorizes_chunk_output_change: false",
    ):
        if phrase not in t371_packet_text:
            raise PreflightError(f"{_rel(T371_DECISION_PACKET)}: missing T371 packet phrase {phrase!r}")
    promotion_text = _read_text(T371_PROMOTION_RECORD)
    for phrase in (
        "object_type: parent_only_reviewed_gold_promotion_record",
        "selected_option: T371-A",
        "selected_parent: 1Cor.8.1-1Cor.10.33",
        "boundary_dependency_or_non_dependency: variant_non_dependent",
        "reviewed_gold_dependency_or_non_dependency: variant_non_dependent",
        "authorizes_parent_only_reviewed_gold_promotion: true",
        "authorizes_chunk_output_change: false",
        "next_allowed_task: T372",
    ):
        if phrase not in promotion_text:
            raise PreflightError(f"{_rel(T371_PROMOTION_RECORD)}: missing promotion phrase {phrase!r}")
    t372_plan_text = _read_text(T372_HARNESS_PLAN)
    for phrase in (
        "object_type: route_isolation_harness_plan",
        "task_id: T372",
        "status: complete_non_output_changing_plan",
        "authorizes_route_behavior: false",
        "authorizes_chunk_output_change: false",
        "T372-HARN-003",
        "non_target_identity_proof",
        "next_task_id: T373",
        "parent_only_gold_as_chunk_boundary",
    ):
        if phrase not in t372_plan_text:
            raise PreflightError(f"{_rel(T372_HARNESS_PLAN)}: missing T372 plan phrase {phrase!r}")
    onecor_docket_text = _read_text(ONECOR_OWNER_DOCKET)
    for phrase in (
        "object_type: epistle_argument_owner_review_docket",
        "target_id: 1cor8_10_food_offered_to_idols",
        "exact_parent_candidate: 1Cor.8.1-1Cor.10.33",
        "owner_selection_status: selected",
        "selection_mode: projected_owner_pattern",
        "selected_option: 1COR8-10-T369-B",
        "1COR8-10-T369-C",
        "authorizes_reviewed_gold: false",
        "authorizes_chunk_boundaries: false",
        "chunk_output_change",
    ):
        if phrase not in onecor_docket_text:
            raise PreflightError(f"{_rel(ONECOR_OWNER_DOCKET)}: missing 1Cor.8-10 docket phrase {phrase!r}")
    evidence_packet_text = _read_text(ONECOR_EVIDENCE_PACKET)
    for phrase in (
        "object_type: parent_only_review_evidence_packet",
        "selected_parent: 1Cor.8.1-1Cor.10.33",
        "selected_children: []",
        "review_status: ready_for_owner_promotion_review",
        "reviewed_gold_promoted: false",
        "authorizes_output_change: false",
        "strong_style_numbers_are_metadata_not_lexical_or_theological_truth",
        "capitalization_is_translation_evidence_not_divine_identity_or_chunk_authority",
        "stop and surface the conflict",
    ):
        if phrase not in evidence_packet_text:
            raise PreflightError(f"{_rel(ONECOR_EVIDENCE_PACKET)}: missing evidence-packet phrase {phrase!r}")
    manifest_text = _read_text(EPISTLE_ARGUMENT_GOLD_MANIFEST)
    for phrase in (
        '"manifest_id": "epistle-argument-gold-v0"',
        '"case_id": "1cor8_10_parent_only_reviewed_gold"',
        '"osis_span": "1Cor.8.1-1Cor.10.33"',
        '"selected_option": "T371-A"',
        '"selected_children": []',
        '"chunk_output_change_authorized": false',
    ):
        if phrase not in manifest_text:
            raise PreflightError(f"{_rel(EPISTLE_ARGUMENT_GOLD_MANIFEST)}: missing manifest phrase {phrase!r}")
    forecast_text = _read_text(HUMAN_DECISION_FORECAST)
    for phrase in (
        "object_type: chunking_human_decision_forecast",
        "HDF-001",
        "HDF-012",
        "thread_goal_status: blocked",
        "ready_for_first_output_changing_chunk_pr_requires",
        "authorizes_chunk_output_change: false",
        "do_not_treat_this_forecast_as_authorization",
    ):
        if phrase not in forecast_text:
            raise PreflightError(f"{_rel(HUMAN_DECISION_FORECAST)}: missing human-decision forecast phrase {phrase!r}")
    durability_text = _read_text(GOVERNANCE_MEMORY_DURABILITY)
    for phrase in (
        "object_type: governance_memory_durability_policy",
        "critical_non_deletable_governance_memory",
        "authorizes_register_deletion: false",
        "chunking_theological_decision_register.yaml",
        "bypassing_register_validator",
    ):
        if phrase not in durability_text:
            raise PreflightError(f"{_rel(GOVERNANCE_MEMORY_DURABILITY)}: missing durability phrase {phrase!r}")
    projection_text = _read_text(OWNER_DECISION_PROJECTION)
    for phrase in (
        "object_type: owner_decision_projection_policy",
        "conflict_scan_required_for_every_projected_decision: true",
        "prior_owner_decisions_conflict_for_the_target_text",
        "ODP-20260618-1COR8-10-PARENT",
        "ODP-005",
        "selected_option: 1COR8-10-T369-B",
        "child_span_projection",
    ):
        if phrase not in projection_text:
            raise PreflightError(f"{_rel(OWNER_DECISION_PROJECTION)}: missing projection phrase {phrase!r}")
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
        "owner_selection_status: selected",
        "selected_option: JOHN3-T356-B",
        "selected_parent: John.3.1-John.3.36",
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
