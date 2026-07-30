from __future__ import annotations
import sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from build_review_artifacts_generic import build
E='514c16d019d7818e6b3bbaa9b265d2b85d477450ea5ba11be59904aafed46f60'
def ids(a,b):return [f'M7_sol-Zech-{i:03d}' for i in range(a,b+1)]
relations=(
('001',ids(1,1),['Deut.30.1-Deut.30.20','Jer.3.11-Jer.4.4','Hag.1.1-Hag.1.15'],'return_word_event_ancestors_and_response_relations'),
('002',ids(2,4),['Job.1.1-Job.2.13','Ezek.1.1-Ezek.3.27','Ezek.40.1-Ezek.48.35','Rev.6.1-Rev.6.17','Rev.21.1-Rev.22.21'],'patrol_horns_measurement_vision_dialogue_relations'),
('003',ids(5,6),['Lev.16.1-Lev.16.34','Ezra.3.1-Ezra.6.22','Hag.2.1-Hag.2.23','Rev.11.1-Rev.11.19'],'Joshua_clothing_branch_stone_lampstand_olive_tree_relations'),
('004',ids(7,10),['Deut.27.1-Deut.28.68','Ezek.2.1-Ezek.3.27','1Kgs.22.1-1Kgs.22.40','Jer.23.1-Jer.23.40'],'scroll_ephah_chariots_crown_branch_sign_act_relations'),
('005',ids(11,15),['Isa.58.1-Isa.58.14','Jer.7.1-Jer.7.34','Isa.2.1-Isa.2.5','Mic.4.1-Mic.4.13','Hag.1.1-Hag.2.23'],'fasting_justice_restoration_peace_nations_relations'),
('006',ids(16,19),['Ps.72.1-Ps.72.20','Isa.9.1-Isa.11.16','Hos.1.1-Hos.3.5','Mic.5.1-Mic.5.15','Matt.21.1-Matt.21.11','John.12.12-John.12.19'],'burden_cities_royal_arrival_covenant_prisoners_shepherd_gathering_relations'),
('007',ids(20,22),['Jer.23.1-Jer.23.40','Ezek.34.1-Ezek.34.31','Matt.26.1-Matt.27.66'],'forest_lament_slaughter_flock_staffs_wages_and_foolish_shepherd_relations'),
('008',ids(23,24),['Joel.3.1-Joel.3.21','John.19.31-John.19.42','Rev.1.1-Rev.1.20'],'siege_defense_poured_supplication_piercing_mourning_and_fountain_relations'),
('009',ids(25,26),['Deut.13.1-Deut.13.18','Ezek.36.1-Ezek.36.38','Matt.26.31-Matt.26.35','Mark.14.27-Mark.14.31'],'prophet_removal_wounds_struck_shepherd_scattering_and_refining_relations'),
('010',ids(27,28),['Joel.3.1-Joel.3.21','Ezek.47.1-Ezek.48.35','Mal.3.1-Mal.4.6','Rev.21.1-Rev.22.21'],'day_battle_living_waters_kingship_plague_pilgrimage_and_holiness_relations'))
build(book='Zech',expected_sha=E,roles=(('hebrew','zech-primary-hebrew-textual-20260723-a','Hebrew_vision_oracle_speaker_textual_translation_specialist'),('literary','zech-primary-literary-20260723-b','vision_dialogue_sign_act_burden_lament_form_specialist'),('canonical','zech-primary-canonical-premortem-20260723-c','canonical_relations_prooftext_identity_fulfillment_premortem_specialist')),peer_attempt='zech-peer-crosscheck-20260723-d',boss_attempt='zech-boss-adjudicator-20260723-e',post_attempt='zech-role-separated-postchecker-20260723-f',relation_specs=relations,reviewer_hint='human_or_external_ai_Biblical_Hebrew_Zechariah_vision_oracle_textual_Second_Temple_ancient_Jewish_reception_specialist')
