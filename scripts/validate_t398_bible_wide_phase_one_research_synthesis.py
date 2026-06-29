#!/usr/bin/env python3
"""Validate the T398 Bible-wide phase-one research synthesis."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
SYNTHESIS = ROOT / ".ai" / "control" / "t398_bible_wide_phase_one_research_synthesis.yaml"
SUMMARY = ROOT / ".ai" / "control" / "bible_verse_passage_coverage_summary.yaml"
REGISTRY = ROOT / ".ai" / "control" / "bible_wide_chunking_research_registry.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
LESSON_INDEX = ROOT / ".ai" / "control" / "chunking_lesson_index.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
ROADMAP = ROOT / "ROADMAP_STATE.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
MAIN_TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"
ROADMAP_DOC = ROOT / "docs" / "roadmap" / "T398_BIBLE_WIDE_PHASE_ONE_RESEARCH_SYNTHESIS.md"
TASK = ROOT / ".ai" / "tasks" / "T398.task.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T398" / "handoff.md"
AUDIT = ROOT / ".ai" / "audits" / "reports" / "20260623-T398-bible-wide-phase-one-research-synthesis.md"
AUDIT_README = ROOT / ".ai" / "audits" / "reports" / "README.md"
VALIDATE_ALL = ROOT / "scripts" / "validate_all.py"

SYNTHESIS_REL = ".ai/control/t398_bible_wide_phase_one_research_synthesis.yaml"
VALIDATOR_REL = "scripts/validate_t398_bible_wide_phase_one_research_synthesis.py"
ROADMAP_DOC_REL = "docs/roadmap/T398_BIBLE_WIDE_PHASE_ONE_RESEARCH_SYNTHESIS.md"

REQUIRED_FALSE_AUTHORITY = {
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
    "authorizes_source_or_manuscript_row_population",
    "authorizes_denominational_systematic_theology_as_chunk_authority",
}

REQUIRED_PROMPTS = {f"T398-HDP-{number:03d}" for number in range(1, 10)}

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
    "source_or_manuscript_row_population",
    "denominational_systematic_theology_as_chunk_authority",
    "liberal_critical_default",
    "anti_supernatural_default",
    "anti_canonical_default",
}


class T398SynthesisError(ValueError):
    """Raised when the T398 phase-one synthesis is stale or authorizing."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise T398SynthesisError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise T398SynthesisError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise T398SynthesisError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    if not isinstance(actual, list):
        raise T398SynthesisError(f"{label} must be a list")
    missing = sorted(required - {str(item) for item in actual})
    if missing:
        raise T398SynthesisError(f"{label} missing {missing}")


