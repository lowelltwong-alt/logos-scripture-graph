#!/usr/bin/env python3
"""Validate T411 Cursor readiness and future emitted batch artifacts."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
TASK_ID = "T411"
TASK_FILE = ROOT / ".ai" / "tasks" / "T411.task.yaml"
CONTRACT = ROOT / ".ai" / "control" / "cursor_to_codex_transparency_contract.yaml"
QUEUE = ROOT / ".ai" / "control" / "whole_bible_low_complexity_chunking_candidate_queue.yaml"
AGENT_WORK = ROOT / ".ai" / "context" / "agent_work" / "T411"
HANDOFF_DIR = ROOT / ".ai" / "handoffs" / "T411"

EXPECTED_CANDIDATES = {
    "T402-LC-063": "2John.1.1-2John.1.3",
    "T402-LC-057": "Phlm.1.1-Phlm.1.7",
    "T402-LC-032": "Jonah.1.1-Jonah.1.3",
}

FORBIDDEN_TRUE_FIELDS = {
    "authorizes_chunk_output_change",
    "authorizes_reviewed_gold_promotion",
    "authorizes_child_spans",
    "authorizes_route_behavior_change",
    "authorizes_evaluator_change",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_embedding_or_vector_work",
    "authorizes_boundary_import",
    "authorizes_theology_authority_change",
    "cursor_may_select_target",
    "promotes_reviewed_gold",
    "implements_chunk_output",
    "adds_child_spans",
    "changes_route_behavior",
    "changes_evaluator_behavior",
    "creates_graph_or_retrieval_truth",
    "runs_embeddings_or_builds_indexes",
    "imports_boundary_material",
    "chooses_backend",
    "promotes_retrieval_profile",
    "selects_preferred_reading_or_source_tradition",
    "changes_canon_scope",
    "authorizes_source_or_manuscript_rows",
    "authorizes_theology_authority",
}

FORBIDDEN_ARTIFACT_PATTERNS = [
    re.compile(r"\b(cursor_may_select_target|promotes_reviewed_gold|implements_chunk_output|adds_child_spans)\s*:\s*true\b", re.I),
    re.compile(r"\b(authorizes?_(?:reviewed_gold|chunk_output|child_span|route|evaluator|graph|retrieval|embedding|vector|boundary|theology)[\w-]*)\s*:\s*true\b", re.I),
    re.compile(r"\b(reviewed gold promoted|chunk output created|child span created|embedding run|vector index built)\b", re.I),
]


class T411CursorBatchArtifactError(ValueError):
    """Raised when T411 setup or emitted Cursor artifacts are invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _strip_front_matter(text: str) -> str:
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            return parts[2]
    return text


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
        data = yaml.safe_load(_strip_front_matter(text))
    except (OSError, yaml.YAMLError) as exc:
        raise T411CursorBatchArtifactError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise T411CursorBatchArtifactError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_path(path: Path, *, directory: bool = False) -> None:
    if directory:
        if not path.is_dir():
            raise T411CursorBatchArtifactError(f"{_rel(path)}: required directory is missing")
    elif not path.is_file():
        raise T411CursorBatchArtifactError(f"{_rel(path)}: required file is missing")


def _string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise T411CursorBatchArtifactError(f"{label} must be a list of non-empty strings")
    return value


def _bool(value: Any) -> bool:
    return value is True


def _require_false_authority(mapping: Any, label: str) -> None:
    if not isinstance(mapping, dict):
        raise T411CursorBatchArtifactError(f"{label}: authority mapping is required")
    true_forbidden = sorted(key for key in FORBIDDEN_TRUE_FIELDS if mapping.get(key) is True)
    if true_forbidden:
        raise T411CursorBatchArtifactError(f"{label}: forbidden authority field(s) true: {true_forbidden}")


def _expected_artifact_paths(agent_work: Path = AGENT_WORK, handoff_dir: Path = HANDOFF_DIR) -> dict[str, Path]:
    return {
        "source_size_manifest": agent_work / "source_size_manifest.jsonl",
        "confidence_register": agent_work / "confidence_register.jsonl",
        "audit_log": agent_work / "audit_log.jsonl",
        "claim_traceability_matrix": agent_work / "claim_traceability_matrix.md",
        "escalation_packets": agent_work / "escalation_packets",
        "cursor_notes_to_codex": handoff_dir / "cursor_notes_to_codex.md",
        "handoff": handoff_dir / "handoff.md",
    }


