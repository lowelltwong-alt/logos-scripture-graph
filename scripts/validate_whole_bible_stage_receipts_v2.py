#!/usr/bin/env python3
"""Validate the selected revision-7 B00/B01 receipt chain."""
from __future__ import annotations

import argparse
import json
import sys

from scripts import whole_bible_replay_evidence_v2 as core
from scripts import write_whole_bible_stage_receipt_v2 as writer


def validate_run(*, book: str, run_id: str, require_through: str = "B00") -> dict:
    if require_through not in core.AUTHORIZED_STAGES:
        raise core.ReplayEvidenceError("QF-21-UNMIGRATED-STAGE", "revision 7 supports only B00/B01")
    core.validate_runtime_contract()
    campaign = core.load_json(core.CAMPAIGN)
    directory = core.run_dir(core.MODEL_ROOT, book, run_id)
    index = core.read_index(directory, campaign, book, run_id)
    required = core.AUTHORIZED_STAGES[:core.AUTHORIZED_STAGES.index(require_through) + 1]
    selected = index["selected"]
    if any(stage not in selected for stage in required):
        raise core.ReplayEvidenceError("QF-01-PLAN-NOT-RUN", f"missing selected receipt through {require_through}")
    if set(selected) - set(core.AUTHORIZED_STAGES):
        raise core.ReplayEvidenceError("QF-21-UNMIGRATED-STAGE", "unmigrated stage selected in revision 7")
    receipts = []
    prior_sha = None
    for stage_id in core.AUTHORIZED_STAGES:
        if stage_id not in selected:
            break
        ref = selected[stage_id]
        receipt_path = core.resolve_repo_path(ref["path"])
        expected_receipt_path = directory / "stages" / stage_id / f"{ref['attempt_id']}.json"
        if receipt_path.resolve() != expected_receipt_path.resolve():
            raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", f"selected {stage_id} receipt path is non-canonical")
        if not receipt_path.is_file() or core.digest_file(receipt_path) != ref.get("sha256"):
            raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", f"selected {stage_id} receipt stale")
        receipt = core.load_json(receipt_path)
        base = core.attempt_root(core.MODEL_ROOT, book, run_id, stage_id, ref["attempt_id"])
        candidate, _, _ = writer._build_candidate(
            draft_path=base / "draft.json", campaign_path=core.CAMPAIGN, registry_path=core.REGISTRY,
            model_root=core.MODEL_ROOT, root=core.ROOT, allow_selected_validation=True,
        )
        prepared = core.load_json(base / "prepared_commit.json")
        if receipt != candidate or prepared.get("candidate_receipt") != receipt or prepared.get("candidate_receipt_sha256") != core.digest_bytes(core.canonical_bytes(receipt)):
            raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", f"selected {stage_id} differs from prepared candidate")
        if receipt.get("prior_stage_receipt_sha256") != prior_sha:
            raise core.ReplayEvidenceError("QF-02-FORGED-CHAIN", f"selected {stage_id} predecessor chain")
        expected_log = {"schema_version": "whole_bible_stage_receipt_log.v2", "campaign_id": campaign["campaign_id"], "book": book, "run_id": run_id, "stage_id": stage_id, "attempt_id": ref["attempt_id"], "receipt_path": core.repo_relative(receipt_path), "receipt_sha256": ref["sha256"], "outcome": receipt["outcome"], "non_authorizing": True}
        identity_keys = ("campaign_id", "book", "run_id", "stage_id", "attempt_id")
        for log_path in (directory / "receipts.v2.jsonl", core.MODEL_ROOT / "state" / "receipts.v2.jsonl"):
            matches = [row for row in core.load_v2_receipt_log(log_path) if tuple(row[key] for key in identity_keys) == tuple(expected_log[key] for key in identity_keys)]
            if matches != [expected_log]:
                raise core.ReplayEvidenceError("QF-LOG-PARITY", f"selected {stage_id} receipt log parity")
        prior_sha = ref["sha256"]
        receipts.append({"stage_id": stage_id, "attempt_id": ref["attempt_id"], "receipt_sha256": ref["sha256"]})
    return {
        "schema_version": "whole_bible_stage_chain_validation.v2", "book": book, "run_id": run_id,
        "campaign_revision": 7, "selected": receipts,
        "first_missing_stage": next((stage for stage in core.AUTHORIZED_STAGES if stage not in selected), "B01_unmigrated"),
        "B02_authorized": False, "replay_qualified": False, "launch_qualified": False,
        "non_authorizing": True,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--require-through", choices=core.AUTHORIZED_STAGES, default="B00")
    args = parser.parse_args(argv)
    try:
        result = validate_run(book=args.book, run_id=args.run_id, require_through=args.require_through)
    except core.ReplayEvidenceError as exc:
        print(f"V2 chain validation failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
