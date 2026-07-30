#!/usr/bin/env python3
"""One-time fail-closed migration from shell-chained book gates to the bundle."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
CAMPAIGN = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol" / "campaign.json"
EXPECTED = "fe0f2f2fb1d9187a768392fa9a4da8c58b384a928d30cac9aece793ab15a77e2"
BUNDLE = ".ai/scratch/multi_model_bible_chunking/M7_sol/checks/validate_book_completion_bundle.py"


def main() -> int:
    actual = hashlib.sha256(CAMPAIGN.read_bytes()).hexdigest()
    if actual != EXPECTED:
        raise SystemExit(f"refusing campaign migration: expected {EXPECTED}, found {actual}")
    campaign = json.loads(CAMPAIGN.read_text(encoding="utf-8"))
    jobs = campaign["phases"][0]["waves"][0]["subwaves"][0]["jobs"]
    if len(jobs) != 67 or not jobs[-1]["id"].endswith("MERGE"):
        raise SystemExit("expected 66 canonical book jobs followed by one merge job")

    campaign["revision"] = 3
    campaign["execution"]["durability_command"] = f"python {BUNDLE} --book <Book>"
    completion_evidence = campaign.setdefault("completion_evidence", [])
    if BUNDLE not in completion_evidence:
        completion_evidence.append(BUNDLE)

    migrated = 0
    for job in jobs[:-1]:
        checkpoint = job.get("checkpoint", "")
        match = re.fullmatch(r".*/books/([^/]+)\.json", checkpoint)
        if not match:
            raise SystemExit(f"cannot derive book from checkpoint for {job.get('id')}")
        book = match.group(1)
        bundle_command = f"python {BUNDLE} --book {book}"
        job["durability_check"] = bundle_command
        if BUNDLE not in job["inputs"]:
            job["inputs"].append(BUNDLE)
        job["input_digests"][BUNDLE] = "sha256:verified-at-book-job-start"

        chained = [
            gate for gate in job["acceptance"]
            if isinstance(gate.get("command"), str) and ";" in gate["command"]
        ]
        if len(chained) != 1:
            raise SystemExit(f"{job['id']}: expected exactly one chained acceptance gate")
        gate = chained[0]
        gate["id"] = f"G-{book}-COMPLETION-BUNDLE"
        gate["revision"] = "2"
        gate["command"] = bundle_command
        gate["evidence"] = (
            f".ai/scratch/multi_model_bible_chunking/M7_sol/state/evidence/books/"
            f"{book}-completion-bundle.json"
        )
        if BUNDLE not in gate["inputs"]:
            gate["inputs"].append(BUNDLE)
        gate["revalidation_triggers"] = list(dict.fromkeys(gate["revalidation_triggers"] + [
            "completion bundle revision change",
            "postcheck or completion receipt change",
        ]))
        migrated += 1

    forbidden = (";", "&&", "||", "|", ">", "<", "\n", "\r")
    for job in jobs[:-1]:
        values = [job.get("durability_check", "")] + [
            gate.get("command", "") for gate in job.get("acceptance", [])
        ]
        for value in values:
            if value == "not-applicable":
                continue
            if any(token in value for token in forbidden):
                raise SystemExit(f"{job['id']}: unsafe shell composition remains in {value!r}")

    if migrated != 66:
        raise SystemExit(f"expected 66 migrated book gates, found {migrated}")
    CAMPAIGN.write_text(
        json.dumps(campaign, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print("migrated 66 book jobs to fail-fast completion bundles; merge job unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
