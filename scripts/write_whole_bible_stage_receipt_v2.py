#!/usr/bin/env python3
"""Prepare or commit an immutable revision-7 B00/B01 stage receipt."""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from scripts import whole_bible_replay_evidence_v2 as core

DRAFT_REQUIRED = {
    "schema_version", "book", "run_id", "stage_id", "attempt_id", "attempt_kind",
    "role_or_deterministic_gate", "executor_kind", "started_at", "finished_at",
    "outcome", "unresolved_holds", "input_manifest_path", "output_manifest_path",
    "stage_evidence", "independence_scope", "non_authorizing",
}


def _prior(index: dict[str, Any], stage_id: str, *, root: Path) -> tuple[str | None, str | None]:
    if stage_id == "B00":
        return None, None
    prior = index["selected"].get("B00")
    if not isinstance(prior, dict):
        raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", "B01 requires selected B00")
    path = core.resolve_repo_path(prior["path"], root)
    if not path.is_file() or core.digest_file(path) != prior.get("sha256"):
        raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", "selected B00 is stale")
    return prior["sha256"], prior["path"]


def _build_candidate(*, draft_path: Path, campaign_path: Path, registry_path: Path,
                     model_root: Path, root: Path, allow_test_roots: bool = False,
                     allow_selected_validation: bool = False) -> tuple[dict[str, Any], dict[str, Any], Path]:
    core.validate_runtime_contract(campaign_path=campaign_path, registry_path=registry_path, root=root, model_root=model_root, allow_test_roots=allow_test_roots)
    draft = core.load_json(draft_path)
    if set(draft) != DRAFT_REQUIRED or draft.get("schema_version") != "whole_bible_stage_receipt_draft.v2" or draft.get("non_authorizing") is not True:
        raise core.ReplayEvidenceError("QF-SCHEMA", "v2 stage draft shape")
    book, run_id, stage_id, attempt_id = (draft[key] for key in ("book", "run_id", "stage_id", "attempt_id"))
    if stage_id not in core.AUTHORIZED_STAGES:
        raise core.ReplayEvidenceError("QF-21-UNMIGRATED-STAGE", "revision 7 authorizes B00 only; B01 remains a candidate design")
    campaign = core.load_json(campaign_path)
    if campaign.get("revision") != 7:
        raise core.ReplayEvidenceError("QF-13-ADAPTER-SPLIT", "v2 writer requires campaign revision 7")
    job = core.campaign_job(campaign, book)
    plan = core.stage_plan(job, stage_id)
    input_path = core.resolve_repo_path(draft["input_manifest_path"], root)
    output_path = core.resolve_repo_path(draft["output_manifest_path"], root)
    base = core.validate_attempt_bundle_paths(draft_path=draft_path, input_manifest_path=input_path, output_manifest_path=output_path, model_root=model_root, book=book, run_id=run_id, stage_id=stage_id, attempt_id=attempt_id)
    _, input_hashes, input_ids = core.validate_artifact_manifest(input_path, root=root, model_root=model_root, job=job, book=book, run_id=run_id, stage_id=stage_id, attempt_id=attempt_id, direction="input")
    _, output_hashes, output_ids = core.validate_artifact_manifest(output_path, root=root, model_root=model_root, job=job, book=book, run_id=run_id, stage_id=stage_id, attempt_id=attempt_id, direction="output")
    if set(input_ids) & set(output_ids):
        raise core.ReplayEvidenceError("QF-SCHEMA", "artifact IDs duplicated across v2 manifests")
    if set(input_hashes) & set(output_hashes):
        raise core.ReplayEvidenceError("QF-SCHEMA", "physical artifact path appears in both input and output manifests")
    evidence = draft["stage_evidence"]
    if not isinstance(evidence, dict) or set(evidence) != {"artifact_refs", "values"}:
        raise core.ReplayEvidenceError("QF-SCHEMA", "v2 stage evidence shape")
    ids = {**input_ids, **output_ids}
    hashes = {**input_hashes, **output_hashes}
    stage_evidence = {
        "artifact_refs": evidence["artifact_refs"],
        "artifact_sha256": core.v1.derive_stage_hashes(evidence["artifact_refs"], ids, hashes),
        "values": evidence["values"],
    }
    directory = core.run_dir(model_root, book, run_id)
    index = core.read_index(directory, campaign, book, run_id)
    if stage_id in index["selected"] and not allow_selected_validation:
        raise core.ReplayEvidenceError("QF-12-IMMUTABLE-ATTEMPT", f"successful {stage_id} is already selected; use a fresh run")
    prior_sha, prior_path = _prior(index, stage_id, root=root)
    prompt_binding = plan.get("prompt_template_ids") or ["deterministic"]
    core_hashes = {
        "workflow_sha256": core.digest_file(core.WORKFLOW),
        "prompt_pack_sha256": core.digest_file(core.PROMPTS),
        "runtime_adapter_sha256": core.digest_file(core.ADAPTER),
        "input_manifest_sha256": core.digest_file(input_path),
        "output_manifest_sha256": core.digest_file(output_path),
    }
    state_fingerprint = core.digest_bytes(core.canonical_bytes({
        "book": book, "run_id": run_id, "stage_id": stage_id, "attempt_id": attempt_id,
        "prompt_binding": prompt_binding, "prior": prior_sha, "core_hashes": core_hashes,
        "stage_evidence": stage_evidence,
    }))
    receipt = {
        "schema_version": "whole_bible_stage_receipt.v2",
        "receipt_id": f"{campaign['campaign_id']}:{book}:{run_id}:{stage_id}:{attempt_id}",
        "campaign_id": campaign["campaign_id"], "campaign_revision": campaign["revision"],
        "book": book, "run_id": run_id, "stage_id": stage_id, "attempt_id": attempt_id,
        "attempt_kind": draft["attempt_kind"], "role_or_deterministic_gate": draft["role_or_deterministic_gate"],
        "executor_kind": draft["executor_kind"], "prompt_template_id_or_deterministic": prompt_binding,
        **core_hashes,
        "input_manifest_path": core.repo_relative(input_path, root),
        "output_manifest_path": core.repo_relative(output_path, root),
        "input_artifact_sha256": input_hashes, "output_artifact_sha256": output_hashes,
        "prior_stage_receipt_sha256": prior_sha, "prior_stage_receipt_path": prior_path,
        "started_at": draft["started_at"], "finished_at": draft["finished_at"],
        "outcome": draft["outcome"], "unresolved_holds": draft["unresolved_holds"],
        "stage_evidence": stage_evidence, "independence_scope": draft["independence_scope"],
        "shared_model_substrate": draft["independence_scope"]["shared_model_substrate"],
        "counts_as_cross_model_independent_vote": draft["independence_scope"]["counts_as_cross_model_independent_vote"],
        "state_fingerprint": state_fingerprint, "non_authorizing": True,
    }
    core.validate_schema(receipt, core.STAGE_SCHEMA, "v2 stage receipt")
    core.validate_stage_semantics(receipt)
    if stage_id == "B00":
        core.validate_b00_artifact_content(receipt=receipt, ids=ids, campaign_path=campaign_path, registry_path=registry_path, root=root)
    else:
        core.validate_b01_artifact_content(receipt=receipt, ids=ids, input_ids=set(input_ids), output_ids=set(output_ids), root=root)
    return receipt, index, base


