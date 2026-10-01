#!/usr/bin/env python3
"""Replace Leviticus rows in the three T423 uncertainty sidecars."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
MODEL = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol"
CHUNKS = MODEL / "book_chunks" / "Lev" / "chunks.jsonl"
RELATIONS = MODEL / "reviews" / "Lev" / "decision_relations.jsonl"


SPECIAL = {
    "M7_sol-Lev-007": (
        "web_mt_versification_and_case_boundary",
        ["WEB:Lev.6.1-Lev.6.7=MT/OSHB:Lev.5.20-Lev.5.26", "OSHB:Lev.6.1=WEB:Lev.6.8", "resynchronization@Lev.7.1"],
        "The fraud-restoration case is complete, but WEB and MT/OSHB numbering diverge across its chapter label and can misattach Hebrew evidence.",
        "Unlabelled versification can fabricate a chapter seam or attach morphology to the wrong English verse.",
        "Hebrew versification and reparation-law specialist",
    ),
    "M7_sol-Lev-019": (
        "unauthorized_fire_narrative_scope",
        ["narrative-crisis@Lev.10.1-2", "removal-and-speech@Lev.10.3-5", "mourning-constraints@Lev.10.6-7"],
        "Death, removal, divine interpretation, and mourning constraints form one crisis movement with several scene and speech transitions.",
        "Splitting can detach death from its priestly response; retaining can bury the distinct mourning instruction.",
        "Hebrew narrative and priestly-text specialist",
    ),
    "M7_sol-Lev-026": (
        "bodily_surface_diagnostic_sequence",
        ["diagnosis@Lev.13.1-8", "reinspection@Lev.13.9-37", "public-status@Lev.13.45-46"],
        "Repeated inspection and isolation formulas contain many usable seams but jointly govern one bodily-surface diagnostic system.",
        "Modern medical labels can create false boundaries; mechanical case splitting can erase the diagnostic workflow.",
        "Hebrew purity and diagnostic-text specialist",
    ),
    "M7_sol-Lev-028": (
        "restored_person_cleansing_sequence",
        ["restoration-rite@Lev.14.1-9", "eighth-day-offerings@Lev.14.10-20", "reduced-cost@Lev.14.21-32"],
        "Reentry washing, seven-day timing, eighth-day offerings, and reduced-cost alternatives are complete phases of one restoration procedure.",
        "Phase splitting may detach alternatives from the procedure; one block may hide independently reusable rites.",
        "Hebrew ritual-sequence and purity specialist",
    ),
    "M7_sol-Lev-029": (
        "house_diagnostic_and_cleansing_sequence",
        ["house-diagnosis@Lev.14.33-47", "house-cleansing@Lev.14.48-53", "summary@Lev.14.54-57"],
        "Diagnosis, remediation, cleansing, and summary shift functions while remaining one house-surface procedure.",
        "Splitting can sever diagnosis from resolution; retaining may bury the closing classification summary.",
        "Hebrew purity and house-procedure specialist",
    ),
    "M7_sol-Lev-030": (
        "discharge_case_collection_scope",
        ["male-cases@Lev.15.1-18", "female-cases@Lev.15.19-30", "sanctuary-risk-summary@Lev.15.31-33"],
        "Male and female cases share washing, timing, offering, sanctuary-risk, and summary logic but contain strong internal case seams.",
        "Modern diagnostic assumptions can distort grouping; atomization can erase the collection-level sanctuary rationale.",
        "Hebrew purity-case and discourse specialist",
    ),
    "M7_sol-Lev-031": (
        "atonement_day_access_preparation_phase",
        ["death-frame@Lev.16.1-2", "access-and-vesting@Lev.16.3-5", "goat-selection@Lev.16.6-10"],
        "Access warning, vesting, preliminary offerings, and goat selection are distinct prerequisites that depend on the full Lev.16 rite.",
        "Standalone retrieval can detach prerequisites from execution and annual observance.",
        "Hebrew atonement-rite and discourse specialist",
    ),
    "M7_sol-Lev-032": (
        "atonement_day_ordered_rites_phase",
        ["inner-sanctuary@Lev.16.11-19", "live-goat@Lev.16.20-22", "exit-and-disposal@Lev.16.23-28"],
        "Several ordered sanctuary, altar, live-goat, washing, offering, and disposal procedures form the ritual core.",
        "Subprocedure splitting can erase order and prerequisites; retaining can obscure distinct ritual movements.",
        "Senior Hebrew ritual-sequence specialist",
    ),
    "M7_sol-Lev-033": (
        "atonement_day_annual_statute_phase",
        ["dated-statute@Lev.16.29", "inclusive-rest@Lev.16.29-31", "annual-close@Lev.16.32-34"],
        "The dated annual statute is internally complete yet depends on the rites specified earlier in Lev.16.",
        "Isolated retrieval can reduce the observance to a calendar rule detached from its ritual referent.",
        "Hebrew ritual-calendar specialist",
    ),
    "M7_sol-Lev-035": (
        "blood_life_to_carrion_case_seam",
        ["blood-and-game@Lev.17.10-14", "carrion-case@Lev.17.15-16", "relation@Lev.11.39-40"],
        "Verse 15 opens a carrion washing and temporary-impurity case, but a two-verse output child would over-fragment one resident-inclusive speech.",
        "Retaining can hide the form shift; splitting can detach a weak child from its blood/life and purity contexts.",
        "Hebrew legal-form and purity specialist",
    ),
    "M7_sol-Lev-036": (
        "prohibition_collection_and_dependent_close",
        ["frame@Lev.18.1-5", "prohibitions@Lev.18.6-23", "dependent-parent@Lev.18.1-30"],
        "The prohibition series is retrievable, but its force and land rationale are completed only by the backward-dependent 18:24-30 close.",
        "Standalone retrieval can sever prohibitions from rationale and later corresponding sanctions in Lev.20.",
        "Hebrew legal-discourse and anaphora specialist",
    ),
    "M7_sol-Lev-037": (
        "land_sanction_dependent_close",
        ["anaphora@Lev.18.24", "land-expulsion@Lev.18.25-28", "cutoff-and-guard@Lev.18.29-30"],
        "Repeated reference to these things makes this sanction close grammatically dependent despite its distinct rhetorical function.",
        "Treating it independently can obscure its antecedents; merging can hide its sanction and land function.",
        "Hebrew discourse, anaphora, and legal-form specialist",
    ),
    "M7_sol-Lev-040": (
        "heterogeneous_holiness_legal_list",
        ["mixture@Lev.19.19", "pledged-servant-case@Lev.19.20-22", "fruit-years@Lev.19.23-25", "body-and-exploitation@Lev.19.26-29"],
        "Four materially different legal and procedural subclusters share one statutes reset without a new divine-speech frame.",
        "Splitting may destroy the legal-list form; retaining may bury distinct reusable cases and procedures.",
        "Hebrew legal-list and case-law specialist",
    ),
    "M7_sol-Lev-051": (
        "first_sheaf_to_weeks_calendar_complex",
        ["first-sheaf@Lev.23.9-14", "seven-week-count@Lev.23.15-21", "gleaning-close@Lev.23.22"],
        "First sheaf, seven-week count, feast offering, and gleaning close are linked calendrically but functionally distinct.",
        "Calendar atomization can sever the count relation; one unit can bury the gleaning bridge.",
        "Hebrew festival-calendar and legal-form specialist",
    ),
    "M7_sol-Lev-053": (
        "booths_observance_and_supplement",
        ["booths-speech@Lev.23.33-36", "calendar-summary@Lev.23.37-38", "supplement@Lev.23.39-43"],
        "A complete Booths speech is followed by a calendar summary and a resumed Booths supplement before narrative closure.",
        "Splitting can detach the supplement; retaining may hide the summary/resumption architecture.",
        "Hebrew festival-calendar and discourse specialist",
    ),
    "M7_sol-Lev-057": (
        "jubilee_proclamation_pricing_and_provision",
        ["jubilee-count@Lev.25.8-12", "return-and-pricing@Lev.25.13-17", "obedience-provision@Lev.25.18-22"],
        "Jubilee proclamation, return, transaction pricing, obedience, and provision form one land-rest complex with strong subfunctions.",
        "Splitting can sever pricing ethics from Jubilee; retaining can bury the provision response.",
        "Hebrew Jubilee and legal-form specialist",
    ),
    "M7_sol-Lev-059": (
        "impoverished_kin_and_service_contrast",
        ["support@Lev.25.35-38", "Israelite-service@Lev.25.39-43", "foreign-service-contrast@Lev.25.44-46"],
        "Support, Israelite service limits, and foreign-service contrast are linked by impoverishment and exodus rationale but shift case and status.",
        "English servant/slave and foreigner labels can manufacture social boundaries or erase legal contrasts.",
        "Hebrew status-terminology and legal-case specialist",
    ),
    "M7_sol-Lev-060": (
        "resident_foreigner_redemption_case",
        ["sale-case@Lev.25.47", "redemption-calculation@Lev.25.48-52", "service-and-exodus-close@Lev.25.53-55"],
        "A complete redemption case contains calculation, treatment, release, and exodus-servitude rationale phases.",
        "Formula splitting can detach calculation from release; retaining may hide distinct procedural stages.",
        "Hebrew redemption-law and status specialist",
    ),
    "M7_sol-Lev-061a": (
        "textual_seam_but_failed_standalone_fitness",
        ["MT/OSHB-samekh@Lev.26.2", "conditional-reset@Lev.26.3", "parent@Lev.25.1-26.46", "sibling:M7_sol-Lev-061b"],
        "The 26:3 seam is strong, but the two-verse command frame is highly parent-dependent and failed both final standalone-retrieval reviews.",
        "Surfacing it alone can detach allegiance commands from blessings and sanctions; merging would erase a supported Hebrew seam.",
        "Human or independent external-AI retrieval reviewer",
    ),
    "M7_sol-Lev-062": (
        "graded_sanctions_and_obscure_lexeme",
        ["escalation@Lev.26.14-39", "קרי@Lev.26.21,23-24,27-28,40-41", "exile-close@Lev.26.34-39"],
        "Repeated escalation stages form one sanctions discourse, while the obscure קרי lexeme creates major translation pressure without deciding seams.",
        "English contrary/hostile/by-chance choices can imply false stages; excessive splitting can flatten escalation.",
        "Senior Hebrew lexicography and discourse specialist",
    ),
    "M7_sol-Lev-063": (
        "restoration_to_corpus_colophon",
        ["confession@Lev.26.40-41", "covenant-and-land@Lev.26.42-45", "corpus-colophon@Lev.26.46"],
        "Confession and covenant remembrance transition from sanctions into land recovery and the Sinai corpus colophon.",
        "Splitting can detach restoration from sanctions; merging can bury the distinct 26:46 closure.",
        "Hebrew covenant-discourse and colophon specialist",
    ),
    "M7_sol-Lev-067": (
        "firstborn_and_devoted_exceptions",
        ["firstborn@Lev.27.26-27", "חרם@Lev.27.28-29", "parent@Lev.27.1-34"],
        "Firstborn and irrevocably devoted exceptions are short, lexically difficult rules inside the final valuation speech.",
        "Unsourced ethical or historical reconstruction can distort חרם; atomization can detach exceptions from valuation rules.",
        "Hebrew valuation-law and lexicography specialist",
    ),
    "M7_sol-Lev-068": (
        "tithes_and_book_final_colophon",
        ["land-tithe@Lev.27.30-31", "herd-tithe@Lev.27.32-33", "book-colophon@Lev.27.34"],
        "Two tithe rules close with the book-final Sinai colophon, distinct from the covenant-sanctions colophon at 26:46.",
        "Merging can hide double closure; splitting a one-verse colophon can over-fragment the book ending.",
        "Hebrew legal-form and literary-closure specialist",
    ),
}


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")


def reviewer_for(row: dict) -> str:
    text = f"{row['literature_type_guess']} {row['working_title']}".lower()
    if any(word in text for word in ("diagnos", "purity", "unclean", "carcass", "discharge", "cleansing")):
        return "Biblical Hebrew purity and diagnostic-text specialist"
    if any(word in text for word in ("offering", "ritual", "priest", "sanctuary", "ordination", "atonement")):
        return "Biblical Hebrew ritual-procedure specialist"
    if any(word in text for word in ("calendar", "sabbath", "jubilee", "feast", "sheaf", "booths")):
        return "Hebrew calendar and legal-form specialist"
    if any(word in text for word in ("law", "sanction", "valuation", "redemption", "service", "prohibition")):
        return "Biblical Hebrew legal-form specialist"
    if "narrative" in text or "fire" in text:
        return "Hebrew narrative and literary-form specialist"
    return "Biblical Hebrew discourse and translation specialist"


def main() -> int:
    chunks = [row for row in read_jsonl(CHUNKS) if row.get("confidence") in {"low", "medium_low"}]
    if len(chunks) != 55:
        raise SystemExit(f"expected 55 low/medium-low Leviticus chunks, found {len(chunks)}")
    relation_ids: dict[str, list[str]] = {}
    for relation in read_jsonl(RELATIONS):
        for decision_id in relation.get("decision_ids", []):
            relation_ids.setdefault(decision_id, []).append(relation["note_id"])

    low_rows, frontier_rows, atlas_rows = [], [], []
    for row in chunks:
        decision_id = row["decision_id"]
        if decision_id in SPECIAL:
            concern, signals, why, risk, reviewer = SPECIAL[decision_id]
        else:
            concern = f"{row['literature_type_guess']}_boundary_scope"
            signals = [f"direct-read@{row['span']}", f"form@{row['literature_type_guess']}"]
            signals.extend(f"relation:{note_id}" for note_id in relation_ids.get(decision_id, [])[:2])
            why = f"{row['boundary_rationale']} Confidence remains {row['confidence']} because the span contains subordinate functions not promoted to top-level seams."
            risk = f"Splitting may sever the function named in '{row['working_title']}'; retaining may hide its subordinate transitions."
            reviewer = reviewer_for(row)
        appeal_ids = row.get("appeal_ids", [])
        appeal_status = "deferred_human_or_external_ai" if row.get("candidate_hold_state") else "specialist_review_required"
        common = {
            "model_id": "M7_sol", "book": "Lev", "span": row["span"],
            "chunk_decision_id": decision_id, "confidence": row["confidence"],
            "concern_type": concern, "observed_substrate_signals": signals,
            "why_low_confidence": why, "possible_downstream_risk": risk,
            "suggested_reviewer": reviewer, "appeal_status": appeal_status,
            "appeal_ids": appeal_ids, "non_authorizing": True,
        }
        if decision_id == "M7_sol-Lev-061a":
            common.update({
                "required_parent_span": "Lev.25.1-Lev.26.46",
                "required_sibling_decision_id": "M7_sol-Lev-061b",
                "standalone_retrieval_state": "withheld_pending_human_or_external_ai",
                "human_question": "Should Lev.26.1-2 surface only with mandatory parent/sibling hydration, or remain an internal boundary never surfaced standalone?",
            })
        low_rows.append({
            key: value for key, value in common.items()
            if key not in {"concern_type", "suggested_reviewer"}
        } | {"competing_boundary_risk": risk})
        frontier_rows.append(common | {
            "why_frontier_review_needed": why,
            "disposition": appeal_status,
            "promotion_authority": "none",
        })
        atlas_rows.append(common | {
            "proposed_atlas_action": "consider_only",
            "atlas_promotion_authority": "none",
        })

    for filename, new_rows in (
        ("low_confidence_register.jsonl", low_rows),
        ("frontier_escalation_queue.jsonl", frontier_rows),
        ("atlas_candidate_feed.jsonl", atlas_rows),
    ):
        path = MODEL / filename
        preserved = [row for row in read_jsonl(path) if row.get("book") != "Lev"]
        write_jsonl(path, preserved + new_rows)
    print("wrote 55 passage-specific Leviticus rows to each uncertainty sidecar")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
