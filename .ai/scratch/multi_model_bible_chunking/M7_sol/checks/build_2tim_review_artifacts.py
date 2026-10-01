from __future__ import annotations
import sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from build_review_artifacts_generic import build
E='c89057593bebc3c9e033203648a78adafdce6e2aa9285d45f665f7441316db36'
def ids(a,b):return [f'M7_sol-2Tim-{i:03d}' for i in range(a,b+1)]
relations=(
('001',ids(1,4),['Deut.6.1-Deut.6.25','Acts.20.17-Acts.20.38'],'prescript_thanksgiving_remembrance_gift_suffering_testimony_deposit_and_examples_relations'),
('002',ids(5,6),['Prov.27.1-Prov.27.27','1Cor.9.1-1Cor.9.27'],'entrusting_soldier_athlete_farmer_remembrance_suffering_and_faithful_saying_relations'),
('003',ids(7,8),['Num.16.1-Num.18.32','Jer.18.1-Jer.18.23'],'quarrel_warning_approved_worker_foundation_vessels_flight_pursuit_and_servant_correction_relations'),
('004',ids(9,10),['Exod.7.1-Exod.9.35','Deut.6.1-Deut.6.25','Ps.119.1-Ps.119.176'],'last_days_vice_opponent_examples_following_suffering_sacred_writings_scripture_and_equipment_relations'),
('005',ids(11,12),['Acts.20.17-Acts.20.38','Phil.2.1-Phil.2.30'],'solemn_proclamation_charge_departure_contest_race_faith_crown_and_appearing_relations'),
('006',ids(13,15),['Ps.22.1-Ps.22.31','Acts.27.1-Acts.28.31'],'personal_requests_travel_register_warning_defense_rescue_doxology_greetings_and_grace_close_relations'))
build(book='2Tim',expected_sha=E,roles=(('greek','2tim-primary-greek-textual-20260724-a','Koine_Greek_epistolary_textual_translation_saying_list_and_close_specialist'),('literary','2tim-primary-literary-20260724-b','epistolary_charge_metaphor_saying_register_testimony_and_close_specialist'),('canonical','2tim-primary-canonical-context-premortem-20260724-c','canonical_relations_Second_Temple_later_Jewish_context_and_premortem_specialist')),peer_attempt='2tim-peer-crosscheck-20260724-d',boss_attempt='2tim-boss-adjudicator-20260724-e',post_attempt='2tim-role-separated-postchecker-20260724-f',relation_specs=relations,reviewer_hint='human_or_external_ai_Koine_Greek_2Timothy_textual_literary_register_and_canon_pressure_specialist')