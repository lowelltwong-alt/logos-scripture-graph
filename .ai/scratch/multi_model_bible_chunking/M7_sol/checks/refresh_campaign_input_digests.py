#!/usr/bin/env python3
"""Refresh revision-4 external input digests without pretending to self-hash campaign.json."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
CAMPAIGN = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol" / "campaign.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    campaign = json.loads(CAMPAIGN.read_text(encoding="utf-8"))
    if campaign.get("revision") not in {4, 5}:
        raise SystemExit("digest refresh requires campaign revision 4 or 5")
    campaign_ref = CAMPAIGN.relative_to(ROOT).as_posix()
    jobs = campaign["phases"][0]["waves"][0]["subwaves"][0]["jobs"]
    refreshed = 0
    for job in jobs[:-1]:
        recorded: dict[str, str] = {}
        for value in job.get("inputs", []):
            if value == campaign_ref:
                recorded[value] = "stage_receipt:B00.input_artifact_sha256.campaign"
            else:
                path = ROOT / value
                if not path.is_file():
                    raise SystemExit(f"{job.get('id')}: missing input {value}")
                recorded[value] = f"sha256:{digest(path)}"
        if job.get("input_digests") != recorded:
            refreshed += 1
        job["input_digests"] = recorded

    for field in ("workflow", "prompt_pack", "runtime_adapter"):
        record = campaign["replay_contract"][field]
        path = ROOT / record["path"]
        record["digest"] = f"sha256:{digest(path)}"

    campaign["input_digest_refresh"] = {
        "strategy": "real_sha256_for_external_files",
        "campaign_self": "deferred_to_B00_stage_receipt",
        "book_jobs_refreshed": refreshed,
        "non_authorizing": True,
    }
    CAMPAIGN.write_text(
        json.dumps(campaign, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"refreshed external input digests for {refreshed} changed book jobs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())