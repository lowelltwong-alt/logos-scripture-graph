from __future__ import annotations
import sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from build_review_artifacts_generic import build
E='1baea443264604c2a25f471fa5d2785ac58b2d8b4aab52931533fe65d7c3c8a6'
def ids(a,b):return [f'M7_sol-John-{i:03d}' for i in range(a,b+1)]
relations=(
('001',ids(1,7),['Gen.1.1-Gen.2.25','Exod.12.1-Exod.12.51','Exod.33.1-Exod.34.35','Isa.40.1-Isa.40.11','Mal.3.1-Mal.3.5'],'opening_witness_disciple_calls_Cana_and_temple_relations'),
('002',ids(8,10),['Num.21.1-Num.21.35','Ezek.36.1-Ezek.37.28','Dan.7.1-Dan.7.28','Isa.9.1-Isa.9.21'],'Nicodemus_light_baptism_and_above_earth_witness_relations'),
('003',ids(11,14),['Gen.24.1-Gen.24.67','Gen.29.1-Gen.29.35','2Kgs.5.1-2Kgs.5.27','Isa.55.1-Isa.55.13','Amos.9.1-Amos.9.15'],'Samaritan_well_harvest_town_response_and_official_healing_relations'),
('004',ids(15,17),['Exod.20.1-Exod.20.21','Deut.5.1-Deut.5.33','Dan.7.1-Dan.7.28','Isa.35.1-Isa.35.10'],'festival_healing_Sabbath_life_judgment_and_witness_relations'),
('005',ids(18,22),['Exod.16.1-Exod.17.16','Num.11.1-Num.11.35','2Kgs.4.1-2Kgs.4.44','Ps.78.1-Ps.78.72'],'feeding_sea_bread_dialogue_murmuring_and_disciple_response_relations'),
('006',ids(23,32),['Lev.23.1-Lev.23.44','Deut.16.1-Deut.16.22','Isa.55.1-Isa.55.13','Ezek.47.1-Ezek.47.23','Gen.18.1-Gen.19.38'],'festival_origin_living_water_received_coordinate_light_witness_and_Abraham_disputes_relations'),
('007',ids(33,40),['Exod.3.1-Exod.4.31','Ps.23.1-Ps.23.6','Ps.82.1-Ps.82.8','Isa.35.1-Isa.35.10','Ezek.34.1-Ezek.34.31'],'blind_man_investigation_shepherd_Dedication_and_beyond_Jordan_relations'),
('008',ids(41,45),['1Kgs.17.1-1Kgs.17.24','2Kgs.4.1-2Kgs.4.37','Isa.25.1-Isa.26.21','Ezek.37.1-Ezek.37.28'],'Lazarus_dialogues_tomb_sign_council_response_and_withdrawal_relations'),
('009',ids(46,50),['Ps.118.1-Ps.118.29','Isa.6.1-Isa.6.13','Isa.52.1-Isa.53.12','Zech.9.1-Zech.14.21'],'anointing_entry_Greek_visitors_voice_response_and_public_close_relations'),
('010',ids(51,56),['Exod.12.1-Exod.12.51','Ps.41.1-Ps.41.13','Lev.19.1-Lev.19.37','Deut.6.1-Deut.6.25'],'supper_footwashing_betrayal_departure_command_way_advocate_and_peace_relations'),
('011',ids(57,64),['Isa.5.1-Isa.5.30','Ps.69.1-Ps.69.36','Deut.6.1-Deut.6.25','Jer.31.1-Jer.31.40'],'vine_love_hatred_advocate_sorrow_joy_plain_speech_and_prayer_relations'),
('012',ids(65,70),['Ps.2.1-Ps.2.12','Ps.41.1-Ps.41.13','Isa.53.1-Isa.53.12','Zech.11.1-Zech.13.9'],'garden_arrest_Annas_denials_Pilate_kingship_mockery_and_handover_relations'),
('013',ids(71,73),['Exod.12.1-Exod.12.51','Ps.22.1-Ps.22.31','Ps.69.1-Ps.69.36','Zech.12.1-Zech.13.9','Isa.52.1-Isa.53.12'],'crucifixion_title_garments_family_death_side_witness_and_burial_relations'),
('014',ids(74,78),['Gen.2.1-Gen.3.24','Ps.16.1-Ps.16.11','Isa.52.1-Isa.53.12','Dan.7.1-Dan.7.28'],'tomb_Mary_evening_Thomas_signs_and_purpose_close_relations'),
('015',ids(79,82),['Ezek.47.1-Ezek.47.23','Luke.5.1-Luke.5.11','Acts.1.1-Acts.2.47','Rev.1.1-Rev.22.21'],'lakeside_catch_Peter_exchange_beloved_disciple_witness_and_books_close_relations'))
build(book='John',expected_sha=E,roles=(('greek','john-primary-greek-textual-20260724-a','Koine_Greek_discourse_textual_variant_translation_specialist'),('literary','john-primary-literary-replacement-20260724-b2','narrative_sign_dialogue_festival_discourse_literary_form_specialist_with_prior_role_disclosure'),('canonical','john-primary-canonical-context-premortem-20260724-c','canonical_relations_Second_Temple_rabbinic_chronology_premortem_specialist')),peer_attempt='john-peer-crosscheck-20260724-d',boss_attempt='john-boss-adjudicator-20260724-e',post_attempt='john-role-separated-postchecker-20260724-f',relation_specs=relations,reviewer_hint='human_or_external_ai_Koine_Greek_John_dialogue_sign_textual_Second_Temple_ancient_Jewish_reception_specialist')