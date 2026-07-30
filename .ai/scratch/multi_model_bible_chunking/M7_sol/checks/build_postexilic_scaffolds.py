#!/usr/bin/env python3
"""Build independent, candidate-only chapter-frame scaffolds for the post-exilic books.

These are exact-coverage placeholders, deliberately low confidence.  They are not
derived from another model's map and remain blocked pending the four-lane B01 mesh.
"""
from __future__ import annotations

import json
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
MODEL = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol"
PASSAGES = ROOT / "data" / "canonical" / "scripture" / "passages" / "passages.jsonl"

BOOKS = {
    "1Chr": {
        1: ("Adam-to-Israel genealogy", "genealogy_register"), 2: ("Judah genealogy and clans", "genealogy_register"),
        3: ("Davidic genealogy", "genealogy_register"), 4: ("Judah and Simeon clans", "genealogy_register"),
        5: ("Transjordan tribes and exile notice", "genealogy_and_exile_register"), 6: ("Levitical genealogy and service lines", "genealogy_register"),
        7: ("Northern tribal genealogies", "genealogy_register"), 8: ("Benjamin genealogy", "genealogy_register"),
        9: ("Post-exilic Jerusalem registries", "genealogy_and_registry"), 10: ("Saul's death", "royal_death_narrative"),
        11: ("David established at Jerusalem and mighty men", "royal_accession_and_list"), 12: ("Warriors join David", "military_joining_register"),
        13: ("Ark transport attempt", "cultic_narrative"), 14: ("David's house and victories", "royal_narrative"),
        15: ("Ark brought up with ordered Levites", "cultic_procession_narrative"), 16: ("Ark service and thanksgiving song", "liturgy_and_song"),
        17: ("Davidic oracle and prayer", "royal_oracle_and_prayer"), 18: ("David's victories and administration", "war_and_administration"),
        19: ("Ammonite-Aramean war", "war_narrative"), 20: ("Rabbah and Philistine campaigns", "war_narrative"),
        21: ("Census, judgment, and altar site", "judgment_and_temple_site_narrative"), 22: ("Temple preparations and charge", "temple_preparation_speech"),
        23: ("Levite organization", "cultic_register"), 24: ("Priestly divisions", "cultic_register"),
        25: ("Singers' divisions", "cultic_register"), 26: ("Gatekeepers and treasurers", "cultic_register"),
        27: ("Military and provincial administration", "administrative_register"), 28: ("David's assembly and temple charge", "royal_speech"),
        29: ("Offerings, prayer, accession, and David's death notice", "assembly_prayer_and_succession"),
    },
    "2Chr": {
        1: ("Solomon's accession and wisdom request", "royal_narrative_and_prayer"), 2: ("Temple workforce and materials", "temple_preparation"),
        3: ("Temple construction", "temple_construction"), 4: ("Temple furnishings", "temple_construction"),
        5: ("Ark installation and glory", "temple_dedication_narrative"), 6: ("Solomon's dedication prayer", "royal_prayer"),
        7: ("Fire, dedication, and divine response", "temple_dedication_narrative"), 8: ("Solomon's works and administration", "royal_administration"),
        9: ("Queen of Sheba, wealth, and Solomon's death", "royal_report_and_closure"), 10: ("Rehoboam and divided kingdom", "succession_and_division"),
        11: ("Rehoboam fortifies Judah", "royal_narrative"), 12: ("Shishak invasion and repentance", "judgment_and_reversal_narrative"),
        13: ("Abijah's speech and war", "royal_speech_and_war"), 14: ("Asa's reforms and victory", "royal_narrative"),
        15: ("Asa's covenant assembly", "royal_reform_speech"), 16: ("Asa's alliance and illness", "royal_narrative"),
        17: ("Jehoshaphat's teaching and strength", "royal_administration"), 18: ("Jehoshaphat and Ahab at Ramoth", "war_council_narrative"),
        19: ("Jehoshaphat's judicial reforms", "royal_reform"), 20: ("Moab-Ammon threat and deliverance", "war_and_liturgy_narrative"),
        21: ("Jehoram's reign and judgment", "royal_narrative"), 22: ("Ahaziah and Athaliah", "succession_narrative"),
        23: ("Jehoiada's coup and Joash's enthronement", "coup_and_cultic_narrative"), 24: ("Joash repairs temple and falls", "royal_narrative"),
        25: ("Amaziah's reign", "royal_narrative"), 26: ("Uzziah's reign and temple trespass", "royal_narrative"),
        27: ("Jotham's reign", "royal_narrative"), 28: ("Ahaz's reign and crisis", "royal_narrative"),
        29: ("Hezekiah cleanses and reopens temple", "cultic_reform_narrative"), 30: ("Hezekiah's Passover invitation", "festival_narrative"),
        31: ("Hezekiah's cultic provisioning", "cultic_administration"), 32: ("Sennacherib, prayer, and Hezekiah's closure", "war_and_closure_narrative"),
        33: ("Manasseh and Amon", "royal_narrative"), 34: ("Josiah's reform and law-book discovery", "cultic_reform_narrative"),
        35: ("Josiah's Passover and death", "festival_and_death_narrative"), 36: ("Final kings, exile, and Cyrus decree", "royal_closure_and_return_edict"),
    },
    "Ezra": {
        1: ("Cyrus decree and return vessels", "return_edict"), 2: ("Returnee register", "genealogy_and_return_register"),
        3: ("Altar, foundation, and mixed response", "restoration_narrative"), 4: ("Opposition and halted building", "opposition_correspondence"),
        5: ("Prophetic restart and inquiry", "restoration_narrative"), 6: ("Darius decree and temple completion", "royal_edict_and_completion"),
        7: ("Ezra's commission and travel", "commission_and_travel"), 8: ("Ezra's return party and safeguards", "return_register_and_travel"),
        9: ("Ezra's communal report and prayer", "confession_prayer"), 10: ("Assembly, proposal, and separation register", "assembly_and_register"),
    },
    "Neh": {
        1: ("Nehemiah's report and prayer", "commission_prayer"), 2: ("Royal permission and wall inspection", "commission_and_inspection"),
        3: ("Wall repairers' register", "construction_register"), 4: ("Opposition and guarded building", "construction_conflict_narrative"),
        5: ("Economic grievance and reform", "social_reform_narrative"), 6: ("Plots, completion, and intimidation", "construction_conflict_narrative"),
        7: ("Gate orders and returnee register", "administration_and_register"), 8: ("Public reading and festival", "public_reading_and_festival"),
        9: ("Corporate confession prayer", "confession_prayer"), 10: ("Covenant signers and obligations", "covenant_register"),
        11: ("Residents of Jerusalem and towns", "population_register"), 12: ("Priests, wall dedication, and temple provisions", "cultic_register_and_dedication"),
        13: ("Final reforms and memoir notices", "reform_memoir_closure"),
    },
    "Esth": {
        1: ("Vashti's refusal and royal decree", "court_narrative"), 2: ("Esther's elevation and Mordecai's discovery", "court_narrative"),
        3: ("Haman's plot and edict", "court_conflict_narrative"), 4: ("Mordecai's summons and Esther's resolve", "crisis_dialogue"),
        5: ("Esther's banquets and Haman's plan", "court_narrative"), 6: ("Royal reversal and Haman's humiliation", "reversal_narrative"),
        7: ("Esther's accusation and Haman's death", "court_judgment_narrative"), 8: ("Counter-edict and Jewish deliverance preparation", "royal_edict_narrative"),
        9: ("Deliverance, Purim, and memorial decree", "battle_and_festival_closure"), 10: ("Mordecai's greatness notice", "royal_closure_notice"),
    },
}


