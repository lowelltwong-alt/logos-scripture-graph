#!/usr/bin/env python3
"""Validate the T374 additive parent overlay implementation."""
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
MANIFEST = ROOT / ".ai" / "control" / "t374_additive_parent_overlay_manifest.yaml"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
ROADMAP = ROOT / "ROADMAP_STATE.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
TASK = ROOT / ".ai" / "tasks" / "T374.task.yaml"
AUDIT_REPORT = ROOT / ".ai" / "audits" / "reports" / "20260620-T374-additive-parent-overlay.md"
ORCHESTRATOR = ROOT / "pipelines" / "chunking" / "orchestrator.py"
EVALUATOR = ROOT / "pipelines" / "chunking" / "evaluate_chunks.py"

PASSAGES = ROOT / "data" / "canonical" / "scripture" / "passages" / "passages.jsonl"
WITNESSES = ROOT / "data" / "canonical" / "translations" / "eng-web" / "translation_witnesses.jsonl"
BOUNDARIES = ROOT / "data" / "canonical" / "translations" / "eng-web" / "boundary_claims.jsonl"
FOOTNOTES = ROOT / "data" / "canonical" / "translations" / "eng-web" / "footnotes.jsonl"
CROSSREFS = ROOT / "data" / "canonical" / "translations" / "eng-web" / "editorial_cross_references.jsonl"

MANIFEST_REL = ".ai/control/t374_additive_parent_overlay_manifest.yaml"
AUDIT_REL = ".ai/audits/reports/20260620-T374-additive-parent-overlay.md"
VALIDATOR_REL = "scripts/validate_t374_additive_parent_overlay.py"
OVERLAY_ID = (
    "chunk--eng-web--chunk-policy-v0.1.0--epistles-parent-overlay--"
    "1Cor.8.1--1Cor.10.33--T374-OVERLAP-B"
)
OVERLAY_START = "1Cor.8.1"
OVERLAY_END = "1Cor.10.33"
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


