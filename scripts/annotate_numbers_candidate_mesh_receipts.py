#!/usr/bin/env python3
"""Bind Numbers draft chunks to the completed r8 role/red-team receipt refs."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHUNKS = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks/Num/chunks.jsonl"
REFS = [
    ".ai/scratch/multi_model_bible_chunking/M7_sol/state/r8/Num/num-r8-20260722a/packet/role-original_language_translation_scout.json",
    ".ai/scratch/multi_model_bible_chunking/M7_sol/state/r8/Num/num-r8-20260722a/packet/role-literary_form_scout.json",
    ".ai/scratch/multi_model_bible_chunking/M7_sol/state/r8/Num/num-r8-20260722a/packet/role-canonical_relations_and_premortem_scout.json",
    ".ai/scratch/multi_model_bible_chunking/M7_sol/state/r8/Num/num-r8-20260722a/packet/role-second_temple_rabbinic_context_scout.json",
    ".ai/scratch/multi_model_bible_chunking/M7_sol/state/r8/Num/num-r8-20260722a/redteam-note.json",
    ".ai/scratch/multi_model_bible_chunking/M7_sol/state/r8/Num/num-r8-20260722a/packet/boss-authorization.json",
]

def main() -> int:
    rows = []
    for line in CHUNKS.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        row["review_status"] = "candidate_role_mesh_complete_boss_receipt_only"
        row["boundary_evidence_refs"] = list(dict.fromkeys(row["boundary_evidence_refs"] + REFS))
        row["review_holds"] = list(dict.fromkeys(row["review_holds"] + ["QF-CORRELATED-SUBSTRATE", "QF-ANCIENT-CONTEXT-GAP", "external_provider_review", "human_appeal_review"]))
        rows.append(row)
    CHUNKS.write_text("".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows), encoding="utf-8", newline="\n")
    print(CHUNKS); return 0
if __name__ == "__main__": raise SystemExit(main())
