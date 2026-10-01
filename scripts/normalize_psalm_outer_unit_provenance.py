#!/usr/bin/env python3
"""Mark Psalm-level outer units accurately without changing spans."""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATHS=[ROOT/".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks/Ps/chunks.jsonl",ROOT/".ai/scratch/multi_model_bible_chunking/M7_sol/state/evidence/final/whole_bible_candidate_map.jsonl"]
WAVE="psalm_level_outer_unit_provenance.v1"

def main()->int:
    reports=[]
    for p in PATHS:
        rows=[json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
        changed=0
        for r in rows:
            if r.get("book")!="Ps": continue
            tags=[x for x in (r.get("strong_or_hebrew_tags_used") or []) if x!="chapter_scaffold_not_boundary_authority"]
            if "psalm_level_outer_unit" not in tags: tags.append("psalm_level_outer_unit")
            r["strong_or_hebrew_tags_used"]=tags
            r["working_title_origin"]=WAVE
            r["working_title_is_boundary_authority"]=False
            r["boundary_rationale"]="Whole-Psalm outer candidate retained as a natural poetic/document unit; superscription, stanza, refrain, acrostic, and collection relations remain internal review questions."
            refs=list(r.get("boundary_evidence_refs") or [])
            if WAVE not in refs: refs.append(WAVE)
            r["boundary_evidence_refs"]=refs
            r["candidate_only"]=True; r["non_authorizing"]=True
            changed+=1
        p.write_text("".join(json.dumps(r,ensure_ascii=False,separators=(",",":"))+"\n" for r in rows),encoding="utf-8",newline="\n")
        reports.append({"path":str(p),"rows_changed":changed})
    print(json.dumps({"book":"Ps","wave":WAVE,"reports":reports,"spans_unchanged":True,"candidate_only":True,"non_authorizing":True},sort_keys=True))
    return 0
if __name__=="__main__": raise SystemExit(main())
