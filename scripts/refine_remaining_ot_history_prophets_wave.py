#!/usr/bin/env python3
"""Refine remaining OT historical/prophetic metadata without changing spans."""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MODEL=ROOT/".ai/scratch/multi_model_bible_chunking/M7_sol"
BOOKS=["1Chr","1Kgs","1Sam","2Chr","2Kgs","2Sam","Ezra","Neh","Josh","Judg","Ruth","Esth","Amos","Hab","Hag","Hos","Joel","Jonah","Mal","Mic","Nah","Obad","Zeph"]
WAVE="remaining_ot_history_prophets_wave.v1"
FORM={
 "1Chr":"chronicle_genealogy_and_court_narrative","2Chr":"chronicle_court_and_temple_narrative","1Kgs":"royal_succession_and_annalistic_narrative","2Kgs":"royal_annalistic_and_exile_narrative","1Sam":"prophetic_and_royal_narrative","2Sam":"royal_narrative_and_lament","Josh":"conquest_and_allocation_narrative","Judg":"deliverer_cycle_narrative","Ruth":"short_prose_kinship_narrative","Ezra":"restoration_and_community_narrative","Neh":"restoration_memoir_and_register","Esth":"court_reversal_narrative","2Sam":"royal_narrative_and_lament",
 "Amos":"prophetic_lawsuit_and_vision_collection","Hab":"prophetic_complaint_and_response","Hag":"dated_prophetic_exhortation","Hos":"prophetic_marriage_and_lawsuit_collection","Joel":"prophetic_lament_and_day_oracle","Jonah":"prophetic_commission_and_narrative","Mal":"disputation_oracle_collection","Mic":"prophetic_lawsuit_and_hope_collection","Nah":"judgment_oracle_and_hymnic_opening","Obad":"single_prophetic_oracle","Zeph":"day_of_YHWH_oracle_collection"
}

def classify(book,title):
    t=title.lower()
    if any(k in t for k in ["genealog", "register", "list", "inventory", "annal"]): return "register_or_annalistic_unit",["register_formula","name_or_territory_transition","register_closure"]
    if any(k in t for k in ["lament","song","poem"]): return "narrative_or_poetic_insert",["poetic_opening","lament_or_song_turn","poetic_closure"]
    if book in {"Amos","Hab","Hag","Hos","Joel","Mal","Mic","Nah","Obad","Zeph"}: return FORM[book],["oracle_heading_or_date","oracle_or_vision_turn","oracle_closure"]
    if book=="Jonah": return FORM[book],["commission_or_departure","prayer_or_dialogue","narrative_closure"]
    if book=="Ruth": return FORM[book],["scene_change","dialogue_or_legal_exchange","genealogy_or_closure"]
    if book=="Esth": return FORM[book],["court_scene","banquet_or_decree","reversal_or_closure"]
    return FORM[book],["scene_or_speech_transition","war_court_or_ritual_turn","narrative_closure"]

def update(rows,book):
    n=0
    for r in rows:
        if r.get("book")!=book: continue
        form,seams=classify(book,r.get("working_title",""))
        r["literature_type_guess"]=form; r["working_title_origin"]=WAVE; r["working_title_is_boundary_authority"]=False
        r["boundary_rationale"]="Outer candidate span retained provisionally; narrative, register, oracle, lament, and closure signals are seam leads requiring qualified Hebrew review."
        r["candidate_internal_seams"]=seams
        r["translation_difficulties"]=["Hebrew narrative sequencing, proper names, poetic wordplay, prophetic particles, chronology, and register formulae require source-level review"]
        r["original_language_translation_holds"]=["OSHB/UXLC comparison required; English headings, chronology, and inherited paragraphing cannot decide seams"]
        r["cross_reference_clusters"]=["Internal historical, prophetic, royal, exile, and restoration parallels are evidence-only relation leads"]
        r["cross_reference_holds"]=["Do not harmonize parallel histories or use later canonical reception as boundary authority"]
        r["hard_passage_forecast"]=["Chronological notices, embedded speeches, register-to-narrative shifts, and oracle headings may cross modern chapter edges"]
        r["red_team_questions"]=["Does each seam survive removal of English headings and chapter numbers?","Is chronology or a parallel account being mistaken for local literary boundary evidence?"]
        r["red_team_premortem_holds"]=["Do not turn historical or prophetic labels into theological conclusions; preserve Hebrew lexical and textual-variant holds"]
        r["review_revision"]=int(r.get("review_revision",0))+1
        refs=list(r.get("boundary_evidence_refs") or [])
        if WAVE not in refs: refs.append(WAVE)
        r["boundary_evidence_refs"]=refs; r["candidate_only"]=True; r["non_authorizing"]=True; n+=1
    return n

def main():
    reports=[]; paths=[MODEL/"state/evidence/final/whole_bible_candidate_map.jsonl"]+[MODEL/"book_chunks"/b/"chunks.jsonl" for b in BOOKS]
    for p in paths:
        rows=[json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
        for b in BOOKS:
            n=update(rows,b)
            if n: reports.append({"path":str(p),"book":b,"rows_changed":n})
        p.write_text("".join(json.dumps(r,ensure_ascii=False,separators=(",",":"))+"\n" for r in rows),encoding="utf-8",newline="\n")
    print(json.dumps({"books":BOOKS,"wave":WAVE,"reports":reports,"candidate_only":True,"non_authorizing":True,"spans_unchanged":True},sort_keys=True))
if __name__=="__main__": main()
