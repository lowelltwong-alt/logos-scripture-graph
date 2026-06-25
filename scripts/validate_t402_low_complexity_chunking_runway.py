#!/usr/bin/env python3
"""Validate the T402 whole-Bible low-complexity chunking runway."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / ".ai" / "control" / "whole_bible_low_complexity_chunking_candidate_queue.yaml"
POST_PILOT_REVIEW = ROOT / ".ai" / "control" / "t402_eph1_post_pilot_review.yaml"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
LESSON_INDEX = ROOT / ".ai" / "control" / "chunking_lesson_index.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
ROADMAP = ROOT / "ROADMAP_STATE.yaml"
PROJECT_STATUS = ROOT / ".ai" / "control" / "PROJECT_STATUS.md"
CURRENT_FOCUS = ROOT / ".ai" / "control" / "current_focus.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
MAIN_TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"
ROADMAP_DOC = ROOT / "docs" / "roadmap" / "T402_LOW_COMPLEXITY_CHUNKING_RUNWAY.md"
TASK = ROOT / ".ai" / "tasks" / "T402.task.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T402" / "handoff.md"
AUDIT = ROOT / ".ai" / "audits" / "reports" / "20260625-T402-low-complexity-runway.md"
AUDIT_README = ROOT / ".ai" / "audits" / "reports" / "README.md"
VALIDATE_ALL = ROOT / "scripts" / "validate_all.py"
COVERAGE = ROOT / ".ai" / "control" / "bible_verse_passage_coverage_inventory.jsonl"

QUEUE_REL = ".ai/control/whole_bible_low_complexity_chunking_candidate_queue.yaml"
POST_PILOT_REL = ".ai/control/t402_eph1_post_pilot_review.yaml"
VALIDATOR_REL = "scripts/validate_t402_low_complexity_chunking_runway.py"

CANONICAL_BOOKS = [
    "Gen",
    "Exod",
    "Lev",
    "Num",
    "Deut",
    "Josh",
    "Judg",
    "Ruth",
    "1Sam",
    "2Sam",
    "1Kgs",
    "2Kgs",
    "1Chr",
    "2Chr",
    "Ezra",
    "Neh",
    "Esth",
    "Job",
    "Ps",
    "Prov",
    "Eccl",
    "Song",
    "Isa",
    "Jer",
    "Lam",
    "Ezek",
    "Dan",
    "Hos",
    "Joel",
    "Amos",
    "Obad",
    "Jonah",
    "Mic",
    "Nah",
    "Hab",
    "Zeph",
    "Hag",
    "Zech",
    "Mal",
    "Matt",
    "Mark",
    "Luke",
    "John",
    "Acts",
    "Rom",
    "1Cor",
    "2Cor",
    "Gal",
    "Eph",
    "Phil",
    "Col",
    "1Thess",
    "2Thess",
    "1Tim",
    "2Tim",
    "Titus",
    "Phlm",
    "Heb",
    "Jas",
    "1Pet",
    "2Pet",
    "1John",
    "2John",
    "3John",
    "Jude",
    "Rev",
]

STATUS_VALUES = {
    "ready_for_review_packet",
    "needs_context_research",
    "needs_original_language_review",
    "variant_sensitive_hold",
    "theological_risk_hold",
    "not_low_complexity",
    "owner_decision_required",
    "do_not_chunk_now",
}

EXPECTED_STATUS_COUNTS = {
    "ready_for_review_packet": 38,
    "needs_context_research": 16,
    "needs_original_language_review": 2,
    "variant_sensitive_hold": 2,
    "theological_risk_hold": 6,
    "not_low_complexity": 0,
    "owner_decision_required": 1,
    "do_not_chunk_now": 1,
}

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
    "authorizes_theology_authority_change",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "exact_target_selection",
    "reviewed_gold_promotion",
    "child_span_selection",
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
    "theology_authority_change",
}

REQUIRED_CANDIDATE_FIELDS = {
    "candidate_id",
    "book",
    "lane_id",
    "proposed_parent",
    "osis_start",
    "osis_end",
    "status",
    "complexity_estimate",
    "review_eligibility_confidence",
    "why_low_complexity",
    "context_dependencies",
    "source_metadata_evidence",
    "variant_source_tradition_flags",
    "theological_risk_flags",
    "original_language_review",
    "child_span_policy",
    "required_human_decision",
    "recommended_next_action",
    "non_authorizations",
}

REQUIRED_SOURCE_INPUTS = {
    ".ai/control/t402_eph1_post_pilot_review.yaml",
    ".ai/control/t398_bible_wide_phase_one_research_synthesis.yaml",
    ".ai/control/t399_focused_bible_wide_research_queue.yaml",
    ".ai/control/bible_verse_passage_coverage_summary.yaml",
    ".ai/control/bible_verse_passage_readiness_matrix.yaml",
    ".ai/control/bible_verse_passage_gap_register.yaml",
    ".ai/control/bible_verse_passage_human_review_docket.yaml",
    ".ai/control/bible_wide_chunking_research_registry.yaml",
    ".ai/control/source_metadata_research_atlas.yaml",
    ".ai/control/original_language_phrase_context_policy.yaml",
    ".ai/control/contextual_reading_policy.yaml",
    ".ai/control/orthodox_hermeneutic_firewall_docket.yaml",
}

TEXT_SURFACE_REQUIREMENTS = {
    REGISTER: ["CD-077", "T402 low-complexity queue is review eligibility", QUEUE_REL],
    LESSON_INDEX: ["LSN-031", "Low-complexity status is review eligibility", QUEUE_REL],
    PREFLIGHT: ["CD-077", "LSN-031", QUEUE_REL, POST_PILOT_REL],
    READINESS: ["parallel_t402_low_complexity_runway", "CD-077", "LSN-031"],
    ROADMAP: ["id: T402", "low_complexity_means_review_eligibility_only: true"],
    PROJECT_STATUS: ["T402 low-complexity", "Low-complexity means review eligibility only"],
    CURRENT_FOCUS: ["current_task: T402", "t402_low_complexity_candidate_queue"],
    FRONT_DOOR: [QUEUE_REL, VALIDATOR_REL, "Low-complexity means review"],
    MAIN_TOC: ["t402", "low-complexity", QUEUE_REL, VALIDATOR_REL],
    ROADMAP_TOC: ["T402", "low-complexity", QUEUE_REL],
    ROADMAP_DOC: ["T402 Low-Complexity Chunking Runway", "Low-complexity status means review eligibility only"],
    TASK: ["id: T402", "complete_review_research_only_candidate_runway", QUEUE_REL],
    HANDOFF: ["T402 - Whole-Bible Low-Complexity", "Files changed", QUEUE_REL],
    AUDIT: ["T402 Low-Complexity Runway Audit", "Low-complexity means review eligibility"],
    AUDIT_README: ["20260625-T402-low-complexity-runway.md", "low-complexity means review eligibility only"],
    VALIDATE_ALL: ["validate_t402_low_complexity_chunking_runway.py"],
}


class T402RunwayError(ValueError):
    """Raised when T402 runway artifacts are stale, incomplete, or authorizing."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise T402RunwayError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise T402RunwayError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise T402RunwayError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise T402RunwayError(f"{label} must be a non-empty string")
    return value


