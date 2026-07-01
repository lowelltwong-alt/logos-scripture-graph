#!/usr/bin/env python3
"""Validate the T416 batch1 post-pilot review."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTROL = ROOT / ".ai/control/t416_batch1_post_pilot_review.yaml"
T415_MANIFEST = ROOT / ".ai/control/t415_batch1_output_pilot_manifest.yaml"
T415_HARNESS = ROOT / ".ai/control/t415_batch1_route_isolation_harness.yaml"
T414_PROMOTION = ROOT / ".ai/control/t414_batch1_parent_only_reviewed_gold_promotion.yaml"
T413_STRENGTHENING = ROOT / ".ai/control/t413_batch1_review_packet_strengthening.yaml"
GOLD_MANIFEST = ROOT / "eval/chunking_gold/per_form/epistle_opening_gold_manifest.json"
REGISTER = ROOT / ".ai/control/chunking_theological_decision_register.yaml"
LESSON_INDEX = ROOT / ".ai/control/chunking_lesson_index.yaml"
PREFLIGHT = ROOT / ".ai/control/chunking_agent_preflight.yaml"
READINESS = ROOT / ".ai/control/bible_chunking_readiness_map.yaml"
PROJECT_STATUS = ROOT / ".ai/control/PROJECT_STATUS.md"
CURRENT_FOCUS = ROOT / ".ai/control/current_focus.yaml"
ROADMAP_STATE = ROOT / "ROADMAP_STATE.yaml"
TASK = ROOT / ".ai/tasks/T416.task.yaml"
HANDOFF = ROOT / ".ai/handoffs/T416/handoff.md"
T415_HANDOFF = ROOT / ".ai/handoffs/T415/handoff.md"
ROADMAP_DOC = ROOT / "docs/roadmap/T416_BATCH1_POST_PILOT_REVIEW.md"
AUDIT = ROOT / ".ai/audits/reports/20260701-T416-batch1-post-pilot-review.md"
VALIDATE_ALL = ROOT / "scripts/validate_all.py"

EXPECTED = [
    ("T402-LC-064", "3John.1.1-3John.1.4", "3john_1_1_4_parent_only_reviewed_gold"),
    ("T402-LC-047", "2Cor.1.1-2Cor.1.2", "2cor_1_1_2_parent_only_reviewed_gold"),
    ("T402-LC-054", "1Tim.1.1-1Tim.1.2", "1tim_1_1_2_parent_only_reviewed_gold"),
    ("T402-LC-059", "Jas.1.1-Jas.1.1", "jas_1_1_parent_only_reviewed_gold"),
    ("T402-LC-063", "2John.1.1-2John.1.3", "2john_1_1_3_parent_only_reviewed_gold"),
]
NEXT_DOCKET = {
    "T402-LC-057": "Phlm.1.1-Phlm.1.7",
    "T402-LC-065": "Jude.1.1-Jude.1.2",
    "T402-LC-032": "Jonah.1.1-Jonah.1.3",
}
FORBIDDEN_TRUE_AUTHORITY = {
    "authorizes_child_spans",
    "authorizes_child_span_reviewed_gold",
    "authorizes_batch2_output",
    "authorizes_whole_bible_output_pass",
    "authorizes_broader_epistle_generalization",
    "authorizes_reviewed_gold_promotion",
    "authorizes_new_chunk_output",
    "authorizes_route_behavior_change",
    "authorizes_evaluator_change",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_embedding_or_vector_work",
    "authorizes_preferred_reading",
    "authorizes_source_tradition_preference",
    "authorizes_boundary_import",
}


class T416PostPilotError(ValueError):
    """Raised when the T416 post-pilot review is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise T416PostPilotError(f"{_rel(path)}: expected YAML mapping")
    return data


def _read_json(path: Path) -> dict[str, Any]:
    data = json.loads(_read_text(path))
    if not isinstance(data, dict):
        raise T416PostPilotError(f"{_rel(path)}: expected JSON object")
    return data


def _require_text(path: Path, phrases: tuple[str, ...]) -> None:
    text = _read_text(path)
    for phrase in phrases:
        if phrase not in text:
            raise T416PostPilotError(f"{_rel(path)} missing {phrase!r}")


def _span(start: str, end: str) -> str:
    return f"{start}-{end}"


