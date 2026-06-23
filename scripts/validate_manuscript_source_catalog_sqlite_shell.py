#!/usr/bin/env python3
"""Validate the T392 manuscript source-catalog SQLite schema shell."""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTROL = ROOT / ".ai" / "control" / "manuscript_source_catalog_sqlite_shell.yaml"
MANIFEST = ROOT / "data" / "candidate" / "source_catalog" / "manuscript_reliability" / "sqlite" / "manifest.yaml"
SCHEMA = ROOT / "data" / "candidate" / "source_catalog" / "manuscript_reliability" / "sqlite" / "schema.sql"
SEED = ROOT / "data" / "candidate" / "source_catalog" / "manuscript_reliability" / "sqlite" / "seed_rows.jsonl"
T391_PACKET = ROOT / ".ai" / "control" / "manuscript_source_catalog_research_packet.yaml"
ROADMAP_DOC = ROOT / "docs" / "roadmap" / "T392_SQLITE_SOURCE_CATALOG_SCHEMA_SHELL.md"
TASK = ROOT / ".ai" / "tasks" / "T392.task.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T392" / "handoff.md"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
MAIN_TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"
ROADMAP_STATE = ROOT / "ROADMAP_STATE.yaml"
VALIDATE_ALL = ROOT / "scripts" / "validate_all.py"
DATA_MAP = ROOT / ".ai" / "control" / "DATA_MAP.md"

SEEDED_TABLE_COUNTS = {
    "scripture_source_family": 5,
    "scripture_source_catalog": 18,
    "evidence_source_catalog_method_profile": 5,
    "evidence_source_trust_rule": 9,
}

EMPTY_SHELL_TABLES = {
    "scripture_holding_institution",
    "scripture_catalog_witness_record",
    "scripture_witness_identifier",
    "scripture_witness_date_claim",
    "scripture_witness_material_claim",
    "scripture_witness_coverage_claim",
    "scripture_witness_discovery_event",
    "evidence_catalog_review_queue",
}

REQUIRED_TABLES = set(SEEDED_TABLE_COUNTS) | EMPTY_SHELL_TABLES
FORBIDDEN_PREFIXES = ("canonical_", "boundary_", "doctrine_")

COMMON_REQUIRED_ROW_FIELDS = {
    "source_url",
    "method",
    "confidence",
    "provenance_note",
    "review_status",
    "source_family",
    "rights_access_status",
    "non_authorizing_scope_label",
    "stores_scripture_text",
    "stores_transcription_text",
    "stores_boundary_text",
}

REQUIRED_FALSE_AUTHORITY = {
    "authorizes_committed_sqlite_database_file",
    "authorizes_witness_row_population",
    "authorizes_holding_institution_row_population",
    "authorizes_date_claim_row_population",
    "authorizes_material_claim_row_population",
    "authorizes_coverage_claim_row_population",
    "authorizes_discovery_event_row_population",
    "authorizes_review_queue_row_population",
    "authorizes_source_text_import",
    "authorizes_transcription_storage",
    "authorizes_bible_text_storage",
    "authorizes_canonical_bible_text_change",
    "authorizes_canonical_passage_record_change",
    "authorizes_chunk_output_change",
    "authorizes_reviewed_gold_promotion",
    "authorizes_textual_critical_decision",
    "authorizes_preferred_reading",
    "authorizes_source_tradition_preference",
    "authorizes_canon_scope_change",
    "authorizes_boundary_import",
    "authorizes_commentary_or_patristic_import",
    "authorizes_doctrine_genealogy_import",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_embedding_or_vector_work",
    "authorizes_doctrinal_system",
    "authorizes_apologetic_conclusion_as_truth",
}

REQUIRED_WIRING = {
    FRONT_DOOR: ["manuscript_source_catalog_sqlite_shell.yaml", "T392 SQLite source-catalog shell"],
    MAIN_TOC: ["source-catalog-sqlite", "manuscript_source_catalog_sqlite_shell.yaml", "T392_SQLITE_SOURCE_CATALOG_SCHEMA_SHELL.md"],
    ROADMAP_TOC: ["T392 | SQLite source catalog schema shell", "source-catalog-sqlite", "scripts/validate_manuscript_source_catalog_sqlite_shell.py"],
    ROADMAP_STATE: ["T392", "SQLite Source Catalog Schema Shell", "manuscript_source_catalog_sqlite_shell.yaml"],
    VALIDATE_ALL: ["validate_manuscript_source_catalog_sqlite_shell.py"],
    DATA_MAP: [
        "data/candidate/source_catalog/manuscript_reliability/sqlite/schema.sql",
        "data/candidate/source_catalog/manuscript_reliability/sqlite/seed_rows.jsonl",
    ],
}


