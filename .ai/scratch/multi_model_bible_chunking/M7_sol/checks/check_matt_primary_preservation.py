import hashlib,json,re
from pathlib import Path
M=Path(__file__).resolve().parents[1];R=M/'reviews'/'Matt';C=M/'book_chunks'/'Matt'/'chunks.jsonl'
def L(n):return json.loads((R/n).read_text(encoding='utf-8-sig'))
def rows(d):return d.get('chunks') or d.get('units') or d.get('proposed_chunks') or d.get('proposed_units') or []
def pt(v):
 m=re.fullmatch(r'Matt\.(\d+)\.(\d+)',v);assert m,v;return int(m.group(1)),int(m.group(2))
def pair(v):p=v.split('-');return pt(p[0]),pt(p[-1])
def ov(a,b):a0,a1=pair(a);b0,b1=pair(b);return a0<=b1 and b0<=a1
def ren(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
ds=[L('blind_proposal_literary_v1.json'),L('blind_proposal_greek_textual_v1.json'),L('blind_proposal_canonical_premortem_v1.json')];ch=[json.loads(x) for x in C.read_text(encoding='utf-8-sig').splitlines() if x.strip()];om=[];ck={'overlaps':0,'alternatives':0,'globals':0}
for x in ch:
 b=x['rejected_alternative']
 for d in ds:
  for q in [z for z in rows(d) if ov(x['span'],z['span'])]:
   ck['overlaps']+=1
   if ren(q) not in b:om.append(('overlap',q['span'],x['decision_id']))
   for a in q.get('exact_alternatives',[]):
    ck['alternatives']+=1
    if str(a) not in b:om.append(('alternative',str(a),x['decision_id']))
  gg={k:v for k,v in d.items() if k not in {'chunks','units','proposed_chunks','proposed_units'}};ck['globals']+=1
  if ren(gg) not in b:om.append(('global','',x['decision_id']))
assert not om,om[:20];print(json.dumps({'verdict':'PASS','chunks_sha256':hashlib.sha256(C.read_bytes()).hexdigest(),'checks':ck,'omissions':0},sort_keys=True))
