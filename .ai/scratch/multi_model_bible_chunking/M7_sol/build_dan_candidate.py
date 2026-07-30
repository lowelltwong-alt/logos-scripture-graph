from __future__ import annotations
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent; REV=ROOT/'reviews'/'Dan'; OUT=ROOT/'book_chunks'/'Dan'/'chunks.jsonl'
def load(name): return json.loads((REV/name).read_text(encoding='utf-8'))
def point(v):
 v=v.replace('Dan.','').replace('.',':'); c,n=v.split(':'); return int(c),int(n)
def pair(v):
 a,b=v.split('-'); return point(a),point(b)
def overlaps(a,b):
 a0,a1=pair(a); b0,b1=pair(b); return a0<=b1 and b0<=a1
def render(v): return v if isinstance(v,str) else json.dumps(v,ensure_ascii=False,sort_keys=True)
lit=load('blind_proposal_literary_v1.json'); can=load('blind_proposal_canonical_premortem_v1.json')
selected_rows=lit['units']; canonical_rows=can['chunks']
heb_path=REV/'blind_proposal_hebrew_textual_v1.json'; heb=load('blind_proposal_hebrew_textual_v1.json') if heb_path.exists() else None
hebrew_rows=(heb.get('proposed_chunks') or heb.get('units') or heb.get('chunks') or []) if heb else []
global_lit='literary macro parents='+' | '.join(render(x) for x in lit.get('macro_parent_alternatives',[]))+'; literary global hot zones='+' | '.join(render(x) for x in lit.get('global_hot_zones',[]))
global_can='canonical premortem holds='+' | '.join(render(x) for x in can.get('premortem_holds',[]))+'; canonical evidence-only relations='+' | '.join(render(x) for x in can.get('evidence_only_canonical_relations',[]))+'; canonical hardest-boundary order='+' | '.join(render(x) for x in can.get('hardest_boundary_order',[]))+'; canonical global guards='+render(can.get('global_guards',{}))
global_heb=('Hebrew-Aramaic primary global guard='+render(heb.get('evidence_only_guard',{}))+'; Hebrew-Aramaic macro parents='+' | '.join(render(x) for x in heb.get('macro_parent_alternatives',[]))+'; textual/translation hot zones='+' | '.join(render(x) for x in heb.get('textual_translation_hot_zone_audit',[]))) if heb else 'Hebrew-Aramaic primary missing; build must not freeze or complete.'
rows=[]
for index,selected in enumerate(selected_rows,1):
 span=selected['span']; did=f'M7_sol-Dan-{index:03d}'; can_over=[x for x in canonical_rows if overlaps(span,x['span'])]; heb_over=[x for x in hebrew_rows if overlaps(span,x['span'])]
 assert can_over
 lit_e=(f"{span}: title={selected['title']}; form={selected['literary_form']}; marker={selected['deciding_marker']}; risk={selected['risk']}; rejected={selected['rejected_alternative']}; alternatives={'; '.join(selected.get('exact_alternatives',[])) or 'none stated'}")
 can_e=' | '.join(f"{x['span']}: form={x['form']}; marker={x['marker']}; risk={x['risk']}; rejected={x['rejected_alternative']}; hold={x['hold']}; alternatives={'; '.join(x.get('exact_alternatives',[])) or 'none stated'}" for x in can_over)
 heb_e=' | '.join(f"{x['span']}: form={x['literary_form']}; marker={x['deciding_marker']}; risk={x['risk']}; rejected={x['rejected_alternative']}; Hebrew/textual/translation evidence={x['hebrew_textual_translation_evidence']}" for x in heb_over) if heb_over else 'missing Hebrew-Aramaic primary'
 competing=f'selected larger literary unit [{lit_e}]; overlapping canonical-premortem alternatives [{can_e}]; overlapping Hebrew-Aramaic/textual primary [{heb_e}]; {global_lit}; {global_can}; {global_heb}'
 marker=selected['deciding_marker'].rstrip('.'); form=selected['literary_form']
 language_hold=(f"{span}: {heb_e}. MT, Old Greek, Theodotion, Qumran fragments, Syriac, Vulgate, Hebrew-Aramaic language transitions, qere/ketiv, rare syntax, court titles/loanwords, bar-enash, maskilim, tamid, shiqqus/shomem, sevens and time formulas remain evidence only. No preferred witness/order, authorship/date/history/redaction, ruler/empire/horn/human-like figure/prince/Michael/messenger identity, resurrection, fulfillment, eschatology, chronology, miracle, divine-agency ethics, canon or theology.")
 rows.append({'model_id':'M7_sol','book':'Dan','span':span,'chunk_index_in_book':index,'working_title':selected['title'],'literature_type_guess':form,'literary_form':form,
 'boundary_evidence_refs':[f'direct_read:eng-web:{span}',f'direct_read:oshb:Dan.xml#{span}',f'direct_read:uxlc:Dan.xml#{span}','book_strategy/Dan.md','reviews/Dan/blind_proposal_literary_v1.json','reviews/Dan/blind_proposal_canonical_premortem_v1.json','reviews/Dan/blind_proposal_hebrew_textual_v1.json','reviews/Dan/peer_crosscheck_v1.json','reviews/Dan/boss_ruling_v1.json','reviews/Dan/decision_relations.jsonl'],
 'strong_or_hebrew_tags_used':['direct_Hebrew_Aramaic_court_tale_and_apocalyptic_form_considered','MT_OG_Theodotion_Qumran_versions_order_numbering_evidence_only','bar_enash_maskilim_tamid_shiqqus_sevens_time_formulas_evidence_only','roots_are_not_meaning','source_metadata_corrob_only'],
 'wj_or_red_letter_considered':False,'frontier_flag_considered':True,'confidence':'low','decision_id':did,'deciding_marker_or_seam':marker+'.',
 'boundary_rationale':f'Prefer the complete larger {form} movement {span}. {marker}. Retain command-performance-interpretation, riddle/allegory-explanation, lament image chain, dated oracle, guided vision/tour, measurement itinerary, legal register or allotment function as a coherent unit.',
 'rejected_alternative':f'Preserved exact competing evidence for {span}: {competing}.','defensible_basis':f'{did}: {marker}. Date/word-event, location/addressee reset, command-performance-interpretation, riddle/allegory, lament formula, messenger arrival, guided movement, refrain-plus-closure, or register-function evidence—not chapter numbering, witness preference, chronology, identity, fulfillment or theology—supports this candidate.',
 'review_revision':1,'review_status':'final_deferred_appeal','review_holds':['deferred_human_or_external_ai','external_provider_review_at_convergence'],'non_authorizing':True,'candidate_internal_seams':[competing+'.'],'original_language_translation_holds':[language_hold],
 'cross_reference_holds':['Relations to Torah, Samuel-Kings/Chronicles, Isaiah, Jeremiah, Ezekiel, the Twelve, Psalms and later reuse are evidence only; they cannot harmonize history, identify rulers/empires/horns/the human-like figure/princes/Michael/messengers, settle chronology/fulfillment/resurrection/eschatology, select readings, force symmetry or theology.'],
 'red_team_premortem_holds':[f'{span}: chapter fallback, dream/vision-interpretation detachment, court/instrument/kingdom list atomization, proof-texting, Hebrew-Aramaic switch overreach, MT/OG/Theodotion/Qumran preference, Greek-addition/canon inference, authorship/date/history/miracle, identity, seventy-weeks/time calculation, resurrection/fulfillment/eschatology/theology risks. Exact evidence: {competing}.'],
 'working_title_is_boundary_authority':False,'working_title_origin':'independent_daniel_three_blind_primary_larger_unit_reconciliation_v1','candidate_only':True,'review_evidence_summary':marker+'. Candidate-only and non-authorizing.','red_team_questions':[f'Does the seam after {span.split("-")[1]} survive removal of chapters, headings and later reuse?',f'Would an exact Hebrew/textual or canonical alternative better preserve the complete court tale, dream/interpretation, vision/dialogue, prayer/response or final revelation: {competing}?'],'hard_passage_forecast':[language_hold],'candidate_hold_state':'deferred_human_or_external_ai','candidate_hold_basis':'preserved_appeal'})
assert len(rows)==35 and [r['chunk_index_in_book'] for r in rows]==list(range(1,36))
OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(''.join(json.dumps(r,ensure_ascii=False,separators=(',',':'))+'\n' for r in rows),encoding='utf-8',newline='\n')
print(json.dumps({'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'chunks':len(rows),'low':len(rows),'hebrew_primary_embedded':bool(heb)}))