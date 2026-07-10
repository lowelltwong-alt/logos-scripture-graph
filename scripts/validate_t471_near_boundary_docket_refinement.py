#!/usr/bin/env python3
"""Validate T471 near-boundary and owner-docket refinement artifacts."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = {
    "task": ".ai/tasks/T471.task.yaml",
    "control": ".ai/control/t471_near_boundary_docket_refinement.yaml",
    "register": ".ai/control/chunking_theological_decision_register.yaml",
    "lesson_index": ".ai/control/chunking_lesson_index.yaml",
    "status": ".ai/control/PROJECT_STATUS.md",
    "focus": ".ai/control/current_focus.yaml",
    "handoff": ".ai/handoffs/T471/handoff.md",
    "roadmap": "docs/roadmap/T471_NEAR_BOUNDARY_DOCKET_REFINEMENT.md",
    "builder": "scripts/build_t471_near_boundary_docket_refinement.py",
    "delta_out": ".ai/context/agent_work/T471/near_boundary_delta_refinement.jsonl",
    "owner_out": ".ai/context/agent_work/T471/owner_candidate_support_debate_docket.yaml",
    "summary": ".ai/context/agent_work/T471/refinement_summary.md",
    "source_delta": ".ai/scratch/multi_model_bible_chunking/comparison/disagreement_delta.jsonl",
    "source_t465": ".ai/context/agent_work/T465/owner_candidate_docket.yaml",
}

FORBIDDEN_AUTH_FIELDS = {
    "authorizes_target_selection",
    "authorizes_reviewed_gold",
    "authorizes_chunk_output",
    "authorizes_child_spans",
    "changes_route_behavior",
    "changes_evaluator_behavior",
    "creates_graph_truth",
    "creates_retrieval_truth",
    "creates_vector_truth",
    "runs_embeddings_or_builds_indexes",
    "imports_boundary_material",
    "selects_preferred_reading",
    "selects_source_tradition",
    "changes_canon_scope",
    "authorizes_theology_authority",
    "decides_variant_or_inspiration_status",
    "writes_dad_reports",
}

TASK_FORBIDDEN_AUTH_FIELDS = {
    "authorizes_target_selection",
    "authorizes_reviewed_gold",
    "authorizes_chunk_output",
    "authorizes_child_spans",
    "changes_route_behavior",
    "changes_evaluator_behavior",
    "creates_graph_or_retrieval_truth",
    "runs_embeddings_or_builds_indexes",
    "imports_boundary_material",
    "selects_preferred_reading_or_source_tradition",
    "changes_canon_scope",
    "authorizes_theology_authority",
    "decides_variant_or_inspiration_status",
    "writes_dad_reports",
}

REFINED_CLASSES = {
    "codex_fable_owner_ready_candidate",
    "minor_near_boundary_offset",
    "real_literary_disagreement",
    "frontier_review_required",
    "harness_fix_or_rerun_required",
    "owner_decision_required",
}

REQUIRED_REGISTER_NON_AUTHS = {
    "target_selection",
    "chunk_output_change",
    "reviewed_gold_promotion",
    "child_span_creation",
    "route_or_evaluator_behavior",
    "graph_or_retrieval_truth",
    "vector_or_embedding_truth",
    "preferred_reading_selection",
    "source_tradition_preference",
    "canon_scope_change",
    "variant_or_inspiration_decision",
    "theology_authority_change",
    "dad_reporting_as_success_gate",
}


def _strip_front_matter(text: str) -> str:
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            return parts[1] + "\n" + parts[2]
    return text


def _read_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(_strip_front_matter(path.read_text(encoding="utf-8")))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected YAML mapping")
    return data


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            row = json.loads(stripped)
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_no}: expected JSON object")
            rows.append(row)
    return rows


def _require(condition: bool, error: str, errors: list[str]) -> None:
    if not condition:
        errors.append(error)


def _validate_false_flags(auth: dict[str, Any], fields: set[str], label: str, errors: list[str]) -> None:
    for field in sorted(fields):
        if auth.get(field) is not False:
            errors.append(f"{label}: {field} must be false")


def _find_item(items: Any, key: str, value: str) -> dict[str, Any] | None:
    if not isinstance(items, list):
        return None
    for item in items:
        if isinstance(item, dict) and item.get(key) == value:
            return item
    return None


def _validate_support_table(candidate: dict[str, Any], errors: list[str]) -> None:
    table = candidate.get("t470_support_debate_table")
    label = str(candidate.get("source_id", "candidate"))
    if not isinstance(table, list) or len(table) < 3:
        errors.append(f"{label}: support/debate table must contain at least three rows")
        return
    for index, row in enumerate(table, start=1):
        if not isinstance(row, dict):
            errors.append(f"{label}: table row {index} must be a mapping")
            continue
        for field in ("claim", "support_level", "how_concluded", "downstream_chunking_implication", "limits"):
            if not str(row.get(field, "")).strip():
                errors.append(f"{label}: table row {index} missing {field}")
        refs = row.get("source_refs")
        if not isinstance(refs, list) or not refs:
            errors.append(f"{label}: table row {index} source_refs must be non-empty")
        elif not all(isinstance(ref, dict) and (ref.get("path") or ref.get("url")) for ref in refs):
            errors.append(f"{label}: table row {index} source_refs need path or url")


def validate_t471_package(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    paths = {key: root / rel for key, rel in REQUIRED_FILES.items()}
    for key, path in paths.items():
        if not path.is_file():
            errors.append(f"missing required T471 file {REQUIRED_FILES[key]}")
    if errors:
        return errors

    task = _read_yaml(paths["task"])
    control = _read_yaml(paths["control"])
    register = _read_yaml(paths["register"])
    lesson_index = _read_yaml(paths["lesson_index"])
    focus = _read_yaml(paths["focus"])
    delta_rows = _read_jsonl(paths["delta_out"])
    source_deltas = _read_jsonl(paths["source_delta"])
    owner = _read_yaml(paths["owner_out"])
    t465 = _read_yaml(paths["source_t465"])
    status_text = paths["status"].read_text(encoding="utf-8")
    roadmap_text = paths["roadmap"].read_text(encoding="utf-8")
    handoff_text = paths["handoff"].read_text(encoding="utf-8")
    summary_text = paths["summary"].read_text(encoding="utf-8")

    _require(task.get("id") == "T471", "task id must be T471", errors)
    _require(control.get("object_type") == "t471_near_boundary_docket_refinement", "control object_type mismatch", errors)
    _require(control.get("schema_version") == "t471_near_boundary_docket_refinement.v1", "control schema_version mismatch", errors)
    _require(focus.get("current_task") == "T471", "current_focus current_task must be T471", errors)
    _validate_false_flags(task.get("authorization", {}), TASK_FORBIDDEN_AUTH_FIELDS, "task.authorization", errors)
    _validate_false_flags(control.get("authorization", {}), FORBIDDEN_AUTH_FIELDS, "control.authorization", errors)

    _require(len(delta_rows) == len(source_deltas), "T471 delta refinement row count must match T464 source deltas", errors)
    source_ids = {str(row.get("delta_id", "")) for row in source_deltas}
    refined_ids = {str(row.get("source_id", "")) for row in delta_rows}
    _require(source_ids == refined_ids, "T471 refined source ids must match T464 delta ids exactly", errors)

    class_counts: dict[str, int] = {name: 0 for name in REFINED_CLASSES}
    for row in delta_rows:
        label = str(row.get("source_id", "row"))
        refined_class = str(row.get("refined_class", ""))
        if refined_class not in REFINED_CLASSES:
            errors.append(f"{label}: invalid refined_class {refined_class}")
        else:
            class_counts[refined_class] += 1
        _require(row.get("non_authorizing") is True, f"{label}: non_authorizing must be true", errors)
        _require(row.get("promotion_authority") == "none", f"{label}: promotion_authority must be none", errors)
        for field in ("recommended_next_gate", "t470_support_level", "how_concluded", "downstream_chunking_implication", "limits"):
            if not str(row.get(field, "")).strip():
                errors.append(f"{label}: missing {field}")
        if refined_class == "codex_fable_owner_ready_candidate":
            _require(row.get("codex_fable_alignment") is True, f"{label}: owner-ready candidate must have codex_fable_alignment", errors)

    _require(class_counts["codex_fable_owner_ready_candidate"] == 19, "T471 must preserve 19 M4/M6 owner-ready candidates", errors)
    _require(class_counts["frontier_review_required"] >= 900, "T471 should keep most hard rows in frontier review", errors)
    _require(class_counts["harness_fix_or_rerun_required"] == 78, "T471 must preserve 78 harness/rerun rows", errors)

    candidates = owner.get("candidates", [])
    t465_candidates = t465.get("candidates", [])
    _require(owner.get("object_type") == "t471_owner_candidate_support_debate_docket", "owner docket object_type mismatch", errors)
    _require(owner.get("candidate_count") == len(candidates) == len(t465_candidates) == 19, "owner candidate docket must contain 19 candidates", errors)
    first = owner.get("recommended_first_t472_candidate", {})
    _require(first.get("source_id") == "DELTA-2John-001", "recommended first T472 candidate must be DELTA-2John-001", errors)
    _require(first.get("non_authorizing") is True, "recommended first candidate must be non-authorizing", errors)
    for candidate in candidates:
        _require(candidate.get("non_authorizing") is True, f"{candidate.get('source_id')}: non_authorizing must be true", errors)
        _require(candidate.get("promotion_authority") == "none", f"{candidate.get('source_id')}: promotion_authority must be none", errors)
        _validate_support_table(candidate, errors)

    register_decision = _find_item(register.get("decisions"), "decision_id", "CD-109")
    if register_decision is None:
        errors.append("decision register missing CD-109")
    else:
        _require("T471" in register_decision.get("task_ids", []), "CD-109 must cover T471", errors)
        _require(register_decision.get("classification") == "non_authorizing_review", "CD-109 classification must be non_authorizing_review", errors)
        _require(REQUIRED_REGISTER_NON_AUTHS.issubset(set(register_decision.get("non_authorizations", []))), "CD-109 missing required non-authorizations", errors)
    _require("T471" in set(register.get("backfill_coverage", {}).get("required_task_ids", [])), "register backfill must include T471", errors)

    lesson = _find_item(lesson_index.get("lessons"), "lesson_id", "LSN-054")
    if lesson is None:
        errors.append("lesson index missing LSN-054")
    else:
        _require("T471" in lesson.get("related_task_ids", []), "LSN-054 must cover T471", errors)
        _require("CD-109" in lesson.get("related_decision_ids", []), "LSN-054 must reference CD-109", errors)
        _require("near-boundary" in " ".join(lesson.get("tags", [])), "LSN-054 tags must include near-boundary", errors)
        _require("near_boundary_refinement_as_reviewed_gold" in lesson.get("non_authorizations", []), "LSN-054 must forbid refinement as reviewed gold", errors)
    _require(lesson_index.get("last_updated_by_task") == "T471", "lesson index last_updated_by_task must be T471", errors)

    joined = status_text + roadmap_text + handoff_text + summary_text
    for needle in ("T471", "near-boundary", "support/debate", "non-authorizing", "T472", "2John"):
        if needle not in joined:
            errors.append(f"T471 surfaces missing {needle!r}")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    errors = validate_t471_package(args.root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("T471 near-boundary docket refinement validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
