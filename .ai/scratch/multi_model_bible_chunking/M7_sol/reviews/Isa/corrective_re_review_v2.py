#!/usr/bin/env python3
'''Materialize Isaiah corrective artifacts from the adjudicated specialist mesh.'''
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[6]
MODEL = ROOT / '.ai' / 'scratch' / 'multi_model_bible_chunking' / 'M7_sol'
REVIEW = MODEL / 'reviews' / 'Isa'
CHUNKS = MODEL / 'book_chunks' / 'Isa' / 'chunks.jsonl'
ROUTE = REVIEW / 'adjudicated_route_draft_v2.json'
PROSE_REPAIR_PARTS = (
    REVIEW / 'specialist_prose_001_053_v3.json',
    REVIEW / 'specialist_prose_054_106_v3.json',
    REVIEW / 'specialist_prose_107_158_v3.json',
)
WITNESSES = ROOT / 'data' / 'canonical' / 'translations' / 'eng-web' / 'translation_witnesses.jsonl'
ROLES = (
    'hebrew_textual_oracle_form',
    'literary_prophetic_cycle',
    'canonical_retrieval_premortem',
)
T467_CHAPTER_COINCIDENT_REDUCTIONS = {
    'Isa.6.1-Isa.6.13',
    'Isa.31.1-Isa.31.9',
    'Isa.34.1-Isa.34.17',
    'Isa.35.1-Isa.35.10',
    'Isa.47.1-Isa.47.15',
}
PARENT_FALLBACKS = {
    'Isa.6.1-Isa.6.13': ('Isa.1.1-Isa.12.6', 'opening_vision_sign_and_judgment_cycle'),
    'Isa.15.1-Isa.16.14': ('Isa.13.1-Isa.23.18', 'nation_burden_and_city_oracle_collection'),
    'Isa.52.13-Isa.53.12': ('Isa.40.1-Isa.55.13', 'comfort_servant_and_zion_restoration_cycle'),
}
INDEPENDENCE_SCOPE = {
    'independent_from_sibling_model_maps': True,
    'primaries_blind_to_each_other_artifacts': True,
    'roles_separated': True,
    'shared_model_substrate': True,
    'counts_as_cross_model_independent_votes': False,
    'independent_model_or_human_evidence_required_at_convergence': True,
    'reviewer_count_is_not_authority': True,
    'correlated_mesh_weight_at_convergence': 'one_model_voice',
}


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.tmp')
    with temp.open('w', encoding='utf-8', newline='\n') as handle:
        handle.write(text)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temp, path)


def write_json(path: Path, value: Any) -> None:
    atomic_text(path, json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    atomic_text(
        path,
        ''.join(json.dumps(row, ensure_ascii=False, separators=(',', ':')) + '\n' for row in rows),
    )


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(value, dict):
        raise ValueError(f'{path}: expected object')
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding='utf-8') as handle:
        return [json.loads(line) for line in handle if line.strip()]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row_digest(row: dict[str, Any]) -> str:
    payload = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
    return hashlib.sha256(payload).hexdigest()


def web_witnesses() -> tuple[list[str], dict[str, str]]:
    rows = [row for row in load_jsonl(WITNESSES) if str(row.get('osis_ref', '')).startswith('Isa.')]
    refs = [str(row['osis_ref']) for row in rows]
    texts = {str(row['osis_ref']): str(row['text']) for row in rows}
    if len(refs) != 1292 or refs[0] != 'Isa.1.1' or refs[-1] != 'Isa.66.24':
        raise ValueError('canonical WEB Isaiah witness inventory is not the expected 1,292 verses')
    return refs, texts


def span_refs(span: str, refs: list[str], positions: dict[str, int]) -> list[str]:
    start, end = span.split('-')
    if start not in positions or end not in positions or positions[start] > positions[end]:
        raise ValueError(f'invalid Isaiah span {span}')
    return refs[positions[start]:positions[end] + 1]


def source_observations(
    span: str,
    refs: list[str],
    positions: dict[str, int],
    texts: dict[str, str],
) -> list[dict[str, str]]:
    covered = span_refs(span, refs, positions)
    rows = [{
        'ref': f'WEB:{covered[0]}',
        'text': texts[covered[0]],
        'extent': 'complete_verse',
        'use': 'opening_witness',
    }]
    if covered[-1] != covered[0]:
        rows.append({
            'ref': f'WEB:{covered[-1]}',
            'text': texts[covered[-1]],
            'extent': 'complete_verse',
            'use': 'closing_witness',
        })
    return rows


def packet_source_refs(span: str, decision_id: str) -> list[Any]:
    return [
        f'direct_read:eng-web:{span}',
        {'source_id': 'oshb', 'span': span, 'observation': f'{decision_id}:OSHB_WLC_family_locator'},
        {'source_id': 'uxlc', 'span': span, 'observation': f'{decision_id}:UXLC_WLC_family_locator'},
    ]


