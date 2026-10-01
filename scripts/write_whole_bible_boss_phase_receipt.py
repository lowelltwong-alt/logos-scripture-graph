#!/usr/bin/env python3
"""Commit B06a before peer exposure, then B06b against that immutable commit."""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from scripts import whole_bible_replay_evidence as core


def write_phase(*, phase: str, book: str, run_id: str, attempt_id: str, assignment_manifest: Path, output_ruling: Path, provisional_receipt: Path | None, peer_premortem_manifest: Path | None, campaign_path: Path = core.DEFAULT_CAMPAIGN, model_root: Path = core.DEFAULT_MODEL_ROOT, root: Path = core.ROOT, allow_test_roots: bool = False) -> Path:
    core.validate_authoritative_runtime_paths(campaign_path=campaign_path, model_root=model_root, root=root, allow_test_roots=allow_test_roots)
    if phase not in {"provisional_B06a", "final_B06b"} or not core.SAFE_ID.fullmatch(run_id) or not core.SAFE_ID.fullmatch(attempt_id): raise core.ReplayEvidenceError("QF-SCHEMA", "boss phase identity")
    campaign = core.load_json(campaign_path); job = core.campaign_job(campaign, book)
    assignment, inputs, ids = core.validate_artifact_manifest(assignment_manifest, root=root, model_root=model_root, book=book, run_id=run_id, stage_id="B06", direction="input", job=job)
    ruling = output_ruling.resolve(); normalized_ruling = core.repo_relative(ruling, root); model_prefix = core.repo_relative(model_root, root).rstrip("/") + "/"
    if not ruling.is_file() or not normalized_ruling.startswith(model_prefix): raise core.ReplayEvidenceError("QF-09-FORBIDDEN-EFFECT", normalized_ruling)
    lowered = {key.lower(): value.lower() for key, value in ids.items()}
    prior_path: str | None = None; prior_hash: str | None = None; exposure: dict[str, str] = {}
    if phase == "provisional_B06a":
        if provisional_receipt is not None or peer_premortem_manifest is not None: raise core.ReplayEvidenceError("QF-03-BOSS-BACKFILL", "B06a cannot receive prior/peer inputs")
        forbidden = [key for key, value in lowered.items() if "peer" in key or "premortem" in key or "peer" in value or "premortem" in value]
        if forbidden: raise core.ReplayEvidenceError("QF-03-BOSS-BACKFILL", f"B06a assignment exposes peer/premortem: {forbidden}")
    else:
        if provisional_receipt is None or peer_premortem_manifest is None: raise core.ReplayEvidenceError("QF-03-BOSS-BACKFILL", "B06b needs B06a and peer/premortem manifest")
        provisional = provisional_receipt.resolve(); prior = core.load_json(provisional); core.validate_schema(prior, core.BOSS_PHASE_SCHEMA, "B06a receipt")
        if prior["phase"] != "provisional_B06a" or prior["book"] != book or prior["run_id"] != run_id: raise core.ReplayEvidenceError("QF-03-BOSS-BACKFILL", "B06a identity")
        peer_manifest, exposure, peer_ids = core.validate_artifact_manifest(peer_premortem_manifest, root=root, model_root=model_root, book=book, run_id=run_id, stage_id="B06", direction="input", job=job)
        if not any("peer" in key.lower() for key in peer_ids) or not any("premortem" in key.lower() for key in peer_ids): raise core.ReplayEvidenceError("QF-03-BOSS-BACKFILL", "peer/premortem exposure manifest incomplete")
        if "provisional_commit_receipt" not in ids or "peer_premortem_input_manifest" not in ids: raise core.ReplayEvidenceError("QF-03-BOSS-BACKFILL", "B06b assignment omits immutable predecessor/exposure manifest")
        if inputs[ids["provisional_commit_receipt"]] != core.digest_file(provisional) or inputs[ids["peer_premortem_input_manifest"]] != core.digest_file(peer_premortem_manifest): raise core.ReplayEvidenceError("QF-03-BOSS-BACKFILL", "B06b assignment hashes stale")
        prior_path, prior_hash = core.repo_relative(provisional, root), core.digest_file(provisional)
    receipt = {
        "schema_version": "whole_bible_boss_phase_receipt.v1", "phase_receipt_id": f"{campaign['campaign_id']}:{book}:{run_id}:{phase}:{attempt_id}",
        "campaign_id": campaign["campaign_id"], "campaign_revision": campaign["revision"], "book": book, "run_id": run_id, "phase": phase, "attempt_id": attempt_id,
        "controller_assignment_manifest_path": core.repo_relative(assignment_manifest, root), "controller_assignment_manifest_sha256": core.digest_file(assignment_manifest),
        "allowed_input_artifact_sha256": inputs, "output_ruling_path": normalized_ruling, "output_ruling_sha256": core.digest_file(ruling),
        "prior_boss_phase_receipt_path": prior_path, "prior_boss_phase_receipt_sha256": prior_hash, "peer_premortem_exposure_artifact_sha256": exposure,
        "committed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"), "shared_model_substrate": True,
        "counts_as_cross_model_independent_vote": False, "non_authorizing": True,
    }
    core.validate_schema(receipt, core.BOSS_PHASE_SCHEMA, phase); output = core.run_dir(model_root, book, run_id) / "boss_phases" / phase / f"{attempt_id}.json"
    with core.exclusive_lock(model_root / "state"): core.atomic_write(output, core.canonical_bytes(receipt), immutable=True)
    return output


def main(argv: list[str] | None = None) -> int:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--phase", choices=("provisional_B06a","final_B06b"), required=True); parser.add_argument("--book", required=True); parser.add_argument("--run-id", required=True); parser.add_argument("--attempt-id", required=True); parser.add_argument("--assignment-manifest", type=Path, required=True); parser.add_argument("--output-ruling", type=Path, required=True); parser.add_argument("--provisional-receipt", type=Path); parser.add_argument("--peer-premortem-manifest", type=Path); parser.add_argument("--campaign", type=Path, default=core.DEFAULT_CAMPAIGN); parser.add_argument("--model-root", type=Path, default=core.DEFAULT_MODEL_ROOT); args=parser.parse_args(argv)
    try: path=write_phase(phase=args.phase, book=args.book, run_id=args.run_id, attempt_id=args.attempt_id, assignment_manifest=args.assignment_manifest, output_ruling=args.output_ruling, provisional_receipt=args.provisional_receipt, peer_premortem_manifest=args.peer_premortem_manifest, campaign_path=args.campaign, model_root=args.model_root)
    except core.ReplayEvidenceError as exc: print(f"Boss phase commit failed: {exc}", file=sys.stderr); return 1
    print(f"Wrote immutable boss phase receipt: {core.repo_relative(path)}"); return 0

if __name__ == "__main__": raise SystemExit(main())
