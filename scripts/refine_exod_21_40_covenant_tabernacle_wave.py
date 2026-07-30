#!/usr/bin/env python3
"""Refine Exodus 21–40 law/tabernacle metadata without changing spans."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks/Exod/chunks.jsonl",
    ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/state/evidence/final/whole_bible_candidate_map.jsonl",
]
WAVE = "exod_21_40_covenant_tabernacle_wave.v1"
DETAILS = {
    21: ("casuistic_covenant_law", "Casuistic ordinances concerning persons, injury, property, and restitution", ["case_heading", "condition_action_result", "restitution_closure"]),
    22: ("apodictic_social_law", "Social, judicial, sabbatical, and festival directives", ["directive_sequence", "social_case", "festival_transition"]),
    23: ("covenant_journey_speech", "Covenant journey, land, protection, and epilogue speech", ["messenger_or_journey", "land_promise", "speech_closure"]),
    24: ("covenant_ratification_narrative", "Covenant assent, writing, blood rite, ascent, and cloud", ["ratification_sequence", "blood_rite", "cloud_closure"]),
    25: ("sanctuary_instruction", "Offering and sanctuary-furniture instructions", ["offering_call", "furniture_sequence", "presence_or_closure"]),
    26: ("tabernacle_instruction", "Curtains, frames, veil, and entrance instructions", ["material_specification", "assembly_sequence", "veil_or_entrance_closure"]),
    27: ("tabernacle_court_instruction", "Altar, court, and continual lamp instructions", ["altar_specification", "court_specification", "continual_lamp_closure"]),
    28: ("priestly_garment_instruction", "Priestly office authorization and garment instructions", ["office_heading", "garment_sequence", "presence_or_memorial_closure"]),
    29: ("priestly_consecration_instruction", "Priestly consecration, daily offerings, and meeting-place closure", ["consecration_sequence", "daily_offering", "meeting_place_closure"]),
    30: ("sanctuary_equipment_instruction", "Incense altar, ransom, basin, anointing oil, and incense formulations", ["equipment_sequence", "ransom_or_purity_case", "formula_restriction"]),
    31: ("artisan_commission_and_sabbath_close", "Artisan commission, Sabbath close, and tablets", ["commission_notice", "sabbath_frame", "tablets_closure"]),
    32: ("covenant_breach_narrative", "Calf construction and first intercession", ["construction_scene", "divine_response", "intercession"]),
    33: ("covenant_breach_aftermath", "Descent, broken tablets, inquiry, Levite action, and aftermath", ["descent_scene", "inquiry_or_judgment", "action_closure"]),
    34: ("intercession_and_presence_dialogue", "Second intercession, messenger response, mourning, and presence dialogue", ["intercession_sequence", "camp_mourning", "presence_request"]),
    35: ("tent_of_meeting_presence_dialogue", "Tent-of-meeting frame and presence/glory dialogue", ["tent_frame", "presence_dialogue", "glory_question"]),
    36: ("covenant_renewal_narrative", "New tablets, name proclamation, and Moses' appeal", ["tablet_replacement", "name_proclamation", "appeal_closure"]),
    37: ("covenant_renewal_stipulation", "Covenant-renewal stipulations and inscription", ["stipulation_sequence", "festival_or_sabbath_rule", "inscription_closure"]),
    38: ("radiant_descent_frame", "Radiant descent and veil notice", ["descent_notice", "radiance_effect", "veil_closure"]),
    39: ("tabernacle_contribution_and_commission", "Sabbath frame, contribution call, and willing offerings", ["sabbath_frame", "contribution_call", "willing_response"]),
    40: ("tabernacle_construction_and_closure", "Artisan commissioning, construction, inventory, garments, inspection, and glory closure", ["commission_and_construction", "inventory_or_inspection", "glory_and_travel_closure"]),
}


def refine(rows: list[dict]) -> int:
    changed = 0
    for row in rows:
        if row.get("book") != "Exod":
            continue
        chapter = int(row["span"].split(".", 2)[1].split("-", 1)[0])
        if chapter not in DETAILS:
            continue
        form, title, seams = DETAILS[chapter]
        row["literature_type_guess"] = form
        row["working_title"] = title
        row["working_title_origin"] = WAVE
        row["working_title_is_boundary_authority"] = False
        row["boundary_rationale"] = "Outer candidate span retained provisionally; law-form, covenant, specification/construction, and prose-frame signals are seam leads requiring qualified Hebrew review."
        row["candidate_internal_seams"] = seams
        row["translation_difficulties"] = ["Hebrew casuistic/apodictic syntax, technical tabernacle vocabulary, covenant formulae, and specification/construction repetition require source-level review"]
        row["original_language_translation_holds"] = ["OSHB/UXLC comparison required; English legal or architectural labels cannot decide seams"]
        row["cross_reference_clusters"] = ["Covenant, sanctuary, priestly, construction, and glory/travel parallels are evidence-only internal relation leads"]
        row["cross_reference_holds"] = ["Do not use later tabernacle/temple or theological harmonization as boundary authority"]
        row["hard_passage_forecast"] = ["Casuistic clauses, repeated specification/construction lists, and covenant-renewal speech may cross modern chapter edges"]
        row["red_team_questions"] = ["Does each seam preserve condition→action→result or specification→execution logic after removing English headings?", "Are repeated architectural terms source-verified rather than assumed from translation tradition?"]
        row["red_team_premortem_holds"] = ["Do not collapse law, narrative, specification, and construction functions; preserve unresolved Hebrew lexical and textual-variant holds"]
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
    print(json.dumps({"book": "Exod", "wave": WAVE, "rows_changed": reports, "spans_unchanged": True, "candidate_only": True, "non_authorizing": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
