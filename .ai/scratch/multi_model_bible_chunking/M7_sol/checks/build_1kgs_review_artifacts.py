from build_review_artifacts_generic import build

if __name__=='__main__':
    build(
      book='1Kgs',expected_sha='50dd96ed5ae0875fdeac0873d7252495f68245168aed47813cd74d53820c31e2',
      roles=(('hebrew','1kgs-primary-hebrew-20260722-a','original_language_translation_specialist'),('literary','1kgs-primary-literary-20260722-b','literary_form_specialist'),('canonical','1kgs-primary-canonical-20260722-c','canonical_intertext_and_premortem_specialist')),
      peer_attempt='1kgs-peer-crosscheck-20260722-d',boss_attempt='1kgs-boss-adjudicator-20260722-e',post_attempt='1kgs-post-resolution-checker-20260722-f',
      reviewer_hint='human_or_external_ai_Hebrew_literary_temple_regnal_trauma_aware_and_ancient_context_specialist',
      relation_specs=(
       ('001',['M7_sol-1Kgs-001','M7_sol-1Kgs-002'],['2Sam.7.1-2Sam.7.29','2Sam.15.1-2Sam.20.26','Deut.17.14-Deut.17.20'],'succession_charge_and_kingship_law_relations'),
       ('002',['M7_sol-1Kgs-002'],['1Sam.2.27-1Sam.3.21'],'Abiathar_removal_and_Eli_house_oracle_relation'),
       ('003',['M7_sol-1Kgs-008','M7_sol-1Kgs-009','M7_sol-1Kgs-010','M7_sol-1Kgs-011','M7_sol-1Kgs-012','M7_sol-1Kgs-013','M7_sol-1Kgs-014','M7_sol-1Kgs-015','M7_sol-1Kgs-016','M7_sol-1Kgs-017','M7_sol-1Kgs-018'],['Exod.25.1-Exod.40.38','Deut.12.1-Deut.12.14','2Sam.7.1-2Sam.7.17','Ps.132.1-Ps.132.18','2Chr.2.1-2Chr.7.22'],'temple_ark_dedication_and_parallel_relations'),
       ('004',['M7_sol-1Kgs-020','M7_sol-1Kgs-021'],['2Chr.9.1-2Chr.9.28','Matt.12.42-Matt.12.42','Luke.11.31-Luke.11.31'],'Sheba_visit_wealth_and_later_reuse_relations'),
       ('005',['M7_sol-1Kgs-022','M7_sol-1Kgs-023','M7_sol-1Kgs-024','M7_sol-1Kgs-025'],['Deut.7.1-Deut.7.6','Deut.17.14-Deut.17.20','Neh.13.26-Neh.13.27'],'Solomon_reported_change_adversaries_Jeroboam_and_death_relations'),
       ('006',['M7_sol-1Kgs-026','M7_sol-1Kgs-027','M7_sol-1Kgs-028','M7_sol-1Kgs-029','M7_sol-1Kgs-030'],['2Chr.10.1-2Chr.12.16','2Kgs.23.15-2Kgs.23.20'],'kingdom_division_Jeroboam_policy_and_later_sign_fulfillment_relations'),
       ('007',['M7_sol-1Kgs-034','M7_sol-1Kgs-035','M7_sol-1Kgs-036'],['1Kgs.14.1-1Kgs.16.34'],'regnal_oracle_coup_and_Ahab_transition_relations'),
       ('008',['M7_sol-1Kgs-037','M7_sol-1Kgs-038','M7_sol-1Kgs-039','M7_sol-1Kgs-040','M7_sol-1Kgs-041','M7_sol-1Kgs-042','M7_sol-1Kgs-043'],['Exod.19.1-Exod.20.21','Luke.4.25-Luke.4.26','Rom.11.2-Rom.11.4','Jas.5.17-Jas.5.18'],'Elijah_drought_widow_Carmel_Horeb_and_later_reuse_relations'),
       ('009',['M7_sol-1Kgs-044','M7_sol-1Kgs-045','M7_sol-1Kgs-046'],['Exod.20.13-Exod.20.17','Deut.19.15-Deut.19.21','2Kgs.9.25-2Kgs.9.26'],'Ahab_war_treaty_Naboth_legal_and_bloodguilt_relations'),
       ('010',['M7_sol-1Kgs-047','M7_sol-1Kgs-048','M7_sol-1Kgs-049'],['2Chr.18.1-2Chr.20.37','Isa.6.1-Isa.6.13','Jer.23.16-Jer.23.22'],'Micaiah_council_battle_Ahab_death_and_regnal_closure_relations')))
