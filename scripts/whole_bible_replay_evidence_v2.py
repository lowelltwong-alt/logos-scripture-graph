#!/usr/bin/env python3
"""Version-2 replay primitives for attempt-scoped B00/B01 evidence.

The v1 module remains immutable historical machinery for revision-6 receipts.
This module deliberately supports only B00 and B01.  Later stages fail closed
until they receive the same attempt-scoped migration.
"""
from __future__ import annotations

import json
import re
import zipfile
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable
from xml.etree import ElementTree

from scripts import whole_bible_replay_evidence as v1

ROOT = v1.ROOT
FAMILY = v1.FAMILY
MODEL_ROOT = v1.DEFAULT_MODEL_ROOT
CAMPAIGN = MODEL_ROOT / "campaign.rev7.json"
REGISTRY = FAMILY / "whole_bible_campaign_registry.v1.json"
WORKFLOW = FAMILY / "whole_bible_candidate_workflow.v2.yaml"
PROMPTS = FAMILY / "whole_bible_candidate_prompt_pack.v2.yaml"
ADAPTER = FAMILY / "codex_desktop_campaign_adapter.v2.yaml"
RUNBOOK = ROOT / "docs" / "governance" / "WHOLE_BIBLE_B01_REPLAY_RUNBOOK.md"
STAGE_SCHEMA = FAMILY / "whole_bible_stage_receipt.schema.v2.json"
MANIFEST_SCHEMA = FAMILY / "whole_bible_artifact_manifest.schema.v2.json"
PREPARED_SCHEMA = FAMILY / "whole_bible_prepared_stage_commit.schema.v1.json"
B01_EXECUTION_SCHEMA = FAMILY / "whole_bible_b01_prompt_execution.schema.v1.json"
B01_LEDGER_SCHEMA = FAMILY / "whole_bible_b01_execution_ledger.schema.v1.json"
SUPPORTED_STAGES = ("B00", "B01")
AUTHORIZED_STAGES = ("B00",)
B01_MATERIALIZATION_ENABLED = False
SAFE_ID = v1.SAFE_ID
SUCCESS_OUTCOMES = v1.SUCCESS_OUTCOMES
ReplayEvidenceError = v1.ReplayEvidenceError

load_json = v1.load_json
load_yaml = v1.load_yaml
canonical_bytes = v1.canonical_bytes
digest_bytes = v1.digest_bytes
digest_file = v1.digest_file
repo_relative = v1.repo_relative
resolve_repo_path = v1.resolve_repo_path
parse_time = v1.parse_time
validate_schema = v1.validate_schema
atomic_write = v1.atomic_write
exclusive_lock = v1.exclusive_lock
campaign_job = v1.campaign_job
stage_plan = v1.stage_plan
run_dir = v1.run_dir
read_index = v1.read_index
append_receipt_log = v1.append_receipt_log

REQUIRED_PROMPTS = (
    "original_language_translation_scout",
    "literary_form_scout",
    "canonical_relations_and_premortem_scout",
    "second_temple_rabbinic_context_scout",
)
EXPECTED_ROLES = {
    "original_language_translation_scout": "original_language_translation_specialist",
    "literary_form_scout": "literary_form_specialist",
    "canonical_relations_and_premortem_scout": "canonical_intertext_specialist",
    "second_temple_rabbinic_context_scout": "bounded_ancient_jewish_context_specialist",
}
REQUIRED_B01_OUTPUT_IDS = {
    "book_strategy", "form_inventory", "hardest_passage_forecast",
    "source_gap_register", "ancient_context_gap_or_qualified_receipt",
    "b01_execution_ledger", "b01_role_report", "synthesis_lineage", "b01_integrity_scan",
    "b01_boss_authorization",
}
FORBIDDEN_B01_KEYS = {
    "chunks", "chunk_map", "chunk_id", "chunk_index", "chunk_index_in_book",
    "decision_id", "selected_boundary", "final_boundary", "reviewed_gold",
    "final_chunk_map", "final_chunk_map_present", "chain_of_thought",
    "hidden_reasoning", "system_prompt", "user_prompt", "assistant_prompt",
    "messages", "conversation", "hebrew_text", "greek_text", "source_text",
}
REQUIRED_B01_HOLDS = {
    "NUM-B01-HOLD-ANCIENT-CONTEXT-CORPUS",
    "NUM-B01-HOLD-TOKEN-CROSSWALK",
    "NUM-B01-HOLD-EXTERNAL-INDEPENDENCE",
}


