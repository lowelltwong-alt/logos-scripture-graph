#!/usr/bin/env python3
"""Add conservative, candidate-only literary metadata to Sol's OT scaffolds.

This does not move a boundary or promote a chunk.  It annotates the existing
exact chapter frames so downstream specialist lanes know what to challenge.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol"
TARGETS = ["Deut", "Josh", "Judg", "Ruth", "2Kgs", "1Chr", "2Chr", "Ezra", "Neh", "Esth", "Ezek", "Dan", "Hos", "Joel", "Amos", "Obad", "Jonah", "Mic", "Nah", "Hab", "Zeph", "Hag", "Zech", "Mal"]

PROPHETS = {"Ezek", "Dan", "Hos", "Joel", "Amos", "Obad", "Jonah", "Mic", "Nah", "Hab", "Zeph", "Hag", "Zech", "Mal"}
HARD = {
    "Deut": {4: "Deut 4:6-8 wisdom/torah vocabulary and nations framing", 28: "Deut 28 blessing/curse parallelism and rare covenant terms", 32: "Deut 32 archaic Song of Moses diction and textual variants", 33: "Deut 33 tribal blessing poetry"},
    "Josh": {6: "Josh 6 ritual battle report and repeated formulae", 10: "Josh 10 long-day narrative and poetic quotation", 22: "Josh 22 altar dispute speech/report boundary"},
    "Judg": {5: "Judg 5 archaic victory song and tribal catalogue", 11: "Judg 11 vow narrative and translation ambiguity", 19: "Judg 19-21 escalating atrocity appendix"},
    "Ruth": {3: "Ruth 3 threshing-floor euphemism and dialogue ambiguity", 4: "Ruth 4 gate/legal-redeemer terminology and genealogy"},
    "2Kgs": {2: "2 Kgs 2 prophetic succession and ascension idiom", 5: "2 Kgs 5 purity/foreign-name translation issues", 17: "2 Kgs 17 historiographic editorial evaluation", 18: "2 Kgs 18 Rabshakeh speech and Assyrian loanwords", 25: "2 Kgs 25 siege chronology and restoration notice"},
    "1Chr": {1: "1 Chr 1 genealogical lists and name transliteration", 16: "1 Chr 16 liturgical psalm composite", 21: "1 Chr 21 census/angel narrative", 29: "1 Chr 29 doxological prayer and succession"},
    "2Chr": {5: "2 Chr 5 temple dedication liturgy", 20: "2 Chr 20 battle prayer/song", 30: "2 Chr 30 Passover reform narrative", 34: "2 Chr 34 law-book discovery and reform report", 36: "2 Chr 36 exile/decree closure"},
    "Ezra": {3: "Ezra 3 altar/foundation parallel ceremony", 4: "Ezra 4 imperial correspondence and register", 7: "Ezra 7 commission letter and legal diction", 9: "Ezra 9 communal confession prayer"},
    "Neh": {2: "Neh 2 royal authorization and inspection narrative", 8: "Neh 8 public reading/interpretive assembly", 9: "Neh 9 historical confession liturgy", 13: "Neh 13 episodic reform memoir"},
    "Esth": {1: "Esth 1 court banquet and reversal setup", 4: "Esth 4 lament/appeal dialogue", 8: "Esth 8 counter-edict legal formula", 9: "Esth 9 festival etiology and chronology"},
    "Ezek": {1: "Ezek 1 throne-chariot vision and technical imagery", 16: "Ezek 16 extended marriage allegory and difficult metaphors", 18: "Ezek 18 proverbial disputation", 37: "Ezek 37 valley vision and enacted oracle", 40: "Ezek 40-48 temple vision measurements"},
    "Dan": {2: "Dan 2 dream report/interpreted court tale", 3: "Dan 3 Aramaic court narrative and hymn", 7: "Dan 7 apocalyptic beasts and Aramaic symbols", 9: "Dan 9 penitential prayer and seventy-weeks vision", 12: "Dan 12 apocalyptic closure and sealed words"},
    "Hos": {1: "Hos 1 enacted marriage sign and naming", 6: "Hos 6 covenant lawsuit/poetic turns", 11: "Hos 11 parental metaphor and pathos", 14: "Hos 14 restoration poem"},
    "Joel": {2: "Joel 2 locust/army imagery and promise oracle", 3: "Joel 3 judgment vision and Zion oracle"},
    "Amos": {1: "Amos 1-2 nations oracle pattern and refrain", 5: "Amos 5 lament/woe and justice rhetoric", 7: "Amos 7 vision cycle and priest-prophet confrontation", 9: "Amos 9 restoration coda"},
    "Obad": {1: "Obadiah single oracle: Edom indictment, day-of-YHWH reversal"},
    "Jonah": {1: "Jonah 1 prophetic commission and storm narrative", 2: "Jonah 2 psalm embedded in narrative", 3: "Jonah 3 Nineveh proclamation and response", 4: "Jonah 4 disputation/parabolic plant episode"},
    "Mic": {1: "Mic 1 lament/procession oracle", 3: "Mic 3 indictment of leaders", 4: "Mic 4 Zion future poem", 6: "Mic 6 covenant lawsuit and liturgical question", 7: "Mic 7 lament/confession and restoration"},
    "Nah": {1: "Nah 1 acrostic-like opening and theophany", 2: "Nah 2 siege taunt/war tableau", 3: "Nah 3 city taunt and judgment imagery"},
    "Hab": {1: "Hab 1 prophetic complaint and divine answer", 2: "Hab 2 woe series and watchtower vision", 3: "Hab 3 theophanic psalm"},
    "Zeph": {1: "Zeph 1 day-of-YHWH indictment", 2: "Zeph 2 nations oracles", 3: "Zeph 3 judgment-to-restoration turn"},
    "Hag": {1: "Hag 1 dated exhortation and building response", 2: "Hag 2 dated oracles and signet promise"},
    "Zech": {1: "Zech 1 night visions and dated exhortation", 3: "Zech 3 heavenly tribunal vision", 4: "Zech 4 lampstand/olive trees vision", 9: "Zech 9-11 burden oracles and shepherd imagery", 12: "Zech 12-14 eschatological oracle cycle"},
    "Mal": {1: "Mal 1 disputation oracle and altar critique", 2: "Mal 2 priestly covenant disputation", 3: "Mal 3 messenger/refiner and tithe disputation", 4: "Mal 4 day-of-YHWH closing oracle"},
}

def chapter(row: dict) -> int:
    m = re.search(r"\.(\d+)\.", row["span"])
    if not m:
        raise ValueError(row["span"])
    return int(m.group(1))

def classify(book: str, ch: int) -> tuple[str, str]:
    if book == "Deut":
        if ch <= 4: return "historical_sermon", "Moses' retrospective wilderness address"
        if ch <= 11: return "covenant_exhortation", "covenant speech with remembered events and imperatives"
        if ch <= 26: return "covenant_law_collection", "stipulations framed as covenant instruction"
        if ch <= 30: return "covenant_ceremony_and_blessing", "ceremonial ratification, blessing/curse and choice speeches"
        return ("succession_speech_and_poetry" if ch < 34 else "blessing_poetry_and_death_notice"), "succession, song, blessing, and closing notices"
    if book in {"Josh", "Judg", "2Kgs", "1Chr", "2Chr", "Ezra", "Neh", "Esth"}:
        if book == "Esth": return "court_narrative", "court-scene narrative with reversal, decree, and banquet units"
        if book in {"Ezra", "Neh"} and ch in {7, 8, 9, 10, 13}: return "memoir_or_community_liturgy", "first-person/memoir, public reading, prayer, or reform report"
        if book in {"1Chr", "2Chr"} and ch in {1, 2, 3, 4, 5, 6, 7, 8, 9}: return "genealogy_or_annalistic_register", "genealogical/register material with formulaic transitions"
        if book in {"1Chr", "2Chr"} and ch in {16, 29, 20, 30}: return "liturgical_or_reform_narrative", "worship, prayer/song, or cultic reform narrative"
        return "historical_narrative", "annalistic or episodic narrative with speeches and formulaic notices"
    if book == "Ruth": return "short_story_with_dialogue_and_genealogy", "scene-based narrative with dialogue and genealogy closure"
    if book == "Dan": return ("apocalyptic_vision" if ch >= 7 else "court_tale"), "Aramaic court tale or symbolic vision cycle"
    if book in PROPHETS:
        return ("vision_oracle_cycle" if ch in HARD.get(book, {}) else "prophetic_oracle_poetry"), "oracle, disputation, lament, vision, or restoration poetry"
    return "literary_unit", "candidate chapter frame retained pending specialist boundary review"

def enrich(row: dict) -> dict:
    book, ch = row["book"], chapter(row)
    typ, rationale = classify(book, ch)
    hard = HARD.get(book, {}).get(ch)
    row.update({
        "literature_type_guess": typ,
        "working_title": hard or f"{book} {ch}: {rationale}",
        "boundary_rationale": f"Chapter frame retained as a conservative candidate; {rationale}. Internal shifts, refrains, speeches, and genre markers are flagged for red-team review.",
        "boundary_evidence_refs": [f"direct_read:eng-web:{row['span']}", f"literary_form_lane:{book}:{ch}", "whole_bible_role_source_matrix.v1", "candidate_only_no_authority"],
        "translation_difficulties": ["lexical and idiomatic Hebrew/Aramaic choices require specialist comparison", "English chapter boundary is a locator, not a literary-authority claim"],
        "cross_reference_clusters": [f"{book}:{ch}:internal_refrain_or_formula_review", "canonical_relations_lane_pending"],
        "hard_passage_forecast": hard or "No single high-risk feature preselected; inspect discourse shifts, rare lexemes, and textual variants.",
        "red_team_questions": ["Does a discourse, speaker, scene, refrain, or genre shift justify a subchapter boundary?", "Could a translation or chapter division conceal a continuous unit?", "Are cross-book echoes being mistaken for a boundary?"],
        "strong_or_hebrew_tags_used": ["evidence_only", "candidate_boundary", "literary_metadata_enriched", "not_boundary_authority"],
        "confidence": "medium_low" if hard else "low",
        "review_status": "candidate_literary_metadata_enriched_pending_b01_mesh",
        "review_holds": ["original_language_review", "canonical_premortem_review", "ancient_context_gap", "red_team_boundary_review", "boss_authorization"],
        "non_authorizing": True,
    })
    return row

def main() -> int:
    changed = 0
    for book in TARGETS:
        path = MODEL / "book_chunks" / book / "chunks.jsonl"
        rows = [enrich(json.loads(line)) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        path.write_text("".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in rows), encoding="utf-8", newline="\n")
        changed += len(rows)
    # Rebuild the canonical candidate-only aggregate using the existing builder.
    import subprocess, sys
    subprocess.run([sys.executable, str(ROOT / "scripts/build_m7_sol_whole_bible_candidate_map.py")], check=True)
    print(json.dumps({"books": len(TARGETS), "rows_enriched": changed, "candidate_only": True, "non_authorizing": True}, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
