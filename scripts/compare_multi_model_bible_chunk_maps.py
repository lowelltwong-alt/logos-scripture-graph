#!/usr/bin/env python3
"""Compare T423 model whole_bible_chunk_map.jsonl files — agreement vs delta."""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from scripts.t423_chunk_map_utils import (
    SCRATCH_ROOT,
    canonical_books,
    compare_book_verse_coverage,
    completed_books,
    discover_model_folders,
    load_chunk_map,
    load_fork_policy,
    load_model_manifest,
    majority_required,
    model_is_complete,
)

ROOT = Path(__file__).resolve().parent.parent
COMPARISON_ROOT = SCRATCH_ROOT / "comparison"
STRESS_ATLAS = ROOT / "eval" / "chunking_stress_atlas" / "biblical_chunking_stress_atlas.json"


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def _load_stress_books() -> set[str]:
    if not STRESS_ATLAS.is_file():
        return set()
    data = json.loads(STRESS_ATLAS.read_text(encoding="utf-8"))
    books: set[str] = set()
    for entry in data.get("entries", []):
        book = entry.get("book")
        if isinstance(book, str):
            books.add(book)
    return books


def _load_t417_overlap_books(policy: dict[str, Any]) -> set[str]:
    isolation = policy.get("parallel_path_isolation", {})
    overlap = isolation.get("overlap_books_with_T417_batch2", [])
    if isinstance(overlap, list):
        return {str(b) for b in overlap}
    return set()


def select_models(
    folders: list[Path],
    *,
    min_complete: int,
    require_all_initial_target: bool,
    initial_target: int,
    interim: bool,
) -> tuple[list[Path], list[str]]:
    errors: list[str] = []
    complete = [f for f in folders if model_is_complete(f)]
    if require_all_initial_target and not interim:
        if len(complete) < initial_target:
            errors.append(
                f"need {initial_target} complete models for default compare; have {len(complete)}"
            )
    elif len(complete) < min_complete:
        errors.append(f"need at least {min_complete} complete models; have {len(complete)}")
    return complete, errors


def books_in_scope(
    model_folders: list[Path],
    *,
    books_filter: set[str] | None,
    require_book_complete: bool,
) -> list[str]:
    if books_filter:
        return sorted(books_filter)
    if require_book_complete:
        sets = [completed_books(f) for f in model_folders]
        if not sets:
            return []
        common = set.intersection(*sets)
        return sorted(common)
    return canonical_books()


