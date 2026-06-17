# Observed Stress Atlas Behavior

Status: diagnostic observation only. This audit does not authorize output-changing work, does not promote reviewed gold, and does not change evaluator policy.

Current official post-T327 canonical-66 baseline is D / Claude pass2 = 93.6 under the unchanged T314 reviewed-structural-split evaluator policy. The prior 93.5 row is a pre-T327 wider-corpus baseline. Movement between those rows is corpus-scope correction / baseline reset, not chunking improvement.

The audit was generated from a temporary local pre-T327 chunker run against the wider corpus. The chunk output itself is not committed. The observed rows remain diagnostic triage evidence only and should be refreshed before any future output-changing work cites current post-T327 behavior.

## Summary

- Stress cases audited: 44
- Fully contained in one current chunk: 16
- Split across current chunks: 25
- Mixed with extra context: 34
- Needs review packet: 19
- Review packet pending: 12
- Reviewed gold preserving current behavior: 2
- Variant-policy required: 2
- Speaker-review required: 5
- Source-tradition review required: 3
- Unknown/manual investigation required: 1

## Highest-Risk Observed Behaviors

| Case | Observed status | Current behavior | Why it is high risk |
| --- | --- | --- | --- |
| `jeremiah_mt_lxx_divergence` | `unknown_needs_human_review` | broad/diagnostic | textual or tradition policy |
| `john7_53_8_11_pericope_adulterae` | `review_packet_pending` | split, mixed with extra context | textual or tradition policy, speaker marker evidence, pending packet |
| `john7_53_8_11_wj_variant_speech` | `review_packet_pending` | split, mixed with extra context | textual or tradition policy, speaker marker evidence, pending packet |
| `mark16_9_20_longer_ending` | `review_packet_pending` | mixed with extra context, contained | textual or tradition policy, speaker marker evidence, pending packet |
| `deut32_8_9_divine_council_variant` | `variant_policy_required` | mixed with extra context, contained | textual or tradition policy |
| `isa52_13_53_12_servant_song` | `review_packet_pending` | mixed with extra context, contained | pending packet |
| `rom9_11_argument` | `review_packet_pending` | split, mixed with extra context | pending packet |
| `heb7_10_priesthood_argument` | `review_packet_pending` | split, mixed with extra context | pending packet |
| `john3_wj_speaker_boundary` | `review_packet_pending` | split, mixed with extra context | speaker marker evidence, pending packet |
| `matt5_7_sermon_on_mount_wj_discourse` | `review_packet_pending` | split, mixed with extra context | speaker marker evidence, pending packet |
| `1cor8_10_food_offered_to_idols` | `review_packet_pending` | split, mixed with extra context | pending packet |
| `synoptic_apocalyptic_wj_discourses` | `speaker_review_required` | split, mixed with extra context | speaker marker evidence |
| `rev12_18_vision_cycle` | `speaker_review_required` | split, mixed with extra context | speaker marker evidence |

## Observed Cases

