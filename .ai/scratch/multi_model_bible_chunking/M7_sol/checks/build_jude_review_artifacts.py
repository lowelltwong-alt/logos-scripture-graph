from __future__ import annotations
import sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from build_review_artifacts_generic import build
E='97db8960265e4fd639ca054c83a7692560d9339c341f93c60228286ecc283c4a'
def ids(a,b):return [f'M7_sol-Jude-{i:03d}' for i in range(a,b+1)]
relations=(
('001',ids(1,1),['Deut.13.1-Deut.13.18'],'prescript_mercy_peace_love_common_salvation_appeal_contend_intruders_and_judgment_description_relations'),
('002',ids(2,2),['Exod.12.1-Exod.15.27','Gen.6.1-Gen.19.38','Num.16.1-Num.16.50','Num.22.1-Num.24.25'],'Egypt_angels_Sodom_dreamers_Michael_Moses_Cain_Balaam_Korah_love_feasts_metaphors_Enoch_prophecy_and_behavior_relations'),
('003',ids(3,3),['Acts.20.1-Acts.20.38','2Pet.3.1-2Pet.3.18'],'apostolic_remembrance_scoffers_divisions_build_pray_keep_await_mercy_save_snatch_and_garment_relations'),
('004',ids(4,4),['Ps.145.1-Ps.150.6'],'keep_from_stumbling_present_with_joy_only_God_Savior_glory_majesty_power_authority_and_temporal_acclamation_relations'))
build(book='Jude',expected_sha=E,roles=(('greek','jude-primary-greek-textual-20260724-a','Koine_Greek_textual_translation_variant_angel_Moses_Enoch_rescue_and_doxology_specialist'),('literary','jude-primary-literary-20260724-b','brief_epistle_triads_catalogues_prophecy_application_remembrance_response_and_doxology_specialist'),('canonical','jude-primary-canonical-context-premortem-20260724-c','canonical_relations_Second_Temple_Enochic_angel_Moses_Balaam_invective_Jewish_patristic_reception_and_premortem_specialist')),peer_attempt='jude-peer-crosscheck-20260724-d',boss_attempt='jude-boss-adjudicator-20260724-e',post_attempt='jude-role-separated-postchecker-20260724-f',relation_specs=relations,reviewer_hint='human_or_external_ai_Koine_Greek_Jude_textual_Second_Temple_Enochic_Moses_literary_and_reception_specialist')