def compare_models(
    model_folders: list[Path],
    *,
    books: list[str],
    allow_easy_at_n3: bool,
    t417_overlap_books: set[str] | None = None,
) -> dict[str, Any]:
    model_ids = [str(load_model_manifest(f).get("model_id", f.name)) for f in model_folders]
    n = len(model_folders)
    majority = majority_required(n)
    overlap = t417_overlap_books or set()
    maps: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for folder, model_id in zip(model_folders, model_ids, strict=True):
        by_book: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for record in load_chunk_map(folder):
            book = str(record.get("book", ""))
            if book in books:
                by_book[book].append(record)
        for book in by_book:
            by_book[book].sort(key=lambda r: int(r["chunk_index_in_book"]))
        maps[model_id] = by_book

    agreements: list[dict[str, Any]] = []
    deltas: list[dict[str, Any]] = []
    per_book_stats: dict[str, dict[str, Any]] = {}
    stress_books = _load_stress_books()

    for book in books:
        book_chunks = {mid: maps[mid].get(book, []) for mid in model_ids}
        result = compare_book_verse_coverage(
            book_chunks,
            book,
            model_ids,
            allow_easy_at_n3=allow_easy_at_n3,
            stress_book=book in stress_books,
            overlap_t417=book in overlap,
        )
        agreements.extend(result.span_consensus_chunks)
        deltas.extend(result.boundary_deltas)
        per_book_stats[book] = {
            "verse_coverage_agreement_rate": result.verse_coverage_agreement_rate,
            "verses_total": result.verses_total,
            "verses_agreed": result.verses_agreed,
            "agreement_rate_exact_span": result.agreement_rate_exact_span_legacy,
            "chunk_counts": result.chunk_counts,
            "chunk_count_mismatch": len(set(result.chunk_counts.values())) > 1,
        }

    total_verses = sum(s.get("verses_total", 0) for s in per_book_stats.values())
    total_agreed = sum(s.get("verses_agreed", 0) for s in per_book_stats.values())
    overall_verse_rate = (total_agreed / total_verses) if total_verses else 0.0

    total_chunks = sum(
        max(s.get("chunk_counts", {}).values()) if s.get("chunk_counts") else 0
        for s in per_book_stats.values()
    )
    legacy_agreed = sum(
        1 for a in agreements if a.get("book") in per_book_stats
    )
    overall_legacy_rate = (legacy_agreed / total_chunks) if total_chunks else 0.0

    false_consensus: list[dict[str, str]] = []
    for row in agreements:
        if row["agreement_tier"] == "full_consensus" and row["book"] in stress_books:
            false_consensus.append(
                {
                    "book": row["book"],
                    "span": row["span"],
                    "warning": "full_consensus_on_stress_atlas_book",
                }
            )

    return {
        "model_ids": model_ids,
        "complete_model_count": n,
        "majority_required": majority,
        "books_compared": books,
        "agreements": agreements,
        "deltas": deltas,
        "per_book_stats": per_book_stats,
        "overall_verse_coverage_agreement_rate": round(overall_verse_rate, 4),
        "overall_agreement_rate": round(overall_legacy_rate, 4),
        "false_consensus_warnings": false_consensus,
    }


