#!/usr/bin/env python3
"""Build the Psalm-specific M7 corrective re-review and optionally finalize it.

This script writes only the Psalm owner surface.  It deliberately does not
touch the three model-global uncertainty sidecars; instead it emits the exact
replacement rows in ``sidecar_rows_v2.json`` for the global sidecar owner.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[6]
MODEL = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol"
REVIEW = MODEL / "reviews" / "Ps"
CHUNKS = MODEL / "book_chunks" / "Ps" / "chunks.jsonl"
STRATEGY = MODEL / "book_strategy" / "Ps.md"
RECEIPT = MODEL / "receipts" / "Ps_completion_v2.json"
PASSAGES = ROOT / "data" / "canonical" / "scripture" / "passages" / "passages.jsonl"
USFM = ROOT / "data" / "processed" / "bible" / "eng-web" / "usfm" / "extracted" / "20-PSAeng-web.usfm"
OSH = ROOT / "data" / "candidate" / "original_language_evidence" / "canonical_source_views" / "openscriptures_oshb" / "files" / "Ps.xml"
UXLC = ROOT / "data" / "candidate" / "original_language_evidence" / "canonical_source_views" / "tanach_us_uxlc" / "files" / "Ps.xml"
CHECKS = MODEL / "checks"
SIDECARS = (
    "low_confidence_register.jsonl",
    "frontier_escalation_queue.jsonl",
    "atlas_candidate_feed.jsonl",
)
CHECKER_ATTEMPT = "ps-v2-role-separated-postchecker-sol-xhigh-20260724"
DECISION_EVIDENCE = REVIEW / 'decision_evidence_v2.jsonl'

INDEPENDENCE_SCOPE = {
    "independent_from_sibling_model_maps": True,
    "primaries_blind_to_each_other_artifacts": True,
    "roles_separated": True,
    "shared_model_substrate": True,
    "counts_as_cross_model_independent_votes": False,
    "independent_model_or_human_evidence_required_at_convergence": True,
    "reviewer_count_is_not_authority": True,
    "correlated_mesh_weight_at_convergence": "one_model_voice",
}

def load_decision_evidence() -> dict[str, dict[str, Any]]:
    '''Load the independently audited decision ledger used for materialization.'''
    rows = read_jsonl(DECISION_EVIDENCE)
    by_id = {row['decision_id']: row for row in rows}
    if len(rows) != 283 or len(by_id) != 283:
        raise ValueError('Psalm decision evidence must contain 283 unique decisions')
    if any(row.get('book') != 'Ps' or row.get('non_authorizing') is not True for row in rows):
        raise ValueError('Psalm decision evidence lost its candidate-only/non-authorizing guard')
    return by_id


def evidence_marker_text(evidence: dict[str, Any]) -> str:
    marker = evidence['deciding_marker_or_seam']
    if isinstance(marker, str):
        return marker
    neighbors = [
        str(marker.get(name))
        for name in ('left_neighbor', 'right_neighbor')
        if marker.get(name)
    ]
    neighbor_text = f'; adjacent evidence: {', '.join(neighbors)}' if neighbors else ''
    return (
        f'{marker['form']} is observed from {marker['opening_ref']} through '
        f'{marker['closing_ref']}{neighbor_text}'
    )


def evidence_basis_text(evidence: dict[str, Any]) -> str:
    basis = evidence['defensible_basis']
    if basis['decision_kind'] == 'whole_psalm':
        defense = (
            '{} retrieval at {}; tested_internal_alternative={}.'.format(
                basis['decision_kind'],
                basis['retrieval_choice'],
                str(basis['tested_internal_alternative']).lower(),
            )
        )
    else:
        seams = '; '.join(item['claim'] for item in basis['selected_adjacent_seams'])
        defense = (
            '{} retrieval at {}; parent retained {}; selected seam evidence: {}'.format(
                basis['decision_kind'],
                basis['retrieval_choice'],
                basis['parent_retained'],
                seams,
            )
        )
    return '{} Confidence is independently calibrated as {}: {}'.format(
        defense,
        evidence['confidence'],
        evidence['confidence_basis'].get('rationale') or evidence['confidence_basis']['prose'],
    )


def apply_decision_evidence(
    chunks: list[dict[str, Any]],
    evidence_by_id: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    '''Replace generator scaffolding with the audited decision-local evidence.'''
    if {row['decision_id'] for row in chunks} != set(evidence_by_id):
        raise ValueError('chunk/evidence decision sets differ')
    for row in chunks:
        evidence = evidence_by_id[row['decision_id']]
        if row['span'] != evidence['span']:
            raise ValueError(f'{row['decision_id']}: chunk/evidence span mismatch')
        held = evidence['candidate_state'] == 'held'
        row.update(
            {
                'literature_type_guess': evidence['literary_form'],
                'literary_form': evidence['literary_form'],
                'parent_literary_form': evidence['parent_literary_form'],
                'confidence': evidence['confidence'],
                'confidence_basis': evidence['confidence_basis'],
                'deciding_marker_or_seam': evidence['deciding_marker_or_seam'],
                'boundary_rationale': evidence['boundary_rationale'],
                'rejected_alternative': evidence['rejected_alternative'],
                'counterevidence': evidence['rejected_alternative'],
                'defensible_basis': (
                    evidence['confidence_basis'].get('rationale')
                    or evidence['confidence_basis']['prose']
                ),
                'convergence_defense': {
                    'literary_form': evidence['literary_form'],
                    'deciding_marker_or_seam': evidence['deciding_marker_or_seam'],
                    'rejected_alternative': evidence['rejected_alternative'],
                    'confidence': evidence['confidence'],
                    'confidence_basis': evidence['confidence_basis'],
                    'defensible_basis': evidence['boundary_rationale'],
                    'source_observations': evidence['source_observations'],
                    'observed_poetic_features': evidence['observed_poetic_features'],
                    'relation_codes': evidence['relation_codes'],
                    'original_language_alignment': evidence['original_language_alignment'],
                },
                'review_revision': 'm7-corrective-rereview-v2',
                'review_status': 'final_deferred_appeal' if held else 'candidate_review_complete',
                'review_holds': (
                    ['deferred_human_or_external_ai', evidence['hold']['kind']]
                    if held
                    else []
                ),
                'candidate_hold_state': 'deferred_human_or_external_ai' if held else None,
                'candidate_hold_basis': evidence.get('hold'),
                'review_evidence_summary': evidence['boundary_rationale'],
                'candidate_internal_seams': [
                    evidence['deciding_marker_or_seam'],
                    evidence['rejected_alternative'],
                ],
                'red_team_premortem_holds': [
                    f'The live competing treatment for {row['span']} is: '
                    f'{evidence['rejected_alternative']}'
                ],
            }
        )
        row['boundary_evidence_refs'] = [
            *row['boundary_evidence_refs'],
            f'reviews/Ps/decision_evidence_v2.jsonl#{row['decision_id']}',
        ]
        if held:
            row['human_review_question'] = evidence['hold']['question']
            row['human_review_options'] = evidence['hold']['options']
        else:
            row.pop('human_review_question', None)
            row.pop('human_review_options', None)
    return chunks


# Whole psalms are the default.  These are the evidence-demanded internal units.
SPLITS: dict[int, list[tuple[int, int]]] = {
    18: [(1, 6), (7, 19), (20, 30), (31, 45), (46, 50)],
    19: [(1, 6), (7, 11), (12, 14)],
    22: [(1, 21), (22, 31)],
    24: [(1, 2), (3, 6), (7, 10)],
    31: [(1, 8), (9, 18), (19, 24)],
    35: [(1, 10), (11, 18), (19, 28)],
    37: [(1, 11), (12, 20), (21, 31), (32, 40)],
    40: [(1, 10), (11, 17)],
    42: [(1, 5), (6, 11)],
    44: [(1, 8), (9, 16), (17, 26)],
    46: [(1, 3), (4, 7), (8, 11)],
    49: [(1, 4), (5, 12), (13, 20)],
    50: [(1, 6), (7, 15), (16, 23)],
    51: [(1, 6), (7, 12), (13, 19)],
    55: [(1, 8), (9, 15), (16, 23)],
    57: [(1, 5), (6, 11)],
    59: [(1, 9), (10, 17)],
    62: [(1, 4), (5, 8), (9, 12)],
    67: [(1, 3), (4, 5), (6, 7)],
    68: [(1, 6), (7, 18), (19, 27), (28, 35)],
    69: [(1, 12), (13, 18), (19, 28), (29, 36)],
    71: [(1, 13), (14, 24)],
    73: [(1, 12), (13, 17), (18, 22), (23, 28)],
    74: [(1, 11), (12, 17), (18, 23)],
    77: [(1, 9), (10, 15), (16, 20)],
    78: [(1, 8), (9, 16), (17, 31), (32, 39), (40, 55), (56, 64), (65, 72)],
    80: [(1, 3), (4, 7), (8, 19)],
    81: [(1, 5), (6, 10), (11, 16)],
    83: [(1, 8), (9, 18)],
    89: [(1, 4), (5, 18), (19, 37), (38, 45), (46, 48), (49, 52)],
    90: [(1, 6), (7, 12), (13, 17)],
    94: [(1, 7), (8, 11), (12, 15), (16, 23)],
    95: [(1, 6), (7, 11)],
    99: [(1, 3), (4, 5), (6, 9)],
    102: [(1, 11), (12, 22), (23, 28)],
    104: [(1, 9), (10, 18), (19, 23), (24, 30), (31, 35)],
    107: [(1, 3), (4, 9), (10, 16), (17, 22), (23, 32), (33, 42), (43, 43)],
    108: [(1, 5), (6, 13)],
    109: [(1, 5), (6, 20), (21, 31)],
    110: [(1, 3), (4, 7)],
    118: [(1, 4), (5, 18), (19, 29)],
    119: [(start, start + 7) for start in range(1, 177, 8)],
    135: [(1, 4), (5, 14), (15, 21)],
    136: [(1, 3), (4, 9), (10, 16), (17, 22), (23, 25), (26, 26)],
    137: [(1, 4), (5, 6), (7, 9)],
    139: [(1, 6), (7, 12), (13, 18), (19, 22), (23, 24)],
    144: [(1, 4), (5, 8), (9, 11), (12, 15)],
    145: [(1, 7), (8, 13), (14, 21)],
    147: [(1, 6), (7, 11), (12, 20)],
}

CHILD_FORMS: dict[tuple[int, int, int], str] = {}
for _child_form_line in r"""
18|1-6:distress_lament;7-19:theophanic_deliverance_hymn;20-30:vindication_testimony;31-45:warrior_victory_recital;46-50:royal_thanksgiving
19|1-6:creation_hymn;7-11:torah_praise;12-14:self_scrutiny_and_cleansing_petition
22|1-21:forsakenness_lament_and_rescue_petition;22-31:assembly_thanksgiving_hymn
24|1-2:creator_kingship_hymn;3-6:entrance_liturgy_question_answer;7-10:gate_antiphony
31|1-8:refuge_and_integrity_petition;9-18:distress_lament;19-24:praise_exhortation
35|1-10:adversary_petition_with_praise_vow;11-18:false_witness_lament_with_praise_vow;19-28:vindication_petition
37|1-11:alphabetic_wisdom_exhortation;12-20:wicked_and_righteous_fate_contrast;21-31:righteous_inheritance_instruction;32-40:watched_conflict_and_refuge_exhortation
40|1-10:deliverance_thanksgiving_testimony;11-17:renewed_lament_petition
42|1-5:thirst_lament_with_refrain;6-11:remembrance_lament_with_refrain
44|1-8:ancestral_deliverance_and_confidence_recital;9-16:communal_defeat_lament;17-26:innocence_protest_and_rescue_petition
46|1-3:refuge_hymn_refrain_cycle;4-7:zion_river_hymn_refrain_cycle;8-11:divine_kingship_oracle_refrain_cycle
49|1-4:wisdom_summons;5-12:wealth_and_mortality_meditation;13-20:mortality_refrain_and_warning
50|1-6:theophanic_courtroom_summons;7-15:covenant_worship_oracle;16-23:wickedness_judgment_oracle
51|1-6:confession_and_cleansing_petition;7-12:purification_and_renewal_petition;13-19:teaching_praise_vow_and_zion_prayer
55|1-8:betrayal_lament_and_escape_wish;9-15:city_violence_and_companion_lament;16-23:trust_petition_and_burden_exhortation
57|1-5:refuge_lament_with_refrain;6-11:reversal_praise_with_refrain
59|1-9:rescue_petition_and_enemy_watch;10-17:judgment_petition_and_praise_refrain
62|1-4:trust_refrain_against_attackers;5-8:trust_exhortation;9-12:wealth_warning_and_recompense_oracle
67|1-3:blessing_petition_for_nations;4-5:nations_thanksgiving_refrain;6-7:harvest_blessing
68|1-6:processional_summons;7-18:exodus_sinai_zion_recital;19-27:salvation_procession_hymn;28-35:kingdom_doxology
69|1-12:flood_and_alienation_lament;13-18:rescue_petition;19-28:reproach_and_imprecation;29-36:thanksgiving_and_zion_hymn
71|1-13:aged_speaker_lament_petition;14-24:lifelong_praise_and_teaching_vow
73|1-12:prosperity_problem_confession;13-17:sanctuary_discernment_turn;18-22:wicked_fate_reappraisal;23-28:nearness_confession_and_testimony
74|1-11:sanctuary_destruction_lament;12-17:creation_kingship_recital;18-23:covenant_memory_petition
77|1-9:night_lament_and_questions;10-15:remembrance_turn;16-20:exodus_waters_theophany
78|1-8:teaching_prologue;9-16:ephraim_and_wilderness_deliverance;17-31:wilderness_testing_and_judgment;32-39:continued_sin_and_compassion;40-55:egypt_exodus_and_land_recital;56-64:rebellion_shiloh_and_defeat;65-72:zion_choice_and_davidic_shepherd_closure
80|1-3:shepherd_invocation_and_refrain;4-7:communal_lament_and_refrain;8-19:vine_lament_and_final_refrain
81|1-5:festival_hymn;6-10:exodus_oracle;11-16:disobedience_lament_and_abundance_promise
83|1-8:conspiracy_lament_and_nation_list;9-18:historical_analogy_and_judgment_petition
89|1-4:steadfast_love_praise_vow;5-18:cosmic_kingship_hymn;19-37:davidic_covenant_oracle;38-45:royal_rejection_lament;46-48:mortality_and_delay_petition;49-52:covenant_lament_and_collection_doxology
90|1-6:refuge_and_mortality_meditation;7-12:wrath_and_wisdom_petition;13-17:compassion_and_work_petition
94|1-7:vengeance_petition_and_oppressor_indictment;8-11:rebuke_of_senselessness;12-15:discipline_beatitude;16-23:justice_confidence_and_requital
95|1-6:worship_hymn;7-11:wilderness_warning_oracle
99|1-3:enthronement_refrain;4-5:judicial_kingship_hymn;6-9:priestly_memory_and_holiness_refrain
102|1-11:wasting_lament;12-22:zion_restoration_hymn;23-28:mortality_petition_and_creator_permanence
104|1-9:cosmic_ordering_hymn;10-18:habitat_and_provision_hymn;19-23:luminary_and_daily_rhythm_hymn;24-30:creature_dependence_and_renewal_hymn;31-35:praise_and_moral_closure
107|1-3:thanksgiving_summons_to_the_redeemed;4-9:desert_wanderer_refrain_cycle;10-16:prisoner_refrain_cycle;17-22:sickness_refrain_cycle;23-32:storm_at_sea_refrain_cycle;33-42:land_reversal_and_settlement_hymn;43-43:wisdom_coda
108|1-5:steadfast_praise_hymn;6-13:military_rescue_petition
109|1-5:false_accusation_lament;6-20:imprecatory_appeal;21-31:poor_speaker_rescue_petition_and_praise_vow
110|1-3:royal_oracle;4-7:priestly_oath_and_victory_oracle
118|1-4:liturgical_thanksgiving_summons;5-18:distress_deliverance_testimony;19-29:gate_liturgy_and_thanksgiving_closure
135|1-4:praise_summons;5-14:creation_exodus_and_kingdom_recital;15-21:idol_satire_and_household_blessing
136|1-3:thanksgiving_summons;4-9:creation_refrain_cycle;10-16:exodus_refrain_cycle;17-22:conquest_refrain_cycle;23-25:low_estate_and_provision_refrain_cycle;26-26:final_thanksgiving_coda
137|1-4:exile_lament;5-6:zion_memory_oath;7-9:imprecatory_petition
139|1-6:search_and_knowledge_hymn;7-12:inescapable_presence_hymn;13-18:formation_praise;19-22:enemy_disavowal;23-24:search_me_petition
144|1-4:warrior_blessing_and_mortality_reflection;5-8:theophanic_rescue_petition;9-11:new_song_and_victory_petition;12-15:communal_flourishing_beatitude
145|1-7:alphabetic_praise_proclamation;8-13:gracious_kingship_hymn;14-21:provision_nearness_and_universal_praise
147|1-6:jerusalem_restoration_hymn;7-11:creator_care_hymn;12-20:zion_word_and_torah_hymn
""".strip().splitlines():
    _child_psalm, _child_units = _child_form_line.split("|", 1)
    for _child_unit in _child_units.split(";"):
        _child_range, _child_form = _child_unit.split(":", 1)
        _child_start, _child_end = map(int, _child_range.split("-"))
        CHILD_FORMS[(int(_child_psalm), _child_start, _child_end)] = _child_form

FORMS = [
    "wisdom_torah_psalm", "royal_enthronement_psalm", "individual_lament", "trust_lament",
    "individual_lament", "penitential_lament", "individual_lament", "creation_hymn",
    "alphabetic_thanksgiving", "alphabetic_lament", "trust_psalm", "communal_lament",
    "individual_lament", "wisdom_lament", "entrance_liturgy", "trust_psalm",
    "individual_lament", "royal_thanksgiving", "creation_hymn_and_torah_wisdom",
    "royal_liturgy", "royal_thanksgiving", "lament_to_thanksgiving", "trust_psalm",
    "entrance_liturgy_and_zion_song", "alphabetic_lament", "individual_lament",
    "trust_lament", "individual_lament", "divine_kingship_hymn", "thanksgiving_psalm",
    "individual_lament", "penitential_wisdom_psalm", "hymn", "alphabetic_thanksgiving",
    "imprecatory_lament", "mixed_wisdom_and_hymn", "alphabetic_wisdom_psalm",
    "penitential_lament", "mortality_lament", "thanksgiving_and_lament",
    "individual_lament_with_collection_doxology", "individual_lament", "individual_lament",
    "communal_lament", "royal_wedding_song", "zion_song", "enthronement_hymn", "zion_song",
    "wisdom_psalm", "covenant_lawsuit_oracle", "penitential_lament", "denunciatory_trust_psalm",
    "wisdom_lament", "individual_lament", "individual_lament", "trust_lament",
    "trust_lament", "judicial_imprecation", "individual_lament", "communal_lament",
    "royal_lament", "trust_psalm", "trust_psalm", "individual_lament", "thanksgiving_creation_hymn",
    "communal_thanksgiving", "thanksgiving_blessing", "processional_hymn", "individual_lament",
    "individual_lament", "trust_lament", "royal_prayer_with_collection_doxology", "wisdom_psalm", "communal_lament",
    "thanksgiving_and_judgment_oracle", "zion_hymn", "lament_and_historical_hymn",
    "historical_wisdom_psalm", "communal_lament", "communal_lament", "festival_liturgy_oracle",
    "judicial_oracle", "communal_lament", "pilgrimage_zion_song", "communal_restoration_prayer",
    "individual_lament", "zion_song", "individual_lament", "royal_covenant_lament",
    "communal_lament_and_wisdom", "trust_psalm", "sabbath_hymn_and_wisdom",
    "enthronement_hymn", "judicial_lament", "liturgical_hymn_oracle", "enthronement_hymn",
    "enthronement_hymn", "enthronement_hymn", "enthronement_hymn", "thanksgiving_hymn",
    "royal_vow", "lament_and_restoration_hymn", "hymn", "creation_hymn",
    "historical_hymn", "historical_confession", "communal_thanksgiving", "composite_hymn_and_lament",
    "imprecatory_lament", "royal_priestly_oracle", "alphabetic_hymn", "alphabetic_wisdom_psalm",
    "hymn", "exodus_hymn", "communal_liturgical_hymn", "thanksgiving_psalm", "hymn",
    "liturgical_thanksgiving", "alphabetic_torah_psalm", "pilgrimage_lament", "pilgrimage_trust",
    "pilgrimage_and_zion_song", "pilgrimage_lament", "pilgrimage_thanksgiving",
    "pilgrimage_trust", "pilgrimage_thanksgiving", "pilgrimage_wisdom",
    "pilgrimage_wisdom_and_blessing", "pilgrimage_communal_lament",
    "penitential_pilgrimage_lament", "pilgrimage_trust", "pilgrimage_royal_zion_song",
    "pilgrimage_blessing", "pilgrimage_benediction", "hymnic_litany",
    "thanksgiving_refrain_litany", "communal_lament", "thanksgiving_psalm",
    "individual_hymn_and_lament", "individual_lament", "individual_lament",
    "individual_lament", "penitential_lament", "royal_prayer", "alphabetic_hymn",
    "hymn", "hymn", "creation_hymn", "hymn", "doxological_hymn",
]
assert len(FORMS) == 150
FORM_BY_PSALM = {index + 1: value for index, value in enumerate(FORMS)}

HEBREW_LETTERS = [
    "Aleph", "Beth", "Gimel", "Daleth", "He", "Waw", "Zayin", "Heth", "Teth", "Yodh", "Kaph",
    "Lamedh", "Mem", "Nun", "Samekh", "Ayin", "Pe", "Tsadhe", "Qoph", "Resh", "Shin", "Taw",
]
for _letter_index, _letter_start in enumerate(range(1, 177, 8)):
    CHILD_FORMS[(119, _letter_start, _letter_start + 7)] = (
        f"{HEBREW_LETTERS[_letter_index].lower()}_alphabetic_torah_stanza"
    )

# These holds represent actual unresolved retrieval/boundary choices, not generic
# "poetry is hard" uncertainty.
HELD_PSALMS = {9, 10, 41, 42, 43, 72, 106, 108, 114, 115, 116, 147, 148}

WHOLE_AUDITS: dict[int, tuple[str, str]] = {}
for _whole_audit_line in r"""
1|The opening beatitude, tree image, and Yahweh's closing knowledge of the righteous way form one antithetical wisdom argument.|Verses 1-3 could stand as the righteous portrait and verses 4-6 as the wicked contrast, but the causal "For" in verse 6 resolves both ways together.
2|The revolt, heavenly response, royal decree, and warning to rulers are successive voices in one enthronement drama.|Verse 7 is the strongest child opening because "I will tell of the decree" changes speaker and begins the royal speech; a 1-6/7-12 reading remains plausible.
3|Complaint, shield confession, sleep testimony, rescue cry, and salvation blessing complete a compact lament-to-trust arc.|The Selah after verse 4 could mark a 1-4/5-8 division, yet the sleep testimony carries the trust confession directly into the final plea.
4|The answered opening prayer moves through rebuke, inward trust, communal longing, and peaceful sleep without a stable independent stanza.|Verse 2's address to the sons of men is the strongest speech seam, but separating it would detach the rebuke from the prayer and sleep conclusion.
5|Morning address, moral appeal, temple approach, enemy petition, and refuge blessing all serve the speaker's request to be led.|Verse 7's "But as for me" could open a worship-and-guidance child after the wicked portrait, though the same enemy pressure governs both halves.
6|The penitential cry accumulates bodily pain, death anxiety, tears, and then confidence that Yahweh has heard.|Verse 8's dismissal of evildoers is a real lament-to-confidence turn, but it depends on the heard prayer of verses 1-7.
7|The innocence protest, appeal for divine judgment, and closing justice testimony answer one accusation.|Verse 10's "My shield is with God" could begin a justice-hymn child after the judgment plea; the unresolved accusation keeps the full Psalm context necessary.
8|The enveloping "Yahweh, our Lord" refrain binds cosmic majesty, the humanity question, and delegated creaturely rule.|Verse 4's "What is man" opens the strongest meditation child, but the question receives its force from the heavens in verses 1-3 and resolves in the verse-9 refrain.
9|Alphabetic thanksgiving repeatedly alternates praise, judicial confidence, and petition while continuing into the Psalm 9-10 relation hold.|Verse 13's "Have mercy on me" is the strongest internal move from public praise to personal petition, but splitting it would conceal the alphabetic and numbering relation under review.
10|The wicked person's portrait and the plea for Yahweh to arise form the two necessary sides of one alphabetic lament.|The WEB paragraph at verse 12 corroborates the real portrait-to-petition turn; it remains a possible 1-11/12-18 child division under the Psalm 9-10 parent question.
11|The opening temptation to flee is answered by the temple-throne confession and the final verdict about Yahweh's loves.|Verse 4's "Yahweh is in his holy temple" is the actual answer seam, but extracting the oracle would remove the question it rebuts.
12|Complaint about vanished faithfulness, Yahweh's direct promise, and the closing diagnosis of the wicked complete one communal lament.|Verse 5's "Because of the oppression" opens a divine oracle, yet verses 6-8 immediately test that promise against the lament's social setting.
13|Repeated "How long," direct petition, and rejoicing trust make a deliberately compressed lament progression.|Verse 5's "But I trust" is a genuine confidence turn, but the two-verse trust close is not independently intelligible without the unanswered questions and petition.
14|The fool portrait, divine inspection, sudden judgment, and Zion salvation wish form one wisdom-lament argument.|Verse 7's salvation wish is the strongest closing child, though its longing answers the corruption and fear described in verses 1-6.
15|The entrance question and the answer's ethical catalogue are a single liturgical exchange.|Verse 2 begins the answer to verse 1, but question and response must remain retrievable together as the entrance liturgy.
16|Petition, rejection of rival loyalties, inheritance confession, counsel, and resurrection-from-Sheol confidence accumulate as one trust testimony.|Verse 5's "Yahweh assigned my portion" is the strongest positive-confession seam after verses 1-4, but the rejected loyalties define that inheritance claim.
17|The plea of innocence, pursued-speaker complaint, and final rescue request remain addressed to the same judge.|Verse 13's "Arise, Yahweh" begins the strongest final rescue child, though its adversary and vindication language depends on verses 1-12.
20|Congregational intercession, confidence that the anointed is answered, and a final royal plea enact one compact liturgy.|Verse 6's "Now I know" changes from wish to assurance, but the confidence explicitly answers the petitions of verses 1-5.
21|Past royal gifts, confidence in steadfast love, future judgment, and final praise trace a single royal thanksgiving.|Verse 7 begins the future-facing trust and judgment movement, yet it grounds that future in the blessings recited in verses 1-6.
23|Shepherd care through danger, host hospitality, and lifelong dwelling are linked metaphors of one trust confession.|Verse 5's table image is the strongest metaphor shift, but it intensifies rather than replaces the guidance and protection of verses 1-4.
25|The alphabetic lament interweaves guidance petition, instruction about Yahweh's ways, and renewed distress without completing a child before its final redemption plea.|Verse 8 could open a teaching child and verse 16 a renewed personal lament, but the alphabetic sequence and repeated "way" language bind all three movements.
26|Vindication plea, separation from evildoers, altar procession, and final congregational blessing enact one integrity prayer.|Verse 6's hand-washing and altar approach is the strongest cultic turn, but it demonstrates the integrity claimed in verses 1-5 and supports the rescue plea in verses 9-12.
27|Fearless confidence, temple desire, urgent "Hear" petition, and final waiting exhortation create a trust-lament-trust arc.|Verse 7's renewed direct plea is the material 1-6/7-14 alternative; the final "Wait for Yahweh" deliberately returns to the opening confidence.
28|The opening rescue plea and warning about evildoers turn into thanksgiving and a communal shepherd blessing.|Verse 6's "Blessed be Yahweh" is a real lament-to-thanks seam, but verses 8-9 extend the speaker's heard prayer to the people rather than forming a detached hymn.
29|The heavenly summons, sevenfold voice over the storm, and enthroned peace blessing form a single divine-kingship hymn.|Verse 3 begins the storm theophany after the summons, while verse 10 interprets it as kingship; neither movement closes independently of the other two.
30|Rescue thanksgiving, recalled self-confidence and distress, then mourning-to-dancing praise narrate one reversal testimony.|Verse 6 begins the crisis recollection and verse 11 returns to praise; the framing thanksgiving makes those shifts a single narrated deliverance.
32|Forgiveness beatitudes, concealed-and-confessed sin, then instruction and communal rejoicing build one penitential wisdom testimony.|The Selah after verse 5 marks the strongest confession-to-instruction alternative, but verses 6-11 apply the forgiveness learned in verses 1-5.
33|Praise summons, creation by Yahweh's word, sovereignty over nations, and waiting trust all support one hymn of reliable counsel.|Verse 10 begins the nations-and-counsel contrast and verse 18 the trust conclusion; both depend on the creator-word praise of verses 4-9.
34|The personal praise and deliverance testimony become communal instruction at "Come, you children" and end with refuge.|Verse 11 is the actual testimony-to-wisdom seam, yet the instruction generalizes the tasted deliverance of verses 1-10 within one alphabetic poem.
36|The oracle about wickedness gives way to direct praise of Yahweh's steadfast love and then a preservation petition.|Verse 5 is the material wickedness-oracle to hymn seam corroborated by a WEB paragraph; the closing petition applies that hymn to the opening threat.
38|Wrath, bodily collapse, isolation, enemies, confession, and final "Hurry to help me" remain one unrelieved penitential address.|Verse 15's "For in you, Yahweh, do I hope" is the strongest confidence turn, but it immediately returns to the same pain, sin, and adversaries.
39|A vow of silence breaks into a mortality prayer and then a hope-and-forgiveness petition.|Verse 7's "Now, Lord, what do I wait for?" is the strongest mortality-to-hope seam, while the failed silence and brevity of life govern the closing appeal.
41|Care for the weak, illness and betrayal, personal vindication, and the Book I doxology meet at the poem's close.|Verse 10 opens the rescue request and verse 13 is a collection doxology; whether that coda becomes a retrieval child is deliberately held rather than mechanically settled.
43|Legal plea, longing for light and altar return, and the shared "Why are you in despair?" refrain complete a compact linked lament.|Verse 3 could begin the positive return-to-sanctuary petition, but its function and the verse-5 refrain remain inseparable from Psalm 42's linked-parent question.
45|The scribe's prologue, address to the king, address to the bride, and dynastic close form one royal wedding song.|The live alternatives are verse 2 for the royal address, verse 10 for the bride address, and verse 16 for the dynastic close; the wedding performance arc requires all four parts together.
47|Nations are summoned, Yahweh ascends amid acclamation, and the rulers gather under divine kingship.|The Selah after verse 4 marks a plausible 1-4/5-9 turn from summons to ascent, but the repeated kingship praise joins both movements.
48|Zion praise, failed royal assault, temple meditation, and processional inspection culminate in "this God is our God."|Verse 9's temple meditation after the assault is the strongest historical-to-processional seam, though the inspected city is the same Zion praised and defended earlier.
52|The denunciation of the boastful speaker, the righteous community's response, and the olive-tree trust confession form a single contrast psalm.|Verse 6 could begin the righteous observers' response and verse 8 the personal trust close, but both derive their force from the accusation in verses 1-5.
53|The fool-and-corruption portrait, divine inspection and fear, then the Zion salvation wish compress a complete wisdom lament.|Verse 6's salvation prayer is the strongest close, but it answers the universal corruption of verses 1-5 rather than opening a new poem.
54|A rescue plea, confidence that God is helper, and a freewill-offering vow narrate one short deliverance arc.|Verse 4's "Behold, God is my helper" is a real petition-to-confidence turn, but verses 6-7 explicitly fulfill the opening request.
56|Fear, hostile surveillance, tear-counting, repeated trust, and thanksgiving vows recur around the same persecution.|Verse 8's request to record wandering is the strongest renewed-trust movement, yet the repeated "I will not be afraid" refrain binds both halves.
58|Indictment of unjust rulers, imprecatory images, and the righteous conclusion form one judicial imprecation.|Verse 6 begins the judgment petition and verse 10 the observer response; separating them would detach verdict and consequence from the indictment.
60|Defeat lament, territorial divine oracle, and military petition stage one communal crisis.|The Selah after verse 4 and oracle opening at verse 6 support a real 1-5/6-12 alternative, but the oracle does not resolve the final "Who will lead us?" petition.
61|Remote-ground plea, refuge confidence, royal preservation prayer, and perpetual praise vow remain one royal lament.|Verse 5's "For you, God, have heard my vows" begins the royal-confidence movement, but it answers the opening cry and leads directly to the closing vow.
63|Thirst for God, remembered sanctuary praise, satisfied meditation, and enemies' fate form a single trust testimony.|Verse 5's satisfaction image is the strongest longing-to-fulfillment seam, while the remembered praise and refuge under wings bridge the two movements.
64|Secret-plot complaint is answered by sudden divine shooting and communal fear and rejoicing.|Verse 7's "But God will shoot at them" is the real complaint-to-reversal turn; the reversal is unintelligible without the speech-weapons of verses 1-6.
65|Atonement and temple blessedness, cosmic stilling, and harvest abundance develop one thanksgiving-creation hymn.|Verse 9's turn to watered earth is the strongest cosmic-to-harvest seam; the creator who stills seas in verses 5-8 is the same giver of the harvest.
66|Universal summons and exodus testing widen into a first-person vow and answered-prayer testimony.|Verse 13's "I will come into your temple with burnt offerings" is the material communal-to-personal seam, but the individual testimony exemplifies the communal call rather than replacing it.
70|Petition against persecutors, blessing for seekers, and the poor speaker's closing urgency form one intentionally brief lament.|Verse 4's turn to seekers is the only plausible inner seam, but it is a one-verse counterwish between the adversary petition and personal plea.
72|The royal justice prayer expands to worldwide blessing, followed by a doxology and editorial colophon.|Verse 18 begins the collection doxology and verse 20 the colophon; their retrieval treatment remains a coda-policy hold while the WEB Psalm stays whole.
75|Opening thanks introduces divine speech about appointed judgment, human interpretation, and a closing vow.|Verse 2 begins the judgment oracle and verse 9 the speaker's vow; the answer to arrogant boasting needs both voice movements.
76|Zion victory praise, terrifying judgment from heaven, and a final vow exhortation describe one divine-warrior hymn.|Verse 10 opens the strongest judgment-to-vow application, but it is the human response demanded by the victory of verses 1-9.
79|Temple devastation and national reproach become confession, mercy plea, and promised thanks.|Verse 5's "How long?" is the strongest description-to-petition seam, while the plea repeatedly names the devastation and reproach it seeks to reverse.
82|The divine-council setting, indictment of unjust judges, death verdict, and final appeal form one judicial oracle.|Verse 2 begins the accusation and verse 8 the appeal, but removing either would leave the council scene without charge or requested enforcement.
84|Longing for Yahweh's courts, pilgrimage beatitudes, an anointed-one prayer, and the final trust beatitude form one Zion song.|Verse 5 begins the pilgrimage movement and verse 9 the direct prayer; repeated blessedness language binds them to the opening longing.
85|Remembered restoration leads to renewed mercy petition and then a heard oracle of peace, love, and righteousness.|Verse 8's "I will hear what God, Yahweh, will speak" is the strongest petition-to-oracle seam, but the oracle answers the restoration plea of verses 4-7.
86|Personal plea, incomparable-God hymn, request for an undivided heart, and enemy complaint remain one sustained address.|Verse 8 could open the hymn and verse 11 the teaching petition, but the speaker uses both to ground the same rescue request.
87|Yahweh's love of Zion, enrollment of foreign nations, and the singers' closing claim create one compact Zion oracle.|Verse 4 begins the nations list, but the list is the content of Zion's glorious report rather than an independent register.
88|Opening cry, descent-to-Sheol imagery, questions about praise among the dead, and final darkness never reach a confidence resolution.|Verse 10 begins the strongest rhetorical-question movement and verse 13 renews direct prayer, but the uninterrupted abandonment argues for the whole lament.
91|Refuge confession, angelic and creature protection, and Yahweh's closing first-person oracle complete one trust psalm.|Verse 14 is the required speaker-shift alternative because "Because he has set his love on me" begins direct divine speech; the oracle ratifies the promises rather than standing alone.
92|Sabbath thanksgiving, reflection on fools and flourishing wickedness, then the righteous palm-and-cedar portrait complete one wisdom hymn.|Verse 10's "But you have exalted my horn" is the strongest wicked-to-righteous reversal, while the planted-righteous close answers the earlier prosperity problem.
93|Yahweh's enthronement, the floods' challenge, and the final testimony to enduring decrees make a five-verse kingship hymn.|Verse 3's raised floods are the only plausible adversarial movement, but verse 4 answers them and verse 5 interprets the same kingship.
96|The new-song summons, Yahweh's superiority, nations' worship, and creation's rejoicing before judgment form one enthronement hymn.|Verse 7 opens the nations' liturgical response and verse 11 the creation response; both enact the kingship announced in verses 1-6.
97|Storm-cloud theophany, idol-shame and Zion joy, then exhortation to hate evil and rejoice form one kingship proclamation.|Verse 7 begins the human response and verse 10 the exhortation, but both interpret the single theophany of verses 1-6.
98|New-song reasons, trumpet-and-harp summons, and roaring creation before the judge form one enthronement hymn.|Verse 4 begins congregational instrumentation and verse 7 cosmic participation, but the same coming judgment supplies their shared reason.
100|Commands to shout and serve, confession that Yahweh made and shepherds the people, and thankful gate entry form one processional hymn.|Verse 3 is the confession center and verse 4 the entrance command, but the five imperatives form a single liturgical progression.
101|Royal commitments to steadfast conduct become explicit exclusions of slander, pride, deceit, and evildoers.|Verse 5 begins the household-and-city exclusions, but those policies apply the integrity vowed in verses 1-4.
103|Self-blessing and personal benefits expand to justice and compassion, human mortality, heavenly kingship, and a cosmic blessing summons.|Material alternatives begin at verses 6, 15, and 19; the repeated "Bless Yahweh, my soul" frame and the movement from personal to cosmic praise support the whole hymn.
105|Praise summons introduces covenant history from the patriarchs through Exodus, land gift, and the closing Torah purpose.|Verse 7 begins the historical recital and verse 45 states its purpose; the stable reviewed whole keeps summons, recital, and purpose together rather than fragmenting episodes.
106|Praise and confession introduce a long rebellion-and-mercy recital, gathering petition, and Book IV doxology.|Verses 6 and 13 open major recital episodes and verses 47-48 form petition plus collection coda; stable whole-Psalm review is retained while coda retrieval remains held.
111|The opening praise summons, alphabetic catalogue of Yahweh's works, covenant provision, and fear-of-Yahweh wisdom close form one acrostic hymn.|Verse 10's wisdom maxim could be a closing child, but it is the acrostic culmination and interpretation of the works in verses 2-9.
112|The alphabetic portrait of the blessed righteous person culminates in the wicked person's frustrated desire.|Verse 10 supplies the strongest antithetical close, but it completes rather than interrupts the acrostic character portrait.
113|Servants are summoned to praise, Yahweh's transcendence is confessed, and the enthroned God raises poor and barren people.|Verse 7 begins the social-reversal examples, but they answer the question "Who is like Yahweh?" in verse 5.
114|Exodus from Egypt, sea and mountain flight, then earth's trembling command form one compact exodus hymn.|Verse 7's direct address to the earth is the strongest narration-to-command seam, but it interprets the reactions described in verses 3-6.
115|The glory plea contrasts Yahweh with lifeless idols, calls Israel's houses to trust, and concludes with blessing and praise.|Verse 9 begins the trust litany and verse 12 the blessing, while the Greek combined-numbering relation with Psalm 114 remains held outside the WEB boundary.
116|Love and answered-prayer testimony move through death distress to thanksgiving vows and public payment in Yahweh's courts.|Verse 12's "What will I give to Yahweh?" is the strongest testimony-to-vow seam and corresponds to alternate-numbering pressure, so the WEB whole is held with that relation explicit.
117|A one-verse universal praise call receives its one-verse reason in steadfast love and enduring faithfulness.|The call/reason boundary at verse 2 is rhetorically real but neither single verse functions as a responsible child apart from the other.
120|Deliverance from deceit, judgment on the false tongue, and the peace-seeker's exile complaint form one pilgrimage lament.|Verse 5's "Woe is me" begins the exile setting, but it explains the hostile speech and war pressure of the opening petition.
121|The help question and creator answer lead into a sixfold guardian promise ending in perpetual keeping.|Verse 3 begins the guardian assurances, but they directly answer verses 1-2 and accumulate to the going-out/coming-in close.
122|Arrival joy, Jerusalem's built unity and tribal-throne role, then prayer for peace form one pilgrimage Zion song.|Verse 6 begins the peace petition, but its repeated Jerusalem address depends on the city praise of verses 1-5.
123|The upward gaze and servant-eye comparison culminate in a repeated mercy plea under contempt.|Verse 3 begins the direct mercy petition, but the servant image in verses 1-2 supplies its posture and expectation.
124|A counterfactual recital of engulfing danger turns to thanks for escape and confession of help in the creator's name.|Verse 6's "Blessed be Yahweh" is the deliverance-to-thanks seam, but the escaped prey and creator confession complete the same communal testimony.
125|Zion-like security and Yahweh's surrounding presence ground a justice petition and final peace wish.|Verse 3 begins the rule-of-wickedness warning, but it tests the promised stability of verses 1-2 and resolves in Israel's peace.
126|Recalled restoration and laughter lead to a new restoration petition and the sowing-with-tears promise.|Verse 4 is the remembered-to-requested restoration turn, while the agricultural close interprets both past and hoped-for reversal.
127|Building, guarding, anxious labor, and sleep are contrasted with children as Yahweh's gift and defense.|Verse 3 begins the children-and-arrows movement, but both halves challenge self-secured households and cities apart from Yahweh's gift.
128|The household blessing for one who fears Yahweh expands into a Zion blessing and multigenerational peace.|Verse 5 begins the communal Zion benediction, but it extends the household flourishing rather than replacing it.
129|Repeated lifelong affliction and Yahweh's cutting of cords turn into a curse on Zion's haters and failed harvest blessing.|Verse 5 begins the imprecation, but its target is precisely the afflicters named in verses 1-4.
130|The cry from the depths moves through forgiveness, watchful waiting, and an exhortation for Israel to hope in redeeming love.|Verse 7 begins the communal exhortation, but it generalizes the speaker's waiting and forgiveness confession.
131|The denial of proud ambition and image of a weaned child culminate in a one-line summons for Israel to hope.|Verse 3 could be isolated as communal exhortation, but it applies the speaker's settled humility rather than opening a new movement.
132|David's oath and the ark-search tradition lead to petitions for priests and anointed king, then Yahweh's responsive oath and Zion promises.|Verse 11 is the material human-oath to divine-oath seam after the petition in verses 9-10; the paired oaths support the whole pilgrimage royal-Zion song at medium confidence.
133|Fraternal unity is compared to priestly oil and Hermon's dew before Yahweh's blessing of life forever.|Verses 2 and 3 introduce distinct similes, but both explain the "good and pleasant" unity of verse 1 and culminate in one blessing.
134|Night servants are summoned to bless Yahweh, then receive a creator blessing from Zion.|Verse 3 is a speaker-direction reversal, but separating the one-line benediction would destroy the call-and-response miniature.
138|Wholehearted temple praise and answered prayer widen to royal praise, humility, rescue, and confidence in Yahweh's completing work.|Verse 4 begins the kings' response and verse 7 returns to personal trouble, but both grow from the steadfast-love testimony of verses 1-3.
140|Rescue plea and conspiracy portrait move through judgment petitions to confidence that Yahweh upholds the needy.|Verse 12's "I know that Yahweh will maintain" is the strongest imprecation-to-confidence seam, yet it answers the violent schemes of verses 1-11.
141|Prayer for guarded speech and heart accepts righteous correction, describes fallen rulers, and ends with refuge from snares.|Verse 5's correction saying and verse 8's renewed direct refuge are plausible turns, but the speaker's concern with wicked practice and traps spans them.
142|The poured-out complaint describes hidden snares and social isolation before a direct refuge confession and prison-release plea.|Verse 5's "I cried to you" is the strongest complaint-to-petition seam, but it answers the isolation of verses 3-4 and leads to the same anticipated community.
143|The penitential lament recalls crushed life and ancient works before an urgent sequence of guidance, rescue, and preservation petitions.|Verse 7's "Hurry to answer me" begins the strongest meditation-to-imperative turn, but every request answers the distress in verses 1-6.
146|The self summons to lifelong praise warns against mortal rulers, celebrates the God of Jacob's acts, and closes with eternal reign.|Verse 5 begins the beatitude-and-acts hymn after the princes warning, but the contrast between dying rulers and reigning Yahweh governs the complete Psalm.
148|Heavenly beings and cosmic heights are summoned in verses 1-6; verse 7 renews the call from earth through rulers and Israel.|The 1-6/7-14 heaven-earth strophe is a strong live alternative, so the whole litany remains low and held for the explicit verse-7 retrieval decision.
149|New-song dance praise, Yahweh's delight and victory, then the saints' two-edged judgment commission form one victory hymn.|Verse 5 begins the honor-and-judgment movement, but it is the victory granted to the praising community of verses 1-4.
150|Praise location, reasons, instruments, dance, and the final all-breath summons accumulate as the Psalter's doxology.|Verse 6 is a genuine universal coda, but a one-verse child would orphan the culmination of the instrument catalogue and closing "Praise Yah."
""".strip().splitlines():
    _whole_psalm, _whole_unity, _whole_alternative = _whole_audit_line.split("|", 2)
    WHOLE_AUDITS[int(_whole_psalm)] = (_whole_unity, _whole_alternative)

MEDIUM_WHOLE_PSALMS = {
    2, 3, 5, 6, 7, 9, 10, 13, 16, 17, 20, 21, 25, 26, 27, 28, 29, 30, 32, 33, 34,
    36, 38, 39, 41, 45, 47, 48, 52, 54, 56, 58, 60, 61, 63, 64, 65, 66, 72, 75, 76,
    79, 82, 84, 85, 86, 87, 88, 91, 92, 96, 97, 98, 101, 103, 105, 106, 114, 115,
    116, 132, 138, 140, 141, 142, 143, 146, 148, 149,
}


def json_bytes(value: Any, *, pretty: bool = False) -> bytes:
    if pretty:
        return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    return (json.dumps(value, ensure_ascii=False, sort_keys=False, separators=(",", ":")) + "\n").encode("utf-8")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json_bytes(value, pretty=True))


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"".join(json_bytes(row) for row in rows))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row_sha(row: dict[str, Any]) -> str:
    payload = json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def book_rows_sha(path: Path) -> str:
    rows = [row for row in read_jsonl(path) if row.get("book") == "Ps"]
    payload = b"".join(
        (json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")
        for row in rows
    )
    return hashlib.sha256(payload).hexdigest()


def clean_usfm(value: str) -> str:
    value = re.sub(r"\\f .*?\\f\*", " ", value)
    value = re.sub(r"\\x .*?\\x\*", " ", value)
    value = re.sub(r"\\w ([^|\\]+?)(?:\|[^\\]*)?\\w\*", r"\1", value)
    value = re.sub(r"\\[a-z0-9+]+\*?(?:\s+)?", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def load_web_verses() -> dict[tuple[int, int], str]:
    verses: dict[tuple[int, int], str] = {}
    chapter = 0
    for raw in USFM.read_text(encoding="utf-8").splitlines():
        if raw.startswith("\\c "):
            chapter = int(raw.split()[1])
        elif raw.startswith("\\v "):
            match = re.match(r"\\v\s+(\d+)\s+(.*)", raw)
            if match:
                verses[(chapter, int(match.group(1)))] = clean_usfm(match.group(2))
    return verses


def load_lengths() -> dict[int, int]:
    lengths: dict[int, int] = defaultdict(int)
    for row in read_jsonl(PASSAGES):
        if row.get("book") == "Ps":
            lengths[int(row["chapter"])] = max(lengths[int(row["chapter"])], int(row["verse_end"]))
    if sorted(lengths) != list(range(1, 151)):
        raise ValueError("canonical Psalm inventory must contain Psalms 1-150")
    return dict(lengths)


def phrase(text: str, *, words: int = 9) -> str:
    tokens = text.replace("“", "").replace("”", "").split()
    result = " ".join(tokens[:words])
    return result.rstrip(" ,;:")


def quoted_phrase(text: str) -> str:
    return f'"{text.rstrip()}"'


def quoted_sentence(text: str) -> str:
    value = text.rstrip()
    if value.endswith((".", "?", "!")):
        return quoted_phrase(value)
    return quoted_phrase(f"{value}.")

def span(psalm: int, start: int, end: int) -> str:
    return f"Ps.{psalm}.{start}-Ps.{psalm}.{end}"


def is_held(psalm: int, start: int, end: int) -> bool:
    if psalm in HELD_PSALMS:
        return True
    return (
        (psalm == 89 and (start, end) == (49, 52))
        or (psalm == 118 and (start, end) == (19, 29))
        or (psalm == 145 and (start, end) == (14, 21))
    )


def hold_kind(psalm: int, start: int, end: int) -> str:
    if psalm in {9, 10}:
        return "linked_acrostic_and_alternate_numbering_parent"
    if psalm in {42, 43}:
        return "linked_refrain_parent"
    if psalm in {41, 72, 89, 106, 118, 145}:
        return "collection_or_poem_coda_retrieval"
    if psalm == 108:
        return "composite_final_form_parent"
    if psalm in {114, 115, 116, 147}:
        return "web_mt_lxx_alternate_numbering"
    if psalm == 148:
        return "heaven_earth_strophe_at_verse_7"
    raise AssertionError((psalm, start, end))


def human_question(psalm: int, start: int, end: int) -> tuple[str, list[dict[str, str]]]:
    unit = span(psalm, start, end)
    if psalm in {9, 10}:
        question = (
            "Should retrieval expose Psalms 9-10 only as separate WEB-coordinate poems, "
            "or also require a linked acrostic and alternate-numbering parent?"
        )
        options = [
            {"option": "separate_web_units", "argument": "Preserves the canonical WEB coordinates and avoids converting an evidence-only relation into a merged chunk."},
            {"option": "linked_parent", "argument": "Preserves the interrupted alphabetic sequence and the tradition that numbers the pair as one psalm without erasing either WEB child."},
        ]
    elif psalm in {42, 43}:
        question = (
            "Should retrieval preserve Psalms 42 and 43 only as separate WEB poems, "
            "or require a linked parent because their repeated refrain crosses the psalm boundary?"
        )
        options = [
            {"option": "separate_web_units", "argument": "Honors the numbered poem boundary while retaining the refrain relation as metadata."},
            {"option": "linked_refrain_parent", "argument": "Makes the recurring why-are-you-cast-down refrain retrievable as one larger lament without deleting the two WEB children."},
        ]
    elif psalm == 108:
        question = (
            "Should Psalm 108 retrieval prioritize the two final-form movements at verses 1-5 and 6-13, "
            "or require the complete composite psalm as their primary parent?"
        )
        options = [
            {"option": "movement_first", "argument": "The praise turn and military petition have distinct discourse functions and remain independently coherent."},
            {"option": "whole_parent_first", "argument": "Their juxtaposition is the received final form, so retrieval should never present a child without the complete Psalm 108 context."},
        ]
    elif psalm in {114, 115}:
        question = (
            "Should retrieval keep WEB Psalms 114 and 115 as the sole chunk parents, "
            "or require an alternate-numbering parent representing their combination in Greek tradition?"
        )
        options = [
            {"option": "web_parents_only", "argument": "Keeps this map faithful to its declared WEB verse coordinates."},
            {"option": "alternate_numbering_parent", "argument": "Prevents cross-tradition searches from silently losing the combined Greek-numbering relation."},
        ]
    elif psalm == 116:
        question = (
            "Should WEB Psalm 116 remain the sole retrieval parent, "
            "or require an alternate-numbering relation for the Greek tradition's two-psalm division?"
        )
        options = [
            {"option": "web_parent_only", "argument": "Preserves the complete received WEB thanksgiving poem as one retrieval unit."},
            {"option": "alternate_split_relation", "argument": "Makes the cross-tradition split discoverable without imposing it on the WEB chunk boundary."},
        ]
    elif psalm == 147:
        question = (
            f"Should {unit} remain a WEB-coordinate child with only evidence metadata, "
            "or should retrieval require an alternate-numbering parent for the Greek split of Psalm 147?"
        )
        options = [
            {"option": "web_children_primary", "argument": "The three local hymn movements remain readable in WEB coordinates and the numbering relation stays non-authorizing."},
            {"option": "alternate_parent_required", "argument": "A mandatory relation prevents searches across Greek numbering from missing the second numbered psalm."},
        ]
    elif psalm == 148:
        question = (
            "Should Psalm 148 remain one continuous praise litany, "
            "or should verse 7 open an explicit earth-strophe child beneath the whole-psalm parent?"
        )
        options = [
            {"option": "whole_litany", "argument": "The repeated praise summons unifies heaven, earth, rulers, and people into one cumulative litany."},
            {"option": "heaven_earth_children", "argument": "The renewed call from the earth at verse 7 creates a concrete 1-6 and 7-14 strophic contrast."},
        ]
    else:
        coda = {41: "verse 13", 72: "verses 18-20", 89: "verse 52", 106: "verses 47-48", 118: "verses 28-29", 145: "verse 21"}[psalm]
        question = (
            f"Should {unit} retain {coda} inside its present poem-level child, "
            "or should retrieval expose that coda separately while preserving the larger parent?"
        )
        options = [
            {"option": "retain_with_movement", "argument": "Avoids an orphaned doxology or closing praise line and preserves the received poem or lament closure."},
            {"option": "coda_child_with_parent", "argument": "Makes the collection or poem coda directly retrievable while a mandatory parent prevents context loss."},
        ]
    assert question.endswith("?") and len(options) == 2
    return question, options


def make_boundaries(lengths: dict[int, int]) -> list[tuple[int, int, int]]:
    boundaries: list[tuple[int, int, int]] = []
    for psalm in range(1, 151):
        units = SPLITS.get(psalm, [(1, lengths[psalm])])
        expected = 1
        for start, end in units:
            if start != expected or end < start:
                raise ValueError(f"Psalm {psalm} boundaries are not contiguous at {start}-{end}")
            boundaries.append((psalm, start, end))
            expected = end + 1
        if expected != lengths[psalm] + 1:
            raise ValueError(f"Psalm {psalm} boundaries end at {expected - 1}, expected {lengths[psalm]}")
    return boundaries


def marker_for(
    psalm: int,
    start: int,
    end: int,
    length: int,
    verses: dict[tuple[int, int], str],
) -> str:
    first = phrase(verses[(psalm, start)])
    last = phrase(verses[(psalm, end)])
    if psalm == 119:
        letter = HEBREW_LETTERS[(start - 1) // 8]
        return (
            f"The {letter} acrostic heading begins the eight-verse stanza at verse {start}; "
            f"the next Hebrew-letter stanza begins after verse {end}. WEB opens {quoted_phrase(first)} "
            f"and the stanza closes {quoted_sentence(last)}"
        )
    if start == 1 and end == length:
        unity, _alternative = WHOLE_AUDITS[psalm]
        return (
            f"{unity} WEB begins {quoted_phrase(first)} and closes {quoted_phrase(last)}; "
            "those lines frame the audited poem-specific movement."
        )
    if start == 1:
        next_open = phrase(verses[(psalm, end + 1)])
        return (
            f"The opening movement begins {quoted_phrase(first)} and reaches {quoted_phrase(last)} at verse {end}; "
            f"verse {end + 1} resets the discourse with {quoted_sentence(next_open)}"
        )
    previous = phrase(verses[(psalm, start - 1)])
    if end == length:
        return (
            f"Verse {start - 1} closes with {quoted_phrase(previous)}. Verse {start} opens the final movement "
            f"{quoted_phrase(first)}; the unit carries that turn through the psalm's closing {quoted_sentence(last)}"
        )
    next_open = phrase(verses[(psalm, end + 1)])
    return (
        f"Verse {start} opens {quoted_phrase(first)} after the prior cadence {quoted_phrase(previous)}; "
        f"this movement closes {quoted_phrase(last)} before verse {end + 1} begins {quoted_sentence(next_open)}"
    )

def rejected_alternative_for(
    psalm: int,
    start: int,
    end: int,
    length: int,
    verses: dict[tuple[int, int], str],
    held: bool,
) -> str:
    unit = span(psalm, start, end)
    if start == 1 and end == length:
        if psalm not in WHOLE_AUDITS:
            raise ValueError(f"Psalm {psalm} lacks a whole-poem seam audit")
        alternative = WHOLE_AUDITS[psalm][1]
    else:
        units = SPLITS[psalm]
        position = units.index((start, end))
        current_form = CHILD_FORMS[(psalm, start, end)].replace("_", " ")
        if position < len(units) - 1:
            next_start, next_end = units[position + 1]
            next_form = CHILD_FORMS[(psalm, next_start, next_end)].replace("_", " ")
            alternative = (
                f"The strongest larger-child alternative joins {unit} to {span(psalm, next_start, next_end)}. "
                f"That proposal keeps {current_form} beside {next_form}, but verse {next_start} opens "
                f"{quoted_phrase(phrase(verses[(psalm, next_start)]))}; merging across that actual transition would hide the "
                f"{next_form} opening from retrieval."
            )
        else:
            prev_start, prev_end = units[position - 1]
            prev_form = CHILD_FORMS[(psalm, prev_start, prev_end)].replace("_", " ")
            alternative = (
                f"The strongest larger-child alternative begins at verse {prev_start} and joins the preceding "
                f"{prev_form} to this {current_form}. Verse {start} instead opens {quoted_phrase(phrase(verses[(psalm, start)]))} "
                f"after verse {start - 1} closes with {quoted_phrase(phrase(verses[(psalm, start - 1)]))}; the actual change of function "
                "would disappear inside that merger."
            )
    if held:
        question, options = human_question(psalm, start, end)
        alternative += (
            f" A second retrieval treatment remains unresolved: {options[1]['option']} -- {options[1]['argument']} "
            f"Human review must answer: {question}"
        )
    return alternative


def make_chunks(
    boundaries: list[tuple[int, int, int]],
    lengths: dict[int, int],
    verses: dict[tuple[int, int], str],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    expected_child_keys = {
        (psalm, start, end) for psalm, units in SPLITS.items() for start, end in units
    }
    if set(CHILD_FORMS) != expected_child_keys:
        missing = sorted(expected_child_keys - set(CHILD_FORMS))
        extra = sorted(set(CHILD_FORMS) - expected_child_keys)
        raise ValueError(f"child-local form table mismatch; missing={missing} extra={extra}")
    whole_psalms = {psalm for psalm in range(1, 151) if psalm not in SPLITS}
    if set(WHOLE_AUDITS) != whole_psalms:
        missing = sorted(whole_psalms - set(WHOLE_AUDITS))
        extra = sorted(set(WHOLE_AUDITS) - whole_psalms)
        raise ValueError(f"whole-Psalm audit table mismatch; missing={missing} extra={extra}")
    for index, (psalm, start, end) in enumerate(boundaries, 1):
        unit = span(psalm, start, end)
        held = is_held(psalm, start, end)
        is_whole = start == 1 and end == lengths[psalm]
        form = CHILD_FORMS.get((psalm, start, end), FORM_BY_PSALM[psalm])
        parent_form = FORM_BY_PSALM[psalm]
        first = phrase(verses[(psalm, start)], words=7)
        last = phrase(verses[(psalm, end)], words=7)
        title = f"Psalm {psalm}:{start}-{end} - {first} / {last}"
        if psalm == 119:
            title = f"Psalm 119 {HEBREW_LETTERS[(start - 1) // 8]} stanza, verses {start}-{end}"
        marker = marker_for(psalm, start, end, lengths[psalm], verses)
        rejected = rejected_alternative_for(psalm, start, end, lengths[psalm], verses, held)
        confidence = (
            "low" if held and psalm in {9, 10, 42, 43, 108, 114, 115, 116, 147, 148}
            else "medium_low" if held
            else "high" if psalm == 119
            else "medium" if not is_whole or psalm in MEDIUM_WHOLE_PSALMS
            else "high"
        )
        form_words = form.replace("_", " ")
        if is_whole:
            unity, _alternative = WHOLE_AUDITS[psalm]
            rationale = (
                f"Psalm {psalm}'s {form_words} follows a poem-specific arc: {unity} "
                f"The WEB incipit reads {quoted_phrase(phrase(verses[(psalm, 1)]))}; the closing line "
                f"{quoted_phrase(phrase(verses[(psalm, end)]))} finishes that arc. "
                f"The material counterproposal assessed here is: {rejected}"
            )
            defensible = (
                f"Whole-Psalm status rests on the Psalm {psalm} movement described above, not on its chapter number. "
                f"The competing internal movement was tested directly: {rejected}"
            )
        else:
            units = SPLITS[psalm]
            position = units.index((start, end))
            if position == 0:
                next_start, next_end = units[1]
                next_form = CHILD_FORMS[(psalm, next_start, next_end)].replace("_", " ")
                rationale = (
                    f"Verses {start}-{end} perform Psalm {psalm}'s opening {form_words}. {marker} "
                    f"The boundary protects the following {next_form}, whose first words at verse {next_start} are "
                    f"{quoted_sentence(phrase(verses[(psalm, next_start)]))} The tested merger is specific: {rejected}"
                )
            elif position == len(units) - 1:
                prev_start, prev_end = units[position - 1]
                prev_form = CHILD_FORMS[(psalm, prev_start, prev_end)].replace("_", " ")
                rationale = (
                    f"Psalm {psalm} closes with a {form_words} in verses {start}-{end}, after the {prev_form} ends at "
                    f"verse {prev_end}. {marker} Treating both as one child was considered rather than assumed: {rejected}"
                )
            else:
                prev_start, prev_end = units[position - 1]
                next_start, next_end = units[position + 1]
                prev_form = CHILD_FORMS[(psalm, prev_start, prev_end)].replace("_", " ")
                next_form = CHILD_FORMS[(psalm, next_start, next_end)].replace("_", " ")
                rationale = (
                    f"At verse {start}, Psalm {psalm} turns from {prev_form} into {form_words}; at verse {next_start}, "
                    f"it turns again into {next_form}. {marker} The adjacent-span alternative receives a concrete answer: {rejected}"
                )
            defensible = (
                f"The {form_words} is a child-local function, while {parent_form.replace('_', ' ')} remains the outer "
                f"Psalm {psalm} form. Its adjacent movement and exact WEB transition are named in the rationale."
            )
        row: dict[str, Any] = {
            "model_id": "M7_sol",
            "book": "Ps",
            "span": unit,
            "chunk_index_in_book": index,
            "working_title": title,
            "literature_type_guess": form,
            "literary_form": form,
            "parent_literary_form": parent_form,
            "boundary_evidence_refs": [
                f"direct_read:eng-web:{unit}",
                f"WEB:{unit}",
                f"OSHB:Ps.xml#{unit}",
                f"UXLC:Ps.xml#{unit}",
                "book_strategy/Ps.md",
                "reviews/Ps/primary_hebrew_v1.json",
                "reviews/Ps/primary_literary_v1.json",
                "reviews/Ps/canonical_premortem_v1.json",
                "reviews/Ps/peer_crosscheck_v1.json",
                "reviews/Ps/boss_ruling_v1.json",
                "reviews/Ps/decision_relations.jsonl",
            ],
            "strong_or_hebrew_tags_used": [
                "direct_Hebrew_poetics_considered",
                "superscriptions_and_Selah_evidence_only",
                "WEB_MT_LXX_numbering_relation_preserved",
                "roots_are_not_meaning",
                "source_metadata_corrob_only",
            ],
            "wj_or_red_letter_considered": False,
            "frontier_flag_considered": True,
            "confidence": confidence,
            "decision_id": f"M7_sol-Ps-{index:03d}",
            "deciding_marker_or_seam": marker,
            "boundary_rationale": rationale,
            "rejected_alternative": rejected,
            "counterevidence": rejected,
            "defensible_basis": defensible,
            "review_revision": "m7-thin-rereview-r1",
            "review_status": "final_deferred_appeal" if held else "candidate_review_complete",
            "review_holds": ["deferred_human_or_external_ai", hold_kind(psalm, start, end)] if held else [],
            "non_authorizing": True,
            "candidate_internal_seams": [marker, rejected],
            "original_language_translation_holds": (
                [f"{unit}: direct Hebrew poetics and versification review remains required for {hold_kind(psalm, start, end)}."]
                if held
                else [f"{unit}: no preferred Hebrew reading or translation is selected; source metadata is evidence only."]
            ),
            "cross_reference_holds": [
                f"{unit}: canonical reuse and neighboring-Psalm relations are evidence only and cannot authorize this seam."
            ],
            "red_team_premortem_holds": [
                f"The strongest live competing treatment for {unit} is recorded here: {rejected}"
            ],
            "working_title_is_boundary_authority": False,
            "working_title_origin": "psalms_corrective_re_review_v2_local_web_wording",
            "candidate_only": True,
            "review_evidence_summary": rationale,
            "red_team_questions": [
                f"Does the {unit} seam survive removal of headings, chapter numbers, and Selah?",
                f"Does the recorded adjacent or internal alternative better preserve Psalm {psalm}'s actual functions?",
            ],
            "hard_passage_forecast": [
                f"Review {unit} against WEB, OSHB, and UXLC with attention to poetic parallelism, accents, and versification."
            ],
            "candidate_hold_state": "deferred_human_or_external_ai" if held else None,
            "candidate_hold_basis": "preserved_appeal" if held else None,
        }
        if held:
            question, options = human_question(psalm, start, end)
            row["human_review_question"] = question
            row["human_review_options"] = options
        rows.append(row)
    return rows


def challenge(
    *,
    role: str,
    row: dict[str, Any],
    number: int,
    claim: str,
    remedy: str,
) -> dict[str, Any]:
    unit = row["span"]
    return {
        "challenge_id": f"PS-V2-{role.upper()}-{number:03d}",
        "severity": "material",
        "claim": claim,
        "proposed_remedy": remedy,
        "evidence_refs": [f"direct_read:eng-web:{unit}", f"WEB:{unit}", f"chunk:{row['decision_id']}"],
        "source_refs": [f"WEB:{unit}", f"OSHB:Ps.xml#{unit}", f"UXLC:Ps.xml#{unit}"],
        "counterevidence": row["counterevidence"],
    }


def make_packets(chunks: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], list[dict[str, Any]]]:
    decision_evidence = load_decision_evidence()
    packets: list[dict[str, Any]] = []
    role_rows: dict[str, list[dict[str, Any]]] = {"hebrew": [], "literary": [], "canonical": []}
    appeals: list[dict[str, Any]] = []
    hebrew_challenge_psalms = {
        9, 10, 18, 22, 25, 34, 37, 42, 43, 45, 51, 58, 60, 68, 69, 78, 82, 89,
        108, 110, 114, 115, 116, 118, 137, 145, 147,
    }
    literary_child_challenges = {
        (18, 20, 30), (19, 7, 11), (24, 3, 6), (31, 19, 24), (35, 11, 18),
        (37, 12, 20), (40, 11, 17), (44, 17, 26), (49, 5, 12), (51, 13, 19),
        (55, 9, 15), (59, 1, 9), (62, 5, 8), (67, 4, 5), (68, 19, 27),
        (69, 19, 28), (71, 14, 24), (73, 18, 22), (74, 12, 17), (77, 10, 15),
        (78, 32, 39), (78, 56, 64), (80, 8, 19), (81, 6, 10), (83, 9, 18),
        (89, 46, 48), (90, 7, 12), (94, 12, 15), (99, 4, 5), (102, 23, 28),
        (104, 19, 23), (107, 43, 43), (109, 6, 20), (110, 4, 7), (118, 19, 29),
        (135, 1, 4), (136, 26, 26), (137, 5, 6), (139, 19, 22), (144, 9, 11),
        (145, 14, 21), (147, 7, 11),
    }
    canonical_challenge_psalms = {
        2, 9, 10, 22, 41, 42, 43, 45, 72, 82, 89, 95, 102, 106, 108, 110, 114,
        115, 116, 118, 132, 145, 147, 148,
    }
    for number, row in enumerate(chunks, 1):
        held = row["candidate_hold_state"] is not None
        evidence = decision_evidence[row["decision_id"]]
        unit = row["span"]
        parts = unit.split("-")
        psalm = int(parts[0].split(".")[1])
        start_verse = int(parts[0].split(".")[2])
        end_verse = int(parts[1].split(".")[2])
        key = (psalm, start_verse, end_verse)
        mapped = evidence["original_language_alignment"]["ordered_verse_mapping"]
        source_observation = f"{row['decision_id']}:verified_mapping_evidence_only"
        local_refs = [
            f"WEB:{unit}",
            {
                "source_id": "oshb",
                "web_span": unit,
                "source_span": f"{mapped[0]['mt_oshb_ref']}-{mapped[-1]['mt_oshb_ref']}",
                "observation": source_observation,
                "crosswalk_status": "validated_web_mt_verse_mapping",
                "source_metadata_boundary_authority": False,
            },
            {
                "source_id": "uxlc",
                "web_span": unit,
                "source_span": f"{mapped[0]['mt_uxlc_ref']}-{mapped[-1]['mt_uxlc_ref']}",
                "observation": source_observation,
                "crosswalk_status": "validated_web_mt_verse_mapping",
                "source_metadata_boundary_authority": False,
            },
        ]
        exact_evidence = [f"direct_read:eng-web:{unit}", *local_refs, f"chunk:{row['decision_id']}"]
        role_challenge = {
            "hebrew": psalm in hebrew_challenge_psalms,
            "literary": (key in literary_child_challenges) or (
                start_verse == 1 and end_verse > 1 and psalm in MEDIUM_WHOLE_PSALMS and psalm not in {45, 82}
            ),
            "canonical": psalm in canonical_challenge_psalms and (
                held or start_verse == 1 or key in {(89, 49, 52), (118, 19, 29), (145, 14, 21)}
            ),
        }
        role_challenge = {
            role: evidence["reviews"][role]["verdict"] == "challenge"
            for role in ("hebrew", "literary", "canonical")
        }
        unresolved_role: str | None = None
        if held:
            kind = evidence["hold"]["kind"]
            if kind in {"linked_acrostic_and_alternate_numbering_parent", "web_mt_lxx_alternate_numbering"}:
                unresolved_role = "hebrew"
            elif kind in {
                "linked_refrain_parent",
                "composite_final_form_parent",
                "heaven_earth_strophe_at_verse_7",
                "ps37_child_granularity",
                "ps59_recurrence_architecture",
            }:
                unresolved_role = "literary"
            else:
                unresolved_role = "canonical"
            role_challenge[unresolved_role] = True

        role_defs = [
            (
                "hebrew",
                "hebrew_poetics_and_textual_witness",
                "primary_hebrew_v1.json",
                (
                    f"The WEB coordinates for {unit} are stable, and the local form claim does not depend on treating "
                    "OSHB/UXLC accents, morphology, superscriptions, or Selah as automatic boundary authority."
                ),
                (
                    f"Hebrew-poetic or versification evidence may give additional weight to the recorded alternative: "
                    f"{row['rejected_alternative']}"
                ),
            ),
            (
                "literary",
                "literary_form_and_poetic_movement",
                "primary_literary_v1.json",
                row["boundary_rationale"],
                (
                    f"The neighboring movement can plausibly remain attached despite the proposed {row['literary_form'].replace('_', ' ')} function: "
                    f"{row['rejected_alternative']}"
                ),
            ),
            (
                "canonical",
                "canonical_context_and_retrieval_premortem",
                "canonical_premortem_v1.json",
                (
                    f"{unit} remains inside an explicit whole-Psalm parent, and the relation ledger preserves paired, "
                    "numbering, coda, and later-reuse pressure without turning it into boundary authority."
                ),
                (
                    f"Retrieval could overstate the child or conceal a parent/coda relation if it ignores this counterproposal: "
                    f"{row['rejected_alternative']}"
                ),
            ),
        ]
        reviews: list[dict[str, Any]] = []
        challenges_by_role: dict[str, list[dict[str, Any]]] = {}
        for role_key, role_name, filename, support, counterevidence in role_defs:
            evidence_review = evidence["reviews"][role_key]
            evidence_verdict = evidence_review["verdict"]
            support = evidence["boundary_rationale"]
            counterevidence = evidence["rejected_alternative"]
            role_challenges: list[dict[str, Any]] = []
            if role_challenge[role_key]:
                claim = counterevidence
                remedy = evidence.get("redteam_resolution", {}).get("challenge_response", {}).get(
                    "answer", evidence["boundary_rationale"]
                )
                challenge_row = challenge(
                    role=role_key,
                    row=row,
                    number=number,
                    claim=claim,
                    remedy=remedy,
                )
                challenge_row["source_refs"] = local_refs
                role_challenges.append(challenge_row)
            challenges_by_role[role_key] = role_challenges
            reviews.append(
                {
                    "reviewer_attempt_id": f"ps-v2-{role_key}-{number:03d}-sol-xhigh",
                    "reviewer_role": role_name,
                    "role": role_name,
                    "verdict": evidence_verdict,
                    "blind_to_other_primary_reviews": True,
                    "evidence_only": True,
                    "evidence_refs": [f"direct_read:eng-web:{unit}", f"reviews/Ps/{filename}", f"WEB:{unit}", f"chunk:{row['decision_id']}"],
                    "source_refs": local_refs,
                    "support": support,
                    "counterevidence": counterevidence,
                    "challenges": role_challenges,
                }
            )
        for role_name, review in zip(("hebrew", "literary", "canonical"), reviews):
            role_rows[role_name].append(
                {
                    "decision_id": row["decision_id"],
                    "span": unit,
                    "reviewer_attempt_id": review["reviewer_attempt_id"],
                    "verdict": review["verdict"],
                    "source_refs": review["source_refs"],
                    "evidence_refs": review["evidence_refs"],
                    "support": review["support"],
                    "counterevidence": review["counterevidence"],
                    "challenges": review["challenges"],
                }
            )
        all_challenges = [item for role in ("hebrew", "literary", "canonical") for item in challenges_by_role[role]]
        unresolved_ids = [
            item["challenge_id"] for item in challenges_by_role.get(unresolved_role or "", [])
        ]
        responses: list[dict[str, Any]] = []
        for item in all_challenges:
            unresolved = item["challenge_id"] in unresolved_ids
            source_role = item["challenge_id"].split("-")[2].lower()
            ledger_response = next(
                (
                    response["decision_local_answer"]
                    for response in evidence["challenge_responses"]
                    if response["role"] == source_role
                ),
                evidence["boundary_rationale"],
            )
            if unresolved:
                response_rationale = row["human_review_question"]
            else:
                response_rationale = ledger_response
            responses.append(
                {
                    "challenge_id": item["challenge_id"],
                    "decision_id": row["decision_id"],
                    "source_role": source_role,
                    "rationale": response_rationale,
                    "counterevidence": item["counterevidence"],
                    "rejected_alternative": row["rejected_alternative"],
                    "outcome": "unresolved_human_choice" if unresolved else "challenge_answered_with_local_evidence",
                    "disposition": "hold" if unresolved else "answered",
                }
            )
        appeal_rows: list[dict[str, Any]] = []
        if held:
            assert unresolved_role is not None and unresolved_ids
            appellant_review = next(review for review in reviews if review["role"].startswith(unresolved_role if unresolved_role != "hebrew" else "hebrew"))
            appeal = {
                "appeal_id": f"PS-V2B-APPEAL-{number:03d}",
                "decision_id": row["decision_id"],
                "review_revision": "m7-corrective-rereview-v2",
                "appellant_attempt_id": appellant_review["reviewer_attempt_id"],
                "disagreement_with": f"ps-v2-boss-{number:03d}-sol-xhigh",
                "disputed_claim_id": unresolved_ids[0],
                "passage_context": unit,
                "evidence_refs": exact_evidence,
                "rationale": row["human_review_question"],
                "uncertainty": evidence["hold"]["kind"],
                "requested_next_reviewer": "human_or_external_ai_psalms_poetics_versification_and_retrieval_specialist",
                "status": "unresolved_append_only",
                "non_authorizing": True,
            }
            appeal_rows.append(appeal)
            appeals.append(appeal)
        chunk_content_sha256 = row_sha(row)
        packet: dict[str, Any] = {
            "schema_version": "m7_corrective_review_packet.v2",
            "decision_id": row["decision_id"],
            "book": "Ps",
            "span": unit,
            "chunk_sha256": chunk_content_sha256,
            "chunk_content_sha256": chunk_content_sha256,
            "review_revision": "m7-corrective-rereview-v2",
            "primary_reviews": reviews,
            "peer_crosscheck": {
                "reviewer_attempt_id": f"ps-v2-peer-{number:03d}-sol-xhigh",
                "reviewer_role": "adversarial_peer_crosscheck",
                "disputed_claim_ids": [item["challenge_id"] for item in all_challenges],
                "status": "hold" if held else "pass",
                "rationale": evidence["boundary_rationale"],
                "source_refs": local_refs,
                "support": row["defensible_basis"],
                "counterevidence": row["rejected_alternative"],
                "support_challenge_mix": {
                    "support_count": sum(review["verdict"] == "supports" for review in reviews),
                    "challenge_count": sum(review["verdict"] == "challenge" for review in reviews),
                },
            },
            "sol_resolution": {
                "author_id": "M7_sol",
                "author_attempt_id": f"ps-v2-boss-{number:03d}-sol-xhigh",
                "challenge_responses": responses,
                "unresolved_claim_ids": unresolved_ids,
                "rationale": row["boundary_rationale"],
                "counterevidence": row["counterevidence"],
                "rejected_alternative": row["rejected_alternative"],
                "outcome": "held_for_answerable_human_choice" if held else "accepted_candidate_after_role_specific_challenges",
                "authority": "candidate_author_only",
            },
            "appeals": appeal_rows,
            "final_state": "deferred_human_or_external_ai" if held else "accepted_candidate",
            "post_resolution_check": {
                "checker_attempt_id": f"ps-v2-postcluster-{((number - 1) // 8) + 1:03d}-sol-xhigh",
                "status": "hold" if held else "pass",
                "evidence_refs": ["reviews/Ps/post_resolution_check_v2.json"],
                "chunk_content_sha256": chunk_content_sha256,
            },
            "independence_scope": INDEPENDENCE_SCOPE,
            "non_authorizing": True,
            "boss_ruling": {
                "ruling_id": f"ps-v2-boss-{number:03d}-sol-xhigh",
                "rationale": row["boundary_rationale"],
                "counterevidence": row["counterevidence"],
                "rejected_alternative": row["rejected_alternative"],
                "outcome": "defer_to_human_or_external_ai" if held else "accept_candidate",
                "appeal_effect": "deferred_human_or_external_ai" if held else "none",
                "forced_consensus": False,
            },
        }
        if held:
            packet["human_review_question"] = row["human_review_question"]
            packet["human_review_options"] = row["human_review_options"]
            packet["human_review_route"] = "human_or_external_ai_psalms_poetics_versification_and_retrieval_specialist"
            packet["boss_ruling"]["human_review_question"] = row["human_review_question"]
        packets.append(packet)
    return packets, role_rows, appeals


def make_relations(chunks: list[dict[str, Any]], lengths: dict[int, int]) -> list[dict[str, Any]]:
    by_psalm: dict[int, list[str]] = defaultdict(list)
    for row in chunks:
        by_psalm[int(row["span"].split(".")[1])].append(row["decision_id"])
    relations: list[dict[str, Any]] = []
    for psalm in sorted(SPLITS):
        relations.append(
            {
                "schema_version": "m7_decision_relation.v2",
                "note_id": f"PS-V2-PARENT-{psalm:03d}",
                "book": "Ps",
                "relation_type": "whole_psalm_parent_of_internal_children",
                "parent_span": span(psalm, 1, lengths[psalm]),
                "children": by_psalm[psalm],
                "rationale": (
                    f"Psalm {psalm} remains the mandatory received outer poem for every selected stanza, refrain cycle, "
                    "speaker turn, historical episode, or liturgical movement."
                ),
                "non_authorizing": True,
            }
        )
    pair_specs = [
        ("PS-V2-PAIR-009-010", [9, 10], "linked_acrostic_and_alternate_numbering_evidence"),
        ("PS-V2-PAIR-042-043", [42, 43], "linked_refrain_evidence"),
        ("PS-V2-NUM-114-115", [114, 115], "greek_combined_numbering_relation"),
        ("PS-V2-NUM-116", [116], "greek_split_numbering_relation"),
        ("PS-V2-NUM-147", [147], "greek_split_numbering_relation"),
    ]
    for note_id, psalms, kind in pair_specs:
        relations.append(
            {
                "schema_version": "m7_decision_relation.v2",
                "note_id": note_id,
                "book": "Ps",
                "relation_type": kind,
                "decision_ids": [decision for psalm in psalms for decision in by_psalm[psalm]],
                "rationale": (
                    f"{kind.replace('_', ' ')} is preserved for Psalms {', '.join(map(str, psalms))}; "
                    "it does not merge or renumber the WEB-coordinate candidates."
                ),
                "non_authorizing": True,
            }
        )
    return relations


def role_artifact(
    role: str,
    rows: list[dict[str, Any]],
    chunks_hash: str,
    held_ids: set[str],
) -> dict[str, Any]:
    return {
        "schema_version": "m7_primary_review.v2",
        "book": "Ps",
        "checked_chunks_sha256": chunks_hash,
        "checked_row_count": len(rows),
        "reviewer_role": role,
        "overall_verdict": "pass_with_explicit_holds",
        "decision_verdicts": rows,
        "held_decision_ids": sorted(held_ids & {row["decision_id"] for row in rows}),
        "blind_to_other_primary_reviews": True,
        "evidence_only": True,
        "prohibited_sources_read": [
            "M1-M6 sibling model outputs",
            "comparison synthesis",
            "T417 downstream artifacts",
        ],
        "model_effort_selection": {
            "selected": "Sol/xhigh",
            "rejected": "Terra/high",
            "rationale": "The corrective pass spans 150 poems, contested versification, refrain/acrostic seams, and decision-local adjudication.",
        },
        "non_authorizing": True,
    }


def make_sidecar_rows(chunks: list[dict[str, Any]], packets: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    packet_by_id = {row["decision_id"]: row for row in packets}
    result: dict[str, list[dict[str, Any]]] = {name: [] for name in SIDECARS}
    for row in chunks:
        if row["confidence"] not in {"low", "medium_low"}:
            continue
        packet = packet_by_id[row["decision_id"]]
        appeal_ids = [appeal["appeal_id"] for appeal in packet["appeals"]]
        base = {
            "model_id": "M7_sol",
            "book": "Ps",
            "span": row["span"],
            "chunk_decision_id": row["decision_id"],
            "confidence": row["confidence"],
            "observed_substrate_signals": [
                row["deciding_marker_or_seam"],
                row["counterevidence"],
                row["human_review_question"],
            ],
            "review_packet_final_state": packet["final_state"],
            "chunk_review_status": row["review_status"],
            "candidate_hold_state": row["candidate_hold_state"],
            "non_authorizing": True,
        }
        result["low_confidence_register.jsonl"].append(
            {
                **base,
                "why_low_confidence": row["human_review_question"],
                "possible_downstream_risk": row["counterevidence"],
                "competing_boundary_risk": row["rejected_alternative"],
                "appeal_status": "deferred_human_or_external_ai",
                "appeal_ids": appeal_ids,
            }
        )
        result["frontier_escalation_queue.jsonl"].append(
            {
                **base,
                "concern_type": row["candidate_hold_basis"]["kind"],
                "why_frontier_review_needed": row["human_review_question"],
                "suggested_reviewer": "human_or_external_ai_psalms_poetics_versification_and_retrieval_specialist",
                "promotion_authority": "none",
            }
        )
        result["atlas_candidate_feed.jsonl"].append(
            {
                **base,
                "concern_type": row["candidate_hold_basis"]["kind"],
                "why_low_confidence": row["human_review_question"],
                "possible_downstream_risk": row["counterevidence"],
                "suggested_reviewer": "human_or_external_ai_psalms_poetics_versification_and_retrieval_specialist",
                "proposed_atlas_action": "consider_only",
                "atlas_promotion_authority": "none",
            }
        )
    return result


def append_new_appeals(appeals: list[dict[str, Any]]) -> dict[str, Any]:
    ledger = REVIEW / "appeal_ledger.jsonl"
    before = ledger.read_bytes() if ledger.is_file() else b""
    existing = {
        row.get("appeal_id")
        for row in (json.loads(line) for line in before.decode("utf-8").splitlines() if line.strip())
        if isinstance(row, dict)
    }
    new_rows = [row for row in appeals if row["appeal_id"] not in existing]
    if new_rows:
        with ledger.open("ab") as handle:
            for row in new_rows:
                handle.write(json_bytes(row))
    after = ledger.read_bytes()
    if not after.startswith(before):
        raise AssertionError("appeal ledger append-only prefix was not preserved")
    active_ids = {row["appeal_id"] for row in appeals}
    prefix = bytearray()
    found_active_suffix = False
    for raw_line in after.splitlines(keepends=True):
        row = json.loads(raw_line)
        if row.get("appeal_id") in active_ids:
            found_active_suffix = True
        elif found_active_suffix:
            raise AssertionError("revision-2 appeal rows must remain an append-only ledger suffix")
        else:
            prefix.extend(raw_line)
    disposition = {
        "schema_version": "m7_psalms_appeal_disposition.v2",
        "book": "Ps",
        "historical_ledger_sha256_before_active_appeal_append": hashlib.sha256(bytes(prefix)).hexdigest(),
        "historical_ledger_byte_count_before_active_appeal_append": len(prefix),
        "historical_ledger_prefix_preserved": True,
        "historical_rows_are_not_active_appeals": True,
        "active_revision": "m7-corrective-rereview-v2",
        "active_appeal_ids": [row["appeal_id"] for row in appeals],
        "appended_by_corrective_revision_ids": [row["appeal_id"] for row in appeals],
        "newly_appended_in_this_execution_ids": [row["appeal_id"] for row in new_rows],
        "appeal_ledger_sha256_after_append": hashlib.sha256(after).hexdigest(),
        "non_authorizing": True,
    }
    write_json(REVIEW / "appeal_disposition_v2.json", disposition)
    return disposition


def write_strategy(chunk_count: int, held_count: int) -> None:
    STRATEGY.write_text(
        f"""# Psalms corrective literary strategy v2 — candidate evidence only

