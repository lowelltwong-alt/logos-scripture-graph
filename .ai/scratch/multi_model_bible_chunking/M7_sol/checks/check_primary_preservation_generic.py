"""M7_sol runtime adapter: verify a candidate preserves all overlapping blind-proposal evidence."""
from __future__ import annotations
import argparse,hashlib,json,re
from pathlib import Path
M=Path(__file__).resolve().parents[1]
def load(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def rows(d):return d.get('chunks') or d.get('units') or d.get('proposed_chunks') or d.get('proposed_units') or d.get('candidate_units') or []
def ren(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def main():
 a=argparse.ArgumentParser();a.add_argument('--book',required=True);z=a.parse_args();b=z.book;r=M/'reviews'/b;c=M/'book_chunks'/b/'chunks.jsonl';rx=re.compile(re.escape(b)+r'\.(\d+)\.(\d+)')
 def pt(v):
  m=rx.fullmatch(v);assert m,v;return int(m.group(1)),int(m.group(2))
 def pair(v):p=v.split('-');return pt(p[0]),pt(p[-1])
 def ov(x,y):x0,x1=pair(x);y0,y1=pair(y);return x0<=y1 and y0<=x1
 ds=[load(r/'blind_proposal_literary_v1.json'),load(r/'blind_proposal_greek_textual_v1.json'),load(r/'blind_proposal_canonical_premortem_v1.json')];ch=[json.loads(x) for x in c.read_text(encoding='utf-8-sig').splitlines() if x.strip()];om=[];ck={'overlaps':0,'alternatives':0,'globals':0}
 for x in ch:
  preserved=x['rejected_alternative']
  for d in ds:
   for q in [v for v in rows(d) if ov(x['span'],v['span'])]:
    ck['overlaps']+=1
    if ren(q) not in preserved:om.append(('overlap',q['span'],x['decision_id']))
    for key,val in q.items():
     if ('alternative' in key or key.endswith('_routes')) and val:
      vals=val if isinstance(val,list) else [val]
      for alt in vals:
       ck['alternatives']+=1
       if ren(alt) not in preserved:om.append(('alternative',key,ren(alt),x['decision_id']))
   g={k:v for k,v in d.items() if k not in {'chunks','units','proposed_chunks','proposed_units','candidate_units'}};ck['globals']+=1
   if ren(g) not in preserved:om.append(('global','',x['decision_id']))
 assert not om,om[:20];print(json.dumps({'verdict':'PASS','book':b,'chunks_sha256':hashlib.sha256(c.read_bytes()).hexdigest(),'checks':ck,'omissions':0},sort_keys=True))
if __name__=='__main__':main()