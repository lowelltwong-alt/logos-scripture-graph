#!/usr/bin/env python3
"""Prepare, but never auto-commit, a revision-7 B00 attempt bundle."""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from scripts import whole_bible_replay_evidence_v2 as core
from scripts import write_whole_bible_stage_receipt_v2 as writer


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _row(artifact_id: str, path: Path, *, root: Path, scope: str) -> dict[str, str]:
    return {"artifact_id": artifact_id, "path": core.repo_relative(path, root), "sha256": core.digest_file(path), "media_type": "application/json", "scope": scope}


def _dependency(*, book: str, run_id: str, model_root: Path, root: Path) -> dict[str, Any]:
    if book == "Num":
        predecessor = model_root / "receipts" / "Lev_completion_v2.json"
        if not predecessor.is_file():
            raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", "Numbers predecessor snapshot missing")
        return {
            "schema_version": "whole_bible_dependency_evidence.v2", "book": book, "run_id": run_id,
            "status": "precontract_snapshot_waiver", "dependency_job_id": "J-003-LEV",
            "dependency_receipt_path": core.repo_relative(predecessor, root),
            "dependency_receipt_sha256": core.digest_file(predecessor),
            "precontract_waiver_reason": "revision_6_Leviticus_candidate_snapshot_precedes_revision_7_attempt_contract",
            "non_authorizing": True,
        }
    return {"schema_version": "whole_bible_dependency_evidence.v2", "book": book, "run_id": run_id, "status": "blocked_unmigrated_predecessor", "dependency_job_id": None, "dependency_receipt_path": None, "dependency_receipt_sha256": None, "precontract_waiver_reason": None, "non_authorizing": True}


