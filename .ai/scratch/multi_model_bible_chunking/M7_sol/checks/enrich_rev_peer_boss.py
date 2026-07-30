from __future__ import annotations
import json
from pathlib import Path
M=Path(__file__).resolve().parents[1];R=M/'reviews'/'Rev'
def load(n):return json.loads((R/n).read_text(encoding='utf-8-sig'))
def dump(n,o):(R/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def readj(n):return [json.loads(x) for x in (R/n).read_text(encoding='utf-8-sig').splitlines() if x.strip()]
def writej(n,rs):(R/n).write_text(''.join(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n' for x in rs),encoding='utf-8',newline='\n')
peer=load('peer_crosscheck_v1.json');families=peer['material_families'];assert len(families)==15
covered=[d for x in families for d in x['challenged_candidate_ids']];assert sorted(covered)==[f'M7_sol-Rev-{i:03d}' for i in range(1,58)] and len(covered)==57
boss=load('boss_ruling_v1.json');existing={x['challenge_id'] for x in boss['challenge_responses']}
for x in families:
 if x['family_id'] not in existing:boss['challenge_responses'].append({'challenge_id':x['family_id'],'decision_ids':x['challenged_candidate_ids'],'author_response':'Accept the material challenge. Retain selected vision unit(s) only at LOW confidence; preserve Greek larger seams, literary finer routes, canonical envelopes, attachments, variants, and appeals append-only; defer selection to a human or external AI.','disposition':'hold_larger_unit_deferred_human_or_external_ai','appeal_preserved':True,'authority':'candidate_author_only'})
boss['unresolved_claim_ids']=list(dict.fromkeys(boss.get('unresolved_claim_ids',[])+[x['family_id'] for x in families]));boss.update(peer_ruling='All fifteen peer challenge families, nine canonical envelopes, Greek larger seams, and literary finer routes remain preserved. No witness, reading, translation, punctuation, speaker identity, source, fulfillment, symbol referent, political figure, geography, authorship, date, history, chronology, recapitulation sequence, millennium, eschatological system, Christology, angelology, ecclesiology, empire policy, canon, doctrine, or theology selection.',external_or_human_review_still_required=True,forced_consensus=False,shared_model_substrate=True,counts_as_cross_model_independent_vote=False,non_authorizing=True);dump('boss_ruling_v1.json',boss)
by={d:x for x in families for d in x['challenged_candidate_ids']};packets=readj('review_packets.jsonl')
for q in packets:
 x=by[q['decision_id']];q['span_specific_peer_challenge']={'challenge_id':x['family_id'],'family':x['material_family'],'material_challenge':x['material_challenge'],'greek_larger_seam_test':x['greek_larger_seam_test'],'literary_finer_route_test':x['literary_finer_route_test'],'canonical_envelope_test':x['canonical_envelope_test'],'attachment_tests':x['attachment_tests'],'key_variant_tests':x['key_variant_tests'],'status':'deferred_human_or_external_ai','non_authorizing':True}
writej('review_packets.jsonl',packets);print(json.dumps({'families':len(families),'boss_responses':len(boss['challenge_responses']),'packets':len(packets)}))