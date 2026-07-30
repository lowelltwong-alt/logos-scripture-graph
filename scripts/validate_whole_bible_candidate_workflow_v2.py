#!/usr/bin/env python3
"""Static fail-closed validation for revision-7 B00/B01 replay contracts."""
from __future__ import annotations

import sys

from scripts import whole_bible_replay_evidence_v2 as core


def require(condition: bool, message: str) -> None:
    if not condition:
        raise core.ReplayEvidenceError("QF-V2-SPEC", message)


def validate() -> dict:
    workflow = core.load_yaml(core.WORKFLOW)
    prompts = core.load_yaml(core.PROMPTS)
    adapter = core.load_yaml(core.ADAPTER)
    require(workflow.get("schema_version") == "scripture_first_whole_bible_candidate_workflow.v2", "workflow schema")
    require(workflow.get("workflow_version") == "2.0.0", "workflow version")
    require(prompts.get("schema_version") == "scripture_first_whole_bible_candidate_prompt_pack.v2", "prompt schema")
    require(prompts.get("prompt_pack_version") == "2.0.0", "prompt version")
    require(adapter.get("schema_version") == "scripture_first_whole_bible_runtime_adapter.v2", "adapter schema")
    require(adapter.get("adapter_version") == "2.0.0", "adapter version")
    bindings = workflow.get("executable_stage_bindings") or {}
    require(list(bindings)[:2] == ["B00", "B01"], "B00/B01 binding order")
    require(tuple(bindings["B01"].get("prompt_templates") or []) == core.REQUIRED_PROMPTS, "B01 exact four prompts")
    implementation = workflow.get("replay_evidence_implementation") or {}
    require(implementation.get("contract_generation") == 2 and implementation.get("campaign_revision") == 7, "v2 implementation identity")
    require(implementation.get("replay_runbook") == core.repo_relative(core.RUNBOOK) and core.RUNBOOK.is_file(), "replay runbook binding")
    require(implementation.get("supported_stage_ceiling") == "B00" and implementation.get("B01_through_B10_status") == "blocked_pending_typed_evidence_and_attempt_scoped_migration" and implementation.get("B01_candidate_design_only") is True and implementation.get("B01_materialization_enabled") is False, "stage ceiling")
    campaign = core.load_json(core.CAMPAIGN)
    require(campaign.get("revision") == 7, "campaign revision")
    execution = campaign.get("execution") or {}
    require(execution.get("mode") == "specification_only" and execution.get("supported_stage_ceiling") == "B00" and execution.get("B02_authorized") is False and execution.get("launch_command") == "not-authorized", "campaign authority boundary")
    blocked_labels = {"qualification_status": "blocked_pending_B01_typed_evidence_and_B01_B10_migration", "authorization_receipt": "absent", "dry_run_evidence": "absent", "independent_launch_review": "absent", "qualification_evidence": "absent"}
    require(all(execution.get(key) == value for key, value in blocked_labels.items()), "campaign exact blocked qualification labels")
    require(execution.get("workflow_ref") == core.repo_relative(core.WORKFLOW) and execution.get("prompt_pack_ref") == core.repo_relative(core.PROMPTS) and execution.get("runtime_adapter_ref") == core.repo_relative(core.ADAPTER), "top-level v2 contract refs")
    require(execution.get("durability_command") == "python -m scripts.validate_whole_bible_stage_receipts_v2 --book <Book> --run-id <run_id> --require-through B00" and execution.get("terminal_completion_writer") == "not-authorized-revision-7", "top-level v2 command ceiling")
    replay = campaign.get("replay_contract") or {}
    for key, path in (("workflow", core.WORKFLOW), ("prompt_pack", core.PROMPTS), ("runtime_adapter", core.ADAPTER)):
        require((replay.get(key) or {}).get("path") == core.repo_relative(path) and (replay.get(key) or {}).get("digest") == core.digest_file(path), f"replay contract {key}")
    require(replay.get("supported_stage_ceiling") == "B00" and replay.get("B01_through_B10_status") == "blocked_pending_typed_evidence_and_attempt_scoped_migration", "replay stage ceiling")
    receipt_contract = workflow.get("stage_receipt_contract") or {}
    require(str(receipt_contract.get("per_run_append_only_log_template", "")).endswith("/receipts.v2.jsonl") and str(receipt_contract.get("global_append_only_log", "")).endswith("/receipts.v2.jsonl"), "v2 receipt log bindings")
    require(all(replay.get(key) == value for key, value in blocked_labels.items()), "replay exact blocked qualification labels")
    jobs = campaign["phases"][0]["waves"][0]["subwaves"][0]["jobs"]
    require(len(jobs) == 67 and jobs[-1].get("id") == "J-067-MERGE", "campaign must contain 66 book jobs plus merge")
    book_jobs = jobs[:66]
    require(jobs[-1].get("max_authorized_stage") == "none" and jobs[-1].get("revision_7_status") == "blocked_pending_all_66_revision_7_book_receipts", "merge must remain blocked")
    for job in book_jobs:
        book = str(job.get("idempotency_key", "")).split(":")[1]
        require(job.get("max_authorized_stage") == "B00" and job.get("B01_status") == "blocked_pending_typed_controller_role_boss_challenge_and_appeal_evidence" and job.get("B02_authorized") is False, f"{book}: stage ceiling")
        require(job.get("workflow_ref") == core.repo_relative(core.WORKFLOW) and job.get("prompt_pack_ref") == core.repo_relative(core.PROMPTS) and job.get("runtime_adapter_ref") == core.repo_relative(core.ADAPTER), f"{book}: v2 refs")
        require(job.get("durability_check") == f"python -m scripts.validate_whole_bible_stage_receipts_v2 --book {book} --run-id <run_id> --require-through B00", f"{book}: v2 durability")
        require(set(job.get("input_digests") or {}) == set(job.get("inputs") or []), f"{book}: input digest closure")
        for relative in job.get("inputs") or []:
            declared = job["input_digests"][relative]
            if relative == core.repo_relative(core.CAMPAIGN):
                require(declared == "stage_receipt_v2:B00.campaign_sha256", f"{book}: campaign self marker")
            else:
                require(declared == core.digest_file(core.resolve_repo_path(relative)), f"{book}: stale input {relative}")
        plan = job.get("stage_plan") or []
        require([row.get("stage_id") for row in plan] == [f"B{index:02d}" for index in range(11)], f"{book}: stage plan")
        for row in plan[:1]:
            token = f"/attempts/{row['stage_id']}/<attempt_id>/"
            require(token in row.get("input_manifest", "") and token in row.get("output_manifest", "") and token in row.get("prepared_commit", ""), f"{book}: attempt-scoped {row['stage_id']}")
            require(row.get("attempt_contract") == "immutable_prepare_then_revalidated_commit", f"{book}: prepare/commit")
        require(all(row.get("revision_7_status") == "blocked_pending_typed_evidence_and_attempt_scoped_migration" for row in plan[1:]), f"{book}: B01-B10 must remain blocked")
    registry = core.validate_runtime_contract()
    return {
        "schema_version": "whole_bible_candidate_workflow_validation.v2", "campaign_revision": 7,
        "book_jobs": len(book_jobs), "supported_stage_ceiling": "B00", "registry_sha256": core.digest_file(core.REGISTRY),
        "replay_qualified": False, "launch_qualified": False, "B02_authorized": False, "non_authorizing": True,
    }


def main() -> int:
    try:
        result = validate()
    except core.ReplayEvidenceError as exc:
        print(f"V2 workflow validation failed: {exc}", file=sys.stderr)
        return 1
    print(core.canonical_bytes(result).decode("utf-8"), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
