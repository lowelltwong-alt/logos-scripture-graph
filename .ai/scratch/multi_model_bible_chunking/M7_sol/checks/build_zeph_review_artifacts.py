from __future__ import annotations
import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from build_review_artifacts_generic import build
M=H.parent;E='c137099b0e890774a26172c257d9cc3c93ca1bb85c3247eb7db36f20e7ce2341'
def pt(v):v=v.replace('Zeph.','').replace('.',':');a,b=v.split(':');return int(a),int(b)
def pair(v):p=v.split('-');return pt(p[0]),pt(p[-1])
def ov(a,b):a0,a1=pair(a);b0,b1=pair(b);return a0<=b1 and b0<=a1
ch=[json.loads(x) for x in (M/'book_chunks/Zeph/chunks.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()];can=json.loads((M/'reviews/Zeph/blind_proposal_canonical_premortem_v1.json').read_text(encoding='utf-8'));spec=[]
for r in can['evidence_only_canonical_relations']:
 scopes=[x.strip() for x in r['zeph_scope'].split(';')];ids=[x['decision_id'] for x in ch if any(ov(x['span'],s) for s in scopes)];spec.append((r['relation_id'].split('-')[-1],ids,r['canonical_passages'],r['observed_relation']+' Guard: '+r['guard']))
build(book='Zeph',expected_sha=E,roles=(('hebrew','zeph-qualified-hebrew-textual-audit-20260723-a','qualified_nonvoting_Hebrew_textual_audit_with_placeholder_exposure'),('literary','zeph-primary-literary-20260723-b','clean_blind_day_oracle_nations_woe_remnant_song_specialist'),('canonical','zeph-primary-canonical-premortem-20260723-c','clean_blind_canonical_relations_history_ethics_fulfillment_premortem_specialist')),peer_attempt='zeph-peer-crosscheck-20260723-d',boss_attempt='zeph-boss-adjudicator-20260723-e',post_attempt='zeph-role-separated-postchecker-20260723-f',relation_specs=tuple(spec),reviewer_hint='human_or_external_ai_Biblical_Hebrew_Zephaniah_day_oracles_ancient_Jewish_reception_specialist')
rev=M/'reviews/Zeph';hp=rev/'primary_hebrew_v1.json';h=json.loads(hp.read_text(encoding='utf-8'));h.update(counts_as_uncontaminated_blind_vote=False,review_weight='qualified_nonvoting_original_language_audit',procedural_isolation_exception='filename search exposed only known chapter-placeholder summaries');hp.write_text(json.dumps(h,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
pp=rev/'review_packets.jsonl';ps=[json.loads(x) for x in pp.read_text(encoding='utf-8').splitlines() if x.strip()]
for q in ps:
 for r in q['primary_reviews']:
  if r['reviewer_attempt_id']=='zeph-qualified-hebrew-textual-audit-20260723-a':r.update(counts_as_uncontaminated_blind_vote=False,review_weight='qualified_nonvoting_original_language_audit')
pp.write_text(''.join(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n' for x in ps),encoding='utf-8',newline='\n')