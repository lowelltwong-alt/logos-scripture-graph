#!/usr/bin/env python3
"""Validate T464 multi-model comparison and owner-decision docket artifacts."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.t423_chunk_map_utils import canonical_books

SCRATCH_ROOT = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking"
COMPARISON = SCRATCH_ROOT / "comparison"
MANIFEST = SCRATCH_ROOT / "manifest.yaml"
CODEX_MODEL_ID = "M4_codex_gpt55"
FABLE_MODEL_ID = "M6_fable5"
STALE_MODEL_IDS = {"M2_codex", "M3_claude", "M4_gemini", "M5_composer_alt"}
DECISION_STATUSES = {
    "consensus_low_risk_candidate",
    "codex_fable_recommended_candidate",
    "frontier_review_required",
    "owner_decision_required",
    "harness_fix_or_rerun_required",
    "phase2_deferred",
}
REQUIRED_COMPARISON_FILES = {
    "agreement_chunks.jsonl",
    "disagreement_delta.jsonl",
    "model_agreement_matrix.yaml",
    "delta_focus_queue.yaml",
    "delta_summary.md",
    "owner_decision_docket.yaml",
    "frontier_review_queue.jsonl",
    "harness_improvement_queue.md",
}
REQUIRED_MODEL_FILES = {
    "model_manifest.yaml",
    "marathon_progress.yaml",
    "whole_bible_chunk_map.jsonl",
    "low_confidence_register.jsonl",
    "frontier_escalation_queue.jsonl",
    "atlas_candidate_feed.jsonl",
    "model_quality_summary.md",
}


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError(f"{_rel(path)}: expected YAML mapping")
    return data


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.is_file():
        return rows
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            row = json.loads(stripped)
            if not isinstance(row, dict):
                raise ValueError(f"{_rel(path)}:{line_no}: expected JSON object")
            rows.append(row)
    return rows


def _active_models(manifest: dict[str, Any]) -> list[str]:
    active = manifest.get("model_count", {}).get("active_slots", [])
    if not isinstance(active, list):
        return []
    return [str(item) for item in active]


def _assert_non_authorizing(row: dict[str, Any], label: str, errors: list[str]) -> None:
    if row.get("non_authorizing") is not True:
        errors.append(f"{label}: non_authorizing must be true")
    if row.get("promotion_authority") not in {None, "none"}:
        errors.append(f"{label}: promotion_authority must be none")
    forbidden_truth = (
        "reviewed_gold",
        "chunk_output",
        "child_span_authority",
        "route_behavior_authority",
        "evaluator_behavior_authority",
        "graph_truth",
        "retrieval_truth",
        "vector_truth",
        "theology_authority",
    )
    for key in forbidden_truth:
        if row.get(key) is True:
            errors.append(f"{label}: forbidden authority field {key}=true")


def _validate_models(root: Path, active_models: list[str], errors: list[str]) -> None:
    canon = set(canonical_books())
    for model_id in active_models:
        folder = root / model_id
        if not folder.is_dir():
            errors.append(f"missing model folder {_rel(folder)}")
            continue
        for filename in REQUIRED_MODEL_FILES:
            if not (folder / filename).is_file():
                errors.append(f"missing {_rel(folder / filename)}")
        manifest_path = folder / "model_manifest.yaml"
        if manifest_path.is_file():
            model_manifest = _read_yaml(manifest_path)
            if model_manifest.get("model_id") != model_id:
                errors.append(f"{_rel(manifest_path)}: model_id must be {model_id}")
        book_dirs = {
            path.name
            for path in (folder / "book_chunks").iterdir()
            if path.is_dir() and (path / "chunks.jsonl").is_file()
        } if (folder / "book_chunks").is_dir() else set()
        if book_dirs != canon:
            missing = sorted(canon - book_dirs)
            extra = sorted(book_dirs - canon)
            if missing:
                errors.append(f"{_rel(folder)}: missing canonical book chunks {missing[:10]}")
            if extra:
                errors.append(f"{_rel(folder)}: noncanonical book chunk dirs {extra}")
        strategy_dir = folder / "book_strategy"
        strategy_books = {path.stem for path in strategy_dir.glob("*.md")} if strategy_dir.is_dir() else set()
        if strategy_books != canon:
            missing = sorted(canon - strategy_books)
            extra = sorted(strategy_books - canon)
            if missing:
                errors.append(f"{_rel(strategy_dir)}: missing strategies {missing[:10]}")
            if extra:
                errors.append(f"{_rel(strategy_dir)}: noncanonical strategies {extra}")


def _validate_outputs(
    *,
    active_models: list[str],
    agreements: list[dict[str, Any]],
    deltas: list[dict[str, Any]],
    matrix: dict[str, Any],
    docket: dict[str, Any],
    frontier_rows: list[dict[str, Any]],
    errors: list[str],
) -> None:
    if matrix.get("models_compared") != active_models:
        errors.append("model_agreement_matrix.yaml models_compared must match manifest active_slots")
    if matrix.get("complete_model_count") != len(active_models):
        errors.append("model_agreement_matrix.yaml complete_model_count mismatch")
    if set(matrix.get("books_compared", [])) != set(canonical_books()):
        errors.append("model_agreement_matrix.yaml must compare all 66 canonical books")

    ids_in_docket: set[str] = set()
    statuses = docket.get("statuses", {})
    if not isinstance(statuses, dict):
        errors.append("owner_decision_docket.yaml statuses must be a mapping")
        statuses = {}
    for status, entries in statuses.items():
        if status not in DECISION_STATUSES:
            errors.append(f"owner_decision_docket.yaml unknown status {status}")
        if not isinstance(entries, list):
            errors.append(f"owner_decision_docket.yaml statuses.{status} must be a list")
            continue
        for index, entry in enumerate(entries, start=1):
            if not isinstance(entry, dict):
                errors.append(f"owner_decision_docket.yaml statuses.{status}[{index}] must be a mapping")
                continue
            _assert_non_authorizing(entry, f"docket {status}[{index}]", errors)
            source_id = str(entry.get("source_id", ""))
            if source_id:
                ids_in_docket.add(source_id)

    agreement_ids: set[str] = set()
    for index, row in enumerate(agreements, start=1):
        label = f"agreement_chunks.jsonl:{index}"
        _assert_non_authorizing(row, label, errors)
        agreement_id = str(row.get("agreement_id", ""))
        if not agreement_id:
            errors.append(f"{label}: missing agreement_id")
        agreement_ids.add(agreement_id)
        if row.get("docket_status") not in DECISION_STATUSES:
            errors.append(f"{label}: invalid docket_status")
        if "variant_hot_zone" in set(row.get("risk_flags", [])) and row.get("docket_status") != "frontier_review_required":
            errors.append(f"{label}: variant hot zone must route to frontier_review_required")
        if row.get("requires_frontier_review") is True and row.get("docket_status") != "frontier_review_required":
            errors.append(f"{label}: frontier-required agreement must route to frontier_review_required")
        models_agreeing = set(row.get("models_agreeing", []))
        if not models_agreeing.issubset(set(active_models)):
            errors.append(f"{label}: models_agreeing outside active model set")

    delta_ids: set[str] = set()
    for index, row in enumerate(deltas, start=1):
        label = f"disagreement_delta.jsonl:{index}"
        _assert_non_authorizing(row, label, errors)
        delta_id = str(row.get("delta_id", ""))
        if not delta_id:
            errors.append(f"{label}: missing delta_id")
        delta_ids.add(delta_id)
        if row.get("docket_status") not in DECISION_STATUSES:
            errors.append(f"{label}: invalid docket_status")
        if "variant_hot_zone" in set(row.get("risk_flags", [])) and row.get("docket_status") != "frontier_review_required":
            errors.append(f"{label}: variant hot zone must route to frontier_review_required")
        if row.get("decision_route") != row.get("docket_status"):
            errors.append(f"{label}: decision_route must equal docket_status")
        if row.get("requires_frontier_review") is True and row.get("docket_status") != "frontier_review_required":
            errors.append(f"{label}: frontier-required delta must route to frontier_review_required")
        models = row.get("models", {})
        if isinstance(models, dict):
            model_keys = set(str(key) for key in models)
            if not model_keys.issubset(set(active_models)):
                errors.append(f"{label}: delta model set contains inactive model id")
            m4 = models.get(CODEX_MODEL_ID)
            m6 = models.get(FABLE_MODEL_ID)
            if isinstance(m4, str) and isinstance(m6, str) and m4 == m6:
                if row.get("recommended_candidate_basis") != "codex_fable_alignment":
                    errors.append(f"{label}: M4/M6 agreement must be marked codex_fable_alignment")

    missing_from_docket = (agreement_ids | delta_ids) - ids_in_docket
    if missing_from_docket:
        errors.append(f"owner_decision_docket.yaml missing source ids: {sorted(missing_from_docket)[:10]}")

    for index, row in enumerate(frontier_rows, start=1):
        label = f"frontier_review_queue.jsonl:{index}"
        _assert_non_authorizing(row, label, errors)
        if row.get("source_id") not in agreement_ids | delta_ids:
            errors.append(f"{label}: source_id must reference agreement or delta ledger")


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    scratch = root / ".ai" / "scratch" / "multi_model_bible_chunking"
    comparison = scratch / "comparison"
    manifest_path = scratch / "manifest.yaml"
    if not manifest_path.is_file():
        return [f"missing {_rel(manifest_path)}"]
    manifest = _read_yaml(manifest_path)
    active_models = _active_models(manifest)
    if len(active_models) < 6:
        errors.append("T464 requires six active complete model slots")
    stale_active = sorted(set(active_models).intersection(STALE_MODEL_IDS))
    if stale_active:
        errors.append(f"manifest active_slots contains stale model ids: {stale_active}")

    _validate_models(scratch, active_models, errors)

    for filename in REQUIRED_COMPARISON_FILES:
        if not (comparison / filename).is_file():
            errors.append(f"missing {_rel(comparison / filename)}")
    if errors:
        return errors

    agreements = _read_jsonl(comparison / "agreement_chunks.jsonl")
    deltas = _read_jsonl(comparison / "disagreement_delta.jsonl")
    frontier_rows = _read_jsonl(comparison / "frontier_review_queue.jsonl")
    matrix = _read_yaml(comparison / "model_agreement_matrix.yaml")
    docket = _read_yaml(comparison / "owner_decision_docket.yaml")

    for path in REQUIRED_COMPARISON_FILES:
        text = (comparison / path).read_text(encoding="utf-8")
        for stale in STALE_MODEL_IDS:
            pattern = rf"(?<![A-Za-z0-9_]){re.escape(stale)}(?![A-Za-z0-9_])"
            if re.search(pattern, text):
                errors.append(f"{_rel(comparison / path)} contains stale model id {stale}")

    _validate_outputs(
        active_models=active_models,
        agreements=agreements,
        deltas=deltas,
        matrix=matrix,
        docket=docket,
        frontier_rows=frontier_rows,
        errors=errors,
    )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("T464 multi-model comparison decision docket validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
