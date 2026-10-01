#!/usr/bin/env python3
"""Materialize a hash-bound v2 postcheck from a fresh role-separated verdict."""
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


def read_verdict(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise SystemExit("checker verdict must be a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", required=True)
    parser.add_argument("--checker-verdict-file", required=True)
    args = parser.parse_args()
    book = args.book
    chunks_path = MODEL / "book_chunks" / book / "chunks.jsonl"
    packets_path = MODEL / "reviews" / book / "review_packets.jsonl"
    relations_path = MODEL / "reviews" / book / "decision_relations.jsonl"
    actual_chunks = digest(chunks_path)
    actual_packets = digest(packets_path)
    actual_relations = digest(relations_path)
    sidecar_hashes = {name: book_rows_digest(MODEL / name, book) for name in SIDECARS}

    verdict_path = Path(args.checker_verdict_file)
    if not verdict_path.is_absolute():
        verdict_path = ROOT / verdict_path
    verdict_path = verdict_path.resolve()
    expected_parent = (MODEL / "reviews" / book).resolve()
    if verdict_path.parent != expected_parent:
        raise SystemExit("checker verdict must live in the book review directory")
    verdict = read_verdict(verdict_path)
    required_verdict = {
        "schema_version": "m7_role_separated_checker_verdict.v1",
        "book": book,
        "checked_chunks_sha256": actual_chunks,
        "checked_review_packets_sha256": actual_packets,
        "checked_decision_relations_sha256": actual_relations,
        "checked_uncertainty_sidecar_sha256": sidecar_hashes,
        "role_separated_from_author": True,
        "shared_model_substrate": True,
        "counts_as_cross_model_independent_vote": False,
        "non_authorizing": True,
    }
    for field, expected in required_verdict.items():
        if verdict.get(field) != expected:
            raise SystemExit(f"checker verdict field {field} mismatch")
    checker_attempt_id = verdict.get("checker_attempt_id")
    if not isinstance(checker_attempt_id, str) or not checker_attempt_id or checker_attempt_id == "M7_sol":
        raise SystemExit("checker verdict needs a distinct checker_attempt_id")
    if verdict.get("findings") not in ([], None):
        raise SystemExit("checker verdict retains unresolved findings")

    commands = [
        ("exact_ordered_coverage", [sys.executable, str(CHECKS / "validate_exact_book_coverage.py"), "--book", book]),
        ("official_chunk_map", [sys.executable, str(ROOT / "scripts" / "validate_whole_bible_chunk_map.py"), str(chunks_path), "--model-id", "M7_sol", "--book", book, "--python-only"]),
        ("review_status_sidecar_independence_parity", [sys.executable, str(CHECKS / "validate_book_review_coverage.py"), "--book", book]),
        ("literary_quality_protocol", [sys.executable, str(ROOT / "scripts" / "validate_t423_literary_quality_protocol.py"), "--model-folder", str(MODEL), "--book", book, "--require-artifacts"]),
        ("corrective_review_depth", [sys.executable, str(ROOT / "scripts" / "validate_m7_corrective_review_depth.py"), "--model-root", str(MODEL), "--book", book, "--json"]),
    ]
    results: list[dict] = []
    for gate_id, command in commands:
        result = subprocess.run(command, cwd=ROOT, shell=False, check=False, capture_output=True, text=True)
        results.append({
            "gate_id": gate_id,
            "command": " ".join(command),
            "exit_code": result.returncode,
            "status": "pass" if result.returncode == 0 else "fail",
            "output": (result.stdout or result.stderr).strip(),
        })
        if result.returncode:
            raise SystemExit(f"{gate_id} failed; refusing postcheck materialization")

    chunks = read_jsonl(chunks_path)
    packets = read_jsonl(packets_path)
    accepted = sorted(row["decision_id"] for row in packets if row.get("final_state") == "accepted_candidate")
    held = sorted(row["decision_id"] for row in packets if row.get("final_state") != "accepted_candidate")
    appeals = sorted(
        appeal["appeal_id"]
        for row in packets
        for appeal in row.get("appeals", [])
        if isinstance(appeal, dict) and isinstance(appeal.get("appeal_id"), str)
    )
    expected_verdict = "pass_with_holds" if held else "pass"
    if verdict.get("verdict") != expected_verdict:
        raise SystemExit(
            f"role-separated verdict {verdict.get('verdict')} conflicts with held set {held}"
        )
    output = {
        "schema_version": "m7_post_resolution_check.v2",
        "checker_attempt_id": checker_attempt_id,
        "role": "fresh_read_only_post_resolution_checker",
        "book": book,
        "checked_chunks_sha256": actual_chunks,
        "checked_review_packets_sha256": actual_packets,
        "checked_decision_relations_sha256": actual_relations,
        "checked_uncertainty_sidecar_sha256": sidecar_hashes,
        "checked_decision_ids": sorted(row["decision_id"] for row in packets),
        "checker_verdict_path": verdict_path.relative_to(ROOT).as_posix(),
        "checker_verdict_sha256": digest(verdict_path),
        "validation_results": results,
        "chunk_count": len(chunks),
        "review_packet_count": len(packets),
        "accepted_decision_count": len(accepted),
        "accepted_decision_ids": accepted,
        "held_decision_count": len(held),
        "held_decision_ids": held,
        "appeal_count": len(appeals),
        "appeal_ids": appeals,
        "independence_scope": INDEPENDENCE_SCOPE,
        "independence_limit": "Role-separated checks share one model substrate and count as one correlated model voice.",
        "role_separated_checker_verdict_received": True,
        "independent_model_verdict_received": False,
        "failures": [],
        "overall_status": verdict["verdict"],
        "forced_consensus": False,
        "non_authorizing": True,
    }
    output_path = MODEL / "reviews" / book / "post_resolution_check_v2.json"
    output_path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"wrote {output_path.relative_to(ROOT).as_posix()} for {actual_chunks}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
