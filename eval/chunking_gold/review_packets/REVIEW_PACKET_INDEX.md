# Review Packet Index And Promotion Queue

Status: diagnostic/control surface with later owner decisions. T319 did not authorize
output-changing work or add reviewed gold; T337B later authorizes only the exact Psalm 89 Option C
reviewed-gold target, and T344 later authorizes only Revelation research/prep under REV-T344-E.
This index does not change evaluator policy.

Current post-T327 canonical-66 baseline is D / Claude pass2 = 93.6 under the unchanged T314 reviewed-structural-split evaluator policy. The prior 93.5 row is a pre-T327 wider-corpus baseline. This movement is corpus-scope correction / baseline reset, not chunking improvement.

## Source Surfaces

- `eval/chunking_gold/review_packets`
- `eval/chunking_gold/per_form/psalms_gold_manifest.json`
- `eval/chunking_gold/stress_atlas/observed_stress_behavior.json`
- `eval/chunking_gold/stress_atlas/OBSERVED_STRESS_BEHAVIOR.md`
- `eval/chunking_gold/GOLD_COVERAGE_INVENTORY.md`

## Summary

- Total entries: 64
- Reviewed gold entries: 15
- Pending human review: 15
- Needs review packet: 23
- Variant policy required: 2
- Speaker review required: 5
- Source/tradition review required: 3
- Manual investigation required: 1

## Promotion Queue

The queue is a review queue, not an implementation queue. Every queued item has `implementation_allowed: false` and `output_change_authorized: false`. Psalm 89 was removed from the queue by the T337B owner decision.

| Priority | Case | Status | Next action | Gate |
| ---: | --- | --- | --- | --- |
| 1 | `jeremiah_mt_lxx_divergence` | `manual_investigation_required` | `manual_investigation_required` | `manual_investigation_before_packet` |
| 2 | `1sam10_27_11_1_dss_nahash` | `variant_policy_required` | `define_variant_policy_before_gold` | `variant_policy_before_gold` |
| 3 | `deut32_8_9_divine_council_variant` | `variant_policy_required` | `define_variant_policy_before_gold` | `variant_policy_before_gold` |
| 4 | `gospels_wj_marker_spans` | `speaker_review_required` | `define_speaker_policy_before_gold` | `speaker_boundary_review_before_gold` |
| 5 | `john13_17_farewell_discourse` | `speaker_review_required` | `define_speaker_policy_before_gold` | `speaker_boundary_review_before_gold` |
| 6 | `john13_17_wj_farewell_discourse_marker_focus` | `speaker_review_required` | `define_speaker_policy_before_gold` | `speaker_boundary_review_before_gold` |
| 7 | `rev12_18_vision_cycle` | `speaker_review_required` | `define_speaker_policy_before_gold` | `speaker_boundary_review_before_gold` |
| 8 | `synoptic_apocalyptic_wj_discourses` | `speaker_review_required` | `define_speaker_policy_before_gold` | `speaker_boundary_review_before_gold` |
| 9 | `deut32_song_of_moses` | `source_tradition_review_required` | `define_source_tradition_policy_before_gold` | `source_tradition_review_before_gold` |
| 10 | `gen6_1_4_sons_of_god` | `source_tradition_review_required` | `define_source_tradition_policy_before_gold` | `source_tradition_review_before_gold` |
| 11 | `jude5_15_examples_and_enoch` | `source_tradition_review_required` | `define_source_tradition_policy_before_gold` | `source_tradition_review_before_gold` |
| 12 | `isa52_13_53_12_servant_song` | `pending_human_review` | `await_human_review` | `human_review_required` |
| 13 | `john3_wj_speaker_boundary` | `pending_human_review` | `await_human_review` | `human_review_required` |
| 14 | `john7_53_8_11_pericope_adulterae` | `pending_human_review` | `await_human_review` | `human_review_required` |
| 15 | `john7_53_8_11_wj_variant_speech` | `pending_human_review` | `await_human_review` | `human_review_required` |
| 16 | `mark16_9_20_longer_ending` | `pending_human_review` | `await_human_review` | `human_review_required` |
| 17 | `matt5_7_sermon_on_mount_wj_discourse` | `pending_human_review` | `await_human_review` | `human_review_required` |
| 18 | `rev12_14_symbolic_scenes` | `pending_human_review` | `continue_revelation_research_prep` | `research_prep_before_gold` |
| 19 | `ps136_refrain_litany` | `pending_human_review` | `await_human_review` | `human_review_required` |
| 20 | `1chr1_9_primeval_genealogies` | `needs_review_packet` | `create_review_packet` | `create_review_packet_before_gold` |
| 21 | `1cor8_10_food_offered_to_idols` | `needs_review_packet` | `create_review_packet` | `create_review_packet_before_gold` |
| 22 | `1kgs22_micaiah_council_scene` | `needs_review_packet` | `create_review_packet` | `create_review_packet_before_gold` |
| 23 | `1pet3_18_22_spirits_prison` | `needs_review_packet` | `create_review_packet` | `create_review_packet_before_gold` |
| 24 | `dan10_12_final_vision` | `needs_review_packet` | `create_review_packet` | `create_review_packet_before_gold` |
| 25 | `eph1_3_14_greek_sentence` | `needs_review_packet` | `create_review_packet` | `create_review_packet_before_gold` |
| ... | 19 additional queued cases |  |  |  |

