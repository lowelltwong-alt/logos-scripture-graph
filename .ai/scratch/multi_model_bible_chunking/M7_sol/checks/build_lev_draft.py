#!/usr/bin/env python3
"""Build M7 Sol's independent revision-0 Leviticus candidate."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
MODEL = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol"
OUTPUT = MODEL / "book_chunks" / "Lev" / "chunks.jsonl"


# span, title, literary form, confidence, independent boundary rationale
SPECS = [
    ("Lev.1.1-Lev.1.17","Burnt offering procedure across herd, flock, and bird variants","burnt_offering_procedure","medium","The Tent-of-Meeting address and repeated offering logic govern all three material variants through the shared aroma closure."),
    ("Lev.2.1-Lev.2.16","Grain offering forms, restrictions, covenant salt, and first produce","grain_offering_procedure","medium_low","Flour, cooked, restricted, salted, and first-produce forms remain one offering-type procedure despite several internal variants."),
    ("Lev.3.1-Lev.3.17","Well-being offering procedure and fat/blood statute","well_being_offering_procedure","medium","Herd, sheep, and goat procedures share handling and disposition, culminating in the fat-and-blood statute."),
    ("Lev.4.1-Lev.4.35","Unintentional-sin purification offerings by communal status","status_graded_purification_offering","medium_low","One divine speech gives a status-graded case hierarchy for priest, congregation, ruler, and common person, each closed by atonement and forgiveness."),
    ("Lev.5.1-Lev.5.13","Specified offenses, confession, and means-based purification alternatives","offense_and_affordability_cases","medium_low","Four triggering cases lead to confession and a nested livestock, bird, or grain remedy that should remain one affordability ladder."),
    ("Lev.5.14-Lev.5.19","Holy-property trespass and unknown-command liability","reparation_offering_cases","medium_low","A new speech introduces reparation, valuation, restitution, and two liability cases sharing the same ram-based remedy."),
    ("Lev.6.1-Lev.6.7","Neighbor fraud, restitution, and reparation offering","fraud_restitution_reparation_case","low","One condition-to-restoration case crosses the MT/English versification seam and closes with priestly atonement and forgiveness."),
    ("Lev.6.8-Lev.6.13","Priestly burnt-offering handling and perpetual altar fire","priestly_burnt_offering_manual","medium","A new priest-directed speech gives the overnight procedure, ash removal, and repeated perpetual-fire closure."),
    ("Lev.6.14-Lev.6.18","Priestly handling and consumption of grain offerings","priestly_grain_offering_manual","medium","The law-of formula governs memorial burning, priestly consumption, place, and holiness-contact closure."),
    ("Lev.6.19-Lev.6.23","Priestly installation grain offering","priestly_installation_grain_offering","medium","A fresh speech frames the daily installation offering and its complete-burning rule."),
    ("Lev.6.24-Lev.6.30","Priestly handling of purification offerings","priestly_purification_offering_manual","medium","A fresh speech frames slaughter, consumption, contact, vessel, washing, and sanctuary-blood exceptions."),
    ("Lev.7.1-Lev.7.10","Reparation offering procedure and priestly shares","priestly_reparation_offering_manual","medium_low","The reparation-offering law proceeds through blood/fat handling and then coordinates priestly allocation with purification, burnt, and grain offerings."),
    ("Lev.7.11-Lev.7.21","Thanksgiving, vow, freewill, and purity rules for well-being offerings","well_being_offering_consumption_manual","medium_low","Thanksgiving and vow/freewill time limits lead into a single purity-controlled consumption framework."),
    ("Lev.7.22-Lev.7.27","Prohibition of eating fat and blood","fat_and_blood_prohibition","medium","A fresh speech states the fat and blood rules and their matching cut-off sanctions."),
    ("Lev.7.28-Lev.7.38","Priestly portions and offering-corpus colophon","priestly_portions_and_corpus_summary","medium_low","A fresh speech allocates breast and thigh, then the 7:35-38 summary closes the full offering corpus."),
    ("Lev.8.1-Lev.8.13","Assembly, washing, clothing, and anointing of Aaron and sons","ordination_installation_opening","medium_low","Command execution moves from assembly through washing, vesting, sanctuary anointing, and Aaron's anointing before the sacrificial phase."),
    ("Lev.8.14-Lev.8.36","Ordination sacrifices, blood application, meal, and seven-day charge","ordination_sacrifices_and_completion","medium_low","The purification, burnt, and installation offerings form a linked sequence completed by blood/oil application, sacred meal, and seven-day charge."),
    ("Lev.9.1-Lev.9.24","Eighth-day inaugural service and glory-fire climax","inaugural_priestly_service_narrative","medium_low","Preparatory commands, Aaron's first service, blessing, divine glory, and consuming fire form one command-execution-result movement."),
    ("Lev.10.1-Lev.10.7","Unauthorized fire, death, removal, and mourning constraints","unauthorized_fire_crisis","low","The fatal breach immediately generates interpretation, removal, and mourning restrictions for the surviving priestly household."),
    ("Lev.10.8-Lev.10.11","Priestly sobriety, distinction, and teaching mandate","priestly_distinction_teaching_charge","medium","A direct speech to Aaron gives a bounded alcohol restriction whose purpose is distinguishing and teaching."),
    ("Lev.10.12-Lev.10.20","Remaining offerings, disputed consumption, and Aaron's accepted explanation","post_crisis_offering_adjudication","medium_low","Moses' consumption instructions lead to inquiry, anger, Aaron's contextual defense, and explicit acceptance."),
    ("Lev.11.1-Lev.11.23","Land, water, bird, and winged-creature food classifications","animal_food_classification","medium_low","A joint Moses/Aaron speech classifies edible and prohibited creatures by successive domains without turning each species into a unit."),
    ("Lev.11.24-Lev.11.40","Carcass contact and transmission procedures","carcass_impurity_procedures","medium_low","Contact, carrying, vessels, seed, and edible-animal carcasses form a coherent contamination-and-cleansing procedure."),
    ("Lev.11.41-Lev.11.47","Creeping-creature prohibition, holiness rationale, and classification summary","creeping_creature_holiness_close","medium_low","The final prohibition expands into the holiness motive and the formal law-of-animals summary."),
    ("Lev.12.1-Lev.12.8","Childbirth purification periods and offering with reduced-cost alternative","childbirth_purification_procedure","medium_low","Sex-specific time periods, sanctuary restriction, full offering, and bird alternative are dependent stages of one procedure."),
    ("Lev.13.1-Lev.13.46","Bodily surface diagnosis, isolation, and public status","bodily_surface_diagnostic_manual","low","One priestly diagnostic corpus covers swellings, chronic conditions, boils, burns, scalp, spots, baldness, and the declared person's exclusion."),
    ("Lev.13.47-Lev.13.59","Garment and leather-surface diagnosis","garment_surface_diagnostic_manual","medium_low","Material inspection, quarantine, washing, destruction, and clean/unclean pronouncement form a separate non-bodily algorithm."),
    ("Lev.14.1-Lev.14.32","Restored-person cleansing and reduced-cost alternative","restored_person_cleansing_procedure","low","Outside-camp inspection, two-bird rite, seven-day transition, eighth-day offerings, and poverty alternative form one restoration sequence."),
    ("Lev.14.33-Lev.14.57","House diagnosis, cleansing, and surface-condition summary","house_surface_diagnosis_and_close","low","A fresh speech gives removal, quarantine, repair, destruction, and cleansing for houses, followed by the summary of person, garment, and house cases."),
    ("Lev.15.1-Lev.15.33","Male and female discharge cases, cleansing, sanctuary-risk rationale, and summary","bodily_discharge_procedures","low","Parallel male and female cases pair transmission and cleansing rules before a sanctuary-protection rationale and comprehensive summary."),
    ("Lev.16.1-Lev.16.10","Death-framed access warning, vesting, offerings, and two-goat selection","atonement_day_access_and_selection","low","The death notice governs restricted access; vesting, preliminary offerings, lots, and presentation establish all later ritual prerequisites."),
    ("Lev.16.11-Lev.16.28","Inner-sanctuary, altar, live-goat, exit, and disposal rites","atonement_day_ordered_rites","low","Bull and goat blood rites, sanctuary and altar purification, confession/removal, washing, offerings, and disposal form the procedural core."),
    ("Lev.16.29-Lev.16.34","Annual self-affliction, rest, and atonement statute","atonement_day_annual_statute","medium_low","The ordered rite is translated into a dated, inclusive, perpetual annual observance and closes with execution."),
    ("Lev.17.1-Lev.17.9","Slaughter and sacrifice at the Tent of Meeting","slaughter_and_sanctuary_sacrifice_law","medium_low","A fresh speech governs slaughter, blood presentation, priestly burning, illicit sacrifice, and resident-inclusive offering requirements."),
    ("Lev.17.10-Lev.17.16","Blood consumption, hunted game, and carcass handling","blood_life_and_carcass_law","low","Blood/life rationale links cut-off sanction, hunted-game draining, and carcass cleansing while retaining separate cases."),
    ("Lev.18.1-Lev.18.23","Land-and-obedience frame with prohibited sexual and cultic acts","prohibition_collection","low","Egypt/Canaan contrast and life-through-statutes frame the complete prohibition series before the land-defilement rationale."),
    ("Lev.18.24-Lev.18.30","Land defilement, expulsion, cut-off, and guarding closure","prohibition_collection_sanction_close","low","The nations/land rationale, expulsion warning, individual cut-off, and final guard interpret the preceding prohibitions as a unit."),
    ("Lev.19.1-Lev.19.10","Holiness call, family/Sabbath, worship, and gleaning","holiness_exhortation_opening","medium_low","The communal holiness address moves through foundational loyalties, acceptable worship, and harvest provision for poor and foreigner."),
    ("Lev.19.11-Lev.19.18","Neighbor-directed truth, justice, rebuke, and love","neighbor_justice_and_love_cluster","medium_low","Prohibitions against theft, deception, oppression, and partiality culminate in truthful rebuke and love of neighbor."),
    ("Lev.19.19-Lev.19.29","Mixture, pledged servant case, fruit, divination, bodily marks, and sexual exploitation","mixed_holiness_instruction_cluster","low","A statutes reset introduces heterogeneous but bounded separation and land/social instructions through the anti-exploitation warning."),
    ("Lev.19.30-Lev.19.37","Sanctuary, occult, elderly, resident foreigner, and honest measures","reverence_and_equity_close","medium_low","Sabbath/sanctuary reverence frames commands about occult consultation, age, the resident foreigner, and commercial justice before the formal close."),
    ("Lev.20.1-Lev.20.8","Molech and medium sanctions with holiness charge","idolatry_and_holiness_sanctions","medium_low","A fresh speech links Molech worship, communal responsibility, mediums, and the sanctification charge."),
    ("Lev.20.9-Lev.20.21","Family and sexual sanctions","family_and_sexual_sanction_collection","low","A continuous sanction list corresponds to earlier kinship prohibitions while distinguishing death, cut-off, liability, and childlessness outcomes."),
    ("Lev.20.22-Lev.20.27","Land, separation, clean/unclean distinction, and medium sanction close","separation_and_land_close","medium_low","Land-expulsion warning and divine separation interpret the sanctions, reconnect animal distinctions, and end with a final medium/wizard case."),
    ("Lev.21.1-Lev.21.15","Ordinary and high-priest mourning and marriage rules","priestly_status_and_family_rules","medium_low","Priest-addressed rules distinguish ordinary and high-priest mourning and marriage while preserving the shared holiness role."),
    ("Lev.21.16-Lev.21.24","Priestly physical conditions and sanctuary access","priestly_access_restrictions","medium_low","A fresh speech defines service/access limits, preserves holy-food participation, and ends with Moses' relay to all parties."),
    ("Lev.22.1-Lev.22.16","Priestly purity and household eligibility for holy food","holy_food_eligibility_rules","medium_low","A fresh speech governs priestly impurity, recovery, outsider and household eligibility, inadvertent eating, restitution, and non-profanation."),
    ("Lev.22.17-Lev.22.25","Acceptable voluntary offerings and disqualifying conditions","acceptable_animal_offering_rules","medium_low","A fresh public speech defines acceptable vows/freewill offerings and excludes specified injuries and foreign-sourced defects."),
    ("Lev.22.26-Lev.22.33","Young-animal timing, thanksgiving, obedience, and name-sanctification close","offering_holiness_close","medium_low","A fresh speech links animal timing and maternal restrictions to thanksgiving handling, obedience, and the sanctified-name motive."),
    ("Lev.23.1-Lev.23.8","Calendar frame, weekly Sabbath, Passover, and Unleavened Bread","calendar_opening_and_passover","medium_low","The appointed-times heading includes weekly Sabbath before the annual calendar opens with Passover and Unleavened Bread."),
    ("Lev.23.9-Lev.23.22","First sheaf, seven-week count, harvest feast, and gleaning","spring_harvest_calendar_procedures","low","A fresh speech coordinates first produce, counting, offerings, and a harvest-linked gleaning close."),
    ("Lev.23.23-Lev.23.32","Seventh-month memorial and Day of Atonement observance","seventh_month_memorial_and_atonement","medium_low","Two fresh speeches give adjacent seventh-month convocations; the atonement observance adds self-affliction and all-day Sabbath bounds."),
    ("Lev.23.33-Lev.23.44","Booths, feast summary, and Booths supplement","booths_and_calendar_close","low","The Booths command, 23:37-38 calendar recap, and 23:39-43 harvest/booth supplement return to one festival before Moses' final declaration."),
    ("Lev.24.1-Lev.24.9","Continual lamp and bread-of-the-presence service","lamp_and_bread_service","medium_low","Lamp oil and twelve loaves are distinct but adjacent perpetual sanctuary-maintenance provisions in one speech."),
    ("Lev.24.10-Lev.24.23","Name-blasphemy case, divine ruling, equal law, and execution","narrative_case_ruling_execution","low","Offense and custody elicit a ruling generalized through homicide/injury and equal-law clauses, then the community executes it."),
    ("Lev.25.1-Lev.25.7","Sabbath year for the land","land_sabbath_law","medium_low","The Mount Sinai speech opens with a complete six-year/seventh-year rest cycle and shared produce provision."),
    ("Lev.25.8-Lev.25.22","Jubilee proclamation, return, pricing, obedience, and provision","jubilee_proclamation_and_provision","low","Counting and trumpet proclamation lead to return, non-wronging price logic, safe dwelling, and the anticipated crop question."),
    ("Lev.25.23-Lev.25.34","Land, house, and Levitical-property redemption","property_redemption_cases","low","Divine land ownership governs kin redemption, rural and walled houses, and the special Levitical city case."),
    ("Lev.25.35-Lev.25.46","Support for impoverished kin and limits on Israelite service","impoverished_kin_and_service_law","low","Support without interest leads to Israelite labor/release and contrasts it with foreign slave acquisition and inherited service."),
    ("Lev.25.47-Lev.25.55","Redemption of an Israelite sold to a resident foreigner","foreigner_held_israelite_redemption","low","One nested kin-redemption case specifies redeemers, Jubilee-based price, service terms, release, and the divine-servant rationale."),
    ("Lev.26.1-Lev.26.13","Allegiance frame and covenant blessings","allegiance_and_blessing_discourse","medium_low","Idol/Sabbath/sanctuary allegiance introduces conditional rain, peace, victory, fruitfulness, presence, and exodus-freedom blessings."),
    ("Lev.26.14-Lev.26.39","Escalating covenant sanctions and exile","escalating_sanction_discourse","low","A refusal frame unfolds in repeated sevenfold escalations through disease, famine, beasts, sword, siege, desolation, exile, and fear."),
    ("Lev.26.40-Lev.26.46","Confession, covenant remembrance, land recovery, and Sinai colophon","confession_remembrance_and_colophon","low","Confession and humbled acceptance lead to patriarchal/land remembrance, non-rejection in exile, and a formal Sinai corpus close."),
    ("Lev.27.1-Lev.27.8","Valuation of persons with poverty adjustment","person_valuation_cases","medium_low","A new speech defines age/sex bands and priestly adjustment for someone unable to pay."),
    ("Lev.27.9-Lev.27.15","Dedicated animals and houses","animal_and_house_dedication_cases","medium_low","Animal substitution/nonredemption and priest-valued house redemption share dedication, assessment, and surcharge logic."),
    ("Lev.27.16-Lev.27.25","Inherited and purchased field valuations under Jubilee","field_valuation_cases","low","Seed-based valuation, timing, surcharge, Jubilee disposition, purchased-field return, and sanctuary-shekel close form one land-dependent schedule."),
    ("Lev.27.26-Lev.27.29","Firstborn and irrevocably devoted exceptions","firstborn_and_devoted_exceptions","low","Firstborn ownership and devoted-property/person rules limit what may be dedicated or redeemed, with acute translation pressure at 27:28-29."),
    ("Lev.27.30-Lev.27.34","Land and herd tithes with book-final Sinai colophon","tithe_rules_and_book_close","medium_low","Land and herd tithe holiness/redemption rules culminate in the comprehensive book-final Sinai command formula."),
]


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for index, (span, title, form, confidence, rationale) in enumerate(SPECS, 1):
        rows.append({
            "model_id":"M7_sol","book":"Lev","span":span,"chunk_index_in_book":index,
            "working_title":title,"literature_type_guess":form,
            "boundary_evidence_refs":[f"direct_read:eng-web:{span}",f"book_strategy:Lev:{form}","source_metadata:evidence_only"],
            "strong_or_hebrew_tags_used":["review_pending","evidence_only","not_boundary_authority"],
            "wj_or_red_letter_considered":False,"frontier_flag_considered":confidence in {"low","medium_low"},
            "confidence":confidence,"decision_id":f"M7_sol-Lev-{index:03d}","boundary_rationale":rationale,
            "review_revision":0,"review_status":"frozen_pending_blind_review","non_authorizing":True,
        })
    with OUTPUT.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"wrote {len(rows)} Leviticus revision-0 chunks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
