#!/usr/bin/env python3
"""Write a v2 completion receipt last from current hash-closed gate evidence."""
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
PASSAGES = ROOT / "data" / "canonical" / "scripture" / "passages" / "passages.jsonl"
SIDECARS = (
    "low_confidence_register.jsonl",
    "frontier_escalation_queue.jsonl",
    "atlas_candidate_feed.jsonl",
)


def read_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected object")
    return value


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def book_rows_digest(path: Path, book: str) -> str:
    rows = [row for row in read_jsonl(path) if row.get("book") == book]
    payload = b"".join(
        (json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")
        for row in rows
    )
    return hashlib.sha256(payload).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", required=True)
    args = parser.parse_args()
    book = args.book
    chunks_path = MODEL / "book_chunks" / book / "chunks.jsonl"
    packets_path = MODEL / "reviews" / book / "review_packets.jsonl"
    postcheck_path = MODEL / "reviews" / book / "post_resolution_check_v2.json"
    relations_path = MODEL / "reviews" / book / "decision_relations.jsonl"
    chunks_hash = digest(chunks_path)
    packets_hash = digest(packets_path)
    postcheck_hash = digest(postcheck_path)
    relations_hash = digest(relations_path)
    sidecar_hashes = {name: book_rows_digest(MODEL / name, book) for name in SIDECARS}
    postcheck = read_json(postcheck_path)
    if postcheck.get("checked_chunks_sha256") != chunks_hash:
        raise SystemExit("v2 postcheck has a stale chunk hash")
    if postcheck.get("checked_review_packets_sha256") != packets_hash:
        raise SystemExit("v2 postcheck has a stale review-packet hash")
    if postcheck.get("checked_decision_relations_sha256") != relations_hash:
        raise SystemExit("v2 postcheck has a stale decision-relations hash")
    if postcheck.get("checked_uncertainty_sidecar_sha256") != sidecar_hashes:
        raise SystemExit("v2 postcheck has stale uncertainty-sidecar hashes")
    if postcheck.get("role_separated_checker_verdict_received") is not True:
        raise SystemExit("v2 postcheck lacks a role-separated checker verdict")
    if postcheck.get("independent_model_verdict_received") is not False:
        raise SystemExit("v2 postcheck overclaims independent-model evidence")
    if postcheck.get("failures") != []:
        raise SystemExit("v2 postcheck retains failures")
    verdict_path_value = postcheck.get("checker_verdict_path")
    if not isinstance(verdict_path_value, str):
        raise SystemExit("v2 postcheck lacks checker verdict path")
    verdict_path = ROOT / verdict_path_value
    if not verdict_path.is_file() or postcheck.get("checker_verdict_sha256") != digest(verdict_path):
        raise SystemExit("v2 postcheck checker verdict is missing or stale")

    commands = [
        ("exact_ordered_coverage", [sys.executable, str(CHECKS / "validate_exact_book_coverage.py"), "--book", book]),
        ("official_chunk_map", [sys.executable, str(ROOT / "scripts" / "validate_whole_bible_chunk_map.py"), str(chunks_path), "--model-id", "M7_sol", "--book", book, "--python-only"]),
        ("review_status_sidecar_independence_parity", [sys.executable, str(CHECKS / "validate_book_review_coverage.py"), "--book", book, "--require-final-artifacts"]),
        ("literary_quality_protocol", [sys.executable, str(ROOT / "scripts" / "validate_t423_literary_quality_protocol.py"), "--model-folder", str(MODEL), "--book", book, "--require-artifacts"]),
        ("corrective_review_depth", [sys.executable, str(ROOT / "scripts" / "validate_m7_corrective_review_depth.py"), "--model-root", str(MODEL), "--book", book, "--json"]),
        ("workflow_replay_contract", [sys.executable, str(ROOT / "scripts" / "validate_whole_bible_candidate_workflow.py")]),
    ]
    gate_results: list[dict] = []
    for gate_id, command in commands:
        result = subprocess.run(command, cwd=ROOT, shell=False, check=False, capture_output=True, text=True)
        if result.returncode:
            raise SystemExit(f"{gate_id} failed; refusing completion receipt")
        gate_results.append({
            "gate_id": gate_id,
            "command": " ".join(command),
            "exit_code": result.returncode,
            "status": "pass",
            "output": result.stdout.strip(),
        })

    chunks = read_jsonl(chunks_path)
    packets = read_jsonl(packets_path)
    canonical_verses = sum(1 for row in read_jsonl(PASSAGES) if row.get("book") == book)
    accepted = sorted(row["decision_id"] for row in packets if row.get("final_state") == "accepted_candidate")
    held = sorted(row["decision_id"] for row in packets if row.get("final_state") != "accepted_candidate")
    appeals = sorted(
        appeal["appeal_id"]
        for row in packets
        for appeal in row.get("appeals", [])
        if isinstance(appeal, dict) and isinstance(appeal.get("appeal_id"), str)
    )
    expected_postcheck_status = "pass_with_holds" if held else "pass"
    if postcheck.get("overall_status") != expected_postcheck_status:
        raise SystemExit("v2 postcheck overall_status conflicts with active holds")
    checked_results = postcheck.get("validation_results")
    if (
        not isinstance(checked_results, list)
        or not checked_results
        or any(
            not isinstance(row, dict)
            or row.get("status") != "pass"
            or row.get("exit_code") != 0
            for row in checked_results
        )
    ):
        raise SystemExit("v2 postcheck validation_results are incomplete or failed")
    receipt = {
        "schema_version": "m7_book_completion_receipt.v2",
        "model_id": "M7_sol",
        "book": book,
        "completion_state": "candidate_complete_with_explicit_holds" if held else "candidate_complete",
        "chunk_count": len(chunks),
        "review_packet_count": len(packets),
        "canonical_verse_count": canonical_verses,
        "covered_verse_count": canonical_verses,
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
        "postcheck_sha256": postcheck_hash,
        "checker_verdict_path": verdict_path_value,
        "checker_verdict_sha256": digest(verdict_path),
        "postchecker_attempt_id": postcheck.get("checker_attempt_id"),
        "postcheck_status": postcheck.get("overall_status"),
        "independence_scope": INDEPENDENCE_SCOPE,
        "pre_receipt_gates": gate_results,
        "receipt_written_after_final_hash_and_gates": True,
        "validation_bundle_command": f"python {CHECKS.relative_to(ROOT).as_posix()}/validate_book_completion_bundle.py --book {book}",
        "post_receipt_validation_required": True,
        "forced_consensus": False,
        "non_authorizing": True,
    }
    receipt_path = MODEL / "receipts" / f"{book}_completion_v2.json"
    receipt_path.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"wrote {receipt_path.relative_to(ROOT).as_posix()} last")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
