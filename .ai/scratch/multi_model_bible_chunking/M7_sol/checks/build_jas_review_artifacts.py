from __future__ import annotations
import sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from build_review_artifacts_generic import build
E='1c2ed27c61cb3131728feb0cb21df28ec7a2e68eb5558eb3a3c3ee3e79e6f26c'
def ids(a,b):return [f'M7_sol-Jas-{i:03d}' for i in range(a,b+1)]
relations=(
('001',ids(1,3),['Deut.8.1-Deut.8.20','Prov.2.1-Prov.3.35'],'prescript_trials_wisdom_rich_reversal_temptation_gift_word_hearing_doing_and_religion_relations'),
('002',ids(4,5),['Gen.15.1-Gen.15.21','Gen.22.1-Gen.22.24','Lev.19.1-Lev.19.37','Josh.2.1-Josh.2.24'],'partiality_scene_royal_law_judgment_mercy_faith_works_dialogue_and_examples_relations'),
('003',ids(6,7),['Gen.1.1-Gen.1.31','Prov.10.1-Prov.18.24'],'teacher_tongue_analogy_blessing_cursing_and_above_below_wisdom_relations'),
('004',ids(8,10),['Prov.3.1-Prov.3.35','Prov.27.1-Prov.27.27'],'desire_conflict_friendship_grace_repentance_judging_law_and_merchant_presumption_relations'),
('005',ids(11,11),['Isa.5.1-Isa.5.30','Amos.2.1-Amos.8.14'],'rich_address_wealth_wages_cries_luxury_and_righteous_one_warning_relations'),
('006',ids(12,13),['Job.1.1-Job.2.13','Job.42.1-Job.42.17','Matt.5.1-Matt.5.48'],'patience_farmer_prophets_job_compassion_oath_and_yes_no_relations'),
('007',ids(14,15),['1Kgs.17.1-1Kgs.18.46','Prov.10.1-Prov.10.32'],'suffering_prayer_praise_elders_oil_confession_elijah_and_restoration_close_relations'))
build(book='Jas',expected_sha=E,roles=(('greek','jas-primary-greek-textual-20260724-a','Koine_Greek_wisdom_dialogue_speaker_textual_translation_and_prayer_specialist'),('literary','jas-primary-literary-20260724-b','wisdom_diatribe_case_analogy_example_warning_and_prayer_register_specialist'),('canonical','jas-primary-canonical-context-premortem-20260724-c','canonical_relations_Second_Temple_Jewish_wisdom_rabbinic_reception_and_premortem_specialist')),peer_attempt='jas-peer-crosscheck-20260724-d',boss_attempt='jas-boss-adjudicator-20260724-e',post_attempt='jas-role-separated-postchecker-20260724-f',relation_specs=relations,reviewer_hint='human_or_external_ai_Koine_Greek_James_wisdom_dialogue_textual_literary_and_Jewish_context_specialist')