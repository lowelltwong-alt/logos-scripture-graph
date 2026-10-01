#!/usr/bin/env python3
"""Apply the appeal-checked Leviticus revision-1 docket and lineage controls."""
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
EXPECTED_FROZEN = "4847715362cc317be828a8610b1b44d58fe8b341213341b78d7a58e7e88f65fe"


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def revised(base: dict, *, decision_id: str | None = None, span: str | None = None,
            title: str | None = None, form: str | None = None,
            confidence: str | None = None, rationale: str | None = None,
            replaces: str | None = None, hold: bool = False) -> dict:
    row = copy.deepcopy(base)
    row.update({
        "decision_id": decision_id or row["decision_id"],
        "span": span or row["span"],
        "working_title": title or row["working_title"],
        "literature_type_guess": form or row["literature_type_guess"],
        "confidence": confidence or row["confidence"],
        "boundary_rationale": rationale or row["boundary_rationale"],
        "review_revision": 1,
        "review_status": "revision_1_pending_fresh_reviews",
    })
    row["boundary_evidence_refs"] = list(dict.fromkeys([
        f"direct_read:eng-web:{row['span']}",
        f"book_strategy:Lev:{row['literature_type_guess']}",
        "reviews/Lev/boss_ruling.json",
        "reviews/Lev/appeal_literary.json",
        "reviews/Lev/appeal_hebrew.json",
        "reviews/Lev/appeal_peer.json",
        "source_metadata:evidence_only",
    ]))
    row["frontier_flag_considered"] = row["confidence"] in {"low", "medium_low"}
    if replaces:
        row["lineage"] = {"revision_0_parent_ids": [replaces], "operation": "split_child"}
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
    if len(original) != 68 or len(by_id) != 68:
        raise SystemExit("expected 68 unique revision-0 Leviticus decisions")

    replacements: dict[str, list[dict]] = {
        "M7_sol-Lev-050": [
            revised(
                by_id["M7_sol-Lev-050"], decision_id="M7_sol-Lev-050a",
                span="Lev.23.1-Lev.23.3", title="Appointed-time heading and weekly Sabbath",
                form="calendar_heading_and_weekly_sabbath", confidence="medium",
                rationale="The appointed-times frame and complete weekly-Sabbath provision close before the repeated annual-calendar heading at Lev.23.4.",
                replaces="M7_sol-Lev-050"),
            revised(
                by_id["M7_sol-Lev-050"], decision_id="M7_sol-Lev-050b",
                span="Lev.23.4-Lev.23.8", title="Annual appointed-times heading, Passover, and Unleavened Bread",
                form="annual_calendar_opening_and_passover", confidence="medium",
                rationale="The repeated appointed-times heading opens the dated annual calendar and completes the Passover and Unleavened Bread observance.",
                replaces="M7_sol-Lev-050"),
        ],
        "M7_sol-Lev-052": [
            revised(
                by_id["M7_sol-Lev-052"], decision_id="M7_sol-Lev-052a",
                span="Lev.23.23-Lev.23.25", title="Seventh-month memorial convocation",
                form="seventh_month_memorial_observance", confidence="medium",
                rationale="A complete divine speech gives the seventh-month date, memorial-rest convocation, work prohibition, and offering requirement.",
                replaces="M7_sol-Lev-052"),
            revised(
                by_id["M7_sol-Lev-052"], decision_id="M7_sol-Lev-052b",
                span="Lev.23.26-Lev.23.32", title="Day of Atonement observance, sanctions, and Sabbath bounds",
                form="atonement_day_calendar_observance", confidence="medium",
                rationale="A fresh complete speech changes date and observance, adds self-affliction and sanctions, and closes with explicit all-day Sabbath bounds.",
                replaces="M7_sol-Lev-052"),
        ],
    }
    metadata_changes = {
        "M7_sol-Lev-012": {
            "title": "Reparation-offering procedure and cross-offering priestly shares",
            "confidence": "medium_low",
            "rationale": "The reparation procedure continues into a cross-offering priestly-allocation digest at Lev.7.7; an internal map preserves the real functional seam without a top-level split.",
        },
        "M7_sol-Lev-018": {"confidence": "medium"},
        "M7_sol-Lev-055": {"confidence": "medium"},
        "M7_sol-Lev-061": {"confidence": "low", "hold": True},
    }

    result: list[dict] = []
    for row in original:
        decision_id = row["decision_id"]
        if decision_id in replacements:
            result.extend(replacements[decision_id])
            continue
        if decision_id in metadata_changes:
            change = metadata_changes[decision_id]
            result.append(revised(
                row,
                title=change.get("title"),
                confidence=change.get("confidence"),
                rationale=change.get("rationale"),
                hold=change.get("hold", False),
            ))
            continue
        result.append(copy.deepcopy(row))

    if len(result) != 70:
        raise SystemExit(f"expected 70 revision-1 chunks, found {len(result)}")
    for index, row in enumerate(result, 1):
        old_index = row.get("chunk_index_in_book")
        row["chunk_index_in_book"] = index
        if row.get("review_revision") == 0 and old_index != index:
            row["index_only_change_from_revision_0"] = True
    active_ids = {row["decision_id"] for row in result}
    if {"M7_sol-Lev-050", "M7_sol-Lev-052"} & active_ids:
        raise SystemExit("retired parent IDs remain active")
    write_jsonl(CHUNKS, result)

    common = {"schema_version":"m7_decision_relation.v1","book":"Lev","non_authorizing":True}
    relations = [
        {"note_id":"RN-LEV-001","decision_ids":["M7_sol-Lev-001"],"parent_span":"Lev.1.1-Lev.1.17","internal_map":["Lev.1.1-Lev.1.2 opening address and offering frame","Lev.1.3-Lev.1.17 burnt-offering procedure"],"relation":"opening_frame_to_first_offering_manual"},
        {"note_id":"RN-LEV-002","decision_ids":["M7_sol-Lev-007","M7_sol-Lev-008","M7_sol-Lev-009","M7_sol-Lev-010","M7_sol-Lev-011"],"parent_span":"WEB Lev.6.1-Lev.6.30","versification_crosswalk":["WEB Lev.6.1-7 = MT/OSHB Lev.5.20-26","WEB Lev.6.8-30 = MT/OSHB Lev.6.1-23","systems resynchronize at Lev.7.1"],"relation":"translation_versification_metadata_not_boundary_authority"},
        {"note_id":"RN-LEV-003","decision_ids":["M7_sol-Lev-012"],"parent_span":"Lev.7.1-Lev.7.10","internal_map":["Lev.7.1-Lev.7.6 reparation-offering procedure","Lev.7.7-Lev.7.10 cross-offering priestly allocations"],"typed_links":[{"source_span":"Lev.7.7","target_decision_id":"M7_sol-Lev-011","relation":"coordinates_with_priestly_purification_offering_manual"},{"source_span":"Lev.7.8","target_decision_id":"M7_sol-Lev-008","relation":"allocates_share_from_priestly_burnt_offering_manual"},{"source_span":"Lev.7.9-Lev.7.10","target_decision_id":"M7_sol-Lev-009","relation":"allocates_shares_from_priestly_grain_offering_manual"}],"alternate_seam":"Lev.7.7","residual_dissent":"physical split remains defensible","relation":"reparation_manual_to_cross_offering_allocation_digest"},
        {"note_id":"RN-LEV-004","decision_ids":["M7_sol-Lev-017","M7_sol-Lev-018","M7_sol-Lev-019"],"parent_span":"Lev.8.1-Lev.10.7","relation":"ordination_to_inaugural_service_to_unauthorized_fire_sequence"},
        {"note_id":"RN-LEV-005","decision_ids":["M7_sol-Lev-024"],"parent_span":"Lev.11.1-Lev.11.47","internal_map":["Lev.11.46-Lev.11.47 classification summary"],"relation":"classification_corpus_summary"},
        {"note_id":"RN-LEV-006","decision_ids":["M7_sol-Lev-031","M7_sol-Lev-032","M7_sol-Lev-033"],"parent_span":"Lev.16.1-Lev.16.34","children":["M7_sol-Lev-031","M7_sol-Lev-032","M7_sol-Lev-033"],"related_passages":["Lev.10.1-Lev.10.2","Lev.23.26-Lev.23.32"],"relation":"death_framed_annual_access_and_atonement_complex"},
        {"note_id":"RN-LEV-007","decision_ids":["M7_sol-Lev-035"],"parent_span":"Lev.17.10-Lev.17.16","internal_map":["Lev.17.10-Lev.17.14 blood consumption and hunted game","Lev.17.15-Lev.17.16 carrion washing and temporary impurity"],"alternate_seam":"Lev.17.15","related_passages":["Lev.11.39-Lev.11.40"],"relation":"blood_life_speech_with_carrion_case_close"},
        {"note_id":"RN-LEV-008","decision_ids":["M7_sol-Lev-036","M7_sol-Lev-037"],"parent_span":"Lev.18.1-Lev.18.30","children":["M7_sol-Lev-036","M7_sol-Lev-037"],"relation":"inseparable_prohibition_and_land_sanction_speech"},
        {"note_id":"RN-LEV-009","decision_ids":["M7_sol-Lev-036","M7_sol-Lev-037","M7_sol-Lev-042","M7_sol-Lev-043","M7_sol-Lev-044"],"source_span":"Lev.18.1-Lev.18.30","target_span":"Lev.20.1-Lev.20.27","relation":"prohibitions_correspond_to_later_sanctions"},
        {"note_id":"RN-LEV-010","decision_ids":["M7_sol-Lev-040"],"parent_span":"Lev.19.19-Lev.19.29","internal_map":["Lev.19.19","Lev.19.20-Lev.19.22","Lev.19.23-Lev.19.25","Lev.19.26-Lev.19.29"],"relation":"mixed_holiness_instruction_subclusters"},
        {"note_id":"RN-LEV-011","decision_ids":["M7_sol-Lev-044"],"parent_span":"Lev.20.22-Lev.20.27","internal_map":["Lev.20.27 medium/wizard sanction reprise"],"relation":"separation_close_with_sanction_reprise"},
        {"note_id":"RN-LEV-012","decision_ids":["M7_sol-Lev-050a","M7_sol-Lev-050b","M7_sol-Lev-051","M7_sol-Lev-052a","M7_sol-Lev-052b","M7_sol-Lev-053"],"parent_span":"Lev.23.1-Lev.23.44","children":["M7_sol-Lev-050a","M7_sol-Lev-050b","M7_sol-Lev-051","M7_sol-Lev-052a","M7_sol-Lev-052b","M7_sol-Lev-053"],"relation":"appointed_times_calendar_corpus"},
        {"note_id":"RN-LEV-013","decision_ids":["M7_sol-Lev-052a","M7_sol-Lev-052b"],"parent_span":"Lev.23.23-Lev.23.32","children":["M7_sol-Lev-052a","M7_sol-Lev-052b"],"related_passages":["Lev.16.29-Lev.16.34"],"relation":"seventh_month_siblings_with_atonement_dependency"},
        {"note_id":"RN-LEV-014","decision_ids":["M7_sol-Lev-054"],"parent_span":"Lev.24.1-Lev.24.9","internal_map":["Lev.24.1-Lev.24.4 lamp service","Lev.24.5-Lev.24.9 bread service"],"relation":"paired_continual_sanctuary_services"},
        {"note_id":"RN-LEV-015","decision_ids":["M7_sol-Lev-056","M7_sol-Lev-057","M7_sol-Lev-058","M7_sol-Lev-059","M7_sol-Lev-060","M7_sol-Lev-061","M7_sol-Lev-062","M7_sol-Lev-063"],"parent_span":"Lev.25.1-Lev.26.46","alternate_seam":"Lev.26.3","held_decision_id":"M7_sol-Lev-061","state":"deferred_human_or_external_ai","relation":"uninterrupted_mount_sinai_speech_with_competing_blessing_seam"},
        {"note_id":"RN-LEV-016","decision_ids":["M7_sol-Lev-063","M7_sol-Lev-068"],"closures":[{"span":"Lev.26.46","function":"covenant_sanctions_and_Sinai_corpus_colophon"},{"span":"Lev.27.34","function":"book_final_colophon"}],"relation":"distinct_double_closure"},
        {"note_id":"RN-LEV-017","decision_ids":["M7_sol-Lev-064","M7_sol-Lev-065","M7_sol-Lev-066","M7_sol-Lev-067","M7_sol-Lev-068"],"parent_span":"Lev.27.1-Lev.27.34","children":["M7_sol-Lev-064","M7_sol-Lev-065","M7_sol-Lev-066","M7_sol-Lev-067","M7_sol-Lev-068"],"internal_maps":{"M7_sol-Lev-067":["Lev.27.26-Lev.27.27 firstborn exception","Lev.27.28-Lev.27.29 irrevocably devoted exception"],"M7_sol-Lev-068":["Lev.27.30-Lev.27.33 tithe rules","Lev.27.34 book-final colophon"]},"relation":"final_valuation_and_dedication_speech"},
    ]
    for relation in relations:
        relation.update(common)
    write_jsonl(RELATIONS, relations)

    lineage = [
        {"schema_version":"m7_revision_lineage.v1","book":"Lev","revision":1,"operation":"split","retired_decision_id":"M7_sol-Lev-050","retired_span":"Lev.23.1-Lev.23.8","replaced_by":["M7_sol-Lev-050a","M7_sol-Lev-050b"],"boss_proposed_ids":["M7_sol-Lev-050","M7_sol-Lev-069"],"appeal_id":"APL-P-LEV-002","fresh_reviews_required":True,"non_authorizing":True},
        {"schema_version":"m7_revision_lineage.v1","book":"Lev","revision":1,"operation":"split","retired_decision_id":"M7_sol-Lev-052","retired_span":"Lev.23.23-Lev.23.32","replaced_by":["M7_sol-Lev-052a","M7_sol-Lev-052b"],"boss_proposed_ids":["M7_sol-Lev-052","M7_sol-Lev-070"],"appeal_id":"APL-P-LEV-002","fresh_reviews_required":True,"non_authorizing":True},
        {"schema_version":"m7_revision_lineage.v1","book":"Lev","revision":1,"operation":"metadata_revision","decision_id":"M7_sol-Lev-012","appeal_id":"APL-P-LEV-001","fresh_reviews_required":True,"residual_dissent":"physical split at Lev.7.7","non_authorizing":True},
    ]
    write_jsonl(LINEAGE, lineage)
    print(f"wrote Leviticus revision 1 with {len(result)} chunks, {len(relations)} relations, and {len(lineage)} lineage rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
