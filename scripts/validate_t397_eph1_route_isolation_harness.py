#!/usr/bin/env python3
"""Validate the T397 Eph.1.3-Eph.1.14 route-isolation harness prep."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
RECORD = ROOT / ".ai" / "control" / "t397_eph1_route_isolation_harness.yaml"
HARNESS_SCRIPT = ROOT / "scripts" / "chunking" / "route_isolation_harness.py"
HARNESS_TEST = ROOT / "tests" / "test_route_isolation_harness.py"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
LESSON_INDEX = ROOT / ".ai" / "control" / "chunking_lesson_index.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
ROADMAP = ROOT / "ROADMAP_STATE.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"
TASK = ROOT / ".ai" / "tasks" / "T397.task.yaml"
ROADMAP_DOC = ROOT / "docs" / "roadmap" / "T397_EPH1_ROUTE_ISOLATION_HARNESS.md"
AUDIT_REPORT = ROOT / ".ai" / "audits" / "reports" / "20260624-T397-eph1-route-isolation-harness.md"
PROMOTION = ROOT / ".ai" / "control" / "t394_eph1_parent_only_reviewed_gold_promotion.yaml"
MANIFEST = ROOT / "eval" / "chunking_gold" / "per_form" / "epistle_argument_gold_manifest.json"
REVIEW_PACKET = ROOT / "eval" / "chunking_gold" / "review_packets" / "eph1_3_14_argument_review.md"

RECORD_REL = ".ai/control/t397_eph1_route_isolation_harness.yaml"
HARNESS_SCRIPT_REL = "scripts/chunking/route_isolation_harness.py"
HARNESS_TEST_REL = "tests/test_route_isolation_harness.py"

REQUIRED_HARNESSES = {
    "T397-HARN-001",
    "T397-HARN-002",
    "T397-HARN-003",
    "T397-HARN-004",
    "T397-HARN-005",
}

REQUIRED_FALSE_AUTHORITY = {
    "authorizes_parent_span_as_chunk_boundary",
    "authorizes_child_spans",
    "authorizes_reviewed_gold_promotion",
    "authorizes_preferred_reading",
    "authorizes_source_tradition_preference",
    "authorizes_canon_scope_change",
    "authorizes_boundary_import",
    "authorizes_route_behavior",
    "authorizes_evaluator_change",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_embedding_or_vector_work",
    "authorizes_chunk_output_change",
    "authorizes_implementation",
    "authorizes_sqlite_database_creation",
    "authorizes_source_or_manuscript_rows",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "parent_span_as_chunk_boundary",
    "child_span_selection",
    "child_span_reviewed_gold_promotion",
    "permanent_child_span_denial",
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
    "denominational_systematic_theology_as_chunk_authority",
    "liberal_critical_default",
    "anti_supernatural_default",
    "source_metadata_as_boundary_authority",
}


class T397HarnessError(ValueError):
    """Raised when T397 harness prep is stale or unsafe."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise T397HarnessError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise T397HarnessError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise T397HarnessError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _string_list(value: Any, label: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not allow_empty and not value):
        raise T397HarnessError(f"{label} must be a {'possibly empty ' if allow_empty else ''}list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise T397HarnessError(f"{label} must contain only non-empty strings")
    return value


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    missing = sorted(required - set(_string_list(actual, label)))
    if missing:
        raise T397HarnessError(f"{label} missing {missing}")


def _validate_record(path: Path) -> dict[str, Any]:
    data = _read_yaml(path)
    expected = {
        "object_type": "eph1_route_isolation_harness_record",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "t397_eph1_route_isolation_harness.v1",
        "record_id": "t397_eph1_3_14_route_isolation_harness",
        "task_id": "T397",
        "status": "complete_non_output_changing_route_isolation_harness_prep",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise T397HarnessError(f"{_rel(path)}: {key} must be {value!r}")

    scope = data.get("goal6_scope")
    if not isinstance(scope, dict):
        raise T397HarnessError(f"{_rel(path)}: goal6_scope must be a mapping")
    expected_scope = {
        "corpus_scope": "canonical_66",
        "translation_scope": "eng-web",
        "lane": "epistle_argument",
        "target_id": "eph1_3_14_argument",
        "selected_parent": "Eph.1.3-Eph.1.14",
        "reviewed_gold_kind": "parent_only_span",
        "reviewed_gold_promoted_by": ".ai/control/t394_eph1_parent_only_reviewed_gold_promotion.yaml",
        "reviewed_gold_manifest": "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json",
        "reviewed_gold_case_id": "eph1_3_14_parent_only_reviewed_gold",
        "review_packet": "eval/chunking_gold/review_packets/eph1_3_14_argument_review.md",
        "owner_packet": ".ai/control/t393_eph1_reviewed_gold_promotion_decision_packet.yaml",
        "boundary_dependency_or_non_dependency": "current_repo_variant_non_dependent",
        "reviewed_gold_dependency_or_non_dependency": "current_repo_variant_non_dependent",
        "source_tradition_dependency_or_non_dependency": "current_repo_source_tradition_non_dependent",
    }
    for key, value in expected_scope.items():
        if scope.get(key) != value:
            raise T397HarnessError(f"{_rel(path)}: goal6_scope.{key} must be {value!r}")
    if scope.get("selected_children") != []:
        raise T397HarnessError(f"{_rel(path)}: goal6_scope.selected_children must be []")
    if scope.get("exact_internal_variant_refs") != []:
        raise T397HarnessError(f"{_rel(path)}: goal6_scope.exact_internal_variant_refs must be []")

    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise T397HarnessError(f"{_rel(path)}: authority must be a mapping")
    if authority.get("records_harness_prep") is not True:
        raise T397HarnessError(f"{_rel(path)}: authority.records_harness_prep must be true")
    if authority.get("provides_future_route_isolation_gate") is not True:
        raise T397HarnessError(f"{_rel(path)}: authority.provides_future_route_isolation_gate must be true")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise T397HarnessError(f"{_rel(path)}: authority.{key} must be false")

    harnesses = data.get("harnesses")
    if not isinstance(harnesses, list):
        raise T397HarnessError(f"{_rel(path)}: harnesses must be a list")
    by_id = {item.get("harness_id"): item for item in harnesses if isinstance(item, dict)}
    if set(by_id) != REQUIRED_HARNESSES:
        raise T397HarnessError(f"{_rel(path)}: harnesses must be {sorted(REQUIRED_HARNESSES)}")
    for harness_id, harness in by_id.items():
        if harness.get("script") != HARNESS_SCRIPT_REL:
            raise T397HarnessError(f"{_rel(path)}: {harness_id}.script must be {HARNESS_SCRIPT_REL}")
        if harness.get("test") != HARNESS_TEST_REL:
            raise T397HarnessError(f"{_rel(path)}: {harness_id}.test must be {HARNESS_TEST_REL}")
        _string_list(harness.get("must_fail_if"), f"{harness_id}.must_fail_if")

    proofs = data.get("synthetic_proof_cases")
    if not isinstance(proofs, list) or len(proofs) < 5:
        raise T397HarnessError(f"{_rel(path)}: synthetic_proof_cases must contain the five proof cases")
    proof_statuses = {item.get("status") for item in proofs if isinstance(item, dict)}
    if {"passing", "failing_as_expected"} - proof_statuses:
        raise T397HarnessError(f"{_rel(path)}: proof cases must include passing and failing_as_expected")

    future = data.get("future_output_pilot_requirements")
    if not isinstance(future, dict):
        raise T397HarnessError(f"{_rel(path)}: future_output_pilot_requirements must be a mapping")
    _require_subset(
        {
            "explicit_owner_output_pilot_authorization_for_Eph_1_3_Eph_1_14",
            "route_isolation_harness_passes_on_real_baseline_candidate_outputs",
            "same_baseline_evaluation_passes_or_records_no_improvement_claim",
            "decision_register_updated_for_output_authority",
            "task_scope_explicitly_allows_output_paths",
        },
        future.get("before_any_candidate_output_change"),
        "future_output_pilot_requirements.before_any_candidate_output_change",
    )
    if future.get("default_if_missing") != "stop_before_implementation_or_output_change":
        raise T397HarnessError(f"{_rel(path)}: future default must stop before implementation")

    _require_subset(REQUIRED_NON_AUTHORIZATIONS, data.get("non_authorizations"), "non_authorizations")
    if data.get("lesson_recorded", {}).get("lesson_id") != "LSN-028":
        raise T397HarnessError(f"{_rel(path)}: lesson_recorded.lesson_id must be LSN-028")
    if data.get("decision_register_entry") != "CD-074":
        raise T397HarnessError(f"{_rel(path)}: decision_register_entry must be CD-074")
    _require_subset(
        {
            "scripts/validate_t397_eph1_route_isolation_harness.py",
            "tests/test_t397_eph1_route_isolation_harness.py",
            HARNESS_SCRIPT_REL,
            HARNESS_TEST_REL,
            "scripts/validate_all.py",
        },
        data.get("validators"),
        "validators",
    )
    return data


def _validate_links() -> None:
    for path in (
        HARNESS_SCRIPT,
        HARNESS_TEST,
        REGISTER,
        PREFLIGHT,
        LESSON_INDEX,
        READINESS,
        ROADMAP,
        FRONT_DOOR,
        TOC,
        ROADMAP_TOC,
        TASK,
        ROADMAP_DOC,
        AUDIT_REPORT,
        PROMOTION,
        MANIFEST,
        REVIEW_PACKET,
    ):
        if not path.exists():
            raise T397HarnessError(f"{_rel(path)}: missing linked surface")

    linked_requirements = (
        (HARNESS_SCRIPT, ("compare_chunk_jsonl", "non-target records remain byte-identical", "does not authorize")),
        (HARNESS_TEST, ("test_exact_parent_overlay_preserves_non_target_bytes", "test_adjacent_spillover_fails")),
        (REGISTER, ("CD-074", RECORD_REL, "route-isolation harnesses prove output shape but do not authorize output")),
        (LESSON_INDEX, ("LSN-028", RECORD_REL, HARNESS_SCRIPT_REL, "route-isolation-harness")),
        (PREFLIGHT, ("CD-074", "LSN-028", RECORD_REL, HARNESS_SCRIPT_REL)),
        (READINESS, ("task_id: T397", RECORD_REL, "complete_non_output_changing_route_isolation_harness_prep")),
        (ROADMAP, ("id: T397", "status: complete_non_output_changing_route_isolation_harness_prep", RECORD_REL)),
        (FRONT_DOOR, (RECORD_REL, HARNESS_SCRIPT_REL, "T397 Eph.1.3-Eph.1.14 route-isolation harness")),
        (TOC, (RECORD_REL, HARNESS_SCRIPT_REL, "route-isolation-harness")),
        (ROADMAP_TOC, ("T397", RECORD_REL, "Route-isolated harness")),
        (TASK, ("id: T397", RECORD_REL, "chunk_output_authorized: false")),
        (ROADMAP_DOC, ("T397 Eph.1.3-Eph.1.14 Route-Isolation Harness", RECORD_REL, HARNESS_SCRIPT_REL)),
        (AUDIT_REPORT, ("T397 No-Context Audit Surface", RECORD_REL, HARNESS_SCRIPT_REL)),
    )
    for path, phrases in linked_requirements:
        text = _read_text(path)
        for phrase in phrases:
            if phrase not in text:
                raise T397HarnessError(f"{_rel(path)}: missing {phrase!r}")


def validate_t397_eph1_route_isolation_harness(path: Path = RECORD) -> dict[str, Any]:
    data = _validate_record(path)
    _validate_links()
    return data


def main() -> int:
    try:
        validate_t397_eph1_route_isolation_harness()
    except T397HarnessError as exc:
        print(f"T397 Eph.1 route-isolation harness validation failed: {exc}", file=sys.stderr)
        return 1
    print("T397 Eph.1 route-isolation harness validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