def prepare_stage_receipt(*, draft_path: Path, campaign_path: Path = core.CAMPAIGN,
                          registry_path: Path = core.REGISTRY, model_root: Path = core.MODEL_ROOT,
                          root: Path = core.ROOT, allow_test_roots: bool = False) -> Path:
    receipt, _, base = _build_candidate(draft_path=draft_path, campaign_path=campaign_path, registry_path=registry_path, model_root=model_root, root=root, allow_test_roots=allow_test_roots)
    prepared_path = base / "prepared_commit.json"
    prepared = {
        "schema_version": "whole_bible_prepared_stage_commit.v1", "book": receipt["book"],
        "run_id": receipt["run_id"], "stage_id": receipt["stage_id"], "attempt_id": receipt["attempt_id"],
        "campaign_path": core.repo_relative(campaign_path, root), "campaign_sha256": core.digest_file(campaign_path),
        "draft_path": core.repo_relative(draft_path, root), "draft_sha256": core.digest_file(draft_path),
        "input_manifest_path": receipt["input_manifest_path"], "input_manifest_sha256": receipt["input_manifest_sha256"],
        "output_manifest_path": receipt["output_manifest_path"], "output_manifest_sha256": receipt["output_manifest_sha256"],
        "prior_stage_receipt_path": receipt["prior_stage_receipt_path"], "prior_stage_receipt_sha256": receipt["prior_stage_receipt_sha256"],
        "candidate_receipt": receipt, "candidate_receipt_sha256": core.digest_bytes(core.canonical_bytes(receipt)),
        "prepared_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"), "non_authorizing": True,
    }
    core.validate_schema(prepared, core.PREPARED_SCHEMA, "prepared stage commit")
    core.atomic_write(prepared_path, core.canonical_bytes(prepared), immutable=True)
    return prepared_path


