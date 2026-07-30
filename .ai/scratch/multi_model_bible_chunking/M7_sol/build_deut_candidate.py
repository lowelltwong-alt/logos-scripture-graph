import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "book_chunks" / "Deut" / "chunks.jsonl"

ROWS = [
    ("1.1","1.5","Second-law book and speech frame","discourse_superscription"),
    ("1.6","1.18","Horeb departure and appointment of judges","retrospective_address"),
    ("1.19","1.46","Kadesh rebellion and judgment","retrospective_rebellion_narrative"),
    ("2.1","2.23","Wilderness passage around Seir Moab and Ammon","retrospective_journey_narrative"),
    ("2.24","3.11","Sihon and Og conquest diptych","conquest_recollection"),
    ("3.12","3.22","East-Jordan allotment duty and Joshua charge","allotment_and_commission_address"),
    ("3.23","3.29","Moses petition denied","petition_and_divine_response"),
    ("4.1","4.8","Call to heed the statutes","covenant_exhortation"),
    ("4.9","4.31","Horeb memory no-form warning and exile-return appeal","covenant_warning"),
    ("4.32","4.40","Appeal from divine uniqueness","rhetorical_exhortation"),
    ("4.41","4.43","East-Jordan refuge-city notice","administrative_notice"),
    ("4.44","5.5","Second discourse heading and Horeb assembly frame","discourse_heading_and_scene_frame"),
    ("5.6","5.21","Decalogue recitation","covenant_command_recitation"),
    ("5.22","5.33","Assembly response mediation and obedience appeal","mediation_recollection"),
    ("6.1","6.9","Command heading Shema and household transmission","covenant_instruction"),
    ("6.10","6.19","Prosperity warning Massah and obedience","covenant_warning"),
    ("6.20","6.25","Child catechesis of exodus and command","catechetical_instruction"),
    ("7.1","7.11","Holy people election and covenant fidelity","identity_and_conquest_exhortation"),
    ("7.12","7.26","Blessing conquest and anti-idolatry appeal","covenant_blessing_exhortation"),
    ("8.1","8.10","Wilderness discipline and the good land","memory_exhortation"),
    ("8.11","8.20","Warning against prosperous forgetfulness","covenant_warning"),
    ("9.1","9.6","Conquest is not by Israel's righteousness","corrective_exhortation"),
    ("9.7","10.11","Rebellion intercession renewed tablets and resumed journey","retrospective_intercession_cycle"),
    ("10.12","11.7","And now Israel covenant demand and eyewitness appeal","covenant_demand"),
    ("11.8","11.25","Land rain obedience and transmitted words","land_obedience_exhortation"),
    ("11.26","11.32","Blessing curse and Gerizim-Ebal prospect","covenant_choice_announcement"),
    ("12.1","12.28","Chosen-place worship slaughter blood and holy gifts","central_worship_code"),
    ("12.29","13.5","Anti-imitation command integrity and prophet test","apostasy_warning_and_case_law"),
    ("13.6","13.11","Intimate enticer case","apostasy_case_law"),
    ("13.12","13.18","Apostate city case","apostasy_case_law"),
    ("14.1","14.21","Holy identity mourning and food distinctions","holiness_code"),
    ("14.22","14.29","Annual and third-year tithe","tithe_instruction"),
    ("15.1","15.11","Release debt and the poor","release_and_poverty_law"),
    ("15.12","15.18","Servant release","servant_release_law"),
    ("15.19","15.23","Firstborn animals","firstborn_instruction"),
    ("16.1","16.17","Pilgrimage festival calendar","festival_calendar"),
    ("16.18","17.13","Judges justice altar integrity apostasy and central tribunal","governance_and_adjudication_code"),
    ("17.14","17.20","Kingship rule","royal_office_instruction"),
    ("18.1","18.8","Priests and Levites provision and mobility","levitical_provision_law"),
    ("18.9","18.22","Prohibited divination and authorized prophet tests","prophetic_discernment_code"),
    ("19.1","19.14","Refuge cities culpability and land boundary","refuge_city_law"),
    ("19.15","19.21","Witnesses and false testimony","judicial_evidence_law"),
    ("20.1","20.9","Battle address and muster exemptions","war_address_and_muster_law"),
    ("20.10","20.20","Siege terms and preservation of trees","siege_law"),
    ("21.1","21.9","Unsolved homicide rite","atonement_rite"),
    ("21.10","21.23","Captive woman firstborn rebellious son and executed body","household_and_execution_case_collection"),
    ("22.1","22.12","Neighbor aid and material boundary ordinances","neighbor_and_distinction_law_collection"),
    ("22.13","22.30","Sexual and marital case collection","sexual_case_law_collection"),
    ("23.1","23.8","Assembly admission and exclusion","assembly_membership_law"),
    ("23.9","23.14","Camp holiness","camp_holiness_instruction"),
    ("23.15","23.25","Escaped servant cultic economic vow and field-neighbor duties","mixed_neighbor_duty_collection"),
    ("24.1","24.9","Remarriage and household-life safeguards","household_safeguard_collection"),
    ("24.10","24.22","Pledges wages liability and vulnerable gleaning","vulnerable_neighbor_protection_code"),
    ("25.1","25.4","Punishment restraint and work animal","judicial_restraint_collection"),
    ("25.5","25.16","Levirate assault and honest measures","household_and_commercial_justice_collection"),
    ("25.17","25.19","Amalek remembrance","remembrance_command"),
    ("26.1","26.11","Firstfruits confession","liturgical_confession"),
    ("26.12","26.15","Third-year tithe confession","liturgical_confession"),
    ("26.16","26.19","Reciprocal covenant declarations","covenant_ratification_declaration"),
    ("27.1","27.10","Inscription altar and identity proclamation","covenant_ceremony_instruction"),
    ("27.11","27.26","Gerizim-Ebal assignment and responsive curses","responsive_curse_liturgy"),
    ("28.1","28.14","Covenant blessings","covenant_blessing_oracle"),
    ("28.15","28.68","Cumulative covenant curses","covenant_curse_oracle"),
    ("29.1","29.15","Moab covenant heading historical prologue and inclusive oath","covenant_renewal_address"),
    ("29.16","29.29","Hidden apostasy future devastation and revealed-secret closure","covenant_warning"),
    ("30.1","30.10","Return and restoration","restoration_oracle"),
    ("30.11","30.20","Accessible command and life-death appeal","covenant_choice_appeal"),
    ("31.1","31.8","Moses and Joshua transition addresses","succession_address"),
    ("31.9","31.13","Torah deposit and septennial reading","document_deposit_instruction"),
    ("31.14","31.23","Tent commission and song-as-witness setup","commission_scene"),
    ("31.24","31.29","Document deposit and witness summons","document_deposit_and_summons"),
    ("31.30","32.43","Song of Moses with narrative introduction","covenant_witness_song"),
    ("32.44","32.47","Post-song exhortation","post_song_exhortation"),
    ("32.48","32.52","Death command","death_announcement"),
    ("33.1","33.5","Blessing superscription and theophanic prologue","tribal_blessing_prologue"),
    ("33.6","33.25","Named tribal blessing sequence","tribal_blessing_collection"),
    ("33.26","33.29","Poetic blessing coda","tribal_blessing_coda"),
    ("34.1","34.8","Land view death burial and mourning","death_narrative"),
    ("34.9","34.12","Joshua succession and Moses eulogy","succession_and_eulogy"),
]

