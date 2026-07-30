#!/usr/bin/env python3
"""Normalize the one noncanonical Leviticus confidence label without changing spans."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
CHUNKS = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol" / "book_chunks" / "Lev" / "chunks.jsonl"
EXPECTED = "720354c8dc684a36cd962fc0822d397235804f123548184bade7173c510c23e6"


def main() -> int:
    actual = hashlib.sha256(CHUNKS.read_bytes()).hexdigest()
    if actual != EXPECTED:
        raise SystemExit(f"expected final Leviticus hash {EXPECTED}, found {actual}")
    rows = [json.loads(line) for line in CHUNKS.read_text(encoding="utf-8").splitlines() if line.strip()]
    changed = []
    for row in rows:
        if row.get("confidence") == "medium_high":
            row["confidence"] = "medium"
            row["confidence_normalization"] = "medium_high_review_language_normalized_to_protocol_medium"
            changed.append(row["decision_id"])
    if changed != ["M7_sol-Lev-012a"]:
        raise SystemExit(f"expected only M7_sol-Lev-012a normalization, found {changed}")
    with CHUNKS.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
    print("normalized M7_sol-Lev-012a confidence medium_high -> medium")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
