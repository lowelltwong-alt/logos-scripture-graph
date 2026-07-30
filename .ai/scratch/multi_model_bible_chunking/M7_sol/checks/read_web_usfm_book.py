#!/usr/bin/env python3
"""Read a pinned WEB USFM book from its source archive without extracting it."""
from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
PASSAGES = ROOT / "data" / "canonical" / "scripture" / "passages" / "passages.jsonl"
ARCHIVE = ROOT / "data" / "raw" / "bible" / "eng-web" / "usfm" / "eng-web_usfm.zip"
CHAPTER_RE = re.compile(r"^\\c\s+(\d+)\s*$")


def source_file_for(book: str) -> str:
    with PASSAGES.open(encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            if row.get("book") == book:
                return str(row["source_file"])
    raise SystemExit(f"unknown book: {book}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", required=True)
    parser.add_argument("--chapters", default="1-999")
    parser.add_argument("--markers-only", action="store_true")
    args = parser.parse_args()
    start, end = (int(value) for value in args.chapters.split("-", 1))
    source_file = source_file_for(args.book)
    with zipfile.ZipFile(ARCHIVE) as archive:
        matches = [name for name in archive.namelist() if Path(name).name == source_file]
        if len(matches) != 1:
            raise SystemExit(f"expected one {source_file} archive entry, found {matches}")
        text = archive.read(matches[0]).decode("utf-8-sig")
    chapter = 0
    for line in text.splitlines():
        match = CHAPTER_RE.match(line)
        if match:
            chapter = int(match.group(1))
        if not start <= chapter <= end:
            continue
        if args.markers_only:
            if line.startswith(("\\c ", "\\s", "\\ms", "\\r ", "\\d ", "\\qa ", "\\q ", "\\p", "\\m")):
                print(line)
        else:
            print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
