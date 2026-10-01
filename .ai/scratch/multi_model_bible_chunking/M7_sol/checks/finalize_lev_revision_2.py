#!/usr/bin/env python3
"""Finalize Leviticus review states without changing revision-2 boundaries."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
MODEL = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol"
CHUNKS = MODEL / "book_chunks" / "Lev" / "chunks.jsonl"
LINEAGE = MODEL / "reviews" / "Lev" / "revision_lineage.jsonl"
EXPECTED_FROZEN = "298a01001b885c6b50ae031107234d72bbd9621861a31dbd269a75070fdff5ad"
APPEALS = ["APL-R1-P-LEV-061-01", "APL-R2-H-LEV-061A-01", "APL-R2-L-LEV-061A-01"]


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def main() -> int:
    actual = hashlib.sha256(CHUNKS.read_bytes()).hexdigest()
    if actual != EXPECTED_FROZEN:
        raise SystemExit(f"expected revision-2 freeze {EXPECTED_FROZEN}, found {actual}")
    rows = read_jsonl(CHUNKS)
    for row in rows:
        decision_id = row["decision_id"]
        row["review_status"] = "candidate_review_complete"
        if decision_id in {"M7_sol-Lev-012a", "M7_sol-Lev-012b"}:
            row["parent_hydration_required"] = True
            row["required_parent_span"] = "Lev.7.1-Lev.7.10"
        elif decision_id == "M7_sol-Lev-061a":
            row["review_status"] = "final_deferred_appeal"
            row["candidate_hold_state"] = "deferred_human_or_external_ai"
            row["appeal_ids"] = APPEALS
            row["parent_hydration_required"] = True
            row["required_parent_span"] = "Lev.25.1-Lev.26.46"
            row["required_sibling_decision_id"] = "M7_sol-Lev-061b"
            row["standalone_retrieval_state"] = "withheld_pending_human_or_external_ai"
        elif decision_id == "M7_sol-Lev-061b":
            row["parent_hydration_required"] = True
            row["required_parent_span"] = "Lev.25.1-Lev.26.46"
            row["required_sibling_decision_id"] = "M7_sol-Lev-061a"
    write_jsonl(CHUNKS, rows)

    lineage = read_jsonl(LINEAGE)
    lineage.extend([
        {"schema_version":"m7_revision_finalization.v1","book":"Lev","revision":2,"decision_ids":["M7_sol-Lev-012a","M7_sol-Lev-012b"],"fresh_review_attempt_ids":["lev-r2-hebrew-20260721-t","lev-r2-literary-20260721-u"],"postcheck_attempt_id":"lev-r2-postcheck-20260721-v2","final_state":"accepted_candidate_with_parent_hydration","fresh_reviews_completed":True,"non_authorizing":True},
        {"schema_version":"m7_revision_finalization.v1","book":"Lev","revision":2,"decision_ids":["M7_sol-Lev-061a","M7_sol-Lev-061b"],"fresh_review_attempt_ids":["lev-r2-hebrew-20260721-t","lev-r2-literary-20260721-u"],"postcheck_attempt_id":"lev-r2-postcheck-20260721-v2","appeal_ids":APPEALS,"final_states":{"M7_sol-Lev-061a":"deferred_human_or_external_ai","M7_sol-Lev-061b":"accepted_candidate_with_parent_hydration"},"fresh_reviews_completed":True,"human_question":"Should Lev.26.1-2 be independently retrievable with mandatory parent and sibling hydration, or remain an internal boundary never surfaced standalone?","non_authorizing":True},
    ])
    write_jsonl(LINEAGE, lineage)
    print(f"finalized {len(rows)} Leviticus chunks; held M7_sol-Lev-061a with {len(APPEALS)} appeals")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
