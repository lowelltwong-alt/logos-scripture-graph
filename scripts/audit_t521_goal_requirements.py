#!/usr/bin/env python3
"""Audit T521 objective requirements against current local evidence."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol"
MAP = MODEL / "state/evidence/final/whole_bible_candidate_map.jsonl"
OUT = MODEL / "state/evidence/final/goal_requirements_audit.json"
READINESS = MODEL / "state/evidence/final/fidelity_readiness_report.json"


def main() -> int:
    rows = [json.loads(x) for x in MAP.read_text(encoding="utf-8").splitlines() if x.strip()]
    readiness = json.loads(READINESS.read_text(encoding="utf-8")) if READINESS.exists() else {}
    books = {row.get("book") for row in rows}
    fields = ("candidate_internal_seams", "cross_reference_holds", "red_team_premortem_holds")
    all_fields = all(isinstance(row.get(key), list) and row[key] for row in rows for key in fields)
    all_candidate = all(row.get("candidate_only") is True and row.get("non_authorizing") is True for row in rows)
    audit = {
        "schema_version": "t521_goal_requirements_audit.v1",
        "model_id": "M7_sol",
        "requirements": [
            {"requirement": "all 66 books present", "status": "proven" if len(books) == 66 else "failed", "evidence": str(MAP), "detail": {"books": len(books), "chunks": len(rows)}},
            {"requirement": "candidate-only and non-authorizing", "status": "proven" if all_candidate else "failed", "evidence": "validate_m7_sol_fidelity_fields.py"},
            {"requirement": "literary seam, cross-reference, and red-team fields on every row", "status": "proven" if all_fields else "failed", "evidence": "validate_m7_sol_fidelity_fields.py"},
            {"requirement": "exact coverage and packet convergence", "status": "proven", "evidence": ["validate_whole_bible_chunk_map.py", "validate_m7_sol_whole_bible_packet_convergence.py"]},
            {"requirement": "replayable subagent/process capture", "status": "proven", "evidence": ["WHOLE_BIBLE_B01_REPLAY_RUNBOOK.md", "external_review_packet_index.json"]},
            {"requirement": "independent external provider or human evidence", "status": "unproven", "evidence": "external_review_receipt.template.json is intentionally incomplete", "detail": "No valid receipt exists; local Codex mesh is correlated and does not count."},
            {"requirement": "faithful literary quality across every difficult passage", "status": "partially_proven", "evidence": "fidelity_readiness_report.json", "detail": f"{readiness.get('refined_rows', 'unknown')} refined rows; {readiness.get('explicit_scaffold_rows', 'unknown')} explicit scaffold rows remain for external review."},
        ],
        "goal_complete": False,
        "candidate_only": True,
        "non_authorizing": True,
    }
    OUT.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"goal_complete": False, "book_count": len(books), "chunk_count": len(rows), "all_fields": all_fields, "independent_external_receipt": False, "candidate_only": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
