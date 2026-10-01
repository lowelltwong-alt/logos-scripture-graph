#!/usr/bin/env python3
"""Mechanically derive the revision-7 campaign and contract registry from rev6."""
from __future__ import annotations

import json
from pathlib import Path

import yaml

from scripts import whole_bible_replay_evidence_v2 as core

REV6 = core.MODEL_ROOT / "campaign.json"
REV7 = core.CAMPAIGN

CONTRACT_PATHS = (
    core.WORKFLOW, core.PROMPTS, core.ADAPTER, core.RUNBOOK, core.STAGE_SCHEMA, core.MANIFEST_SCHEMA,
    core.PREPARED_SCHEMA,
    core.ROOT / "scripts/whole_bible_replay_evidence_v2.py",
    core.ROOT / "scripts/write_whole_bible_stage_receipt_v2.py",
    core.ROOT / "scripts/build_whole_bible_b00_preflight_v2.py",
    core.ROOT / "scripts/validate_whole_bible_stage_receipts_v2.py",
    core.ROOT / "scripts/validate_whole_bible_candidate_workflow_v2.py",
    core.ROOT / "scripts/upgrade_whole_bible_campaign_rev7.py",
    core.ROOT / "tests/test_whole_bible_replay_evidence_v2.py",
)


def _jobs(campaign: dict) -> list[dict]:
    return campaign["phases"][0]["waves"][0]["subwaves"][0]["jobs"]


def _book(job: dict) -> str:
    key = str(job.get("idempotency_key", ""))
    parts = key.split(":")
    if len(parts) < 2 or not parts[1]:
        raise RuntimeError(f"{job.get('id')}: cannot derive canonical book ID")
    return parts[1]


