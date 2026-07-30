#!/usr/bin/env python3
"""Mark a supplied book batch as receipt-only mesh-complete after packet checks."""
from __future__ import annotations
import argparse, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; MODEL=ROOT/".ai/scratch/multi_model_bible_chunking/M7_sol"
def main()->int:
  ap=argparse.ArgumentParser(); ap.add_argument("books",nargs="+"); a=ap.parse_args()
  for book in a.books:
    run=f"{book.lower()}-r8-held-1"; base=f".ai/scratch/multi_model_bible_chunking/M7_sol/state/r8/{book}/{run}"; p=MODEL/"book_chunks"/book/"chunks.jsonl"; refs=[f"{base}/packet/role-{r}.json" for r in ("original_language_translation_scout","literary_form_scout","canonical_relations_and_premortem_scout","second_temple_rabbinic_context_scout")]+[f"{base}/redteam-note.json",f"{base}/packet/boss-authorization.json"]; rows=[]
    for line in p.read_text(encoding="utf-8").splitlines():
      r=json.loads(line); r["review_status"]="candidate_role_mesh_complete_boss_receipt_only"; r["boundary_evidence_refs"]=list(dict.fromkeys(r.get("boundary_evidence_refs",[])+refs)); r["review_holds"]=list(dict.fromkeys(r.get("review_holds",[])+["QF-CORRELATED-SUBSTRATE","QF-ANCIENT-CONTEXT-GAP","external_provider_review","human_appeal_review"])); rows.append(r)
    p.write_text("".join(json.dumps(r,ensure_ascii=False,separators=(",", ":"))+"\n" for r in rows),encoding="utf-8",newline="\n")
  print(a.books); return 0
if __name__=="__main__": raise SystemExit(main())
