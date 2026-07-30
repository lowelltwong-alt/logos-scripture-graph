#!/usr/bin/env python3
"""Render a pinned WEB USFM book as compact UTF-8 verse text for direct reading."""
from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
PASSAGES = ROOT / "data" / "canonical" / "scripture" / "passages" / "passages.jsonl"
ARCHIVE = ROOT / "data" / "raw" / "bible" / "eng-web" / "usfm" / "eng-web_usfm.zip"
WORD_RE = re.compile(r"\\w\s+([^|]+)\|[^\\]*?\\w\*")
FOOTNOTE_RE = re.compile(r"\\f\s.*?\\f\*")
CHAR_RE = re.compile(r"\\[+]?[a-z0-9]+\*?(?:\s+)?")


def source_file_for(book: str) -> str:
    with PASSAGES.open(encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            if row.get("book") == book:
                return str(row["source_file"])
    raise SystemExit(f"unknown book: {book}")


def clean(text: str) -> str:
    text = FOOTNOTE_RE.sub("", text)
    text = WORD_RE.sub(lambda match: match.group(1), text)
    text = CHAR_RE.sub("", text)
    return re.sub(r"\s+", " ", text).strip()


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", required=True)
    parser.add_argument("--chapters", default="1-999")
    parser.add_argument("--paragraph-starts-only", action="store_true")
    args = parser.parse_args()
    start, end = (int(value) for value in args.chapters.split("-", 1))
    with zipfile.ZipFile(ARCHIVE) as archive:
        source_file = source_file_for(args.book)
        names = [name for name in archive.namelist() if Path(name).name == source_file]
        if len(names) != 1:
            raise SystemExit(f"expected one {source_file} archive entry, found {names}")
        lines = archive.read(names[0]).decode("utf-8-sig").splitlines()
    chapter = 0
    paragraph_pending = False
    for line in lines:
        if line.startswith("\\c "):
            chapter = int(line.split()[1])
            paragraph_pending = True
            continue
        if not start <= chapter <= end:
            continue
        if line.startswith(("\\p", "\\m", "\\q", "\\d", "\\s")):
            paragraph_pending = True
        match = re.match(r"^\\v\s+(\d+)\s+(.*)$", line)
        if not match:
            continue
        verse, body = match.groups()
        if args.paragraph_starts_only and not paragraph_pending:
            continue
        prefix = "¶" if paragraph_pending else " "
        print(f"{prefix}{args.book}.{chapter}.{verse} {clean(body)}")
        paragraph_pending = False
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
