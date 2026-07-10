#!/usr/bin/env python3
"""Validate T472 model-panel calibration and provenance correction."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = {
    "task": ".ai/tasks/T472.task.yaml",
    "control": ".ai/control/t472_model_panel_calibration_gate.yaml",
    "withdrawn_control": ".ai/control/t472_2john_owner_packet.yaml",
    "withdrawn_packet": ".ai/context/agent_work/T472/owner_packet_DELTA-2John-001.yaml",
    "classifications": ".ai/context/agent_work/T472/all_delta_mechanical_classification.jsonl",
    "dissent": ".ai/context/agent_work/T472/larger_unit_dissent.jsonl",
    "routing": ".ai/context/agent_work/T472/corrected_routing_overlay.jsonl",
    "legacy": ".ai/context/agent_work/T472/corrected_legacy_19_docket.yaml",
    "agreement": ".ai/context/agent_work/T472/agreement_recalibration.yaml",
    "models": ".ai/context/agent_work/T472/model_panel_calibration.yaml",
    "frozen": ".ai/context/agent_work/T472/frozen_artifact_manifest.yaml",
    "summary": ".ai/context/agent_work/T472/correction_summary.md",
    "findings": ".ai/context/agent_work/T472/frontier_and_subagent_findings.md",
    "traceability": ".ai/context/agent_work/T472/evidence_traceability_matrix.md",
    "recommendation": ".ai/context/agent_work/T472/recommendation_summary.md",
    "roadmap": "docs/roadmap/T472_MODEL_PANEL_CALIBRATION_AND_PROVENANCE_CORRECTION.md",
    "tombstone": "docs/roadmap/T472_2JOHN_OWNER_PACKET.md",
    "handoff": ".ai/handoffs/T472/handoff.md",
    "focus": ".ai/control/current_focus.yaml",
    "status": ".ai/control/PROJECT_STATUS.md",
    "register": ".ai/control/chunking_theological_decision_register.yaml",
    "lessons": ".ai/control/chunking_lesson_index.yaml",
    "dad_outbox": ".digital-asset/mail/outbox.jsonl",
    "dad_context": ".digital-asset/context-map.json",
    "dad_lesson": ".digital-asset/lessons/t472_model_panel_calibration_lessons.yaml",
}
CLASS_COUNTS = {
    "coverage_gap": 3, "region_pair_span_mismatch": 127,
    "strict_larger_calibrated_dissent": 29, "m1_m5_oversplit_only": 44,
    "chapter_coincident_pair_alignment": 4, "variant_frontier": 777,
    "genuine_non_chapter_literary_disagreement": 64,
}
FEATURE_COUNTS = {
    "region_not_observed_as_model_span": 130, "pair_alignment_observation": 83,
    "pair_span_chapter_coincident": 76, "strict_larger_calibrated_dissent": 33,
    "m1_m5_oversplit_only": 46, "variant_or_frontier": 951,
}
MODEL_COUNTS = {
    "M1_cursor": (9237, 3795, 0, True),
    "M2_claude_sonnet5": (1135, 1, 139, True),
    "M3_claude_frontier": (1242, 0, 179, True),
    "M4_codex_gpt55": (1319, 4, 633, True),
    "M5_gemini_thinking": (15119, 9916, 0, False),
    "M6_fable5": (1456, 0, 126, True),
}
FALSE_AUTH_FLAGS = {
    "authorizes_model_deletion", "authorizes_model_rerun", "authorizes_target_selection",
    "authorizes_reviewed_gold", "authorizes_chunk_output", "authorizes_child_spans",
    "changes_route_behavior", "changes_evaluator_behavior", "creates_graph_truth",
    "creates_retrieval_truth", "creates_vector_truth", "selects_preferred_reading",
    "selects_source_tradition", "changes_canon_scope", "authorizes_theology_authority",
    "decides_variant_or_inspiration_status",
}


def _yaml(path: Path) -> dict[str, Any]:
    docs = [doc for doc in yaml.safe_load_all(path.read_text(encoding="utf-8")) if isinstance(doc, dict)]
    if not docs:
        raise ValueError(f"{path}: expected YAML mapping")
    merged: dict[str, Any] = {}
    for doc in docs:
        merged.update(doc)
    return merged


def _jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{line_no}: expected object")
        rows.append(value)
    return rows


def _find(rows: Any, key: str, value: str) -> dict[str, Any] | None:
    if not isinstance(rows, list):
        return None
    return next((row for row in rows if isinstance(row, dict) and row.get(key) == value), None)


def _require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate_t472(root: Path = ROOT, *, verify_frozen_sources: bool = True) -> list[str]:
    errors: list[str] = []
    paths = {name: root / rel for name, rel in REQUIRED_FILES.items()}
    missing = [rel for name, rel in REQUIRED_FILES.items() if not paths[name].is_file()]
    if missing:
        return [f"missing required T472 file {rel}" for rel in missing]
    try:
        task, control = _yaml(paths["task"]), _yaml(paths["control"])
        withdrawn_control, withdrawn_packet = _yaml(paths["withdrawn_control"]), _yaml(paths["withdrawn_packet"])
        classifications, dissent, routing = _jsonl(paths["classifications"]), _jsonl(paths["dissent"]), _jsonl(paths["routing"])
        legacy, agreement = _yaml(paths["legacy"]), _yaml(paths["agreement"])
        models, frozen = _yaml(paths["models"]), _yaml(paths["frozen"])
        focus, register, lessons = _yaml(paths["focus"]), _yaml(paths["register"]), _yaml(paths["lessons"])
        dad_context = json.loads(paths["dad_context"].read_text(encoding="utf-8"))
        dad_lesson, dad_rows = _yaml(paths["dad_lesson"]), _jsonl(paths["dad_outbox"])
    except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError) as exc:
        return [f"T472 artifact parse failure: {exc}"]

    _require(task.get("id") == "T472", "task id must be T472", errors)
    t472_is_current = focus.get("current_task") == "T472"
    t472_is_retained = (
        focus.get("t472_task") == ".ai/tasks/T472.task.yaml"
        and focus.get("t472_control") == ".ai/control/t472_model_panel_calibration_gate.yaml"
        and focus.get("t472_correction_overlay")
        == ".ai/context/agent_work/T472/corrected_routing_overlay.jsonl"
    )
    _require(
        t472_is_current or t472_is_retained,
        "current focus must retain T472 task, control, and correction overlay after later tasks advance",
        errors,
    )
    if t472_is_current:
        _require(
            "calibration" in str(focus.get("focus", "")).lower(),
            "current focus must describe calibration correction while T472 is current",
            errors,
        )
    _require(control.get("object_type") == "t472_model_panel_calibration_gate", "control object_type mismatch", errors)
    _require(control.get("supersedes_routing_only") is True, "T472 must supersede routing only", errors)
    authorization = control.get("authorization", {})
    for field in sorted(FALSE_AUTH_FLAGS):
        _require(authorization.get(field) is False, f"control.authorization.{field} must be false", errors)
    _require(authorization.get("preserves_model_evidence") is True, "T472 must preserve model evidence", errors)

    _require(len(classifications) == 1048, "classification ledger must contain 1048 rows", errors)
    ids = [str(row.get("source_id")) for row in classifications]
    _require(len(set(ids)) == 1048, "classification source_id values must be unique", errors)
    actual_classes = Counter(str(row.get("mechanical_class")) for row in classifications)
    _require(actual_classes == Counter(CLASS_COUNTS), "classification counts mismatch", errors)
    for field, expected in FEATURE_COUNTS.items():
        actual = sum(row.get(field) is True for row in classifications)
        _require(actual == expected, f"{field} count must be {expected}, got {actual}", errors)
    for row in classifications:
        label = str(row.get("source_id"))
        _require(row.get("candidate_eligible") is False, f"{label}: candidate_eligible must be false", errors)
        _require(row.get("promotion_authority") == "none", f"{label}: promotion_authority must be none", errors)
        _require(row.get("non_authorizing") is True, f"{label}: non_authorizing must be true", errors)

    _require(len(routing) == 1048, "corrected routing overlay must contain 1048 rows", errors)
    _require(len(dissent) == 33, "larger-unit dissent ledger must contain 33 rows", errors)
    for row in dissent:
        label = str(row.get("source_id"))
        _require(row.get("candidate_eligible") is False, f"{label}: dissent cannot be candidate eligible", errors)
        _require(row.get("promotion_authority") == "none", f"{label}: dissent promotion authority must be none", errors)

    expected_legacy = {
        "legacy_row_count": 19, "owner_ready_count": 0, "region_span_mismatch_count": 1,
        "chapter_coincident_count": 18, "strict_larger_dissent_count": 11,
        "potentially_defensible_after_literary_review_count": 8,
    }
    for field, expected in expected_legacy.items():
        _require(legacy.get(field) == expected, f"legacy docket {field} must be {expected}", errors)
    two_john = _find(legacy.get("rows"), "source_id", "DELTA-2John-001")
    _require(two_john is not None, "corrected legacy docket missing DELTA-2John-001", errors)
    if two_john:
        _require(two_john.get("disagreement_region") == "2John.1.1-2John.1.13", "2 John disagreement region mismatch", errors)
        _require(two_john.get("actual_pair_span") == "2John.1.12-2John.1.13", "2 John actual pair span mismatch", errors)
        _require(two_john.get("legacy_region_span_mismatch") is True, "2 John region/span defect must be explicit", errors)
        _require(two_john.get("owner_ready") is False, "2 John cannot be owner ready", errors)

    for artifact in (withdrawn_control, withdrawn_packet):
        _require(artifact.get("object_type") == "t472_withdrawn_2john_owner_packet", "old 2 John packet must be a withdrawal tombstone", errors)
        _require(artifact.get("t473_eligibility") is False, "withdrawn 2 John packet must block T473", errors)
    candidate, overlap = withdrawn_packet.get("candidate", {}), withdrawn_packet.get("existing_overlap", {})
    _require(candidate.get("actual_m4_span") == "2John.1.12-2John.1.13", "withdrawn packet must preserve actual M4 span", errors)
    _require(overlap.get("reviewed_gold_span") == "2John.1.1-2John.1.3", "withdrawn packet must expose reviewed-gold overlap", errors)

    _require(agreement.get("legacy_easy_agreement_count") == 144, "legacy agreement count must be 144", errors)
    _require(agreement.get("core_four_present_count") == 143, "core-four agreement count must be 143", errors)
    _require(agreement.get("dropped_when_M1_M5_are_ineligible") == ["AGREE-Esth-00001"], "only AGREE-Esth-00001 may drop", errors)
    _require(agreement.get("core_four_chapter_coincident_count") == 143, "all retained easy agreements must be chapter envelopes", errors)
    _require(agreement.get("automatic_reviewed_gold_count") == 0, "agreement cannot create automatic gold", errors)

    model_rows = {str(row.get("model_id")): row for row in models.get("models", []) if isinstance(row, dict)}
    _require(set(model_rows) == set(MODEL_COUNTS), "model calibration must contain exact six model ids", errors)
    for model_id, (chunks, singles, cross, consistent) in MODEL_COUNTS.items():
        row = model_rows.get(model_id, {})
        _require(row.get("chunk_count") == chunks, f"{model_id}: chunk count mismatch", errors)
        _require(row.get("single_verse_chunks") == singles, f"{model_id}: single-verse count mismatch", errors)
        _require(row.get("cross_chapter_chunks") == cross, f"{model_id}: cross-chapter count mismatch", errors)
        _require(row.get("manifest_progress_consistent") is consistent, f"{model_id}: manifest/progress consistency mismatch", errors)
        _require(row.get("eligible_for_confidence_or_majority") is False, f"{model_id}: voting eligibility must be false", errors)
        _require(row.get("delete_or_discard") is False, f"{model_id}: evidence must not be discarded", errors)
    _require(models.get("preferred_pair") is None, "preferred model pair must be retired", errors)
    _require(models.get("all_self_reported_confidence_role") == "archival_only", "self-reported confidence must be archival only", errors)

    artifacts = frozen.get("artifacts", [])
    _require(len(artifacts) == 4, "frozen artifact manifest must contain four sources", errors)
    for item in artifacts:
        if not isinstance(item, dict):
            errors.append("frozen artifact row must be a mapping")
            continue
        rel, digest = item.get("path"), item.get("sha256")
        _require(isinstance(digest, str) and len(digest) == 64, f"{rel}: invalid frozen sha256", errors)
        _require(item.get("mutation_allowed_by_T472") is False, f"{rel}: mutation must be forbidden", errors)
        if verify_frozen_sources and isinstance(rel, str):
            source = root / rel
            _require(source.is_file(), f"{rel}: frozen source missing", errors)
            if source.is_file():
                actual = hashlib.sha256(source.read_bytes()).hexdigest()
                _require(actual == digest, f"{rel}: frozen source hash drift", errors)

    decision = _find(register.get("decisions"), "decision_id", "CD-110")
    _require(decision is not None, "decision register missing CD-110", errors)
    if decision:
        _require("calibration" in str(decision.get("title", "")).lower(), "CD-110 must record calibration correction", errors)
        _require("scripts/validate_t472_model_panel_calibration_gate.py" in decision.get("validators", []), "CD-110 must use corrective validator", errors)
    lesson = _find(lessons.get("lessons"), "lesson_id", "LSN-055")
    _require(lesson is not None, "lesson index missing LSN-055", errors)
    if lesson:
        needed = {"region-span", "chapter-anchor", "negative-control", "proposer-critic"}
        _require(needed.issubset(set(lesson.get("tags", []))), "LSN-055 missing corrective tags", errors)
        _require("model_agreement_as_owner_approval" in lesson.get("non_authorizations", []), "LSN-055 must deny model agreement as owner approval", errors)

    dad_id = "msg-20260710-t472-model-panel-calibration-lessons"
    dad_row = _find(dad_rows, "message_id", dad_id)
    _require(dad_row is not None, "DAD outbox missing T472 lesson candidate", errors)
    if dad_row:
        _require(dad_row.get("trust_zone") == "candidate", "DAD lesson must remain candidate", errors)
        _require(dad_row.get("local_adoption_required") is True, "DAD lesson must require local adoption", errors)
        _require("pair_alignment_as_owner_selection" in dad_row.get("non_authorizations", []), "DAD message must deny pair authority", errors)
    context = _find(dad_context.get("contexts"), "context_id", "ctx-t472-model-panel-calibration-lessons")
    _require(context is not None, "DAD context map missing T472 context", errors)
    _require(dad_lesson.get("trust_zone") == "candidate", "DAD lesson slot must remain candidate", errors)
    _require(dad_lesson.get("local_adoption_required") is True, "DAD lesson slot must require local adoption", errors)
    _require("checking_system_principle" in dad_lesson, "DAD lesson must explain correction-system principle", errors)
    _require(len(dad_lesson.get("root_causes", [])) >= 6, "DAD lesson must record root causes", errors)

    narrative = ("summary", "findings", "traceability", "recommendation", "roadmap", "tombstone", "handoff", "status")
    text = "\n".join(paths[name].read_text(encoding="utf-8") for name in narrative)
    for needle in ("2John.1.12-2John.1.13", "2John.1.1-2John.1.3", "region", "chapter", "negative control", "proposer", "independent", "non-authorizing", "no reviewed gold"):
        _require(needle.lower() in text.lower(), f"T472 narrative surfaces missing {needle!r}", errors)
    _require("T472-A is recommended" not in text, "withdrawn T472-A recommendation must not survive", errors)
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--skip-frozen-source-hashes", action="store_true")
    args = parser.parse_args(argv)
    errors = validate_t472(args.root.resolve(), verify_frozen_sources=not args.skip_frozen_source_hashes)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("T472 model-panel calibration validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