# Independent literary-unit hypotheses. Conservative endpoints may cross chapters
# when a register, speech, scene, or closure continues; B01 must challenge each.
UNIT_SPANS = {
    "1Chr": "1.1-1.41|1.42-2.23|2.24-2.55|3.1-4.9|4.10-4.43|5.1-6.14|6.15-6.48|6.49-6.81|7.1-7.40|8.1-8.40|9.1-9.33|9.34-11.16|11.17-11.47|12.1-12.40|13.1-14.17|15.1-15.29|16.1-16.42|16.43-17.27|18.1-19.19|20.1-21.30|22.1-23.22|23.23-24.31|25.1-25.31|26.1-26.32|27.1-27.34|28.1-29.21|29.22-29.30".split("|"),
    "2Chr": "1.1-2.18|3.1-4.22|5.1-6.26|6.27-7.22|8.1-9.20|9.21-10.19|11.1-12.16|13.1-14.15|15.1-16.14|17.1-18.23|18.24-20.19|20.20-21.20|22.1-23.21|24.1-25.15|25.16-26.23|27.1-28.27|29.1-29.36|30.1-31.9|31.10-32.30|32.31-33.25|34.1-34.33|35.1-36.15|36.16-36.23".split("|"),
    "Ezra": "1.1-2.1|2.2-2.41|2.42-2.70|3.1-4.24|5.1-6.22|7.1-7.28|8.1-8.36|9.1-10.27|10.28-10.44".split("|"),
    "Neh": "1.1-2.20|3.1-3.32|4.1-5.19|6.1-7.23|7.24-7.64|7.65-9.14|9.15-9.38|10.1-10.39|11.1-11.36|12.1-12.42|12.43-13.31".split("|"),
    "Esth": "1.1-2.17|2.18-4.17|5.1-6.14|7.1-9.14|9.15-10.3".split("|"),
}


