#!/usr/bin/env python3
"""Validate the T399 focused Bible-wide research queue."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / ".ai" / "control" / "t399_focused_bible_wide_research_queue.yaml"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
LESSON_INDEX = ROOT / ".ai" / "control" / "chunking_lesson_index.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
ROADMAP = ROOT / "ROADMAP_STATE.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
MAIN_TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"
ROADMAP_DOC = ROOT / "docs" / "roadmap" / "T399_FOCUSED_BIBLE_WIDE_RESEARCH_QUEUE.md"
TASK = ROOT / ".ai" / "tasks" / "T399.task.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T399" / "handoff.md"
AUDIT = ROOT / ".ai" / "audits" / "reports" / "20260624-T399-focused-bible-wide-research-queue.md"
AUDIT_README = ROOT / ".ai" / "audits" / "reports" / "README.md"
VALIDATE_ALL = ROOT / "scripts" / "validate_all.py"

QUEUE_REL = ".ai/control/t399_focused_bible_wide_research_queue.yaml"
VALIDATOR_REL = "scripts/validate_t399_focused_bible_wide_research_queue.py"
ROADMAP_DOC_REL = "docs/roadmap/T399_FOCUSED_BIBLE_WIDE_RESEARCH_QUEUE.md"

REQUIRED_FALSE_AUTHORITY = {
    "authorizes_exact_target_selection",
    "authorizes_review_packet_strengthening_without_owner_selection",
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
    "authorizes_source_or_manuscript_row_population",
    "authorizes_denominational_systematic_theology_as_chunk_authority",
}

REQUIRED_SOURCE_INPUTS = {
    ".ai/control/t398_bible_wide_phase_one_research_synthesis.yaml",
    ".ai/control/bible_verse_passage_coverage_summary.yaml",
    ".ai/control/bible_verse_passage_readiness_matrix.yaml",
    ".ai/control/bible_verse_passage_gap_register.yaml",
    ".ai/control/bible_verse_passage_human_review_docket.yaml",
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
    ".ai/control/original_language_phrase_context_policy.yaml",
    ".ai/control/contextual_reading_policy.yaml",
    ".ai/control/orthodox_hermeneutic_firewall_docket.yaml",
    ".ai/control/manuscript_source_catalog_metadata_plan.yaml",
    ".ai/control/manuscript_source_catalog_research_packet.yaml",
    ".ai/control/manuscript_source_catalog_sqlite_shell.yaml",
}

REQUIRED_CANDIDATES = {
    "T399-Q001",
    "T399-Q002",
    "T399-Q003",
    "T399-Q004",
    "T399-Q005",
    "T399-Q006",
    "T399-Q007",
    "T399-Q008",
    "T399-Q009",
    "T399-Q010",
    "T399-Q011",
    "T399-Q012",
    "T399-Q013",
    "T399-Q014",
    "T399-Q015",
    "T399-Q016",
    "T399-Q017",
    "T399-Q018",
    "T399-Q019",
    "T399-Q020",
    "T399-Q021",
    "T399-Q022",
}

REQUIRED_LANES = {
    "epistle_argument",
    "gospel_discourse_wj",
    "acts_narrative_speech_transition",
    "revelation_apocalyptic",
    "narrative_legal_covenant",
    "textual_variant_source_tradition",
    "wisdom_dialogue_poetry",
    "prophetic_oracle_vision",
    "original_language_pressure",
}

REQUIRED_QUEUE_FIELDS = {
    "rank",
    "candidate_id",
    "lane_id",
    "title",
    "candidate_passages",
    "score",
    "source_basis",
    "why_may_affect_chunking",
    "theological_or_hermeneutical_risks",
    "variant_source_tradition_dependency",
    "source_metadata_evidence_needs",
    "original_language_phrase_context_needs",
    "likely_owner_decisions_required",
    "safe_for_review_only_strengthening_now",
    "review_only_safety_status",
    "downstream_gates_before_promotion_or_implementation",
    "non_authorizations",
}

SAFE_STATUS_VALUES = {
    "safe_for_review_only_strengthening_now",
    "safe_for_research_packet_prep_only",
    "blocked_until_case_policy_or_owner_decision",
    "parallel_harness_route_not_goal2_selection",
}

BLOCKED_CANDIDATES = {"T399-Q009", "T399-Q014", "T399-Q017", "T399-Q018", "T399-Q019", "T399-Q022"}
RESEARCH_PREP_ONLY_CANDIDATES = {"T399-Q007", "T399-Q016", "T399-Q021"}
REQUIRED_OWNER_DECISIONS = {f"T399-HDM-{number:03d}" for number in range(1, 9)}

REQUIRED_NON_AUTHORIZATIONS = {
    "exact_target_selection",
    "final_target_selection",
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
    "source_or_manuscript_row_population",
    "source_text_import",
    "denominational_systematic_theology_as_chunk_authority",
    "liberal_critical_default",
    "anti_supernatural_default",
    "anti_canonical_default",
}


class T399QueueError(ValueError):
    """Raised when the T399 queue is stale or authorizing."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise T399QueueError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise T399QueueError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise T399QueueError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise T399QueueError(f"{label} must be a non-empty string")
    return value


