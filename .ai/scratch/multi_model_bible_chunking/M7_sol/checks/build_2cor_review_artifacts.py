from __future__ import annotations
import sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from build_review_artifacts_generic import build
E='c1c57b0fa3d18cba55a6e39340f9eab42c20ba0681fbd1bddd175075a3270f56'
def ids(a,b):return [f'M7_sol-2Cor-{i:03d}' for i in range(a,b+1)]
relations=(
('001',ids(1,8),['Acts.18.1-Acts.20.38','Ps.34.1-Ps.34.22','Ps.116.1-Ps.116.19'],'prescript_consolation_affliction_travel_defense_grief_forgiveness_and_Troas_relations'),
('002',ids(9,12),['Exod.24.1-Exod.34.35','Jer.31.1-Jer.31.40','Ezek.36.1-Ezek.37.28'],'triumph_aroma_commendation_letter_Spirit_glory_veil_and_light_relations'),
('003',ids(13,19),['Gen.1.1-Gen.2.25','Ps.116.1-Ps.116.19','Isa.42.1-Isa.49.26'],'treasure_affliction_renewal_dwelling_judgment_reconciliation_ministry_and_open_heart_relations'),
('004',ids(20,22),['Lev.19.1-Lev.20.27','Isa.52.1-Isa.52.15','Jer.31.1-Jer.31.40'],'unequal_yoke_citation_catena_holiness_inference_appeal_grief_repentance_and_comfort_relations'),
('005',ids(23,27),['Exod.16.1-Exod.16.36','Prov.3.1-Prov.3.35','Ps.112.1-Ps.112.10'],'collection_exempla_equality_delegation_safeguards_preparation_sowing_thanksgiving_and_prayer_relations'),
('006',ids(28,32),['Jer.9.1-Jer.9.26','Deut.19.1-Deut.19.21','Acts.18.1-Acts.20.38'],'presence_absence_warfare_authority_measure_jealousy_rivals_free_proclamation_and_disguise_relations'),
('007',ids(33,35),['Deut.24.1-Deut.25.19','1Kgs.19.1-1Kgs.19.21','Job.1.1-Job.2.13'],'fool_speech_hardship_catalogue_escape_visions_thorn_weakness_signs_and_grievance_relations'),
('008',ids(36,40),['Deut.19.1-Deut.19.21','Acts.18.1-Acts.20.38','Rom.1.1-Rom.16.25'],'third_visit_spending_delegation_feared_disorders_warning_self_test_prayer_exhortations_greetings_and_benediction_relations'))
build(book='2Cor',expected_sha=E,roles=(('greek','2cor-primary-greek-textual-20260724-a','Koine_Greek_epistolary_argument_textual_variant_translation_specialist'),('literary','2cor-primary-literary-20260724-b','epistolary_rhetoric_travel_defense_irony_catalogue_and_argument_specialist'),('canonical','2cor-primary-canonical-context-premortem-20260724-c','canonical_relations_Second_Temple_rabbinic_partition_premortem_specialist')),peer_attempt='2cor-peer-crosscheck-20260724-d',boss_attempt='2cor-boss-adjudicator-20260724-e',post_attempt='2cor-role-separated-postchecker-20260724-f',relation_specs=relations,reviewer_hint='human_or_external_ai_Koine_Greek_2Corinthians_epistolary_rhetoric_textual_partition_specialist')