#!/usr/bin/env python3
"""Write one immutable B00-B10 attempt receipt and update derived indexes."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scripts import whole_bible_replay_evidence as core

DRAFT_REQUIRED = {
    "schema_version", "book", "run_id", "stage_id", "attempt_id", "attempt_kind",
    "role_or_deterministic_gate", "executor_kind", "started_at", "finished_at",
    "outcome", "unresolved_holds", "input_manifest_path", "output_manifest_path",
    "stage_evidence", "independence_scope", "non_authorizing",
}


def write_receipt(*, draft_path: Path, campaign_path: Path = core.DEFAULT_CAMPAIGN, model_root: Path = core.DEFAULT_MODEL_ROOT, root: Path = core.ROOT, allow_test_roots: bool = False) -> Path:
    core.validate_authoritative_runtime_paths(campaign_path=campaign_path, model_root=model_root, root=root, allow_test_roots=allow_test_roots)
    draft = core.load_json(draft_path)
    if not DRAFT_REQUIRED.issubset(draft) or set(draft) - DRAFT_REQUIRED - {"failure_fingerprint"}:
        raise core.ReplayEvidenceError("QF-SCHEMA", f"{core.repo_relative(draft_path, root)}: draft fields")
    if draft["schema_version"] != "whole_bible_stage_receipt_draft.v1" or draft["non_authorizing"] is not True:
        raise core.ReplayEvidenceError("QF-10-AUTHORITY-SMUGGLING", "draft schema/authority")
    book, run_id, stage_id, attempt_id = (draft[key] for key in ("book", "run_id", "stage_id", "attempt_id"))
    if stage_id not in core.STAGES or not core.SAFE_ID.fullmatch(run_id) or not core.SAFE_ID.fullmatch(attempt_id):
        raise core.ReplayEvidenceError("QF-SCHEMA", "unsafe run/stage/attempt identity")
    campaign = core.load_json(campaign_path); job = core.campaign_job(campaign, book); plan = core.stage_plan(job, stage_id)
    prompt_binding = plan.get("prompt_template_ids") or ["deterministic"]
    input_path = core.resolve_repo_path(draft["input_manifest_path"], root)
    output_path = core.resolve_repo_path(draft["output_manifest_path"], root)
    _, input_hashes, input_ids = core.validate_artifact_manifest(input_path, root=root, model_root=model_root, book=book, run_id=run_id, stage_id=stage_id, direction="input", job=job)
    _, output_hashes, output_ids = core.validate_artifact_manifest(output_path, root=root, model_root=model_root, book=book, run_id=run_id, stage_id=stage_id, direction="output", job=job)
    if set(input_ids) & set(output_ids): raise core.ReplayEvidenceError("QF-SCHEMA", "artifact IDs duplicated across manifests")
    evidence = draft["stage_evidence"]
    if not isinstance(evidence, dict) or set(evidence) != {"artifact_refs", "values"} or not isinstance(evidence["artifact_refs"], dict) or not isinstance(evidence["values"], dict):
        raise core.ReplayEvidenceError("QF-SCHEMA", "draft stage evidence shape")
    ids = {**input_ids, **output_ids}; hashes = {**input_hashes, **output_hashes}
    stage_evidence = {"artifact_refs": evidence["artifact_refs"], "artifact_sha256": core.derive_stage_hashes(evidence["artifact_refs"], ids, hashes), "values": evidence["values"]}
    directory = core.run_dir(model_root, book, run_id); state_root = model_root / "state"
    with core.exclusive_lock(state_root):
        index = core.read_index(directory, campaign, book, run_id); number = core.STAGES.index(stage_id)
        previous = core.STAGES[number - 1] if number else None
        if previous:
            prior_ref = index["selected"].get(previous)
            if not isinstance(prior_ref, dict): raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", f"{stage_id}: {previous} missing")
            prior_path = core.resolve_repo_path(prior_ref["path"], root)
            if not prior_path.is_file() or core.digest_file(prior_path) != prior_ref.get("sha256"): raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", f"{stage_id}: stale prior")
            if core.load_json(prior_path).get("outcome") not in core.SUCCESS_OUTCOMES: raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", f"{stage_id}: prior failed")
            prior_digest, prior_relative = prior_ref["sha256"], prior_ref["path"]
        else: prior_digest, prior_relative = None, None
        core_hashes = {
            "workflow_sha256": core.digest_file(core.WORKFLOW), "prompt_pack_sha256": core.digest_file(core.PROMPTS),
            "runtime_adapter_sha256": core.digest_file(core.ADAPTER), "input_manifest_sha256": core.digest_file(input_path),
            "output_manifest_sha256": core.digest_file(output_path),
        }
        state_fingerprint = core.digest_bytes(core.canonical_bytes({"book": book, "run_id": run_id, "stage_id": stage_id, "prompt_binding": prompt_binding, "prior": prior_digest, "core_hashes": core_hashes, "stage_evidence": stage_evidence}))
        stage_directory = directory / "stages" / stage_id
        if stage_directory.exists():
            for existing_path in stage_directory.glob("*.json"):
                existing = core.load_json(existing_path)
                if existing.get("outcome") in {"failed", "blocked_human"} and existing.get("state_fingerprint") == state_fingerprint:
                    raise core.ReplayEvidenceError("QF-12-SAME-STATE-RETRY", stage_id)
        receipt = {
            "schema_version": "whole_bible_stage_receipt.v1", "receipt_id": f"{campaign['campaign_id']}:{book}:{run_id}:{stage_id}:{attempt_id}",
            "campaign_id": campaign["campaign_id"], "campaign_revision": campaign["revision"], "book": book, "run_id": run_id,
            "stage_id": stage_id, "attempt_id": attempt_id, "attempt_kind": draft["attempt_kind"],
            "role_or_deterministic_gate": draft["role_or_deterministic_gate"], "executor_kind": draft["executor_kind"],
            "prompt_template_id_or_deterministic": prompt_binding, **core_hashes,
            "input_manifest_path": core.repo_relative(input_path, root), "output_manifest_path": core.repo_relative(output_path, root),
            "input_artifact_sha256": input_hashes, "output_artifact_sha256": output_hashes,
            "prior_stage_receipt_sha256": prior_digest, "prior_stage_receipt_path": prior_relative,
            "started_at": draft["started_at"], "finished_at": draft["finished_at"], "outcome": draft["outcome"],
            "unresolved_holds": draft["unresolved_holds"], "stage_evidence": stage_evidence, "independence_scope": draft["independence_scope"],
            "shared_model_substrate": draft["independence_scope"]["shared_model_substrate"],
            "counts_as_cross_model_independent_vote": draft["independence_scope"]["counts_as_cross_model_independent_vote"],
            "state_fingerprint": state_fingerprint, "non_authorizing": True,
        }
        if draft.get("failure_fingerprint") is not None: receipt["failure_fingerprint"] = draft["failure_fingerprint"]
        core.validate_schema(receipt, core.STAGE_SCHEMA, "stage receipt"); core.validate_stage_semantics(receipt); core.validate_stage_artifact_content(receipt, ids, root=root); core.validate_boss_phase_pair(receipt, ids, hashes, root)
        receipt_path = stage_directory / f"{attempt_id}.json"; payload = core.canonical_bytes(receipt)
        core.atomic_write(receipt_path, payload, immutable=True); receipt_digest = core.digest_bytes(payload)
        selected = {key: value for key, value in index["selected"].items() if key in core.STAGES and core.STAGES.index(key) < number}
        selected[stage_id] = {"attempt_id": attempt_id, "path": core.repo_relative(receipt_path, root), "sha256": receipt_digest}
        index["selected"] = selected; core.atomic_write(directory / "run_index.json", core.canonical_bytes(index))
        log_entry = {"schema_version": "whole_bible_stage_receipt_log.v1", "campaign_id": campaign["campaign_id"], "book": book, "run_id": run_id, "stage_id": stage_id, "attempt_id": attempt_id, "receipt_path": core.repo_relative(receipt_path, root), "receipt_sha256": receipt_digest, "outcome": receipt["outcome"], "non_authorizing": True}
        core.append_receipt_log(directory / "receipts.jsonl", log_entry); core.append_receipt_log(state_root / "receipts.jsonl", log_entry)
    return receipt_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--draft", type=Path, required=True); parser.add_argument("--campaign", type=Path, default=core.DEFAULT_CAMPAIGN); parser.add_argument("--model-root", type=Path, default=core.DEFAULT_MODEL_ROOT); args = parser.parse_args(argv)
    try: path = write_receipt(draft_path=args.draft, campaign_path=args.campaign, model_root=args.model_root)
    except core.ReplayEvidenceError as exc: print(f"Stage receipt write failed: {exc}", file=sys.stderr); return 1
    print(f"Wrote immutable stage receipt: {core.repo_relative(path)}"); return 0

if __name__ == "__main__": raise SystemExit(main())
