#!/usr/bin/env python3
"""Validate that owner-selection dockets cannot be treated as implementation authority."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
ROADMAP_STATE = ROOT / "ROADMAP_STATE.yaml"
T344_TASK = ROOT / ".ai" / "tasks" / "T344.task.yaml"
T345_TASK = ROOT / ".ai" / "tasks" / "T345.task.yaml"
READINESS_MAP = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
HARNESS_ROADMAP = ROOT / ".ai" / "control" / "harness_upgrade_roadmap.yaml"
T344_DOCKET = ROOT / "docs" / "roadmap" / "T344_REVELATION_OWNER_SELECTION_DOCKET.md"
REVIEW_PACKET = ROOT / "eval" / "chunking_gold" / "review_packets" / "rev12_14_symbolic_scenes_review.md"
VALIDATOR_PATH = "scripts/validate_owner_selection_implementation_gate.py"

OWNER_OPTIONS = {"REV-T344-A", "REV-T344-B", "REV-T344-C", "REV-T344-D", "REV-T344-E"}
IMPLEMENTATION_OPTIONS = {"REV-T344-B", "REV-T344-C"}


class OwnerSelectionGateError(ValueError):
    """Raised when owner-selection and implementation state disagree."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise OwnerSelectionGateError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        text = _read_text(path)
        if text.startswith("---\n"):
            parts = text.split("---\n", 2)
            if len(parts) == 3:
                text = parts[1] + "\n" + parts[2]
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise OwnerSelectionGateError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise OwnerSelectionGateError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _extract_markdown_yaml(path: Path, required_key: str) -> dict[str, Any]:
    text = _read_text(path)
    blocks = re.findall(r"```yaml\s*\n(.*?)\n```", text, flags=re.DOTALL)
    for block in blocks:
        try:
            data = yaml.safe_load(block)
        except yaml.YAMLError as exc:
            raise OwnerSelectionGateError(f"{_rel(path)}: fenced YAML unreadable: {exc}") from exc
        if isinstance(data, dict) and required_key in data:
            value = data[required_key]
            if not isinstance(value, dict):
                raise OwnerSelectionGateError(f"{_rel(path)}: {required_key} must be a mapping")
            return value
    raise OwnerSelectionGateError(f"{_rel(path)}: missing fenced YAML key {required_key}")


def _find_task(state: dict[str, Any], task_id: str) -> tuple[dict[str, Any], str]:
    phases = state.get("phases")
    if not isinstance(phases, dict):
        raise OwnerSelectionGateError("ROADMAP_STATE.yaml: phases must be a mapping")
    for phase in phases.values():
        if not isinstance(phase, dict):
            continue
        for collection_name in ("tasks", "future_sequence"):
            collection = phase.get(collection_name, [])
            if not isinstance(collection, list):
                continue
            for task in collection:
                if isinstance(task, dict) and task.get("id") == task_id:
                    return task, collection_name
    raise OwnerSelectionGateError(f"ROADMAP_STATE.yaml: missing task {task_id}")


def _require_false(mapping: dict[str, Any], key: str, label: str) -> None:
    if mapping.get(key) is not False:
        raise OwnerSelectionGateError(f"{label}.{key} must be false")


def _require_equal(actual: Any, expected: Any, label: str) -> None:
    if actual != expected:
        raise OwnerSelectionGateError(f"{label} must be {expected!r}, got {actual!r}")


def _selected_option(*values: str) -> str:
    unique = set(values)
    if len(unique) != 1:
        raise OwnerSelectionGateError(f"selected_option surfaces disagree: {sorted(unique)}")
    selected = values[0]
    if selected != "pending" and selected not in OWNER_OPTIONS:
        raise OwnerSelectionGateError(f"selected_option {selected!r} is not a valid T344 option")
    return selected


def _implementation_attempted(t345_state: dict[str, Any], t345_task: Path) -> bool:
    return t345_task.exists() or t345_state.get("status") in {"in_progress", "complete"}


def _require_non_authorizing_revelation_state(
    *,
    auth: dict[str, Any],
    docket_owner: dict[str, Any],
    packet_decision: dict[str, Any],
    selected_target: dict[str, Any],
    next_route: dict[str, Any],
) -> None:
    for label, mapping, implementation_key in (
        ("T344.authorization", auth, "revelation_implementation_allowed"),
        ("T344 docket owner_selection", docket_owner, "implementation_allowed"),
        ("review packet human_review_decision", packet_decision, "implementation_allowed"),
        ("readiness selected_review_target", selected_target, "implementation_allowed"),
    ):
        _require_false(mapping, implementation_key, label)
        _require_false(mapping, "output_change_authorized", label)
        _require_false(mapping, "reviewed_gold_promoted", label)
    _require_false(next_route, "implementation_authorized", "readiness.next_route")
    _require_false(next_route, "output_change_authorized", "readiness.next_route")


