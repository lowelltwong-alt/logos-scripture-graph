#!/usr/bin/env python3
"""Normalize final Leviticus review tags and revision-2 evidence references."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
CHUNKS = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol" / "book_chunks" / "Lev" / "chunks.jsonl"
EXPECTED = "ee15f8cb82302bc71d7bc4d963e136d7835f993bbbddc0c46ddc8c36dea4cf41"
R2_IDS = {"M7_sol-Lev-012a", "M7_sol-Lev-012b", "M7_sol-Lev-061a", "M7_sol-Lev-061b"}


def main() -> int:
    actual = hashlib.sha256(CHUNKS.read_bytes()).hexdigest()
    if actual != EXPECTED:
        raise SystemExit(f"expected finalized hash {EXPECTED}, found {actual}")
    rows = [json.loads(line) for line in CHUNKS.read_text(encoding="utf-8").splitlines() if line.strip()]
    for row in rows:
        tags = ["review_complete" if tag == "review_pending" else tag for tag in row.get("strong_or_hebrew_tags_used", [])]
        row["strong_or_hebrew_tags_used"] = list(dict.fromkeys(tags))
        if row["decision_id"] in R2_IDS:
            row["boundary_evidence_refs"] = list(dict.fromkeys(row["boundary_evidence_refs"] + [
                "reviews/Lev/primary_r2_hebrew.json",
                "reviews/Lev/primary_r2_literary.json",
                "reviews/Lev/postcheck_r2.json",
            ]))
    with CHUNKS.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"normalized final review metadata for {len(rows)} Leviticus chunks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
