#!/usr/bin/env python3
"""Validate the T475 shadow-delta contract and, when required, its frozen evidence."""
from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

try:
    from scripts.validate_t475_generated_transition_state import DEFERRED_PYTEST_NODES
except ModuleNotFoundError:
    from validate_t475_generated_transition_state import DEFERRED_PYTEST_NODES

try:
    from scripts.validate_task_execution_overlay import ExecutionOverlayError, validate_execution_overlay
except ModuleNotFoundError:
    from validate_task_execution_overlay import ExecutionOverlayError, validate_execution_overlay

ROOT = Path(__file__).resolve().parent.parent
CONTROL = ROOT / ".ai" / "control" / "t475_usfm_shadow_delta_gate.yaml"
TASK = ROOT / ".ai" / "tasks" / "T475.task.yaml"
PROMPT = ROOT / ".ai" / "prompts" / "t475_independent_audit_prompt.md"

REQUIRED_FAMILIES = {
    "scripture/passages/passages.jsonl",
    "translations/eng-web/translation_witnesses.jsonl",
    "translations/eng-web/word_tokens.jsonl",
    "translations/eng-web/footnotes.jsonl",
    "translations/eng-web/editorial_cross_references.jsonl",
    "translations/eng-web/section_headings.jsonl",
    "translations/eng-web/boundary_claims.jsonl",
    "translations/eng-web/glossary_entries.jsonl",
    "usfm_events.jsonl",
    "unsupported_usfm_markers.jsonl",
    "extraction_manifest.yaml",
    "parser_report.yaml",
}
REQUIRED_EVIDENCE = {
    "input_manifest.json",
    "baseline_manifest.json",
    "candidate_manifest.json",
    "repeatability_and_benchmark.json",
    "delta_summary.json",
    "mismatch_ledger.jsonl.gz",
    "sensitive_scope_summary.json",
    "chunk_input_impact.json",
    "sol_acceptance_report.md",
    "terra_parity_report.md",
    "luna_trial_log.md",
    "frozen_evidence_manifest.json",
}
REQUIRED_DEFERRED_GENERATED_VALIDATORS = {
    "validate_t374_additive_parent_overlay.py",
    "validate_t401_eph1_output_pilot.py",
    "validate_t415_batch1_output_pilot.py",
    "validate_source_metadata_research_atlas.py",
    "validate_1cor8_10_parent_evidence_packet.py",
    "validate_divine_capitalization_inventory.py",
    "validate_wj_marker_inventory.py",
}

FALSE_AUTHORITY = {
    "modifies_committed_raw_or_generated_data",
    "modifies_reviewed_gold",
    "authorizes_target_selection",
    "authorizes_reviewed_gold",
    "authorizes_chunk_output",
    "authorizes_child_spans",
    "changes_chunker_or_form_consumer_behavior",
    "changes_route_or_evaluator_behavior",
    "creates_graph_retrieval_or_vector_truth",
    "runs_embeddings_or_builds_indexes",
    "selects_preferred_reading_or_source_tradition",
    "changes_canon_scope",
    "authorizes_theology_authority",
}


class T475ValidationError(ValueError):
    """Raised when T475 contract or evidence is incomplete."""


def _read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise T475ValidationError(f"{path}: missing")
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        header = yaml.safe_load(parts[1]) or {}
        body = yaml.safe_load(parts[2]) or {}
        if not isinstance(header, dict) or not isinstance(body, dict):
            raise T475ValidationError(f"{path}: expected YAML mappings")
        return {**header, **body}
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise T475ValidationError(f"{path}: expected YAML mapping")
    return data


def _mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise T475ValidationError(f"{label}: expected mapping")
    return value


def _git_object_exists(root: Path, ref: str) -> bool:
    if not (root / ".git").exists():
        return True
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{ref}^{{commit}}"],
        cwd=root,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def _read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise T475ValidationError(f"{path}: expected JSON object")
    return data


