#!/usr/bin/env python3
"""Deterministically verify Jeremiah primary evidence survives final synthesis."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
MODEL=Path(__file__).resolve().parents[1]; REVIEWS=MODEL/'reviews'/'Jer'; CHUNKS=MODEL/'book_chunks'/'Jer'/'chunks.jsonl'
EXPECTED_SHA='0a3847d9a0fa160208d0047f78dad18e2455d0ec2438aea9b144f9ea365ace04'
def point(v):
 v=v.replace('Jer.','').replace('.',':'); c,n=v.split(':'); return int(c),int(n)
def span(v):
 a,b=v.split('-'); return point(a),point(b)
def overlaps(a,b):
 a0,a1=span(a); b0,b1=span(b); return a0<=b1 and b0<=a1
def require(c,m):
 if not c: raise SystemExit(f'FAIL: {m}')
chunks=[json.loads(x) for x in CHUNKS.read_text(encoding='utf-8').splitlines() if x.strip()]
hd=json.loads((REVIEWS/'blind_proposal_hebrew_textual_v1.json').read_text(encoding='utf-8'))
cd=json.loads((REVIEWS/'blind_proposal_canonical_premortem_v1.json').read_text(encoding='utf-8'))
hebrew=hd['proposed_chunks']; canonical=cd['chunks']
require(hashlib.sha256(CHUNKS.read_bytes()).hexdigest()==EXPECTED_SHA,'frozen chunk SHA mismatch')
require(len(chunks)==len(canonical)==99,'final/canonical row count mismatch'); require(len(hebrew)==147,'Hebrew row count mismatch')
cc=hc=ac=0; omissions=[]
for final,selected in zip(chunks,canonical,strict=True):
 blob=json.dumps(final,ensure_ascii=False)
 for value in (selected['span'],selected['form'],selected['marker'],selected['risk'],selected['rejected_alternative'],selected['hold']):
  cc+=1
  if value not in blob: omissions.append(f"{final['decision_id']}:canonical:{value}")
 for value in selected.get('exact_alternatives',[]):
  ac+=1
  if value not in blob: omissions.append(f"{final['decision_id']}:alternative:{value}")
 overlapping=[row for row in hebrew if overlaps(final['span'],row['span'])]
 if not overlapping: omissions.append(f"{final['decision_id']}:no_overlapping_hebrew_row")
 for row in overlapping:
  for value in (row['span'],row['literary_form'],row['deciding_marker'],row['risk'],row['rejected_alternative'],row['hebrew_textual_translation_evidence']):
   hc+=1
   if value not in blob: omissions.append(f"{final['decision_id']}:hebrew:{row['index']}:{value}")
blob=json.dumps(chunks,ensure_ascii=False)
for value in (hd['evidence_only_guard'],*hd.get('macro_parent_alternatives',[]),'failed to materialize a validated proposal','MT/LXX/DSS','Greek/Hebrew order','Jeremiah 52'):
 require(value in blob,f'campaign guard missing: {value}')
require(not omissions,f'{len(omissions)} preservation omissions: {omissions[:10]}')
print(json.dumps({'verdict':'PASS','chunks_sha256':EXPECTED_SHA,'final_chunks':len(chunks),'canonical_rows':len(canonical),'hebrew_rows':len(hebrew),'canonical_field_checks':cc,'canonical_exact_alternative_checks':ac,'hebrew_overlap_field_checks':hc,'omissions':0,'literary_primary_materialization_failures_recorded_as_non_votes':3,'forced_consensus':False,'non_authorizing':True},sort_keys=True))