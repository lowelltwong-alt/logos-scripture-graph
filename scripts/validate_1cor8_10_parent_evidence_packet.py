#!/usr/bin/env python3
"""Validate the T370 1Cor.8-10 parent-only evidence packet."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
PACKET = ROOT / "eval" / "chunking_gold" / "review_packets" / "1cor8_10_parent_only_evidence_packet.yaml"
REVIEW_PACKET = ROOT / "eval" / "chunking_gold" / "review_packets" / "1cor8_10_food_offered_to_idols_review.md"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
ROADMAP = ROOT / "ROADMAP_STATE.yaml"
CANON = ROOT / "data" / "canonical" / "translations" / "eng-web"

REQUIRED_TOP_LEVEL = {
    "object_type",
    "trust_zone",
    "lifecycle_status",
    "provenance_note",
    "reason_for_inclusion",
    "schema_version",
    "packet_id",
    "owner",
    "authority",
    "scope",
    "dependencies",
    "source_inputs",
    "parent_span_evidence",
    "source_metadata_evidence",
    "governed_parent_evidence_claim",
    "conflict_scan",
    "promotion_blockers_for_t371",
    "non_authorizations",
    "validators",
}

REQUIRED_FALSE_AUTHORITY = {
    "authorizes_parent_span_as_reviewed_gold",
    "authorizes_child_spans",
    "authorizes_chunk_boundaries",
    "authorizes_route_behavior",
    "authorizes_evaluator_change",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_embedding_or_vector_work",
    "authorizes_textual_critical_policy",
    "authorizes_doctrinal_system",
    "authorizes_output_change",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "reviewed_gold_promotion",
    "parent_span_as_chunk_boundary",
    "child_span_selection",
    "argument_outline_as_child_boundary",
    "paragraph_marker_as_chunk_boundary",
    "source_metadata_as_authority",
    "cross_reference_as_graph_edge",
    "strong_number_as_lexical_truth",
    "capitalization_as_divine_identity",
    "textual_critical_policy_selection",
    "sacramental_system_selection",
    "ecclesial_system_selection",
    "weak_strong_system_selection",
    "christian_liberty_system_selection",
    "law_gospel_system_selection",
    "covenant_system_selection",
    "route_behavior_change",
    "evaluator_change",
    "graph_edge_generation",
    "retrieval_truth",
    "embedding_or_vector_work",
    "chunk_output_change",
}

REQUIRED_STRONGS = {
    "G1108",
    "G4893",
    "G1494",
    "G1497",
    "G1849",
    "G4624",
    "G5132",
    "G4221",
    "G1140",
    "G2842",
    "G2316",
    "G2962",
    "G5547",
}

REQUIRED_CAPITALIZATION_TERMS = {"God", "gods", "Lord", "lords", "Christ", "Jesus", "Father"}


class ParentEvidenceError(ValueError):
    """Raised when the T370 evidence packet is stale or authorizing."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ParentEvidenceError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise ParentEvidenceError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise ParentEvidenceError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    try:
        with path.open(encoding="utf-8") as handle:
            return [json.loads(line) for line in handle if line.strip()]
    except (OSError, json.JSONDecodeError) as exc:
        raise ParentEvidenceError(f"{_rel(path)}: JSONL unreadable: {exc}") from exc


def _ref_key(ref: str) -> tuple[str, int, int]:
    try:
        book, chapter, verse = ref.split(".")
        return book, int(chapter), int(verse)
    except ValueError as exc:
        raise ParentEvidenceError(f"invalid OSIS ref {ref!r}") from exc


def _in_parent(ref: str) -> bool:
    book, chapter, verse = _ref_key(ref)
    return book == "1Cor" and ((chapter == 8 and verse >= 1) or chapter == 9 or (chapter == 10 and verse <= 33))