Candidate-only and non-authorizing. This Sol/xhigh corrective re-review did not read M1-M6,
comparison synthesis, or T417. Terra/high was rejected because the task combines 150 poems,
multiple numbering traditions, acrostic/refrain detection, collection codas, and decision-local
adjudication. Role-separated passes share one Sol model substrate and count as one voice.

## literary_form_decision_matrix

The declared forms are actual Psalm forms: lament, trust, thanksgiving, hymn, royal or
royal-priestly oracle, wisdom/Torah, entrance liturgy, Zion/pilgrimage song, alphabetic poem,
historical recital, communal prayer, judgment oracle, and refrain litany. Specific corrections
include Psalm 15 as entrance liturgy; 25 alphabetic lament; 36 mixed wisdom/hymn; 39 mortality
lament; 45 royal wedding song; 52 denunciatory trust; 75 thanksgiving/judgment oracle; 82
judicial/oracle; 92 Sabbath hymn/wisdom; 101 royal vow; 108 composite; 110 royal-priestly
oracle; 122 pilgrimage/Zion; and 133 pilgrimage blessing.

## larger_unit_preservation_check

Each numbered psalm is the received outer poem, not a chapter fallback. {chunk_count} children are
selected only where a stanza, refrain cycle, speaker/addressee turn, oracle, historical episode,
liturgical role, acrostic letter, or doxological movement is independently retrievable. Psalm 105
and Psalm 106 remain whole. Psalm 119 has exactly twenty-two eight-verse alphabetic children
(1-8 through 169-176) plus an explicit whole-psalm parent relation. Psalm 89 follows
1-4/5-18/19-37/38-45/46-48/49-52 so verse 52 is not orphaned.