def _validate_harn_012(harness_roadmap: Path) -> None:
    data = _read_yaml(harness_roadmap)
    candidates = data.get("candidate_harnesses")
    if not isinstance(candidates, list):
        raise OwnerSelectionGateError(f"{_rel(harness_roadmap)}: candidate_harnesses must be a list")
    harn_012 = next(
        (item for item in candidates if isinstance(item, dict) and item.get("harness_id") == "HARN-012"),
        None,
    )
    if harn_012 is None:
        raise OwnerSelectionGateError(f"{_rel(harness_roadmap)}: missing HARN-012")
    _require_equal(harn_012.get("status"), "implemented_v1", "HARN-012.status")
    surfaces = harn_012.get("implemented_surfaces")
    if not isinstance(surfaces, list) or VALIDATOR_PATH not in surfaces:
        raise OwnerSelectionGateError(f"HARN-012.implemented_surfaces must include {VALIDATOR_PATH}")
    if "implementation_without_owner_selection" not in harn_012.get("non_authorizations", []):
        raise OwnerSelectionGateError("HARN-012.non_authorizations missing implementation_without_owner_selection")


def validate_owner_selection_implementation_gate(
    *,
    roadmap_state: Path = ROADMAP_STATE,
    t344_task: Path = T344_TASK,
    t345_task: Path = T345_TASK,
    readiness_map: Path = READINESS_MAP,
    harness_roadmap: Path = HARNESS_ROADMAP,
    docket: Path = T344_DOCKET,
    review_packet: Path = REVIEW_PACKET,
) -> dict[str, Any]:
    """Return a compact state summary when the owner-selection gate is valid."""

    _validate_harn_012(harness_roadmap)

    state = _read_yaml(roadmap_state)
    task = _read_yaml(t344_task)
    readiness = _read_yaml(readiness_map)
    docket_owner = _extract_markdown_yaml(docket, "owner_selection")
    packet_decision = _extract_markdown_yaml(review_packet, "human_review_decision")

    roadmap_t344, t344_collection = _find_task(state, "T344")
    roadmap_t345, t345_collection = _find_task(state, "T345")
    if t344_collection != "tasks":
        raise OwnerSelectionGateError("T344 must remain an active task until the owner-selection gate is closed")
    if t345_collection != "future_sequence":
        raise OwnerSelectionGateError("T345 must remain in future_sequence until the gate is satisfied")

    auth = task.get("authorization")
    if not isinstance(auth, dict):
        raise OwnerSelectionGateError(f"{_rel(t344_task)}: authorization must be a mapping")
    if auth.get("owner_selection_required") is not True:
        raise OwnerSelectionGateError("T344.authorization.owner_selection_required must be true")

    lanes = readiness.get("lane_sequence")
    if not isinstance(lanes, list):
        raise OwnerSelectionGateError(f"{_rel(readiness_map)}: lane_sequence must be a list")
    by_lane = {lane.get("lane_id"): lane for lane in lanes if isinstance(lane, dict)}
    revelation_lane = by_lane.get("revelation_apocalyptic")
    if not isinstance(revelation_lane, dict):
        raise OwnerSelectionGateError(f"{_rel(readiness_map)}: missing revelation_apocalyptic lane")
    selected_target = revelation_lane.get("selected_review_target")
    if not isinstance(selected_target, dict):
        raise OwnerSelectionGateError("revelation_apocalyptic.selected_review_target must be a mapping")

    next_route = readiness.get("next_route")
    if not isinstance(next_route, dict):
        raise OwnerSelectionGateError(f"{_rel(readiness_map)}: next_route must be a mapping")

    selected_option_values = [
        str(auth.get("selected_option")),
        str(docket_owner.get("selected_option")),
        str(packet_decision.get("selected_option")),
        str(selected_target.get("selected_option")),
        str(roadmap_t344.get("selected_option")),
    ]
    if "selected_option" in next_route:
        selected_option_values.append(str(next_route.get("selected_option")))
    selected_option = _selected_option(*selected_option_values)

    owner_statuses = {
        str(auth.get("owner_selection_status")),
        str(selected_target.get("owner_selection_status")),
        str(roadmap_t344.get("owner_selection_status")),
    }
    if "owner_selection_status" in next_route and next_route.get("task_id") != "T369":
        owner_statuses.add(str(next_route.get("owner_selection_status")))
    if len(owner_statuses) != 1:
        raise OwnerSelectionGateError(f"owner_selection_status surfaces disagree: {sorted(owner_statuses)}")
    owner_status = owner_statuses.pop()

    if selected_option == "pending" or owner_status == "pending":
        _require_equal(selected_option, "pending", "selected_option")
        _require_equal(owner_status, "pending", "owner_selection_status")
        _require_equal(roadmap_t344.get("status"), "in_progress", "ROADMAP_STATE.T344.status")
        _require_equal(roadmap_t345.get("status"), "planned", "ROADMAP_STATE.T345.status")
        _require_equal(roadmap_t345.get("requires_reviewed_gold"), True, "ROADMAP_STATE.T345.requires_reviewed_gold")
        _require_equal(
            roadmap_t345.get("requires_owner_selection_gate"),
            VALIDATOR_PATH,
            "ROADMAP_STATE.T345.requires_owner_selection_gate",
        )
        if _implementation_attempted(roadmap_t345, t345_task):
            raise OwnerSelectionGateError(
                "T345 implementation cannot start while T344 owner selection is pending"
            )
        _require_non_authorizing_revelation_state(
            auth=auth,
            docket_owner=docket_owner,
            packet_decision=packet_decision,
            selected_target=selected_target,
            next_route=next_route,
        )
        return {
            "gate_id": "HARN-012",
            "owner_selection_status": owner_status,
            "selected_option": selected_option,
            "t345_status": roadmap_t345.get("status"),
            "implementation_allowed": False,
        }

    _require_equal(owner_status, "selected", "owner_selection_status")
    if roadmap_t344.get("status") not in {"in_progress", "complete"}:
        raise OwnerSelectionGateError("ROADMAP_STATE.T344.status must be 'in_progress' or 'complete'")
    _require_equal(roadmap_t345.get("status"), "planned", "ROADMAP_STATE.T345.status")
    _require_equal(roadmap_t345.get("requires_reviewed_gold"), True, "ROADMAP_STATE.T345.requires_reviewed_gold")
    _require_equal(
        roadmap_t345.get("requires_owner_selection_gate"),
        VALIDATOR_PATH,
        "ROADMAP_STATE.T345.requires_owner_selection_gate",
    )

    if selected_option not in IMPLEMENTATION_OPTIONS and _implementation_attempted(roadmap_t345, t345_task):
        raise OwnerSelectionGateError(
            f"T345 implementation is not allowed for selected option {selected_option}"
        )

    if selected_option not in IMPLEMENTATION_OPTIONS:
        _require_non_authorizing_revelation_state(
            auth=auth,
            docket_owner=docket_owner,
            packet_decision=packet_decision,
            selected_target=selected_target,
            next_route=next_route,
        )
        if selected_option == "REV-T344-E":
            next_task_id = next_route.get("task_id")
            if next_task_id not in {"T351", "T352", "T354", "T355", "T356", "T368", "T369"}:
                raise OwnerSelectionGateError(
                    "readiness.next_route.task_id must be 'T351', 'T352', 'T354', 'T355', 'T356', 'T368', or 'T369' under REV-T344-E"
                )
            if next_task_id == "T351":
                _require_equal(
                    next_route.get("route_type"),
                    "bible_wide_research_triage",
                    "readiness.next_route.route_type",
                )
                _require_equal(
                    next_route.get("requires_triage_before_lane_selection"),
                    True,
                    "readiness.next_route.requires_triage_before_lane_selection",
                )
                _require_equal(
                    next_route.get("next_review_lane_after_completion"),
                    "select_from_review_packet_ready_lanes",
                    "readiness.next_route.next_review_lane_after_completion",
                )
            if next_task_id == "T352":
                _require_equal(
                    next_route.get("route_type"),
                    "epistle_argument_review_packet_prep",
                    "readiness.next_route.route_type",
                )
                _require_equal(next_route.get("prior_triage_task"), "T351", "readiness.next_route.prior_triage_task")
                _require_equal(
                    next_route.get("review_packet_lane"),
                    "epistle_argument",
                    "readiness.next_route.review_packet_lane",
                )
                _require_equal(
                    next_route.get("packet_status"),
                    "pending_human_review",
                    "readiness.next_route.packet_status",
                )
            if next_task_id == "T354":
                _require_equal(
                    next_route.get("route_type"),
                    "gospel_wj_marker_inventory_harness",
                    "readiness.next_route.route_type",
                )
                _require_equal(next_route.get("prior_triage_task"), "T351", "readiness.next_route.prior_triage_task")
                _require_equal(next_route.get("prior_inventory_task"), "T353", "readiness.next_route.prior_inventory_task")
                _require_equal(
                    next_route.get("review_packet_lane"),
                    "gospel_discourse_wj",
                    "readiness.next_route.review_packet_lane",
                )
                _require_equal(
                    next_route.get("inventory_status"),
                    "generated_non_authorizing",
                    "readiness.next_route.inventory_status",
                )
            if next_task_id == "T355":
                _require_equal(
                    next_route.get("route_type"),
                    "wj_speaker_discourse_policy_and_target_selection",
                    "readiness.next_route.route_type",
                )
                _require_equal(next_route.get("prior_triage_task"), "T351", "readiness.next_route.prior_triage_task")
                _require_equal(next_route.get("prior_inventory_task"), "T354", "readiness.next_route.prior_inventory_task")
                _require_equal(
                    next_route.get("review_packet_lane"),
                    "gospel_discourse_wj",
                    "readiness.next_route.review_packet_lane",
                )
                _require_equal(
                    next_route.get("policy"),
                    ".ai/control/wj_speaker_discourse_policy.yaml",
                    "readiness.next_route.policy",
                )
                _require_equal(
                    next_route.get("selected_target"),
                    "john3_wj_speaker_boundary",
                    "readiness.next_route.selected_target",
                )
                _require_equal(
                    next_route.get("selected_target_status"),
                    "selected_for_next_owner_review",
                    "readiness.next_route.selected_target_status",
                )
                _require_false(next_route, "reviewed_gold_promoted", "readiness.next_route")
            if next_task_id == "T356":
                _require_equal(
                    next_route.get("route_type"),
                    "john3_wj_owner_review_docket",
                    "readiness.next_route.route_type",
                )
                _require_equal(next_route.get("prior_triage_task"), "T351", "readiness.next_route.prior_triage_task")
                _require_equal(next_route.get("prior_inventory_task"), "T354", "readiness.next_route.prior_inventory_task")
                _require_equal(next_route.get("prior_policy_task"), "T355", "readiness.next_route.prior_policy_task")
                _require_equal(
                    next_route.get("review_packet_lane"),
                    "gospel_discourse_wj",
                    "readiness.next_route.review_packet_lane",
                )
                _require_equal(
                    next_route.get("docket"),
                    ".ai/control/john3_wj_owner_review_docket.yaml",
                    "readiness.next_route.docket",
                )
                _require_equal(
                    next_route.get("selected_target"),
                    "john3_wj_speaker_boundary",
                    "readiness.next_route.selected_target",
                )
                _require_equal(
                    next_route.get("john3_owner_selection_status"),
                    "pending",
                    "readiness.next_route.john3_owner_selection_status",
                )
                _require_equal(
                    next_route.get("john3_selected_option"),
                    "pending",
                    "readiness.next_route.john3_selected_option",
                )
                _require_false(next_route, "reviewed_gold_promoted", "readiness.next_route")
            if next_task_id == "T368":
                _require_equal(
                    next_route.get("route_type"),
                    "epistle_argument_review_packet_strengthening",
                    "readiness.next_route.route_type",
                )
                _require_equal(
                    next_route.get("selected_target"),
                    "1cor8_10_food_offered_to_idols",
                    "readiness.next_route.selected_target",
                )
                _require_equal(
                    next_route.get("review_packet"),
                    "eval/chunking_gold/review_packets/1cor8_10_food_offered_to_idols_review.md",
                    "readiness.next_route.review_packet",
                )
                _require_equal(next_route.get("prior_owner_decision_task"), "T367", "readiness.next_route.prior_owner_decision_task")
                _require_equal(
                    next_route.get("orthodox_firewall"),
                    ".ai/control/orthodox_hermeneutic_firewall_docket.yaml",
                    "readiness.next_route.orthodox_firewall",
                )
                _require_equal(
                    next_route.get("textual_critical_policy_docket"),
                    ".ai/control/textual_critical_policy_docket.yaml",
                    "readiness.next_route.textual_critical_policy_docket",
                )
                _require_equal(next_route.get("review_only"), True, "readiness.next_route.review_only")
                _require_equal(next_route.get("john3_owner_selection_status"), "selected", "readiness.next_route.john3_owner_selection_status")
                _require_equal(next_route.get("john3_selected_option"), "JOHN3-T356-B", "readiness.next_route.john3_selected_option")
                _require_false(next_route, "reviewed_gold_promoted", "readiness.next_route")
                _require_false(next_route, "route_behavior_authorized", "readiness.next_route")
                _require_false(next_route, "evaluator_change_authorized", "readiness.next_route")
                _require_false(next_route, "graph_edge_generation_allowed", "readiness.next_route")
                _require_false(next_route, "retrieval_truth_authorized", "readiness.next_route")
            if next_task_id == "T369":
                expected = {
                    "route_type": "epistle_argument_owner_review_gate",
                    "recommended_target": "epistle_argument",
                    "selected_target": "1cor8_10_food_offered_to_idols",
                    "selected_passage": "1Cor.8-1Cor.10",
                    "exact_parent_candidate": "1Cor.8.1-1Cor.10.33",
                    "review_packet": "eval/chunking_gold/review_packets/1cor8_10_food_offered_to_idols_review.md",
                    "owner_review_docket": ".ai/control/1cor8_10_epistle_owner_review_docket.yaml",
                    "packet_status": "pending_human_review",
                    "owner_selection_status": "pending_owner_decision",
                    "prior_owner_decision_task": "T367",
                    "packet_strengthening_task": "T368",
                    "prior_packet_task": "T352",
                    "prior_issue_dossier_task": "T361",
                    "orthodox_firewall": ".ai/control/orthodox_hermeneutic_firewall_docket.yaml",
                    "textual_critical_policy_docket": ".ai/control/textual_critical_policy_docket.yaml",
                }
                for key, value in expected.items():
                    _require_equal(next_route.get(key), value, f"readiness.next_route.{key}")
                _require_equal(next_route.get("review_only"), True, "readiness.next_route.review_only")
                _require_false(next_route, "reviewed_gold_promoted", "readiness.next_route")
                _require_false(next_route, "route_behavior_authorized", "readiness.next_route")
                _require_false(next_route, "evaluator_change_authorized", "readiness.next_route")
                _require_false(next_route, "graph_edge_generation_allowed", "readiness.next_route")
                _require_false(next_route, "retrieval_truth_authorized", "readiness.next_route")
            _require_equal(
                packet_decision.get("decision"),
                "requires_more_research_before_gold",
                "review packet human_review_decision.decision",
            )
            _require_equal(
                auth.get("revelation_research_prep_only_allowed"),
                True,
                "T344.authorization.revelation_research_prep_only_allowed",
            )
            _require_equal(
                auth.get("next_review_lane_after_revelation_research_prep"),
                "epistle_argument_boundaries",
                "T344.authorization.next_review_lane_after_revelation_research_prep",
            )
            for label, mapping in (
                ("T344 docket owner_selection", docket_owner),
                ("review packet human_review_decision", packet_decision),
                ("ROADMAP_STATE.T344", roadmap_t344),
            ):
                continuing = mapping.get("continuing_authorization")
                if not isinstance(continuing, dict):
                    raise OwnerSelectionGateError(f"{label}.continuing_authorization must be a mapping")
                _require_equal(
                    continuing.get("revelation_research_prep_only"),
                    True,
                    f"{label}.continuing_authorization.revelation_research_prep_only",
                )
                _require_equal(
                    continuing.get("next_review_lane_after_revelation_research_prep"),
                    "epistle_argument_boundaries",
                    f"{label}.continuing_authorization.next_review_lane_after_revelation_research_prep",
                )

    if selected_option in IMPLEMENTATION_OPTIONS and _implementation_attempted(roadmap_t345, t345_task):
        for label, mapping, implementation_key in (
            ("T344.authorization", auth, "revelation_implementation_allowed"),
            ("T344 docket owner_selection", docket_owner, "implementation_allowed"),
            ("review packet human_review_decision", packet_decision, "implementation_allowed"),
            ("readiness selected_review_target", selected_target, "implementation_allowed"),
        ):
            if mapping.get(implementation_key) is not True:
                raise OwnerSelectionGateError(f"{label}.{implementation_key} must be true before T345")
            if mapping.get("output_change_authorized") is not True:
                raise OwnerSelectionGateError(f"{label}.output_change_authorized must be true before T345")
            if mapping.get("reviewed_gold_promoted") is not True:
                raise OwnerSelectionGateError(f"{label}.reviewed_gold_promoted must be true before T345")
        return {
            "gate_id": "HARN-012",
            "owner_selection_status": owner_status,
            "selected_option": selected_option,
            "t345_status": roadmap_t345.get("status"),
            "implementation_allowed": True,
        }

    return {
        "gate_id": "HARN-012",
        "owner_selection_status": owner_status,
        "selected_option": selected_option,
        "t345_status": roadmap_t345.get("status"),
        "implementation_allowed": False,
    }


def main() -> int:
    try:
        validate_owner_selection_implementation_gate()
    except OwnerSelectionGateError as exc:
        print(f"Owner-selection implementation gate validation failed: {exc}", file=sys.stderr)
        return 1
    print("Owner-selection implementation gate validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
