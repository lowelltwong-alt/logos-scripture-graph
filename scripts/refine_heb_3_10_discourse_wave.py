#!/usr/bin/env python3
"""Refine Hebrews 3–10 quotation/exposition/warning seam metadata."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks/Heb/chunks.jsonl"

DETAILS = {
    3: ("quotation_exposition_warning", "Moses/house comparison and wilderness-warning exposition", ["quotation_onset", "exposition", "warning_interruption", "continuity_to_4"]),
    4: ("scriptural_exposition_rest_warning", "Rest promise exposition and exhortation to enter rest", ["quotation_continuation", "exposition", "exhortation", "argument_resumption"]),
    5: ("priesthood_exposition_warning", "High-priest exposition, appointment, and maturity warning", ["exposition", "priesthood_turn", "warning", "continuity_to_6"]),
    6: ("warning_and_promise_exhortation", "Warning passage, promise, and hope-anchor exhortation", ["warning_frame", "promise", "oath_anchor", "argument_resumption"]),
    7: ("priesthood_scriptural_exposition", "Melchizedek/priesthood exposition and scriptural citation chain", ["citation_catena", "exposition", "contrast_turn", "closure"]),
    8: ("covenant_tabernacle_exposition", "Covenant quotation, tabernacle contrast, and transition", ["quotation", "tabernacle_description", "covenant_turn", "continuity_to_9"]),
    9: ("ritual_tabernacle_exposition", "Tabernacle arrangement, ritual access, and blood/covenant exposition", ["spatial_description", "ritual_exposition", "citation_or_testament_turn", "argument_closure"]),
    10: ("sacrifice_exposition_warning", "Sacrifice quotation, access exhortation, warning, and faith transition", ["quotation_catena", "exposition", "warning", "exhortation_to_faith"]),
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
        row["working_title_origin"] = "heb_3_10_discourse_wave_v1"
        row["working_title_is_boundary_authority"] = False
        row["boundary_rationale"] = "Chapter-sized outer candidate retained provisionally; quotation, exposition, warning, and exhortation transitions require independent Koine review."
        row["candidate_internal_seams"] = seams
        row["koine_greek_translation_holds"] = ["participial chains, connective particles, embedded quotations, and lexical range require Koine review"]
        row["cross_reference_holds"] = ["Hebrews quotation/allusion leads require verified source mapping; citation boundaries are not automatically discourse boundaries"]
        row["red_team_premortem_holds"] = ["test whether a warning interrupts or completes exposition; test continuity across modern chapter edges"]
        row["review_revision"] = int(row.get("review_revision", 0)) + 1
        row["candidate_only"] = True
        row["non_authorizing"] = True
        refs = list(row.get("boundary_evidence_refs") or [])
        if "heb_3_10_discourse_wave.v1" not in refs:
            refs.append("heb_3_10_discourse_wave.v1")
        row["boundary_evidence_refs"] = refs
        changed += 1
    PATH.write_text("".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in rows), encoding="utf-8", newline="\n")
    print(json.dumps({"book": "Heb", "chapters": list(DETAILS), "rows_changed": changed, "spans_unchanged": True, "candidate_only": True, "non_authorizing": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
