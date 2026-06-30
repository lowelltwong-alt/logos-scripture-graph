#!/usr/bin/env python3
"""Build or check a Cursor-readable pack from the T412 Rust observation substrate."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

ROOT_FOR_IMPORT = Path(__file__).resolve().parent.parent
if str(ROOT_FOR_IMPORT) not in sys.path:
    sys.path.insert(0, str(ROOT_FOR_IMPORT))

from scripts.validate_rust_observation_substrate import (
    ROOT,
    RustObservationSubstrateError,
    validate_generated_substrate,
)

TASK_ROOT = ROOT / ".ai" / "tasks"


class CursorObservationPackError(ValueError):
    """Raised when a Cursor observation pack cannot be built safely."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            if not isinstance(row, dict):
                raise CursorObservationPackError(f"{_rel(path)}: expected JSON object rows")
            rows.append(row)
    return rows


def _task_books(task_id: str) -> set[str]:
    task_path = TASK_ROOT / f"{task_id}.task.yaml"
    if not task_path.is_file():
        return set()
    data = yaml.safe_load(task_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return set()
    docket = data.get("candidate_docket")
    if not isinstance(docket, dict):
        return set()
    books = set()
    for item in docket.get("candidates", []):
        if isinstance(item, dict) and isinstance(item.get("book"), str):
            books.add(item["book"])
    return books


def build_cursor_observation_pack(
    *,
    input_dir: Path,
    task_id: str,
    output_dir: Path | None = None,
    check: bool = False,
) -> dict[str, Any]:
    try:
        validation = validate_generated_substrate(input_dir)
    except RustObservationSubstrateError as exc:
        raise CursorObservationPackError(str(exc)) from exc

    book_rows = _read_jsonl(input_dir / "book_observations.jsonl")
    risk_rows = _read_jsonl(input_dir / "risk_signal_index.jsonl")
    span_rows = _read_jsonl(input_dir / "span_observation_features.jsonl")
    task_books = _task_books(task_id)
    selected_books = task_books or {row["book_id"] for row in book_rows if row.get("source_class") == "canonical_66"}

    selected_book_rows = [row for row in book_rows if row.get("book_id") in selected_books]
    selected_span_rows = [row for row in span_rows if row.get("book_id") in selected_books]
    risk_counts = Counter(row.get("signal_kind") for row in risk_rows if row.get("book_id") in selected_books)

    manifest = {
        "type": "CursorObservationPackManifest",
        "schema_version": "cursor_observation_pack.v1",
        "task_id": task_id,
        "source_substrate": _rel(input_dir),
        "non_authorizing": True,
        "no_text": True,
        "selected_books": sorted(selected_books),
        "book_rows": len(selected_book_rows),
        "span_rows": len(selected_span_rows),
        "risk_signal_counts": dict(sorted(risk_counts.items())),
        "cursor_may_select_target": False,
        "authorizes_reviewed_gold_promotion": False,
        "authorizes_chunk_output_change": False,
    }

    if check:
        return {"mode": "check", "validation": validation, "manifest": manifest}

    if output_dir is None:
        output_dir = ROOT / ".ai" / "context" / "agent_work" / task_id / "ledger_inputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "cursor_pack_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    with (output_dir / "book_ledger_summary.jsonl").open("w", encoding="utf-8") as handle:
        for row in selected_book_rows:
            summary = {
                "task_id": task_id,
                "book_id": row["book_id"],
                "source_entry": row["source_entry"],
                "chapter_count": row["chapter_count"],
                "verse_count": row["verse_count"],
                "marker_counts": row["marker_counts"],
                "strong_h_count": row["strong_h_count"],
                "strong_g_count": row["strong_g_count"],
                "feature_flags": row["feature_flags"],
                "non_authorizing": True,
                "no_text": True,
            }
            handle.write(json.dumps(summary, sort_keys=True) + "\n")
    with (output_dir / "span_feature_summary.jsonl").open("w", encoding="utf-8") as handle:
        for row in selected_span_rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
    (output_dir / "README.md").write_text(
        "# Cursor Observation Ledger Inputs\n\n"
        "Generated from the T412 Rust observation substrate. These files are evidence only, "
        "contain no Bible text, and authorize no target selection, reviewed gold, chunk output, "
        "route/evaluator behavior, graph/retrieval/vector truth, or theology authority.\n",
        encoding="utf-8",
    )
    return {"mode": "write", "validation": validation, "manifest": manifest, "output_dir": _rel(output_dir)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = build_cursor_observation_pack(
            input_dir=args.input,
            task_id=args.task_id,
            output_dir=args.output,
            check=args.check,
        )
    except CursorObservationPackError as exc:
        print(f"Cursor observation pack validation failed: {exc}", file=sys.stderr)
        return 1
    print(f"Cursor observation pack {result['mode']} passed for {args.task_id}.")
    print(json.dumps(result["manifest"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