def validate_t416_batch1_post_pilot_review() -> dict[str, Any]:
    control = _read_yaml(CONTROL)
    if control.get("task_id") != "T416":
        raise T416PostPilotError("control task_id must be T416")
    if control.get("verdict") != "APPROVE_BATCH1_POST_PILOT":
        raise T416PostPilotError("T416 verdict must be APPROVE_BATCH1_POST_PILOT")
    if control.get("status") != "APPROVE_BATCH1_POST_PILOT":
        raise T416PostPilotError("T416 status must be APPROVE_BATCH1_POST_PILOT")
    if control.get("scope", {}).get("post_pilot_decision_register_entry") != "CD-083":
        raise T416PostPilotError("T416 must record CD-083")
    if control.get("scope", {}).get("post_pilot_lesson_entry") != "LSN-038":
        raise T416PostPilotError("T416 must record LSN-038")

    authority = control.get("authority", {})
    for key in FORBIDDEN_TRUE_AUTHORITY:
        if authority.get(key) is not False:
            raise T416PostPilotError(f"authority.{key} must be false")
    if authority.get("records_post_pilot_review") is not True:
        raise T416PostPilotError("T416 must record post-pilot review")

    t415 = _read_yaml(T415_MANIFEST)
    same = control.get("same_baseline_review", {})
    output = t415.get("output_change", {})
    route = t415.get("route_isolation", {})
    expected_counts = {
        "baseline_chunk_count": 1138,
        "candidate_chunk_count": 1143,
        "added_overlay_count": 5,
    }
    for key, value in expected_counts.items():
        if same.get(key) != value or output.get(key) != value:
            raise T416PostPilotError(f"{key} must be {value}")
    if same.get("non_target_output_diff_detected") is not False:
        raise T416PostPilotError("non_target_output_diff_detected must be false")
    if same.get("changed_existing_output_ids") != []:
        raise T416PostPilotError("changed_existing_output_ids must be []")
    if same.get("removed_output_ids") != []:
        raise T416PostPilotError("removed_output_ids must be []")
    if route.get("non_target_byte_identical") is not True:
        raise T416PostPilotError("T415 route isolation must prove non-target byte identity")
    for key in ("baseline_chunk_sha256", "candidate_chunk_sha256", "preserved_baseline_prefix_sha256"):
        if same.get(key) != output.get(key):
            raise T416PostPilotError(f"{key} must match T415 manifest")

    exact = control.get("route_isolation_review", {}).get("exact_overlays")
    if not isinstance(exact, list) or len(exact) != 5:
        raise T416PostPilotError("route_isolation_review.exact_overlays must list five entries")
    exact_map = {item.get("candidate_id"): item for item in exact if isinstance(item, dict)}
    overlay_records = t415.get("overlay_records", [])
    overlay_map = {item.get("candidate_id"): item for item in overlay_records if isinstance(item, dict)}

    gold = _read_json(GOLD_MANIFEST)
    gold_by_case = {item["case_id"]: item for item in gold.get("reviewed_gold", [])}
    promotion = _read_yaml(T414_PROMOTION)
    promoted_by_candidate = {
        item["candidate_id"]: item for item in promotion.get("promoted_spans", [])
    }
    strengthening = _read_yaml(T413_STRENGTHENING)
    strengthened_by_candidate = {
        item["candidate_id"]: item for item in strengthening.get("docket", [])
    }
    for candidate_id, span, case_id in EXPECTED:
        review_entry = exact_map.get(candidate_id)
        overlay = overlay_map.get(candidate_id)
        promoted = promoted_by_candidate.get(candidate_id)
        strengthened = strengthened_by_candidate.get(candidate_id)
        if not all((review_entry, overlay, promoted, strengthened)):
            raise T416PostPilotError(f"missing linkage for {candidate_id}")
        if review_entry["span"] != span or _span(overlay["osis_start"], overlay["osis_end"]) != span:
            raise T416PostPilotError(f"{candidate_id} span mismatch")
        if promoted["selected_parent"] != span or strengthened["span"] != span:
            raise T416PostPilotError(f"{candidate_id} source span mismatch")
        if review_entry["reviewed_gold_case_id"] != case_id or overlay["reviewed_gold_case_id"] != case_id:
            raise T416PostPilotError(f"{candidate_id} reviewed_gold_case_id mismatch")
        if promoted["reviewed_gold_case_id"] != case_id or case_id not in gold_by_case:
            raise T416PostPilotError(f"{candidate_id} gold manifest mismatch")
        if overlay.get("included_text_span_count") is None or overlay["included_text_span_count"] < 1:
            raise T416PostPilotError(f"{candidate_id} overlay span count is invalid")

    child = control.get("child_necessity_review", {})
    if child.get("finding") != "child_spans_not_necessary_now_for_batch1":
        raise T416PostPilotError("child necessity finding is wrong")
    if child.get("selected_children") != [] or child.get("current_child_span_authority") != "none":
        raise T416PostPilotError("child spans must remain empty and unauthorized")

    t411 = control.get("t411_alignment", {})
    if set(t411.get("implemented_candidates", [])) != {item[0] for item in EXPECTED}:
        raise T416PostPilotError("implemented candidates must match T413 owner docket")
    if set(t411.get("not_implemented_from_prior_triage", [])) != set(NEXT_DOCKET):
        raise T416PostPilotError("not_implemented_from_prior_triage must be Phlm/Jude/Jonah")
    if t411.get("cursor_selected_targets") is not False:
        raise T416PostPilotError("Cursor target selection must be false")

    next_route = control.get("next_route", {})
    if next_route.get("route_type") != "owner_selection_for_batch2_review_packet_strengthening_only":
        raise T416PostPilotError("next_route must be review-packet strengthening only")
    if next_route.get("batch2_output_authorized") is not False:
        raise T416PostPilotError("batch2 output must not be authorized")
    if next_route.get("reviewed_gold_promotion_authorized") is not False:
        raise T416PostPilotError("reviewed-gold promotion must not be authorized")
    if next_route.get("cursor_execution_allowed") is not False:
        raise T416PostPilotError("Cursor execution must remain false")
    docket = next_route.get("recommended_batch2_owner_docket", [])
    docket_map = {item.get("candidate_id"): item.get("span") for item in docket if isinstance(item, dict)}
    if docket_map != NEXT_DOCKET:
        raise T416PostPilotError("recommended batch2 docket must be Phlm/Jude/Jonah")
    for hold in ("variant_sensitive_hold", "theological_risk_hold", "owner_decision_required", "do_not_chunk_now", "Revelation"):
        if hold not in next_route.get("must_stay_deferred", []):
            raise T416PostPilotError(f"must_stay_deferred missing {hold}")

    eval_review = control.get("evaluator_and_leaderboard_review", {})
    for key in ("evaluator_formula_changed", "leaderboard_updated", "improvement_claim_allowed"):
        if eval_review.get(key) is not False:
            raise T416PostPilotError(f"{key} must be false")

    for item in (
        "child_span_selection",
        "batch2_output",
        "whole_bible_output_pass",
        "broader_epistle_opening_generalization",
        "leaderboard_improvement_claim",
        "theology_authority_change",
    ):
        if item not in control.get("non_authorizations", []):
            raise T416PostPilotError(f"non_authorizations missing {item}")

    _require_text(REGISTER, ("decision_id: CD-083", "T416 batch1 post-pilot", "task_ids: [T416]"))
    _require_text(LESSON_INDEX, ("lesson_id: LSN-038", "CD-083", "T416 batch1"))
    _require_text(PREFLIGHT, ("CD-083", "LSN-038", "t416_batch1_post_pilot_review.yaml"))
    _require_text(READINESS, ("task_id: T416", "batch1_post_pilot_review", "CD-083"))
    _require_text(PROJECT_STATUS, ("T416 batch1 post-pilot review", "CD-083", "LSN-038"))
    _require_text(CURRENT_FOCUS, ("current_task: T416", "t416_batch1_post_pilot_review.yaml"))
    _require_text(ROADMAP_STATE, ("id: T416", "CD-083", "LSN-038"))
    _require_text(TASK, ("id: T416", "authorizes_batch2_output: false"))
    _require_text(HANDOFF, ("APPROVE_BATCH1_POST_PILOT", "T402-LC-057", "T402-LC-065", "T402-LC-032"))
    _require_text(T415_HANDOFF, ("T416 post-pilot review", "APPROVE_BATCH1_POST_PILOT"))
    _require_text(ROADMAP_DOC, ("T416 Batch1 Post-Pilot Review", "APPROVE_BATCH1_POST_PILOT"))
    _require_text(AUDIT, ("APPROVE_BATCH1_POST_PILOT", "P0: none", "P1: none", "P2: none open"))
    _require_text(VALIDATE_ALL, ("validate_t416_batch1_post_pilot_review.py",))
    return control


def main() -> int:
    try:
        validate_t416_batch1_post_pilot_review()
    except T416PostPilotError as exc:
        print(f"T416 batch1 post-pilot review validation failed: {exc}", file=sys.stderr)
        return 1
    print("T416 batch1 post-pilot review validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
