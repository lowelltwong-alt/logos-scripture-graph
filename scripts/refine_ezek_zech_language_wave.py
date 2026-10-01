#!/usr/bin/env python3
"""Refine conservative literary metadata for Ezekiel 40–48 and Zechariah 9–14."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks"


def chapter(span: str) -> int:
    return int(span.split(".", 2)[1].split("-", 1)[0])


def data(book: str, ch: int) -> tuple[str, str, list[str], list[str], list[str]]:
    if book == "Ezek":
        if ch == 40:
            return ("temple_vision_frame", "Vision frame and guide-led measurement begins", ["vision_frame", "guide_introduction", "measurement_onset"], ["Hebrew measurement vocabulary and directional terms"], ["Do not treat architectural diagram conventions as automatic boundaries"])
        if ch <= 42:
            return ("temple_measurement_sequence", "Outer courts, gates, chambers, and measured temple complex", ["measurement_block", "guide_speech", "spatial_transition"], ["technical Hebrew nouns and textual witness variants"], ["Test each spatial transition against local guide speech and formulae"])
        if ch <= 46:
            return ("temple_ritual_instruction", "Inner sanctuary, altar, priestly access, and offering regulations", ["sanctuary_transition", "priestly_instruction", "ritual_schedule"], ["cultic/legal Hebrew and number expressions"], ["Do not let later ritual interpretation decide structural seams"])
        return ("land_allocation_and_closure", "Land allocation, river/territory arrangement, and naming closure", ["allocation_block", "river_vision", "boundary_formula", "city_name_closure"], ["topographic terms, measurements, and repeated closure formulae"], ["Test whether allocation and city-name closure form distinct movements without importing a scheme"])
    if book == "Zech":
        if ch <= 10:
            return ("oracle_cycle", "Oracle and burden sequence with address and response turns", ["oracle_heading", "address_shift", "poetic_insert", "closure_formula"], ["Hebrew wordplay, burden formulae, and speaker deixis"], ["Do not use later fulfillment frameworks as boundary evidence"])
        if ch == 11:
            return ("symbolic_shepherd_act", "Symbolic shepherd action and contested response", ["sign_act", "speech_turn", "symbolic_closure"], ["metaphorical Hebrew and disputed lexical items"], ["Test sign-act frame against adjacent oracle material"])
        if ch == 12:
            return ("oracle_of_burden", "Jerusalem oracle with lament and response movements", ["burden_heading", "lament_insert", "response_oracle"], ["collective/person reference and poetic parallelism"], ["Test addressee changes without theological identification"])
        if ch == 13:
            return ("purification_and_shepherd_oracle", "Cleansing, removal, and shepherd-related oracle sequence", ["purification_formula", "shepherd_saying", "judgment_turn"], ["Hebrew idiom and quotation/allusion pressure"], ["Do not merge distinct oracle speakers by thematic similarity"])
        return ("eschatological_oracle_cycle", "Day-of-YHWH, living waters, and final oracle movements", ["day_formula", "battle_scene", "living_water_insert", "closing_formula"], ["topographic and temporal Hebrew, dense intertextual echoes"], ["Test each vision/oracle transition locally; avoid chronological system-building"])
    raise ValueError(book)


def main() -> int:
    changed = 0
    for book in ("Ezek", "Zech"):
        path = BASE / book / "chunks.jsonl"
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        for row in rows:
            ch = chapter(row["span"])
            if book == "Ezek" and not 40 <= ch <= 48:
                continue
            if book == "Zech" and not 9 <= ch <= 14:
                continue
            form, rationale, seams, lang, red = data(book, ch)
            row["literature_type_guess"] = form
            row["working_title"] = rationale
            row["working_title_origin"] = "ezek_zech_language_wave_v1"
            row["working_title_is_boundary_authority"] = False
            row["boundary_rationale"] = "Chapter-sized outer candidate retained provisionally; local vision/oracle and technical-language seams require independent review."
            row["candidate_internal_seams"] = seams
            row["original_language_translation_holds"] = lang
            row["red_team_premortem_holds"] = red
            row["review_revision"] = int(row.get("review_revision", 0)) + 1
            row["candidate_only"] = True
            row["non_authorizing"] = True
            refs = list(row.get("boundary_evidence_refs") or [])
            if "ezek_zech_language_wave.v1" not in refs:
                refs.append("ezek_zech_language_wave.v1")
            row["boundary_evidence_refs"] = refs
            changed += 1
        path.write_text("".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows), encoding="utf-8", newline="\n")
    print(json.dumps({"books": ["Ezek", "Zech"], "rows_changed": changed, "spans_unchanged": True, "candidate_only": True, "non_authorizing": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
