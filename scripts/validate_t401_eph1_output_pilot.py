#!/usr/bin/env python3
"""Validate the T401 Eph.1.3-Eph.1.14 exact output pilot."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

MANIFEST = ROOT / ".ai" / "control" / "t401_eph1_output_pilot_manifest.yaml"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
LESSON_INDEX = ROOT / ".ai" / "control" / "chunking_lesson_index.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
ROADMAP = ROOT / "ROADMAP_STATE.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"
TASK = ROOT / ".ai" / "tasks" / "T401.task.yaml"
ROADMAP_DOC = ROOT / "docs" / "roadmap" / "T401_EPH1_OUTPUT_PILOT.md"
AUDIT_REPORT = ROOT / ".ai" / "audits" / "reports" / "20260625-T401-eph1-output-pilot.md"
HANDOFF = ROOT / ".ai" / "handoffs" / "T401" / "handoff.md"
ORCHESTRATOR = ROOT / "pipelines" / "chunking" / "orchestrator.py"
T397_RECORD = ROOT / ".ai" / "control" / "t397_eph1_route_isolation_harness.yaml"
T394_PROMOTION = ROOT / ".ai" / "control" / "t394_eph1_parent_only_reviewed_gold_promotion.yaml"
GOLD_MANIFEST = ROOT / "eval" / "chunking_gold" / "per_form" / "epistle_argument_gold_manifest.json"
REVIEW_PACKET = ROOT / "eval" / "chunking_gold" / "review_packets" / "eph1_3_14_argument_review.md"

PASSAGES = ROOT / "data" / "canonical" / "scripture" / "passages" / "passages.jsonl"
WITNESSES = ROOT / "data" / "canonical" / "translations" / "eng-web" / "translation_witnesses.jsonl"
BOUNDARIES = ROOT / "data" / "canonical" / "translations" / "eng-web" / "boundary_claims.jsonl"
FOOTNOTES = ROOT / "data" / "canonical" / "translations" / "eng-web" / "footnotes.jsonl"
CROSSREFS = ROOT / "data" / "canonical" / "translations" / "eng-web" / "editorial_cross_references.jsonl"

MANIFEST_REL = ".ai/control/t401_eph1_output_pilot_manifest.yaml"
VALIDATOR_REL = "scripts/validate_t401_eph1_output_pilot.py"
AUDIT_REL = ".ai/audits/reports/20260625-T401-eph1-output-pilot.md"
OVERLAY_ID = (
    "chunk--eng-web--chunk-policy-v0.1.0--epistles-parent-overlay--"
    "Eph.1.3--Eph.1.14--T401-EPH1-PILOT"
)
OVERLAY_START = "Eph.1.3"
OVERLAY_END = "Eph.1.14"
REQUIRED_INPUTS = (PASSAGES, WITNESSES, BOUNDARIES, FOOTNOTES, CROSSREFS)
ROUTE_METADATA_KEYS = {
    "route_mode",
    "skill_id",
    "skill_version",
    "registry_surface_sha",
    "input_hash",
    "output_hash",
    "form_based_routing_enabled",
    "detect_form_consumed",
    "route_reason",
    "candidate_skill_ids",
    "skills_used",
}


class T401OutputPilotError(ValueError):
    """Raised when the T401 output pilot is stale or unsafe."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise T401OutputPilotError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise T401OutputPilotError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise T401OutputPilotError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _jsonl_line_sha(record: dict[str, Any]) -> str:
    return _sha256_bytes((json.dumps(record, ensure_ascii=False) + "\n").encode("utf-8"))


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    if not isinstance(actual, list):
        raise T401OutputPilotError(f"{label} must be a list")
    missing = sorted(required - {str(item) for item in actual})
    if missing:
        raise T401OutputPilotError(f"{label} missing {missing}")


