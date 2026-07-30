import json
from pathlib import Path
M=Path(__file__).resolve().parents[1]; P=M/'book_chunks'/'Josh'/'chunks.jsonl'
rows=[json.loads(x) for x in P.read_text(encoding='utf-8').splitlines() if x.strip()]
assert len(rows)==53 and rows[5]['decision_id']=='M7_sol-Josh-006' and rows[6]['decision_id']=='M7_sol-Josh-007'
a=rows[5]
a.update({'decision_id':'M7_sol-Josh-006r1','span':'Josh.5.13-Josh.6.27','working_title':'Commander encounter Jericho instruction procession fall and closure','literature_type_guess':'numinous_encounter_and_battle_ritual_episode','literary_form':'numinous_encounter_and_battle_ritual_episode','confidence':'low','review_status':'final_deferred_appeal','candidate_hold_state':'deferred_human_or_external_ai','candidate_hold_basis':'preserved_appeal'})
marker='Josh.5.13 opens with a new perception and identity question; prostration and holy-ground command lead through Jericho status, sevenfold instruction, enacted procession, fall, Rahab rescue, destruction, curse, and fame closure at 6:27'
hold='Preserve both 5:13-15 / 6:1-27 and 5:13-6:5 / 6:6-27 alternatives. The larger LOW unit avoids choosing the disputed commander/6:2 speaker identity while keeping instruction with execution. The ḥērem/devoted-destruction language is a translation and interpretation hot zone, never seam authority.'
a['deciding_marker_or_seam']=marker+'.'; a['candidate_internal_seams']=[marker+'.',hold]; a['original_language_translation_holds']=[hold]; a['red_team_premortem_holds']=[hold]; a['rejected_alternative']='Preserved competing boundary/evidence alternatives for Josh.5.13-Josh.6.27: '+hold; a['boundary_rationale']='Prefer the larger procedural hold Josh.5.13-Josh.6.27 while speaker identity and the instruction/execution seam remain unresolved. '+marker+'.'; a['defensible_basis']='M7_sol-Josh-006r1: '+marker+'. The larger parent is a procedural hold, not an identity ruling or claim of indivisible form.'; a['review_evidence_summary']=marker+'. Evidence-only; no commander identity, theology, historicity, chronology, or preferred translation is selected.'
rows=rows[:6]+rows[7:]
for i,r in enumerate(rows,1): r['chunk_index_in_book']=i
for i,r in enumerate(rows):
 span=r['span']; start,end=span.split('-'); next_marker=rows[i+1]['deciding_marker_or_seam'] if i+1<len(rows) else 'The canonical book ends at Josh.24.33.'
 r['boundary_evidence_refs']=[f'direct_read:eng-web:{span}',f'direct_read:oshb:Josh.xml#{span}',f'direct_read:uxlc:Josh.xml#{span}','book_strategy/Josh.md','reviews/Josh/primary_hebrew_v1.json','reviews/Josh/primary_literary_v1.json','reviews/Josh/canonical_premortem_v1.json','reviews/Josh/peer_crosscheck_v1.json','reviews/Josh/boss_ruling_v1.json','reviews/Josh/decision_relations.jsonl']
 r['strong_or_hebrew_tags_used']=['direct_hebrew_wording_considered','source_metadata_corrob_only','roots_are_not_meaning','original_language_is_not_boundary_authority']
 if r['confidence']!='low': r['rejected_alternative']=f'Rejected expansion beyond {end} because the next observed movement opens as follows: {next_marker} The current unit retains its own stated closure before that concrete speaker, scene, ritual, register, or summary opening.'
 r['red_team_questions']=[f'Does the candidate seam after {end} survive removal of English headings and chapter numbers?',f'Does the preserved alternative—{r["rejected_alternative"]}—better retain the governing scene, speech, ritual, or register?']
 r['hard_passage_forecast']=[r['original_language_translation_holds'][0] if r['confidence']=='low' else f'Check {end} against the next direct Hebrew/WEB opening quoted in rejected_alternative; source metadata remains corroborating only.']
 n=int(r['decision_id'].split('-')[-1].split('r')[0])
 if n in {6,8,9,11,12,13,14,15,16}:
  h='The ḥērem/devoted-destruction vocabulary and related battle formulae are translation and interpretive hot zones; they do not decide the seam or authorize a moral/theological conclusion.'
  if h not in r['original_language_translation_holds']: r['original_language_translation_holds'].append(h)
P.write_text(''.join(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n' for x in rows),encoding='utf-8',newline='\n')
print(json.dumps({'rows':len(rows),'low':sum(x['confidence']=='low' for x in rows)}))