class ManuscriptSourceCatalogSqliteShellError(ValueError):
    """Raised when the T392 SQLite shell is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(path)}: unreadable: {exc}") from exc


def _strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            return parts[1] + "\n" + parts[2]
    return text


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(_strip_frontmatter(_read_text(path)))
    except yaml.YAMLError as exc:
        raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _read_seed(path: Path = SEED) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(_read_text(path).splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(path)}:{line_number}: invalid JSON: {exc}") from exc
        if not isinstance(record, dict):
            raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(path)}:{line_number}: expected object")
        rows.append(record)
    return rows


def _require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ManuscriptSourceCatalogSqliteShellError(f"{label} must be a mapping")
    return value


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ManuscriptSourceCatalogSqliteShellError(f"{label} must be a non-empty string")
    return value.strip()


def _require_string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ManuscriptSourceCatalogSqliteShellError(f"{label} must be a non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise ManuscriptSourceCatalogSqliteShellError(f"{label} must contain only non-empty strings")
    return [item.strip() for item in value]


def _t391_source_urls() -> set[str]:
    packet = _read_yaml(T391_PACKET)
    sources = packet.get("curated_sources")
    if not isinstance(sources, list):
        raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(T391_PACKET)}: curated_sources must be a list")
    urls = {str(item.get("source_url")) for item in sources if isinstance(item, dict)}
    if len(urls) != 18:
        raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(T391_PACKET)}: expected 18 curated source URLs")
    return urls


def _validate_control_packet(data: dict[str, Any]) -> None:
    expected = {
        "object_type": "manuscript_source_catalog_sqlite_shell",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "manuscript_source_catalog_sqlite_shell.v1",
        "shell_id": "t392_manuscript_source_catalog_sqlite_shell",
        "task_id": "T392",
        "status": "active_source_catalog_seed_only",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(CONTROL)}: {key} must be {value!r}")
    for key in ("provenance_note", "reason_for_inclusion"):
        _require_string(data.get(key), f"{_rel(CONTROL)}.{key}")

    authority = _require_mapping(data.get("authority"), f"{_rel(CONTROL)}.authority")
    for key in (
        "records_sqlite_source_catalog_schema_shell",
        "records_curated_source_family_rows",
        "records_curated_source_catalog_rows",
        "records_curated_method_profile_rows",
        "records_curated_source_trust_rule_rows",
        "refines_t390_metadata_plan",
        "uses_t391_official_source_packet",
        "may_validate_with_in_memory_sqlite",
    ):
        if authority.get(key) is not True:
            raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(CONTROL)}: authority.{key} must be true")
    missing = sorted(REQUIRED_FALSE_AUTHORITY - set(authority))
    if missing:
        raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(CONTROL)}: authority missing {missing}")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(CONTROL)}: authority.{key} must be false")

    boundary = _require_mapping(data.get("data_boundary"), f"{_rel(CONTROL)}.data_boundary")
    allowed = set(_require_string_list(boundary.get("allowed_table_prefixes"), "allowed_table_prefixes"))
    if allowed != {"scripture_", "evidence_"}:
        raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(CONTROL)}: allowed_table_prefixes must be scripture_/evidence_")
    forbidden = set(_require_string_list(boundary.get("forbidden_table_or_view_prefixes"), "forbidden_table_or_view_prefixes"))
    if not set(FORBIDDEN_PREFIXES) <= forbidden:
        raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(CONTROL)}: missing forbidden prefixes")
    if "No canonical_* table or view" not in str(boundary.get("forbidden_table_or_view_rule", "")):
        raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(CONTROL)}: canonical_* rule required")

    artifacts = _require_mapping(data.get("sqlite_artifacts"), f"{_rel(CONTROL)}.sqlite_artifacts")
    for key, expected_path in (("schema_file", _rel(SCHEMA)), ("seed_file", _rel(SEED)), ("manifest_file", _rel(MANIFEST))):
        if artifacts.get(key) != expected_path:
            raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(CONTROL)}: sqlite_artifacts.{key} must be {expected_path}")
    if artifacts.get("binary_database_committed") is not False:
        raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(CONTROL)}: binary_database_committed must be false")


def _validate_manifest(data: dict[str, Any]) -> None:
    expected = {
        "object_type": "sqlite_source_catalog_seed_manifest",
        "trust_zone": "candidate",
        "lifecycle_status": "active",
        "schema_version": "manuscript_source_catalog_sqlite_shell.v1",
        "manifest_id": "t392_sqlite_source_catalog_seed_manifest",
        "task_id": "T392",
        "status": "active_source_catalog_seed_only",
        "schema_file": _rel(SCHEMA),
        "seed_file": _rel(SEED),
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(MANIFEST)}: {key} must be {value!r}")
    if _require_mapping(data.get("allowed_seed_tables"), "allowed_seed_tables") != SEEDED_TABLE_COUNTS:
        raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(MANIFEST)}: allowed_seed_tables mismatch")
    empty = set(_require_string_list(data.get("empty_shell_tables"), "empty_shell_tables"))
    if empty != EMPTY_SHELL_TABLES:
        raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(MANIFEST)}: empty shell table mismatch")
    common = set(_require_string_list(data.get("common_required_row_fields"), "common_required_row_fields"))
    if common != COMMON_REQUIRED_ROW_FIELDS:
        raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(MANIFEST)}: common_required_row_fields mismatch")


def _validate_schema_text(schema_sql: str) -> None:
    lowered = schema_sql.lower()
    for prefix in FORBIDDEN_PREFIXES:
        for phrase in (f"create table {prefix}", f"create view {prefix}"):
            if phrase in lowered:
                raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(SCHEMA)}: forbidden SQLite object prefix {prefix}")
    for forbidden in (
        "scripture_text text",
        "transcription_text text",
        "bible_text text",
        "source_text text",
        "reading_text text",
        "preferred_reading text",
    ):
        if forbidden in lowered:
            raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(SCHEMA)}: forbidden text-bearing column {forbidden!r}")


def _sqlite_objects(conn: sqlite3.Connection, object_type: str) -> set[str]:
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type = ? AND name NOT LIKE 'sqlite_%'", (object_type,))
    return {str(row[0]) for row in cursor.fetchall()}


def _insert_seed_rows(conn: sqlite3.Connection, seed_rows: list[dict[str, Any]], source_urls: set[str]) -> None:
    for index, record in enumerate(seed_rows, start=1):
        table = _require_string(record.get("table"), f"{_rel(SEED)}:{index}.table")
        row = _require_mapping(record.get("row"), f"{_rel(SEED)}:{index}.row")
        if table not in SEEDED_TABLE_COUNTS:
            raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(SEED)}:{index}: forbidden seed table {table}")
        missing = sorted(COMMON_REQUIRED_ROW_FIELDS - set(row))
        if missing:
            raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(SEED)}:{index}: row missing common fields {missing}")
        if row["source_url"] not in source_urls:
            raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(SEED)}:{index}: source_url not from T391 curated sources")
        if row["confidence"] not in {"high", "medium", "low"}:
            raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(SEED)}:{index}: invalid confidence")
        for flag in ("stores_scripture_text", "stores_transcription_text", "stores_boundary_text"):
            if row.get(flag) not in (0, False):
                raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(SEED)}:{index}: {flag} must be false/0")
        if "not" not in str(row["non_authorizing_scope_label"]).lower():
            raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(SEED)}:{index}: non_authorizing_scope_label must deny authority")
        columns = list(row)
        sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join('?' for _ in columns)})"
        try:
            conn.execute(sql, [row[column] for column in columns])
        except sqlite3.Error as exc:
            raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(SEED)}:{index}: SQLite insert failed for {table}: {exc}") from exc


def _build_database(schema_sql: str, seed_rows: list[dict[str, Any]], source_urls: set[str]) -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        conn.executescript(schema_sql)
    except sqlite3.Error as exc:
        raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(SCHEMA)}: SQLite schema failed to load: {exc}") from exc
    tables = _sqlite_objects(conn, "table")
    if tables != REQUIRED_TABLES:
        raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(SCHEMA)}: tables mismatch: {sorted(tables)}")
    views = _sqlite_objects(conn, "view")
    forbidden_objects = sorted(name for name in (tables | views) if name.startswith(FORBIDDEN_PREFIXES))
    if forbidden_objects:
        raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(SCHEMA)}: forbidden SQLite objects {forbidden_objects}")
    _insert_seed_rows(conn, seed_rows, source_urls)
    conn.commit()
    return conn


def _validate_schema_columns(conn: sqlite3.Connection) -> None:
    forbidden_exact = {
        "scripture_text",
        "transcription_text",
        "bible_text",
        "source_text",
        "reading_text",
        "preferred_reading",
        "commentary_text",
        "patristic_text",
        "theologian_text",
        "creed_wording",
    }
    for table in REQUIRED_TABLES:
        columns = {str(row[1]) for row in conn.execute(f"PRAGMA table_info({table})").fetchall()}
        bad = sorted(columns & forbidden_exact)
        if bad:
            raise ManuscriptSourceCatalogSqliteShellError(f"{table}: forbidden text-bearing columns {bad}")
        if table in SEEDED_TABLE_COUNTS and not COMMON_REQUIRED_ROW_FIELDS <= columns:
            missing = sorted(COMMON_REQUIRED_ROW_FIELDS - columns)
            raise ManuscriptSourceCatalogSqliteShellError(f"{table}: missing common columns {missing}")


def _validate_database_counts(conn: sqlite3.Connection) -> dict[str, int]:
    counts = {table: int(conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]) for table in REQUIRED_TABLES}
    for table, expected in SEEDED_TABLE_COUNTS.items():
        if counts[table] != expected:
            raise ManuscriptSourceCatalogSqliteShellError(f"{table}: expected {expected} rows, found {counts[table]}")
    for table in EMPTY_SHELL_TABLES:
        if counts[table] != 0:
            raise ManuscriptSourceCatalogSqliteShellError(f"{table}: must remain empty in T392")
    return counts


def _validate_no_canonical_contamination(conn: sqlite3.Connection) -> None:
    canonical_objects = [
        str(row[0])
        for row in conn.execute("SELECT name FROM sqlite_master WHERE name LIKE 'canonical_%'").fetchall()
    ]
    if canonical_objects:
        raise ManuscriptSourceCatalogSqliteShellError(
            "canonical_* table/view must not include source-catalog, boundary, commentary, "
            f"patristic, theologian, doctrine, or apologetic data: {canonical_objects}"
        )


def _validate_wiring() -> None:
    for path, needles in REQUIRED_WIRING.items():
        text = _read_text(path)
        for needle in needles:
            if needle not in text:
                raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(path)}: missing wiring string {needle!r}")
    for path in (ROADMAP_DOC, TASK, HANDOFF):
        if not path.exists():
            raise ManuscriptSourceCatalogSqliteShellError(f"{_rel(path)}: required T392 surface is missing")


def validate_manuscript_source_catalog_sqlite_shell(*, check_wiring: bool = True) -> dict[str, Any]:
    control = _read_yaml(CONTROL)
    manifest = _read_yaml(MANIFEST)
    _validate_control_packet(control)
    _validate_manifest(manifest)
    schema_sql = _read_text(SCHEMA)
    _validate_schema_text(schema_sql)
    conn = _build_database(schema_sql, _read_seed(SEED), _t391_source_urls())
    try:
        _validate_schema_columns(conn)
        _validate_no_canonical_contamination(conn)
        counts = _validate_database_counts(conn)
    finally:
        conn.close()
    if check_wiring:
        _validate_wiring()
    return {
        "shell_id": control["shell_id"],
        "table_count": len(REQUIRED_TABLES),
        "seeded_row_count": sum(SEEDED_TABLE_COUNTS.values()),
        "seeded_table_counts": {table: counts[table] for table in SEEDED_TABLE_COUNTS},
        "empty_shell_table_count": len(EMPTY_SHELL_TABLES),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-wiring", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = validate_manuscript_source_catalog_sqlite_shell(check_wiring=not args.skip_wiring)
    except ManuscriptSourceCatalogSqliteShellError as exc:
        print(f"T392 manuscript source-catalog SQLite shell validation failed: {exc}", file=sys.stderr)
        return 1
    print(
        "T392 manuscript source-catalog SQLite shell validation passed "
        f"({result['table_count']} tables, {result['seeded_row_count']} seeded source rows, "
        f"{result['empty_shell_table_count']} empty shell tables)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
