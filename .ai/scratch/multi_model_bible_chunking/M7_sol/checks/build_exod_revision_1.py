#!/usr/bin/env python3
"""Apply the accepted Exodus boss docket while preserving the unresolved appeal hold."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
MODEL = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol"
CHUNKS = MODEL / "book_chunks" / "Exod" / "chunks.jsonl"
RELATIONS = MODEL / "reviews" / "Exod" / "decision_relations.jsonl"
EXPECTED_FROZEN = "f12a9e58c36af30a0df05c48d944ebdc756610da71eb5abc1208633f52d58cf4"


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def revised(base: dict, *, decision_id: str, index: float | int, span: str, title: str,
            form: str, confidence: str, rationale: str, hold: bool = False) -> dict:
    row = copy.deepcopy(base)
    row.update({
        "span": span,
        "chunk_index_in_book": index,
        "working_title": title,
        "literature_type_guess": form,
        "boundary_evidence_refs": [
            f"direct_read:eng-web:{span}",
            f"book_strategy:Exod:{form}",
            "reviews/Exod/boss_ruling.json",
            "source_metadata:evidence_only",
        ],
        "confidence": confidence,
        "decision_id": decision_id,
        "boundary_rationale": rationale,
        "review_revision": 1,
        "review_status": "revision_1_pending_fresh_reviews",
        "frontier_flag_considered": confidence in {"low", "medium_low"},
    })
    if hold:
        row["candidate_hold_state"] = "deferred_human_or_external_ai"
    else:
        row.pop("candidate_hold_state", None)
    return row


def main() -> int:
    actual = hashlib.sha256(CHUNKS.read_bytes()).hexdigest()
    if actual != EXPECTED_FROZEN:
        raise SystemExit(f"expected revision-0 hash {EXPECTED_FROZEN}, found {actual}")
    original = read_jsonl(CHUNKS)
    by_id = {row["decision_id"]: row for row in original}
    replacements: dict[str, list[dict]] = {
        "M7_sol-Exod-005": [revised(
            by_id["M7_sol-Exod-005"], decision_id="M7_sol-Exod-005r1", index=5,
            span="Exod.2.23-Exod.4.17",
            title="Israel's cry, bush encounter, and complete commission-objection dialogue",
            form="affliction_and_commission_dialogue", confidence="medium_low",
            rationale="Preserves affliction, encounter, commission, Moses' answering objections, signs, and Aaron provision as one discourse ladder.")],
        "M7_sol-Exod-006": [],
        "M7_sol-Exod-007": [
            revised(by_id["M7_sol-Exod-007"], decision_id="M7_sol-Exod-007a", index=7,
                    span="Exod.4.18-Exod.4.23", title="Departure from Midian and commission for the return to Egypt",
                    form="return_journey_commission", confidence="medium",
                    rationale="Departure preparations and the firstborn warning form the opening return-journey frame."),
            revised(by_id["M7_sol-Exod-007"], decision_id="M7_sol-Exod-007b", index=7.1,
                    span="Exod.4.24-Exod.4.26", title="Lodging-place circumcision incident",
                    form="opaque_lodging_incident", confidence="low",
                    rationale="Fresh lodging/action frame and internal release closure mark a bounded but translation-sensitive incident."),
            revised(by_id["M7_sol-Exod-007"], decision_id="M7_sol-Exod-007c", index=7.2,
                    span="Exod.4.27-Exod.4.31", title="Aaron's meeting with Moses and Israel's recognition response",
                    form="reunion_and_recognition_narrative", confidence="medium",
                    rationale="New Aaron-directed speech initiates reunion, report, authentication, and Israel's response.")],
        "M7_sol-Exod-010": [
            revised(by_id["M7_sol-Exod-010"], decision_id="M7_sol-Exod-010a", index=10,
                    span="Exod.6.14-Exod.6.27", title="Genealogy identifying Moses and Aaron for the commission",
                    form="genealogical_register", confidence="medium",
                    rationale="Complete lineage register identifies the commissioned speakers before narrative resumption."),
            revised(by_id["M7_sol-Exod-010"], decision_id="M7_sol-Exod-010b", index=10.1,
                    span="Exod.6.28-Exod.7.13", title="Resumed commission and rod sign before Pharaoh",
                    form="recommission_and_sign_narrative", confidence="medium_low",
                    rationale="Resumed commission dialogue continues into the complete public rod-sign scene.")],
        "M7_sol-Exod-022": [
            revised(by_id["M7_sol-Exod-022"], decision_id="M7_sol-Exod-022a", index=22,
                    span="Exod.12.43-Exod.12.51", title="Passover participation ordinance and departure compliance",
                    form="passover_participation_ordinance", confidence="medium",
                    rationale="A complete participation rule closes with Israel's compliance and departure summary."),
            revised(by_id["M7_sol-Exod-022"], decision_id="M7_sol-Exod-022b", index=22.1,
                    span="Exod.13.1-Exod.13.16", title="Firstborn consecration, departure remembrance, and teaching signs",
                    form="firstborn_and_memorial_instruction", confidence="medium",
                    rationale="New speech frame begins a firstborn and memorial-teaching complex with repeated child-question closure.")],
        "M7_sol-Exod-043": [
            revised(by_id["M7_sol-Exod-043"], decision_id="M7_sol-Exod-043a", index=43,
                    span="Exod.30.1-Exod.30.10", title="Incense altar and annual service instruction",
                    form="incense_altar_instruction", confidence="medium",
                    rationale="Incense-altar construction and its annual service form a complete procedure."),
            revised(by_id["M7_sol-Exod-043"], decision_id="M7_sol-Exod-043b", index=43.1,
                    span="Exod.30.11-Exod.30.21", title="Census ransom and bronze basin service provisions",
                    form="sanctuary_service_provisions", confidence="medium_low",
                    rationale="Two newly framed service provisions form the middle sanctuary supplement while remaining internally indexed."),
            revised(by_id["M7_sol-Exod-043"], decision_id="M7_sol-Exod-043c", index=43.2,
                    span="Exod.30.22-Exod.30.38", title="Anointing oil and incense formulations",
                    form="sacred_formulation_instructions", confidence="medium_low",
                    rationale="Paired formulation speeches govern anointing oil and incense and close the supplement.")],
    }
    metadata: dict[str, dict] = {
        "M7_sol-Exod-019": {},
        "M7_sol-Exod-024": {"title": "Song of the Sea, prose bridge, and Miriam's responsive refrain"},
        "M7_sol-Exod-031": {"hold": True},
        "M7_sol-Exod-033": {"title": "Covenant Code threshold: heavenly speech reminder and altar directives"},
        "M7_sol-Exod-035": {"confidence": "low", "hold": True},
        "M7_sol-Exod-036": {},
        "M7_sol-Exod-037": {"confidence": "low", "hold": True},
        "M7_sol-Exod-040": {"confidence": "low", "hold": True},
        "M7_sol-Exod-041": {"title": "Priestly office authorization and garment instructions"},
        "M7_sol-Exod-042": {"confidence": "low", "hold": True},
        "M7_sol-Exod-044": {"confidence": "low", "hold": True},
        "M7_sol-Exod-047": {"title": "Second intercession, messenger response, and camp mourning"},
        "M7_sol-Exod-048": {},
        "M7_sol-Exod-050": {"confidence": "low", "hold": True},
        "M7_sol-Exod-060": {"confidence": "low", "hold": True},
    }
    result: list[dict] = []
    for row in original:
        decision_id = row["decision_id"]
        if decision_id in replacements:
            result.extend(replacements[decision_id])
            continue
        if decision_id in metadata:
            change = metadata[decision_id]
            result.append(revised(
                row, decision_id=decision_id, index=row["chunk_index_in_book"], span=row["span"],
                title=change.get("title", row["working_title"]), form=row["literature_type_guess"],
                confidence=change.get("confidence", row["confidence"]),
                rationale=change.get("title", row["boundary_rationale"]), hold=change.get("hold", False)))
            continue
        result.append(row)
    with CHUNKS.open("w", encoding="utf-8", newline="\n") as handle:
        for row in result:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")

    relations = [
        {"note_id":"RN-EXOD-001","parent_span":"Exod.2.23-Exod.4.17","internal_map":["Exod.2.23-25","Exod.3.1-22","Exod.4.1-17"],"relation":"non_severable_commission_dialogue"},
        {"note_id":"RN-EXOD-002","parent_span":"Exod.4.18-Exod.4.31","children":["M7_sol-Exod-007a","M7_sol-Exod-007b","M7_sol-Exod-007c"],"relation":"return_journey_to_recognition_sequence"},
        {"note_id":"RN-EXOD-003","parent_span":"Exod.6.14-Exod.7.13","children":["M7_sol-Exod-010a","M7_sol-Exod-010b"],"relation":"genealogical_identification_precedes_resumed_commission"},
        {"note_id":"RN-EXOD-004","parent_span":"Exod.12.43-Exod.13.16","children":["M7_sol-Exod-022a","M7_sol-Exod-022b"],"relation":"shared_departure_memorial_sequence"},
        {"note_id":"RN-EXOD-005","parent_span":"Exod.20.22-Exod.23.33","children":["M7_sol-Exod-033","M7_sol-Exod-034","M7_sol-Exod-035","M7_sol-Exod-036"],"alternate_seams":["Exod.22.31","Exod.23.1","Exod.23.10","Exod.23.14"],"relation":"covenant_code_larger_unit"},
        {"note_id":"RN-EXOD-006","parent_span":"Exod.30.1-Exod.30.38","children":["M7_sol-Exod-043a","M7_sol-Exod-043b","M7_sol-Exod-043c"],"internal_anchors":["Exod.30.11","Exod.30.17","Exod.30.22","Exod.30.34"],"relation":"sanctuary_service_supplement"},
        {"note_id":"RN-EXOD-007","parent_span":"Exod.40.1-Exod.40.38","internal_map":["Exod.40.1-16","Exod.40.17-33","Exod.40.34-38"],"relation":"book_close_command_fulfillment_climax","state":"deferred_human_or_external_ai","appeal_id":"APL-L-EXOD-007-01"},
        {"note_id":"RN-EXOD-008","parent_span":"Exod.13.17-Exod.15.21","children":["M7_sol-Exod-023","M7_sol-Exod-024"],"internal_map":["Exod.15.1-18","Exod.15.19","Exod.15.20-21"],"relation":"deliverance_narrative_to_poetic_response"},
        {"note_id":"RN-EXOD-009","parent_span":"Exod.24.1-Exod.24.18","internal_map":["Exod.24.1-11","Exod.24.12-18"],"relation":"ratification_to_instruction_transition","state":"deferred_human_or_external_ai"},
        {"note_id":"RN-EXOD-010","parent_span":"Exod.25.1-Exod.31.18","children":["M7_sol-Exod-038","M7_sol-Exod-039","M7_sol-Exod-040","M7_sol-Exod-041","M7_sol-Exod-042","M7_sol-Exod-043a","M7_sol-Exod-043b","M7_sol-Exod-043c","M7_sol-Exod-044"],"relation":"sanctuary_instruction_corpus"},
        {"note_id":"RN-EXOD-011","parent_span":"Exod.32.30-Exod.34.28","children":["M7_sol-Exod-047","M7_sol-Exod-048","M7_sol-Exod-049","M7_sol-Exod-050"],"relation":"crisis_presence_and_renewal_sequence"},
    ]
    with RELATIONS.open("w", encoding="utf-8", newline="\n") as handle:
        for row in relations:
            row.update({"schema_version":"m7_decision_relation.v1","book":"Exod","non_authorizing":True})
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"wrote revision 1 with {len(result)} chunks and {len(relations)} relation notes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
