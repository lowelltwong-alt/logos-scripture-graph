#!/usr/bin/env python3
"""Add candidate-only literary/discourse metadata to Romans--Revelation.

This is a deterministic refinement of chapter-complete scaffolds.  It does not
claim specialist review, translation resolution, or theological authority.
Both the per-book files and the consolidated candidate feed are updated so
their records remain byte-for-byte semantically consistent.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol"
TARGETS = ["Rom","1Cor","2Cor","Gal","Eph","Phil","Col","1Thess","2Thess","1Tim","2Tim","Titus","Phlm","Heb","Jas","1Pet","2Pet","1John","2John","3John","Jude","Rev"]

EPISTLE = {"Rom":"argumentative_letter","1Cor":"argumentative_letter","2Cor":"apologia_and_paraenesis","Gal":"argumentative_letter","Eph":"circular_letter_exposition","Phil":"friendship_letter_paraenesis","Col":"christological_exposition_letter","1Thess":"pastoral_letter_paraenesis","2Thess":"eschatological_paraenesis_letter","1Tim":"pastoral_instruction_letter","2Tim":"farewell_pastoral_letter","Titus":"pastoral_instruction_letter","Phlm":"situational_request_letter","Heb":"homiletic_exposition_with_paraenesis","Jas":"wisdom_paraenesis_letter","1Pet":"diaspora_paraenesis_letter","2Pet":"testamentary_paraenesis_letter","1John":"circular_homily","2John":"epistolary_warning","3John":"epistolary_recommendation","Jude":"polemical_paraenesis_letter"}
GREEK_HOLDS = {
 "Rom":["dikaiosyne/pistis/sarx lexical range","nomos and ergon translation choices","oun/gar discourse connectors"],
 "1Cor":["soma and pneuma lexical range","agape and charismata translation choices","hina/de discourse transitions"],
 "2Cor":["paraklesis and diakonia lexical range","doxa and katallasso translation choices","de/gar contrast markers"],
 "Gal":["pistis and nomos lexical range","paidagogos and stoicheia translation choices","de/oun argumentative particles"],
 "Eph":["mysterion and oikonomia lexical range","kephale and pleroma translation choices","dio/oun discourse transitions"],
 "Phil":["kenosis and phroneo lexical range","politeuma and dikaiosyne translation choices","oun/men discourse markers"],
 "Col":["pleroma and stoicheia lexical range","mysterion and eikon translation choices","oun/dia discourse transitions"],
 "1Thess":["parousia and hagiasmos lexical range","ekloge and hypomone translation choices","dio/oun discourse markers"],
 "2Thess":["apostasia and katechon lexical range","parousia and apokalypsis translation choices","de/gar eschatological transitions"],
 "1Tim":["episkope and eusebeia lexical range","pistis and syneidesis translation choices","oun/ina instruction markers"],
 "2Tim":["paratheke and hypomone lexical range","theopneustos and elencho translation choices","oun/de farewell transitions"],
 "Titus":["soterios and epiphaneia lexical range","presbyteros and sophron translation choices","gar/ina instruction markers"],
 "Phlm":["paraklesis and koinonia lexical range","anapempo and splanchna translation choices","dio/oun request transitions"],
 "Heb":["teleios and pistis lexical range","diatheke and leitourgos translation choices","dio/oun homiletic transitions"],
 "Jas":["dipsychos and teleios lexical range","ergon and nomos translation choices","dio/oun paraenetic transitions"],
 "1Pet":["paroikia and anastrophe lexical range","pascho and episkope translation choices","dio/oun paraenetic transitions"],
 "2Pet":["epignosis and apoleia lexical range","parousia and rhetorically compressed idioms","dio/oun warning transitions"],
 "1John":["koinonia and hilasmos lexical range","meno and parresia translation choices","hina/oti discourse markers"],
 "2John":["plane and antichristos lexical range","meno and didache translation choices","oti/gar warning transitions"],
 "3John":["philoproteuo and mimou lexical range","martyria and propempo translation choices","gar/oun recommendation transitions"],
 "Jude":["asebeia and tereo lexical range","sarka and doxa translation choices","de/oun polemical transitions"],
 "Rev":["apokalypsis and martyria lexical range","therion, nikao, and proskuneo translation choices","kai/tote vision transitions"]}

def chapter_role(book: str, n: int, total: int) -> tuple[str,str]:
    if book == "Rev":
        if n <= 3: return "epistolary_prologue_and_apocalyptic_commissions", "address-to-vision transition"
        if 4 <= n <= 5: return "heavenly_throne_vision", "throne-room frame"
        if 6 <= n <= 16: return "cycle_of_apocalyptic_visions", "seal/trumpet/bowl cycle seam"
        if 17 <= n <= 20: return "judgment_and_victory_vision_cycle", "Babylon/judgment/kingdom seam"
        return "new_creation_epilogue_vision", "vision-to-epilogue seam"
    if book == "Heb":
        if n in (1,2,3,4,5,6,7,8,9,10,11): return "scriptural_exposition_with_exhortation", "exposition-to-warning or exhortation seam"
        return "closing_paraenesis_and_benediction", "exposition-to-closing seam"
    if book in {"Jas","1Pet","2Pet","Jude"}: return "paraenetic_exhortation_and_warning", "virtue/warning movement seam"
    if book in {"1John","2John","3John"}: return "testimony_and_community_discernment", "claim-testimony-application seam"
    if n == 1: return "opening_salutation_and_thesis", "salutation-to-thesis seam"
    if n == total: return "closing_paraenesis_and_greetings", "argument-to-closing seam"
    if n <= max(2, total//3): return "argumentative_exposition", "thesis-to-support transition"
    if n <= max(3, (2*total)//3): return "scriptural_reasoning_and_counterargument", "proof/counterargument seam"
    return "paraenesis_and_community_application", "exposition-to-exhortation seam"

def update(rec: dict) -> dict:
    b = rec["book"]; n = int(rec["chunk_index_in_book"]); total = 1
    # total is filled by caller; this fallback is only defensive.
    role, seam = chapter_role(b, n, rec.get("_total", n))
    rec.pop("_total", None)
    rec["literature_type_guess"] = role
    rec["structural_unit_type"] = role
    rec["discourse_function_guess"] = seam
    rec["boundary_rationale"] = ("Candidate chapter-span retained as a structural unit; " + seam + ". "
        "Internal seams are flagged for specialist review; no theological conclusion is asserted.")
    rec["candidate_internal_seams"] = [seam, "speech/quotation or scene transition where present", "chapter-boundary fallback pending B01 mesh"]
    rec["koine_greek_translation_holds"] = GREEK_HOLDS[b]
    rec["cross_reference_holds"] = ["intra-book discourse and quotation links require verified canonical source mapping", "parallel NT/OT echoes are leads only; no directionality asserted"]
    rec["red_team_premortem_holds"] = ["chapter boundary may hide a speech or vision seam", "translation particle/lexeme may alter apparent discourse boundary", "quotation/allusion boundary must not be inferred without source evidence"]
    rec["review_revision"] = max(int(rec.get("review_revision", 0)), 1)
    rec["review_status"] = "candidate_scaffold_literary_refinement_pending_typed_b01_mesh"
    rec["review_holds"] = sorted(set(rec.get("review_holds", [])) | {"literary_form_review","original_language_review","canonical_premortem_review","translation_review","red_team_review","ancient_context_gap","boss_authorization"})
    rec["confidence"] = "low"
    rec["non_authorizing"] = True
    return rec

def main() -> None:
    paths = [MODEL/"state/evidence/final/whole_bible_candidate_map.jsonl"] + [MODEL/"book_chunks"/b/"chunks.jsonl" for b in TARGETS]
    for path in paths:
        if not path.exists(): continue
        rows = [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
        totals = {}
        for r in rows: totals[r["book"]] = max(totals.get(r["book"], 0), int(r["chunk_index_in_book"]))
        out=[]
        for r in rows:
            if r.get("book") in TARGETS:
                r["_total"] = totals[r["book"]]
                r = update(r)
            out.append(json.dumps(r, ensure_ascii=False, separators=(",", ":")))
        path.write_text("\n".join(out)+"\n", encoding="utf-8")
        print(path)

if __name__ == "__main__": main()