def validate_runtime_contract(*, campaign_path: Path = CAMPAIGN, registry_path: Path = REGISTRY,
                              root: Path = ROOT, model_root: Path = MODEL_ROOT,
                              allow_test_roots: bool = False) -> dict[str, Any]:
    if not allow_test_roots:
        if root.resolve() != ROOT.resolve() or model_root.resolve() != MODEL_ROOT.resolve():
            raise ReplayEvidenceError("QF-13-ADAPTER-SPLIT", "non-authoritative v2 roots")
        if campaign_path.resolve() != CAMPAIGN.resolve() or registry_path.resolve() != REGISTRY.resolve():
            raise ReplayEvidenceError("QF-13-ADAPTER-SPLIT", "non-registry v2 campaign")
    registry = load_json(registry_path)
    required = {"schema_version", "registry_id", "campaign_path", "campaign_sha256", "contract_files", "candidate_only", "non_authorizing"}
    if set(registry) != required or registry.get("schema_version") != "whole_bible_campaign_registry.v1" or registry.get("candidate_only") is not True or registry.get("non_authorizing") is not True:
        raise ReplayEvidenceError("QF-SCHEMA", "campaign registry shape")
    if registry.get("campaign_path") != repo_relative(campaign_path, root) or registry.get("campaign_sha256") != digest_file(campaign_path):
        raise ReplayEvidenceError("QF-02-FORGED-CHAIN", "registry campaign binding stale")
    expected_paths = {_display_path(path, root) for path in (
        WORKFLOW, PROMPTS, ADAPTER, RUNBOOK, STAGE_SCHEMA, MANIFEST_SCHEMA, PREPARED_SCHEMA,
        ROOT / "scripts" / "whole_bible_replay_evidence_v2.py",
        ROOT / "scripts" / "write_whole_bible_stage_receipt_v2.py",
        ROOT / "scripts" / "build_whole_bible_b00_preflight_v2.py",
        ROOT / "scripts" / "validate_whole_bible_stage_receipts_v2.py",
        ROOT / "scripts" / "validate_whole_bible_candidate_workflow_v2.py",
        ROOT / "scripts" / "upgrade_whole_bible_campaign_rev7.py",
        ROOT / "tests" / "test_whole_bible_replay_evidence_v2.py",
    )}
    rows = registry.get("contract_files")
    if not isinstance(rows, list) or {row.get("path") for row in rows if isinstance(row, dict)} != expected_paths:
        raise ReplayEvidenceError("QF-02-FORGED-CHAIN", "registry contract closure")
    for row in rows:
        path = resolve_repo_path(row["path"], root)
        if not path.is_file() or row.get("sha256") != digest_file(path):
            raise ReplayEvidenceError("QF-02-FORGED-CHAIN", f"stale registry contract file: {row.get('path')}")
    return registry


def attempt_root(model_root: Path, book: str, run_id: str, stage_id: str, attempt_id: str) -> Path:
    if stage_id not in SUPPORTED_STAGES or not SAFE_ID.fullmatch(run_id) or not SAFE_ID.fullmatch(attempt_id):
        raise ReplayEvidenceError("QF-SCHEMA", "unsafe v2 attempt identity")
    return run_dir(model_root, book, run_id) / "attempts" / stage_id / attempt_id


def validate_attempt_bundle_paths(*, draft_path: Path, input_manifest_path: Path,
                                  output_manifest_path: Path, model_root: Path,
                                  book: str, run_id: str, stage_id: str,
                                  attempt_id: str) -> Path:
    base = attempt_root(model_root, book, run_id, stage_id, attempt_id).resolve()
    expected = {
        draft_path.resolve(): base / "draft.json",
        input_manifest_path.resolve(): base / "manifests" / "input.json",
        output_manifest_path.resolve(): base / "manifests" / "output.json",
    }
    for actual, required in expected.items():
        if actual != required:
            raise ReplayEvidenceError("QF-12-IMMUTABLE-ATTEMPT", f"attempt bundle path mismatch: {actual}")
    return base


def _job_path_authorized(normalized: str, job: dict[str, Any], *, run_id: str, attempt_id: str, direction: str) -> bool:
    if direction == "input" and normalized == repo_relative(REGISTRY):
        return True
    templates = list(job.get("inputs") or []) if direction == "input" else list(job.get("outputs") or []) + list(job.get("allowed_paths") or [])
    for template in templates:
        pattern = re.escape(str(template).replace("\\", "/"))
        pattern = pattern.replace(re.escape("<run_id>"), re.escape(run_id))
        pattern = pattern.replace(re.escape("<RunId>"), re.escape(run_id))
        pattern = pattern.replace(re.escape("<attempt_id>"), re.escape(attempt_id))
        if re.fullmatch(pattern, normalized):
            return True
    return False


def validate_artifact_manifest(path: Path, *, root: Path, model_root: Path, job: dict[str, Any],
                               book: str, run_id: str, stage_id: str, attempt_id: str,
                               direction: str) -> tuple[dict[str, Any], dict[str, str], dict[str, str]]:
    manifest = load_json(path)
    validate_schema(manifest, MANIFEST_SCHEMA, "v2 artifact manifest")
    expected = {"book": book, "run_id": run_id, "stage_id": stage_id, "attempt_id": attempt_id, "direction": direction}
    if any(manifest.get(key) != value for key, value in expected.items()):
        raise ReplayEvidenceError("QF-02-FORGED-CHAIN", "v2 manifest identity")
    if direction == "output" and any(manifest.get(key) is not False for key in ("contains_scripture_text", "contains_source_rows", "contains_prompts_or_hidden_reasoning")):
        raise ReplayEvidenceError("QF-10-AUTHORITY-SMUGGLING", "v2 output payload declaration")
    if direction == "input" and manifest.get("contains_prompts_or_hidden_reasoning") is not False:
        raise ReplayEvidenceError("QF-10-AUTHORITY-SMUGGLING", "runtime prompt payload is forbidden")
    ids: dict[str, str] = {}
    hashes: dict[str, str] = {}
    seen_paths: set[str] = set()
    base = attempt_root(model_root, book, run_id, stage_id, attempt_id).resolve()
    model_prefix = repo_relative(model_root, root).rstrip("/") + "/"
    for row in manifest["artifacts"]:
        artifact_id = row["artifact_id"]
        if artifact_id in ids:
            raise ReplayEvidenceError("QF-SCHEMA", f"duplicate artifact id: {artifact_id}")
        artifact = resolve_repo_path(row["path"], root)
        if artifact.is_symlink() or not artifact.is_file():
            raise ReplayEvidenceError("QF-02-FORGED-CHAIN", f"missing/symlink artifact: {row['path']}")
        normalized = repo_relative(artifact, root)
        if not _job_path_authorized(normalized, job, run_id=run_id, attempt_id=attempt_id, direction=direction):
            raise ReplayEvidenceError("QF-08-SIBLING-CONTAMINATION", f"outside direction-specific job allowlist: {normalized}")
        if normalized in seen_paths:
            raise ReplayEvidenceError("QF-SCHEMA", f"duplicate physical artifact path: {normalized}")
        seen_paths.add(normalized)
        if normalized.startswith(".ai/scratch/multi_model_bible_chunking/") and not normalized.startswith(model_prefix):
            raise ReplayEvidenceError("QF-08-SIBLING-CONTAMINATION", normalized)
        if direction == "output":
            try:
                artifact.resolve().relative_to((base / "evidence").resolve())
            except ValueError as exc:
                raise ReplayEvidenceError("QF-12-IMMUTABLE-ATTEMPT", f"B00/B01 output not attempt-scoped: {normalized}") from exc
            if row.get("media_type") != "application/json":
                raise ReplayEvidenceError("QF-20-B01-PAYLOAD", f"unsupported receipt-bound output type: {normalized}")
        actual = digest_file(artifact)
        if row.get("sha256") != actual:
            raise ReplayEvidenceError("QF-02-FORGED-CHAIN", f"stale artifact hash: {normalized}")
        ids[artifact_id] = normalized
        hashes[normalized] = actual
    return manifest, hashes, ids


