#!/usr/bin/env python3
"""Deterministic, read-only Proverbs post-resolution evidence check."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

MODEL = Path(__file__).resolve().parents[1]
BOOK = "Prov"
EXPECTED_SHA = "9a10edf0d4928842493bfa34430d06d93671ad2ac4e57421d10c1601daa4c2d0"
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
require(actual_sha == EXPECTED_SHA, f"chunk SHA {actual_sha} != {EXPECTED_SHA}")
require(len(chunks) == 36, "expected 36 chunks")
require([row["chunk_index_in_book"] for row in chunks] == list(range(1, 37)), "indices not contiguous")
require(all(row.get("confidence") == "low" for row in chunks), "every chunk must remain LOW")
require(all(row.get("candidate_hold_state") == "deferred_human_or_external_ai" for row in chunks), "hold-state mismatch")
require(all(row.get("non_authorizing") is True and row.get("candidate_only") is True for row in chunks), "authority guard mismatch")
require(not any("chapter" in row.get("working_title", "").lower() for row in chunks), "chapter placeholder title found")
require(not any("chapter_scaffold" in json.dumps(row).lower() for row in chunks), "chapter scaffold marker found")

require(len(packets) == 36, "expected 36 review packets")
challenges = [
    challenge
    for packet in packets
    for primary in packet["primary_reviews"]
    for challenge in primary["challenges"]
]
challenge_ids = [challenge["challenge_id"] for challenge in challenges]
peer_ids = [claim_id for packet in packets for claim_id in packet["peer_crosscheck"]["disputed_claim_ids"]]
responses = [
    response
    for packet in packets
    for response in packet["sol_resolution"]["challenge_responses"]
]
response_ids = [response["challenge_id"] for response in responses]
require(len(challenges) == len(set(challenge_ids)) == 108, "challenge count/uniqueness mismatch")
require(len(peer_ids) == 108 and sorted(peer_ids) == sorted(challenge_ids), "peer-dispute parity mismatch")
require(len(responses) == 108 and sorted(response_ids) == sorted(challenge_ids), "author-response parity mismatch")
require(all(packet["boss_ruling"]["outcome"] == "retain_larger_low" for packet in packets), "boss outcome mismatch")
require(all(packet["boss_ruling"]["forced_consensus"] is False for packet in packets), "forced consensus found")
appeals = [appeal for packet in packets for appeal in packet["appeals"]]
require(len(appeals) == 36, "appeal count mismatch")
require(all(appeal["status"] == "unresolved_append_only" for appeal in appeals), "appeal status mismatch")
require(all(packet["final_state"] == "deferred_human_or_external_ai" for packet in packets), "final-state mismatch")

require(len(relations) == 6, "relation count mismatch")
require(all(row.get("non_authorizing") is True and row.get("boundary_authority") is False for row in relations), "relation authority mismatch")
sidecar_counts = {}
for name in SIDECARS:
    book_rows = [row for row in read_jsonl(MODEL / name) if row.get("book") == BOOK]
    sidecar_counts[name] = len(book_rows)
    require(len(book_rows) == 36, f"{name} Proverbs count mismatch")

by_id = {row["decision_id"]: row for row in chunks}
expected_spans = {
    "M7_sol-Prov-021": "Prov.10.1-Prov.22.16",
    "M7_sol-Prov-022": "Prov.22.17-Prov.24.22",
    "M7_sol-Prov-024": "Prov.25.1-Prov.29.27",
    "M7_sol-Prov-025": "Prov.30.1-Prov.30.9",
    "M7_sol-Prov-026": "Prov.30.10-Prov.30.10",
    "M7_sol-Prov-027": "Prov.30.11-Prov.30.14",
    "M7_sol-Prov-028": "Prov.30.15-Prov.30.16",
    "M7_sol-Prov-029": "Prov.30.17-Prov.30.17",
    "M7_sol-Prov-030": "Prov.30.18-Prov.30.20",
    "M7_sol-Prov-031": "Prov.30.21-Prov.30.23",
    "M7_sol-Prov-032": "Prov.30.24-Prov.30.28",
    "M7_sol-Prov-033": "Prov.30.29-Prov.30.31",
    "M7_sol-Prov-034": "Prov.30.32-Prov.30.33",
    "M7_sol-Prov-035": "Prov.31.1-Prov.31.9",
    "M7_sol-Prov-036": "Prov.31.10-Prov.31.31",
}
require(all(by_id[decision_id]["span"] == span for decision_id, span in expected_spans.items()), "hard-zone span mismatch")
for decision_id in ("M7_sol-Prov-021", "M7_sol-Prov-022", "M7_sol-Prov-024"):
    blob = json.dumps(by_id[decision_id], ensure_ascii=False).lower()
    require("collection" in blob and "larger" in blob and "superscription" in blob, f"{decision_id} lacks collection-parent defense")
require("alphabetic" in json.dumps(by_id["M7_sol-Prov-036"]).lower(), "D036 lacks alphabetic-poem defense")

print(
    json.dumps(
        {
            "verdict": "PASS",
            "chunks_sha256": actual_sha,
            "chunks": len(chunks),
            "low_deferred": 36,
            "review_packets": len(packets),
            "formal_challenges": len(challenges),
            "peer_disputes": len(peer_ids),
            "author_responses": len(responses),
            "boss_rulings_covering_all_challenges": 36,
            "append_only_appeals": len(appeals),
            "decision_relations": len(relations),
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
