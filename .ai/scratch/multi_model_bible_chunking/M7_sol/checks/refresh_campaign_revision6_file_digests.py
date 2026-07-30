from __future__ import annotations
import hashlib,json,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
P=ROOT/'.ai/scratch/multi_model_bible_chunking/M7_sol/campaign.json'
def dig(p): return 'sha256:'+hashlib.sha256(p.read_bytes()).hexdigest()
c=json.loads(P.read_text(encoding='utf-8'))
if c.get('revision')!=6: raise SystemExit('requires campaign revision 6')
changed=0; jobs=c['phases'][0]['waves'][0]['subwaves'][0]['jobs']
for job in jobs:
 d=job.get('input_digests',{})
 for rel in list(d):
  p=ROOT/rel
  if rel==P.relative_to(ROOT).as_posix():
   now='stage_receipt:B00.input_artifact_sha256.campaign'
   if d[rel]!=now: d[rel]=now; changed+=1
  elif p.is_file():
   now=dig(p)
   if d[rel]!=now: d[rel]=now; changed+=1
for field in ('workflow','prompt_pack','runtime_adapter'):
 rec=c['replay_contract'][field]; p=ROOT/rec['path']; now=dig(p)
 if rec.get('digest')!=now: rec['digest']=now; changed+=1
c['input_digest_refresh']={'strategy':'revision6_existing_file_inputs_only','changed_pins':changed,'non_authorizing':True}
payload=(json.dumps(c,ensure_ascii=False,indent=2)+'\n').encode(); tmp=P.with_name(P.name+f'.tmp-{os.getpid()}')
with tmp.open('xb') as h: h.write(payload); h.flush(); os.fsync(h.fileno())
os.replace(tmp,P)
print(f'refreshed {changed} revision-6 file digest pins')