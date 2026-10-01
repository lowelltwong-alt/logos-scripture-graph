#!/usr/bin/env python3
"""Build and materialize an authoritative, hash-bound B00 preflight receipt."""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from scripts import whole_bible_replay_evidence as core
from scripts import write_whole_bible_stage_receipt as stage_writer


def artifact_row(artifact_id: str, path: Path, *, root: Path, scope: str) -> dict[str, str]:
    return {
        "artifact_id": artifact_id,
        "path": core.repo_relative(path, root),
        "sha256": core.digest_file(path),
        "media_type": "application/json" if path.suffix == ".json" else "application/yaml",
        "scope": scope,
    }


def dependency_evidence(*, campaign: dict[str, Any], job: dict[str, Any], book: str, run_id: str, model_root: Path, root: Path) -> dict[str, Any]:
    dependencies = job.get("depends_on") or []
    digests = job.get("dependency_digests") or {}
    if not dependencies:
        return {"schema_version": "whole_bible_dependency_evidence.v1", "book": book, "run_id": run_id, "status": "no_dependency", "dependency_job_id": None, "dependency_receipt_path": None, "dependency_receipt_sha256": None, "precontract_waiver_reason": None, "non_authorizing": True}
    if len(dependencies) != 1 or set(digests) != set(dependencies):
        raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", "exactly one declared predecessor is required")
    dependency = dependencies[0]
    declared = digests[dependency]
    if book == "Num" and dependency == "J-003-LEV":
        receipt = model_root / "receipts" / "Lev_completion_v2.json"
        expected = f"precontract_snapshot_waiver:Lev_completion_v2:{core.digest_file(receipt)}" if receipt.is_file() else None
        if declared != expected:
            raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", "Numbers needs the exact Leviticus precontract waiver hash")
        return {"schema_version": "whole_bible_dependency_evidence.v1", "book": book, "run_id": run_id, "status": "precontract_snapshot_waiver", "dependency_job_id": dependency, "dependency_receipt_path": core.repo_relative(receipt, root), "dependency_receipt_sha256": core.digest_file(receipt), "precontract_waiver_reason": "Genesis_Exodus_Leviticus_are_explicit_precontract_candidate_snapshots_and_Numbers_is_first_native_replay", "non_authorizing": True}
    if "resolved-from-prior" in str(declared):
        raise core.ReplayEvidenceError("QF-01-PLAN-NOT-RUN", f"dependency digest unresolved for {book}")
    candidates = sorted((model_root / "receipts").glob(f"*_completion_v3.*.json"))
    matches = [path for path in candidates if core.digest_file(path) == declared]
    if len(matches) != 1:
        raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", f"dependency terminal receipt not found for {book}")
    terminal = core.load_json(matches[0])
    if terminal.get("candidate_only") is not True or terminal.get("promotion_authorized") is not False:
        raise core.ReplayEvidenceError("QF-10-AUTHORITY-SMUGGLING", "dependency receipt authority")
    return {"schema_version": "whole_bible_dependency_evidence.v1", "book": book, "run_id": run_id, "status": "terminal_predecessor", "dependency_job_id": dependency, "dependency_receipt_path": core.repo_relative(matches[0], root), "dependency_receipt_sha256": declared, "precontract_waiver_reason": None, "non_authorizing": True}


