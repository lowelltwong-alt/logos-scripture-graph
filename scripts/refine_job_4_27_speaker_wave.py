#!/usr/bin/env python3
"""Refine Job 4-27 speaker/discourse metadata without changing spans."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks/Job/chunks.jsonl",
    ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/state/evidence/final/whole_bible_candidate_map.jsonl",
]
WAVE = "job_4_27_speaker_wave.v1"
REDTEAM = ".ai/scratch/multi_model_bible_chunking/M7_sol/reviews/Job/job_4_27_redteam_review.json"

# These are conservative voice hypotheses for the dialogue sequence. They are
# not claims about disputed Hebrew attribution and do not authorize boundaries.
DETAILS = {
    4: ("eliphaz_speech", "Eliphaz first speech: address, observation, and night-vision report", ["speaker_opening", "vision_report", "speech_closure"]),
    5: ("eliphaz_speech", "Eliphaz first speech: exhortation, proverb, and appeal", ["exhortation_turn", "wisdom_unit", "appeal_closure"]),
    6: ("job_response", "Job response: complaint, appeal, and friendship rebuke", ["response_opening", "complaint_unit", "address_to_friends"]),
    7: ("job_response", "Job response: mortal-condition lament and direct appeal", ["lament_continuation", "rhetorical_question", "appeal_closure"]),
    8: ("bildad_speech", "Bildad first speech: ancestral wisdom and conditional restoration", ["speaker_opening", "ancestral_proverb", "conditional_closure"]),
    9: ("job_response", "Job response: dispute over adjudication and divine hiddenness", ["legal_metaphor", "question_sequence", "response_closure"]),
    10: ("job_response", "Job response: complaint, creation imagery, and plea", ["complaint_continuation", "creation_image", "plea_closure"]),
    11: ("zophar_speech", "Zophar first speech: rebuke, hidden wisdom, and repentance appeal", ["speaker_opening", "wisdom_claim", "repentance_appeal"]),
    12: ("job_response", "Job response: irony, common wisdom, and divine sovereignty", ["ironic_reply", "common_wisdom_unit", "sovereignty_turn"]),
    13: ("job_response", "Job response: forensic complaint and demand for hearing", ["forensic_address", "false_speech_rebuke", "hearing_request"]),
    14: ("job_response", "Job response: frailty, hope question, and mortality lament", ["mortality_image", "hope_question", "lament_closure"]),
    15: ("eliphaz_speech", "Eliphaz second speech: rebuke and inherited-wisdom indictment", ["speaker_return", "rebuke", "wickedness_catalogue"]),
    16: ("job_response", "Job response: witness imagery, lament, and appeal", ["consoler_rebuke", "witness_image", "appeal_continuation"]),
    17: ("job_response", "Job response: burial/hope imagery and appeal for vindication", ["despair_unit", "hope_or_vindication_question", "closure"]),
    18: ("bildad_speech", "Bildad second speech: wicked-person fate catalogue", ["speaker_return", "fate_catalogue", "warning_closure"]),
    19: ("job_response", "Job response: abandonment, redeemer hope, and witness appeal", ["abandonment_catalogue", "hope_statement", "witness_appeal"]),
    20: ("zophar_speech", "Zophar second speech: transient wickedness and retribution catalogue", ["speaker_return", "transience_image", "retribution_closure"]),
    21: ("job_response", "Job response: counterexample to retribution and divine-distance questions", ["counterexample_catalogue", "retribution_question", "response_closure"]),
    22: ("eliphaz_speech", "Eliphaz third speech: accusation, counsel, and return appeal", ["speaker_return", "accusation_list", "return_exhortation"]),
    23: ("job_response", "Job response: search for adjudication and hidden presence", ["hearing_search", "presence_absence", "integrity_claim"]),
    24: ("job_response", "Job response: social injustice observations and delayed judgment", ["injustice_catalogue", "social_observation", "judgment_question"]),
    25: ("bildad_speech", "Bildad third speech: human frailty and divine dominion maxim", ["brief_speech_opening", "dominion_maxim", "closure"]),
    26: ("job_response", "Job response: divine power hymn and ironic extension", ["reply_opening", "cosmic_power_catalogue", "ironic_closure"]),
    27: ("job_response_attribution_hold", "Job speech and attribution hold: integrity oath, wickedness maxim, and disputed transition", ["oath_or_integrity_unit", "wickedness_maxim", "speaker_attribution_hold"]),
}


def refine(rows: list[dict]) -> int:
    changed = 0
    for row in rows:
        if row.get("book") != "Job":
            continue
        chapter = int(row["span"].split(".", 2)[1].split("-", 1)[0])
        if chapter not in DETAILS:
            continue
        form, title, seams = DETAILS[chapter]
        row["literature_type_guess"] = form
        row["working_title"] = title
        row["working_title_origin"] = WAVE
        row["working_title_is_boundary_authority"] = False
        row["boundary_rationale"] = "Outer chapter-sized candidate retained provisionally; speaker and discourse labels are hypotheses requiring qualified Hebrew review and do not decide a boundary."
        row["candidate_internal_seams"] = seams
        row["translation_difficulties"] = ["Hebrew ellipsis, vocatives, discourse particles, rare lexemes, and poetic parallelism may obscure speaker or speech closure"]
        row["original_language_translation_holds"] = ["OSHB/UXLC comparison and source-level speaker-attribution review required; English paragraphing is insufficient"]
        row["cross_reference_clusters"] = ["Job wisdom, lament, legal-metaphor, and retribution motifs are internal relation leads only"]
        row["cross_reference_holds"] = ["Do not use canonical parallels or later reception to settle speaker attribution or boundaries"]
        row["hard_passage_forecast"] = ["Speech-turn edges, disputed attribution in Job 27, and compact Hebrew poetic syntax require adversarial review"]
        row["red_team_questions"] = ["Does the proposed voice survive removal of English headings and chapter numbers?", "Could a translation paragraph or inherited speaker label strand a response or closure?"]
        row["red_team_premortem_holds"] = ["Never treat chapter edge or conventional speaker label as boundary authority; preserve Job 27 attribution dispute as an appealable hold"]
        row["review_revision"] = int(row.get("review_revision", 0)) + 1
        refs = list(row.get("boundary_evidence_refs") or [])
        if WAVE not in refs:
            refs.append(WAVE)
        if REDTEAM not in refs:
            refs.append(REDTEAM)
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
    print(json.dumps({"book": "Job", "wave": WAVE, "rows_changed": reports, "spans_unchanged": True, "candidate_only": True, "non_authorizing": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
