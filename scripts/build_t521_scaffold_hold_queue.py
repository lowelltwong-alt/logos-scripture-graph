#!/usr/bin/env python3
"""Build a deterministic queue of still-explicit scaffold holds for external review."""
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAP=ROOT/".ai/scratch/multi_model_bible_chunking/M7_sol/state/evidence/final/whole_bible_candidate_map.jsonl"
OUT=ROOT/".ai/scratch/multi_model_bible_chunking/M7_sol/state/evidence/final/scaffold_hold_queue.jsonl"
SCHEMA="t521_scaffold_hold_queue.v1"

def main()->int:
    raw=MAP.read_bytes(); map_hash="sha256:"+hashlib.sha256(raw).hexdigest()
    rows=[json.loads(x) for x in raw.decode("utf-8").splitlines() if x.strip()]
    holds=[]
    for r in rows:
        tags=set(r.get("strong_or_hebrew_tags_used") or [])
        rationale=str(r.get("boundary_rationale") or "").lower()
        if "chapter_scaffold_not_boundary_authority" not in tags and "chapter boundary fallback" not in rationale:
            continue
        book=r["book"]
        family="Koine Greek (CNTR/SBLGNT/UGNT)" if book in {"Matt","Mark","Luke","John","Acts","Rom","1Cor","2Cor","Gal","Eph","Phil","Col","1Thess","2Thess","1Tim","2Tim","Titus","Phlm","Heb","Jas","1Pet","2Pet","1John","2John","3John","Jude","Rev"} else "Hebrew/Aramaic (OSHB/UXLC)"
        holds.append({
            "schema_version":SCHEMA,
            "model_id":"M7_sol",
            "book":book,
            "span":r["span"],
            "decision_id":r.get("decision_id"),
            "chunk_index_in_book":r.get("chunk_index_in_book"),
            "working_title":r.get("working_title"),
            "literature_type_guess":r.get("literature_type_guess"),
            "candidate_internal_seams":r.get("candidate_internal_seams") or [],
            "translation_holds":r.get("translation_difficulties") or r.get("original_language_translation_holds") or [],
            "cross_reference_holds":r.get("cross_reference_holds") or [],
            "red_team_holds":r.get("red_team_premortem_holds") or [],
            "required_source_family":family,
            "review_requirement":"external literary/original-language review before any promotion",
            "candidate_only":True,
            "non_authorizing":True,
            "map_sha256":map_hash,
        })
    OUT.write_text("".join(json.dumps(x,ensure_ascii=False,separators=(",",":"))+"\n" for x in holds),encoding="utf-8",newline="\n")
    print(json.dumps({"schema_version":SCHEMA,"map_sha256":map_hash,"rows":len(holds),"path":str(OUT),"candidate_only":True,"non_authorizing":True},sort_keys=True))
    return 0
if __name__=="__main__": raise SystemExit(main())
