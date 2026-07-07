#!/usr/bin/env python3
"""Validate the T450 Bible edge taxonomy planning contract."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTROL = ROOT / ".ai" / "control" / "bible_edge_taxonomy_research_program.yaml"
ROADMAP = ROOT / "docs" / "roadmap" / "T450_BIBLE_EDGE_TAXONOMY_RESEARCH_PROGRAM.md"
HANDOFF = ROOT / ".ai" / "handoffs" / "T450" / "handoff.md"
DAD_OUTBOX = ROOT / ".digital-asset" / "mail" / "outbox.jsonl"

REQUIRED_LANES = {
    "structural_source_occurrence",
    "editorial_metadata",
    "intertext_canonical",
    "prophecy_apocalyptic",
    "orthodox_creedal_theology",
    "covenant_biblical_theology",
    "sacrifice_temple_priesthood",
    "literary_discourse_genre",
    "chronology_calendar_geography",
    "linguistic_original_language",
    "manuscript_textual_witness",
    "historical_cultural_reception",
    "apologetic_polemic",
}

FORBIDDEN_TRUE_AUTHORITY = {
    "expands_predicate_registry",
    "generates_graph_edges",
    "creates_candidate_edge_rows",
    "creates_retrieval_truth",
    "creates_vector_truth",
    "runs_embeddings_or_builds_indexes",
    "imports_boundary_material",
    "changes_chunk_output",
    "promotes_reviewed_gold",
    "changes_route_or_evaluator_behavior",
    "selects_preferred_reading_or_source_tradition",
    "selects_canon_scope",
    "selects_theological_system",
    "authorizes_theology_authority",
    "authorizes_apologetic_or_polemic_conclusion",
}

EVIDENCE_ONLY_TERMS = {
    "Strong's numbers",
    "WJ or red-letter formatting",
    "editorial cross-references",
    "oldest witness",
    "model agreement",
}

DAD_MESSAGE_IDS = {
    "msg-20260705-t450-bible-edge-taxonomy-program",
    "msg-20260705-dad-dirty-parallel-rust-rollout",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_yaml(path: Path) -> dict:
    if not path.exists():
        fail(f"missing {path.relative_to(ROOT)}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        fail(f"{path.relative_to(ROOT)} must be a mapping")
    return data


def validate_control(data: dict) -> None:
    if data.get("task_id") != "T450":
        fail("control task_id must be T450")
    if data.get("planning_only") is not True or data.get("non_authorizing") is not True:
        fail("control must be planning_only and non_authorizing")

    boundary = data.get("authority_boundary")
    if not isinstance(boundary, dict):
        fail("authority_boundary must be a mapping")
    for key in FORBIDDEN_TRUE_AUTHORITY:
        if boundary.get(key) is not False:
            fail(f"authority_boundary.{key} must be false")

    registry = data.get("current_predicate_registry_snapshot", {})
    registered = set(registry.get("registered_predicates", []))
    expected_registered = {
        "editorial_cross_reference",
        "quotesFrom",
        "alludesTo",
        "echoes",
        "fulfills",
        "typifies",
        "parallelTo",
        "thematicallyRelatedTo",
        "groundedIn",
        "renders",
        "occursIn",
    }
    if registered != expected_registered:
        fail("current predicate registry snapshot is missing or changed")

    evidence_floor = data.get("global_evidence_floor", {})
    shortcuts = set(evidence_floor.get("forbidden_shortcuts", []))
    evidence_only = "\n".join(evidence_floor.get("evidence_only_metadata", []))
    shortcut_text = "\n".join(shortcuts)
    combined = f"{evidence_only}\n{shortcut_text}"
    for term in EVIDENCE_ONLY_TERMS:
        if term not in combined:
            fail(f"missing evidence-only/forbidden-shortcut term: {term}")

    lanes = data.get("edge_family_lanes")
    if not isinstance(lanes, list):
        fail("edge_family_lanes must be a list")
    lane_ids = {lane.get("lane_id") for lane in lanes if isinstance(lane, dict)}
    missing = sorted(REQUIRED_LANES - lane_ids)
    if missing:
        fail(f"missing required lane(s): {', '.join(missing)}")

    for lane in lanes:
        if not isinstance(lane, dict):
            fail("each edge family lane must be a mapping")
        lane_id = lane.get("lane_id")
        for key in (
            "scope",
            "risk_level",
            "candidate_predicate_names",
            "evidence_requirements",
            "assertion_mode_policy",
            "escalation_triggers",
            "non_authorizations",
        ):
            if key not in lane:
                fail(f"lane {lane_id} missing {key}")
        if not lane["evidence_requirements"]:
            fail(f"lane {lane_id} must have evidence requirements")
        if not lane["escalation_triggers"]:
            fail(f"lane {lane_id} must have escalation triggers")
        if not lane["non_authorizations"]:
            fail(f"lane {lane_id} must have non_authorizations")

    frontier = data.get("model_review_ladder", [])
    frontier_text = yaml.safe_dump(frontier, sort_keys=True)
    for required in ("frontier_review", "owner_gate", "implementation"):
        if required not in frontier_text:
            fail(f"model_review_ladder missing {required}")

    rust_lane = data.get("future_rust_validator_lane", {})
    if not rust_lane.get("rust_allowed_for") or not rust_lane.get("rust_forbidden_for"):
        fail("future_rust_validator_lane must define allowed and forbidden Rust uses")
    forbidden_rust_text = "\n".join(rust_lane["rust_forbidden_for"])
    for forbidden in ("deciding theology", "selecting predicates", "resolving textual variants"):
        if forbidden not in forbidden_rust_text:
            fail(f"Rust forbidden-use list missing {forbidden}")


def validate_text_files() -> None:
    for path in (ROADMAP, HANDOFF):
        if not path.exists():
            fail(f"missing {path.relative_to(ROOT)}")
        text = path.read_text(encoding="utf-8").lower()
        for phrase in (
            "planning-only",
            "predicate registry",
            "graph edges",
            "theology authority",
        ):
            if phrase not in text:
                fail(f"{path.relative_to(ROOT)} missing phrase: {phrase}")


def validate_dad_outbox() -> None:
    if not DAD_OUTBOX.exists():
        fail("missing DAD outbox")
    seen: set[str] = set()
    for line_number, line in enumerate(DAD_OUTBOX.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"DAD outbox line {line_number} is invalid JSON: {exc}")
        message_id = row.get("message_id")
        if message_id in DAD_MESSAGE_IDS:
            seen.add(message_id)
            if row.get("trust_zone") != "candidate":
                fail(f"{message_id} must be candidate trust_zone")
            if row.get("requires_local_adoption") is not True:
                fail(f"{message_id} must require local adoption")
            non_auth = "\n".join(row.get("non_authorizations", []))
            if "dad_override_local_authority" not in non_auth:
                fail(f"{message_id} must forbid DAD overriding local authority")
    missing = sorted(DAD_MESSAGE_IDS - seen)
    if missing:
        fail(f"missing DAD outbox message(s): {', '.join(missing)}")


def main() -> int:
    data = load_yaml(CONTROL)
    validate_control(data)
    validate_text_files()
    validate_dad_outbox()
    print("T450 Bible edge taxonomy planning contract OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
