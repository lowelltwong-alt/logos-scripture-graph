"""Contract checks for the provider-neutral M7 corrective re-review workflow."""
from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent
CONTRACT = (
    ROOT
    / ".ai"
    / "scratch"
    / "multi_model_bible_chunking"
    / "M7_sol"
    / "corrective_rereview_contract.v1.yaml"
)
ADAPTER = CONTRACT.parent / "runtime" / "corrective_rereview_codex_adapter.v1.yaml"


def _read(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_corrective_contract_preserves_scope_and_authority_barriers() -> None:
    contract = _read(CONTRACT)
    assert contract["schema_version"] == "m7_corrective_rereview_contract.v1"
    assert contract["provider_neutral"] == "candidate"
    assert contract["portability_status"] == "provider_neutral_candidate_core_single_runtime_evidence"
    assert contract["runtime_evidence_count"] == 1
    assert contract["candidate_only"] is True
    assert contract["non_authorizing"] is True
    assert contract["promotion_authority"] == "none"
    assert contract["scope"]["excluded_completed_books"] == ["Gen", "Exod", "Lev"]
    assert contract["scope"]["forbidden_inputs"] == ["M1-M6", "comparison", "T417"]
    assert contract["ownership"]["one_write_owner_per_book"] is True
    assert contract["review_rules"]["append_only_appeals"] is True
    assert contract["review_rules"]["each_primary_attests_blind_to_other_primary_reviews"] is True
    assert contract["review_rules"]["shared_model_mesh_cannot_claim_cross_model_votes"] is True
    assert contract["evidence_rules"]["new_testament_source_families"] == ["SBLGNT", "UGNT", "CNTR"]
    assert contract["evidence_rules"]["english_translation_alone_cannot_satisfy_original_language_primary"] is True
    assert contract["evidence_rules"]["psalms_web_mt_crosswalk_required_before_original_language_boundary_claim"] is True
    assert contract["evidence_rules"]["unverified_crosswalk_requires_structured_source_gap_and_insufficient_evidence_verdict"] is True
    assert contract["review_rules"]["cross_model_or_human_receipt_required_for_convergence"] is True
    assert contract["completion"]["publication_forbidden"] is True


def test_corrective_contract_encodes_red_team_failure_controls() -> None:
    contract = _read(CONTRACT)
    gates = contract["anti_batch_gates"]
    assert gates["reject_arithmetic_midpoint_alternative_signature"] is True
    assert gates["reject_pervasive_parent_form_copy_to_children"] is True
    assert gates["reject_role_deterministic_verdicts"] is True
    assert gates["reject_bookwide_reviewer_attempt_id"] is True
    assert gates["reject_lossy_unicode_or_question_mark_opening_punctuation"] is True
    assert gates["reject_repeated_rationale_and_review_prose_shells"] is True
    assert gates["reject_seven_word_prose_ngrams_reused_across_ten_or_more_decisions"] is True
    assert gates["reject_clipped_source_quotations_and_doubled_quote_terminals"] is True
    assert contract["chunk_rules"]["child_local_literary_form_required"] is True
    assert contract["hold_rules"]["report_held_rows_and_deduplicated_issue_clusters"] is True
    validators = "\n".join(contract["validators"])
    assert "validate_m7_corrective_review_depth.py" in validators
    assert "validate_whole_bible_chunk_map.py" in validators


def test_codex_adapter_is_explicit_and_revision_bound() -> None:
    contract = _read(CONTRACT)
    adapter = _read(ADAPTER)
    assert adapter["schema_version"] == "m7_corrective_rereview_codex_adapter.v1"
    assert adapter["contract_revision"] == contract["contract_revision"]
    assert adapter["provider_neutral_candidate_core_preserved"] is True
    assert adapter["portability_claim"] == "single_runtime_evidence_only"
    assert adapter["mesh"]["book_writer"]["max_active"] == 1
    assert adapter["mesh"]["reference_auditor"]["read_only"] is True
    assert adapter["mesh"]["adversarial_specialist"]["read_only"] is True
    assert adapter["non_authorizations"] == [
        "read_sibling_model_maps",
        "publication",
        "force_consensus",
        "external_review_receipt_fabrication",
        "theology_or_canon_authority",
    ]