V2_LOG_FIELDS = {
    "schema_version", "campaign_id", "book", "run_id", "stage_id", "attempt_id",
    "receipt_path", "receipt_sha256", "outcome", "non_authorizing",
}


def validate_v2_log_entry(entry: dict[str, Any]) -> None:
    if set(entry) != V2_LOG_FIELDS or entry.get("schema_version") != "whole_bible_stage_receipt_log.v2" or entry.get("non_authorizing") is not True:
        raise ReplayEvidenceError("QF-LOG-PARITY", "v2 receipt log entry shape")
    for key in ("campaign_id", "book", "run_id", "stage_id", "attempt_id", "receipt_path", "receipt_sha256", "outcome"):
        if not isinstance(entry.get(key), str) or not entry[key]:
            raise ReplayEvidenceError("QF-LOG-PARITY", f"v2 receipt log field: {key}")


def load_v2_receipt_log(path: Path, *, root: Path = ROOT) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ReplayEvidenceError("QF-LOG-PARITY", f"invalid receipt log JSON: {_display_path(path, root)}:{number}") from exc
        if not isinstance(row, dict):
            raise ReplayEvidenceError("QF-LOG-PARITY", f"non-object receipt log row: {_display_path(path, root)}:{number}")
        validate_v2_log_entry(row)
        rows.append(row)
    return rows


def ensure_v2_receipt_log(path: Path, entry: dict[str, Any], *, root: Path = ROOT) -> None:
    validate_v2_log_entry(entry)
    rows = load_v2_receipt_log(path, root=root)
    identity = tuple(entry[key] for key in ("campaign_id", "book", "run_id", "stage_id", "attempt_id"))
    matches = [row for row in rows if tuple(row[key] for key in ("campaign_id", "book", "run_id", "stage_id", "attempt_id")) == identity]
    if matches:
        if len(matches) != 1 or matches[0] != entry:
            raise ReplayEvidenceError("QF-LOG-PARITY", f"conflicting receipt log identity: {_display_path(path, root)}")
        return
    if any(row["receipt_path"] == entry["receipt_path"] or row["receipt_sha256"] == entry["receipt_sha256"] for row in rows):
        raise ReplayEvidenceError("QF-LOG-PARITY", f"receipt path/hash alias in log: {_display_path(path, root)}")
    append_receipt_log(path, entry)