def _artifact_presence(paths: dict[str, Path]) -> dict[str, bool]:
    return {
        name: path.is_dir() if name == "escalation_packets" else path.is_file()
        for name, path in paths.items()
    }


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    _require_path(path)
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise T411CursorBatchArtifactError(f"{_rel(path)}:{line_number}: invalid JSON: {exc}") from exc
        if not isinstance(row, dict):
            raise T411CursorBatchArtifactError(f"{_rel(path)}:{line_number}: expected JSON object")
        rows.append(row)
    if not rows:
        raise T411CursorBatchArtifactError(f"{_rel(path)}: must contain at least one JSONL row")
    return rows


def _require_fields(row: dict[str, Any], fields: list[str], path: Path, index: int) -> None:
    missing = [field for field in fields if field not in row]
    if missing:
        raise T411CursorBatchArtifactError(f"{_rel(path)} row {index}: missing required field(s) {missing}")


def _require_non_negative_int(row: dict[str, Any], field: str, path: Path, index: int) -> None:
    value = row.get(field)
    if not isinstance(value, int) or value < 0:
        raise T411CursorBatchArtifactError(f"{_rel(path)} row {index}: {field} must be a non-negative integer")


def _require_task_and_non_authorizing(row: dict[str, Any], path: Path, index: int) -> None:
    if row.get("task_id") != TASK_ID:
        raise T411CursorBatchArtifactError(f"{_rel(path)} row {index}: task_id must be {TASK_ID}")
    if row.get("non_authorizing") is not True:
        raise T411CursorBatchArtifactError(f"{_rel(path)} row {index}: non_authorizing must be true")


def validate_task_setup(
    *,
    task_file: Path = TASK_FILE,
    queue_path: Path = QUEUE,
    agent_work: Path = AGENT_WORK,
    handoff_dir: Path = HANDOFF_DIR,
) -> dict[str, Any]:
    _require_path(task_file)
    task = _read_yaml(task_file)
    if task.get("id") != TASK_ID:
        raise T411CursorBatchArtifactError(f"{_rel(task_file)}: id must be {TASK_ID}")
    if task.get("branch") != "codex/t411-cursor-readiness-gate":
        raise T411CursorBatchArtifactError(f"{_rel(task_file)}: branch must be codex/t411-cursor-readiness-gate")
    if task.get("cursor_execution_allowed") is not False:
        raise T411CursorBatchArtifactError(f"{_rel(task_file)}: cursor_execution_allowed must be false before Cursor runs")
    if task.get("cursor_run_status") != "not_started":
        raise T411CursorBatchArtifactError(f"{_rel(task_file)}: cursor_run_status must be not_started in setup")
    _require_false_authority(task.get("authorization"), _rel(task_file))

    roots = _string_list(task.get("cursor_allowed_write_roots"), f"{_rel(task_file)}: cursor_allowed_write_roots")
    if roots != [".ai/context/agent_work/T411/", ".ai/handoffs/T411/"]:
        raise T411CursorBatchArtifactError(f"{_rel(task_file)}: cursor_allowed_write_roots must be exact T411 roots")

    gate = task.get("claude_final_audit_gate")
    if not isinstance(gate, dict) or gate.get("status") != "passed_no_p0_p1_forward_p2s_only":
        raise T411CursorBatchArtifactError(f"{_rel(task_file)}: Claude gate must record no P0/P1 and forward P2s only")

    docket = task.get("candidate_docket")
    if not isinstance(docket, dict) or docket.get("cursor_may_choose_candidates") is not False:
        raise T411CursorBatchArtifactError(f"{_rel(task_file)}: candidate_docket must forbid Cursor selection")
    candidates = docket.get("candidates")
    if not isinstance(candidates, list):
        raise T411CursorBatchArtifactError(f"{_rel(task_file)}: candidate_docket.candidates must be a list")
    actual = {item.get("candidate_id"): item.get("parent_span") for item in candidates if isinstance(item, dict)}
    if actual != EXPECTED_CANDIDATES:
        raise T411CursorBatchArtifactError(f"{_rel(task_file)}: candidate docket must exactly match {EXPECTED_CANDIDATES}")

    queue = _read_yaml(queue_path)
    queue_items = queue.get("candidate_queue") or queue.get("candidates")
    if not isinstance(queue_items, list):
        raise T411CursorBatchArtifactError(f"{_rel(queue_path)}: candidates must be a list")
    queue_by_id = {item.get("candidate_id"): item for item in queue_items if isinstance(item, dict)}
    for candidate_id, span in EXPECTED_CANDIDATES.items():
        item = queue_by_id.get(candidate_id)
        if not isinstance(item, dict):
            raise T411CursorBatchArtifactError(f"{_rel(queue_path)}: missing {candidate_id}")
        if item.get("proposed_parent") != span:
            raise T411CursorBatchArtifactError(f"{_rel(queue_path)}: {candidate_id} proposed_parent must be {span}")
        if item.get("status") != "ready_for_review_packet":
            raise T411CursorBatchArtifactError(f"{_rel(queue_path)}: {candidate_id} must be ready_for_review_packet")

    _require_path(handoff_dir / "handoff.md")
    _require_path(agent_work / "candidate_options_docket.md")
    _require_path(agent_work / "per_candidate_prompt_notes.md")
    _require_path(agent_work / "validation_runtime_note.md")
    for name in ("biblical_literature_review.md", "greek_review.md", "hebrew_review.md", "frontier_review.md"):
        _require_path(agent_work / "escalation_packet_templates" / name)

    return {"task_id": TASK_ID, "candidates": sorted(EXPECTED_CANDIDATES)}


