#!/usr/bin/env python3
"""Normalize one book's uncertainty sidecars under one exclusive atomic write lock."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
MODEL = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol"
LOW_CONFIDENCE = {"low", "medium_low"}
SIDECARS = (
    "low_confidence_register.jsonl",
    "frontier_escalation_queue.jsonl",
    "atlas_candidate_feed.jsonl",
)
LOCK = MODEL / "runtime" / "uncertainty_sidecar_write.lock"


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_jsonl_atomic(path: Path, rows: list[dict]) -> None:
    temporary = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    try:
        with temporary.open("x", encoding="utf-8", newline="\n") as handle:
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)

def normalize_book(book: str) -> None:
    chunks = read_jsonl(MODEL / "book_chunks" / book / "chunks.jsonl")
    packets = read_jsonl(MODEL / "reviews" / book / "review_packets.jsonl")
    packet_by_id = {row["decision_id"]: row for row in packets}
    expected = {
        row["decision_id"]: row
        for row in chunks
        if row.get("confidence") in LOW_CONFIDENCE
    }
    if set(expected) - set(packet_by_id):
        raise SystemExit(f"{book}: low-confidence chunks lack review packets")

    for filename in SIDECARS:
        path = MODEL / filename
        all_rows = read_jsonl(path)
        other_rows = [row for row in all_rows if row.get("book") != book]
        current_by_id = {
            row.get("chunk_decision_id"): row
            for row in all_rows
            if row.get("book") == book and row.get("chunk_decision_id") in expected
        }
        missing = sorted(set(expected) - set(current_by_id))
        if missing:
            raise SystemExit(f"{book} {filename}: missing active low-confidence rows {missing}")

        normalized: list[dict] = []
        for decision_id, chunk in expected.items():
            row = current_by_id[decision_id]
            packet = packet_by_id[decision_id]
            held = packet.get("final_state") != "accepted_candidate"
            has_appeals = bool(packet.get("appeals"))
            row["span"] = chunk["span"]
            row["confidence"] = chunk["confidence"]
            row["review_packet_final_state"] = packet.get("final_state")
            row["chunk_review_status"] = chunk.get("review_status")
            if held:
                row["candidate_hold_state"] = "deferred_human_or_external_ai"
            else:
                row.pop("candidate_hold_state", None)

            if filename == "low_confidence_register.jsonl":
                if has_appeals:
                    row["appeal_status"] = "deferred_human_or_external_ai"
                elif held:
                    row["appeal_status"] = "no_appeal_specialist_or_external_review_hold"
                else:
                    row["appeal_status"] = "candidate_review_complete_specialist_followup_optional"
            elif filename == "frontier_escalation_queue.jsonl":
                row["disposition"] = (
                    "deferred_human_or_external_ai"
                    if held
                    else "specialist_followup_optional_candidate_review_complete"
                )
            else:
                row["proposed_atlas_action"] = (
                    "withhold_pending_human_or_external_ai"
                    if held
                    else "consider_only_review_complete"
                )
            normalized.append(row)

        write_jsonl_atomic(path, other_rows + normalized)
        removed = sum(1 for row in all_rows if row.get("book") == book) - len(normalized)
        print(f"normalized {filename}: {book} rows={len(normalized)} retired_orphans_removed={removed}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", required=True)
    args = parser.parse_args()
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise SystemExit(
            f"shared sidecar writer lock exists at {LOCK.relative_to(ROOT).as_posix()}; "
            "serialize book normalizers and investigate a stale lock before retrying"
        )
    os.close(descriptor)
    try:
        normalize_book(args.book)
    finally:
        LOCK.unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())