def _validate_manifest_static(path: Path = MANIFEST) -> dict[str, Any]:
    data = _read_yaml(path)
    expected = {
        "object_type": "t401_eph1_output_pilot_manifest",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "t401_eph1_output_pilot_manifest.v1",
        "manifest_id": "t401_eph1_3_14_output_pilot_manifest",
        "task_id": "T401",
        "status": "complete_output_changed_eph1_parent_overlay",
        "selected_option": "T401-A",
        "selected_parent": "Eph.1.3-Eph.1.14",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise T401OutputPilotError(f"{_rel(path)}: {key} must be {value!r}")
    if data.get("selected_children") != []:
        raise T401OutputPilotError(f"{_rel(path)}: selected_children must be []")

    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise T401OutputPilotError(f"{_rel(path)}: authority must be a mapping")
    for required_true in (
        "records_output_change",
        "authorizes_exact_additive_parent_overlay",
        "authorizes_exact_parent_span_as_chunk_boundary_for_pilot",
        "authorizes_chunk_output_change",
        "authorizes_implementation",
        "authorizes_route_behavior_for_exact_target_overlay",
    ):
        if authority.get(required_true) is not True:
            raise T401OutputPilotError(f"{_rel(path)}: authority.{required_true} must be true")
    for forbidden in (
        "authorizes_child_spans",
        "authorizes_deleting_or_replacing_existing_chunks",
        "authorizes_adjacent_spill_splits",
        "authorizes_broader_epistle_generalization",
        "authorizes_evaluator_change",
        "authorizes_graph_edges",
        "authorizes_retrieval_truth",
        "authorizes_embedding_or_vector_work",
        "authorizes_preferred_reading",
        "authorizes_source_tradition_preference",
        "authorizes_boundary_import",
        "authorizes_canon_scope_change",
        "authorizes_theology_authority_change",
        "authorizes_source_or_manuscript_rows",
        "authorizes_sqlite_database_creation",
        "authorizes_whole_bible_output_pass",
    ):
        if authority.get(forbidden) is not False:
            raise T401OutputPilotError(f"{_rel(path)}: authority.{forbidden} must be false")

    output = data.get("output_change")
    if not isinstance(output, dict):
        raise T401OutputPilotError(f"{_rel(path)}: output_change must be a mapping")
    expected_output = {
        "baseline_chunk_count": 1137,
        "candidate_chunk_count": 1138,
        "added_overlay_count": 1,
        "baseline_chunk_sha256": "681a0840edd8513daeb204579ed0a1b0b0f818c910abfc83a7890317c3b481e7",
        "candidate_chunk_sha256": "6b0f0210ac6a31090b5ceb42d104278e8d93fc53be098535f231b04b8fcab6f7",
        "preserved_baseline_prefix_sha256": "681a0840edd8513daeb204579ed0a1b0b0f818c910abfc83a7890317c3b481e7",
        "baseline_prefix_matches_pre_t401_bytes": True,
        "non_target_output_diff_detected": False,
    }
    for key, value in expected_output.items():
        if output.get(key) != value:
            raise T401OutputPilotError(f"{_rel(path)}: output_change.{key} must be {value!r}")
    if output.get("changed_output_ids") != [OVERLAY_ID]:
        raise T401OutputPilotError(f"{_rel(path)}: output_change.changed_output_ids must contain only the overlay")
    if output.get("changed_spans") != ["Eph.1.3-Eph.1.14"]:
        raise T401OutputPilotError(f"{_rel(path)}: output_change.changed_spans must be exact")
    if output.get("changed_existing_output_ids") != []:
        raise T401OutputPilotError(f"{_rel(path)}: changed_existing_output_ids must be []")
    if output.get("removed_output_ids") != []:
        raise T401OutputPilotError(f"{_rel(path)}: removed_output_ids must be []")

    route = data.get("route_isolation")
    if not isinstance(route, dict):
        raise T401OutputPilotError(f"{_rel(path)}: route_isolation must be a mapping")
    expected_route = {
        "harness": "scripts/chunking/route_isolation_harness.py",
        "target_span": "Eph.1.3-Eph.1.14",
        "child_spans_authorized": False,
        "baseline_count": 1137,
        "candidate_count": 1138,
        "changed_keys": [],
        "added_keys": [OVERLAY_ID],
        "removed_keys": [],
        "changed_spans": ["Eph.1.3-Eph.1.14"],
        "non_target_byte_identical": True,
    }
    for key, value in expected_route.items():
        if route.get(key) != value:
            raise T401OutputPilotError(f"{_rel(path)}: route_isolation.{key} must be {value!r}")

    overlay = data.get("overlay_record")
    if not isinstance(overlay, dict):
        raise T401OutputPilotError(f"{_rel(path)}: overlay_record must be a mapping")
    expected_overlay = {
        "id": OVERLAY_ID,
        "chunk_kind": "epistles_parent_overlay",
        "overlay_kind": "additive_parent_only",
        "osis_start": OVERLAY_START,
        "osis_end": OVERLAY_END,
        "included_text_span_count": 12,
        "text_sha256": "d5e81b42b224b55eff8df6a2507f673b9a82b5f65b87e6ae9ff32062b44fe5eb",
        "overlay_record_line_sha256": "8065457d2949f433940a8ad0be6772b5e118e60bf045a0d61b355a81ec2ad32e",
        "footnote_ref_count": 0,
        "editorial_crossref_ref_count": 0,
        "reviewed_gold_case_id": "eph1_3_14_parent_only_reviewed_gold",
        "owner_decision_ref": MANIFEST_REL,
        "implementation_manifest": MANIFEST_REL,
        "decision_register_entry": "CD-076",
        "baseline_chunks_preserved_byte_identical": True,
        "non_truth_bearing_overlay": True,
        "graph_retrieval_truth_authorized": False,
        "child_span_authorized": False,
        "broader_epistle_generalization_authorized": False,
    }
    for key, value in expected_overlay.items():
        if overlay.get(key) != value:
            raise T401OutputPilotError(f"{_rel(path)}: overlay_record.{key} must be {value!r}")
    if overlay.get("selected_children") != []:
        raise T401OutputPilotError(f"{_rel(path)}: overlay_record.selected_children must be []")
    _require_subset(
        {
            "additive_parent_overlay",
            "owner_authorized_t401_eph1_exact_output_pilot",
            "reviewed_gold_parent_only",
            "route_isolated_exact_pilot",
        },
        overlay.get("boundary_basis"),
        "overlay_record.boundary_basis",
    )
    _require_subset(
        {
            "child_span_selection",
            "deleting_or_replacing_existing_chunks",
            "adjacent_spill_splits",
            "graph_edge_generation",
            "retrieval_truth",
            "evaluator_change",
            "broader_epistle_generalization",
            "whole_bible_output_pass",
            "treating_parent_overlay_as_child_span_authority",
        },
        data.get("non_authorizations"),
        "non_authorizations",
    )
    return data


def _run_orchestrator(out: Path, *, disable_t401: bool = False, disable_t415: bool = False, ledger: Path | None = None) -> None:
    cmd = [
        sys.executable,
        str(ORCHESTRATOR),
        "--passages",
        str(PASSAGES),
        "--witnesses",
        str(WITNESSES),
        "--boundary-claims",
        str(BOUNDARIES),
        "--footnotes",
        str(FOOTNOTES),
        "--crossrefs",
        str(CROSSREFS),
        "--out",
        str(out),
    ]
    if ledger:
        cmd.extend(["--route-ledger", str(ledger)])
    if disable_t401:
        cmd.append("--disable-t401-eph1-overlay")
    if disable_t415:
        cmd.append("--disable-t415-batch1-overlay")
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        raise T401OutputPilotError(result.stdout + result.stderr)


def _score(path: Path) -> dict[str, Any]:
    from pipelines.chunking.evaluate_chunks import load, score

    return score(load(path))


def _canonical_inputs_present() -> bool:
    return all(path.exists() for path in REQUIRED_INPUTS)


def _validate_generated_outputs(manifest: dict[str, Any]) -> None:
    if not _canonical_inputs_present():
        return

    from scripts.chunking.route_isolation_harness import compare_chunk_jsonl

    output = manifest["output_change"]
    expected_overlay = manifest["overlay_record"]
    expected_metrics = manifest["same_baseline_evaluation"]
    expected_route = manifest["route_isolation"]
    with tempfile.TemporaryDirectory(prefix="t401-eph1-pilot-") as tmp:
        tmp_path = Path(tmp)
        baseline = tmp_path / "baseline.jsonl"
        candidate = tmp_path / "candidate.jsonl"
        ledger = tmp_path / "candidate-ledger.jsonl"
        _run_orchestrator(baseline, disable_t401=True, disable_t415=True)
        _run_orchestrator(candidate, ledger=ledger, disable_t415=True)

        baseline_records = _read_jsonl(baseline)
        candidate_records = _read_jsonl(candidate)
        if len(candidate_records) != len(baseline_records) + 1:
            raise T401OutputPilotError("candidate must equal baseline records plus one overlay")
        if candidate_records[:-1] != baseline_records:
            raise T401OutputPilotError("candidate baseline records must be byte-identical JSON records")

        candidate_lines = candidate.read_bytes().splitlines(keepends=True)
        prefix_bytes = b"".join(candidate_lines[:len(baseline_records)])
        if prefix_bytes != baseline.read_bytes():
            raise T401OutputPilotError("candidate prefix bytes must equal baseline output bytes")

        overlay = candidate_records[-1]
        if overlay.get("id") != OVERLAY_ID:
            raise T401OutputPilotError("last candidate record must be the T401 overlay")
        leaked = ROUTE_METADATA_KEYS & set(overlay)
        if leaked:
            raise T401OutputPilotError(f"overlay leaked route metadata keys: {sorted(leaked)}")

        if _sha256_file(baseline) != output["baseline_chunk_sha256"]:
            raise T401OutputPilotError("baseline hash is stale")
        if _sha256_file(candidate) != output["candidate_chunk_sha256"]:
            raise T401OutputPilotError("candidate hash is stale")
        if _sha256_bytes(prefix_bytes) != output["preserved_baseline_prefix_sha256"]:
            raise T401OutputPilotError("preserved baseline prefix hash is stale")
        if _jsonl_line_sha(overlay) != expected_overlay["overlay_record_line_sha256"]:
            raise T401OutputPilotError("overlay record line hash is stale")
        if _sha256_bytes(overlay["text"].encode("utf-8")) != expected_overlay["text_sha256"]:
            raise T401OutputPilotError("overlay text hash is stale")

        generated_fields = {
            "chunk_kind": overlay.get("chunk_kind"),
            "overlay_kind": overlay.get("overlay_kind"),
            "osis_start": overlay.get("osis_start"),
            "osis_end": overlay.get("osis_end"),
            "reviewed_gold_case_id": overlay.get("reviewed_gold_case_id"),
            "owner_decision_ref": overlay.get("owner_decision_ref"),
            "implementation_manifest": overlay.get("implementation_manifest"),
            "decision_register_entry": overlay.get("decision_register_entry"),
            "baseline_chunks_preserved_byte_identical": overlay.get("baseline_chunks_preserved_byte_identical"),
            "non_truth_bearing_overlay": overlay.get("non_truth_bearing_overlay"),
            "graph_retrieval_truth_authorized": overlay.get("graph_retrieval_truth_authorized"),
            "child_span_authorized": overlay.get("child_span_authorized"),
        }
        for key, value in generated_fields.items():
            if expected_overlay.get(key) != value:
                raise T401OutputPilotError(f"generated overlay {key} drifted")
        if overlay.get("selected_children") != []:
            raise T401OutputPilotError("generated overlay selected_children must be []")
        if len(overlay.get("included_text_span_ids", [])) != expected_overlay["included_text_span_count"]:
            raise T401OutputPilotError("generated overlay span count is stale")
        if len(overlay.get("footnote_refs", [])) != expected_overlay["footnote_ref_count"]:
            raise T401OutputPilotError("generated overlay footnote count is stale")
        if len(overlay.get("editorial_crossref_refs", [])) != expected_overlay["editorial_crossref_ref_count"]:
            raise T401OutputPilotError("generated overlay crossref count is stale")

        report = compare_chunk_jsonl(baseline, candidate, target_span="Eph.1.3-Eph.1.14")
        report_data = report.as_dict()
        for key in (
            "baseline_count",
            "candidate_count",
            "changed_keys",
            "added_keys",
            "removed_keys",
            "changed_spans",
            "non_target_byte_identical",
            "target_span",
            "child_spans_authorized",
        ):
            if report_data.get(key) != expected_route.get(key):
                raise T401OutputPilotError(f"route isolation {key} is stale")

        baseline_score = _score(baseline)
        candidate_score = _score(candidate)
        for key, value in expected_metrics["baseline_metrics"].items():
            if baseline_score.get(key) != value:
                raise T401OutputPilotError(f"baseline metric {key} is stale")
        for key, value in expected_metrics["candidate_metrics"].items():
            if candidate_score.get(key) != value:
                raise T401OutputPilotError(f"candidate metric {key} is stale")

        ledger_records = _read_jsonl(ledger)
        first, last = ledger_records[0], ledger_records[-1]
        if first.get("t374_additive_overlay_count") != 1:
            raise T401OutputPilotError("route ledger must preserve the prior T374 overlay")
        if first.get("t401_eph1_additive_overlay_count") != 1:
            raise T401OutputPilotError("route ledger must record one T401 overlay")
        if first.get("t401_eph1_additive_overlay_ids") != [OVERLAY_ID]:
            raise T401OutputPilotError("route ledger T401 overlay IDs are stale")
        if first.get("validation_status") != "t401_eph1_additive_parent_overlay_parent_only":
            raise T401OutputPilotError("route ledger validation status is stale")
        if last.get("type") != "ChunkingRouteLedgerOverlay" or last.get("overlay_id") != OVERLAY_ID:
            raise T401OutputPilotError("route ledger must end with the T401 overlay record")


def _validate_links() -> None:
    for path in (
        REGISTER,
        LESSON_INDEX,
        PREFLIGHT,
        READINESS,
        ROADMAP,
        FRONT_DOOR,
        TOC,
        ROADMAP_TOC,
        TASK,
        ROADMAP_DOC,
        AUDIT_REPORT,
        HANDOFF,
        T397_RECORD,
        T394_PROMOTION,
        GOLD_MANIFEST,
        REVIEW_PACKET,
    ):
        if not path.exists():
            raise T401OutputPilotError(f"{_rel(path)}: missing linked surface")

    linked_requirements = (
        (REGISTER, ("CD-076", MANIFEST_REL, "T401 implements Eph.1.3-14 exact parent-only output pilot")),
        (LESSON_INDEX, ("LSN-030", MANIFEST_REL, "eph1-output-pilot")),
        (PREFLIGHT, ("CD-076", "LSN-030", MANIFEST_REL, "--disable-t401-eph1-overlay")),
        (READINESS, ("task_id: T401", MANIFEST_REL, "complete_output_changed_eph1_parent_overlay")),
        (ROADMAP, ("id: T401", "complete_output_changed_eph1_parent_overlay", MANIFEST_REL)),
        (FRONT_DOOR, (MANIFEST_REL, VALIDATOR_REL, "T401 Eph.1.3-Eph.1.14 output pilot")),
        (TOC, (MANIFEST_REL, VALIDATOR_REL, "eph1-output-pilot")),
        (ROADMAP_TOC, ("T401", MANIFEST_REL, "Eph.1.3-Eph.1.14 output pilot")),
        (TASK, ("id: T401", MANIFEST_REL, "chunk_output_authorized: true")),
        (ROADMAP_DOC, ("T401 Eph.1.3-Eph.1.14 Output Pilot", MANIFEST_REL, OVERLAY_ID)),
        (AUDIT_REPORT, ("T401 Eph.1.3-Eph.1.14 Output Pilot", MANIFEST_REL, OVERLAY_ID)),
        (HANDOFF, ("task_id: T401", MANIFEST_REL, "complete_output_changed_eph1_parent_overlay")),
    )
    for path, phrases in linked_requirements:
        text = _read_text(path)
        for phrase in phrases:
            if phrase not in text:
                raise T401OutputPilotError(f"{_rel(path)}: missing {phrase!r}")


def validate_t401_eph1_output_pilot(path: Path = MANIFEST) -> dict[str, Any]:
    manifest = _validate_manifest_static(path)
    _validate_generated_outputs(manifest)
    _validate_links()
    return manifest


def main() -> int:
    try:
        validate_t401_eph1_output_pilot()
    except T401OutputPilotError as exc:
        print(f"T401 Eph.1 output pilot validation failed: {exc}", file=sys.stderr)
        return 1
    print("T401 Eph.1 output pilot validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