def _validate_static(data: dict[str, Any]) -> None:
    expected = {
        "object_type": "bible_wide_phase_one_research_synthesis",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "t398_bible_wide_phase_one_research_synthesis.v1",
        "synthesis_id": "t398_bible_wide_phase_one_research_synthesis",
        "task_id": "T398",
        "status": "complete_phase_one_whole_corpus_research_synthesis",
        "owner": "Lowell Wong",
        "decision_register_entry": "CD-072",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise T398SynthesisError(f"{SYNTHESIS_REL}: {key} must be {value!r}")

    definition = data.get("phase_one_definition")
    if not isinstance(definition, dict):
        raise T398SynthesisError(f"{SYNTHESIS_REL}: phase_one_definition must be a mapping")
    expected_definition = {
        "corpus_scope": "canonical_66",
        "canonical_book_count": 66,
        "canonical_passage_count": 31103,
        "every_canonical_passage_accounted_for_at_triage_depth": True,
        "every_canonical_book_accounted_for_at_registry_depth": True,
        "every_verse_deeply_researched": False,
        "does_not_mean_chunking_ready_for_whole_bible_output": True,
        "does_not_replace_goal2_focused_research": True,
    }
    for key, value in expected_definition.items():
        if definition.get(key) != value:
            raise T398SynthesisError(f"{SYNTHESIS_REL}: phase_one_definition.{key} must be {value!r}")

    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise T398SynthesisError(f"{SYNTHESIS_REL}: authority must be a mapping")
    for key in ("records_phase_one_synthesis", "records_human_decision_prompts", "records_goal2_research_inputs"):
        if authority.get(key) is not True:
            raise T398SynthesisError(f"{SYNTHESIS_REL}: authority.{key} must be true")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise T398SynthesisError(f"{SYNTHESIS_REL}: authority.{key} must be false")

    boundary = data.get("orthodoxy_boundary")
    if not isinstance(boundary, dict) or boundary.get("default") != "nicene_chalcedonian_core":
        raise T398SynthesisError(f"{SYNTHESIS_REL}: orthodoxy boundary must stay Nicene/Chalcedonian")
    if boundary.get("canonical_scripture_authority") is not True:
        raise T398SynthesisError(f"{SYNTHESIS_REL}: canonical Scripture authority must stay true")


def _validate_evidence_snapshot(data: dict[str, Any]) -> None:
    summary = _read_yaml(SUMMARY)
    snapshot = data.get("evidence_snapshot")
    if not isinstance(snapshot, dict):
        raise T398SynthesisError(f"{SYNTHESIS_REL}: evidence_snapshot must be a mapping")
    expected_summary_keys = {
        "passage_status_counts": "status_counts",
        "passage_flag_counts": "flag_counts",
        "owner_decision_counts": "owner_decision_counts",
    }
    for snapshot_key, summary_key in expected_summary_keys.items():
        if snapshot.get(snapshot_key) != summary.get(summary_key):
            raise T398SynthesisError(f"{SYNTHESIS_REL}: evidence_snapshot.{snapshot_key} must match T386 summary")
    if snapshot.get("passage_status_counts", {}).get("deeper_review_required") != 12625:
        raise T398SynthesisError(f"{SYNTHESIS_REL}: deeper_review_required count is stale")
    if snapshot.get("passage_status_counts", {}).get("blocked_before_chunking") != 1940:
        raise T398SynthesisError(f"{SYNTHESIS_REL}: blocked_before_chunking count is stale")

    registry = _read_yaml(REGISTRY)
    books = registry.get("book_research_queue")
    if not isinstance(books, list) or len(books) != 66:
        raise T398SynthesisError(f"{_rel(REGISTRY)}: expected 66 registry books")
    if sum(snapshot.get("registry_status_counts", {}).values()) != 66:
        raise T398SynthesisError(f"{SYNTHESIS_REL}: registry status counts must total 66")


def _validate_prompts_and_goal2(data: dict[str, Any]) -> None:
    prompts = data.get("phase_one_human_decision_prompt_queue")
    if not isinstance(prompts, list):
        raise T398SynthesisError(f"{SYNTHESIS_REL}: prompt queue must be a list")
    prompt_ids = {item.get("prompt_id") for item in prompts if isinstance(item, dict)}
    missing = sorted(REQUIRED_PROMPTS - prompt_ids)
    if missing:
        raise T398SynthesisError(f"{SYNTHESIS_REL}: missing prompts {missing}")
    for prompt in prompts:
        if not isinstance(prompt, dict):
            raise T398SynthesisError(f"{SYNTHESIS_REL}: each prompt must be a mapping")
        label = f"{SYNTHESIS_REL}:{prompt.get('prompt_id')}"
        for key in ("title", "owner_question", "recommendation"):
            if not isinstance(prompt.get(key), str) or not prompt[key].strip():
                raise T398SynthesisError(f"{label}: {key} must be a non-empty string")
        _require_subset({"output_change"}, prompt.get("non_authorizations"), f"{label}.non_authorizations")

    recommendation = data.get("phase_two_research_recommendation")
    if not isinstance(recommendation, dict):
        raise T398SynthesisError(f"{SYNTHESIS_REL}: phase_two_research_recommendation must be a mapping")
    for phrase in ("Goal 2 focused Bible-wide research", "Do not select targets", "Do not select preferred readings/source traditions"):
        if phrase not in recommendation.get("goal_prompt", ""):
            raise T398SynthesisError(f"{SYNTHESIS_REL}: Goal 2 prompt missing {phrase!r}")
    if "T397 remains the next route" not in recommendation.get("relation_to_t397", ""):
        raise T398SynthesisError(f"{SYNTHESIS_REL}: relation_to_t397 must preserve T397")

    _require_subset(REQUIRED_NON_AUTHORIZATIONS, data.get("non_authorizations"), "non_authorizations")
    lesson = data.get("lesson_recorded")
    if not isinstance(lesson, dict) or lesson.get("lesson_id") != "LSN-026":
        raise T398SynthesisError(f"{SYNTHESIS_REL}: lesson_recorded.lesson_id must be LSN-026")


def _validate_links() -> None:
    linked_requirements = (
        (REGISTER, ("CD-072", "T398 phase-one whole-corpus research synthesis is triage, not output authority", SYNTHESIS_REL)),
        (LESSON_INDEX, ("LSN-026", "Phase-one whole-corpus research is triage, not deep verse exegesis", SYNTHESIS_REL)),
        (PREFLIGHT, ("CD-072", "LSN-026", SYNTHESIS_REL)),
        (READINESS, ("parallel_t398_phase_one_research_synthesis", SYNTHESIS_REL, "relation_to_next_route: \"Parallel phase-one research synthesis; does not supersede the T401 output pilot/post-pilot review gate or authorize output.\"")),
        (ROADMAP, ("id: T398", "complete_phase_one_whole_corpus_research_synthesis", "T401")),
        (FRONT_DOOR, (SYNTHESIS_REL, VALIDATOR_REL, "T398 phase-one whole-corpus research synthesis")),
        (MAIN_TOC, (SYNTHESIS_REL, "phase-one-research", "Goal 2 focused")),
        (ROADMAP_TOC, ("T398 | Bible-wide phase-one research synthesis", ROADMAP_DOC_REL, VALIDATOR_REL)),
        (ROADMAP_DOC, ("T398 Bible-Wide Phase-One Research Synthesis", "every verse has been deeply exegeted", "T397 remains")),
        (TASK, ("id: T398", "CD-072", "LSN-026")),
        (HANDOFF, ("task_id: T398", "CD-072", "LSN-026")),
        (AUDIT, ("T398 No-Context Audit Surface", SYNTHESIS_REL, "every_verse_deeply_researched: false")),
        (AUDIT_README, ("20260623-T398-bible-wide-phase-one-research-synthesis.md", "T398")),
        (VALIDATE_ALL, ("validate_t398_bible_wide_phase_one_research_synthesis.py",)),
    )
    for path, phrases in linked_requirements:
        text = _read_text(path)
        for phrase in phrases:
            if phrase not in text:
                raise T398SynthesisError(f"{_rel(path)}: missing {phrase!r}")

    readiness = _read_yaml(READINESS)
    if readiness.get("next_route", {}).get("task_id") not in {"T397", "T401"}:
        raise T398SynthesisError(f"{_rel(READINESS)}: T398 must not change next_route outside the later T397/T401 path")


def validate_t398_bible_wide_phase_one_research_synthesis(path: Path = SYNTHESIS) -> dict[str, Any]:
    data = _read_yaml(path)
    _validate_static(data)
    _validate_evidence_snapshot(data)
    _validate_prompts_and_goal2(data)
    _validate_links()
    return data


def main() -> int:
    try:
        validate_t398_bible_wide_phase_one_research_synthesis()
    except T398SynthesisError as exc:
        print(f"T398 Bible-wide phase-one research synthesis validation failed: {exc}", file=sys.stderr)
        return 1
    print("T398 Bible-wide phase-one research synthesis validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
