#!/usr/bin/env python3
"""Audit all 66 Sol B01 held packets without claiming provider independence."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; MODEL=ROOT/".ai/scratch/multi_model_bible_chunking/M7_sol"
BOOKS=["Gen","Exod","Lev","Num","Deut","Josh","Judg","Ruth","1Sam","2Sam","1Kgs","2Kgs","1Chr","2Chr","Ezra","Neh","Esth","Job","Ps","Prov","Eccl","Song","Isa","Jer","Lam","Ezek","Dan","Hos","Joel","Amos","Obad","Jonah","Mic","Nah","Hab","Zeph","Hag","Zech","Mal","Matt","Mark","Luke","John","Acts","Rom","1Cor","2Cor","Gal","Eph","Phil","Col","1Thess","2Thess","1Tim","2Tim","Titus","Phlm","Heb","Jas","1Pet","2Pet","1John","2John","3John","Jude","Rev"]
ROLES=["original_language_translation_scout","literary_form_scout","canonical_relations_and_premortem_scout","second_temple_rabbinic_context_scout"]
def main()->int:
 missing=[]; invalid=[]
 for book in BOOKS:
  root=MODEL/"state/r8"/book/f"{book.lower()}-r8-held-1"; packet=root/"packet"; names={p.name for p in packet.glob("*.json")}; expected={"input-manifest.json","boss-authorization.json"}|{f"role-{r}.json" for r in ROLES}; ledger=root/"challenge_appeal_ledger"
  if not expected.issubset(names) or not (ledger/f"{book}-challenge.json").is_file() or not (ledger/f"{book}-appeal.json").is_file(): missing.append(book); continue
  boss=json.loads((packet/"boss-authorization.json").read_text(encoding="utf-8"));
  if boss.get("B02_authorized",False) or boss.get("verdict")!="GO_B01_RECEIPT_ONLY" or boss.get("non_authorizing") is not True: invalid.append(book)
 result={"books":len(BOOKS),"missing_or_incomplete":missing,"invalid_boss":invalid,"all_packets_complete":not missing and not invalid,"cross_model_independence_claimed":False,"promotion_qualified":False,"candidate_only":True,"non_authorizing":True}; print(json.dumps(result,sort_keys=True)); return 0 if result["all_packets_complete"] else 1
if __name__=="__main__": raise SystemExit(main())
