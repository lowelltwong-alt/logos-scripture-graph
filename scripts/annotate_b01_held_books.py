#!/usr/bin/env python3
"""Attach receipt-only r8 packet references to a bounded book batch."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; MODEL=ROOT/".ai/scratch/multi_model_bible_chunking/M7_sol"; BOOKS=("Deut","Josh","Judg","Ruth")
def main()->int:
  for book in BOOKS:
    run=f"{book.lower()}-r8-held-1"; base=f".ai/scratch/multi_model_bible_chunking/M7_sol/state/r8/{book}/{run}"; p=MODEL/"book_chunks"/book/"chunks.jsonl"; rows=[]
    refs=[f"{base}/packet/role-{role}.json" for role in ("original_language_translation_scout","literary_form_scout","canonical_relations_and_premortem_scout","second_temple_rabbinic_context_scout")]+[f"{base}/redteam-note.json",f"{base}/packet/boss-authorization.json"]
    for line in p.read_text(encoding="utf-8").splitlines():
      r=json.loads(line); r["review_status"]="candidate_role_mesh_complete_boss_receipt_only"; r["confidence"]="low"; r["boundary_evidence_refs"]=list(dict.fromkeys(r.get("boundary_evidence_refs",[])+refs)); r["review_holds"]=list(dict.fromkeys(r.get("review_holds",[])+["QF-CORRELATED-SUBSTRATE","QF-ANCIENT-CONTEXT-GAP","external_provider_review","human_appeal_review"])); rows.append(r)
    p.write_text("".join(json.dumps(r,ensure_ascii=False,separators=(",", ":"))+"\n" for r in rows),encoding="utf-8",newline="\n")
  print(BOOKS); return 0
if __name__=="__main__": raise SystemExit(main())
