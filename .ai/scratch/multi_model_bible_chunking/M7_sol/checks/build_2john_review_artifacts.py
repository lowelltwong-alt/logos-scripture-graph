from __future__ import annotations
import sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from build_review_artifacts_generic import build
E='f42afdff9db02cb5dda50d21fccdfd9421924ba390b9f825d5a8f9075065c60c'
def ids(a,b):return [f'M7_sol-2John-{i:03d}' for i in range(a,b+1)]
relations=(
('001',ids(1,1),['Deut.6.1-Deut.6.25','John.1.1-John.1.18'],'elder_elect_lady_children_truth_love_and_expanded_grace_mercy_peace_greeting_relations'),
('002',ids(2,2),['Deut.6.1-Deut.6.25','John.13.1-John.15.27'],'joy_walking_truth_received_command_mutual_love_and_love_defined_as_walking_relations'),
('003',ids(3,3),['Deut.13.1-Deut.13.18','1John.2.1-1John.5.21'],'deceivers_confession_watch_reward_abiding_teaching_reception_greeting_and_participation_relations'),
('004',ids(4,4),['3John.1.1-3John.1.15'],'paper_ink_face_to_face_joy_elect_sister_children_and_final_greeting_relations'))
build(book='2John',expected_sha=E,roles=(('greek','2john-primary-greek-textual-20260724-a','Koine_Greek_textual_translation_identity_and_hospitality_case_specialist'),('literary','2john-primary-literary-20260724-b','brief_epistle_prescript_command_definition_warning_case_consequence_and_close_specialist'),('canonical','2john-primary-canonical-context-premortem-20260724-c','canonical_relations_Second_Temple_truth_love_ancient_letter_hospitality_Jewish_patristic_reception_and_premortem_specialist')),peer_attempt='2john-peer-crosscheck-20260724-d',boss_attempt='2john-boss-adjudicator-20260724-e',post_attempt='2john-role-separated-postchecker-20260724-f',relation_specs=relations,reviewer_hint='human_or_external_ai_Koine_Greek_2John_textual_literary_identity_hospitality_and_reception_specialist')