#!/usr/bin/env python3
"""Provider-neutral primitives for immutable whole-Bible replay evidence."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shlex
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Iterator

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent.parent
FAMILY = ROOT / "config" / "agents" / "families" / "scripture-first-biblical-chunking"
WORKFLOW = FAMILY / "whole_bible_candidate_workflow.v1.yaml"
PROMPTS = FAMILY / "whole_bible_candidate_prompt_pack.v1.yaml"
ADAPTER = FAMILY / "codex_desktop_campaign_adapter.v1.yaml"
STAGE_SCHEMA = FAMILY / "whole_bible_stage_receipt.schema.v1.json"
EXTENDED_SCHEMA = FAMILY / "whole_bible_extended_evidence_manifest.schema.v1.json"
TERMINAL_SCHEMA = FAMILY / "whole_bible_terminal_completion_receipt.schema.v1.json"
BOSS_PHASE_SCHEMA = FAMILY / "whole_bible_boss_phase_receipt.schema.v1.json"
DEFAULT_CAMPAIGN = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol" / "campaign.json"
DEFAULT_MODEL_ROOT = ROOT / ".ai" / "scratch" / "multi_model_bible_chunking" / "M7_sol"
STAGES = tuple(f"B{index:02d}" for index in range(11))
SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
SUCCESS_OUTCOMES = {"succeeded", "pass_with_holds"}

REQUIRED_STAGE_ARTIFACTS = {
    "B00": {"campaign_projection", "workflow", "prompt_pack", "runtime_adapter", "preflight_report", "dependency_evidence"},
    "B01": {"book_strategy", "form_inventory", "hardest_passage_forecast", "source_gap_register", "ancient_context_gap_or_qualified_receipt"},
    "B02": {"chunks", "initial_decision_relations_or_no_relation"},
    "B03": {"frozen_chunks", "per_chunk_digest_manifest", "freeze_validator_result"},
    "B04": {"original_language_assignment", "literary_assignment", "original_language_primary_review", "literary_primary_review", "frozen_chunks"},
    "B05": {"peer_crosscheck", "premortem", "frozen_chunks"},
    "B06": {"provisional_commit_receipt", "provisional_ruling", "peer_premortem_input_manifest", "final_commit_receipt", "final_ruling"},
    "B07": {"appeal_ledger_or_explicit_empty"},
    "B08": {"lineage", "revision_disposition", "final_chunks", "fresh_primary_reviews_or_no_change_attestation"},
    "B09": {"checker_verdict", "postcheck", "final_chunks", "review_packets", "decision_relations_or_no_relation", "uncertainty_low_confidence", "uncertainty_frontier", "uncertainty_atlas", "hold_disposition"},
    "B10": {"extended_evidence_manifest", "completion_gate_bundle"},
}
REQUIRED_STAGE_VALUES = {
    "B00": {"sibling_map_exclusion_verified", "source_digests_pinned", "campaign_projection_algorithm"},
    "B01": {"ancient_context_activation_status"}, "B02": {"root_author_attempt_id"},
    "B03": {"frozen_revision", "per_chunk_sha256"},
    "B04": {"primary_role_ids", "review_revision", "blindness_attested", "controller_assignment_ids"},
    "B05": {"frozen_revision"},
    "B06": {"provisional_written_at", "peer_premortem_first_read_at", "final_ruling_written_at", "changes_after_peer_or_premortem"},
    "B07": {"appeal_count", "unresolved_appeal_count", "appeal_ids", "unresolved_appeal_ids"},
    "B08": {"revision_action", "invalidated_review_ids"},
    "B09": {"checked_decision_ids", "overall_status", "unresolved_hold_ids", "unresolved_appeal_ids"},
    "B10": {"terminal_completion_receipt_path_intent", "terminal_completion_receipt_written"},
}
CORE_GROUPS = {"chunks", "review_packets", "decision_relations_or_no_relation", "uncertainty_low_confidence", "uncertainty_frontier", "uncertainty_atlas", "checker_verdict", "postcheck"}
EXTENDED_GROUPS = {"freeze_receipts", "primary_reviews", "peer_crosscheck", "premortem", "provisional_boss_ruling", "final_boss_ruling", "appeal_ledger", "lineage", "source_gap_register", "form_inventory", "hardest_passages"}

class ReplayEvidenceError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReplayEvidenceError("QF-JSON", f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ReplayEvidenceError("QF-JSON", f"{path}: expected JSON object")
    return value


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ReplayEvidenceError("QF-YAML", f"cannot read YAML {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ReplayEvidenceError("QF-YAML", f"{path}: expected YAML mapping")
    return value


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def digest_bytes(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def digest_file(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def repo_relative(path: Path, root: Path = ROOT) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as exc:
        raise ReplayEvidenceError("QF-08-SIBLING-CONTAMINATION", f"path escapes repository: {path}") from exc


def resolve_repo_path(value: str, root: Path = ROOT) -> Path:
    if not isinstance(value, str) or not value or Path(value).is_absolute() or ".." in Path(value).parts:
        raise ReplayEvidenceError("QF-08-SIBLING-CONTAMINATION", f"unsafe repository-relative path: {value!r}")
    path = (root / value).resolve()
    repo_relative(path, root)
    return path


def validate_authoritative_runtime_paths(*, campaign_path: Path, model_root: Path, root: Path, allow_test_roots: bool = False) -> None:
    if allow_test_roots:
        return
    expected = (ROOT.resolve(), DEFAULT_CAMPAIGN.resolve(), DEFAULT_MODEL_ROOT.resolve())
    observed = (root.resolve(), campaign_path.resolve(), model_root.resolve())
    if observed != expected:
        raise ReplayEvidenceError("QF-13-ADAPTER-SPLIT", f"non-authoritative runtime roots: {observed}")


def validate_input_path_authority(normalized: str, *, model_prefix: str) -> None:
    trusted_exact = {
        DEFAULT_CAMPAIGN.relative_to(ROOT).as_posix(),
        WORKFLOW.relative_to(ROOT).as_posix(),
        PROMPTS.relative_to(ROOT).as_posix(),
        ADAPTER.relative_to(ROOT).as_posix(),
        "config/canon/canonical_66_books.yaml",
        "data/canonical/translations/eng-web/translation_witnesses.jsonl",
        "data/canonical/scripture/passages/passages.jsonl",
        "config/chunking/form_registry.yaml",
        "build/observation_substrate/current/scan_manifest.json",
    }
    trusted_prefixes = (
        "config/agents/families/scripture-first-biblical-chunking/",
        "data/raw/original_language/hebrew/",
        "data/raw/original_language/greek/",
        ".ai/control/",
        "scripts/",
    )
    if normalized.startswith(model_prefix) or normalized in trusted_exact or normalized.startswith(trusted_prefixes):
        return
    raise ReplayEvidenceError("QF-08-SIBLING-CONTAMINATION", f"untrusted input provenance path: {normalized}")


def expected_completion_gate_argv(*, book: str, run_id: str) -> dict[str, list[str]]:
    workflow = load_yaml(WORKFLOW)
    result: dict[str, list[str]] = {}
    for row in workflow["required_completion_gates"]:
        command = str(row["command_template"])
        command = command.replace("<model>", "M7_sol").replace("<Book>", book).replace("<RunId>", run_id)
        result[row["gate_id"]] = shlex.split(command, posix=True)
    return result


def validate_completion_gate_bundle(path: Path, *, book: str, run_id: str, root: Path = ROOT) -> list[dict[str, Any]]:
    bundle = load_json(path)
    required = {"schema_version", "book", "run_id", "gates", "contains_scripture_text", "contains_source_rows", "non_authorizing"}
    if set(bundle) != required or bundle.get("schema_version") != "whole_bible_completion_gate_bundle.v1" or bundle.get("book") != book or bundle.get("run_id") != run_id:
        raise ReplayEvidenceError("QF-SCHEMA", "completion gate bundle identity/shape")
    if bundle.get("contains_scripture_text") is not False or bundle.get("contains_source_rows") is not False or bundle.get("non_authorizing") is not True:
        raise ReplayEvidenceError("QF-10-AUTHORITY-SMUGGLING", "gate bundle payload/authority")
    expected = expected_completion_gate_argv(book=book, run_id=run_id)
    gates = bundle.get("gates")
    if not isinstance(gates, list) or {row.get("gate_id") for row in gates if isinstance(row, dict)} != set(expected) or len(gates) != len(expected):
        raise ReplayEvidenceError("QF-GATE", f"gate IDs must be exact: {sorted(expected)}")
    for row in gates:
        required_row = {"gate_id", "argv", "exit_code", "status", "evidence_path", "evidence_sha256", "stdout_sha256"}
        gate_id = row.get("gate_id") if isinstance(row, dict) else None
        if set(row) != required_row or row.get("argv") != expected.get(gate_id) or row.get("exit_code") != 0 or row.get("status") != "passed":
            raise ReplayEvidenceError("QF-GATE", f"invalid or masqueraded gate record {gate_id}")
        if any(any(token in arg for token in (";", "&&", "||", "|", "\n", "\r")) for arg in row["argv"]):
            raise ReplayEvidenceError("QF-GATE", f"shell composition {gate_id}")
        evidence = resolve_repo_path(row["evidence_path"], root)
        if not evidence.is_file() or digest_file(evidence) != row["evidence_sha256"] or row["stdout_sha256"] != row["evidence_sha256"]:
            raise ReplayEvidenceError("QF-GATE", f"stale or non-exact stdout evidence {gate_id}")
    return gates

def parse_time(value: str, label: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise ReplayEvidenceError("QF-TIME", f"{label} must be RFC3339") from exc
    if parsed.tzinfo is None:
        raise ReplayEvidenceError("QF-TIME", f"{label} must include timezone")
    return parsed


def validate_schema(instance: dict[str, Any], schema_path: Path, label: str) -> None:
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    errors = sorted(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(instance), key=lambda error: list(error.absolute_path))
    if errors:
        detail = "; ".join(f"/{'/'.join(map(str, error.absolute_path))}: {error.message}" for error in errors[:10])
        raise ReplayEvidenceError("QF-SCHEMA", f"{label}: {detail}")


def atomic_write(path: Path, payload: bytes, *, immutable: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if immutable and path.read_bytes() == payload:
            return
        if immutable:
            raise ReplayEvidenceError("QF-12-IMMUTABLE-ATTEMPT", f"different bytes already exist: {path.as_posix()}")
    temporary = path.with_name(path.name + f".tmp-{os.getpid()}")
    if temporary.exists():
        raise ReplayEvidenceError("QF-LOCK", f"temporary path collision: {repo_relative(temporary)}")
    try:
        with temporary.open("xb") as handle:
            handle.write(payload); handle.flush(); os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists(): temporary.unlink()


@contextmanager
def exclusive_lock(state_root: Path) -> Iterator[None]:
    state_root.mkdir(parents=True, exist_ok=True)
    lock = state_root / "replay-evidence.lock"
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise ReplayEvidenceError("QF-LOCK", f"lock exists: {repo_relative(lock)}") from exc
    try:
        os.write(descriptor, f"pid={os.getpid()}\n".encode("ascii")); os.fsync(descriptor); os.close(descriptor)
        yield
    finally:
        try: os.close(descriptor)
        except OSError: pass
        if lock.exists(): lock.unlink()


def campaign_job(campaign: dict[str, Any], book: str) -> dict[str, Any]:
    try: jobs = campaign["phases"][0]["waves"][0]["subwaves"][0]["jobs"]
    except (KeyError, IndexError, TypeError) as exc: raise ReplayEvidenceError("QF-CAMPAIGN", "job topology malformed") from exc
    matches = [job for job in jobs if isinstance(job, dict) and str(job.get("id", "")).endswith(f"-{book.upper()}")]
    if len(matches) != 1: raise ReplayEvidenceError("QF-CAMPAIGN", f"need one job for {book}")
    return matches[0]


def stage_plan(job: dict[str, Any], stage_id: str) -> dict[str, Any]:
    matches = [row for row in (job.get("stage_plan") or []) if row.get("stage_id") == stage_id]
    if len(matches) != 1: raise ReplayEvidenceError("QF-01-PLAN-NOT-RUN", f"{job.get('id')}: missing {stage_id}")
    return matches[0]

def job_path_authorized(normalized: str, job: dict[str, Any], *, run_id: str) -> bool:
    candidates = list(job.get("inputs") or []) + list(job.get("outputs") or []) + list(job.get("allowed_paths") or [])
    for template in candidates:
        pattern = re.escape(str(template).replace("\\", "/"))
        pattern = pattern.replace(re.escape("<run_id>"), re.escape(run_id))
        pattern = pattern.replace(re.escape("<RunId>"), re.escape(run_id))
        pattern = pattern.replace(re.escape("<attempt_id>"), r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")
        if re.fullmatch(pattern, normalized):
            return True
    return False

def validate_artifact_manifest(path: Path, *, root: Path, model_root: Path, book: str, run_id: str, stage_id: str, direction: str, job: dict[str, Any] | None = None) -> tuple[dict[str, Any], dict[str, str], dict[str, str]]:
    manifest = load_json(path)
    required = {"schema_version", "manifest_id", "book", "run_id", "stage_id", "direction", "artifacts", "contains_scripture_text", "contains_source_rows", "contains_prompts_or_hidden_reasoning", "non_authorizing"}
    if set(manifest) != required or manifest.get("schema_version") != "whole_bible_artifact_manifest.v1":
        raise ReplayEvidenceError("QF-SCHEMA", f"{repo_relative(path, root)}: artifact manifest shape")
    for key, expected in (("book", book), ("run_id", run_id), ("stage_id", stage_id), ("direction", direction)):
        if manifest.get(key) != expected: raise ReplayEvidenceError("QF-02-FORGED-CHAIN", f"{repo_relative(path, root)}: {key} mismatch")
    if any(manifest.get(key) is not False for key in ("contains_scripture_text", "contains_source_rows", "contains_prompts_or_hidden_reasoning")) or manifest.get("non_authorizing") is not True:
        raise ReplayEvidenceError("QF-10-AUTHORITY-SMUGGLING", f"{repo_relative(path, root)}: payload/authority declaration")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts: raise ReplayEvidenceError("QF-SCHEMA", "artifact list empty")
    hashes: dict[str, str] = {}; ids: dict[str, str] = {}
    model_prefix = repo_relative(model_root, root).rstrip("/") + "/"
    for row in artifacts:
        if not isinstance(row, dict) or set(row) != {"artifact_id", "path", "sha256", "media_type", "scope"}:
            raise ReplayEvidenceError("QF-SCHEMA", "malformed artifact record")
        artifact_id, relative = row.get("artifact_id"), row.get("path")
        if not isinstance(artifact_id, str) or not artifact_id or artifact_id in ids: raise ReplayEvidenceError("QF-SCHEMA", "duplicate artifact ID")
        artifact_path = resolve_repo_path(relative, root)
        if not artifact_path.is_file(): raise ReplayEvidenceError("QF-02-FORGED-CHAIN", f"artifact missing: {relative}")
        normalized = repo_relative(artifact_path, root)
        if job is not None and not job_path_authorized(normalized, job, run_id=run_id):
            raise ReplayEvidenceError("QF-08-SIBLING-CONTAMINATION", f"artifact is outside active job/run allowlist: {normalized}")
        if normalized.startswith(".ai/scratch/multi_model_bible_chunking/") and not normalized.startswith(model_prefix):
            raise ReplayEvidenceError("QF-08-SIBLING-CONTAMINATION", normalized)
        if direction == "output" and not normalized.startswith(model_prefix):
            raise ReplayEvidenceError("QF-09-FORBIDDEN-EFFECT", normalized)
        if direction == "input":
            validate_input_path_authority(normalized, model_prefix=model_prefix)
        actual = digest_file(artifact_path)
        if row.get("sha256") != actual: raise ReplayEvidenceError("QF-02-FORGED-CHAIN", f"stale artifact hash: {normalized}")
        if normalized in hashes: raise ReplayEvidenceError("QF-SCHEMA", f"duplicate path: {normalized}")
        hashes[normalized] = actual; ids[artifact_id] = normalized
    return manifest, hashes, ids


def derive_stage_hashes(refs: dict[str, Any], ids: dict[str, str], hashes: dict[str, str]) -> dict[str, Any]:
    derived: dict[str, Any] = {}
    for semantic_id, reference in refs.items():
        values = reference if isinstance(reference, list) else [reference]
        if not values or not all(isinstance(value, str) and value in ids for value in values):
            raise ReplayEvidenceError("QF-02-FORGED-CHAIN", f"{semantic_id}: unknown artifact ref")
        derived[semantic_id] = ({ids[value]: hashes[ids[value]] for value in values} if isinstance(reference, list) else hashes[ids[reference]])
    return derived


def validate_stage_semantics(receipt: dict[str, Any]) -> None:
    stage_id = receipt["stage_id"]; evidence = receipt["stage_evidence"]; values = evidence["values"]
    missing_refs = REQUIRED_STAGE_ARTIFACTS[stage_id] - set(evidence["artifact_refs"])
    missing_values = REQUIRED_STAGE_VALUES[stage_id] - set(values)
    if missing_refs or missing_values: raise ReplayEvidenceError("QF-02-FORGED-CHAIN", f"{stage_id}: missing refs={sorted(missing_refs)} values={sorted(missing_values)}")
    if set(evidence["artifact_sha256"]) != set(evidence["artifact_refs"]): raise ReplayEvidenceError("QF-02-FORGED-CHAIN", f"{stage_id}: evidence projection")
    scope = receipt["independence_scope"]
    if receipt["shared_model_substrate"] != scope["shared_model_substrate"] or receipt["counts_as_cross_model_independent_vote"] != scope["counts_as_cross_model_independent_vote"]:
        raise ReplayEvidenceError("QF-04-FAKE-BLINDNESS", f"{stage_id}: disclosure mismatch")
    if (
        receipt["counts_as_cross_model_independent_vote"] is not False
        or scope["counts_as_cross_model_independent_vote"] is not False
        or scope["independent_model_or_provider_evidence"] is not False
        or scope["runtime_model_identity_attested"] is not False
        or scope["shared_model_substrate"] is not True
        or scope["convergence_weight"] != "one_model_voice"
        or scope.get("independence_evidence_ref") is not None
    ):
        raise ReplayEvidenceError("QF-04-FAKE-BLINDNESS", f"{stage_id}: runtime-local attempts are one correlated voice; external independence belongs in qualification evidence")
    if parse_time(receipt["started_at"], "started_at") > parse_time(receipt["finished_at"], "finished_at"):
        raise ReplayEvidenceError("QF-TIME", f"{stage_id}: reversed times")
    if receipt["outcome"] in {"failed", "blocked_human"} and not receipt.get("failure_fingerprint"):
        raise ReplayEvidenceError("QF-12-SAME-STATE-RETRY", f"{stage_id}: missing failure fingerprint")
    if stage_id == "B00":
        if receipt.get("prior_stage_receipt_sha256") is not None or receipt.get("prior_stage_receipt_path") is not None: raise ReplayEvidenceError("QF-02-FORGED-CHAIN", "B00 has prior")
        if values["sibling_map_exclusion_verified"] is not True or values["source_digests_pinned"] is not True: raise ReplayEvidenceError("QF-08-SIBLING-CONTAMINATION", "B00 pin/exclusion false")
        if values["campaign_projection_algorithm"] != "exact_campaign_bytes_and_canonical_job_projection": raise ReplayEvidenceError("QF-11-HASH-CYCLE", "B00 projection")
    if stage_id == "B04":
        roles, assignments = values["primary_role_ids"], values["controller_assignment_ids"]
        if not isinstance(roles, list) or len(roles) != 2 or len(set(roles)) != 2 or not isinstance(assignments, list) or len(assignments) != 2 or len(set(assignments)) != 2 or values["blindness_attested"] is not True:
            raise ReplayEvidenceError("QF-04-FAKE-BLINDNESS", "B04 roles/assignments/blindness")
    if stage_id == "B06":
        provisional = parse_time(values["provisional_written_at"], "B06 provisional")
        exposure = parse_time(values["peer_premortem_first_read_at"], "B06 exposure")
        final = parse_time(values["final_ruling_written_at"], "B06 final")
        if not provisional < exposure <= final or not isinstance(values["changes_after_peer_or_premortem"], list): raise ReplayEvidenceError("QF-03-BOSS-BACKFILL", "B06 causal order")
    if stage_id == "B07":
        total, unresolved = values["appeal_count"], values["unresolved_appeal_count"]
        appeal_ids, unresolved_ids = values["appeal_ids"], values["unresolved_appeal_ids"]
        if (
            not isinstance(total, int) or not isinstance(unresolved, int) or total < unresolved or unresolved < 0
            or not isinstance(appeal_ids, list) or not isinstance(unresolved_ids, list)
            or len(appeal_ids) != len(set(appeal_ids)) or len(unresolved_ids) != len(set(unresolved_ids))
            or total != len(appeal_ids) or unresolved != len(unresolved_ids) or not set(unresolved_ids).issubset(appeal_ids)
        ): raise ReplayEvidenceError("QF-05-APPEAL-ERASURE", "appeal IDs/counts")
    if stage_id == "B08" and (values["revision_action"] not in {"no_change", "revised"} or not isinstance(values["invalidated_review_ids"], list)):
        raise ReplayEvidenceError("QF-06-LINEAGE-LOSS", "B08 revision/lineage")
    if stage_id == "B09":
        ids = values["checked_decision_ids"]
        holds, appeals = values["unresolved_hold_ids"], values["unresolved_appeal_ids"]
        if (
            not isinstance(ids, list) or len(ids) != len(set(ids))
            or not isinstance(holds, list) or len(holds) != len(set(holds))
            or not isinstance(appeals, list) or len(appeals) != len(set(appeals))
            or values["overall_status"] not in {"pass", "pass_with_holds"}
            or (bool(holds or appeals) != (values["overall_status"] == "pass_with_holds"))
        ): raise ReplayEvidenceError("QF-05-APPEAL-ERASURE", "B09 decision/hold/appeal status")
    if stage_id == "B10" and values["terminal_completion_receipt_written"] is not False: raise ReplayEvidenceError("QF-11-HASH-CYCLE", "B10 must precede terminal completion")


def validate_disposition_file(path: Path, *, kind: str, book: str, run_id: str) -> dict[str, Any]:
    record = load_json(path)
    if kind == "appeal":
        required = {"schema_version", "book", "run_id", "appeal_ids", "unresolved_appeal_ids", "non_authorizing"}
        expected_schema = "whole_bible_appeal_disposition.v1"
        list_fields = ("appeal_ids", "unresolved_appeal_ids")
    elif kind == "hold":
        required = {"schema_version", "book", "run_id", "unresolved_hold_ids", "non_authorizing"}
        expected_schema = "whole_bible_hold_disposition.v1"
        list_fields = ("unresolved_hold_ids",)
    else:
        raise ReplayEvidenceError("QF-SCHEMA", f"unknown disposition kind: {kind}")
    if set(record) != required or record.get("schema_version") != expected_schema or record.get("book") != book or record.get("run_id") != run_id or record.get("non_authorizing") is not True:
        raise ReplayEvidenceError("QF-05-APPEAL-ERASURE", f"{kind} disposition identity/shape")
    for field in list_fields:
        values = record.get(field)
        if not isinstance(values, list) or not all(isinstance(value, str) and value for value in values) or len(values) != len(set(values)):
            raise ReplayEvidenceError("QF-05-APPEAL-ERASURE", f"{kind} disposition {field}")
    if kind == "appeal" and not set(record["unresolved_appeal_ids"]).issubset(record["appeal_ids"]):
        raise ReplayEvidenceError("QF-05-APPEAL-ERASURE", "unresolved appeal not in appeal ledger")
    return record


def validate_stage_artifact_content(receipt: dict[str, Any], ids: dict[str, str], *, root: Path = ROOT) -> None:
    stage_id = receipt["stage_id"]
    refs = receipt["stage_evidence"]["artifact_refs"]
    values = receipt["stage_evidence"]["values"]
    if stage_id == "B00":
        projection_path = resolve_repo_path(ids[refs["campaign_projection"]], root)
        report_path = resolve_repo_path(ids[refs["preflight_report"]], root)
        dependency_path = resolve_repo_path(ids[refs["dependency_evidence"]], root)
        projection = load_json(projection_path); report = load_json(report_path); dependency = load_json(dependency_path)
        campaign = load_json(DEFAULT_CAMPAIGN); job = campaign_job(campaign, receipt["book"])
        required_projection = {"schema_version", "campaign_id", "campaign_revision", "campaign_path", "campaign_sha256", "book", "run_id", "job_id", "job_projection_sha256", "input_sha256", "source_manifest_sha256", "sibling_map_exclusion_verified", "campaign_projection_algorithm", "contains_scripture_text", "contains_source_rows", "non_authorizing"}
        if set(projection) != required_projection or projection.get("schema_version") != "whole_bible_campaign_projection.v1":
            raise ReplayEvidenceError("QF-02-FORGED-CHAIN", "B00 campaign projection shape")
        expected_identity = {"campaign_id": campaign["campaign_id"], "campaign_revision": campaign["revision"], "campaign_path": repo_relative(DEFAULT_CAMPAIGN, root), "campaign_sha256": digest_file(DEFAULT_CAMPAIGN), "book": receipt["book"], "run_id": receipt["run_id"], "job_id": job["id"], "job_projection_sha256": digest_bytes(canonical_bytes(job)), "sibling_map_exclusion_verified": True, "campaign_projection_algorithm": "exact_campaign_bytes_and_canonical_job_projection", "contains_scripture_text": False, "contains_source_rows": False, "non_authorizing": True}
        if any(projection.get(key) != value for key, value in expected_identity.items()):
            raise ReplayEvidenceError("QF-02-FORGED-CHAIN", "B00 campaign projection identity/hash")
        model_prefix = repo_relative(DEFAULT_MODEL_ROOT, root).rstrip("/") + "/"
        for relative in job.get("inputs") or []:
            validate_input_path_authority(relative, model_prefix=model_prefix)
        expected_inputs = {relative: digest_file(resolve_repo_path(relative, root)) for relative in job.get("inputs") or []}
        if projection.get("input_sha256") != expected_inputs:
            raise ReplayEvidenceError("QF-02-FORGED-CHAIN", "B00 pinned input projection stale")
        source_paths = (job.get("source_route") or {}).get("manifest_paths") or []
        if projection.get("source_manifest_sha256") != {relative: expected_inputs[relative] for relative in source_paths}:
            raise ReplayEvidenceError("QF-02-FORGED-CHAIN", "B00 source manifest projection stale")
        required_report = {"schema_version", "book", "run_id", "campaign_projection_sha256", "source_digests_pinned", "sibling_map_exclusion_verified", "dependency_status", "static_specification_valid_only", "replay_qualified", "launch_qualified", "non_authorizing"}
        if set(report) != required_report or report.get("campaign_projection_sha256") != digest_file(projection_path) or report.get("source_digests_pinned") is not True or report.get("sibling_map_exclusion_verified") is not True or report.get("static_specification_valid_only") is not True or report.get("replay_qualified") is not False or report.get("launch_qualified") is not False or report.get("non_authorizing") is not True:
            raise ReplayEvidenceError("QF-02-FORGED-CHAIN", "B00 preflight report stale or inflated")
        required_dependency = {"schema_version", "book", "run_id", "status", "dependency_job_id", "dependency_receipt_path", "dependency_receipt_sha256", "precontract_waiver_reason", "non_authorizing"}
        if set(dependency) != required_dependency or dependency.get("schema_version") != "whole_bible_dependency_evidence.v1" or dependency.get("book") != receipt["book"] or dependency.get("run_id") != receipt["run_id"] or dependency.get("non_authorizing") is not True or report.get("dependency_status") != dependency.get("status"):
            raise ReplayEvidenceError("QF-02-FORGED-CHAIN", "B00 dependency evidence shape")
        declared_dependencies = job.get("depends_on") or []
        if not declared_dependencies and dependency.get("status") != "no_dependency":
            raise ReplayEvidenceError("QF-02-FORGED-CHAIN", "B00 unexpected dependency")
        if declared_dependencies:
            if dependency.get("dependency_job_id") != declared_dependencies[0]:
                raise ReplayEvidenceError("QF-02-FORGED-CHAIN", "B00 dependency job mismatch")
            bound = resolve_repo_path(dependency.get("dependency_receipt_path"), root)
            if not bound.is_file() or digest_file(bound) != dependency.get("dependency_receipt_sha256"):
                raise ReplayEvidenceError("QF-02-FORGED-CHAIN", "B00 dependency receipt stale")
            declared = (job.get("dependency_digests") or {}).get(declared_dependencies[0])
            if dependency.get("status") == "precontract_snapshot_waiver":
                expected_declared = f"precontract_snapshot_waiver:Lev_completion_v2:{dependency['dependency_receipt_sha256']}"
                if receipt["book"] != "Num" or declared != expected_declared:
                    raise ReplayEvidenceError("QF-02-FORGED-CHAIN", "B00 invalid precontract waiver")
            elif dependency.get("status") != "terminal_predecessor" or declared != dependency.get("dependency_receipt_sha256"):
                raise ReplayEvidenceError("QF-02-FORGED-CHAIN", "B00 unresolved predecessor")
    if stage_id == "B07":
        path = resolve_repo_path(ids[refs["appeal_ledger_or_explicit_empty"]], root)
        record = validate_disposition_file(path, kind="appeal", book=receipt["book"], run_id=receipt["run_id"])
        if record["appeal_ids"] != values["appeal_ids"] or record["unresolved_appeal_ids"] != values["unresolved_appeal_ids"]:
            raise ReplayEvidenceError("QF-05-APPEAL-ERASURE", "B07 appeal disposition projection")
    if stage_id == "B09":
        path = resolve_repo_path(ids[refs["hold_disposition"]], root)
        record = validate_disposition_file(path, kind="hold", book=receipt["book"], run_id=receipt["run_id"])
        if record["unresolved_hold_ids"] != values["unresolved_hold_ids"]:
            raise ReplayEvidenceError("QF-05-APPEAL-ERASURE", "B09 hold disposition projection")


def derive_terminal_dispositions(b07_receipt: dict[str, Any], b09_receipt: dict[str, Any]) -> tuple[list[str], list[str], str]:
    b07 = b07_receipt["stage_evidence"]["values"]
    b09 = b09_receipt["stage_evidence"]["values"]
    appeals = list(b07["unresolved_appeal_ids"])
    if appeals != b09["unresolved_appeal_ids"]:
        raise ReplayEvidenceError("QF-05-APPEAL-ERASURE", "B07/B09 unresolved appeal mismatch")
    holds = list(b09["unresolved_hold_ids"])
    outcome = "candidate_complete_with_holds" if holds or appeals else "candidate_complete"
    return holds, appeals, outcome

def run_dir(model_root: Path, book: str, run_id: str) -> Path:
    return model_root / "state" / "books" / book / "runs" / run_id


def read_index(directory: Path, campaign: dict[str, Any], book: str, run_id: str) -> dict[str, Any]:
    path = directory / "run_index.json"
    if not path.exists(): return {"schema_version": "whole_bible_run_index.v1", "campaign_id": campaign["campaign_id"], "campaign_revision": campaign["revision"], "book": book, "run_id": run_id, "selected": {}, "non_authorizing": True}
    index = load_json(path); required = {"schema_version", "campaign_id", "campaign_revision", "book", "run_id", "selected", "non_authorizing"}
    if set(index) != required or index["schema_version"] != "whole_bible_run_index.v1": raise ReplayEvidenceError("QF-SCHEMA", "run index shape")
    expected = {"campaign_id": campaign["campaign_id"], "campaign_revision": campaign["revision"], "book": book, "run_id": run_id, "non_authorizing": True}
    if any(index.get(key) != value for key, value in expected.items()) or not isinstance(index["selected"], dict): raise ReplayEvidenceError("QF-02-FORGED-CHAIN", "run index identity")
    return index


def append_receipt_log(path: Path, entry: dict[str, Any]) -> None:
    rows: list[dict[str, Any]] = []
    if path.exists():
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip(): continue
            try: row = json.loads(line)
            except json.JSONDecodeError as exc: raise ReplayEvidenceError("QF-JSON", f"{repo_relative(path)}:{number}") from exc
            if not isinstance(row, dict): raise ReplayEvidenceError("QF-JSON", f"{repo_relative(path)}:{number}")
            rows.append(row)
    key = (entry["receipt_path"], entry["receipt_sha256"])
    if any((row.get("receipt_path"), row.get("receipt_sha256")) == key for row in rows): return
    rows.append(entry); atomic_write(path, b"".join(canonical_bytes(row) for row in rows))
def validate_boss_phase_pair(receipt: dict[str, Any], ids: dict[str, str], hashes: dict[str, str], root: Path = ROOT) -> None:
    if receipt.get("stage_id") != "B06": return
    refs = receipt["stage_evidence"]["artifact_refs"]; values = receipt["stage_evidence"]["values"]
    provisional_path = resolve_repo_path(ids[refs["provisional_commit_receipt"]], root); final_path = resolve_repo_path(ids[refs["final_commit_receipt"]], root)
    provisional = load_json(provisional_path); final = load_json(final_path)
    validate_schema(provisional, BOSS_PHASE_SCHEMA, "B06a"); validate_schema(final, BOSS_PHASE_SCHEMA, "B06b")
    if provisional["phase"] != "provisional_B06a" or final["phase"] != "final_B06b" or provisional["book"] != receipt["book"] or final["book"] != receipt["book"] or provisional["run_id"] != receipt["run_id"] or final["run_id"] != receipt["run_id"]:
        raise ReplayEvidenceError("QF-03-BOSS-BACKFILL", "boss phase identities")
    if final["prior_boss_phase_receipt_path"] != repo_relative(provisional_path, root) or final["prior_boss_phase_receipt_sha256"] != digest_file(provisional_path):
        raise ReplayEvidenceError("QF-03-BOSS-BACKFILL", "B06b does not bind B06a")
    provisional_time = parse_time(provisional["committed_at"], "B06a committed_at"); final_time = parse_time(final["committed_at"], "B06b committed_at"); exposure_time = parse_time(values["peer_premortem_first_read_at"], "B06 exposure")
    if not provisional_time < exposure_time <= final_time or values["provisional_written_at"] != provisional["committed_at"] or values["final_ruling_written_at"] != final["committed_at"]:
        raise ReplayEvidenceError("QF-03-BOSS-BACKFILL", "boss commit/exposure chronology")
    if provisional["peer_premortem_exposure_artifact_sha256"] or not final["peer_premortem_exposure_artifact_sha256"]:
        raise ReplayEvidenceError("QF-03-BOSS-BACKFILL", "boss exposure scopes")
    provisional_ruling = ids[refs["provisional_ruling"]]; final_ruling = ids[refs["final_ruling"]]
    if provisional["output_ruling_path"] != provisional_ruling or provisional["output_ruling_sha256"] != hashes[provisional_ruling] or final["output_ruling_path"] != final_ruling or final["output_ruling_sha256"] != hashes[final_ruling]:
        raise ReplayEvidenceError("QF-03-BOSS-BACKFILL", "boss ruling hashes")