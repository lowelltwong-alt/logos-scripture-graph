#!/usr/bin/env python3
"""Replace the over-broad Numbers 16:1–18:32 candidate with five candidates.

This is a candidate-only structural refinement.  It preserves the original
record as lineage, carries every hold forward, and does not authorize or
promote any boundary.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks/Num/chunks.jsonl"

SPLITS = [
    ("Num.16.1-Num.16.35", "Korah, Dathan, and Abiram conflict through judgment", "rebellion_conflict_and_judgment", "Conflict, challenge, adjudication, and judgment movement."),
    ("Num.16.36-Num.16.40", "Censer memorial and altar-covering instruction", "memorial_instruction", "Memorial/legal instruction separates from the preceding judgment narrative."),
    ("Num.16.41-Num.16.50", "Congregational accusation, plague, and atonement", "plague_and_atonement_narrative", "Complaint, plague, intercession, and atonement movement."),
    ("Num.17.1-Num.17.13", "Rod test and priestly confirmation", "rod_test_narrative", "Test, sign, and response movement with closure."),
    ("Num.18.1-Num.18.32", "Priest and Levite duties and portions", "priestly_statute", "Direct statute/instruction movement after the conflict cycle."),
]


def main() -> int:
    rows = [json.loads(line) for line in PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    target = next((r for r in rows if r["span"] == "Num.16.1-Num.18.32"), None)
    if target is None:
        raise SystemExit("target Num macro candidate not found")
    new_rows = []
    for idx, (span, title, form, rationale) in enumerate(SPLITS, 1):
        row = copy.deepcopy(target)
        row["span"] = span
        row["working_title"] = title
        row["working_title_origin"] = "num_16_18_structural_refinement_v1"
        row["working_title_is_boundary_authority"] = False
        row["literature_type_guess"] = form
        row["boundary_rationale"] = rationale
        row["chunk_index_in_book"] = target["chunk_index_in_book"] + idx - 1
        row["decision_id"] = f"M7_sol-Num-009{chr(96 + idx)}"
        row["split_from_decision_id"] = target["decision_id"]
        row["review_revision"] = int(target.get("review_revision", 0)) + 1
        row["candidate_internal_seams"] = ["scene_or_function_transition", "translation_crosswalk_review"]
        row["translation_and_crossref_holds"] = [
            "Hebrew/Aramaic terminology and versification crosswalk require specialist review",
            "canonical parallels are leads only and cannot authorize a boundary",
        ]
        row["red_team_premortem_holds"] = [
            "test whether the movement is genuinely distinct from adjacent conflict/statute material",
            "test exact coverage and no overlap after any future revision",
        ]
        row["review_status"] = "candidate_role_mesh_complete_boss_receipt_only"
        row["candidate_only"] = True
        row["non_authorizing"] = True
        refs = list(row.get("boundary_evidence_refs") or [])
        if "num_16_18_structural_refinement.v1" not in refs:
            refs.append("num_16_18_structural_refinement.v1")
        row["boundary_evidence_refs"] = refs
        new_rows.append(row)
    out = []
    for row in rows:
        if row is target or row["span"] == target["span"]:
            out.extend(new_rows)
        else:
            out.append(row)
    for i, row in enumerate(out, 1):
        row["chunk_index_in_book"] = i
    PATH.write_text("".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in out), encoding="utf-8", newline="\n")
    print(json.dumps({"book": "Num", "replaced_span": target["span"], "new_spans": [x[0] for x in SPLITS], "rows": len(out), "candidate_only": True, "non_authorizing": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
