#!/usr/bin/env python3
"""Validate the chunking lesson index and its changed-path gate."""
from __future__ import annotations

import argparse
import subprocess
import sys
from fnmatch import fnmatch
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
LESSON_INDEX = ROOT / ".ai" / "control" / "chunking_lesson_index.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
WORKFLOW_LESSONS = ROOT / "docs" / "methodology" / "WORKFLOW_LESSONS.md"

REQUIRED_TOP_LEVEL = {
    "object_type",
    "trust_zone",
    "lifecycle_status",
    "provenance_note",
    "reason_for_inclusion",
    "schema_version",
    "index_id",
    "owner",
    "prepared_by_task",
    "authority",
    "update_policy",
    "category_taxonomy",
    "lessons",
    "lesson_graph",
    "validator",
}

REQUIRED_AUTHORITY_FALSE = {
    "authorizes_chunk_output_change",
    "authorizes_reviewed_gold_promotion",
    "authorizes_route_behavior",
    "authorizes_evaluator_change",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_boundary_import",
}

REQUIRED_CATEGORIES = {
    "source_metadata",
    "original_language",
    "theological_risk",
    "owner_decision",
    "auditability",
    "workflow_governance",
    "graph_retrieval_vector",
    "contextual_reading",
}

REQUIRED_LESSON_IDS = {
    "LSN-001",
    "LSN-002",
    "LSN-003",
    "LSN-004",
    "LSN-005",
    "LSN-006",
    "LSN-007",
    "LSN-008",
    "LSN-009",
    "LSN-010",
    "LSN-011",
    "LSN-012",
    "LSN-013",
    "LSN-014",
    "LSN-015",
    "LSN-016",
    "LSN-017",
    "LSN-018",
    "LSN-019",
    "LSN-020",
    "LSN-021",
    "LSN-022",
    "LSN-023",
    "LSN-024",
    "LSN-025",
    "LSN-026",
    "LSN-027",
    "LSN-028",
    "LSN-029",
}

REQUIRED_TAGS = {
    "source-metadata",
    "lessons-learned",
    "preflight",
    "lesson-index",
    "ai-toc",
    "original-language",
    "orthodox-hermeneutic-firewall",
    "textual-critical-policy",
    "owner-projection",
    "parent-first-pilot",
    "graph",
    "no-context-review",
    "contextual-reading",
    "chapter-context",
    "historical-context",
    "research-runway",
    "authority-boundary",
    "bible-wide-readiness",
    "research-synthesis",
    "human-decision-map",
    "chunking-ready",
    "verse-passage-coverage",
    "coverage-inventory",
    "coverage-taxonomy",
    "readiness-matrix",
    "gap-register",
    "human-review-docket",
    "target-passage-lookup",
    "test-runtime",
    "pytest-timeout",
    "long-running-tests",
    "focused-tests",
    "manuscript-witness",
    "reliability-provenance",
    "oldest-fragments",
    "dead-sea-scrolls",
    "nt-papyri",
    "copy-abundance",
    "discovery-timeline",
    "evidence-namespace",
    "boundary-routing",
    "owner-decision-packet",
    "recommendation-not-selection",
    "goal4",
    "ephesians",
    "owner-gate",
    "review-packet-strengthening",
    "premortem",
    "red-team",
    "promotion-gate",
    "t392",
    "reviewed-gold-promotion-decision",
    "t393",
    "goal5",
    "variant-non-dependency",
    "child-span-necessity",
    "source-catalog-research",
    "official-sources",
    "t391",
    "source-catalog-sqlite",
    "sqlite-shell",
    "source-family",
    "method-profile",
    "source-trust",
    "seed-rows",
    "t395",
    "reviewed-gold",
    "parent-only",
    "goal6",
    "t394",
    "t393-a",
    "source-tradition-non-dependency",
    "implementation-blocked",
    "non-output-changing",
    "phase-one-research",
    "whole-corpus",
    "triage-not-exegesis",
    "goal2",
    "focused-research",
    "human-decision-prompts",
    "t398",
    "focused-research-queue",
    "owner-decision-map",
    "scoring-not-authority",
    "review-only-safety",
    "variant-blocked-status",
    "original-language-pressure",
    "t399",
    "route-isolation-harness",
    "non-target-identity",
    "same-baseline",
    "spill-protection",
    "child-span-denial",
    "exact-parent-target",
    "t397",
    "output-gate",
    "dss-biblical-witness-rows",
    "great-isaiah-scroll",
    "witness-row-population",
    "t396",
}

