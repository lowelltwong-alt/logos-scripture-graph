#!/usr/bin/env python3
"""Validate the T415 batch1 exact output pilot."""
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

MANIFEST = ROOT / ".ai/control/t415_batch1_output_pilot_manifest.yaml"
HARNESS = ROOT / ".ai/control/t415_batch1_route_isolation_harness.yaml"
ORCHESTRATOR = ROOT / "pipelines/chunking/orchestrator.py"
REGISTER = ROOT / ".ai/control/chunking_theological_decision_register.yaml"
LESSON_INDEX = ROOT / ".ai/control/chunking_lesson_index.yaml"
PREFLIGHT = ROOT / ".ai/control/chunking_agent_preflight.yaml"
READINESS = ROOT / ".ai/control/bible_chunking_readiness_map.yaml"
ROADMAP = ROOT / "ROADMAP_STATE.yaml"
TASK = ROOT / ".ai/tasks/T415.task.yaml"
ROADMAP_DOC = ROOT / "docs/roadmap/T415_BATCH1_OUTPUT_PILOT.md"
PROJECT_STATUS = ROOT / ".ai/control/PROJECT_STATUS.md"
CURRENT_FOCUS = ROOT / ".ai/control/current_focus.yaml"

PASSAGES = ROOT / "data/canonical/scripture/passages/passages.jsonl"
WITNESSES = ROOT / "data/canonical/translations/eng-web/translation_witnesses.jsonl"
BOUNDARIES = ROOT / "data/canonical/translations/eng-web/boundary_claims.jsonl"
FOOTNOTES = ROOT / "data/canonical/translations/eng-web/footnotes.jsonl"
CROSSREFS = ROOT / "data/canonical/translations/eng-web/editorial_cross_references.jsonl"
REQUIRED_INPUTS = (PASSAGES, WITNESSES, BOUNDARIES, FOOTNOTES, CROSSREFS)
METRIC_KEYS = (
    "chunks", "tok_p50", "tok_p90", "tok_max", "sentence_integrity_pct",
    "literal_psalms_fragmented", "poetry_books_fragmented", "book_crossings", "usfm_leaks",
    "boundary_basis_cov_pct", "metadata_carry_pct", "gold_psalm23_one_chunk", "gold_gen1_no_midsentence",
)


class T415Batch1Error(ValueError):
    """Raised when T415 batch1 output pilot is stale or unsafe."""


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
        raise T415Batch1Error(f"{_rel(path)}: expected YAML mapping")
    return data


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _jsonl_line_sha(record: dict[str, Any]) -> str:
    return hashlib.sha256((json.dumps(record, ensure_ascii=False) + "\n").encode("utf-8")).hexdigest()


def _run_orchestrator(out: Path, *, disable_t415: bool = False) -> None:
    cmd = [
        sys.executable,
        str(ORCHESTRATOR),
        "--passages", str(PASSAGES),
        "--witnesses", str(WITNESSES),
        "--boundary-claims", str(BOUNDARIES),
        "--footnotes", str(FOOTNOTES),
        "--crossrefs", str(CROSSREFS),
        "--out", str(out),
    ]
    if disable_t415:
        cmd.append("--disable-t415-batch1-overlay")
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        raise T415Batch1Error(result.stdout + result.stderr)


def _validate_manifest_static() -> dict[str, Any]:
    data = _read_yaml(MANIFEST)
    if data.get("task_id") != "T415":
        raise T415Batch1Error("manifest task_id must be T415")
    auth = data.get("authority", {})
    if auth.get("authorizes_chunk_output_change") is not True:
        raise T415Batch1Error("manifest must authorize chunk output for pilot")
    if auth.get("authorizes_child_spans") is not False:
        raise T415Batch1Error("manifest must deny child spans")
    overlays = data.get("overlay_records")
    if not isinstance(overlays, list) or len(overlays) != 5:
        raise T415Batch1Error("manifest overlay_records must list five overlays")
    output = data.get("output_change", {})
    if output.get("added_overlay_count") != 5:
        raise T415Batch1Error("output_change.added_overlay_count must be 5")
    return data


