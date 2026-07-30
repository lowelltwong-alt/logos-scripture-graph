#!/usr/bin/env python3
"""Materialize a coarse Numbers candidate draft from reviewed form zones.

This is deliberately a draft-only artifact: each zone remains low-confidence,
role review and boss/red-team evidence are required before any promotion.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol"

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--output", type=Path, default=MODEL / "book_chunks/Num/chunks.jsonl"); args = ap.parse_args()
    inv = json.loads((MODEL / "reviews/Num/form_inventory.json").read_text(encoding="utf-8"))
    zones = inv["form_zones"]
    rows = []
    for i, zone in enumerate(zones, 1):
        scope = zone["scope"]
        rows.append({
            "model_id": "M7_sol", "book": "Num", "span": scope,
            "chunk_index_in_book": i,
            "working_title": "; ".join(zone["forms"]),
            "literature_type_guess": "+".join(zone["forms"]),
            "boundary_evidence_refs": [f"form_inventory:Num:{zone['zone_id']}", "source_gap_register:Num:crosswalk_required"],
            "strong_or_hebrew_tags_used": ["evidence_only", "crosswalk_pending", "no_boundary_authority"],
            "wj_or_red_letter_considered": False, "frontier_flag_considered": True,
            "confidence": "low", "decision_id": f"M7_sol-Num-{i:03d}",
            "boundary_rationale": zone["parent_child_test"],
            "review_revision": 0, "review_status": "candidate_draft_pending_four_role_mesh",
            "review_holds": ["original_language_review", "literary_redteam", "canonical_premortem", "ancient_context_gap", "boss_authorization"],
            "non_authorizing": True,
        })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows), encoding="utf-8", newline="\n")
    print(args.output); print(json.dumps({"book": "Num", "chunks": len(rows), "status": "candidate_draft_only", "non_authorizing": True}))
    return 0
if __name__ == "__main__": raise SystemExit(main())
