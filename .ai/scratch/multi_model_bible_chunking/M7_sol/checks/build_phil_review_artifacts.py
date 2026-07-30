from __future__ import annotations
import sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from build_review_artifacts_generic import build
E='03f32e89ac4d50cb9e31ff94538e0ad72aefe40f051788716e531c61f6d352be'
def ids(a,b):return [f'M7_sol-Phil-{i:03d}' for i in range(a,b+1)]
relations=(
('001',ids(1,2),['Acts.16.1-Acts.16.40','Ps.1.1-Ps.1.6'],'prescript_thanksgiving_partnership_discernment_prayer_and_horizon_relations'),
('002',ids(3,4),['Acts.21.1-Acts.28.31','Ps.118.1-Ps.118.29'],'imprisonment_gospel_advance_rival_motives_rejoicing_life_death_deliberation_and_confidence_relations'),
('003',ids(5,7),['Isa.45.1-Isa.45.25','Deut.32.1-Deut.32.52','Ps.22.1-Ps.22.31'],'worthy_conduct_unity_self_emptying_exaltation_poetic_movement_obedience_shining_labor_and_offering_relations'),
('004',ids(8,9),['Acts.16.1-Acts.20.38','Rom.16.1-Rom.16.27'],'Timothy_travel_plan_Epaphroditus_illness_return_risk_and_commendation_relations'),
('005',ids(10,11),['Deut.10.1-Deut.10.22','Isa.45.1-Isa.45.25','Ps.84.1-Ps.84.12'],'warning_confidence_catalogue_loss_gain_knowing_pressing_maturity_imitation_opponents_citizenship_and_standing_relations'),
('006',ids(12,13),['Ps.4.1-Ps.4.8','Prov.3.1-Prov.4.27'],'Euodia_Syntyche_coworker_appeal_rejoicing_gentleness_prayer_peace_thought_and_practice_relations'),
('007',ids(14,15),['Deut.15.1-Deut.15.23','Prov.11.1-Prov.11.31','Acts.16.1-Acts.16.40'],'renewed_gift_contentment_partnership_account_fragrant_offering_greetings_household_and_grace_relations'))
build(book='Phil',expected_sha=E,roles=(('greek','phil-primary-greek-textual-20260724-a','Koine_Greek_epistolary_poetic_textual_translation_hymn_source_specialist'),('literary','phil-primary-literary-20260724-b','epistolary_report_deliberation_poetry_exemplum_list_specialist'),('canonical','phil-primary-canonical-context-premortem-20260724-c','canonical_relations_Second_Temple_civic_benefaction_premortem_specialist')),peer_attempt='phil-peer-crosscheck-20260724-d',boss_attempt='phil-boss-adjudicator-20260724-e',post_attempt='phil-role-separated-postchecker-20260724-f',relation_specs=relations,reviewer_hint='human_or_external_ai_Koine_Greek_Philippians_epistolary_poetry_textual_hymn_source_specialist')