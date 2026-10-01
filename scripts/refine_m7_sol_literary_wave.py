#!/usr/bin/env python3
"""Refine Sol's candidate-only literary metadata for the wisdom/prophetic wave.

This deliberately leaves every span and chapter/psalm coverage boundary unchanged.
The chapter-sized scaffold is the conservative outer boundary; this pass records
form signals, likely internal seams, and translation/cross-reference holds for the
typed B01 reviewers to challenge.  It never promotes a chunk or makes a theological
claim.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol" / "book_chunks"
BOOKS = ("Job", "Ps", "Prov", "Eccl", "Song", "Isa", "Jer", "Lam")


def chapter(span: str) -> int:
    return int(span.split(".", 2)[1].split("-", 1)[0])


def classify(book: str, ch: int) -> tuple[str, str, list[str], list[str]]:
    if book == "Job":
        if ch <= 2:
            return "prose_prologue", "Narrative frame; preserve as outer frame around the poetic disputation.", ["prose_to_poetry_seam_after_2"], ["Job 1-2 prose/poetry boundary; Hebrew genre labels are not asserted"]
        if ch == 3:
            return "individual_lament_poem", "Job's opening lament; poetic monologue with repeated wish/curse motifs.", ["lament_turns_in_3"], ["Job 3; lexical force of curse/wish verbs requires Hebrew review"]
        if 4 <= ch <= 27:
            return "dialogue_speech_poetry", "Friends/Job speech cycle; chapter boundary retained while speech turns may cross chapters.", ["speech_turns_and_refrains", "cycle_seams"], ["Job 4-27; disputed lexemes and discourse markers require Hebrew review"]
        if ch == 28:
            return "wisdom_poem", "Self-contained wisdom poem with marked rhetorical closure.", ["wisdom_poem_frame"], ["Job 28; personification and rare terms require Hebrew/ancient-version review"]
        if 29 <= ch <= 31:
            return "final_lament_oath", "Job's closing lament and oath; chapter-sized scaffold preserves possible internal oath seams.", ["lament_to_oath_transition"], ["Job 29-31; oath formula and legal vocabulary require Hebrew review"]
        if 32 <= ch <= 37:
            return "mediating_speech_poetry", "Elihu speech sequence; preserve speaker change and possible editorial seam.", ["speaker_change_32", "speech_cycle_closure_37"], ["Job 32-37; speaker attribution and rare vocabulary require review"]
        if ch <= 40:
            return "divine_speech_poetry", "Storm/theophany speech sequence; do not collapse question-answer turns.", ["speech_turns_38_40"], ["Job 38-40; animal terms and rhetorical questions require Hebrew review"]
        return "response_and_prose_epilogue", "Job's response and prose restoration frame; preserve genre shift.", ["poetry_to_prose_seam"], ["Job 41-42; epilogue relationship to frame remains a structural hold"]
    if book == "Ps":
        groups = ((2, "royal_wisdom", "Wisdom/royal opening; superscription and parallelism require Hebrew review"), (7, "individual_lament", "Individual lament; address, petition, and confidence turns"), (14, "mixed_lament_hymn", "Lament/hymnic confidence mix; refrain and turn seams"), (18, "royal_thanksgiving", "Royal thanksgiving/hymn; long-form parallelism"), (24, "hymn_liturgy", "Processional/liturgical hymn signals"), (32, "penitential_wisdom", "Penitential/wisdom instruction signals"), (41, "individual_lament", "Individual lament/thanksgiving cycle"), (49, "wisdom_instruction", "Wisdom poem/instruction"), (51, "penitential_lament", "Penitential lament; lexical and superscription holds"), (72, "royal_prayer", "Royal prayer/epilogue of first two books"), (89, "lament_and_covenant", "Communal lament with covenant rhetoric"), (100, "hymn", "Hymnic praise and enthronement signals"), (106, "historical_liturgy", "Historical/communal confession"), (110, "royal_oracle", "Royal/oracular form; speaker attribution hold"), (119, "torah_acrostic", "Alphabetic acrostic wisdom; stanza letters are structural evidence"), (134, "songs_of_ascents", "Pilgrimage/ascents collection; collection seam"), (145, "acrostic_hymn", "Alphabetic hymn"), (150, "doxological_hymn", "Closing doxological hymn"))
        for end, form, note in groups:
            if ch <= end:
                return form, note, ["superscription_boundary", "parallelism_or_refrain"], [f"Ps {ch}; Hebrew poetic parallelism and superscription semantics require review"]
        return "hymn_or_lament", "Psalm-level outer boundary retained; internal stanzas are candidate seams only.", ["parallelism_or_refrain"], [f"Ps {ch}; Hebrew poetic structure requires review"]
    if book == "Prov":
        if ch <= 9:
            return "instructional_wisdom_discourse", "Extended parental instruction with embedded poems and personified voices.", ["instructional_unit_seams", "embedded_poem"], [f"Prov {ch}; Hebrew parallelism and personification require review"]
        if ch <= 22:
            return "aphoristic_sayings_collection", "Short sayings collection; preserve individual aphorisms as internal candidates.", ["saying_boundaries", "collection_seam"], [f"Prov {ch}; terse Hebrew syntax and parallelism require review"]
        if ch <= 24:
            return "sayings_of_the_wise", "Named sayings-of-wise collection; chapter outer boundary is conservative.", ["collection_heading", "saying_boundaries"], [f"Prov {ch}; heading scope and textual variants require review"]
        if ch <= 29:
            return "hezekiah_collection", "Collected sayings with editorial heading; preserve collection seam.", ["editorial_heading", "saying_boundaries"], [f"Prov {ch}; Hebrew proverb compression requires review"]
        if ch == 30:
            return "agur_speech", "Agur sayings/discourse with numerical sayings and confession-like units.", ["speaker_heading", "numerical_saying"], ["Prov 30; rare terms and numerical-form syntax require Hebrew review"]
        return "lemuel_and_acrostic_instruction", "Lemuel heading followed by acrostic wisdom poem; retain internal seam.", ["speaker_heading", "acrostic_poem"], ["Prov 31; acrostic and rare vocabulary require Hebrew review"]
    if book == "Eccl":
        if ch <= 2:
            return "frame_and_reflection", "Qoheleth frame/quest reflections; preserve repeated refrain signals.", ["frame_voice", "refrain"], [f"Eccl {ch}; Hebrew voice and refrain terms require review"]
        if ch == 3:
            return "time_poem_and_reflection", "Time poem embedded within reflective discourse; internal poem seam is held.", ["embedded_poem", "poem_to_prose_seam"], ["Eccl 3; lexical pairings and poem boundaries require Hebrew review"]
        if ch <= 6:
            return "observational_wisdom_discourse", "Observations and rhetorical questions; chapter boundary is outer scaffold.", ["refrain", "rhetorical_question"], [f"Eccl {ch}; ambiguous Hebrew particles require review"]
        if ch <= 11:
            return "instructional_reflection", "Wisdom instructions/interleaved observations; preserve tonal shifts.", ["instructional_turn", "refrain"], [f"Eccl {ch}; translation ambiguity and discourse shifts require review"]
        return "closing_poem_and_epilogue", "Closing aging/death poem with editorial epilogue; genre seam is explicit.", ["poem_to_epilogue_seam", "frame_closure"], ["Eccl 12; rare metaphors and epilogue voice require review"]
    if book == "Song":
        return "lyric_dialogue_and_chorus", "Song lyric/dialogue outer unit; refrain, speaker, and scene shifts are candidate internal seams.", ["speaker_turn", "refrain", "scene_shift"], [f"Song {ch}; Hebrew erotic imagery, speaker attribution, and refrain wording require review"]
    if book == "Isa":
        if ch <= 12:
            return "judgment_and_hope_oracle_cycle", "Prophetic oracle cycle with alternating accusation, sign, and hope units.", ["oracle_heading", "judgment_to_hope_turn"], [f"Isa {ch}; Hebrew wordplay and oracle headings require review"]
        if ch <= 27:
            return "nations_and_cosmic_oracle_cycle", "Oracle collection with woe/song/vision seams; chapter outer boundary retained.", ["oracle_heading", "hymnic_insert"], [f"Isa {ch}; place names and rare poetic terms require review"]
        if ch <= 35:
            return "zion_and_return_oracle_cycle", "Woe/return/restoration oracle cycle; preserve alternating prose-like and poetic units.", ["woe_oracle", "return_song"], [f"Isa {ch}; Hebrew rhetorical markers and topographical terms require review"]
        if ch <= 39:
            return "royal_narrative_interlude", "Hezekiah narrative interlude; prose framing around prophetic material.", ["narrative_oracle_seam"], [f"Isa {ch}; parallel with 2 Kgs requires cross-reference review"]
        if ch <= 55:
            return "consolation_servant_poetry", "Consolation/servant song sequence; poem and speech seams are held, not interpreted.", ["servant_song", "consolation_refrain"], [f"Isa {ch}; Hebrew servant-song syntax and intertextual echoes require review"]
        return "restoration_and_disputation_oracles", "Post-consolation disputation/restoration oracle cycle.", ["oracle_heading", "disputation_turn"], [f"Isa {ch}; Hebrew legal/disputation terms and cross-references require review"]
    if book == "Jer":
        if ch == 1:
            return "call_narrative_and_oracle", "Call narrative with embedded visions; preserve prose/poetry seam.", ["call_narrative", "vision_oracle_seam"], ["Jer 1; Hebrew prophetic formulae require review"]
        if ch <= 25:
            return "covenant_lawsuit_oracle_cycle", "Accusation, sign-act, and warning oracle cycle; headings and speaker turns are held.", ["oracle_heading", "sign_act", "lament_insert"], [f"Jer {ch}; Hebrew legal terms and textual-order variants require review"]
        if ch <= 29:
            return "conflict_and_narrative_cycle", "Narratives of prophetic conflict with embedded oracle/letter units.", ["narrative_oracle_seam", "letter_unit"], [f"Jer {ch}; parallel traditions and chronology require cross-reference review"]
        if ch <= 33:
            return "consolation_oracle_cycle", "Consolation/hope oracle collection; preserve poem, sign-act, and prose seams.", ["consolation_refrain", "sign_act"], [f"Jer {ch}; Hebrew restoration vocabulary requires review"]
        if ch <= 45:
            return "fall_and_aftermath_narrative_cycle", "Fall/aftermath narratives with embedded prophetic speech.", ["narrative_oracle_seam", "lament_insert"], [f"Jer {ch}; chronology and parallel Kings material require review"]
        if ch <= 51:
            return "nations_oracle_collection", "Oracles against nations; heading, address, and closure seams are structural.", ["oracle_heading", "nation_address"], [f"Jer {ch}; place names and textual variants require review"]
        return "historical_epilogue", "Historical appendix/epilogue; preserve as separate prose frame.", ["epilogue_frame"], ["Jer 52; parallel 2 Kgs 24-25 requires cross-reference review"]
    if book == "Lam":
        if ch <= 4:
            return "alphabetic_lament", "Alphabetic city/communal lament; stanza letters and meter are structural evidence.", ["alphabetic_stanza", "lament_turn"], [f"Lam {ch}; Hebrew acrostic, meter, and rare terms require review"]
        return "non_acrostic_communal_prayer", "Closing communal prayer without the preceding acrostic constraint; retain contrast.", ["acrostic_to_nonacrostic_seam", "communal_petition"], ["Lam 5; Hebrew meter and syntax require review"]
    raise ValueError(book)


def main() -> None:
    for book in BOOKS:
        path = BASE / book / "chunks.jsonl"
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        for row in rows:
            ch = chapter(row["span"])
            form, rationale, seams, holds = classify(book, ch)
            row["literature_type_guess"] = form
            row["boundary_rationale"] = rationale
            row["candidate_internal_seams"] = seams
            row["translation_and_crossref_holds"] = holds
            row["review_status"] = "candidate_literary_refinement_pending_typed_b01_mesh"
            row["review_revision"] = int(row.get("review_revision", 0)) + 1
            row["non_authorizing"] = True
            refs = list(row.get("boundary_evidence_refs") or [])
            if "sol_literary_wave_refinement.v1" not in refs:
                refs.append("sol_literary_wave_refinement.v1")
            row["boundary_evidence_refs"] = refs
        path.write_text("".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows), encoding="utf-8")
    print(json.dumps({"books": list(BOOKS), "candidate_only": True, "spans_unchanged": True}, separators=(",", ":")))


if __name__ == "__main__":
    main()