REQUIRED_SURFACES = {
    ".ai/control/chunking_agent_preflight.yaml",
    ".ai/control/chunking_lesson_index.yaml",
    ".ai/control/chunking_theological_decision_register.yaml",
    ".ai/control/source_metadata_research_atlas.yaml",
    ".ai/control/original_language_phrase_context_policy.yaml",
    ".ai/control/contextual_reading_policy.yaml",
    ".ai/control/t376_epistle_research_runway.yaml",
    ".ai/control/t384_bible_wide_research_readiness_synthesis.yaml",
    "docs/roadmap/T384_BIBLE_WIDE_RESEARCH_READINESS_SYNTHESIS.md",
    ".ai/control/t385_owner_decision_packet.yaml",
    "docs/roadmap/T385_OWNER_DECISION_PACKET.md",
    "scripts/validate_t385_owner_decision_packet.py",
    "tests/test_t385_owner_decision_packet.py",
    "eval/chunking_gold/review_packets/eph1_3_14_argument_review.md",
    "docs/roadmap/T392_EPH1_REVIEW_PACKET_STRENGTHENING.md",
    ".ai/tasks/T392.task.yaml",
    ".ai/audits/reports/20260623-T392-eph1-review-packet-strengthening.md",
    "scripts/validate_t392_eph1_review_packet_strengthening.py",
    "tests/test_t392_eph1_review_packet_strengthening.py",
    ".ai/control/t393_eph1_reviewed_gold_promotion_decision_packet.yaml",
    "docs/roadmap/T393_EPH1_REVIEWED_GOLD_PROMOTION_DECISION_PACKET.md",
    ".ai/tasks/T393.task.yaml",
    ".ai/audits/reports/20260623-T393-eph1-reviewed-gold-promotion-decision-packet.md",
    "scripts/validate_t393_eph1_reviewed_gold_promotion_decision_packet.py",
    "tests/test_t393_eph1_reviewed_gold_promotion_decision_packet.py",
    ".ai/control/t394_eph1_parent_only_reviewed_gold_promotion.yaml",
    "docs/roadmap/T394_EPH1_PARENT_ONLY_REVIEWED_GOLD_PROMOTION.md",
    ".ai/tasks/T394.task.yaml",
    ".ai/handoffs/T394/handoff.md",
    ".ai/audits/reports/20260623-T394-eph1-parent-only-reviewed-gold-promotion.md",
    "scripts/validate_t394_eph1_parent_only_reviewed_gold_promotion.py",
    "tests/test_t394_eph1_parent_only_reviewed_gold_promotion.py",
    ".ai/control/manuscript_source_catalog_research_packet.yaml",
    "docs/roadmap/T391_MANUSCRIPT_SOURCE_CATALOG_RESEARCH_PACKET.md",
    ".ai/tasks/T391.task.yaml",
    ".ai/handoffs/T391/handoff.md",
    "scripts/validate_manuscript_source_catalog_research_packet.py",
    "tests/test_manuscript_source_catalog_research_packet.py",
    ".ai/control/manuscript_source_catalog_sqlite_shell.yaml",
    "data/candidate/source_catalog/manuscript_reliability/sqlite/schema.sql",
    "data/candidate/source_catalog/manuscript_reliability/sqlite/seed_rows.jsonl",
    "data/candidate/source_catalog/manuscript_reliability/sqlite/manifest.yaml",
    "docs/roadmap/T395_SQLITE_SOURCE_CATALOG_SCHEMA_SHELL.md",
    ".ai/tasks/T395.task.yaml",
    ".ai/handoffs/T395/handoff.md",
    "scripts/validate_manuscript_source_catalog_sqlite_shell.py",
    "tests/test_manuscript_source_catalog_sqlite_shell.py",
    ".ai/control/dss_biblical_witness_source_rows.yaml",
    "data/candidate/source_catalog/manuscript_reliability/sqlite/dss_biblical_witness_rows.jsonl",
    "data/candidate/source_catalog/manuscript_reliability/sqlite/dss_biblical_witness_rows_manifest.yaml",
    "docs/roadmap/T396_DSS_BIBLICAL_WITNESS_SOURCE_ROWS.md",
    ".ai/tasks/T396.task.yaml",
    ".ai/handoffs/T396/handoff.md",
    "scripts/validate_dss_biblical_witness_source_rows.py",
    "tests/test_dss_biblical_witness_source_rows.py",
    ".ai/control/bible_verse_passage_coverage_inventory.jsonl",
    ".ai/control/bible_verse_passage_coverage_taxonomy.yaml",
    ".ai/control/bible_verse_passage_coverage_summary.yaml",
    ".ai/control/bible_verse_passage_readiness_matrix.yaml",
    ".ai/control/bible_verse_passage_gap_register.yaml",
    ".ai/control/bible_verse_passage_human_review_docket.yaml",
    "docs/roadmap/T386_BIBLE_VERSE_PASSAGE_COVERAGE_INVENTORY.md",
    ".ai/control/test_runtime_preflight.yaml",
    "scripts/validate_test_runtime_preflight.py",
    "tests/test_test_runtime_preflight.py",
    ".ai/control/manuscript_witness_reliability_scaffold.yaml",
    "docs/roadmap/T387_MANUSCRIPT_WITNESS_RELIABILITY_SCAFFOLD.md",
    ".ai/control/orthodox_hermeneutic_firewall_docket.yaml",
    ".ai/control/textual_critical_case_policy.yaml",
    ".ai/control/owner_decision_projection_policy.yaml",
    ".ai/control/t373_owner_implementation_authorization.yaml",
    ".ai/control/t375_post_pilot_review.yaml",
    ".ai/control/t398_bible_wide_phase_one_research_synthesis.yaml",
    "docs/roadmap/T398_BIBLE_WIDE_PHASE_ONE_RESEARCH_SYNTHESIS.md",
    ".ai/tasks/T398.task.yaml",
    ".ai/handoffs/T398/handoff.md",
    ".ai/audits/reports/20260623-T398-bible-wide-phase-one-research-synthesis.md",
    "scripts/validate_t398_bible_wide_phase_one_research_synthesis.py",
    "tests/test_t398_bible_wide_phase_one_research_synthesis.py",
    ".ai/control/t399_focused_bible_wide_research_queue.yaml",
    "docs/roadmap/T399_FOCUSED_BIBLE_WIDE_RESEARCH_QUEUE.md",
    ".ai/tasks/T399.task.yaml",
    ".ai/handoffs/T399/handoff.md",
    ".ai/audits/reports/20260624-T399-focused-bible-wide-research-queue.md",
    "scripts/validate_t399_focused_bible_wide_research_queue.py",
    "tests/test_t399_focused_bible_wide_research_queue.py",
    ".ai/control/t397_eph1_route_isolation_harness.yaml",
    "docs/roadmap/T397_EPH1_ROUTE_ISOLATION_HARNESS.md",
    ".ai/tasks/T397.task.yaml",
    ".ai/handoffs/T397/handoff.md",
    ".ai/audits/reports/20260624-T397-eph1-route-isolation-harness.md",
    "scripts/chunking/route_isolation_harness.py",
    "tests/test_route_isolation_harness.py",
    "scripts/validate_t397_eph1_route_isolation_harness.py",
    "tests/test_t397_eph1_route_isolation_harness.py",
    ".ai/audits/README.md",
    "AI_TABLE_OF_CONTENTS.md",
    "docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md",
}

