from __future__ import annotations
import hashlib,json
from pathlib import Path
M=Path(__file__).resolve().parents[1];R=M/'reviews'/'Amos';C=M/'book_chunks'/'Amos'/'chunks.jsonl'
def load(n):return json.loads((R/n).read_text(encoding='utf-8'))
def jl(p):return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
def rows(d):return d.get('chunks') or d.get('units') or d.get('proposed_chunks') or []
def pt(v):v=v.replace('Amos.','').replace('.',':');c,n=v.split(':');return int(c),int(n)
def pair(v):a,b=v.split('-');return pt(a),pt(b)
def ov(a,b):a0,a1=pair(a);b0,b1=pair(b);return a0<=b1 and b0<=a1
def ren(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
can=load('blind_proposal_canonical_premortem_v1.json');lit=load('blind_proposal_literary_v1.json');heb=load('blind_proposal_hebrew_textual_v1.json');ch=jl(C)
assert hashlib.sha256((R/'blind_proposal_canonical_premortem_v1.json').read_bytes()).hexdigest()=='a3d8eb0104f57830330ccdf76f51938f8ec513f0592aa2e6511d4aab41ae770a';assert hashlib.sha256((R/'blind_proposal_literary_v1.json').read_bytes()).hexdigest()=='16741849c35982e12d89201dfbe86f7ce5a57110f669e284f3b028e3aa5b6526';assert hashlib.sha256((R/'blind_proposal_hebrew_textual_v1.json').read_bytes()).hexdigest()=='f4ff8c379f81c9ceb96b47f18e06907b0847f14ebf6f29df8d1c0f90ab25f79e'
om=[];ck={'canonical':0,'literary_overlaps':0,'hebrew_overlaps':0,'alternatives':0,'globals':0}
for x in ch:
 b=x['rejected_alternative'];sp=x['span']
 for label,d,key in [('canonical',can,'canonical'),('literary',lit,'literary_overlaps'),('hebrew',heb,'hebrew_overlaps')]:
  for q in [z for z in rows(d) if ov(sp,z['span'])]:
   ck[key]+=1
   if ren(q) not in b:om.append(f"{x['decision_id']} missing {label} {q['span']}")
   for a in q.get('exact_alternatives',[]):ck['alternatives']+=1;om.extend([f"{x['decision_id']} missing alt {a}"] if str(a) not in b else [])
  gg={k:v for k,v in d.items() if k not in {'chunks','units','proposed_chunks'}};ck['globals']+=1
  if ren(gg) not in b:om.append(f"{x['decision_id']} missing {label} globals")
assert not om,'\n'.join(om[:25]);print(json.dumps({'verdict':'PASS','chunks_sha256':hashlib.sha256(C.read_bytes()).hexdigest(),'checks':ck,'omissions':0},sort_keys=True))