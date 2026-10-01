#!/usr/bin/env python3
"""Split the over-broad Acts 19:1–20:38 candidate into local movements."""
from __future__ import annotations

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks/Acts/chunks.jsonl"
SPLITS = [
    ("Acts.19.1-Acts.19.10", "Ephesus disciples, synagogue, and lecture", "mission_teaching_episode"),
    ("Acts.19.11-Acts.19.20", "Extraordinary works, failed exorcism, and word-growth closure", "sign_and_response_episode"),
    ("Acts.19.21-Acts.19.41", "Travel purpose, Artemis disturbance, and civic assembly", "riot_and_civic_speech_narrative"),
    ("Acts.20.1-Acts.20.12", "Macedonian travel, Troas gathering, and Eutychus episode", "travel_and_resurrection_like_episode"),
    ("Acts.20.13-Acts.20.38", "Miletus farewell speech to the Ephesian elders", "farewell_speech"),
]


def main() -> int:
    rows = [json.loads(line) for line in PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    target = next((r for r in rows if r["span"] == "Acts.19.1-Acts.20.38"), None)
    if target is None:
        raise SystemExit("target Acts macro candidate not found")
    generated = []
    for n, (span, title, form) in enumerate(SPLITS, 1):
        row = copy.deepcopy(target)
        row["span"] = span
        row["working_title"] = title
        row["working_title_origin"] = "acts_19_20_structural_refinement_v1"
        row["working_title_is_boundary_authority"] = False
        row["literature_type_guess"] = form
        row["boundary_rationale"] = "Local narrated scene, speech, or travel transition; outer candidate only pending independent literary and Koine review."
        row["chunk_index_in_book"] = target["chunk_index_in_book"] + n - 1
        row["decision_id"] = f"M7_sol-Acts-009{chr(96+n)}"
        row["split_from_decision_id"] = target["decision_id"]
        row["review_revision"] = int(target.get("review_revision", 0)) + 1
        row["candidate_internal_seams"] = ["scene_transition", "speech_or_crowd_shift", "travel_notice_or_closure"]
        row["koine_greek_translation_holds"] = ["discourse particles, speech framing, and technical civic/leadership terms require review"]
        row["cross_reference_holds"] = ["Acts and Pauline parallels are leads only; do not harmonize them into boundaries"]
        row["red_team_premortem_holds"] = ["test whether local scene/speech markers support the edge without relying on modern chapter numbers"]
        row["review_status"] = "candidate_role_mesh_complete_boss_receipt_only"
        row["candidate_only"] = True
        row["non_authorizing"] = True
        refs = list(row.get("boundary_evidence_refs") or [])
        if "acts_19_20_structural_refinement.v1" not in refs:
            refs.append("acts_19_20_structural_refinement.v1")
        row["boundary_evidence_refs"] = refs
        generated.append(row)
    output = []
    for row in rows:
        if row["span"] == target["span"]:
            output.extend(generated)
        else:
            output.append(row)
    for i, row in enumerate(output, 1):
        row["chunk_index_in_book"] = i
    PATH.write_text("".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in output), encoding="utf-8", newline="\n")
    print(json.dumps({"book": "Acts", "replaced_span": target["span"], "new_spans": [x[0] for x in SPLITS], "rows": len(output), "candidate_only": True, "non_authorizing": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
