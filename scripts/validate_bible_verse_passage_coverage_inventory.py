#!/usr/bin/env python3
"""Validate the T386 Bible-wide verse/passage coverage inventory."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
PASSAGES = ROOT / "data" / "canonical" / "scripture" / "passages" / "passages.jsonl"
INVENTORY = ROOT / ".ai" / "control" / "bible_verse_passage_coverage_inventory.jsonl"
TAXONOMY = ROOT / ".ai" / "control" / "bible_verse_passage_coverage_taxonomy.yaml"
SUMMARY = ROOT / ".ai" / "control" / "bible_verse_passage_coverage_summary.yaml"
MATRIX = ROOT / ".ai" / "control" / "bible_verse_passage_readiness_matrix.yaml"
GAPS = ROOT / ".ai" / "control" / "bible_verse_passage_gap_register.yaml"
DOCKET = ROOT / ".ai" / "control" / "bible_verse_passage_human_review_docket.yaml"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
LESSON_INDEX = ROOT / ".ai" / "control" / "chunking_lesson_index.yaml"
READINESS = ROOT / ".ai" / "control" / "bible_chunking_readiness_map.yaml"
ROADMAP = ROOT / "ROADMAP_STATE.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
MAIN_TOC = ROOT / "AI_TABLE_OF_CONTENTS.md"
ROADMAP_TOC = ROOT / "docs" / "roadmap" / "AI_ROADMAP_TABLE_OF_CONTENTS.md"
ROADMAP_DOC = ROOT / "docs" / "roadmap" / "T386_BIBLE_VERSE_PASSAGE_COVERAGE_INVENTORY.md"
TASK = ROOT / ".ai" / "tasks" / "T386.task.yaml"
HANDOFF = ROOT / ".ai" / "handoffs" / "T386" / "handoff.md"
AUDIT_README = ROOT / ".ai" / "audits" / "reports" / "README.md"
AUDIT = ROOT / ".ai" / "audits" / "reports" / "20260622-T386-bible-verse-passage-coverage.md"

REQUIRED_STATUS = {
    "routine_under_existing_policy",
    "deeper_review_required",
    "human_decision_required",
    "blocked_before_chunking",
}

REQUIRED_FLAGS = {
    "translation_witness_missing",
    "source_metadata_sensitive",
    "strongs_metadata_present",
    "original_language_phrase_context_review",
    "textual_variant_source_tradition_sensitive",
    "editorial_cross_reference_present",
    "cross_reference_or_intertext_risk",
    "speaker_wj_red_letter_discourse_boundary_risk",
    "divine_name_title_capitalization_sensitive",
    "known_non_orthodox_pressure_passage",
    "theological_downstream_risk",
    "review_packet_needed",
    "human_owner_decision_required",
    "blocked_authority_action",
}

REQUIRED_DECISIONS = {
    "T386-HDM-001",
    "T386-HDM-002",
    "T386-HDM-003",
    "T386-HDM-004",
    "T386-HDM-005",
    "T386-HDM-006",
    "T386-HDM-007",
    "T386-HDM-008",
}

REQUIRED_AUTHORITY_FALSE = {
    "authorizes_chunk_output_change",
    "authorizes_reviewed_gold_promotion",
    "authorizes_child_spans",
    "authorizes_route_behavior_change",
    "authorizes_evaluator_change",
    "authorizes_graph_edges",
    "authorizes_retrieval_truth",
    "authorizes_embedding_or_vector_work",
    "authorizes_boundary_import",
    "authorizes_preferred_reading_or_source_tradition",
    "authorizes_canon_scope_change",
    "authorizes_denominational_systematic_theology_as_chunk_authority",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "chunk_output_change",
    "reviewed_gold_promotion",
    "child_span_selection",
    "route_behavior_change",
    "evaluator_change",
    "graph_edge_generation",
    "retrieval_truth",
    "embedding_or_vector_work",
    "boundary_import",
    "preferred_reading_selection",
    "source_tradition_preference",
    "canon_scope_change",
    "denominational_systematic_theology_as_chunk_authority",
}

REQUIRED_INVENTORY_FIELDS = {
    "schema_version",
    "coverage_id",
    "passage_id",
    "osis_ref",
    "book",
    "chapter",
    "verse_start",
    "verse_end",
    "lane_id",
    "coverage_status",
    "flags",
    "source_evidence_counts",
    "source_surface_ids",
    "owner_decision_ids",
    "non_authorizations",
}

REQUIRED_COUNT_FIELDS = {
    "translation_witnesses",
    "word_tokens",
    "strongs_tokens",
    "wj_tokens",
    "footnotes",
    "alternate_reading_footnotes",
    "hebrew_word_footnotes",
    "greek_word_footnotes",
    "editorial_cross_references",
    "boundary_claims",
    "divine_capitalization_tokens",
}

REQUIRED_WIRING_STRINGS = {
    FRONT_DOOR: [
        "bible_verse_passage_coverage_inventory.jsonl",
        "bible_verse_passage_human_review_docket.yaml",
        "T386 Bible-wide verse/passage coverage",
    ],
    MAIN_TOC: [
        "verse-passage-coverage",
        "bible_verse_passage_coverage_inventory.jsonl",
        "bible_verse_passage_human_review_docket.yaml",
    ],
    ROADMAP_TOC: ["T386_BIBLE_VERSE_PASSAGE_COVERAGE_INVENTORY.md", "verse-passage-coverage"],
    REGISTER: ["CD-062", "T386", "bible_verse_passage_coverage_inventory.jsonl"],
    PREFLIGHT: [
        "bible_verse_passage_coverage_summary.yaml",
        "bible_verse_passage_gap_register.yaml",
        "bible_verse_passage_human_review_docket.yaml",
    ],
    LESSON_INDEX: ["LSN-014", "verse-passage-coverage", "T386"],
    READINESS: ["T386", "bible_verse_passage_coverage_summary.yaml", "T385"],
    ROADMAP: ["T386", "Bible-Wide Verse/Passage Coverage Inventory", "T385"],
    str(AUDIT_README): ["20260622-T386-bible-verse-passage-coverage.md"],
}


class CoverageInventoryError(ValueError):
    """Raised when the Bible-wide coverage inventory is invalid."""


def _rel(path: Path | str) -> str:
    path = Path(path)
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise CoverageInventoryError(f"{_rel(path)}: unreadable: {exc}") from exc


def _strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            return parts[1] + "\n" + parts[2]
    return text


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _strip_frontmatter(_read_text(path))
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise CoverageInventoryError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise CoverageInventoryError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        with path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                try:
                    item = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise CoverageInventoryError(f"{_rel(path)}:{line_number}: invalid JSON: {exc}") from exc
                if not isinstance(item, dict):
                    raise CoverageInventoryError(f"{_rel(path)}:{line_number}: expected JSON object")
                rows.append(item)
    except OSError as exc:
        raise CoverageInventoryError(f"{_rel(path)}: unreadable: {exc}") from exc
    return rows


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise CoverageInventoryError(f"{_rel(path)}: unreadable: {exc}") from exc
    return digest.hexdigest()


def _require_string_list(value: Any, label: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not allow_empty and not value):
        raise CoverageInventoryError(f"{label} must be a {'possibly empty ' if allow_empty else ''}list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise CoverageInventoryError(f"{label} must contain only non-empty strings")
    return [str(item) for item in value]


def _canonical_refs() -> tuple[list[str], dict[str, dict[str, Any]]]:
    passages = _read_jsonl(PASSAGES)
    refs: list[str] = []
    by_ref: dict[str, dict[str, Any]] = {}
    for passage in passages:
        ref = passage.get("osis_ref")
        if not isinstance(ref, str):
            raise CoverageInventoryError(f"{_rel(PASSAGES)}: canonical passage missing osis_ref")
        if ref in by_ref:
            raise CoverageInventoryError(f"{_rel(PASSAGES)}: duplicate canonical ref {ref}")
        refs.append(ref)
        by_ref[ref] = passage
    if len(refs) != 31103:
        raise CoverageInventoryError(f"{_rel(PASSAGES)}: expected 31103 canonical passages, found {len(refs)}")
    books = {str(passage.get("book")) for passage in passages}
    if len(books) != 66:
        raise CoverageInventoryError(f"{_rel(PASSAGES)}: expected 66 canonical books, found {len(books)}")
    return refs, by_ref


def _validate_taxonomy(data: dict[str, Any]) -> None:
    expected = {
        "object_type": "bible_verse_passage_coverage_taxonomy",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "bible_verse_passage_coverage_taxonomy.v1",
        "taxonomy_id": "t386_bible_verse_passage_coverage_taxonomy",
        "task_id": "T386",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise CoverageInventoryError(f"{_rel(TAXONOMY)}: {key} must be {value!r}")
    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise CoverageInventoryError(f"{_rel(TAXONOMY)}: authority must be a mapping")
    if authority.get("records_coverage") is not True:
        raise CoverageInventoryError(f"{_rel(TAXONOMY)}: authority.records_coverage must be true")
    for key in REQUIRED_AUTHORITY_FALSE:
        if authority.get(key) is not False:
            raise CoverageInventoryError(f"{_rel(TAXONOMY)}: authority.{key} must be false")
    statuses = {
        item.get("status")
        for item in data.get("coverage_statuses", [])
        if isinstance(item, dict)
    }
    if statuses != REQUIRED_STATUS:
        raise CoverageInventoryError(f"{_rel(TAXONOMY)}: coverage_statuses must be {sorted(REQUIRED_STATUS)}")
    if set(data.get("flag_taxonomy", [])) != REQUIRED_FLAGS:
        raise CoverageInventoryError(f"{_rel(TAXONOMY)}: flag_taxonomy must match required flags")
    if set(data.get("decision_id_taxonomy", [])) != REQUIRED_DECISIONS:
        raise CoverageInventoryError(f"{_rel(TAXONOMY)}: decision_id_taxonomy must match required decisions")


def _validate_inventory(
    path: Path,
    canonical_refs: list[str],
    canonical_by_ref: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], Counter[str], Counter[str], Counter[str]]:
    rows = _read_jsonl(path)
    by_ref: dict[str, dict[str, Any]] = {}
    status_counts: Counter[str] = Counter()
    flag_counts: Counter[str] = Counter()
    decision_counts: Counter[str] = Counter()
    seen_refs: set[str] = set()
    for index, row in enumerate(rows, start=1):
        label = f"{_rel(path)}:{index}"
        missing = sorted(REQUIRED_INVENTORY_FIELDS - set(row))
        if missing:
            raise CoverageInventoryError(f"{label}: missing fields {missing}")
        ref = row.get("osis_ref")
        if ref not in canonical_by_ref:
            raise CoverageInventoryError(f"{label}: noncanonical or unknown osis_ref {ref!r}")
        if ref in seen_refs:
            raise CoverageInventoryError(f"{label}: duplicate coverage record for {ref}")
        seen_refs.add(str(ref))
        canonical = canonical_by_ref[str(ref)]
        if row.get("passage_id") != canonical.get("id"):
            raise CoverageInventoryError(f"{label}: passage_id does not match canonical passage")
        for key in ("book", "chapter", "verse_start", "verse_end"):
            if row.get(key) != canonical.get(key):
                raise CoverageInventoryError(f"{label}: {key} does not match canonical passage")
        if row.get("schema_version") != "bible_verse_passage_coverage.v1":
            raise CoverageInventoryError(f"{label}: invalid schema_version")
        if row.get("coverage_id") != f"coverage:{ref}":
            raise CoverageInventoryError(f"{label}: invalid coverage_id")
        status = row.get("coverage_status")
        if status not in REQUIRED_STATUS:
            raise CoverageInventoryError(f"{label}: invalid coverage_status {status!r}")
        flags = set(_require_string_list(row.get("flags"), f"{label}.flags", allow_empty=True))
        invalid_flags = sorted(flags - REQUIRED_FLAGS)
        if invalid_flags:
            raise CoverageInventoryError(f"{label}: invalid flags {invalid_flags}")
        decision_ids = set(_require_string_list(row.get("owner_decision_ids"), f"{label}.owner_decision_ids", allow_empty=True))
        invalid_decisions = sorted(decision_ids - REQUIRED_DECISIONS)
        if invalid_decisions:
            raise CoverageInventoryError(f"{label}: invalid owner decision ids {invalid_decisions}")
        non_auth = set(_require_string_list(row.get("non_authorizations"), f"{label}.non_authorizations"))
        missing_non_auth = sorted(REQUIRED_NON_AUTHORIZATIONS - non_auth)
        if missing_non_auth:
            raise CoverageInventoryError(f"{label}: missing non_authorizations {missing_non_auth}")
        counts = row.get("source_evidence_counts")
        if not isinstance(counts, dict):
            raise CoverageInventoryError(f"{label}: source_evidence_counts must be a mapping")
        if set(counts) != REQUIRED_COUNT_FIELDS:
            raise CoverageInventoryError(f"{label}: source_evidence_counts keys must match required fields")
        for count_key, count_value in counts.items():
            if not isinstance(count_value, int) or count_value < 0:
                raise CoverageInventoryError(f"{label}: count {count_key} must be a non-negative integer")
        if "blocked_authority_action" in flags and status != "blocked_before_chunking":
            raise CoverageInventoryError(f"{label}: blocked_authority_action must use blocked_before_chunking status")
        if "human_owner_decision_required" in flags and status == "routine_under_existing_policy":
            raise CoverageInventoryError(f"{label}: human_owner_decision_required cannot be routine")
        if "source_metadata_sensitive" in flags and counts["word_tokens"] == 0 and counts["footnotes"] == 0 and counts["editorial_cross_references"] == 0 and counts["boundary_claims"] == 0:
            raise CoverageInventoryError(f"{label}: source_metadata_sensitive requires source evidence counts")
        status_counts[str(status)] += 1
        for flag in flags:
            flag_counts[flag] += 1
        for decision_id in decision_ids:
            decision_counts[decision_id] += 1
        by_ref[str(ref)] = row

    missing_refs = sorted(set(canonical_refs) - seen_refs, key=canonical_refs.index)
    extra_refs = sorted(seen_refs - set(canonical_refs))
    if missing_refs:
        raise CoverageInventoryError(f"{_rel(path)}: missing coverage for {len(missing_refs)} canonical refs; first missing {missing_refs[:5]}")
    if extra_refs:
        raise CoverageInventoryError(f"{_rel(path)}: extra refs {extra_refs[:5]}")
    if len(rows) != len(canonical_refs):
        raise CoverageInventoryError(f"{_rel(path)}: expected {len(canonical_refs)} records, found {len(rows)}")
    for required_flag in REQUIRED_FLAGS - {"translation_witness_missing"}:
        if flag_counts[required_flag] <= 0:
            raise CoverageInventoryError(f"{_rel(path)}: required flag {required_flag} has no coverage records")
    for required_decision in REQUIRED_DECISIONS - {"T386-HDM-008"}:
        if decision_counts[required_decision] <= 0:
            raise CoverageInventoryError(f"{_rel(path)}: required decision {required_decision} has no coverage records")
    return rows, by_ref, status_counts, flag_counts, decision_counts


def _validate_summary(
    data: dict[str, Any],
    digest: str,
    status_counts: Counter[str],
    flag_counts: Counter[str],
    decision_counts: Counter[str],
) -> None:
    expected = {
        "object_type": "bible_verse_passage_coverage_summary",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "bible_verse_passage_coverage_summary.v1",
        "summary_id": "t386_bible_verse_passage_coverage_summary",
        "task_id": "T386",
        "canonical_scope": "canonical_66",
        "canonical_book_count": 66,
        "canonical_passage_count": 31103,
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise CoverageInventoryError(f"{_rel(SUMMARY)}: {key} must be {value!r}")
    if data.get("inventory_sha256") != digest:
        raise CoverageInventoryError(f"{_rel(SUMMARY)}: inventory_sha256 does not match inventory")
    if data.get("status_counts") != dict(sorted(status_counts.items())):
        raise CoverageInventoryError(f"{_rel(SUMMARY)}: status_counts do not match inventory")
    if data.get("flag_counts") != dict(sorted(flag_counts.items())):
        raise CoverageInventoryError(f"{_rel(SUMMARY)}: flag_counts do not match inventory")
    if data.get("owner_decision_counts") != dict(sorted(decision_counts.items())):
        raise CoverageInventoryError(f"{_rel(SUMMARY)}: owner_decision_counts do not match inventory")


def _validate_matrix(
    data: dict[str, Any],
    digest: str,
    records: dict[str, dict[str, Any]],
) -> None:
    if data.get("object_type") != "bible_verse_passage_readiness_matrix":
        raise CoverageInventoryError(f"{_rel(MATRIX)}: object_type must be bible_verse_passage_readiness_matrix")
    if data.get("task_id") != "T386":
        raise CoverageInventoryError(f"{_rel(MATRIX)}: task_id must be T386")
    if data.get("inventory_sha256") != digest:
        raise CoverageInventoryError(f"{_rel(MATRIX)}: inventory_sha256 does not match inventory")
    book_counts: dict[str, Counter[str]] = defaultdict(Counter)
    book_flags: dict[str, Counter[str]] = defaultdict(Counter)
    lane_counts: dict[str, Counter[str]] = defaultdict(Counter)
    lane_flags: dict[str, Counter[str]] = defaultdict(Counter)
    lane_books: dict[str, set[str]] = defaultdict(set)
    for record in records.values():
        book = str(record["book"])
        lane = str(record["lane_id"])
        status = str(record["coverage_status"])
        book_counts[book][status] += 1
        lane_counts[lane][status] += 1
        lane_books[lane].add(book)
        for flag in record["flags"]:
            book_flags[book][flag] += 1
            lane_flags[lane][flag] += 1
    book_matrix = data.get("book_matrix")
    if not isinstance(book_matrix, list) or len(book_matrix) != 66:
        raise CoverageInventoryError(f"{_rel(MATRIX)}: book_matrix must include 66 books")
    matrix_books = {item.get("book") for item in book_matrix if isinstance(item, dict)}
    if matrix_books != set(book_counts):
        raise CoverageInventoryError(f"{_rel(MATRIX)}: book_matrix books do not match inventory")
    for item in book_matrix:
        if not isinstance(item, dict):
            raise CoverageInventoryError(f"{_rel(MATRIX)}: each book_matrix item must be a mapping")
        book = str(item.get("book"))
        if item.get("passage_count") != sum(book_counts[book].values()):
            raise CoverageInventoryError(f"{_rel(MATRIX)}:{book}: passage_count mismatch")
        if item.get("status_counts") != dict(sorted(book_counts[book].items())):
            raise CoverageInventoryError(f"{_rel(MATRIX)}:{book}: status_counts mismatch")
        if item.get("flag_counts") != dict(sorted(book_flags[book].items())):
            raise CoverageInventoryError(f"{_rel(MATRIX)}:{book}: flag_counts mismatch")
    lane_matrix = data.get("lane_matrix")
    if not isinstance(lane_matrix, list) or not lane_matrix:
        raise CoverageInventoryError(f"{_rel(MATRIX)}: lane_matrix must be a non-empty list")
    matrix_lanes = {item.get("lane_id") for item in lane_matrix if isinstance(item, dict)}
    if matrix_lanes != set(lane_counts):
        raise CoverageInventoryError(f"{_rel(MATRIX)}: lane_matrix lanes do not match inventory")
    for item in lane_matrix:
        if not isinstance(item, dict):
            raise CoverageInventoryError(f"{_rel(MATRIX)}: each lane_matrix item must be a mapping")
        lane = str(item.get("lane_id"))
        if item.get("book_count") != len(lane_books[lane]):
            raise CoverageInventoryError(f"{_rel(MATRIX)}:{lane}: book_count mismatch")
        if item.get("passage_count") != sum(lane_counts[lane].values()):
            raise CoverageInventoryError(f"{_rel(MATRIX)}:{lane}: passage_count mismatch")
        if item.get("status_counts") != dict(sorted(lane_counts[lane].items())):
            raise CoverageInventoryError(f"{_rel(MATRIX)}:{lane}: status_counts mismatch")
        if item.get("flag_counts") != dict(sorted(lane_flags[lane].items())):
            raise CoverageInventoryError(f"{_rel(MATRIX)}:{lane}: flag_counts mismatch")


def _validate_gaps(data: dict[str, Any], digest: str, flag_counts: Counter[str]) -> None:
    if data.get("object_type") != "bible_verse_passage_gap_register":
        raise CoverageInventoryError(f"{_rel(GAPS)}: object_type must be bible_verse_passage_gap_register")
    if data.get("task_id") != "T386":
        raise CoverageInventoryError(f"{_rel(GAPS)}: task_id must be T386")
    if data.get("inventory_sha256") != digest:
        raise CoverageInventoryError(f"{_rel(GAPS)}: inventory_sha256 does not match inventory")
    entries = data.get("gap_entries")
    if not isinstance(entries, list) or not entries:
        raise CoverageInventoryError(f"{_rel(GAPS)}: gap_entries must be a non-empty list")
    entry_flags = {entry.get("flag") for entry in entries if isinstance(entry, dict)}
    if entry_flags != set(flag_counts):
        raise CoverageInventoryError(f"{_rel(GAPS)}: gap_entries flags do not match inventory")
    for entry in entries:
        if not isinstance(entry, dict):
            raise CoverageInventoryError(f"{_rel(GAPS)}: gap entry must be a mapping")
        flag = str(entry.get("flag"))
        if entry.get("passage_count") != flag_counts[flag]:
            raise CoverageInventoryError(f"{_rel(GAPS)}:{flag}: passage_count mismatch")
        sample_refs = _require_string_list(entry.get("sample_refs"), f"{_rel(GAPS)}:{flag}.sample_refs")
        if len(sample_refs) > 12:
            raise CoverageInventoryError(f"{_rel(GAPS)}:{flag}: sample_refs must stay compact")
        if entry.get("authority_status") != "evidence_only_non_authorizing":
            raise CoverageInventoryError(f"{_rel(GAPS)}:{flag}: authority_status must be evidence_only_non_authorizing")


def _validate_docket(data: dict[str, Any]) -> None:
    expected = {
        "object_type": "bible_verse_passage_human_review_docket",
        "trust_zone": "canonical",
        "lifecycle_status": "active",
        "schema_version": "bible_verse_passage_human_review_docket.v1",
        "docket_id": "t386_bible_verse_passage_human_review_docket",
        "task_id": "T386",
        "orthodoxy_boundary": "nicene_chalcedonian_core",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise CoverageInventoryError(f"{_rel(DOCKET)}: {key} must be {value!r}")
    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise CoverageInventoryError(f"{_rel(DOCKET)}: authority must be a mapping")
    for key in REQUIRED_AUTHORITY_FALSE:
        if authority.get(key) is not False:
            raise CoverageInventoryError(f"{_rel(DOCKET)}: authority.{key} must be false")
    decisions = data.get("decisions")
    if not isinstance(decisions, list):
        raise CoverageInventoryError(f"{_rel(DOCKET)}: decisions must be a list")
    decision_ids = {item.get("decision_id") for item in decisions if isinstance(item, dict)}
    if decision_ids != REQUIRED_DECISIONS:
        raise CoverageInventoryError(f"{_rel(DOCKET)}: decisions must match {sorted(REQUIRED_DECISIONS)}")
    for item in decisions:
        if not isinstance(item, dict):
            raise CoverageInventoryError(f"{_rel(DOCKET)}: each decision must be a mapping")
        label = f"{_rel(DOCKET)}:{item.get('decision_id')}"
        for key in ("title", "recommended_conservative_path"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                raise CoverageInventoryError(f"{label}: {key} must be a non-empty string")
        _require_string_list(item.get("trigger_flags"), f"{label}.trigger_flags")
        _require_string_list(item.get("stop_conditions"), f"{label}.stop_conditions")
        options = item.get("faithful_options")
        if not isinstance(options, list) or not options:
            raise CoverageInventoryError(f"{label}: faithful_options must be a non-empty list")
    next_step = data.get("exact_next_non_output_step")
    if not isinstance(next_step, dict) or next_step.get("task_id") != "T385":
        raise CoverageInventoryError(f"{_rel(DOCKET)}: exact_next_non_output_step.task_id must be T385")
    for key in ("output_change_authorized", "reviewed_gold_promoted", "implementation_authorized"):
        if next_step.get(key) is not False:
            raise CoverageInventoryError(f"{_rel(DOCKET)}: exact_next_non_output_step.{key} must be false")


def _validate_repo_wiring() -> None:
    for path, required_strings in REQUIRED_WIRING_STRINGS.items():
        real_path = Path(path)
        if not real_path.is_absolute():
            real_path = ROOT / real_path
        text = _read_text(real_path)
        for needle in required_strings:
            if needle not in text:
                raise CoverageInventoryError(f"{_rel(real_path)}: missing required T386 wiring string {needle!r}")
    for path in (ROADMAP_DOC, TASK, HANDOFF, AUDIT):
        if not path.exists():
            raise CoverageInventoryError(f"{_rel(path)}: required T386 surface is missing")


def validate_bible_verse_passage_coverage_inventory(
    inventory_path: Path = INVENTORY,
    *,
    check_generated_summaries: bool = True,
    check_repo_wiring: bool = True,
) -> dict[str, Any]:
    taxonomy = _read_yaml(TAXONOMY)
    _validate_taxonomy(taxonomy)
    canonical_refs, canonical_by_ref = _canonical_refs()
    rows, records, status_counts, flag_counts, decision_counts = _validate_inventory(
        inventory_path,
        canonical_refs,
        canonical_by_ref,
    )
    if check_generated_summaries:
        digest = _sha256(inventory_path)
        _validate_summary(_read_yaml(SUMMARY), digest, status_counts, flag_counts, decision_counts)
        _validate_matrix(_read_yaml(MATRIX), digest, records)
        _validate_gaps(_read_yaml(GAPS), digest, flag_counts)
        _validate_docket(_read_yaml(DOCKET))
    if check_repo_wiring:
        _validate_repo_wiring()
    return {
        "inventory_path": inventory_path,
        "record_count": len(rows),
        "status_counts": dict(sorted(status_counts.items())),
        "flag_counts": dict(sorted(flag_counts.items())),
        "owner_decision_counts": dict(sorted(decision_counts.items())),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", type=Path, default=INVENTORY)
    parser.add_argument("--skip-generated-summaries", action="store_true")
    parser.add_argument("--skip-repo-wiring", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = validate_bible_verse_passage_coverage_inventory(
            args.inventory,
            check_generated_summaries=not args.skip_generated_summaries,
            check_repo_wiring=not args.skip_repo_wiring,
        )
    except CoverageInventoryError as exc:
        print(f"T386 Bible-wide verse/passage coverage validation failed: {exc}", file=sys.stderr)
        return 1
    print(
        "T386 Bible-wide verse/passage coverage validation passed "
        f"({result['record_count']} canonical passage records)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