def prepare_b00(*, book: str, run_id: str, attempt_id: str,
                campaign_path: Path = core.CAMPAIGN, registry_path: Path = core.REGISTRY,
                model_root: Path = core.MODEL_ROOT, root: Path = core.ROOT) -> Path:
    started = _now()
    core.validate_runtime_contract(campaign_path=campaign_path, registry_path=registry_path, root=root, model_root=model_root)
    campaign = core.load_json(campaign_path)
    if campaign.get("revision") != 7:
        raise core.ReplayEvidenceError("QF-13-ADAPTER-SPLIT", "B00 v2 requires revision 7")
    job = core.campaign_job(campaign, book)
    input_sha = {}
    for relative in job.get("inputs") or []:
        path = core.resolve_repo_path(relative, root)
        if not path.is_file():
            raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", f"missing campaign input: {relative}")
        input_sha[relative] = core.digest_file(path)
        declared = (job.get("input_digests") or {}).get(relative)
        if relative == core.repo_relative(campaign_path, root):
            if declared != "stage_receipt_v2:B00.campaign_sha256":
                raise core.ReplayEvidenceError("QF-11-HASH-CYCLE", "revision-7 campaign self marker")
        elif declared != input_sha[relative]:
            raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", f"stale campaign input digest: {relative}")
    base = core.attempt_root(model_root, book, run_id, "B00", attempt_id)
    evidence = base / "evidence"
    projection_path = evidence / "campaign_projection.json"
    dependency_path = evidence / "dependency_evidence.json"
    report_path = evidence / "preflight_report.json"
    projection = {
        "schema_version": "whole_bible_campaign_projection.v2", "campaign_id": campaign["campaign_id"],
        "campaign_revision": campaign["revision"], "campaign_path": core.repo_relative(campaign_path, root),
        "campaign_sha256": core.digest_file(campaign_path), "registry_path": core.repo_relative(registry_path, root),
        "registry_sha256": core.digest_file(registry_path), "book": book, "run_id": run_id, "job_id": job["id"],
        "job_projection_sha256": core.digest_bytes(core.canonical_bytes(job)), "input_sha256": input_sha,
        "sibling_map_exclusion_verified": True,
        "campaign_projection_algorithm": "registry_bound_exact_campaign_and_job_projection",
        "contains_scripture_text": False, "contains_source_rows": False, "non_authorizing": True,
    }
    dependency = _dependency(book=book, run_id=run_id, model_root=model_root, root=root)
    report = {
        "schema_version": "whole_bible_B00_preflight_report.v2", "book": book, "run_id": run_id,
        "campaign_projection_sha256": core.digest_bytes(core.canonical_bytes(projection)),
        "source_digests_pinned": True, "sibling_map_exclusion_verified": True,
        "supported_stage_ceiling": "B00", "B02_authorized": False,
        "static_specification_valid_only": True, "replay_qualified": False,
        "launch_qualified": False, "non_authorizing": True,
    }
    with core.exclusive_lock(model_root / "state"):
        core.atomic_write(projection_path, core.canonical_bytes(projection), immutable=True)
        core.atomic_write(dependency_path, core.canonical_bytes(dependency), immutable=True)
        core.atomic_write(report_path, core.canonical_bytes(report), immutable=True)
    input_manifest = {
        "schema_version": "whole_bible_artifact_manifest.v2", "manifest_id": f"{campaign['campaign_id']}:{book}:{run_id}:B00:{attempt_id}:input",
        "book": book, "run_id": run_id, "stage_id": "B00", "attempt_id": attempt_id, "direction": "input",
        "artifacts": [
            _row("campaign_registry", registry_path, root=root, scope="governance_input"),
            _row("workflow", core.WORKFLOW, root=root, scope="governance_input"),
            _row("prompt_pack", core.PROMPTS, root=root, scope="governance_input"),
            _row("runtime_adapter", core.ADAPTER, root=root, scope="governance_input"),
        ],
        "contains_scripture_text": False, "contains_source_rows": False,
        "contains_prompts_or_hidden_reasoning": False, "non_authorizing": True,
    }
    output_manifest = {
        "schema_version": "whole_bible_artifact_manifest.v2", "manifest_id": f"{campaign['campaign_id']}:{book}:{run_id}:B00:{attempt_id}:output",
        "book": book, "run_id": run_id, "stage_id": "B00", "attempt_id": attempt_id, "direction": "output",
        "artifacts": [
            _row("campaign_projection", projection_path, root=root, scope="validator_evidence"),
            _row("preflight_report", report_path, root=root, scope="validator_evidence"),
            _row("dependency_evidence", dependency_path, root=root, scope="validator_evidence"),
        ],
        "contains_scripture_text": False, "contains_source_rows": False,
        "contains_prompts_or_hidden_reasoning": False, "non_authorizing": True,
    }
    input_path = base / "manifests" / "input.json"
    output_path = base / "manifests" / "output.json"
    with core.exclusive_lock(model_root / "state"):
        core.atomic_write(input_path, core.canonical_bytes(input_manifest), immutable=True)
        core.atomic_write(output_path, core.canonical_bytes(output_manifest), immutable=True)
    finished = _now()
    if core.parse_time(started, "B00 start") >= core.parse_time(finished, "B00 finish"):
        raise core.ReplayEvidenceError("QF-19-B01-TIMING", "B00 controller clock did not advance")
    draft = {
        "schema_version": "whole_bible_stage_receipt_draft.v2", "book": book, "run_id": run_id,
        "stage_id": "B00", "attempt_id": attempt_id, "attempt_kind": "original",
        "role_or_deterministic_gate": "authoritative_B00_preflight_builder_v2", "executor_kind": "deterministic",
        "started_at": started, "finished_at": finished, "outcome": "succeeded", "unresolved_holds": [],
        "input_manifest_path": core.repo_relative(input_path, root), "output_manifest_path": core.repo_relative(output_path, root),
        "stage_evidence": {"artifact_refs": {
            "campaign_projection": "campaign_projection", "workflow": "workflow", "prompt_pack": "prompt_pack",
            "runtime_adapter": "runtime_adapter", "campaign_registry": "campaign_registry",
            "preflight_report": "preflight_report", "dependency_evidence": "dependency_evidence",
        }, "values": {"sibling_map_exclusion_verified": True, "source_digests_pinned": True, "campaign_projection_algorithm": "registry_bound_exact_campaign_and_job_projection"}},
        "independence_scope": {"authoring_independent_from_sibling_maps": True, "artifact_blindness": False,
            "role_separation": False, "shared_model_substrate": True, "runtime_model_identity_attested": False,
            "independent_model_or_provider_evidence": False, "counts_as_cross_model_independent_vote": False,
            "convergence_weight": "one_model_voice"},
        "non_authorizing": True,
    }
    draft_path = base / "draft.json"
    with core.exclusive_lock(model_root / "state"):
        core.atomic_write(draft_path, core.canonical_bytes(draft), immutable=True)
    return writer.prepare_stage_receipt(draft_path=draft_path, campaign_path=campaign_path, registry_path=registry_path, model_root=model_root, root=root)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--attempt-id", required=True)
    args = parser.parse_args(argv)
    try:
        path = prepare_b00(book=args.book, run_id=args.run_id, attempt_id=args.attempt_id)
    except core.ReplayEvidenceError as exc:
        print(f"B00 v2 prepare failed: {exc}", file=sys.stderr)
        return 1
    print(core.repo_relative(path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
