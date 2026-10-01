#!/usr/bin/env python3
"""Record cross-chapter argument continuity for Romans 9–11 candidates."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks/Rom/chunks.jsonl"
DETAILS = {
    9: ("scriptural_argument_and_objection", "Israel, promise, and objection-response sequence", ["lament/opening", "scriptural citation", "objection-response", "chapter-continuity-to-10"]),
    10: ("scriptural_argument_and_proclamation", "Scriptural citation, proclamation, and response sequence", ["citation-catena", "rhetorical-question", "proclamation-response", "chapter-continuity-from-9-to-11"]),
    11: ("argument_closure_and_doxology", "Remnant, grafting warning, mystery exposition, and doxological closure", ["objection-response", "hortatory warning", "mystery/argument closure", "doxology"]),
}


def main() -> int:
    rows = [json.loads(line) for line in PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    changed = 0
    for row in rows:
        ch = int(row["span"].split(".", 2)[1].split("-", 1)[0])
        if ch not in DETAILS:
            continue
        form, rationale, seams = DETAILS[ch]
        row["literature_type_guess"] = form
        row["working_title"] = rationale
        row["working_title_origin"] = "rom_9_11_argument_refinement_v1"
        row["working_title_is_boundary_authority"] = False
        row["boundary_rationale"] = "Chapter-sized outer candidate retained provisionally; argument continuity across Romans 9–11 is explicit and internal citation/objection seams require review."
        row["candidate_internal_seams"] = seams
        row["koine_greek_translation_holds"] = ["diatribe voice, rhetorical questions, citation connectors, and lexical range require Koine review"]
        row["cross_reference_holds"] = ["quotation/allusion links are review leads only; do not let canonical parallels determine a boundary"]
        row["red_team_premortem_holds"] = ["test chapter edge against argument continuity and citation-catena; test embedded voice attribution"]
        row["review_revision"] = int(row.get("review_revision", 0)) + 1
        refs = list(row.get("boundary_evidence_refs") or [])
        if "rom_9_11_argument_refinement.v1" not in refs:
            refs.append("rom_9_11_argument_refinement.v1")
        row["boundary_evidence_refs"] = refs
        row["candidate_only"] = True
        row["non_authorizing"] = True
        changed += 1
    PATH.write_text("".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows), encoding="utf-8", newline="\n")
    print(json.dumps({"book": "Rom", "chapters": [9, 10, 11], "rows_changed": changed, "spans_unchanged": True, "candidate_only": True, "non_authorizing": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
