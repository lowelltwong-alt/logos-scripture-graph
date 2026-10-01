#!/usr/bin/env python3
"""Build Sol's independent Exodus revision-0 candidate from the signed-off book strategy."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
MODEL = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol"
OUTPUT = MODEL / "book_chunks" / "Exod" / "chunks.jsonl"
PASSAGES = ROOT / "data" / "canonical" / "scripture" / "passages" / "passages.jsonl"

# start, end, title, literary form, confidence
ENTRIES = [
    ("1.1", "1.7", "Names of Israel and multiplication threshold", "genealogical_threshold", "medium"),
    ("1.8", "1.22", "Escalating oppression, midwives, and river decree", "oppression_narrative", "high"),
    ("2.1", "2.10", "Moses' birth, river rescue, adoption, and naming", "origin_narrative", "high"),
    ("2.11", "2.22", "Moses' interventions, flight, and settlement in Midian", "flight_and_settlement_narrative", "high"),
    ("2.23", "3.22", "Israel's cry, divine remembrance, bush encounter, and first commission", "affliction_and_commission_narrative", "medium_low"),
    ("4.1", "4.17", "Signs, objections, and Aaron's provision complete the call dialogue", "commission_objection_dialogue", "medium_low"),
    ("4.18", "4.31", "Return journey, lodging incident, Aaron's meeting, and Israel's response", "return_and_recognition_narrative", "low"),
    ("5.1", "6.1", "First audience, increased burden, protests, and response", "confrontation_setback_narrative", "high"),
    ("6.2", "6.13", "Renewed commission speech and Moses' renewed objection", "recommission_dialogue", "medium_low"),
    ("6.14", "7.13", "Genealogical authorization, resumed commission, and rod sign", "embedded_genealogy_and_sign", "medium_low"),
    ("7.14", "7.25", "Nile confrontation and blood-plague cycle", "plague_cycle", "high"),
    ("8.1", "8.15", "Frog-plague cycle through Pharaoh's reversal", "plague_cycle", "high"),
    ("8.16", "8.19", "Dust and lice sign with magicians' recognition", "plague_cycle", "high"),
    ("8.20", "8.32", "Swarms, negotiation, removal, and renewed refusal", "plague_cycle", "high"),
    ("9.1", "9.7", "Livestock-plague warning, distinction, and refusal", "plague_cycle", "high"),
    ("9.8", "9.12", "Ashes and boils sign", "plague_cycle", "high"),
    ("9.13", "9.35", "Hail warning, differentiated response, storm, and reversal", "plague_cycle", "medium"),
    ("10.1", "10.20", "Locust warning, negotiations, devastation, and reversal", "plague_cycle", "medium"),
    ("10.21", "11.10", "Darkness confrontation and continuous final-plague announcement", "plague_cycle_and_final_warning", "medium_low"),
    ("12.1", "12.28", "Passover and unleavened-bread instruction through Israel's response", "ritual_instruction_and_response", "medium_low"),
    ("12.29", "12.42", "Death of the firstborn, urgent departure, and vigil summary", "departure_narrative", "high"),
    ("12.43", "13.16", "Passover participation, firstborn consecration, and memorial teaching", "ritual_memorial_instruction", "medium_low"),
    ("13.17", "14.31", "Wilderness route, pursuit, sea crossing, and prose resolution", "deliverance_narrative", "high"),
    ("15.1", "15.21", "Song of the Sea and Miriam's responsive refrain", "victory_song_with_refrain", "medium_low"),
    ("15.22", "15.27", "Marah testing, provision, and Elim transition", "wilderness_episode", "high"),
    ("16.1", "16.36", "Manna, quail, Sabbath test, naming, and memorial", "provision_narrative_with_instruction", "medium_low"),
    ("17.1", "17.7", "Water crisis at Rephidim and naming closure", "wilderness_episode", "high"),
    ("17.8", "17.16", "Amalek conflict and memorial closure", "conflict_and_memorial_narrative", "high"),
    ("18.1", "18.12", "Jethro's arrival, recounting, acclaim, and meal", "reunion_and_report_narrative", "high"),
    ("18.13", "18.27", "Judicial overload, Jethro's counsel, implementation, and departure", "administrative_narrative", "high"),
    ("19.1", "19.25", "Sinai arrival, covenant address, preparation, theophany, and bounds", "sinai_theophany_narrative", "medium_low"),
    ("20.1", "20.21", "Divine covenant address and the people's fearful response", "decalogue_and_narrative_response", "medium_low"),
    ("20.22", "20.26", "Heavenly speech reminder and altar directives", "covenant_speech_opening", "medium"),
    ("21.1", "22.17", "Casuistic ordinances concerning persons, injury, property, and restitution", "casuistic_legal_collection", "medium_low"),
    ("22.18", "23.19", "Apodictic social, judicial, sabbatical, and festival directives", "apodictic_legal_collection", "medium_low"),
    ("23.20", "23.33", "Covenant speech's journey and land epilogue", "covenant_speech_epilogue", "medium"),
    ("24.1", "24.18", "Covenant assent, writing, blood rite, communal ascent, and cloud", "covenant_ratification_and_ascent", "medium_low"),
    ("25.1", "25.40", "Offering and sanctuary-furniture instructions", "sanctuary_instruction_cluster", "medium_low"),
    ("26.1", "26.37", "Tabernacle curtains, frame, veil, and entrance instructions", "architectural_instruction_cluster", "medium_low"),
    ("27.1", "27.21", "Altar, court, and continual lamp instructions", "sanctuary_instruction_cluster", "medium_low"),
    ("28.1", "28.43", "Priestly office and garment instructions", "priestly_instruction_cluster", "medium_low"),
    ("29.1", "29.46", "Priestly consecration, daily offerings, and meeting-place closure", "consecration_instruction_cluster", "medium_low"),
    ("30.1", "30.38", "Incense altar, census, basin, anointing oil, and incense", "ritual_instruction_cluster", "medium_low"),
    ("31.1", "31.18", "Artisan commission, Sabbath close, and tablets", "instruction_corpus_closure", "medium_low"),
    ("32.1", "32.14", "Calf construction and Moses' first intercession", "breach_and_intercession_narrative", "medium_low"),
    ("32.15", "32.29", "Descent, broken tablets, Aaron inquiry, and Levite action", "breach_judgment_narrative", "medium_low"),
    ("32.30", "33.6", "Second intercession, divine response, and camp mourning", "intercession_and_presence_crisis", "medium_low"),
    ("33.7", "33.23", "Tent-of-meeting frame and presence/glory dialogue", "presence_dialogue", "medium_low"),
    ("34.1", "34.9", "New tablets, name proclamation, and Moses' appeal", "renewal_encounter", "medium_low"),
    ("34.10", "34.28", "Covenant renewal stipulations and inscription", "renewal_covenant_speech", "medium_low"),
    ("34.29", "34.35", "Radiant descent and veil notice", "descent_and_closure_narrative", "medium"),
    ("35.1", "35.29", "Sabbath frame, contribution call, and willing offerings", "assembly_and_offering_narrative", "medium_low"),
    ("35.30", "36.7", "Artisan commissioning and sufficient-contribution closure", "artisan_commission_narrative", "medium"),
    ("36.8", "36.38", "Construction of the tabernacle structure", "construction_report", "medium_low"),
    ("37.1", "37.29", "Construction of ark, table, lampstand, incense altar, oil, and incense", "construction_report", "medium_low"),
    ("38.1", "38.20", "Construction of altar, basin, and court", "construction_report", "medium_low"),
    ("38.21", "38.31", "Tabernacle material inventory", "material_inventory", "medium"),
    ("39.1", "39.31", "Construction of priestly garments", "construction_report", "medium_low"),
    ("39.32", "39.43", "Completion, presentation, inspection, and blessing", "completion_and_inspection_narrative", "high"),
    ("40.1", "40.38", "Installation command and execution through glory and travel closure", "installation_and_book_closure", "medium_low"),
]


def canonical_refs() -> list[str]:
    refs = []
    with PASSAGES.open(encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            if row.get("book") == "Exod":
                refs.append(row["osis_ref"])
    return refs


def main() -> int:
    refs = canonical_refs()
    positions = {ref: index for index, ref in enumerate(refs)}
    covered: list[str] = []
    rows: list[dict] = []
    for index, (start, end, title, form, confidence) in enumerate(ENTRIES, 1):
        start_ref, end_ref = f"Exod.{start}", f"Exod.{end}"
        if start_ref not in positions or end_ref not in positions:
            raise SystemExit(f"unknown endpoint {start_ref}-{end_ref}")
        covered.extend(refs[positions[start_ref] : positions[end_ref] + 1])
        decision_id = f"M7_sol-Exod-{index:03d}"
        rows.append({
            "model_id": "M7_sol",
            "book": "Exod",
            "span": f"{start_ref}-{end_ref}",
            "chunk_index_in_book": index,
            "working_title": title,
            "literature_type_guess": form,
            "boundary_evidence_refs": [
                f"direct_read:eng-web:{start_ref}-{end_ref}",
                f"book_strategy:Exod:{form}",
                "source_metadata:evidence_only",
            ],
            "strong_or_hebrew_tags_used": ["review_pending", "evidence_only", "not_boundary_authority"],
            "wj_or_red_letter_considered": False,
            "frontier_flag_considered": confidence in {"low", "medium_low"},
            "confidence": confidence,
            "decision_id": decision_id,
            "boundary_rationale": title,
            "review_revision": 0,
            "review_status": "frozen_pending_blind_review",
            "non_authorizing": True,
        })
    if covered != refs:
        missing = [ref for ref in refs if ref not in set(covered)]
        duplicates = sorted({ref for ref in covered if covered.count(ref) > 1})
        raise SystemExit(f"coverage mismatch expected={len(refs)} covered={len(covered)} missing={missing[:8]} duplicates={duplicates[:8]}")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"wrote {len(rows)} Exodus chunks with exact {len(refs)}/{len(refs)} ordered verse coverage")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
