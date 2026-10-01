#!/usr/bin/env python3
"""Refine Genesis 1–11 literary metadata without changing candidate spans."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks/Gen/chunks.jsonl",
    ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/state/evidence/final/whole_bible_candidate_map.jsonl",
]
WAVE = "gen_1_11_literary_wave.v1"

DETAILS = {
    1: ("creation_sequence", "Creation sequence with repeated day-formula and seventh-day closure", ["day_formula_refrain", "evaluation_formula", "seventh_day_closure"]),
    2: ("creation_garden_narrative", "Creation/garden narrative with human placement and kinship scene", ["garden_setup", "human_formation", "command_and_kinship_transition"]),
    3: ("transgression_expulsion_narrative", "Serpent dialogue, transgression, judgment speeches, and expulsion", ["dialogue_sequence", "judgment_speech", "expulsion_closure"]),
    4: ("sibling_conflict_and_genealogy", "Sibling conflict narrative followed by genealogy and cultural notices", ["offering_or_conflict_scene", "judgment_dialogue", "genealogy_transition"]),
    5: ("genealogical_register", "Adam-to-Noah genealogy with repeated begetting/death formula", ["genealogy_formula", "exception_or_note", "register_closure"]),
    6: ("corruption_and_flood_preparation", "Humanity-corruption notice, Noah frame, and flood preparation instructions", ["corruption_notice", "noah_favor_frame", "construction_instruction"]),
    7: ("flood_narrative", "Flood entry, rising waters, and enclosure/forty-day sequence", ["entry_notice", "rising_waters", "forty_day_or_closure_formula"]),
    8: ("flood_receding_and_covenant_setup", "Waters recede, ark release tests, altar scene, and earth-cycle promise", ["receding_waters", "release_test", "altar_and_promise_transition"]),
    9: ("noahic_covenant_and_household_narrative", "Covenant sign speech, household episode, and genealogy transition", ["covenant_speech", "sign_formula", "household_episode"]),
    10: ("table_of_nations_genealogy", "Nations genealogy organized by descendant and territorial notices", ["genealogical_unit", "territory_or_language_notice", "register_closure"]),
    11: ("babel_and_shem_genealogy", "Babel city/tower episode followed by Shem genealogy and migration frame", ["city_project", "divine_speech_and_dispersion", "genealogy_to_migration_transition"]),
}


def refine(rows: list[dict]) -> int:
    changed = 0
    for row in rows:
        if row.get("book") != "Gen":
            continue
        chapter = int(row["span"].split(".", 2)[1].split("-", 1)[0])
        if chapter not in DETAILS:
            continue
        form, title, seams = DETAILS[chapter]
        row["literature_type_guess"] = form
        row["working_title"] = title
        row["working_title_origin"] = WAVE
        row["working_title_is_boundary_authority"] = False
        row["boundary_rationale"] = "Outer candidate span retained provisionally; repeated formulas, scene transitions, and genealogy/register signals are internal seam leads requiring independent Hebrew review."
        row["candidate_internal_seams"] = seams
        row["translation_difficulties"] = ["Hebrew waw-consecutive/narrative sequencing, repeated formula scope, lexical ambiguity, and genealogy/register syntax require source-level review"]
        row["original_language_translation_holds"] = ["OSHB/UXLC comparison required; English paragraphing, headings, and inherited verse presentation cannot decide seams"]
        row["cross_reference_clusters"] = ["Creation, flood, covenant, genealogy, and Babel parallels are internal canonical retrieval leads only"]
        row["cross_reference_holds"] = ["Do not use later biblical reuse or theological harmonization as boundary authority"]
        row["hard_passage_forecast"] = ["Formula repetition, genealogy/register transitions, and dialogue-to-narrative shifts may cross modern chapter edges"]
        row["red_team_questions"] = ["Does each proposed seam survive removal of English headings and chapter numbers?", "Are formula repetition and scene closure being distinguished from mere translation paragraphing?"]
        row["red_team_premortem_holds"] = ["Do not treat creation-day, flood, covenant, or Babel labels as theological conclusions or authoritative boundaries"]
        row["review_revision"] = int(row.get("review_revision", 0)) + 1
        refs = list(row.get("boundary_evidence_refs") or [])
        if WAVE not in refs:
            refs.append(WAVE)
        row["boundary_evidence_refs"] = refs
        row["candidate_only"] = True
        row["non_authorizing"] = True
        changed += 1
    return changed


def main() -> int:
    reports = []
    for path in PATHS:
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        changed = refine(rows)
        path.write_text("".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows), encoding="utf-8", newline="\n")
        reports.append({"path": str(path), "rows_changed": changed})
    print(json.dumps({"book": "Gen", "chapters": list(DETAILS), "wave": WAVE, "rows_changed": reports, "spans_unchanged": True, "candidate_only": True, "non_authorizing": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
