#!/usr/bin/env python3
"""Refine Daniel 2–7 Aramaic/court/vision seam metadata."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks/Dan/chunks.jsonl"
DETAILS = {
    2: ("dream_report_and_court_tale", "Court crisis, dream report, interpretation, and royal response", ["narrative_frame", "Aramaic_language_onset", "dream_report", "interpretation", "response_closure"]),
    3: ("court_tale_with_hymnic_insert", "Image dedication, refusal, furnace narrative, and deliverance hymn/response", ["decree", "refusal_dialogue", "hymnic_insert", "narrative_closure"]),
    4: ("royal_dream_testimony", "Royal proclamation, dream, interpretation, humiliation, and restoration", ["proclamation_frame", "dream_report", "interpretation", "first_person_testimony", "restoration_closure"]),
    5: ("banquet_sign_and_judgment_tale", "Banquet, writing sign, interpretation, judgment, and succession", ["banquet_frame", "sign_event", "interpretation", "judgment_closure"]),
    6: ("court_plot_and_lions_tale", "Administrative plot, decree, lions episode, and royal proclamation", ["administrative_frame", "decree", "night_intervention", "proclamation_closure"]),
    7: ("aramaic_apocalyptic_vision", "Night vision of beasts, heavenly court, interpretation, and closure", ["vision_frame", "beast_sequence", "heavenly_court", "interpretation", "vision_closure"]),
}


def main() -> int:
    rows = [json.loads(x) for x in PATH.read_text(encoding="utf-8").splitlines() if x.strip()]
    changed = 0
    for row in rows:
        ch = int(row["span"].split(".", 2)[1].split("-", 1)[0])
        if ch not in DETAILS:
            continue
        form, title, seams = DETAILS[ch]
        row["literature_type_guess"] = form
        row["working_title"] = title
        row["working_title_origin"] = "dan_2_7_aramaic_wave_v1"
        row["working_title_is_boundary_authority"] = False
        row["boundary_rationale"] = "Chapter-sized outer candidate retained provisionally; Aramaic/Hebrew language shifts, court-tale frames, dream reports, hymnic inserts, and vision interpretations require independent review."
        row["candidate_internal_seams"] = seams
        row["original_language_translation_holds"] = ["Aramaic/Hebrew language boundary, court titles, dream/vision vocabulary, and textual variants require qualified review"]
        row["cross_reference_holds"] = ["Daniel/prophetic/apocalyptic parallels are leads only; symbol correspondence cannot authorize a seam"]
        row["red_team_premortem_holds"] = ["test whether language change, dream report, interpretation, or hymn is a local seam rather than an automatic chapter boundary"]
        row["review_revision"] = int(row.get("review_revision", 0)) + 1
        row["candidate_only"] = True
        row["non_authorizing"] = True
        refs = list(row.get("boundary_evidence_refs") or [])
        if "dan_2_7_aramaic_wave.v1" not in refs:
            refs.append("dan_2_7_aramaic_wave.v1")
        row["boundary_evidence_refs"] = refs
        changed += 1
    PATH.write_text("".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in rows), encoding="utf-8", newline="\n")
    print(json.dumps({"book": "Dan", "chapters": list(DETAILS), "rows_changed": changed, "spans_unchanged": True, "candidate_only": True, "non_authorizing": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