def write_outputs(result: dict[str, Any], *, dry_run: bool) -> None:
    comp = COMPARISON_ROOT
    if dry_run:
        print(json.dumps({k: v for k, v in result.items() if k not in {"agreements", "deltas"}}, indent=2))
        print(f"agreements={len(result['agreements'])} deltas={len(result['deltas'])}")
        return

    _write_jsonl(comp / "agreement_chunks.jsonl", result["agreements"])
    _write_jsonl(comp / "disagreement_delta.jsonl", result["deltas"])

    top_disagreement = sorted(
        result["per_book_stats"].items(),
        key=lambda item: item[1].get("verse_coverage_agreement_rate", 0),
    )[:10]

    matrix = {
        "object_type": "model_agreement_matrix",
        "schema_version": "model_agreement_matrix.v1",
        "generated_at": datetime.now(UTC).isoformat(),
        "complete_model_count": result["complete_model_count"],
        "majority_required": result["majority_required"],
        "models_compared": result["model_ids"],
        "books_compared": result["books_compared"],
        "overall_verse_coverage_agreement_rate": result["overall_verse_coverage_agreement_rate"],
        "overall_agreement_rate_exact_span_legacy": result["overall_agreement_rate"],
        "per_book": result["per_book_stats"],
        "false_consensus_warnings": result["false_consensus_warnings"],
        "non_authorizing": True,
        "promotion_authority": "none",
    }
    (comp / "model_agreement_matrix.yaml").write_text(
        yaml.safe_dump(matrix, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    focus = {
        "object_type": "delta_focus_queue",
        "schema_version": "delta_focus_queue.v1",
        "status": "populated",
        "strategy": "focus_governed_work_on_disagreement_only",
        "easy_chunks_from_agreement": "agreement_chunks.jsonl",
        "delta_source": "disagreement_delta.jsonl",
        "overall_verse_coverage_agreement_rate": result["overall_verse_coverage_agreement_rate"],
        "priority_books": [b for b, _ in top_disagreement],
        "candidates": [
            {
                "delta_id": d["delta_id"],
                "book": d["book"],
                "priority": d.get("priority", "medium"),
                "delta_kind": d.get("delta_kind"),
            }
            for d in result["deltas"][:50]
        ],
        "non_authorizing": True,
        "promotion_authority": "none",
    }
    (comp / "delta_focus_queue.yaml").write_text(
        yaml.safe_dump(focus, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    lines = [
        "# Delta Summary — Multi-Model Whole-Bible Chunk Comparison",
        "",
        "## Scope",
        f"- Models: {', '.join(result['model_ids'])}",
        f"- N = {result['complete_model_count']}; majority = ceil(0.7×N) = {result['majority_required']}",
        f"- Books compared: {len(result['books_compared'])}",
        "",
        "## Headline metrics",
        f"- Overall verse-coverage agreement rate: {result['overall_verse_coverage_agreement_rate']:.2%}",
        f"- Legacy exact-span rate (audit only): {result['overall_agreement_rate']:.2%}",
        f"- Easy chunk count: {len(result['agreements'])}",
        f"- Delta span count: {len(result['deltas'])}",
        "",
        "## Highest-disagreement books (top 10)",
    ]
    for book, stats in top_disagreement:
        lines.append(f"- {book}: {stats.get('verse_coverage_agreement_rate', 0):.2%}")
    lines.extend(
        [
            "",
            "## False consensus warnings",
        ]
    )
    if result["false_consensus_warnings"]:
        for w in result["false_consensus_warnings"][:20]:
            lines.append(f"- {w['book']} {w['span']}: {w['warning']}")
    else:
        lines.append("- none flagged")
    lines.extend(
        [
            "",
            "## Non-authorizations",
            "- Agreement does not promote gold or chunk output",
            "- promotion_authority: none",
        ]
    )
    (comp / "delta_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scratch-root", type=Path, default=SCRATCH_ROOT)
    parser.add_argument("--interim", action="store_true", help="Allow compare before initial_target complete")
    parser.add_argument("--book", action="append", dest="books", help="Compare specific book(s) only")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--require-book-complete",
        action="store_true",
        default=True,
        help="Only compare books marked complete in all model marathon_progress.yaml (default)",
    )
    args = parser.parse_args()

    policy = load_fork_policy()
    rules = policy.get("comparison_rules", {})
    model_count = policy.get("model_count", {})
    min_complete = int(rules.get("compare_when_at_least_models", 3))
    initial_target = int(model_count.get("initial_target", 5))
    interim_default = bool(rules.get("interim_compare_default_requires_initial_target", True))
    allow_easy_at_n3 = bool(rules.get("allow_easy_majority_at_n3", False))
    t417_overlap = _load_t417_overlap_books(policy)

    folders = discover_model_folders(args.scratch_root)
    if not folders:
        print("ERROR: no model folders found", file=sys.stderr)
        return 1

    selected, errors = select_models(
        folders,
        min_complete=min_complete,
        require_all_initial_target=interim_default and not args.interim,
        initial_target=initial_target,
        interim=args.interim,
    )
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1

    books_filter = set(args.books) if args.books else None
    books = books_in_scope(
        selected,
        books_filter=books_filter,
        require_book_complete=args.require_book_complete and not args.books,
    )
    if not books:
        print("ERROR: no books in scope for comparison", file=sys.stderr)
        return 1

    for folder in selected:
        map_path = folder / "whole_bible_chunk_map.jsonl"
        if not map_path.is_file():
            print(f"ERROR: missing {_rel(map_path)}", file=sys.stderr)
            return 1

    result = compare_models(
        selected,
        books=books,
        allow_easy_at_n3=allow_easy_at_n3,
        t417_overlap_books=t417_overlap,
    )
    write_outputs(result, dry_run=args.dry_run)
    if not args.dry_run:
        print(f"OK: compared {result['complete_model_count']} models, {len(books)} books")
        print(f"  verse_coverage_agreement_rate={result['overall_verse_coverage_agreement_rate']:.2%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
