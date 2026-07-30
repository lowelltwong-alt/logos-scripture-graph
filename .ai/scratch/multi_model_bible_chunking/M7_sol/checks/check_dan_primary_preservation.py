#!/usr/bin/env python3
"""Verify every blind Daniel proposal survives final synthesis."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
MODEL=Path(__file__).resolve().parents[1]; REV=MODEL/'reviews'/'Dan'; CH=MODEL/'book_chunks'/'Dan'/'chunks.jsonl'; SHA='5aa00dbfead664fccccaff826a1454531873baa2ebc22a840143b1a1cbac14c1'
def pt(v):
 v=v.replace('Dan.','').replace('.',':'); c,n=v.split(':'); return int(c),int(n)
def sp(v):
 a,b=v.split('-'); return pt(a),pt(b)
def ov(a,b):
 a0,a1=sp(a); b0,b1=sp(b); return a0<=b1 and b0<=a1
def req(c,m):
 if not c: raise SystemExit('FAIL: '+m)
def strings(v):
 if isinstance(v,str): yield v
 elif isinstance(v,dict):
  for x in v.values(): yield from strings(x)
 elif isinstance(v,list):
  for x in v: yield from strings(x)
rows=[json.loads(x) for x in CH.read_text(encoding='utf-8').splitlines() if x.strip()]
lit=json.loads((REV/'blind_proposal_literary_v1.json').read_text(encoding='utf-8')); can=json.loads((REV/'blind_proposal_canonical_premortem_v1.json').read_text(encoding='utf-8')); heb=json.loads((REV/'blind_proposal_hebrew_textual_v1.json').read_text(encoding='utf-8'))
lr,cr,hr=lit['units'],can['chunks'],heb['proposed_chunks']; req(hashlib.sha256(CH.read_bytes()).hexdigest()==SHA,'SHA'); req((len(rows),len(lr),len(cr),len(hr))==(35,35,35,42),'counts')
lc=cc=hc=ac=0; missing=[]
for final,selected in zip(rows,lr,strict=True):
 blob=json.dumps(final,ensure_ascii=False)
 for value in (selected['span'],selected['title'],selected['literary_form'],selected['deciding_marker'],selected['risk'],selected['rejected_alternative']):
  lc+=1
  if value not in blob: missing.append(f"{final['decision_id']}:literary:{value}")
 for value in selected.get('exact_alternatives',[]):
  ac+=1
  if value not in blob: missing.append(f"{final['decision_id']}:lit_alt:{value}")
 for hrow in (x for x in hr if ov(final['span'],x['span'])):
  for value in (hrow['span'],hrow['literary_form'],hrow['deciding_marker'],hrow['risk'],hrow['rejected_alternative'],hrow['hebrew_textual_translation_evidence']):
   hc+=1
   if value not in blob: missing.append(f"{final['decision_id']}:hebrew:{hrow['index']}:{value}")
 for crow in (x for x in cr if ov(final['span'],x['span'])):
  for value in (crow['span'],crow['form'],crow['marker'],crow['risk'],crow['rejected_alternative'],crow['hold']):
   cc+=1
   if value not in blob: missing.append(f"{final['decision_id']}:canonical:{crow['index']}:{value}")
  for value in crow.get('exact_alternatives',[]):
   ac+=1
   if value not in blob: missing.append(f"{final['decision_id']}:can_alt:{value}")
blob_all=json.dumps(rows,ensure_ascii=False); gc=0
for source,label in ((lit.get('macro_parent_alternatives',[]),'lit_macro'),(lit.get('global_hot_zones',[]),'lit_hot'),(can.get('premortem_holds',[]),'can_premortem'),(can.get('evidence_only_canonical_relations',[]),'can_relation'),(can.get('hardest_boundary_order',[]),'can_hard'),(can.get('global_guards',[]),'can_guard'),(heb.get('evidence_only_guard',{}),'heb_guard'),(heb.get('macro_parent_alternatives',[]),'heb_macro'),(heb.get('textual_translation_hot_zone_audit',[]),'heb_hot')):
 for value in strings(source):
  gc+=1
  if value not in blob_all: missing.append(f'global:{label}:{value}')
req(not missing,f'{len(missing)} omissions: {missing[:10]}')
print(json.dumps({'verdict':'PASS','chunks_sha256':SHA,'final_chunks':35,'literary_rows':35,'canonical_rows':35,'hebrew_rows':42,'literary_field_checks':lc,'canonical_overlap_field_checks':cc,'hebrew_overlap_field_checks':hc,'exact_alternative_checks':ac,'global_scalar_checks':gc,'omissions':0,'forced_consensus':False,'non_authorizing':True},sort_keys=True))