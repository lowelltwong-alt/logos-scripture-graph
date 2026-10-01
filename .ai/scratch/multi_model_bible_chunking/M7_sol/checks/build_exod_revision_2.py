#!/usr/bin/env python3
"""Apply Exodus' second and final automatic rewrite."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
MODEL = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol"
CHUNKS = MODEL / "book_chunks" / "Exod" / "chunks.jsonl"
RELATIONS = MODEL / "reviews" / "Exod" / "decision_relations.jsonl"
EXPECTED_FROZEN = "24894c4bf6ba562e91507cf4297bfe84d47f0cd7497fd6a9f1983289ebd38b4f"


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def child(base: dict, *, decision_id: str, index: float, span: str, title: str,
          form: str, rationale: str) -> dict:
    row = copy.deepcopy(base)
    row.update({
        "span": span,
        "chunk_index_in_book": index,
        "working_title": title,
        "literature_type_guess": form,
        "boundary_evidence_refs": [
            f"direct_read:eng-web:{span}",
            f"book_strategy:Exod:{form}",
            "reviews/Exod/primary_r1_hebrew.json",
            "reviews/Exod/primary_r1_literary.json",
            "reviews/Exod/peer_r1_crosscheck.json",
            "reviews/Exod/boss_r1_ruling.json",
            "source_metadata:evidence_only",
        ],
        "confidence": "medium",
        "decision_id": decision_id,
        "boundary_rationale": rationale,
        "review_revision": 2,
        "review_status": "revision_2_final_cycle_pending_postcheck",
        "frontier_flag_considered": False,
    })
    row.pop("candidate_hold_state", None)
    return row


def main() -> int:
    actual = hashlib.sha256(CHUNKS.read_bytes()).hexdigest()
    if actual != EXPECTED_FROZEN:
        raise SystemExit(f"expected revision-1 hash {EXPECTED_FROZEN}, found {actual}")
    original = read_jsonl(CHUNKS)
    result: list[dict] = []
    for row in original:
        decision_id = row["decision_id"]
        if decision_id == "M7_sol-Exod-043b":
            result.extend([
                child(row, decision_id="M7_sol-Exod-043b1", index=43.1,
                      span="Exod.30.11-Exod.30.16", title="Census ransom for sanctuary service",
                      form="census_ransom_instruction",
                      rationale="A fresh speech formula introduces a complete census-ransom procedure with its own purpose and closure."),
                child(row, decision_id="M7_sol-Exod-043b2", index=43.2,
                      span="Exod.30.17-Exod.30.21", title="Bronze basin washing provision",
                      form="basin_washing_instruction",
                      rationale="A fresh speech formula and distinct cultic object introduce a complete priestly washing procedure."),
            ])
            continue
        if decision_id == "M7_sol-Exod-043c":
            result.extend([
                child(row, decision_id="M7_sol-Exod-043c1", index=43.3,
                      span="Exod.30.22-Exod.30.33", title="Holy anointing oil formulation and restrictions",
                      form="anointing_oil_procedure",
                      rationale="A fresh speech formula frames the anointing-oil recipe, uses, holiness rule, and imitation sanction as one procedure."),
                child(row, decision_id="M7_sol-Exod-043c2", index=43.4,
                      span="Exod.30.34-Exod.30.38", title="Sacred incense formulation and restrictions",
                      form="sacred_incense_procedure",
                      rationale="A fresh speech formula frames a distinct incense recipe, sanctuary use, holiness rule, and imitation sanction."),
            ])
            continue
        if decision_id == "M7_sol-Exod-044":
            row = copy.deepcopy(row)
            row["review_status"] = "revision_2_final_deferred_appeal"
            row["boundary_evidence_refs"] = list(dict.fromkeys(row["boundary_evidence_refs"] + [
                "reviews/Exod/boss_r1_ruling.json",
                "reviews/Exod/appeal_round_2.json",
            ]))
        result.append(row)
    with CHUNKS.open("w", encoding="utf-8", newline="\n") as handle:
        for row in result:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")

    relations = read_jsonl(RELATIONS)
    for relation in relations:
        if relation["note_id"] == "RN-EXOD-006":
            relation["children"] = ["M7_sol-Exod-043a","M7_sol-Exod-043b1","M7_sol-Exod-043b2","M7_sol-Exod-043c1","M7_sol-Exod-043c2"]
        elif relation["note_id"] == "RN-EXOD-010":
            relation["children"] = ["M7_sol-Exod-038","M7_sol-Exod-039","M7_sol-Exod-040","M7_sol-Exod-041","M7_sol-Exod-042","M7_sol-Exod-043a","M7_sol-Exod-043b1","M7_sol-Exod-043b2","M7_sol-Exod-043c1","M7_sol-Exod-043c2","M7_sol-Exod-044"]
    relations.extend([
        {"note_id":"RN-EXOD-012","parent_span":"Exod.27.1-Exod.27.21","internal_map":["Exod.27.1-19","Exod.27.20-21"],"alternate_seam":"Exod.27.20","relation":"courtyard_to_lamp_service","state":"deferred_human_or_external_ai"},
        {"note_id":"RN-EXOD-013","parent_span":"Exod.29.1-Exod.29.46","internal_map":["Exod.29.1-37","Exod.29.38-46"],"alternate_seam":"Exod.29.38","relation":"consecration_to_daily_offering_presence_close","state":"deferred_human_or_external_ai"},
        {"note_id":"RN-EXOD-014","parent_span":"Exod.30.11-Exod.30.21","children":["M7_sol-Exod-043b1","M7_sol-Exod-043b2"],"relation":"paired_sanctuary_service_provisions"},
        {"note_id":"RN-EXOD-015","parent_span":"Exod.30.22-Exod.30.38","children":["M7_sol-Exod-043c1","M7_sol-Exod-043c2"],"relation":"paired_sacred_formulations"},
        {"note_id":"RN-EXOD-016","parent_span":"Exod.31.1-Exod.31.18","internal_map":["Exod.31.1-11","Exod.31.12-17","Exod.31.18"],"relation":"instruction_corpus_close","state":"deferred_human_or_external_ai","appeal_id":"APL-R1-H-EXOD-022-01","boss_ruling_id":"R1-BR-EXOD-022"},
    ])
    with RELATIONS.open("w", encoding="utf-8", newline="\n") as handle:
        for relation in relations:
            relation.update({"schema_version":"m7_decision_relation.v1","book":"Exod","non_authorizing":True})
            handle.write(json.dumps(relation, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"wrote revision 2 with {len(result)} chunks and {len(relations)} relation notes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
