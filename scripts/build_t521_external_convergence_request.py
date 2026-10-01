#!/usr/bin/env python3
"""Freeze a privacy-safe request for an independent external review."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; MODEL=ROOT/".ai/scratch/multi_model_bible_chunking/M7_sol"; MAP=MODEL/"state/evidence/final/whole_bible_candidate_map.jsonl"; PROMPT=ROOT/"docs/governance/T521_EXTERNAL_CONVERGENCE_HANDOFF_PROMPT.md"
def d(p): return "sha256:"+hashlib.sha256(p.read_bytes()).hexdigest()
def main()->int:
  rows=[json.loads(x) for x in MAP.read_text(encoding="utf-8").splitlines() if x.strip()]; out=MODEL/"state/evidence/final/external_convergence_request.json"; payload={"schema_version":"t521_external_convergence_request.v1","map_path":str(MAP.relative_to(ROOT)).replace("\\","/"),"map_sha256":d(MAP),"prompt_path":str(PROMPT.relative_to(ROOT)).replace("\\","/"),"prompt_sha256":d(PROMPT),"book_count":len({r["book"] for r in rows}),"chunk_count":len(rows),"sibling_maps_read_before_review":False,"candidate_only":True,"non_authorizing":True,"promotion_authorized":False,"independence_status":"awaiting_external_provider_or_human_receipt"}; out.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8",newline="\n"); print(out); print(json.dumps(payload,sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
