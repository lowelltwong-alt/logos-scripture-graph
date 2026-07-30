#!/usr/bin/env python3
"""Audit Sol's candidate map for chapter-scaffold fallback coverage.

This is a read-only, candidate-only quality audit.  It does not change chunks,
choose boundaries, or authorize promotion.  It flags records whose working
title or explicit marker shows that a chapter-sized fallback remains in use.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def audit(path: Path) -> dict:
    by_book: dict[str, list[dict]] = defaultdict(list)
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            by_book[row["book"]].append(row)

    books = []
    fallback_total = 0
    for book, rows in by_book.items():
        fallback = [
            r for r in rows
            if "chapter_scaffold_not_boundary_authority" in r.get("strong_or_hebrew_tags_used", [])
            or "structural frame (draft)" in r.get("working_title", "")
            or "chapter boundary fallback" in r.get("boundary_rationale", "").lower()
        ]
        fallback_total += len(fallback)
        if fallback:
            books.append({
                "book": book,
                "candidate_count": len(rows),
                "fallback_count": len(fallback),
                "fallback_ratio": round(len(fallback) / len(rows), 4),
                "priority": "high" if len(fallback) == len(rows) else "medium",
                "required_next_review": [
                    "replace or justify chapter-sized fallback with literary seam evidence",
                    "check original-language discourse/translation pressure",
                    "check internal canonical relation and quotation/allusion pressure",
                    "preserve red-team challenges and appeals; do not promote boundaries",
                ],
            })
    books.sort(key=lambda x: (-x["fallback_ratio"], -x["fallback_count"], x["book"]))
    return {
        "schema_version": "m7_sol_scaffold_fidelity_audit.v1",
        "model_id": "M7_sol",
        "candidate_only": True,
        "non_authorizing": True,
        "map_path": str(path),
        "book_count": len(by_book),
        "chunk_count": sum(len(v) for v in by_book.values()),
        "books_with_fallbacks": len(books),
        "fallback_chunk_count": fallback_total,
        "promotion_qualified": False,
        "books": books,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("map_path", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit(args.map_path)
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8", newline="\n")
    print(json.dumps({k: result[k] for k in (
        "book_count", "chunk_count", "books_with_fallbacks",
        "fallback_chunk_count", "candidate_only", "non_authorizing",
        "promotion_qualified",
    )}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