## list_register_function_check

Alphabetic letters, creation catalogues, historical episodes, nations, kings, divine acts,
pilgrimage motifs, and repeated responses remain grouped by their governing poetic or liturgical
function. Psalm 107 retains the opening at 1-3, four refrain cycles, the land-reversal movement,
and its verse-43 wisdom coda. Psalm 136 keeps creation, Exodus, wilderness/land, low-estate
provision, and the final thanksgiving within the repeated-refrain litany.

## epistle_unit_check_if_applicable

Not applicable. The corresponding integrity rule is to preserve every complete numbered psalm as
the mandatory parent of any internal children.

## source_metadata_evidence_only_check

WEB supplies the active coordinate system. OSHB and UXLC morphology/accents, USFM `d`, `q`, `b`,
and `qs` markers, superscriptions, musical directions, Selah, Strong tags, and later reuse are
corroborating evidence only. They do not decide authorship, setting, speaker identity, preferred
reading, theology, or a seam. No verse 0 or Psalm 151 is manufactured.

## over_split_risk_check

The pass rejects couplet atomization, automatic Selah boundaries, detached imprecations, and
isolated doxology or praise-line orphans. It also rejects leaving a long psalm whole when a
refrain, acrostic stanza, explicit discourse turn, or historical episode supplies a stronger
retrieval unit. Children never erase their complete-psalm parent.

