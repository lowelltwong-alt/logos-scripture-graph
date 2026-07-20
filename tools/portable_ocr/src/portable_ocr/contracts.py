"""Dependency-free integrity helpers for immutable OCR artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


class ContractError(ValueError):
    """A portable OCR contract is malformed, unsafe, or unverifiable."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"cannot read JSON contract {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ContractError(f"JSON contract must be an object: {path}")
    return value


def write_json_exclusive(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(value, handle, indent=2, sort_keys=True, ensure_ascii=False)
            handle.write("\n")
    except FileExistsError as exc:
        raise ContractError(f"refusing to overwrite immutable artifact: {path}") from exc


def verify_run_artifacts(run_dir: Path, run: dict[str, Any]) -> None:
    """Recompute the evidence hash chain before review or handoff."""
    if run.get("schema") != "portable_ocr_run.v1":
        raise ContractError("unsupported OCR run schema")
    snapshots = [path for path in run_dir.glob("source.*") if path.is_file()]
    if len(snapshots) != 1:
        raise ContractError("run directory requires exactly one source snapshot")
    expected_source = str(run.get("source", {}).get("sha256", ""))
    if len(expected_source) != 64 or sha256_file(snapshots[0]) != expected_source:
        raise ContractError("OCR source snapshot hash mismatch")
    candidates = run.get("candidates")
    if not isinstance(candidates, list) or len(candidates) < 2:
        raise ContractError("OCR run requires at least two candidates")
    ids: set[str] = set()
    labels: set[str] = set()
    for candidate in candidates:
        candidate_id = str(candidate.get("candidate_id", ""))
        label = str(candidate.get("blind_label", ""))
        text = candidate.get("text")
        if not candidate_id or candidate_id in ids or not label or label in labels or not isinstance(text, str):
            raise ContractError("OCR candidate identity or text is invalid")
        if canonical_sha256(text) != candidate.get("text_sha256"):
            raise ContractError(f"OCR candidate text hash mismatch: {label}")
        ids.add(candidate_id)
        labels.add(label)
    from .comparison import compare_candidates

    if compare_candidates(candidates) != run.get("comparison"):
        raise ContractError("OCR candidate comparison evidence mismatch")
