#!/usr/bin/env python3
"""Deterministic, read-only Ezekiel post-resolution evidence check."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

MODEL = Path(__file__).resolve().parents[1]
BOOK = "Ezek"
EXPECTED_SHA = "b91240561f69c3fecea61523ed621d458c43e77665020c63080b35d1f270fa46"
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
require(len(chunks) == 89, "expected 89 chunks")
require([row["chunk_index_in_book"] for row in chunks] == list(range(1, 90)), "indices not contiguous")
require(all(row.get("confidence") == "low" for row in chunks), "every chunk must remain LOW")
require(all(row.get("candidate_hold_state") == "deferred_human_or_external_ai" for row in chunks), "hold-state mismatch")
require(all(row.get("non_authorizing") is True and row.get("candidate_only") is True for row in chunks), "authority guard mismatch")
require(not any("chapter" in row.get("working_title", "").lower() for row in chunks), "chapter placeholder title found")
require(not any("chapter_scaffold" in json.dumps(row).lower() for row in chunks), "chapter scaffold marker found")

require(len(packets) == 89, "expected 89 review packets")
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
require(len(challenges) == len(set(challenge_ids)) == 178, "challenge count/uniqueness mismatch")
require(len(peer_ids) == 178 and sorted(peer_ids) == sorted(challenge_ids), "peer parity mismatch")
require(len(responses) == 178 and sorted(response_ids) == sorted(challenge_ids), "author-response parity mismatch")
require(all(packet["boss_ruling"]["outcome"] == "retain_larger_low" for packet in packets), "boss outcome mismatch")
require(all(packet["boss_ruling"]["forced_consensus"] is False for packet in packets), "forced consensus found")
appeals = [appeal for packet in packets for appeal in packet["appeals"]]
require(len(appeals) == 89, "appeal count mismatch")
require(all(appeal["status"] == "unresolved_append_only" for appeal in appeals), "appeal status mismatch")
require(all(packet["final_state"] == "deferred_human_or_external_ai" for packet in packets), "final-state mismatch")

require(len(relations) == 12, "relation count mismatch")
require(all(row.get("non_authorizing") is True and row.get("boundary_authority") is False for row in relations), "relation authority mismatch")
sidecar_counts = {}
for name in SIDECARS:
    book_rows = [row for row in read_jsonl(MODEL / name) if row.get("book") == BOOK]
    sidecar_counts[name] = len(book_rows)
    require(len(book_rows) == 89, f"{name} Ezekiel count mismatch")

peer=json.loads((MODEL/'reviews'/BOOK/'peer_crosscheck_evidence_v1.json').read_text(encoding='utf-8'))
hebrew=json.loads((MODEL/'reviews'/BOOK/'hebrew_textual_audit_v1.json').read_text(encoding='utf-8'))
require(peer.get('frozen_chunks_sha256')==EXPECTED_SHA,'peer frozen SHA mismatch')
require(peer.get('challenge_count')==89 and len(peer.get('challenges',[]))==89,'peer challenge count mismatch')
require(peer.get('global_hold_challenge_count')==12 and len(peer.get('global_hold_challenges',[]))==12,'global hold challenge count mismatch')
require(peer.get('preservation_audit',{}).get('official_checker',{}).get('omissions')==0,'peer preservation omissions')
require(peer.get('consensus_policy',{}).get('forced_consensus') is False,'peer forced consensus')
require(hebrew.get('final_map_sha256')==EXPECTED_SHA and len(hebrew.get('units',[]))==89,'Hebrew audit lifecycle pin mismatch')
by_id={row['decision_id']:row for row in chunks}
expected_spans={
 'M7_sol-Ezek-001':'Ezek.1.1-Ezek.1.28','M7_sol-Ezek-004':'Ezek.3.16-Ezek.3.27',
 'M7_sol-Ezek-009':'Ezek.8.1-Ezek.8.18','M7_sol-Ezek-013':'Ezek.11.14-Ezek.11.25',
 'M7_sol-Ezek-021':'Ezek.16.1-Ezek.16.14','M7_sol-Ezek-022':'Ezek.16.15-Ezek.16.43','M7_sol-Ezek-023':'Ezek.16.44-Ezek.16.63',
 'M7_sol-Ezek-029':'Ezek.20.45-Ezek.21.7','M7_sol-Ezek-035':'Ezek.23.1-Ezek.23.49','M7_sol-Ezek-037':'Ezek.24.15-Ezek.24.27',
 'M7_sol-Ezek-043':'Ezek.27.1-Ezek.27.36','M7_sol-Ezek-045':'Ezek.28.11-Ezek.28.19','M7_sol-Ezek-055':'Ezek.33.21-Ezek.33.33',
 'M7_sol-Ezek-060':'Ezek.36.16-Ezek.36.38','M7_sol-Ezek-061':'Ezek.37.1-Ezek.37.14','M7_sol-Ezek-063':'Ezek.38.1-Ezek.38.23','M7_sol-Ezek-065':'Ezek.39.21-Ezek.39.29',
 'M7_sol-Ezek-071':'Ezek.40.48-Ezek.41.4','M7_sol-Ezek-076':'Ezek.43.1-Ezek.43.12','M7_sol-Ezek-082':'Ezek.45.18-Ezek.46.15','M7_sol-Ezek-085':'Ezek.47.1-Ezek.47.12','M7_sol-Ezek-089':'Ezek.48.23-Ezek.48.35'}
require(all(by_id[k]['span']==v for k,v in expected_spans.items()),'hard-zone span mismatch')
for did in expected_spans:
 blob=json.dumps(by_id[did],ensure_ascii=False).lower(); require('larger' in blob and 'deferred' in blob,f'{did} lacks larger-unit/hold defense')
all_blob=json.dumps(chunks,ensure_ascii=False).lower()
for token in ('p967','ben_adam','ruach','gog','divine-agency','sexualized','measurement','proof-texting'):
 require(token in all_blob,f'missing evidence-only guard: {token}')
print(
    json.dumps(
        {
            "verdict": "PASS",
            "chunks_sha256": actual_sha,
            "chunks": 89,
            "low_deferred": 89,
            "review_packets": 89,
            "formal_challenges": 178,
            "peer_disputes": 178,
            "author_responses": 178,
            "boss_rulings_covering_all_challenges": 89,
            "append_only_appeals": 89,
            "decision_relations": 12,
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
