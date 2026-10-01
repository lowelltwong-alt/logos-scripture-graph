from __future__ import annotations
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent; R=ROOT/"reviews"/"Ps"; OUT=ROOT/"book_chunks"/"Ps"/"chunks.jsonl"
def load(n): return json.loads((R/n).read_text(encoding="utf-8"))
def pt(v):
 v=v.replace("Ps.",""); c,x=(v.split(".") if "." in v else v.split(":")); return int(c),int(x)
def pair(v):
 if "-" not in v: p=pt(v); return p,p
 a,b=v.split("-")
 if ":" not in b and "." not in b: b=f"{a.replace('Ps.','').replace('.',':').split(':')[0]}:{b}"
 return pt(a),pt(b)
def full(v):
 (a,b),(c,d)=pair(v); return f"Ps.{a}.{b}-Ps.{c}.{d}"
def short(v):
 (a,b),(c,d)=pair(v); return f"{a}:{b}-{c}:{d}"
def ov(a,b):
 a0,a1=pair(a); b0,b1=pair(b); return a0<=b1 and b0<=a1
cd=load("blind_proposal_canonical_premortem_v1.json"); ld=load("blind_proposal_literary_v1.json"); hd=load("blind_proposal_hebrew_poetics_v1.json")
cs=cd["chunks"]; ls=ld["proposal"]; hs=hd["proposed_chunks"]
lex={full(x["span"]) for x in ls}; hexact={full(x["span"]) for x in hs}; globalholds=" | ".join(hd["web_mt_lxx_versification_holds"])
T467_WHOLE_PSALM_LOW={1,3,4,5,6,7,8,11,12,13,14,15,17,24,25,29,31,32,34,35,36,40,42,46,51,52,63,64,74,75,76,80,82,84,85,87,88,100,110,111,122,132,133,134,135,146,153,154,156,157,188,189,190,191,194,220,221,222,223,224,225,226,227,228,229,230,231,233,234,243,248,249,250,251,258,262,263}
rows=[]
for i,s in enumerate(cs,1):
 span=full(s["span"]); did=f"M7_sol-Ps-{i:03d}"; ho=[x for x in hs if ov(span,x["span"])]; lo=[x for x in ls if ov(span,x["span"])]
 exact=span in lex and span in hexact
 holds=[x for x in hd["exact_low_holds"] if ov(span,x["span"])]
 low=(not exact or i in T467_WHOLE_PSALM_LOW or s["confidence"].upper()=="LOW" or bool(holds) or any(x["confidence"].upper()=="LOW" for x in ho) or any(x["confidence"].upper()=="LOW" for x in lo))
 competing=(f"canonical exact alternatives {' | '.join(s.get('exact_alternatives',[])) or 'none stated'}; "
  f"Hebrew/poetics overlap {' + '.join(short(x['span']) for x in ho)}; Hebrew chosen forms {' | '.join(x['span']+': '+x['literary_form'] for x in ho)}; Hebrew rejected alternatives {' | '.join(x['rejected_alternative'] for x in ho)}; "
  f"Hebrew exact low holds {' | '.join(x['span']+': '+', '.join(x['competing_internal_units'])+': '+x['hold'] for x in holds) or 'none stated'}; "
  f"literary overlap {' + '.join(short(x['span']) for x in lo)}; "
  f"literary chosen evidence {' | '.join(x['span']+': '+x['literary_form']+': '+x['deciding_marker']+': '+x['risk'] for x in lo)}; "
  f"literary exact alternatives {' | '.join(a for x in lo for a in x.get('exact_alternatives',[])) or 'none stated'}")
 detail=" | ".join(f"{x['span']} [{x['risk']}]: {x['deciding_marker']}" for x in ho)
 lang=(f"{span}: {detail}. Exact competing evidence: {competing}. Global numbering/textual holds: {globalholds}. "
 "Hebrew poetics, accents, qere/ketiv, Selah, superscriptions, refrains, acrostics, WEB/MT/LXX numbering and later reuse are evidence only; no verse 0, Psalm 151, preferred reading, authorship, setting, speaker identity, imprecatory ethic, messianic/Christological or theological ruling.")
 form=s["form"]; marker=s["seam"].rstrip(".")
 row={"model_id":"M7_sol","book":"Ps","span":span,"chunk_index_in_book":i,"working_title":re.sub("_+"," ",form).capitalize(),"literature_type_guess":form,"literary_form":form,
 "boundary_evidence_refs":[f"direct_read:eng-web:{span}",f"direct_read:oshb:Ps.xml#{span}",f"direct_read:uxlc:Ps.xml#{span}","book_strategy/Ps.md","reviews/Ps/blind_proposal_hebrew_poetics_v1.json","reviews/Ps/blind_proposal_literary_v1.json","reviews/Ps/blind_proposal_canonical_premortem_v1.json","reviews/Ps/peer_crosscheck_v1.json","reviews/Ps/boss_ruling_v1.json","reviews/Ps/decision_relations.jsonl"],
 "strong_or_hebrew_tags_used":["direct_Hebrew_poetics_considered","superscriptions_and_Selah_evidence_only","WEB_MT_LXX_numbering_preserved","roots_are_not_meaning","source_metadata_corrob_only"],
 "wj_or_red_letter_considered":False,"frontier_flag_considered":True,"confidence":"low" if low else "medium","decision_id":did,"deciding_marker_or_seam":marker+".",
 "boundary_rationale":f"Prefer the complete {form} unit {span}. {marker}. Whole-psalm parent remains explicit whenever an internal unit is selected.",
 "rejected_alternative":f"Preserved exact competing evidence for {span}: {competing}.","defensible_basis":f"{did}: {marker}. Complete poem or local stanza/refrain/acrostic/liturgical function—not chapter fallback, Selah alone, superscription history, later quotation, or theology—supports this candidate.",
 "review_revision":1,"review_status":"final_deferred_appeal" if low else "candidate_review_complete","review_holds":["deferred_human_or_external_ai","external_provider_review_at_convergence"] if low else ["external_provider_review_at_convergence"],"non_authorizing":True,
 "candidate_internal_seams":[competing+"."],"original_language_translation_holds":[lang],"cross_reference_holds":["Relations to Torah, history, wisdom, prophets and later reuse are evidence only; they cannot merge psalms, dictate seams, identify speakers, establish superscription history, select readings or force messianic/Christological conclusions."],
 "red_team_premortem_holds":[f"{span}: couplet atomization, whole-psalm fallback, Selah authority, forced Psalm merger, numbering, superscription, imprecation and theology-smuggling risks. Exact evidence: {competing}."],
 "working_title_is_boundary_authority":False,"working_title_origin":"independent_psalms_three_primary_reconciliation_v1","candidate_only":True,"review_evidence_summary":marker+". Candidate-only and non-authorizing.",
 "red_team_questions":[f"Does the seam after {span.split('-')[1]} survive removal of headings, chapters and Selah?",f"Does an exact alternative better preserve whole-poem and stanza function: {competing}?"],"hard_passage_forecast":[lang]}
 if low: row.update(candidate_hold_state="deferred_human_or_external_ai",candidate_hold_basis="preserved_appeal")
 rows.append(row)
assert len(rows)==263 and [x["chunk_index_in_book"] for x in rows]==list(range(1,264))
OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text("".join(json.dumps(x,ensure_ascii=False,separators=(",",":"))+"\n" for x in rows),encoding="utf-8",newline="\n")
print(json.dumps({"sha256":hashlib.sha256(OUT.read_bytes()).hexdigest(),"chunks":len(rows),"low":sum(x["confidence"]=="low" for x in rows),"accepted":sum(x["confidence"]!="low" for x in rows)}))
