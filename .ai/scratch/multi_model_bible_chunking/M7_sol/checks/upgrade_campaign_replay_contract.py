#!/usr/bin/env python3
"""One-time upgrade of the M7 campaign to replay-contract revision 4."""
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
EXPECTED = "0a812cc515aa63d29174cfd5e4ad20df7ab366a4f66987e53887bdf764a22ea7"
WORKFLOW = "config/agents/families/scripture-first-biblical-chunking/whole_bible_candidate_workflow.v1.yaml"
PROMPTS = "config/agents/families/scripture-first-biblical-chunking/whole_bible_candidate_prompt_pack.v1.yaml"
ADAPTER = "config/agents/families/scripture-first-biblical-chunking/codex_desktop_campaign_adapter.v1.yaml"
TRANSLATION = "data/canonical/translations/eng-web/translation_witnesses.jsonl"
OBSERVATION = "build/observation_substrate/current/scan_manifest.json"
OT_SOURCES = (
    "data/raw/original_language/hebrew/openscriptures_oshb/source_manifest.yaml",
    "data/raw/original_language/hebrew/tanach_us_uxlc/source_manifest.yaml",
)
NT_SOURCES = (
    "data/raw/original_language/greek/sblgnt/source_manifest.yaml",
    "data/raw/original_language/greek/cntr_sr/source_manifest.yaml",
    "data/raw/original_language/greek/ugnt/source_manifest.yaml",
)
STAGES = tuple(f"B{index:02d}" for index in range(11))
STAGE_PROMPTS = {
    "B00": [],
    "B01": [
        "original_language_translation_scout",
        "literary_form_scout",
        "canonical_relations_and_premortem_scout",
        "second_temple_rabbinic_context_scout",
    ],
    "B02": ["root_author_candidate_map"],
    "B03": [],
    "B04": ["original_language_primary_review", "literary_primary_review"],
    "B05": ["peer_crosscheck", "premortem_review"],
    "B06": ["evidence_dispute_boss"],
    "B07": ["appeal_response"],
    "B08": [
        "root_author_candidate_map",
        "original_language_primary_review",
        "literary_primary_review",
    ],
    "B09": ["final_post_resolution_check"],
    "B10": [],
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def main() -> int:
    actual = digest(CAMPAIGN)
    if actual != EXPECTED:
        raise SystemExit(f"refusing replay migration: expected {EXPECTED}, found {actual}")
    campaign = json.loads(CAMPAIGN.read_text(encoding="utf-8"))
    canon = yaml.safe_load(CANON.read_text(encoding="utf-8"))["canonical_66_books"]
    jobs = campaign["phases"][0]["waves"][0]["subwaves"][0]["jobs"]
    if len(canon) != 66 or len(jobs) != 67 or not jobs[-1]["id"].endswith("MERGE"):
        raise SystemExit("campaign/canon topology mismatch")

    campaign["revision"] = 4
    campaign["execution"].update({
        "mode": "specification_only",
        "workflow_ref": WORKFLOW,
        "prompt_pack_ref": PROMPTS,
        "runtime_adapter_ref": ADAPTER,
        "stage_receipt_contract_ref": f"{WORKFLOW}#stage_receipt_contract",
        "input_digest_strategy": "real_sha256_for_files_and_B00_receipt_for_campaign_self",
        "qualification_status": "blocked_pending_stage_receipt_harness_and_one_book_dry_replay",
        "launch_command": "not-authorized",
    })
    campaign["replay_contract"] = {
        "workflow": {"path": WORKFLOW, "digest": f"sha256:{digest(ROOT / WORKFLOW)}"},
        "prompt_pack": {"path": PROMPTS, "digest": f"sha256:{digest(ROOT / PROMPTS)}"},
        "runtime_adapter": {"path": ADAPTER, "digest": f"sha256:{digest(ROOT / ADAPTER)}"},
        "all_book_jobs_have_unique_idempotency_keys": True,
        "all_book_jobs_instantiate_B00_through_B10": True,
        "qualification_is_not_activation": True,
        "unattended_launch_authorized": False,
    }
    campaign["authority"]["human_gates"] = [
        "authority or theology decision",
        "unresolved reasoned appeal blocks promotion and convergence but not the next canonical book",
        "scope expansion",
        "promotion or publication",
    ]
    campaign["authority"]["appeal_progression"] = {
        "preserve_append_only": True,
        "blocks_promotion_and_convergence": True,
        "does_not_block_next_book": True,
    }

    source_authority = campaign.setdefault("source_authority", [])
    by_path = {row.get("path"): row for row in source_authority if isinstance(row, dict)}
    for path in (*OT_SOURCES, *NT_SOURCES):
        by_path[path] = {"path": path, "digest": f"sha256:{digest(ROOT / path)}"}
    campaign["source_authority"] = list(by_path.values())

    ot_books = set(canon[:39])
    for expected_index, job in enumerate(jobs[:-1], 1):
        checkpoint = str(job.get("checkpoint", ""))
        match = re.fullmatch(r".*/books/([^/]+)[.]json", checkpoint)
        if not match:
            raise SystemExit(f"{job.get('id')}: malformed checkpoint")
        book = match.group(1)
        if book != canon[expected_index - 1]:
            raise SystemExit(f"{job.get('id')}: noncanonical book order")

        source_inputs = list(OT_SOURCES if book in ot_books else NT_SOURCES)
        old_inputs = [
            value
            for value in job.get("inputs", [])
            if isinstance(value, str) and not value.endswith("/")
        ]
        inputs = unique(old_inputs + [OBSERVATION, WORKFLOW, PROMPTS, ADAPTER, *source_inputs])
        job["inputs"] = inputs
        input_digests: dict[str, str] = {}
        for value in inputs:
            if value == CAMPAIGN.relative_to(ROOT).as_posix():
                input_digests[value] = "stage_receipt:B00.input_artifact_sha256.campaign"
                continue
            path = ROOT / value
            if not path.is_file():
                raise SystemExit(f"{job['id']}: immutable input is absent or not a file: {value}")
            input_digests[value] = f"sha256:{digest(path)}"
        job["input_digests"] = input_digests
        job["idempotency_key"] = f"T521-M7-sol:{book}:workflow-1.1.0"
        job["workflow_ref"] = WORKFLOW
        job["prompt_pack_ref"] = PROMPTS
        job["runtime_adapter_ref"] = ADAPTER
        job["source_route"] = {
            "testament": "old" if book in ot_books else "new",
            "original_language": "hebrew_aramaic" if book in ot_books else "koine_greek",
            "manifest_paths": source_inputs,
            "ancient_context_default": "corpus_gap_unless_qualified_and_pinned",
        }
        job["stage_plan"] = [
            {
                "stage_id": stage,
                "prompt_template_ids": STAGE_PROMPTS[stage],
                "receipt": (
                    f".ai/scratch/multi_model_bible_chunking/M7_sol/state/books/"
                    f"{book}/stages/{stage}.json"
                ),
            }
            for stage in STAGES
        ]
        job["stage_receipts"] = [row["receipt"] for row in job["stage_plan"]]
        job["qualification_evidence_status"] = "required_missing_blocks_launch"
        review_root = f".ai/scratch/multi_model_bible_chunking/M7_sol/reviews/{book}"
        explicit_outputs = [
            f".ai/scratch/multi_model_bible_chunking/M7_sol/book_strategy/{book}.md",
            f".ai/scratch/multi_model_bible_chunking/M7_sol/book_chunks/{book}/chunks.jsonl",
            f"{review_root}/review_packets.jsonl",
            f"{review_root}/book_difficulty.md",
            f"{review_root}/freeze_receipt_v1.json",
            f"{review_root}/primary_original_language.json",
            f"{review_root}/primary_literary.json",
            f"{review_root}/peer_crosscheck.json",
            f"{review_root}/premortem.json",
            f"{review_root}/boss_provisional.json",
            f"{review_root}/boss_rulings.json",
            f"{review_root}/appeals.jsonl",
            f"{review_root}/decision_relations.jsonl",
            f"{review_root}/no_decision_relations_v1.json",
            f"{review_root}/lineage.jsonl",
            f"{review_root}/source_gap_register.json",
            f"{review_root}/role_separated_checker_verdict_v1.json",
            f"{review_root}/post_resolution_check_v2.json",
            f".ai/scratch/multi_model_bible_chunking/M7_sol/receipts/{book}_completion_v2.json",
            *job["stage_receipts"],
        ]
        job["outputs"] = unique(explicit_outputs)
        job["allowed_paths"] = unique(job.get("allowed_paths", []) + explicit_outputs)
        job["required_output_alternatives"] = [
            {
                "one_of": [
                    f"{review_root}/decision_relations.jsonl",
                    f"{review_root}/no_decision_relations_v1.json",
                ]
            }
        ]
        job["shared_write_contract"] = {
            "shared_sidecars": [
                ".ai/scratch/multi_model_bible_chunking/M7_sol/low_confidence_register.jsonl",
                ".ai/scratch/multi_model_bible_chunking/M7_sol/frontier_escalation_queue.jsonl",
                ".ai/scratch/multi_model_bible_chunking/M7_sol/atlas_candidate_feed.jsonl",
            ],
            "exclusive_lock_required": True,
            "atomic_replace_required": True,
            "concurrent_book_writes_forbidden": True,
        }

    state = MODEL / "state"
    (state / "books").mkdir(parents=True, exist_ok=True)
    (state / "evidence" / "qualifications").mkdir(parents=True, exist_ok=True)
    readme = state / "README.md"
    if not readme.exists():
        readme.write_text(
            "# M7 replay state\n\n"
            "This state root is initialized but not qualified for unattended execution. "
            "Each book must produce B00-B10 hash-linked receipts and a one-book dry replay "
            "must pass before launch authorization. Missing qualification evidence is a block, "
            "not an implicit pass.\n",
            encoding="utf-8",
            newline="\n",
        )

    CAMPAIGN.write_text(
        json.dumps(campaign, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print("upgraded 66 book jobs to replay-contract revision 4; launch remains blocked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())