#!/usr/bin/env python3
"""Build a whole-map fidelity/readiness snapshot without promoting candidates."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol"
MAP = MODEL / "state/evidence/final/whole_bible_candidate_map.jsonl"
OUT = MODEL / "state/evidence/final/fidelity_readiness_report.json"


def main() -> int:
    rows = [json.loads(x) for x in MAP.read_text(encoding="utf-8").splitlines() if x.strip()]
    by_book: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_book[row["book"]].append(row)
    refined = {}
    scaffolds = {}
    for book, items in by_book.items():
        refined[book] = sum(1 for row in items if any("wave" in str(ref) or "refinement" in str(ref) for ref in row.get("boundary_evidence_refs", [])))
        scaffolds[book] = sum(1 for row in items if "chapter_scaffold_not_boundary_authority" in row.get("strong_or_hebrew_tags_used", []))
    report = {
        "schema_version": "t521_fidelity_readiness_report.v1",
        "model_id": "M7_sol",
        "candidate_only": True,
        "non_authorizing": True,
        "promotion_qualified": False,
        "independence_status": "awaiting_external_provider_or_human_receipt",
        "book_count": len(by_book),
        "chunk_count": len(rows),
        "books_with_refinement_metadata": sorted(book for book, count in refined.items() if count),
        "books_without_refinement_metadata": sorted(book for book, count in refined.items() if not count),
        "refined_rows": sum(refined.values()),
        "explicit_scaffold_rows": sum(scaffolds.values()),
        "per_book": {book: {"chunks": len(by_book[book]), "refined_rows": refined[book], "explicit_scaffold_rows": scaffolds[book]} for book in sorted(by_book)},
        "known_limitations": [
            "same-model Codex role mesh is correlated, not independent provider evidence",
            "ancient Jewish/Second Temple/rabbinic context remains gap-only without qualification receipt",
            "OT source routes require Hebrew/Aramaic specialist review; NT Greek closure is corpus-level",
            "external reviewer receipt is absent and promotion remains unauthorized",
        ],
        "required_next_gate": "hash-bound external provider or human receipt validated by validate_t521_external_review_receipt.py",
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: report[k] for k in ("book_count", "chunk_count", "refined_rows", "explicit_scaffold_rows", "candidate_only", "non_authorizing", "independence_status")}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