def _require_string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise T402RunwayError(f"{label} must be a non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise T402RunwayError(f"{label} must contain only non-empty strings")
    return value


def _require_false_flags(mapping: Any, label: str, keys: set[str]) -> None:
    if not isinstance(mapping, dict):
        raise T402RunwayError(f"{label} must be a mapping")
    for key in sorted(keys):
        if mapping.get(key) is not False:
            raise T402RunwayError(f"{label}.{key} must be false")


def _coverage_refs() -> set[str]:
    refs: set[str] = set()
    try:
        lines = COVERAGE.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise T402RunwayError(f"{_rel(COVERAGE)}: unreadable: {exc}") from exc
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise T402RunwayError(f"{_rel(COVERAGE)}:{line_number}: invalid JSON: {exc}") from exc
        ref = record.get("osis_ref")
        if isinstance(ref, str) and ref:
            refs.add(ref)
    if len(refs) != 31103:
        raise T402RunwayError(f"{_rel(COVERAGE)}: expected 31103 coverage refs, found {len(refs)}")
    return refs


def _validate_queue_static(data: dict[str, Any]) -> None:
    expected = {
        "object_type": "whole_bible_low_complexity_chunking_candidate_queue",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "whole_bible_low_complexity_chunking_candidate_queue.v1",
        "queue_id": "t402_whole_bible_low_complexity_chunking_candidate_queue",
        "task_id": "T402",
        "status": "complete_review_research_only_candidate_runway",
        "owner": "Lowell Wong",
        "decision_register_entry": "CD-077",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise T402RunwayError(f"{QUEUE_REL}: {key} must be {value!r}")

    lesson = data.get("lesson_recorded")
    if not isinstance(lesson, dict) or lesson.get("lesson_id") != "LSN-031":
        raise T402RunwayError(f"{QUEUE_REL}: lesson_recorded.lesson_id must be 'LSN-031'")

    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise T402RunwayError(f"{QUEUE_REL}: authority must be a mapping")
    for key in (
        "records_candidate_queue",
        "records_low_complexity_criteria",
        "records_status_buckets",
        "records_terminology_policy",
    ):
        if authority.get(key) is not True:
            raise T402RunwayError(f"{QUEUE_REL}: authority.{key} must be true")
    _require_false_flags(authority, f"{QUEUE_REL}: authority", REQUIRED_FALSE_AUTHORITY)

    source_inputs = set(_require_string_list(data.get("source_inputs"), f"{QUEUE_REL}: source_inputs"))
    missing_inputs = sorted(REQUIRED_SOURCE_INPUTS - source_inputs)
    if missing_inputs:
        raise T402RunwayError(f"{QUEUE_REL}: source_inputs missing {missing_inputs}")

    terms = data.get("terminology_policy")
    if not isinstance(terms, dict):
        raise T402RunwayError(f"{QUEUE_REL}: terminology_policy must be a mapping")
    allowed_terms = terms.get("allowed_terms")
    if not isinstance(allowed_terms, dict):
        raise T402RunwayError(f"{QUEUE_REL}: terminology_policy.allowed_terms must be a mapping")
    for term in ("unit", "parent", "child", "overlay", "lane", "route", "depth"):
        if term not in allowed_terms:
            raise T402RunwayError(f"{QUEUE_REL}: terminology_policy.allowed_terms missing {term}")
    avoided = set(_require_string_list(terms.get("avoided_terms"), f"{QUEUE_REL}: terminology_policy.avoided_terms"))
    for term in ("grandparent", "great_grandparent"):
        if term not in avoided:
            raise T402RunwayError(f"{QUEUE_REL}: terminology_policy.avoided_terms missing {term}")

    rule = _require_string(data.get("low_complexity_rule"), f"{QUEUE_REL}: low_complexity_rule")
    if "review eligibility only" not in rule or "does not mean AI may chunk automatically" not in rule:
        raise T402RunwayError(f"{QUEUE_REL}: low_complexity_rule must deny automatic chunking authority")

    statuses = set(_require_string_list(data.get("status_values"), f"{QUEUE_REL}: status_values"))
    if statuses != STATUS_VALUES:
        raise T402RunwayError(f"{QUEUE_REL}: status_values must equal {sorted(STATUS_VALUES)}")

    common = set(_require_string_list(data.get("common_non_authorizations"), f"{QUEUE_REL}: common_non_authorizations"))
    missing_non_auth = sorted(REQUIRED_NON_AUTHORIZATIONS - common)
    if missing_non_auth:
        raise T402RunwayError(f"{QUEUE_REL}: common_non_authorizations missing {missing_non_auth}")


def _validate_candidates(data: dict[str, Any]) -> None:
    refs = _coverage_refs()
    candidates = data.get("candidate_queue")
    if not isinstance(candidates, list):
        raise T402RunwayError(f"{QUEUE_REL}: candidate_queue must be a list")
    if len(candidates) != 66:
        raise T402RunwayError(f"{QUEUE_REL}: candidate_queue must contain 66 candidates")

    books: list[str] = []
    statuses: Counter[str] = Counter()
    for index, candidate in enumerate(candidates, start=1):
        label = f"{QUEUE_REL}: candidate_queue[{index - 1}]"
        if not isinstance(candidate, dict):
            raise T402RunwayError(f"{label} must be a mapping")
        missing_fields = sorted(REQUIRED_CANDIDATE_FIELDS - set(candidate))
        if missing_fields:
            raise T402RunwayError(f"{label} missing fields {missing_fields}")

        expected_id = f"T402-LC-{index:03d}"
        if candidate.get("candidate_id") != expected_id:
            raise T402RunwayError(f"{label}.candidate_id must be {expected_id}")

        book = _require_string(candidate.get("book"), f"{label}.book")
        books.append(book)

        status = _require_string(candidate.get("status"), f"{label}.status")
        if status not in STATUS_VALUES:
            raise T402RunwayError(f"{label}.status is not allowed: {status}")
        statuses[status] += 1

        for key in (
            "lane_id",
            "proposed_parent",
            "osis_start",
            "osis_end",
            "complexity_estimate",
            "review_eligibility_confidence",
            "why_low_complexity",
            "original_language_review",
            "required_human_decision",
            "recommended_next_action",
        ):
            _require_string(candidate.get(key), f"{label}.{key}")

        if candidate.get("proposed_parent") != f"{candidate['osis_start']}-{candidate['osis_end']}":
            raise T402RunwayError(f"{label}.proposed_parent must equal osis_start-osis_end")
        for ref_key in ("osis_start", "osis_end"):
            if candidate[ref_key] not in refs:
                raise T402RunwayError(f"{label}.{ref_key} not found in coverage inventory: {candidate[ref_key]}")

        for key in ("context_dependencies", "variant_source_tradition_flags", "theological_risk_flags"):
            _require_string_list(candidate.get(key), f"{label}.{key}")

        metadata = _require_string_list(candidate.get("source_metadata_evidence"), f"{label}.source_metadata_evidence")
        if not all("evidence_only" in item for item in metadata):
            raise T402RunwayError(f"{label}.source_metadata_evidence must mark every item evidence_only")

        if candidate.get("child_span_policy") != "parent_only_assumed_no_children_authorized":
            raise T402RunwayError(f"{label}.child_span_policy must deny child-span authorization")

        non_auth = set(_require_string_list(candidate.get("non_authorizations"), f"{label}.non_authorizations"))
        missing_non_auth = sorted(REQUIRED_NON_AUTHORIZATIONS - non_auth)
        if missing_non_auth:
            raise T402RunwayError(f"{label}.non_authorizations missing {missing_non_auth}")

    if books != CANONICAL_BOOKS:
        raise T402RunwayError(f"{QUEUE_REL}: candidate books must match canonical order")
    if dict(statuses) != {key: value for key, value in EXPECTED_STATUS_COUNTS.items() if value}:
        raise T402RunwayError(f"{QUEUE_REL}: status counts are {dict(statuses)}, expected {EXPECTED_STATUS_COUNTS}")

    summary = data.get("summary_counts")
    if not isinstance(summary, dict):
        raise T402RunwayError(f"{QUEUE_REL}: summary_counts must be a mapping")
    if summary.get("canonical_book_count") != 66 or summary.get("candidate_count") != 66:
        raise T402RunwayError(f"{QUEUE_REL}: summary_counts must record 66 books and candidates")
    for key, value in EXPECTED_STATUS_COUNTS.items():
        if summary.get(key) != value:
            raise T402RunwayError(f"{QUEUE_REL}: summary_counts.{key} must be {value}")

    by_book = {candidate["book"]: candidate for candidate in candidates}
    if by_book["John"]["status"] != "owner_decision_required":
        raise T402RunwayError(f"{QUEUE_REL}: John must remain owner_decision_required")
    if by_book["Rev"]["status"] != "do_not_chunk_now":
        raise T402RunwayError(f"{QUEUE_REL}: Rev must remain do_not_chunk_now")


def _validate_post_pilot_review() -> None:
    data = _read_yaml(POST_PILOT_REVIEW)
    expected = {
        "object_type": "t402_eph1_post_pilot_review",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "t402_eph1_post_pilot_review.v1",
        "task_id": "T402",
        "status": "complete_review_only_child_spans_not_necessary_now",
        "owner": "Lowell Wong",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise T402RunwayError(f"{POST_PILOT_REL}: {key} must be {value!r}")
    scope = data.get("scope")
    if not isinstance(scope, dict):
        raise T402RunwayError(f"{POST_PILOT_REL}: scope must be a mapping")
    if scope.get("selected_parent") != "Eph.1.3-Eph.1.14" or scope.get("selected_children") != []:
        raise T402RunwayError(f"{POST_PILOT_REL}: selected parent/children mismatch")
    if scope.get("decision_register_entry") != "CD-077":
        raise T402RunwayError(f"{POST_PILOT_REL}: scope.decision_register_entry must be CD-077")

    authority = data.get("authority")
    _require_false_flags(
        authority,
        f"{POST_PILOT_REL}: authority",
        {
            "authorizes_child_spans",
            "authorizes_child_span_reviewed_gold",
            "authorizes_new_chunk_output",
            "authorizes_route_behavior_change",
            "authorizes_evaluator_change",
            "authorizes_graph_edges",
            "authorizes_retrieval_truth",
            "authorizes_embedding_or_vector_work",
            "authorizes_preferred_reading",
            "authorizes_source_tradition_preference",
            "authorizes_boundary_import",
            "authorizes_broader_epistle_generalization",
            "authorizes_whole_bible_output_pass",
        },
    )
    child_review = data.get("child_necessity_review")
    if not isinstance(child_review, dict):
        raise T402RunwayError(f"{POST_PILOT_REL}: child_necessity_review must be a mapping")
    if child_review.get("finding") != "child_spans_not_necessary_now":
        raise T402RunwayError(f"{POST_PILOT_REL}: child_necessity_review.finding must deny current need")
    if child_review.get("selected_children") != []:
        raise T402RunwayError(f"{POST_PILOT_REL}: child_necessity_review.selected_children must be []")
    non_auth = set(_require_string_list(data.get("non_authorizations"), f"{POST_PILOT_REL}: non_authorizations"))
    for required in ("child_span_selection", "chunk_output_change", "route_behavior_change", "whole_bible_output_pass"):
        if required not in non_auth:
            raise T402RunwayError(f"{POST_PILOT_REL}: non_authorizations missing {required}")


def _validate_text_surfaces() -> None:
    for path, phrases in TEXT_SURFACE_REQUIREMENTS.items():
        text = _read_text(path)
        for phrase in phrases:
            if phrase not in text:
                raise T402RunwayError(f"{_rel(path)}: missing required T402 phrase {phrase!r}")


def validate_t402_low_complexity_chunking_runway(path: Path = QUEUE) -> dict[str, Any]:
    data = _read_yaml(path)
    _validate_queue_static(data)
    _validate_candidates(data)
    _validate_post_pilot_review()
    _validate_text_surfaces()
    return data


def main() -> int:
    try:
        validate_t402_low_complexity_chunking_runway()
    except T402RunwayError as exc:
        print(f"T402 low-complexity runway validation failed: {exc}", file=sys.stderr)
        return 1
    print("T402 low-complexity runway validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
