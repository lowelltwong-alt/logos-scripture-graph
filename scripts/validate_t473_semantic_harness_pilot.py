#!/usr/bin/env python3
"""Validate the T473 semantic-harness contract and source-marker integrity stop gate."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = {
    "task": ".ai/tasks/T473.task.yaml",
    "control": ".ai/control/t473_semantic_harness_pilot.yaml",
    "scope_manifest": ".ai/context/agent_work/T473/pilot_scope_manifest.yaml",
    "anchor_audit": ".ai/context/agent_work/T473/source_marker_anchor_audit.json",
    "overlap_report": ".ai/context/agent_work/T473/reviewed_gold_output_overlap_report.json",
    "ps119_owner": ".ai/context/agent_work/T473/ps119_correction_owner_packet.yaml",
    "anchor_owner": ".ai/context/agent_work/T473/source_anchor_repair_owner_packet.yaml",
    "schema": "schemas/t473_semantic_harness_pilot.schema.json",
    "proposer": ".ai/prompts/t473_semantic_pilot_proposer.md",
    "critic": ".ai/prompts/t473_semantic_pilot_critic.md",
    "roadmap": "docs/roadmap/T473_SEMANTIC_HARNESS_AND_SOURCE_MARKER_INTEGRITY.md",
    "handoff": ".ai/handoffs/T473/handoff.md",
    "status": ".ai/control/PROJECT_STATUS.md",
    "focus": ".ai/control/current_focus.yaml",
    "register": ".ai/control/chunking_theological_decision_register.yaml",
    "lessons": ".ai/control/chunking_lesson_index.yaml",
    "raw": "data/raw/bible/eng-web/usfm/eng-web_usfm.zip",
    "gold": "eval/chunking_gold/per_form/psalms_gold_manifest.json",
    "skill": "pipelines/chunking/skills/candidate/psalm-whole-then-stanza-v1/algorithm.py",
}

TASK_FALSE_FIELDS = {
    "executes_model_pilot",
    "fixes_importer_or_chunker",
    "modifies_reviewed_gold",
    "authorizes_target_selection",
    "authorizes_reviewed_gold",
    "authorizes_chunk_output",
    "authorizes_child_spans",
    "changes_route_behavior",
    "changes_evaluator_behavior",
    "creates_graph_or_retrieval_truth",
    "runs_embeddings_or_builds_indexes",
    "imports_boundary_material",
    "selects_preferred_reading_or_source_tradition",
    "changes_canon_scope",
    "authorizes_theology_authority",
    "decides_variant_or_inspiration_status",
}

CONTROL_FALSE_FIELDS = {
    "executes_models",
    "fixes_importer",
    "changes_reviewed_gold",
    "authorizes_target_selection",
    "authorizes_reviewed_gold",
    "authorizes_chunk_output",
    "authorizes_child_spans",
    "changes_route_behavior",
    "changes_evaluator_behavior",
    "creates_graph_or_retrieval_truth",
    "runs_embeddings_or_builds_indexes",
    "imports_boundary_material",
    "selects_preferred_reading_or_source_tradition",
    "changes_canon_scope",
    "authorizes_theology_authority",
    "decides_variant_or_inspiration_status",
}

EXPECTED_SCOPES = {
    "T473-SCOPE-2KGS": "2Kgs.18.1-2Kgs.19.37",
    "T473-SCOPE-1CHR": "1Chr.23.1-1Chr.27.34",
    "T473-SCOPE-2JOHN": "2John.1.1-2John.1.13",
    "T473-SCOPE-PS119": "Ps.119.1-Ps.119.176",
}

EXPECTED_PS119_STARTS = list(range(1, 170, 8))
EXPECTED_PS119_SPANS = [
    [f"Ps.119.{start}", f"Ps.119.{start + 7}"]
    for start in EXPECTED_PS119_STARTS
]

REQUIRED_ANCHOR_KINDS = {
    "current_content",
    "next_content_start",
    "between_units",
    "chapter_context",
    "book_context",
    "unresolved",
}


def _load_yaml(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        text = parts[1] + "\n" + parts[2]
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected YAML mapping")
    return data


def _load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def _require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def _false_flags(block: dict[str, Any], fields: set[str], label: str, errors: list[str]) -> None:
    for field in sorted(fields):
        if block.get(field) is not False:
            errors.append(f"{label}.{field} must be false")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _ps119_raw_headings(archive: Path) -> list[dict[str, Any]]:
    with zipfile.ZipFile(archive) as zf:
        name = next((n for n in zf.namelist() if n.endswith("20-PSAeng-web.usfm")), None)
        if name is None:
            raise ValueError("raw WEB archive missing 20-PSAeng-web.usfm")
        lines = zf.read(name).decode("utf-8-sig").splitlines()

    in_ps119 = False
    pending: dict[str, Any] | None = None
    headings: list[dict[str, Any]] = []
    for source_line, raw in enumerate(lines, start=1):
        line = raw.strip()
        if line == r"\c 119":
            in_ps119 = True
            continue
        if in_ps119 and line == r"\c 120":
            break
        if not in_ps119:
            continue
        if line.startswith(r"\d "):
            pending = {
                "source_line": source_line,
                "label": re.sub(r"\\w\*?|\|strong=\"[^\"]+\"", "", line[3:]).strip(),
            }
            continue
        match = re.match(r"^\\v\s+(\d+)", line)
        if pending is not None and match:
            pending["next_verse"] = int(match.group(1))
            headings.append(pending)
            pending = None
    return headings


def _gold_ps119_spans(gold: dict[str, Any]) -> list[list[str]]:
    for case in gold.get("reviewed_gold", []):
        if case.get("case_id") == "ps119_acrostic_sections":
            return case.get("expected", {}).get("spans", [])
    return []


def _skill_ps119_spans(path: Path) -> list[list[str]]:
    module = ast.parse(path.read_text(encoding="utf-8"))
    for node in module.body:
        target = None
        value = None
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            target, value = node.target.id, node.value
        elif isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            target, value = node.targets[0].id, node.value
        if target == "REVIEWED_PSALM_CHAPTER_SPANS" and isinstance(value, ast.Dict):
            for key_node, value_node in zip(value.keys, value.values, strict=True):
                if isinstance(key_node, ast.Constant) and key_node.value == "ps119_acrostic_sections":
                    return [list(span) for span in ast.literal_eval(value_node)]
    return []


def _find_item(items: Any, key: str, value: str) -> dict[str, Any] | None:
    if not isinstance(items, list):
        return None
    for item in items:
        if isinstance(item, dict) and item.get(key) == value:
            return item
    return None


def validate_t473_artifact(schema: dict[str, Any], artifact: dict[str, Any]) -> list[str]:
    errors = [
        error.message
        for error in Draft202012Validator(schema).iter_errors(artifact)
    ]
    if artifact.get("artifact_type") == "candidate_span":
        if artifact.get("span") != artifact.get("observed_source_span"):
            errors.append("candidate span must equal observed source span")
        if artifact.get("derived_from_region_or_vote") is not False:
            errors.append("candidate span cannot derive from region or vote")
    return errors


def _validate_schema(schema: dict[str, Any], errors: list[str]) -> None:
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:
        errors.append(f"T473 JSON Schema invalid: {exc}")
        return

    region = {
        "artifact_type": "disagreement_region",
        "schema_version": "t473_semantic_harness_pilot.v1",
        "region_id": "REGION-1",
        "scope_id": "T473-SCOPE-2JOHN",
        "region_span": "2John.1.1-2John.1.13",
        "model_decision_ids": ["MODEL-A", "MODEL-B"],
        "diagnostic_only": True,
        "candidate_span_eligible": False,
        "non_authorizing": True,
        "candidate_eligible": False,
        "promotion_authority": "none",
    }
    if validate_t473_artifact(schema, region):
        errors.append("T473 schema rejects valid disagreement_region fixture")

    inflated = {
        "artifact_type": "candidate_span",
        "schema_version": "t473_semantic_harness_pilot.v1",
        "candidate_id": "CANDIDATE-1",
        "scope_id": "T473-SCOPE-2JOHN",
        "span": "2John.1.1-2John.1.13",
        "origin_kind": "exact_observed_model_span",
        "source_model_id": "M4",
        "source_decision_id": "MODEL-A",
        "observed_source_span": "2John.1.12-2John.1.13",
        "literary_evidence_ids": ["EVIDENCE-1"],
        "overlap_admission_id": "OVERLAP-1",
        "derived_from_region_or_vote": False,
        "non_authorizing": True,
        "candidate_eligible": False,
        "promotion_authority": "none",
    }
    if not validate_t473_artifact(schema, inflated):
        errors.append("T473 schema must reject candidate span that differs from observed source span")


def validate_t473_package(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    paths = {key: root / rel for key, rel in REQUIRED_FILES.items()}
    for key, path in paths.items():
        if not path.is_file():
            errors.append(f"missing required T473 file {REQUIRED_FILES[key]}")
    if errors:
        return errors

    task = _load_yaml(paths["task"])
    control = _load_yaml(paths["control"])
    scope_manifest = _load_yaml(paths["scope_manifest"])
    audit = _load_json(paths["anchor_audit"])
    overlap = _load_json(paths["overlap_report"])
    ps119_owner = _load_yaml(paths["ps119_owner"])
    anchor_owner = _load_yaml(paths["anchor_owner"])
    schema = _load_json(paths["schema"])
    focus = _load_yaml(paths["focus"])
    register = _load_yaml(paths["register"])
    lessons = _load_yaml(paths["lessons"])

    _require(task.get("id") == "T473", "task id must be T473", errors)
    _require(
        control.get("object_type") == "t473_semantic_harness_pilot",
        "control object_type mismatch",
        errors,
    )
    _false_flags(task.get("authorization", {}), TASK_FALSE_FIELDS, "task.authorization", errors)
    _false_flags(control.get("authorization", {}), CONTROL_FALSE_FIELDS, "control.authorization", errors)

    execution = control.get("execution_state", {})
    _require(execution.get("pilot_execution_allowed") is False, "pilot execution must remain false", errors)
    _require(execution.get("t474_allowed") is False, "T474 must remain owner-blocked", errors)
    _require(scope_manifest.get("execution_allowed") is False, "scope manifest must block execution", errors)
    _require(scope_manifest.get("run_lock_status") == "not_created_execution_forbidden", "run lock must be absent", errors)

    scopes = control.get("pilot_scopes", [])
    observed_scopes = {item.get("scope_id"): item.get("calibration_span") for item in scopes if isinstance(item, dict)}
    _require(observed_scopes == EXPECTED_SCOPES, "pilot scopes must match the fixed four-scope inventory", errors)
    two_john = _find_item(scopes, "scope_id", "T473-SCOPE-2JOHN")
    ps119 = _find_item(scopes, "scope_id", "T473-SCOPE-PS119")
    _require(two_john is not None and two_john.get("current_status") == "research_only_overlap_blocked", "2 John must remain overlap-blocked", errors)
    _require(ps119 is not None and str(ps119.get("current_status", "")).startswith("stop_line"), "Psalm 119 must remain stop-line blocked", errors)

    provenance = control.get("typed_provenance_rules", {})
    _require(provenance.get("disagreement_region_candidate_eligible") is False, "region must be candidate-ineligible", errors)
    prohibited = set(provenance.get("prohibited_candidate_derivations", []))
    _require({"disagreement_region", "union", "envelope", "majority_vote", "preferred_pair"} <= prohibited, "provenance rules missing prohibited derivations", errors)

    sealing = control.get("independence_and_sealing", {})
    _require(sealing.get("critic_may_read_proposer_before_seal") is False, "critic must be independently sealed", errors)
    _require(sealing.get("reconciliation_may_begin_before_both_seals") is False, "reconciliation must wait for both seals", errors)
    _require(control.get("chapter_anchor_gate", {}).get("maximum_unjustified_anchor_count") == 0, "unjustified chapter anchors must be zero", errors)

    anchor_gate = control.get("source_marker_anchor_integrity", {})
    _require(anchor_gate.get("root_cause_not") == "inclusive_or_half_open_endpoint_arithmetic", "root cause must reject endpoint arithmetic diagnosis", errors)
    _require(anchor_gate.get("status") == "blocked_pending_owner_correction", "source anchor gate must remain blocked", errors)
    _require(anchor_gate.get("measured_characterization", {}).get("currently_backward_bound") == 13977, "backward-bound characterization mismatch", errors)

    headings = _ps119_raw_headings(paths["raw"])
    _require(len(headings) == 22, f"raw Psalm 119 must have 22 d headings, found {len(headings)}", errors)
    _require([row.get("next_verse") for row in headings] == EXPECTED_PS119_STARTS, "raw Psalm 119 heading starts must be 1, 9, ..., 169", errors)

    gold_spans = _gold_ps119_spans(_load_json(paths["gold"]))
    skill_spans = _skill_ps119_spans(paths["skill"])
    live_shifted_defect = gold_spans != EXPECTED_PS119_SPANS or skill_spans != EXPECTED_PS119_SPANS
    if live_shifted_defect:
        _require(anchor_gate.get("status") == "blocked_pending_owner_correction", "live shifted spans require blocked gate", errors)
        _require(ps119_owner.get("owner_selection") == "pending", "live shifted spans require pending owner packet", errors)

    _require(audit.get("severity") == "P0_canonical_text_and_token_integrity", "audit must record P0 integrity severity", errors)
    _require(audit.get("raw_heading_next_verses") == EXPECTED_PS119_STARTS, "audit raw heading starts mismatch", errors)
    _require(audit.get("boundary_claim_characterization", {}).get("classified_next_bound") == 15303, "audit next-bound count mismatch", errors)
    _require(set(audit.get("required_anchor_kinds", [])) == REQUIRED_ANCHOR_KINDS, "audit anchor kinds mismatch", errors)
    _require(audit.get("pilot_blocked") is True, "audit must block pilot", errors)

    expected_hashes = audit.get("source_hashes", {})
    for rel in ("data/raw/bible/eng-web/usfm/eng-web_usfm.zip", "eval/chunking_gold/per_form/psalms_gold_manifest.json", "pipelines/chunking/skills/candidate/psalm-whole-then-stanza-v1/algorithm.py"):
        if anchor_gate.get("status") == "blocked_pending_owner_correction":
            _require(expected_hashes.get(rel) == _sha256(root / rel), f"audit source hash drift for {rel}", errors)

    rows = {row.get("scope_id"): row for row in overlap.get("rows", []) if isinstance(row, dict)}
    _require(set(rows) == set(EXPECTED_SCOPES), "overlap report must cover all four scopes", errors)
    _require(rows.get("T473-SCOPE-2JOHN", {}).get("status") == "research_only_overlap_blocked", "2 John overlap report must block", errors)
    _require(rows.get("T473-SCOPE-PS119", {}).get("status") == "gold_endpoint_integrity_quarantined", "Psalm 119 overlap report must quarantine gold endpoints", errors)
    _require(overlap.get("promotion_authorized") is False, "overlap report cannot authorize promotion", errors)

    _require(ps119_owner.get("owner_selection") == "pending", "Psalm 119 owner choice must be pending", errors)
    _require(ps119_owner.get("recommended_owner_choice") == "T473-PS119-A", "Psalm 119 faithful correction must be recommended", errors)
    _require(anchor_owner.get("owner_selection") == "pending", "source repair owner choice must be pending", errors)
    _require(anchor_owner.get("recommended_owner_choice") == "T473-ANCHOR-A", "staged source repair must be recommended", errors)
    owner_effect = anchor_owner.get("owner_gate_effect", {})
    for field in ("authorizes_canonical_regeneration_now", "authorizes_reviewed_gold_change_now", "authorizes_chunk_output_now"):
        _require(owner_effect.get(field) is False, f"source owner packet {field} must be false", errors)

    route = control.get("route_after_t473", {})
    _require(set(route) == {"T474", "T475", "T476", "T477", "T478", "T479", "T480", "T481_plus"}, "T473 route must cover repair ladder and T481+ pilot", errors)
    _require("semantic pilot" in route.get("T481_plus", ""), "semantic pilot must move to T481+", errors)

    _validate_schema(schema, errors)

    joined = "\n".join(
        paths[key].read_text(encoding="utf-8")
        for key in ("proposer", "critic", "roadmap", "handoff", "status")
    )
    for needle in (
        "non-authorizing",
        "T481+",
        "previous-versus-next",
        "reviewed gold",
        "chunk output",
    ):
        _require(needle in joined, f"T473 surfaces missing required text {needle!r}", errors)

    _require(
        focus.get("current_task") == "T473" or focus.get("t473_task") == ".ai/tasks/T473.task.yaml",
        "current focus must retain T473 task surface",
        errors,
    )
    decision = _find_item(register.get("decisions"), "decision_id", "CD-111")
    _require(decision is not None and "T473" in decision.get("task_ids", []), "decision register missing CD-111/T473", errors)
    lesson = _find_item(lessons.get("lessons"), "lesson_id", "LSN-056")
    _require(lesson is not None and "T473" in lesson.get("related_task_ids", []), "lesson index missing LSN-056/T473", errors)

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    errors = validate_t473_package(args.root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("T473 semantic harness and source-marker integrity validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
