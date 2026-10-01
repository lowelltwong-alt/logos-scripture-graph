from __future__ import annotations
import json
from pathlib import Path
M=Path(__file__).resolve().parents[1];R=M/'reviews'/'Heb'
def load(n):return json.loads((R/n).read_text(encoding='utf-8-sig'))
def dump(n,o):(R/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def readj(n):return [json.loads(x) for x in (R/n).read_text(encoding='utf-8-sig').splitlines() if x.strip()]
def writej(n,rs):(R/n).write_text(''.join(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n' for x in rs),encoding='utf-8',newline='\n')
def ids(a,b):return [f'M7_sol-Heb-{i:03d}' for i in range(a,b+1)]
specs=[
('F01',ids(1,4),'Catena, warning, and Psalm 8 exposition may be detached.',['1:1-2|1:3-4','1:5-6|1:7-12|1:13-14'],['1:1-2:18'],['citation/speaker/witness/translation'],'RN-HEB-001'),
('F02',ids(5,6),'Chapter fallback and 4:12-13 proof-texting threaten the Psalm 95-rest-warning close.',['3:7-11|3:12-19|4:1-10|4:11-13','3:7-4:11|4:12-13'],['3:1-4:13'],['Spirit-speech/textual/lexical'],'RN-HEB-002'),
('F03',ids(7,9),'Confession/qualification and warning/remedy cross-chapter movements may be split.',['4:14-16|5:1-4|5:5-10','5:11-14|6:1-8|6:9-12','5:11-14|6:1-12'],['4:14-6:20'],['speaker/apostasy/priesthood'],'RN-HEB-003'),
('F04',ids(10,11),'Narrative/tithe and comparison/oath conclusions may detach.',['7:1-3|7:4-10','7:11-19|7:20-25|7:26-28'],['7:1-28','7:1-10:18'],['citation/genealogy/priesthood'],'RN-HEB-004'),
('F05',ids(12,12),'Main point, Jeremiah quotation, and 8:13 close may split.',['8:1-6|8:7-12|8:13'],['8:1-13','7:1-10:18'],['diatheke/speaker/covenant/supersession'],'RN-HEB-005'),
('F06',ids(13,15),'Cultic atomization and detached 9:27/Psalm40/Jeremiah proof texts threaten the argument.',['9:1-5|9:6-10','9:11-14|9:15-22|9:23-28','10:1-4|10:5-10|10:11-18'],['9:1-28','7:1-10:18'],['witness/diatheke/covenant/sacrifice'],'RN-HEB-006'),
('F07',ids(16,16),'10:25 and deliberate-sin warning may detach from access and endurance remedy.',['10:19-25|10:26-31|10:32-39','10:19-31|10:32-39'],['10:19-39','10:19-12:29'],['speaker/text/apostasy'],'RN-HEB-007'),
('F08',ids(17,17),'11:1 proof-texting and name atomization may erase catalogue frame/common close.',['11:1-3|11:4-12|11:13-16|11:17-31|11:32-38|11:39-40','11:1-2|11:3-31|11:32-40'],['11:1-40','10:19-12:29'],['textual/name-order/history/doctrine'],'RN-HEB-008'),
('F09',ids(18,19),'Race/discipline/Esau and Sinai-Zion/refusal conclusions may detach.',['12:1-3|12:4-13|12:14-17','12:18-24|12:25-29'],['12:1-29','10:19-12:29'],['speaker/citation/witness/supersession'],'RN-HEB-009'),
('F10',ids(20,22),'Topic/name atomization, 13:8 proof-texting, and travel/office reconstruction threaten the close.',['13:1-6|13:7-17|13:18-19','13:22|13:23|13:24-25'],['13:1-25'],['speaker/leadership/history'],'RN-HEB-010')]
f=[]
for code,dids,claim,fine,large,holds,rn in specs:f.append({'challenge_id':f'HEB-PEER-{code}','decision_ids':dids,'claim':claim,'exact_finer_routes':fine,'exact_larger_routes':large,'unresolved_holds':holds,'evidence_refs':['book_chunks/Heb/chunks.jsonl','reviews/Heb/blind_proposal_greek_textual_v1.json','reviews/Heb/blind_proposal_literary_v1.json','reviews/Heb/blind_proposal_canonical_premortem_v1.json',f'decision_relations.jsonl#{rn}'],'proposed_remedy':'retain current coherent unit(s) LOW and every exact route/parent append-only for human or external-AI adjudication','verdict':'material_challenge','status':'deferred_human_or_external_ai','forced_consensus':False,'non_authorizing':True})
peer=load('peer_crosscheck_v1.json');peer.update(attempt_id='heb-peer-crosscheck-20260724-d',reviewer_role='independent_peer_red_team_sol_high',status='pass_with_material_holds',macro_material_challenge_families=f,current_boundary_verdict='all_22_defensible_only_as_LOW_deferred_candidates',highest_seam_pressure=[f'M7_sol-Heb-{i:03d}' for i in [6,8,13,14,15,16,17,20,21,22]],promotion_verdict='blocked_pending_external_or_human_cross_model_review',forced_consensus=False,shared_model_substrate=True,counts_as_cross_model_independent_vote=False,non_authorizing=True);peer['disputed_claim_ids']=list(dict.fromkeys(peer.get('disputed_claim_ids',[])+[x['challenge_id'] for x in f]));dump('peer_crosscheck_v1.json',peer)
boss=load('boss_ruling_v1.json')
for x in f:boss['challenge_responses'].append({'challenge_id':x['challenge_id'],'decision_ids':x['decision_ids'],'author_response':'Accept challenge. Retain coherent unit(s) LOW; preserve all exact routes, six parents, and holds append-only; defer selection.','disposition':'hold_larger_unit_deferred_human_or_external_ai','appeal_preserved':True,'authority':'candidate_author_only'})
boss['unresolved_claim_ids']=list(dict.fromkeys(boss.get('unresolved_claim_ids',[])+[x['challenge_id'] for x in f]));boss.update(peer_ruling='all ten macro challenges and six parents preserved; no witness, speaker attribution, authorship, history, priesthood, covenant, sacrifice, apostasy, canon, supersession, fulfillment, doctrine, or theology selection',external_or_human_review_still_required=True,forced_consensus=False,non_authorizing=True);dump('boss_ruling_v1.json',boss)
by={d:x for x in f for d in x['decision_ids']};ps=readj('review_packets.jsonl')
for p in ps:
 x=by[p['decision_id']];p['span_specific_peer_challenge']={'challenge_id':x['challenge_id'],'claim':x['claim'],'exact_finer_routes':x['exact_finer_routes'],'exact_larger_routes':x['exact_larger_routes'],'unresolved_holds':x['unresolved_holds'],'status':'deferred_human_or_external_ai','non_authorizing':True}
writej('review_packets.jsonl',ps);print(json.dumps({'families':len(f),'boss_responses':len(boss['challenge_responses']),'packets':len(ps)}))