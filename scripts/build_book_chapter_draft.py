#!/usr/bin/env python3
"""Create explicit low-confidence chapter frames for a book pending B01 mesh.

Chapter frames are scaffolding only; they are not claimed as faithful final
literary boundaries and must be replaced/refined by role evidence.
"""
from __future__ import annotations
import argparse, json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol"

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("books", nargs="+", help="canonical book IDs"); args = ap.parse_args()
    passages = defaultdict(list)
    with (ROOT / "data/canonical/scripture/passages/passages.jsonl").open(encoding="utf-8") as fh:
        for line in fh:
            row = json.loads(line)
            if row["book"] in args.books: passages[row["book"]].append(row)
    for book in args.books:
        if not passages[book]: raise SystemExit(f"no canonical passages for {book}")
        by_chapter = defaultdict(list)
        for row in passages[book]: by_chapter[row["chapter"]].append(row)
        out = MODEL / "book_chunks" / book / "chunks.jsonl"; out.parent.mkdir(parents=True, exist_ok=True)
        rows = []
        for i, chapter in enumerate(sorted(by_chapter), 1):
            verses = by_chapter[chapter]
            rows.append({"model_id":"M7_sol","book":book,"span":f"{book}.{chapter}.{min(v['verse_start'] for v in verses)}-{book}.{chapter}.{max(v['verse_end'] for v in verses)}","chunk_index_in_book":i,"working_title":f"Chapter {chapter} structural frame (draft)","literature_type_guess":"chapter_frame_pending_form_review","boundary_evidence_refs":["canonical_passage_identity_only","whole_bible_role_source_matrix.v1"],"strong_or_hebrew_tags_used":["evidence_only","chapter_scaffold_not_boundary_authority"],"wj_or_red_letter_considered":False,"frontier_flag_considered":True,"confidence":"low","decision_id":f"M7_sol-{book}-{i:03d}","boundary_rationale":"Temporary chapter frame pending literary, original-language, canonical/premortem, and ancient-context gap review.","review_revision":0,"review_status":"candidate_scaffold_pending_b01_mesh","review_holds":["literary_form_review","original_language_review","canonical_premortem_review","ancient_context_gap","boss_authorization"],"non_authorizing":True})
        out.write_text("".join(json.dumps(row,separators=(",", ":"))+"\n" for row in rows),encoding="utf-8",newline="\n")
        strategy = MODEL / "book_strategy" / f"{book}.md"; strategy.parent.mkdir(parents=True, exist_ok=True); strategy.write_text(f"# {book} candidate strategy\n\nThis is a low-confidence chapter-frame scaffold only. It is not a final literary map. Four-role B01 review, red-team, preserved appeals, and boss receipt are required.\n\n- candidate_only: true\n- non_authorizing: true\n- chapter_frames: {len(rows)}\n- ancient_context: explicit corpus gap until qualified\n", encoding="utf-8", newline="\n")
        print(json.dumps({"book":book,"chunks":len(rows),"status":"scaffold_pending_b01_mesh"}))
    return 0
if __name__ == "__main__": raise SystemExit(main())
