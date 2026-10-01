#!/usr/bin/env python3
"""Fail-fast completion gate bundle with hash-closed postcheck and receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from review_contract_constants import INDEPENDENCE_SCOPE


ROOT = Path(__file__).resolve().parents[5]
MODEL = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol"
CHECKS = MODEL / "checks"
SIDECARS = (
    "low_confidence_register.jsonl",
    "frontier_escalation_queue.jsonl",
    "atlas_candidate_feed.jsonl",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT).as_posix()}: expected object")
    return value


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        rows = [json.loads(line) for line in handle if line.strip()]
    if any(not isinstance(row, dict) for row in rows):
        raise ValueError(f"{path.relative_to(ROOT).as_posix()}: expected object rows")
    return rows


def book_rows_digest(path: Path, book: str) -> str:
    rows = [row for row in read_jsonl(path) if row.get("book") == book]
    payload = b"".join(
        (json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")
        for row in rows
    )
    return hashlib.sha256(payload).hexdigest()


def postcheck_gate_commands(book: str) -> list[tuple[str, list[str]]]:
    chunk_path = MODEL / "book_chunks" / book / "chunks.jsonl"
    return [
        ("exact_ordered_coverage", [sys.executable, str(CHECKS / "validate_exact_book_coverage.py"), "--book", book]),
        ("official_chunk_map", [sys.executable, str(ROOT / "scripts" / "validate_whole_bible_chunk_map.py"), str(chunk_path), "--model-id", "M7_sol", "--book", book, "--python-only"]),
        ("review_status_sidecar_independence_parity", [sys.executable, str(CHECKS / "validate_book_review_coverage.py"), "--book", book]),
        ("literary_quality_protocol", [sys.executable, str(ROOT / "scripts" / "validate_t423_literary_quality_protocol.py"), "--model-folder", str(MODEL), "--book", book, "--require-artifacts"]),
        ("corrective_review_depth", [sys.executable, str(ROOT / "scripts" / "validate_m7_corrective_review_depth.py"), "--model-root", str(MODEL), "--book", book, "--json"]),
    ]


def completion_gate_commands(book: str) -> list[tuple[str, list[str]]]:
    commands = postcheck_gate_commands(book)
    commands[2] = (
        "review_status_sidecar_independence_parity",
        [sys.executable, str(CHECKS / "validate_book_review_coverage.py"), "--book", book, "--require-final-artifacts"],
    )
    commands.append(
        ("workflow_replay_contract", [sys.executable, str(ROOT / "scripts" / "validate_whole_bible_candidate_workflow.py")])
    )
    return commands


def run_gate(gate_id: str, args: list[str]) -> bool:
    print(f"RUN {gate_id}: {' '.join(args)}")
    result = subprocess.run(args, cwd=ROOT, shell=False, check=False)
    if result.returncode:
        print(f"FAIL {gate_id}: exit={result.returncode}", file=sys.stderr)
        return False
    print(f"PASS {gate_id}")
    return True


def validate_closure(book: str) -> list[str]:
    errors: list[str] = []
    chunks_path = MODEL / "book_chunks" / book / "chunks.jsonl"
    packets_path = MODEL / "reviews" / book / "review_packets.jsonl"
    postcheck_path = MODEL / "reviews" / book / "post_resolution_check_v2.json"
    relations_path = MODEL / "reviews" / book / "decision_relations.jsonl"
    receipt_path = MODEL / "receipts" / f"{book}_completion_v2.json"
    for path in (chunks_path, packets_path, relations_path, postcheck_path, receipt_path):
        if not path.is_file():
            errors.append(f"missing final artifact {path.relative_to(ROOT).as_posix()}")
    if errors:
        return errors

    try:
        chunks = read_jsonl(chunks_path)
        packets = read_jsonl(packets_path)
        postcheck = read_json(postcheck_path)
        receipt = read_json(receipt_path)
    except (ValueError, json.JSONDecodeError) as exc:
        return [str(exc)]

    chunks_hash = digest(chunks_path)
    packets_hash = digest(packets_path)
    postcheck_hash = digest(postcheck_path)
    relations_hash = digest(relations_path)
    sidecar_hashes = {name: book_rows_digest(MODEL / name, book) for name in SIDECARS}
    if postcheck.get("book") != book:
        errors.append("postcheck book mismatch")
    if postcheck.get("checked_chunks_sha256") != chunks_hash:
        errors.append("postcheck checked_chunks_sha256 is stale")
    if postcheck.get("checked_review_packets_sha256") != packets_hash:
        errors.append("postcheck checked_review_packets_sha256 is stale")
    if postcheck.get("checked_decision_relations_sha256") != relations_hash:
        errors.append("postcheck checked_decision_relations_sha256 is stale")
    if postcheck.get("checked_uncertainty_sidecar_sha256") != sidecar_hashes:
        errors.append("postcheck uncertainty-sidecar hashes are stale")
    if postcheck.get("independence_scope") != INDEPENDENCE_SCOPE:
        errors.append("postcheck independence_scope is missing or inaccurate")
    if postcheck.get("non_authorizing") is not True:
        errors.append("postcheck must be non_authorizing")
    if postcheck.get("role_separated_checker_verdict_received") is not True:
        errors.append("postcheck lacks role-separated checker verdict")
    if postcheck.get("independent_model_verdict_received") is not False:
        errors.append("postcheck overclaims independent-model evidence")
    if postcheck.get("independent_agent_verdict_received") is not None:
        errors.append("postcheck retains deprecated self-attested independent-agent field")
    if postcheck.get("failures") != []:
        errors.append("postcheck retains failures")

    accepted = sorted(row["decision_id"] for row in packets if row.get("final_state") == "accepted_candidate")
    held = sorted(row["decision_id"] for row in packets if row.get("final_state") != "accepted_candidate")
    appeals = sorted(
        appeal["appeal_id"]
        for row in packets
        for appeal in row.get("appeals", [])
        if isinstance(appeal, dict) and isinstance(appeal.get("appeal_id"), str)
    )
    if sorted(postcheck.get("accepted_decision_ids", [])) != accepted:
        errors.append("postcheck accepted_decision_ids mismatch")
    if sorted(postcheck.get("held_decision_ids", [])) != held:
        errors.append("postcheck held_decision_ids mismatch")
    if sorted(postcheck.get("appeal_ids", [])) != appeals:
        errors.append("postcheck appeal_ids mismatch")
    if sorted(postcheck.get("checked_decision_ids", [])) != sorted(row["decision_id"] for row in packets):
        errors.append("postcheck checked_decision_ids mismatch")
    expected_status = "pass_with_holds" if held else "pass"
    if postcheck.get("overall_status") != expected_status:
        errors.append("postcheck overall_status mismatch")

    expected_postcheck_commands = {
        gate_id: " ".join(command)
        for gate_id, command in postcheck_gate_commands(book)
    }
    postcheck_results = postcheck.get("validation_results")
    if not isinstance(postcheck_results, list) or len(postcheck_results) != len(expected_postcheck_commands):
        errors.append("postcheck validation_results count mismatch")
    else:
        seen_postcheck_ids: set[str] = set()
        for result in postcheck_results:
            if not isinstance(result, dict):
                errors.append("postcheck validation result must be an object")
                continue
            gate_id = result.get("gate_id")
            if gate_id in seen_postcheck_ids or gate_id not in expected_postcheck_commands:
                errors.append(f"postcheck validation result has duplicate or unknown gate {gate_id!r}")
                continue
            seen_postcheck_ids.add(gate_id)
            if (
                result.get("command") != expected_postcheck_commands[gate_id]
                or result.get("exit_code") != 0
                or result.get("status") != "pass"
                or not isinstance(result.get("output"), str)
                or not result.get("output").strip()
            ):
                errors.append(f"postcheck validation result {gate_id} is incomplete or untrusted")
        if seen_postcheck_ids != set(expected_postcheck_commands):
            errors.append("postcheck validation result gate set mismatch")

    verdict_path_value = postcheck.get("checker_verdict_path")
    verdict_path = ROOT / verdict_path_value if isinstance(verdict_path_value, str) else None
    verdict_hash = digest(verdict_path) if verdict_path is not None and verdict_path.is_file() else None
    if verdict_hash is None or postcheck.get("checker_verdict_sha256") != verdict_hash:
        errors.append("postcheck checker verdict artifact is missing or stale")
    else:
        try:
            checker_verdict = read_json(verdict_path)
        except (ValueError, json.JSONDecodeError) as exc:
            errors.append(str(exc))
        else:
            required_verdict = {
                "schema_version": "m7_role_separated_checker_verdict.v1",
                "book": book,
                "checker_attempt_id": postcheck.get("checker_attempt_id"),
                "checked_chunks_sha256": chunks_hash,
                "checked_review_packets_sha256": packets_hash,
                "checked_decision_relations_sha256": relations_hash,
                "checked_uncertainty_sidecar_sha256": sidecar_hashes,
                "verdict": expected_status,
                "role_separated_from_author": True,
                "shared_model_substrate": True,
                "counts_as_cross_model_independent_vote": False,
                "non_authorizing": True,
            }
            for field, expected in required_verdict.items():
                if checker_verdict.get(field) != expected:
                    errors.append(f"checker verdict field {field} mismatch")
            if checker_verdict.get("findings") not in ([], None):
                errors.append("checker verdict retains findings")

    expected_receipt = {
        "book": book,
        "chunks_sha256": chunks_hash,
        "review_packets_sha256": packets_hash,
        "decision_relations_sha256": relations_hash,
        "uncertainty_sidecar_sha256": sidecar_hashes,
        "postcheck_sha256": postcheck_hash,
        "checker_verdict_path": verdict_path_value,
        "checker_verdict_sha256": verdict_hash,
        "postchecker_attempt_id": postcheck.get("checker_attempt_id"),
        "postcheck_status": expected_status,
        "completion_state": "candidate_complete_with_explicit_holds" if held else "candidate_complete",
        "receipt_written_after_final_hash_and_gates": True,
        "chunk_count": len(chunks),
        "review_packet_count": len(packets),
        "accepted_decision_count": len(accepted),
        "held_decision_count": len(held),
        "unresolved_appeal_count": len(appeals),
        "accepted_decision_ids": accepted,
        "held_decision_ids": held,
        "unresolved_appeal_ids": appeals,
        "independence_scope": INDEPENDENCE_SCOPE,
        "post_receipt_validation_required": True,
        "non_authorizing": True,
    }
    for field, expected in expected_receipt.items():
        actual = receipt.get(field)
        if isinstance(expected, list):
            actual = sorted(actual) if isinstance(actual, list) else actual
        if actual != expected:
            errors.append(f"completion receipt field {field} mismatch")
    expected_gate_commands = {
        gate_id: " ".join(command)
        for gate_id, command in completion_gate_commands(book)
    }
    gate_rows = receipt.get("pre_receipt_gates")
    if not isinstance(gate_rows, list) or len(gate_rows) != len(expected_gate_commands):
        errors.append("completion receipt pre_receipt_gates count mismatch")
    else:
        seen_gate_ids: set[str] = set()
        for gate in gate_rows:
            if not isinstance(gate, dict):
                errors.append("completion receipt gate must be an object")
                continue
            gate_id = gate.get("gate_id")
            if gate_id in seen_gate_ids or gate_id not in expected_gate_commands:
                errors.append(f"completion receipt duplicate or unknown gate {gate_id!r}")
                continue
            seen_gate_ids.add(gate_id)
            if (
                gate.get("command") != expected_gate_commands[gate_id]
                or gate.get("exit_code") != 0
                or gate.get("status") != "pass"
                or not isinstance(gate.get("output"), str)
                or not gate.get("output").strip()
            ):
                errors.append(f"completion receipt gate {gate_id} is incomplete or untrusted")
        if seen_gate_ids != set(expected_gate_commands):
            errors.append("completion receipt pre_receipt_gates set mismatch")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", required=True)
    args = parser.parse_args()
    book = args.book
    gates = completion_gate_commands(book)
    for gate_id, command in gates:
        if not run_gate(gate_id, command):
            return 1
    errors = validate_closure(book)
    if errors:
        for error in errors:
            print(f"ERROR completion_receipt_closure: {error}", file=sys.stderr)
        return 1
    print(f"PASS completion_receipt_closure")
    print(f"OK: {book} completion bundle")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
