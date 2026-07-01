#!/usr/bin/env python3
"""Validate T414 batch1 parent-only reviewed-gold promotion."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
PROMOTION = ROOT / ".ai/control/t414_batch1_parent_only_reviewed_gold_promotion.yaml"
PACKET = ROOT / ".ai/control/t414_batch1_reviewed_gold_promotion_decision_packet.yaml"
MANIFEST = ROOT / "eval/chunking_gold/per_form/epistle_opening_gold_manifest.json"
REGISTER = ROOT / ".ai/control/chunking_theological_decision_register.yaml"
LESSON_INDEX = ROOT / ".ai/control/chunking_lesson_index.yaml"
PREFLIGHT = ROOT / ".ai/control/chunking_agent_preflight.yaml"
READINESS = ROOT / ".ai/control/bible_chunking_readiness_map.yaml"
ROADMAP = ROOT / "ROADMAP_STATE.yaml"
TASK = ROOT / ".ai/tasks/T415.task.yaml"
ROADMAP_DOC = ROOT / "docs/roadmap/T414_BATCH1_PARENT_ONLY_REVIEWED_GOLD_PROMOTION.md"
PROJECT_STATUS = ROOT / ".ai/control/PROJECT_STATUS.md"
CURRENT_FOCUS = ROOT / ".ai/control/current_focus.yaml"

CASE_IDS = {
    "3John.1.1-3John.1.4": "3john_1_1_4_parent_only_reviewed_gold",
    "2Cor.1.1-2Cor.1.2": "2cor_1_1_2_parent_only_reviewed_gold",
    "1Tim.1.1-1Tim.1.2": "1tim_1_1_2_parent_only_reviewed_gold",
    "Jas.1.1-Jas.1.1": "jas_1_1_parent_only_reviewed_gold",
    "2John.1.1-2John.1.3": "2john_1_1_3_parent_only_reviewed_gold",
}


class T414Batch1Error(ValueError):
    """Raised when T414 batch1 promotion state is invalid."""


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
        raise T414Batch1Error(f"{_rel(path)}: expected YAML mapping")
    return data


def _read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise T414Batch1Error(f"{_rel(path)}: expected JSON object")
    return data


def validate_t414_batch1() -> None:
    promo = _read_yaml(PROMOTION)
    if promo.get("task_id") != "T414":
        raise T414Batch1Error("promotion task_id must be T414")
    if promo.get("owner_decision", {}).get("decision_register_update") != "CD-081":
        raise T414Batch1Error("promotion decision_register_update must be CD-081")
    spans = promo.get("promoted_spans")
    if not isinstance(spans, list) or len(spans) != 5:
        raise T414Batch1Error("promotion must list five promoted spans")
    auth = promo.get("authority", {})
    if auth.get("authorizes_parent_only_reviewed_gold_promotion") is not True:
        raise T414Batch1Error("promotion must authorize parent-only reviewed gold")
    if auth.get("authorizes_chunk_output_change") is not False:
        raise T414Batch1Error("promotion must not authorize chunk output")

    manifest = _read_json(MANIFEST)
    reviewed = manifest.get("reviewed_gold")
    if not isinstance(reviewed, list) or len(reviewed) != 5:
        raise T414Batch1Error("manifest must contain five reviewed_gold entries")
    manifest_cases = {entry.get("case_id") for entry in reviewed}
    if manifest_cases != set(CASE_IDS.values()):
        raise T414Batch1Error("manifest case_ids must match batch1 docket")
    for entry in reviewed:
        owner = entry.get("owner_decision", {})
        if owner.get("task_id") != "T414":
            raise T414Batch1Error("manifest owner_decision.task_id must be T414")
        if owner.get("selected_option") != "T414-A":
            raise T414Batch1Error("manifest selected_option must be T414-A")
        if owner.get("output_change_authorized") is not False:
            raise T414Batch1Error("manifest output_change_authorized must be false")

    packet = _read_yaml(PACKET)
    if packet.get("decision_register_entry") != "CD-081":
        raise T414Batch1Error("decision packet decision_register_entry must be CD-081")

    for path, phrases in (
        (REGISTER, ("decision_id: CD-081", "T414 batch1", "task_ids: [T414]")),
        (LESSON_INDEX, ("lesson_id: LSN-036", "CD-081")),
        (PREFLIGHT, ("CD-081", "LSN-036", "t414_batch1_parent_only_reviewed_gold_promotion.yaml")),
        (READINESS, ("task_id: T414", "batch1_parent_only_reviewed_gold_promotion", "CD-081")),
        (ROADMAP, ("id: T414", "CD-081")),
        (PROJECT_STATUS, ("T414 batch1", "CD-081", "LSN-036")),
        (CURRENT_FOCUS, ("t414_batch1_parent_only_reviewed_gold_promotion.yaml", "T415")),
        (TASK, ("id: T415", "authorizes_reviewed_gold: true", "T413 batch1")),
        (ROADMAP_DOC, ("T414 batch1", "parent-only reviewed gold")),
    ):
        text = _read_text(path)
        for phrase in phrases:
            if phrase not in text:
                raise T414Batch1Error(f"{_rel(path)} missing {phrase!r}")


def main() -> int:
    try:
        validate_t414_batch1()
    except T414Batch1Error as exc:
        print(f"T414 batch1 reviewed-gold promotion validation failed: {exc}", file=sys.stderr)
        return 1
    print("T414 batch1 reviewed-gold promotion validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
