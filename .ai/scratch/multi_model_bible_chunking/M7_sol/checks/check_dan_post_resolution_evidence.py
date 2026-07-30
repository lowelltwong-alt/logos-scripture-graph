#!/usr/bin/env python3
"""Deterministic, read-only Daniel post-resolution evidence check."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

MODEL = Path(__file__).resolve().parents[1]
BOOK = "Dan"
EXPECTED_SHA = "5aa00dbfead664fccccaff826a1454531873baa2ebc22a840143b1a1cbac14c1"
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
require(len(chunks) == 35, "expected 35 chunks")
require([row["chunk_index_in_book"] for row in chunks] == list(range(1, 36)), "indices not contiguous")
require(all(row.get("confidence") == "low" for row in chunks), "every chunk must remain LOW")
require(all(row.get("candidate_hold_state") == "deferred_human_or_external_ai" for row in chunks), "hold-state mismatch")
require(all(row.get("non_authorizing") is True and row.get("candidate_only") is True for row in chunks), "authority guard mismatch")
require(not any("chapter" in row.get("working_title", "").lower() for row in chunks), "chapter placeholder title found")
require(not any("chapter_scaffold" in json.dumps(row).lower() for row in chunks), "chapter scaffold marker found")

require(len(packets) == 35, "expected 35 review packets")
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
require(len(challenges) == len(set(challenge_ids)) == 105, "challenge count/uniqueness mismatch")
require(len(peer_ids) == 105 and sorted(peer_ids) == sorted(challenge_ids), "peer parity mismatch")
require(len(responses) == 105 and sorted(response_ids) == sorted(challenge_ids), "author-response parity mismatch")
require(all(packet["boss_ruling"]["outcome"] == "retain_larger_low" for packet in packets), "boss outcome mismatch")
require(all(packet["boss_ruling"]["forced_consensus"] is False for packet in packets), "forced consensus found")
appeals = [appeal for packet in packets for appeal in packet["appeals"]]
require(len(appeals) == 35, "appeal count mismatch")
require(all(appeal["status"] == "unresolved_append_only" for appeal in appeals), "appeal status mismatch")
require(all(packet["final_state"] == "deferred_human_or_external_ai" for packet in packets), "final-state mismatch")

require(len(relations) == 10, "relation count mismatch")
require(all(row.get("non_authorizing") is True and row.get("boundary_authority") is False for row in relations), "relation authority mismatch")
sidecar_counts = {}
for name in SIDECARS:
    book_rows = [row for row in read_jsonl(MODEL / name) if row.get("book") == BOOK]
    sidecar_counts[name] = len(book_rows)
    require(len(book_rows) == 35, f"{name} Daniel count mismatch")

peer=json.loads((MODEL/'reviews'/BOOK/'peer_crosscheck_evidence_v1.json').read_text(encoding='utf-8'))
require(peer.get('frozen_candidate',{}).get('sha256')==EXPECTED_SHA,'peer frozen SHA mismatch')
require(len(peer.get('decision_challenges',[]))==35,'peer challenge count mismatch')
require(len(peer.get('global_hold_challenges',[]))==9,'global challenge group count mismatch')
require(peer.get('deterministic_verification',{}).get('preservation_omissions')==0,'peer preservation omissions')
require(peer.get('forced_consensus') is False and peer.get('non_authorizing') is True,'peer authority guard mismatch')
by_id={row['decision_id']:row for row in chunks}
expected_spans={
 'M7_sol-Dan-002':'Dan.1.8-Dan.1.21','M7_sol-Dan-003':'Dan.2.1-Dan.2.13','M7_sol-Dan-004':'Dan.2.14-Dan.2.23','M7_sol-Dan-005':'Dan.2.24-Dan.2.45','M7_sol-Dan-006':'Dan.2.46-Dan.2.49',
 'M7_sol-Dan-009':'Dan.3.19-Dan.3.30','M7_sol-Dan-010':'Dan.4.1-Dan.4.3','M7_sol-Dan-013':'Dan.4.28-Dan.4.37','M7_sol-Dan-016':'Dan.5.17-Dan.5.31',
 'M7_sol-Dan-020':'Dan.7.1-Dan.7.8','M7_sol-Dan-021':'Dan.7.9-Dan.7.14','M7_sol-Dan-022':'Dan.7.15-Dan.7.28','M7_sol-Dan-024':'Dan.8.15-Dan.8.26','M7_sol-Dan-025':'Dan.8.27-Dan.8.27','M7_sol-Dan-028':'Dan.9.20-Dan.9.27',
 'M7_sol-Dan-029':'Dan.10.1-Dan.10.9','M7_sol-Dan-030':'Dan.10.10-Dan.11.1','M7_sol-Dan-031':'Dan.11.2-Dan.11.20','M7_sol-Dan-032':'Dan.11.21-Dan.11.35','M7_sol-Dan-033':'Dan.11.36-Dan.11.45','M7_sol-Dan-034':'Dan.12.1-Dan.12.4','M7_sol-Dan-035':'Dan.12.5-Dan.12.13'}
require(all(by_id[k]['span']==v for k,v in expected_spans.items()),'hard-zone span mismatch')
for did in expected_spans:
 blob=json.dumps(by_id[did],ensure_ascii=False).lower(); require('larger' in blob and 'deferred' in blob,f'{did} lacks larger-unit/hold defense')
all_blob=json.dumps(chunks,ensure_ascii=False).lower()
for token in ('hebrew_aramaic','bar_enash','theodotion','greek additions','seventy','time formula','proof-texting'):
 require(token in all_blob,f'missing evidence-only guard: {token}')
print(
    json.dumps(
        {
            "verdict": "PASS",
            "chunks_sha256": actual_sha,
            "chunks": 35,
            "low_deferred": 35,
            "review_packets": 35,
            "formal_challenges": 105,
            "peer_disputes": 105,
            "author_responses": 105,
            "boss_rulings_covering_all_challenges": 35,
            "append_only_appeals": 35,
            "decision_relations": 10,
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
