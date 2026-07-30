#!/usr/bin/env python3
"""Fail-closed validation for the T521 external review packet index."""
from __future__ import annotations
import hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MODEL=ROOT/".ai/scratch/multi_model_bible_chunking/M7_sol"
INDEX=MODEL/"state/evidence/final/external_review_packet_index.json"
MAP=MODEL/"state/evidence/final/whole_bible_candidate_map.jsonl"
PROMPT=ROOT/"docs/governance/T521_EXTERNAL_REVIEWER_COPY_PASTE_PROMPT.md"
HANDOFF=ROOT/"docs/governance/T521_EXTERNAL_CONVERGENCE_HANDOFF_PROMPT.md"
QUEUE=MODEL/"state/evidence/final/scaffold_hold_queue.jsonl"

def digest(p:Path)->str: return "sha256:"+hashlib.sha256(p.read_bytes()).hexdigest()
def main()->int:
    d=json.loads(INDEX.read_text(encoding="utf-8")); errors=[]
    if d.get("candidate_only") is not True: errors.append("candidate_only must equal True")
    if d.get("non_authorizing") is not True: errors.append("non_authorizing must equal True")
    if d.get("promotion_authorized") is not False: errors.append("promotion_authorized must equal False")
    if d.get("sibling_maps_read_before_review") is not False: errors.append("sibling_maps_read_before_review must equal False")
    if d.get("map",{}).get("sha256") != digest(MAP): errors.append("map hash mismatch")
    prompt_path=Path(d.get("prompt",{}).get("path",str(HANDOFF)))
    if d.get("prompt",{}).get("sha256") != digest(prompt_path): errors.append("handoff prompt hash mismatch")
    reviewer=d.get("reviewer_prompt")
    if reviewer and reviewer.get("sha256") != digest(PROMPT): errors.append("reviewer prompt hash mismatch")
    q=d.get("scaffold_hold_queue")
    if not q or q.get("sha256") != digest(QUEUE): errors.append("scaffold queue hash mismatch")
    if q and q.get("rows") != sum(1 for x in QUEUE.read_text(encoding="utf-8").splitlines() if x.strip()): errors.append("scaffold queue row count mismatch")
    allowed="\n".join(str(x).lower() for x in d.get("allowed_inputs",[]))
    if "sibling" in allowed or "m1_" in allowed or "m2_" in allowed or "m3_" in allowed or "m4_" in allowed or "m5_" in allowed or "m6_" in allowed: errors.append("sibling map/provider input exposed")
    if errors:
        print(json.dumps({"status":"FAIL","errors":errors},sort_keys=True)); return 1
    print(json.dumps({"status":"OK","books":d.get("map",{}).get("books"),"chunks":d.get("map",{}).get("chunks"),"scaffold_rows":d.get("scaffold_hold_queue",{}).get("rows"),"candidate_only":True,"non_authorizing":True,"independence_status":d.get("independence_status")},sort_keys=True)); return 0
if __name__=="__main__": raise SystemExit(main())
