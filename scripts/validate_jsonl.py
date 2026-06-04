#!/usr/bin/env python3
"""Validate generated JSONL records for WEB ingest invariants."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

RAW_USFM_RE = re.compile(r"\\(?:\+?[A-Za-z0-9]+)\*?")
OSIS_RE = re.compile(r"^[1-4]?[A-Za-z][A-Za-z0-9]*(?:\.[A-Za-z0-9]+)?\.\d+\.\d+(?:-[1-4]?[A-Za-z][A-Za-z0-9]*(?:\.[A-Za-z0-9]+)?\.\d+\.\d+)?$")
REQUIRED_META = ["source_sha256", "license"]


def iter_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if line.strip():
                yield line_no, json.loads(line)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    parser.add_argument(
        "--translation-id",
        default="eng-web",
        help="Expected translation_id for generated witness output (default: eng-web). "
        "Parameterized so non-WEB corpora (WLC/SBLGNT) can be validated later (SCHEMA-LOCK).",
    )
    parser.add_argument(
        "--require-canon",
        action="store_true",
        help="Fail if any ScripturePassage lacks canon_profiles (CANON-1 guard).",
    )
    args = parser.parse_args(argv)
    expected_translation = args.translation_id

    failures: list[str] = []
    ids: set[str] = set()
    passages: set[str] = set()
    witnesses: list[dict[str, Any]] = []

    for raw_path in args.paths:
        path = Path(raw_path)
        if not path.exists():
            failures.append(f"Missing JSONL file: {path}")
            continue
        for line_no, record in iter_jsonl(path):
            rid = record.get("id")
            if not rid:
                failures.append(f"{path}:{line_no}: missing id")
            elif rid in ids:
                failures.append(f"{path}:{line_no}: duplicate id {rid}")
            else:
                ids.add(rid)
            for key in REQUIRED_META:
                if not record.get(key):
                    failures.append(f"{path}:{line_no}: missing {key}")
            osis_ref = record.get("osis_ref")
            if osis_ref and not OSIS_RE.match(osis_ref):
                failures.append(f"{path}:{line_no}: malformed OSIS reference {osis_ref}")
            if record.get("type") == "ScripturePassage":
                passages.add(record["id"])
                if args.require_canon and not record.get("canon_profiles"):
                    failures.append(f"{path}:{line_no}: ScripturePassage {record.get('id')} missing canon_profiles (CANON-1)")
            if record.get("type") == "TranslationWitness":
                witnesses.append(record)
                if RAW_USFM_RE.search(record.get("text", "")):
                    failures.append(f"{path}:{line_no}: TranslationWitness.text contains raw USFM marker")
                if record.get("translation_id") != expected_translation:
                    failures.append(f"{path}:{line_no}: unexpected translation_id {record.get('translation_id')}")
            if record.get("translation_id") and record.get("translation_id") != expected_translation:
                failures.append(f"{path}:{line_no}: generated output translation_id {record.get('translation_id')} != expected {expected_translation}")
            if record.get("relation_type") and record.get("relation_type") != "editorial_cross_reference":
                failures.append(f"{path}:{line_no}: disallowed relation_type {record.get('relation_type')}")

    for witness in witnesses:
        if witness.get("passage_id") not in passages:
            failures.append(f"{witness.get('id')}: points to missing ScripturePassage {witness.get('passage_id')}")

    if failures:
        print("JSONL VALIDATION FAILED")
        for failure in failures[:200]:
            print(f"- {failure}")
        if len(failures) > 200:
            print(f"- ... {len(failures) - 200} additional failures")
        return 1
    print(f"JSONL validation passed for {len(ids)} records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
