from __future__ import annotations
import json
from pathlib import Path
M=Path(__file__).resolve().parents[1];R=M/'reviews'/'3John'
def load(n):return json.loads((R/n).read_text(encoding='utf-8-sig'))
def dump(n,o):(R/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def readj(n):return [json.loads(x) for x in (R/n).read_text(encoding='utf-8-sig').splitlines() if x.strip()]
def writej(n,rs):(R/n).write_text(''.join(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n' for x in rs),encoding='utf-8',newline='\n')
peer=load('peer_crosscheck_v1.json');families=peer['macro_material_challenge_families'];assert len(families)==5
covered=[d for x in families for d in x['decision_ids']];assert sorted(covered)==[f'M7_sol-3John-{i:03d}' for i in range(1,6)] and len(covered)==5
boss=load('boss_ruling_v1.json');existing={x['challenge_id'] for x in boss['challenge_responses']}
for x in families:
 if x['challenge_id'] not in existing:boss['challenge_responses'].append({'challenge_id':x['challenge_id'],'decision_ids':x['decision_ids'],'author_response':'Accept the material challenge. Retain the selected larger coherent unit(s) only at LOW confidence; preserve every exact route, witness/source guard, and appeal append-only; defer selection to a human or external AI.','disposition':'hold_larger_unit_deferred_human_or_external_ai','appeal_preserved':True,'authority':'candidate_author_only'})
boss['unresolved_claim_ids']=list(dict.fromkeys(boss.get('unresolved_claim_ids',[])+[x['challenge_id'] for x in families]));boss.update(peer_ruling='All five peer challenge families and five literary units remain preserved. The official 14-coordinate and Greek 15-coordinate close remain evidence-only alternatives. No witness, reading, translation, versification tradition, speaker, source, identity, authorship, history, office, faction, mission, hospitality, finance, discipline policy, canon, doctrine, or theology selection.',external_or_human_review_still_required=True,forced_consensus=False,shared_model_substrate=True,counts_as_cross_model_independent_vote=False,non_authorizing=True);dump('boss_ruling_v1.json',boss)
by={d:x for x in families for d in x['decision_ids']};packets=readj('review_packets.jsonl')
for p in packets:
 x=by[p['decision_id']];p['span_specific_peer_challenge']={'challenge_id':x['challenge_id'],'family':x['family'],'material_challenge':x['material_challenge'],'exact_alternatives':x['exact_alternatives'],'prohibited_selections':x['prohibited_selections'],'status':'deferred_human_or_external_ai','non_authorizing':True}
writej('review_packets.jsonl',packets);print(json.dumps({'families':len(families),'boss_responses':len(boss['challenge_responses']),'packets':len(packets)}))