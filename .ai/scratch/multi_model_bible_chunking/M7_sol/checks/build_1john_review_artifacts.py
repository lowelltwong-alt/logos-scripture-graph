from __future__ import annotations
import sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from build_review_artifacts_generic import build
E='1798af95c5eed9c6a3f5ee5f9c47547d1a7ed85d2ad96742a4713c4215c50bbe'
def ids(a,b):return [f'M7_sol-1John-{i:03d}' for i in range(a,b+1)]
relations=(
('001',ids(1,2),['Gen.1.1-Gen.1.31','John.1.1-John.1.18'],'sensory_witness_word_life_manifestation_fellowship_joy_message_light_dark_conditional_confession_cleansing_advocate_and_hilasmos_relations'),
('002',ids(3,5),['Deut.6.1-Deut.6.25','John.13.1-John.15.27'],'knowing_command_love_sibling_light_addressee_stanzas_world_desire_last_hour_opponents_anointing_truth_promise_and_abiding_relations'),
('003',ids(6,6),['Gen.3.1-Gen.4.26'],'abiding_appearance_confidence_righteous_birth_purification_sin_lawlessness_seed_and_children_contrast_relations'),
('004',ids(7,7),['Gen.4.1-Gen.4.26','Deut.15.1-Deut.15.23'],'love_message_cain_hatred_death_life_self_giving_material_aid_truth_deed_heart_assurance_prayer_command_and_spirit_relations'),
('005',ids(8,9),['Deut.13.1-Deut.13.18','John.1.1-John.1.18'],'spirit_testing_prophets_confession_world_hearing_truth_error_God_love_manifestation_sending_abiding_confession_perfected_love_judgment_and_sibling_relations'),
('006',ids(10,11),['Deut.19.1-Deut.19.21','John.19.1-John.19.42'],'belief_birth_love_commands_victory_faith_water_blood_spirit_witness_human_divine_testimony_son_and_life_relations'),
('007',ids(12,12),['Deut.13.1-Deut.13.18','John.20.1-John.20.31'],'purpose_eternal_life_prayer_confidence_sin_not_unto_death_life_giving_assurances_true_one_and_idol_warning_relations'))
build(book='1John',expected_sha=E,roles=(('greek','1john-primary-greek-textual-20260724-a','Koine_Greek_textual_translation_aspect_recursive_confession_witness_and_closing_specialist'),('literary','1john-primary-literary-20260724-b','recursive_claim_test_ground_remedy_stanza_contrast_confession_witness_and_assurance_specialist'),('canonical','1john-primary-canonical-context-premortem-20260724-c','canonical_relations_Second_Temple_dualism_wisdom_forensic_witness_Jewish_patristic_text_reception_and_premortem_specialist')),peer_attempt='1john-peer-crosscheck-20260724-d',boss_attempt='1john-boss-adjudicator-20260724-e',post_attempt='1john-role-separated-postchecker-20260724-f',relation_specs=relations,reviewer_hint='human_or_external_ai_Koine_Greek_1John_textual_recursive_literary_canonical_and_reception_specialist')