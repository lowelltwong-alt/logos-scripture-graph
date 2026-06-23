#!/usr/bin/env python3
"""Validate T392 Eph.1.3-Eph.1.14 review-packet strengthening."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
PACKET = ROOT / "eval" / "chunking_gold" / "review_packets" / "eph1_3_14_argument_review.md"
INDEX = ROOT / "eval" / "chunking_gold" / "review_packets" / "review_packet_index.json"
OBSERVED = ROOT / "eval" / "chunking_gold" / "stress_atlas" / "observed_stress_behavior.json"
TASK = ROOT / ".ai" / "tasks" / "T392.task.yaml"
ROADMAP_DOC = ROOT / "docs" / "roadmap" / "T392_EPH1_REVIEW_PACKET_STRENGTHENING.md"
AUDIT_NOTE = ROOT / ".ai" / "audits" / "reports" / "20260623-T392-eph1-review-packet-strengthening.md"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
LESSON_INDEX = ROOT / ".ai" / "control" / "chunking_lesson_index.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
MAIN_TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"
ROADMAP_STATE = ROOT / "ROADMAP_STATE.yaml"
CURRENT_FOCUS = ROOT / ".ai" / "control" / "current_focus.yaml"
PROJECT_STATUS = ROOT / ".ai" / "control" / "PROJECT_STATUS.md"

PACKET_REQUIRED_PHRASES = {
    "Status: `pending_human_review`",
    "Stress atlas case ID: `eph1_3_14_greek_sentence`",
    "Decision: pending",
    "Implementation allowed: false",
    "Output change authorized: false",
    "Reviewed gold promoted: false",
    "T392 strengthened packet: true",
    "Owner-selected option: `T385-A`",
    "Review-only strengthening: true",
    "This packet does not authorize output-changing work.",
    "exact_passage_scope: `Eph.1.3-Eph.1.14`",
    "immediate_previous_context:",
    "immediate_following_context:",
    "paragraph_or_section_context:",
    "chapter_context:",
    "book_argument_or_narrative_context:",
    "canonical_context_links_considered:",
    "original_language_context_if_used:",
    "historical_cultural_context_if_used:",
    "source_metadata_context_if_used:",
    "context_needed_to_avoid_prooftexting:",
    "assumptions_avoided:",
    "orthodox_options_preserved:",
    "theological_downstream_risks:",
    "reviewed_gold_dependency:",
    "non_authorizations:",
    "validator_or_test_plan:",
    "boundary-claim:79-EPHeng-web.usfm:25:p",
    "source_metadata_sensitive",
    "strongs_metadata_present",
    "divine_name_title_capitalization_sensitive",
    "God` in `Eph.1.14` with",
    "`G1519`",
    "Phrase-before-word rule:",
    "variant_sensitive_for_current_packet: false",
    "internal_target_variant_observed_in_current_sidecars: false",
    "exact_internal_variant_refs: []",
    "TCP-T378-B",
    "election and predestination",
    "adoption language",
    "redemption and forgiveness",
    "sealing and Holy Spirit",
    "Trinitarian economy",
    "we/you",
    "Premortem Red-Team Pass",
    "No option above is approved. No reviewed gold is promoted.",
    "Goal 5 owner reviewed-gold promotion decision packet",
}

PACKET_FORBIDDEN_PHRASES = {
    "Status: `reviewed_gold`",
    "implementation_allowed: true",
    "output_change_authorized: true",
    "reviewed_gold_promoted: true",
    "approved for implementation",
    "Reviewed gold promoted: true",
    "Output change authorized: true",
    "Implementation allowed: true",
}

SURFACE_REQUIREMENTS = {
    TASK: {"id: T392", "selected_option: T385-A", "authorizes_chunk_output_change: false", "authorizes_reviewed_gold: false"},
    ROADMAP_DOC: {"T392", "Eph.1.3-Eph.1.14", "CD-067", "LSN-021", "reviewed_gold_promotion"},
    AUDIT_NOTE: {"T392", "What Did Not Change", "No reviewed gold is promoted", "No chunk output is implemented"},
    REGISTER: {"decision_id: CD-067", "T392 strengthens Eph.1.3-14 review packet without promotion", "task_ids: [T392]"},
    LESSON_INDEX: {"lesson_id: LSN-021", "Review-packet strengthening requires premortem red-team before promotion", "related_decision_ids: [CD-067]"},
    PREFLIGHT: {"CD-067", "LSN-021", "eval/chunking_gold/review_packets/eph1_3_14_argument_review.md"},
    READINESS: {"task_id: T393", "prior_strengthening:", "task_id: T392", "selected_option: T385-A", "review_packet_strengthened: true"},
    FRONT_DOOR: {"T392", "Eph.1.3-Eph.1.14", "Goal 5", "validate_t392_eph1_review_packet_strengthening.py"},
    MAIN_TOC: {"t392", "review-packet-strengthening", "eph1_3_14_argument_review.md"},
    ROADMAP_TOC: {"T392 | Eph.1.3-Eph.1.14 review packet strengthening", "T392_EPH1_REVIEW_PACKET_STRENGTHENING.md"},
    ROADMAP_STATE: {"id: T392", "status: complete_review_packet_strengthening_only", "next_task: T393"},
    CURRENT_FOCUS: {"current_task: T393", "t393_eph1_reviewed_gold_promotion_decision_packet.yaml"},
    PROJECT_STATUS: {"T392 Eph.1.3-Eph.1.14 review packet strengthening", "Goal 5"},
}


class T392PacketError(ValueError):
    """Raised when T392 packet strengthening state is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise T392PacketError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        text = _read_text(path)
        if text.startswith("---\n"):
            parts = text.split("---\n", 2)
            if len(parts) == 3:
                text = parts[1] + "\n" + parts[2]
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise T392PacketError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise T392PacketError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(_read_text(path))
    except json.JSONDecodeError as exc:
        raise T392PacketError(f"{_rel(path)}: JSON unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise T392PacketError(f"{_rel(path)}: expected a JSON object")
    return data


def _require_phrases(text: str, phrases: set[str], path: Path) -> None:
    missing = sorted(phrase for phrase in phrases if phrase not in text)
    if missing:
        raise T392PacketError(f"{_rel(path)} missing required phrase(s): {missing}")


def _reject_phrases(text: str, phrases: set[str], path: Path) -> None:
    present = sorted(phrase for phrase in phrases if phrase in text)
    if present:
        raise T392PacketError(f"{_rel(path)} contains forbidden phrase(s): {present}")


def _entry_by_id(entries: list[dict[str, Any]], entry_id: str) -> dict[str, Any]:
    for entry in entries:
        if entry.get("entry_id") == entry_id:
            return entry
    raise T392PacketError(f"missing index entry {entry_id}")


def _entry_by_case(entries: list[dict[str, Any]], case_id: str) -> dict[str, Any]:
    for entry in entries:
        if entry.get("case_id") == case_id:
            return entry
    raise T392PacketError(f"missing observed case {case_id}")


def _require_false(mapping: dict[str, Any], key: str, label: str) -> None:
    if mapping.get(key) is not False:
        raise T392PacketError(f"{label}.{key} must be false")


def _validate_index_surfaces() -> None:
    index = _read_json(INDEX)
    observed = _read_json(OBSERVED)
    index_entries = index.get("entries")
    observed_entries = observed.get("entries")
    if not isinstance(index_entries, list) or not all(isinstance(item, dict) for item in index_entries):
        raise T392PacketError("review_packet_index.entries must be a list of objects")
    if not isinstance(observed_entries, list) or not all(isinstance(item, dict) for item in observed_entries):
        raise T392PacketError("observed_stress_behavior.entries must be a list of objects")

    packet_entry = _entry_by_id(index_entries, "packet_eph1_3_14_argument_review")
    if packet_entry.get("status") != "pending_human_review":
        raise T392PacketError("packet_eph1_3_14_argument_review.status must remain pending_human_review")
    if packet_entry.get("decision") != "pending":
        raise T392PacketError("packet_eph1_3_14_argument_review.decision must remain pending")
    _require_false(packet_entry, "implementation_allowed", "packet_eph1_3_14_argument_review")
    _require_false(packet_entry, "output_change_authorized", "packet_eph1_3_14_argument_review")

    observed_entry = _entry_by_case(observed_entries, "eph1_3_14_greek_sentence")
    if observed_entry.get("observed_status") != "review_packet_pending":
        raise T392PacketError("eph1_3_14_greek_sentence.observed_status must remain review_packet_pending")
    if observed_entry.get("review_status") != "pending_human_review":
        raise T392PacketError("eph1_3_14_greek_sentence.review_status must remain pending_human_review")
    _require_false(observed_entry, "implementation_allowed", "eph1_3_14_greek_sentence")


def _validate_task_authority() -> None:
    task = _read_yaml(TASK)
    auth = task.get("authorization")
    if not isinstance(auth, dict):
        raise T392PacketError("T392 task authorization must be a mapping")
    if auth.get("authorizes_review_packet_strengthening") is not True:
        raise T392PacketError("T392 must authorize only review-packet strengthening")
    for key in (
        "authorizes_chunk_output_change",
        "authorizes_reviewed_gold",
        "authorizes_child_spans",
        "authorizes_route_behavior",
        "authorizes_evaluator_change",
        "authorizes_graph_edges",
        "authorizes_retrieval_truth",
        "authorizes_embedding_or_vector_work",
        "authorizes_boundary_import",
        "authorizes_preferred_reading_or_source_tradition",
        "authorizes_canon_scope_change",
        "authorizes_whole_bible_output",
    ):
        if auth.get(key) is not False:
            raise T392PacketError(f"T392 authorization.{key} must be false")


def validate_t392(packet_path: Path = PACKET) -> None:
    packet_text = _read_text(packet_path)
    _require_phrases(packet_text, PACKET_REQUIRED_PHRASES, packet_path)
    _reject_phrases(packet_text, PACKET_FORBIDDEN_PHRASES, packet_path)
    for path, phrases in SURFACE_REQUIREMENTS.items():
        _require_phrases(_read_text(path), phrases, path)
    _validate_index_surfaces()
    _validate_task_authority()


def main() -> int:
    try:
        validate_t392()
    except T392PacketError as exc:
        print(f"T392 Ephesians review-packet strengthening validation failed: {exc}", file=sys.stderr)
        return 1
    print("T392 Ephesians review-packet strengthening validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
