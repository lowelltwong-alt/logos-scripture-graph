from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent; REV=ROOT/'reviews'/'Hos'; OUT=ROOT/'book_chunks'/'Hos'/'chunks.jsonl'
def load(n): return json.loads((REV/n).read_text(encoding='utf-8'))
def rows(d): return d.get('chunks') or d.get('units') or d.get('proposed_chunks') or []
def point(v):
 v=v.replace('Hos.','').replace('.',':'); c,n=v.split(':'); return int(c),int(n)
def pair(v):
 a,b=v.split('-'); return point(a),point(b)
def overlaps(a,b):
 a0,a1=pair(a); b0,b1=pair(b); return a0<=b1 and b0<=a1
def render(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
can=load('blind_proposal_canonical_premortem_v1.json'); heb=load('blind_proposal_hebrew_textual_v1.json'); lit=load('blind_proposal_literary_fresh_v1.json')
cr,hr,lr=rows(can),rows(heb),rows(lit); assert cr and hr and lr
cg={k:v for k,v in can.items() if k not in {'chunks','units','proposed_chunks'}}
hg={k:v for k,v in heb.items() if k not in {'chunks','units','proposed_chunks'}}
lg={k:v for k,v in lit.items() if k not in {'chunks','units','proposed_chunks'}}
out=[]
for i,s in enumerate(cr,1):
 span=s['span']; did=f'M7_sol-Hos-{i:03d}'; hov=[x for x in hr if overlaps(span,x['span'])]; lov=[x for x in lr if overlaps(span,x['span'])]; assert hov and lov
 competing=f"selected canonical-premortem record={render(s)}; overlapping uncontaminated Hebrew/textual records={render(hov)}; overlapping fresh literary records={render(lov)}; canonical globals={render(cg)}; Hebrew/textual globals={render(hg)}; fresh literary globals={render(lg)}"
 form=s['form']; marker=s['marker'].rstrip('.')
 language=f"{span}: all overlapping Hebrew/textual evidence is preserved exactly: {render(hov)}. Hebrew syntax, lexemes, parallelism, pronoun/addressee shifts, MT/LXX/DSS/Syriac/Vulgate/Targum evidence, and the Hosea 1-2 versification offset remain evidence only. No preferred witness/emendation or speaker, spouse/child, Adam, king, nation, ancestor, prophet, death/Sheol, authorship, date, history, ethics, fulfillment, canon, covenant, divine-psychology, or theology ruling."
 out.append({'model_id':'M7_sol','book':'Hos','span':span,'chunk_index_in_book':i,'working_title':form.capitalize(),'literature_type_guess':form,'literary_form':form,
 'boundary_evidence_refs':[f'direct_read:eng-web:{span}',f'direct_read:oshb:Hos.xml#{span}',f'direct_read:uxlc:Hos.xml#{span}','book_strategy/Hos.md','reviews/Hos/blind_proposal_hebrew_textual_v1.json','reviews/Hos/blind_proposal_literary_fresh_v1.json','reviews/Hos/blind_proposal_canonical_premortem_v1.json','reviews/Hos/peer_crosscheck_v1.json','reviews/Hos/boss_ruling_v1.json','reviews/Hos/decision_relations.jsonl'],
 'strong_or_hebrew_tags_used':['direct_Biblical_Hebrew_prophetic_poetry_and_discourse_form_considered','MT_LXX_DSS_Syriac_Vulgate_Targum_and_versification_evidence_only','speaker_addressee_roots_and_lexemes_not_boundary_authority','roots_are_not_meaning','source_metadata_corrob_only'],
 'wj_or_red_letter_considered':False,'frontier_flag_considered':True,'confidence':'low','decision_id':did,'deciding_marker_or_seam':marker+'.',
 'boundary_rationale':f'Prefer the complete larger {form} movement {span}. {marker}. Retain accusation-consequence, recollection-appeal, judgment-restoration, enacted sign, lawsuit, lament, question chain, image cluster, or wisdom closure as a coherent movement.',
 'rejected_alternative':f'Preserved exact competing evidence for {span}: {competing}.','defensible_basis':f'{did}: {marker}. Form, discourse reset, vocative/imperative, speaker or addressee pressure, refrain, image field, enacted-sign sequence, lawsuit progression, reversal, or closure evidence—not chapter numbering, witness preference, identity, chronology, later reuse, fulfillment, or theology—supports this candidate.',
 'review_revision':1,'review_status':'final_deferred_appeal','review_holds':['deferred_human_or_external_ai','external_provider_review_at_convergence'],'non_authorizing':True,'candidate_internal_seams':[competing+'.'],'original_language_translation_holds':[language],
 'cross_reference_holds':['Relations to Torah, Samuel-Kings/Chronicles, Psalms, Isaiah, Jeremiah, Ezekiel, the Twelve, and later reuse are evidence only; they cannot force boundary symmetry, harmonize history, identify speakers/referents, select readings, settle chronology/fulfillment, or authorize theology.'],
 'red_team_premortem_holds':[f'{span}: chapter fallback, accusation/consequence detachment, judgment/restoration detachment, metaphor atomization, famous-verse proof-texting, speaker/addressee overconfidence, Hebrew emendation or witness preference, versification error, history/ethics/identity/fulfillment/theology smuggling risks. Exact primary evidence: {competing}.'],
 'working_title_is_boundary_authority':False,'working_title_origin':'independent_hosea_uncontaminated_three_primary_larger_unit_reconciliation_v1','candidate_only':True,'review_evidence_summary':marker+'. Candidate-only and non-authorizing.',
 'red_team_questions':[f"Does the seam after {span.split('-')[1]} survive removal of chapter numbers, headings, and later reuse?",f'Would an exact Hebrew/textual or fresh literary alternative better preserve the complete form: {competing}?'],'hard_passage_forecast':[language],'candidate_hold_state':'deferred_human_or_external_ai','candidate_hold_basis':'preserved_appeal'})
assert len(out)==len(cr)==30 and [x['chunk_index_in_book'] for x in out]==list(range(1,31))
OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(''.join(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n' for x in out),encoding='utf-8',newline='\n')
print(json.dumps({'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'chunks':len(out),'low':len(out),'hebrew_units':len(hr),'literary_units':len(lr)}))