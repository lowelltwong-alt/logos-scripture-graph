#!/usr/bin/env python3
"""Replace Exodus rows in the three T423 uncertainty sidecars."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
MODEL = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol"
CHUNKS = MODEL / "book_chunks" / "Exod" / "chunks.jsonl"


DETAILS = {
    "M7_sol-Exod-005r1": ("commission_dialogue_scope", ["elapsed-time@Exod.2.23","scene@Exod.3.1","speech-ladder@Exod.3.4-Exod.4.17"], "The cry notice, bush encounter, commission, objections, signs, and Aaron provision form one escalating dialogue, but 3:1 and 4:1 are plausible retrieval seams.", "Splitting by scene can detach Moses' objections from their answers; merging can bury the call encounter.", "Biblical Hebrew discourse and commissioning-narrative specialist"),
    "M7_sol-Exod-007b": ("opaque_circumcision_incident", ["lodging-scene@Exod.4.24","ambiguous-pronouns@Exod.4.24-26","blood-bridegroom-idiom@Exod.4.25-26"], "Compressed Hebrew participants, pronominal referents, and the bridegroom-of-blood expression make both the incident's meaning and its link to the journey unusually translation-sensitive.", "English renderings may falsely resolve the actor or detach the episode from the firstborn/journey frame.", "Senior Biblical Hebrew syntax, ancient rite, and narrative-context specialist"),
    "M7_sol-Exod-009": ("renewed_commission_and_objection", ["divine-speech@Exod.6.2","identity-formula@Exod.6.2-8","objection@Exod.6.12"], "The identity-and-promise speech closes at 6:8, yet Israel's non-hearing and Moses' renewed objection complete its failed-reception movement through 6:13.", "A seam at 6:9 or 6:10 may improve retrieval but sever speech from response.", "Hebrew speech-discourse and translation specialist"),
    "M7_sol-Exod-010b": ("recommission_to_public_sign", ["resumption@Exod.6.28","new-command@Exod.7.8","sign-closure@Exod.7.13"], "The resumed commission and Pharaoh-facing rod sign are causally joined, but 7:8 begins a separately framed sign procedure.", "Over-merging obscures the sign scene; splitting can detach authorization from performance.", "Hebrew narrative and sign-procedure specialist"),
    "M7_sol-Exod-019": ("darkness_to_final_plague_bridge", ["plague-command@Exod.10.21","pharaoh-dialogue@Exod.10.24-29","new-speech@Exod.11.1"], "The darkness confrontation flows into Moses' final-plague announcement, while 11:1 presents a formal transition whose chronology is rendered differently across translations.", "A chapter seam can misorder or isolate the final announcement; a merge can flatten the ninth/tenth-plague distinction.", "Hebrew narrative chronology and plague-cycle specialist"),
    "M7_sol-Exod-020": ("passover_instruction_complex", ["speech@Exod.12.1","calendar-and-lamb@Exod.12.2-13","unleavened-bread@Exod.12.14-20","elders-response@Exod.12.21-28"], "Calendar, lamb, blood-sign, festival, and household instruction culminate in Moses' relay and Israel's response, but contain multiple procedural subunits.", "Atomizing rules loses the first-Passover sequence; one large chunk may hide reusable festival instructions.", "Hebrew ritual-procedure and legal-form specialist"),
    "M7_sol-Exod-024": ("song_prose_refrain_boundary", ["song-opening@Exod.15.1","poetic-lines@Exod.15.1-18","prose-bridge@Exod.15.19","Miriam-refrain@Exod.15.20-21"], "The victory poem, prose bridge, and Miriam's responsive refrain form one performative response, but shifts in voice, lineation, and prose create real child-unit pressure.", "English poetic formatting may dictate false seams or erase the response relation to the sea narrative.", "Biblical Hebrew poetry, performance, and translation specialist"),
    "M7_sol-Exod-026": ("manna_test_and_memorial", ["complaint@Exod.16.2","food-speech@Exod.16.4","Sabbath-test@Exod.16.22","naming@Exod.16.31","memorial@Exod.16.32-36"], "Complaint, quail/manna provision, Sabbath test, naming, and memorial are one etiological sequence with several complete internal episodes.", "Splitting can lose the test-to-Sabbath arc; merging may bury the memorial procedure.", "Wilderness narrative and legal-etiology specialist"),
    "M7_sol-Exod-031": ("sinai_arrival_to_theophany", ["arrival@Exod.19.1","covenant-speech@Exod.19.3","preparation@Exod.19.10","theophany@Exod.19.16","bounds-dialogue@Exod.19.21-25"], "Arrival, covenant address, preparation, theophany, and renewed bounds are sequentially dependent but distinguishable discourse and scene units.", "A flat parent hides major forms; premature splits detach preparation from theophany.", "Senior Hebrew discourse, theophany, and covenant-narrative specialist"),
    "M7_sol-Exod-032": ("decalogue_and_fear_response", ["divine-address@Exod.20.1","command-series@Exod.20.2-17","fear-response@Exod.20.18-21"], "The divine covenant address is followed by the people's fear and Moses' interpretive reply; the response frames reception but is narratively distinct.", "Separating 20:18-21 may hide reception; merging may impair Decalogue retrieval.", "Hebrew legal-speech and covenant-form specialist"),
    "M7_sol-Exod-034": ("casuistic_law_cluster", ["heading@Exod.21.1","conditional-laws@Exod.21.2-Exod.22.17","topic-shifts@Exod.21.12;Exod.21.28;Exod.22.1"], "Casuistic formulations link laws on servants, violence, livestock, and property, while topic and formula shifts permit several defensible clusters.", "Verse-level splitting destroys case-law form; one block can make distinct legal clusters hard to retrieve.", "Biblical Hebrew legal-form and ancient law-collection specialist"),
    "M7_sol-Exod-035": ("apodictic_to_calendar_collection", ["apodictic-shift@Exod.22.18","judicial-shift@Exod.23.1","sabbatical-shift@Exod.23.10","festival-shift@Exod.23.14"], "Social, judicial, sabbatical, and festival directives share a covenant-code speech frame but have strong internal seams, especially 23:10 and 23:14.", "A single retrieval unit may flatten legal forms; subdivision may sever the collection's rhetoric and land/Sabbath links.", "Hebrew legal collections and festival-calendar specialist"),
    "M7_sol-Exod-037": ("ratification_to_ascent_transition", ["summons@Exod.24.1","blood-rite@Exod.24.3-8","communal-ascent@Exod.24.9-11","new-ascent-speech@Exod.24.12","cloud@Exod.24.15-18"], "Ratification, communal vision, and Moses' ascent lead from covenant closure into sanctuary instruction; 24:12 is a strong but transitional seam.", "Splitting may erase the hinge into chapters 25-31; merging may bury the completed ratification scene.", "Hebrew covenant-ritual and narrative-transition specialist"),
    "M7_sol-Exod-038": ("offering_and_furniture_instruction", ["offering-speech@Exod.25.1","ark@Exod.25.10","table@Exod.25.23","lampstand@Exod.25.31"], "The offering purpose frames three furniture procedures, each independently introduced and internally complete.", "Object-level splitting risks technical fragmentation; merging makes individual procedures harder to retrieve.", "Tabernacle procedure and Hebrew discourse specialist"),
    "M7_sol-Exod-039": ("tabernacle_structure_procedures", ["curtains@Exod.26.1","tent-covering@Exod.26.7","frames@Exod.26.15","veil@Exod.26.31","entrance@Exod.26.36"], "Curtains, coverings, frames, veil, and entrance are distinct construction procedures that jointly specify one structure.", "Too many object chunks lose architectural dependency; one chapter-sized unit hides procedural closures.", "Ancient construction-procedure and Hebrew technical-text specialist"),
    "M7_sol-Exod-040": ("court_to_lamp_service", ["altar@Exod.27.1","court@Exod.27.9","fresh-speech@Exod.27.20"], "Altar and court specifications cohere architecturally, while 27:20 begins a distinct lamp-oil service procedure that also bridges to priestly material.", "Retaining the parent may obscure 27:20-21; splitting it may detach the bridge from its exterior-service context.", "Hebrew procedure-form and sanctuary-architecture specialist"),
    "M7_sol-Exod-041": ("priestly_office_and_garments", ["Aaron-selection@Exod.28.1","garment-list@Exod.28.4","ephod@Exod.28.6","breastpiece@Exod.28.15","other-garments@Exod.28.31-43"], "Authorization and multiple garment procedures share priestly consecration purpose but have strong object-level subdivisions.", "Fragmentation loses office/garment function; chapter-level grouping can bury distinct symbolic and construction forms.", "Priestly-text, Hebrew technical vocabulary, and material-culture specialist"),
    "M7_sol-Exod-042": ("consecration_to_daily_offering", ["consecration@Exod.29.1","seven-day-close@Exod.29.35-37","daily-offering@Exod.29.38","presence-close@Exod.29.42-46"], "The daily offering and meeting-place promise close the consecration complex, yet 29:38 opens an independently reusable perpetual procedure.", "A parent chunk may hide the daily offering; splitting can weaken the consecration-to-presence culmination.", "Priestly ritual-sequence and Hebrew discourse specialist"),
    "M7_sol-Exod-044": ("instruction_corpus_close_dispute", ["artisan-speech@Exod.31.1","new-Sabbath-speech@Exod.31.12","narrative-handoff@Exod.31.18","appeal:APL-R1-H-EXOD-022-01"], "Artisan commission, Sabbath sign, and tablet handoff collectively close the instruction corpus, but Hebrew marks a new speech at 31:12 and discourse-to-narrative transition at 31:18.", "The flat parent may hide three forms; a three-way split may isolate a one-verse hinge and weaken corpus closure.", "Human or external-AI Hebrew discourse and literary-architecture reviewer"),
    "M7_sol-Exod-045": ("calf_crisis_and_first_intercession", ["calf-scene@Exod.32.1","divine-notice@Exod.32.7","intercession@Exod.32.11-14"], "The calf construction triggers divine notice and Moses' first intercession, but the heavenly dialogue is a distinct embedded form.", "Splitting detaches plea from crisis; merging may obscure a key intercession unit.", "Hebrew narrative and intercession-speech specialist"),
    "M7_sol-Exod-046": ("descent_judgment_and_levite_action", ["descent@Exod.32.15","tablet-breaking@Exod.32.19","Aaron-inquiry@Exod.32.21","Levite-action@Exod.32.25"], "Descent, destruction of the calf, Aaron's inquiry, and Levite violence form the earthly crisis response but shift repeatedly in scene and speech.", "Over-splitting severs causal judgment; merging can obscure ethically and literarily distinct episodes.", "Hebrew narrative, dialogue, and violence-text specialist"),
    "M7_sol-Exod-047": ("second_intercession_to_mourning", ["second-plea@Exod.32.30","reply@Exod.32.33","messenger-speech@Exod.33.1","mourning@Exod.33.4"], "Moses' second plea elicits a messenger/presence crisis and the camp's mourning across a chapter boundary.", "A chapter split severs response from petition; a merge can conceal the new departure speech.", "Hebrew intercession and cross-chapter narrative specialist"),
    "M7_sol-Exod-048": ("tent_frame_and_presence_dialogue", ["tent-custom@Exod.33.7-11","new-plea@Exod.33.12","glory-request@Exod.33.18","response@Exod.33.19-23"], "The tent-of-meeting custom establishes relational context for the presence/glory dialogue, yet prose frame and direct speech are separable forms.", "Splitting may lose setup; merging may bury a translation-sensitive divine self-declaration.", "Senior Hebrew dialogue, divine-presence language, and translation specialist"),
    "M7_sol-Exod-049": ("new_tablets_name_and_appeal", ["tablet-command@Exod.34.1","descent@Exod.34.5","name-proclamation@Exod.34.6-7","appeal@Exod.34.8-9"], "Preparation, divine name proclamation, and Moses' appeal form one encounter, but 34:6-7 is a dense poetic/proclamatory unit widely echoed elsewhere.", "Isolating the formula can detach narrative response; merging can hide its formal closure and translation pressure.", "Hebrew proclamation, intertext, and translation specialist"),
    "M7_sol-Exod-050": ("renewal_stipulations_and_inscription", ["covenant-speech@Exod.34.10","cultic-series@Exod.34.11-26","writing-command@Exod.34.27","forty-days@Exod.34.28"], "Renewal promise, cultic stipulations, writing command, and inscription notice cohere but differ in speech function and possible source-form boundaries.", "A large unit may flatten forms; a split may obscure covenant-renewal closure.", "Hebrew covenant-form and legal-collection specialist"),
    "M7_sol-Exod-052": ("Sabbath_to_willing_offerings", ["assembly@Exod.35.1","Sabbath@Exod.35.2-3","contribution-call@Exod.35.4","response@Exod.35.20-29"], "The Sabbath frame introduces the execution corpus, while the contribution call and willing response form a separate command-fulfillment movement.", "Merging may hide 35:4 as a seam; splitting can erase the corpus-opening Sabbath frame.", "Hebrew assembly discourse and command-fulfillment specialist"),
    "M7_sol-Exod-054": ("tabernacle_structure_execution", ["curtains@Exod.36.8","coverings@Exod.36.14","frames@Exod.36.20","veil@Exod.36.35","screen@Exod.36.37"], "Several completed construction procedures collectively realize the single tabernacle structure and mirror Exodus 26.", "Object-level atomization loses instruction/execution architecture; one unit hides completed work stages.", "Technical procedure and instruction-execution parallel specialist"),
    "M7_sol-Exod-055": ("furniture_and_compounds_execution", ["ark@Exod.37.1","table@Exod.37.10","lampstand@Exod.37.17","altar@Exod.37.25","oil-incense@Exod.37.29"], "Multiple objects and sacred compounds mirror several instruction units but are linked as Bezalel's interior-furnishing work.", "A chapter unit may be too broad for retrieval; mirroring every instruction boundary may over-fragment execution.", "Tabernacle technical-text and literary-parallel specialist"),
    "M7_sol-Exod-056": ("exterior_execution_cluster", ["altar@Exod.38.1","basin@Exod.38.8","court@Exod.38.9"], "Altar, basin, and court are distinct completed objects linked by exterior sanctuary function.", "One unit may bury the basin notice; separate chunks may lose spatial/procedural cohesion.", "Ancient material-culture and Hebrew procedure specialist"),
    "M7_sol-Exod-058": ("priestly_garment_execution", ["service-cloths@Exod.39.1","ephod@Exod.39.2","breastpiece@Exod.39.8","other-garments@Exod.39.22-31"], "Garment procedures mirror Exodus 28 and repeatedly close with command-fulfillment formulas, creating both corpus and object-level boundaries.", "Mechanical formula splitting over-fragments; chapter grouping can hide coherent garment procedures.", "Priestly garment, technical Hebrew, and instruction-execution specialist"),
    "M7_sol-Exod-060": ("book_close_command_execution_glory", ["installation-command@Exod.40.1-16","dated-execution@Exod.40.17","work-close@Exod.40.33","glory-epilogue@Exod.40.34-38","appeal:APL-L-EXOD-007-01"], "Installation command, dated execution, work completion, glory filling, and travel epilogue create a strong parent close with three defensible retrieval children.", "A flat close hides command/fulfillment/climax forms; a three-way split may weaken the designed book-ending culmination.", "Human or external-AI literary-form and Hebrew narrative reviewer"),
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


def main() -> int:
    chunks = [row for row in read_jsonl(CHUNKS) if row.get("confidence") in {"low", "medium_low"}]
    missing = [row["decision_id"] for row in chunks if row["decision_id"] not in DETAILS]
    extra = sorted(set(DETAILS) - {row["decision_id"] for row in chunks})
    if missing or extra:
        raise SystemExit(f"sidecar detail mismatch missing={missing} extra={extra}")
    low_rows, frontier_rows, atlas_rows = [], [], []
    for row in chunks:
        decision_id = row["decision_id"]
        concern, signals, why, risk, reviewer = DETAILS[decision_id]
        low_rows.append({
            "model_id":"M7_sol","book":"Exod","span":row["span"],"chunk_decision_id":decision_id,
            "confidence":row["confidence"],"why_low_confidence":why,"observed_substrate_signals":signals,
            "appeal_status":"deferred_human_or_external_ai" if row.get("candidate_hold_state") else "specialist_review_required",
            "competing_boundary_risk":risk,"non_authorizing":True,
        })
        frontier_rows.append({
            "model_id":"M7_sol","book":"Exod","span":row["span"],"chunk_decision_id":decision_id,
            "concern_type":concern,"observed_substrate_signals":signals,"why_frontier_review_needed":why,
            "suggested_reviewer":reviewer,"disposition":"specialist_review_required","promotion_authority":"none",
            "possible_downstream_risk":risk,"non_authorizing":True,
        })
        atlas_rows.append({
            "model_id":"M7_sol","book":"Exod","span":row["span"],"chunk_decision_id":decision_id,
            "confidence":row["confidence"],"concern_type":concern,"observed_substrate_signals":signals,
            "why_low_confidence":why,"possible_downstream_risk":risk,"suggested_reviewer":reviewer,
            "proposed_atlas_action":"consider_only","atlas_promotion_authority":"none","non_authorizing":True,
        })
    for filename, new_rows in (
        ("low_confidence_register.jsonl", low_rows),
        ("frontier_escalation_queue.jsonl", frontier_rows),
        ("atlas_candidate_feed.jsonl", atlas_rows),
    ):
        path = MODEL / filename
        preserved = [row for row in read_jsonl(path) if row.get("book") != "Exod"]
        write_jsonl(path, preserved + new_rows)
    print(f"wrote {len(chunks)} passage-specific Exodus rows to each uncertainty sidecar")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
