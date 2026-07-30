#!/usr/bin/env python3
"""Audit whole-Bible candidate coverage without treating scaffolds as reviewed maps."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol"
BOOKS = json.loads((MODEL / "state/evidence/book_inventory_candidate_only.json").read_text(encoding="utf-8"))["rows"]

def main() -> int:
    missing = [row["book"] for row in BOOKS if not row["candidate_chunks_present"]]
    reviewed = []
    scaffold = []
    for row in BOOKS:
        path = MODEL / "book_chunks" / row["book"] / "chunks.jsonl"
        if not path.is_file(): continue
        statuses = {json.loads(line).get("review_status") for line in path.read_text(encoding="utf-8").splitlines() if line.strip()}
        if not statuses or not all(("candidate_review_complete" in str(s)) or ("candidate_role_mesh_complete_boss_receipt_only" in str(s)) or ("final_deferred_appeal" in str(s)) or ("final_deferred_review" in str(s)) for s in statuses): scaffold.append(row["book"])
        else: reviewed.append(row["book"])
    result = {"book_count": len(BOOKS), "missing_books": missing, "books_with_candidate_files": len(BOOKS)-len(missing), "books_with_reviewed_or_held_candidates": reviewed, "books_still_scaffold_or_unreviewed": scaffold, "candidate_only": True, "non_authorizing": True, "promotion_qualified": False}
    print(json.dumps(result, sort_keys=True)); return 0 if len(BOOKS)==66 and not missing else 1
if __name__ == "__main__": raise SystemExit(main())




