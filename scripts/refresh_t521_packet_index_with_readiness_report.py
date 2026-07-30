#!/usr/bin/env python3
"""Bind the current fidelity-readiness report into the external packet index."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/state/evidence/final/external_review_packet_index.json"
REPORT = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/state/evidence/final/fidelity_readiness_report.json"


def main() -> int:
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    index["fidelity_readiness_report"] = {
        "path": str(REPORT),
        "sha256": "sha256:" + hashlib.sha256(REPORT.read_bytes()).hexdigest(),
        "disclosure": "candidate process/readiness evidence; not independent literary validation",
    }
    index["allowed_inputs"] = list(dict.fromkeys(index.get("allowed_inputs", []) + [str(REPORT)]))
    INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"packet_index": str(INDEX), "readiness_report_sha256": index["fidelity_readiness_report"]["sha256"], "candidate_only": True, "non_authorizing": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
