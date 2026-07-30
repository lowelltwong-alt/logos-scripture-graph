from __future__ import annotations
import sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from build_review_artifacts_generic import build
E='b0f022ea605d69824b714cd78d8f601709380da03c1f23d45fd1f790338a1b8f'
def ids(a,b):return [f'M7_sol-Phlm-{i:03d}' for i in range(a,b+1)]
relations=(
('001',ids(1,2),['Col.1.1-Col.1.14'],'prescript_thanksgiving_prayer_love_faith_fellowship_and_refreshment_relations'),
('002',ids(3,4),['Exod.21.1-Exod.21.36','Deut.15.1-Deut.15.23'],'boldness_love_appeal_kinship_sending_retention_consent_separation_and_reception_relations'),
('003',ids(5,5),['Prov.11.1-Prov.11.31','Matt.18.1-Matt.18.35'],'partnership_welcome_wrong_debt_account_autograph_refresh_confidence_and_lodging_relations'),
('004',ids(6,6),['Col.4.1-Col.4.18'],'co_worker_greeting_register_and_grace_close_relations'))
build(book='Phlm',expected_sha=E,roles=(('greek','phlm-primary-greek-textual-20260724-a','Koine_Greek_epistolary_appeal_account_textual_translation_and_close_specialist'),('literary','phlm-primary-literary-20260724-b','epistolary_rhetorical_appeal_account_request_and_close_specialist'),('canonical','phlm-primary-canonical-context-premortem-20260724-c','canonical_relations_ancient_letter_legal_language_Jewish_context_and_premortem_specialist')),peer_attempt='phlm-peer-crosscheck-20260724-d',boss_attempt='phlm-boss-adjudicator-20260724-e',post_attempt='phlm-role-separated-postchecker-20260724-f',relation_specs=relations,reviewer_hint='human_or_external_ai_Koine_Greek_Philemon_literary_legal_language_social_hazard_and_close_specialist')