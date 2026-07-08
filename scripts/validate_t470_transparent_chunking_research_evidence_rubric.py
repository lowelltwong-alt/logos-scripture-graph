#!/usr/bin/env python3
"""Validate T470 transparent chunking research evidence rubric."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = {
    "task": ".ai/tasks/T470.task.yaml",
    "control": ".ai/control/t470_transparent_chunking_research_evidence_rubric.yaml",
    "register": ".ai/control/chunking_theological_decision_register.yaml",
    "lesson_index": ".ai/control/chunking_lesson_index.yaml",
    "status": ".ai/control/PROJECT_STATUS.md",
    "focus": ".ai/control/current_focus.yaml",
    "handoff": ".ai/handoffs/T470/handoff.md",
    "roadmap": "docs/roadmap/T470_TRANSPARENT_CHUNKING_RESEARCH_EVIDENCE_RUBRIC.md",
    "source_notes": ".ai/context/agent_work/T470/research_source_notes.md",
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

EXPECTED_SUPPORT_LEVELS = {
    "well_supported",
    "well_supported_with_project_scope",
    "supported_but_contextual",
    "debated",
    "not_authorized",
}

REQUIRED_WELL_SUPPORTED_IDS = {f"T470-WS-{idx:03d}" for idx in range(1, 8)}
REQUIRED_DEBATED_IDS = {f"T470-DB-{idx:03d}" for idx in range(1, 8)}

REQUIRED_URL_FRAGMENTS = {
    "sil.org",
    "bibletranslationcompetencies.org",
    "diu.edu",
    "brill.com",
    "asburyseminary.edu",
    "tyndalehouse.com",
    "aclanthology.org/J97-1003",
    "aclanthology.org/J02-1002",
    "cckpca.org",
    "textandcanon.org",
    "biblicaltraining.org",
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


def _validate_claims(claims: Any, expected_ids: set[str], label: str, errors: list[str]) -> list[str]:
    if not isinstance(claims, list):
        errors.append(f"{label} must be a list")
        return []
    ids: list[str] = []
    for claim in claims:
        if not isinstance(claim, dict):
            errors.append(f"{label}: each claim must be a mapping")
            continue
        claim_id = str(claim.get("claim_id", ""))
        ids.append(claim_id)
        for field in ("claim", "support_level", "how_concluded", "limits"):
            if not str(claim.get(field, "")).strip():
                errors.append(f"{claim_id}: missing {field}")
        if not claim.get("downstream_chunking_rule") and not claim.get("downstream_chunking_implication"):
            errors.append(f"{claim_id}: missing downstream chunking rule or implication")
        refs = claim.get("source_refs")
        if not isinstance(refs, list) or not refs:
            errors.append(f"{claim_id}: source_refs must be a non-empty list")
            continue
        for ref in refs:
            if not isinstance(ref, dict):
                errors.append(f"{claim_id}: source_refs entries must be mappings")
                continue
            if not str(ref.get("label", "")).strip():
                errors.append(f"{claim_id}: source ref missing label")
            url = str(ref.get("url", ""))
            if not url.startswith("http"):
                errors.append(f"{claim_id}: source ref URL must start with http")
    missing = expected_ids - set(ids)
    if missing:
        errors.append(f"{label} missing required claim ids {sorted(missing)}")
    return ids


def validate_t470_package(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    paths = {key: root / rel for key, rel in REQUIRED_FILES.items()}
    for key, path in paths.items():
        if not path.is_file():
            errors.append(f"missing required T470 file {REQUIRED_FILES[key]}")
    if errors:
        return errors

    task = _read_yaml(paths["task"])
    control = _read_yaml(paths["control"])
    register = _read_yaml(paths["register"])
    lesson_index = _read_yaml(paths["lesson_index"])
    focus = _read_yaml(paths["focus"])
    status_text = paths["status"].read_text(encoding="utf-8")
    handoff_text = paths["handoff"].read_text(encoding="utf-8")
    roadmap_text = paths["roadmap"].read_text(encoding="utf-8")
    source_notes_text = paths["source_notes"].read_text(encoding="utf-8")
    control_text = paths["control"].read_text(encoding="utf-8")

    _require(task.get("id") == "T470", "task id must be T470", errors)
    _require(control.get("object_type") == "t470_transparent_chunking_research_evidence_rubric", "control object_type mismatch", errors)
    _require(control.get("schema_version") == "t470_transparent_chunking_research_evidence_rubric.v1", "control schema_version mismatch", errors)
    _require(focus.get("current_task") == "T470", "current_focus current_task must be T470", errors)

    _validate_false_flags(task.get("authorization", {}), TASK_FORBIDDEN_AUTH_FIELDS, "task.authorization", errors)
    _validate_false_flags(control.get("authorization", {}), FORBIDDEN_AUTH_FIELDS, "control.authorization", errors)
    _require(control.get("authorization", {}).get("records_research_transparency") is True, "control must record research transparency", errors)

    levels = set(control.get("support_levels", []))
    _require(EXPECTED_SUPPORT_LEVELS.issubset(levels), "support_levels missing required values", errors)

    ws_ids = _validate_claims(control.get("well_supported_claims"), REQUIRED_WELL_SUPPORTED_IDS, "well_supported_claims", errors)
    db_ids = _validate_claims(control.get("debated_claims"), REQUIRED_DEBATED_IDS, "debated_claims", errors)
    _require(len(ws_ids) >= 7, "must include at least seven well-supported claims", errors)
    _require(len(db_ids) >= 7, "must include at least seven debated claims", errors)

    all_urls = [
        str(ref.get("url", ""))
        for section in ("well_supported_claims", "debated_claims")
        for claim in control.get(section, [])
        if isinstance(claim, dict)
        for ref in claim.get("source_refs", [])
        if isinstance(ref, dict)
    ]
    for fragment in sorted(REQUIRED_URL_FRAGMENTS):
        if not any(fragment in url for url in all_urls):
            errors.append(f"missing required source URL fragment {fragment}")

    mark16 = _find_item(control.get("debated_claims"), "claim_id", "T470-DB-001")
    if mark16 is None:
        errors.append("missing Mark 16 debated claim T470-DB-001")
    else:
        mark_text = " ".join(str(mark16.get(field, "")) for field in ("claim", "how_concluded", "downstream_chunking_implication", "limits"))
        for needle in ("Mark 16", "Vaticanus", "Sinaiticus", "inspiration", "canon"):
            if needle not in mark_text:
                errors.append(f"T470-DB-001 missing {needle!r}")

    rec_text = " ".join(str(item.get("recommendation", "")) for item in control.get("t470_recommendations", []) if isinstance(item, dict))
    _require("WindowDiff" in rec_text or "near-boundary" in rec_text, "recommendations must include WindowDiff or near-boundary comparison", errors)
    _require("T465 19-row" in rec_text, "recommendations must keep T465 19-row docket visible", errors)

    joined_text = status_text + handoff_text + roadmap_text + source_notes_text + control_text
    for needle in ("well-supported", "debated", "how_concluded", "downstream", "limits", "non-authorizing"):
        if needle not in joined_text:
            errors.append(f"T470 surfaces missing required text {needle!r}")
    _require("WindowDiff" in joined_text, "T470 surfaces must mention WindowDiff", errors)

    register_decision = _find_item(register.get("decisions"), "decision_id", "CD-108")
    if register_decision is None:
        errors.append("decision register missing CD-108")
    else:
        _require("T470" in register_decision.get("task_ids", []), "CD-108 must cover T470", errors)
        _require(register_decision.get("classification") == "non_authorizing_review", "CD-108 classification must be non_authorizing_review", errors)
        _require(REQUIRED_REGISTER_NON_AUTHS.issubset(set(register_decision.get("non_authorizations", []))), "CD-108 missing required non-authorizations", errors)

    required_task_ids = set(register.get("backfill_coverage", {}).get("required_task_ids", []))
    _require("T470" in required_task_ids, "backfill_coverage.required_task_ids must include T470", errors)

    lesson = _find_item(lesson_index.get("lessons"), "lesson_id", "LSN-053")
    if lesson is None:
        errors.append("lesson index missing LSN-053")
    else:
        _require("T470" in lesson.get("related_task_ids", []), "LSN-053 must cover T470", errors)
        _require("CD-108" in lesson.get("related_decision_ids", []), "LSN-053 must reference CD-108", errors)
        tag_text = " ".join(lesson.get("tags", []))
        for tag in ("research-transparency", "well-supported", "debated"):
            if tag not in tag_text:
                errors.append(f"LSN-053 tags missing {tag}")
        _require("research_transparency_as_reviewed_gold" in lesson.get("non_authorizations", []), "LSN-053 must forbid research transparency as reviewed gold", errors)
    _require(lesson_index.get("last_updated_by_task") == "T470", "lesson index last_updated_by_task must be T470", errors)

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    errors = validate_t470_package(args.root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("T470 transparent chunking research evidence rubric validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