def _validate_frozen_evidence(
    root: Path,
    control: dict[str, Any],
    *,
    require_independent_audit: bool,
) -> None:
    evidence = _mapping(control["required_evidence"], "required_evidence")
    report_root = root / str(evidence["report_root"])
    for name in REQUIRED_EVIDENCE:
        path = report_root / name
        if not path.is_file():
            raise T475ValidationError(f"required evidence missing: {path}")

    benchmark = _read_json(report_root / "repeatability_and_benchmark.json")
    receipts = benchmark.get("receipts")
    if (
        benchmark.get("deterministic") is not True
        or benchmark.get("repetitions", 0) < 3
        or not isinstance(receipts, list)
        or len(receipts) < 3
    ):
        raise T475ValidationError("repeatability evidence must contain three deterministic trials")
    if len({row.get("baseline_manifest_sha256") for row in receipts if isinstance(row, dict)}) != 1:
        raise T475ValidationError("baseline trial hashes are not deterministic")
    if len({row.get("candidate_manifest_sha256") for row in receipts if isinstance(row, dict)}) != 1:
        raise T475ValidationError("candidate trial hashes are not deterministic")

    summary = _read_json(report_root / "delta_summary.json")
    totals = summary.get("totals")
    if not isinstance(totals, dict):
        raise T475ValidationError("delta_summary.json: totals must be a mapping")
    ledger_counts: Counter[str] = Counter()
    ledger_path = report_root / "mismatch_ledger.jsonl.gz"
    allowed_row_keys = {
        "surface", "class", "stable_key", "before_sha256", "after_sha256",
        "safe_metadata", "field_changes",
    }
    safe_fields = set(control["comparison_contract"]["safe_visible_fields"])
    with gzip.open(ledger_path, "rt", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            row = json.loads(line)
            if not isinstance(row, dict) or set(row) != allowed_row_keys:
                raise T475ValidationError(f"mismatch ledger line {line_no}: unexpected row shape")
            cls = row.get("class")
            if not isinstance(cls, str):
                raise T475ValidationError(f"mismatch ledger line {line_no}: class missing")
            ledger_counts[cls] += 1
            metadata = row.get("safe_metadata")
            if not isinstance(metadata, dict) or not set(metadata).issubset(safe_fields):
                raise T475ValidationError(f"mismatch ledger line {line_no}: unsafe metadata field")
            changes = row.get("field_changes")
            if not isinstance(changes, list):
                raise T475ValidationError(f"mismatch ledger line {line_no}: field_changes must be a list")
            for change in changes:
                if not isinstance(change, dict) or not {"path", "before_sha256", "after_sha256"}.issubset(change):
                    raise T475ValidationError(f"mismatch ledger line {line_no}: invalid field change")
                extra = set(change) - {"path", "before_sha256", "after_sha256", "before", "after"}
                if extra:
                    raise T475ValidationError(f"mismatch ledger line {line_no}: unexpected field keys {sorted(extra)}")
                leaf = str(change["path"]).rsplit(".", 1)[-1]
                if leaf not in safe_fields and ({"before", "after"} & set(change)):
                    raise T475ValidationError(
                        f"mismatch ledger line {line_no}: non-safe value exposed for {change['path']}"
                    )
    expected_counts = {
        key: int(value)
        for key, value in totals.items()
        if key != "unchanged" and int(value) != 0
    }
    if dict(ledger_counts) != expected_counts:
        raise T475ValidationError(
            f"mismatch ledger arithmetic differs from delta summary: {dict(ledger_counts)} != {expected_counts}"
        )

    chunk_impact = _read_json(report_root / "chunk_input_impact.json")
    if chunk_impact.get("chunker_executed") is not False or chunk_impact.get("chunk_output_emitted") is not False:
        raise T475ValidationError("chunk impact evidence indicates forbidden chunker/output execution")
    if _read_json(report_root / "input_manifest.json").get("non_authorizing") is not True:
        raise T475ValidationError("input manifest must remain non-authorizing")

    frozen_path = report_root / "frozen_evidence_manifest.json"
    frozen = _read_json(frozen_path)
    rows = frozen.get("files")
    if not isinstance(rows, list) or not rows:
        raise T475ValidationError("frozen_evidence_manifest.json: files must be non-empty")
    indexed = {row.get("path"): row for row in rows if isinstance(row, dict)}
    for name in REQUIRED_EVIDENCE - {"frozen_evidence_manifest.json"}:
        rel = f".ai/context/agent_work/T475/{name}"
        row = indexed.get(rel)
        if not row:
            raise T475ValidationError(f"frozen manifest missing {rel}")
        digest = hashlib.sha256((root / rel).read_bytes()).hexdigest()
        if row.get("sha256") != digest:
            raise T475ValidationError(f"frozen manifest hash mismatch: {rel}")

    if require_independent_audit:
        audit_path = root / str(evidence["independent_audit_report"])
        if not audit_path.is_file():
            raise T475ValidationError(f"independent audit report missing: {audit_path}")
        if evidence.get("independent_audit_status") not in {
            "PASS", "APPROVE_WITH_NONBLOCKING_FINDINGS"
        }:
            raise T475ValidationError("independent audit status does not permit continuation")


def validate_t475(
    root: Path = ROOT,
    *,
    require_artifacts: bool = False,
    require_independent_audit: bool = False,
) -> dict[str, Any]:
    try:
        validate_execution_overlay(root, "T475")
    except ExecutionOverlayError as exc:
        raise T475ValidationError(str(exc)) from exc
    control_path = root / CONTROL.relative_to(ROOT)
    control = _read_yaml(control_path)
    if control.get("schema_version") != "t475_usfm_shadow_delta_gate.v1":
        raise T475ValidationError("unexpected T475 schema_version")
    if control.get("task_id") != "T475":
        raise T475ValidationError("task_id must be T475")

    revisions = _mapping(control.get("source_revisions"), "source_revisions")
    for key in ("baseline_ref", "candidate_ref"):
        ref = revisions.get(key)
        if not isinstance(ref, str) or len(ref) != 40 or not _git_object_exists(root, ref):
            raise T475ValidationError(f"source_revisions.{key}: missing Git commit")

    inputs = _mapping(control.get("identical_input_contract"), "identical_input_contract")
    for key in ("raw_archive", "source_manifest", "canon_config", "marker_coverage"):
        rel = inputs.get(key)
        if not isinstance(rel, str) or not (root / rel).is_file():
            raise T475ValidationError(f"identical_input_contract.{key}: missing {rel!r}")
    if inputs.get("required_flag") != "--canonical-66-filter":
        raise T475ValidationError("canonical-66 filter is required")
    if inputs.get("forbidden_flag") != "--skip-sha-check":
        raise T475ValidationError("SHA bypass must remain forbidden")

    roots = _mapping(control.get("shadow_roots"), "shadow_roots")
    if roots.get("tracked_output_allowed") is not False or roots.get("require_git_ignored") is not True:
        raise T475ValidationError("shadow outputs must be ignored and untracked")
    if not all(str(roots.get(key, "")).replace("\\", "/").startswith("build/T475") for key in ("root", "baseline", "candidate", "source_snapshots")):
        raise T475ValidationError("all shadow roots must stay under build/T475")

    trials = _mapping(control.get("trial_contract"), "trial_contract")
    if trials.get("repetitions", 0) < 3 or trials.get("byte_identical_repeated_output_required") is not True:
        raise T475ValidationError("three deterministic repetitions are required")

    families = control.get("required_output_families")
    if not isinstance(families, list) or set(families) != REQUIRED_FAMILIES:
        raise T475ValidationError("required output families are incomplete")

    comparison = _mapping(control.get("comparison_contract"), "comparison_contract")
    if comparison.get("visible_scripture_text_allowed_in_reports") is not False:
        raise T475ValidationError("Scripture text must not be visible in delta reports")
    if comparison.get("aggregate_must_equal_row_ledger") is not True:
        raise T475ValidationError("aggregate and row ledger must reconcile")
    if not (root / str(comparison.get("streaming_python_oracle", ""))).is_file():
        raise T475ValidationError("streaming Python oracle is missing")

    chunk = _mapping(control.get("chunk_impact_contract"), "chunk_impact_contract")
    if chunk.get("run_chunker") is not False or chunk.get("emit_chunk_output") is not False:
        raise T475ValidationError("T475 may not run the chunker or emit chunk output")

    transition = _mapping(
        control.get("ci_generated_transition_policy"),
        "ci_generated_transition_policy",
    )
    if set(transition.get("deferred_legacy_generated_validators", [])) != REQUIRED_DEFERRED_GENERATED_VALIDATORS:
        raise T475ValidationError("T475 deferred generated-validator set changed")
    if set(transition.get("deferred_pytest_nodes", [])) != DEFERRED_PYTEST_NODES:
        raise T475ValidationError("T475 deferred pytest node set changed")
    if transition.get("active_task_required") != "T475":
        raise T475ValidationError("T475 transition policy must require active task T475")
    if transition.get("detected_candidate_counts") != {
        "word_tokens": 677686,
        "footnotes": 1130,
    }:
        raise T475ValidationError("T475 transition candidate counts changed")
    if transition.get("transitional_data_map_check") != "scripts/generate_data_map.py --check":
        raise T475ValidationError("T475 transition DATA_MAP check changed")
    if transition.get("data_map_candidate_delta") != {
        "total_jsonl_records": {"baseline": 847086, "candidate": 847084},
        "word_tokens": {"baseline": 677688, "candidate": 677686},
        "footnotes": {"baseline": 1130, "candidate": 1130},
    }:
        raise T475ValidationError("T475 transition DATA_MAP delta changed")
    for key in ("authorizes_baseline_update", "authorizes_gold_or_output_change"):
        if transition.get(key) is not False:
            raise T475ValidationError(f"ci_generated_transition_policy.{key} must be false")
    transition_validator = root / str(transition.get("validator", ""))
    if not transition_validator.is_file():
        raise T475ValidationError("T475 generated-transition validator is missing")

    evidence = _mapping(control.get("required_evidence"), "required_evidence")
    if set(evidence.get("files", [])) != REQUIRED_EVIDENCE:
        raise T475ValidationError("required evidence files are incomplete")

    authority = _mapping(control.get("authority"), "authority")
    wrong = sorted(key for key in FALSE_AUTHORITY if authority.get(key) is not False)
    if wrong:
        raise T475ValidationError(f"authority flags must remain false: {wrong}")

    prompt_path = root / PROMPT.relative_to(ROOT)
    prompt_text = prompt_path.read_text(encoding="utf-8").lower()
    for phrase in ("cannot authorize", "do not implement fixes", "speed alone is never sufficient"):
        if phrase not in prompt_text:
            raise T475ValidationError(f"independent audit prompt missing guard: {phrase}")

    if require_independent_audit:
        require_artifacts = True
    if require_artifacts:
        _validate_frozen_evidence(
            root,
            control,
            require_independent_audit=require_independent_audit,
        )

    return {
        "families": len(families),
        "require_artifacts": require_artifacts,
        "require_independent_audit": require_independent_audit,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-artifacts", action="store_true")
    parser.add_argument("--require-independent-audit", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = validate_t475(
            ROOT,
            require_artifacts=args.require_artifacts,
            require_independent_audit=args.require_independent_audit,
        )
    except T475ValidationError as exc:
        print(f"T475 shadow-delta validation failed: {exc}", file=sys.stderr)
        return 1
    print(f"T475 shadow-delta validation passed ({result['families']} output families).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
