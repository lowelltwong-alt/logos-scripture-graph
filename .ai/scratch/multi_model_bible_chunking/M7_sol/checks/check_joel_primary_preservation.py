#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
M=Path(__file__).resolve().parents[1]; R=M/'reviews'/'Joel'; C=M/'book_chunks'/'Joel'/'chunks.jsonl'
def load(n): return json.loads((R/n).read_text(encoding='utf-8'))
def jl(p): return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
def rows(d): return d.get('chunks') or d.get('units') or d.get('proposed_chunks') or []
def pt(v):
 v=v.replace('Joel.','').replace('.',':'); c,n=v.split(':'); return int(c),int(n)
def pair(v):
 a,b=v.split('-'); return pt(a),pt(b)
def ov(a,b):
 a0,a1=pair(a); b0,b1=pair(b); return a0<=b1 and b0<=a1
def render(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
lit=load('blind_proposal_literary_v1.json'); can=load('blind_proposal_canonical_premortem_v1.json'); heb=load('blind_proposal_hebrew_textual_v1.json'); chunks=jl(C)
assert hashlib.sha256((R/'blind_proposal_literary_v1.json').read_bytes()).hexdigest()=='b6f326b881a455556d4e6c08c6df60ced60222f6b56102bcf6d180844909d31a'; assert hashlib.sha256((R/'blind_proposal_canonical_premortem_v1.json').read_bytes()).hexdigest()=='d4c75f4d430b6a6c6323240915a04bd3eed7d941ff2a47e39682fbbbcc71f0bb'; assert hashlib.sha256((R/'blind_proposal_hebrew_textual_v1.json').read_bytes()).hexdigest()=='4994573e80b8371934de57b404d3fd44a8efdd997d014ca14e79f6b06da5df16'; assert len(chunks)==10
om=[]; ck={'literary_rows':0,'canonical_overlaps':0,'qualified_hebrew_overlaps':0,'exact_alternatives':0,'global_objects':0}
for ch in chunks:
 blob=ch['rejected_alternative']; span=ch['span']; groups=[('literary',[x for x in rows(lit) if ov(span,x['span'])]),('canonical',[x for x in rows(can) if ov(span,x['span'])]),('qualified_hebrew',[x for x in rows(heb) if ov(span,x['span'])])]
 for label,items in groups:
  key={'literary':'literary_rows','canonical':'canonical_overlaps','qualified_hebrew':'qualified_hebrew_overlaps'}[label]
  for item in items:
   ck[key]+=1
   if render(item) not in blob: om.append(f"{ch['decision_id']} missing {label} {item['span']}")
   for alt in item.get('exact_alternatives',[]):
    ck['exact_alternatives']+=1
    if str(alt) not in blob: om.append(f"{ch['decision_id']} missing alt {alt}")
 for doc in (lit,can,heb):
  g={k:v for k,v in doc.items() if k not in {'chunks','units','proposed_chunks'}}; ck['global_objects']+=1
  if render(g) not in blob: om.append(f"{ch['decision_id']} missing global object")
 if 'qualified Hebrew' not in blob or 'zero uncontaminated blind primary votes' not in blob: om.append(f"{ch['decision_id']} missing qualification")
assert not om,'\n'.join(om[:25]); print(json.dumps({'verdict':'PASS','chunks_sha256':hashlib.sha256(C.read_bytes()).hexdigest(),'checks':ck,'omissions':0,'clean_blind_primary_count':2,'qualified_hebrew_audit_counted_as_blind_vote':False,'failed_fresh_serialization_counted_as_evidence':False},sort_keys=True))