def _require_string_list(value: Any, label: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not value and not allow_empty):
        raise T399QueueError(f"{label} must be a {'possibly empty ' if allow_empty else ''}list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise T399QueueError(f"{label} must contain only non-empty strings")
    return value


def _validate_owner_options(value: Any, label: str) -> None:
    if not isinstance(value, list) or not value:
        raise T399QueueError(f"{label} must be a non-empty list")
    for index, option in enumerate(value):
        item_label = f"{label}[{index}]"
        if isinstance(option, str):
            _require_string(option, item_label)
            continue
        if not isinstance(option, dict):
            raise T399QueueError(f"{item_label} must be a string or mapping")
        _require_string(option.get("option_id"), f"{item_label}.option_id")
        _require_string(option.get("label"), f"{item_label}.label")


def _validate_static(data: dict[str, Any]) -> None:
    expected = {
        "object_type": "focused_bible_wide_research_queue",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "t399_focused_bible_wide_research_queue.v1",
        "queue_id": "t399_goal2_focused_bible_wide_research_queue",
        "task_id": "T399",
        "status": "complete_goal2_focused_research_queue",
        "owner": "Lowell Wong",
        "decision_register_entry": "CD-073",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise T399QueueError(f"{QUEUE_REL}: {key} must be {value!r}")

    scope = data.get("goal2_scope")
    if not isinstance(scope, dict):
        raise T399QueueError(f"{QUEUE_REL}: goal2_scope must be a mapping")
    expected_scope = {
        "corpus_scope": "canonical_66",
        "every_canonical_passage_accounted_for_at_triage_depth": True,
        "every_verse_deeply_researched": False,
        "final_target_selected": False,
        "reviewed_gold_promoted": False,
        "chunk_output_changed": False,
    }
    for key, value in expected_scope.items():
        if scope.get(key) != value:
            raise T399QueueError(f"{QUEUE_REL}: goal2_scope.{key} must be {value!r}")
    if "T397 remains" not in scope.get("relation_to_t397", ""):
        raise T399QueueError(f"{QUEUE_REL}: relation_to_t397 must preserve T397")

    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise T399QueueError(f"{QUEUE_REL}: authority must be a mapping")
    for key in ("records_scored_queue", "records_owner_decision_map", "records_review_only_safety_status"):
        if authority.get(key) is not True:
            raise T399QueueError(f"{QUEUE_REL}: authority.{key} must be true")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise T399QueueError(f"{QUEUE_REL}: authority.{key} must be false")

    boundary = data.get("orthodoxy_boundary")
    if not isinstance(boundary, dict) or boundary.get("default") != "nicene_chalcedonian_core":
        raise T399QueueError(f"{QUEUE_REL}: orthodoxy boundary must stay Nicene/Chalcedonian")
    if boundary.get("canonical_scripture_authority") is not True:
        raise T399QueueError(f"{QUEUE_REL}: canonical Scripture authority must stay true")

    note = data.get("parallel_work_note")
    if not isinstance(note, dict) or "T396" not in note.get("open_pr", ""):
        raise T399QueueError(f"{QUEUE_REL}: parallel_work_note must record unmerged T396 handling")
    if "does not create source/manuscript rows" not in note.get("handling", ""):
        raise T399QueueError(f"{QUEUE_REL}: parallel_work_note must deny source/manuscript rows")


def _validate_inputs_and_scoring(data: dict[str, Any]) -> None:
    inputs = data.get("required_source_inputs")
    if not isinstance(inputs, list):
        raise T399QueueError(f"{QUEUE_REL}: required_source_inputs must be a list")
    input_paths = {item.get("path") for item in inputs if isinstance(item, dict)}
    missing = sorted(REQUIRED_SOURCE_INPUTS - input_paths)
    if missing:
        raise T399QueueError(f"{QUEUE_REL}: required_source_inputs missing {missing}")
    for path in input_paths:
        if not isinstance(path, str) or not (ROOT / path).exists():
            raise T399QueueError(f"{QUEUE_REL}: missing source input file {path!r}")

    scoring = data.get("scoring_model")
    if not isinstance(scoring, dict):
        raise T399QueueError(f"{QUEUE_REL}: scoring_model must be a mapping")
    criteria = scoring.get("criteria")
    if not isinstance(criteria, list) or len(criteria) < 7:
        raise T399QueueError(f"{QUEUE_REL}: scoring_model.criteria must include all scoring factors")
    total_weight = 0
    for criterion in criteria:
        if not isinstance(criterion, dict):
            raise T399QueueError(f"{QUEUE_REL}: scoring criteria must be mappings")
        total_weight += int(criterion.get("weight", 0))
        _require_string(criterion.get("criterion_id"), "scoring_model.criteria.criterion_id")
        _require_string(criterion.get("meaning"), "scoring_model.criteria.meaning")
    if total_weight != 100:
        raise T399QueueError(f"{QUEUE_REL}: scoring weights must total 100")
    if set(data.get("safe_status_values", [])) != SAFE_STATUS_VALUES:
        raise T399QueueError(f"{QUEUE_REL}: safe_status_values must match {sorted(SAFE_STATUS_VALUES)}")


def _validate_queue(data: dict[str, Any]) -> None:
    queue = data.get("focused_research_queue")
    if not isinstance(queue, list):
        raise T399QueueError(f"{QUEUE_REL}: focused_research_queue must be a list")
    if len(queue) < len(REQUIRED_CANDIDATES):
        raise T399QueueError(f"{QUEUE_REL}: focused_research_queue is incomplete")

    seen_ids: set[str] = set()
    seen_ranks: set[int] = set()
    lanes: set[str] = set()
    for item in queue:
        if not isinstance(item, dict):
            raise T399QueueError(f"{QUEUE_REL}: queue entries must be mappings")
        missing = sorted(REQUIRED_QUEUE_FIELDS - set(item))
        candidate_id = str(item.get("candidate_id", "<missing>"))
        label = f"{QUEUE_REL}:{candidate_id}"
        if missing:
            raise T399QueueError(f"{label}: missing fields {missing}")
        if candidate_id in seen_ids:
            raise T399QueueError(f"{label}: duplicate candidate_id")
        seen_ids.add(candidate_id)
        rank = item.get("rank")
        if not isinstance(rank, int) or rank < 1:
            raise T399QueueError(f"{label}: rank must be a positive integer")
        if rank in seen_ranks:
            raise T399QueueError(f"{label}: duplicate rank")
        seen_ranks.add(rank)
        lane = _require_string(item.get("lane_id"), f"{label}.lane_id")
        lanes.add(lane)
        score = item.get("score")
        if not isinstance(score, int) or score < 0 or score > 100:
            raise T399QueueError(f"{label}: score must be 0..100")
        for key in (
            "candidate_passages",
            "source_basis",
            "theological_or_hermeneutical_risks",
            "source_metadata_evidence_needs",
            "original_language_phrase_context_needs",
            "likely_owner_decisions_required",
            "downstream_gates_before_promotion_or_implementation",
            "non_authorizations",
        ):
            _require_string_list(item.get(key), f"{label}.{key}")
        _require_string(item.get("why_may_affect_chunking"), f"{label}.why_may_affect_chunking")
        _require_string(item.get("variant_source_tradition_dependency"), f"{label}.variant_source_tradition_dependency")
        status = item.get("review_only_safety_status")
        if status not in SAFE_STATUS_VALUES:
            raise T399QueueError(f"{label}: invalid review_only_safety_status {status!r}")
        safe = item.get("safe_for_review_only_strengthening_now")
        if not isinstance(safe, bool):
            raise T399QueueError(f"{label}: safe_for_review_only_strengthening_now must be boolean")
        if candidate_id in BLOCKED_CANDIDATES:
            if safe is not False or status != "blocked_until_case_policy_or_owner_decision":
                raise T399QueueError(f"{label}: variant/source-tradition candidate must stay blocked")
        if candidate_id in RESEARCH_PREP_ONLY_CANDIDATES:
            if safe is not False or status != "safe_for_research_packet_prep_only":
                raise T399QueueError(f"{label}: research-prep-only candidate must not be review-strengthening safe")
        if safe is True and status != "safe_for_review_only_strengthening_now":
            raise T399QueueError(f"{label}: safe=true requires safe_for_review_only_strengthening_now status")
        if "output_change" not in set(item["non_authorizations"]):
            raise T399QueueError(f"{label}: non_authorizations must include output_change")

    missing_candidates = sorted(REQUIRED_CANDIDATES - seen_ids)
    if missing_candidates:
        raise T399QueueError(f"{QUEUE_REL}: missing candidates {missing_candidates}")
    missing_lanes = sorted(REQUIRED_LANES - lanes)
    if missing_lanes:
        raise T399QueueError(f"{QUEUE_REL}: missing lanes {missing_lanes}")
    if sorted(seen_ranks) != list(range(1, len(seen_ranks) + 1)):
        raise T399QueueError(f"{QUEUE_REL}: queue ranks must be contiguous")


def _validate_owner_decision_map(data: dict[str, Any]) -> None:
    decisions = data.get("owner_decision_map")
    if not isinstance(decisions, list):
        raise T399QueueError(f"{QUEUE_REL}: owner_decision_map must be a list")
    candidate_ids = {item.get("candidate_id") for item in data.get("focused_research_queue", []) if isinstance(item, dict)}
    decision_ids = {item.get("decision_id") for item in decisions if isinstance(item, dict)}
    missing = sorted(REQUIRED_OWNER_DECISIONS - decision_ids)
    if missing:
        raise T399QueueError(f"{QUEUE_REL}: owner_decision_map missing {missing}")
    for decision in decisions:
        if not isinstance(decision, dict):
            raise T399QueueError(f"{QUEUE_REL}: owner decisions must be mappings")
        decision_id = str(decision.get("decision_id", "<missing>"))
        label = f"{QUEUE_REL}:{decision_id}"
        for key in ("title", "owner_question", "recommendation"):
            _require_string(decision.get(key), f"{label}.{key}")
        _require_string_list(decision.get("candidates"), f"{label}.candidates")
        _validate_owner_options(decision.get("options"), f"{label}.options")
        if decision.get("recommendation_is_owner_selection") is not False:
            raise T399QueueError(f"{label}: recommendation_is_owner_selection must be false")
        unknown = [candidate for candidate in decision["candidates"] if candidate.startswith("T399-Q") and candidate not in candidate_ids]
        if unknown:
            raise T399QueueError(f"{label}: unknown candidates {unknown}")

    next_actions = data.get("recommended_next_actions")
    if not isinstance(next_actions, list) or len(next_actions) < 3:
        raise T399QueueError(f"{QUEUE_REL}: recommended_next_actions must include T397 and owner gate actions")
    if not any("T397" in action.get("action", "") for action in next_actions if isinstance(action, dict)):
        raise T399QueueError(f"{QUEUE_REL}: recommended_next_actions must preserve T397")
    for action in next_actions:
        if not isinstance(action, dict) or action.get("authorizes_output") is not False:
            raise T399QueueError(f"{QUEUE_REL}: recommended_next_actions must not authorize output")


def _validate_non_authorizations(data: dict[str, Any]) -> None:
    actual = set(data.get("non_authorizations", []))
    missing = sorted(REQUIRED_NON_AUTHORIZATIONS - actual)
    if missing:
        raise T399QueueError(f"{QUEUE_REL}: non_authorizations missing {missing}")
    lesson = data.get("lesson_recorded")
    if not isinstance(lesson, dict) or lesson.get("lesson_id") != "LSN-027":
        raise T399QueueError(f"{QUEUE_REL}: lesson_recorded.lesson_id must be LSN-027")


def _validate_links() -> None:
    linked_requirements = (
        (REGISTER, ("CD-073", "T399 focused Bible-wide research queue separates score, safety, and authority", QUEUE_REL)),
        (LESSON_INDEX, ("LSN-027", "Focused Bible-wide research queues must separate score, safety, and authority", QUEUE_REL)),
        (PREFLIGHT, ("CD-073", "LSN-027", QUEUE_REL)),
        (READINESS, ("parallel_t399_focused_research_queue", QUEUE_REL, "relation_to_next_route: \"Parallel focused research queue; does not supersede the T416 batch1 post-pilot review gate or authorize output.\"")),
        (ROADMAP, ("id: T399", "complete_goal2_focused_research_queue", "next_chunking_route_remains: T416_batch1_post_pilot_review_gate_after_exact_output_pilot")),
        (FRONT_DOOR, (QUEUE_REL, VALIDATOR_REL, "T399 focused Bible-wide research queue")),
        (MAIN_TOC, (QUEUE_REL, "goal2", "focused-research-queue")),
        (ROADMAP_TOC, ("T399 | Focused Bible-wide research queue", ROADMAP_DOC_REL, VALIDATOR_REL)),
        (ROADMAP_DOC, ("T399 Focused Bible-Wide Research Queue", "recommendation is not selection", "T397 remains")),
        (TASK, ("id: T399", "CD-073", "LSN-027")),
        (HANDOFF, ("task_id: T399", "CD-073", "LSN-027")),
        (AUDIT, ("T399 No-Context Audit Surface", QUEUE_REL, "A high score is research priority, not authority")),
        (AUDIT_README, ("20260624-T399-focused-bible-wide-research-queue.md", "T399")),
        (VALIDATE_ALL, ("validate_t399_focused_bible_wide_research_queue.py",)),
    )
    for path, phrases in linked_requirements:
        text = _read_text(path)
        for phrase in phrases:
            if phrase not in text:
                raise T399QueueError(f"{_rel(path)}: missing {phrase!r}")

    readiness = _read_yaml(READINESS)
    if readiness.get("next_route", {}).get("task_id") not in {"T397", "T401", "T415", "T416"}:
        raise T399QueueError(f"{_rel(READINESS)}: T399 must not change next_route outside the later T397/T401/T415/T416 path")
    t399 = readiness.get("parallel_t399_focused_research_queue")
    if not isinstance(t399, dict):
        raise T399QueueError(f"{_rel(READINESS)}: parallel_t399_focused_research_queue must be a mapping")
    for key in (
        "output_change_authorized",
        "implementation_authorized",
        "exact_target_selected",
        "reviewed_gold_promoted",
        "child_spans_authorized",
        "route_behavior_authorized",
        "evaluator_change_authorized",
        "graph_edge_generation_allowed",
        "retrieval_truth_authorized",
        "embedding_or_vector_work_allowed",
        "boundary_import_allowed",
        "whole_bible_output_authorized",
        "preferred_reading_authorized",
        "source_tradition_preference_authorized",
        "canon_scope_change_authorized",
        "source_or_manuscript_rows_authorized",
        "theology_authority_change_authorized",
    ):
        if t399.get(key) is not False:
            raise T399QueueError(f"{_rel(READINESS)}: parallel_t399_focused_research_queue.{key} must be false")


def validate_t399_focused_bible_wide_research_queue(path: Path = QUEUE) -> dict[str, Any]:
    data = _read_yaml(path)
    _validate_static(data)
    _validate_inputs_and_scoring(data)
    _validate_queue(data)
    _validate_owner_decision_map(data)
    _validate_non_authorizations(data)
    _validate_links()
    return data


def main() -> int:
    try:
        validate_t399_focused_bible_wide_research_queue()
    except T399QueueError as exc:
        print(f"T399 focused Bible-wide research queue validation failed: {exc}", file=sys.stderr)
        return 1
    print("T399 focused Bible-wide research queue validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
