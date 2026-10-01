#!/usr/bin/env python3
"""Write the terminal, acyclic, candidate-only completion receipt after B10."""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from scripts import whole_bible_replay_evidence as core
from scripts import validate_whole_bible_stage_receipts as chain_validator


def artifact_path_for_id(receipt: dict[str, Any], artifact_id: str, root: Path) -> Path:
    matches: list[str] = []
    for key in ("input_manifest_path", "output_manifest_path"):
        manifest = core.load_json(core.resolve_repo_path(receipt[key], root))
        matches.extend(row["path"] for row in manifest["artifacts"] if row["artifact_id"] == artifact_id)
    if len(matches) != 1: raise core.ReplayEvidenceError("QF-11-HASH-CYCLE", f"B10 needs one {artifact_id}")
    return core.resolve_repo_path(matches[0], root)


def validate_gate_bundle(path: Path, *, book: str, run_id: str, root: Path = core.ROOT) -> list[dict[str, Any]]:
    return core.validate_completion_gate_bundle(path, book=book, run_id=run_id, root=root)


def write_terminal(*, draft_path: Path, campaign_path: Path = core.DEFAULT_CAMPAIGN, model_root: Path = core.DEFAULT_MODEL_ROOT, root: Path = core.ROOT, allow_test_roots: bool = False) -> Path:
    core.validate_authoritative_runtime_paths(campaign_path=campaign_path, model_root=model_root, root=root, allow_test_roots=allow_test_roots)
    draft = core.load_json(draft_path); required = {"schema_version", "book", "run_id", "non_authorizing"}
    if set(draft) != required or draft.get("schema_version") != "whole_bible_terminal_completion_draft.v1" or draft.get("non_authorizing") is not True:
        raise core.ReplayEvidenceError("QF-SCHEMA", "terminal draft")
    book, run_id = draft["book"], draft["run_id"]; campaign = core.load_json(campaign_path); core.campaign_job(campaign, book)
    chain_validator.validate_run(book=book, run_id=run_id, require_complete=True, campaign_path=campaign_path, model_root=model_root, root=root, allow_test_roots=allow_test_roots)
    directory = core.run_dir(model_root, book, run_id); index = core.read_index(directory, campaign, book, run_id); b10_ref = index["selected"]["B10"]
    b07 = core.load_json(core.resolve_repo_path(index["selected"]["B07"]["path"], root))
    b09 = core.load_json(core.resolve_repo_path(index["selected"]["B09"]["path"], root))
    unresolved_holds, unresolved_appeals, outcome = core.derive_terminal_dispositions(b07, b09)
    b10_path = core.resolve_repo_path(b10_ref["path"], root); b10 = core.load_json(b10_path)
    manifest_path = artifact_path_for_id(b10, "extended_evidence_manifest", root); bundle_path = artifact_path_for_id(b10, "completion_gate_bundle", root)
    if b10["stage_evidence"]["artifact_sha256"]["extended_evidence_manifest"] != core.digest_file(manifest_path) or b10["stage_evidence"]["artifact_sha256"]["completion_gate_bundle"] != core.digest_file(bundle_path):
        raise core.ReplayEvidenceError("QF-11-HASH-CYCLE", "B10 artifact binding stale")
    gates = validate_gate_bundle(bundle_path, book=book, run_id=run_id, root=root); manifest = core.load_json(manifest_path); core.validate_schema(manifest, core.EXTENDED_SCHEMA, "extended manifest")
    closure = {row["path"]: row["sha256"] for rows in manifest["artifact_sets"].values() for row in rows}
    if len(closure) != sum(len(rows) for rows in manifest["artifact_sets"].values()): raise core.ReplayEvidenceError("QF-11-HASH-CYCLE", "duplicate closure path")
    receipt = {
        "schema_version": "whole_bible_terminal_completion_receipt.v1", "receipt_id": f"{campaign['campaign_id']}:{book}:{run_id}:terminal",
        "campaign_id": campaign["campaign_id"], "campaign_revision": campaign["revision"], "book": book, "run_id": run_id,
        "b10_stage_receipt_path": core.repo_relative(b10_path, root), "b10_stage_receipt_sha256": core.digest_file(b10_path),
        "extended_evidence_manifest_path": core.repo_relative(manifest_path, root), "extended_evidence_manifest_sha256": core.digest_file(manifest_path),
        "completion_gate_bundle_path": core.repo_relative(bundle_path, root), "completion_gate_bundle_sha256": core.digest_file(bundle_path),
        "completion_gates": gates, "final_artifact_closure": closure, "outcome": outcome,
        "unresolved_hold_ids": unresolved_holds, "unresolved_appeal_ids": unresolved_appeals,
        "written_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"), "receipt_written_last": True,
        "replay_plumbing_validated": True, "replay_qualified": False, "launch_qualified": False, "whole_bible_form_language_qualified": False,
        "counts_as_cross_model_independent_vote": False, "candidate_only": True, "promotion_authorized": False, "non_authorizing": True,
    }
    core.validate_schema(receipt, core.TERMINAL_SCHEMA, "terminal completion receipt")
    output = model_root / "receipts" / f"{book}_completion_v3.{run_id}.json"
    with core.exclusive_lock(model_root / "state"): core.atomic_write(output, core.canonical_bytes(receipt), immutable=True)
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--draft", type=Path, required=True); parser.add_argument("--campaign", type=Path, default=core.DEFAULT_CAMPAIGN); parser.add_argument("--model-root", type=Path, default=core.DEFAULT_MODEL_ROOT); args = parser.parse_args(argv)
    try: path = write_terminal(draft_path=args.draft, campaign_path=args.campaign, model_root=args.model_root)
    except core.ReplayEvidenceError as exc: print(f"Terminal completion write failed: {exc}", file=sys.stderr); return 1
    print(f"Wrote terminal candidate completion receipt: {core.repo_relative(path)}"); return 0

if __name__ == "__main__": raise SystemExit(main())
