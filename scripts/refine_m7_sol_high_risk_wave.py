#!/usr/bin/env python3
"""Add conservative seam metadata for Job, Song, and Revelation.

Outer spans remain unchanged.  This wave records candidate internal seams and
language/canonical/red-team holds only; it never promotes or splits a chunk.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks"


def chapter(span: str) -> int:
    return int(span.split(".", 2)[1].split("-", 1)[0])


def metadata(book: str, ch: int) -> tuple[str, str, list[str], list[str], list[str]]:
    if book == "Job":
        if ch <= 2:
            return ("prose_frame", "Prose opening frame around the poetic dispute", ["prose_to_poetry", "scene_setup"], ["Hebrew frame formulae and narrative tense"], ["Do not infer theology from frame/poetry contrast"])
        if ch == 3:
            return ("lament_monologue", "Opening lament and curse-wish monologue", ["lament_opening", "wish_formulae"], ["Hebrew volitives and rhetorical questions"], ["Test whether translation paragraphing creates false subunits"])
        if 4 <= ch <= 27:
            return ("dialogue_speech_cycle", "Speaker-addressed poetic dispute cycle", ["speaker_turn", "response_closure", "cycle_transition"], ["ellipsis, vocatives, and quoted speech in Hebrew poetry"], ["Never use chapter edge alone as a speaker boundary"])
        if ch == 28:
            return ("wisdom_insert", "Self-contained wisdom poem within the dispute", ["wisdom_poem_frame", "rhetorical_closure"], ["rare lexemes and personification"], ["Test whether the poem is an inserted unit rather than a chapter artifact"])
        if 29 <= ch <= 31:
            return ("closing_lament_oath", "Closing lament with legal oath and appeal", ["lament_to_oath", "oath_closure"], ["legal vocabulary and oath formulae"], ["Preserve lament/oath functions if later split"])
        if 32 <= ch <= 37:
            return ("mediator_speech_cycle", "Elihu speech sequence and speaker transition", ["speaker_introduction", "speech_turn", "cycle_closure"], ["speaker attribution and rare Hebrew terms"], ["Test whether the speech sequence is editorially framed"])
        if 38 <= ch <= 41:
            return ("divine_speech_cycle", "Storm and divine-question speech cycle", ["speech_turn", "animal_catalogue", "answer_transition"], ["animal terms and rhetorical interrogatives"], ["Do not impose a linear vision model on poetic questions"])
        return ("prose_epilogue", "Response and prose closing frame", ["poetry_to_prose", "frame_closure"], ["Hebrew narrative closure and lexical links to prologue"], ["Test frame inclusio without theological adjudication"])
    if book == "Song":
        return ("lyric_dialogue", "Lyric dialogue with chorus/refrain and scene movement", ["speaker_turn", "refrain", "scene_shift", "adjuration"], ["Hebrew speaker attribution, imagery, and refrain wording"], ["Remove English headings and test whether the seam still has textual signals"])
    if book == "Rev":
        if ch == 1:
            return ("epistolary_vision_prologue", "Epistolary address and introductory vision", ["salutation", "vision_onset", "commission"], ["Koine aspect, participles, and title formulae"], ["Do not merge epistolary address with vision solely by chapter number"])
        if ch <= 3:
            return ("seven_letters", "Seven church messages with repeated letter frame", ["letter_frame", "refrain", "promise_closure"], ["Koine imperatives and repeated formulae"], ["Test repeated frame against each local message rather than treating all as one speech"])
        if ch <= 5:
            return ("throne_vision", "Throne-room vision and scroll introduction", ["scene_shift", "hymnic_insert", "scroll_introduction"], ["vision verbs and worship vocabulary"], ["Test audition/vision transitions without assuming chronology"])
        if ch <= 8:
            return ("seal_and_trumpet_cycle", "Seal cycle with transition into trumpet material", ["seal_sequence", "interlude", "trumpet_onset"], ["Greek aspect and connective particles"], ["Red-team recapitulation versus strict sequence assumptions"])
        if ch <= 11:
            return ("trumpet_witness_cycle", "Trumpet judgments, interludes, and witness material", ["trumpet_sequence", "measuring_scene", "witness_cycle", "hymnic_closure"], ["symbolic nouns and OT allusion density"], ["Do not let intertextual echoes alone create boundaries"])
        if ch <= 14:
            return ("dragon_beast_lamb_cycle", "Dragon, beast, Lamb, and harvest visions", ["heavenly_sign", "beast_scene", "lamb_scene", "harvest_transition"], ["Greek participial chains and symbolic referents"], ["Test local vision markers rather than doctrinal system-building"])
        if ch <= 16:
            return ("bowl_cycle", "Temple/preparation and bowl judgment cycle", ["temple_scene", "bowl_sequence", "interlude", "completion_formula"], ["imperatives, genitive constructions, and formula repetition"], ["Check whether bowls recapitulate or follow seals/trumpets; neither decides chunking"])
        if ch <= 19:
            return ("babylon_judgment_cycle", "Babylon oracle, lament, judgment, and victory hymns", ["oracle_heading", "lament_insert", "judgment_scene", "hymnic_closure"], ["personification and quotation/allusion boundaries"], ["Do not import later historical identifications into structural seams"])
        if ch == 20:
            return ("final_judgment_vision", "Binding, reign/judgment, and final judgment vision", ["binding_scene", "reign_interval", "judgment_throne"], ["Greek temporal clauses and ambiguous referents"], ["Test sequence claims independently of millennium theology"])
        return ("new_creation_epilogue", "New Jerusalem vision and book epilogue", ["city_vision", "river/tree_scene", "epilogue_exhortation", "closing_dialogue"], ["Koine imperatives, deixis, and epistolary closure"], ["Keep vision description distinct from final exhortation where local markers support it"])
    raise ValueError(book)


def main() -> int:
    changed = 0
    for book in ("Job", "Song", "Rev"):
        path = BASE / book / "chunks.jsonl"
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        for row in rows:
            form, rationale, seams, lang, redteam = metadata(book, chapter(row["span"]))
            row["literature_type_guess"] = form
            row["boundary_rationale"] = rationale
            row["candidate_internal_seams"] = seams
            row["original_language_translation_holds"] = lang
            row["red_team_premortem_holds"] = redteam
            row["working_title_is_boundary_authority"] = False
            row["review_status"] = "candidate_role_mesh_complete_boss_receipt_only"
            row["candidate_only"] = True
            row["non_authorizing"] = True
            row["review_revision"] = int(row.get("review_revision", 0)) + 1
            refs = list(row.get("boundary_evidence_refs") or [])
            if "sol_high_risk_wave_refinement.v1" not in refs:
                refs.append("sol_high_risk_wave_refinement.v1")
            row["boundary_evidence_refs"] = refs
            holds = list(row.get("review_holds") or [])
            for hold in ("external_provider_review", "human_appeal_review", "QF-CORRELATED-SUBSTRATE"):
                if hold not in holds:
                    holds.append(hold)
            row["review_holds"] = holds
            changed += 1
        path.write_text("".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows), encoding="utf-8", newline="\n")
    print(json.dumps({"books": ["Job", "Song", "Rev"], "rows_changed": changed, "spans_unchanged": True, "candidate_only": True, "non_authorizing": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
