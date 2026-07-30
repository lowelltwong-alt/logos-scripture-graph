#!/usr/bin/env python3
"""Deterministic, read-only Lamentations post-resolution evidence check."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

MODEL = Path(__file__).resolve().parents[1]
BOOK = "Lam"
EXPECTED_SHA = "d95f5186fd07b10865a1e381bf66e2eb637864495b1d28774dd3e84ef460427f"
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
require(len(chunks) == 21, "expected 21 chunks")
require([row["chunk_index_in_book"] for row in chunks] == list(range(1, 22)), "indices not contiguous")
require(all(row.get("confidence") == "low" for row in chunks), "every chunk must remain LOW")
require(all(row.get("candidate_hold_state") == "deferred_human_or_external_ai" for row in chunks), "hold-state mismatch")
require(all(row.get("non_authorizing") is True and row.get("candidate_only") is True for row in chunks), "authority guard mismatch")
require(not any("chapter" in row.get("working_title", "").lower() for row in chunks), "chapter placeholder title found")
require(not any("chapter_scaffold" in json.dumps(row).lower() for row in chunks), "chapter scaffold marker found")

require(len(packets) == 21, "expected 21 review packets")
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
require(len(challenges) == len(set(challenge_ids)) == 63, "challenge count/uniqueness mismatch")
require(len(peer_ids) == 63 and sorted(peer_ids) == sorted(challenge_ids), "peer parity mismatch")
require(len(responses) == 63 and sorted(response_ids) == sorted(challenge_ids), "author-response parity mismatch")
require(all(packet["boss_ruling"]["outcome"] == "retain_larger_low" for packet in packets), "boss outcome mismatch")
require(all(packet["boss_ruling"]["forced_consensus"] is False for packet in packets), "forced consensus found")
appeals = [appeal for packet in packets for appeal in packet["appeals"]]
require(len(appeals) == 21, "appeal count mismatch")
require(all(appeal["status"] == "unresolved_append_only" for appeal in appeals), "appeal status mismatch")
require(all(packet["final_state"] == "deferred_human_or_external_ai" for packet in packets), "final-state mismatch")

require(len(relations) == 6, "relation count mismatch")
require(all(row.get("non_authorizing") is True and row.get("boundary_authority") is False for row in relations), "relation authority mismatch")
sidecar_counts = {}
for name in SIDECARS:
    book_rows = [row for row in read_jsonl(MODEL / name) if row.get("book") == BOOK]
    sidecar_counts[name] = len(book_rows)
    require(len(book_rows) == 21, f"{name} Lamentations count mismatch")

peer=json.loads((MODEL/'reviews'/BOOK/'peer_crosscheck_evidence_v1.json').read_text(encoding='utf-8'))
require(peer.get('frozen_chunks_sha256')==EXPECTED_SHA,'peer frozen SHA mismatch')
require(peer.get('challenge_count')==21 and len(peer.get('challenges',[]))==21,'peer challenge count mismatch')
require(peer.get('preservation_audit',{}).get('official_checker',{}).get('omissions')==0,'peer preservation omissions')
require(peer.get('consensus_policy',{}).get('forced_consensus') is False,'peer forced consensus')
by_id = {row['decision_id']: row for row in chunks}
expected_spans = {
 'M7_sol-Lam-002':'Lam.1.8-Lam.1.11','M7_sol-Lam-003':'Lam.1.12-Lam.1.16','M7_sol-Lam-004':'Lam.1.17-Lam.1.22',
 'M7_sol-Lam-006':'Lam.2.11-Lam.2.17','M7_sol-Lam-007':'Lam.2.18-Lam.2.22',
 'M7_sol-Lam-009':'Lam.3.19-Lam.3.33','M7_sol-Lam-010':'Lam.3.34-Lam.3.39','M7_sol-Lam-011':'Lam.3.40-Lam.3.47','M7_sol-Lam-012':'Lam.3.48-Lam.3.54','M7_sol-Lam-013':'Lam.3.55-Lam.3.63',
 'M7_sol-Lam-016':'Lam.4.11-Lam.4.16','M7_sol-Lam-017':'Lam.4.17-Lam.4.20','M7_sol-Lam-018':'Lam.4.21-Lam.4.22',
 'M7_sol-Lam-019':'Lam.5.1-Lam.5.10','M7_sol-Lam-020':'Lam.5.11-Lam.5.18','M7_sol-Lam-021':'Lam.5.19-Lam.5.22',
}
require(all(by_id[k]['span']==v for k,v in expected_spans.items()),'hard-zone span mismatch')
for decision_id in expected_spans:
 blob=json.dumps(by_id[decision_id],ensure_ascii=False).lower(); require('larger' in blob and 'deferred' in blob,f'{decision_id} lacks larger-unit/hold defense')
all_blob=json.dumps(chunks,ensure_ascii=False).lower()
for token in ('acrostic','pe_ayin','qinah','mt/lxx/dss','jeremiah authorship','divine-agency','proof-texting'):
 require(token in all_blob,f'missing evidence-only guard: {token}')
print(
    json.dumps(
        {
            "verdict": "PASS",
            "chunks_sha256": actual_sha,
            "chunks": 21,
            "low_deferred": 21,
            "review_packets": 21,
            "formal_challenges": 63,
            "peer_disputes": 63,
            "author_responses": 63,
            "boss_rulings_covering_all_challenges": 21,
            "append_only_appeals": 21,
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
