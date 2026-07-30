from __future__ import annotations
import sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from build_review_artifacts_generic import build
E='0e9dc323db5645f539e757370140d504cf2c05caa014386ec8f2ef9802768830'
def ids(a,b):return [f'M7_sol-Acts-{i:03d}' for i in range(a,b+1)]
relations=(
('001',ids(1,8),['Ps.16.1-Ps.16.11','Ps.69.1-Ps.69.36','Ps.110.1-Ps.110.7','Joel.2.1-Joel.3.21','Luke.24.1-Luke.24.53'],'preface_departure_replacement_Pentecost_speech_response_and_summary_relations'),
('002',ids(9,18),['Exod.32.1-Exod.34.35','Deut.18.1-Deut.18.22','Ps.2.1-Ps.2.12','Ps.118.1-Ps.118.29','Dan.3.1-Dan.6.28'],'healing_temple_speeches_arrests_hearings_community_judgment_and_Gamaliel_relations'),
('003',ids(19,25),['Gen.12.1-Gen.50.26','Exod.1.1-Deut.34.12','Isa.53.1-Isa.53.12','Amos.5.1-Amos.5.27'],'seven_Stephen_speech_death_scattering_Samaria_and_official_relations'),
('004',ids(26,31),['1Sam.16.1-1Sam.31.13','1Kgs.17.1-2Kgs.2.25','Isa.35.1-Isa.35.10','Ezek.37.1-Ezek.37.28'],'Saul_encounter_Damascus_Jerusalem_and_Peter_healing_relations'),
('005',ids(32,37),['Lev.11.1-Lev.20.27','Jonah.1.1-Jonah.4.11','Isa.56.1-Isa.56.12','Ezek.4.1-Ezek.5.17'],'Cornelius_Peter_paired_visions_speech_response_and_Jerusalem_report_relations'),
('006',ids(38,43),['1Kgs.17.1-2Kgs.2.25','Dan.3.1-Dan.6.28','Amos.8.1-Amos.9.15'],'Antioch_relief_Herod_prison_deliverance_death_and_transition_relations'),
('007',ids(44,51),['Gen.12.1-Gen.22.24','Deut.7.1-Deut.10.22','Ps.2.1-Ps.2.12','Ps.16.1-Ps.16.11','Hab.1.1-Hab.3.19'],'sending_Cyprus_Pisidian_speech_response_Iconium_Lystra_Derbe_and_return_relations'),
('008',ids(52,56),['Gen.17.1-Gen.17.27','Exod.12.1-Exod.12.51','Lev.17.1-Lev.18.30','Amos.9.1-Amos.9.15'],'Jerusalem_council_speeches_decision_letter_delivery_and_separation_relations'),
('009',ids(57,62),['Dan.3.1-Dan.6.28','Isa.55.1-Isa.55.13','Joel.2.1-Joel.3.21'],'travel_Macedonian_vision_Lydia_spirit_prison_release_and_departure_relations'),
('010',ids(63,70),['Deut.32.1-Deut.32.52','Isa.45.1-Isa.45.25','Isa.55.1-Isa.55.13','Amos.9.1-Amos.9.15'],'Thessalonica_Berea_Athens_speech_Corinth_hearing_travel_and_Apollos_relations'),
('011',ids(71,75),['1Sam.28.1-1Sam.28.25','Deut.18.1-Deut.18.22','Isa.44.1-Isa.47.15'],'Ephesus_disciples_hall_signs_books_transition_and_riot_relations'),
('012',ids(76,79),['1Kgs.17.1-1Kgs.17.24','Ezek.3.1-Ezek.3.27','Ezek.33.1-Ezek.34.31'],'travel_Troas_gathering_Eutychus_itinerary_and_Miletus_farewell_relations'),
('013',ids(80,90),['Isa.6.1-Isa.6.13','Isa.49.1-Isa.49.26','Jer.1.1-Jer.1.19','Dan.3.1-Dan.6.28'],'Jerusalem_journey_warnings_arrival_arrest_defense_council_plot_and_transfer_relations'),
('014',ids(91,93),['Dan.3.1-Dan.6.28','Esth.1.1-Esth.10.3'],'Felix_accusation_defense_delay_and_custody_relations'),
('015',ids(94,98),['Isa.6.1-Isa.6.13','Isa.49.1-Isa.49.26','Dan.3.1-Dan.6.28'],'Festus_appeal_Agrippa_hearing_defense_and_response_relations'),
('016',ids(99,104),['Jonah.1.1-Jonah.2.10','Ps.107.1-Ps.107.43'],'voyage_warning_storm_speech_anchorage_meal_and_shipwreck_relations'),
('017',ids(105,110),['Isa.6.1-Isa.6.13','Isa.49.1-Isa.49.26','Isa.55.1-Isa.55.13','Luke.24.1-Luke.24.53'],'Malta_healings_Rome_journey_Jewish_leader_meetings_speech_response_and_close_relations'))
build(book='Acts',expected_sha=E,roles=(('greek','acts-primary-greek-textual-20260724-a','Koine_Greek_discourse_textual_variant_translation_specialist'),('literary','acts-primary-literary-20260724-b','narrative_speech_travel_hearing_literary_form_specialist'),('canonical','acts-primary-canonical-context-premortem-20260724-c','canonical_relations_Second_Temple_rabbinic_chronology_premortem_specialist')),peer_attempt='acts-peer-crosscheck-20260724-d',boss_attempt='acts-boss-adjudicator-20260724-e',post_attempt='acts-role-separated-postchecker-20260724-f',relation_specs=relations,reviewer_hint='human_or_external_ai_Koine_Greek_Acts_speech_travel_hearing_textual_Second_Temple_ancient_Jewish_reception_specialist')