def _validate_forbidden_text(paths: dict[str, Path]) -> None:
    for name, path in paths.items():
        if name == "escalation_packets":
            files = list(path.rglob("*")) if path.is_dir() else []
        else:
            files = [path] if path.is_file() else []
        for file_path in files:
            if not file_path.is_file():
                continue
            text = file_path.read_text(encoding="utf-8", errors="replace")
            for pattern in FORBIDDEN_ARTIFACT_PATTERNS:
                if pattern.search(text):
                    raise T411CursorBatchArtifactError(f"{_rel(file_path)}: forbidden authority/output claim detected")


def validate_emitted_artifacts(
    *,
    agent_work: Path = AGENT_WORK,
    handoff_dir: Path = HANDOFF_DIR,
    contract_path: Path = CONTRACT,
    require_artifacts: bool = False,
) -> dict[str, Any]:
    contract = _read_yaml(contract_path)
    paths = _expected_artifact_paths(agent_work, handoff_dir)
    presence = _artifact_presence(paths)
    any_present = any(presence.values())
    all_present = all(presence.values())
    setup_only_names = {"handoff"}
    cursor_artifact_presence = {name: value for name, value in presence.items() if name not in setup_only_names}
    any_cursor_artifact = any(cursor_artifact_presence.values())
    all_cursor_artifacts = all(cursor_artifact_presence.values())

    if not require_artifacts and not any_cursor_artifact:
        return {"mode": "setup", "artifacts_present": False}
    if require_artifacts and not all_present:
        missing = sorted(name for name, present in presence.items() if not present)
        raise T411CursorBatchArtifactError(f"missing required T411 artifact(s): {missing}")
    if any_present and not all_present and not (presence.get("handoff") and not any_cursor_artifact):
        missing = sorted(name for name, present in presence.items() if not present)
        raise T411CursorBatchArtifactError(f"partial T411 artifact set is not valid; missing {missing}")
    if any_cursor_artifact and not all_cursor_artifacts:
        missing = sorted(name for name, present in cursor_artifact_presence.items() if not present)
        raise T411CursorBatchArtifactError(f"partial T411 Cursor artifact set is not valid; missing {missing}")

    _validate_forbidden_text(paths)

    source_fields = _string_list(contract.get("source_size_manifest_fields"), "source_size_manifest_fields")
    confidence_fields = _string_list(contract.get("confidence_register_fields"), "confidence_register_fields")
    audit_fields = _string_list(contract.get("audit_log_fields"), "audit_log_fields")
    confidence_values = set(_string_list(contract.get("confidence_values"), "confidence_values"))
    evidence_types = set(_string_list(contract.get("evidence_types"), "evidence_types"))

    source_rows = _read_jsonl(paths["source_size_manifest"])
    for index, row in enumerate(source_rows, start=1):
        _require_fields(row, source_fields, paths["source_size_manifest"], index)
        _require_task_and_non_authorizing({**row, "non_authorizing": True}, paths["source_size_manifest"], index)
        for field in ("bytes_read", "char_count", "line_count", "record_count", "chapter_count", "verse_count"):
            _require_non_negative_int(row, field, paths["source_size_manifest"], index)
        if row.get("files_read") is not True:
            raise T411CursorBatchArtifactError(f"{_rel(paths['source_size_manifest'])} row {index}: files_read must be true")
        if not isinstance(row.get("sha256_short"), str) or not re.fullmatch(r"[0-9a-fA-F]{6,64}", row["sha256_short"]):
            raise T411CursorBatchArtifactError(f"{_rel(paths['source_size_manifest'])} row {index}: sha256_short must be hex-like")

    confidence_rows = _read_jsonl(paths["confidence_register"])
    claim_ids: set[str] = set()
    escalation_needed = False
    for index, row in enumerate(confidence_rows, start=1):
        _require_fields(row, confidence_fields, paths["confidence_register"], index)
        _require_task_and_non_authorizing(row, paths["confidence_register"], index)
        claim_id = row.get("claim_id")
        if not isinstance(claim_id, str) or not claim_id.strip():
            raise T411CursorBatchArtifactError(f"{_rel(paths['confidence_register'])} row {index}: claim_id must be non-empty")
        if claim_id in claim_ids:
            raise T411CursorBatchArtifactError(f"{_rel(paths['confidence_register'])}: duplicate claim_id {claim_id}")
        claim_ids.add(claim_id)
        if row.get("confidence") not in confidence_values:
            raise T411CursorBatchArtifactError(f"{_rel(paths['confidence_register'])} row {index}: invalid confidence")
        if row.get("evidence_type") not in evidence_types:
            raise T411CursorBatchArtifactError(f"{_rel(paths['confidence_register'])} row {index}: invalid evidence_type")
        if not isinstance(row.get("evidence_refs"), list) or not row["evidence_refs"]:
            raise T411CursorBatchArtifactError(f"{_rel(paths['confidence_register'])} row {index}: evidence_refs must be non-empty")
        if row.get("inferred_or_observed") not in {"inferred", "observed"}:
            raise T411CursorBatchArtifactError(f"{_rel(paths['confidence_register'])} row {index}: inferred_or_observed must be inferred or observed")
        if any(_bool(row.get(field)) for field in ("theology_sensitive", "escalation_required")) or row.get("confidence") in {"low", "blocked"}:
            escalation_needed = True
            if not isinstance(row.get("escalation_reason"), str) or not row["escalation_reason"].strip():
                raise T411CursorBatchArtifactError(f"{_rel(paths['confidence_register'])} row {index}: escalation_reason required")

    audit_rows = _read_jsonl(paths["audit_log"])
    has_preflight = False
    for index, row in enumerate(audit_rows, start=1):
        _require_fields(row, audit_fields, paths["audit_log"], index)
        _require_task_and_non_authorizing(row, paths["audit_log"], index)
        action = str(row.get("command_or_action", "")).lower()
        result = str(row.get("result", "")).lower()
        if "git status" in action or "validate_parallel_execution_safety" in action or row.get("git_status_preflight"):
            has_preflight = True
        if result in {"", "failed_authorizing"}:
            raise T411CursorBatchArtifactError(f"{_rel(paths['audit_log'])} row {index}: result must be explicit")
    if not has_preflight:
        raise T411CursorBatchArtifactError(f"{_rel(paths['audit_log'])}: missing git/parallel-safety preflight row")

    trace_text = paths["claim_traceability_matrix"].read_text(encoding="utf-8")
    lowered_trace = trace_text.lower()
    if "non-authorizing" not in lowered_trace and "non_authorizing" not in lowered_trace:
        raise T411CursorBatchArtifactError(f"{_rel(paths['claim_traceability_matrix'])}: must state non-authorizing")
    for claim_id in sorted(claim_ids):
        if claim_id not in trace_text:
            raise T411CursorBatchArtifactError(f"{_rel(paths['claim_traceability_matrix'])}: missing claim_id {claim_id}")

    notes_text = paths["cursor_notes_to_codex"].read_text(encoding="utf-8").lower()
    required_sections = _string_list(
        contract.get("required_handoff_note", {}).get("required_sections"),
        "required_handoff_note.required_sections",
    )
    missing_sections = [section for section in required_sections if section.replace("_", " ") not in notes_text and section not in notes_text]
    if missing_sections:
        raise T411CursorBatchArtifactError(f"{_rel(paths['cursor_notes_to_codex'])}: missing section(s) {missing_sections}")

    packet_files = [path for path in paths["escalation_packets"].rglob("*") if path.is_file()]
    if escalation_needed and not packet_files:
        raise T411CursorBatchArtifactError(f"{_rel(paths['escalation_packets'])}: escalation packet required by confidence rows")

    return {"mode": "artifacts", "claims": len(claim_ids), "source_rows": len(source_rows)}


def validate_t411_cursor_batch_artifacts(
    *,
    require_artifacts: bool = False,
    task_file: Path = TASK_FILE,
    agent_work: Path = AGENT_WORK,
    handoff_dir: Path = HANDOFF_DIR,
) -> dict[str, Any]:
    setup = validate_task_setup(task_file=task_file, agent_work=agent_work, handoff_dir=handoff_dir)
    artifacts = validate_emitted_artifacts(agent_work=agent_work, handoff_dir=handoff_dir, require_artifacts=require_artifacts)
    return {"setup": setup, "artifacts": artifacts}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-artifacts", action="store_true", help="Require the full Cursor artifact set.")
    args = parser.parse_args(argv)
    try:
        result = validate_t411_cursor_batch_artifacts(require_artifacts=args.require_artifacts)
    except T411CursorBatchArtifactError as exc:
        print(f"T411 Cursor batch artifact validation failed: {exc}", file=sys.stderr)
        return 1
    print(f"T411 Cursor batch artifact validation passed ({result['artifacts']['mode']} mode).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
