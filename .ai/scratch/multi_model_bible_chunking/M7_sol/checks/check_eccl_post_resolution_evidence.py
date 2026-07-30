#!/usr/bin/env python3
"""Deterministic, read-only Ecclesiastes post-resolution evidence check."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

MODEL = Path(__file__).resolve().parents[1]
BOOK = "Eccl"
EXPECTED_SHA = "a62fb2971f428a498caf2f2de7929e76eb87c5bd3d9fb5186182da0faa8153b8"
SIDECARS = (
    "low_confidence_register.jsonl",
    "frontier_escalation_queue.jsonl",
    "atlas_candidate_feed.jsonl",
)


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


chunks_path = MODEL / "book_chunks" / BOOK / "chunks.jsonl"
packets_path = MODEL / "reviews" / BOOK / "review_packets.jsonl"
relations_path = MODEL / "reviews" / BOOK / "decision_relations.jsonl"
chunks = read_jsonl(chunks_path)
packets = read_jsonl(packets_path)
relations = read_jsonl(relations_path)
actual_sha = hashlib.sha256(chunks_path.read_bytes()).hexdigest()

require(actual_sha == EXPECTED_SHA, "chunk SHA mismatch")
require(len(chunks) == 29, "expected 29 chunks")
require([row["chunk_index_in_book"] for row in chunks] == list(range(1, 30)), "indices not contiguous")
require(all(row.get("confidence") == "low" for row in chunks), "every chunk must remain LOW")
require(all(row.get("candidate_hold_state") == "deferred_human_or_external_ai" for row in chunks), "hold-state mismatch")
require(all(row.get("non_authorizing") is True and row.get("candidate_only") is True for row in chunks), "authority guard mismatch")
require(not any("chapter" in row.get("working_title", "").lower() for row in chunks), "chapter placeholder title found")
require(not any("chapter_scaffold" in json.dumps(row).lower() for row in chunks), "chapter scaffold marker found")

require(len(packets) == 29, "expected 29 review packets")
challenges = [
    challenge
    for packet in packets
    for primary in packet["primary_reviews"]
    for challenge in primary["challenges"]
]
challenge_ids = [challenge["challenge_id"] for challenge in challenges]
peer_ids = [claim for packet in packets for claim in packet["peer_crosscheck"]["disputed_claim_ids"]]
responses = [response for packet in packets for response in packet["sol_resolution"]["challenge_responses"]]
response_ids = [response["challenge_id"] for response in responses]
require(len(challenges) == len(set(challenge_ids)) == 87, "challenge count/uniqueness mismatch")
require(len(peer_ids) == 87 and sorted(peer_ids) == sorted(challenge_ids), "peer parity mismatch")
require(len(responses) == 87 and sorted(response_ids) == sorted(challenge_ids), "author-response parity mismatch")
require(all(packet["boss_ruling"]["outcome"] == "retain_larger_low" for packet in packets), "boss outcome mismatch")
require(all(packet["boss_ruling"]["forced_consensus"] is False for packet in packets), "forced consensus found")
appeals = [appeal for packet in packets for appeal in packet["appeals"]]
require(len(appeals) == 29, "appeal count mismatch")
require(all(appeal["status"] == "unresolved_append_only" for appeal in appeals), "appeal status mismatch")
require(all(packet["final_state"] == "deferred_human_or_external_ai" for packet in packets), "final-state mismatch")

require(len(relations) == 7, "relation count mismatch")
require(all(row.get("non_authorizing") is True and row.get("boundary_authority") is False for row in relations), "relation authority mismatch")
sidecar_counts = {}
for name in SIDECARS:
    book_rows = [row for row in read_jsonl(MODEL / name) if row.get("book") == BOOK]
    sidecar_counts[name] = len(book_rows)
    require(len(book_rows) == 29, f"{name} Ecclesiastes count mismatch")

by_id = {row["decision_id"]: row for row in chunks}
expected_spans = {
    "M7_sol-Eccl-011": "Eccl.4.4-Eccl.4.12",
    "M7_sol-Eccl-014": "Eccl.5.8-Eccl.5.17",
    "M7_sol-Eccl-015": "Eccl.5.18-Eccl.6.6",
    "M7_sol-Eccl-021": "Eccl.8.10-Eccl.8.17",
    "M7_sol-Eccl-023": "Eccl.9.11-Eccl.9.18",
    "M7_sol-Eccl-028": "Eccl.11.7-Eccl.12.8",
    "M7_sol-Eccl-029": "Eccl.12.9-Eccl.12.14",
}
require(all(by_id[decision_id]["span"] == span for decision_id, span in expected_spans.items()), "hard-zone span mismatch")
for decision_id in expected_spans:
    blob = json.dumps(by_id[decision_id], ensure_ascii=False).lower()
    require("larger" in blob and "deferred" in blob, f"{decision_id} lacks larger-unit/hold defense")
require("web 5:1" in json.dumps(chunks, ensure_ascii=False).lower(), "WEB/MT 5:1 pressure missing")
require("epilogue" in json.dumps(by_id["M7_sol-Eccl-029"], ensure_ascii=False).lower(), "epilogue defense missing")

print(
    json.dumps(
        {
            "verdict": "PASS",
            "chunks_sha256": actual_sha,
            "chunks": 29,
            "low_deferred": 29,
            "review_packets": 29,
            "formal_challenges": 87,
            "peer_disputes": 87,
            "author_responses": 87,
            "boss_rulings_covering_all_challenges": 29,
            "append_only_appeals": 29,
            "decision_relations": 7,
            "sidecar_counts": sidecar_counts,
            "hard_zone_spans": expected_spans,
            "chapter_placeholder_markers": 0,
            "forced_consensus": False,
            "non_authorizing": True,
        },
        ensure_ascii=False,
        sort_keys=True,
    )
)
