from __future__ import annotations
import hashlib, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
REVIEWS=ROOT/"reviews"/"Esth"
OUT=ROOT/"book_chunks"/"Esth"/"chunks.jsonl"
def load(n): return json.loads((REVIEWS/n).read_text(encoding="utf-8"))
def point(v):
    v=v.replace("Esth.",""); c,x=(v.split(".") if "." in v else v.split(":")); return int(c),int(x)
def pair(v):
    if "-" not in v: p=point(v); return p,p
    a,b=v.split("-")
    if ":" not in b and "." not in b:
        c=a.replace("Esth.","").replace(".",":").split(":")[0]; b=f"{c}:{b}"
    return point(a),point(b)
def full(v):
    (a,b),(c,d)=pair(v); return f"Esth.{a}.{b}-Esth.{c}.{d}"
def short(v):
    (a,b),(c,d)=pair(v); return f"{a}:{b}-{c}:{d}"
def overlap(a,b):
    a0,a1=pair(a); b0,b1=pair(b); return a0<=b1 and b0<=a1

can_doc=load("blind_proposal_canonical_premortem_v1.json")
lit_doc=load("blind_proposal_literary_v1.json")
heb_doc=load("blind_proposal_hebrew_textual_v1.json")
canonical=can_doc["chunks"]; literary=lit_doc["proposal"]; hebrew=heb_doc["proposed_chunks"]
lit_exact={full(x["span"]) for x in literary}; heb_exact={full(x["span"]) for x in hebrew}
rows=[]
for i,src in enumerate(canonical,1):
    span=full(src["span"]); did=f"M7_sol-Esth-{i:03d}"
    hs=[x for x in hebrew if overlap(span,x["span"])]
    ls=[x for x in literary if overlap(span,x["span"])]
    exact=span in lit_exact and span in heb_exact
    low=(not exact or src["confidence"].upper()=="LOW" or bool(src.get("appeal"))
         or any(x["confidence"].upper()=="LOW" for x in hs)
         or any(x["confidence"].upper()=="LOW" for x in ls))
    can_alt=json.dumps(src.get("rejected_alternatives",[]),ensure_ascii=False,separators=(",",":"))
    competing=(
      f"canonical rejected alternatives verbatim {can_alt}; "
      f"Hebrew/textual primary overlap {' + '.join(short(x['span']) for x in hs)}; "
      f"Hebrew/textual rejected alternatives {' | '.join(x['rejected_alternative'] for x in hs)}; "
      f"literary primary overlap {' + '.join(short(x['span']) for x in ls)}; "
      f"literary exact internal alternatives "
      f"{' | '.join(a for x in ls for a in x.get('exact_internal_alternatives',[])) or 'none stated'}"
    )
    heb_detail=" | ".join(f"{x['span']} [{x['risk']}]: {x['deciding_marker']}" for x in hs)
    language_hold=(
      f"{span}: {heb_detail}. Exact competing spans: {competing}. "
      f"Canonical scope/textual-history hold: {heb_doc['canonical_scope_and_textual_history_hold']}. "
      "Hebrew wording, qere/ketiv, parashah markers, Persian terms, MT/LXX differences, and Greek "
      "additions are evidence only. Greek additions are not imported; no preferred tradition, "
      "providence, historicity, genealogy, ethnicity, violence ethics, or theology is decided."
    )
    form=src["literary_form"]; marker=src["larger_unit_rationale"].rstrip(".")
    row={
      "model_id":"M7_sol","book":"Esth","span":span,"chunk_index_in_book":i,
      "working_title":src["label"],"literature_type_guess":form,"literary_form":form,
      "boundary_evidence_refs":[f"direct_read:eng-web:{span}",f"direct_read:oshb:Esth.xml#{span}",
       f"direct_read:uxlc:Esth.xml#{span}","book_strategy/Esth.md",
       "reviews/Esth/blind_proposal_hebrew_textual_v1.json","reviews/Esth/blind_proposal_literary_v1.json",
       "reviews/Esth/blind_proposal_canonical_premortem_v1.json","reviews/Esth/peer_crosscheck_v1.json",
       "reviews/Esth/boss_ruling_v1.json","reviews/Esth/decision_relations.jsonl"],
      "strong_or_hebrew_tags_used":["direct_Hebrew_wording_considered","MT_LXX_additions_evidence_only",
       "Greek_additions_not_imported","source_metadata_corrob_only","roots_are_not_meaning"],
      "wj_or_red_letter_considered":False,"frontier_flag_considered":True,
      "confidence":"low" if low else "medium","decision_id":did,
      "deciding_marker_or_seam":"; ".join(src["deciding_markers"])+".",
      "boundary_rationale":f"Prefer the complete {form} unit {span}. {marker}. Unresolved splits retain the larger coherent unit.",
      "rejected_alternative":f"Preserved exact competing evidence for {span}: {competing}.",
      "defensible_basis":f"{did}: {marker}. Local banquet, decree-response, recognition, reversal, conflict-rest, festival-letter, or closure form—not chapter headings, textual additions, providence, chronology, ethnicity, violence ethics, or theology—supports this candidate.",
      "review_revision":1,"review_status":"final_deferred_appeal" if low else "candidate_review_complete",
      "review_holds":["deferred_human_or_external_ai","external_provider_review_at_convergence"] if low else ["external_provider_review_at_convergence"],
      "non_authorizing":True,"candidate_internal_seams":[competing+"."],
      "original_language_translation_holds":[language_hold],
      "cross_reference_holds":["Relations to Joseph, Saul-Agag/Amalek, exile court narratives, Proverbs, festival memorials, and later reuse are evidence only; they cannot establish genealogy, import divine causation, harmonize chronology, authorize violence, or force seams."],
      "red_team_premortem_holds":[f"{span}: fallback, banquet/decree detachment, giant-reversal collapse, Greek-additions import, providence, genealogy, ethnicity, violence and doctrine-smuggling risks. Exact alternatives: {competing}."],
      "working_title_is_boundary_authority":False,"working_title_origin":"independent_esther_three_primary_reconciliation_v1",
      "candidate_only":True,"review_evidence_summary":marker+". Candidate-only and non-authorizing.",
      "red_team_questions":[f"Does the seam after {span.split('-')[1]} survive removal of headings and chapters?",f"Does an exact alternative better preserve cause-response or reversal: {competing}?"],
      "hard_passage_forecast":[language_hold]
    }
    if low: row.update(candidate_hold_state="deferred_human_or_external_ai",candidate_hold_basis="preserved_appeal")
    rows.append(row)
assert len(rows)==12 and [x["chunk_index_in_book"] for x in rows]==list(range(1,13))
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text("".join(json.dumps(x,ensure_ascii=False,separators=(",",":"))+"\n" for x in rows),encoding="utf-8",newline="\n")
print(json.dumps({"sha256":hashlib.sha256(OUT.read_bytes()).hexdigest(),"chunks":len(rows),"low":sum(x["confidence"]=="low" for x in rows),"accepted":sum(x["confidence"]!="low" for x in rows)}))
