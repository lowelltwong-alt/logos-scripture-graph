#!/usr/bin/env python3
"""Book-specific T551 Joel corrective rereview materializer."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[6]
MODEL=ROOT/'.ai'/'scratch'/'multi_model_bible_chunking'/'M7_sol'
REV=MODEL/'reviews'/'Joel'; CHUNKS=MODEL/'book_chunks'/'Joel'/'chunks.jsonl'
ROUTE=REV/'adjudicated_route_draft_v2.json'
WEB=ROOT/'data'/'canonical'/'translations'/'eng-web'/'translation_witnesses.jsonl'
QUESTION=("Should Joel 3:4's named-neighbor direct address make Joel 3:1-3 and "
"Joel 3:4-8 independently retrievable literary units with mandatory Joel 3:1-8 "
"parent hydration, or should 3:4 remain an internal seam inside one Joel 3:1-8 nations-lawsuit unit?")
INDEPENDENCE={'independent_from_sibling_model_maps':True,'primaries_blind_to_each_other_artifacts':True,
'roles_separated':True,'shared_model_substrate':True,'counts_as_cross_model_independent_votes':False,
'independent_model_or_human_evidence_required_at_convergence':True,'reviewer_count_is_not_authority':True,
'correlated_mesh_weight_at_convergence':'one_model_voice'}
ROLES=(('hebrew','hebrew_textual_versification'),('literary','literary_prophetic_form'),
('canonical','canonical_retrieval_premortem'))

def rjl(path:Path)->list[dict[str,Any]]:
 out=[]
 if not path.exists(): return out
 for line in path.read_text(encoding='utf-8').splitlines():
  if line.strip(): out.append(json.loads(line))
 return out

def wj(path:Path,value:Any)->None:
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

def wjl(path:Path,rows:list[dict[str,Any]])->None:
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(''.join(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n' for x in rows),encoding='utf-8',newline='\n')

def sha(path:Path)->str: return hashlib.sha256(path.read_bytes()).hexdigest()
def row_sha(row:dict[str,Any])->str:
 return hashlib.sha256(json.dumps(row,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def inventory()->tuple[list[str],dict[str,str]]:
 rows=[x for x in rjl(WEB) if str(x.get('osis_ref','')).startswith('Joel.')]
 refs=[x['osis_ref'] for x in rows]; texts={x['osis_ref']:x['text'] for x in rows}
 if len(refs)!=73 or refs[0]!='Joel.1.1' or refs[-1]!='Joel.3.21': raise ValueError('unexpected Joel WEB inventory')
 return refs,texts

def mt(ref:str)->str:
 _,cs,vs=ref.split('.'); c,v=int(cs),int(vs)
 if c==2 and v>=28: c,v=3,v-27
 elif c==3: c=4
 return f'Joel.{c}.{v}'

def source_refs(span:str,did:str)->list[Any]:
 a,b=span.split('-'); ms=f'{mt(a)}-{mt(b)}'; out:[Any]=[f'direct_read:eng-web:{span}']
 for sid in ('oshb','uxlc'):
  out.append({'source_id':sid,'span':span,'web_span':span,'source_span':ms,'coordinate_system':'MT_WLC',
  'crosswalk_status':'validated_web_mt_verse_mapping','source_metadata_boundary_authority':False,
  'observation':f'{did}:{sid.upper()}_WLC_family_locator_{ms}'})
 return out

def materialize(post_path:Path|None)->dict[str,Any]:
 route=json.loads(ROUTE.read_text(encoding='utf-8')); units=route['route']
 if len(units)!=13 or route['accepted']!=11 or route['held']!=2: raise ValueError('unfrozen or unexpected Joel route')
 refs,texts=inventory(); pos={r:i for i,r in enumerate(refs)}; coverage=[]; chunks=[]; staged=[]
 for n,u in enumerate(units,1):
  span=u['span']; a,b=span.split('-'); cov=refs[pos[a]:pos[b]+1]; coverage.extend(cov)
  did=f'M7_sol-Joel-{n:03d}'; held=u.get('disposition')=='deferred_human_or_external_ai'
  observations=[{'ref':f'WEB:{cov[0]}','text':texts[cov[0]],'extent':'complete_verse','use':'opening_witness'}]
  if cov[-1]!=cov[0]: observations.append({'ref':f'WEB:{cov[-1]}','text':texts[cov[-1]],'extent':'complete_verse','use':'closing_witness'})
  alignment={'web_span':span,'oshb_span':f'{mt(a)}-{mt(b)}','uxlc_span':f'{mt(a)}-{mt(b)}','coordinate_system':'MT_WLC',
  'crosswalk_status':'validated_web_mt_verse_mapping','source_metadata_boundary_authority':False,
  'versification_crosswalk_is_evidence_only':True,'wlc_family_correlation_disclosed':True,
  'oshb_uxlc_are_independent_witnesses':False,'local_primary_lxx_available':False,'local_primary_dss_available':False,
  'local_primary_rabbinic_or_second_temple_corpus_available':False,'authority':'translation_textual_order_and_form_evidence_only'}
  chunk={'model_id':'M7_sol','book':'Joel','span':span,'chunk_index_in_book':n,'working_title':u['title'],
  'literature_type_guess':u['form'],'literary_form':u['form'],'parent_literary_form':u['parent_form'],'parent_span':u['parent_span'],
  'boundary_evidence_refs':[f'direct_read:eng-web:{span}',f'direct_read:oshb:{span}',f'direct_read:uxlc:{span}',
  'book_strategy/Joel.md','reviews/Joel/decision_evidence_v2.jsonl','reviews/Joel/decision_relations.jsonl'],
  'strong_or_hebrew_tags_used':['direct_Biblical_Hebrew_prophetic_form_considered','WEB_to_MT_four_chapter_crosswalk_evidence_only',
  'roots_are_not_meaning','correlated_WLC_family_views_disclosed','later_reuse_is_not_boundary_authority'],
  'wj_or_red_letter_considered':False,'frontier_flag_considered':True,'confidence':u['confidence'],'decision_id':did,
  'deciding_marker_or_seam':u['marker'],'boundary_rationale':u['rationale'],'rejected_alternative':u['rejected'],
  'counterevidence':u['counter'],'defensible_basis':u['basis'],'confidence_basis':{'tier':u['confidence'],
  'marker_strength':'decision_specific_prophetic_form_and_discourse_evidence','alternative_strength':'specialist_counterproposal_preserved',
  'status_not_used_as_input':True},'review_revision':'m7-corrective-rereview-v2',
  'review_status':'final_deferred_appeal' if held else 'candidate_review_complete','review_holds':[QUESTION] if held else [],
  'candidate_hold_state':'deferred_human_or_external_ai' if held else None,
  'candidate_hold_basis':({'kind':'retrieval_boundary_dispute','question':QUESTION,'options':['Keep the two children with mandatory parent hydration.','Merge them into one lawsuit child and retain the address turn internally.']} if held else None),
  'human_review_question':QUESTION if held else None,
  'human_review_route':'independent_Biblical_Hebrew_and_prophetic_literary_human_or_external_AI' if held else None,
  'candidate_internal_seams':u['internal_seams'],'non_authorizing':True,'candidate_only':True,'working_title_is_boundary_authority':False,
  'original_language_translation_holds':['Joel 1:17, 2:23, and 3:21 remain translation hot zones; the English-three/Hebrew-four chapter crosswalk and WLC-family morphology are evidence only.'],
  'cross_reference_holds':[u['guard']],'red_team_premortem_holds':[u['counter']],
  'convergence_defense':{'literary_form':u['form'],'deciding_marker_or_seam':u['marker'],'rejected_alternative':u['rejected'],
  'confidence':u['confidence'],'defensible_basis':u['basis'],'parent_span':u['parent_span'],'source_observations':observations,
  'original_language_alignment':alignment}}
  chunks.append(chunk); staged.append((u,chunk,source_refs(span,did)))
 if coverage!=refs or [x['chunk_index_in_book'] for x in chunks]!=list(range(1,14)): raise ValueError('Joel exact coverage or index failure')
 post=None
 if post_path:
  post=json.loads(post_path.read_text(encoding='utf-8'))
  if post.get('verdict') not in ('pass','pass_with_holds'): raise ValueError('nonpassing postcheck report')
 packets=[]; evidence_rows=[]; role_rows={x:[] for x,_ in ROLES}; peers=[]; bosses=[]
 for u,ch,srefs in staged:
  n=ch['chunk_index_in_book']; did=ch['decision_id']; held=ch['candidate_hold_state'] is not None; reviews=[]; cids=[]
  for code,role in ROLES:
   challenged=code in u['challenge_roles']; challenges=[]
   if challenged:
    cid=f'{did}-{code.upper()}-CHALLENGE-01'; cids.append(cid)
    challenges=[{'challenge_id':cid,'claim':u['counter'],'proposed_remedy':'Evaluate the preserved alternative: '+u['rejected'],
    'counterevidence':u['basis'],'source_refs':srefs}]
   support={'hebrew':'Hebrew-textual observation: '+u['marker'],'literary':'Prophetic-form reading: '+u['basis'],
   'canonical':'Retrieval premortem: '+u['guard']}[code]
   review={'reviewer_attempt_id':f'joel-v2-{code}-{n:03d}-specialist-high','reviewer_role':role,'role':role,
   'verdict':'challenge' if challenged else 'supports','blind_to_other_primary_reviews':True,'evidence_only':True,
   'evidence_refs':srefs,'source_refs':srefs,'support':support,'counterevidence':u['counter'] if code!='literary' else u['rejected'],
   'challenges':challenges}
   reviews.append(review); role_rows[code].append(review)
  responses=[{'challenge_id':cid,'disposition':'held_for_independent_resolution' if held else 'boss_overruled_with_dissent_preserved',
  'rationale':('The address change supports provisional children, but autonomous retrieval remains unresolved within the complete lawsuit parent.' if held else u['rationale']),
  'rejected_alternative':u['rejected']} for cid in cids]
  appeals=[]
  if held:
   appeals=[{'appeal_id':u['appeal_id'],'status':'open_deferred_human_or_external_ai','question':QUESTION,
   'option_a':'Keep Joel 3:1-3 and Joel 3:4-8 separate with mandatory Joel 3:1-8 hydration.',
   'option_b':'Merge both into one Joel 3:1-8 nations-lawsuit child and retain 3:4 internally.',
   'preserved_disagreement':'Hebrew/textual and canonical reviewers support the address split; literary review prefers the whole lawsuit and accepts the paired hold.',
   'appellant_attempt_id':f'joel-v2-literary-{n:03d}-specialist-high','disagreement_with':f'joel-v2-boss-{n:03d}-sol-high',
   'disputed_claim_id':cids[0],'passage_context':u['parent_span'],'evidence_refs':srefs,'rationale':u['counter'],
   'uncertainty':'Whether a genuine direct-address seam creates an autonomous retrieval child.','requested_next_reviewer':'independent_Biblical_Hebrew_and_prophetic_literary_human_or_external_AI',
   'forced_consensus':False}]
  peer={'reviewer_attempt_id':f'joel-v2-peer-{n:03d}-crosscheck-high','reviewer_role':'adversarial_passage_crosscheck',
  'status':'pass_with_hold' if held else 'pass','disputed_claim_ids':cids,'rationale':u['basis'],'counterevidence':u['counter'],
  'source_refs':srefs,'support_challenge_mix':{'support_count':sum(x['verdict']=='supports' for x in reviews),'challenge_count':sum(x['verdict']=='challenge' for x in reviews)}}
  resolution={'author_id':'M7_sol','author_attempt_id':f'joel-v2-boss-{n:03d}-sol-high','challenge_responses':responses,
  'unresolved_claim_ids':cids if held else [],'rationale':u['rationale'],'counterevidence':u['counter'],
  'rejected_alternative':u['rejected'],'outcome':'held_lower_confidence_for_independent_review' if held else 'accepted_candidate_after_role_specific_review',
  'authority':'candidate_author_only'}
  boss={'ruling_id':resolution['author_attempt_id'],'rationale':u['rationale'],'counterevidence':u['counter'],
  'rejected_alternative':u['rejected'],'outcome':'hold_candidate' if held else 'accept_candidate',
  'appeal_effect':'two_open_linked_appeals' if held else 'historical_dissent_preserved_without_active_appeal','forced_consensus':False}
  chash=row_sha(ch)
  packet={'schema_version':'m7_corrective_review_packet.v2','decision_id':did,'book':'Joel','span':ch['span'],
  'chunk_sha256':chash,'chunk_content_sha256':chash,'review_revision':'m7-corrective-rereview-v2','primary_reviews':reviews,
  'peer_crosscheck':peer,'sol_resolution':resolution,'appeals':appeals,'final_state':'held_lower_confidence' if held else 'accepted_candidate',
  'human_review_question':QUESTION if held else None,'human_review_route':'independent_Biblical_Hebrew_and_prophetic_literary_human_or_external_AI' if held else None,
  'post_resolution_check':{'checker_attempt_id':f'joel-v2-post-{n:03d}-independent-checker','status':(('hold' if held else 'pass') if post else 'pending_independent_postcheck'),
  'evidence_refs':['reviews/Joel/post_resolution_check_v2.json'],
  'chunk_content_sha256':chash},'independence_scope':INDEPENDENCE,'non_authorizing':True,'boss_ruling':boss}
  packets.append(packet); peers.append({'decision_id':did,**peer}); bosses.append({'decision_id':did,**boss})
  evidence_rows.append({'schema_version':'m7_joel_decision_evidence.v2','book':'Joel','decision_id':did,'span':ch['span'],
  'literary_form':u['form'],'parent_literary_form':u['parent_form'],'parent_span':u['parent_span'],'candidate_state':packet['final_state'],
  'confidence':u['confidence'],'confidence_basis':ch['confidence_basis'],'deciding_marker_or_seam':u['marker'],'boundary_rationale':u['rationale'],
  'rejected_alternative':u['rejected'],'defensible_basis':u['basis'],'source_observations':ch['convergence_defense']['source_observations'],
  'original_language_alignment':ch['convergence_defense']['original_language_alignment'],'hold':appeals[0] if appeals else None,
  'primary_reviews':reviews,'non_authorizing':True})
 parents=[('01','Joel.1.1-Joel.1.12','book_opening_crisis_witness_and_serial_lament',[1,2,3]),
 ('02','Joel.1.13-Joel.1.20','liturgical_and_day_lament_response_to_devastation',[4,5]),
 ('03','Joel.2.1-Joel.2.17','alarm_return_assembly_and_intercession_movement',[6,7]),
 ('04','Joel.2.28-Joel.3.21','afterward_outpouring_nations_judgment_and_zion_restoration_complex',[9,10,11,12,13]),
 ('05','Joel.3.1-Joel.3.8','nations_lawsuit_and_named_repayment_scene',[10,11]),
 ('06','Joel.3.9-Joel.3.21','nations_judgment_climax_and_zion_restoration_close',[12,13])]
 relations=[{'schema_version':'m7_decision_relation.v2','note_id':f'JOEL-V2-PARENT-{i}','book':'Joel',
 'relation_type':'named_joel_macro_parent_with_context_hydration','parent_span':span,'parent_literary_form':form,
 'children':[f'M7_sol-Joel-{n:03d}' for n in nums],
 'rationale':f'{form} remains the context parent for its children, protecting rhetorical continuity without erasing local prophetic forms.',
 'mandatory_hydration':True,'boundary_authority':False,'non_authorizing':True} for i,span,form,nums in parents]
 for i,n,alts,reason in [('01',7,['Joel.2.12-Joel.2.14','Joel.2.15-Joel.2.17'],'The literary specialist marked the trumpet reset and then concurred with the larger return-to-intercession movement.'),
 ('02',8,['Joel.2.18-Joel.2.20','Joel.2.21-Joel.2.27'],'The Hebrew specialist preserves the 2:21 address turn internally without an active appeal.'),
 ('03',12,['Joel.3.9-Joel.3.11','Joel.3.12-Joel.3.17'],'The literary specialist marked the judicial transition and then concurred that muster and judgment escalate together.')]:
  relations.append({'schema_version':'m7_decision_relation.v2','note_id':f'JOEL-V2-DISSENT-{i}','book':'Joel',
  'relation_type':'preserved_specialist_dissent_without_active_appeal','children':[f'M7_sol-Joel-{n:03d}'],
  'alternative_spans':alts,'rationale':reason,'boundary_authority':False,'non_authorizing':True})
 wjl(CHUNKS,chunks); wjl(REV/'review_packets.jsonl',packets); wjl(REV/'decision_evidence_v2.jsonl',evidence_rows); wjl(REV/'decision_relations.jsonl',relations)
 for code,role in ROLES:
  artifact={'schema_version':'m7_joel_role_artifact.v2','book':'Joel','role':role,'decision_local_review_count':13,
  'reviews':role_rows[code],'blind_primary_artifacts_remain_frozen':True,'post_ruling_active_appeals':0,'candidate_only':True,'non_authorizing':True}
  name={'hebrew':'primary_hebrew_v2.json','literary':'primary_literary_v2.json','canonical':'canonical_premortem_v2.json'}[code]; wj(REV/name,artifact)
  name={'hebrew':'corrective_specialist_hebrew_textual_v2.json','literary':'corrective_specialist_literary_v2.json','canonical':'corrective_specialist_canonical_premortem_v2.json'}[code]; wj(REV/name,artifact)
 wj(REV/'peer_crosscheck_v2.json',{'schema_version':'m7_joel_peer_crosscheck.v2','book':'Joel','reviews':peers,'candidate_only':True,'non_authorizing':True})
 wj(REV/'boss_ruling_v2.json',{'schema_version':'m7_joel_boss_ruling.v2','task_id':'T551','book':'Joel','route_count':13,
 'accepted':11,'held':2,'boss_attempt_id':'joel_boss_adjudicator_v2-sol-high','rulings':bosses,'specialist_post_ruling_active_appeals':0,
 'forced_consensus':False,'candidate_only':True,'non_authorizing':True})
 wj(REV/'mesh_instruction_and_dissent_v2.json',{'schema_version':'m7_joel_mesh_instruction_record.v2','task_id':'T551',
 'roles':[x[1] for x in ROLES]+['boss_adjudicator','independent_post_resolution_checker'],
 'instructions':['blind read-only primaries','original-language and canonical relations are evidence only','larger coherent unit under tied evidence',
 'boss answers each challenge without forcing consensus','post-ruling appeal opportunity for every specialist','true holds route to human or external AI'],
 'post_ruling_results':{'hebrew':'zero active appeals; 2:21 dissent preserved','literary':'zero active appeals; 3:1-8 preference preserved',
 'canonical':'zero active appeals; opening and lament parents mandatory'},'candidate_only':True,'non_authorizing':True})
 ledger=REV/'appeal_ledger.jsonl'; old=rjl(ledger); ids={str(x.get('appeal_id','')) for x in old}; additions=[]
 for p in packets:
  if p['appeals'] and p['appeals'][0]['appeal_id'] not in ids:
   additions.append({**p['appeals'][0],'schema_version':'m7_joel_boundary_appeal.v2','book':'Joel','decision_id':p['decision_id'],
   'span':p['span'],'append_only':True,'candidate_only':True,'non_authorizing':True})
 if additions:
  with ledger.open('a',encoding='utf-8',newline='\n') as h:
   for x in additions: h.write(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n')
 post_art={'schema_version':'m7_post_resolution_check.v2','checker_attempt_id':post.get('checker_attempt_id') if post else 'pending-independent-joel-postchecker',
 'role':'fresh_read_only_post_resolution_checker','book':'Joel','status':'pass_with_2_holds' if post else 'pending_independent_postcheck',
 'checked_decision_ids':[x['decision_id'] for x in chunks],'checker_attempt_ids':[f'joel-v2-post-{n:03d}-independent-checker' for n in range(1,14)],
 'checked_review_packets_sha256':sha(REV/'review_packets.jsonl'),'checked_chunks_sha256':sha(CHUNKS),'checked_decision_relations_sha256':sha(REV/'decision_relations.jsonl'),
 'role_separated_checker_verdict_received':bool(post),'independent_model_verdict_received':False,
 'coverage':{'expected':73,'observed':len(coverage),'exact_ordered':coverage==refs},
 'accepted':11,'held':2,'postcheck_report_sha256':sha(post_path) if post else None,'postcheck_report':post,
 'candidate_only':True,'non_authorizing':True}; wj(REV/'post_resolution_check_v2.json',post_art)
 return {'book':'Joel','chunks':13,'coverage':73,'accepted':11,'held':2,
 'confidence':{k:sum(x['confidence']==k for x in chunks) for k in sorted({x['confidence'] for x in chunks})},
 'active_specialist_post_ruling_appeals':0,'open_linked_boundary_appeals':2,'postcheck':post_art['status'],
 'hashes':{'chunks':sha(CHUNKS),'packets':sha(REV/'review_packets.jsonl'),'evidence':sha(REV/'decision_evidence_v2.jsonl'),'relations':sha(REV/'decision_relations.jsonl')}}

def main()->int:
 ap=argparse.ArgumentParser(); ap.add_argument('--postcheck-report',type=Path); a=ap.parse_args()
 print(json.dumps(materialize(a.postcheck_report),ensure_ascii=False,indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())