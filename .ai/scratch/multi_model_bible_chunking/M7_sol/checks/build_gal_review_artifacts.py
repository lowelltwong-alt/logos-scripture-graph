from __future__ import annotations
import sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from build_review_artifacts_generic import build
E='f012440aa25ecd4e31bf4b51d37a130fe61d2592dd4de15e408c32c116cd6e40'
def ids(a,b):return [f'M7_sol-Gal-{i:03d}' for i in range(a,b+1)]
relations=(
('001',ids(1,2),['Acts.1.1-Acts.28.31','Rom.1.1-Rom.16.25'],'prescript_grace_peace_rebuke_rival_message_anathema_and_servant_claim_relations'),
('002',ids(3,6),['Acts.9.1-Acts.15.41','Gen.17.1-Gen.17.27'],'commission_autobiography_Jerusalem_consultation_mission_recognition_Antioch_confrontation_and_speech_relations'),
('003',ids(7,8),['Gen.12.1-Gen.22.24','Deut.21.1-Deut.21.23','Deut.27.1-Deut.30.20','Hab.2.1-Hab.2.20'],'hearing_faith_Abraham_blessing_curse_redemption_and_Gentile_promise_relations'),
('004',ids(9,12),['Gen.12.1-Gen.22.24','Exod.19.1-Exod.24.18','Isa.54.1-Isa.54.17'],'covenant_promise_law_purpose_pedagogue_baptismal_unity_heir_guardian_adoption_and_return_warning_relations'),
('005',ids(13,14),['Gen.16.1-Gen.21.34','Isa.54.1-Isa.54.17'],'personal_appeal_remembered_relationship_birth_pangs_Hagar_Sarah_allegory_and_application_relations'),
('006',ids(15,18),['Lev.19.1-Lev.19.37','Deut.10.1-Deut.10.22','Deut.30.1-Deut.30.20'],'freedom_circumcision_warning_love_leaven_flesh_Spirit_conflict_vice_and_fruit_catalogues_relations'),
('007',ids(19,21),['Deut.15.1-Deut.15.23','Ps.125.1-Ps.126.6','Rom.1.1-Rom.16.25'],'restoration_burdens_self_test_sharing_sowing_reaping_doing_good_autograph_boasting_marks_and_benediction_relations'))
build(book='Gal',expected_sha=E,roles=(('greek','gal-primary-greek-textual-20260724-a','Koine_Greek_epistolary_argument_textual_translation_quotation_specialist'),('literary','gal-primary-literary-20260724-b','epistolary_autobiography_proof_analogy_allegory_list_specialist'),('canonical','gal-primary-canonical-context-premortem-20260724-c','canonical_relations_Second_Temple_rabbinic_chronology_premortem_specialist')),peer_attempt='gal-peer-crosscheck-20260724-d',boss_attempt='gal-boss-adjudicator-20260724-e',post_attempt='gal-role-separated-postchecker-20260724-f',relation_specs=relations,reviewer_hint='human_or_external_ai_Koine_Greek_Galatians_epistolary_argument_textual_chronology_specialist')