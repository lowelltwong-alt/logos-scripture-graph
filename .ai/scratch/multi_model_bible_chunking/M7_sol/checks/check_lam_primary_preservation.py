#!/usr/bin/env python3
"""Verify every blind Lamentations proposal field survives synthesis."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
MODEL=Path(__file__).resolve().parents[1]; REV=MODEL/'reviews'/'Lam'; CHUNKS=MODEL/'book_chunks'/'Lam'/'chunks.jsonl'; SHA='d95f5186fd07b10865a1e381bf66e2eb637864495b1d28774dd3e84ef460427f'
def pt(v):
 v=v.replace('Lam.','').replace('.',':'); c,n=v.split(':'); return int(c),int(n)
def sp(v):
 a,b=v.split('-'); return pt(a),pt(b)
def overlap(a,b):
 a0,a1=sp(a); b0,b1=sp(b); return a0<=b1 and b0<=a1
def req(c,m):
 if not c: raise SystemExit('FAIL: '+m)
rows=[json.loads(x) for x in CHUNKS.read_text(encoding='utf-8').splitlines() if x.strip()]
h=json.loads((REV/'blind_proposal_hebrew_textual_v1.json').read_text(encoding='utf-8')); l=json.loads((REV/'blind_proposal_literary_v1.json').read_text(encoding='utf-8')); c=json.loads((REV/'blind_proposal_canonical_premortem_v1.json').read_text(encoding='utf-8'))
hr,lr,cr=h['units'],l['chunks'],c['chunks']; req(hashlib.sha256(CHUNKS.read_bytes()).hexdigest()==SHA,'SHA'); req((len(rows),len(hr),len(lr),len(cr))==(21,22,22,21),'counts')
hc=lc=cc=ac=0; missing=[]
for final,selected in zip(rows,cr,strict=True):
 blob=json.dumps(final,ensure_ascii=False)
 for value in (selected['span'],selected['form'],selected['marker'],selected['risk'],selected['rejected_alternative'],selected['hold']):
  cc+=1
  if value not in blob: missing.append(f"{final['decision_id']}:canonical:{value}")
 for value in selected.get('exact_alternatives',[]):
  ac+=1
  if value not in blob: missing.append(f"{final['decision_id']}:canonical_alt:{value}")
 for source,label,fields in ((hr,'hebrew',('span','literary_form','deciding_marker','risk','rejected_alternative','hebrew_textual_translation_evidence')),(lr,'literary',('span','title','literary_form','deciding_marker','risk','rejected_alternative'))):
  for proposed in (x for x in source if overlap(final['span'],x['span'])):
   for field in fields:
    if label=='hebrew': hc+=1
    else: lc+=1
    if proposed[field] not in blob: missing.append(f"{final['decision_id']}:{label}:{proposed['index']}:{field}")
   if label=='literary':
    for value in proposed.get('exact_alternatives',[]):
     ac+=1
     if value not in blob: missing.append(f"{final['decision_id']}:literary_alt:{value}")
def string_scalars(value):
 if isinstance(value,str): yield value
 elif isinstance(value,dict):
  for item in value.values(): yield from string_scalars(item)
 elif isinstance(value,list):
  for item in value: yield from string_scalars(item)
blob_all=json.dumps(rows,ensure_ascii=False); global_checks=0
for source,label in ((h.get('macro_parent_alternatives',[]),'hebrew_macro'),(l.get('macro_parent_alternatives',[]),'literary_macro'),(c.get('premortem_holds',[]),'canonical_premortem'),(c.get('evidence_only_canonical_relations',[]),'canonical_relation'),(c.get('hardest_boundary_order',[]),'canonical_hardest'),(c.get('global_guards',[]),'canonical_guard'),(h.get('evidence_only_guard',{}),'hebrew_guard')):
 for value in string_scalars(source):
  global_checks+=1
  if value not in blob_all: missing.append(f'global:{label}:{value}')
req(not missing,f'{len(missing)} omissions: {missing[:10]}')
print(json.dumps({'verdict':'PASS','chunks_sha256':SHA,'final_chunks':21,'hebrew_rows':22,'literary_rows':22,'canonical_rows':21,'canonical_field_checks':cc,'hebrew_overlap_field_checks':hc,'literary_overlap_field_checks':lc,'exact_alternative_checks':ac,'global_scalar_checks':global_checks,'omissions':0,'forced_consensus':False,'non_authorizing':True},sort_keys=True))