LOW = {5, 12, 23, 24, 25, 27, 28, 31, 37, 40, 41, 46, 47, 51, 52, 53, 55, 60, 63, 64, 65, 67, 72, 76}

def ref(v):
    return f"Deut.{v}"

rows=[]
for i,(start,end,title,form) in enumerate(ROWS,1):
    span=f"{ref(start)}-{ref(end)}"
    seam=(f"At {ref(start)} a reviewed discourse, speaker, scene, legal-function, liturgical, or poetic movement opens; "
          f"the complete {form} movement '{title}' reaches its local closure at {ref(end)}.")
    low=i in LOW
    did=f"M7_sol-Deut-{i:03d}"
    rows.append({
      "model_id":"M7_sol","book":"Deut","span":span,"chunk_index_in_book":i,
      "working_title":title,"literature_type_guess":form,
      "boundary_evidence_refs":["reviews/Deut/primary_hebrew_v1.json","reviews/Deut/primary_literary_v1.json","reviews/Deut/canonical_premortem_v1.json","reviews/Deut/peer_crosscheck_v1.json","reviews/Deut/boss_ruling_v1.json","reviews/Deut/decision_relations.jsonl"],
      "strong_or_hebrew_tags_used":["evidence_only","roots_are_not_meaning","original_language_is_not_boundary_authority"],
      "wj_or_red_letter_considered":False,"frontier_flag_considered":True,
      "confidence":"low" if low else "medium","decision_id":did,"literary_form":form,
      "deciding_marker_or_seam":seam,
      "boundary_rationale":f"Prefer the larger coherent {form} unit {span}. {seam}",
      "rejected_alternative":f"Rejected narrower seams inside {span} because they would detach setup from response, governing condition from case sequence, or poetic movement from closure; rejected expansion because the adjacent unit changes the reviewed governing function.",
      "defensible_basis":f"{did} is defended by the converging speech/scene/form/function markers at {ref(start)} and closure at {ref(end)}; Hebrew discourse and paragraph signals corroborate but do not authorize the boundary.",
      "review_revision":1,
      "review_status":"final_deferred_appeal" if low else "candidate_review_complete",
      "review_holds":["deferred_human_or_external_ai","external_provider_review_at_convergence"] if low else ["external_provider_review_at_convergence"],
      "non_authorizing":True,"candidate_internal_seams":[seam],
      "original_language_translation_holds":["Hebrew/MT evidence and WEB-to-MT crosswalks are contextual only; variants, lexical choices, and preferred translation remain outside this candidate boundary."],
      "cross_reference_holds":["Internal-Bible relations are recorded separately and do not authorize this local boundary."],
      "red_team_premortem_holds":["The larger-unit default may conceal a defensible inner seam; the append-only appeal ledger preserves that alternative for independent or human review."] if low else ["A narrower split could detach governing setup from response or closure; expansion would mix adjacent literary functions."],
      "working_title_is_boundary_authority":False,"working_title_origin":"independent_deuteronomy_mesh_reconciliation_v1","candidate_only":True,
      "review_evidence_summary":seam+" Evidence is candidate-only and does not select theology, canon, authorship, tradition, or a preferred textual reading."
    })

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("".join(json.dumps(r,ensure_ascii=False,separators=(",",":"))+"\n" for r in rows),encoding="utf-8")
print(json.dumps({"path":str(OUT),"rows":len(rows),"low":sum(r["confidence"]=="low" for r in rows)}))
