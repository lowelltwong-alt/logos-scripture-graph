#!/usr/bin/env python3
"""Validate T423 pilot gate — block full 66 until owner sets go; check batch2 spans surface."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.t423_chunk_map_utils import (
    SCRATCH_ROOT,
    completed_books,
    discover_model_folders,
    load_fork_policy,
    normalize_span,
    parse_span,
    spans_overlap,
)

COMPARISON = SCRATCH_ROOT / "comparison"
AGREEMENT = COMPARISON / "agreement_chunks.jsonl"
DELTAS = COMPARISON / "disagreement_delta.jsonl"


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_jsonl_spans(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def _row_surfaces_span(row: dict[str, Any], *, book: str, span: str) -> bool:
    if str(row.get("book", "")) != book:
        return False
    try:
        required = parse_span(span)
    except ValueError:
        return False

    candidates: list[str] = []
    top_span = row.get("span") or row.get("region")
    if isinstance(top_span, str):
        candidates.append(top_span)
    models = row.get("models", {})
    if isinstance(models, dict):
        candidates.extend(str(value) for value in models.values() if isinstance(value, str))

    for candidate in candidates:
        if "." not in candidate:
            continue
        try:
            if spans_overlap(required, parse_span(candidate)):
                return True
        except ValueError:
            continue
    return False


def validate_pilot_gate(*, policy: dict[str, Any] | None = None, scratch_root: Path | None = None) -> list[str]:
    errors: list[str] = []
    policy = policy or load_fork_policy()
    root = scratch_root or SCRATCH_ROOT
    gate = policy.get("pilot_gate", {})
    status = str(gate.get("status", "pending")).lower()
    pilot_books = set(gate.get("required_books", ["Gen", "Ps", "Phlm", "Jonah", "Rev"]))
    full_blocked = status != "go"

    folders = discover_model_folders(root)

    for folder in folders:
        done = completed_books(folder)
        if full_blocked:
            outside_pilot = done - pilot_books
            if outside_pilot:
                errors.append(
                    f"{folder.name}: books outside pilot set while pilot_gate.status={status}: "
                    f"{', '.join(sorted(outside_pilot))}"
                )
        if done and len(done) >= 66 and full_blocked:
            errors.append(f"{folder.name}: full 66 books complete but pilot_gate.status is not go")

    if status == "go":
        batch2_spans = gate.get("required_checks", {}).get("batch2_span_surfaces", [])
        if not batch2_spans:
            batch2_spans = [
                {"book": "Phlm", "span": "Phlm.1.1-Phlm.1.7"},
                {"book": "Jude", "span": "Jude.1.1-Jude.1.2"},
                {"book": "Jonah", "span": "Jonah.1.1-Jonah.1.3"},
            ]
        agreements = _read_jsonl_spans(AGREEMENT)
        deltas = _read_jsonl_spans(DELTAS)

        for entry in batch2_spans:
            if not isinstance(entry, dict):
                continue
            book = str(entry.get("book", ""))
            span = str(entry.get("span", ""))
            try:
                normalized = normalize_span(span)
            except ValueError:
                normalized = span
            surfaced = any(_row_surfaces_span(row, book=book, span=normalized) for row in agreements + deltas)
            if not surfaced and (COMPARISON / "model_agreement_matrix.yaml").is_file():
                errors.append(f"batch2 span not in agreement or delta ledgers: {book} {span}")

    if not gate:
        errors.append("pilot_gate section missing from fork policy")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scratch-root", type=Path, default=SCRATCH_ROOT)
    args = parser.parse_args()

    errors = validate_pilot_gate(scratch_root=args.scratch_root)
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    print("T423 pilot gate: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