## Reviewed Gold Entries

These entries record existing reviewed decisions plus the later T337B Psalm 89 owner decision.

| Entry | Case | Passage | Decision | Source |
| --- | --- | --- | --- | --- |
| `packet_ps105_boundary_review` | `ps105_historical_psalm` | Ps.105 | `approved_preserve_current_whole_psalm` | `eval/chunking_gold/review_packets/ps105_boundary_review.md` |
| `packet_ps106_boundary_review` | `ps106_historical_confession` | Ps.106 | `approved_preserve_current_whole_psalm` | `eval/chunking_gold/review_packets/ps106_boundary_review.md` |
| `packet_ps78_boundary_review` | `ps78_parent_child_structural_split` | Ps.78.1-Ps.78.72 | `approved_structural_split_under_parent_whole_psalm` | `eval/chunking_gold/review_packets/ps78_boundary_review.md` |
| `packet_ps89_boundary_review` | `ps89_royal_lament` | Ps.89.1-Ps.89.52 | `approved_with_scope_note` | `eval/chunking_gold/review_packets/ps89_boundary_review.md` |
| `manifest_ps23_whole_psalm` | `ps23_whole_psalm` | Ps.23.1-Ps.23.6 | `reviewed_gold` | `eval/chunking_gold/per_form/psalms_gold_manifest.json` |
| `manifest_ps119_acrostic_sections` | `ps119_acrostic_sections` | Ps.119.1-Ps.119.176 | `reviewed_gold` | `eval/chunking_gold/per_form/psalms_gold_manifest.json` |
| `manifest_short_psalm_holdouts` | `short_psalm_holdouts` | Ps.1; Ps.8; Ps.100; Ps.117 | `reviewed_gold` | `eval/chunking_gold/per_form/psalms_gold_manifest.json` |
| `manifest_ps3_superscription_attached` | `ps3_superscription_attached` | Ps.3.1-Ps.3.8 | `reviewed_gold` | `eval/chunking_gold/per_form/psalms_gold_manifest.json` |
| `manifest_non_target_poetry_controls` | `non_target_poetry_controls` | Song; Lam | `reviewed_gold` | `eval/chunking_gold/per_form/psalms_gold_manifest.json` |
| `manifest_ps78_parent_child_structural_split` | `ps78_parent_child_structural_split` | Ps.78.1-Ps.78.72 | `approved_structural_split_under_parent_whole_psalm` | `eval/chunking_gold/per_form/psalms_gold_manifest.json` |
| `manifest_ps105_whole_psalm` | `ps105_whole_psalm` | Ps.105.1-Ps.105.45 | `approved_preserve_current_whole_psalm` | `eval/chunking_gold/per_form/psalms_gold_manifest.json` |
| `manifest_ps106_whole_psalm_with_b_marker_note` | `ps106_whole_psalm_with_b_marker_note` | Ps.106.1-Ps.106.48 | `approved_preserve_current_whole_psalm` | `eval/chunking_gold/per_form/psalms_gold_manifest.json` |
| `manifest_ps89_owner_decision_option_c` | `ps89_owner_decision_option_c` | Ps.89.1-Ps.89.52 | `approved_with_scope_note` | `eval/chunking_gold/per_form/psalms_gold_manifest.json` |
| `observed_ps105_historical_psalm` | `ps105_historical_psalm` | Ps.105 | `approved_preserve_current_behavior` | `eval/chunking_gold/stress_atlas/observed_stress_behavior.json` |
| `observed_ps106_historical_confession` | `ps106_historical_confession` | Ps.106 | `approved_preserve_current_behavior` | `eval/chunking_gold/stress_atlas/observed_stress_behavior.json` |

