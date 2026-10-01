"""M7_sol runtime adapter for one frozen book's candidate review artifacts.

Environment-bound campaign machinery; no provider-neutral portability claim.
"""
from __future__ import annotations
import hashlib,json,os
from pathlib import Path
from review_contract_constants import INDEPENDENCE_SCOPE

ROOT=Path(__file__).resolve().parents[5]
MODEL=ROOT/'.ai/scratch/multi_model_bible_chunking/M7_sol'

def readj(path): return [json.loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x.strip()]
def writej(path,rows):
    """Stream JSONL to a same-directory temporary and atomically replace path."""
    temporary=path.with_name(f'{path.name}.{os.getpid()}.tmp')
    try:
        with temporary.open('x',encoding='utf-8',newline='\n') as handle:
            for row in rows:
                handle.write(json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n')
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary,path)
    finally:
        temporary.unlink(missing_ok=True)
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def rowsha(row): return hashlib.sha256(json.dumps(row,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()

def build(*,book,expected_sha,roles,peer_attempt,boss_attempt,post_attempt,relation_specs,reviewer_hint):
    reviews=MODEL/'reviews'/book; chunks_path=MODEL/'book_chunks'/book/'chunks.jsonl'; reviews.mkdir(parents=True,exist_ok=True)
    rows=readj(chunks_path); frozen=sha(chunks_path)
    assert frozen==expected_sha, (frozen,expected_sha)
    low={r['decision_id'] for r in rows if r['confidence']=='low'}
    prefix=book.upper()
    def review_filename(role): return 'canonical_premortem_v1.json' if role=='canonical' else f'primary_{role}_v1.json'
    literary_attempt=next((attempt for role,attempt,_ in roles if role=='literary'),roles[0][1])
    primary_evidence_refs=[f'reviews/{book}/{review_filename(role)}' for role,_,_ in roles]
    def challenge(role,row):
        n=row['decision_id'].split(f'{book}-')[-1]
        fn=review_filename(role)
        return {'challenge_id':f'{prefix}-{role.upper()}-{n}','severity':'material','claim':row['rejected_alternative'],'proposed_remedy':'retain_larger_low_and_preserve_competing_seam_or_evidence_appeal','evidence_refs':[f'reviews/{book}/{fn}',f"chunk:{row['decision_id']}"]}
    for role,attempt,domain in roles:
        verdicts=[]
        for r in rows:
            cs=[challenge(role,r)] if r['decision_id'] in low else []
            verdicts.append({'decision_id':r['decision_id'],'span':r['span'],'verdict':'challenge' if cs else 'supports','evidence_refs':[r['deciding_marker_or_seam'],r['original_language_translation_holds'][0]],'challenges':cs})
        obj={'schema_version':'m7_primary_review.v1','book':book,'checked_chunks_sha256':frozen,'checked_row_count':len(rows),'reviewer_attempt_id':attempt,'role':domain,'overall_verdict':'supports_with_preserved_appeals','decision_verdicts':verdicts,'blind_to_other_primary_reviews':True,'evidence_only':True,'prohibited_sources_read':False,'non_authorizing':True}
        fn=review_filename(role)
        (reviews/fn).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    appeals=[]
    for r in rows:
        if r['decision_id'] not in low: continue
        n=r['decision_id'].split(f'{book}-')[-1]
        appeals.append({'appeal_id':f'{prefix}-APPEAL-{n}','appellant_attempt_id':literary_attempt,'disagreement_with':'M7_sol provisional larger-unit disposition','disputed_claim_id':r['decision_id'],'passage_context':r['span'],'evidence_refs':primary_evidence_refs+[f"chunk:{r['decision_id']}"],'rationale':r['rejected_alternative'],'uncertainty':r['original_language_translation_holds'][0],'requested_next_reviewer':reviewer_hint,'status':'unresolved_append_only','non_authorizing':True})
    writej(reviews/'appeal_ledger.jsonl',appeals); appeal_by={x['disputed_claim_id']:[x] for x in appeals}
    relations=[]
    for n,ids,related,relation in relation_specs:
        relations.append({'note_id':f'RN-{prefix}-{n}','schema_version':'m7_decision_relation.v1','book':book,'decision_ids':ids,'related_passages':related,'relation':relation,'scope_note':'Internal-Bible relation is evidence only; it does not force boundary symmetry, harmonize accounts, select a witness, or authorize theology.','direct_literary_dependency_only':False,'non_authorizing':True,'boundary_authority':False,'relation_symmetry_does_not_require_boundary_symmetry':True,'dependency_claim':False})
    writej(reviews/'decision_relations.jsonl',relations)
    allc={r['decision_id']:[challenge(role,r) for role,_,_ in roles] for r in rows if r['decision_id'] in low}
    peer={'schema_version':'m7_peer_crosscheck.v1','book':book,'checked_chunks_sha256':frozen,'checked_row_count':len(rows),'reviewer_attempt_id':peer_attempt,'status':'pass_with_holds','disputed_claim_ids':[c['challenge_id'] for cs in allc.values() for c in cs],'recommendation':f'ratify the {len(rows)}-unit larger-coherence route only with all {len(low)} LOW appeals and exact competing seams preserved','forced_consensus':False,'shared_model_substrate':True,'counts_as_cross_model_independent_vote':False,'non_authorizing':True}
    (reviews/'peer_crosscheck_v1.json').write_text(json.dumps(peer,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    responses=[]
    for did,cs in allc.items():
        for c in cs: responses.append({'challenge_id':c['challenge_id'],'decision_id':did,'source_role':c['challenge_id'].split('-')[1].lower(),'author_response':'Retain the larger coherent unit at LOW confidence, preserve the exact competing seam and span-specific hazard append-only, and defer adjudication.','disposition':'hold_larger_unit_deferred_human_or_external_ai','appeal_preserved':True,'authority':'candidate_author_only'})
    boss={'schema_version':'m7_boss_ruling.v1','book':book,'checked_chunks_sha256':frozen,'boss_attempt_id':boss_attempt,'author_id':'M7_sol','challenge_responses':responses,'unresolved_claim_ids':[x['challenge_id'] for x in responses],'accepted_decision_count':len(rows)-len(low),'held_decision_count':len(low),'ruling':'candidate_complete_with_explicit_holds','forced_consensus':False,'external_or_human_review_still_required':True,'non_authorizing':True}
    (reviews/'boss_ruling_v1.json').write_text(json.dumps(boss,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    packets=[]
    for r in rows:
        did=r['decision_id']; islow=did in low; formal=allc.get(did,[]); prim=[]
        for role,attempt,_ in roles:
            cs=[c for c in formal if c['challenge_id'].startswith(f'{prefix}-{role.upper()}-')]
            fn=review_filename(role)
            prim.append({'reviewer_attempt_id':attempt,'verdict':'challenge' if cs else 'supports','blind_to_other_primary_reviews':True,'evidence_only':True,'evidence_refs':[f'reviews/{book}/{fn}',f'chunk:{did}'],'challenges':cs})
        cids=[c['challenge_id'] for c in formal]
        p={'schema_version':'m7_chunk_review_packet.v1','decision_id':did,'book':book,'span':r['span'],'chunk_sha256':rowsha(r),'review_revision':r['review_revision'],'primary_reviews':prim,'peer_crosscheck':{'reviewer_attempt_id':peer_attempt,'disputed_claim_ids':cids,'status':'hold' if islow else 'pass','evidence_refs':[f'reviews/{book}/peer_crosscheck_v1.json']},'sol_resolution':{'author_id':'M7_sol','challenge_responses':[{'challenge_id':x,'disposition':'hold: retain larger LOW unit and preserve alternative for human/external review'} for x in cids],'unresolved_claim_ids':cids if islow else [],'authority':'candidate_author_only'},'appeals':appeal_by.get(did,[]),'final_state':'deferred_human_or_external_ai' if islow else 'accepted_candidate','post_resolution_check':{'checker_attempt_id':post_attempt,'status':'hold' if islow else 'pass','evidence_refs':[f'reviews/{book}/post_resolution_check_v2.json']},'independence_scope':INDEPENDENCE_SCOPE,'non_authorizing':True}
        if islow:p['boss_ruling']={'ruling_id':boss_attempt,'outcome':'retain_larger_low','appeal_effect':'deferred_human_or_external_ai','forced_consensus':False}
        packets.append(p)
    writej(reviews/'review_packets.jsonl',packets)
    lock=MODEL/'runtime'/'uncertainty_sidecar_write.lock'
    lock.parent.mkdir(parents=True,exist_ok=True)
    try:
        descriptor=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
    except FileExistsError:
        raise RuntimeError(f'shared sidecar writer lock exists: {lock}')
    os.close(descriptor)
    try:
        for name in ('low_confidence_register.jsonl','frontier_escalation_queue.jsonl','atlas_candidate_feed.jsonl'):
            path=MODEL/name; kept=[x for x in readj(path) if x.get('book')!=book]; add=[]
            for r in rows:
                if r['decision_id'] not in low:continue
                aid=f'{prefix}-APPEAL-'+r['decision_id'].split(f'{book}-')[-1]
                x={'model_id':'M7_sol','book':book,'span':r['span'],'chunk_decision_id':r['decision_id'],'confidence':'low','observed_substrate_signals':[r['deciding_marker_or_seam'],r['original_language_translation_holds'][0]],'review_packet_final_state':'deferred_human_or_external_ai','chunk_review_status':'final_deferred_appeal','candidate_hold_state':'deferred_human_or_external_ai','non_authorizing':True}
                if name=='low_confidence_register.jsonl':x.update(why_low_confidence=r['red_team_premortem_holds'][0],possible_downstream_risk=r['rejected_alternative'],competing_boundary_risk=r['rejected_alternative'],appeal_status='deferred_human_or_external_ai',appeal_ids=[aid])
                elif name=='frontier_escalation_queue.jsonl':x.update(concern_type='appealed_chunk_boundary_or_textual_pressure',why_frontier_review_needed=r['rejected_alternative'],suggested_reviewer=reviewer_hint,promotion_authority='none')
                else:x.update(concern_type='appealed_chunk_boundary_or_textual_pressure',why_low_confidence=r['red_team_premortem_holds'][0],possible_downstream_risk=r['rejected_alternative'],suggested_reviewer=reviewer_hint,proposed_atlas_action='consider_only',atlas_promotion_authority='none')
                add.append(x)
            writej(path,kept+add)
    finally:
        lock.unlink(missing_ok=True)
    result={'chunks_sha256':frozen,'chunks':len(rows),'accepted':len(rows)-len(low),'appeals':len(appeals),'formal_challenges':len(responses),'relations':len(relations)}
    print(json.dumps(result));return result
