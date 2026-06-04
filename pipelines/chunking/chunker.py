#!/usr/bin/env python3
"""Bible chunker v0 (CHK-4 fix: joins passages + translation witnesses).

This v0 implementation is intentionally conservative:
- joins ScripturePassage records with TranslationWitness text by passage_id
- groups verse records into sentence-safe chunks
- never crosses books
- records boundary basis and policy version
- never mutates source text; reads clean witness text only

NOT YET (Sprint 3, boundary-driven chunker): genre policy, BoundaryClaim
consumption, poetry/psalm units, ContextPacket generation. See CHUNKING_DESIGN.md.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_POLICY = ROOT / "config" / "chunking" / "chunking_policy.yaml"

SENTENCE_END_RE = re.compile(r"[.!?][\"')\]]*$")


def read_policy_version(policy_path: Path) -> str:
    """Dependency-light read of the `version:` field from the policy YAML."""
    try:
        for line in policy_path.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("version:"):
                return line.split(":", 1)[1].strip().strip('"').strip("'")
    except OSError:
        pass
    return "chunk-policy-unknown"


def approx_tokens(text: str) -> int:
    return max(1, len(text.split()))


def sentence_ended(text: str) -> bool:
    return bool(SENTENCE_END_RE.search(text.strip()))


def load_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def load_witness_text(witnesses_path: Path) -> dict[str, str]:
    """Map passage_id -> clean witness text."""
    text_by_passage: dict[str, str] = {}
    for record in load_jsonl(witnesses_path):
        passage_id = record.get("passage_id")
        if passage_id:
            text_by_passage[passage_id] = record.get("text", "")
    return text_by_passage


def make_chunk(buffer, chunk_index: int, policy_version: str) -> dict:
    first, last = buffer[0], buffer[-1]
    text = " ".join(item["text"].strip() for item in buffer).strip()
    chunk_id = (
        f"chunk--eng-web--{policy_version}--"
        f"{first['osis_ref']}--{last['osis_ref']}--{chunk_index:05d}"
    )
    return {
        "id": chunk_id,
        "type": "RetrievalChunk",
        "chunk_kind": "sentence_safe_passage_group",
        "source_text_id": "eng-web",
        "source_artifact_id": "eng-web_usfm",
        "osis_start": first["osis_ref"],
        "osis_end": last["osis_ref"],
        "text": text,
        "included_text_span_ids": [item["passage_id"] for item in buffer],
        "boundary_basis": ["english_sentence", "token_budget", "book_boundary"],
        "chunking_policy_version": policy_version,
        "license": "public-domain",
        "validation": {
            "sentence_ended": sentence_ended(text),
            "book_boundary_crossed": False,
        },
        "status": "active" if sentence_ended(text) else "candidate",
    }


def chunk_records(records, policy_version: str, target_tokens=700, soft_max_tokens=1100):
    """records: iterable of dicts with keys osis_ref, passage_id, book, text."""
    buffer: list[dict] = []
    current_book = None
    idx = 1
    for record in records:
        book = record.get("book")
        if buffer and book != current_book:
            yield make_chunk(buffer, idx, policy_version)
            idx += 1
            buffer = []
        current_book = book
        buffer.append(record)
        joined = " ".join(item["text"] for item in buffer)
        text = record["text"]
        if approx_tokens(joined) >= target_tokens and sentence_ended(text):
            yield make_chunk(buffer, idx, policy_version)
            idx += 1
            buffer = []
        elif approx_tokens(joined) >= soft_max_tokens and sentence_ended(text):
            yield make_chunk(buffer, idx, policy_version)
            idx += 1
            buffer = []
    if buffer:
        yield make_chunk(buffer, idx, policy_version)


def join_passages_witnesses(passages_path: Path, witnesses_path: Path):
    """Yield joined records in passage order, pulling clean text from witnesses."""
    text_by_passage = load_witness_text(witnesses_path)
    for passage in load_jsonl(passages_path):
        passage_id = passage.get("id")
        yield {
            "osis_ref": passage.get("osis_ref"),
            "passage_id": passage_id,
            "book": passage.get("book"),
            "text": text_by_passage.get(passage_id, ""),
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="Bible chunker v0 (passages + witnesses join)")
    parser.add_argument("--passages", required=True, help="ScripturePassage JSONL")
    parser.add_argument("--witnesses", required=True, help="TranslationWitness JSONL")
    parser.add_argument("--out", required=True)
    parser.add_argument("--policy", default=str(DEFAULT_POLICY))
    parser.add_argument("--target-tokens", type=int, default=700)
    parser.add_argument("--soft-max-tokens", type=int, default=1100)
    args = parser.parse_args()

    policy_version = read_policy_version(Path(args.policy))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    records = join_passages_witnesses(Path(args.passages), Path(args.witnesses))
    count = 0
    with out.open("w", encoding="utf-8", newline="\n") as handle:
        for chunk in chunk_records(records, policy_version, args.target_tokens, args.soft_max_tokens):
            handle.write(json.dumps(chunk, ensure_ascii=False) + "\n")
            count += 1
    print(f"Wrote {count} chunks to {out} (policy {policy_version})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
