#!/usr/bin/env python3
"""Snapshot, boss-bind, and prepare a revision-7 B01 evidence attempt.

`--prepare-evidence` snapshots controller-authored role/synthesis JSON only.
`--finalize` requires a boss authorization bound to those exact bytes, derives
the integrity scan/manifests/draft, and invokes the generic prepare-only writer.
Neither mode commits a stage receipt or authorizes B02.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from scripts import whole_bible_replay_evidence_v2 as core
from scripts import write_whole_bible_stage_receipt_v2 as writer

PROMPT_SLUGS = {
    "original_language_translation_scout": "original_language",
    "literary_form_scout": "literary_form",
    "canonical_relations_and_premortem_scout": "canonical_premortem",
    "second_temple_rabbinic_context_scout": "ancient_context",
}
BASE_FILES = {
    "book_strategy": "book_strategy.json",
    "form_inventory": "form_inventory.json",
    "hardest_passage_forecast": "hardest_passage_forecast.json",
    "source_gap_register": "source_gap_register.json",
    "ancient_context_gap_or_qualified_receipt": "ancient_context_gap.json",
    "b01_execution_ledger": "execution_ledger.json",
    "synthesis_lineage": "synthesis_lineage.json",
}


def _artifact_row(artifact_id: str, path: Path, *, root: Path, scope: str) -> dict[str, str]:
    return {"artifact_id": artifact_id, "path": core.repo_relative(path, root), "sha256": core.digest_file(path), "media_type": "application/json", "scope": scope}


def _all_snapshot_files(proposal_dir: Path) -> dict[str, Path]:
    files = {artifact_id: proposal_dir / name for artifact_id, name in BASE_FILES.items()}
    for prompt, slug in PROMPT_SLUGS.items():
        files[f"execution_{slug}"] = proposal_dir / f"execution.{slug}.json"
        files[f"role_report_{slug}"] = proposal_dir / f"role_report.{slug}.json"
    return files


def _validate_json_identity(path: Path, *, book: str, run_id: str, attempt_id: str) -> dict[str, Any]:
    value = core.load_json(path)
    for key, expected in (("book", book), ("run_id", run_id), ("stage_attempt_id", attempt_id)):
        if value.get(key) != expected:
            raise core.ReplayEvidenceError("QF-17-B01-ATTRIBUTION", f"{path.name}: {key} mismatch")
    return value


def prepare_evidence(*, book: str, run_id: str, attempt_id: str, proposal_dir: Path,
                     campaign_path: Path = core.CAMPAIGN, registry_path: Path = core.REGISTRY,
                     model_root: Path = core.MODEL_ROOT, root: Path = core.ROOT) -> Path:
    if not core.B01_MATERIALIZATION_ENABLED:
        raise core.ReplayEvidenceError("QF-21-UNMIGRATED-STAGE", "B01 materialization is blocked pending typed controller, role, boss, challenge, and appeal evidence")
    core.validate_runtime_contract(campaign_path=campaign_path, registry_path=registry_path, root=root, model_root=model_root)
    campaign = core.load_json(campaign_path)
    index = core.read_index(core.run_dir(model_root, book, run_id), campaign, book, run_id)
    if "B00" not in index["selected"] or "B01" in index["selected"]:
        raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", "B01 evidence requires selected B00 and no selected B01")
    sources = _all_snapshot_files(proposal_dir)
    if any(not path.is_file() for path in sources.values()):
        missing = sorted(path.name for path in sources.values() if not path.is_file())
        raise core.ReplayEvidenceError("QF-17-B01-ATTRIBUTION", f"proposal files missing: {missing}")
    base = core.attempt_root(model_root, book, run_id, "B01", attempt_id)
    evidence = base / "evidence"
    snapshots: dict[str, Path] = {}
    for artifact_id, source in sources.items():
        _validate_json_identity(source, book=book, run_id=run_id, attempt_id=attempt_id)
        target = evidence / source.name
        core.atomic_write(target, source.read_bytes(), immutable=True)
        snapshots[artifact_id] = target
    core.validate_b01_payload(list(snapshots.values()), book=book, root=root)
    passages, _ = core._book_rows(book, root)
    ordinals = {row["osis_ref"]: index for index, row in enumerate(passages)}
    for artifact_id in ("book_strategy", "form_inventory", "hardest_passage_forecast", "source_gap_register", "synthesis_lineage"):
        core.reject_partition_like_ranges(core.load_json(snapshots[artifact_id]), ordinals=ordinals)
    index_path = evidence / "evidence_packet_index.json"
    packet_index = {
        "schema_version": "whole_bible_b01_evidence_packet_index.v1", "book": book, "run_id": run_id,
        "stage_attempt_id": attempt_id,
        "artifact_sha256": {core.repo_relative(path, root): core.digest_file(path) for path in sorted(snapshots.values())},
        "boss_review_required": True, "B01_receipt_written": False, "B02_authorized": False,
        "contains_scripture_text": False, "contains_source_rows": False,
        "contains_prompts_or_hidden_reasoning": False, "non_authorizing": True,
    }
    core.atomic_write(index_path, core.canonical_bytes(packet_index), immutable=True)
    return index_path


def _input_paths(book: str, *, root: Path) -> dict[str, Path]:
    if book != "Num":
        raise core.ReplayEvidenceError("QF-21-UNMIGRATED-STAGE", "B01 v2 source closure currently qualified only for Numbers")
    return {
        "campaign_registry": core.REGISTRY,
        "workflow": core.WORKFLOW,
        "prompt_pack": core.PROMPTS,
        "runtime_adapter": core.ADAPTER,
        "canonical_passages": root / "data/canonical/scripture/passages/passages.jsonl",
        "web_witness": root / "data/canonical/translations/eng-web/translation_witnesses.jsonl",
        "oshb_source_manifest": root / "data/raw/original_language/hebrew/openscriptures_oshb/source_manifest.yaml",
        "oshb_raw_archive": root / "data/raw/original_language/hebrew/openscriptures_oshb/raw/openscriptures_oshb-3d15126fb1ef.zip",
        "oshb_view_manifest": root / "data/candidate/original_language_evidence/canonical_source_views/openscriptures_oshb/canonical_source_view_manifest.yaml",
        "oshb_included_files": root / "data/candidate/original_language_evidence/canonical_source_views/openscriptures_oshb/included_files.jsonl",
        "oshb_book_view": root / f"data/candidate/original_language_evidence/canonical_source_views/openscriptures_oshb/files/{book}.xml",
        "uxlc_source_manifest": root / "data/raw/original_language/hebrew/tanach_us_uxlc/source_manifest.yaml",
        "uxlc_raw_archive": root / "data/raw/original_language/hebrew/tanach_us_uxlc/raw/Tanach.xml.zip",
        "uxlc_view_manifest": root / "data/candidate/original_language_evidence/canonical_source_views/tanach_us_uxlc/canonical_source_view_manifest.yaml",
        "uxlc_included_files": root / "data/candidate/original_language_evidence/canonical_source_views/tanach_us_uxlc/included_files.jsonl",
        "uxlc_book_view": root / f"data/candidate/original_language_evidence/canonical_source_views/tanach_us_uxlc/files/{book}.xml",
    }


def finalize_evidence(*, book: str, run_id: str, attempt_id: str, boss_authorization_source: Path,
                      campaign_path: Path = core.CAMPAIGN, registry_path: Path = core.REGISTRY,
                      model_root: Path = core.MODEL_ROOT, root: Path = core.ROOT) -> Path:
    if not core.B01_MATERIALIZATION_ENABLED:
        raise core.ReplayEvidenceError("QF-21-UNMIGRATED-STAGE", "B01 materialization is blocked pending typed controller, role, boss, challenge, and appeal evidence")
    core.validate_runtime_contract(campaign_path=campaign_path, registry_path=registry_path, root=root, model_root=model_root)
    campaign = core.load_json(campaign_path)
    job = core.campaign_job(campaign, book)
    base = core.attempt_root(model_root, book, run_id, "B01", attempt_id)
    evidence = base / "evidence"
    snapshot_sources = _all_snapshot_files(evidence)
    snapshots = dict(snapshot_sources)
    packet_index_path = evidence / "evidence_packet_index.json"
    if not packet_index_path.is_file() or any(not path.is_file() for path in snapshots.values()):
        raise core.ReplayEvidenceError("QF-17-B01-ATTRIBUTION", "prepare-evidence must complete before finalize")
    snapshots["evidence_packet_index"] = packet_index_path
    packet_paths = sorted(core.repo_relative(path, root) for path in snapshots.values())
    packet_sha = core.digest_bytes(core.canonical_bytes({path: core.digest_file(core.resolve_repo_path(path, root)) for path in packet_paths}))
    boss = core.load_json(boss_authorization_source)
    expected_boss = {
        "schema_version": "whole_bible_b01_boss_authorization.v1", "book": book, "run_id": run_id,
        "stage_attempt_id": attempt_id, "evidence_packet_sha256": packet_sha,
        "verdict": "go_B01_receipt_only", "B02_authorized": False, "non_authorizing": True,
    }
    if boss != expected_boss:
        raise core.ReplayEvidenceError("QF-B01-BOSS", "boss authorization source does not bind exact packet")
    boss_path = evidence / "boss_authorization.json"
    core.atomic_write(boss_path, core.canonical_bytes(boss), immutable=True)
    snapshots["b01_boss_authorization"] = boss_path
    core.validate_b01_payload(list(snapshots.values()), book=book, root=root)
    scan_path = evidence / "integrity_scan.json"
    scan = {
        "schema_version": "whole_bible_b01_integrity_scan.v1", "book": book, "run_id": run_id,
        "stage_attempt_id": attempt_id,
        "scanned_artifact_sha256": {core.repo_relative(path, root): core.digest_file(path) for path in sorted(snapshots.values())},
        "scanner_rule_ids": ["QF-15-B01-BOUNDARY-LEAKAGE", "QF-20-B01-PAYLOAD"],
        "finding_count": 0, "status": "passed", "B02_authorized": False, "non_authorizing": True,
    }
    core.atomic_write(scan_path, core.canonical_bytes(scan), immutable=True)
    snapshots["b01_integrity_scan"] = scan_path
    input_paths = _input_paths(book, root=root)
    if any(not path.is_file() for path in input_paths.values()):
        raise core.ReplayEvidenceError("QF-SOURCE-ANCESTRY", "B01 governed input missing")
    input_manifest = {
        "schema_version": "whole_bible_artifact_manifest.v2", "manifest_id": f"{campaign['campaign_id']}:{book}:{run_id}:B01:{attempt_id}:input",
        "book": book, "run_id": run_id, "stage_id": "B01", "attempt_id": attempt_id, "direction": "input",
        "artifacts": [_artifact_row(artifact_id, path, root=root, scope="governed_source_input") for artifact_id, path in input_paths.items()],
        "contains_scripture_text": True, "contains_source_rows": True,
        "contains_prompts_or_hidden_reasoning": False, "non_authorizing": True,
    }
    output_manifest = {
        "schema_version": "whole_bible_artifact_manifest.v2", "manifest_id": f"{campaign['campaign_id']}:{book}:{run_id}:B01:{attempt_id}:output",
        "book": book, "run_id": run_id, "stage_id": "B01", "attempt_id": attempt_id, "direction": "output",
        "artifacts": [_artifact_row(artifact_id, path, root=root, scope="receipt_bound_B01_evidence") for artifact_id, path in snapshots.items()],
        "contains_scripture_text": False, "contains_source_rows": False,
        "contains_prompts_or_hidden_reasoning": False, "non_authorizing": True,
    }
    input_manifest_path = base / "manifests" / "input.json"
    output_manifest_path = base / "manifests" / "output.json"
    with core.exclusive_lock(model_root / "state"):
        core.atomic_write(input_manifest_path, core.canonical_bytes(input_manifest), immutable=True)
        core.atomic_write(output_manifest_path, core.canonical_bytes(output_manifest), immutable=True)
    execution_ids = [f"execution_{slug}" for slug in PROMPT_SLUGS.values()]
    role_report_ids = [f"role_report_{slug}" for slug in PROMPT_SLUGS.values()]
    executions = [core.load_json(snapshots[artifact_id]) for artifact_id in execution_ids]
    synthesis = core.load_json(snapshots["synthesis_lineage"])
    draft = {
        "schema_version": "whole_bible_stage_receipt_draft.v2", "book": book, "run_id": run_id,
        "stage_id": "B01", "attempt_id": attempt_id, "attempt_kind": "original",
        "role_or_deterministic_gate": "four_role_B01_mesh_plus_root_synthesis_and_boss", "executor_kind": "agent",
        "started_at": min(row["started_at"] for row in executions), "finished_at": synthesis["finished_at"],
        "outcome": "pass_with_holds", "unresolved_holds": sorted(core.REQUIRED_B01_HOLDS),
        "input_manifest_path": core.repo_relative(input_manifest_path, root), "output_manifest_path": core.repo_relative(output_manifest_path, root),
        "stage_evidence": {"artifact_refs": {
            "book_strategy": "book_strategy", "form_inventory": "form_inventory",
            "hardest_passage_forecast": "hardest_passage_forecast", "source_gap_register": "source_gap_register",
            "ancient_context_gap_or_qualified_receipt": "ancient_context_gap_or_qualified_receipt",
            "b01_execution_ledger": "b01_execution_ledger", "b01_prompt_execution": execution_ids,
            "b01_role_report": role_report_ids, "synthesis_lineage": "synthesis_lineage",
            "b01_integrity_scan": "b01_integrity_scan", "b01_boss_authorization": "b01_boss_authorization",
        }, "values": {"ancient_context_activation_status": "corpus_gap_recorded",
            "aggregate_artifact_blindness": False, "root_synthesis_attempt_id": synthesis["synthesis_execution_id"],
            "evidence_attempt_scoped": True, "B02_authorized": False}},
        "independence_scope": {"authoring_independent_from_sibling_maps": True, "artifact_blindness": False,
            "role_separation": True, "shared_model_substrate": True, "runtime_model_identity_attested": False,
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
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--prepare-evidence", action="store_true")
    mode.add_argument("--finalize", action="store_true")
    parser.add_argument("--book", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--attempt-id", required=True)
    parser.add_argument("--proposal-dir", type=Path)
    parser.add_argument("--boss-authorization-source", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.prepare_evidence:
            if args.proposal_dir is None:
                raise core.ReplayEvidenceError("QF-SCHEMA", "--proposal-dir is required")
            path = prepare_evidence(book=args.book, run_id=args.run_id, attempt_id=args.attempt_id, proposal_dir=args.proposal_dir)
        else:
            if args.boss_authorization_source is None:
                raise core.ReplayEvidenceError("QF-SCHEMA", "--boss-authorization-source is required")
            path = finalize_evidence(book=args.book, run_id=args.run_id, attempt_id=args.attempt_id, boss_authorization_source=args.boss_authorization_source)
    except core.ReplayEvidenceError as exc:
        print(f"B01 v2 operation failed: {exc}", file=sys.stderr)
        return 1
    print(core.repo_relative(path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
