#!/usr/bin/env python3
"""Validate T352 epistle argument review packets."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
PACKET_DIR = ROOT / "eval" / "chunking_gold" / "review_packets"
INDEX = PACKET_DIR / "review_packet_index.json"
OBSERVED = ROOT / "eval" / "chunking_gold" / "stress_atlas" / "observed_stress_behavior.json"

PACKETS = {
    "eph1_3_14_greek_sentence": {
        "packet": "eph1_3_14_argument_review.md",
        "entry_id": "packet_eph1_3_14_argument_review",
        "passage": "Eph.1.3-Eph.1.14",
    },
    "rom9_11_argument": {
        "packet": "rom9_11_argument_review.md",
        "entry_id": "packet_rom9_11_argument_review",
        "passage": "Rom.9-Rom.11",
    },
    "heb7_10_priesthood_argument": {
        "packet": "heb7_10_priesthood_argument_review.md",
        "entry_id": "packet_heb7_10_priesthood_argument_review",
        "passage": "Heb.7-Heb.10",
    },
    "1cor8_10_food_offered_to_idols": {
        "packet": "1cor8_10_food_offered_to_idols_review.md",
        "entry_id": "packet_1cor8_10_food_offered_to_idols_review",
        "passage": "1Cor.8-1Cor.10",
    },
}


class EpistlePacketError(ValueError):
    """Raised when T352 epistle packet state is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EpistlePacketError(f"{_rel(path)}: JSON unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise EpistlePacketError(f"{_rel(path)}: expected object")
    return data


def _entry_by_id(entries: list[dict[str, Any]], entry_id: str) -> dict[str, Any]:
    for entry in entries:
        if entry.get("entry_id") == entry_id:
            return entry
    raise EpistlePacketError(f"review_packet_index missing {entry_id}")


def _observed_by_case(entries: list[dict[str, Any]], case_id: str) -> dict[str, Any]:
    for entry in entries:
        if entry.get("case_id") == case_id:
            return entry
    raise EpistlePacketError(f"observed_stress_behavior missing {case_id}")


def _require_false(mapping: dict[str, Any], key: str, label: str) -> None:
    if mapping.get(key) is not False:
        raise EpistlePacketError(f"{label}.{key} must be false")


def validate_epistle_packets() -> None:
    index = _read_json(INDEX)
    observed = _read_json(OBSERVED)
    index_entries = index.get("entries")
    observed_entries = observed.get("entries")
    if not isinstance(index_entries, list) or not all(isinstance(item, dict) for item in index_entries):
        raise EpistlePacketError("review_packet_index.entries must be a list of objects")
    if not isinstance(observed_entries, list) or not all(isinstance(item, dict) for item in observed_entries):
        raise EpistlePacketError("observed_stress_behavior.entries must be a list of objects")

    for case_id, spec in PACKETS.items():
        packet_path = PACKET_DIR / spec["packet"]
        text = packet_path.read_text(encoding="utf-8")
        for phrase in (
            "Status: `pending_human_review`",
            f"Stress atlas case ID: `{case_id}`",
            "Decision: pending",
            "Implementation allowed: false",
            "Output change authorized: false",
            "Reviewed gold promoted: false",
            "This packet does not authorize output-changing work.",
            "No option above is approved. No reviewed gold is promoted.",
        ):
            if phrase not in text:
                raise EpistlePacketError(f"{_rel(packet_path)} missing {phrase!r}")
        for forbidden in (
            "Status: `reviewed_gold`",
            "implementation_allowed: true",
            "output_change_authorized: true",
            "reviewed_gold_promoted: true",
            "approved for implementation",
        ):
            if forbidden in text:
                raise EpistlePacketError(f"{_rel(packet_path)} contains forbidden {forbidden!r}")

        packet_entry = _entry_by_id(index_entries, spec["entry_id"])
        if packet_entry.get("entry_type") != "review_packet":
            raise EpistlePacketError(f"{spec['entry_id']}.entry_type must be review_packet")
        if packet_entry.get("status") != "pending_human_review":
            raise EpistlePacketError(f"{spec['entry_id']}.status must be pending_human_review")
        if packet_entry.get("decision") != "pending":
            raise EpistlePacketError(f"{spec['entry_id']}.decision must be pending")
        _require_false(packet_entry, "implementation_allowed", spec["entry_id"])
        _require_false(packet_entry, "output_change_authorized", spec["entry_id"])
        if "pending_packets_non_authorizing" not in packet_entry.get("applicable_rules", []):
            raise EpistlePacketError(f"{spec['entry_id']} missing pending_packets_non_authorizing")

        observed_entry = _observed_by_case(observed_entries, case_id)
        if observed_entry.get("observed_status") != "review_packet_pending":
            raise EpistlePacketError(f"{case_id}.observed_status must be review_packet_pending")
        if observed_entry.get("review_packet_exists") is not True:
            raise EpistlePacketError(f"{case_id}.review_packet_exists must be true")
        if observed_entry.get("review_packet") != spec["packet"]:
            raise EpistlePacketError(f"{case_id}.review_packet must be {spec['packet']}")
        if observed_entry.get("review_status") != "pending_human_review":
            raise EpistlePacketError(f"{case_id}.review_status must be pending_human_review")
        if observed_entry.get("recommended_next_step") != "await_human_review":
            raise EpistlePacketError(f"{case_id}.recommended_next_step must be await_human_review")
        _require_false(observed_entry, "implementation_allowed", case_id)

    summary = observed.get("summary", {})
    if summary.get("needs_review_packet") != 19:
        raise EpistlePacketError("observed summary needs_review_packet must be 19 after T352")
    if summary.get("review_packet_pending") != 12:
        raise EpistlePacketError("observed summary review_packet_pending must be 12 after T352")


def main() -> int:
    try:
        validate_epistle_packets()
    except EpistlePacketError as exc:
        print(f"Epistle argument review packet validation failed: {exc}", file=sys.stderr)
        return 1
    print("Epistle argument review packet validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

