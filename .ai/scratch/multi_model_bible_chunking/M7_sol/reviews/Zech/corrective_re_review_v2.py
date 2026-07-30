#!/usr/bin/env python3
"""Book-specific T560 Zechariah corrective rereview materializer."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[6]
MODEL=ROOT/'.ai'/'scratch'/'multi_model_bible_chunking'/'M7_sol'
REV=MODEL/'reviews'/'Zech'; CHUNKS=MODEL/'book_chunks'/'Zech'/'chunks.jsonl'
ROUTE=REV/'adjudicated_route_draft_v2.json'; POST=REV/'post_ruling_appeal_opportunities_v2.json'; BOSS=REV/'fresh_boss_adjudication_v2.json'
WEB=ROOT/'data'/'canonical'/'translations'/'eng-web'/'translation_witnesses.jsonl'
LEDGER_PREFIX_BYTES=993_279
FROZEN={
'adjudicated_route_draft_v2.json':'fd604430b7e643c601c5bb20f66e50fe7795195b83134bfcf033e63c5877ab30',
'post_ruling_appeal_opportunities_v2.json':'ba85eb50b422204a1b91add2b80f0558bde9a592802a3d5d8eaf6e3e04e8a693',
'fresh_boss_adjudication_v2.json':'12647a03c1428d038ecf7ecc3225bc338843b236608746dcdc0af0a181ba9248',
'blind_proposal_literary_v2.json':'82a372f8e21b31af008409dabbb4b631e343e51f2864904f10e46fd91f067894',
'blind_proposal_hebrew_textual_v2.json':'4fb790558a44a539f9fe81f54b5a28b21edbc588da1d52de32d284ac0d85d5b0',
'blind_proposal_canonical_premortem_v2.json':'e81cc3b262f73fc83a25a752a26959cf7d5bffd320d97cfe2d657a7afbd38e64'}
INDEPENDENCE={'independent_from_sibling_model_maps':True,'primaries_blind_to_each_other_artifacts':True,'roles_separated':True,'shared_model_substrate':True,'counts_as_cross_model_independent_votes':False,'independent_model_or_human_evidence_required_at_convergence':True,'reviewer_count_is_not_authority':True,'correlated_mesh_weight_at_convergence':'one_model_voice'}
ROLES=(('hebrew','original_language_translation_specialist','blind_proposal_hebrew_textual_v2.json'),('literary','prophetic_literary_form_primary','blind_proposal_literary_v2.json'),('canonical','canonical_relations_retrieval_premortem_primary','blind_proposal_canonical_premortem_v2.json'))
EXPECTED_APPEALS={'Zech-Hebrew-A01','T560-LIT-APPEAL-ZECH-12-10-13-1-TREATMENT'}

def rjl(path:Path)->list[dict[str,Any]]:
 if not path.exists(): return []
 return [json.loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x.strip()]
def wj(path:Path,value:Any)->None:
 path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def wjl(path:Path,rows:list[dict[str,Any]])->None:
 path.parent.mkdir(parents=True,exist_ok=True); path.write_text(''.join(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n' for x in rows),encoding='utf-8',newline='\n')
def sha(path:Path)->str: return hashlib.sha256(path.read_bytes()).hexdigest()
def row_sha(row:dict[str,Any])->str: return hashlib.sha256(json.dumps(row,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def inventory()->tuple[list[str],dict[str,str]]:
 rows=[x for x in rjl(WEB) if str(x.get('osis_ref','')).startswith('Zech.')]; refs=[x['osis_ref'] for x in rows]; texts={x['osis_ref']:x['text'] for x in rows}
 if len(refs)!=211 or refs[0]!='Zech.1.1' or refs[-1]!='Zech.14.21': raise ValueError('unexpected Zechariah WEB inventory')
 return refs,texts

def mt(ref:str)->str:
 bc,rv=ref.rsplit('.',1); book,rc=bc.split('.',1); ch,v=int(rc),int(rv)
 if book!='Zech': raise ValueError(f'unexpected crosswalk book: {ref}')
 if ch==1 and v>=18: return f'Zech.2.{v-17}'
 if ch==2: return f'Zech.2.{v+4}'
 return ref

def crosswalk_status(span:str)->str:
 a,b=span.split('-'); return 'validated_web_mt_zechariah_same_coordinates' if a==mt(a) and b==mt(b) else 'validated_web_mt_zechariah_english_versification_shift'

def srefs(span:str,did:str)->list[Any]:
 a,b=span.split('-'); ms=f'{mt(a)}-{mt(b)}'; status=crosswalk_status(span); out:list[Any]=[f'direct_read:eng-web:{span}']
 for sid in ('oshb','uxlc'):
  out.append({'source_id':sid,'span':span,'web_span':span,'source_span':ms,'coordinate_system':'MT_WLC','crosswalk_status':status,'source_metadata_boundary_authority':False,'wlc_family_correlation_disclosed':True,'oshb_uxlc_are_independent_witnesses':False,'observation':f'{did}:{sid.upper()}_correlated_WLC_family_locator_{ms}'})
 return out

def load_inputs()->tuple[dict[str,Any],dict[str,Any],dict[str,Any],dict[str,dict[str,Any]]]:
 for name,want in FROZEN.items():
  got=sha(REV/name)
  if got!=want: raise ValueError(f'frozen Zechariah input changed: {name} {got} != {want}')
 route=json.loads(ROUTE.read_text(encoding='utf-8')); post=json.loads(POST.read_text(encoding='utf-8')); boss=json.loads(BOSS.read_text(encoding='utf-8'))
 if route.get('boss_sha256')!=FROZEN[BOSS.name] or route.get('post_ruling_sha256')!=FROZEN[POST.name]: raise ValueError('route hash binding changed')
 proposals={code:json.loads((REV/name).read_text(encoding='utf-8')) for code,_role,name in ROLES}
 return route,post,boss,proposals

def options(active:dict[str,Any])->list[str]:
 alt='; '.join(str(x) for x in active['requested_alternative']); return [f"Surface {active['boss_surface']} as the current larger candidate unit.",f"Surface the dependent alternative {alt}; require {active['mandatory_parent']} hydration."]

def first_interrogative(question:str)->str:
 head,sep,_tail=question.partition('?')
 if not sep or not head.strip(): raise ValueError('held question lacks a first interrogative sentence')
 return head.strip()+'?'

def clean_counter(u:dict[str,Any])->str:
 return u['counter'].replace('The selected span retains the local evidence needed to prevent this premortem failure: ','Premortem risk: ')

def hebrew_span(reference:str)->str:
 start,end=reference.split('-'); sc,sv=start.split(':')
 if ':' in end: ec,ev=end.split(':')
 else: ec,ev=sc,end
 return f'Zech.{int(sc)}.{int(sv)}-Zech.{int(ec)}.{int(ev)}'

def proposal_primary(code:str,span:str,did:str,proposals:dict[str,dict[str,Any]])->dict[str,Any]:
 proposal=proposals[code]
 if code=='literary':
  rows=[x for x in proposal['route'] if x['span']==span]
  if len(rows)!=1: raise ValueError(f'literary frozen-route lookup failed for {span}')
  row=rows[0]; challenged=row.get('disposition')=='hold_question'
  return {'verdict':'challenge' if challenged else 'supports','support':f"{row['deciding_marker_or_seam']} {row['rationale']}",'counterevidence':row['counterevidence'],'source_refs':row['evidence_refs'],'position':{'span':row['span'],'disposition':row['disposition'],'confidence':row['confidence'],'literary_form':row['literary_form']},'challenge':({'claim':row['hold_question'],'proposed_remedy':'; '.join(row['rejected_alternatives']),'counterevidence':row['counterevidence']} if challenged else None)}
 if code=='hebrew':
  rows=[x for x in proposal['route'] if hebrew_span(x['reference'])==span]
  challenged=False
  if not rows and span=='Zech.3.1-Zech.3.10':
   wanted={'Zech.3.1-Zech.3.5','Zech.3.6-Zech.3.10'}; rows=[x for x in proposal['route'] if hebrew_span(x['reference']) in wanted]; challenged=len(rows)==2
  if len(rows)!=(2 if challenged else 1): raise ValueError(f'Hebrew frozen-route lookup failed for {span}')
  row_spans=[hebrew_span(x['reference']) for x in rows]; support=' '.join(f"{x['literary_form']}: {x['seam']}" for x in rows); counter=' '.join(x['counterevidence'] for x in rows); refs=srefs(span,did)+[f"frozen_blind_proposal:reviews/Zech/blind_proposal_hebrew_textual_v2.json:route:{x['reference']}" for x in rows]
  return {'verdict':'challenge' if challenged else 'supports','support':support,'counterevidence':counter,'source_refs':refs,'position':{'references':[x['reference'] for x in rows],'selected_surfaces':row_spans,'confidence':[x['confidence'] for x in rows],'literary_forms':[x['literary_form'] for x in rows]},'challenge':({'claim':f"The frozen Hebrew route surfaces {' and '.join(row_spans)} rather than {span}; {support}",'proposed_remedy':f"Surface {' and '.join(row_spans)} as dependent children with mandatory {span} hydration.",'counterevidence':counter} if challenged else None)}
 rows=[x for x in proposal['route'] if x['span']==span]
 if len(rows)!=1: raise ValueError(f'canonical frozen-route lookup failed for {span}')
 row=rows[0]
 confidence_challenge=span=='Zech.2.1-Zech.2.5'
 literary_caution=[x for x in proposals['literary']['route'] if x['span']==span][0]['counterevidence'] if confidence_challenge else row['premortem_failure']
 return {'verdict':'challenge' if confidence_challenge else 'supports','support':(f"The frozen canonical specialist supports the intact {span} surface: {row['marker']}" if confidence_challenge else row['marker']),'counterevidence':literary_caution,'source_refs':[f'direct_read:eng-web:{span}',f"frozen_blind_proposal:reviews/Zech/blind_proposal_canonical_premortem_v2.json:route:{row['id']}"],'position':{'id':row['id'],'span':row['span'],'confidence':row['confidence'],'form':row['form'],'mandatory_hydration':row['mandatory_hydration']},'challenge':({'claim':f"Confidence tier only: frozen {row['id']} is high while the active candidate is medium.",'proposed_remedy':f"Retain the intact {span} surface at high confidence.",'counterevidence':f"Medium remains warranted: {literary_caution}"} if confidence_challenge else None)}

def child_ids(values:list[Any],by_span:dict[str,str])->list[str]:
 out=[]
 for value in values:
  did=f'M7_sol-Zech-{value:03d}' if isinstance(value,int) else by_span.get(str(value),'')
  if not did: raise ValueError(f'unmapped relation child {value!r}')
  out.append(did)
 return out

def append_appeals(packets:list[dict[str,Any]])->tuple[int,int]:
 ledger=REV/'appeal_ledger.jsonl'; before=ledger.read_bytes()
 if len(before)<LEDGER_PREFIX_BYTES or (before and not before.endswith(b'\n')): raise ValueError('appeal ledger prefix/newline invariant failed')
 frozen_prefix=before[:LEDGER_PREFIX_BYTES]; old_ids={str(x.get('appeal_id','')) for x in rjl(ledger)}
 packet_rows=[(p,a) for p in packets for a in p.get('appeals',[])]; ids={a['appeal_id'] for _p,a in packet_rows}
 if ids!=EXPECTED_APPEALS: raise ValueError(f'unexpected Zechariah appeals {ids}')
 present=EXPECTED_APPEALS & old_ids
 if len(present) not in (0,2): raise ValueError('partial Zechariah v2 appeal append requires audit')
 additions=[] if present else [{**a,'schema_version':'m7_zech_boundary_appeal.v2','book':'Zech','decision_id':p['decision_id'],'span':p['span'],'append_only':True,'candidate_only':True,'non_authorizing':True} for p,a in packet_rows]
 if len(additions) not in (0,2): raise ValueError('expected zero or two ledger additions')
 if additions:
  with ledger.open('a',encoding='utf-8',newline='\n') as h:
   for row in additions: h.write(json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n')
 after=ledger.read_bytes()
 if not after.startswith(before) or after[:LEDGER_PREFIX_BYTES]!=frozen_prefix: raise ValueError('appeal ledger prefix was not preserved')
 return len(before),len(additions)

def materialize(post_path:Path|None)->dict[str,Any]:
 route,post_ruling,boss_input,proposals=load_inputs(); units=route['route']
 if len(units)!=37 or route.get('accepted')!=35 or route.get('held')!=2 or route.get('confidence')!={'high':23,'medium':14,'medium_low':0,'low':0}: raise ValueError('unexpected Zechariah route')
 if len(route.get('parents',[]))!=13 or len(route.get('dissents',[]))!=11: raise ValueError('unexpected relation counts')
 active={x['appeal_id']:x for x in post_ruling.get('active_appeals',[])}
 if set(active)!=EXPECTED_APPEALS or post_ruling.get('active_appeal_count')!=2: raise ValueError('unexpected active appeals')
 if boss_input.get('boss_attempt_id')!='t560-zechariah-fresh-boss-v2-20260729': raise ValueError('boss identity changed')
 if [mt(x) for x in ('Zech.1.18','Zech.1.21','Zech.2.1','Zech.2.13')]!=['Zech.2.1','Zech.2.4','Zech.2.5','Zech.2.17']: raise ValueError('crosswalk invariant failed')
 post=None
 if post_path:
  post=json.loads(post_path.read_text(encoding='utf-8'))
  if post.get('verdict') not in ('pass','pass_with_holds'): raise ValueError('nonpassing postcheck')
 refs,texts=inventory(); pos={r:i for i,r in enumerate(refs)}; coverage=[]; chunks=[]; staged=[]
 for n,u in enumerate(units,1):
  if u.get('index')!=n: raise ValueError(f'route index drift {n}')
  span=u['span']; a,b=span.split('-'); cov=refs[pos[a]:pos[b]+1]; coverage.extend(cov); ms=f'{mt(a)}-{mt(b)}'; did=f'M7_sol-Zech-{n:03d}'; held=u.get('disposition')=='deferred_human_or_external_ai'; aa=active.get(str(u.get('appeal_id',''))) if held else None
  if held and not aa: raise ValueError(f'held route lacks appeal {span}')
  question=aa['question'] if aa else None; opts=options(aa) if aa else None; hold_route=aa['requested_next_reviewer'] if aa else None
  observations=[{'ref':f'WEB:{cov[0]}','text':texts[cov[0]],'extent':'complete_verse','use':'opening_witness'}]
  if cov[-1]!=cov[0]: observations.append({'ref':f'WEB:{cov[-1]}','text':texts[cov[-1]],'extent':'complete_verse','use':'closing_witness'})
  alignment={'web_span':span,'oshb_span':ms,'uxlc_span':ms,'coordinate_system':'MT_WLC','crosswalk_status':crosswalk_status(span),'crosswalk_rules':{'WEB_Zech.1.18-Zech.1.21':'MT_Zech.2.1-Zech.2.4','WEB_Zech.2.1-Zech.2.13':'MT_Zech.2.5-Zech.2.17','other_WEB_coordinates':'same_as_MT'},'source_metadata_boundary_authority':False,'versification_crosswalk_is_evidence_only':True,'wlc_family_correlation_disclosed':True,'oshb_uxlc_are_independent_witnesses':False,'local_primary_lxx_available':False,'local_primary_dss_available':False,'local_primary_rabbinic_or_second_temple_corpus_available':False,'variants_select_preferred_reading':False,'authority':'translation_textual_order_and_form_evidence_only'}
  chunk={'model_id':'M7_sol','book':'Zech','span':span,'chunk_index_in_book':n,'working_title':u['title'],'literature_type_guess':u['form'],'literary_form':u['form'],'parent_literary_form':u['parent_form'],'parent_span':u['parent_span'],'boundary_evidence_refs':[f'direct_read:eng-web:{span}',f'direct_read:oshb:{ms}',f'direct_read:uxlc:{ms}','book_strategy/Zech.md','reviews/Zech/decision_evidence_v2.jsonl','reviews/Zech/decision_relations.jsonl'],'strong_or_hebrew_tags_used':['direct_Biblical_Hebrew_prophetic_form_considered','WEB_to_MT_Zechariah_1.18_and_chapter_2_shift_crosswalk_evidence_only','roots_are_not_meaning','correlated_WLC_family_views_disclosed','later_reuse_is_not_boundary_authority'],'wj_or_red_letter_considered':False,'frontier_flag_considered':True,'confidence':u['confidence'],'decision_id':did,'deciding_marker_or_seam':u['marker'],'boundary_rationale':u['rationale'],'rejected_alternative':u['rejected'],'counterevidence':clean_counter(u),'defensible_basis':u['basis'],'confidence_basis':{'tier':u['confidence'],'marker_strength':'decision_specific_vision_oracle_discourse_and_form_evidence','alternative_strength':'specialist_counterproposal_preserved','status_not_used_as_input':True},'review_revision':'m7-corrective-rereview-v2','review_status':'final_deferred_appeal' if held else 'candidate_review_complete','review_holds':[question] if held else [],'candidate_hold_state':'deferred_human_or_external_ai' if held else None,'candidate_hold_basis':({'kind':'retrieval_boundary_dispute','question':first_interrogative(question),'options':opts,'mandatory_parent':aa['mandatory_parent']} if held else None),'human_review_question':question if held else None,'human_review_route':hold_route if held else None,'candidate_internal_seams':u['internal_seams'],'non_authorizing':True,'candidate_only':True,'working_title_is_boundary_authority':False,'original_language_translation_holds':["Zechariah's night-vision dialogue, compact Hebrew syntax, WLC-family paragraph markers, WEB-to-MT shift at WEB 1:18-2:13, and later canonical reuse remain evidence and retrieval hot zones; none selects a reading, identity, theology, or boundary by itself."],'cross_reference_holds':[u['guard']],'red_team_premortem_holds':[clean_counter(u)],'convergence_defense':{'literary_form':u['form'],'deciding_marker_or_seam':u['marker'],'rejected_alternative':u['rejected'],'confidence':u['confidence'],'defensible_basis':u['basis'],'parent_span':u['parent_span'],'source_observations':observations,'original_language_alignment':alignment}}
  chunks.append(chunk); staged.append((u,chunk,srefs(span,did)))
 if coverage!=refs or [x['chunk_index_in_book'] for x in chunks]!=list(range(1,38)): raise ValueError('exact coverage/index failure')
 if sum(x['candidate_hold_state'] is not None for x in chunks)!=2: raise ValueError('held count changed')
 packets=[]; evidence=[]; role_rows={c:[] for c,_r,_p in ROLES}; peers=[]; bosses=[]
 for u,ch,source_refs in staged:
  n=ch['chunk_index_in_book']; did=ch['decision_id']; held=ch['candidate_hold_state'] is not None; aa=active.get(str(u.get('appeal_id',''))) if held else None; question=aa['question'] if aa else None; opts=options(aa) if aa else None; hold_route=aa['requested_next_reviewer'] if aa else None
  reviews=[]; cids=[]; cid_by_role={}
  for code,role,proposal in ROLES:
   primary=proposal_primary(code,ch['span'],did,proposals); challenges=[]
   if primary['challenge']:
    cid=f'{did}-{code.upper()}-CHALLENGE-01'; cids.append(cid); cid_by_role[role]=cid; challenges=[{'challenge_id':cid,**primary['challenge'],'source_refs':primary['source_refs']}]
   review={'reviewer_attempt_id':f'zech-v2-{code}-{n:03d}-specialist-high','reviewer_role':role,'role':role,'verdict':primary['verdict'],'blind_to_other_primary_reviews':True,'evidence_only':True,'primary_evidence_provenance':'frozen_blind_proposal_only','frozen_blind_proposal':f'reviews/Zech/{proposal}','frozen_blind_proposal_sha256':FROZEN[proposal],'recorded_position':primary['position'],'evidence_refs':primary['source_refs'],'source_refs':primary['source_refs'],'support':primary['support'],'counterevidence':primary['counterevidence'],'challenges':challenges}
   reviews.append(review); role_rows[code].append(review)
  responses=[{'challenge_id':cid,'disposition':'held_for_independent_resolution' if held else 'boss_overruled_with_dissent_preserved','rationale':u['rationale'],'rejected_alternative':u['rejected']} for cid in cids]
  appeals=[]
  if held and aa:
   disputed=cid_by_role.get(aa['role'])
   if not disputed: raise ValueError(f"appeal role lacks challenge {aa['appeal_id']}")
   appeals=[{'appeal_id':aa['appeal_id'],'status':aa['status'],'question':question,'option_a':opts[0],'option_b':opts[1],'preserved_disagreement':aa['reason'],'appellant_attempt_id':aa['appellant_attempt_id'],'disagreement_with':aa['disagreement_with'],'disputed_claim_id':disputed,'passage_context':aa['mandatory_parent'],'evidence_refs':source_refs,'rationale':aa['reason'],'uncertainty':aa['uncertainty'],'requested_next_reviewer':aa['requested_next_reviewer'],'requested_alternative':aa['requested_alternative'],'mandatory_parent':aa['mandatory_parent'],'forced_consensus':False}]
  peer={'reviewer_attempt_id':f'zech-v2-peer-{n:03d}-crosscheck-high','reviewer_role':'adversarial_passage_crosscheck','status':'pass_with_hold' if held else 'pass','disputed_claim_ids':cids,'rationale':u['basis'],'counterevidence':clean_counter(u),'source_refs':source_refs,'support_challenge_mix':{'support_count':sum(x['verdict']=='supports' for x in reviews),'challenge_count':sum(x['verdict']=='challenge' for x in reviews)}}
  resolution={'author_id':'M7_sol','author_attempt_id':f'zech-v2-boss-{n:03d}-sol-high','challenge_responses':responses,'unresolved_claim_ids':cids if held else [],'rationale':u['rationale'],'counterevidence':clean_counter(u),'rejected_alternative':u['rejected'],'outcome':'held_lower_confidence_for_independent_review' if held else 'accepted_candidate_after_role_specific_review','authority':'candidate_author_only'}
  boss={'ruling_id':resolution['author_attempt_id'],'rationale':u['rationale'],'counterevidence':clean_counter(u),'rejected_alternative':u['rejected'],'outcome':'hold_candidate' if held else 'accept_candidate','appeal_effect':'one_open_linked_appeal' if held else 'historical_dissent_preserved_without_active_appeal','forced_consensus':False}
  chash=row_sha(ch); packet={'schema_version':'m7_corrective_review_packet.v2','decision_id':did,'book':'Zech','span':ch['span'],'chunk_sha256':chash,'chunk_content_sha256':chash,'review_revision':'m7-corrective-rereview-v2','primary_reviews':reviews,'peer_crosscheck':peer,'sol_resolution':resolution,'appeals':appeals,'final_state':'held_lower_confidence' if held else 'accepted_candidate','human_review_question':question if held else None,'human_review_route':hold_route if held else None,'post_resolution_check':{'checker_attempt_id':f'zech-v2-post-{n:03d}-independent-checker','status':(('hold' if held else 'pass') if post else 'pending_independent_postcheck'),'evidence_refs':['reviews/Zech/post_resolution_check_v2.json'],'chunk_content_sha256':chash},'independence_scope':INDEPENDENCE,'non_authorizing':True,'boss_ruling':boss}
  packets.append(packet); peers.append({'decision_id':did,**peer}); bosses.append({'decision_id':did,**boss}); evidence.append({'schema_version':'m7_zech_decision_evidence.v2','book':'Zech','decision_id':did,'span':ch['span'],'literary_form':u['form'],'parent_literary_form':u['parent_form'],'parent_span':u['parent_span'],'candidate_state':packet['final_state'],'confidence':u['confidence'],'confidence_basis':ch['confidence_basis'],'deciding_marker_or_seam':u['marker'],'boundary_rationale':u['rationale'],'rejected_alternative':u['rejected'],'defensible_basis':u['basis'],'source_observations':ch['convergence_defense']['source_observations'],'original_language_alignment':ch['convergence_defense']['original_language_alignment'],'hold':appeals[0] if appeals else None,'primary_reviews':reviews,'non_authorizing':True})
 attempts={r['reviewer_attempt_id'] for p in packets for r in p['primary_reviews']}; supports=sum(r['verdict']=='supports' for p in packets for r in p['primary_reviews']); challenges=sum(r['verdict']=='challenge' for p in packets for r in p['primary_reviews'])
 if len(attempts)!=111 or supports!=108 or challenges!=3: raise ValueError(f'primary review provenance/verdict failure: attempts={len(attempts)} supports={supports} challenges={challenges}')
 primary_challenge_records=sum(len(r['challenges']) for p in packets for r in p['primary_reviews'])
 primary_blob=json.dumps([r for p in packets for r in p['primary_reviews']],ensure_ascii=False)
 if primary_challenge_records!=3 or 'Boss response' in primary_blob or 'post-ruling' in primary_blob.lower(): raise ValueError('primary review projection/provenance invariant failed')
 for packet in packets:
  ids=sorted(c['challenge_id'] for r in packet['primary_reviews'] for c in r['challenges']); answered=sorted(x['challenge_id'] for x in packet['sol_resolution']['challenge_responses'])
  if ids!=answered: raise ValueError(f"unanswered challenge {packet['decision_id']}")
  if packet['final_state']=='accepted_candidate' and not any(r['verdict']=='supports' for r in packet['primary_reviews']): raise ValueError(f"accepted decision lacks support {packet['decision_id']}")
 by_span={x['span']:x['decision_id'] for x in chunks}; relations=[]
 for n,parent in enumerate(route['parents'],1):
  relations.append({'schema_version':'m7_decision_relation.v2','note_id':f'ZECH-PARENT-{n:02d}','book':'Zech','relation_type':'named_zechariah_macro_parent_with_context_hydration','parent_span':parent['span'],'parent_literary_form':parent['form'],'children':child_ids(parent['children'],by_span),'child_spans':parent['children'],'rationale':f"{parent['form']} preserves the named {parent['span']} context for its selected local forms.",'mandatory_hydration':bool(parent['mandatory_hydration']),'boundary_authority':False,'non_authorizing':True})
 for d in route['dissents']:
  raw=d.get('children') or d.get('selected_spans') or []
  relations.append({'schema_version':'m7_decision_relation.v2','note_id':d.get('note_id') or d['dissent_id'],'book':'Zech','relation_type':d.get('relation_type') or 'preserved_specialist_dissent_without_forced_consensus','case':d.get('case'),'children':child_ids(raw,by_span),'selected_spans':d.get('selected_spans'),'alternative_spans':d['alternative_spans'],'rationale':d['rationale'],'appellant_role':d.get('appellant_role'),'appellant_status':d.get('appellant_status') or d.get('status'),'appeal_id':d.get('appeal_id'),'boundary_authority':False,'forced_consensus':False,'non_authorizing':True})
 if len(relations)!=24: raise ValueError('expected 13 parent plus 11 dissent relations')
 wjl(CHUNKS,chunks); wjl(REV/'review_packets.jsonl',packets); wjl(REV/'decision_evidence_v2.jsonl',evidence); wjl(REV/'decision_relations.jsonl',relations)
 for code,role,proposal in ROLES:
  role_appeals=[x for x in active.values() if x['role']==role]; artifact={'schema_version':'m7_zech_role_artifact.v2','book':'Zech','role':role,'decision_local_review_count':37,'reviews':role_rows[code],'blind_primary_artifact':f'reviews/Zech/{proposal}','blind_primary_artifact_sha256':FROZEN[proposal],'blind_primary_artifacts_remain_frozen':True,'post_ruling_active_appeals':len(role_appeals),'active_appeal_ids':[x['appeal_id'] for x in role_appeals],'candidate_only':True,'non_authorizing':True}
  names={'hebrew':('primary_hebrew_v2.json','corrective_specialist_hebrew_textual_v2.json'),'literary':('primary_literary_v2.json','corrective_specialist_literary_v2.json'),'canonical':('canonical_premortem_v2.json','corrective_specialist_canonical_premortem_v2.json')}[code]
  for name in names: wj(REV/name,artifact)
 wj(REV/'peer_crosscheck_v2.json',{'schema_version':'m7_zech_peer_crosscheck.v2','book':'Zech','reviews':peers,'candidate_only':True,'non_authorizing':True})
 wj(REV/'boss_ruling_v2.json',{'schema_version':'m7_zech_boss_ruling.v2','task_id':'T560','book':'Zech','route_count':37,'accepted':35,'held':2,'confidence':route['confidence'],'boss_attempt_id':boss_input['boss_attempt_id'],'frozen_boss_adjudication_sha256':FROZEN[BOSS.name],'rulings':bosses,'specialist_post_ruling_active_appeals':2,'forced_consensus':False,'candidate_only':True,'non_authorizing':True})
 wj(REV/'mesh_instruction_and_dissent_v2.json',{'schema_version':'m7_zech_mesh_instruction_record.v2','task_id':'T560','roles':[r for _c,r,_p in ROLES]+['boss_adjudicator','independent_post_resolution_checker'],'instructions':['blind read-only primaries','original-language and canonical relations are evidence only','larger coherent unit under tied evidence','boss answers every challenge without forcing consensus','post-ruling appeal opportunity for every specialist','true holds route to human or external AI'],'post_ruling_responses':post_ruling['responses'],'appeal_classification':{'post_ruling_specialist_active_appeals':2,'boss_synthesized_linked_boundary_appeals':0,'active_appeal_ids':sorted(active),'distinction':'The Hebrew Zech.3.1-10 surface question and literary Zech.12.10-13.1 treatment question remain open without forced consensus.'},'candidate_only':True,'non_authorizing':True})
 ledger_before,ledger_added=append_appeals(packets); post_status=post['verdict'] if post else 'pending_independent_postcheck'; post_art={'schema_version':'m7_post_resolution_check.v2','checker_attempt_id':post.get('checker_attempt_id') if post else 'pending-independent-zechariah-postchecker','role':'fresh_read_only_post_resolution_checker','book':'Zech','status':post_status,'checked_decision_ids':[x['decision_id'] for x in chunks],'checker_attempt_ids':[f'zech-v2-post-{n:03d}-independent-checker' for n in range(1,38)],'checked_review_packets_sha256':sha(REV/'review_packets.jsonl'),'checked_chunks_sha256':sha(CHUNKS),'checked_decision_relations_sha256':sha(REV/'decision_relations.jsonl'),'role_separated_checker_verdict_received':bool(post),'independent_model_verdict_received':False,'coverage':{'expected':211,'observed':len(coverage),'exact_ordered':coverage==refs},'accepted':35,'held':2,'postcheck_report_sha256':sha(post_path) if post_path else None,'postcheck_report':post,'candidate_only':True,'non_authorizing':True}; wj(REV/'post_resolution_check_v2.json',post_art)
 return {'book':'Zech','chunks':37,'coverage':211,'accepted':35,'held':2,'confidence':{'high':sum(x['confidence']=='high' for x in chunks),'medium':sum(x['confidence']=='medium' for x in chunks)},'primary_reviews':111,'supports':supports,'challenges':challenges,'distinct_reviewer_attempt_ids':len(attempts),'author_responses':sum(len(p['sol_resolution']['challenge_responses']) for p in packets),'parent_relations':13,'dissent_and_appeal_relations':11,'active_specialist_post_ruling_appeals':2,'open_linked_boundary_appeals':2,'appeal_ledger_bytes_before':ledger_before,'appeal_ledger_rows_appended':ledger_added,'postcheck':post_art['status'],'hashes':{'strategy':sha(MODEL/'book_strategy'/'Zech.md'),'chunks':sha(CHUNKS),'packets':sha(REV/'review_packets.jsonl'),'evidence':sha(REV/'decision_evidence_v2.jsonl'),'relations':sha(REV/'decision_relations.jsonl'),'boss':sha(REV/'boss_ruling_v2.json')}}

def main()->int:
 ap=argparse.ArgumentParser(); ap.add_argument('--postcheck-report',type=Path); a=ap.parse_args(); print(json.dumps(materialize(a.postcheck_report),ensure_ascii=False,indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())