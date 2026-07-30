#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
MODEL=Path(__file__).resolve().parents[1]; REV=MODEL/'reviews'/'Hos'; CH=MODEL/'book_chunks'/'Hos'/'chunks.jsonl'
def load(n): return json.loads((REV/n).read_text(encoding='utf-8'))
def readjl(p): return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
def prows(d): return d.get('chunks') or d.get('units') or d.get('proposed_chunks') or []
def point(v):
 v=v.replace('Hos.','').replace('.',':'); c,n=v.split(':'); return int(c),int(n)
def pair(v):
 a,b=v.split('-'); return point(a),point(b)
def overlap(a,b):
 a0,a1=pair(a); b0,b1=pair(b); return a0<=b1 and b0<=a1
def render(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def scalars(v):
 if isinstance(v,dict):
  for x in v.values(): yield from scalars(x)
 elif isinstance(v,list):
  for x in v: yield from scalars(x)
 elif v is not None: yield str(v)
can=load('blind_proposal_canonical_premortem_v1.json'); heb=load('blind_proposal_hebrew_textual_v1.json'); lit=load('blind_proposal_literary_fresh_v1.json'); chunks=readjl(CH)
assert hashlib.sha256((REV/'blind_proposal_canonical_premortem_v1.json').read_bytes()).hexdigest()=='3ea0821908c99f1cbf7b7e5326e81a7b1684c64bd6fee6c4bf84d6ad00001335'
assert hashlib.sha256((REV/'blind_proposal_hebrew_textual_v1.json').read_bytes()).hexdigest()=='30d549600e76678a7ba4e8fcd6df0d0e85aa2d780c1c3e7dbb04701d5d76ecfb'
assert hashlib.sha256((REV/'blind_proposal_literary_fresh_v1.json').read_bytes()).hexdigest()=='50e4f996eab216dfaaedf41a351eca1828732e5fe56cfa0d746a72142ba80716'
assert len(chunks)==30
om=[]; checks={'canonical_rows':0,'hebrew_overlap_rows':0,'literary_overlap_rows':0,'global_scalars':0,'exact_alternatives':0}
for ch in chunks:
 blob=ch['rejected_alternative']; span=ch['span']; cs=[x for x in prows(can) if overlap(span,x['span'])]; hs=[x for x in prows(heb) if overlap(span,x['span'])]; ls=[x for x in prows(lit) if overlap(span,x['span'])]
 for label,items,key in [('canonical',cs,'canonical_rows'),('hebrew',hs,'hebrew_overlap_rows'),('literary',ls,'literary_overlap_rows')]:
  for item in items:
   checks[key]+=1
   if render(item) not in blob: om.append(f"{ch['decision_id']} missing {label} {item.get('span')}")
   for alt in item.get('exact_alternatives',[]):
    checks['exact_alternatives']+=1
    if str(alt) not in blob: om.append(f"{ch['decision_id']} missing alternative {alt}")
 for doc in (can,heb,lit):
  globals_obj={k:v for k,v in doc.items() if k not in {'chunks','units','proposed_chunks'}}
  global_blob=render(globals_obj); checks['global_scalars']+=sum(1 for _ in scalars(globals_obj))
  if global_blob not in blob: om.append(f"{ch['decision_id']} missing serialized global object")
 refs=ch['boundary_evidence_refs'];
 if 'reviews/Hos/blind_proposal_literary_fresh_v1.json' not in refs: om.append(f"{ch['decision_id']} missing fresh literary ref")
 if 'reviews/Hos/blind_proposal_literary_v1.json' in refs: om.append(f"{ch['decision_id']} cites contaminated proposal")
assert not om, '\n'.join(om[:30])
print(json.dumps({'verdict':'PASS','chunks_sha256':hashlib.sha256(CH.read_bytes()).hexdigest(),'checks':checks,'omissions':0,'contaminated_literary_counted_as_vote':False,'fresh_literary_counted':True},sort_keys=True))