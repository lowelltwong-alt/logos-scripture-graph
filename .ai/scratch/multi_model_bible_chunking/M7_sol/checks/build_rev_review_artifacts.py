from __future__ import annotations
import sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from build_review_artifacts_generic import build
E='48360e028e836adbe79757058e8635ac8396ebd9c4ef4d94093657690708cc42'
def ids(a,b):return [f'M7_sol-Rev-{i:03d}' for i in range(a,b+1)]
relations=(
('001',ids(1,2),['Dan.7.1-Dan.7.28','Zech.4.1-Zech.4.14'],'apocalypse_prescript_blessing_coming_doxology_divine_speech_in_Spirit_humanlike_figure_commission_lampstands_and_stars_relations'),
('002',ids(3,9),['Exod.19.1-Exod.20.26','Isa.6.1-Isa.6.13'],'seven_message_oracles_addressee_title_knowledge_evaluation_call_Spirit_hearing_and_overcoming_relations'),
('003',ids(10,11),['Isa.6.1-Isa.6.13','Ezek.1.1-Ezek.2.10','Dan.7.1-Dan.7.28'],'throne_beings_hymns_scroll_search_Lion_Lamb_new_song_and_concentric_acclamation_relations'),
('004',ids(12,16),['Zech.1.1-Zech.6.15','Ezek.9.1-Ezek.10.22','Dan.12.1-Dan.12.13'],'horsemen_souls_cosmic_sixth_seal_question_tribe_sealing_multitude_dialogue_interpretation_and_seventh_seal_relations'),
('005',ids(17,23),['Exod.7.1-Exod.12.51','Joel.1.1-Joel.3.21','Ezek.2.1-Ezek.3.27','Zech.4.1-Zech.4.14'],'incense_trumpets_woes_locusts_Euphrates_riders_mighty_angel_scroll_temple_witnesses_seventh_trumpet_hymn_and_temple_relations'),
('006',ids(24,31),['Gen.3.1-Gen.3.24','Dan.7.1-Dan.12.13','Ps.2.1-Ps.2.12','Joel.3.1-Joel.3.21'],'woman_dragon_child_war_hymn_pursuit_sea_land_beasts_number_Lamb_144000_angel_proclamations_beatitude_and_harvest_relations'),
('007',ids(32,35),['Exod.7.1-Exod.15.27','Deut.32.1-Deut.32.52'],'bowl_prelude_Moses_Lamb_song_temple_smoke_seven_bowls_justice_speeches_Armageddon_interjection_and_seventh_bowl_relations'),
('008',ids(36,43),['Isa.13.1-Isa.14.32','Isa.21.1-Isa.21.17','Jer.50.1-Jer.51.64','Ezek.26.1-Ezek.28.26'],'woman_beast_vision_interpretation_Babylon_fall_separation_kings_merchants_mariners_laments_millstone_sign_hallelujahs_marriage_and_worship_correction_relations'),
('009',ids(44,48),['Ezek.38.1-Ezek.39.29','Dan.7.1-Dan.7.28','Isa.24.1-Isa.27.13'],'rider_names_armies_bird_supper_beast_conflict_dragon_binding_thrones_first_resurrection_release_Gog_Magog_white_throne_books_and_second_death_relations'),
('010',ids(49,53),['Isa.60.1-Isa.66.24','Ezek.40.1-Ezek.48.35','Gen.2.1-Gen.3.24'],'new_creation_city_bride_throne_speech_city_measurement_materials_nations_gates_river_tree_throne_face_name_light_and_reign_relations'),
('011',ids(54,57),['Dan.12.1-Dan.12.13','Isa.55.1-Isa.55.13'],'reliable_words_coming_blessings_worship_correction_unsealed_prophecy_identity_invitation_scroll_warning_final_testimony_prayer_and_benediction_relations'))
build(book='Rev',expected_sha=E,roles=(('greek','rev-primary-greek-textual-20260724-a','Koine_Greek_textual_translation_speaker_oracle_vision_cycle_hymn_lament_city_and_epilogue_specialist'),('literary','rev-primary-literary-20260724-b','apocalypse_oracle_vision_numbered_cycle_interlude_hymn_sign_interpretation_lament_city_tour_and_epilogue_specialist'),('canonical','rev-primary-canonical-context-premortem-20260724-c','canonical_relations_Torah_Prophets_Second_Temple_apocalypse_throne_angel_imperial_Jewish_patristic_reception_and_premortem_specialist')),peer_attempt='rev-peer-crosscheck-20260724-d',boss_attempt='rev-boss-adjudicator-20260724-e',post_attempt='rev-role-separated-postchecker-20260724-f',relation_specs=relations,reviewer_hint='human_or_external_ai_Koine_Greek_Revelation_textual_speaker_literary_apocalyptic_canonical_Second_Temple_and_reception_specialist')