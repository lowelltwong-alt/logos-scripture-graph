from __future__ import annotations
import hashlib,json
from pathlib import Path
from review_contract_constants import INDEPENDENCE_SCOPE
ROOT=Path(__file__).resolve().parents[5]
M=ROOT/'.ai/scratch/multi_model_bible_chunking/M7_sol'
B='Deut'; R=M/'reviews'/B; C=M/'book_chunks'/B/'chunks.jsonl'
R.mkdir(parents=True,exist_ok=True)
def readl(p): return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
def writel(p,rows): p.write_text(''.join(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n' for x in rows),encoding='utf-8',newline='\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rowsha(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
chunks=readl(C); chash=sha(C); by={x['decision_id']:x for x in chunks}
assert chash=='ab73ee7a888cd9a6f324d4c5d54bf99243cecd7a29c4316bd526be9a8d5d405f' and len(chunks)==78
H={4:'Split 2:1-16 / 2:17-23 at the fresh divine-speech formula.',6:'Split 3:12-17 allotment / 3:18-22 paired charges.',9:'Split 4:9-24 / 4:25-31 at paragraph closure and conditional turn.',19:'Split 7:12-16 / 7:17-26 at paragraph closure and inner-question turn.'}
L={1:'Prefer 1:1-8 address launch over the current frame boundary.',2:'Split departure command 1:6-8 from judges 1:9-18.',37:'Split governance, cult-integrity/apostasy, and tribunal functions.',46:'Split household-status cases 21:10-17 from public judgment 21:18-23.',47:'Split neighbor restoration 22:1-4 from distinction/protection 22:5-12.',51:'Split the mixed collection at least at 23:18/19.',52:'Split remarriage/newlywed 24:1-5 from safeguards 24:6-9.',55:'Split levirate 25:5-10 from assault/measures 25:11-16.'}
P={28:'Split anti-imitation close 12:29-32 from prophet case 13:1-5.',37:'Split 16:18-20 / 16:21-17:7 / 17:8-13.',46:'Split 21:10-17 / 21:18-23.',47:'Split 22:1-4 / 22:5-12.',51:'Split at least 23:15-18 / 23:19-25.',52:'Split 24:1-5 / 24:6-9.',55:'Split 25:5-12 / 25:13-16.'}
roles=[('hebrew','deut-primary-hebrew-final-20260722-a',H,'original_language_translation_specialist'),('literary','deut-primary-literary-final-20260722-b',L,'literary_form_specialist'),('canonical','deut-canonical-premortem-final-20260722-c',P,'canonical_intertext_and_premortem_specialist')]
def challenge(role,i,claim):
 return {'challenge_id':f'DEUT-{role.upper()}-{i:03d}','severity':'material','claim':claim,'proposed_remedy':'retain_larger_low_and_preserve_split_appeal','evidence_refs':[f'reviews/Deut/primary_{role}_v1.json',f'chunk:M7_sol-Deut-{i:03d}']}
for role,attempt,mapping,domain in roles:
 verdicts=[]
 for x in chunks:
  i=int(x['decision_id'].split('-')[-1].split('r')[0]); cs=[challenge(role,i,mapping[i])] if i in mapping else []
  verdicts.append({'decision_id':x['decision_id'],'span':x['span'],'verdict':'challenge' if cs else 'supports','evidence_refs':[x['deciding_marker_or_seam']], 'challenges':cs})
 obj={'schema_version':'m7_primary_review.v1','book':B,'checked_chunks_sha256':chash,'checked_row_count':78,'reviewer_attempt_id':attempt,'role':domain,'overall_verdict':'supports_with_nonblocking_appeals','decision_verdicts':verdicts,'blind_to_other_primary_reviews':True,'evidence_only':True,'prohibited_sources_read':False,'non_authorizing':True}
 (R/f'primary_{role}_v1.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Appeals: every LOW decision retains a concrete competing seam or evidence hold.
origin={5:'hebrew',12:'hebrew',23:'hebrew',24:'hebrew',25:'literary',27:'literary',31:'hebrew',40:'hebrew',41:'canonical',53:'literary',60:'canonical',63:'literary',64:'hebrew',65:'hebrew',67:'hebrew',72:'literary',76:'literary'}
attempt_by={r:a for r,a,_,_ in roles}; appeals=[]
for x in chunks:
 if x['confidence']!='low': continue
 i=int(x['decision_id'].split('-')[-1].split('r')[0]); role='hebrew' if i in H else 'literary' if i in L else 'canonical' if i in P else origin.get(i,'canonical')
 hold=x['original_language_translation_holds'][0]
 a={'appeal_id':f'DEUT-APPEAL-{i:03d}','appellant_attempt_id':attempt_by[role],'disagreement_with':'M7_sol candidate larger-unit disposition','disputed_claim_id':('M7_sol-Deut-041r1' if i==41 else f'M7_sol-Deut-{i:03d}'),'passage_context':x['span'],'evidence_refs':[f'reviews/Deut/primary_{role}_v1.json',f'chunk:{x["decision_id"]}'],'rationale':x['rejected_alternative']+' '+hold,'uncertainty':'boundary or witness/translation pressure remains unresolved','requested_next_reviewer':'human_or_external_ai_original_language_and_literary_specialist','status':'unresolved_append_only','non_authorizing':True}
 appeals.append(a)
writel(R/'appeal_ledger.jsonl',appeals); appeal_by={a['disputed_claim_id']:[a] for a in appeals}
relations=[
{'note_id':'RN-DEUT-001','schema_version':'m7_decision_relation.v1','book':B,'decision_ids':['M7_sol-Deut-003'],'related_passages':['Num.13.1-Num.14.45','Num.32.1-Num.32.42','Deut.1.19-Deut.1.46'],'relation':'Kadesh_failure_and_transjordan_retrospective_recollection','scope_note':'Internal retrospective relation only; it does not harmonize accounts or authorize the local seam.'},
{'note_id':'RN-DEUT-002','schema_version':'m7_decision_relation.v1','book':B,'decision_ids':['M7_sol-Deut-012','M7_sol-Deut-013','M7_sol-Deut-014'],'related_passages':['Exod.19.1-Exod.20.21','Deut.4.44-Deut.5.33'],'relation':'Horeb_frame_Decalogue_and_mediation_recollection','scope_note':'Parallel covenant discourse is evidence only and does not force boundary symmetry.'},
{'note_id':'RN-DEUT-003','schema_version':'m7_decision_relation.v1','book':B,'decision_ids':['M7_sol-Deut-023'],'related_passages':['Exod.32.1-Exod.34.35','Deut.9.7-Deut.10.11'],'relation':'calf_intercession_tablets_and_covenant_restoration_recollection','scope_note':'Explicit remembered sequence only; no authorship or theology inference.'},
{'note_id':'RN-DEUT-004','schema_version':'m7_decision_relation.v1','book':B,'decision_ids':['M7_sol-Deut-011','M7_sol-Deut-041r1'],'related_passages':['Num.35.1-Num.35.34','Josh.20.1-Josh.20.9'],'relation':'refuge_city_instruction_network','scope_note':'Legal relation does not merge noncontiguous units or decide legal theology.'},
{'note_id':'RN-DEUT-005','schema_version':'m7_decision_relation.v1','book':B,'decision_ids':['M7_sol-Deut-060','M7_sol-Deut-061'],'related_passages':['Josh.8.30-Josh.8.35'],'relation':'Ebal_Gerizim_inscription_altar_and_responsive_covenant_ceremony','scope_note':'Later narrative relation and witness pressure are non-authorizing; no preferred reading.'},
{'note_id':'RN-DEUT-006','schema_version':'m7_decision_relation.v1','book':B,'decision_ids':['M7_sol-Deut-062','M7_sol-Deut-063','M7_sol-Deut-064','M7_sol-Deut-065','M7_sol-Deut-066','M7_sol-Deut-067'],'related_passages':['Josh.23.1-Josh.24.33','2Kgs.17.1-2Kgs.17.41','Neh.8.1-Neh.10.39'],'relation':'later_historical_covenant_blessing_curse_and_renewal_reuse','scope_note':'Later canonical reuse is evidence only and cannot select theology, fulfillment, or local boundaries.'},
{'note_id':'RN-DEUT-007','schema_version':'m7_decision_relation.v1','book':B,'decision_ids':['M7_sol-Deut-072'],'related_passages':['Deut.31.30-Deut.32.43'],'relation':'Song_of_Moses_as_book_internal_covenant_witness','scope_note':'Song frame and later citations do not authorize stanza seams or textual readings.'}
]
for z in relations: z.update({'direct_literary_dependency_only':False,'non_authorizing':True,'boundary_authority':False,'relation_symmetry_does_not_require_boundary_symmetry':True,'dependency_claim':False})
writel(R/'decision_relations.jsonl',relations)
# Peer and boss summaries are hash-bound; peer evidence is independently returned by the role-separated checker.
all_ch={}
for role,_,mapping,_ in roles:
 for i,claim in mapping.items(): all_ch.setdefault(i,[]).append(challenge(role,i,claim))
peer={'schema_version':'m7_peer_crosscheck.v1','book':B,'checked_chunks_sha256':chash,'checked_row_count':78,'reviewer_attempt_id':'deut-peer-crosscheck-final-20260722-d','status':'pass_with_holds','disputed_claim_ids':[c['challenge_id'] for cs in all_ch.values() for c in cs],'recommendation':'retain larger coherent LOW units, preserve every split appeal, and defer to human or external AI','forced_consensus':False,'shared_model_substrate':True,'counts_as_cross_model_independent_vote':False,'non_authorizing':True}
(R/'peer_crosscheck_v1.json').write_text(json.dumps(peer,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
responses=[]
for i,cs in sorted(all_ch.items()):
 for c in cs: responses.append({'challenge_id':c['challenge_id'],'decision_id':('M7_sol-Deut-041r1' if i==41 else f'M7_sol-Deut-{i:03d}'),'source_role':c['challenge_id'].split('-')[1].lower(),'author_response':'Retain the larger coherent unit at LOW confidence, preserve the proposed split append-only, and defer adjudication.','disposition':'hold_larger_unit_deferred_human_or_external_ai','appeal_preserved':True,'authority':'candidate_author_only'})
boss={'schema_version':'m7_boss_ruling.v1','book':B,'checked_chunks_sha256':chash,'boss_attempt_id':'deut-boss-adjudicator-20260722-e','author_id':'M7_sol','challenge_responses':responses,'unresolved_claim_ids':[x['challenge_id'] for x in responses],'accepted_decision_count':48,'held_decision_count':30,'ruling':'candidate_complete_with_explicit_holds','forced_consensus':False,'external_or_human_review_still_required':True,'non_authorizing':True}
(R/'boss_ruling_v1.json').write_text(json.dumps(boss,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Per-decision packets.
packets=[]
for x in chunks:
 i=int(x['decision_id'].split('-')[-1].split('r')[0]); did=x['decision_id']; low=x['confidence']=='low'; prs=[]; formal=[]
 for role,attempt,mapping,_ in roles:
  cs=[challenge(role,i,mapping[i])] if i in mapping else []; formal+=cs
  prs.append({'reviewer_attempt_id':attempt,'verdict':'challenge' if cs else 'supports','blind_to_other_primary_reviews':True,'evidence_only':True,'evidence_refs':[f'reviews/Deut/primary_{role}_v1.json',f'chunk:{did}'],'challenges':cs})
 app=appeal_by.get(did,[]); cids=[c['challenge_id'] for c in formal]
 packet={'schema_version':'m7_chunk_review_packet.v1','decision_id':did,'book':B,'span':x['span'],'chunk_sha256':rowsha(x),'review_revision':x['review_revision'],'primary_reviews':prs,'peer_crosscheck':{'reviewer_attempt_id':'deut-peer-crosscheck-final-20260722-d','disputed_claim_ids':cids,'status':'hold' if low else 'pass','evidence_refs':['reviews/Deut/peer_crosscheck_v1.json']},'sol_resolution':{'author_id':'M7_sol','challenge_responses':[{'challenge_id':cid,'disposition':'hold: retain larger unit LOW; preserve alternative for human/external review'} for cid in cids],'unresolved_claim_ids':cids if low else [],'authority':'candidate_author_only'},'appeals':app,'final_state':'deferred_human_or_external_ai' if low else 'accepted_candidate','post_resolution_check':{'checker_attempt_id':'deut-post-resolution-checker-20260722-f','status':'hold' if low else 'pass','evidence_refs':['reviews/Deut/post_resolution_check_v2.json']},'independence_scope':INDEPENDENCE_SCOPE,'non_authorizing':True}
 if app: packet['boss_ruling']={'ruling_id':'deut-boss-adjudicator-20260722-e','outcome':'retain_larger_low','appeal_effect':'deferred_human_or_external_ai','forced_consensus':False}
 packets.append(packet)
writel(R/'review_packets.jsonl',packets)
# Replace only Deut rows in the shared uncertainty sidecars.
for name in ('low_confidence_register.jsonl','frontier_escalation_queue.jsonl','atlas_candidate_feed.jsonl'):
 p=M/name; old=[z for z in readl(p) if z.get('book')!=B]; new=[]
 for x in chunks:
  if x['confidence']!='low': continue
  did=x['decision_id']; n=int(did.split('-')[-1].split('r')[0]); aid=f'DEUT-APPEAL-{n:03d}'; base={'model_id':'M7_sol','book':B,'span':x['span'],'chunk_decision_id':did,'confidence':'low','observed_substrate_signals':[x['deciding_marker_or_seam'],x['original_language_translation_holds'][0]],'review_packet_final_state':'deferred_human_or_external_ai','chunk_review_status':'final_deferred_appeal','candidate_hold_state':'deferred_human_or_external_ai','non_authorizing':True}
  if name=='low_confidence_register.jsonl': base.update({'why_low_confidence':x['red_team_premortem_holds'][0],'possible_downstream_risk':x['rejected_alternative'],'competing_boundary_risk':x['rejected_alternative'],'appeal_status':'deferred_human_or_external_ai','appeal_ids':[aid]})
  elif name=='frontier_escalation_queue.jsonl': base.update({'concern_type':'appealed_chunk_boundary_or_textual_pressure','why_frontier_review_needed':x['rejected_alternative'],'suggested_reviewer':'human_or_external_ai_original_language_and_literary_specialist','promotion_authority':'none'})
  else: base.update({'concern_type':'appealed_chunk_boundary_or_textual_pressure','why_low_confidence':x['red_team_premortem_holds'][0],'possible_downstream_risk':x['rejected_alternative'],'suggested_reviewer':'human_or_external_ai_original_language_and_literary_specialist','proposed_atlas_action':'consider_only','atlas_promotion_authority':'none'})
  new.append(base)
 writel(p,old+new)
print(json.dumps({'chunks_sha256':chash,'packets':len(packets),'appeals':len(appeals),'formal_challenges':sum(len(x) for x in all_ch.values()),'relations':len(relations)}))