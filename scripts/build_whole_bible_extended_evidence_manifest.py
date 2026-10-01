#!/usr/bin/env python3
"""Build an immutable B00-B09 precompletion evidence manifest."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from scripts import whole_bible_replay_evidence as core


def artifact_records(records: Any, *, root: Path, model_root: Path, job: dict[str, Any], run_id: str) -> list[dict[str, Any]]:
    if not isinstance(records, list) or not records: raise core.ReplayEvidenceError("QF-SCHEMA", "artifact set empty")
    output: list[dict[str, Any]] = []; seen: set[str] = set(); model_prefix = core.repo_relative(model_root, root).rstrip("/") + "/"
    for row in records:
        if not isinstance(row, dict) or set(row) != {"group", "artifact_id", "path", "media_type", "scope"}: raise core.ReplayEvidenceError("QF-SCHEMA", "artifact spec record")
        artifact_id = row["artifact_id"]
        if not isinstance(artifact_id, str) or not artifact_id or artifact_id in seen: raise core.ReplayEvidenceError("QF-SCHEMA", "duplicate artifact ID")
        path = core.resolve_repo_path(row["path"], root)
        if not path.is_file(): raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", f"missing {row['path']}")
        normalized = core.repo_relative(path, root)
        if not core.job_path_authorized(normalized, job, run_id=run_id): raise core.ReplayEvidenceError("QF-08-SIBLING-CONTAMINATION", f"extended artifact outside active job/run allowlist: {normalized}")
        if normalized.startswith(".ai/scratch/multi_model_bible_chunking/") and not normalized.startswith(model_prefix): raise core.ReplayEvidenceError("QF-08-SIBLING-CONTAMINATION", normalized)
        output.append({**row, "path": normalized, "sha256": core.digest_file(path)}); seen.add(artifact_id)
    return output


def chunk_projection(path: Path) -> tuple[str, str, str]:
    decisions: list[str] = []; statuses: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip(): continue
        try: row = json.loads(line)
        except json.JSONDecodeError as exc: raise core.ReplayEvidenceError("QF-JSON", f"{core.repo_relative(path)}:{number}") from exc
        if not isinstance(row, dict): raise core.ReplayEvidenceError("QF-JSON", f"{core.repo_relative(path)}:{number}")
        decision = row.get("decision_id") or row.get("id")
        if not isinstance(decision, str) or not decision or decision in decisions: raise core.ReplayEvidenceError("QF-06-LINEAGE-LOSS", f"bad decision ID at {number}")
        decisions.append(decision); statuses.append({"decision_id": decision, "review_status": row.get("review_status"), "candidate_hold_state": row.get("candidate_hold_state"), "candidate_hold_basis": row.get("candidate_hold_basis")})
    if not decisions: raise core.ReplayEvidenceError("QF-06-LINEAGE-LOSS", "empty chunks")
    return core.digest_file(path), core.digest_bytes(core.canonical_bytes(decisions)), core.digest_bytes(core.canonical_bytes(statuses))


def build_manifest(*, spec_path: Path, campaign_path: Path = core.DEFAULT_CAMPAIGN, model_root: Path = core.DEFAULT_MODEL_ROOT, root: Path = core.ROOT, allow_test_roots: bool = False) -> Path:
    core.validate_authoritative_runtime_paths(campaign_path=campaign_path, model_root=model_root, root=root, allow_test_roots=allow_test_roots)
    spec = core.load_json(spec_path)
    if set(spec) != {"schema_version", "book", "run_id", "artifact_sets", "non_authorizing"} or spec.get("schema_version") != "whole_bible_extended_evidence_spec.v1" or spec.get("non_authorizing") is not True:
        raise core.ReplayEvidenceError("QF-SCHEMA", "extended manifest spec")
    book, run_id = spec["book"], spec["run_id"]; campaign = core.load_json(campaign_path); job = core.campaign_job(campaign, book); directory = core.run_dir(model_root, book, run_id)
    with core.exclusive_lock(model_root / "state"):
        index = core.read_index(directory, campaign, book, run_id); selected = index["selected"]; stage_refs: dict[str, dict[str, str]] = {}
        prior: str | None = None
        for stage_id in core.STAGES[:10]:
            ref = selected.get(stage_id)
            if not isinstance(ref, dict): raise core.ReplayEvidenceError("QF-01-PLAN-NOT-RUN", f"missing selected {stage_id}")
            path = core.resolve_repo_path(ref["path"], root)
            if not path.is_file() or core.digest_file(path) != ref.get("sha256"): raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", f"stale {stage_id}")
            receipt = core.load_json(path); core.validate_schema(receipt, core.STAGE_SCHEMA, stage_id); core.validate_stage_semantics(receipt)
            if receipt["outcome"] not in core.SUCCESS_OUTCOMES or receipt["prior_stage_receipt_sha256"] != prior: raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", f"invalid {stage_id} chain/outcome")
            stage_refs[stage_id] = {"attempt_id": ref["attempt_id"], "path": ref["path"], "sha256": ref["sha256"]}; prior = ref["sha256"]
        sets = spec["artifact_sets"]
        if not isinstance(sets, dict) or set(sets) != {"core", "extended"}: raise core.ReplayEvidenceError("QF-SCHEMA", "core/extended sets")
        core_rows = artifact_records(sets["core"], root=root, model_root=model_root, job=job, run_id=run_id); extended_rows = artifact_records(sets["extended"], root=root, model_root=model_root, job=job, run_id=run_id)
        missing_core = core.CORE_GROUPS - {row["group"] for row in core_rows}; missing_extended = core.EXTENDED_GROUPS - {row["group"] for row in extended_rows}
        if missing_core or missing_extended: raise core.ReplayEvidenceError("QF-11-HASH-CYCLE", f"missing core={sorted(missing_core)} extended={sorted(missing_extended)}")
        chunks = [row for row in core_rows if row["group"] == "chunks"]
        if len(chunks) != 1: raise core.ReplayEvidenceError("QF-SCHEMA", "exactly one chunks artifact")
        chunks_sha, decisions_sha, status_sha = chunk_projection(core.resolve_repo_path(chunks[0]["path"], root))
        manifest = {
            "schema_version": "whole_bible_extended_evidence_manifest.v1", "manifest_id": f"{campaign['campaign_id']}:{book}:{run_id}:precompletion",
            "scope": "book_precompletion_B00_B09", "campaign_id": campaign["campaign_id"], "campaign_revision": campaign["revision"], "book": book, "run_id": run_id,
            "workflow_sha256": core.digest_file(core.WORKFLOW), "prompt_pack_sha256": core.digest_file(core.PROMPTS), "runtime_adapter_sha256": core.digest_file(core.ADAPTER),
            "artifact_sets": {"core": core_rows, "extended": extended_rows}, "precompletion_stage_receipts": stage_refs,
            "selected_revision": {"chunks_sha256": chunks_sha, "active_decision_ids_sha256": decisions_sha, "status_hold_projection_sha256": status_sha},
            "canonicalization": {"generated_json": "utf8_sorted_keys_compact_json_sha256", "ordinary_artifacts": "sha256_exact_bytes"},
            "contains_scripture_text": False, "contains_source_rows": False, "contains_prompts_or_hidden_reasoning": False, "non_authorizing": True,
        }
        core.validate_schema(manifest, core.EXTENDED_SCHEMA, "extended evidence manifest"); output = directory / "extended_evidence_manifest.precompletion.json"; core.atomic_write(output, core.canonical_bytes(manifest), immutable=True)
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--spec", type=Path, required=True); parser.add_argument("--campaign", type=Path, default=core.DEFAULT_CAMPAIGN); parser.add_argument("--model-root", type=Path, default=core.DEFAULT_MODEL_ROOT); args = parser.parse_args(argv)
    try: path = build_manifest(spec_path=args.spec, campaign_path=args.campaign, model_root=args.model_root)
    except core.ReplayEvidenceError as exc: print(f"Extended evidence manifest build failed: {exc}", file=sys.stderr); return 1
    print(f"Wrote precompletion evidence manifest: {core.repo_relative(path)}"); return 0

if __name__ == "__main__": raise SystemExit(main())
