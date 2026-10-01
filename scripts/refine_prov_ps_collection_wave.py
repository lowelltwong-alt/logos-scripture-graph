#!/usr/bin/env python3
"""Refine Proverbs collection headings and Psalm 42–43 continuity metadata."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def update_prov() -> int:
    path = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks/Prov/chunks.jsonl"
    rows = [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
    changed = 0
    for row in rows:
        ch = int(row["span"].split(".", 2)[1].split("-", 1)[0])
        if ch not in (22, 23, 24):
            continue
        if ch == 22:
            title, form, seams = "Aphoristic sayings and collection transition", "aphoristic_sayings_collection", ["saying_cluster", "collection_heading_scope", "instruction_turn"]
        else:
            title, form, seams = "Sayings of the wise collection and aphorism clusters", "sayings_of_the_wise_collection", ["collection_heading", "saying_cluster", "instruction_turn"]
        row["working_title"] = title
        row["working_title_origin"] = "prov_collection_wave_v1"
        row["working_title_is_boundary_authority"] = False
        row["literature_type_guess"] = form
        row["boundary_rationale"] = "Chapter-sized outer candidate retained provisionally; collection-heading scope and aphorism clusters require Hebrew review."
        row["candidate_internal_seams"] = seams
        row["original_language_translation_holds"] = ["heading syntax, terse Hebrew parallelism, and textual variants may alter collection scope"]
        row["red_team_premortem_holds"] = ["test heading scope across chapter edges; do not use English punctuation as authority"]
        row["review_revision"] = int(row.get("review_revision", 0)) + 1
        row["candidate_only"] = True
        row["non_authorizing"] = True
        refs = list(row.get("boundary_evidence_refs") or [])
        if "prov_collection_wave.v1" not in refs:
            refs.append("prov_collection_wave.v1")
        row["boundary_evidence_refs"] = refs
        changed += 1
    path.write_text("".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in rows), encoding="utf-8", newline="\n")
    return changed


def update_ps() -> int:
    path = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks/Ps/chunks.jsonl"
    rows = [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
    changed = 0
    for row in rows:
        ch = int(row["span"].split(".", 2)[1].split("-", 1)[0])
        if ch not in (42, 43):
            continue
        row["working_title"] = "Korahite lament cycle (Psalm 42–43 continuity candidate)"
        row["working_title_origin"] = "ps_42_43_collection_wave_v1"
        row["working_title_is_boundary_authority"] = False
        row["literature_type_guess"] = "korahite_lament_cycle"
        row["boundary_rationale"] = "Psalm-level outer candidates retained; repeated refrain and collection relation make 42–43 continuity a review question, not a forced merge."
        row["candidate_internal_seams"] = ["refrain_return", "lament_to_petition", "superscription_or_collection_edge", "possible_cross_psalm_continuity"]
        row["original_language_translation_holds"] = ["Hebrew refrain wording, superscription status, and parallelism require source review"]
        row["cross_reference_holds"] = ["cross-psalm relation is a lead only; later liturgical grouping cannot decide a boundary"]
        row["red_team_premortem_holds"] = ["test both preserve-separate and join hypotheses against local refrain and superscription evidence"]
        row["review_revision"] = int(row.get("review_revision", 0)) + 1
        row["candidate_only"] = True
        row["non_authorizing"] = True
        refs = list(row.get("boundary_evidence_refs") or [])
        if "ps_42_43_collection_wave.v1" not in refs:
            refs.append("ps_42_43_collection_wave.v1")
        row["boundary_evidence_refs"] = refs
        changed += 1
    path.write_text("".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in rows), encoding="utf-8", newline="\n")
    return changed


def main() -> int:
    print(json.dumps({"books": ["Prov", "Ps"], "rows_changed": update_prov() + update_ps(), "candidate_only": True, "non_authorizing": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
