#!/usr/bin/env python3
"""Validate a materialized immutable B00-B10 receipt chain.

A passing result proves receipt plumbing only. It never proves independent launch
review, whole-Bible form/language qualification, promotion, or authority.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from scripts import whole_bible_replay_evidence as core


def validate_run(*, book: str, run_id: str, require_complete: bool, require_through: str | None = None, require_terminal: bool = False, campaign_path: Path = core.DEFAULT_CAMPAIGN, model_root: Path = core.DEFAULT_MODEL_ROOT, root: Path = core.ROOT, allow_test_roots: bool = False) -> dict[str, Any]:
    core.validate_authoritative_runtime_paths(campaign_path=campaign_path, model_root=model_root, root=root, allow_test_roots=allow_test_roots)
    campaign = core.load_json(campaign_path); job = core.campaign_job(campaign, book); directory = core.run_dir(model_root, book, run_id)
    index_path = directory / "run_index.json"
    if not index_path.is_file(): raise core.ReplayEvidenceError("QF-01-PLAN-NOT-RUN", f"no materialized run index for {book}/{run_id}")
    index = core.read_index(directory, campaign, book, run_id); selected = index["selected"]; observed: list[str] = []; prior: str | None = None; prior_path_ref: str | None = None
    for stage_id in core.STAGES:
        ref = selected.get(stage_id)
        if ref is None: break
        if stage_id != core.STAGES[len(observed)]: raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", f"gap before {stage_id}")
        path = core.resolve_repo_path(ref.get("path"), root)
        expected_path = directory / "stages" / stage_id / f"{ref.get('attempt_id')}.json"
        if path.resolve() != expected_path.resolve():
            raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", f"selected path substitution at {stage_id}")
        if not path.is_file() or core.digest_file(path) != ref.get("sha256"): raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", f"stale selected {stage_id}")
        receipt = core.load_json(path); core.validate_schema(receipt, core.STAGE_SCHEMA, stage_id); core.validate_stage_semantics(receipt)
        identity = (receipt["book"], receipt["run_id"], receipt["stage_id"], receipt["attempt_id"])
        if (
            identity != (book, run_id, stage_id, ref.get("attempt_id"))
            or receipt["prior_stage_receipt_sha256"] != prior
            or receipt["prior_stage_receipt_path"] != prior_path_ref
        ):
            raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", f"identity/predecessor {stage_id}")
        all_ids: dict[str, str] = {}; all_hashes: dict[str, str] = {}
        for manifest_key, digest_key, direction in (("input_manifest_path", "input_manifest_sha256", "input"), ("output_manifest_path", "output_manifest_sha256", "output")):
            manifest_path = core.resolve_repo_path(receipt[manifest_key], root)
            if not manifest_path.is_file() or core.digest_file(manifest_path) != receipt[digest_key]: raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", f"stale {stage_id} {direction} manifest")
            manifest, hashes, ids = core.validate_artifact_manifest(manifest_path, root=root, model_root=model_root, book=book, run_id=run_id, stage_id=stage_id, direction=direction, job=job)
            if receipt[f"{direction}_artifact_sha256"] != hashes: raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", f"stale {stage_id} {direction} map")
            all_hashes.update(hashes); all_ids.update(ids)
        projected = core.derive_stage_hashes(receipt["stage_evidence"]["artifact_refs"], all_ids, all_hashes)
        if projected != receipt["stage_evidence"]["artifact_sha256"]: raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", f"stale {stage_id} evidence projection")
        core.validate_stage_artifact_content(receipt, all_ids, root=root)
        core.validate_boss_phase_pair(receipt, all_ids, all_hashes, root)
        if receipt["workflow_sha256"] != core.digest_file(core.WORKFLOW) or receipt["prompt_pack_sha256"] != core.digest_file(core.PROMPTS) or receipt["runtime_adapter_sha256"] != core.digest_file(core.ADAPTER):
            raise core.ReplayEvidenceError("QF-13-ADAPTER-SPLIT", f"stale core/adapter at {stage_id}")
        observed.append(stage_id); prior = ref["sha256"]; prior_path_ref = ref["path"]
        if receipt["outcome"] not in core.SUCCESS_OUTCOMES: break
    if set(selected) - set(observed): raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", "downstream selected after gap/failure")
    if require_complete and observed != list(core.STAGES): raise core.ReplayEvidenceError("QF-01-PLAN-NOT-RUN", f"first missing/invalid {core.STAGES[len(observed)]}")
    if require_through is not None:
        required_prefix = list(core.STAGES[: core.STAGES.index(require_through) + 1])
        if observed[: len(required_prefix)] != required_prefix: raise core.ReplayEvidenceError("QF-01-PLAN-NOT-RUN", f"required through {require_through}; observed {observed}")
    if "B10" in observed:
        manifest_path = directory / "extended_evidence_manifest.precompletion.json"
        if not manifest_path.is_file(): raise core.ReplayEvidenceError("QF-11-HASH-CYCLE", "missing precompletion manifest")
        manifest = core.load_json(manifest_path); core.validate_schema(manifest, core.EXTENDED_SCHEMA, "extended manifest")
        if manifest["book"] != book or manifest["run_id"] != run_id or manifest["campaign_revision"] != campaign["revision"]: raise core.ReplayEvidenceError("QF-12-SCOPE-INFLATION", "manifest identity/scope")
        for stage_id, ref in manifest["precompletion_stage_receipts"].items():
            if selected.get(stage_id) != ref: raise core.ReplayEvidenceError("QF-11-HASH-CYCLE", f"manifest stale for {stage_id}")
        for records in manifest["artifact_sets"].values():
            for row in records:
                path = core.resolve_repo_path(row["path"], root)
                if not path.is_file() or core.digest_file(path) != row["sha256"]: raise core.ReplayEvidenceError("QF-11-HASH-CYCLE", f"stale extended artifact {row['path']}")
        b10 = core.load_json(core.resolve_repo_path(selected["B10"]["path"], root)); manifest_hash = core.digest_file(manifest_path)
        if b10["stage_evidence"]["artifact_sha256"].get("extended_evidence_manifest") != manifest_hash: raise core.ReplayEvidenceError("QF-11-HASH-CYCLE", "B10 does not bind manifest")
        if manifest_hash in {ref["sha256"] for ref in manifest["precompletion_stage_receipts"].values()}: raise core.ReplayEvidenceError("QF-11-HASH-CYCLE", "manifest/receipt digest cycle")
    terminal_valid = False
    if require_terminal:
        terminal_path = model_root / "receipts" / f"{book}_completion_v3.{run_id}.json"
        if not terminal_path.is_file(): raise core.ReplayEvidenceError("QF-01-PLAN-NOT-RUN", "terminal completion receipt missing")
        terminal = core.load_json(terminal_path); core.validate_schema(terminal, core.TERMINAL_SCHEMA, "terminal completion receipt")
        if terminal["book"] != book or terminal["run_id"] != run_id or terminal["campaign_revision"] != campaign["revision"]: raise core.ReplayEvidenceError("QF-12-SCOPE-INFLATION", "terminal identity")
        for path_key, hash_key in (("b10_stage_receipt_path", "b10_stage_receipt_sha256"), ("extended_evidence_manifest_path", "extended_evidence_manifest_sha256"), ("completion_gate_bundle_path", "completion_gate_bundle_sha256")):
            bound = core.resolve_repo_path(terminal[path_key], root)
            if not bound.is_file() or core.digest_file(bound) != terminal[hash_key]: raise core.ReplayEvidenceError("QF-11-HASH-CYCLE", f"terminal stale {path_key}")
        for relative, expected in terminal["final_artifact_closure"].items():
            bound = core.resolve_repo_path(relative, root)
            if not bound.is_file() or core.digest_file(bound) != expected: raise core.ReplayEvidenceError("QF-11-HASH-CYCLE", f"terminal stale closure {relative}")
        core.validate_completion_gate_bundle(core.resolve_repo_path(terminal["completion_gate_bundle_path"], root), book=book, run_id=run_id, root=root)
        if terminal["b10_stage_receipt_sha256"] != selected["B10"]["sha256"]: raise core.ReplayEvidenceError("QF-11-HASH-CYCLE", "terminal B10 selection stale")
        terminal_valid = True
    return {
        "validation_scope": "materialized_B00_B10_receipt_plumbing_only", "spec_valid": True,
        "book": book, "run_id": run_id, "selected_stages": observed,
        "first_missing_stage": core.STAGES[len(observed)] if len(observed) < len(core.STAGES) else None,
        "b00_b10_chain_valid": observed == list(core.STAGES), "terminal_completion_valid": terminal_valid, "replay_qualified": False,
        "launch_qualified": False, "whole_bible_form_language_qualified": False,
        "reason": "terminal completion, dimensional calibration, and independent launch review are separate fail-closed gates",
        "non_authorizing": True,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--book", required=True); parser.add_argument("--run-id", required=True); parser.add_argument("--require-complete", action="store_true"); parser.add_argument("--require-through", choices=core.STAGES); parser.add_argument("--require-terminal", action="store_true"); parser.add_argument("--campaign", type=Path, default=core.DEFAULT_CAMPAIGN); parser.add_argument("--model-root", type=Path, default=core.DEFAULT_MODEL_ROOT); args = parser.parse_args(argv)
    try: result = validate_run(book=args.book, run_id=args.run_id, require_complete=args.require_complete, require_through=args.require_through, require_terminal=args.require_terminal, campaign_path=args.campaign, model_root=args.model_root)
    except core.ReplayEvidenceError as exc: print(f"Materialized replay-chain validation failed: {exc}", file=sys.stderr); return 1
    print(json.dumps(result, indent=2, sort_keys=True)); return 0

if __name__ == "__main__": raise SystemExit(main())
