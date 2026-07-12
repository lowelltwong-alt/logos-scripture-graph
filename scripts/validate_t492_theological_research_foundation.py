#!/usr/bin/env python3
"""Validate the planning-only T492 theological research foundation."""
from __future__ import annotations

import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTROL = ROOT / ".ai/control/t492_theological_research_foundation.yaml"
ROADMAP = ROOT / "docs/roadmap/T492_THEOLOGICAL_RESEARCH_FOUNDATION.md"

EXPECTED_LANES = {
    "epistle_argument_theological_issue",
    "gospel_wj_discourse",
    "narrative_legal_covenant",
    "wisdom_dialogue_poetry",
    "prophetic_oracle_vision",
    "apocalyptic_prophetic_intertext",
    "orthodox_original_language_pressure",
}
EXPECTED_NAMES = {"Ezra", "Priscilla", "Luke", "Nathan"}
FORBIDDEN_TRUE = {
    "church_fathers_councils_creeds_reception_history_theologians_in_canonical_records",
    "theology_graph_or_canonical_doctrine_claims",
    "graph_edges_or_predicate_promotion",
    "retrieval_or_vector_index_creation",
    "scripture_text_or_canon_change",
    "preferred_reading_or_source_tradition_selection",
    "doctrinal_system_selection",
}
QUESTION_FIELDS = {
    "question", "context", "evidence_searched", "competing_options",
    "confidence", "owner_needed", "later_fable_candidate",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def load() -> dict:
    if not CONTROL.exists():
        fail("missing T492 control")
    data = yaml.safe_load(CONTROL.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        fail("T492 control must be a mapping")
    return data


def validate(data: dict) -> None:
    if data.get("task_id") != "T492" or data.get("planning_only") is not True or data.get("non_authorizing") is not True:
        fail("T492 must remain planning-only and non-authorizing")
    authority = data.get("authority", {})
    if authority.get("canonical_scripture_research_stays_in_this_repository") is not True:
        fail("canonical Scripture research routing missing")
    for key in FORBIDDEN_TRUE:
        if authority.get(key) is not False:
            fail(f"authority.{key} must be false")
    routes = {row.get("destination") for row in data.get("repository_routing", [])}
    if routes != {"logos-scripture-graph", "logos-boundary-literature", "logos-doctrine-genealogy"}:
        fail("repository routing matrix incomplete")
    lanes = data.get("dossier_lane_map", [])
    if {row.get("lane") for row in lanes} != EXPECTED_LANES:
        fail("dossier lane map incomplete")
    for row in lanes:
        source = ROOT / row.get("source", "")
        if not source.exists() or not row.get("readiness") or not row.get("owner_gate"):
            fail(f"invalid lane row: {row.get('lane')}")
    phases = data.get("phases", [])
    if [row.get("phase") for row in phases] != ["A", "B", "C", "D", "E"]:
        fail("phases A-E required in order")
    if phases[2].get("creates_edges") is not False or set(phases[2].get("required_fields", [])) != {"confidence", "provenance", "review_status"}:
        fail("Phase C must be research-only with evidence fields")
    plan = data.get("named_subagent_plan", {})
    if {row.get("name") for row in plan.get("agents", [])} != EXPECTED_NAMES:
        fail("named subagent plan must use the approved positive biblical names")
    if plan.get("independent_review_required") is not True or plan.get("checker_executes_acceptance_checks") is not True:
        fail("independent executed review required")
    if plan.get("fable_escalation") != "manual_packet_only_for_unresolved_systemic_architecture_questions":
        fail("Fable escalation must remain manual and systemic-only")
    questions = data.get("hard_unsolved_question_register", {}).get("questions", [])
    if not questions:
        fail("hard-unsolved-question register must not be empty")
    for question in questions:
        if not QUESTION_FIELDS.issubset(question) or question.get("owner_needed") is not True:
            fail("each unresolved question needs all fields and an owner")
    if any(row.get("create_now") is not False for row in data.get("future_tasks", [])):
        fail("future tasks must remain uncreated")


def validate_text() -> None:
    if not ROADMAP.exists():
        fail("missing T492 roadmap")
    text = ROADMAP.read_text(encoding="utf-8").lower()
    for phrase in ("research readiness is not target selection", "creates no graph edges", "questions, not conclusions", "logos-doctrine-genealogy"):
        if phrase not in text:
            fail(f"roadmap missing required phrase: {phrase}")


def main() -> int:
    validate(load())
    validate_text()
    print("T492 theological research foundation OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
