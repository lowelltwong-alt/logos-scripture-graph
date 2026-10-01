#!/usr/bin/env python3
"""Deterministic, read-only Isaiah post-resolution evidence check."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

MODEL = Path(__file__).resolve().parents[1]
BOOK = "Isa"
EXPECTED_SHA = "615feb5682bcfc4a9b2b44ec5753a76191e63e83f1e4cd37ff2a5a382a424376"
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
require(len(chunks) == 88, "expected 88 chunks")
require([row["chunk_index_in_book"] for row in chunks] == list(range(1, 89)), "indices not contiguous")
require(all(row.get("confidence") == "low" for row in chunks), "every chunk must remain LOW")
require(all(row.get("candidate_hold_state") == "deferred_human_or_external_ai" for row in chunks), "hold-state mismatch")
require(all(row.get("non_authorizing") is True and row.get("candidate_only") is True for row in chunks), "authority guard mismatch")
require(not any("chapter" in row.get("working_title", "").lower() for row in chunks), "chapter placeholder title found")
require(not any("chapter_scaffold" in json.dumps(row).lower() for row in chunks), "chapter scaffold marker found")

require(len(packets) == 88, "expected 88 review packets")
challenges = [c for p in packets for primary in p["primary_reviews"] for c in primary["challenges"]]
challenge_ids = [c["challenge_id"] for c in challenges]
peer_ids = [claim for p in packets for claim in p["peer_crosscheck"]["disputed_claim_ids"]]
responses = [response for p in packets for response in p["sol_resolution"]["challenge_responses"]]
response_ids = [response["challenge_id"] for response in responses]
require(len(challenges) == len(set(challenge_ids)) == 264, "challenge count mismatch")
require(len(peer_ids) == 264 and sorted(peer_ids) == sorted(challenge_ids), "peer parity mismatch")
require(len(responses) == 264 and sorted(response_ids) == sorted(challenge_ids), "author-response parity mismatch")
require(all(p["boss_ruling"]["outcome"] == "retain_larger_low" for p in packets), "boss outcome mismatch")
require(all(p["boss_ruling"]["forced_consensus"] is False for p in packets), "forced consensus found")
appeals = [appeal for p in packets for appeal in p["appeals"]]
require(len(appeals) == 88 and all(a["status"] == "unresolved_append_only" for a in appeals), "appeal mismatch")
require(all(p["final_state"] == "deferred_human_or_external_ai" for p in packets), "final-state mismatch")

require(len(relations) == 11, "relation count mismatch")
require(all(row.get("non_authorizing") is True and row.get("boundary_authority") is False for row in relations), "relation authority mismatch")
sidecar_counts = {}
for name in SIDECARS:
    book_rows = [row for row in read_jsonl(MODEL / name) if row.get("book") == BOOK]
    sidecar_counts[name] = len(book_rows)
    require(len(book_rows) == 88, f"{name} Isaiah count mismatch")

by_id = {row["decision_id"]: row for row in chunks}
expected_spans = {
    "M7_sol-Isa-012": "Isa.7.1-Isa.7.17",
    "M7_sol-Isa-018": "Isa.12.1-Isa.12.6",
    "M7_sol-Isa-019": "Isa.13.1-Isa.14.23",
    "M7_sol-Isa-032": "Isa.23.1-Isa.23.18",
    "M7_sol-Isa-033": "Isa.24.1-Isa.25.5",
    "M7_sol-Isa-036": "Isa.27.2-Isa.27.13",
    "M7_sol-Isa-046": "Isa.34.1-Isa.35.10",
    "M7_sol-Isa-047": "Isa.36.1-Isa.37.7",
    "M7_sol-Isa-050": "Isa.39.1-Isa.39.8",
    "M7_sol-Isa-051": "Isa.40.1-Isa.40.11",
    "M7_sol-Isa-063": "Isa.48.1-Isa.48.22",
    "M7_sol-Isa-064": "Isa.49.1-Isa.49.13",
    "M7_sol-Isa-070": "Isa.52.13-Isa.53.12",
    "M7_sol-Isa-072": "Isa.55.1-Isa.55.13",
    "M7_sol-Isa-073": "Isa.56.1-Isa.56.8",
    "M7_sol-Isa-078": "Isa.59.16-Isa.59.21",
    "M7_sol-Isa-079": "Isa.60.1-Isa.60.22",
    "M7_sol-Isa-088": "Isa.66.17-Isa.66.24",
}
require(all(by_id[decision_id]["span"] == span for decision_id, span in expected_spans.items()), "hard-zone span mismatch")
for decision_id in expected_spans:
    blob = json.dumps(by_id[decision_id], ensure_ascii=False).lower()
    require("larger" in blob and "deferred" in blob, f"{decision_id} lacks larger-unit/hold defense")
all_blob = json.dumps(chunks, ensure_ascii=False).lower()
for token in ("mt_lxx_dss", "servant identity", "authorship/strata", "claim fulfillment"):
    require(token in all_blob, f"missing evidence-only guard: {token}")

print(
    json.dumps(
        {
            "verdict": "PASS",
            "chunks_sha256": actual_sha,
            "chunks": 88,
            "low_deferred": 88,
            "review_packets": 88,
            "formal_challenges": 264,
            "peer_disputes": 264,
            "author_responses": 264,
            "boss_rulings_covering_all_challenges": 88,
            "append_only_appeals": 88,
            "decision_relations": 11,
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
