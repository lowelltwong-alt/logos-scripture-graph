from __future__ import annotations
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent; R=ROOT/"reviews"/"Job"; OUT=ROOT/"book_chunks"/"Job"/"chunks.jsonl"
def load(n): return json.loads((R/n).read_text(encoding="utf-8"))
def pt(v):
 v=v.replace("Job.",""); c,x=(v.split(".") if "." in v else v.split(":")); return int(c),int(x)
def pair(v):
 if "-" not in v: p=pt(v); return p,p
 a,b=v.split("-")
 if ":" not in b and "." not in b: b=f"{a.replace('Job.','').replace('.',':').split(':')[0]}:{b}"
 return pt(a),pt(b)
def full(v):
 (a,b),(c,d)=pair(v); return f"Job.{a}.{b}-Job.{c}.{d}"
def short(v):
 (a,b),(c,d)=pair(v); return f"{a}:{b}-{c}:{d}"
def ov(a,b):
 a0,a1=pair(a); b0,b1=pair(b); return a0<=b1 and b0<=a1
cd=load("blind_proposal_canonical_premortem_v1.json"); ld=load("blind_proposal_literary_v1.json"); hd=load("blind_proposal_hebrew_textual_v1.json")
cs=cd["chunks"]; ls=ld["proposal"]; hs=hd["proposed_chunks"]
lex={full(x["span"]) for x in ls}; hexact={full(x["span"]) for x in hs}
rows=[]
for i,s in enumerate(cs,1):
 span=full(s["span"]); did=f"M7_sol-Job-{i:03d}"; ho=[x for x in hs if ov(span,x["span"])]; lo=[x for x in ls if ov(span,x["span"])]
 exact=span in lex and span in hexact
 low=(not exact or i in {9,11,15} or s["confidence"].upper()=="LOW" or any(x["confidence"].upper()=="LOW" for x in ho) or any(x["confidence"].upper()=="LOW" for x in lo))
 holds=[x for x in hd["exact_low_holds"] if ov(span,x["span"])]
 competing=(f"canonical exact alternatives {' | '.join(s.get('exact_alternatives',[])) or 'none stated'}; "
  f"Hebrew/textual overlap {' + '.join(short(x['span']) for x in ho)}; Hebrew rejected alternatives {' | '.join(x['rejected_alternative'] for x in ho)}; "
  f"Hebrew exact low holds {' | '.join(x['span']+': '+x['hold'] for x in holds) or 'none stated'}; "
  f"literary overlap {' + '.join(short(x['span']) for x in lo)}; literary rejected alternatives {' | '.join(x['rejected_alternative'] for x in lo)}")
 mapping=hd["web_mt_versification_hold"]; maptext=("; ".join(mapping["mapping"])+": "+mapping["decision"]) if ov(span,"41:1-41:34") else "no WEB/MT offset identified for this span"
 detail=" | ".join(f"{x['span']} [{x['risk']}]: {x['deciding_marker']}" for x in ho)
 lang=(f"{span}: {detail}. Exact competing evidence: {competing}. WEB/MT: {maptext}. Rare Hebrew, qere/ketiv, roots, emendations, speaker allocation, legal and poetic terms are evidence only; no preferred reading, transposition, speaker reassignment, zoological identification, chronology, historicity, theodicy, afterlife, Christology, moral or theological ruling.")
 form=s["form"]; marker=s["seam"].rstrip(".")
 row={"model_id":"M7_sol","book":"Job","span":span,"chunk_index_in_book":i,"working_title":re.sub("_+"," ",form).capitalize(),
 "literature_type_guess":form,"literary_form":form,"boundary_evidence_refs":[f"direct_read:eng-web:{span}",f"direct_read:oshb:Job.xml#{span}",f"direct_read:uxlc:Job.xml#{span}","book_strategy/Job.md","reviews/Job/blind_proposal_hebrew_textual_v1.json","reviews/Job/blind_proposal_literary_v1.json","reviews/Job/blind_proposal_canonical_premortem_v1.json","reviews/Job/peer_crosscheck_v1.json","reviews/Job/boss_ruling_v1.json","reviews/Job/decision_relations.jsonl"],
 "strong_or_hebrew_tags_used":["direct_Hebrew_wording_considered","rare_lexemes_and_emendations_evidence_only","speaker_allocation_not_repaired","roots_are_not_meaning","source_metadata_corrob_only"],
 "wj_or_red_letter_considered":False,"frontier_flag_considered":True,"confidence":"low" if low else "medium","decision_id":did,
 "deciding_marker_or_seam":marker+".","boundary_rationale":f"Prefer the complete {form} unit {span}. {marker}. Unresolved splits retain the larger complete speech, poem, response, or prose scene.",
 "rejected_alternative":f"Preserved exact competing evidence for {span}: {competing}.",
 "defensible_basis":f"{did}: {marker}. Explicit scene/speaker formulas and complete rhetorical or narrative function—not chapter symmetry, emendation, speaker repair, or doctrine—support this candidate.",
 "review_revision":1,"review_status":"final_deferred_appeal" if low else "candidate_review_complete",
 "review_holds":["deferred_human_or_external_ai","external_provider_review_at_convergence"] if low else ["external_provider_review_at_convergence"],
 "non_authorizing":True,"candidate_internal_seams":[competing+"."],"original_language_translation_holds":[lang],
 "cross_reference_holds":["Relations to Genesis, Torah, Psalms, Proverbs, Ecclesiastes, prophets and later reuse are evidence only; they cannot identify Job, harmonize speakers, select readings, force symmetry, or settle theodicy/afterlife/Christology."],
 "red_team_premortem_holds":[f"{span}: speech fragmentation, forced-cycle symmetry, 24-27 speaker repair, authorship, proof-texting, zoological and doctrine-smuggling risks. Exact evidence: {competing}."],
 "working_title_is_boundary_authority":False,"working_title_origin":"independent_job_three_primary_reconciliation_v1","candidate_only":True,
 "review_evidence_summary":marker+". Candidate-only and non-authorizing.","red_team_questions":[f"Does the seam after {span.split('-')[1]} survive removal of chapters/headings?",f"Does an exact alternative better preserve speaker and rhetorical function: {competing}?"],
 "hard_passage_forecast":[lang]}
 if low: row.update(candidate_hold_state="deferred_human_or_external_ai",candidate_hold_basis="preserved_appeal")
 rows.append(row)
assert len(rows)==35 and [x["chunk_index_in_book"] for x in rows]==list(range(1,36))
OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text("".join(json.dumps(x,ensure_ascii=False,separators=(",",":"))+"\n" for x in rows),encoding="utf-8",newline="\n")
print(json.dumps({"sha256":hashlib.sha256(OUT.read_bytes()).hexdigest(),"chunks":len(rows),"low":sum(x["confidence"]=="low" for x in rows),"accepted":sum(x["confidence"]!="low" for x in rows)}))
