#!/usr/bin/env python3
"""Validate T327B canonical 66-book allow-list and optional JSONL records."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.util.canonical_scope import (  # noqa: E402
    CanonicalScopeError,
    assert_records_are_canonical_66,
    canonical_66_books,
    excluded_books,
)


REQUIRED_EXCLUDED = {
    "FRT",
    "GLO",
    "Tob",
    "Jdt",
    "AddEsth",
    "Wis",
    "Sir",
    "Bar",
    "1Macc",
    "2Macc",
    "1Esd",
    "PrMan",
    "Ps151",
    "3Macc",
    "2Esd",
    "4Macc",
    "AddDan",
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                records.append(json.loads(line))
    return records


def validate_config() -> None:
    books = canonical_66_books()
    if books[0] != "Gen" or books[-1] != "Rev":
        raise CanonicalScopeError("Canonical 66-book allow-list must run from Gen through Rev")
    excluded = set(excluded_books())
    missing = REQUIRED_EXCLUDED - excluded
    if missing:
        raise CanonicalScopeError(f"Missing excluded book ids: {sorted(missing)}")
    overlap = set(books) & excluded
    if overlap:
        raise CanonicalScopeError(f"Books cannot be both canonical and excluded: {sorted(overlap)}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "jsonl",
        nargs="*",
        help=(
            "Optional generated JSONL files to validate. Existing canonical outputs are not "
            "passed by validate_all until T327C regeneration."
        ),
    )
    args = parser.parse_args(argv)

    try:
        validate_config()
        for path_text in args.jsonl:
            path = Path(path_text)
            assert_records_are_canonical_66(load_jsonl(path), source=str(path))
    except CanonicalScopeError as exc:
        print(f"Canonical 66 scope validation failed: {exc}", file=sys.stderr)
        return 1

    if args.jsonl:
        print(f"Canonical 66 scope validation passed for {len(args.jsonl)} JSONL file(s).")
    else:
        print("Canonical 66 scope config validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