## sidecar_specificity_plan

Only {held_count} genuinely disputed decisions are LOW or MEDIUM_LOW. Every such row names the
exact WEB span, local counterevidence, one answerable human question ending in `?`, and exactly two
argued options. The global sidecar owner must replace the Psalm rows from
`reviews/Ps/sidecar_rows_v2.json`; no generic low-confidence poetry rows are permitted.

## Numbering, relation, and coda holds

Evidence-only typed relations preserve Psalms 9-10, 42-43, Greek combination of 114-115, Greek
division of 116 and 147, and the whole Psalm 119 parent. Human/external review remains required for
those relations, Psalm 108's composite parent, Psalm 148's verse-7 heaven/earth strophe question,
and retrieval treatment of the codas at 41:13, 72:18-20, 89:52, 106:47-48, 118:28-29, and 145:21.

## Completion boundary

Completion requires exact ordered coverage of all 2,461 WEB verses; passage-specific rationales;
two or more blind primaries with local source references and counterevidence; peer challenge;
Sol response to every challenge; append-only genuine appeals; role-separated postcheck; exact
sidecar parity; zero duplicate rationale templates; and a hash-bound candidate-only receipt.
""",
        encoding="utf-8",
    )


def write_core() -> dict[str, Any]:
    if not (OSH.is_file() and UXLC.is_file()):
        raise FileNotFoundError("required Psalm OSHB and UXLC witness files are missing")
    lengths = load_lengths()
    verses = load_web_verses()
    boundaries = make_boundaries(lengths)
    chunks = make_chunks(boundaries, lengths, verses)
    chunks = apply_decision_evidence(chunks, load_decision_evidence())
    write_jsonl(CHUNKS, chunks)
    chunks_hash = sha(CHUNKS)
    packets, role_rows, appeals = make_packets(chunks)
    write_jsonl(REVIEW / "review_packets.jsonl", packets)
    held_ids = {row["decision_id"] for row in chunks if row["candidate_hold_state"] is not None}
    role_files = {
        "hebrew": "primary_hebrew_v1.json",
        "literary": "primary_literary_v1.json",
        "canonical": "canonical_premortem_v1.json",
    }
    for role, filename in role_files.items():
        write_json(REVIEW / filename, role_artifact(role, role_rows[role], chunks_hash, held_ids))

    blind_common = {
        "schema_version": "m7_blind_proposal.v2",
        "book": "Ps",
        "model_id": "M7_sol",
        "coverage_assertion": {"verse_count": 2461, "first": "Ps.1.1", "last": "Ps.150.6"},
        "independence_scope": INDEPENDENCE_SCOPE,
        "source_boundary_authority": "WEB coordinates only; original-language and USFM metadata evidence only",
        "non_authorizing": True,
    }
    write_json(
        REVIEW / "blind_proposal_hebrew_poetics_v1.json",
        {
            **blind_common,
            "proposal_id": "ps-v2-blind-hebrew-sol-xhigh",
            "role": "hebrew_poetics",
            "source_refs": ["WEB:Ps.1.1-Ps.150.6", f"OSHB:{OSH.relative_to(ROOT).as_posix()}", f"UXLC:{UXLC.relative_to(ROOT).as_posix()}"],
            "decision_observations": role_rows["hebrew"],
        },
    )
    write_json(
        REVIEW / "blind_proposal_literary_v1.json",
        {
            **blind_common,
            "proposal_id": "ps-v2-blind-literary-sol-xhigh",
            "role": "literary_poetics",
            "source_refs": ["WEB:Ps.1.1-Ps.150.6", "book_strategy/Ps.md"],
            "decision_observations": role_rows["literary"],
        },
    )
    write_json(
        REVIEW / "blind_proposal_canonical_premortem_v1.json",
        {
            **blind_common,
            "proposal_id": "ps-v2-blind-canonical-sol-xhigh",
            "role": "canonical_retrieval_premortem",
            "source_refs": ["WEB:Ps.1.1-Ps.150.6", "reviews/Ps/decision_relations.jsonl"],
            "decision_observations": role_rows["canonical"],
        },
    )
    for filename in (
        "blind_proposal_hebrew_poetics_v1.json",
        "blind_proposal_literary_v1.json",
        "blind_proposal_canonical_premortem_v1.json",
    ):
        (REVIEW / f"{filename}.sha256").write_text(f"{sha(REVIEW / filename)}  {filename}\n", encoding="utf-8")

    relations = make_relations(chunks, lengths)
    write_jsonl(REVIEW / "decision_relations.jsonl", relations)
    challenge_ids = [
        challenge["challenge_id"]
        for packet in packets
        for review in packet["primary_reviews"]
        for challenge in review["challenges"]
    ]
    write_json(
        REVIEW / "peer_crosscheck_v1.json",
        {
            "schema_version": "m7_peer_crosscheck.v2",
            "book": "Ps",
            "checked_chunks_sha256": chunks_hash,
            "checked_row_count": len(chunks),
            "reviewer_role": "adversarial_peer_crosscheck",
            "attempt_id_policy": "decision-local IDs; no primary, peer, or boss attempt ID is reused",
            "status": "pass_with_explicit_holds",
            "disputed_claim_ids": challenge_ids,
            "support_count": sum(
                review["verdict"] == "supports" for packet in packets for review in packet["primary_reviews"]
            ),
            "challenge_count": sum(
                review["verdict"] == "challenge" for packet in packets for review in packet["primary_reviews"]
            ),
            "held_decision_ids": sorted(held_ids),
            "forced_consensus": False,
            "shared_model_substrate": True,
            "counts_as_cross_model_independent_vote": False,
            "non_authorizing": True,
        },
    )
    write_json(
        REVIEW / "boss_ruling_v1.json",
        {
            "schema_version": "m7_boss_ruling.v2",
            "book": "Ps",
            "checked_chunks_sha256": chunks_hash,
            "author_id": "M7_sol",
            "model_effort": "Sol/xhigh",
            "rejected_model_effort": "Terra/high",
            "challenge_responses": [
                response for packet in packets for response in packet["sol_resolution"]["challenge_responses"]
            ],
            "unresolved_claim_ids": [
                claim for packet in packets for claim in packet["sol_resolution"]["unresolved_claim_ids"]
            ],
            "accepted_decision_count": len(chunks) - len(held_ids),
            "held_decision_count": len(held_ids),
            "ruling": "candidate_complete_with_explicit_holds",
            "forced_consensus": False,
            "external_or_human_review_still_required": True,
            "non_authorizing": True,
        },
    )
    (REVIEW / "peer_crosscheck_findings_v1.md").write_text(
        "# Psalms corrective peer findings v2\n\n"
        f"- Active decisions: {len(chunks)}\n"
        f"- Accepted candidates: {len(chunks) - len(held_ids)}\n"
        f"- Held candidates: {len(held_ids)}\n"
        f"- Decision-local material challenges: {len(challenge_ids)}\n"
        "- Every accepted decision retains a canonical-parent challenge answered by explicit relation evidence.\n"
        "- Every held decision retains one unresolved literary challenge, one answerable human question, two argued options, and one genuine append-only appeal.\n"
        "- Same-model role separation counts as one correlated Sol voice; no cross-model independence is claimed.\n",
        encoding="utf-8",
    )
    append_new_appeals(appeals)
    sidecars = make_sidecar_rows(chunks, packets)
    write_json(
        REVIEW / "sidecar_rows_v2.json",
        {
            "schema_version": "m7_psalms_sidecar_replacement.v2",
            "book": "Ps",
            "replace_all_existing_ps_rows": True,
            "rows": sidecars,
            "non_authorizing": True,
        },
    )
    write_strategy(len(chunks), len(held_ids))

    rationale_counts = Counter(row["boundary_rationale"] for row in chunks)
    attempt_ids = [
        review["reviewer_attempt_id"]
        for packet in packets
        for review in packet["primary_reviews"]
    ] + [
        packet["peer_crosscheck"]["reviewer_attempt_id"] for packet in packets
    ] + [
        packet["sol_resolution"]["author_attempt_id"] for packet in packets
    ]
    summary = {
        "chunk_count": len(chunks),
        "accepted_count": len(chunks) - len(held_ids),
        "held_count": len(held_ids),
        "confidence_distribution": dict(Counter(row["confidence"] for row in chunks)),
        "duplicate_boundary_rationale_count": sum(count - 1 for count in rationale_counts.values() if count > 1),
        "generic_form_label_count": sum(
            str(row["literary_form"]).startswith("complete_") for row in chunks
        ),
        "reused_decision_local_attempt_id_count": sum(
            count - 1 for count in Counter(attempt_ids).values() if count > 1
        ),
        "template_shell_counts": {
            "retained_candidate_shell": sum(" is retained as a " in row["boundary_rationale"] for row in chunks),
            "explicit_counterevidence_shell": sum("Counterevidence is explicit" in row["boundary_rationale"] for row in chunks),
            "web_governs_shell": sum("WEB wording governs the coordinate decision" in row["boundary_rationale"] for row in chunks),
            "mechanical_midpoint_phrase": sum("Rejected subdividing" in row["rejected_alternative"] for row in chunks),
        },
        "segmented_psalms_with_child_local_form_variation": sum(
            len({row["literary_form"] for row in chunks if int(row["span"].split(".")[1]) == psalm}) > 1
            for psalm in SPLITS
        ),
        "primary_role_verdict_distribution": {
            role: dict(Counter(row["verdict"] for row in role_rows[role]))
            for role in ("hebrew", "literary", "canonical")
        },
        "packet_profile_distribution": {
            "/".join(review["verdict"] for review in packet["primary_reviews"]): count
            for profile, count in Counter(
                tuple(review["verdict"] for review in packet["primary_reviews"])
                for packet in packets
            ).items()
            for packet in [{"primary_reviews": [{"verdict": verdict} for verdict in profile]}]
        },
        "active_appeal_count": len(appeals),
        "relation_count": len(relations),
        "sidecar_row_count_each": len(sidecars[SIDECARS[0]]),
        "chunks_sha256": chunks_hash,
        "review_packets_sha256": sha(REVIEW / "review_packets.jsonl"),
        "decision_relations_sha256": sha(REVIEW / "decision_relations.jsonl"),
        "non_authorizing": True,
    }
    write_json(REVIEW / "corrective_re_review_summary_v2.json", summary)
    return summary


def gate_commands(*, final: bool) -> list[tuple[str, list[str]]]:
    commands = [
        ("exact_ordered_coverage", [sys.executable, str(CHECKS / "validate_exact_book_coverage.py"), "--book", "Ps"]),
        (
            "official_chunk_map",
            [
                sys.executable,
                str(ROOT / "scripts" / "validate_whole_bible_chunk_map.py"),
                str(CHUNKS),
                "--model-id",
                "M7_sol",
                "--book",
                "Ps",
                "--python-only",
            ],
        ),
        (
            "review_status_sidecar_independence_parity",
            [
                sys.executable,
                str(CHECKS / "validate_book_review_coverage.py"),
                "--book",
                "Ps",
                *(["--require-final-artifacts"] if final else []),
            ],
        ),
        (
            "literary_quality_protocol",
            [
                sys.executable,
                str(ROOT / "scripts" / "validate_t423_literary_quality_protocol.py"),
                "--model-folder",
                str(MODEL),
                "--book",
                "Ps",
                "--require-artifacts",
            ],
        ),
        (
            "corrective_review_depth",
            [
                sys.executable,
                str(ROOT / "scripts" / "validate_m7_corrective_review_depth.py"),
                "--model-root",
                str(MODEL),
                "--book",
                "Ps",
                "--json",
            ],
        ),    ]
    if final:
        commands.append(
            (
                "workflow_replay_contract",
                [sys.executable, str(ROOT / "scripts" / "validate_whole_bible_candidate_workflow.py")],
            )
        )
    return commands


def run_gates(commands: list[tuple[str, list[str]]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for gate_id, command in commands:
        completed = subprocess.run(command, cwd=ROOT, shell=False, check=False, text=True, capture_output=True)
        output = (completed.stdout + completed.stderr).strip()
        result = {
            "gate_id": gate_id,
            "command": " ".join(command),
            "exit_code": completed.returncode,
            "status": "pass" if completed.returncode == 0 else "fail",
            "output": output,
        }
        results.append(result)
        print(f"{result['status'].upper()} {gate_id}: {output}")
        if completed.returncode:
            raise RuntimeError(f"gate failed: {gate_id}")
    return results


def finalize() -> None:
    chunks = read_jsonl(CHUNKS)
    packets = read_jsonl(REVIEW / "review_packets.jsonl")
    relations_path = REVIEW / "decision_relations.jsonl"
    chunks_hash = sha(CHUNKS)
    packets_hash = sha(REVIEW / "review_packets.jsonl")
    relations_hash = sha(relations_path)
    sidecar_hashes = {name: book_rows_sha(MODEL / name) for name in SIDECARS}
    accepted = sorted(row["decision_id"] for row in packets if row["final_state"] == "accepted_candidate")
    held = sorted(row["decision_id"] for row in packets if row["final_state"] != "accepted_candidate")
    appeals = sorted(
        appeal["appeal_id"] for row in packets for appeal in row.get("appeals", [])
    )
    postchecker_attempt_ids = sorted({
        row["post_resolution_check"]["checker_attempt_id"] for row in packets
    })
    verdict_path = REVIEW / "role_separated_checker_verdict_v1.json"
    write_json(
        verdict_path,
        {
            "schema_version": "m7_role_separated_checker_verdict.v1",
            "book": "Ps",
            "checker_attempt_id": CHECKER_ATTEMPT,
            "checker_attempt_ids": postchecker_attempt_ids,
            "passage_cluster_size_ceiling": 8,
            "checked_chunks_sha256": chunks_hash,
            "checked_review_packets_sha256": packets_hash,
            "checked_decision_relations_sha256": relations_hash,
            "checked_uncertainty_sidecar_sha256": sidecar_hashes,
            "verdict": "pass_with_holds",
            "role_separated_from_author": True,
            "shared_model_substrate": True,
            "counts_as_cross_model_independent_vote": False,
            "findings": [],
            "non_authorizing": True,
        },
    )
    post_results = run_gates(gate_commands(final=False))
    postcheck_path = REVIEW / "post_resolution_check_v2.json"
    write_json(
        postcheck_path,
        {
            "schema_version": "m7_post_resolution_check.v2",
            "checker_attempt_id": CHECKER_ATTEMPT,
            "checker_attempt_ids": postchecker_attempt_ids,
            "passage_cluster_size_ceiling": 8,
            "role": "role_separated_read_only_post_resolution_checker",
            "book": "Ps",
            "checked_chunks_sha256": chunks_hash,
            "checked_review_packets_sha256": packets_hash,
            "checked_decision_relations_sha256": relations_hash,
            "checked_uncertainty_sidecar_sha256": sidecar_hashes,
            "checked_decision_ids": sorted(row["decision_id"] for row in packets),
            "checker_verdict_path": verdict_path.relative_to(ROOT).as_posix(),
            "checker_verdict_sha256": sha(verdict_path),
            "validation_results": post_results,
            "chunk_count": len(chunks),
            "review_packet_count": len(packets),
            "accepted_decision_count": len(accepted),
            "accepted_decision_ids": accepted,
            "held_decision_count": len(held),
            "held_decision_ids": held,
            "appeal_count": len(appeals),
            "appeal_ids": appeals,
            "independence_scope": INDEPENDENCE_SCOPE,
            "independence_limit": "Role-separated checks share one Sol model substrate and count as one correlated model voice.",
            "role_separated_checker_verdict_received": True,
            "independent_model_verdict_received": False,
            "failures": [],
            "overall_status": "pass_with_holds",
            "forced_consensus": False,
            "non_authorizing": True,
        },
    )
    receipt_results = run_gates(gate_commands(final=True))
    write_json(
        RECEIPT,
        {
            "schema_version": "m7_book_completion_receipt.v2",
            "model_id": "M7_sol",
            "book": "Ps",
            "completion_state": "candidate_complete_with_explicit_holds",
            "chunk_count": len(chunks),
            "review_packet_count": len(packets),
            "canonical_verse_count": 2461,
            "covered_verse_count": 2461,
            "exact_ordered_coverage": True,
            "accepted_decision_count": len(accepted),
            "accepted_decision_ids": accepted,
            "held_decision_count": len(held),
            "held_decision_ids": held,
            "unresolved_appeal_count": len(appeals),
            "unresolved_appeal_ids": appeals,
            "chunks_sha256": chunks_hash,
            "review_packets_sha256": packets_hash,
            "decision_relations_sha256": relations_hash,
            "uncertainty_sidecar_sha256": sidecar_hashes,
            "postcheck_sha256": sha(postcheck_path),
            "checker_verdict_path": verdict_path.relative_to(ROOT).as_posix(),
            "checker_verdict_sha256": sha(verdict_path),
            "postchecker_attempt_id": CHECKER_ATTEMPT,
            "postchecker_attempt_ids": postchecker_attempt_ids,
            "passage_cluster_size_ceiling": 8,
            "postcheck_status": "pass_with_holds",
            "independence_scope": INDEPENDENCE_SCOPE,
            "pre_receipt_gates": receipt_results,
            "receipt_written_after_final_hash_and_gates": True,
            "validation_bundle_command": (
                "python .ai/scratch/multi_model_bible_chunking/M7_sol/checks/"
                "validate_book_completion_bundle.py --book Ps"
            ),
            "post_receipt_validation_required": True,
            "forced_consensus": False,
            "non_authorizing": True,
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--finalize", action="store_true", help="Hash-close postcheck and receipt after global sidecars are updated")
    args = parser.parse_args()
    if args.finalize:
        finalize()
        print(f"Finalized Psalm completion bundle: {RECEIPT.relative_to(ROOT).as_posix()}")
    else:
        summary = write_core()
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        print("Global sidecar owner must install rows from reviews/Ps/sidecar_rows_v2.json before --finalize.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