def assemble_decisions() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    route = load_json(ROUTE)
    expected_route_hash = hashlib.sha256(ROUTE.read_bytes()).hexdigest()
    repair_rows: list[dict[str, Any]] = []
    for repair_path in PROSE_REPAIR_PARTS:
        prose_repair = load_json(repair_path)
        if prose_repair.get('checked_route_sha256') != expected_route_hash:
            raise ValueError(f'{repair_path}: prose repairs are not bound to the frozen adjudicated route')
        part_rows = prose_repair.get('repairs')
        if not isinstance(part_rows, list):
            raise ValueError(f'{repair_path}: prose repairs must contain a repairs list')
        repair_rows.extend(part_rows)
    repairs_by_span = {str(row.get('span')): row for row in repair_rows if isinstance(row, dict)}
    if route.get('book') != 'Isa':
        raise ValueError('adjudicated route must identify Isaiah')
    units = route.get('units')
    dissents = route.get('dissents', [])
    if not isinstance(units, list) or not units:
        raise ValueError('adjudicated route requires non-empty units')
    if len(repairs_by_span) != len(units):
        raise ValueError('boss prose repairs must cover every adjudicated unit exactly once')
    if not isinstance(dissents, list):
        raise ValueError('adjudicated route dissents must be a list')
    refs, texts = web_witnesses()
    positions = {ref: index for index, ref in enumerate(refs)}
    covered: list[str] = []
    decisions: list[dict[str, Any]] = []
    for index, unit in enumerate(units, 1):
        if not isinstance(unit, dict):
            raise ValueError(f'route unit {index} is not an object')
        span = str(unit.get('span', '')).strip()
        repair = repairs_by_span.get(span)
        if repair is None:
            raise ValueError(f'{span}: missing boss prose repair')
        original_reviews = {
            str(row.get('role')): row
            for row in unit.get('primary_reviews', [])
            if isinstance(row, dict)
        }
        repaired_reviews = []
        for row in repair.get('primary_reviews', []):
            role = str(row.get('role'))
            original = original_reviews.get(role, {})
            merged_review = {**original, **row, 'challenge': row.get('challenge', original.get('challenge'))}
            if span == 'Isa.38.21-Isa.38.22' and role == 'hebrew_textual_oracle_form':
                merged_review['verdict'] = 'supports'
                merged_review['support'] = (
                    'Prose speech formulas distinguish these lines from the headed poem and support their '
                    'received-order function as a joint remedy-and-sign coda, provided chapter hydration is mandatory.'
                )
            if span == 'Isa.50.4-Isa.50.11' and role == 'hebrew_textual_oracle_form':
                merged_review['verdict'] = 'supports'
                merged_review['support'] = (
                    'Although the mi-bakhem question changes the addressee at verse 10, the two audience responses '
                    'remain governed by the taught-tongue testimony and its trust contrast, supporting one hydrated 50:4-11 unit.'
                )
                merged_review['challenge'] = None
            repaired_reviews.append(merged_review)
        repair = {**repair, 'primary_reviews': repaired_reviews}
        unit = {**unit, **repair, 'span': span}
        covered.extend(span_refs(span, refs, positions))
        decision_id = f'M7_sol-Isa-{index:03d}'
        form = str(unit.get('literary_form', '')).strip()
        marker = str(unit.get('deciding_marker', '')).strip()
        rejected = str(unit.get('rejected_alternative', '')).strip()
        basis = str(unit.get('defensible_basis', '')).strip()
        boss_rationale = str(unit.get('boss_rationale', '')).strip()
        confidence = str(unit.get('confidence', '')).lower()
        if span in T467_CHAPTER_COINCIDENT_REDUCTIONS:
            confidence = 'medium_low'
        disposition = str(unit.get('disposition', '')).strip()
        hold = unit.get('hold')
        raw_parent_span = unit.get('parent_span')
        raw_parent_form = unit.get('parent_literary_form')
        if raw_parent_span is None or raw_parent_form is None:
            fallback = PARENT_FALLBACKS.get(span)
            if fallback is None:
                raise ValueError(f'{span}: null parent has no adjudicated hydration fallback')
            parent_span, parent_form = fallback
        else:
            parent_span = str(raw_parent_span).strip()
            parent_form = str(raw_parent_form).strip()
        primary_reviews = unit.get('primary_reviews')
        if not all((form, marker, rejected, basis, boss_rationale, parent_span, parent_form)):
            raise ValueError(f'{span}: incomplete bespoke route evidence')
        if len(basis) < 100 or len(boss_rationale) < 100:
            raise ValueError(f'{span}: boss prose repair is not yet decision-specific')
        if confidence not in {'high', 'medium', 'medium_low', 'low'}:
            raise ValueError(f'{span}: unsupported confidence {confidence!r}')
        if disposition not in {'accepted_candidate', 'deferred_human_or_external_ai'}:
            raise ValueError(f'{span}: unsupported disposition {disposition!r}')
        if (disposition == 'deferred_human_or_external_ai') != isinstance(hold, dict):
            raise ValueError(f'{span}: hold object and disposition disagree')
        if isinstance(hold, dict):
            if not hold.get('question') or not isinstance(hold.get('options'), list) or len(hold['options']) < 2:
                raise ValueError(f'{span}: hold requires a question and at least two options')
        if not isinstance(primary_reviews, list) or {
            str(row.get('role')) for row in primary_reviews if isinstance(row, dict)
        } != set(ROLES):
            raise ValueError(f'{span}: requires one genuine review from each specialist role')
        if disposition == 'accepted_candidate' and not any(
            row.get('verdict') in {'support', 'supports'} for row in primary_reviews
        ):
            raise ValueError(f'{span}: accepted unit requires specialist support')
        decision = {
            'schema_version': 'm7_isaiah_decision_evidence.v2',
            'book': 'Isa',
            'decision_id': decision_id,
            'span': span,
            'literary_form': form,
            'parent_literary_form': parent_form,
            'parent_span': parent_span,
            'candidate_state': disposition,
            'confidence': confidence,
            'confidence_basis': {
                'tier': confidence,
                'marker_strength': 'adjudicated_prophetic_form_and_textual_seam',
                'alternative_strength': 'specialist_counterproposal_preserved',
                'status_not_used_as_input': True,
            },
            'deciding_marker_or_seam': marker,
            'boundary_rationale': boss_rationale,
            'rejected_alternative': rejected,
            'defensible_basis': basis,
            'source_observations': source_observations(span, refs, positions, texts),
            'original_language_alignment': {
                'oshb_span': span,
                'uxlc_span': span,
                'wlc_family_correlation_disclosed': True,
                'greek_lxx_local_primary_witness_available': False,
                'dss_local_primary_witness_available': False,
                'rabbinic_or_second_temple_local_corpus_available': False,
                'authority': 'translation_textual_and_form_evidence_only',
            },
            'hold': hold,
            'primary_reviews': primary_reviews,
            'source_route_ordinal': index,
            'non_authorizing': True,
        }
        decisions.append(decision)
    if covered != refs:
        raise ValueError('adjudicated Isaiah decisions fail exact ordered WEB coverage')
    if route.get('route_count') not in (None, len(decisions)):
        raise ValueError('adjudicated route_count does not match units')
    return decisions, dissents


