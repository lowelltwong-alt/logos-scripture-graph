#!/usr/bin/env python3
"""One-time revision-5 repair for merge, form, appeal, and qualification semantics."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[5]
MODEL = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol"
CAMPAIGN = MODEL / "campaign.json"
CANON = ROOT / "config" / "canon" / "canonical_66_books.yaml"
EXPECTED = "8cb42edcc8413a443e57d1914fa609074481ca63046354d69a674523c41ae256"
CAMPAIGN_REF = ".ai/scratch/multi_model_bible_chunking/M7_sol/campaign.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    actual = digest(CAMPAIGN)
    if actual != EXPECTED:
        raise SystemExit(f"refusing revision-5 migration: expected {EXPECTED}, found {actual}")
    campaign = json.loads(CAMPAIGN.read_text(encoding="utf-8"))
    canon = yaml.safe_load(CANON.read_text(encoding="utf-8"))["canonical_66_books"]
    jobs = campaign["phases"][0]["waves"][0]["subwaves"][0]["jobs"]
    if campaign.get("revision") != 4 or len(jobs) != 67 or len(canon) != 66:
        raise SystemExit("revision-4 campaign topology required")

    campaign["revision"] = 5
    campaign["execution"]["qualification_status"] = (
        "blocked_pending_stage_receipts_dry_replay_form_inventory_primary_freshness_"
        "extended_closure_and_independent_launch_review"
    )
    campaign["replay_contract"].update({
        "merge_inputs_are_receipt_resolved_not_directory_placeholders": True,
        "form_inventory_is_B01_hash_bound": True,
        "appeals_block_promotion_not_next_book": True,
        "primary_role_freshness_and_extended_closure_required_for_qualification": True,
    })

    blocked_human = (
        "a theology, reading, canon, tradition, authority, security, privacy, "
        "or scope decision requires a human; an ordinary preserved boundary appeal "
        "is pass_with_holds and does not stop the next book"
    )
    pass_with_holds = (
        "mechanical candidate snapshot passes with preserved appeals or specialist "
        "holds; promotion and convergence remain blocked while the next book may proceed"
    )

    for job in jobs[:-1]:
        match = re.fullmatch(r".*/books/([^/]+)[.]json", str(job.get("checkpoint", "")))
        if not match:
            raise SystemExit(f"{job.get('id')}: malformed checkpoint")
        book = match.group(1)
        review_root = f".ai/scratch/multi_model_bible_chunking/M7_sol/reviews/{book}"
        form_inventory = f"{review_root}/form_inventory.json"
        if form_inventory not in job["outputs"]:
            job["outputs"].append(form_inventory)
        if form_inventory not in job["allowed_paths"]:
            job["allowed_paths"].append(form_inventory)
        job["form_inventory_artifact"] = form_inventory
        b01 = next(row for row in job["stage_plan"] if row["stage_id"] == "B01")
        b01["required_artifacts"] = [
            form_inventory,
            f".ai/scratch/multi_model_bible_chunking/M7_sol/book_strategy/{book}.md",
            f"{review_root}/book_difficulty.md",
            f"{review_root}/source_gap_register.json",
        ]
        for gate in job.get("acceptance", []):
            semantics = gate.setdefault("result_semantics", {})
            semantics["pass_with_holds"] = pass_with_holds
            semantics["blocked_human"] = blocked_human
        conditions = job.get("escalation", {}).get("conditions", [])
        job["escalation"]["conditions"] = [
            (
                "reasoned appeal remains for promotion/convergence queue; "
                "record it and continue to the next book"
                if value == "reasoned appeal remains"
                else value
            )
            for value in conditions
        ]

    merge = jobs[-1]
    completion_receipts = [
        f".ai/scratch/multi_model_bible_chunking/M7_sol/receipts/{book}_completion_v2.json"
        for book in canon
    ]
    merge_inputs = [
        CAMPAIGN_REF,
        ".ai/scratch/multi_model_bible_chunking/M7_sol/model_manifest.yaml",
        "scripts/t423_merge_book_chunks.py",
        "scripts/validate_whole_bible_chunk_map.py",
        *completion_receipts,
    ]
    merge["inputs"] = merge_inputs
    merge["input_digests"] = {
        CAMPAIGN_REF: "stage_receipt:MERGE.input_artifact_sha256.campaign",
        ".ai/scratch/multi_model_bible_chunking/M7_sol/model_manifest.yaml": (
            f"sha256:{digest(MODEL / 'model_manifest.yaml')}"
        ),
        "scripts/t423_merge_book_chunks.py": f"sha256:{digest(ROOT / 'scripts/t423_merge_book_chunks.py')}",
        "scripts/validate_whole_bible_chunk_map.py": (
            f"sha256:{digest(ROOT / 'scripts/validate_whole_bible_chunk_map.py')}"
        ),
        **{
            receipt: f"book_completion_receipt:{book}.sha256"
            for book, receipt in zip(canon, completion_receipts, strict=True)
        },
    }
    merge["idempotency_key"] = "T521-M7-sol:merge:workflow-1.1.0"
    merge["merge_input_resolution_required_at_dispatch"] = True
    merge["merge_requires_all_book_receipts_hash_valid"] = True
    for gate in merge.get("acceptance", []):
        semantics = gate.setdefault("result_semantics", {})
        semantics["pass_with_holds"] = pass_with_holds
        semantics["blocked_human"] = blocked_human

    for stop in campaign.get("stop_conditions", []):
        if stop.get("code") == "human_gate_required":
            stop["detection"] = (
                "an authority, theology, reading, canon, tradition, security, privacy, "
                "or scope decision requires human authorization; ordinary preserved "
                "boundary appeals enter the promotion queue without stopping the next book"
            )
            stop["shutdown"] = "block only the unauthorized effect or affected promotion"
        elif stop.get("code") == "validation_inconclusive":
            stop["detection"] = (
                "a deterministic or role-separated gate lacks pass or pass_with_holds"
            )

    CAMPAIGN.write_text(
        json.dumps(campaign, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print("upgraded campaign to revision 5 with receipt-resolved merge and consistent hold semantics")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())