| Case | Passage | Status | Chunks | Fully contained | Split | Mixed extra context | Review | Next |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| `ps89_royal_lament` | Ps.89 | `review_packet_pending` | 1 | true | false | false | `pending_human_review` | `await_human_review` |
| `ps105_historical_psalm` | Ps.105 | `reviewed_gold_preserves_current_behavior` | 1 | true | false | false | `reviewed_gold` | `none_current_behavior_acceptable` |
| `ps106_historical_confession` | Ps.106 | `reviewed_gold_preserves_current_behavior` | 1 | true | false | false | `reviewed_gold` | `none_current_behavior_acceptable` |
| `ps136_refrain_litany` | Ps.136 | `review_packet_pending` | 1 | true | false | false | `pending_human_review` | `await_human_review` |
| `lam1_4_acrostic_poems` | Lam.1-Lam.4 | `needs_review_packet` | 4 | false | true | false | `none` | `create_review_packet` |
| `prov31_10_31_acrostic_woman` | Prov.31.10-31 | `needs_review_packet` | 2 | false | true | true | `none` | `create_review_packet` |
| `job38_41_divine_speeches` | Job.38-Job.41 | `needs_review_packet` | 5 | false | true | true | `none` | `create_review_packet` |
| `deut32_song_of_moses` | Deut.32 | `source_tradition_review_required` | 2 | false | true | true | `none` | `define_source_tradition_policy_before_gold` |
| `isa52_13_53_12_servant_song` | Isa.52.13-Isa.53.12 | `review_packet_pending` | 1 | true | false | true | `pending_human_review` | `await_human_review` |
| `dan10_12_final_vision` | Dan.10-Dan.12 | `needs_review_packet` | 5 | false | true | true | `none` | `create_review_packet` |
| `rev12_18_vision_cycle` | Rev.12-Rev.18 | `speaker_review_required` | 5 | false | true | true | `none` | `define_speaker_policy_before_gold` |
| `eph1_3_14_greek_sentence` | Eph.1.3-Eph.1.14 | `review_packet_pending` | 1 | true | false | true | `pending_human_review` | `await_human_review` |
| `mark16_9_20_longer_ending` | Mark.16.9-Mark.16.20 | `review_packet_pending` | 1 | true | false | true | `pending_human_review` | `await_human_review` |
| `john7_53_8_11_pericope_adulterae` | John.7.53-John.8.11 | `review_packet_pending` | 2 | false | true | true | `pending_human_review` | `await_human_review` |
| `jeremiah_mt_lxx_divergence` | Jeremiah MT/LXX divergence | `unknown_needs_human_review` | 0 | false | false | false | `none` | `manual_investigation_required` |
| `1sam10_27_11_1_dss_nahash` | 1Sam.10.27-1Sam.11.1 | `variant_policy_required` | 1 | true | false | true | `none` | `define_variant_policy_before_gold` |
| `gen6_1_4_sons_of_god` | Gen.6.1-Gen.6.4 | `source_tradition_review_required` | 1 | true | false | true | `none` | `define_source_tradition_policy_before_gold` |
| `deut32_8_9_divine_council_variant` | Deut.32.8-Deut.32.9 | `variant_policy_required` | 1 | true | false | true | `none` | `define_variant_policy_before_gold` |
| `ps82_divine_council` | Ps.82 | `needs_review_packet` | 1 | true | false | false | `none` | `create_review_packet` |
| `1kgs22_micaiah_council_scene` | 1Kgs.22 | `needs_review_packet` | 2 | false | true | true | `none` | `create_review_packet` |
| `ezek1_throne_vision` | Ezek.1 | `needs_review_packet` | 1 | true | false | false | `none` | `create_review_packet` |
| `ezek40_48_temple_vision` | Ezek.40-Ezek.48 | `needs_review_packet` | 12 | false | true | true | `none` | `create_review_packet` |
| `zech1_6_night_visions` | Zech.1-Zech.6 | `needs_review_packet` | 3 | false | true | true | `none` | `create_review_packet` |
| `matt24_25_olivet_discourse` | Matt.24-Matt.25 | `needs_review_packet` | 4 | false | true | true | `none` | `create_review_packet` |
| `john13_17_farewell_discourse` | John.13-John.17 | `speaker_review_required` | 6 | false | true | true | `none` | `define_speaker_policy_before_gold` |
| `rom9_11_argument` | Rom.9-Rom.11 | `review_packet_pending` | 4 | false | true | true | `pending_human_review` | `await_human_review` |
| `1pet3_18_22_spirits_prison` | 1Pet.3.18-1Pet.3.22 | `needs_review_packet` | 1 | true | false | true | `none` | `create_review_packet` |
| `jude5_15_examples_and_enoch` | Jude.5-Jude.15 | `source_tradition_review_required` | 1 | true | false | true | `none` | `define_source_tradition_policy_before_gold` |
| `esth8_9_long_administrative_verse` | Esth.8.9 | `needs_review_packet` | 1 | true | false | true | `none` | `create_review_packet` |
| `matt1_genealogy` | Matt.1 | `needs_review_packet` | 1 | true | false | true | `none` | `create_review_packet` |
| `luke3_genealogy` | Luke.3 | `needs_review_packet` | 2 | false | true | true | `none` | `create_review_packet` |
| `1chr1_9_primeval_genealogies` | 1Chr.1-1Chr.9 | `needs_review_packet` | 9 | false | true | true | `none` | `create_review_packet` |
| `josh13_21_land_allotments` | Josh.13-Josh.21 | `needs_review_packet` | 7 | false | true | true | `none` | `create_review_packet` |
| `lev16_day_of_atonement` | Lev.16 | `needs_review_packet` | 3 | false | true | true | `none` | `create_review_packet` |
| `exod20_23_covenant_code` | Exod.20-Exod.23 | `needs_review_packet` | 5 | false | true | true | `none` | `create_review_packet` |
| `heb7_10_priesthood_argument` | Heb.7-Heb.10 | `review_packet_pending` | 4 | false | true | true | `pending_human_review` | `await_human_review` |
| `1cor8_10_food_offered_to_idols` | 1Cor.8-1Cor.10 | `review_packet_pending` | 3 | false | true | true | `pending_human_review` | `await_human_review` |
| `gospels_wj_marker_spans` | Gospels / Acts / Rev words-of-Jesus spans | `speaker_review_required` | 1 | false | false | false | `none` | `define_speaker_policy_before_gold` |
| `psalms_selah_qs_markers` | Psalms with Selah / `\qs` markers | `needs_review_packet` | 7 | false | false | false | `none` | `create_review_packet` |
| `john3_wj_speaker_boundary` | John.3 | `review_packet_pending` | 2 | false | true | true | `pending_human_review` | `await_human_review` |
| `matt5_7_sermon_on_mount_wj_discourse` | Matt.5-Matt.7 | `review_packet_pending` | 5 | false | true | true | `pending_human_review` | `await_human_review` |
| `john13_17_wj_farewell_discourse_marker_focus` | John.13-John.17 | `speaker_review_required` | 6 | false | true | true | `none` | `define_speaker_policy_before_gold` |
| `synoptic_apocalyptic_wj_discourses` | Matt.24-Matt.25 / Mark.13 | `speaker_review_required` | 6 | false | true | true | `none` | `define_speaker_policy_before_gold` |
| `john7_53_8_11_wj_variant_speech` | John.7.53-John.8.11 | `review_packet_pending` | 2 | false | true | true | `pending_human_review` | `await_human_review` |

## Governance Boundary

- `implementation_allowed` remains `false` for every observed entry.
- Observed behavior is not reviewed gold.
- Existing reviewed gold for Ps.105 and Ps.106 is preserved; no new reviewed gold is added here.
- Existing pending packets remain pending.
- Marker evidence such as `\wj`, `\qs`, `\sp`, and `\b` is diagnostic evidence, not boundary or speaker authority.
- Textual-critical, source-tradition, speaker-attribution, theological, and canon decisions remain human-gated.
- No evaluator formula or scoring policy changed.
- No chunk output changed.