def build_b00(*, book: str, run_id: str, attempt_id: str, campaign_path: Path = core.DEFAULT_CAMPAIGN, model_root: Path = core.DEFAULT_MODEL_ROOT, root: Path = core.ROOT) -> Path:
    core.validate_authoritative_runtime_paths(campaign_path=campaign_path, model_root=model_root, root=root)
    if not core.SAFE_ID.fullmatch(run_id) or not core.SAFE_ID.fullmatch(attempt_id):
        raise core.ReplayEvidenceError("QF-SCHEMA", "unsafe B00 run/attempt identity")
    campaign = core.load_json(campaign_path)
    job = core.campaign_job(campaign, book)
    execution = campaign.get("execution") or {}
    if execution.get("mode") != "specification_only" or execution.get("launch_command") != "not-authorized" or execution.get("auto_advance_requires_qualification_receipt") is not True:
        raise core.ReplayEvidenceError("QF-14-QUALIFIED-BY-LABEL", "campaign qualification boundary changed")
    input_hashes: dict[str, str] = {}
    sibling_prefix = ".ai/scratch/multi_model_bible_chunking/"
    m7_prefix = core.repo_relative(model_root, root).rstrip("/") + "/"
    for relative in job.get("inputs") or []:
        path = core.resolve_repo_path(relative, root)
        if not path.is_file():
            raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", f"missing pinned input: {relative}")
        normalized = core.repo_relative(path, root)
        if normalized.startswith(sibling_prefix) and not normalized.startswith(m7_prefix):
            raise core.ReplayEvidenceError("QF-08-SIBLING-CONTAMINATION", normalized)
        core.validate_input_path_authority(normalized, model_prefix=m7_prefix)
        input_hashes[normalized] = core.digest_file(path)
        declared = (job.get("input_digests") or {}).get(relative)
        if relative == core.repo_relative(campaign_path, root):
            if declared != "stage_receipt:B00.input_artifact_sha256.campaign":
                raise core.ReplayEvidenceError("QF-11-HASH-CYCLE", "campaign self-digest marker changed")
        elif declared != input_hashes[normalized]:
            raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", f"stale pinned input digest: {relative}")
    source_route = job.get("source_route") or {}
    source_hashes = {relative: input_hashes[relative] for relative in source_route.get("manifest_paths") or []}
    if set(source_hashes) != set(source_route.get("manifest_paths") or []):
        raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", "source route manifests are not fully pinned")
    dependency = dependency_evidence(campaign=campaign, job=job, book=book, run_id=run_id, model_root=model_root, root=root)
    directory = core.run_dir(model_root, book, run_id)
    preflight_dir = directory / "preflight"
    projection_path = preflight_dir / "campaign_projection.json"
    dependency_path = preflight_dir / "dependency_evidence.json"
    report_path = preflight_dir / "preflight_report.json"
    projection = {
        "schema_version": "whole_bible_campaign_projection.v1", "campaign_id": campaign["campaign_id"], "campaign_revision": campaign["revision"], "campaign_path": core.repo_relative(campaign_path, root), "campaign_sha256": core.digest_file(campaign_path),
        "book": book, "run_id": run_id, "job_id": job["id"], "job_projection_sha256": core.digest_bytes(core.canonical_bytes(job)), "input_sha256": input_hashes, "source_manifest_sha256": source_hashes,
        "sibling_map_exclusion_verified": True, "campaign_projection_algorithm": "exact_campaign_bytes_and_canonical_job_projection", "contains_scripture_text": False, "contains_source_rows": False, "non_authorizing": True,
    }
    report = {
        "schema_version": "whole_bible_B00_preflight_report.v1", "book": book, "run_id": run_id, "campaign_projection_sha256": core.digest_bytes(core.canonical_bytes(projection)), "source_digests_pinned": True,
        "sibling_map_exclusion_verified": True, "dependency_status": dependency["status"], "static_specification_valid_only": True, "replay_qualified": False, "launch_qualified": False, "non_authorizing": True,
    }
    with core.exclusive_lock(model_root / "state"):
        core.atomic_write(projection_path, core.canonical_bytes(projection), immutable=True)
        core.atomic_write(dependency_path, core.canonical_bytes(dependency), immutable=True)
        core.atomic_write(report_path, core.canonical_bytes(report), immutable=True)
    input_manifest = {
        "schema_version": "whole_bible_artifact_manifest.v1", "manifest_id": f"{campaign['campaign_id']}:{book}:{run_id}:B00:input", "book": book, "run_id": run_id, "stage_id": "B00", "direction": "input",
        "artifacts": [artifact_row("workflow", core.WORKFLOW, root=root, scope="governance_input"), artifact_row("prompt_pack", core.PROMPTS, root=root, scope="governance_input"), artifact_row("runtime_adapter", core.ADAPTER, root=root, scope="governance_input")],
        "contains_scripture_text": False, "contains_source_rows": False, "contains_prompts_or_hidden_reasoning": False, "non_authorizing": True,
    }
    output_manifest = {
        "schema_version": "whole_bible_artifact_manifest.v1", "manifest_id": f"{campaign['campaign_id']}:{book}:{run_id}:B00:output", "book": book, "run_id": run_id, "stage_id": "B00", "direction": "output",
        "artifacts": [artifact_row("campaign_projection", projection_path, root=root, scope="validator_evidence"), artifact_row("preflight_report", report_path, root=root, scope="validator_evidence"), artifact_row("dependency_evidence", dependency_path, root=root, scope="validator_evidence")],
        "contains_scripture_text": False, "contains_source_rows": False, "contains_prompts_or_hidden_reasoning": False, "non_authorizing": True,
    }
    manifests = directory / "manifests"
    input_manifest_path = manifests / "B00.input.json"
    output_manifest_path = manifests / "B00.output.json"
    with core.exclusive_lock(model_root / "state"):
        core.atomic_write(input_manifest_path, core.canonical_bytes(input_manifest), immutable=True)
        core.atomic_write(output_manifest_path, core.canonical_bytes(output_manifest), immutable=True)
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    draft = {
        "schema_version": "whole_bible_stage_receipt_draft.v1", "book": book, "run_id": run_id, "stage_id": "B00", "attempt_id": attempt_id, "attempt_kind": "original", "role_or_deterministic_gate": "authoritative_B00_preflight_builder", "executor_kind": "deterministic",
        "started_at": now, "finished_at": now, "outcome": "succeeded", "unresolved_holds": [], "input_manifest_path": core.repo_relative(input_manifest_path, root), "output_manifest_path": core.repo_relative(output_manifest_path, root),
        "stage_evidence": {"artifact_refs": {"campaign_projection": "campaign_projection", "workflow": "workflow", "prompt_pack": "prompt_pack", "runtime_adapter": "runtime_adapter", "preflight_report": "preflight_report", "dependency_evidence": "dependency_evidence"}, "values": {"sibling_map_exclusion_verified": True, "source_digests_pinned": True, "campaign_projection_algorithm": "exact_campaign_bytes_and_canonical_job_projection"}},
        "independence_scope": {"authoring_independent_from_sibling_maps": True, "artifact_blindness": False, "role_separation": False, "shared_model_substrate": True, "runtime_model_identity_attested": False, "independent_model_or_provider_evidence": False, "counts_as_cross_model_independent_vote": False, "convergence_weight": "one_model_voice"},
        "non_authorizing": True,
    }
    draft_path = directory / "drafts" / f"B00.{attempt_id}.json"
    with core.exclusive_lock(model_root / "state"):
        core.atomic_write(draft_path, core.canonical_bytes(draft), immutable=True)
    return stage_writer.write_receipt(draft_path=draft_path, campaign_path=campaign_path, model_root=model_root, root=root)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--attempt-id", required=True)
    args = parser.parse_args(argv)
    try:
        output = build_b00(book=args.book, run_id=args.run_id, attempt_id=args.attempt_id)
    except core.ReplayEvidenceError as exc:
        print(f"B00 preflight failed: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote authoritative B00 receipt: {core.repo_relative(output)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())