from __future__ import annotations
import sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from build_review_artifacts_generic import build
E='51a2a56c5d228e7ab472282408b5c7569747ae0df3cebb085fd9ba1cb42d3116'
def ids(a,b):return [f'M7_sol-1Thess-{i:03d}' for i in range(a,b+1)]
relations=(
('001',ids(1,2),['Acts.17.1-Acts.17.15','Ps.1.1-Ps.1.6'],'prescript_thanksgiving_work_labor_endurance_reception_example_turning_and_waiting_relations'),
('002',ids(3,4),['Jer.1.1-Jer.1.19','Ps.131.1-Ps.131.3'],'arrival_boldness_defense_non_flattery_non_greed_nurse_parent_labor_conduct_and_exhortation_relations'),
('003',ids(5,6),['Jer.6.1-Jer.7.34','Ps.44.1-Ps.44.26'],'reception_persecution_comparison_wrath_statement_separation_desire_hope_and_crown_relations'),
('004',ids(7,9),['Acts.17.1-Acts.18.28','Ps.126.1-Ps.126.6'],'Timothy_mission_concern_report_joy_return_desire_and_way_love_strength_prayer_relations'),
('005',ids(10,11),['Lev.18.1-Lev.20.27','Deut.6.1-Deut.6.25'],'conduct_holiness_sexual_instruction_rationale_brotherly_love_quiet_work_and_outsider_relations'),
('006',ids(12,13),['Isa.25.1-Isa.27.13','Dan.12.1-Dan.12.13','Ps.90.1-Ps.90.17'],'dead_and_coming_instruction_consolation_times_seasons_day_night_vigilance_salvation_and_encouragement_relations'),
('007',ids(14,16),['Num.11.1-Num.11.35','Joel.2.1-Joel.3.21','Ps.150.1-Ps.150.6'],'recognition_peace_community_commands_rejoice_pray_thanks_Spirit_prophecy_testing_peace_prayer_greeting_reading_and_grace_relations'))
build(book='1Thess',expected_sha=E,roles=(('greek','1thess-primary-greek-textual-20260724-a','Koine_Greek_epistolary_discourse_textual_translation_speaker_specialist'),('literary','1thess-primary-literary-20260724-b','epistolary_report_defense_consolation_vigilance_catalogue_specialist'),('canonical','1thess-primary-canonical-context-premortem-20260724-c','canonical_relations_Second_Temple_apocalyptic_historical_premortem_specialist')),peer_attempt='1thess-peer-crosscheck-20260724-d',boss_attempt='1thess-boss-adjudicator-20260724-e',post_attempt='1thess-role-separated-postchecker-20260724-f',relation_specs=relations,reviewer_hint='human_or_external_ai_Koine_Greek_1Thessalonians_epistolary_historical_apocalyptic_textual_specialist')