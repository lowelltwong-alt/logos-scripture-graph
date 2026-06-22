#!/usr/bin/env python3
"""Validate the T384 Bible-wide research/readiness synthesis."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
SYNTHESIS = ROOT / ".ai" / "control" / "t384_bible_wide_research_readiness_synthesis.yaml"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
LESSON_INDEX = ROOT / ".ai" / "control" / "chunking_lesson_index.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
REGISTRY = ROOT / ".ai" / "control" / "bible_wide_chunking_research_registry.yaml"
ROADMAP = ROOT / "ROADMAP_STATE.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
MAIN_TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"
ROADMAP_DOC = ROOT / "docs" / "roadmap" / "T384_BIBLE_WIDE_RESEARCH_READINESS_SYNTHESIS.md"
TASK = ROOT / ".ai" / "tasks" / "T384.task.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T384" / "handoff.md"
AUDIT_README = ROOT / ".ai" / "audits" / "reports" / "README.md"
AUDIT = ROOT / ".ai" / "audits" / "reports" / "20260621-T384-bible-wide-research-readiness.md"

SYNTHESIS_REL = ".ai/control/t384_bible_wide_research_readiness_synthesis.yaml"
VALIDATOR_REL = "scripts/validate_t384_bible_wide_research_readiness.py"
DOC_REL = "docs/roadmap/T384_BIBLE_WIDE_RESEARCH_READINESS_SYNTHESIS.md"

REQUIRED_AUTHORITY_FALSE = {
    "authorizes_exact_target_selection",
    "authorizes_reviewed_gold_promotion",
    "authorizes_child_spans",
    "authorizes_chunk_output_change",
    "authorizes_route_behavior_change",
    "authorizes_evaluator_change",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_embedding_or_vector_work",
    "authorizes_boundary_import",
    "authorizes_whole_bible_output_pass",
    "authorizes_preferred_reading_or_source_tradition",
    "authorizes_canon_scope_change",
    "authorizes_denominational_systematic_theology_as_chunk_authority",
}

REQUIRED_READY_LANES = {
    "epistle_argument",
    "gospel_discourse_wj",
    "source_metadata_and_original_language",
}

REQUIRED_MORE_RESEARCH_LANES = {
    "revelation_apocalyptic",
    "narrative_legal_covenant",
    "wisdom_dialogue_poetry",
    "prophetic_oracle_vision",
    "textual_variant_source_tradition",
}

REQUIRED_BLOCKERS = {
    "BLOCK-001",
    "BLOCK-002",
    "BLOCK-003",
    "BLOCK-004",
}

REQUIRED_HUMAN_DECISIONS = {
    "HDM-001",
    "HDM-002",
    "HDM-003",
    "HDM-004",
    "HDM-005",
    "HDM-006",
    "HDM-007",
}

REQUIRED_T384_OPTIONS = {
    "T384-A",
    "T384-B",
    "T384-C",
    "T384-D",
    "T384-E",
    "T384-F",
}

REQUIRED_NEXT_FALSE = {
    "output_change_authorized",
    "implementation_authorized",
    "reviewed_gold_promoted",
    "route_behavior_authorized",
    "evaluator_change_authorized",
    "child_spans_authorized",
    "graph_edge_generation_allowed",
    "retrieval_truth_authorized",
    "embedding_or_vector_work_allowed",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "exact_target_selection",
    "reviewed_gold_promotion",
    "child_span_selection",
    "child_span_reviewed_gold_promotion",
    "chunk_output_change",
    "route_behavior_change",
    "evaluator_change",
    "graph_edge_generation",
    "retrieval_truth",
    "embedding_or_vector_work",
    "boundary_import",
    "whole_bible_output_pass",
    "preferred_reading_selection",
    "source_tradition_preference",
    "canon_scope_change",
    "denominational_systematic_theology_as_chunk_authority",
    "liberal_critical_default",
    "anti_supernatural_default",
}


class T384ReadinessError(ValueError):
    """Raised when the T384 synthesis loses readiness, audit, or authority boundaries."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise T384ReadinessError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise T384ReadinessError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise T384ReadinessError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    if not isinstance(actual, list):
        raise T384ReadinessError(f"{label} must be a list")
    missing = sorted(required - {str(item) for item in actual})
    if missing:
        raise T384ReadinessError(f"{label} missing {missing}")


def _require_lane_ids(required: set[str], actual: Any, label: str) -> None:
    if not isinstance(actual, list):
        raise T384ReadinessError(f"{label} must be a list")
    lane_ids = {item.get("lane_id") for item in actual if isinstance(item, dict)}
    missing = sorted(required - lane_ids)
    if missing:
        raise T384ReadinessError(f"{label} missing lane ids {missing}")


def _require_ids(required: set[str], actual: Any, label: str, key: str) -> None:
    if not isinstance(actual, list):
        raise T384ReadinessError(f"{label} must be a list")
    ids = {item.get(key) for item in actual if isinstance(item, dict)}
    missing = sorted(required - ids)
    if missing:
        raise T384ReadinessError(f"{label} missing {missing}")


