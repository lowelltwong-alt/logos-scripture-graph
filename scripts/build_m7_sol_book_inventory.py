#!/usr/bin/env python3
"""Build a privacy-safe, candidate-only inventory of all 66 Sol book jobs.

This does not read or emit Scripture text. It records whether a book has
candidate chunks and the review artifacts needed before B01 migration.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol"
BOOKS = ["Gen", "Exod", "Lev", "Num", "Deut", "Josh", "Judg", "Ruth", "1Sam", "2Sam", "1Kgs", "2Kgs", "1Chr", "2Chr", "Ezra", "Neh", "Esth", "Job", "Ps", "Prov", "Eccl", "Song", "Isa", "Jer", "Lam", "Ezek", "Dan", "Hos", "Joel", "Amos", "Obad", "Jonah", "Mic", "Nah", "Hab", "Zeph", "Hag", "Zech", "Mal", "Matt", "Mark", "Luke", "John", "Acts", "Rom", "1Cor", "2Cor", "Gal", "Eph", "Phil", "Col", "1Thess", "2Thess", "1Tim", "2Tim", "Titus", "Phlm", "Heb", "Jas", "1Pet", "2Pet", "1John", "2John", "3John", "Jude", "Rev"]


def main() -> int:
    rows = []
    for book in BOOKS:
        chunks = MODEL / "book_chunks" / book / "chunks.jsonl"
        reviews = MODEL / "reviews" / book
        rows.append({
            "book": book,
            "candidate_chunks_present": chunks.is_file(),
            "candidate_chunk_count": sum(1 for _ in chunks.open(encoding="utf-8")) if chunks.is_file() else 0,
            "review_directory_present": reviews.is_dir(),
            "b01_status": "blocked_pending_typed_evidence",
            "candidate_only": True,
            "non_authorizing": True,
        })
    out = MODEL / "state" / "evidence" / "book_inventory_candidate_only.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {"schema_version": "m7_sol_book_inventory.v1", "book_count": len(rows), "rows": rows, "B01_authorized": False, "non_authorizing": True}
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(out)
    print(json.dumps({"book_count": len(rows), "candidate_chunk_books": sum(row["candidate_chunks_present"] for row in rows), "candidate_chunks": sum(row["candidate_chunk_count"] for row in rows)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
