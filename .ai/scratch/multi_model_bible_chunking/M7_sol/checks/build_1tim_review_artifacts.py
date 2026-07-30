from __future__ import annotations
import sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from build_review_artifacts_generic import build
E='861d779607ef740ed6d2f2248fde65ddf131b85c0591713b959832777b111bfa'
def ids(a,b):return [f'M7_sol-1Tim-{i:03d}' for i in range(a,b+1)]
relations=(
('001',ids(1,3),['Deut.6.1-Deut.6.25','Acts.20.17-Acts.20.38','Titus.1.1-Titus.1.16'],'prescript_charge_command_love_law_list_and_entrusted_message_relations'),
('002',ids(4,5),['Ps.51.1-Ps.51.19','Acts.9.1-Acts.9.31'],'thanksgiving_mercy_faithful_saying_doxology_renewed_charge_and_warning_example_relations'),
('003',ids(6,7),['Gen.1.1-Gen.3.24','Ps.67.1-Ps.67.7','Mark.10.35-Mark.10.45'],'prayer_rationale_mediation_conduct_instruction_creation_deception_and_childbearing_hot_zone_relations'),
('004',ids(8,10),['Acts.6.1-Acts.6.7','Titus.1.5-Titus.1.16'],'qualification_list_household_conduct_purpose_and_confessional_close_relations'),
('005',ids(11,12),['Gen.1.1-Gen.2.25','Prov.3.1-Prov.3.35'],'reported_warning_creation_thanksgiving_training_instruction_example_gift_and_perseverance_relations'),
('006',ids(13,13),['Deut.10.1-Deut.10.22','Ruth.1.1-Ruth.4.22','Prov.31.1-Prov.31.31'],'household_age_widow_honor_enrollment_and_relief_relations'),
('007',ids(14,15),['Deut.19.1-Deut.19.21','Deut.25.1-Deut.25.19','Lev.19.1-Lev.19.37'],'elder_honor_accusation_reproof_appointment_counsel_and_bondservant_master_address_relations'),
('008',ids(16,19),['Prov.11.1-Prov.11.31','Prov.30.1-Prov.30.33','Matt.6.1-Matt.6.34'],'divergent_teaching_gain_contentment_money_warning_vocative_charge_doxology_rich_charge_deposit_and_grace_close_relations'))
build(book='1Tim',expected_sha=E,roles=(('greek','1tim-primary-greek-textual-20260724-a','Koine_Greek_epistolary_list_textual_translation_hot_zone_specialist'),('literary','1tim-primary-literary-20260724-b','epistolary_paraenesis_list_function_confession_and_close_specialist'),('canonical','1tim-primary-canonical-context-premortem-20260724-c','canonical_relations_Second_Temple_later_Jewish_context_and_premortem_specialist')),peer_attempt='1tim-peer-crosscheck-20260724-d',boss_attempt='1tim-boss-adjudicator-20260724-e',post_attempt='1tim-role-separated-postchecker-20260724-f',relation_specs=relations,reviewer_hint='human_or_external_ai_Koine_Greek_1Timothy_textual_list_household_and_literary_specialist')