def _validate_static(synthesis: dict[str, Any]) -> None:
    expected = {
        "object_type": "bible_wide_chunking_research_readiness_synthesis",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "t384_bible_wide_research_readiness_synthesis.v1",
        "synthesis_id": "t384_bible_wide_chunking_research_readiness",
        "task_id": "T384",
        "status": "complete_bible_wide_research_readiness_synthesis",
        "owner": "Lowell Wong",
    }
    for key, value in expected.items():
        if synthesis.get(key) != value:
            raise T384ReadinessError(f"{SYNTHESIS_REL}: {key} must be {value!r}")

    goal = synthesis.get("goal_completed")
    if not isinstance(goal, dict):
        raise T384ReadinessError(f"{SYNTHESIS_REL}: goal_completed must be a mapping")
    if goal.get("completed_as_non_output_changing_research_readiness") is not True:
        raise T384ReadinessError(f"{SYNTHESIS_REL}: goal must complete as non-output readiness")
    if goal.get("does_not_mean_chunking_ready_for_output") is not True:
        raise T384ReadinessError(f"{SYNTHESIS_REL}: goal must deny output readiness")

    authority = synthesis.get("authority")
    if not isinstance(authority, dict):
        raise T384ReadinessError(f"{SYNTHESIS_REL}: authority must be a mapping")
    for required_true in (
        "records_research_readiness",
        "records_human_decision_needs",
        "records_next_non_output_step",
    ):
        if authority.get(required_true) is not True:
            raise T384ReadinessError(f"{SYNTHESIS_REL}: authority.{required_true} must be true")
    for key in REQUIRED_AUTHORITY_FALSE:
        if authority.get(key) is not False:
            raise T384ReadinessError(f"{SYNTHESIS_REL}: authority.{key} must be false")

    boundary = synthesis.get("orthodoxy_boundary")
    if not isinstance(boundary, dict):
        raise T384ReadinessError(f"{SYNTHESIS_REL}: orthodoxy_boundary must be a mapping")
    if boundary.get("default") != "nicene_chalcedonian_core":
        raise T384ReadinessError(f"{SYNTHESIS_REL}: orthodoxy boundary must be Nicene/Chalcedonian")
    if boundary.get("canonical_scripture_authority") is not True:
        raise T384ReadinessError(f"{SYNTHESIS_REL}: canonical Scripture authority must stay true")

    sources = synthesis.get("required_source_surfaces")
    if not isinstance(sources, dict):
        raise T384ReadinessError(f"{SYNTHESIS_REL}: required_source_surfaces must be a mapping")
    required_source_paths = {
        ".ai/control/bible_wide_chunking_research_registry.yaml",
        ".ai/control/bible_chunking_readiness_map.yaml",
        ".ai/control/chunking_human_decision_forecast.yaml",
        ".ai/control/source_metadata_research_atlas.yaml",
        ".ai/control/contextual_reading_policy.yaml",
        ".ai/control/original_language_phrase_context_policy.yaml",
        ".ai/control/orthodox_hermeneutic_firewall_docket.yaml",
    }
    actual_paths = {
        item.get("path")
        for item in sources.values()
        if isinstance(item, dict)
    }
    missing_paths = sorted(required_source_paths - actual_paths)
    if missing_paths:
        raise T384ReadinessError(f"{SYNTHESIS_REL}: missing source surfaces {missing_paths}")

    coverage = synthesis.get("coverage")
    if not isinstance(coverage, dict):
        raise T384ReadinessError(f"{SYNTHESIS_REL}: coverage must be a mapping")
    if coverage.get("corpus_scope") != "canonical_66":
        raise T384ReadinessError(f"{SYNTHESIS_REL}: coverage.corpus_scope must be canonical_66")
    if coverage.get("bible_wide_research_registry_book_count") != 66:
        raise T384ReadinessError(f"{SYNTHESIS_REL}: book count must be 66")
    _require_subset(
        {
            "seeded_needs_research",
            "research_first",
            "review_packet_pending",
            "governed_hold_existing_gold",
            "owner_decision_pending",
        },
        coverage.get("registry_statuses_observed"),
        "coverage.registry_statuses_observed",
    )

    _require_lane_ids(
        REQUIRED_READY_LANES,
        synthesis.get("what_is_ready_for_review_packet_strengthening"),
        "what_is_ready_for_review_packet_strengthening",
    )
    _require_lane_ids(
        REQUIRED_MORE_RESEARCH_LANES,
        synthesis.get("what_needs_more_research"),
        "what_needs_more_research",
    )
    _require_ids(
        REQUIRED_BLOCKERS,
        synthesis.get("what_must_remain_blocked"),
        "what_must_remain_blocked",
        "blocker_id",
    )
    _require_ids(
        REQUIRED_HUMAN_DECISIONS,
        synthesis.get("human_decisions_required"),
        "human_decisions_required",
        "decision_id",
    )

    human = synthesis["human_decisions_required"]
    hdm001 = next(item for item in human if item["decision_id"] == "HDM-001")
    options = hdm001.get("faithful_options")
    if not isinstance(options, list):
        raise T384ReadinessError(f"{SYNTHESIS_REL}: HDM-001 faithful_options must be a list")
    option_ids = {item.get("option_id") for item in options if isinstance(item, dict)}
    missing_options = sorted(REQUIRED_T384_OPTIONS - option_ids)
    if missing_options:
        raise T384ReadinessError(f"{SYNTHESIS_REL}: HDM-001 missing {missing_options}")
    if "selection_by_this_synthesis" not in hdm001.get("non_authorizations", []):
        raise T384ReadinessError(f"{SYNTHESIS_REL}: HDM-001 must deny selection by this synthesis")

    next_step = synthesis.get("exact_next_non_output_step")
    if not isinstance(next_step, dict):
        raise T384ReadinessError(f"{SYNTHESIS_REL}: exact_next_non_output_step must be a mapping")
    expected_next = {
        "task_id": "T385",
        "title": "Owner Decision Packet From T384 Research Readiness Synthesis",
        "route_type": "owner_decision_packet_only",
        "starts_only_if": "T384_bible_wide_research_readiness_synthesis_complete",
        "required_input": SYNTHESIS_REL,
        "owner_decision_required_before_promotion_or_implementation": True,
    }
    for key, value in expected_next.items():
        if next_step.get(key) != value:
            raise T384ReadinessError(f"{SYNTHESIS_REL}: exact_next_non_output_step.{key} must be {value!r}")
    for key in REQUIRED_NEXT_FALSE:
        if next_step.get(key) is not False:
            raise T384ReadinessError(f"{SYNTHESIS_REL}: exact_next_non_output_step.{key} must be false")

    _require_subset(REQUIRED_NON_AUTHORIZATIONS, synthesis.get("non_authorizations"), "non_authorizations")
    lesson = synthesis.get("lesson_recorded")
    if not isinstance(lesson, dict) or lesson.get("lesson_id") != "LSN-013":
        raise T384ReadinessError(f"{SYNTHESIS_REL}: lesson_recorded.lesson_id must be LSN-013")
    if synthesis.get("decision_register_entry") != "CD-061":
        raise T384ReadinessError(f"{SYNTHESIS_REL}: decision_register_entry must be CD-061")


