#!/usr/bin/env python3
"""Upgrade the M7 campaign to immutable run/attempt receipts and terminal v3 closure."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
CAMPAIGN = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/campaign.json"
MODEL = ".ai/scratch/multi_model_bible_chunking/M7_sol"
WORKFLOW = "config/agents/families/scripture-first-biblical-chunking/whole_bible_candidate_workflow.v1.yaml"
PROMPTS = "config/agents/families/scripture-first-biblical-chunking/whole_bible_candidate_prompt_pack.v1.yaml"
ADAPTER = "config/agents/families/scripture-first-biblical-chunking/codex_desktop_campaign_adapter.v1.yaml"
HARNESS_INPUTS = [
    "scripts/whole_bible_replay_evidence.py",
    "scripts/write_whole_bible_stage_receipt.py",
    "scripts/write_whole_bible_boss_phase_receipt.py",
    "scripts/build_whole_bible_extended_evidence_manifest.py",
    "scripts/validate_whole_bible_stage_receipts.py",
    "scripts/write_whole_bible_terminal_completion_receipt.py",
    "scripts/run_whole_bible_completion_gates.py",
    "scripts/build_whole_bible_b00_preflight.py",
    f"config/agents/families/scripture-first-biblical-chunking/whole_bible_stage_receipt.schema.v1.json",
    f"config/agents/families/scripture-first-biblical-chunking/whole_bible_boss_phase_receipt.schema.v1.json",
    f"config/agents/families/scripture-first-biblical-chunking/whole_bible_extended_evidence_manifest.schema.v1.json",
    f"config/agents/families/scripture-first-biblical-chunking/whole_bible_terminal_completion_receipt.schema.v1.json",
]

def digest(relative: str) -> str:
    return "sha256:" + hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()

def add_unique(rows: list[str], value: str) -> None:
    if value not in rows: rows.append(value)

def main() -> int:
    campaign = json.loads(CAMPAIGN.read_text(encoding="utf-8")); campaign["revision"] = 6
    execution = campaign["execution"]
    execution["qualification_status"] = "blocked_pending_materialized_B00_B10_terminal_completion_dry_replay_dimensional_calibration_and_independent_launch_review"
    execution["run_id_binding"] = "required_at_dispatch"
    execution["stage_attempt_id_binding"] = "required_per_stage_attempt"
    execution["receipt_dag"] = "B00-B09 -> precompletion manifest -> B10 -> terminal completion -> external qualification"
    execution["terminal_completion_writer"] = "python scripts/write_whole_bible_terminal_completion_receipt.py"
    execution["durability_command"] = "python -m scripts.validate_whole_bible_stage_receipts --book <Book> --run-id <run_id> --require-complete --require-terminal"
    replay = campaign["replay_contract"]
    for key, relative in (("workflow", WORKFLOW), ("prompt_pack", PROMPTS), ("runtime_adapter", ADAPTER)):
        replay[key]["digest"] = digest(relative)
    jobs = campaign["phases"][0]["waves"][0]["subwaves"][0]["jobs"]
    for job in jobs[:-1]:
        book = Path(job["checkpoint"]).stem
        job["idempotency_key"] = f"T521-M7-sol:{book}:workflow-1.2.0:<run_id>"
        job["run_id_binding"] = "required_at_dispatch"
        job["attempt_ids_are_stage_local"] = True
        if book == "Num":
            lev_v2 = f"{MODEL}/receipts/Lev_completion_v2.json"
            job["dependency_digests"]["J-003-LEV"] = f"precontract_snapshot_waiver:Lev_completion_v2:{digest(lev_v2)}"
        stage_paths: list[str] = []
        manifests: list[str] = []
        for row in job["stage_plan"]:
            stage = row["stage_id"]
            receipt = f"{MODEL}/state/books/{book}/runs/<run_id>/stages/{stage}/<attempt_id>.json"
            row["receipt"] = receipt
            row["input_manifest"] = f"{MODEL}/state/books/{book}/runs/<run_id>/manifests/{stage}.input.json"
            row["output_manifest"] = f"{MODEL}/state/books/{book}/runs/<run_id>/manifests/{stage}.output.json"
            stage_paths.append(receipt); manifests.extend([row["input_manifest"], row["output_manifest"]])
        job["stage_receipts"] = stage_paths
        terminal = f"{MODEL}/receipts/{book}_completion_v3.<run_id>.json"
        extended = f"{MODEL}/state/books/{book}/runs/<run_id>/extended_evidence_manifest.precompletion.json"
        run_index = f"{MODEL}/state/books/{book}/runs/<run_id>/run_index.json"
        run_log = f"{MODEL}/state/books/{book}/runs/<run_id>/receipts.jsonl"
        gate_bundle = f"{MODEL}/state/books/{book}/runs/<run_id>/completion_gate_bundles/<attempt_id>.json"
        gate_evidence = [f"{MODEL}/state/books/{book}/runs/<run_id>/gate_evidence/<attempt_id>/{gate_id}.stdout" for gate_id in ("exact_coverage", "official_chunk_map_schema", "review_packet_parity", "literary_quality", "workflow_replay_contract", "materialized_stage_chain_precompletion")]
        boss_a = f"{MODEL}/state/books/{book}/runs/<run_id>/boss_phases/provisional_B06a/<attempt_id>.json"
        boss_b = f"{MODEL}/state/books/{book}/runs/<run_id>/boss_phases/final_B06b/<attempt_id>.json"
        preflight_outputs = [
            f"{MODEL}/state/books/{book}/runs/<run_id>/preflight/campaign_projection.json",
            f"{MODEL}/state/books/{book}/runs/<run_id>/preflight/preflight_report.json",
            f"{MODEL}/state/books/{book}/runs/<run_id>/preflight/dependency_evidence.json",
            f"{MODEL}/state/books/{book}/runs/<run_id>/drafts/B00.<attempt_id>.json",
        ]
        disposition_outputs = [f"{MODEL}/reviews/{book}/appeal_disposition.json", f"{MODEL}/reviews/{book}/hold_disposition.json"]
        by_stage = {row["stage_id"]: row for row in job["stage_plan"]}
        by_stage["B00"]["required_artifacts"] = preflight_outputs[:3]
        by_stage["B07"]["required_artifacts"] = [disposition_outputs[0]]
        by_stage["B09"]["required_artifacts"] = [disposition_outputs[1]]
        old_completion = f"{MODEL}/receipts/{book}_completion_v2.json"
        outputs = [terminal if value == old_completion else value for value in job["outputs"] if "/state/books/" not in value or "/stages/" not in value]
        for value in stage_paths + manifests + gate_evidence + preflight_outputs + disposition_outputs + [extended, run_index, run_log, gate_bundle, boss_a, boss_b, terminal]: add_unique(outputs, value)
        job["outputs"] = outputs
        allowed = [terminal if value == old_completion else value for value in job["allowed_paths"] if "/state/books/" not in value or "/stages/" not in value]
        for value in outputs: add_unique(allowed, value)
        job["allowed_paths"] = allowed
        job["qualification_evidence"] = [f"{MODEL}/state/evidence/qualifications/{book}.<run_id>.json"]
        command = f"python -m scripts.validate_whole_bible_stage_receipts --book {book} --run-id <run_id> --require-complete --require-terminal"
        old_command = job["durability_check"]; job["durability_check"] = command
        for gate in job["acceptance"]:
            if gate.get("command") == old_command: gate["command"] = command
        for relative in HARNESS_INPUTS:
            add_unique(job["inputs"], relative); job["input_digests"][relative] = digest(relative)
        for relative in (WORKFLOW, PROMPTS, ADAPTER):
            job["input_digests"][relative] = digest(relative)
        for relative in job["inputs"]:
            if relative != CAMPAIGN.relative_to(ROOT).as_posix() and (ROOT / relative).is_file():
                job["input_digests"][relative] = digest(relative)
    merge = jobs[-1]
    merge["idempotency_key"] = "T521-M7-sol:merge:workflow-1.2.0:<campaign_run_id>"
    merge["book_run_id_resolution_required_at_dispatch"] = True
    new_inputs: list[str] = []; new_digests: dict[str, str] = {}
    for relative in merge["inputs"]:
        if relative.endswith("_completion_v2.json"):
            prefix = relative.removesuffix("_completion_v2.json")
            book = prefix.rsplit("/", 1)[-1]
            value = prefix + "_completion_v3.<book_run_id>.json"
            new_inputs.append(value); new_digests[value] = f"terminal_book_completion_receipt:{book}.sha256"
        else:
            new_inputs.append(relative); new_digests[relative] = merge["input_digests"][relative]
    merge["inputs"], merge["input_digests"] = new_inputs, new_digests
    payload = (json.dumps(campaign, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    temporary = CAMPAIGN.with_name(CAMPAIGN.name + f".tmp-{os.getpid()}")
    with temporary.open("xb") as handle: handle.write(payload); handle.flush(); os.fsync(handle.fileno())
    os.replace(temporary, CAMPAIGN)
    print("Upgraded campaign to replay contract revision 6.")
    return 0

if __name__ == "__main__": raise SystemExit(main())