def main() -> int:
    all_rows = [json.loads(line) for line in PASSAGES.open(encoding="utf-8") if line.strip()]
    for book, labels in BOOKS.items():
        chapters: OrderedDict[int, list[dict]] = OrderedDict()
        for row in all_rows:
            if row.get("book") == book:
                chapters.setdefault(int(row["chapter"]), []).append(row)
        if set(chapters) != set(labels):
            raise SystemExit(f"chapter mismatch {book}: {sorted(chapters)} vs {sorted(labels)}")
        refs = [r["osis_ref"] for rows in chapters.values() for r in rows]
        positions = {ref: i for i, ref in enumerate(refs)}
        spans = []
        for raw in UNIT_SPANS[book]:
            start, end = raw.split("-")
            start_ref, end_ref = f"{book}.{start}", f"{book}.{end}"
            if start_ref not in positions or end_ref not in positions:
                raise SystemExit(f"unknown endpoint {start_ref}-{end_ref}")
            spans.append((start_ref, end_ref))
        covered = [ref for start, end in spans for ref in refs[positions[start] : positions[end] + 1]]
        if covered != refs:
            raise SystemExit(f"coverage mismatch {book}: {len(covered)} vs {len(refs)}")
        out = MODEL / "book_chunks" / book / "chunks.jsonl"
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", encoding="utf-8", newline="\n") as handle:
            for index, (start, end) in enumerate(spans, 1):
                first_chapter = int(start.split(".")[1])
                title, form = labels[first_chapter]
                handle.write(json.dumps({
                    "model_id": "M7_sol", "book": book,
                    "span": f"{start}-{end}", "chunk_index_in_book": index,
                    "working_title": f"{title} (literary-unit hypothesis; draft)",
                    "literature_type_guess": form,
                    "boundary_evidence_refs": ["canonical_passage_identity_only", "whole_bible_role_source_matrix.v1", "chapter_frame_scaffold"],
                    "strong_or_hebrew_tags_used": ["evidence_only", "chapter_scaffold_not_boundary_authority"],
                    "wj_or_red_letter_considered": False, "frontier_flag_considered": True,
                    "confidence": "low", "decision_id": f"M7_sol-{book}-{index:03d}",
                    "boundary_rationale": "Temporary exact-coverage literary-unit hypothesis; endpoint follows a provisional scene, speech, register, song, correspondence, or closure transition and remains reviewable.",
                    "review_revision": 0, "review_status": "candidate_scaffold_pending_b01_mesh",
                    "review_holds": ["literary_form_review", "original_language_review", "canonical_premortem_review", "ancient_context_gap", "boss_authorization"],
                    "non_authorizing": True,
                }, ensure_ascii=False, separators=(",", ":")) + "\n")
        # Independent strategy is intentionally brief and explicit about its limits.
        strategy = MODEL / "book_strategy" / f"{book}.md"
        strategy.write_text(
            f"# {book} candidate strategy\n\n"
            "This is an independent, low-confidence literary-unit hypothesis for exact canonical passage coverage. "
            "Boundaries follow provisional scene, speech, register, song, correspondence, or closure transitions; no "
            "chapter or editorial marker is treated as literary authority. B01 role review must split or merge "
            "frames on observed scene, speech, register, song, prayer, correspondence, or closure changes.\n\n"
            "- candidate_only: true\n- non_authorizing: true\n"
            f"- provisional_units: {len(spans)}\n- source_chapter_count: {len(chapters)}\n- ancient_context: explicit corpus gap until qualified\n"
            "- required_lanes: original_language_translation, literary_form, canonical_relations_premortem, ancient_context_gap\n"
            "- no_theology_decisions: true\n- sibling_model_paths_read: false\n",
            encoding="utf-8",
        )
        print(f"{book}: wrote {len(spans)} exact literary units covering {len(refs)} passages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
