#!/usr/bin/env python3
"""Bind the human-copy reviewer prompt into the external packet index."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/state/evidence/final/external_review_packet_index.json"
PROMPT = ROOT / "docs/governance/T521_EXTERNAL_REVIEWER_COPY_PASTE_PROMPT.md"


def main() -> int:
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    index["reviewer_copy_prompt"] = {
        "path": str(PROMPT),
        "sha256": "sha256:" + hashlib.sha256(PROMPT.read_bytes()).hexdigest(),
    }
    index["allowed_inputs"] = list(dict.fromkeys(index.get("allowed_inputs", []) + [str(PROMPT)]))
    index["external_review_receipt_schema"] = "config/agents/families/scripture-first-biblical-chunking/t521_external_review_receipt.schema.v1.json"
    INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"packet_index": str(INDEX), "reviewer_prompt_sha256": index["reviewer_copy_prompt"]["sha256"], "candidate_only": True, "non_authorizing": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
