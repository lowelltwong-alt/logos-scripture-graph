import hashlib,json
from pathlib import Path
M=Path(__file__).resolve().parents[1];R=M/'reviews'/'Nah';C=M/'book_chunks'/'Nah'/'chunks.jsonl'
def L(n):return json.loads((R/n).read_text(encoding='utf-8'))
def rows(d):return d.get('chunks') or d.get('units') or d.get('proposed_chunks') or []
def pt(v):v=v.replace('Nah.','').replace('.',':');a,b=v.split(':');return int(a),int(b)
def pair(v):a,b=v.split('-');return pt(a),pt(b)
def ov(a,b):a0,a1=pair(a);b0,b1=pair(b);return a0<=b1 and b0<=a1
def ren(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
ds=[L('blind_proposal_canonical_premortem_v1.json'),L('blind_proposal_literary_v1.json'),L('blind_proposal_hebrew_textual_v1.json')];ch=[json.loads(x) for x in C.read_text(encoding='utf-8').splitlines() if x.strip()];om=[];ck={'overlaps':0,'alternatives':0,'globals':0}
for x in ch:
 b=x['rejected_alternative']
 for d in ds:
  for q in [z for z in rows(d) if ov(x['span'],z['span'])]:
   ck['overlaps']+=1
   if ren(q) not in b:om.append(q['span'])
   for a in q.get('exact_alternatives',[]):ck['alternatives']+=1;om.extend([str(a)] if str(a) not in b else [])
  gg={k:v for k,v in d.items() if k not in {'chunks','units','proposed_chunks'}};ck['globals']+=1
  if ren(gg) not in b:om.append('global')
assert not om,om[:20];print(json.dumps({'verdict':'PASS','chunks_sha256':hashlib.sha256(C.read_bytes()).hexdigest(),'checks':ck,'omissions':0},sort_keys=True))