def _validate_generated_outputs(manifest: dict[str, Any]) -> None:
    if not all(path.exists() for path in REQUIRED_INPUTS):
        return

    from pipelines.chunking.evaluate_chunks import load, score

    output = manifest["output_change"]
    expected_overlays = {item["id"]: item for item in manifest["overlay_records"]}
    with tempfile.TemporaryDirectory(prefix="t415-batch1-pilot-") as tmp:
        tmp_path = Path(tmp)
        baseline = tmp_path / "baseline.jsonl"
        candidate = tmp_path / "candidate.jsonl"
        _run_orchestrator(baseline, disable_t415=True)
        _run_orchestrator(candidate)

        baseline_records = _read_jsonl(baseline)
        candidate_records = _read_jsonl(candidate)
        if len(candidate_records) != len(baseline_records) + 5:
            raise T415Batch1Error("candidate must equal baseline plus five overlays")
        if candidate_records[: len(baseline_records)] != baseline_records:
            raise T415Batch1Error("candidate baseline prefix records must match baseline JSON")

        prefix_bytes = candidate.read_bytes()[: len(baseline.read_bytes())]
        if prefix_bytes != baseline.read_bytes():
            raise T415Batch1Error("candidate prefix bytes must equal baseline output bytes")

        if _sha256_file(baseline) != output["baseline_chunk_sha256"]:
            raise T415Batch1Error("baseline hash is stale")
        if _sha256_file(candidate) != output["candidate_chunk_sha256"]:
            raise T415Batch1Error("candidate hash is stale")
        if hashlib.sha256(prefix_bytes).hexdigest() != output["preserved_baseline_prefix_sha256"]:
            raise T415Batch1Error("preserved baseline prefix hash is stale")

        overlay_records = candidate_records[len(baseline_records) :]
        for overlay in overlay_records:
            expected = expected_overlays.get(overlay["id"])
            if expected is None:
                raise T415Batch1Error(f"unexpected overlay id {overlay['id']}")
            if _jsonl_line_sha(overlay) != expected["overlay_record_line_sha256"]:
                raise T415Batch1Error(f"overlay line hash stale for {overlay['id']}")
            if hashlib.sha256(overlay["text"].encode("utf-8")).hexdigest() != expected["text_sha256"]:
                raise T415Batch1Error(f"overlay text hash stale for {overlay['id']}")
            if len(overlay.get("included_text_span_ids", [])) != expected["included_text_span_count"]:
                raise T415Batch1Error(f"overlay span count stale for {overlay['id']}")

        baseline_score = score(load(baseline))
        candidate_score = score(load(candidate))
        for key in METRIC_KEYS:
            if baseline_score.get(key) != manifest["same_baseline_evaluation"]["baseline_metrics"].get(key):
                raise T415Batch1Error(f"baseline metric {key} is stale")
            if candidate_score.get(key) != manifest["same_baseline_evaluation"]["candidate_metrics"].get(key):
                raise T415Batch1Error(f"candidate metric {key} is stale")


def _validate_surfaces() -> None:
    for path in (HARNESS, REGISTER, LESSON_INDEX, PREFLIGHT, READINESS, ROADMAP, TASK, ROADMAP_DOC, PROJECT_STATUS, CURRENT_FOCUS):
        if not path.exists():
            raise T415Batch1Error(f"missing linked surface {_rel(path)}")
    checks = (
        (REGISTER, ("decision_id: CD-082", "T415 batch1", "task_ids: [T415]")),
        (LESSON_INDEX, ("lesson_id: LSN-037", "CD-082")),
        (PREFLIGHT, ("CD-082", "LSN-037", "t415_batch1_output_pilot_manifest.yaml", "--disable-t415-batch1-overlay")),
        (READINESS, ("task_id: T415", "batch1_output_pilot", "CD-082")),
        (ROADMAP, ("id: T415", "CD-082")),
        (PROJECT_STATUS, ("T415 batch1", "CD-082", "LSN-037")),
        (CURRENT_FOCUS, ("t415_batch1_output_pilot_manifest.yaml", "complete_output_changed_batch1_parent_overlays")),
        (TASK, ("id: T415", "chunk_output_authorized: true")),
        (ROADMAP_DOC, ("T415 batch1", "output pilot")),
        (HARNESS, ("task_id: T415", "CD-082")),
    )
    for path, phrases in checks:
        text = _read_text(path)
        for phrase in phrases:
            if phrase not in text:
                raise T415Batch1Error(f"{_rel(path)} missing {phrase!r}")


def validate_t415_batch1() -> dict[str, Any]:
    manifest = _validate_manifest_static()
    _validate_generated_outputs(manifest)
    _validate_surfaces()
    return manifest


def main() -> int:
    try:
        validate_t415_batch1()
    except T415Batch1Error as exc:
        print(f"T415 batch1 output pilot validation failed: {exc}", file=sys.stderr)
        return 1
    print("T415 batch1 output pilot validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
