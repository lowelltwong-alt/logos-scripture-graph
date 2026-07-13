#!/usr/bin/env python3
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTROL = ROOT / ".ai/control/t497_fable_architecture_owner_decisions.yaml"
ROADMAP = ROOT / "docs/roadmap/T497_FABLE_ARCHITECTURE_OWNER_DECISIONS.md"
DECISION_IDS = {"OD-A1", "OD-A2", "OD-A3", "OD-K", "OD-Q", "OD-M"}


def fail(message):
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate(data):
    if data.get("task_id") != "T497" or data.get("source_role") != "advisory_only":
        fail("T497 identity and Fable advisory boundary are required")
    decisions = data.get("decisions", {})
    if set(decisions) != DECISION_IDS or any(item.get("status") != "approved" for item in decisions.values()):
        fail("all six explicit owner decisions must be recorded")
    if decisions["OD-A1"].get("registration_authorized") is not False:
        fail("genealogy registration remains unauthorized")
    if decisions["OD-A2"].get("influence_record_requires_one_of") != ["E1", "E2", "E3"]:
        fail("influence evidence threshold drifted")
    if decisions["OD-A2"].get("resemblance_plus_chronology_maximum") != "correspondence":
        fail("resemblance plus chronology must remain correspondence")
    if decisions["OD-A3"].get("all_families_dossier_only") is not True or decisions["OD-A3"].get("predicate_created_now") is not False:
        fail("research families must remain dossier-only without predicates")
    if decisions["OD-K"].get("dependency_order") != ["LSG-O2A", "LSG-O3A", "LSG-O1A"]:
        fail("kernel dependency order drifted")
    if decisions["OD-Q"].get("authority_consequence_batch_approval_allowed") is not False or decisions["OD-Q"].get("cooling_period_days") != 7:
        fail("authority packet no-batch/cooling policy drifted")
    if decisions["OD-M"].get("branch_protection_changes_owner_applied_only") is not True:
        fail("branch-protection changes must remain owner-applied")
    unresolved = set(data.get("unresolved_and_unapproved", []))
    required = {"future_registration_of_logos_doctrine_genealogy", "canon_change", "graph_edge_or_predicate_creation", "theology_authority"}
    if not required.issubset(unresolved):
        fail("unapproved authority boundaries are incomplete")


def main():
    data = yaml.safe_load(CONTROL.read_text(encoding="utf-8"))
    validate(data)
    text = ROADMAP.read_text(encoding="utf-8").lower()
    for phrase in ("frozen,\n  unregistered", "correspondence, not influence", "section 17 remains unresolved", "no predicate is approved"):
        if phrase not in text:
            fail(f"roadmap missing boundary phrase: {phrase}")
    print("T497 Fable architecture owner decisions OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