WATCHED_PATTERNS = (
    ".ai/control/chunking_agent_preflight.yaml",
    "docs/methodology/WORKFLOW_LESSONS.md",
    "docs/methodology/LOGOS_CHUNKING_WORKFLOW_RULES_REGISTRY.md",
    "docs/methodology/CHUNKING_SKILL_SUPPLY_CHAIN.md",
    ".ai/control/chunking_theological_decision_register.yaml",
    ".ai/control/bible_chunking_readiness_map.yaml",
    ".ai/control/*_dossier_queue.yaml",
    ".ai/control/*_policy*.yaml",
    ".ai/control/*_inventory.yaml",
    ".ai/control/*_review*.yaml",
    ".ai/audits/reports/*",
    "AI_TABLE_OF_CONTENTS.md",
    "docs/roadmap/AI_ROADMAP_TABLE_OF_CONTENTS.md",
)

ALLOWED_PLACEHOLDER_PATHS = {
    ".ai/handoffs/<task_id>/handoff.md",
}


class LessonIndexError(ValueError):
    """Raised when the chunking lesson index is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _normalize_path(path: str) -> str:
    normalized = path.replace("\\", "/").strip()
    if normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
        if text.startswith("---\n"):
            parts = text.split("---\n", 2)
            if len(parts) == 3:
                text = parts[1] + "\n" + parts[2]
        data = yaml.safe_load(text)
    except (OSError, yaml.YAMLError) as exc:
        raise LessonIndexError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise LessonIndexError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise LessonIndexError(f"{_rel(path)}: unreadable: {exc}") from exc


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LessonIndexError(f"{label} must be a non-empty string")
    return value.strip()


def _require_string_list(value: Any, label: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not value and not allow_empty):
        raise LessonIndexError(f"{label} must be a {'possibly empty ' if allow_empty else ''}list")
    result: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise LessonIndexError(f"{label} must contain only non-empty strings")
        result.append(item.strip())
    return result


def _path_exists(path: str) -> bool:
    path = _normalize_path(path)
    if path in ALLOWED_PLACEHOLDER_PATHS:
        return True
    return (ROOT / path).exists()


def _git_output(args: list[str]) -> list[str]:
    try:
        output = subprocess.check_output(
            ["git", *args],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    return [_normalize_path(line) for line in output.splitlines() if line.strip()]


def _git_changed_files(base_ref: str) -> list[str]:
    paths: list[str] = []
    try:
        merge_base = subprocess.check_output(
            ["git", "merge-base", "HEAD", base_ref],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        paths.extend(_git_output(["diff", "--name-only", f"{merge_base}...HEAD"]))
    except (subprocess.CalledProcessError, FileNotFoundError):
        paths.extend(_git_output(["diff", "--name-only", "HEAD^1...HEAD"]))
    paths.extend(_git_output(["diff", "--cached", "--name-only"]))
    paths.extend(_git_output(["diff", "--name-only"]))
    paths.extend(_git_output(["ls-files", "--others", "--exclude-standard"]))
    return sorted(set(paths))


def validate_lesson_index(path: Path = LESSON_INDEX) -> dict[str, Any]:
    data = _read_yaml(path)
    missing = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing:
        raise LessonIndexError(f"{_rel(path)}: missing top-level keys {missing}")
    if data["object_type"] != "chunking_lesson_index":
        raise LessonIndexError(f"{_rel(path)}: object_type must be chunking_lesson_index")
    if data["trust_zone"] != "canonical":
        raise LessonIndexError(f"{_rel(path)}: trust_zone must be canonical")
    if data["lifecycle_status"] != "active":
        raise LessonIndexError(f"{_rel(path)}: lifecycle_status must be active")
    if data["validator"] != "scripts/validate_chunking_lesson_index.py":
        raise LessonIndexError(f"{_rel(path)}: validator path is wrong")

    authority = data["authority"]
    if not isinstance(authority, dict):
        raise LessonIndexError(f"{_rel(path)}: authority must be a mapping")
    if authority.get("records_lessons") is not True:
        raise LessonIndexError(f"{_rel(path)}: authority.records_lessons must be true")
    for key in REQUIRED_AUTHORITY_FALSE:
        if authority.get(key) is not False:
            raise LessonIndexError(f"{_rel(path)}: authority.{key} must be false")

    update_policy = data["update_policy"]
    if not isinstance(update_policy, dict):
        raise LessonIndexError(f"{_rel(path)}: update_policy must be a mapping")
    if update_policy.get("status") != "required":
        raise LessonIndexError(f"{_rel(path)}: update_policy.status must be required")
    if update_policy.get("changed_path_gate_enabled") is not True:
        raise LessonIndexError(f"{_rel(path)}: changed path gate must be enabled")
    _require_string(update_policy.get("rule"), "update_policy.rule")
    _require_string_list(update_policy.get("update_required_when_paths_change"), "update_policy.update_required_when_paths_change")

    categories = data["category_taxonomy"]
    if not isinstance(categories, list):
        raise LessonIndexError(f"{_rel(path)}: category_taxonomy must be a list")
    category_ids = set()
    for category in categories:
        if not isinstance(category, dict):
            raise LessonIndexError(f"{_rel(path)}: each category must be a mapping")
        category_id = _require_string(category.get("category_id"), "category.category_id")
        category_ids.add(category_id)
        _require_string(category.get("use_when"), f"{category_id}.use_when")
    missing_categories = sorted(REQUIRED_CATEGORIES - category_ids)
    if missing_categories:
        raise LessonIndexError(f"{_rel(path)}: missing categories {missing_categories}")

    register_text = _read_text(REGISTER)
    workflow_text = _read_text(WORKFLOW_LESSONS)
    lessons = data["lessons"]
    if not isinstance(lessons, list) or not lessons:
        raise LessonIndexError(f"{_rel(path)}: lessons must be a non-empty list")
    lesson_ids: set[str] = set()
    all_tags: set[str] = set()
    all_surfaces: set[str] = set()
    for lesson in lessons:
        if not isinstance(lesson, dict):
            raise LessonIndexError(f"{_rel(path)}: each lesson must be a mapping")
        lesson_id = _require_string(lesson.get("lesson_id"), "lesson.lesson_id")
        label = f"{_rel(path)}:{lesson_id}"
        if lesson_id in lesson_ids:
            raise LessonIndexError(f"{label}: duplicate lesson_id")
        lesson_ids.add(lesson_id)
        for key in ("title", "lifecycle_status", "priority", "preflight_stage", "downstream_risk"):
            _require_string(lesson.get(key), f"{label}.{key}")
        if lesson["lifecycle_status"] != "active":
            raise LessonIndexError(f"{label}: lifecycle_status must be active")
        lesson_categories = set(_require_string_list(lesson.get("categories"), f"{label}.categories"))
        if not lesson_categories <= category_ids:
            raise LessonIndexError(f"{label}: categories outside taxonomy {sorted(lesson_categories - category_ids)}")
        tags = set(_require_string_list(lesson.get("tags"), f"{label}.tags"))
        all_tags.update(tags)
        use_when = _require_string_list(lesson.get("use_when"), f"{label}.use_when")
        if not all(len(item) >= 20 for item in use_when):
            raise LessonIndexError(f"{label}: use_when entries must be descriptive")
        for list_key in (
            "source_surfaces",
            "related_decision_ids",
            "related_workflow_lesson_ids",
            "related_task_ids",
            "required_preflight_surfaces",
            "non_authorizations",
            "validators",
        ):
            _require_string_list(lesson.get(list_key), f"{label}.{list_key}", allow_empty=list_key in {"related_decision_ids", "related_workflow_lesson_ids"})
        for surface in lesson["source_surfaces"] + lesson["required_preflight_surfaces"]:
            normalized = _normalize_path(surface)
            all_surfaces.add(normalized)
            if not _path_exists(normalized):
                raise LessonIndexError(f"{label}: referenced surface missing: {surface}")
        for validator in lesson["validators"]:
            if not _path_exists(validator):
                raise LessonIndexError(f"{label}: validator missing: {validator}")
        for decision_id in lesson["related_decision_ids"]:
            if decision_id not in register_text:
                raise LessonIndexError(f"{label}: related decision missing from register: {decision_id}")
        for workflow_lesson_id in lesson["related_workflow_lesson_ids"]:
            if workflow_lesson_id not in workflow_text:
                raise LessonIndexError(f"{label}: related workflow lesson missing: {workflow_lesson_id}")

    missing_lessons = sorted(REQUIRED_LESSON_IDS - lesson_ids)
    if missing_lessons:
        raise LessonIndexError(f"{_rel(path)}: missing lessons {missing_lessons}")
    missing_tags = sorted(REQUIRED_TAGS - all_tags)
    if missing_tags:
        raise LessonIndexError(f"{_rel(path)}: missing searchable tags {missing_tags}")
    missing_surfaces = sorted(REQUIRED_SURFACES - all_surfaces)
    if missing_surfaces:
        raise LessonIndexError(f"{_rel(path)}: missing required surfaces {missing_surfaces}")

    graph = data["lesson_graph"]
    if not isinstance(graph, list) or not graph:
        raise LessonIndexError(f"{_rel(path)}: lesson_graph must be a non-empty list")
    for edge in graph:
        if not isinstance(edge, dict):
            raise LessonIndexError(f"{_rel(path)}: each lesson_graph edge must be a mapping")
        source = _require_string(edge.get("from"), "lesson_graph.from")
        target = _require_string(edge.get("to"), "lesson_graph.to")
        relation = _require_string(edge.get("relation"), "lesson_graph.relation")
        if source not in lesson_ids or target not in lesson_ids:
            raise LessonIndexError(f"{_rel(path)}: graph edge references unknown lesson {source}->{target}")
        if relation not in {"governs_update_of", "constrains", "audits", "discovers"}:
            raise LessonIndexError(f"{_rel(path)}: invalid graph relation {relation!r}")

    preflight = _read_yaml(PREFLIGHT)
    reading_paths = {
        str(item.get("path"))
        for item in preflight.get("mandatory_reading", [])
        if isinstance(item, dict)
    }
    if ".ai/control/chunking_lesson_index.yaml" not in reading_paths:
        raise LessonIndexError(f"{_rel(PREFLIGHT)}: lesson index must be mandatory reading")
    capture = preflight.get("midflight_lesson_capture", {})
    if ".ai/control/chunking_lesson_index.yaml" not in capture.get("required_surfaces", []):
        raise LessonIndexError(f"{_rel(PREFLIGHT)}: lesson index must be a midflight required surface")

    return data


def validate_changed_path_gate(
    *,
    changed_files: list[str],
    index_path: Path = LESSON_INDEX,
    index_updated: bool | None = None,
) -> None:
    normalized = [_normalize_path(path) for path in changed_files]
    watched = [
        path for path in normalized
        if any(fnmatch(path, pattern) for pattern in WATCHED_PATTERNS)
    ]
    if index_updated is None:
        index_updated = _rel(index_path) in normalized
    if watched and not index_updated:
        raise LessonIndexError(
            "chunking lesson index must be updated when lesson/preflight surfaces change: "
            + ", ".join(watched)
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, default=LESSON_INDEX)
    parser.add_argument("--base-ref", default="origin/main")
    parser.add_argument("--changed-file", action="append", default=[])
    parser.add_argument("--index-updated", choices=["true", "false"], default=None)
    args = parser.parse_args(argv)

    try:
        validate_lesson_index(args.index)
        changed_files = args.changed_file or _git_changed_files(args.base_ref)
        index_updated = None
        if args.index_updated is not None:
            index_updated = args.index_updated == "true"
        validate_changed_path_gate(
            changed_files=changed_files,
            index_path=args.index,
            index_updated=index_updated,
        )
    except LessonIndexError as exc:
        print(f"Chunking lesson index validation failed: {exc}", file=sys.stderr)
        return 1

    print("Chunking lesson index validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
