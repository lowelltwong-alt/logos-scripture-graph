"""Replay-validate review evidence and emit an unpromoted derivative."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .contracts import ContractError, canonical_sha256, load_json, verify_run_artifacts, write_json_exclusive


def validate_review(run: dict[str, Any], review: dict[str, Any]) -> str | None:
    if review.get("schema") != "portable_ocr_review_session.v1" or review.get("run_id") != run.get("run_id"):
        raise ContractError("review schema or run_id mismatch")
    if review.get("source_sha256") != run.get("source", {}).get("sha256"):
        raise ContractError("review source hash mismatch")
    expected = {(c["candidate_id"], c["text_sha256"]) for c in run.get("candidates", [])}
    observed = {(c.get("candidate_id"), c.get("text_sha256")) for c in review.get("candidate_hashes", [])}
    if expected != observed:
        raise ContractError("review candidate hashes mismatch")
    events = review.get("events")
    if review.get("state") != "complete" or not isinstance(events, list) or len(events) < 2:
        raise ContractError("review is incomplete or not replayable")
    if [e.get("sequence") for e in events] != list(range(1, len(events) + 1)):
        raise ContractError("review event sequence is invalid")
    interpreted, confirmation = events[-2], events[-1]
    if confirmation.get("question_state") != "confirm_interpretation" or confirmation.get("interpreted_intent") != "confirm":
        raise ContractError("review lacks explicit confirmation")
    if review.get("reviewer_attestation") is not True:
        raise ContractError("reviewer visual-inspection attestation is required")
    decision = review.get("decision") or {}
    if decision.get("human_confirmed") is not True or decision.get("automatic_promotion_performed") is not False:
        raise ContractError("human authority boundary is invalid")
    mapping = {"choose_candidate": "selected_engine_candidate", "supply_text": "verified_with_corrections",
               "cannot_read": "needs_second_review", "no_text_by_design": "no_extractable_text_by_design"}
    if mapping.get(interpreted.get("interpreted_intent")) != decision.get("disposition"):
        raise ContractError("decision does not replay from confirmed answer")
    if decision["disposition"] == "selected_engine_candidate":
        matches = [c for c in run["candidates"] if c["blind_label"] == decision.get("value")]
        if len(matches) != 1:
            raise ContractError("selected candidate is unavailable")
        return str(matches[0]["text"])
    if decision["disposition"] == "verified_with_corrections":
        value = decision.get("value")
        if not isinstance(value, str) or not value.strip():
            raise ContractError("exact correction is required")
        return value
    return None


def build_handoff(run_dir: Path, review_path: Path, output: Path) -> Path:
    run, review = load_json(run_dir / "run.json"), load_json(review_path)
    verify_run_artifacts(run_dir, run)
    text = validate_review(run, review)
    write_json_exclusive(output, {"schema": "portable_ocr_reviewed_text_handoff.v1", "run_id": run["run_id"],
        "source": run["source"], "review_disposition": review["decision"]["disposition"], "reviewed_text": text,
        "reviewed_text_sha256": None if text is None else canonical_sha256(text),
        "review_record_sha256": canonical_sha256(review), "created_at": datetime.now(timezone.utc).isoformat(),
        "reviewed_derivative_not_source_truth": True, "host_promotion_required": True})
    return output
