#!/usr/bin/env python3
"""Validate JSONL records against their JSON Schemas (best-effort).

Uses the `jsonschema` package when available (install via the optional extra:
`pip install -e ".[validate]"`). If jsonschema is not installed, this script
SKIPS with exit 0 so dependency-light environments stay green. CI installs the
extra so the gate is real there.

Maps record `type` -> schema file. Usage:
    python scripts/validate_schemas.py data/canonical/**/*.jsonl
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "schemas"

TYPE_TO_SCHEMA = {
    "ScripturePassage": "scripture_passage.schema.json",
    "TranslationWitness": "translation_witness.schema.json",
    "WordToken": "word_token.schema.json",
    "Footnote": "footnote.schema.json",
    "EditorialCrossReference": "editorial_cross_reference.schema.json",
    "SectionHeading": "section_heading.schema.json",
    "BoundaryClaim": "boundary_claim.schema.json",
    "GlossaryEntry": "glossary_entry.schema.json",
    "RetrievalChunk": "chunk.schema.json",
    "TextSpan": "text_span.schema.json",
    "ContextPacket": "context_packet.schema.json",
    "RelationshipObject": "relationship_object.schema.json",
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--limit", type=int, default=0, help="Max records per file (0 = all)")
    args = parser.parse_args(argv)

    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        print("jsonschema not installed; skipping schema validation (install '.[validate]').")
        return 0

    validators: dict[str, object] = {}
    for rec_type, schema_file in TYPE_TO_SCHEMA.items():
        schema_path = SCHEMA_DIR / schema_file
        if schema_path.exists():
            validators[rec_type] = Draft202012Validator(
                json.loads(schema_path.read_text(encoding="utf-8"))
            )

    failures: list[str] = []
    for raw_path in args.paths:
        path = Path(raw_path)
        if not path.exists():
            failures.append(f"Missing file: {path}")
            continue
        with path.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                if args.limit and line_no > args.limit:
                    break
                record = json.loads(line)
                validator = validators.get(record.get("type"))
                if validator is None:
                    continue
                for err in validator.iter_errors(record):
                    failures.append(f"{path}:{line_no}: {record.get('type')}: {err.message}")
                    if len(failures) > 200:
                        break

    if failures:
        print("SCHEMA VALIDATION FAILED")
        for failure in failures[:200]:
            print(f"- {failure}")
        return 1
    print("Schema validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
