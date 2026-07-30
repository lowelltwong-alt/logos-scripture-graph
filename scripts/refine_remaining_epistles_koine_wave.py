#!/usr/bin/env python3
"""Refine remaining epistle metadata without changing candidate spans."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol"
BOOKS = ["1Cor","2Cor","Gal","Eph","Phil","Col","1Thess","2Thess","1Tim","2Tim","Titus","Phlm","Jas","1Pet","2Pet","1John","2John","3John","Jude"]
WAVE = "remaining_epistles_koine_wave.v1"
FORMS = {
 "1Cor":"argumentative_letter", "2Cor":"apologia_and_paraenesis", "Gal":"argumentative_letter", "Eph":"circular_exposition_letter", "Phil":"friendship_paraenesis_letter", "Col":"exposition_letter", "1Thess":"pastoral_paraenesis_letter", "2Thess":"eschatological_paraenesis_letter", "1Tim":"pastoral_instruction_letter", "2Tim":"farewell_pastoral_letter", "Titus":"pastoral_instruction_letter", "Phlm":"situational_request_letter", "Jas":"wisdom_paraenesis_letter", "1Pet":"diaspora_paraenesis_letter", "2Pet":"testamentary_warning_letter", "1John":"circular_homily", "2John":"epistolary_warning", "3John":"epistolary_recommendation", "Jude":"polemical_paraenesis_letter"
}

def update(rows: list[dict], book: str) -> int:
    target=[r for r in rows if r.get("book")==book]
    total=max([int(r["chunk_index_in_book"]) for r in target] or [1])
    for r in target:
        n=int(r["chunk_index_in_book"])
        if n==1: seams=["salutation_to_thesis", "opening_prayer_or_thanks"]
        elif n==total: seams=["exposition_to_closing", "paraenesis_or_greeting_closure"]
        elif n <= max(2,total//3): seams=["thesis_to_support", "quotation_or_reasoning_transition"]
        elif n <= max(3,(2*total)//3): seams=["scriptural_reasoning_or_counterargument", "discourse_resumption"]
        else: seams=["exposition_to_paraenesis", "community_application_or_warning"]
        r["literature_type_guess"]=FORMS[book]
        r["working_title_origin"]=WAVE
        r["working_title_is_boundary_authority"]=False
        r["boundary_rationale"]="Candidate outer span retained provisionally; epistolary exposition, argument, quotation, and paraenesis signals are seam leads requiring independent Koine review."
        r["candidate_internal_seams"]=seams
        r["translation_difficulties"]=["Koine Greek aspect, participles, discourse particles, quotation scope, and compressed lexical fields require source-level review"]
        r["original_language_translation_holds"]=["CNTR/SBLGNT/UGNT comparison required; English paragraphing cannot decide seams"]
        r["cross_reference_clusters"]=["Internal argument, scriptural quotation, and parallel epistolary motifs are evidence-only relation leads"]
        r["cross_reference_holds"]=["Do not harmonize epistles or use later doctrinal reception as boundary authority"]
        r["hard_passage_forecast"]=["Quotation/echo boundaries, diatribe voices, and exposition-to-paraenesis transitions may cross chapter edges"]
        r["red_team_questions"]=["Does each seam survive removal of English headings and chapter numbers?", "Is a quoted source or rhetorical voice being mistaken for an authorial boundary?"]
        r["red_team_premortem_holds"]=["Do not turn lexical or doctrinal labels into theological conclusions; preserve Greek textual and discourse uncertainty"]
        r["review_revision"]=int(r.get("review_revision",0))+1
        refs=list(r.get("boundary_evidence_refs") or [])
        if WAVE not in refs: refs.append(WAVE)
        r["boundary_evidence_refs"]=refs
        r["candidate_only"]=True; r["non_authorizing"]=True
    return len(target)

def main()->int:
    reports=[]
    paths=[MODEL/"state/evidence/final/whole_bible_candidate_map.jsonl"]+[MODEL/"book_chunks"/b/"chunks.jsonl" for b in BOOKS]
    for path in paths:
        rows=[json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
        for b in BOOKS:
            n=update(rows,b)
            if n: reports.append({"path":str(path),"book":b,"rows_changed":n})
        path.write_text("".join(json.dumps(r,ensure_ascii=False,separators=(",",":"))+"\n" for r in rows),encoding="utf-8",newline="\n")
    print(json.dumps({"books":BOOKS,"wave":WAVE,"reports":reports,"candidate_only":True,"non_authorizing":True,"spans_unchanged":True},sort_keys=True))
    return 0
if __name__=="__main__": raise SystemExit(main())
