from __future__ import annotations
import json
from pathlib import Path
M=Path(__file__).resolve().parents[1];R=M/'reviews'/'Jas'
def load(n):return json.loads((R/n).read_text(encoding='utf-8-sig'))
def dump(n,o):(R/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def readj(n):return [json.loads(x) for x in (R/n).read_text(encoding='utf-8-sig').splitlines() if x.strip()]
def writej(n,rs):(R/n).write_text(''.join(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n' for x in rs),encoding='utf-8',newline='\n')
def ids(a,b):return [f'M7_sol-Jas-{i:03d}' for i in range(a,b+1)]
specs=[
('F01',ids(1,3),'Selected 1:2-18 may flatten trials/wisdom, reversal, and temptation/gift chains; 1:19-27 retains command/doer/religion seams.',['1:2-8|1:9-12|1:13-18','1:2-4|1:5-8','1:9-11|1:12','1:13-15|1:16-18','1:19-21|1:22-25|1:26-27'],['1:1-27'],['peirasmos/source/gift syntax','speaker/authorship/history'],'RN-JAS-001'),
('F02',ids(4,5),'Partiality case may detach from law/mercy and imagined dialogue from examples/analogy.',['2:1-4|2:5-7|2:8-13','2:14-17|2:18-20|2:21-24|2:25-26'],['2:1-26'],['dialogue speaker','citation/source','faith-works doctrine','economic policy'],'RN-JAS-002'),
('F03',ids(6,7),'Tongue analogies and above/below wisdom conclusion may be atomized.',['3:1-2|3:3-6|3:7-12','3:13-16|3:17-18'],['3:1-18','3:13-4:10','3:1-4:17'],['translation/text','teacher policy','source/theology'],'RN-JAS-003'),
('F04',ids(8,10),'Conflict diagnosis/citation may detach from repentance; 4:5/source, lawgiver, and merchant correction seams remain live.',['4:1-3|4:4-6|4:7-10','4:1-5|4:6-10','4:11|4:12','4:13-14|4:15-17'],['3:13-4:10','3:1-4:17'],['4:5 speaker/source/identity/text','discipline/commerce/providence policy'],'RN-JAS-004'),
('F05',ids(11,11),'Rich-warning catalogue may atomize or select righteous-one identity.',['5:1-3|5:4-6'],['5:1-11','5:1-20'],['identity/source/economic policy/history'],'RN-JAS-005'),
('F06',ids(12,13),'Patience may detach from examples/mercy; oath seam may attach backward or forward.',['5:7-9|5:10-11'],['5:7-12','5:12-18','5:1-20'],['source/text','oath speaker','policy'],'RN-JAS-006'),
('F07',ids(14,15),'Prayer/healing cases may fragment and restoration subject/object may be settled.',['5:13|5:14-16|5:17-18','5:13-15|5:16-18'],['5:12-18','5:13-20','5:1-20'],['healing/office/prayer policy','identity/speaker/source/doctrine'],'RN-JAS-007')]
f=[]
for code,dids,claim,fine,large,holds,rn in specs:f.append({'challenge_id':f'JAS-PEER-{code}','decision_ids':dids,'claim':claim,'exact_finer_routes':fine,'exact_larger_routes':large,'unresolved_holds':holds,'evidence_refs':['book_chunks/Jas/chunks.jsonl','reviews/Jas/blind_proposal_greek_textual_v1.json','reviews/Jas/blind_proposal_literary_v1.json','reviews/Jas/blind_proposal_canonical_premortem_v1.json',f'decision_relations.jsonl#{rn}'],'proposed_remedy':'retain current unit(s) LOW and all routes append-only for human or external-AI adjudication','verdict':'material_challenge','status':'deferred_human_or_external_ai','forced_consensus':False,'non_authorizing':True})
peer=load('peer_crosscheck_v1.json');peer.update(attempt_id='jas-peer-crosscheck-20260724-d',reviewer_role='independent_peer_red_team_sol_high',status='pass_with_material_holds',macro_material_challenge_families=f,current_boundary_verdict='all_15_defensible_only_as_LOW_deferred_candidates',highest_seam_pressure=['M7_sol-Jas-002','M7_sol-Jas-013'],promotion_verdict='blocked_pending_external_or_human_cross_model_review',forced_consensus=False,shared_model_substrate=True,counts_as_cross_model_independent_vote=False,non_authorizing=True);peer['disputed_claim_ids']=list(dict.fromkeys(peer.get('disputed_claim_ids',[])+[x['challenge_id'] for x in f]));dump('peer_crosscheck_v1.json',peer)
boss=load('boss_ruling_v1.json')
for x in f:boss['challenge_responses'].append({'challenge_id':x['challenge_id'],'decision_ids':x['decision_ids'],'author_response':'Accept challenge. Retain unit(s) LOW; preserve all exact routes and guards append-only; defer selection.','disposition':'hold_larger_unit_deferred_human_or_external_ai','appeal_preserved':True,'authority':'candidate_author_only'})
boss['unresolved_claim_ids']=list(dict.fromkeys(boss.get('unresolved_claim_ids',[])+[x['challenge_id'] for x in f]));boss.update(peer_ruling='all seven macro challenges/four parents preserved; no speaker/source/identity, faith-works, economic/office/healing/discipline policy, authorship/history/canon/doctrine/theology selection',external_or_human_review_still_required=True,forced_consensus=False,non_authorizing=True);dump('boss_ruling_v1.json',boss)
by={d:x for x in f for d in x['decision_ids']};ps=readj('review_packets.jsonl')
for p in ps:
 x=by[p['decision_id']];p['span_specific_peer_challenge']={'challenge_id':x['challenge_id'],'claim':x['claim'],'exact_finer_routes':x['exact_finer_routes'],'exact_larger_routes':x['exact_larger_routes'],'unresolved_holds':x['unresolved_holds'],'status':'deferred_human_or_external_ai','non_authorizing':True}
writej('review_packets.jsonl',ps);print(json.dumps({'families':len(f),'boss_responses':len(boss['challenge_responses']),'packets':len(ps)}))