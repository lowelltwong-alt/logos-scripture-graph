from __future__ import annotations
import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from build_review_artifacts_generic import build
M=H.parent;E='51cffd8262768895d2172e7200cbad1ab2107315f11641de86f04c4bc3ad05ce'
def pt(v):v=v.replace('Hag.','').replace('.',':');a,b=v.split(':');return int(a),int(b)
def pair(v):p=v.split('-');return pt(p[0]),pt(p[-1])
def ov(a,b):a0,a1=pair(a);b0,b1=pair(b);return a0<=b1 and b0<=a1
ch=[json.loads(x) for x in (M/'book_chunks/Hag/chunks.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()];can=json.loads((M/'reviews/Hag/blind_proposal_canonical_premortem_v1.json').read_text(encoding='utf-8'));spec=[]
for r in can['evidence_only_canonical_relations']:
 scopes=[x.strip() for x in r['hag_scope'].split(';')];ids=[x['decision_id'] for x in ch if any(ov(x['span'],s) for s in scopes)];spec.append((r['relation_id'].split('-')[-1],ids,r['canonical_passages'],r['observed_relation']+' Guard: '+r['guard']))
build(book='Hag',expected_sha=E,roles=(('hebrew','hag-primary-hebrew-textual-20260723-a','Hebrew_dated_oracle_Torah_inquiry_translation_specialist'),('literary','hag-primary-literary-20260723-b','dated_speech_response_inquiry_oracle_specialist'),('canonical','hag-primary-canonical-premortem-20260723-c','canonical_relations_history_purity_identity_fulfillment_premortem_specialist')),peer_attempt='hag-peer-crosscheck-20260723-d',boss_attempt='hag-boss-adjudicator-20260723-e',post_attempt='hag-role-separated-postchecker-20260723-f',relation_specs=tuple(spec),reviewer_hint='human_or_external_ai_Biblical_Hebrew_Haggai_Persian_period_priestly_Torah_ancient_Jewish_reception_specialist')