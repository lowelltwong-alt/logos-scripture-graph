#!/usr/bin/env python3
"""Annotate remaining scaffold rows with generic, non-authorizing review holds.

The annotator derives only from each row's existing form label and book family;
it does not invent a new boundary, title, or theological claim.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks"
BOOKS = [p.name for p in BASE.iterdir() if p.is_dir() and (p / "chunks.jsonl").is_file()]
NT = {"Matt","Mark","Luke","John","Acts","Rom","1Cor","2Cor","Gal","Eph","Phil","Col","1Thess","2Thess","1Tim","2Tim","Titus","Phlm","Heb","Jas","1Pet","2Pet","1John","2John","3John","Jude","Rev"}


def seams(form: str) -> list[str]:
    f = form.lower()
    out = []
    if any(k in f for k in ("poem", "hymn", "lament", "lyric", "song", "poetry")):
        out += ["parallelism_or_refrain", "speaker_or_stanza_shift"]
    if any(k in f for k in ("oracle", "prophecy", "vision", "apocalyptic")):
        out += ["oracle_or_vision_heading", "speaker_or_scene_shift", "closure_formula"]
    if any(k in f for k in ("narrative", "tale", "history", "episode", "story")):
        out += ["scene_transition", "speech_or_travel_notice", "episode_closure"]
    if any(k in f for k in ("law", "statute", "ritual", "diagnostic", "covenant", "ceremony")):
        out += ["legal_or_ritual_function_shift", "formula_or_colophon", "instruction_closure"]
    if any(k in f for k in ("epistle", "exposition", "exhortation", "argument", "discourse")):
        out += ["quotation_or_citation", "argument_or_exhortation_turn", "discourse_closure"]
    if not out:
        out = ["local_form_or_scene_shift", "translation_sensitive_transition", "closure_or_collection_edge"]
    return list(dict.fromkeys(out))


def main() -> int:
    changed = 0
    for book in sorted(BOOKS):
        path = BASE / book / "chunks.jsonl"
        rows = [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
        for row in rows:
            refs = list(row.get("boundary_evidence_refs") or [])
            if any("wave" in str(ref) or "refinement" in str(ref) for ref in refs):
                continue
            form = str(row.get("literature_type_guess", ""))
            row["candidate_internal_seams"] = list(dict.fromkeys(list(row.get("candidate_internal_seams") or []) + seams(form)))
            if book in NT:
                row["koine_greek_translation_holds"] = list(dict.fromkeys(list(row.get("koine_greek_translation_holds") or []) + ["Koine morphology, discourse connectors, embedded quotation scope, and translation range require specialist review"]))
            else:
                row["original_language_translation_holds"] = list(dict.fromkeys(list(row.get("original_language_translation_holds") or []) + ["Hebrew/Aramaic morphology, syntax, versification, and translation range require specialist review"]))
            row["cross_reference_holds"] = list(dict.fromkeys(list(row.get("cross_reference_holds") or []) + ["internal/canonical relation and quotation/allusion leads are unverified and cannot authorize a boundary"]))
            row["red_team_premortem_holds"] = list(dict.fromkeys(list(row.get("red_team_premortem_holds") or []) + ["test the candidate edge against local form, discourse, translation, and closure signals rather than chapter numbering alone"]))
            row["working_title_is_boundary_authority"] = False
            row["working_title_origin"] = row.get("working_title_origin", "generic_form_fallback_v1")
            row["candidate_only"] = True
            row["non_authorizing"] = True
            if "generic_scaffold_review_holds.v1" not in refs:
                refs.append("generic_scaffold_review_holds.v1")
            row["boundary_evidence_refs"] = refs
            changed += 1
        path.write_text("".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in rows), encoding="utf-8", newline="\n")
    print(json.dumps({"books": len(BOOKS), "rows_changed": changed, "candidate_only": True, "non_authorizing": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