def _validate_registry_count() -> None:
    registry = _read_yaml(REGISTRY)
    books = registry.get("book_research_queue")
    if not isinstance(books, list) or len(books) != 66:
        raise T384ReadinessError(f"{_rel(REGISTRY)}: book_research_queue must contain 66 books")


def _validate_links() -> None:
    linked_requirements = (
        (REGISTER, ("CD-061", "T384 completes Bible-wide research/readiness synthesis", SYNTHESIS_REL)),
        (PREFLIGHT, ("CD-061", "LSN-013", SYNTHESIS_REL, "Bible-wide research readiness must be synthesized before chunking resumes")),
        (LESSON_INDEX, ("LSN-013", "Bible-wide research readiness must be synthesized before chunking resumes", "T384", SYNTHESIS_REL)),
        (READINESS, ("task_id: T384", SYNTHESIS_REL, "exact_next_non_output_step: T385")),
        (ROADMAP, ("id: T384", "complete_bible_wide_research_readiness_synthesis", "id: T385")),
        (FRONT_DOOR, (SYNTHESIS_REL, VALIDATOR_REL, "T385 owner decision packet")),
        (MAIN_TOC, (SYNTHESIS_REL, VALIDATOR_REL, "bible-wide-readiness")),
        (ROADMAP_TOC, (SYNTHESIS_REL, DOC_REL, "T384 | Bible-wide research readiness synthesis")),
        (ROADMAP_DOC, (SYNTHESIS_REL, "HDM-001", "T385")),
        (TASK, ("id: T384", "CD-061", "LSN-013")),
        (HANDOFF, ("task_id: T384", "CD-061", "T385")),
        (AUDIT_README, ("20260621-T384-bible-wide-research-readiness.md", "T384")),
        (AUDIT, ("T384 No-Context Audit Surface", "CD-061", "T385")),
    )
    for path, phrases in linked_requirements:
        text = _read_text(path)
        for phrase in phrases:
            if phrase not in text:
                raise T384ReadinessError(f"{_rel(path)}: missing {phrase!r}")


def validate_t384_bible_wide_research_readiness(path: Path = SYNTHESIS) -> dict[str, Any]:
    synthesis = _read_yaml(path)
    _validate_static(synthesis)
    _validate_registry_count()
    _validate_links()
    return synthesis


def main() -> int:
    try:
        validate_t384_bible_wide_research_readiness()
    except T384ReadinessError as exc:
        print(f"T384 Bible-wide research/readiness validation failed: {exc}", file=sys.stderr)
        return 1
    print("T384 Bible-wide research/readiness validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
