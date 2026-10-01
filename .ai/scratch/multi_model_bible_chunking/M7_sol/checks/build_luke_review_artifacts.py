from __future__ import annotations
import sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from build_review_artifacts_generic import build
E='e7409a58915e31ea2ee9d077f0e9c40d537e2009d98cbf01f8dbc18fb5c71d8a'
def ids(a,b):return [f'M7_sol-Luke-{i:03d}' for i in range(a,b+1)]
relations=(
('001',ids(1,10),['Gen.18.1-Gen.21.21','1Sam.1.1-1Sam.2.11','2Sam.7.1-2Sam.7.29','Mal.3.1-Mal.4.6','Isa.7.1-Isa.11.16'],'preface_annunciations_births_songs_presentation_and_childhood_relations'),
('002',ids(11,15),['Gen.5.1-Gen.36.43','Deut.6.1-Deut.8.20','Isa.40.1-Isa.40.11','Isa.61.1-Isa.61.11','Mal.3.1-Mal.4.6'],'John_baptism_genealogy_testing_and_Nazareth_relations'),
('003',ids(16,24),['Lev.13.1-Lev.14.57','1Sam.21.1-1Sam.21.9','Isa.35.1-Isa.35.10','Hos.6.1-Hos.6.11','Mark.1.1-Mark.3.19'],'teaching_healing_call_controversy_Twelve_and_crowd_relations'),
('004',ids(25,28),['Lev.19.1-Lev.19.37','Deut.15.1-Deut.15.23','Ps.1.1-Ps.1.6','Prov.10.1-Prov.31.31','Isa.5.1-Isa.5.30'],'blessings_woes_enemy_love_judgment_fruit_and_builders_relations'),
('005',ids(29,33),['1Kgs.17.1-1Kgs.17.24','2Kgs.4.1-2Kgs.4.37','Isa.35.1-Isa.35.10','Isa.61.1-Isa.61.11','Mal.3.1-Mal.4.6'],'centurion_widow_John_response_anointing_and_women_summary_relations'),
('006',ids(34,39),['Ps.78.1-Ps.78.72','Jonah.1.1-Jonah.2.10','1Kgs.17.1-1Kgs.17.24','2Kgs.4.1-2Kgs.4.44','Mark.4.1-Mark.5.43'],'sower_lamp_family_sea_deliverance_and_Jairus_woman_relations'),
('007',ids(40,45),['Exod.16.1-Exod.17.16','Exod.24.1-Exod.34.35','Dan.7.1-Dan.7.28','Mal.4.1-Mal.4.6','Mark.6.1-Mark.9.50'],'mission_Herod_feeding_confession_prediction_transfiguration_and_healing_relations'),
('008',ids(46,54),['Gen.18.1-Gen.19.38','Deut.6.1-Deut.6.25','2Kgs.2.1-2Kgs.2.25','Jonah.1.1-Jonah.4.11','Isa.5.1-Isa.5.30'],'journey_turn_mission_lawyer_Samaritan_hospitality_prayer_sign_and_woes_relations'),
('009',ids(55,63),['Exod.12.1-Exod.12.51','Isa.5.1-Isa.5.30','Isa.55.1-Isa.55.13','Jer.7.1-Jer.7.34','Mic.3.1-Mic.3.12'],'warnings_wealth_watchfulness_repentance_healing_narrow_door_and_lament_relations'),
('010',ids(64,72),['Lev.19.1-Lev.19.37','Deut.15.1-Deut.15.23','Deut.24.1-Deut.24.22','1Sam.2.1-1Sam.2.36','Amos.4.1-Amos.8.14'],'meal_banquet_cost_lost_items_two_sons_manager_wealth_and_discipleship_relations'),
('011',ids(73,82),['Gen.18.1-Gen.19.38','Lev.13.1-Lev.14.57','Isa.53.1-Isa.53.12','Dan.7.1-Dan.7.28','1Sam.8.1-1Sam.8.22'],'ten_cleansed_kingdom_prayer_children_wealth_prediction_Zacchaeus_and_minas_relations'),
('012',ids(83,92),['Ps.110.1-Ps.110.7','Ps.118.1-Ps.118.29','Isa.5.1-Isa.5.30','Isa.56.1-Isa.56.12','Jer.7.1-Jer.7.34','Zech.9.1-Zech.14.21'],'entry_lament_temple_authority_tenants_tax_resurrection_David_scribes_and_widow_relations'),
('013',ids(93,95),['Dan.7.1-Dan.7.28','Dan.9.1-Dan.12.13','Zech.12.1-Zech.14.21','1Thess.4.1-1Thess.5.28','Rev.6.1-Rev.22.21'],'temple_destruction_distress_signs_fig_watchfulness_and_teaching_relations'),
('014',ids(96,104),['Exod.12.1-Exod.12.51','Ps.41.1-Ps.41.13','Ps.42.1-Ps.43.5','Isa.53.1-Isa.53.12','Zech.11.1-Zech.13.9'],'plot_Passover_meal_service_Peter_prayer_arrest_denial_mockery_and_council_relations'),
('015',ids(105,111),['Ps.22.1-Ps.22.31','Ps.69.1-Ps.69.36','Isa.52.1-Isa.53.12','Amos.8.1-Amos.8.14','Zech.12.1-Zech.13.9'],'Pilate_Herod_procession_crucifixion_death_witness_and_burial_relations'),
('016',ids(112,115),['Gen.18.1-Gen.19.38','Ps.16.1-Ps.16.11','Isa.52.1-Isa.53.12','Jonah.1.1-Jonah.2.10','Acts.1.1-Acts.2.47'],'tomb_road_recognition_Jerusalem_appearance_promise_and_departure_relations'))
build(book='Luke',expected_sha=E,roles=(('greek','luke-primary-greek-textual-20260724-a','Koine_Greek_discourse_textual_variant_translation_specialist'),('literary','luke-primary-literary-20260724-b','narrative_paired_panel_journey_discourse_literary_form_specialist'),('canonical','luke-primary-canonical-context-premortem-20260724-c','canonical_relations_Second_Temple_rabbinic_chronology_premortem_specialist')),peer_attempt='luke-peer-crosscheck-20260724-d',boss_attempt='luke-boss-adjudicator-20260724-e',post_attempt='luke-role-separated-postchecker-20260724-f',relation_specs=relations,reviewer_hint='human_or_external_ai_Koine_Greek_Luke_narrative_journey_textual_Second_Temple_ancient_Jewish_reception_specialist')