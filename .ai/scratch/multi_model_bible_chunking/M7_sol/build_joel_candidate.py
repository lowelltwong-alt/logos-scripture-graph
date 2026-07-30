from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent; REV=ROOT/'reviews'/'Joel'; OUT=ROOT/'book_chunks'/'Joel'/'chunks.jsonl'
def load(n): return json.loads((REV/n).read_text(encoding='utf-8'))
def rows(d): return d.get('chunks') or d.get('units') or d.get('proposed_chunks') or []
def pt(v):
 v=v.replace('Joel.','').replace('.',':'); c,n=v.split(':'); return int(c),int(n)
def pair(v):
 a,b=v.split('-'); return pt(a),pt(b)
def ov(a,b):
 a0,a1=pair(a); b0,b1=pair(b); return a0<=b1 and b0<=a1
def render(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
lit=load('blind_proposal_literary_v1.json'); can=load('blind_proposal_canonical_premortem_v1.json'); heb=load('blind_proposal_hebrew_textual_v1.json')
lr,cr,hr=rows(lit),rows(can),rows(heb); assert lr and cr and hr
lg={k:v for k,v in lit.items() if k not in {'chunks','units','proposed_chunks'}}; cg={k:v for k,v in can.items() if k not in {'chunks','units','proposed_chunks'}}; hg={k:v for k,v in heb.items() if k not in {'chunks','units','proposed_chunks'}}
out=[]
for i,s in enumerate(lr,1):
 span=s['span']; did=f'M7_sol-Joel-{i:03d}'; cov=[x for x in cr if ov(span,x['span'])]; hov=[x for x in hr if ov(span,x['span'])]; assert cov and hov
 competing=f"selected clean blind literary record={render(s)}; overlapping clean blind canonical-premortem records={render(cov)}; overlapping qualified Hebrew/textual audit records={render(hov)}; literary globals={render(lg)}; canonical globals={render(cg)}; qualified Hebrew globals={render(hg)}; Hebrew audit procedural limitation=accidentally saw only the known three chapter-fallback rows, supplied no positive seam evidence, and counts as zero uncontaminated blind primary votes"
 form=s['literary_form']; marker=s['deciding_marker'].rstrip('.')
 language=f"{span}: qualified Hebrew/textual audit preserved exactly: {render(hov)}. Direct ancient Hebrew/version files were not independently available to the failed fresh rerun. MT/LXX/DSS/Syriac/Vulgate/Targum, Hebrew three/four-chapter versus English three-chapter numbering, locust terms, northern-one referent, teacher/rain wording, afterward, all flesh, signs, survivors, valleys, nations, harvest/winepress, and geography remain evidence only; no preferred witness/emendation, identity, date, chronology, fulfillment, ethics, canon, or theology."
 out.append({'model_id':'M7_sol','book':'Joel','span':span,'chunk_index_in_book':i,'working_title':s['title'],'literature_type_guess':form,'literary_form':form,'boundary_evidence_refs':[f'direct_read:eng-web:{span}','book_strategy/Joel.md','reviews/Joel/blind_proposal_literary_v1.json','reviews/Joel/blind_proposal_canonical_premortem_v1.json','reviews/Joel/blind_proposal_hebrew_textual_v1.json','reviews/Joel/peer_crosscheck_v1.json','reviews/Joel/boss_ruling_v1.json','reviews/Joel/decision_relations.jsonl'],
 'strong_or_hebrew_tags_used':['qualified_Biblical_Hebrew_textual_audit_not_uncontaminated_vote','MT_LXX_DSS_versions_and_three_four_chapter_versification_evidence_only','locust_army_northern_one_teacher_rain_spirit_nations_referents_deferred','roots_are_not_meaning','source_metadata_corrob_only'],
 'wj_or_red_letter_considered':False,'frontier_flag_considered':True,'confidence':'low','decision_id':did,'deciding_marker_or_seam':marker+'.','boundary_rationale':f'Prefer the complete larger {form} movement {span}. {marker}. Retain summons-lament, alarm-host, return-intercession, answer-restoration, outpouring-signs-escape, nations-lawsuit, battle-harvest, or closing restoration as a coherent movement.',
 'rejected_alternative':f'Preserved exact competing evidence for {span}: {competing}.','defensible_basis':f'{did}: {marker}. Imperative/vocative chain, trumpet reset, day formula, speaker shift, answer pivot, repeated outpouring/sign sequence, nations summons, harvest scene, recognition formula, or dwelling refrain—not chapter numbering, witness preference, identity, chronology, later reuse, fulfillment, or theology—supports this candidate.',
 'review_revision':1,'review_status':'final_deferred_appeal','review_holds':['deferred_human_or_external_ai','external_provider_review_at_convergence','fresh_direct_Hebrew_witness_review_needed'],'non_authorizing':True,'candidate_internal_seams':[competing+'.'],'original_language_translation_holds':[language],
 'cross_reference_holds':['Relations to Torah, Samuel-Kings/Chronicles, Psalms, Isaiah, Jeremiah, Ezekiel, the Twelve, Acts, Romans, Revelation, and other reuse are evidence only; they cannot force symmetry, harmonize events, identify locust/army/northern one/Spirit/nations/valleys, select readings, settle chronology/fulfillment, or authorize theology.'],
 'red_team_premortem_holds':[f'{span}: chapter fallback, imperative/list atomization, alarm/return or answer/restoration detachment, proof-texting, locust/army identity, versification error, witness/emendation preference, later-reuse backprojection, date/chronology/fulfillment/Spirit-system/nations-geography/ethics/theology smuggling risks. Exact evidence: {competing}.'],
 'working_title_is_boundary_authority':False,'working_title_origin':'independent_joel_two_clean_blind_primaries_plus_qualified_Hebrew_audit_larger_unit_reconciliation_v1','candidate_only':True,'review_evidence_summary':marker+'. Candidate-only and non-authorizing.','red_team_questions':[f"Does the seam after {span.split('-')[1]} survive removal of chapters, headings, and later reuse?",f'Would a preserved canonical or qualified Hebrew alternative better retain the full movement: {competing}?'],'hard_passage_forecast':[language],'candidate_hold_state':'deferred_human_or_external_ai','candidate_hold_basis':'preserved_appeal'})
assert len(out)==len(lr)==10 and [x['chunk_index_in_book'] for x in out]==list(range(1,11))
OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(''.join(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n' for x in out),encoding='utf-8',newline='\n'); print(json.dumps({'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'chunks':len(out),'low':len(out),'clean_blind_primary_count':2,'qualified_hebrew_audit_units':len(hr)}))