def _parent_records(filename: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for item in _load_jsonl(CANON / filename):
        ref = item.get("osis_ref")
        if not ref:
            continue
        try:
            if _in_parent(str(ref)):
                records.append(item)
        except ParentEvidenceError:
            continue
    return records


def _sorted_refs(refs: set[str] | list[str]) -> list[str]:
    return sorted({str(ref) for ref in refs}, key=_ref_key)


def _require_subset(required: set[str], actual: Any, label: str) -> None:
    if not isinstance(actual, list):
        raise ParentEvidenceError(f"{label} must be a list")
    missing = sorted(required - {str(item) for item in actual})
    if missing:
        raise ParentEvidenceError(f"{label} missing {missing}")


def _validate_authority(data: dict[str, Any], path: Path) -> None:
    missing = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing:
        raise ParentEvidenceError(f"{_rel(path)}: missing top-level keys {missing}")
    if data["object_type"] != "parent_only_review_evidence_packet":
        raise ParentEvidenceError(f"{_rel(path)}: object_type must be parent_only_review_evidence_packet")
    if data["trust_zone"] != "canonical":
        raise ParentEvidenceError(f"{_rel(path)}: trust_zone must be canonical")
    if data["lifecycle_status"] != "active":
        raise ParentEvidenceError(f"{_rel(path)}: lifecycle_status must be active")

    authority = data["authority"]
    if not isinstance(authority, dict):
        raise ParentEvidenceError(f"{_rel(path)}: authority must be a mapping")
    if authority.get("records_parent_only_evidence") is not True:
        raise ParentEvidenceError(f"{_rel(path)}: authority.records_parent_only_evidence must be true")
    if authority.get("may_surface_for_owner_promotion_review") is not True:
        raise ParentEvidenceError(f"{_rel(path)}: authority.may_surface_for_owner_promotion_review must be true")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise ParentEvidenceError(f"{_rel(path)}: authority.{key} must be false")

    scope = data["scope"]
    if scope.get("selected_option") != "1COR8-10-T369-B":
        raise ParentEvidenceError(f"{_rel(path)}: scope.selected_option is stale")
    if scope.get("selected_parent") != "1Cor.8.1-1Cor.10.33":
        raise ParentEvidenceError(f"{_rel(path)}: scope.selected_parent is wrong")
    if scope.get("selected_children") != []:
        raise ParentEvidenceError(f"{_rel(path)}: scope.selected_children must be []")
    if scope.get("evidence_scope") != "parent_only":
        raise ParentEvidenceError(f"{_rel(path)}: scope.evidence_scope must be parent_only")
    if scope.get("review_status") != "ready_for_owner_promotion_review":
        raise ParentEvidenceError(f"{_rel(path)}: scope.review_status is wrong")
    if scope.get("reviewed_gold_promoted") is not False:
        raise ParentEvidenceError(f"{_rel(path)}: scope.reviewed_gold_promoted must be false")

    _require_subset(REQUIRED_NON_AUTHORIZATIONS, data["non_authorizations"], "non_authorizations")


def _validate_canonical_evidence(data: dict[str, Any], path: Path) -> None:
    witness = _parent_records("translation_witnesses.jsonl")
    boundary = _parent_records("boundary_claims.jsonl")
    footnotes = _parent_records("footnotes.jsonl")
    crossrefs = _parent_records("editorial_cross_references.jsonl")
    sections = _parent_records("section_headings.jsonl")
    words = _parent_records("word_tokens.jsonl")

    parent = data["parent_span_evidence"]
    witness_refs = _sorted_refs([item["osis_ref"] for item in witness])
    if len(witness_refs) != 73 or witness_refs[0] != "1Cor.8.1" or witness_refs[-1] != "1Cor.10.33":
        raise ParentEvidenceError(f"{_rel(path)}: canonical witness parent span is stale")
    if parent.get("verse_count") != len(witness_refs):
        raise ParentEvidenceError(f"{_rel(path)}: parent_span_evidence.verse_count is stale")
    if parent.get("first_ref") != witness_refs[0] or parent.get("last_ref") != witness_refs[-1]:
        raise ParentEvidenceError(f"{_rel(path)}: parent first/last refs are stale")
    chapter_counts = Counter(f"1Cor.{_ref_key(ref)[1]}" for ref in witness_refs)
    if dict(parent.get("chapter_verse_counts", {})) != dict(chapter_counts):
        raise ParentEvidenceError(f"{_rel(path)}: chapter_verse_counts are stale")
    source_lines = [int(item["source_line"]) for item in witness]
    if parent.get("source_line_range") != [min(source_lines), max(source_lines)]:
        raise ParentEvidenceError(f"{_rel(path)}: source_line_range is stale")
    if parent.get("section_headings_in_parent") != [item.get("osis_ref") for item in sections]:
        raise ParentEvidenceError(f"{_rel(path)}: section_headings_in_parent is stale")

    observed = parent["current_chunk_behavior"]
    if observed.get("case_fully_contained_in_one_chunk") is not False:
        raise ParentEvidenceError(f"{_rel(path)}: current behavior containment must be false")
    if observed.get("case_split_across_chunks") is not True:
        raise ParentEvidenceError(f"{_rel(path)}: current behavior split flag must be true")
    if observed.get("case_mixed_with_extra_context") is not True:
        raise ParentEvidenceError(f"{_rel(path)}: current behavior mixed-context flag must be true")
    if observed.get("diagnostic_only") is not True:
        raise ParentEvidenceError(f"{_rel(path)}: current behavior must be diagnostic only")

    metadata = data["source_metadata_evidence"]
    boundary_refs = _sorted_refs([item["osis_ref"] for item in boundary if item.get("marker") == "p"])
    if metadata["paragraph_markers"].get("refs") != boundary_refs:
        raise ParentEvidenceError(f"{_rel(path)}: paragraph marker refs are stale")
    if metadata["paragraph_markers"].get("count") != len(boundary_refs):
        raise ParentEvidenceError(f"{_rel(path)}: paragraph marker count is stale")

    packet_footnotes = {item["ref"]: item for item in metadata["footnotes"]}
    source_footnotes = {item["osis_ref"]: item["text"] for item in footnotes}
    if set(packet_footnotes) != set(source_footnotes):
        raise ParentEvidenceError(f"{_rel(path)}: footnote refs are stale")
    for ref in source_footnotes:
        if not packet_footnotes[ref].get("evidence_summary"):
            raise ParentEvidenceError(f"{_rel(path)}: footnote summary for {ref} is missing")
        if "authority_limit" not in packet_footnotes[ref]:
            raise ParentEvidenceError(f"{_rel(path)}: footnote authority_limit for {ref} is missing")
    if packet_footnotes["1Cor.9.20"].get("authority_limit") != "variant_sensitive_evidence_only":
        raise ParentEvidenceError(f"{_rel(path)}: 1Cor.9.20 footnote authority_limit is stale")
    if packet_footnotes["1Cor.10.9"].get("authority_limit") != "textual_critical_policy_required_before_use":
        raise ParentEvidenceError(f"{_rel(path)}: 1Cor.10.9 footnote authority_limit is stale")

    packet_crossrefs = {item["ref"]: item["targets"] for item in metadata["editorial_cross_references"]}
    source_crossrefs = {item["osis_ref"]: item["candidate_osis_refs"] for item in crossrefs}
    if packet_crossrefs != source_crossrefs:
        raise ParentEvidenceError(f"{_rel(path)}: editorial cross-reference evidence is stale")

    by_code = {item["code"]: item for item in metadata["strong_style_clusters"]}
    missing_codes = sorted(REQUIRED_STRONGS - set(by_code))
    if missing_codes:
        raise ParentEvidenceError(f"{_rel(path)}: missing Strong-style clusters {missing_codes}")
    for code in REQUIRED_STRONGS:
        hits = [item for item in words if item.get("strong") == code]
        refs = _sorted_refs([item["osis_ref"] for item in hits])
        if by_code[code].get("count") != len(hits):
            raise ParentEvidenceError(f"{_rel(path)}: {code} count is stale")
        if by_code[code].get("refs") != refs:
            raise ParentEvidenceError(f"{_rel(path)}: {code} refs are stale")
    if metadata.get("strong_style_authority_limit") != "strong_style_numbers_are_metadata_not_lexical_or_theological_truth":
        raise ParentEvidenceError(f"{_rel(path)}: Strong-style authority limit is missing")

    cap_by_term = {item["term"]: item["refs"] for item in metadata["divine_name_title_capitalization"]}
    missing_terms = sorted(REQUIRED_CAPITALIZATION_TERMS - set(cap_by_term))
    if missing_terms:
        raise ParentEvidenceError(f"{_rel(path)}: missing capitalization terms {missing_terms}")
    for term in REQUIRED_CAPITALIZATION_TERMS:
        pattern = re.compile(r"\b" + re.escape(term) + r"\b")
        refs = [item["osis_ref"] for item in witness if pattern.search(str(item.get("text", "")))]
        if cap_by_term[term] != refs:
            raise ParentEvidenceError(f"{_rel(path)}: capitalization refs for {term} are stale")
    if metadata.get("capitalization_authority_limit") != "capitalization_is_translation_evidence_not_divine_identity_or_chunk_authority":
        raise ParentEvidenceError(f"{_rel(path)}: capitalization authority limit is missing")


def _validate_theological_controls(data: dict[str, Any], path: Path) -> None:
    claim = data["governed_parent_evidence_claim"]
    if "sufficient governed evidence" not in claim.get("claim", ""):
        raise ParentEvidenceError(f"{_rel(path)}: governed claim must be explicit")
    for phrase in (
        "This packet does not approve the parent span as reviewed gold.",
        "This packet does not approve child spans or argument-outline boundaries.",
        "This packet does not select a textual-critical policy for 1Cor.9.20 or 1Cor.10.9.",
        "This packet does not authorize route, evaluator, graph, retrieval, vector, chunk, or output behavior.",
    ):
        if phrase not in claim.get("evidence_limits", []):
            raise ParentEvidenceError(f"{_rel(path)}: missing evidence limit {phrase!r}")

    conflict = data["conflict_scan"]
    if conflict.get("result") != "no_conflict_detected_for_parent_only_evidence_prep":
        raise ParentEvidenceError(f"{_rel(path)}: conflict scan result is stale")
    _require_subset(
        {"JOHN3-T356-B", "REV-T344-E", "CD-040", "CD-041"},
        conflict.get("prior_decisions_considered"),
        "conflict_scan.prior_decisions_considered",
    )
    if "stop and surface the conflict" not in conflict.get("stop_rule", ""):
        raise ParentEvidenceError(f"{_rel(path)}: conflict stop rule is missing")

    _require_subset(
        {
            "explicit_owner_reviewed_gold_promotion_decision",
            "textual_critical_policy_before_variant_sensitive_use",
            "child_span_review_if_any_child_span_would_be_used",
            "route_isolation_plan_before_implementation",
            "same_baseline_evaluation_plan_before_output_change",
            "non_target_identity_proof_before_output_change",
        },
        data["promotion_blockers_for_t371"],
        "promotion_blockers_for_t371",
    )


def _validate_governed_links() -> None:
    review_text = _read_text(REVIEW_PACKET)
    for phrase in (
        "T370 parent-only evidence packet",
        "eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml",
        "No reviewed gold is promoted by the T370 evidence packet.",
    ):
        if phrase not in review_text:
            raise ParentEvidenceError(f"{_rel(REVIEW_PACKET)}: missing T370 link phrase {phrase!r}")

    register_text = _read_text(REGISTER)
    for phrase in (
        "CD-042",
        "1 Corinthians 8-10 parent-only evidence packet remains non-authorizing",
        "T370",
    ):
        if phrase not in register_text:
            raise ParentEvidenceError(f"{_rel(REGISTER)}: missing {phrase!r}")

    readiness = _read_yaml(READINESS)
    next_route = readiness.get("next_route", {})
    if next_route.get("task_id") != "T372":
        raise ParentEvidenceError(f"{_rel(READINESS)}: next_route.task_id must advance to T372 after T371-A")
    if next_route.get("starts_only_if") != "T371_A_parent_only_reviewed_gold_promoted":
        raise ParentEvidenceError(f"{_rel(READINESS)}: T372 starts_only_if is stale")
    if next_route.get("evidence_packet") != "eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml":
        raise ParentEvidenceError(f"{_rel(READINESS)}: next_route.evidence_packet is stale")
    if next_route.get("promotion_record") != ".ai/control/t371_parent_only_reviewed_gold_promotion.yaml":
        raise ParentEvidenceError(f"{_rel(READINESS)}: next_route.promotion_record is stale")
    if next_route.get("reviewed_gold_manifest") != "eval/chunking_gold/per_form/epistle_argument_gold_manifest.json":
        raise ParentEvidenceError(f"{_rel(READINESS)}: next_route.reviewed_gold_manifest is stale")
    if next_route.get("harness_only") is not True:
        raise ParentEvidenceError(f"{_rel(READINESS)}: next_route.harness_only must be true")
    if next_route.get("reviewed_gold_promoted") is not True:
        raise ParentEvidenceError(f"{_rel(READINESS)}: next_route.reviewed_gold_promoted must be true")
    for key in (
        "output_change_authorized",
        "implementation_authorized",
        "route_behavior_authorized",
        "evaluator_change_authorized",
        "graph_edge_generation_allowed",
        "retrieval_truth_authorized",
    ):
        if next_route.get(key) is not False:
            raise ParentEvidenceError(f"{_rel(READINESS)}: next_route.{key} must be false")

    roadmap = _read_yaml(ROADMAP)
    phase_4 = roadmap.get("phases", {}).get("phase_4", {})
    future = {item.get("id"): item for item in phase_4.get("future_sequence", []) if isinstance(item, dict)}
    t370 = future.get("T370")
    if not isinstance(t370, dict):
        raise ParentEvidenceError(f"{_rel(ROADMAP)}: missing T370")
    if t370.get("status") != "complete":
        raise ParentEvidenceError(f"{_rel(ROADMAP)}: T370 must be complete after evidence prep")
    if t370.get("evidence_packet") != "eval/chunking_gold/review_packets/1cor8_10_parent_only_evidence_packet.yaml":
        raise ParentEvidenceError(f"{_rel(ROADMAP)}: T370 evidence_packet is stale")
    if future.get("T371", {}).get("starts_only_if") != "T370_builds_governed_evidence_and_T379_selects_case_policy":
        raise ParentEvidenceError(f"{_rel(ROADMAP)}: T371 starts_only_if is stale")


def validate_1cor8_10_parent_evidence_packet(path: Path = PACKET) -> dict[str, Any]:
    data = _read_yaml(path)
    _validate_authority(data, path)
    _validate_canonical_evidence(data, path)
    _validate_theological_controls(data, path)
    _validate_governed_links()
    return data


def main() -> int:
    try:
        validate_1cor8_10_parent_evidence_packet()
    except ParentEvidenceError as exc:
        print(f"1Cor.8-10 parent evidence packet validation failed: {exc}", file=sys.stderr)
        return 1
    print("1Cor.8-10 parent evidence packet validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
