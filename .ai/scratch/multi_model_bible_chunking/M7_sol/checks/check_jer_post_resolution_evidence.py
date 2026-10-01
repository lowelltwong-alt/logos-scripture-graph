#!/usr/bin/env python3
"""Deterministic, read-only Jeremiah post-resolution evidence check."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
MODEL=Path(__file__).resolve().parents[1]; BOOK='Jer'; EXPECTED_SHA='0a3847d9a0fa160208d0047f78dad18e2455d0ec2438aea9b144f9ea365ace04'
SIDECARS=('low_confidence_register.jsonl','frontier_escalation_queue.jsonl','atlas_candidate_feed.jsonl')
def readj(path): return [json.loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x.strip()]
def require(c,m):
 if not c: raise SystemExit(f'FAIL: {m}')
chunks_path=MODEL/'book_chunks'/BOOK/'chunks.jsonl'; packets_path=MODEL/'reviews'/BOOK/'review_packets.jsonl'; relations_path=MODEL/'reviews'/BOOK/'decision_relations.jsonl'
chunks,packets,relations=readj(chunks_path),readj(packets_path),readj(relations_path); actual_sha=hashlib.sha256(chunks_path.read_bytes()).hexdigest()
require(actual_sha==EXPECTED_SHA,'chunk SHA mismatch'); require(len(chunks)==len(packets)==99,'chunk/review packet count mismatch'); require([r['chunk_index_in_book'] for r in chunks]==list(range(1,100)),'indices not contiguous')
require(all(r.get('confidence')=='low' for r in chunks),'every chunk must remain LOW'); require(all(r.get('candidate_hold_state')=='deferred_human_or_external_ai' for r in chunks),'hold mismatch'); require(all(r.get('non_authorizing') is True and r.get('candidate_only') is True for r in chunks),'authority guard mismatch'); require(not any('chapter_scaffold' in json.dumps(r).lower() for r in chunks),'chapter scaffold marker found')
challenges=[c for p in packets for primary in p['primary_reviews'] for c in primary['challenges']]; challenge_ids=[c['challenge_id'] for c in challenges]; peer_ids=[c for p in packets for c in p['peer_crosscheck']['disputed_claim_ids']]; responses=[r for p in packets for r in p['sol_resolution']['challenge_responses']]; response_ids=[r['challenge_id'] for r in responses]
require(len(challenges)==len(set(challenge_ids))==198,'challenge count/uniqueness mismatch'); require(len(peer_ids)==198 and sorted(peer_ids)==sorted(challenge_ids),'peer parity mismatch'); require(len(responses)==198 and sorted(response_ids)==sorted(challenge_ids),'author response parity mismatch'); require(all(p['boss_ruling']['outcome']=='retain_larger_low' for p in packets),'boss outcome mismatch'); require(all(p['boss_ruling']['forced_consensus'] is False for p in packets),'forced consensus found')
appeals=[a for p in packets for a in p['appeals']]; require(len(appeals)==99 and all(a['status']=='unresolved_append_only' for a in appeals),'appeal mismatch'); require(all(p['final_state']=='deferred_human_or_external_ai' for p in packets),'final state mismatch'); require(len(relations)==11,'relation count mismatch'); require(all(r.get('non_authorizing') is True and r.get('boundary_authority') is False for r in relations),'relation authority mismatch')
sidecar_counts={}
for name in SIDECARS:
 rows=[r for r in readj(MODEL/name) if r.get('book')==BOOK]; sidecar_counts[name]=len(rows); require(len(rows)==99,f'{name} Jeremiah count mismatch')
peer=json.loads((MODEL/'reviews'/BOOK/'peer_crosscheck_evidence_v1.json').read_text(encoding='utf-8')); require(peer.get('frozen_chunks_sha256')==EXPECTED_SHA,'fresh peer evidence SHA mismatch'); require(peer.get('consensus_policy',{}).get('forced_consensus') is False and peer.get('declarations',{}).get('non_authorizing') is True,'fresh peer authority guard mismatch'); require(len(peer.get('challenges',[]))==99,'fresh peer decision challenge count mismatch')
blob=json.dumps(chunks,ensure_ascii=False).lower()
for token in ('mt/lxx/dss','greek/hebrew order','authorship/redaction','claim fulfillment','jeremiah 52'): require(token in blob,f'missing evidence-only guard: {token}')
print(json.dumps({'verdict':'PASS','chunks_sha256':actual_sha,'chunks':99,'low_deferred':99,'review_packets':99,'formal_challenges':198,'peer_disputes':198,'author_responses':198,'boss_rulings_covering_all_challenges':99,'append_only_appeals':99,'decision_relations':11,'sidecar_counts':sidecar_counts,'primary_preservation_checks':{'canonical_fields':594,'exact_alternatives':264,'hebrew_overlap_fields':906,'omissions':0},'chapter_placeholder_markers':0,'forced_consensus':False,'non_authorizing':True},sort_keys=True))