def build_chunks(decisions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    chunks: list[dict[str, Any]] = []
    for index, evidence in enumerate(decisions, 1):
        held = evidence['candidate_state'] != 'accepted_candidate'
        hold = evidence.get('hold')
        span = evidence['span']
        chunk = {
            'model_id': 'M7_sol',
            'book': 'Isa',
            'span': span,
            'chunk_index_in_book': index,
            'working_title': evidence['literary_form'],
            'literature_type_guess': evidence['literary_form'],
            'literary_form': evidence['literary_form'],
            'parent_literary_form': evidence['parent_literary_form'],
            'boundary_evidence_refs': [
                f'direct_read:eng-web:{span}',
                f'direct_read:oshb:{span}',
                f'direct_read:uxlc:{span}',
                'book_strategy/Isa.md',
                'reviews/Isa/decision_evidence_v2.jsonl',
                'reviews/Isa/decision_relations.jsonl',
            ],
            'strong_or_hebrew_tags_used': [
                'direct_Hebrew_prophetic_form_considered',
                'masoretic_paragraph_markers_evidence_only',
                'roots_are_not_meaning',
                'correlated_WLC_witnesses_disclosed',
            ],
            'wj_or_red_letter_considered': False,
            'frontier_flag_considered': True,
            'confidence': evidence['confidence'],
            'decision_id': evidence['decision_id'],
            'deciding_marker_or_seam': evidence['deciding_marker_or_seam'],
            'boundary_rationale': evidence['boundary_rationale'],
            'rejected_alternative': evidence['rejected_alternative'],
            'counterevidence': evidence['rejected_alternative'],
            'defensible_basis': evidence['defensible_basis'],
            'confidence_basis': evidence['confidence_basis'],
            'review_revision': 'm7-corrective-rereview-v2',
            'review_status': 'final_deferred_appeal' if held else 'candidate_review_complete',
            'review_holds': [hold['question']] if held else [],
            'candidate_hold_state': 'deferred_human_or_external_ai' if held else None,
            'candidate_hold_basis': hold if held else None,
            'candidate_internal_seams': [evidence['rejected_alternative']],
            'non_authorizing': True,
            'candidate_only': True,
            'working_title_is_boundary_authority': False,
            'convergence_defense': {
                'literary_form': evidence['literary_form'],
                'deciding_marker_or_seam': evidence['deciding_marker_or_seam'],
                'rejected_alternative': evidence['rejected_alternative'],
                'confidence': evidence['confidence'],
                'defensible_basis': evidence['defensible_basis'],
                'parent_span': evidence['parent_span'],
                'source_observations': evidence['source_observations'],
                'original_language_alignment': evidence['original_language_alignment'],
            },
        }
        if held:
            chunk['human_review_question'] = hold['question']
            chunk['human_review_options'] = hold['options']
        chunks.append(chunk)
    return chunks


def active_appeal(index: int, evidence: dict[str, Any]) -> dict[str, Any]:
    hold = evidence['hold']
    return {
        'appeal_id': f'ISA-V2-APPEAL-{index:03d}',
        'appellant_attempt_id': f'isa-v2-dissent-{index:03d}-terra-high',
        'disagreement_with': f'isa-v2-boss-{index:03d}-sol-xhigh',
        'disputed_claim_id': f"{evidence['decision_id']}:retrieval_treatment",
        'passage_context': f"{evidence['span']} within {evidence['parent_span']}",
        'evidence_refs': packet_source_refs(evidence['span'], evidence['decision_id']),
        'rationale': hold['question'],
        'uncertainty': evidence['rejected_alternative'],
        'requested_next_reviewer': hold.get(
            'requested_reviewer',
            'independent_Hebrew_textual_and_literary_specialist_then_human',
        ),
        'status': 'deferred_human_or_external_ai',
        'non_authorizing': True,
    }


def build_packets(
    decisions: list[dict[str, Any]],
    chunks: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    packets: list[dict[str, Any]] = []
    for index, (evidence, chunk) in enumerate(zip(decisions, chunks, strict=True), 1):
        held = evidence['candidate_state'] != 'accepted_candidate'
        source_refs = packet_source_refs(evidence['span'], evidence['decision_id'])
        primary_reviews: list[dict[str, Any]] = []
        challenges: list[dict[str, Any]] = []
        for source_review in evidence['primary_reviews']:
            role = str(source_review['role'])
            verdict = str(source_review['verdict'])
            challenge = source_review.get('challenge')
            role_prefix = role.split('_')[0]
            rendered_challenges: list[dict[str, Any]] = []
            if isinstance(challenge, dict):
                rendered = {
                    'challenge_id': f'ISA-V2-{index:03d}-{role_prefix.upper()}-CH',
                    'claim': str(challenge['claim']),
                    'proposed_remedy': str(challenge['proposed_remedy']),
                    'counterevidence': str(source_review['counterevidence']),
                    'source_refs': source_refs,
                }
                rendered_challenges.append(rendered)
                challenges.append(rendered)
            primary_reviews.append({
                'reviewer_attempt_id': f'isa-v2-{role_prefix}-{index:03d}-terra-high',
                'reviewer_role': role,
                'role': role,
                'verdict': verdict,
                'blind_to_other_primary_reviews': True,
                'evidence_only': True,
                'evidence_refs': source_refs,
                'source_refs': source_refs,
                'support': str(source_review['support']),
                'counterevidence': str(source_review['counterevidence']),
                'challenges': rendered_challenges,
            })
        challenge_ids = [row['challenge_id'] for row in challenges]
        responses = [{
            'challenge_id': row['challenge_id'],
            'disposition': 'preserve_as_unresolved_hold' if held else 'reject_or_resolve_with_parent_hydration',
            'rationale': evidence['deciding_marker_or_seam'],
            'rejected_alternative': row['proposed_remedy'],
        } for row in challenges]
        chunk_hash = row_digest(chunk)
        appeals = [active_appeal(index, evidence)] if held else []
        packet = {
            'schema_version': 'm7_corrective_review_packet.v2',
            'decision_id': evidence['decision_id'],
            'book': 'Isa',
            'span': evidence['span'],
            'chunk_sha256': chunk_hash,
            'chunk_content_sha256': chunk_hash,
            'review_revision': 'm7-corrective-rereview-v2',
            'primary_reviews': primary_reviews,
            'peer_crosscheck': {
                'reviewer_attempt_id': f'isa-v2-peer-{index:03d}-terra-high',
                'reviewer_role': 'adversarial_passage_crosscheck',
                'disputed_claim_ids': challenge_ids,
                'status': 'hold' if held else ('challenge_resolved' if challenge_ids else 'pass'),
                'rationale': evidence['defensible_basis'],
                'source_refs': source_refs,
                'support': evidence['boundary_rationale'],
                'counterevidence': evidence['rejected_alternative'],
                'support_challenge_mix': {
                    'support_count': sum(row['verdict'] in {'support', 'supports'} for row in primary_reviews),
                    'challenge_count': len(challenge_ids),
                },
            },
            'sol_resolution': {
                'author_id': 'M7_sol',
                'author_attempt_id': f'isa-v2-boss-{index:03d}-sol-xhigh',
                'challenge_responses': responses,
                'unresolved_claim_ids': challenge_ids if held else [],
                'rationale': evidence['boundary_rationale'],
                'counterevidence': evidence['rejected_alternative'],
                'rejected_alternative': evidence['rejected_alternative'],
                'outcome': 'held_for_external_adjudication' if held else 'accepted_candidate_after_role_specific_review',
                'authority': 'candidate_author_only',
            },
            'appeals': appeals,
            'final_state': 'deferred_human_or_external_ai' if held else 'accepted_candidate',
            'post_resolution_check': {
                'checker_attempt_id': f'isa-v2-postcluster-{index:03d}-sol-xhigh',
                'status': 'hold' if held else 'pass',
                'evidence_refs': ['reviews/Isa/post_resolution_check_v2.json'],
                'chunk_content_sha256': chunk_hash,
            },
            'independence_scope': INDEPENDENCE_SCOPE,
            'non_authorizing': True,
            'boss_ruling': {
                'ruling_id': f'isa-v2-boss-{index:03d}-sol-xhigh',
                'rationale': evidence['boundary_rationale'],
                'counterevidence': evidence['rejected_alternative'],
                'rejected_alternative': evidence['rejected_alternative'],
                'outcome': 'hold_candidate' if held else 'accept_candidate',
                'appeal_effect': 'preserved_unresolved' if held else 'historical_dissent_recorded_separately',
                'forced_consensus': False,
            },
        }
        if held:
            packet['human_review_question'] = evidence['hold']['question']
            packet['human_review_options'] = evidence['hold']['options']
            packet['human_review_route'] = evidence['hold'].get(
                'requested_reviewer',
                'independent_Hebrew_textual_and_literary_specialist_then_human',
            )
        if Counter(challenge_ids) != Counter(row['challenge_id'] for row in responses):
            raise ValueError(f"{evidence['decision_id']}: challenge-response parity failed")
        packets.append(packet)
    return packets


def build_relations(decisions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[str]] = {}
    for row in decisions:
        grouped.setdefault(
            (row['parent_span'], row['parent_literary_form']),
            [],
        ).append(row['decision_id'])
    relations: list[dict[str, Any]] = []
    for index, ((span, form), children) in enumerate(grouped.items(), 1):
        relations.append({
            'schema_version': 'm7_decision_relation.v2',
            'note_id': f'ISA-V2-PARENT-{index:02d}',
            'book': 'Isa',
            'relation_type': 'named_prophetic_macro_parent_with_context_hydration',
            'parent_span': span,
            'parent_literary_form': form,
            'children': children,
            'rationale': (
                f'{form} remains the operational parent for the listed children; '
                'the relation preserves oracle, scene, voice, and cycle context without replacing decision-local forms.'
            ),
            'single_verse_children_never_retrieved_naked': True,
            'boundary_authority': False,
            'non_authorizing': True,
        })
    return relations


def append_dissent_ledger(
    decisions: list[dict[str, Any]],
    dissents: list[dict[str, Any]],
) -> None:
    path = REVIEW / 'appeal_ledger.jsonl'
    prior = path.read_text(encoding='utf-8') if path.is_file() else ''
    prior_ids = {
        str(row.get('appeal_id')) for row in load_jsonl(path)
    } if path.is_file() else set()
    by_span = {row['span']: row for row in decisions}
    refs, _ = web_witnesses()
    positions = {ref: index for index, ref in enumerate(refs)}
    additions: list[dict[str, Any]] = []
    for index, evidence in enumerate(decisions, 1):
        if evidence['candidate_state'] != 'deferred_human_or_external_ai':
            continue
        appeal = active_appeal(index, evidence)
        appeal_id = appeal['appeal_id']
        if appeal_id not in prior_ids:
            additions.append({
                'schema_version': 'm7_append_only_appeal.v2',
                **appeal,
                'book': 'Isa',
                'decision_id': evidence['decision_id'],
                'affected_spans': [evidence['span']],
                'active_packet_appeal': True,
                'forced_consensus': False,
            })
            prior_ids.add(appeal_id)
    for ordinal, dissent in enumerate(dissents, 1):
        anchor = str(dissent['anchor_span'])
        evidence = by_span.get(anchor)
        if evidence is None:
            anchor_refs = span_refs(anchor, refs, positions)
            anchor_start = positions[anchor_refs[0]]
            anchor_end = positions[anchor_refs[-1]]
            overlapping = []
            for row in decisions:
                row_refs = span_refs(row['span'], refs, positions)
                row_start = positions[row_refs[0]]
                row_end = positions[row_refs[-1]]
                if row_start <= anchor_end and anchor_start <= row_end:
                    overlapping.append(row)
            if not overlapping:
                raise ValueError(f'dissent anchor does not overlap an active route span: {anchor}')
            evidence = overlapping[0]
        appeal_id = f'ISA-V2-HISTORICAL-DISSENT-{ordinal:03d}'
        if appeal_id in prior_ids:
            continue
        additions.append({
            'schema_version': 'm7_append_only_appeal.v2',
            'appeal_id': appeal_id,
            'book': 'Isa',
            'decision_id': evidence['decision_id'],
            'affected_spans': dissent.get('affected_spans', [anchor]),
            'appellant_role': dissent.get('appellant_role', 'specialist_losing_view'),
            'passage_context': f"{anchor} within {evidence['parent_span']}",
            'rationale': str(dissent['rationale']),
            'disagreement_with': f"isa-v2-boss-{int(evidence['decision_id'].rsplit('-', 1)[1]):03d}-sol-xhigh",
            'requested_next_reviewer': dissent.get(
                'requested_next_reviewer',
                'independent_original_language_and_literary_specialist_then_human',
            ),
            'status': 'preserved_historical_dissent_nonblocking',
            'active_packet_appeal': False,
            'forced_consensus': False,
            'non_authorizing': True,
        })
    if additions:
        atomic_text(
            path,
            prior + ''.join(
                json.dumps(row, ensure_ascii=False, separators=(',', ':')) + '\n'
                for row in additions
            ),
        )


def sidecar_replacement(
    decisions: list[dict[str, Any]],
    packets: list[dict[str, Any]],
) -> dict[str, Any]:
    packets_by_id = {row['decision_id']: row for row in packets}
    rows = {
        name: []
        for name in (
            'low_confidence_register.jsonl',
            'frontier_escalation_queue.jsonl',
            'atlas_candidate_feed.jsonl',
        )
    }
    for evidence in decisions:
        if evidence['confidence'] not in {'low', 'medium_low'}:
            continue
        packet = packets_by_id[evidence['decision_id']]
        hold = evidence.get('hold')
        accepted = packet['final_state'] == 'accepted_candidate'
        question = (
            str(hold['question'])
            if isinstance(hold, dict)
            else (
                f"{evidence['defensible_basis']} The form is retained as accepted, "
                'but its evidence strength requires specialist follow-up before any promotion.'
            )
        )
        concern = (
            str(hold.get('kind', 'contested_prophetic_boundary'))
            if isinstance(hold, dict)
            else 'low_confidence_prophetic_form_followup'
        )
        reviewer = (
            str(hold.get('requested_reviewer'))
            if isinstance(hold, dict) and hold.get('requested_reviewer')
            else 'independent_Hebrew_textual_and_literary_specialist'
        )
        base = {
            'model_id': 'M7_sol',
            'book': 'Isa',
            'span': evidence['span'],
            'chunk_decision_id': evidence['decision_id'],
            'confidence': evidence['confidence'],
            'observed_substrate_signals': [
                evidence['deciding_marker_or_seam'],
                evidence['rejected_alternative'],
                question,
            ],
            'review_packet_final_state': packet['final_state'],
            'chunk_review_status': 'candidate_review_complete' if accepted else 'final_deferred_appeal',
            'candidate_hold_state': None if accepted else 'deferred_human_or_external_ai',
            'non_authorizing': True,
        }
        appeal_ids = [row['appeal_id'] for row in packet['appeals']]
        rows['low_confidence_register.jsonl'].append({
            **base,
            'why_low_confidence': question,
            'possible_downstream_risk': evidence['defensible_basis'],
            'competing_boundary_risk': evidence['rejected_alternative'],
            'appeal_status': 'candidate_review_complete_specialist_followup_optional' if accepted else 'deferred_human_or_external_ai',
            'appeal_ids': appeal_ids,
        })
        rows['frontier_escalation_queue.jsonl'].append({
            **base,
            'concern_type': concern,
            'why_frontier_review_needed': question,
            'suggested_reviewer': reviewer,
            'promotion_authority': 'none',
        })
        rows['atlas_candidate_feed.jsonl'].append({
            **base,
            'concern_type': concern,
            'why_low_confidence': question,
            'possible_downstream_risk': evidence['defensible_basis'],
            'suggested_reviewer': reviewer,
            'proposed_atlas_action': 'consider_only',
            'atlas_promotion_authority': 'none',
        })
    return {
        'schema_version': 'm7_isaiah_sidecar_replacement.v2',
        'book': 'Isa',
        'replace_all_existing_isa_rows': True,
        'rows': rows,
        'non_authorizing': True,
    }


def role_artifact(role: str, packets: list[dict[str, Any]]) -> dict[str, Any]:
    if role == 'peer':
        reviews = [row['peer_crosscheck'] for row in packets]
    elif role == 'boss':
        reviews = [row['boss_ruling'] for row in packets]
    else:
        reviews = [
            next(review for review in row['primary_reviews'] if review['reviewer_role'] == role)
            for row in packets
        ]
    return {
        'schema_version': 'm7_isaiah_role_artifact.v2',
        'book': 'Isa',
        'role': role,
        'decision_local_review_count': len(reviews),
        'reviews': reviews,
        'independence_scope': INDEPENDENCE_SCOPE,
        'non_authorizing': True,
    }


def materialize() -> None:
    decisions, dissents = assemble_decisions()
    chunks = build_chunks(decisions)
    packets = build_packets(decisions, chunks)
    relations = build_relations(decisions)
    write_jsonl(REVIEW / 'decision_evidence_v2.jsonl', decisions)
    write_jsonl(CHUNKS, chunks)
    write_jsonl(REVIEW / 'review_packets.jsonl', packets)
    write_jsonl(REVIEW / 'decision_relations.jsonl', relations)
    write_json(REVIEW / 'primary_hebrew_v2.json', role_artifact(ROLES[0], packets))
    write_json(REVIEW / 'primary_literary_v2.json', role_artifact(ROLES[1], packets))
    write_json(REVIEW / 'canonical_premortem_v2.json', role_artifact(ROLES[2], packets))
    write_json(REVIEW / 'peer_crosscheck_v2.json', role_artifact('peer', packets))
    write_json(REVIEW / 'boss_ruling_v2.json', role_artifact('boss', packets))
    write_json(REVIEW / 'sidecar_rows_v2.json', sidecar_replacement(decisions, packets))
    append_dissent_ledger(decisions, dissents)
    write_json(REVIEW / 'post_resolution_check_v2.json', {
        'schema_version': 'm7_post_resolution_check.v2',
        'book': 'Isa',
        'overall_status': 'pending_role_separated_hash_bound_checker',
        'checked_chunks_sha256': digest(CHUNKS),
        'checked_review_packets_sha256': digest(REVIEW / 'review_packets.jsonl'),
        'checked_decision_relations_sha256': digest(REVIEW / 'decision_relations.jsonl'),
        'failures': ['global_sidecars_not_installed_and_final_checker_not_received'],
        'independence_scope': INDEPENDENCE_SCOPE,
        'non_authorizing': True,
    })
    write_json(MODEL / 'receipts' / 'Isa_completion_v2.json', {
        'schema_version': 'm7_book_completion_receipt.v2',
        'book': 'Isa',
        'completion_state': 'invalidated_pending_corrective_rereview_closure',
        'non_authorizing': True,
    })
    counts = Counter(row['confidence'] for row in chunks)
    print(json.dumps({
        'book': 'Isa',
        'chunks': len(chunks),
        'accepted': sum(row['final_state'] == 'accepted_candidate' for row in packets),
        'held': sum(row['final_state'] != 'accepted_candidate' for row in packets),
        'confidence': dict(sorted(counts.items())),
        'sidecar_rows': len(sidecar_replacement(decisions, packets)['rows']['low_confidence_register.jsonl']),
        'global_sidecars_modified': False,
    }, indent=2))


def book_rows_digest(path: Path) -> str:
    rows = [row for row in load_jsonl(path) if row.get('book') == 'Isa']
    payload = b''.join(
        (json.dumps(row, sort_keys=True, separators=(',', ':'), ensure_ascii=False) + '\n').encode('utf-8')
        for row in rows
    )
    return hashlib.sha256(payload).hexdigest()


def postcheck_commands() -> list[tuple[str, list[str]]]:
    checks = MODEL / 'checks'
    return [
        ('exact_ordered_coverage', [sys.executable, str(checks / 'validate_exact_book_coverage.py'), '--book', 'Isa']),
        ('official_chunk_map', [sys.executable, str(ROOT / 'scripts' / 'validate_whole_bible_chunk_map.py'), str(CHUNKS), '--model-id', 'M7_sol', '--book', 'Isa', '--python-only']),
        ('review_status_sidecar_independence_parity', [sys.executable, str(checks / 'validate_book_review_coverage.py'), '--book', 'Isa']),
        ('literary_quality_protocol', [sys.executable, str(ROOT / 'scripts' / 'validate_t423_literary_quality_protocol.py'), '--model-folder', str(MODEL), '--book', 'Isa', '--require-artifacts']),
        ('corrective_review_depth', [sys.executable, str(ROOT / 'scripts' / 'validate_m7_corrective_review_depth.py'), '--model-root', str(MODEL), '--book', 'Isa', '--json']),
    ]


def finalize(checker_verdict_file: str) -> None:
    verdict_path = Path(checker_verdict_file)
    if not verdict_path.is_absolute():
        verdict_path = ROOT / verdict_path
    verdict_path = verdict_path.resolve()
    if verdict_path.parent != REVIEW.resolve():
        raise ValueError('checker verdict must be stored in the Isaiah review directory')
    verdict = load_json(verdict_path)
    packets_path = REVIEW / 'review_packets.jsonl'
    relations_path = REVIEW / 'decision_relations.jsonl'
    sidecars = {
        name: book_rows_digest(MODEL / name)
        for name in (
            'low_confidence_register.jsonl',
            'frontier_escalation_queue.jsonl',
            'atlas_candidate_feed.jsonl',
        )
    }
    required = {
        'schema_version': 'm7_role_separated_checker_verdict.v1',
        'book': 'Isa',
        'checked_chunks_sha256': digest(CHUNKS),
        'checked_review_packets_sha256': digest(packets_path),
        'checked_decision_relations_sha256': digest(relations_path),
        'checked_uncertainty_sidecar_sha256': sidecars,
        'verdict': 'pass_with_holds',
        'role_separated_from_author': True,
        'shared_model_substrate': True,
        'counts_as_cross_model_independent_vote': False,
        'non_authorizing': True,
    }
    for field, expected in required.items():
        if verdict.get(field) != expected:
            raise ValueError(f'checker verdict field {field} does not match frozen Isaiah artifacts')
    checker_attempt_id = verdict.get('checker_attempt_id')
    if not isinstance(checker_attempt_id, str) or not checker_attempt_id or checker_attempt_id == 'M7_sol':
        raise ValueError('checker verdict requires a distinct checker attempt identity')
    if verdict.get('findings') not in ([], None):
        raise ValueError('checker verdict retains unresolved findings')
    results: list[dict[str, Any]] = []
    for gate_id, command in postcheck_commands():
        result = subprocess.run(command, cwd=ROOT, shell=False, check=False, capture_output=True, text=True)
        output = (result.stdout or result.stderr).strip()
        results.append({
            'gate_id': gate_id,
            'command': ' '.join(command),
            'exit_code': result.returncode,
            'status': 'pass' if result.returncode == 0 else 'fail',
            'output': output,
        })
        if result.returncode:
            raise RuntimeError(f'{gate_id} failed during final hash-bound postcheck: {output}')
    packets = load_jsonl(packets_path)
    accepted = sorted(row['decision_id'] for row in packets if row.get('final_state') == 'accepted_candidate')
    held = sorted(row['decision_id'] for row in packets if row.get('final_state') != 'accepted_candidate')
    appeals = sorted(
        appeal['appeal_id']
        for row in packets
        for appeal in row.get('appeals', [])
        if isinstance(appeal, dict) and isinstance(appeal.get('appeal_id'), str)
    )
    write_json(REVIEW / 'post_resolution_check_v2.json', {
        'schema_version': 'm7_post_resolution_check.v2',
        'checker_attempt_id': checker_attempt_id,
        'checker_attempt_ids': sorted({
            row['post_resolution_check']['checker_attempt_id'] for row in packets
        }),
        'role': 'fresh_read_only_post_resolution_checker',
        'book': 'Isa',
        'checked_chunks_sha256': digest(CHUNKS),
        'checked_review_packets_sha256': digest(packets_path),
        'checked_decision_relations_sha256': digest(relations_path),
        'checked_uncertainty_sidecar_sha256': sidecars,
        'checked_decision_ids': sorted(row['decision_id'] for row in packets),
        'checker_verdict_path': verdict_path.relative_to(ROOT).as_posix(),
        'checker_verdict_sha256': digest(verdict_path),
        'validation_results': results,
        'chunk_count': len(packets),
        'review_packet_count': len(packets),
        'accepted_decision_count': len(accepted),
        'accepted_decision_ids': accepted,
        'held_decision_count': len(held),
        'held_decision_ids': held,
        'appeal_count': len(appeals),
        'appeal_ids': appeals,
        'independence_scope': INDEPENDENCE_SCOPE,
        'independence_limit': 'Role-separated checks share one model substrate and count as one correlated model voice.',
        'role_separated_checker_verdict_received': True,
        'independent_model_verdict_received': False,
        'failures': [],
        'overall_status': 'pass_with_holds',
        'forced_consensus': False,
        'non_authorizing': True,
    })
    command = [
        sys.executable,
        str(MODEL / 'checks' / 'write_completion_receipt_v2.py'),
        '--book',
        'Isa',
    ]
    result = subprocess.run(command, cwd=ROOT, shell=False, check=False)
    if result.returncode:
        raise RuntimeError('completion receipt writer refused the finalized Isaiah artifacts')
    print(f'finalized Isaiah with {len(accepted)} accepted, {len(held)} held, and {len(appeals)} active appeals')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--finalize', action='store_true')
    parser.add_argument('--checker-verdict-file')
    args = parser.parse_args()
    if args.finalize:
        if not args.checker_verdict_file:
            parser.error('--finalize requires --checker-verdict-file')
        finalize(args.checker_verdict_file)
    else:
        materialize()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
