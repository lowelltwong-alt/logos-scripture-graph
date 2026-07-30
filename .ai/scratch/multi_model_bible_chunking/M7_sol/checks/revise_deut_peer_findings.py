import json
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'book_chunks'/'Deut'/'chunks.jsonl'
rows=[json.loads(x) for x in P.read_text(encoding='utf-8').splitlines() if x.strip()]
assert len(rows)==79 and rows[40]['decision_id']=='M7_sol-Deut-041' and rows[41]['decision_id']=='M7_sol-Deut-042'
a=rows[40]; b=rows[41]
a.update({'decision_id':'M7_sol-Deut-041r1','span':'Deut.19.1-Deut.19.21','working_title':'Refuge cities landmark safeguard and witness procedures','literature_type_guess':'refuge_city_and_evidence_code','literary_form':'refuge_city_and_evidence_code','confidence':'low','review_status':'final_deferred_appeal','candidate_hold_state':'deferred_human_or_external_ai','candidate_hold_basis':'preserved_appeal'})
marker="Deut.19.1 opens the refuge-city conditional; manslaughter and murder procedure, the disputed 19:14 landmark safeguard, and witness/false-testimony procedure reach closure at 19:21 before the battle conditional at 20:1."
a['deciding_marker_or_seam']=marker; a['candidate_internal_seams']=[marker,"Appealed inner attachments: 19:1-13 / 19:14-21 versus 19:1-14 / 19:15-21."]
a['original_language_translation_holds']=["The legal-function turn at 19:14/15 is genuinely disputed: two blind roles attach 19:14 forward, while another attaches it backward. Retain the larger 19:1-21 parent; select no forced seam."]
a['red_team_premortem_holds']=["A split at 19:13/14 or 19:14/15 risks assigning the landmark safeguard to the wrong procedure; the larger LOW parent preserves both appeals."]
a['rejected_alternative']="Rejected choosing either contested attachment: 19:1-13 / 19:14-21 or 19:1-14 / 19:15-21. Both remain append-only appeals under the larger 19:1-21 parent."
a['boundary_rationale']="Prefer the larger coherent legal parent Deut.19.1-Deut.19.21 while the 19:14 attachment remains unresolved. "+marker
a['defensible_basis']=a['decision_id']+": "+marker+" The larger parent is a procedural hold, not a claim that refuge, landmark, and witness laws share one indivisible form."
a['review_evidence_summary']=marker+" The larger parent follows the unresolved-to-larger rule and selects no theology, canon, authorship, or preferred reading."
rows=rows[:41]+rows[42:]
for i,row in enumerate(rows,1): row['chunk_index_in_book']=i
for i,row in enumerate(rows):
 marker=row['deciding_marker_or_seam']; nxt=rows[i+1]['deciding_marker_or_seam'].split(';',1)[0] if i+1<len(rows) else 'the canonical end of Deuteronomy'
 if row['decision_id']!='M7_sol-Deut-041r1':
  if row['confidence']=='low':
   specific=row['original_language_translation_holds'][0]
   if row['decision_id'] in {'M7_sol-Deut-001','M7_sol-Deut-002'}: specific=row['rejected_alternative']
   row['rejected_alternative']="Preserved competing boundary/evidence alternative for this exact span: "+specific
  else:
   row['rejected_alternative']=f"Rejected expansion beyond {row['span'].split('-')[1]} because the next reviewed movement begins with {nxt}. No narrower seam was adopted absent a competing role-specific marker within '{row['working_title']}'."
  row['defensible_basis']=f"{row['decision_id']}: {marker} This exact observed opening/closure evidence, not a chapter division or lexical root, supports the candidate boundary."
P.write_text(''.join(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n' for x in rows),encoding='utf-8',newline='\n')
print(json.dumps({'rows':len(rows),'low':sum(x['confidence']=='low' for x in rows)}))