def commit_prepared_stage_receipt(*, prepared_path: Path, campaign_path: Path = core.CAMPAIGN,
                                  registry_path: Path = core.REGISTRY, model_root: Path = core.MODEL_ROOT,
                                  root: Path = core.ROOT, allow_test_roots: bool = False) -> Path:
    prepared = core.load_json(prepared_path)
    core.validate_schema(prepared, core.PREPARED_SCHEMA, "prepared stage commit")
    if prepared.get("campaign_path") != core.repo_relative(campaign_path, root) or prepared.get("campaign_sha256") != core.digest_file(campaign_path):
        raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", "prepared campaign drift")
    draft_path = core.resolve_repo_path(prepared["draft_path"], root)
    if core.digest_file(draft_path) != prepared["draft_sha256"]:
        raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", "prepared draft drift")
    receipt, _, base = _build_candidate(draft_path=draft_path, campaign_path=campaign_path, registry_path=registry_path, model_root=model_root, root=root, allow_test_roots=allow_test_roots, allow_selected_validation=True)
    if prepared_path.resolve() != (base / "prepared_commit.json").resolve() or receipt != prepared["candidate_receipt"] or core.digest_bytes(core.canonical_bytes(receipt)) != prepared["candidate_receipt_sha256"]:
        raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", "prepared candidate changed")
    directory = core.run_dir(model_root, receipt["book"], receipt["run_id"])
    state_root = model_root / "state"
    with core.exclusive_lock(state_root):
        locked_receipt, _, locked_base = _build_candidate(
            draft_path=draft_path, campaign_path=campaign_path, registry_path=registry_path,
            model_root=model_root, root=root, allow_test_roots=allow_test_roots,
            allow_selected_validation=True,
        )
        if locked_base.resolve() != base.resolve() or locked_receipt != prepared["candidate_receipt"] or core.digest_bytes(core.canonical_bytes(locked_receipt)) != prepared["candidate_receipt_sha256"]:
            raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", "candidate changed during commit lock revalidation")
        receipt = locked_receipt
        campaign = core.load_json(campaign_path)
        index = core.read_index(directory, campaign, receipt["book"], receipt["run_id"])
        prior_sha, prior_path = _prior(index, receipt["stage_id"], root=root)
        if (prior_sha, prior_path) != (receipt["prior_stage_receipt_sha256"], receipt["prior_stage_receipt_path"]):
            raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", "predecessor changed after prepare")
        receipt_path = directory / "stages" / receipt["stage_id"] / f"{receipt['attempt_id']}.json"
        receipt_relative = core.repo_relative(receipt_path, root)
        payload = core.canonical_bytes(receipt)
        receipt_sha = core.digest_bytes(payload)
        expected_ref = {"attempt_id": receipt["attempt_id"], "path": receipt_relative, "sha256": receipt_sha}
        log = {"schema_version": "whole_bible_stage_receipt_log.v2", "campaign_id": campaign["campaign_id"], "book": receipt["book"], "run_id": receipt["run_id"], "stage_id": receipt["stage_id"], "attempt_id": receipt["attempt_id"], "receipt_path": receipt_relative, "receipt_sha256": receipt_sha, "outcome": receipt["outcome"], "non_authorizing": True}
        core.validate_v2_log_entry(log)
        selected = index["selected"].get(receipt["stage_id"])
        if selected is not None:
            if selected != expected_ref or not receipt_path.is_file() or receipt_path.read_bytes() != payload:
                raise core.ReplayEvidenceError("QF-12-IMMUTABLE-ATTEMPT", "selected stage conflicts with exact prepared candidate")
        else:
            core.atomic_write(receipt_path, payload, immutable=True)
            index["selected"][receipt["stage_id"]] = expected_ref
            core.atomic_write(directory / "run_index.json", core.canonical_bytes(index))
        core.ensure_v2_receipt_log(directory / "receipts.v2.jsonl", log, root=root)
        core.ensure_v2_receipt_log(state_root / "receipts.v2.jsonl", log, root=root)
    return receipt_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--prepare-draft", type=Path)
    mode.add_argument("--commit-prepared", type=Path)
    args = parser.parse_args(argv)
    try:
        path = prepare_stage_receipt(draft_path=args.prepare_draft) if args.prepare_draft else commit_prepared_stage_receipt(prepared_path=args.commit_prepared)
    except core.ReplayEvidenceError as exc:
        print(f"V2 stage receipt operation failed: {exc}", file=sys.stderr)
        return 1
    print(core.repo_relative(path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
