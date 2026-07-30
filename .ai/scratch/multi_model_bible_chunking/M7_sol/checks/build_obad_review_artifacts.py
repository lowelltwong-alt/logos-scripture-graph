from __future__ import annotations
import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from build_review_artifacts_generic import build
M=H.parent;E='3faea6b1b5b66a39fc130e5c6a123616c1b74ea4edf8ba9a4c6b8a24f9206b7d'
def pt(v):v=v.replace('Obad.','').replace('.',':');c,n=v.split(':');return int(c),int(n)
def pair(v):a,b=v.split('-');return pt(a),pt(b)
def ov(a,b):a0,a1=pair(a);b0,b1=pair(b);return a0<=b1 and b0<=a1
ch=[json.loads(x) for x in (M/'book_chunks/Obad/chunks.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()];can=json.loads((M/'reviews/Obad/blind_proposal_canonical_premortem_v1.json').read_text(encoding='utf-8'));spec=[]
for r in can['evidence_only_canonical_relations']:
 scopes=[x.strip() for x in r['obad_scope'].split(';')];ids=[x['decision_id'] for x in ch if any(ov(x['span'],s) for s in scopes)];spec.append((r['relation_id'].split('-')[-1],ids,r['canonical_passages'],r['observed_relation']+' Guard: '+r['guard']))
build(book='Obad',expected_sha=E,roles=(('hebrew','obad-primary-hebrew-textual-20260723-a','Biblical_Hebrew_oracle_wordplay_witness_and_translation_specialist'),('literary','obad-primary-literary-20260723-b','compact_oracle_accusation_day_reversal_register_and_closure_specialist'),('canonical','obad-primary-canonical-premortem-20260723-c','canonical_relations_source_direction_identity_ethics_fulfillment_premortem_specialist')),peer_attempt='obad-peer-crosscheck-20260723-d',boss_attempt='obad-boss-adjudicator-20260723-e',post_attempt='obad-role-separated-postchecker-20260723-f',relation_specs=tuple(spec),reviewer_hint='human_or_external_ai_Biblical_Hebrew_Obadiah_Jeremiah_Edom_oracles_ancient_Jewish_reception_specialist')