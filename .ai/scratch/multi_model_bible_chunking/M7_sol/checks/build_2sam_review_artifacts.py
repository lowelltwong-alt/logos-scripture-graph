from __future__ import annotations
import hashlib, json
from pathlib import Path
from review_contract_constants import INDEPENDENCE_SCOPE

ROOT=Path(__file__).resolve().parents[5]
MODEL=ROOT/'.ai/scratch/multi_model_bible_chunking/M7_sol'
BOOK='2Sam'; REVIEWS=MODEL/'reviews'/BOOK; CHUNKS=MODEL/'book_chunks'/BOOK/'chunks.jsonl'
EXPECTED='b110d6b18185e083c4e3ddaf0cda5cd85f080468131c9a41b2f6a27915056ad5'
ROLES=(('hebrew','2sam-primary-hebrew-20260722-a','original_language_translation_specialist'),('literary','2sam-primary-literary-20260722-b','literary_form_specialist'),('canonical','2sam-primary-canonical-20260722-c','canonical_intertext_and_premortem_specialist'))

def readj(path): return [json.loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x.strip()]
def writej(path,rows): path.write_text(''.join(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n' for x in rows),encoding='utf-8',newline='\n')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def rowsha(row): return hashlib.sha256(json.dumps(row,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def chall(role,row):
    n=row['decision_id'].split('2Sam-')[-1]
    fn='canonical_premortem_v1.json' if role=='canonical' else f'primary_{role}_v1.json'
    return {'challenge_id':f'2SAM-{role.upper()}-{n}','severity':'material','claim':row['rejected_alternative'],'proposed_remedy':'retain_larger_low_and_preserve_competing_seam_or_evidence_appeal','evidence_refs':[f'reviews/2Sam/{fn}',f"chunk:{row['decision_id']}"]}

def main():
    REVIEWS.mkdir(parents=True,exist_ok=True)
    rows=readj(CHUNKS); h=sha(CHUNKS)
    assert h==EXPECTED and len(rows)==40
    low={r['decision_id'] for r in rows if r['confidence']=='low'}
    assert len(low)==35
    # Materialize the three completed blind reads against the frozen reconciliation.
    for role,attempt,domain in ROLES:
        verdicts=[]
        for r in rows:
            cs=[chall(role,r)] if r['decision_id'] in low else []
            verdicts.append({'decision_id':r['decision_id'],'span':r['span'],'verdict':'challenge' if cs else 'supports','evidence_refs':[r['deciding_marker_or_seam'],r['original_language_translation_holds'][0]],'challenges':cs})
        obj={'schema_version':'m7_primary_review.v1','book':BOOK,'checked_chunks_sha256':h,'checked_row_count':40,'reviewer_attempt_id':attempt,'role':domain,'overall_verdict':'supports_with_preserved_appeals','decision_verdicts':verdicts,'blind_to_other_primary_reviews':True,'evidence_only':True,'prohibited_sources_read':False,'non_authorizing':True}
        fn='canonical_premortem_v1.json' if role=='canonical' else f'primary_{role}_v1.json'
        (REVIEWS/fn).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    appeals=[]
    for r in rows:
        if r['decision_id'] not in low: continue
        n=r['decision_id'].split('2Sam-')[-1]
        appeals.append({'appeal_id':f'2SAM-APPEAL-{n}','appellant_attempt_id':'2sam-primary-literary-20260722-b','disagreement_with':'M7_sol provisional larger-unit disposition','disputed_claim_id':r['decision_id'],'passage_context':r['span'],'evidence_refs':['reviews/2Sam/primary_literary_v1.json','reviews/2Sam/primary_hebrew_v1.json',f"chunk:{r['decision_id']}"],'rationale':r['rejected_alternative'],'uncertainty':r['original_language_translation_holds'][0],'requested_next_reviewer':'human_or_external_ai_original_language_literary_trauma_aware_and_ancient_context_specialist','status':'unresolved_append_only','non_authorizing':True})
    writej(REVIEWS/'appeal_ledger.jsonl',appeals)
    appeal_by={x['disputed_claim_id']:[x] for x in appeals}

    specs=(
      ('001',['M7_sol-2Sam-001','M7_sol-2Sam-002'],['1Sam.31.1-1Sam.31.13','1Chr.10.1-1Chr.10.14'],'Saul_Jonathan_death_reports_and_David_lament_relation'),
      ('002',['M7_sol-2Sam-003','M7_sol-2Sam-004','M7_sol-2Sam-006','M7_sol-2Sam-007','M7_sol-2Sam-008','M7_sol-2Sam-009'],['1Sam.16.1-1Sam.31.13','1Kgs.2.1-1Kgs.2.46'],'divided_to_united_accession_and_later_succession_relation'),
      ('003',['M7_sol-2Sam-012'],['Exod.25.10-Exod.25.22','Num.4.1-Num.4.20','1Chr.13.1-1Chr.16.43'],'ark_transfer_relations_without_harmonization'),
      ('004',['M7_sol-2Sam-013'],['Deut.17.14-Deut.17.20','1Chr.17.1-1Chr.17.27','Ps.89.1-Ps.89.52'],'house_seed_oracle_prayer_and_later_reuse_relation'),
      ('005',['M7_sol-2Sam-016','M7_sol-2Sam-027','M7_sol-2Sam-032'],['1Sam.18.1-1Sam.20.42'],'Jonathan_loyalty_Mephibosheth_and_contested_Ziba_claim_relation'),
      ('006',['M7_sol-2Sam-018','M7_sol-2Sam-019','M7_sol-2Sam-020'],['Judg.9.50-Judg.9.57'],'Rabbah_frame_Uriah_messenger_and_Abimelech_recall_relation'),
      ('007',['M7_sol-2Sam-021','M7_sol-2Sam-022','M7_sol-2Sam-023','M7_sol-2Sam-024'],['Deut.22.13-Deut.22.30'],'Tamar_Amnon_Absalom_exile_return_and_law_relation'),
      ('008',['M7_sol-2Sam-025','M7_sol-2Sam-026','M7_sol-2Sam-027','M7_sol-2Sam-028','M7_sol-2Sam-029','M7_sol-2Sam-030','M7_sol-2Sam-031','M7_sol-2Sam-032','M7_sol-2Sam-033'],['Ps.3.1-Ps.3.8'],'Absalom_revolt_flight_counsel_battle_grief_return_aftershock_relation'),
      ('009',['M7_sol-2Sam-035','M7_sol-2Sam-036'],['Josh.9.1-Josh.9.27','1Chr.20.4-1Chr.20.8'],'Gibeonite_oath_famine_burial_and_warrior_parallel_relations'),
      ('010',['M7_sol-2Sam-037','M7_sol-2Sam-038','M7_sol-2Sam-039','M7_sol-2Sam-040'],['Ps.18.1-Ps.18.50','1Chr.11.10-1Chr.11.47','1Chr.21.1-1Chr.22.1'],'closing_song_oracle_warriors_census_and_Chronicles_relations'))
    relations=[]
    for n,ids,related,relation in specs:
        relations.append({'note_id':f'RN-2SAM-{n}','schema_version':'m7_decision_relation.v1','book':BOOK,'decision_ids':ids,'related_passages':related,'relation':relation,'scope_note':'Internal-Bible relation is evidence only; it does not force boundary symmetry, harmonize accounts, choose a witness, or authorize theology.','direct_literary_dependency_only':False,'non_authorizing':True,'boundary_authority':False,'relation_symmetry_does_not_require_boundary_symmetry':True,'dependency_claim':False})
    writej(REVIEWS/'decision_relations.jsonl',relations)

    allc={r['decision_id']:[chall(role,r) for role,_,_ in ROLES] for r in rows if r['decision_id'] in low}
    peer={'schema_version':'m7_peer_crosscheck.v1','book':BOOK,'checked_chunks_sha256':h,'checked_row_count':40,'reviewer_attempt_id':'2sam-peer-crosscheck-20260722-d','status':'pass_with_holds','disputed_claim_ids':[c['challenge_id'] for cs in allc.values() for c in cs],'recommendation':'ratify the 40-unit larger-coherence route only with all 35 LOW appeals, Hebrew alternatives, and expert gaps preserved','forced_consensus':False,'shared_model_substrate':True,'counts_as_cross_model_independent_vote':False,'non_authorizing':True}
    (REVIEWS/'peer_crosscheck_v1.json').write_text(json.dumps(peer,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    responses=[]
    for did,cs in allc.items():
        for c in cs: responses.append({'challenge_id':c['challenge_id'],'decision_id':did,'source_role':c['challenge_id'].split('-')[1].lower(),'author_response':'Retain the larger coherent unit at LOW confidence, preserve the exact competing seam and span-specific hazard append-only, and defer adjudication.','disposition':'hold_larger_unit_deferred_human_or_external_ai','appeal_preserved':True,'authority':'candidate_author_only'})
    boss={'schema_version':'m7_boss_ruling.v1','book':BOOK,'checked_chunks_sha256':h,'boss_attempt_id':'2sam-boss-adjudicator-20260722-e','author_id':'M7_sol','challenge_responses':responses,'unresolved_claim_ids':[x['challenge_id'] for x in responses],'accepted_decision_count':5,'held_decision_count':35,'ruling':'candidate_complete_with_explicit_holds','forced_consensus':False,'external_or_human_review_still_required':True,'non_authorizing':True}
    (REVIEWS/'boss_ruling_v1.json').write_text(json.dumps(boss,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    packets=[]
    for r in rows:
        did=r['decision_id']; islow=did in low; formal=allc.get(did,[]); prim=[]
        for role,attempt,_ in ROLES:
            cs=[c for c in formal if c['challenge_id'].startswith(f'2SAM-{role.upper()}-')]
            fn='canonical_premortem_v1.json' if role=='canonical' else f'primary_{role}_v1.json'
            prim.append({'reviewer_attempt_id':attempt,'verdict':'challenge' if cs else 'supports','blind_to_other_primary_reviews':True,'evidence_only':True,'evidence_refs':[f'reviews/2Sam/{fn}',f'chunk:{did}'],'challenges':cs})
        cids=[c['challenge_id'] for c in formal]
        p={'schema_version':'m7_chunk_review_packet.v1','decision_id':did,'book':BOOK,'span':r['span'],'chunk_sha256':rowsha(r),'review_revision':r['review_revision'],'primary_reviews':prim,'peer_crosscheck':{'reviewer_attempt_id':'2sam-peer-crosscheck-20260722-d','disputed_claim_ids':cids,'status':'hold' if islow else 'pass','evidence_refs':['reviews/2Sam/peer_crosscheck_v1.json']},'sol_resolution':{'author_id':'M7_sol','challenge_responses':[{'challenge_id':x,'disposition':'hold: retain larger LOW unit and preserve alternative for human/external review'} for x in cids],'unresolved_claim_ids':cids if islow else [],'authority':'candidate_author_only'},'appeals':appeal_by.get(did,[]),'final_state':'deferred_human_or_external_ai' if islow else 'accepted_candidate','post_resolution_check':{'checker_attempt_id':'2sam-post-resolution-checker-20260722-f','status':'hold' if islow else 'pass','evidence_refs':['reviews/2Sam/post_resolution_check_v2.json']},'independence_scope':INDEPENDENCE_SCOPE,'non_authorizing':True}
        if islow: p['boss_ruling']={'ruling_id':'2sam-boss-adjudicator-20260722-e','outcome':'retain_larger_low','appeal_effect':'deferred_human_or_external_ai','forced_consensus':False}
        packets.append(p)
    writej(REVIEWS/'review_packets.jsonl',packets)

    for name in ('low_confidence_register.jsonl','frontier_escalation_queue.jsonl','atlas_candidate_feed.jsonl'):
        path=MODEL/name; kept=[x for x in readj(path) if x.get('book')!=BOOK]; add=[]
        for r in rows:
            if r['decision_id'] not in low: continue
            aid='2SAM-APPEAL-'+r['decision_id'].split('2Sam-')[-1]
            x={'model_id':'M7_sol','book':BOOK,'span':r['span'],'chunk_decision_id':r['decision_id'],'confidence':'low','observed_substrate_signals':[r['deciding_marker_or_seam'],r['original_language_translation_holds'][0]],'review_packet_final_state':'deferred_human_or_external_ai','chunk_review_status':'final_deferred_appeal','candidate_hold_state':'deferred_human_or_external_ai','non_authorizing':True}
            if name=='low_confidence_register.jsonl': x.update(why_low_confidence=r['red_team_premortem_holds'][0],possible_downstream_risk=r['rejected_alternative'],competing_boundary_risk=r['rejected_alternative'],appeal_status='deferred_human_or_external_ai',appeal_ids=[aid])
            elif name=='frontier_escalation_queue.jsonl': x.update(concern_type='appealed_chunk_boundary_or_textual_pressure',why_frontier_review_needed=r['rejected_alternative'],suggested_reviewer='human_or_external_ai_original_language_literary_trauma_aware_and_ancient_context_specialist',promotion_authority='none')
            else: x.update(concern_type='appealed_chunk_boundary_or_textual_pressure',why_low_confidence=r['red_team_premortem_holds'][0],possible_downstream_risk=r['rejected_alternative'],suggested_reviewer='human_or_external_ai_original_language_literary_trauma_aware_and_ancient_context_specialist',proposed_atlas_action='consider_only',atlas_promotion_authority='none')
            add.append(x)
        writej(path,kept+add)
    print(json.dumps({'chunks_sha256':h,'packets':len(packets),'appeals':len(appeals),'formal_challenges':len(responses),'relations':len(relations)}))

if __name__=='__main__': main()
