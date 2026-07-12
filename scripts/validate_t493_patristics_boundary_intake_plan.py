#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTROL = ROOT / ".ai/control/t493_patristics_boundary_intake_plan.yaml"
ROADMAP = ROOT / "docs/roadmap/T493_PATRISTICS_BOUNDARY_INTAKE_PLAN.md"
FAMILIES = {"apostolic_fathers", "ante_nicene_writers", "nicene_and_post_nicene_writers", "councils_and_synodal_records", "creeds_and_confessions", "disputed_pseudonymous_or_fragmentary_material"}

def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)

def validate(data: dict) -> None:
    if data.get("task_id") != "T493" or data.get("planning_only") is not True or data.get("non_authorizing") is not True:
        fail("T493 must be planning-only and non-authorizing")
    authority = data.get("authority", {})
    for key in ("imports_or_downloads_authorized", "canonical_records_or_default_retrieval_authorized", "doctrine_or_reception_claims_authorized"):
        if authority.get(key) is not False:
            fail(f"authority.{key} must be false")
    if authority.get("future_patristics_owner") != "logos-boundary-literature":
        fail("patristics must route to logos-boundary-literature")
    if {row.get("family") for row in data.get("source_family_classes", [])} != FAMILIES:
        fail("source family classes incomplete")
    if len(data.get("required_future_metadata", [])) < 12 or len(data.get("intake_gates", [])) < 8:
        fail("metadata or intake gates incomplete")
    handoff = data.get("handoff_packet", {})
    if handoff.get("destination") != "logos-boundary-literature" or handoff.get("creates_boundary_records") is not False:
        fail("handoff must remain future and record-free")
    for question in data.get("unresolved_questions", []):
        if question.get("owner_needed") is not True or question.get("conclusion") != "unresolved":
            fail("unresolved questions must remain owner-gated")

def main() -> int:
    data = yaml.safe_load(CONTROL.read_text(encoding="utf-8"))
    validate(data)
    text = ROADMAP.read_text(encoding="utf-8").lower()
    for phrase in ("planning-only", "classification is not acquisition readiness", "unresolved questions remain questions", "logos-boundary-literature"):
        if phrase not in text:
            fail(f"roadmap missing {phrase}")
    print("T493 patristics boundary intake plan OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
