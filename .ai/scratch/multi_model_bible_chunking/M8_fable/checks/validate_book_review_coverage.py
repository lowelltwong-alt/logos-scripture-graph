#!/usr/bin/env python3
"""Validate exact verse coverage and per-chunk M7 review/appeal parity."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from review_contract_constants import INDEPENDENCE_SCOPE

ROOT = Path(__file__).resolve().parents[5]
MODEL_ROOT = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M8_fable"
PASSAGES = ROOT / "data" / "canonical" / "scripture" / "passages" / "passages.jsonl"
SPAN_RE = re.compile(r"^([1-4]?[A-Za-z][A-Za-z0-9]*)\.(\d+)\.(\d+)-([1-4]?[A-Za-z][A-Za-z0-9]*)\.(\d+)\.(\d+)$")
LOW_CONFIDENCE = {"low", "medium_low"}
HELD_STATES = {"held_lower_confidence", "deferred_human_or_external_ai"}


def read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"missing {path.relative_to(ROOT).as_posix()}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path.relative_to(ROOT).as_posix()}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT).as_posix()}: expected object")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise ValueError(f"missing {path.relative_to(ROOT).as_posix()}")
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path.relative_to(ROOT).as_posix()}:{line_no}: {exc}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"{path.relative_to(ROOT).as_posix()}:{line_no}: expected object")
            rows.append(row)
    return rows


def canonical_refs(book: str) -> list[str]:
    refs: list[str] = []
    for row in read_jsonl(PASSAGES):
        if row.get("book") == book:
            ref = row.get("osis_ref")
            if isinstance(ref, str):
                refs.append(ref)
    if not refs:
        raise ValueError(f"canonical passage inventory contains no rows for {book}")
    return refs


def chunk_digest(row: dict[str, Any]) -> str:
    payload = json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def span_refs(span: str, book: str, refs: list[str], positions: dict[str, int]) -> list[str]:
    match = SPAN_RE.fullmatch(span)
    if not match:
        raise ValueError(f"invalid full span {span!r}")
    start_book, start_chapter, start_verse, end_book, end_chapter, end_verse = match.groups()
    if start_book != book or end_book != book:
        raise ValueError(f"span {span!r} must remain inside {book}")
    start = f"{book}.{int(start_chapter)}.{int(start_verse)}"
    end = f"{book}.{int(end_chapter)}.{int(end_verse)}"
    if start not in positions or end not in positions:
        raise ValueError(f"span {span!r} endpoint absent from canonical passage inventory")
    a, b = positions[start], positions[end]
    if a > b:
        raise ValueError(f"span {span!r} is inverted")
    return refs[a : b + 1]


def validate(book: str, *, require_final_artifacts: bool = False) -> list[str]:
    errors: list[str] = []
    chunk_path = MODEL_ROOT / "book_chunks" / book / "chunks.jsonl"
    review_path = MODEL_ROOT / "reviews" / book / "review_packets.jsonl"
    try:
        chunks = read_jsonl(chunk_path)
        packets = read_jsonl(review_path)
        refs = canonical_refs(book)
    except ValueError as exc:
        return [str(exc)]

    positions = {ref: index for index, ref in enumerate(refs)}
    covered: list[str] = []
    chunk_by_id: dict[str, dict[str, Any]] = {}
    indices = [row.get("chunk_index_in_book") for row in chunks]
    if not chunks:
        errors.append(f"{book}: at least one chunk is required")
    if any(type(value) is not int or value < 1 for value in indices):
        errors.append(f"{book}: chunk_index_in_book values must be positive integers")
    elif indices != list(range(1, len(chunks) + 1)):
        errors.append(
            f"{book}: chunk_index_in_book must follow physical canonical order as 1..{len(chunks)}; "
            f"actual={indices[:12]}"
        )
    for row in chunks:
        decision_id = row.get("decision_id")
        if not isinstance(decision_id, str) or not decision_id:
            errors.append("chunk missing decision_id")
            continue
        if decision_id in chunk_by_id:
            errors.append(f"duplicate chunk decision_id {decision_id}")
        chunk_by_id[decision_id] = row
        try:
            covered.extend(span_refs(str(row.get("span", "")), book, refs, positions))
        except ValueError as exc:
            errors.append(f"{decision_id}: {exc}")

    if covered != refs:
        covered_set = set(covered)
        missing = [ref for ref in refs if ref not in covered_set]
        duplicates = sorted({ref for ref in covered if covered.count(ref) > 1})
        errors.append(
            f"{book}: exact verse coverage mismatch; expected={len(refs)} covered={len(covered)} "
            f"missing={missing[:8]} duplicates={duplicates[:8]}"
        )

    packet_by_id: dict[str, dict[str, Any]] = {}
    for packet in packets:
        decision_id = packet.get("decision_id")
        if not isinstance(decision_id, str) or not decision_id:
            errors.append("review packet missing decision_id")
            continue
        if decision_id in packet_by_id:
            errors.append(f"duplicate review packet {decision_id}")
        packet_by_id[decision_id] = packet

    if set(chunk_by_id) != set(packet_by_id):
        errors.append(
            "decision/review set mismatch: "
            f"missing_reviews={sorted(set(chunk_by_id) - set(packet_by_id))} "
            f"orphan_reviews={sorted(set(packet_by_id) - set(chunk_by_id))}"
        )

    expected_low_ids = {
        decision_id
        for decision_id, chunk in chunk_by_id.items()
        if chunk.get("confidence") in LOW_CONFIDENCE
    }
    for sidecar_name in (
        "low_confidence_register.jsonl",
        "frontier_escalation_queue.jsonl",
        "atlas_candidate_feed.jsonl",
    ):
        try:
            book_rows = [
                row for row in read_jsonl(MODEL_ROOT / sidecar_name)
                if row.get("book") == book
            ]
        except ValueError as exc:
            errors.append(str(exc))
            continue
        sidecar_by_id: dict[str, dict[str, Any]] = {}
        for row in book_rows:
            decision_id = row.get("chunk_decision_id")
            if not isinstance(decision_id, str) or not decision_id:
                errors.append(f"{book} {sidecar_name}: row missing chunk_decision_id")
            elif decision_id in sidecar_by_id:
                errors.append(f"{book} {sidecar_name}: duplicate {decision_id}")
            else:
                sidecar_by_id[decision_id] = row
        if set(sidecar_by_id) != expected_low_ids:
            errors.append(
                f"{book} {sidecar_name}: low-confidence set mismatch; "
                f"missing={sorted(expected_low_ids - set(sidecar_by_id))} "
                f"orphan={sorted(set(sidecar_by_id) - expected_low_ids)}"
            )
        for decision_id in expected_low_ids & set(sidecar_by_id) & set(packet_by_id):
            row = sidecar_by_id[decision_id]
            chunk = chunk_by_id[decision_id]
            packet = packet_by_id[decision_id]
            if row.get("span") != chunk.get("span") or row.get("confidence") != chunk.get("confidence"):
                errors.append(f"{book} {sidecar_name} {decision_id}: stale span or confidence")
            if row.get("review_packet_final_state") != packet.get("final_state"):
                errors.append(f"{book} {sidecar_name} {decision_id}: stale review_packet_final_state")
            if row.get("chunk_review_status") != chunk.get("review_status"):
                errors.append(f"{book} {sidecar_name} {decision_id}: stale chunk_review_status")
            if row.get("candidate_hold_state") != chunk.get("candidate_hold_state"):
                errors.append(f"{book} {sidecar_name} {decision_id}: hold-state mismatch")
            if sidecar_name == "low_confidence_register.jsonl":
                appeals = bool(packet.get("appeals"))
                held = packet.get("final_state") != "accepted_candidate"
                expected_appeal_status = (
                    "deferred_human_or_external_ai"
                    if appeals
                    else "no_appeal_specialist_or_external_review_hold"
                    if held
                    else "candidate_review_complete_specialist_followup_optional"
                )
                if row.get("appeal_status") != expected_appeal_status:
                    errors.append(
                        f"{book} {sidecar_name} {decision_id}: appeal_status conflates "
                        "appeal-backed and non-appeal holds"
                    )

    relation_path = MODEL_ROOT / "reviews" / book / "decision_relations.jsonl"
    try:
        relations = read_jsonl(relation_path)
    except ValueError as exc:
        errors.append(str(exc))
        relations = []
    if not relations:
        no_relation_path = MODEL_ROOT / "reviews" / book / "no_decision_relations_v1.json"
        try:
            no_relation = read_json(no_relation_path)
        except ValueError as exc:
            errors.append(
                f"{book}: decision relations require scoped rows or an explicit no-relation receipt; {exc}"
            )
        else:
            expected_ids = sorted(chunk_by_id)
            if (
                no_relation.get("schema_version") != "m7_no_decision_relations.v1"
                or no_relation.get("book") != book
                or no_relation.get("reviewed_decision_ids") != expected_ids
                or no_relation.get("non_authorizing") is not True
                or not isinstance(no_relation.get("reviewer_attempt_id"), str)
                or not no_relation.get("reviewer_attempt_id")
                or not isinstance(no_relation.get("rationale"), str)
                or not no_relation.get("rationale").strip()
            ):
                errors.append(f"{book}: explicit no-relation receipt is malformed or stale")
    relation_ids: set[str] = set()
    for relation in relations:
        note_id = relation.get("note_id")
        if not isinstance(note_id, str) or not note_id:
            errors.append(f"{book}: decision relation missing note_id")
        elif note_id in relation_ids:
            errors.append(f"{book}: duplicate decision relation {note_id}")
        else:
            relation_ids.add(note_id)
        if relation.get("book") != book or relation.get("non_authorizing") is not True:
            errors.append(f"{book} {note_id}: relation must match book and be non-authorizing")
        referenced_ids = list(relation.get("decision_ids", []) or []) + list(relation.get("children", []) or [])
        for link in relation.get("typed_links", []) or []:
            if not isinstance(link, dict):
                errors.append(f"{book} {note_id}: typed link must be an object")
                continue
            referenced_ids.extend([link.get("source_decision_id"), link.get("target_decision_id")])
        unknown = sorted({
            value for value in referenced_ids
            if isinstance(value, str) and value not in chunk_by_id
        })
        if unknown:
            errors.append(f"{book} {note_id}: relation references inactive decisions {unknown}")

    final_postcheck: dict[str, Any] | None = None
    if require_final_artifacts:
        postcheck_path = MODEL_ROOT / "reviews" / book / "post_resolution_check_v2.json"
        try:
            final_postcheck = read_json(postcheck_path)
        except ValueError as exc:
            errors.append(str(exc))
        else:
            packets_hash = hashlib.sha256(review_path.read_bytes()).hexdigest()
            if final_postcheck.get("book") != book:
                errors.append(f"{book}: final postcheck book mismatch")
            if final_postcheck.get("checked_review_packets_sha256") != packets_hash:
                errors.append(f"{book}: final postcheck is not bound to the current review packets")
            if sorted(final_postcheck.get("checked_decision_ids", [])) != sorted(packet_by_id):
                errors.append(f"{book}: final postcheck does not enumerate every active decision")
            if final_postcheck.get("role_separated_checker_verdict_received") is not True:
                errors.append(f"{book}: final postcheck lacks a role-separated checker verdict")
            if final_postcheck.get("independent_model_verdict_received") is not False:
                errors.append(f"{book}: final postcheck must not imply independent-model evidence")
            if final_postcheck.get("independent_agent_verdict_received") is not None:
                errors.append(f"{book}: deprecated self-attested independent-agent field must be absent")
            declared_checker_ids = final_postcheck.get("checker_attempt_ids")
            if declared_checker_ids is not None:
                if (
                    not isinstance(declared_checker_ids, list)
                    or not declared_checker_ids
                    or any(not isinstance(value, str) or not value for value in declared_checker_ids)
                    or len(declared_checker_ids) != len(set(declared_checker_ids))
                ):
                    errors.append(f"{book}: final postcheck checker_attempt_ids must be unique non-empty strings")
                else:
                    packet_checker_ids = {
                        str(packet.get("post_resolution_check", {}).get("checker_attempt_id", ""))
                        for packet in packets
                    }
                    if set(declared_checker_ids) != packet_checker_ids:
                        errors.append(
                            f"{book}: final postcheck checker_attempt_ids do not match packet cluster checkers"
                        )
            elif not isinstance(final_postcheck.get("checker_attempt_id"), str) or not final_postcheck.get(
                "checker_attempt_id"
            ):
                errors.append(f"{book}: final postcheck requires checker_attempt_id or checker_attempt_ids")

    for decision_id, chunk in chunk_by_id.items():
        packet = packet_by_id.get(decision_id)
        if not packet:
            continue
        if packet.get("book") != book or packet.get("span") != chunk.get("span"):
            errors.append(f"{decision_id}: review packet book/span differs from frozen chunk")
        if packet.get("review_revision") != chunk.get("review_revision", 0):
            errors.append(f"{decision_id}: review packet review_revision differs from frozen chunk")
        expected_digest = chunk_digest(chunk)
        if packet.get("chunk_sha256") != expected_digest:
            errors.append(f"{decision_id}: stale or invalid chunk_sha256")
        if packet.get("non_authorizing") is not True:
            errors.append(f"{decision_id}: review packet non_authorizing must be true")
        if packet.get("independence_scope") != INDEPENDENCE_SCOPE:
            errors.append(f"{decision_id}: missing or inaccurate independence_scope disclosure")

        reviews = packet.get("primary_reviews")
        if not isinstance(reviews, list) or len(reviews) < 2:
            errors.append(f"{decision_id}: at least two primary_reviews required")
            reviews = []
        reviewer_ids = [str(review.get("reviewer_attempt_id", "")) for review in reviews if isinstance(review, dict)]
        if len(reviewer_ids) != len(set(reviewer_ids)) or any(not value for value in reviewer_ids):
            errors.append(f"{decision_id}: primary reviewers must have distinct non-empty attempt IDs")
        for review in reviews:
            if not isinstance(review, dict):
                errors.append(f"{decision_id}: primary review must be an object")
                continue
            if review.get("blind_to_other_primary_reviews") is not True:
                errors.append(f"{decision_id}: primary review must be blind")
            if review.get("evidence_only") is not True:
                errors.append(f"{decision_id}: primary review must declare evidence_only")
            if not isinstance(review.get("evidence_refs"), list):
                errors.append(f"{decision_id}: primary review evidence_refs must be a list")

        challenges: dict[str, dict[str, Any]] = {}
        for review in reviews:
            if not isinstance(review, dict):
                continue
            for challenge in review.get("challenges", []) or []:
                if not isinstance(challenge, dict):
                    errors.append(f"{decision_id}: challenge must be an object")
                    continue
                challenge_id = challenge.get("challenge_id")
                if not isinstance(challenge_id, str) or not challenge_id:
                    errors.append(f"{decision_id}: challenge missing challenge_id")
                elif challenge_id in challenges:
                    errors.append(f"{decision_id}: duplicate challenge_id {challenge_id}")
                else:
                    challenges[challenge_id] = challenge

        crosscheck = packet.get("peer_crosscheck")
        if not isinstance(crosscheck, dict):
            errors.append(f"{decision_id}: peer_crosscheck required")
        else:
            checker = str(crosscheck.get("reviewer_attempt_id", ""))
            if not checker or checker in reviewer_ids:
                errors.append(f"{decision_id}: peer crosschecker must be distinct from primary reviewers")
            disputed_ids = set(crosscheck.get("disputed_claim_ids", []) or [])
            if not disputed_ids.issubset(set(challenges)):
                errors.append(f"{decision_id}: peer crosscheck references unknown challenge IDs")

        resolution = packet.get("sol_resolution")
        if not isinstance(resolution, dict):
            errors.append(f"{decision_id}: sol_resolution required")
            resolution = {}
        if resolution.get("author_id") != "M8_fable":
            errors.append(f"{decision_id}: sol_resolution author_id must be M8_fable")
        responses = resolution.get("challenge_responses", []) or []
        response_ids = {
            response.get("challenge_id")
            for response in responses
            if isinstance(response, dict) and isinstance(response.get("challenge_id"), str)
        }
        if response_ids != set(challenges):
            errors.append(
                f"{decision_id}: every challenge must have exactly one Sol response; "
                f"expected={sorted(challenges)} actual={sorted(response_ids)}"
            )
        final_state = packet.get("final_state")
        unresolved = resolution.get("unresolved_claim_ids", []) or []
        appeals = packet.get("appeals", []) or []
        if (unresolved or appeals) and final_state not in HELD_STATES:
            errors.append(f"{decision_id}: unresolved claims or appeals require a held/deferred final_state")
        # Boundary confidence and review disposition are independent axes. A
        # well-evidenced ambiguity can be a MEDIUM-confidence hold when the
        # unresolved question concerns retrieval treatment rather than whether
        # the observed seam exists.
        if final_state not in {"accepted_candidate", *HELD_STATES}:
            errors.append(f"{decision_id}: invalid final_state {final_state!r}")
        if final_state == "accepted_candidate":
            if chunk.get("review_status") != "candidate_review_complete":
                errors.append(f"{decision_id}: accepted packet requires candidate_review_complete chunk status")
            if chunk.get("candidate_hold_state") is not None:
                errors.append(f"{decision_id}: accepted packet must not retain candidate_hold_state")
            if packet.get("post_resolution_check", {}).get("status") != "pass":
                errors.append(f"{decision_id}: accepted packet requires a passing postcheck state")
        elif final_state in HELD_STATES:
            expected_status = "final_deferred_appeal" if appeals else "final_deferred_review"
            expected_basis = "preserved_appeal" if appeals else "specialist_or_external_review"
            if chunk.get("review_status") != expected_status:
                errors.append(f"{decision_id}: held packet requires {expected_status} chunk status")
            if chunk.get("candidate_hold_state") != "deferred_human_or_external_ai":
                errors.append(f"{decision_id}: held packet requires matching candidate_hold_state")
            hold_basis = chunk.get("candidate_hold_basis")
            structured_basis = (
                isinstance(hold_basis, dict)
                and isinstance(hold_basis.get("kind"), str)
                and isinstance(hold_basis.get("question"), str)
                and hold_basis["question"].endswith("?")
                and isinstance(hold_basis.get("options"), list)
                and len(hold_basis["options"]) == 2
            )
            if hold_basis != expected_basis and not structured_basis:
                errors.append(
                    f"{decision_id}: held packet requires {expected_basis} or a specific structured hold basis"
                )
            if packet.get("post_resolution_check", {}).get("status") != "hold":
                errors.append(f"{decision_id}: held packet requires a held postcheck state")
        if appeals and not isinstance(packet.get("boss_ruling"), dict):
            errors.append(f"{decision_id}: appeals require a preserved boss_ruling")
        for appeal in appeals:
            required = {
                "appeal_id",
                "appellant_attempt_id",
                "disagreement_with",
                "disputed_claim_id",
                "passage_context",
                "evidence_refs",
                "rationale",
                "uncertainty",
                "requested_next_reviewer",
            }
            if not isinstance(appeal, dict) or not required.issubset(appeal):
                errors.append(f"{decision_id}: appeal missing required context fields")

        postcheck = packet.get("post_resolution_check")
        if not isinstance(postcheck, dict):
            errors.append(f"{decision_id}: post_resolution_check required")
        else:
            checker = str(postcheck.get("checker_attempt_id", ""))
            if not checker or checker == "M8_fable":
                errors.append(f"{decision_id}: post-resolution checker must be role-separated from the author")
            if postcheck.get("status") not in {"pass", "hold"}:
                errors.append(f"{decision_id}: post-resolution status must be pass or hold")
            if require_final_artifacts:
                evidence_refs = postcheck.get("evidence_refs", [])
                if not isinstance(evidence_refs, list) or not evidence_refs:
                    errors.append(f"{decision_id}: final post-resolution check needs evidence_refs")
                else:
                    expected_ref = f"reviews/{book}/post_resolution_check_v2.json"
                    if evidence_refs != [expected_ref]:
                        errors.append(
                            f"{decision_id}: post-resolution evidence must point exactly to {expected_ref}"
                        )
                    elif final_postcheck is not None:
                        declared_checker_ids = final_postcheck.get("checker_attempt_ids")
                        if isinstance(declared_checker_ids, list):
                            if checker not in declared_checker_ids:
                                errors.append(f"{decision_id}: packet checker ID is absent from final cluster inventory")
                        elif final_postcheck.get("checker_attempt_id") != checker:
                            errors.append(f"{decision_id}: packet checker ID differs from final postcheck")
                        if decision_id not in final_postcheck.get("checked_decision_ids", []):
                            errors.append(f"{decision_id}: final postcheck omits this decision")
                        expected_status = "pass" if final_state == "accepted_candidate" else "hold"
                        if postcheck.get("status") != expected_status:
                            errors.append(f"{decision_id}: packet postcheck status is inconsistent")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", required=True)
    parser.add_argument("--require-final-artifacts", action="store_true")
    args = parser.parse_args()
    errors = validate(args.book, require_final_artifacts=args.require_final_artifacts)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: {args.book} exact verse coverage and review parity")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