def _walk(value: Any) -> Iterable[tuple[str | None, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield key, child
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield None, child
            yield from _walk(child)


def _book_rows(book: str, root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    passages_path = root / "data/canonical/scripture/passages/passages.jsonl"
    witnesses_path = root / "data/canonical/translations/eng-web/translation_witnesses.jsonl"
    return _book_rows_cached(book, root, digest_file(passages_path), digest_file(witnesses_path))


@lru_cache(maxsize=128)
def _book_rows_cached(book: str, root: Path, passages_sha256: str, witnesses_sha256: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    passages: list[dict[str, Any]] = []
    witnesses: list[dict[str, Any]] = []
    for path, target, field in (
        (root / "data/canonical/scripture/passages/passages.jsonl", passages, "book"),
        (root / "data/canonical/translations/eng-web/translation_witnesses.jsonl", witnesses, "osis_ref"),
    ):
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                row = json.loads(line)
                if (field == "book" and row.get(field) == book) or (field == "osis_ref" and str(row.get(field, "")).startswith(book + ".")):
                    target.append(row)
    if not passages or len(passages) != len(witnesses):
        raise ReplayEvidenceError("QF-15-B01-BOUNDARY-LEAKAGE", "canonical book coverage unavailable")
    return passages, witnesses


def _scope_interval(scope: str, ordinals: dict[str, int]) -> tuple[int, int] | None:
    match = re.fullmatch(r"([1-3]?[A-Za-z][A-Za-z0-9]*\.\d+\.\d+)-([1-3]?[A-Za-z][A-Za-z0-9]*\.\d+\.\d+)", scope)
    if not match or match.group(1) not in ordinals or match.group(2) not in ordinals:
        return None
    start, end = ordinals[match.group(1)], ordinals[match.group(2)]
    return (start, end) if start <= end else None


def reject_partition_like_ranges(value: Any, *, ordinals: dict[str, int]) -> None:
    if isinstance(value, list) and len(value) >= 2:
        intervals = []
        for row in value:
            if not isinstance(row, dict) or not isinstance(row.get("scope"), str):
                intervals = []
                break
            parsed = _scope_interval(row["scope"], ordinals)
            if parsed is None:
                intervals = []
                break
            intervals.append(parsed)
        if intervals:
            ordered = sorted(intervals)
            if ordered[0][0] == 0 and ordered[-1][1] == len(ordinals) - 1 and all(left[1] + 1 == right[0] for left, right in zip(ordered, ordered[1:])):
                raise ReplayEvidenceError("QF-15-B01-BOUNDARY-LEAKAGE", "B01 range collection is an exact book partition")
    if isinstance(value, dict):
        for child in value.values():
            reject_partition_like_ranges(child, ordinals=ordinals)
    elif isinstance(value, list):
        for child in value:
            reject_partition_like_ranges(child, ordinals=ordinals)


def _display_path(path: Path, root: Path) -> str:
    try:
        return repo_relative(path, root)
    except ReplayEvidenceError:
        return f"<external-isolated-artifact>/{path.name}"
def validate_b01_payload(paths: list[Path], *, book: str, root: Path) -> None:
    _, witnesses = _book_rows(book, root)
    verse_texts = {str(row.get("text", "")).strip() for row in witnesses if str(row.get("text", "")).strip()}
    secret = re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|(?:api[_-]?key|secret|token)\s*[:=]\s*[A-Za-z0-9_\-]{20,}", re.I)
    for path in paths:
        try:
            raw = path.read_text(encoding="utf-8")
            value = json.loads(raw)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ReplayEvidenceError("QF-20-B01-PAYLOAD", f"non-UTF8/non-JSON B01 output: {_display_path(path, root)}") from exc
        if "<osis" in raw or "<reversednun" in raw or "translation-witness:eng-web:" in raw or secret.search(raw):
            raise ReplayEvidenceError("QF-20-B01-PAYLOAD", f"source/prompt/secret payload signature: {_display_path(path, root)}")
        for key, child in _walk(value):
            if key in FORBIDDEN_B01_KEYS or key == "text":
                raise ReplayEvidenceError("QF-20-B01-PAYLOAD", f"forbidden B01 field {key}: {_display_path(path, root)}")
            if isinstance(child, str):
                stripped = child.strip()
                if stripped in verse_texts or any(len(verse) >= 40 and verse in child for verse in verse_texts):
                    raise ReplayEvidenceError("QF-20-B01-PAYLOAD", f"canonical witness payload: {_display_path(path, root)}")


def _jsonl_book_row(path: Path, book: str) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        rows = [json.loads(line) for line in handle if line.strip() and json.loads(line).get("book_id") == book]
    if len(rows) != 1:
        raise ReplayEvidenceError("QF-SOURCE-ANCESTRY", f"need one {book} ledger row: {repo_relative(path)}")
    return rows[0]


def validate_source_view_ancestry(*, manifest_path: Path, archive_path: Path, view_manifest_path: Path,
                                  ledger_path: Path, view_path: Path, book: str) -> None:
    source_manifest = load_yaml(manifest_path)
    view_manifest = load_yaml(view_manifest_path)
    ledger = _jsonl_book_row(ledger_path, book)
    expected_archive = source_manifest.get("archive_path")
    if expected_archive != repo_relative(archive_path) or "sha256:" + str(source_manifest.get("sha256")) != digest_file(archive_path):
        raise ReplayEvidenceError("QF-SOURCE-ANCESTRY", "raw archive manifest mismatch")
    if view_manifest.get("source_archive") != expected_archive or "sha256:" + str(view_manifest.get("source_archive_sha256")) != digest_file(archive_path):
        raise ReplayEvidenceError("QF-SOURCE-ANCESTRY", "view manifest archive mismatch")
    if ledger.get("view_path") != repo_relative(view_path) or "sha256:" + str(ledger.get("sha256")) != digest_file(view_path):
        raise ReplayEvidenceError("QF-SOURCE-ANCESTRY", "view ledger mismatch")
    with zipfile.ZipFile(archive_path) as archive:
        archived = archive.read(ledger["source_archive_path"])
    if archived != view_path.read_bytes():
        raise ReplayEvidenceError("QF-SOURCE-ANCESTRY", "derived view bytes differ from archive entry")


def _oshb_num_features(path: Path) -> tuple[list[str], list[str]]:
    tree = ElementTree.parse(path)
    qere: list[str] = []
    reversed_nun: list[str] = []
    for verse in tree.iter():
        if verse.tag.rsplit("}", 1)[-1] != "verse" or not verse.attrib.get("osisID"):
            continue
        ref = verse.attrib["osisID"]
        if any(node.attrib.get("type") == "x-ketiv" for node in verse.iter()):
            qere.append(ref)
        if any(node.attrib.get("type") == "x-reversednun" for node in verse.iter()):
            reversed_nun.append(ref)
    return qere, reversed_nun


def validate_b01_execution(execution: dict[str, Any], *, book: str, run_id: str,
                           attempt_id: str, input_ids: set[str], output_ids: set[str]) -> None:
    validate_schema(execution, B01_EXECUTION_SCHEMA, "B01 prompt execution")
    if execution["book"] != book or execution["run_id"] != run_id or execution["stage_attempt_id"] != attempt_id:
        raise ReplayEvidenceError("QF-16-B01-ROLE-EXECUTION-GAP", "execution identity mismatch")
    prompt = execution["prompt_template_id"]
    if execution["role_id"] != EXPECTED_ROLES[prompt]:
        raise ReplayEvidenceError("QF-16-B01-ROLE-EXECUTION-GAP", "prompt/role mismatch")
    if not set(execution["input_artifact_ids"]).issubset(input_ids) or not set(execution["output_artifact_ids"]).issubset(output_ids):
        raise ReplayEvidenceError("QF-16-B01-ROLE-EXECUTION-GAP", "execution artifact closure")
    if execution["prompt_pack_sha256"] != digest_file(PROMPTS) or execution["workflow_sha256"] != digest_file(WORKFLOW) or execution["runtime_adapter_sha256"] != digest_file(ADAPTER):
        raise ReplayEvidenceError("QF-16-B01-ROLE-EXECUTION-GAP", "execution contract hash drift")
    start, finish = parse_time(execution["started_at"], "execution started"), parse_time(execution["finished_at"], "execution finished")
    if execution["time_source"] != "runtime_attested" or not start < finish:
        raise ReplayEvidenceError("QF-19-B01-TIMING", "execution chronology unavailable or non-strict")
    if prompt == "second_temple_rabbinic_context_scout" and execution["status"] != "gap_returned":
        raise ReplayEvidenceError("QF-16-B01-ROLE-EXECUTION-GAP", "unqualified ancient-context execution must return a gap")
    if prompt == "canonical_relations_and_premortem_scout":
        if set(execution["assigned_functions"]) != {"canonical_relation_forecast", "premortem"} or execution["dual_role_assignment"] is not True:
            raise ReplayEvidenceError("QF-16-B01-ROLE-EXECUTION-GAP", "canonical/premortem dual-function disclosure")


def validate_b01_artifact_content(*, receipt: dict[str, Any], ids: dict[str, str],
                                  input_ids: set[str], output_ids: set[str], root: Path = ROOT) -> None:
    refs = receipt["stage_evidence"]["artifact_refs"]
    if REQUIRED_B01_OUTPUT_IDS - set(refs) or "b01_prompt_execution" not in refs:
        raise ReplayEvidenceError("QF-16-B01-ROLE-EXECUTION-GAP", "B01 required evidence missing")
    prompt_refs = refs["b01_prompt_execution"]
    role_report_refs = refs["b01_role_report"]
    if not isinstance(prompt_refs, list) or len(prompt_refs) != 4 or not isinstance(role_report_refs, list) or len(role_report_refs) != 4:
        raise ReplayEvidenceError("QF-16-B01-ROLE-EXECUTION-GAP", "exactly four prompt executions and reports required")
    output_paths = [resolve_repo_path(ids[artifact_id], root) for artifact_id in output_ids]
    validate_b01_payload(output_paths, book=receipt["book"], root=root)
    passages, _ = _book_rows(receipt["book"], root)
    ordinals = {row["osis_ref"]: index for index, row in enumerate(passages)}
    execution_rows = [load_json(resolve_repo_path(ids[artifact_id], root)) for artifact_id in prompt_refs]
    for row in execution_rows:
        validate_b01_execution(row, book=receipt["book"], run_id=receipt["run_id"], attempt_id=receipt["attempt_id"], input_ids=input_ids, output_ids=output_ids)
    prompts = [row["prompt_template_id"] for row in execution_rows]
    unique_fields = ("execution_id", "assignment_id", "agent_instance_id")
    if set(prompts) != set(REQUIRED_PROMPTS) or len(prompts) != len(set(prompts)) or any(len({row[field] for row in execution_rows}) != 4 for field in unique_fields):
        raise ReplayEvidenceError("QF-16-B01-ROLE-EXECUTION-GAP", "four distinct role executions required")
    if {artifact_id for row in execution_rows for artifact_id in row["output_artifact_ids"]} != set(role_report_refs) or any(len(row["output_artifact_ids"]) != 1 for row in execution_rows):
        raise ReplayEvidenceError("QF-17-B01-ATTRIBUTION", "each role execution must bind one distinct role report")
    for row in execution_rows:
        report_id = row["output_artifact_ids"][0]
        report_path = resolve_repo_path(ids[report_id], root)
        if row["raw_result_path_or_gap"] != ids[report_id] or row["raw_result_sha256_or_gap"] != digest_file(report_path):
            raise ReplayEvidenceError("QF-17-B01-ATTRIBUTION", "raw role result binding mismatch")
    ledger = load_json(resolve_repo_path(ids[refs["b01_execution_ledger"]], root))
    validate_schema(ledger, B01_LEDGER_SCHEMA, "B01 execution ledger")
    if ledger["book"] != receipt["book"] or ledger["run_id"] != receipt["run_id"] or ledger["stage_attempt_id"] != receipt["attempt_id"]:
        raise ReplayEvidenceError("QF-17-B01-ATTRIBUTION", "ledger identity")
    if set(ledger["required_prompt_template_ids"]) != set(REQUIRED_PROMPTS) or set(ledger["contributor_execution_ids"]) != {row["execution_id"] for row in execution_rows} or set(ledger["prompt_execution_artifact_ids"]) != set(prompt_refs):
        raise ReplayEvidenceError("QF-17-B01-ATTRIBUTION", "ledger execution closure")
    synthesis = load_json(resolve_repo_path(ids[refs["synthesis_lineage"]], root))
    required_synthesis = {"schema_version", "book", "run_id", "stage_attempt_id", "synthesis_execution_id", "agent_instance_id", "contributor_execution_ids", "contributor_artifact_sha256", "started_at", "finished_at", "time_source", "root_synthesizer_read_contributor_outputs", "aggregate_artifact_blindness", "shared_model_substrate", "counts_as_cross_model_independent_vote", "contains_scripture_text", "contains_source_rows", "contains_prompts_or_hidden_reasoning", "non_authorizing"}
    if set(synthesis) != required_synthesis or synthesis["schema_version"] != "whole_bible_b01_synthesis_lineage.v1" or synthesis["book"] != receipt["book"] or synthesis["run_id"] != receipt["run_id"] or synthesis["stage_attempt_id"] != receipt["attempt_id"]:
        raise ReplayEvidenceError("QF-17-B01-ATTRIBUTION", "synthesis lineage shape/identity")
    contributor_ids = {row["execution_id"] for row in execution_rows}
    expected_reports = {ids[artifact_id]: digest_file(resolve_repo_path(ids[artifact_id], root)) for artifact_id in role_report_refs}
    if set(synthesis["contributor_execution_ids"]) != contributor_ids or synthesis["contributor_artifact_sha256"] != expected_reports or synthesis["synthesis_execution_id"] != ledger["synthesis_attempt_id"] or synthesis["agent_instance_id"] in {row["agent_instance_id"] for row in execution_rows}:
        raise ReplayEvidenceError("QF-17-B01-ATTRIBUTION", "synthesis contributor closure/identity")
    synthesis_start = parse_time(synthesis["started_at"], "synthesis started")
    synthesis_finish = parse_time(synthesis["finished_at"], "synthesis finished")
    role_finishes = [parse_time(row["finished_at"], "role finished") for row in execution_rows]
    if synthesis["time_source"] != "runtime_attested" or not max(role_finishes) <= synthesis_start < synthesis_finish:
        raise ReplayEvidenceError("QF-19-B01-TIMING", "synthesis chronology")
    if receipt["started_at"] != min(row["started_at"] for row in execution_rows) or receipt["finished_at"] != synthesis["finished_at"]:
        raise ReplayEvidenceError("QF-19-B01-TIMING", "receipt chronology must be derived from executions")
    values = receipt["stage_evidence"]["values"]
    if receipt["independence_scope"].get("artifact_blindness") is not False or values.get("aggregate_artifact_blindness") is not False or values.get("B02_authorized") is not False:
        raise ReplayEvidenceError("QF-18-B01-BLINDNESS", "root synthesis is not artifact-blind and cannot authorize B02")
    if set(receipt["unresolved_holds"]) != REQUIRED_B01_HOLDS:
        raise ReplayEvidenceError("QF-10-AUTHORITY-SMUGGLING", "B01 holds are incomplete")
    for artifact_id in ("book_strategy", "form_inventory", "hardest_passage_forecast", "source_gap_register", "synthesis_lineage"):
        value = load_json(resolve_repo_path(ids[refs[artifact_id]], root))
        for key, _ in _walk(value):
            if key in FORBIDDEN_B01_KEYS:
                raise ReplayEvidenceError("QF-15-B01-BOUNDARY-LEAKAGE", f"forbidden B01 key: {key}")
        reject_partition_like_ranges(value, ordinals=ordinals)
    form = load_json(resolve_repo_path(ids[refs["form_inventory"]], root))
    coverage = form.get("whole_book_coverage") or {}
    expected_chapters = sorted({row["chapter"] for row in passages})
    expected_coverage = {"first_osis_ref": passages[0]["osis_ref"], "last_osis_ref": passages[-1]["osis_ref"], "passage_records": len(passages), "web_witness_records": len(passages), "chapters_covered": expected_chapters}
    if coverage != expected_coverage:
        raise ReplayEvidenceError("QF-15-B01-BOUNDARY-LEAKAGE", "whole-book coverage metadata mismatch")
    source = load_json(resolve_repo_path(ids[refs["source_gap_register"]], root))
    if source.get("book") != receipt["book"] or source.get("run_id") != receipt["run_id"] or source.get("stage_attempt_id") != receipt["attempt_id"]:
        raise ReplayEvidenceError("QF-SOURCE-ANCESTRY", "source register identity")
    if source.get("contains_final_chunk_map") is not False or source.get("B02_authorized") is not False:
        raise ReplayEvidenceError("QF-15-B01-BOUNDARY-LEAKAGE", "source register authority")
    ancient = source.get("ancient_context") or {}
    if ancient.get("activation_status") != "corpus_gap_unqualified" or ancient.get("contextual_observations") != [] or ancient.get("hold_id") != "NUM-B01-HOLD-ANCIENT-CONTEXT-CORPUS":
        raise ReplayEvidenceError("QF-UNQUALIFIED-CORPUS", "ancient-context gap must be empty and held")
    closure = source.get("source_input_closure")
    if not isinstance(closure, list) or not closure:
        raise ReplayEvidenceError("QF-SOURCE-ANCESTRY", "source input closure missing")
    for row in closure:
        artifact_id = row.get("artifact_id")
        if artifact_id not in input_ids or ids[artifact_id] != row.get("path") or digest_file(resolve_repo_path(row["path"], root)) != row.get("sha256"):
            raise ReplayEvidenceError("QF-SOURCE-ANCESTRY", "unbound source input")
    lineage = source.get("witness_lineage") or []
    relevant = [row for row in lineage if row.get("witness_id") in {"openscriptures_oshb", "tanach_us_uxlc"}]
    if len(relevant) != 2 or len({row.get("lineage_group_id") for row in relevant}) != 1 or any(row.get("counts_as_independent_textual_witness") is not False for row in relevant):
        raise ReplayEvidenceError("QF-WITNESS-LINEAGE", "correlated WLC witnesses inflated")
    if receipt["book"] == "Num":
        expected_crosswalk = [
            (["Num.17.1-Num.17.15"], ["Num.16.36-Num.16.50"]),
            (["Num.17.16-Num.17.28"], ["Num.17.1-Num.17.13"]),
            (["Num.25.19", "Num.26.1"], ["Num.26.1"]),
            (["Num.30.1"], ["Num.29.40"]),
            (["Num.30.2-Num.30.17"], ["Num.30.1-Num.30.16"]),
        ]
        crosswalk = source.get("versification_crosswalk") or {}
        observed = [(row.get("mt_refs"), row.get("web_refs")) for row in crosswalk.get("records") or []]
        if observed != expected_crosswalk or crosswalk.get("claim_level") != "reference_label_alignment_only" or crosswalk.get("token_phrase_alignment_status") != "missing_hold" or crosswalk.get("authorizes_boundary") is not False:
            raise ReplayEvidenceError("QF-XWALK-SCOPE", "Numbers reference crosswalk mismatch/inflation")
        features = source.get("hebrew_metadata_pressures") or {}
        expected_qere = ["Num.1.16", "Num.12.3", "Num.14.36", "Num.16.11", "Num.21.32", "Num.23.13", "Num.26.9", "Num.32.7", "Num.34.4"]
        if features.get("qere_ketiv_refs") != expected_qere or features.get("reversed_nun_source_anchors") != ["Num.10.34", "Num.10.36"]:
            raise ReplayEvidenceError("QF-FEATURE-SET", "Numbers Hebrew metadata declaration mismatch")
        oshb_path = resolve_repo_path(ids["oshb_book_view"], root)
        actual_qere, actual_nun = _oshb_num_features(oshb_path)
        if actual_qere != expected_qere or actual_nun != ["Num.10.34", "Num.10.36"]:
            raise ReplayEvidenceError("QF-FEATURE-SET", "Numbers OSHB feature bytes mismatch")
        ux_path = resolve_repo_path(ids["uxlc_book_view"], root)
        if ux_path.read_text(encoding="utf-8").count("<reversednun/>") != 2:
            raise ReplayEvidenceError("QF-FEATURE-SET", "Numbers UXLC reversed-nun count")
        validate_source_view_ancestry(
            manifest_path=resolve_repo_path(ids["oshb_source_manifest"], root), archive_path=resolve_repo_path(ids["oshb_raw_archive"], root),
            view_manifest_path=resolve_repo_path(ids["oshb_view_manifest"], root), ledger_path=resolve_repo_path(ids["oshb_included_files"], root),
            view_path=oshb_path, book="Num")
        validate_source_view_ancestry(
            manifest_path=resolve_repo_path(ids["uxlc_source_manifest"], root), archive_path=resolve_repo_path(ids["uxlc_raw_archive"], root),
            view_manifest_path=resolve_repo_path(ids["uxlc_view_manifest"], root), ledger_path=resolve_repo_path(ids["uxlc_included_files"], root),
            view_path=ux_path, book="Num")
    scan = load_json(resolve_repo_path(ids[refs["b01_integrity_scan"]], root))
    scanned = scan.get("scanned_artifact_sha256")
    expected_scan = {ids[artifact_id]: digest_file(resolve_repo_path(ids[artifact_id], root)) for artifact_id in output_ids if artifact_id != refs["b01_integrity_scan"]}
    if scan.get("schema_version") != "whole_bible_b01_integrity_scan.v1" or scan.get("status") != "passed" or scan.get("finding_count") != 0 or scanned != expected_scan:
        raise ReplayEvidenceError("QF-20-B01-PAYLOAD", "integrity scan closure mismatch")
    boss = load_json(resolve_repo_path(ids[refs["b01_boss_authorization"]], root))
    packet_paths = sorted(ids[artifact_id] for artifact_id in output_ids if artifact_id not in {refs["b01_boss_authorization"], refs["b01_integrity_scan"]})
    packet_sha = digest_bytes(canonical_bytes({path: digest_file(resolve_repo_path(path, root)) for path in packet_paths}))
    if boss.get("schema_version") != "whole_bible_b01_boss_authorization.v1" or boss.get("book") != receipt["book"] or boss.get("run_id") != receipt["run_id"] or boss.get("stage_attempt_id") != receipt["attempt_id"] or boss.get("evidence_packet_sha256") != packet_sha or boss.get("verdict") != "go_B01_receipt_only" or boss.get("B02_authorized") is not False or boss.get("non_authorizing") is not True:
        raise ReplayEvidenceError("QF-B01-BOSS", "boss authorization absent, stale, or overbroad")


def validate_b00_artifact_content(*, receipt: dict[str, Any], ids: dict[str, str],
                                  campaign_path: Path = CAMPAIGN, registry_path: Path = REGISTRY,
                                  root: Path = ROOT) -> None:
    refs = receipt["stage_evidence"]["artifact_refs"]
    required = {"campaign_projection", "workflow", "prompt_pack", "runtime_adapter", "campaign_registry", "preflight_report", "dependency_evidence"}
    if set(refs) != required:
        raise ReplayEvidenceError("QF-02-FORGED-CHAIN", "B00 v2 artifact closure")
    campaign = load_json(campaign_path)
    job = campaign_job(campaign, receipt["book"])
    projection_path = resolve_repo_path(ids[refs["campaign_projection"]], root)
    projection = load_json(projection_path)
    declared_inputs = job.get("input_digests") or {}
    if set(declared_inputs) != set(job.get("inputs") or []):
        raise ReplayEvidenceError("QF-02-FORGED-CHAIN", "campaign job input digest closure")
    campaign_relative = repo_relative(campaign_path, root)
    expected_inputs: dict[str, str] = {}
    for relative in job.get("inputs") or []:
        actual = digest_file(resolve_repo_path(relative, root))
        expected_inputs[relative] = actual
        expected_declaration = "stage_receipt_v2:B00.campaign_sha256" if relative == campaign_relative else actual
        if declared_inputs.get(relative) != expected_declaration:
            raise ReplayEvidenceError("QF-02-FORGED-CHAIN", f"campaign job input digest stale: {relative}")
    expected = {
        "schema_version": "whole_bible_campaign_projection.v2",
        "campaign_id": campaign["campaign_id"], "campaign_revision": campaign["revision"],
        "campaign_path": repo_relative(campaign_path, root), "campaign_sha256": digest_file(campaign_path),
        "registry_path": repo_relative(registry_path, root), "registry_sha256": digest_file(registry_path),
        "book": receipt["book"], "run_id": receipt["run_id"], "job_id": job["id"],
        "job_projection_sha256": digest_bytes(canonical_bytes(job)), "input_sha256": expected_inputs,
        "sibling_map_exclusion_verified": True,
        "campaign_projection_algorithm": "registry_bound_exact_campaign_and_job_projection",
        "contains_scripture_text": False, "contains_source_rows": False, "non_authorizing": True,
    }
    if projection != expected:
        raise ReplayEvidenceError("QF-02-FORGED-CHAIN", "B00 v2 campaign projection stale")
    report = load_json(resolve_repo_path(ids[refs["preflight_report"]], root))
    if report != {
        "schema_version": "whole_bible_B00_preflight_report.v2", "book": receipt["book"], "run_id": receipt["run_id"],
        "campaign_projection_sha256": digest_file(projection_path), "source_digests_pinned": True,
        "sibling_map_exclusion_verified": True, "supported_stage_ceiling": "B00",
        "B02_authorized": False, "static_specification_valid_only": True,
        "replay_qualified": False, "launch_qualified": False, "non_authorizing": True,
    }:
        raise ReplayEvidenceError("QF-02-FORGED-CHAIN", "B00 v2 report stale/inflated")
    dependency = load_json(resolve_repo_path(ids[refs["dependency_evidence"]], root))
    if dependency.get("schema_version") != "whole_bible_dependency_evidence.v2" or dependency.get("book") != receipt["book"] or dependency.get("run_id") != receipt["run_id"] or dependency.get("non_authorizing") is not True:
        raise ReplayEvidenceError("QF-02-FORGED-CHAIN", "B00 v2 dependency evidence")
    if receipt["book"] == "Num":
        predecessor = MODEL_ROOT / "receipts" / "Lev_completion_v2.json"
        if dependency.get("status") != "precontract_snapshot_waiver" or dependency.get("dependency_receipt_path") != repo_relative(predecessor, root) or dependency.get("dependency_receipt_sha256") != digest_file(predecessor):
            raise ReplayEvidenceError("QF-02-FORGED-CHAIN", "Numbers predecessor waiver mismatch")

def validate_stage_semantics(receipt: dict[str, Any]) -> None:
    if receipt["stage_id"] not in SUPPORTED_STAGES:
        raise ReplayEvidenceError("QF-21-UNMIGRATED-STAGE", "v2 supports only B00/B01")
    if parse_time(receipt["started_at"], "started_at") >= parse_time(receipt["finished_at"], "finished_at"):
        raise ReplayEvidenceError("QF-19-B01-TIMING", "v2 stage times must be strict")
    scope = receipt["independence_scope"]
    if scope.get("shared_model_substrate") is not True or scope.get("counts_as_cross_model_independent_vote") is not False or scope.get("independent_model_or_provider_evidence") is not False or scope.get("convergence_weight") != "one_model_voice":
        raise ReplayEvidenceError("QF-04-FAKE-BLINDNESS", "v2 correlated-model disclosure")
    if receipt["stage_id"] == "B00":
        if receipt.get("attempt_kind") != "original" or receipt.get("role_or_deterministic_gate") != "authoritative_B00_preflight_builder_v2" or receipt.get("executor_kind") != "deterministic" or receipt.get("outcome") != "succeeded" or receipt.get("unresolved_holds") != []:
            raise ReplayEvidenceError("QF-02-FORGED-CHAIN", "B00 executor/outcome/gate semantics")
        if scope.get("authoring_independent_from_sibling_maps") is not True or scope.get("artifact_blindness") is not False or scope.get("role_separation") is not False:
            raise ReplayEvidenceError("QF-04-FAKE-BLINDNESS", "B00 independence semantics")
        values = receipt["stage_evidence"]["values"]
        if values != {"sibling_map_exclusion_verified": True, "source_digests_pinned": True, "campaign_projection_algorithm": "registry_bound_exact_campaign_and_job_projection"}:
            raise ReplayEvidenceError("QF-02-FORGED-CHAIN", "B00 v2 semantic values")
    else:
        values = receipt["stage_evidence"]["values"]
        required = {"ancient_context_activation_status", "aggregate_artifact_blindness", "root_synthesis_attempt_id", "evidence_attempt_scoped", "B02_authorized"}
        if set(values) != required or values["ancient_context_activation_status"] != "corpus_gap_recorded" or values["aggregate_artifact_blindness"] is not False or values["evidence_attempt_scoped"] is not True or values["B02_authorized"] is not False:
            raise ReplayEvidenceError("QF-10-AUTHORITY-SMUGGLING", "B01 v2 semantic values")
