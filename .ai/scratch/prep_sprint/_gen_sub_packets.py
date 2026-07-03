#!/usr/bin/env python3
"""One-off generator for SUB-009..SUB-011 promotion packets."""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent.parent.parent

PACKETS = {
    "SUB-009": {
        "requested_promotion": "prep_artifacts_only",
        "title": "Phase 6 reviewed gold promotion PREP (33 candidates)",
        "artifact_glob": ".ai/context/agent_work/T417/reviewed_gold_promotion_prep/*_gold_promotion_prep.yaml",
        "evidence": ".ai/context/agent_work/T417/reviewed_gold_promotion_prep/",
        "medium_risk": "gold_prep_may_read_like_t414_without_owner_gate",
    },
    "SUB-010": {
        "requested_promotion": "prep_artifacts_only",
        "title": "Phase 7 route isolation harness PREP (9 batches)",
        "artifact_glob": ".ai/context/agent_work/T417/route_harness_prep/*_route_harness_prep.yaml",
        "evidence": ".ai/context/agent_work/T417/route_harness_prep/",
        "medium_risk": "harness_prep_references_executable_script_without_running_it",
    },
    "SUB-011": {
        "requested_promotion": "prep_artifacts_only",
        "title": "Phase 8 output pilot PREP (33 candidates)",
        "artifact_glob": ".ai/context/agent_work/T417/output_pilot_prep/*_output_pilot_prep.yaml",
        "evidence": ".ai/context/agent_work/T417/output_pilot_prep/",
        "medium_risk": "output_prep_may_read_like_t415_manifest_without_hashes",
    },
}


def rels(glob: str) -> list[str]:
    return sorted(p.relative_to(ROOT).as_posix() for p in ROOT.glob(glob))


def main() -> None:
    for sid, meta in PACKETS.items():
        files = rels(meta["artifact_glob"])
        body = {
            "object_type": "promotion_packet",
            "schema_version": "promotion_packet.v1",
            "submission_id": sid,
            "source_branch": "scratch/phase-ladder-678",
            "source_worktree": "../logos-scratch",
            "target_task_id": "T417",
            "status": "draft_pending_codex_promotion_review",
            "risk_summary": {
                "high": [],
                "medium": [meta["medium_risk"]],
                "low": ["batch1_output_candidates_skipped_by_design"],
            },
            "decisions": [
                {
                    "decision_id": "D-001",
                    "choice": meta["title"],
                    "rationale": (
                        "Scratch lane pre-builds governed ladder prep under agent_work only; "
                        "no eval/chunking_gold or chunk output"
                    ),
                    "alternatives_rejected": [
                        "Write directly to eval/chunking_gold",
                        "Run route isolation harness in scratch",
                        "Regenerate chunk output for overlay hashes",
                    ],
                    "might_be_wrong": (
                        "Codex may HOLD if prep implies authority from standing phrase alone"
                    ),
                    "confidence": "medium",
                }
            ],
            "evidence_refs": [
                ".ai/scratch/prep_sprint/scratch_phase_ladder_queue.yaml",
                meta["evidence"],
                ".ai/control/t415_batch1_output_pilot_manifest.yaml",
            ],
            "validators_run_in_scratch": [
                "python .ai/scratch/prep_sprint/run_phase_ladder.py --validate-only",
                f"python scripts/validate_promotion_packet.py --packet .ai/scratch/submissions/{sid}/promotion_packet.yaml",
            ],
            "requested_promotion": meta["requested_promotion"],
            "non_authorizations": [
                "reviewed_gold_promotion",
                "chunk_output_change",
                "child_span_selection",
                "standing_policy_activation",
                "harness_execution_in_scratch",
                "ladder_auto_unlock_from_standing_phrase",
            ],
            "reviewer_notes_for_codex": (
                f"{meta['title']}. All artifacts keep explicit false authorizations and live "
                "under agent_work only. Owner APPROVE_STANDING_ESCALATION_POLICY plus per-step "
                "Codex gates still required."
            ),
            "files_promoted": [
                ".ai/scratch/prep_sprint/scratch_phase_ladder_queue.yaml",
                ".ai/scratch/prep_sprint/run_phase_ladder.py",
                *files,
            ],
            "vendor_imports": [],
        }
        out_dir = ROOT / ".ai/scratch/submissions" / sid
        out_dir.mkdir(parents=True, exist_ok=True)
        header = "---\nobject_type: promotion_packet\nschema_version: promotion_packet.v1\n---\n"
        (out_dir / "promotion_packet.yaml").write_text(
            header + yaml.safe_dump(body, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
        print(f"{sid}: {len(files)} artifact files")


if __name__ == "__main__":
    main()
