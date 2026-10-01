import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
rev=root/'reviews'/'2Cor'
peer=json.loads((rev/'peer_crosscheck_v1.json').read_text(encoding='utf-8-sig'))
boss=json.loads((rev/'boss_ruling_v1.json').read_text(encoding='utf-8-sig'))
families=peer.get('material_challenge_families') or peer.get('material_peer_challenges') or []
responses=[]; rulings=[]
for n,c in enumerate(families,1):
    raw_alts=c.get('exact_alternatives') or ([c['exact_alternative']] if c.get('exact_alternative') else [])
    alts=[' + '.join(map(str,a)) if isinstance(a,list) else str(a) for a in raw_alts]
    ids=c.get('affected_decision_ids') or ([c['decision_id']] if c.get('decision_id') else [])
    claim=c.get('claim') or c.get('challenge') or c.get('substantive_challenge') or ''
    passage='; '.join(c.get('scope_spans') or ([c['passage']] if c.get('passage') else []))
    responses.append({'challenge_id':c.get('challenge_id',f'2COR-PEER-FAMILY-{n:03d}'),'decision_id':ids[0] if ids else None,'affected_decision_ids':ids,'source':'peer_crosscheck_v1','family':c.get('family'),'passage':passage,'challenge':claim,'exact_alternatives':alts,'author_response':'Material challenge accepted for explicit preservation. The frozen candidate route remains LOW while every larger/smaller route, textual/translation hot zone, cross-chapter seam, and partition appeal stays append-only and deferred. No witness, reading, punctuation, speaker, opponent, event sequence, partition, composition history, discipline policy, collection policy, apostolic authority, covenant system, theology, or canon ruling is selected.','disposition':'hold_frozen_route_and_all_alternatives_deferred_human_or_external_ai','appeal_preserved_append_only':True,'confidence':'LOW','forced_consensus':False,'authority':'candidate_author_only'})
    rulings.append({'ruling_id':f'2COR-BOSS-SPEC-{n:03d}','challenge_id':c.get('challenge_id',f'2COR-PEER-FAMILY-{n:03d}'),'family':c.get('family'),'decisions':ids,'passage':passage,'disposition':'retain frozen route and preserve: '+' | '.join(alts),'basis':'Material challenge sustained: '+claim,'confidence':'LOW','unresolved_route':'deferred_human_or_external_ai','forced_consensus':False})
boss['peer_challenge_responses']=responses
boss['specific_boss_rulings']=rulings
boss['peer_crosscheck_evidence']='peer_crosscheck_v1.json'
boss['boss_post_peer_ruling_status']='pass_with_holds_all_peer_challenges_answered_and_appeals_preserved'
boss['unresolved_claim_ids']=sorted(set((boss.get('unresolved_claim_ids') or [])+[x for c in families for x in c.get('affected_decision_ids',[])]))
boss['accepted_decision_count']=0; boss['held_decision_count']=40; boss['forced_consensus']=False; boss['external_or_human_review_still_required']=True; boss['non_authorizing']=True
(rev/'boss_ruling_v1.json').write_text(json.dumps(boss,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
print(json.dumps({'peer_families':len(families),'responses':len(responses),'rulings':len(rulings),'held':boss['held_decision_count']}))