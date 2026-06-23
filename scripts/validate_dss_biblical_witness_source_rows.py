#!/usr/bin/env python3
"""Validate the T396 DSS biblical witness source-row population."""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import validate_manuscript_source_catalog_sqlite_shell as shell_validator

CONTROL = ROOT / ".ai" / "control" / "dss_biblical_witness_source_rows.yaml"
MANIFEST = (
    ROOT
    / "data"
    / "candidate"
    / "source_catalog"
    / "manuscript_reliability"
    / "sqlite"
    / "dss_biblical_witness_rows_manifest.yaml"
)
POPULATION_ROWS = (
    ROOT
    / "data"
    / "candidate"
    / "source_catalog"
    / "manuscript_reliability"
    / "sqlite"
    / "dss_biblical_witness_rows.jsonl"
)
ROADMAP_DOC = ROOT / "docs" / "roadmap" / "T396_DSS_BIBLICAL_WITNESS_SOURCE_ROWS.md"
TASK = ROOT / ".ai" / "tasks" / "T396.task.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T396" / "handoff.md"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
MAIN_TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"
ROADMAP_STATE = ROOT / "ROADMAP_STATE.yaml"
VALIDATE_ALL = ROOT / "scripts" / "validate_all.py"
DATA_MAP = ROOT / ".ai" / "control" / "DATA_MAP.md"

WITNESS_ID = "dss_great_isaiah_scroll_1qisa"
ALLOWED_SOURCE_URLS = {
    "https://dss.collections.imj.org.il/isaiah",
    "https://www.imj.org.il/en/collections/198208-0",
    "https://www.deadseascrolls.org.il/learn-about-the-scrolls/discovery-and-publication",
}
POPULATED_TABLE_COUNTS = {
    "scripture_holding_institution": 1,
    "scripture_catalog_witness_record": 1,
    "scripture_witness_identifier": 2,
    "scripture_witness_date_claim": 1,
    "scripture_witness_material_claim": 1,
    "scripture_witness_coverage_claim": 1,
    "scripture_witness_discovery_event": 1,
    "evidence_catalog_review_queue": 1,
}
ALLOWED_POPULATION_TABLES = set(POPULATED_TABLE_COUNTS)
COMMON_REQUIRED_ROW_FIELDS = shell_validator.COMMON_REQUIRED_ROW_FIELDS
FALSE_TEXT_FLAGS = {"stores_scripture_text", "stores_transcription_text", "stores_boundary_text"}
FORBIDDEN_ROW_KEYS = {
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
    "image_path",
    "image_text",
}
REQUIRED_FALSE_AUTHORITY = {
    "authorizes_general_witness_row_population",
    "authorizes_additional_dss_witnesses_without_row_level_sources",
    "authorizes_committed_sqlite_database_file",
    "authorizes_source_text_import",
    "authorizes_transcription_storage",
    "authorizes_bible_text_storage",
    "authorizes_image_ingestion",
    "authorizes_image_derived_text",
    "authorizes_canonical_bible_text_change",
    "authorizes_canonical_passage_record_change",
    "authorizes_chunk_output_change",
    "authorizes_reviewed_gold_promotion",
    "authorizes_textual_critical_decision",
    "authorizes_preferred_reading",
    "authorizes_source_tradition_preference",
    "authorizes_canon_scope_change",
    "authorizes_non_biblical_dss_import",
    "authorizes_boundary_import",
    "authorizes_commentary_or_patristic_import",
    "authorizes_doctrine_genealogy_import",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_embedding_or_vector_work",
    "authorizes_apologetic_conclusion_as_truth",
}
REQUIRED_WIRING = {
    FRONT_DOOR: [
        "dss_biblical_witness_source_rows.yaml",
        "T396 DSS biblical witness source rows",
        "scripts/validate_dss_biblical_witness_source_rows.py",
    ],
    MAIN_TOC: [
        "dss-biblical-witness-rows",
        "dss_biblical_witness_source_rows.yaml",
        "T396_DSS_BIBLICAL_WITNESS_SOURCE_ROWS.md",
    ],
    ROADMAP_TOC: [
        "T396 | DSS biblical witness source rows",
        "dss-biblical-witness-rows",
        "scripts/validate_dss_biblical_witness_source_rows.py",
    ],
    ROADMAP_STATE: ["T396", "DSS Biblical Witness Source Rows", "dss_biblical_witness_source_rows.yaml"],
    VALIDATE_ALL: ["validate_dss_biblical_witness_source_rows.py"],
    DATA_MAP: [
        "data/candidate/source_catalog/manuscript_reliability/sqlite/dss_biblical_witness_rows.jsonl",
        "data/candidate/source_catalog/manuscript_reliability/sqlite/dss_biblical_witness_rows_manifest.yaml",
    ],
}


