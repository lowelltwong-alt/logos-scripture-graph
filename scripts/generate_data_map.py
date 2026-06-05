#!/usr/bin/env python3
"""Generate .ai/control/DATA_MAP.md — a live map of data, schemas, and endpoints.

Agents MUST run this after changing pipelines, schemas, or data outputs:
    python scripts/generate_data_map.py

The map records, for each data file: path, size, record count (jsonl), trust zone;
the JSON Schema contracts; and pipeline "endpoints" with declared inputs/outputs.

`--check` regenerates in-memory and compares against the committed file IGNORING
the timestamp line — exit 1 if stale. Used as a CI staleness gate (after ingest).

Deterministic and dependency-light. Safe to run any time; output is rebuildable.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / ".ai" / "control" / "DATA_MAP.md"
SCHEMA_DIR = ROOT / "schemas"
GENERATED_LINE_PREFIX = "**Generated:**"

TRUST_ZONE_BY_PREFIX = [
    ("data/raw", "raw"),
    ("data/canonical", "canonical"),
    ("data/processed", "processed"),
    ("data/derived", "derived"),
    ("data/candidate", "candidate"),
]

DATA_DIRS = ["data/raw", "data/canonical", "data/processed", "data/derived", "data/candidate"]
SKIP_SUBSTRINGS = ("extracted", "__pycache__", ".pytest_cache", "derived/chunks")

LFS_THRESHOLD_BYTES = 100 * 1024 * 1024  # flag files >100MB

# Declared pipeline endpoints: (script, role, inputs, outputs)
PIPELINE_ENDPOINTS = [
    {
        "script": "pipelines/ingest/usfm_importer.py",
        "role": "USFM ingest (raw zip -> canonical + processed); emits canon_profiles",
        "inputs": [
            "data/raw/bible/eng-web/usfm/eng-web_usfm.zip",
            "data/raw/bible/eng-web/source_manifest.yaml",
        ],
        "outputs": [
            "data/canonical/scripture/passages/passages.jsonl",
            "data/canonical/translations/eng-web/*.jsonl",
            "data/processed/bible/eng-web/usfm/usfm_events.jsonl",
            "data/processed/bible/eng-web/usfm/parser_report.yaml",
        ],
    },
    {
        "script": "pipelines/ingest/usfm_inline_parser.py",
        "role": "Inline USFM feature extraction (used by importer)",
        "inputs": ["raw USFM text segments"],
        "outputs": ["WordToken / Footnote / EditorialCrossReference sidecars"],
    },
    {
        "script": "pipelines/util/usfm_to_osis.py",
        "role": "USFM book code -> OSIS reference helper",
        "inputs": ["USFM book codes"],
        "outputs": ["OSIS refs"],
    },
    {
        "script": "pipelines/util/canon.py",
        "role": "Canon profiles + testament per OSIS book (ADR-0005)",
        "inputs": ["OSIS book code"],
        "outputs": ["canon_profiles {tradition: status}, testament"],
    },
    {
        "script": "pipelines/chunking/chunker.py",
        "role": "Chunk assembler v1 (genre-aware, boundary-driven; whole-psalm, no mid-sentence)",
        "inputs": [
            "data/canonical/scripture/passages/passages.jsonl (--passages)",
            "data/canonical/translations/eng-web/translation_witnesses.jsonl (--witnesses)",
            "data/canonical/translations/eng-web/boundary_claims.jsonl (--boundary-claims)",
            "data/canonical/translations/eng-web/footnotes.jsonl + editorial_cross_references.jsonl (carry-through)",
            "config/chunking/book_genres.yaml (--genres), config/chunking/chunking_policy.yaml (--policy)",
        ],
        "outputs": [
            "data/derived/chunks/eng-web/chunks.jsonl",
            "data/derived/chunks/eng-web/context_packets.jsonl (--context-out)",
        ],
    },
    {
        "script": "pipelines/chunking/orchestrator.py",
        "role": "T310 byte-identical orchestrator shim (monolith Pass-2 route ledger)",
        "inputs": [
            "data/canonical/scripture/passages/passages.jsonl (--passages)",
            "data/canonical/translations/eng-web/translation_witnesses.jsonl (--witnesses)",
            "data/canonical/translations/eng-web/boundary_claims.jsonl (--boundary-claims)",
            "data/canonical/translations/eng-web/footnotes.jsonl + editorial_cross_references.jsonl (carry-through)",
            "config/chunking/book_genres.yaml (--genres), config/chunking/chunking_policy.yaml (--policy)",
            "registry/chunking/approved-skills.json (--approved-skills)",
        ],
        "outputs": [
            "chunks JSONL byte-identical to chunker.py (--out)",
            "optional ContextPacket JSONL byte-identical to chunker.py (--context-out)",
            "optional JSONL route ledger (--route-ledger)",
        ],
    },
    {
        "script": "pipelines/chunking/boundary_scorer.py",
        "role": "Boundary scoring helper (Sprint 3: wire into boundary-driven chunker)",
        "inputs": ["boundary evidence types"],
        "outputs": ["boundary scores"],
    },
    {
        "script": "pipelines/chunking/detect_form.py",
        "role": "T310 read-only textual-form detector (candidate ClassificationAssignment sidecar)",
        "inputs": [
            "data/canonical/scripture/passages/passages.jsonl (--passages)",
            "data/canonical/translations/eng-web/translation_witnesses.jsonl (--witnesses)",
            "data/canonical/translations/eng-web/boundary_claims.jsonl (--boundary-claims)",
            "config/chunking/book_genres.yaml (--genres), config/chunking/form_registry.yaml (--form-registry)",
            "optional word_tokens.jsonl (--word-tokens), footnotes.jsonl (--footnotes)",
        ],
        "outputs": [
            "data/candidate/chunking/form_assignments/<source>-detect_form-v0.1.0-<timestamp>.jsonl",
        ],
    },
    {
        "script": "pipelines/chunking/evaluate_chunks.py",
        "role": "A/B evaluation harness — scores chunk variants (sentence integrity, psalm fragmentation, size, gold checks)",
        "inputs": ["one or more chunks.jsonl variants (name=path)"],
        "outputs": ["comparison table + report.md + scores.json"],
    },
    {
        "script": "pipelines/graph/discover_connections.py",
        "role": "Candidate-only connection discovery (Strong's co-occurrence, rare phrase overlap, citation formulas)",
        "inputs": [
            "data/canonical/translations/eng-web/word_tokens.jsonl",
            "data/canonical/translations/eng-web/translation_witnesses.jsonl",
            "data/canonical/translations/eng-web/editorial_cross_references.jsonl",
        ],
        "outputs": [
            "data/candidate/connections/<agent>-<date>.jsonl",
            "data/candidate/connections/<agent>-<date>.manifest.yaml",
            "build/discovery/<agent>-report.md",
        ],
    },
    {
        "script": "pipelines/graph/compare_candidate_batches.py",
        "role": "Compare candidate batches and split agreement/disagreement sets for human adjudication",
        "inputs": ["two or more data/candidate/connections/*.jsonl batches"],
        "outputs": [
            "build/discovery/comparison.md",
            "build/discovery/comparison/agreement.jsonl",
            "build/discovery/comparison/disagreement.jsonl",
        ],
    },
    {
        "script": "pipelines/validate/validate_manifest.py",
        "role": "Source manifest + checksum validation",
        "inputs": ["data/raw/**/source_manifest.yaml"],
        "outputs": ["pass/fail"],
    },
    {
        "script": "scripts/scan_raw_sources.py",
        "role": "First-pass scan of the REAL raw documents (mandatory before processing)",
        "inputs": ["data/raw/**/*.zip (USFM)"],
        "outputs": [".ai/control/RAW_SOURCE_INVENTORY.md"],
    },
    {
        "script": "scripts/validate_raw_coverage.py",
        "role": "HARD gate: every raw USFM marker must be classified",
        "inputs": ["data/raw/**/*.zip", "config/ingest/usfm_marker_coverage.yaml"],
        "outputs": ["pass/fail"],
    },
    {
        "script": "scripts/validate_jsonl.py",
        "role": "JSONL referential integrity + canon presence (--require-canon)",
        "inputs": ["data/canonical/**/*.jsonl"],
        "outputs": ["pass/fail"],
    },
    {
        "script": "scripts/validate_schemas.py",
        "role": "JSON Schema validation of records (best-effort; needs '.[validate]')",
        "inputs": ["data/canonical/**/*.jsonl", "schemas/*.json"],
        "outputs": ["pass/fail"],
    },
]


def trust_zone(rel: str) -> str:
    for prefix, zone in TRUST_ZONE_BY_PREFIX:
        if rel.startswith(prefix):
            return zone
    return "other"


def count_jsonl_records(path: Path) -> int:
    count = 0
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                count += 1
    return count


def fmt_size(n: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    size = float(n)
    for unit in units:
        if size < 1024 or unit == "GB":
            return f"{size:.1f}{unit}" if unit != "B" else f"{int(size)}B"
        size /= 1024
    return f"{n}B"


def iter_data_files():
    for d in DATA_DIRS:
        base = ROOT / d
        if not base.exists():
            continue
        # Sort by posix string (NOT Path objects): WindowsPath sorts case-
        # insensitively while PosixPath sorts case-sensitively, which would make
        # the file order — and thus the staleness gate — differ across OS.
        for path in sorted(base.rglob("*"), key=lambda p: p.as_posix()):
            if not path.is_file():
                continue
            rel = path.relative_to(ROOT).as_posix()
            if any(s in rel for s in SKIP_SUBSTRINGS):
                continue
            if path.name == ".gitkeep":
                continue
            yield path, rel


def build_data_table() -> tuple[list[str], int, int]:
    rows = []
    total_bytes = 0
    total_records = 0
    for path, rel in iter_data_files():
        size = path.stat().st_size
        total_bytes += size
        records = ""
        if rel.endswith(".jsonl"):
            n = count_jsonl_records(path)
            total_records += n
            records = f"{n:,}"
        note = " ⚠️ LFS/regenerate" if size > LFS_THRESHOLD_BYTES else ""
        rows.append(f"| `{rel}` | {trust_zone(rel)} | {fmt_size(size)}{note} | {records} |")
    return rows, total_bytes, total_records


def build_schema_rows() -> list[str]:
    rows = []
    for path in sorted(SCHEMA_DIR.glob("*.json"), key=lambda p: p.as_posix()):
        try:
            title = json.loads(path.read_text(encoding="utf-8")).get("title", "")
        except (OSError, json.JSONDecodeError):
            title = "(unparseable)"
        rows.append(f"| `schemas/{path.name}` | {title} |")
    return rows


def render() -> str:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    data_rows, total_bytes, total_records = build_data_table()
    schema_rows = build_schema_rows()

    lines: list[str] = []
    lines.append("# Data Map & Pipeline Endpoints (generated)")
    lines.append("")
    lines.append("<!-- GENERATED by scripts/generate_data_map.py. Do not hand-edit.")
    lines.append("     Re-run after any pipeline/schema/data change. CI: --check (post-ingest). -->")
    lines.append("")
    lines.append(f"{GENERATED_LINE_PREFIX} {now}")
    lines.append("**Generator:** `scripts/generate_data_map.py`")
    lines.append("")
    lines.append("Self-aware map of the project's data surface, schema contracts, and endpoints.")
    lines.append("Generated data (canonical/processed) is gitignored and regenerable from raw + importer.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Cross-Repo Governance Contract")
    lines.append("")
    lines.append("```text")
    lines.append("logos-governance-architecture")
    lines.append("  -> upstream governance / theological architecture authority")
    lines.append("  -> governance_contract")
    lines.append("  -> logos-scripture-graph")
    lines.append("     -> governed Scripture data-plane / knowledge-plane implementation")
    lines.append("     -> validated release artifacts for future runtime consumers")
    lines.append("```")
    lines.append("")
    lines.append("- Contract: `config/governance/repository_link_contract.yaml`")
    lines.append("- Agent-hostile policy: `config/agents/agent_hostile_policy.yaml`")
    lines.append("- Parent issue: `https://github.com/lowelltwong-alt/logos-governance-architecture/issues/54`")
    lines.append("- Child issue: `https://github.com/lowelltwong-alt/logos-scripture-graph/issues/7`")
    lines.append("")
    lines.append("Downstream data-plane artifacts consume upstream governance meaning; they do not silently redefine it.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Totals")
    lines.append("")
    lines.append(f"- Data files mapped: **{len(data_rows)}**")
    lines.append(f"- Total data size: **{fmt_size(total_bytes)}**")
    lines.append(f"- Total JSONL records: **{total_records:,}**")
    lines.append(f"- Schema contracts: **{len(schema_rows)}**")
    lines.append("")
    lines.append("> Files >100MB are flagged ⚠️ — gitignored + regenerated in CI (commit policy: PROJECT_STATUS.md).")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Data artifacts (by trust zone)")
    lines.append("")
    if data_rows:
        lines.append("| Path | Trust zone | Size | Records |")
        lines.append("|------|------------|------|---------|")
        lines.extend(data_rows)
    else:
        lines.append("_No generated data present (run the importer to regenerate)._")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Schema contracts")
    lines.append("")
    lines.append("| Schema | Title |")
    lines.append("|--------|-------|")
    lines.extend(schema_rows)
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Pipeline + validation endpoints (inputs -> outputs)")
    lines.append("")
    for ep in PIPELINE_ENDPOINTS:
        lines.append(f"### `{ep['script']}`")
        lines.append("")
        lines.append(f"- **Role:** {ep['role']}")
        lines.append("- **Inputs:**")
        for i in ep["inputs"]:
            lines.append(f"  - `{i}`")
        lines.append("- **Outputs:**")
        for o in ep["outputs"]:
            lines.append(f"  - `{o}`")
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Flow")
    lines.append("")
    lines.append("```text")
    lines.append("raw zip + manifest")
    lines.append("  -> usfm_importer (+ usfm_inline_parser, usfm_to_osis, canon)")
    lines.append("     -> canonical: passages (+canon_profiles), translation_witnesses, word_tokens,")
    lines.append("        footnotes, editorial_cross_references, section_headings, boundary_claims, glossary_entries")
    lines.append("     -> processed: usfm_events, parser_report, extraction_manifest")
    lines.append("  -> chunker v0 (passages + witnesses join) -> derived/chunks")
    lines.append("```")
    lines.append("")
    return "\n".join(lines) + "\n"


def _canonical_for_check(text: str) -> str:
    """Normalize for the staleness gate: ignore the timestamp and platform-dependent
    byte sizes (line endings differ across OS). Compares structure + record counts —
    the meaningful drift signal — not bytes."""
    out: list[str] = []
    for line in text.splitlines():
        if line.startswith(GENERATED_LINE_PREFIX):
            continue
        if line.startswith("- Total data size:"):
            continue
        if line.startswith("| `data/"):
            parts = line.split(" | ")
            if len(parts) == 4:  # | `path` | zone | size | records |
                parts[2] = "SIZE"
                line = " | ".join(parts)
        out.append(line)
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true",
                        help="Exit 1 if DATA_MAP.md is stale (ignores timestamp line).")
    args = parser.parse_args()

    content = render()
    if args.check:
        if not OUT.exists():
            print("DATA_MAP.md missing; run generate_data_map.py", file=sys.stderr)
            return 1
        existing = OUT.read_text(encoding="utf-8")
        want = _canonical_for_check(content)
        have = _canonical_for_check(existing)
        if have != want:
            import difflib
            print("DATA_MAP.md is STALE — run: python scripts/generate_data_map.py", file=sys.stderr)
            diff = difflib.unified_diff(
                have.splitlines(), want.splitlines(),
                fromfile="committed DATA_MAP.md", tofile="freshly generated", lineterm="",
            )
            for line in list(diff)[:60]:
                print(line, file=sys.stderr)
            return 1
        print("DATA_MAP.md is current.")
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(content, encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
