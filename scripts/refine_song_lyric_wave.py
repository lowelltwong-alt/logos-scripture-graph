#!/usr/bin/env python3
"""Refine Song of Songs speaker/refrain/scene seam metadata."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks/Song/chunks.jsonl"
DETAILS = {
    1: ("lyric_dialogue_and_chorus", "Opening desire, address, and chorus refrain", ["speaker_attribution", "chorus_refrain", "scene_shift"]),
    2: ("lyric_dialogue_and_chorus", "Spring/landscape imagery, beloved address, and adjuration", ["season_image", "speaker_turn", "adjuration_refrain"]),
    3: ("lyric_search_and_procession", "Night search, finding, and royal/processional scene", ["search_scene", "finding_closure", "procession_shift"]),
    4: ("praise_and_response_lyric", "Extended praise address and garden imagery", ["praise_speech", "garden_image", "response_or_chorus"]),
    5: ("dream_search_and_praise_dialogue", "Door/search episode, chorus question, and praise response", ["door_scene", "search_lament", "chorus_question", "praise_catalogue"]),
    6: ("garden_dialogue_and_collection_refrain", "Garden/assembly dialogue and recurring identity refrain", ["speaker_turn", "garden_scene", "identity_refrain"]),
    7: ("body_praise_and_desire_lyric", "Body-praise sequence and reciprocal desire", ["praise_catalogue", "speaker_turn", "desire_response"]),
    8: ("love_adjuration_and_closure", "Love poem, adjuration, sibling/garden material, and closing dialogue", ["love_maxim", "adjuration", "sibling_scene", "garden_closure"]),
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
        row["working_title_origin"] = "song_lyric_wave_v1"
        row["working_title_is_boundary_authority"] = False
        row["boundary_rationale"] = "Chapter-sized outer candidate retained provisionally; speaker, chorus, refrain, adjuration, and scene transitions require independent Hebrew lyric review."
        row["candidate_internal_seams"] = seams
        row["original_language_translation_holds"] = ["Hebrew speaker attribution, compact syntax, erotic imagery, and refrain wording require qualified review"]
        row["cross_reference_holds"] = ["lyric imagery parallels are leads only; do not impose allegorical or theological structure"]
        row["red_team_premortem_holds"] = ["remove English headings and test whether each proposed speaker/scene seam survives local textual signals"]
        row["review_revision"] = int(row.get("review_revision", 0)) + 1
        row["candidate_only"] = True
        row["non_authorizing"] = True
        refs = list(row.get("boundary_evidence_refs") or [])
        if "song_lyric_wave.v1" not in refs:
            refs.append("song_lyric_wave.v1")
        row["boundary_evidence_refs"] = refs
        changed += 1
    PATH.write_text("".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in rows), encoding="utf-8", newline="\n")
    print(json.dumps({"book": "Song", "chapters": list(DETAILS), "rows_changed": changed, "spans_unchanged": True, "candidate_only": True, "non_authorizing": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
