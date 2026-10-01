from __future__ import annotations
import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent; sys.path.insert(0,str(H)); from build_review_artifacts_generic import build
M=H.parent; B='Joel'; E='be30094141eeb56a1a5e9eed20e892076896cd04b1c024a11e3bfe6062942888'
def pt(v):
 v=v.replace('Joel.','').replace('.',':'); c,n=v.split(':'); return int(c),int(n)
def pair(v):
 a,b=v.split('-'); return pt(a),pt(b)
def ov(a,b):
 a0,a1=pair(a); b0,b1=pair(b); return a0<=b1 and b0<=a1
chunks=[json.loads(x) for x in (M/'book_chunks/Joel/chunks.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]; can=json.loads((M/'reviews/Joel/blind_proposal_canonical_premortem_v1.json').read_text(encoding='utf-8')); specs=[]
for r in can['evidence_only_canonical_relations']:
 scopes=[x.strip() for x in r['joel_scope'].split(';')]; ids=[x['decision_id'] for x in chunks if any(ov(x['span'],s) for s in scopes)]; specs.append((r['relation_id'].split('-')[-1],ids,r['canonical_passages'],r['observed_relation']+' Guard: '+r['guard']))
build(book=B,expected_sha=E,roles=(('hebrew','joel-qualified-hebrew-textual-audit-20260723-a','qualified_nonvoting_Hebrew_textual_versification_translation_audit_with_disclosed_fallback_exposure'),('literary','joel-primary-literary-20260723-b','clean_blind_prophetic_lament_alarm_oracle_nations_scene_and_restoration_form_specialist'),('canonical','joel-primary-canonical-premortem-20260723-c','clean_blind_canonical_relations_identity_chronology_fulfillment_and_premortem_specialist')),peer_attempt='joel-peer-crosscheck-20260723-d',boss_attempt='joel-boss-adjudicator-20260723-e',post_attempt='joel-role-separated-postchecker-20260723-f',relation_specs=tuple(specs),reviewer_hint='human_or_external_ai_Biblical_Hebrew_Joel_textual_versification_prophetic_poetry_ancient_Jewish_reception_and_canonical_relations_specialist')
# Honest role accounting: the qualified Hebrew audit is useful challenge evidence but not a clean blind vote.
rev=M/'reviews/Joel'; hp=rev/'primary_hebrew_v1.json'; h=json.loads(hp.read_text(encoding='utf-8')); h['blind_to_other_primary_reviews']=True; h['procedural_isolation_exception']='Accidentally saw only the known three chapter-fallback rows; no genuine proposal or positive seam evidence was exposed.'; h['counts_as_uncontaminated_blind_vote']=False; h['review_weight']='qualified_nonvoting_original_language_audit'; hp.write_text(json.dumps(h,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
pp=rev/'review_packets.jsonl'; packets=[json.loads(x) for x in pp.read_text(encoding='utf-8').splitlines() if x.strip()]
for p in packets:
 for pr in p['primary_reviews']:
  if pr['reviewer_attempt_id']=='joel-qualified-hebrew-textual-audit-20260723-a': pr.update(counts_as_uncontaminated_blind_vote=False,review_weight='qualified_nonvoting_original_language_audit',procedural_isolation_exception='saw_only_known_chapter_fallback_no_genuine_route')
pp.write_text(''.join(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n' for x in packets),encoding='utf-8',newline='\n')
incident={'schema_version':'m7_independence_incident.v1','book':'Joel','candidate_sha256':E,'clean_blind_primary_count':2,'qualified_audit':{'artifact':'blind_proposal_hebrew_textual_v1.json','sha256':'4994573e80b8371934de57b404d3fd44a8efdd997d014ca14e79f6b06da5df16','exposure':'known three chapter-fallback rows only','substantive_genuine_route_exposure':False,'counts_as_uncontaminated_blind_vote':False},'failed_fresh_rerun':{'result':'zero_byte_serialization_failure','sha256':'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855','counts_as_evidence':False},'boss_disposition':'Retain two clean blind primaries; use Hebrew artifact only as qualified non-voting challenge evidence; require direct Hebrew witness review at convergence.','forced_consensus':False,'non_authorizing':True}; (rev/'independence_incident_v1.json').write_text(json.dumps(incident,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')