class T374OverlayError(ValueError):
    """Raised when the T374 implementation is stale or unsafe."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise T374OverlayError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise T374OverlayError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise T374OverlayError(f"{_rel(path)}: expected a YAML mapping")
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
        raise T374OverlayError(f"{label} must be a list")
    missing = sorted(required - {str(item) for item in actual})
    if missing:
        raise T374OverlayError(f"{label} missing {missing}")


def _validate_manifest_static(path: Path = MANIFEST) -> dict[str, Any]:
    data = _read_yaml(path)
    expected = {
        "object_type": "t374_additive_parent_overlay_manifest",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "t374_additive_parent_overlay_manifest.v1",
        "manifest_id": "t374_1cor8_10_additive_parent_overlay_manifest",
        "task_id": "T374",
        "status": "complete_output_changed_additive_parent_overlay",
        "selected_option": "T374-OVERLAP-B",
        "selected_parent": "1Cor.8.1-1Cor.10.33",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise T374OverlayError(f"{_rel(path)}: {key} must be {value!r}")
    if data.get("selected_children") != []:
        raise T374OverlayError(f"{_rel(path)}: selected_children must be []")

    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise T374OverlayError(f"{_rel(path)}: authority must be a mapping")
    if authority.get("records_output_change") is not True:
        raise T374OverlayError(f"{_rel(path)}: authority.records_output_change must be true")
    if authority.get("authorizes_exact_additive_parent_overlay") is not True:
        raise T374OverlayError(f"{_rel(path)}: exact additive overlay must be authorized")
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
        "authorizes_whole_bible_output_pass",
    ):
        if authority.get(forbidden) is not False:
            raise T374OverlayError(f"{_rel(path)}: authority.{forbidden} must be false")

    output = data.get("output_change")
    if not isinstance(output, dict):
        raise T374OverlayError(f"{_rel(path)}: output_change must be a mapping")
    expected_output = {
        "baseline_chunk_count": 1136,
        "candidate_chunk_count": 1137,
        "added_overlay_count": 1,
        "baseline_chunk_sha256": "eda6232b2cb7f0ab4c8dacac10ed672c247a1e41ccb1f807ace05d0ca9eec619",
        "candidate_chunk_sha256": "681a0840edd8513daeb204579ed0a1b0b0f818c910abfc83a7890317c3b481e7",
        "preserved_baseline_prefix_sha256": "eda6232b2cb7f0ab4c8dacac10ed672c247a1e41ccb1f807ace05d0ca9eec619",
        "baseline_prefix_matches_pre_t374_bytes": True,
        "non_target_output_diff_detected": False,
    }
    for key, value in expected_output.items():
        if output.get(key) != value:
            raise T374OverlayError(f"{_rel(path)}: output_change.{key} must be {value!r}")
    if output.get("changed_output_ids") != [OVERLAY_ID]:
        raise T374OverlayError(f"{_rel(path)}: output_change.changed_output_ids must contain only the overlay")
    if output.get("changed_spans") != ["1Cor.8.1-1Cor.10.33"]:
        raise T374OverlayError(f"{_rel(path)}: output_change.changed_spans must be exact")

    overlay = data.get("overlay_record")
    if not isinstance(overlay, dict):
        raise T374OverlayError(f"{_rel(path)}: overlay_record must be a mapping")
    expected_overlay = {
        "id": OVERLAY_ID,
        "chunk_kind": "epistles_parent_overlay",
        "overlay_kind": "additive_parent_only",
        "osis_start": OVERLAY_START,
        "osis_end": OVERLAY_END,
        "included_text_span_count": 73,
        "text_sha256": "819c54cd3cac60746f35b1cde8c13d20d7d7b5bc2b876eb9ccd8ac528a149eaa",
        "overlay_record_line_sha256": "cf115a3b457192b7e79a9500d5ed8371f32afc7bf6e0281e3f246f7d1d6d7d90",
        "footnote_ref_count": 2,
        "editorial_crossref_ref_count": 3,
        "reviewed_gold_case_id": "1cor8_10_parent_only_reviewed_gold",
        "owner_decision_ref": ".ai/control/t374_baseline_overlap_owner_decision_packet.yaml",
        "implementation_manifest": MANIFEST_REL,
        "decision_register_entry": "CD-056",
        "baseline_chunks_preserved_byte_identical": True,
        "non_truth_bearing_overlay": True,
        "graph_retrieval_truth_authorized": False,
        "child_span_authorized": False,
        "broader_epistle_generalization_authorized": False,
    }
    for key, value in expected_overlay.items():
        if overlay.get(key) != value:
            raise T374OverlayError(f"{_rel(path)}: overlay_record.{key} must be {value!r}")
    if overlay.get("selected_children") != []:
        raise T374OverlayError(f"{_rel(path)}: overlay_record.selected_children must be []")
    _require_subset(
        {"additive_parent_overlay", "owner_selected_t374_overlap_b", "reviewed_gold_parent_only", "route_isolated_exact_pilot"},
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
            "treating_overlay_as_truth_bearing_hierarchy",
        },
        data.get("non_authorizations"),
        "non_authorizations",
    )
    return data


def _run_orchestrator(out: Path, *, disable_overlay: bool = False, ledger: Path | None = None) -> None:
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
    if disable_overlay:
        cmd.append("--disable-t374-overlay")
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        raise T374OverlayError(result.stdout + result.stderr)


def _score(path: Path) -> dict[str, Any]:
    from pipelines.chunking.evaluate_chunks import load, score

    return score(load(path))


def _canonical_inputs_present() -> bool:
    return all(path.exists() for path in REQUIRED_INPUTS)


def _validate_generated_outputs(manifest: dict[str, Any]) -> None:
    if not _canonical_inputs_present():
        return

    output = manifest["output_change"]
    expected_overlay = manifest["overlay_record"]
    expected_metrics = manifest["same_baseline_evaluation"]
    with tempfile.TemporaryDirectory(prefix="t374-overlay-") as tmp:
        tmp_path = Path(tmp)
        baseline = tmp_path / "baseline.jsonl"
        candidate = tmp_path / "candidate.jsonl"
        ledger = tmp_path / "candidate-ledger.jsonl"
        _run_orchestrator(baseline, disable_overlay=True)
        _run_orchestrator(candidate, ledger=ledger)

        baseline_records = _read_jsonl(baseline)
        candidate_records = _read_jsonl(candidate)
        if len(candidate_records) != len(baseline_records) + 1:
            raise T374OverlayError("candidate must equal baseline records plus one overlay")
        if candidate_records[:-1] != baseline_records:
            raise T374OverlayError("candidate baseline records must be byte-identical JSON records")

        candidate_lines = candidate.read_bytes().splitlines(keepends=True)
        prefix_bytes = b"".join(candidate_lines[:len(baseline_records)])
        if prefix_bytes != baseline.read_bytes():
            raise T374OverlayError("candidate prefix bytes must equal baseline output bytes")

        overlay = candidate_records[-1]
        if overlay.get("id") != OVERLAY_ID:
            raise T374OverlayError("last candidate record must be the T374 overlay")
        leaked = ROUTE_METADATA_KEYS & set(overlay)
        if leaked:
            raise T374OverlayError(f"overlay leaked route metadata keys: {sorted(leaked)}")

        if _sha256_file(baseline) != output["baseline_chunk_sha256"]:
            raise T374OverlayError("baseline hash is stale")
        if _sha256_file(candidate) != output["candidate_chunk_sha256"]:
            raise T374OverlayError("candidate hash is stale")
        if _sha256_bytes(prefix_bytes) != output["preserved_baseline_prefix_sha256"]:
            raise T374OverlayError("preserved baseline prefix hash is stale")
        if _jsonl_line_sha(overlay) != expected_overlay["overlay_record_line_sha256"]:
            raise T374OverlayError("overlay record line hash is stale")
        if _sha256_bytes(overlay["text"].encode("utf-8")) != expected_overlay["text_sha256"]:
            raise T374OverlayError("overlay text hash is stale")

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
                raise T374OverlayError(f"generated overlay {key} drifted")
        if overlay.get("selected_children") != []:
            raise T374OverlayError("generated overlay selected_children must be []")
        if len(overlay.get("included_text_span_ids", [])) != expected_overlay["included_text_span_count"]:
            raise T374OverlayError("generated overlay span count is stale")
        if len(overlay.get("footnote_refs", [])) != expected_overlay["footnote_ref_count"]:
            raise T374OverlayError("generated overlay footnote count is stale")
        if len(overlay.get("editorial_crossref_refs", [])) != expected_overlay["editorial_crossref_ref_count"]:
            raise T374OverlayError("generated overlay crossref count is stale")

        baseline_score = _score(baseline)
        candidate_score = _score(candidate)
        for key, value in expected_metrics["baseline_metrics"].items():
            if baseline_score.get(key) != value:
                raise T374OverlayError(f"baseline metric {key} is stale")
        for key, value in expected_metrics["candidate_metrics"].items():
            if candidate_score.get(key) != value:
                raise T374OverlayError(f"candidate metric {key} is stale")

        ledger_records = _read_jsonl(ledger)
        first, last = ledger_records[0], ledger_records[-1]
        if first.get("t374_additive_overlay_count") != 1:
            raise T374OverlayError("route ledger must record one T374 overlay")
        if first.get("t374_additive_overlay_ids") != [OVERLAY_ID]:
            raise T374OverlayError("route ledger overlay IDs are stale")
        if first.get("validation_status") != "t374_additive_parent_overlay_parent_only":
            raise T374OverlayError("route ledger validation status is stale")
        if last.get("type") != "ChunkingRouteLedgerOverlay" or last.get("overlay_id") != OVERLAY_ID:
            raise T374OverlayError("route ledger must end with the overlay record")


def _validate_links() -> None:
    linked_requirements = (
        (REGISTER, ("CD-056", "T374 additive parent overlay implemented as output-changing exact parent-only pilot", MANIFEST_REL)),
        (PREFLIGHT, ("CD-056", MANIFEST_REL)),
        (READINESS, ("task_id: T375", MANIFEST_REL, "t375_post_pilot_review_complete_next_lane_selection_required")),
        (ROADMAP, ("id: T374", "status: complete_output_changed_additive_parent_overlay", MANIFEST_REL)),
        (FRONT_DOOR, (MANIFEST_REL, VALIDATOR_REL, "T374 additive parent overlay implementation manifest")),
        (TOC, (MANIFEST_REL, VALIDATOR_REL, "output-manifest")),
        (TASK, ("id: T374", "complete_output_changed_additive_parent_overlay", MANIFEST_REL)),
        (AUDIT_REPORT, ("T374 Additive Parent Overlay", MANIFEST_REL, OVERLAY_ID)),
    )
    for path, phrases in linked_requirements:
        if not path.exists():
            raise T374OverlayError(f"{_rel(path)}: missing linked surface")
        text = _read_text(path)
        for phrase in phrases:
            if phrase not in text:
                raise T374OverlayError(f"{_rel(path)}: missing {phrase!r}")


def validate_t374_additive_parent_overlay(path: Path = MANIFEST) -> dict[str, Any]:
    manifest = _validate_manifest_static(path)
    _validate_generated_outputs(manifest)
    _validate_links()
    return manifest


def main() -> int:
    try:
        validate_t374_additive_parent_overlay()
    except T374OverlayError as exc:
        print(f"T374 additive parent overlay validation failed: {exc}", file=sys.stderr)
        return 1
    print("T374 additive parent overlay validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
