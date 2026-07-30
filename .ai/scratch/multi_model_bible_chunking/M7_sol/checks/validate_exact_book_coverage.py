#!/usr/bin/env python3
"""Validate exact ordered verse coverage for one M7 candidate book, independent of reviews."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
MODEL = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol"
PASSAGES = ROOT / "data" / "canonical" / "scripture" / "passages" / "passages.jsonl"
SPAN_RE = re.compile(r"^([1-4]?[A-Za-z][A-Za-z0-9]*)\.(\d+)\.(\d+)-([1-4]?[A-Za-z][A-Za-z0-9]*)\.(\d+)\.(\d+)$")


def read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", required=True)
    parser.add_argument(
        "--model-root",
        type=Path,
        default=MODEL,
        help="candidate model root; defaults to the active M7_sol folder",
    )
    args = parser.parse_args()
    model_root = args.model_root.resolve()
    refs = [row["osis_ref"] for row in read_jsonl(PASSAGES) if row.get("book") == args.book]
    positions = {ref: index for index, ref in enumerate(refs)}
    chunks = read_jsonl(
        model_root / "book_chunks" / args.book / "chunks.jsonl"
    )
    covered: list[str] = []
    for chunk in chunks:
        match = SPAN_RE.fullmatch(chunk["span"])
        if not match or match.group(1) != args.book or match.group(4) != args.book:
            raise SystemExit(f"invalid span {chunk.get('span')}")
        start = f"{args.book}.{int(match.group(2))}.{int(match.group(3))}"
        end = f"{args.book}.{int(match.group(5))}.{int(match.group(6))}"
        covered.extend(refs[positions[start] : positions[end] + 1])
    if covered != refs:
        missing = [ref for ref in refs if ref not in set(covered)]
        duplicates = sorted({ref for ref in covered if covered.count(ref) > 1})
        raise SystemExit(f"coverage mismatch expected={len(refs)} covered={len(covered)} missing={missing[:8]} duplicates={duplicates[:8]}")
    print(f"OK: {args.book} chunks={len(chunks)} exact ordered coverage={len(refs)}/{len(refs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
