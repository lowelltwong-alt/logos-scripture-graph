from __future__ import annotations
import sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from build_review_artifacts_generic import build
E='9fc0612e476a654fe171f9d5951d49d8a4c235309a604e6ed699948b91da4e69'
def ids(a,b):return [f'M7_sol-3John-{i:03d}' for i in range(a,b+1)]
relations=(
('001',ids(1,1),['2John.1.1-2John.1.13'],'elder_gaius_truth_love_wellbeing_prayer_visitor_testimony_joy_and_children_walking_relations'),
('002',ids(2,2),['Gen.18.1-Gen.18.33','Deut.10.1-Deut.10.22'],'faithful_hospitality_siblings_strangers_assembly_testimony_worthy_sending_name_mission_and_coworkers_truth_relations'),
('003',ids(3,3),['Prov.6.1-Prov.6.35','Ezek.34.1-Ezek.34.31'],'prior_writing_diotrephes_first_place_rejection_malicious_speech_hospitality_prevention_expulsion_and_recollection_relations'),
('004',ids(4,4),['Deut.19.1-Deut.19.21','Prov.3.1-Prov.3.35'],'imitate_good_not_evil_knowing_seeing_God_Demetrius_all_truth_and_we_testimony_relations'),
('005',ids(5,5),['2John.1.12-2John.1.13'],'ink_pen_face_to_face_peace_friends_name_by_name_and_versification_relations'))
build(book='3John',expected_sha=E,roles=(('greek','3john-primary-greek-textual-20260724-a','Koine_Greek_textual_translation_versification_identity_and_policy_specialist'),('literary','3john-primary-literary-20260724-b','brief_epistle_prayer_commendation_rationale_conflict_report_testimony_and_close_specialist'),('canonical','3john-primary-canonical-context-premortem-20260724-c','canonical_relations_Second_Temple_hospitality_truth_ancient_letter_travel_support_Jewish_patristic_reception_and_premortem_specialist')),peer_attempt='3john-peer-crosscheck-20260724-d',boss_attempt='3john-boss-adjudicator-20260724-e',post_attempt='3john-role-separated-postchecker-20260724-f',relation_specs=relations,reviewer_hint='human_or_external_ai_Koine_Greek_3John_versification_textual_literary_identity_hospitality_and_history_specialist')