#!/usr/bin/env python3
"""Refine Deuteronomy 27–30 ceremony/covenant seam metadata."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks/Deut/chunks.jsonl"
DETAILS = {
    27: ("inscription_and_ceremony", "Inscription, altar/ceremony, and responsive pronouncement sequence", ["inscription", "altar_ceremony", "responsive_formula", "blessing_curse_onset"]),
    28: ("blessing_curse_covenant_speech", "Blessing and curse parallel speech sequence", ["blessing_block", "curse_block", "refrain", "formula_closure"]),
    29: ("covenant_renewal_speech", "Covenant-renewal assembly and hidden-things discourse", ["assembly_frame", "covenant_formula", "warning_speech", "public_private_turn"]),
    30: ("restoration_and_choice_speech", "Restoration promise, command accessibility, and life/death choice", ["restoration_turn", "command_discourse", "witness_formula", "choice_closure"]),
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
        row["working_title_origin"] = "deut_27_30_covenant_wave_v1"
        row["working_title_is_boundary_authority"] = False
        row["boundary_rationale"] = "Chapter-sized outer candidate retained provisionally; ceremony, formula, speaker, and blessing/curse or choice transitions require Hebrew review."
        row["candidate_internal_seams"] = seams
        row["original_language_translation_holds"] = ["Hebrew discourse particles, repeated formulae, legal/covenant terms, and translation variants require review"]
        row["cross_reference_holds"] = ["canonical covenant echoes are leads only and cannot authorize a seam"]
        row["red_team_premortem_holds"] = ["test whether repeated formula is internal architecture or a true closure; test chapter-edge continuity"]
        row["review_revision"] = int(row.get("review_revision", 0)) + 1
        row["candidate_only"] = True
        row["non_authorizing"] = True
        refs = list(row.get("boundary_evidence_refs") or [])
        if "deut_27_30_covenant_wave.v1" not in refs:
            refs.append("deut_27_30_covenant_wave.v1")
        row["boundary_evidence_refs"] = refs
        changed += 1
    PATH.write_text("".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in rows), encoding="utf-8", newline="\n")
    print(json.dumps({"book": "Deut", "chapters": [27, 28, 29, 30], "rows_changed": changed, "spans_unchanged": True, "candidate_only": True, "non_authorizing": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
