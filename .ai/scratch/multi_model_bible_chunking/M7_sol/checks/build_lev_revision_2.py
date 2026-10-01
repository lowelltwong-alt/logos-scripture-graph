#!/usr/bin/env python3
"""Apply Leviticus' second and final automatic material rewrite."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
MODEL = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol"
CHUNKS = MODEL / "book_chunks" / "Lev" / "chunks.jsonl"
RELATIONS = MODEL / "reviews" / "Lev" / "decision_relations.jsonl"
LINEAGE = MODEL / "reviews" / "Lev" / "revision_lineage.jsonl"
EXPECTED_FROZEN = "6288ae5c332e97de6fb499de30891bcc18a34bf556de139a84c19782d9ed7e67"


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def child(base: dict, *, decision_id: str, span: str, title: str,
          form: str, confidence: str, rationale: str, held: bool = False) -> dict:
    row = copy.deepcopy(base)
    row.update({
        "decision_id": decision_id,
        "span": span,
        "working_title": title,
        "literature_type_guess": form,
        "confidence": confidence,
        "boundary_rationale": rationale,
        "review_revision": 2,
        "review_status": "revision_2_final_cycle_pending_fresh_child_reviews",
        "frontier_flag_considered": confidence in {"low", "medium_low"},
        "lineage": {"revision_1_parent_ids": [base["decision_id"]], "operation": "split_child"},
    })
    row["boundary_evidence_refs"] = [
        f"direct_read:eng-web:{span}",
        f"book_strategy:Lev:{form}",
        "reviews/Lev/primary_r1_hebrew.json",
        "reviews/Lev/primary_r1_literary.json",
        "reviews/Lev/peer_r1_crosscheck.json",
        "reviews/Lev/premortem_r1.json",
        "reviews/Lev/boss_r1_ruling.json",
        "reviews/Lev/appeal_round_2_peer.json",
        "source_metadata:evidence_only",
    ]
    if held:
        row["candidate_hold_state"] = "deferred_human_or_external_ai"
        row["active_appeal_id"] = "APL-R1-P-LEV-061-01"
    else:
        row.pop("candidate_hold_state", None)
        row.pop("active_appeal_id", None)
    return row


def main() -> int:
    actual = hashlib.sha256(CHUNKS.read_bytes()).hexdigest()
    if actual != EXPECTED_FROZEN:
        raise SystemExit(f"expected revision-1 hash {EXPECTED_FROZEN}, found {actual}")
    original = read_jsonl(CHUNKS)
    result: list[dict] = []
    fresh_supported = {
        "M7_sol-Lev-018", "M7_sol-Lev-050a", "M7_sol-Lev-050b",
        "M7_sol-Lev-052a", "M7_sol-Lev-052b", "M7_sol-Lev-055",
    }
    for row in original:
        decision_id = row["decision_id"]
        if decision_id == "M7_sol-Lev-012":
            result.extend([
                child(row, decision_id="M7_sol-Lev-012a", span="Lev.7.1-Lev.7.6",
                      title="Reparation-offering procedure", form="reparation_offering_procedure",
                      confidence="medium_high",
                      rationale="The reparation-offering manual completes slaughter, blood, fat, altar handling, priestly consumption, and most-holy status before the comparative allocation digest."),
                child(row, decision_id="M7_sol-Lev-012b", span="Lev.7.7-Lev.7.10",
                      title="Cross-offering priestly allocations", form="comparative_priestly_allocation_digest",
                      confidence="medium",
                      rationale="The comparative formula opens a coherent allocation digest spanning purification, reparation, burnt, and grain offerings, while parent and typed relations preserve its backward linkage."),
            ])
            continue
        if decision_id == "M7_sol-Lev-061":
            result.extend([
                child(row, decision_id="M7_sol-Lev-061a", span="Lev.26.1-Lev.26.2",
                      title="Idol, Sabbath, and sanctuary commands", form="allegiance_command_frame",
                      confidence="low",
                      rationale="A compact apodictic frame closes with divine self-identification and an MT/OSHB section marker before the conditional blessing syntax.", held=True),
                child(row, decision_id="M7_sol-Lev-061b", span="Lev.26.3-Lev.26.13",
                      title="Conditional obedience and promised blessings", form="conditional_blessing_discourse",
                      confidence="high",
                      rationale="The explicit conditional protasis opens a coherent blessing sequence that closes with divine presence, exodus liberation, broken yoke bars, and upright walking."),
            ])
            continue
        row = copy.deepcopy(row)
        if decision_id in fresh_supported:
            row["review_status"] = "revision_1_fresh_reviews_supported"
        result.append(row)

    if len(result) != 72:
        raise SystemExit(f"expected 72 revision-2 chunks, found {len(result)}")
    for index, row in enumerate(result, 1):
        old_index = row.get("chunk_index_in_book")
        row["chunk_index_in_book"] = index
        if row.get("review_revision") in {0, 1} and old_index != index:
            row["index_only_change_from_prior_revision"] = True
    active_ids = {row["decision_id"] for row in result}
    if {"M7_sol-Lev-012", "M7_sol-Lev-061"} & active_ids:
        raise SystemExit("retired revision-1 parents remain active")
    write_jsonl(CHUNKS, result)

    relations = read_jsonl(RELATIONS)
    for relation in relations:
        if relation["note_id"] == "RN-LEV-003":
            relation.update({
                "decision_ids": ["M7_sol-Lev-012a", "M7_sol-Lev-012b"],
                "children": ["M7_sol-Lev-012a", "M7_sol-Lev-012b"],
                "typed_links": [
                    {"source_decision_id":"M7_sol-Lev-012b","source_span":"Lev.7.7","target_decision_id":"M7_sol-Lev-011","relation":"coordinates_with_priestly_purification_offering_manual"},
                    {"source_decision_id":"M7_sol-Lev-012b","source_span":"Lev.7.8","target_decision_id":"M7_sol-Lev-008","relation":"allocates_share_from_priestly_burnt_offering_manual"},
                    {"source_decision_id":"M7_sol-Lev-012b","source_span":"Lev.7.9-Lev.7.10","target_decision_id":"M7_sol-Lev-009","relation":"allocates_shares_from_priestly_grain_offering_manual"},
                    {"source_decision_id":"M7_sol-Lev-012a","target_decision_id":"M7_sol-Lev-012b","relation":"procedure_to_comparative_allocation_digest"},
                ],
                "residual_dissent": "Retaining Lev.7.1-Lev.7.10 remains defensible because Lev.7.7 deliberately links the offerings and lacks an MT/OSHB section break.",
                "relation": "reparation_procedure_to_cross_offering_allocation_digest",
            })
            relation.pop("internal_map", None)
            relation.pop("alternate_seam", None)
        elif relation["note_id"] == "RN-LEV-015":
            relation.update({
                "decision_ids": ["M7_sol-Lev-056","M7_sol-Lev-057","M7_sol-Lev-058","M7_sol-Lev-059","M7_sol-Lev-060","M7_sol-Lev-061a","M7_sol-Lev-061b","M7_sol-Lev-062","M7_sol-Lev-063"],
                "children": ["M7_sol-Lev-056","M7_sol-Lev-057","M7_sol-Lev-058","M7_sol-Lev-059","M7_sol-Lev-060","M7_sol-Lev-061a","M7_sol-Lev-061b","M7_sol-Lev-062","M7_sol-Lev-063"],
                "held_decision_id": "M7_sol-Lev-061a",
                "active_appeal_id": "APL-R1-P-LEV-061-01",
                "typed_links": [
                    {"source_decision_id":"M7_sol-Lev-061a","target_spans":["Lev.19.4","Lev.19.30"],"relation":"allegiance_command_parallel"},
                    {"source_decision_id":"M7_sol-Lev-061a","target_decision_id":"M7_sol-Lev-061b","relation":"allegiance_frame_to_conditional_blessing"},
                    {"source_decision_id":"M7_sol-Lev-061b","target_decision_ids":["M7_sol-Lev-062","M7_sol-Lev-063"],"relation":"blessing_to_sanctions_and_restoration"},
                    {"source_decision_id":"M7_sol-Lev-061b","target_spans":["Lev.25.38","Lev.25.42","Lev.25.55"],"relation":"exodus_servitude_refrain"},
                ],
                "state": "deferred_human_or_external_ai",
                "relation": "mount_sinai_speech_with_held_short_allegiance_child",
            })
            relation.pop("alternate_seam", None)
    relations.append({
        "schema_version":"m7_decision_relation.v1","book":"Lev","non_authorizing":True,
        "note_id":"RN-LEV-018","decision_ids":[f"M7_sol-Lev-{index:03d}" for index in range(1, 12)] + ["M7_sol-Lev-012a","M7_sol-Lev-012b","M7_sol-Lev-013","M7_sol-Lev-014","M7_sol-Lev-015","M7_sol-Lev-016"],
        "parent_span":"Lev.1.1-Lev.7.38","relation":"offering_instruction_corpus"
    })
    write_jsonl(RELATIONS, relations)

    lineage = read_jsonl(LINEAGE)
    lineage.extend([
        {"schema_version":"m7_revision_lineage.v1","book":"Lev","revision":2,"operation":"split","retired_decision_id":"M7_sol-Lev-012","retired_span":"Lev.7.1-Lev.7.10","replaced_by":["M7_sol-Lev-012a","M7_sol-Lev-012b"],"boss_attempt_id":"lev-r1-boss-sol-20260721-p2","fresh_reviews_required":True,"residual_retain_position_preserved":True,"non_authorizing":True},
        {"schema_version":"m7_revision_lineage.v1","book":"Lev","revision":2,"operation":"split","retired_decision_id":"M7_sol-Lev-061","retired_span":"Lev.26.1-Lev.26.13","replaced_by":["M7_sol-Lev-061a","M7_sol-Lev-061b"],"boss_attempt_id":"lev-r1-boss-sol-20260721-p2","fresh_reviews_required":True,"active_appeal_id":"APL-R1-P-LEV-061-01","non_authorizing":True},
    ])
    write_jsonl(LINEAGE, lineage)
    print(f"wrote Leviticus revision 2 with {len(result)} chunks, {len(relations)} relations, and {len(lineage)} lineage rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
