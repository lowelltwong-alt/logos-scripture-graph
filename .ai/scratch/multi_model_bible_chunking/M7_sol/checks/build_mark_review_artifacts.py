from __future__ import annotations
import sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from build_review_artifacts_generic import build
E='917b5cccd8445a016970450b9d86c8514d68ffd3b44ecce91f66b4e1a8651c2f'
def ids(a,b):return [f'M7_sol-Mark-{i:03d}' for i in range(a,b+1)]
relations=(
('001',ids(1,6),['Exod.23.20-Exod.23.33','Mal.3.1-Mal.3.5','Isa.40.1-Isa.40.11','Matt.3.1-Matt.4.25','Luke.3.1-Luke.5.16'],'opening_preparation_baptism_testing_call_and_healing_relations'),
('002',ids(7,13),['Lev.13.1-Lev.14.57','1Sam.21.1-1Sam.21.9','Hos.6.1-Hos.6.11','Isa.5.1-Isa.5.30','Matt.9.1-Matt.12.50'],'healing_table_fasting_Sabbath_Twelve_family_and_scribes_relations'),
('003',ids(14,17),['Ps.78.1-Ps.78.72','Jonah.1.1-Jonah.2.10','1Kgs.17.1-1Kgs.17.24','2Kgs.4.1-2Kgs.4.44','Matt.13.1-Matt.14.36'],'parable_sea_deliverance_and_intercalated_healing_relations'),
('004',ids(18,24),['1Kgs.17.1-1Kgs.19.21','Exod.16.1-Exod.17.16','Num.11.1-Num.11.35','2Kgs.4.38-2Kgs.4.44','Matt.10.1-Matt.15.28'],'rejection_mission_John_feeding_sea_purity_and_Gentile_relations'),
('005',ids(25,31),['Exod.24.1-Exod.34.35','Isa.35.1-Isa.35.10','Dan.7.1-Dan.7.28','Mal.4.1-Mal.4.6','Matt.15.29-Matt.17.21'],'healing_feeding_sign_confession_prediction_transfiguration_and_exorcism_relations'),
('006',ids(32,38),['Gen.1.1-Gen.2.25','Deut.24.1-Deut.24.22','Isa.53.1-Isa.53.12','Matt.17.22-Matt.20.34','Luke.9.43-Luke.18.43'],'community_divorce_children_wealth_passion_service_and_healing_relations'),
('007',ids(39,47),['Ps.110.1-Ps.110.7','Ps.118.1-Ps.118.29','Isa.5.1-Isa.5.30','Isa.56.1-Isa.56.12','Jer.7.1-Jer.7.34','Zech.9.1-Zech.14.21'],'entry_fig_temple_authority_tenant_tax_resurrection_command_and_widow_relations'),
('008',ids(48,51),['Dan.7.1-Dan.7.28','Dan.9.1-Dan.12.13','Zech.12.1-Zech.14.21','1Thess.4.1-1Thess.5.28','Rev.6.1-Rev.22.21'],'temple_signs_desolation_cosmic_scene_fig_lesson_and_watch_relations'),
('009',ids(52,55),['Exod.12.1-Exod.12.51','Ps.41.1-Ps.41.13','Zech.11.1-Zech.13.9','Matt.26.1-Matt.26.35','Luke.22.1-Luke.22.38'],'plot_anointing_betrayal_Passover_meal_and_denial_prediction_relations'),
('010',ids(56,59),['Ps.42.1-Ps.43.5','Ps.69.1-Ps.69.36','Zech.13.1-Zech.13.9','Matt.26.36-Matt.27.26','John.18.1-John.18.40'],'Gethsemane_arrest_hearing_denial_and_Pilate_relations'),
('011',ids(60,63),['Ps.22.1-Ps.22.31','Ps.69.1-Ps.69.36','Isa.52.1-Isa.53.12','Amos.8.1-Amos.8.14','Zech.12.1-Zech.13.9'],'mockery_crucifixion_death_witness_and_burial_relations'),
('012',ids(64,65),['Isa.52.1-Isa.53.12','Dan.7.1-Dan.7.28','Matt.28.1-Matt.28.20','Luke.24.1-Luke.24.53','John.20.1-John.21.25','Acts.1.1-Acts.2.47'],'tomb_report_received_ending_coordinate_and_Gospel_Acts_relations'))
build(book='Mark',expected_sha=E,roles=(('greek','mark-primary-greek-textual-20260723-a','Koine_Greek_discourse_textual_variant_translation_specialist'),('literary','mark-primary-literary-20260723-b','narrative_intercalation_discourse_literary_form_specialist'),('canonical','mark-primary-canonical-context-premortem-20260723-c','canonical_relations_Second_Temple_rabbinic_chronology_premortem_specialist')),peer_attempt='mark-peer-crosscheck-20260723-d',boss_attempt='mark-boss-adjudicator-20260723-e',post_attempt='mark-role-separated-postchecker-20260723-f',relation_specs=relations,reviewer_hint='human_or_external_ai_Koine_Greek_Mark_intercalation_textual_Second_Temple_ancient_Jewish_reception_specialist')