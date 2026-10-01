#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; MODEL=ROOT/".ai/scratch/multi_model_bible_chunking/M7_sol"
BOOKS=["Gen","Exod","Lev","Num","Deut","Josh","Judg","Ruth","1Sam","2Sam","1Kgs","2Kgs","1Chr","2Chr","Ezra","Neh","Esth","Job","Ps","Prov","Eccl","Song","Isa","Jer","Lam","Ezek","Dan","Hos","Joel","Amos","Obad","Jonah","Mic","Nah","Hab","Zeph","Hag","Zech","Mal","Matt","Mark","Luke","John","Acts","Rom","1Cor","2Cor","Gal","Eph","Phil","Col","1Thess","2Thess","1Tim","2Tim","Titus","Phlm","Heb","Jas","1Pet","2Pet","1John","2John","3John","Jude","Rev"]
def main()->int:
  for book in BOOKS:
    p=MODEL/"book_chunks"/book/"chunks.jsonl"; rid=f"{book.lower()}-r8-held-1"; base=f".ai/scratch/multi_model_bible_chunking/M7_sol/state/r8/{book}/{rid}"; refs=[f"{base}/challenge_appeal_ledger/{book}-challenge.json",f"{base}/challenge_appeal_ledger/{book}-appeal.json"]
    rows=[]
    for line in p.read_text(encoding="utf-8").splitlines():
      r=json.loads(line); r["boundary_evidence_refs"]=list(dict.fromkeys(r.get("boundary_evidence_refs",[])+refs)); r["review_holds"]=list(dict.fromkeys(r.get("review_holds",[])+["append_only_challenge_ledger","append_only_appeal_ledger"])); rows.append(r)
    p.write_text("".join(json.dumps(r,ensure_ascii=False,separators=(",", ":"))+"\n" for r in rows),encoding="utf-8",newline="\n")
  return 0
if __name__=="__main__": raise SystemExit(main())
