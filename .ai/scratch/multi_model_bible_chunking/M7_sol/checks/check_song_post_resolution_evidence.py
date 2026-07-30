#!/usr/bin/env python3
"""Deterministic, read-only Song post-resolution evidence check."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

MODEL = Path(__file__).resolve().parents[1]
BOOK = "Song"
EXPECTED_SHA = "d09352901c58f0b543f846eb5471a858f7b0154ec1980bd105d7e960f3d325c7"
SIDECARS = ("low_confidence_register.jsonl", "frontier_escalation_queue.jsonl", "atlas_candidate_feed.jsonl")


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
require(len(chunks) == 17, "expected 17 chunks")
require([row["chunk_index_in_book"] for row in chunks] == list(range(1, 18)), "indices not contiguous")
require(all(row.get("confidence") == "low" for row in chunks), "every chunk must remain LOW")
require(all(row.get("candidate_hold_state") == "deferred_human_or_external_ai" for row in chunks), "hold-state mismatch")
require(all(row.get("non_authorizing") is True and row.get("candidate_only") is True for row in chunks), "authority guard mismatch")
require(not any("chapter" in row.get("working_title", "").lower() for row in chunks), "chapter placeholder title found")
require(not any("chapter_scaffold" in json.dumps(row).lower() for row in chunks), "chapter scaffold marker found")

require(len(packets) == 17, "expected 17 packets")
challenges = [c for p in packets for primary in p["primary_reviews"] for c in primary["challenges"]]
challenge_ids = [c["challenge_id"] for c in challenges]
peer_ids = [claim for p in packets for claim in p["peer_crosscheck"]["disputed_claim_ids"]]
responses = [response for p in packets for response in p["sol_resolution"]["challenge_responses"]]
response_ids = [response["challenge_id"] for response in responses]
require(len(challenges) == len(set(challenge_ids)) == 51, "challenge count mismatch")
require(len(peer_ids) == 51 and sorted(peer_ids) == sorted(challenge_ids), "peer parity mismatch")
require(len(responses) == 51 and sorted(response_ids) == sorted(challenge_ids), "author-response parity mismatch")
require(all(p["boss_ruling"]["outcome"] == "retain_larger_low" for p in packets), "boss outcome mismatch")
require(all(p["boss_ruling"]["forced_consensus"] is False for p in packets), "forced consensus found")
appeals = [appeal for p in packets for appeal in p["appeals"]]
require(len(appeals) == 17 and all(a["status"] == "unresolved_append_only" for a in appeals), "appeal mismatch")
require(all(p["final_state"] == "deferred_human_or_external_ai" for p in packets), "final-state mismatch")

require(len(relations) == 6, "relation count mismatch")
require(all(row.get("non_authorizing") is True and row.get("boundary_authority") is False for row in relations), "relation authority mismatch")
sidecar_counts = {}
for name in SIDECARS:
    book_rows = [row for row in read_jsonl(MODEL / name) if row.get("book") == BOOK]
    sidecar_counts[name] = len(book_rows)
    require(len(book_rows) == 17, f"{name} Song count mismatch")

by_id = {row["decision_id"]: row for row in chunks}
expected_spans = {
    "M7_sol-Song-003": "Song.1.9-Song.2.7",
    "M7_sol-Song-004": "Song.2.8-Song.2.17",
    "M7_sol-Song-008": "Song.4.8-Song.5.1",
    "M7_sol-Song-009": "Song.5.2-Song.6.3",
    "M7_sol-Song-011": "Song.6.11-Song.6.13",
    "M7_sol-Song-012": "Song.7.1-Song.7.9",
    "M7_sol-Song-013": "Song.7.10-Song.8.4",
    "M7_sol-Song-014": "Song.8.5-Song.8.7",
    "M7_sol-Song-015": "Song.8.8-Song.8.10",
    "M7_sol-Song-016": "Song.8.11-Song.8.12",
    "M7_sol-Song-017": "Song.8.13-Song.8.14",
}
require(all(by_id[decision_id]["span"] == span for decision_id, span in expected_spans.items()), "hard-zone span mismatch")
for decision_id in expected_spans:
    blob = json.dumps(by_id[decision_id], ensure_ascii=False).lower()
    require("larger" in blob and "deferred" in blob, f"{decision_id} lacks larger-unit/hold defense")
all_blob = json.dumps(chunks, ensure_ascii=False).lower()
require("web 6:13" in all_blob and "mt 7:1" in all_blob, "WEB/MT 6:13/7:1 pressure missing")
require("allegorical/literal" in all_blob and "preferred speaker" in all_blob, "interpretive guards missing")

print(
    json.dumps(
        {
            "verdict": "PASS",
            "chunks_sha256": actual_sha,
            "chunks": 17,
            "low_deferred": 17,
            "review_packets": 17,
            "formal_challenges": 51,
            "peer_disputes": 51,
            "author_responses": 51,
            "boss_rulings_covering_all_challenges": 17,
            "append_only_appeals": 17,
            "decision_relations": 6,
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