def _source_support(job: dict) -> list[str]:
    book = _book(job)
    sources = ["openscriptures_oshb", "tanach_us_uxlc"] if (job.get("source_route") or {}).get("testament") == "old" else ["sblgnt", "cntr_sr", "ugnt"]
    result: list[str] = []
    for source in sources:
        language = "hebrew" if source in {"openscriptures_oshb", "tanach_us_uxlc"} else "greek"
        raw_manifest = core.ROOT / f"data/raw/original_language/{language}/{source}/source_manifest.yaml"
        manifest = yaml.safe_load(raw_manifest.read_text(encoding="utf-8"))
        view_root = core.ROOT / f"data/candidate/original_language_evidence/canonical_source_views/{source}"
        ledger_path = view_root / "included_files.jsonl"
        rows = [json.loads(line) for line in ledger_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        matches = [row for row in rows if row.get("book_id") == book]
        if not matches and len(rows) == 1 and rows[0].get("book_id") == "GreekNT":
            matches = rows
        if len(matches) != 1:
            raise RuntimeError(f"{job['id']}: no unique {source} view for {book}")
        result.extend([
            manifest["archive_path"],
            core.repo_relative(view_root / "canonical_source_view_manifest.yaml"),
            core.repo_relative(ledger_path),
            matches[0]["view_path"],
        ])
    return result


def _attempt_paths(book: str, stage: str) -> list[str]:
    base = f".ai/scratch/multi_model_bible_chunking/M7_sol/state/books/{book}/runs/<run_id>/attempts/{stage}/<attempt_id>"
    common = [f"{base}/manifests/input.json", f"{base}/manifests/output.json", f"{base}/draft.json", f"{base}/prepared_commit.json"]
    if stage == "B00":
        return common + [f"{base}/evidence/campaign_projection.json", f"{base}/evidence/preflight_report.json", f"{base}/evidence/dependency_evidence.json"]
    names = list(core.BASE_FILES.values()) if hasattr(core, "BASE_FILES") else []
    names = ["book_strategy.json", "form_inventory.json", "hardest_passage_forecast.json", "source_gap_register.json", "ancient_context_gap.json", "execution_ledger.json", "synthesis_lineage.json"]
    names += [f"execution.{slug}.json" for slug in ("original_language", "literary_form", "canonical_premortem", "ancient_context")]
    names += [f"role_report.{slug}.json" for slug in ("original_language", "literary_form", "canonical_premortem", "ancient_context")]
    names += ["evidence_packet_index.json", "boss_authorization.json", "integrity_scan.json"]
    return common + [f"{base}/evidence/{name}" for name in names]


def build_campaign() -> dict:
    campaign = core.load_json(REV6)
    campaign["campaign_id"] = "T521-M7-sol-whole-bible-r7"
    campaign["revision"] = 7
    execution = campaign.setdefault("execution", {})
    execution["mode"] = "specification_only"
    execution["supported_stage_ceiling"] = "B00"
    execution["B01_through_B10_status"] = "blocked_pending_typed_evidence_and_attempt_scoped_migration"
    execution["B02_authorized"] = False
    execution["launch_command"] = "not-authorized"
    execution["auto_advance_requires_qualification_receipt"] = True
    execution["adapter"] = {"name": "codex_desktop_m7_adapter_v2", "revision": "2"}
    execution["workflow_ref"] = core.repo_relative(core.WORKFLOW)
    execution["prompt_pack_ref"] = core.repo_relative(core.PROMPTS)
    execution["runtime_adapter_ref"] = core.repo_relative(core.ADAPTER)
    execution["stage_receipt_contract_ref"] = core.repo_relative(core.WORKFLOW) + "#stage_receipt_contract"
    execution["durability_command"] = "python -m scripts.validate_whole_bible_stage_receipts_v2 --book <Book> --run-id <run_id> --require-through B00"
    execution["receipt_log"] = ".ai/scratch/multi_model_bible_chunking/M7_sol/state/receipts.v2.jsonl"
    execution["receipt_dag"] = "B00 -> B01_through_B10_blocked_pending_migration"
    execution["terminal_completion_writer"] = "not-authorized-revision-7"
    execution["qualification_status"] = "blocked_pending_B01_typed_evidence_and_B01_B10_migration"
    execution["authorization_receipt"] = "absent"
    execution["dry_run_evidence"] = "absent"
    execution["independent_launch_review"] = "absent"
    execution["qualification_evidence"] = "absent"
    replay = campaign.setdefault("replay_contract", {})
    replay["workflow"] = {"path": core.repo_relative(core.WORKFLOW), "digest": core.digest_file(core.WORKFLOW)}
    replay["prompt_pack"] = {"path": core.repo_relative(core.PROMPTS), "digest": core.digest_file(core.PROMPTS)}
    replay["runtime_adapter"] = {"path": core.repo_relative(core.ADAPTER), "digest": core.digest_file(core.ADAPTER)}
    replay["campaign_registry"] = {"path": core.repo_relative(core.REGISTRY), "digest_binding": "B00_input_manifest_exact_hash"}
    replay["supported_stage_ceiling"] = "B00"
    replay["B01_through_B10_status"] = "blocked_pending_typed_evidence_and_attempt_scoped_migration"
    replay["qualification_status"] = "blocked_pending_B01_typed_evidence_and_B01_B10_migration"
    replay["authorization_receipt"] = "absent"
    replay["dry_run_evidence"] = "absent"
    replay["independent_launch_review"] = "absent"
    replay["qualification_evidence"] = "absent"
    replay["form_inventory_is_B01_hash_bound"] = False
    replay["form_observations_are_attempt_scoped_and_partition_scanned"] = True
    old_campaign = core.repo_relative(REV6)
    new_campaign = core.repo_relative(REV7)
    replacements = {
        old_campaign: new_campaign,
        "config/agents/families/scripture-first-biblical-chunking/whole_bible_candidate_workflow.v1.yaml": core.repo_relative(core.WORKFLOW),
        "config/agents/families/scripture-first-biblical-chunking/whole_bible_candidate_prompt_pack.v1.yaml": core.repo_relative(core.PROMPTS),
        "config/agents/families/scripture-first-biblical-chunking/codex_desktop_campaign_adapter.v1.yaml": core.repo_relative(core.ADAPTER),
    }
    contract_rel = [core.repo_relative(path) for path in CONTRACT_PATHS]
    for job in _jobs(campaign):
        book = _book(job)
        inputs = [replacements.get(path, path) for path in job.get("inputs") or []]
        remove_inputs = {
            "scripts/whole_bible_replay_evidence.py", "scripts/write_whole_bible_stage_receipt.py",
            "scripts/build_whole_bible_b00_preflight.py", "scripts/validate_whole_bible_stage_receipts.py",
            "config/agents/families/scripture-first-biblical-chunking/whole_bible_stage_receipt.schema.v1.json",
        }
        inputs = [path for path in inputs if path not in remove_inputs]
        source_paths = [] if job.get("id") == "J-067-MERGE" else _source_support(job)
        for path in contract_rel + source_paths:
            if path not in inputs:
                inputs.append(path)
        job["inputs"] = inputs
        job["workflow_ref"] = core.repo_relative(core.WORKFLOW)
        job["prompt_pack_ref"] = core.repo_relative(core.PROMPTS)
        job["runtime_adapter_ref"] = core.repo_relative(core.ADAPTER)
        if job.get("id") != "J-067-MERGE":
            job["durability_check"] = f"python -m scripts.validate_whole_bible_stage_receipts_v2 --book {book} --run-id <run_id> --require-through B00"
        job["max_authorized_stage"] = "none" if job.get("id") == "J-067-MERGE" else "B00"
        job["B01_status"] = "blocked_pending_typed_controller_role_boss_challenge_and_appeal_evidence"
        job["B02_authorized"] = False
        if job.get("id") == "J-067-MERGE":
            job["revision_7_status"] = "blocked_pending_all_66_revision_7_book_receipts"
            if isinstance(job.get("idempotency_key"), str):
                job["idempotency_key"] = job["idempotency_key"].replace("workflow-1.2.0", "workflow-2.0.0")
            continue
        legacy_prefix = f".ai/scratch/multi_model_bible_chunking/M7_sol/state/books/{book}/runs/<run_id>/"
        def keep(path: str) -> bool:
            if not path.startswith(legacy_prefix):
                return True
            return not ("/manifests/B00." in path or "/manifests/B01." in path or "/preflight/" in path or "/drafts/B00." in path)
        for key in ("outputs", "allowed_paths"):
            values = [path for path in (job.get(key) or []) if keep(path)]
            extra_paths = _attempt_paths(book, "B00")
            if key == "allowed_paths":
                extra_paths.append(core.repo_relative(core.REGISTRY))
            for path in extra_paths:
                if path not in values:
                    values.append(path)
            job[key] = values
        for stage in job.get("stage_plan") or []:
            stage_id = stage["stage_id"]
            if stage_id == "B00":
                base = f".ai/scratch/multi_model_bible_chunking/M7_sol/state/books/{book}/runs/<run_id>/attempts/{stage_id}/<attempt_id>"
                stage["input_manifest"] = f"{base}/manifests/input.json"
                stage["output_manifest"] = f"{base}/manifests/output.json"
                stage["prepared_commit"] = f"{base}/prepared_commit.json"
                stage["attempt_contract"] = "immutable_prepare_then_revalidated_commit"
                stage["required_artifacts"] = [f"{base}/evidence/campaign_projection.json", f"{base}/evidence/preflight_report.json", f"{base}/evidence/dependency_evidence.json"]
            else:
                stage["revision_7_status"] = "blocked_pending_typed_evidence_and_attempt_scoped_migration"
        if isinstance(job.get("idempotency_key"), str):
            job["idempotency_key"] = job["idempotency_key"].replace("workflow-1.2.0", "workflow-2.0.0")
    merge = campaign.get("merge") or {}
    if isinstance(merge.get("idempotency_key"), str):
        merge["idempotency_key"] = merge["idempotency_key"].replace("workflow-1.2.0", "workflow-2.0.0")
    for job in _jobs(campaign):
        prior_digests = dict(job.get("input_digests") or {})
        digests = {}
        for relative in job["inputs"]:
            if relative == new_campaign:
                digests[relative] = "stage_receipt_v2:B00.campaign_sha256"
            else:
                path = core.resolve_repo_path(relative)
                if path.is_file():
                    digests[relative] = core.digest_file(path)
                elif relative in prior_digests:
                    digests[relative] = prior_digests[relative]
                else:
                    raise RuntimeError(f"{job['id']}: unresolved input digest {relative}")
        job["input_digests"] = digests
    return campaign


def build_registry(campaign: dict) -> dict:
    return {
        "schema_version": "whole_bible_campaign_registry.v1", "registry_id": "T521-whole-bible-replay-contract-r7",
        "campaign_path": core.repo_relative(REV7), "campaign_sha256": core.digest_file(REV7),
        "contract_files": [{"path": core.repo_relative(path), "sha256": core.digest_file(path)} for path in CONTRACT_PATHS],
        "candidate_only": True, "non_authorizing": True,
    }


def main() -> int:
    campaign = build_campaign()
    core.atomic_write(REV7, core.canonical_bytes(campaign))
    registry = build_registry(campaign)
    core.atomic_write(core.REGISTRY, core.canonical_bytes(registry))
    print(core.repo_relative(REV7))
    print(core.repo_relative(core.REGISTRY))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