class DssBiblicalWitnessSourceRowsError(ValueError):
    """Raised when the T396 DSS biblical witness rows are invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise DssBiblicalWitnessSourceRowsError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        data = shell_validator._read_yaml(path)
    except shell_validator.ManuscriptSourceCatalogSqliteShellError as exc:
        raise DssBiblicalWitnessSourceRowsError(str(exc)) from exc
    if not isinstance(data, dict):
        raise DssBiblicalWitnessSourceRowsError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise DssBiblicalWitnessSourceRowsError(f"{label} must be a mapping")
    return value


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DssBiblicalWitnessSourceRowsError(f"{label} must be a non-empty string")
    return value.strip()


def _require_string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise DssBiblicalWitnessSourceRowsError(f"{label} must be a non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise DssBiblicalWitnessSourceRowsError(f"{label} must contain only non-empty strings")
    return [item.strip() for item in value]


def _read_population_rows(path: Path = POPULATION_ROWS) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(_read_text(path).splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise DssBiblicalWitnessSourceRowsError(f"{_rel(path)}:{line_number}: invalid JSON: {exc}") from exc
        if not isinstance(record, dict):
            raise DssBiblicalWitnessSourceRowsError(f"{_rel(path)}:{line_number}: expected object")
        rows.append(record)
    return rows


def _validate_control_packet(data: dict[str, Any]) -> None:
    expected = {
        "object_type": "dss_biblical_witness_source_rows",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "dss_biblical_witness_source_rows.v1",
        "task_id": "T396",
        "status": "active_great_isaiah_exemplar_rows",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise DssBiblicalWitnessSourceRowsError(f"{_rel(CONTROL)}: {key} must be {value!r}")
    for key in ("provenance_note", "reason_for_inclusion"):
        _require_string(data.get(key), f"{_rel(CONTROL)}.{key}")

    authority = _require_mapping(data.get("authority"), f"{_rel(CONTROL)}.authority")
    for key in (
        "records_scoped_dss_biblical_witness_metadata_rows",
        "uses_t391_official_source_packet",
        "uses_t395_sqlite_schema_shell",
        "authorizes_scoped_great_isaiah_metadata_rows",
        "authorizes_in_memory_sqlite_validation",
    ):
        if authority.get(key) is not True:
            raise DssBiblicalWitnessSourceRowsError(f"{_rel(CONTROL)}: authority.{key} must be true")
    missing = sorted(REQUIRED_FALSE_AUTHORITY - set(authority))
    if missing:
        raise DssBiblicalWitnessSourceRowsError(f"{_rel(CONTROL)}: authority missing {missing}")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise DssBiblicalWitnessSourceRowsError(f"{_rel(CONTROL)}: authority.{key} must be false")

    row_scope = _require_mapping(data.get("row_scope"), f"{_rel(CONTROL)}.row_scope")
    if _require_mapping(row_scope.get("populated_tables"), "populated_tables") != POPULATED_TABLE_COUNTS:
        raise DssBiblicalWitnessSourceRowsError(f"{_rel(CONTROL)}: populated_tables mismatch")
    urls = set(_require_string_list(row_scope.get("allowed_source_urls"), "allowed_source_urls"))
    if urls != ALLOWED_SOURCE_URLS:
        raise DssBiblicalWitnessSourceRowsError(f"{_rel(CONTROL)}: allowed_source_urls mismatch")

    premortem = _require_mapping(data.get("premortem"), f"{_rel(CONTROL)}.premortem")
    if len(_require_string_list(premortem.get("p0_failure_modes"), "p0_failure_modes")) < 8:
        raise DssBiblicalWitnessSourceRowsError(f"{_rel(CONTROL)}: premortem must list P0 risks")
    if len(_require_string_list(premortem.get("fixes_applied"), "fixes_applied")) < 6:
        raise DssBiblicalWitnessSourceRowsError(f"{_rel(CONTROL)}: premortem fixes are incomplete")
    _require_mapping(data.get("red_team_result"), f"{_rel(CONTROL)}.red_team_result")


def _validate_manifest(data: dict[str, Any]) -> None:
    expected = {
        "object_type": "dss_biblical_witness_rows_manifest",
        "trust_zone": "candidate",
        "lifecycle_status": "active",
        "schema_version": "dss_biblical_witness_source_rows.v1",
        "manifest_id": "t396_dss_biblical_witness_rows_manifest",
        "task_id": "T396",
        "status": "active_great_isaiah_exemplar_rows",
        "schema_file": _rel(shell_validator.SCHEMA),
        "source_seed_file": _rel(shell_validator.SEED),
        "population_file": _rel(POPULATION_ROWS),
        "control_file": _rel(CONTROL),
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise DssBiblicalWitnessSourceRowsError(f"{_rel(MANIFEST)}: {key} must be {value!r}")
    if set(_require_string_list(data.get("allowed_witness_ids"), "allowed_witness_ids")) != {WITNESS_ID}:
        raise DssBiblicalWitnessSourceRowsError(f"{_rel(MANIFEST)}: allowed_witness_ids mismatch")
    if _require_mapping(data.get("allowed_population_tables"), "allowed_population_tables") != POPULATED_TABLE_COUNTS:
        raise DssBiblicalWitnessSourceRowsError(f"{_rel(MANIFEST)}: allowed_population_tables mismatch")
    if set(_require_string_list(data.get("allowed_source_urls"), "allowed_source_urls")) != ALLOWED_SOURCE_URLS:
        raise DssBiblicalWitnessSourceRowsError(f"{_rel(MANIFEST)}: allowed_source_urls mismatch")
    if set(_require_string_list(data.get("common_required_row_fields"), "common_required_row_fields")) != COMMON_REQUIRED_ROW_FIELDS:
        raise DssBiblicalWitnessSourceRowsError(f"{_rel(MANIFEST)}: common_required_row_fields mismatch")
    forbidden = set(_require_string_list(data.get("forbidden_row_keys"), "forbidden_row_keys"))
    if not FORBIDDEN_ROW_KEYS <= forbidden:
        raise DssBiblicalWitnessSourceRowsError(f"{_rel(MANIFEST)}: forbidden_row_keys incomplete")


def _validate_row(record: dict[str, Any], index: int) -> tuple[str, dict[str, Any]]:
    table = _require_string(record.get("table"), f"{_rel(POPULATION_ROWS)}:{index}.table")
    row = _require_mapping(record.get("row"), f"{_rel(POPULATION_ROWS)}:{index}.row")
    if table not in ALLOWED_POPULATION_TABLES:
        raise DssBiblicalWitnessSourceRowsError(f"{_rel(POPULATION_ROWS)}:{index}: forbidden population table {table}")
    missing = sorted(COMMON_REQUIRED_ROW_FIELDS - set(row))
    if missing:
        raise DssBiblicalWitnessSourceRowsError(f"{_rel(POPULATION_ROWS)}:{index}: row missing common fields {missing}")
    bad_keys = sorted(FORBIDDEN_ROW_KEYS & set(row))
    if bad_keys:
        raise DssBiblicalWitnessSourceRowsError(f"{_rel(POPULATION_ROWS)}:{index}: forbidden text-bearing keys {bad_keys}")
    if row["source_url"] not in ALLOWED_SOURCE_URLS:
        raise DssBiblicalWitnessSourceRowsError(f"{_rel(POPULATION_ROWS)}:{index}: source_url not allowed for T396")
    if row["confidence"] not in {"high", "medium", "low"}:
        raise DssBiblicalWitnessSourceRowsError(f"{_rel(POPULATION_ROWS)}:{index}: invalid confidence")
    for field in ("source_url", "method", "provenance_note", "review_status", "source_family", "rights_access_status"):
        _require_string(row.get(field), f"{_rel(POPULATION_ROWS)}:{index}.{field}")
    for flag in FALSE_TEXT_FLAGS:
        if row.get(flag) not in (0, False):
            raise DssBiblicalWitnessSourceRowsError(f"{_rel(POPULATION_ROWS)}:{index}: {flag} must be false/0")
    if table == "scripture_witness_coverage_claim" and row.get("stores_text") not in (0, False):
        raise DssBiblicalWitnessSourceRowsError(f"{_rel(POPULATION_ROWS)}:{index}: stores_text must be false/0")
    if "not" not in str(row["non_authorizing_scope_label"]).lower():
        raise DssBiblicalWitnessSourceRowsError(
            f"{_rel(POPULATION_ROWS)}:{index}: non_authorizing_scope_label must deny authority"
        )
    if table != "scripture_holding_institution":
        witness = row.get("witness_id_candidate", row.get("witness_or_catalog_ref", row.get("witness_group")))
        if witness != WITNESS_ID:
            raise DssBiblicalWitnessSourceRowsError(f"{_rel(POPULATION_ROWS)}:{index}: unexpected witness {witness!r}")
    return table, row


def _insert_population_rows(conn: sqlite3.Connection, records: list[dict[str, Any]]) -> dict[str, int]:
    counts = {table: 0 for table in ALLOWED_POPULATION_TABLES}
    for index, record in enumerate(records, start=1):
        table, row = _validate_row(record, index)
        counts[table] += 1
        columns = list(row)
        sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join('?' for _ in columns)})"
        try:
            conn.execute(sql, [row[column] for column in columns])
        except sqlite3.Error as exc:
            raise DssBiblicalWitnessSourceRowsError(
                f"{_rel(POPULATION_ROWS)}:{index}: SQLite insert failed for {table}: {exc}"
            ) from exc
    if counts != POPULATED_TABLE_COUNTS:
        raise DssBiblicalWitnessSourceRowsError(f"{_rel(POPULATION_ROWS)}: population counts mismatch {counts}")
    conn.commit()
    return counts


def _build_t396_database(records: list[dict[str, Any]]) -> sqlite3.Connection:
    t391_urls = shell_validator._t391_source_urls()
    if not ALLOWED_SOURCE_URLS <= t391_urls:
        missing = sorted(ALLOWED_SOURCE_URLS - t391_urls)
        raise DssBiblicalWitnessSourceRowsError(f"T396 source URLs must be in T391 curated sources: {missing}")
    schema_sql = shell_validator._read_text(shell_validator.SCHEMA)
    conn = shell_validator._build_database(schema_sql, shell_validator._read_seed(shell_validator.SEED), t391_urls)
    _insert_population_rows(conn, records)
    return conn


def _validate_database_counts(conn: sqlite3.Connection) -> dict[str, int]:
    tables = shell_validator.REQUIRED_TABLES
    counts = {table: int(conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]) for table in tables}
    for table, expected in shell_validator.SEEDED_TABLE_COUNTS.items():
        if counts[table] != expected:
            raise DssBiblicalWitnessSourceRowsError(f"{table}: expected {expected} T395 seed rows, found {counts[table]}")
    for table, expected in POPULATED_TABLE_COUNTS.items():
        if counts[table] != expected:
            raise DssBiblicalWitnessSourceRowsError(f"{table}: expected {expected} T396 rows, found {counts[table]}")
    return counts


def _validate_no_authority_contamination(conn: sqlite3.Connection) -> None:
    forbidden_objects = [
        str(row[0])
        for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE name LIKE 'canonical_%' OR name LIKE 'boundary_%' OR name LIKE 'doctrine_%'"
        ).fetchall()
    ]
    if forbidden_objects:
        raise DssBiblicalWitnessSourceRowsError(f"forbidden authority namespace objects found: {forbidden_objects}")


def _validate_wiring() -> None:
    for path, needles in REQUIRED_WIRING.items():
        text = _read_text(path)
        for needle in needles:
            if needle not in text:
                raise DssBiblicalWitnessSourceRowsError(f"{_rel(path)}: missing wiring string {needle!r}")
    for path in (ROADMAP_DOC, TASK, HANDOFF, MANIFEST, POPULATION_ROWS):
        if not path.exists():
            raise DssBiblicalWitnessSourceRowsError(f"{_rel(path)}: required T396 surface is missing")


def validate_dss_biblical_witness_source_rows(*, check_wiring: bool = True) -> dict[str, Any]:
    shell_validator.validate_manuscript_source_catalog_sqlite_shell(check_wiring=True)
    control = _read_yaml(CONTROL)
    manifest = _read_yaml(MANIFEST)
    _validate_control_packet(control)
    _validate_manifest(manifest)
    records = _read_population_rows()
    conn = _build_t396_database(records)
    try:
        _validate_no_authority_contamination(conn)
        counts = _validate_database_counts(conn)
    finally:
        conn.close()
    if check_wiring:
        _validate_wiring()
    return {
        "task_id": control["task_id"],
        "witness_id": WITNESS_ID,
        "population_row_count": sum(POPULATED_TABLE_COUNTS.values()),
        "population_table_counts": {table: counts[table] for table in POPULATED_TABLE_COUNTS},
        "seeded_row_count": sum(shell_validator.SEEDED_TABLE_COUNTS.values()),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-wiring", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = validate_dss_biblical_witness_source_rows(check_wiring=not args.skip_wiring)
    except DssBiblicalWitnessSourceRowsError as exc:
        print(f"T396 DSS biblical witness source-row validation failed: {exc}", file=sys.stderr)
        return 1
    except shell_validator.ManuscriptSourceCatalogSqliteShellError as exc:
        print(f"T396 DSS biblical witness source-row validation failed: {exc}", file=sys.stderr)
        return 1
    print(
        "T396 DSS biblical witness source-row validation passed "
        f"({result['population_row_count']} Great Isaiah exemplar rows; "
        f"{result['seeded_row_count']} T395 source seed rows loaded)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
