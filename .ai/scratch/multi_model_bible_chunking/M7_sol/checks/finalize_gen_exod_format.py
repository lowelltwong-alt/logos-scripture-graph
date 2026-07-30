#!/usr/bin/env python3
"""Repair Gen/Exod format and final-state metadata without changing boundaries."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
MODEL = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol"
EXPECTED = {
    "Gen": {
        "chunks": "a22a4638be4dfac0be6e462c5517d53dcccef234fcd6edc5eef7dafbd9502900",
        "packets": "3bac2151ffce2bb2e0d7df4b570a87cd15a7353ddaad6d4d1f3227ab7a7f369f",
    },
    "Exod": {
        "chunks": "d5174fd9ff8b3e5c1db5bb45c5efd06262a88bcfccab5490e887040937159f27",
        "packets": "cb90e6aa32e652f7871b1329589977ebc281b3b9427e8580b23596fe9ecd93a3",
    },
}
HELD_STATES = {"held_lower_confidence", "deferred_human_or_external_ai"}


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", required=True, choices=sorted(EXPECTED))
    args = parser.parse_args()
    book = args.book
    chunks_path = MODEL / "book_chunks" / book / "chunks.jsonl"
    packets_path = MODEL / "reviews" / book / "review_packets.jsonl"
    lineage_path = MODEL / "reviews" / book / "index_normalization.jsonl"

    for label, path in (("chunks", chunks_path), ("packets", packets_path)):
        actual = file_digest(path)
        if actual != EXPECTED[book][label]:
            raise SystemExit(
                f"refusing stale-input rewrite for {book} {label}: "
                f"expected {EXPECTED[book][label]}, found {actual}"
            )

    chunks = read_jsonl(chunks_path)
    packets = read_jsonl(packets_path)
    packet_by_id = {row["decision_id"]: row for row in packets}
    if len(packet_by_id) != len(packets) or set(packet_by_id) != {row["decision_id"] for row in chunks}:
        raise SystemExit(f"{book}: chunks/review-packet decision sets are not one-to-one")

    lineage: list[dict] = []
    for new_index, row in enumerate(chunks, 1):
        decision_id = row["decision_id"]
        old_index = row.get("chunk_index_in_book")
        final_state = packet_by_id[decision_id].get("final_state")
        if final_state == "accepted_candidate":
            row["review_status"] = "candidate_review_complete"
            row.pop("candidate_hold_state", None)
            row.pop("candidate_hold_basis", None)
        elif final_state in HELD_STATES:
            has_appeal = bool(packet_by_id[decision_id].get("appeals"))
            row["review_status"] = "final_deferred_appeal" if has_appeal else "final_deferred_review"
            row["candidate_hold_state"] = "deferred_human_or_external_ai"
            row["candidate_hold_basis"] = "preserved_appeal" if has_appeal else "specialist_or_external_review"
        else:
            raise SystemExit(f"{book} {decision_id}: unsupported packet final_state {final_state!r}")

        row["chunk_index_in_book"] = new_index
        tags = ["review_complete" if tag == "review_pending" else tag for tag in row.get("strong_or_hebrew_tags_used", [])]
        row["strong_or_hebrew_tags_used"] = list(dict.fromkeys(tags))
        if old_index != new_index:
            row["index_normalized_from_pre_audit"] = True
        lineage.append({
            "schema_version": "m7_index_normalization.v1",
            "book": book,
            "decision_id": decision_id,
            "span": row["span"],
            "old_chunk_index_in_book": old_index,
            "new_chunk_index_in_book": new_index,
            "physical_order_authoritative": True,
            "normalized_fields": ["chunk_index_in_book", "review_status", "candidate_hold_state", "candidate_hold_basis", "strong_or_hebrew_tags_used"],
            "boundary_or_decision_id_changed": False,
            "reason": "official_validator_requires_positive_contiguous_integer_indices",
            "non_authorizing": True,
        })

    write_jsonl(chunks_path, chunks)
    write_jsonl(lineage_path, lineage)
    print(
        f"normalized {book}: {len(chunks)} contiguous integer indices, "
        f"{sum(1 for row in chunks if row.get('candidate_hold_state'))} held decisions"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
