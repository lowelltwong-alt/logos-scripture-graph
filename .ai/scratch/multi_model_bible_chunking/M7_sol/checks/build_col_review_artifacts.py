from __future__ import annotations
import sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from build_review_artifacts_generic import build
E='f3b530bfb4ea2e42e13785f81e0e364f449319d9152769a494bc006428dec3a4'
def ids(a,b):return [f'M7_sol-Col-{i:03d}' for i in range(a,b+1)]
relations=(
('001',ids(1,3),['Acts.19.1-Acts.20.38','Ps.1.1-Ps.1.6'],'prescript_thanksgiving_hope_love_report_knowledge_endurance_prayer_and_deliverance_relations'),
('002',ids(4,4),['Gen.1.1-Gen.2.25','Ps.89.1-Ps.89.52','Isa.45.1-Isa.45.25'],'image_creation_firstborn_fullness_reconciliation_poetic_movement_and_application_relations'),
('003',ids(5,5),['Isa.49.1-Isa.55.13','Ps.22.1-Ps.22.31'],'suffering_ministry_stewardship_mystery_struggle_assurance_and_order_relations'),
('004',ids(6,7),['Deut.10.1-Deut.10.22','Deut.30.1-Deut.30.20','Isa.44.1-Isa.45.25'],'rooted_walk_fullness_circumcision_burial_life_triumph_festival_angel_and_ascetic_warning_relations'),
('005',ids(8,10),['Gen.1.1-Gen.3.24','Deut.6.1-Deut.6.25','Ps.150.1-Ps.150.6'],'raised_life_inference_vice_catalogue_new_person_unity_virtue_catalogue_peace_word_singing_and_thanksgiving_relations'),
('006',ids(11,11),['Gen.2.1-Gen.3.24','Deut.5.1-Deut.6.25'],'household_address_spousal_parent_child_enslaved_master_pairs_through_four_one_relations'),
('007',ids(12,15),['Acts.19.1-Acts.28.31','Phlm.1.1-Phlm.1.25'],'prayer_watchfulness_outsider_speech_Tychicus_Onesimus_mission_greetings_Archippus_autograph_and_grace_relations'))
build(book='Col',expected_sha=E,roles=(('greek','col-primary-greek-textual-20260724-a','Koine_Greek_epistolary_poetic_textual_translation_hymn_source_specialist'),('literary','col-primary-literary-20260724-b','epistolary_prayer_argument_poetry_catalogue_household_specialist'),('canonical','col-primary-canonical-context-premortem-20260724-c','canonical_relations_Second_Temple_philosophical_household_premortem_specialist')),peer_attempt='col-peer-crosscheck-20260724-d',boss_attempt='col-boss-adjudicator-20260724-e',post_attempt='col-role-separated-postchecker-20260724-f',relation_specs=relations,reviewer_hint='human_or_external_ai_Koine_Greek_Colossians_poetic_argument_textual_household_specialist')