## Pending And Policy-Required Entries

| Entry | Case | Status | Decision | Rules |
| --- | --- | --- | --- | --- |
| `packet_isa52_13_53_12_boundary_review` | `isa52_13_53_12_servant_song` | `pending_human_review` | `pending` | `no_new_reviewed_gold_t319`, `pending_packets_non_authorizing`, `review_packet_required_before_implementation` |
| `packet_john3_wj_speaker_boundary_review` | `john3_wj_speaker_boundary` | `pending_human_review` | `pending` | `no_new_reviewed_gold_t319`, `pending_packets_non_authorizing`, `speaker_review_required`, `wj_evidence_not_authority` |
| `packet_john7_53_8_11_textual_variant_review` | `john7_53_8_11_pericope_adulterae` | `pending_human_review` | `pending` | `no_new_reviewed_gold_t319`, `pending_packets_non_authorizing`, `speaker_review_required`, `variant_policy_before_gold` |
| `packet_mark16_9_20_textual_variant_review` | `mark16_9_20_longer_ending` | `pending_human_review` | `pending` | `no_new_reviewed_gold_t319`, `pending_packets_non_authorizing`, `variant_policy_before_gold` |
| `packet_matt5_7_wj_discourse_review` | `matt5_7_sermon_on_mount_wj_discourse` | `pending_human_review` | `pending` | `no_new_reviewed_gold_t319`, `parent_child_structural_review`, `pending_packets_non_authorizing`, `speaker_review_required`, `wj_evidence_not_authority` |
| `packet_rev12_14_symbolic_scenes_review` | `rev12_14_symbolic_scenes` | `pending_human_review` | `requires_more_research_before_gold` | `no_new_reviewed_gold_t319`, `pending_packets_non_authorizing`, `rev_t344_e_research_only_non_authorizing`, `review_packet_required_before_implementation`, `speaker_review_required`, `wj_evidence_not_authority` |
| `packet_ps136_boundary_review` | `ps136_refrain_litany` | `pending_human_review` | `pending` | `no_new_reviewed_gold_t319`, `pending_packets_non_authorizing`, `review_packet_required_before_implementation` |
| `observed_ps89_royal_lament` | `ps89_royal_lament` | `pending_human_review` | `pending` | `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `pending_packets_non_authorizing`, `qs_evidence_not_boundary_authority` |
| `observed_ps136_refrain_litany` | `ps136_refrain_litany` | `pending_human_review` | `pending` | `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `pending_packets_non_authorizing` |
| `observed_lam1_4_acrostic_poems` | `lam1_4_acrostic_poems` | `needs_review_packet` | `needs_review_packet` | `current_split_not_automatically_bad_fragmentation`, `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `review_packet_required_before_implementation` |
| `observed_prov31_10_31_acrostic_woman` | `prov31_10_31_acrostic_woman` | `needs_review_packet` | `needs_review_packet` | `current_split_not_automatically_bad_fragmentation`, `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `review_packet_required_before_implementation` |
| `observed_job38_41_divine_speeches` | `job38_41_divine_speeches` | `needs_review_packet` | `needs_review_packet` | `current_split_not_automatically_bad_fragmentation`, `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `review_packet_required_before_implementation` |
| `observed_deut32_song_of_moses` | `deut32_song_of_moses` | `source_tradition_review_required` | `source_tradition_review_required` | `current_split_not_automatically_bad_fragmentation`, `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `source_tradition_review_required`, `variant_policy_before_gold` |
| `observed_isa52_13_53_12_servant_song` | `isa52_13_53_12_servant_song` | `pending_human_review` | `pending` | `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `pending_packets_non_authorizing` |
| `observed_dan10_12_final_vision` | `dan10_12_final_vision` | `needs_review_packet` | `needs_review_packet` | `current_split_not_automatically_bad_fragmentation`, `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `review_packet_required_before_implementation` |
| `observed_rev12_18_vision_cycle` | `rev12_18_vision_cycle` | `speaker_review_required` | `speaker_review_required` | `current_split_not_automatically_bad_fragmentation`, `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `speaker_review_required`, `wj_evidence_not_authority` |
| `observed_eph1_3_14_greek_sentence` | `eph1_3_14_greek_sentence` | `needs_review_packet` | `needs_review_packet` | `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `review_packet_required_before_implementation` |
| `observed_mark16_9_20_longer_ending` | `mark16_9_20_longer_ending` | `pending_human_review` | `pending` | `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `pending_packets_non_authorizing`, `speaker_review_required`, `variant_policy_before_gold`, `wj_evidence_not_authority` |
| `observed_john7_53_8_11_pericope_adulterae` | `john7_53_8_11_pericope_adulterae` | `pending_human_review` | `pending` | `current_split_not_automatically_bad_fragmentation`, `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `pending_packets_non_authorizing`, `speaker_review_required`, `variant_policy_before_gold`, `wj_evidence_not_authority` |
| `observed_jeremiah_mt_lxx_divergence` | `jeremiah_mt_lxx_divergence` | `manual_investigation_required` | `unknown_needs_human_review` | `manual_investigation_required`, `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `variant_policy_before_gold` |
| `observed_1sam10_27_11_1_dss_nahash` | `1sam10_27_11_1_dss_nahash` | `variant_policy_required` | `variant_policy_required` | `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `variant_policy_before_gold` |
| `observed_gen6_1_4_sons_of_god` | `gen6_1_4_sons_of_god` | `source_tradition_review_required` | `source_tradition_review_required` | `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `source_tradition_review_required`, `variant_policy_before_gold` |
| `observed_deut32_8_9_divine_council_variant` | `deut32_8_9_divine_council_variant` | `variant_policy_required` | `variant_policy_required` | `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `variant_policy_before_gold` |
| `observed_ps82_divine_council` | `ps82_divine_council` | `needs_review_packet` | `needs_review_packet` | `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `qs_evidence_not_boundary_authority`, `review_packet_required_before_implementation` |
| `observed_1kgs22_micaiah_council_scene` | `1kgs22_micaiah_council_scene` | `needs_review_packet` | `needs_review_packet` | `current_split_not_automatically_bad_fragmentation`, `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `review_packet_required_before_implementation` |
| `observed_ezek1_throne_vision` | `ezek1_throne_vision` | `needs_review_packet` | `needs_review_packet` | `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `review_packet_required_before_implementation` |
| `observed_ezek40_48_temple_vision` | `ezek40_48_temple_vision` | `needs_review_packet` | `needs_review_packet` | `current_split_not_automatically_bad_fragmentation`, `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `review_packet_required_before_implementation` |
| `observed_zech1_6_night_visions` | `zech1_6_night_visions` | `needs_review_packet` | `needs_review_packet` | `current_split_not_automatically_bad_fragmentation`, `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `review_packet_required_before_implementation` |
| `observed_matt24_25_olivet_discourse` | `matt24_25_olivet_discourse` | `needs_review_packet` | `needs_review_packet` | `current_split_not_automatically_bad_fragmentation`, `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `review_packet_required_before_implementation`, `speaker_review_required`, `wj_evidence_not_authority` |
| `observed_john13_17_farewell_discourse` | `john13_17_farewell_discourse` | `speaker_review_required` | `speaker_review_required` | `current_split_not_automatically_bad_fragmentation`, `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `speaker_review_required`, `wj_evidence_not_authority` |
| `observed_rom9_11_argument` | `rom9_11_argument` | `needs_review_packet` | `needs_review_packet` | `current_split_not_automatically_bad_fragmentation`, `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `review_packet_required_before_implementation` |
| `observed_1pet3_18_22_spirits_prison` | `1pet3_18_22_spirits_prison` | `needs_review_packet` | `needs_review_packet` | `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `review_packet_required_before_implementation` |
| `observed_jude5_15_examples_and_enoch` | `jude5_15_examples_and_enoch` | `source_tradition_review_required` | `source_tradition_review_required` | `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `source_tradition_review_required`, `variant_policy_before_gold` |
| `observed_esth8_9_long_administrative_verse` | `esth8_9_long_administrative_verse` | `needs_review_packet` | `needs_review_packet` | `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `review_packet_required_before_implementation` |
| `observed_matt1_genealogy` | `matt1_genealogy` | `needs_review_packet` | `needs_review_packet` | `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `review_packet_required_before_implementation` |
| `observed_luke3_genealogy` | `luke3_genealogy` | `needs_review_packet` | `needs_review_packet` | `current_split_not_automatically_bad_fragmentation`, `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `review_packet_required_before_implementation` |
| `observed_1chr1_9_primeval_genealogies` | `1chr1_9_primeval_genealogies` | `needs_review_packet` | `needs_review_packet` | `current_split_not_automatically_bad_fragmentation`, `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `review_packet_required_before_implementation` |
| `observed_josh13_21_land_allotments` | `josh13_21_land_allotments` | `needs_review_packet` | `needs_review_packet` | `current_split_not_automatically_bad_fragmentation`, `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `review_packet_required_before_implementation` |
| `observed_lev16_day_of_atonement` | `lev16_day_of_atonement` | `needs_review_packet` | `needs_review_packet` | `current_split_not_automatically_bad_fragmentation`, `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `review_packet_required_before_implementation` |
| `observed_exod20_23_covenant_code` | `exod20_23_covenant_code` | `needs_review_packet` | `needs_review_packet` | `current_split_not_automatically_bad_fragmentation`, `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `review_packet_required_before_implementation` |
| `observed_heb7_10_priesthood_argument` | `heb7_10_priesthood_argument` | `needs_review_packet` | `needs_review_packet` | `current_split_not_automatically_bad_fragmentation`, `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `review_packet_required_before_implementation` |
| `observed_1cor8_10_food_offered_to_idols` | `1cor8_10_food_offered_to_idols` | `needs_review_packet` | `needs_review_packet` | `current_split_not_automatically_bad_fragmentation`, `no_new_reviewed_gold_t319`, `observed_audit_non_authorizing`, `review_packet_required_before_implementation` |
| ... | 7 additional pending/policy entries |  |  |  |

## Governance Boundary

- Pending review packets do not authorize output changes.
- T337B authorizes only the exact Psalm 89 Option C target.
- Observed audit entries do not authorize output changes.
- Textual-variant entries are not reviewed gold unless already explicitly reviewed.
- Words-of-Jesus entries require speaker review unless already reviewed.
- Boundary/source-tradition entries require source/tradition review.
- Current containment is not automatically approved preservation.
- Current splitting is not automatically bad fragmentation.
- `implementation_allowed` remains `false` for every queued or non-authorized entry.
- T319 adds no reviewed gold and authorizes no output-changing work; T337B is a later owner decision.
