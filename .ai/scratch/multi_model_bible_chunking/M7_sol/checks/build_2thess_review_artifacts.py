from __future__ import annotations
import sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from build_review_artifacts_generic import build
E='5a4a5e3b3005aa4b8060105bcf5dc9cb41673a9c5b115f9c469014509f588fe4'
def ids(a,b):return [f'M7_sol-2Thess-{i:03d}' for i in range(a,b+1)]
relations=(
('001',ids(1,3),['Isa.2.1-Isa.4.6','Ps.96.1-Ps.98.9'],'prescript_thanksgiving_faith_love_perseverance_judgment_recompense_relief_revelation_and_worthiness_prayer_relations'),
('002',ids(4,4),['Dan.7.1-Dan.12.13','Isa.11.1-Isa.11.16','Ezek.28.1-Ezek.28.26'],'coming_gathering_day_correction_rebellion_lawlessness_temple_restraint_revelation_destruction_deception_and_judgment_relations'),
('003',ids(5,5),['Deut.7.1-Deut.7.26','Isa.40.1-Isa.40.31'],'thanksgiving_calling_sanctification_good_news_glory_stand_firm_traditions_comfort_and_strength_relations'),
('004',ids(6,6),['Ps.119.1-Ps.119.176','Acts.17.1-Acts.18.28'],'word_spread_rescue_faithfulness_confidence_commands_and_love_endurance_direction_prayer_relations'),
('005',ids(7,8),['Gen.2.1-Gen.3.24','Prov.6.1-Prov.6.35','Prov.24.1-Prov.24.34'],'disorder_tradition_work_example_rule_busybody_quiet_work_doing_good_marking_and_sibling_admonition_relations'),
('006',ids(9,9),['Num.6.1-Num.6.27','Ps.29.1-Ps.29.11'],'peace_presence_autograph_authentication_grace_and_epistolary_close_relations'))
build(book='2Thess',expected_sha=E,roles=(('greek','2thess-primary-greek-textual-20260724-a','Koine_Greek_epistolary_warning_textual_translation_speaker_specialist'),('literary','2thess-primary-literary-20260724-b','epistolary_judgment_warning_paraenesis_close_specialist'),('canonical','2thess-primary-canonical-context-premortem-20260724-c','canonical_relations_Second_Temple_apocalyptic_work_context_premortem_specialist')),peer_attempt='2thess-peer-crosscheck-20260724-d',boss_attempt='2thess-boss-adjudicator-20260724-e',post_attempt='2thess-role-separated-postchecker-20260724-f',relation_specs=relations,reviewer_hint='human_or_external_ai_Koine_Greek_2Thessalonians_apocalyptic_identity_timetable_work_specialist')