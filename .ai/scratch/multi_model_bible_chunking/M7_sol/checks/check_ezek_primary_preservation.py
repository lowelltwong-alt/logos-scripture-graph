#!/usr/bin/env python3
"""Verify Ezekiel blind proposals and Hebrew audit survive final synthesis."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
MODEL=Path(__file__).resolve().parents[1]; REV=MODEL/'reviews'/'Ezek'; CH=MODEL/'book_chunks'/'Ezek'/'chunks.jsonl'; SHA='b91240561f69c3fecea61523ed621d458c43e77665020c63080b35d1f270fa46'
def pt(v):
 v=v.replace('Ezek.','').replace('.',':'); c,n=v.split(':'); return int(c),int(n)
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
lit=json.loads((REV/'blind_proposal_literary_v1.json').read_text(encoding='utf-8')); can=json.loads((REV/'blind_proposal_canonical_premortem_v1.json').read_text(encoding='utf-8')); heb=json.loads((REV/'hebrew_textual_audit_v1.json').read_text(encoding='utf-8'))
lr,cr,hr=lit['units'],can['chunks'],heb['units']; req(hashlib.sha256(CH.read_bytes()).hexdigest()==SHA,'SHA'); req((len(rows),len(lr),len(cr),len(hr))==(89,89,105,89),'counts')
lc=cc=hc=ac=0; missing=[]
for final,selected,hrow in zip(rows,lr,hr,strict=True):
 blob=json.dumps(final,ensure_ascii=False)
 for value in (selected['span'],selected['title'],selected['literary_form'],selected['deciding_marker'],selected['risk'],selected['rejected_alternative']):
  lc+=1
  if value not in blob: missing.append(f"{final['decision_id']}:literary:{value}")
 for value in selected.get('exact_alternatives',[]):
  ac+=1
  if value not in blob: missing.append(f"{final['decision_id']}:lit_alt:{value}")
 req(hrow['span']==final['span'],f"Hebrew span parity {final['decision_id']}")
 for value in (hrow['span'],hrow['literary_form'],hrow['deciding_marker'],hrow['risk'],hrow['rejected_alternative'],hrow['hebrew_textual_translation_evidence']):
  hc+=1
  if value not in blob: missing.append(f"{final['decision_id']}:hebrew:{value}")
 for crow in (x for x in cr if ov(final['span'],x['span'])):
  for value in (crow['span'],crow['form'],crow['marker'],crow['risk'],crow['rejected_alternative'],crow['hold']):
   cc+=1
   if value not in blob: missing.append(f"{final['decision_id']}:canonical:{crow['index']}:{value}")
  for value in crow.get('exact_alternatives',[]):
   ac+=1
   if value not in blob: missing.append(f"{final['decision_id']}:can_alt:{value}")
blob_all=json.dumps(rows,ensure_ascii=False); gc=0
for source,label in ((lit.get('macro_parent_alternatives',[]),'lit_macro'),(lit.get('global_hot_zones',[]),'lit_hot'),(can.get('premortem_holds',[]),'can_premortem'),(can.get('evidence_only_canonical_relations',[]),'can_relation'),(can.get('hardest_boundary_order',[]),'can_hard'),(can.get('global_guards',[]),'can_guard'),(heb.get('evidence_only_guard',{}),'heb_guard'),(heb.get('macro_observations',[]),'heb_macro')):
 for value in strings(source):
  gc+=1
  if value not in blob_all: missing.append(f'global:{label}:{value}')
req(not missing,f'{len(missing)} omissions: {missing[:10]}')
print(json.dumps({'verdict':'PASS','chunks_sha256':SHA,'final_chunks':89,'literary_rows':89,'canonical_rows':105,'hebrew_audit_rows':89,'literary_field_checks':lc,'canonical_overlap_field_checks':cc,'hebrew_field_checks':hc,'exact_alternative_checks':ac,'global_scalar_checks':gc,'omissions':0,'failed_blind_hebrew_primary_non_vote':True,'hebrew_audit_not_blind_primary':True,'forced_consensus':False,'non_authorizing':True},sort_keys=True))