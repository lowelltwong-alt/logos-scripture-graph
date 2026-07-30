#!/usr/bin/env python3
"""Build deterministic, payload-free catalogs for the Scripture-first family.

This builder never reads Scripture text.  It hashes governed repository
references, summarizes the existing no-text passage coverage inventory, and
prepares a metadata-only DAD adaptation candidate.  It cannot activate the
family or change chunk output.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

import yaml


ROOT = Path(__file__).resolve().parent.parent
FAMILY_DIR = ROOT / "config" / "agents" / "families" / "scripture-first-biblical-chunking"
GENERATED_DIR = FAMILY_DIR / "generated"
KNOWLEDGE_MANIFEST = FAMILY_DIR / "knowledge_manifest.v1.yaml"
PILOT_SUITE = FAMILY_DIR / "pilot_suite.v1.yaml"
CANON_ALLOWLIST = ROOT / "config" / "canon" / "canonical_66_books.yaml"
COVERAGE_INVENTORY = ROOT / ".ai" / "control" / "bible_verse_passage_coverage_inventory.jsonl"

KNOWLEDGE_CATALOG = GENERATED_DIR / "knowledge_catalog.v1.json"
REVERSE_DEPENDENCIES = GENERATED_DIR / "reverse_dependencies.v1.json"
PILOT_REPORT = GENERATED_DIR / "controlled_pilot_routing_report.v1.json"
SHADOW_REPORT = GENERATED_DIR / "whole_bible_shadow_report.v1.json"
DAD_ADAPTATION = GENERATED_DIR / "dad_portable_adaptation.candidate.v1.json"

CONSTITUENT_NAMES = (
    "family.v1.yaml",
    "role_profiles.v1.yaml",
    "knowledge_manifest.v1.yaml",
    "routing_policy.v1.yaml",
    "pilot_suite.v1.yaml",
    "release.v1.yaml",
    "whole_bible_candidate_workflow.v1.yaml",
    "whole_bible_candidate_prompt_pack.v1.yaml",
    "codex_desktop_campaign_adapter.v1.yaml",
    "whole_bible_stage_receipt.schema.v1.json",
    "whole_bible_boss_phase_receipt.schema.v1.json",
    "whole_bible_extended_evidence_manifest.schema.v1.json",
    "whole_bible_terminal_completion_receipt.schema.v1.json",
)


class BuildError(RuntimeError):
    """Raised when a deterministic catalog cannot be built safely."""


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise BuildError(f"cannot load {path.relative_to(ROOT).as_posix()}: {exc}") from exc
    if not isinstance(data, dict):
        raise BuildError(f"{path.relative_to(ROOT).as_posix()} must contain a mapping")
    return data


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _stable_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _digest_record(record: dict[str, Any], digest_key: str) -> str:
    unsigned = {key: value for key, value in record.items() if key != digest_key}
    return _sha256_bytes(_stable_text(unsigned).encode("utf-8"))


def _repo_path(relative: str) -> Path:
    path = (ROOT / relative).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise BuildError(f"reference escapes the Logos checkout: {relative}") from exc
    return path


def build_knowledge_catalog() -> tuple[dict[str, Any], dict[str, Any]]:
    manifest = _load_yaml(KNOWLEDGE_MANIFEST)
    entries = manifest.get("entries")
    if not isinstance(entries, list) or not entries:
        raise BuildError("knowledge_manifest.v1.yaml must contain non-empty entries")

    catalog_entries: list[dict[str, Any]] = []
    role_to_knowledge: dict[str, list[str]] = defaultdict(list)
    library_to_knowledge: dict[str, list[str]] = defaultdict(list)
    source_to_knowledge: dict[str, list[str]] = defaultdict(list)

    for raw in entries:
        if not isinstance(raw, dict):
            raise BuildError("knowledge entries must be mappings")
        knowledge_id = raw.get("knowledge_id")
        source_path = raw.get("source_path")
        if not isinstance(knowledge_id, str) or not knowledge_id:
            raise BuildError("knowledge entry missing knowledge_id")
        if not isinstance(source_path, str) or not source_path:
            raise BuildError(f"{knowledge_id}: missing source_path")
        absolute = _repo_path(source_path)
        if not absolute.is_file():
            raise BuildError(f"{knowledge_id}: source does not resolve: {source_path}")
        actual_hash = _sha256_file(absolute)
        declared_hash = raw.get("source_sha256")
        if isinstance(declared_hash, str) and declared_hash.startswith("sha256:"):
            declared_hash = declared_hash.removeprefix("sha256:")
        if declared_hash != actual_hash:
            raise BuildError(
                f"{knowledge_id}: stale source hash for {source_path}; "
                f"declared {declared_hash}, actual {actual_hash}"
            )
        applicable_roles = raw.get("applicable_roles", [])
        if not isinstance(applicable_roles, list) or not applicable_roles:
            raise BuildError(f"{knowledge_id}: applicable_roles must be non-empty")
        catalog_entry = {
            "knowledge_id": knowledge_id,
            "library": raw.get("library"),
            "source_path": source_path,
            "source_sha256": actual_hash,
            "authority": raw.get("authority"),
            "trust_zone": raw.get("trust_zone"),
            "applicable_roles": sorted(applicable_roles),
            "evidence_class": raw.get("evidence_class"),
            "non_authorizations": sorted(raw.get("non_authorizations", [])),
            "freshness_triggers": sorted(raw.get("freshness_triggers", [])),
        }
        catalog_entries.append(catalog_entry)
        source_to_knowledge[source_path].append(knowledge_id)
        library_to_knowledge[str(raw.get("library"))].append(knowledge_id)
        for role_id in applicable_roles:
            role_to_knowledge[str(role_id)].append(knowledge_id)

    catalog_entries.sort(key=lambda item: item["knowledge_id"])
    catalog: dict[str, Any] = {
        "schema_version": "biblical_chunking_generated_knowledge_catalog.v1",
        "family_id": "scripture-first-biblical-chunking",
        "manifest_path": KNOWLEDGE_MANIFEST.relative_to(ROOT).as_posix(),
        "manifest_sha256": _sha256_file(KNOWLEDGE_MANIFEST),
        "entry_count": len(catalog_entries),
        "contains_scripture_or_source_payloads": False,
        "entries": catalog_entries,
    }
    catalog["catalog_digest"] = _digest_record(catalog, "catalog_digest")

    reverse: dict[str, Any] = {
        "schema_version": "biblical_chunking_reverse_dependencies.v1",
        "family_id": "scripture-first-biblical-chunking",
        "catalog_digest": catalog["catalog_digest"],
        "role_to_knowledge": {
            key: sorted(values) for key, values in sorted(role_to_knowledge.items())
        },
        "library_to_knowledge": {
            key: sorted(values) for key, values in sorted(library_to_knowledge.items())
        },
        "source_to_knowledge": {
            key: sorted(values) for key, values in sorted(source_to_knowledge.items())
        },
    }
    reverse["reverse_dependency_digest"] = _digest_record(
        reverse, "reverse_dependency_digest"
    )
    return catalog, reverse


def _pilot_cases(suite: dict[str, Any]) -> Iterable[tuple[str, dict[str, Any]]]:
    for lane in ("reviewed_invariants", "ambiguity_holds", "breadth_cases"):
        cases = suite.get(lane)
        if not isinstance(cases, list):
            raise BuildError(f"pilot suite missing list: {lane}")
        for case in cases:
            if not isinstance(case, dict):
                raise BuildError(f"pilot suite {lane} case must be a mapping")
            yield lane, case


def build_pilot_report() -> dict[str, Any]:
    suite = _load_yaml(PILOT_SUITE)
    cases: list[dict[str, Any]] = []
    for lane, case in _pilot_cases(suite):
        case_id = case.get("case_id")
        if not isinstance(case_id, str) or not case_id:
            raise BuildError(f"pilot suite {lane} case missing case_id")
        expected_pack = case.get("expected_primary_pack")
        outcome = case.get("expected_outcome")
        if lane == "ambiguity_holds":
            route_state = "hold_for_owner_required"
        elif lane == "breadth_cases":
            route_state = "primary_pack_contract_ready"
        else:
            route_state = "identity_comparison_ready"
        cases.append(
            {
                "case_id": case_id,
                "passage": case.get("passage"),
                "lane": lane,
                "route_state": route_state,
                "expected_primary_pack": expected_pack,
                "expected_outcome": outcome,
                "evidence_ref": case.get("evidence_ref"),
                "boundary_proposal_emitted": False,
                "chunk_output_changed": False,
            }
        )
    cases.sort(key=lambda item: item["case_id"])
    counts = Counter(item["lane"] for item in cases)
    report: dict[str, Any] = {
        "schema_version": "scripture_first_controlled_pilot_routing_report.v1",
        "family_id": "scripture-first-biblical-chunking",
        "suite_path": PILOT_SUITE.relative_to(ROOT).as_posix(),
        "suite_sha256": _sha256_file(PILOT_SUITE),
        "execution_scope": "deterministic_routing_contract_preflight_only",
        "status": "hold_before_exegetical_candidate_run",
        "case_count": len(cases),
        "lane_counts": dict(sorted(counts.items())),
        "cases": cases,
        "independent_review_status": "accepted_candidate_foundation_only",
        "holds": [
            "t475_source_marker_integrity_unresolved",
            "run_level_parent_assignment_resolution_required_before_pilots",
        ],
        "reviewed_behavior_compared": False,
        "boundary_proposals_emitted": 0,
        "automatic_candidates_activated": 0,
        "chunk_outputs_changed": 0,
    }
    report["report_digest"] = _digest_record(report, "report_digest")
    return report


def build_shadow_report() -> dict[str, Any]:
    allowlist = _load_yaml(CANON_ALLOWLIST).get("canonical_66_books")
    if not isinstance(allowlist, list) or len(allowlist) != 66:
        raise BuildError("canonical allowlist must contain exactly 66 books")
    allowed_books = set(str(book) for book in allowlist)
    lane_counts: Counter[str] = Counter()
    status_counts: Counter[str] = Counter()
    flag_counts: Counter[str] = Counter()
    surface_counts: Counter[str] = Counter()
    observed_books: set[str] = set()
    excluded_rows = 0
    passage_count = 0

    try:
        lines = COVERAGE_INVENTORY.open(encoding="utf-8")
    except OSError as exc:
        raise BuildError(f"cannot open coverage inventory: {exc}") from exc
    with lines:
        for line_number, line in enumerate(lines, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise BuildError(f"coverage inventory line {line_number}: {exc}") from exc
            passage_count += 1
            book = str(row.get("book"))
            observed_books.add(book)
            if book not in allowed_books:
                excluded_rows += 1
            lane_counts[str(row.get("lane_id"))] += 1
            status_counts[str(row.get("coverage_status"))] += 1
            flag_counts.update(str(item) for item in row.get("flags", []))
            surface_counts.update(str(item) for item in row.get("source_surface_ids", []))

    missing_books = sorted(allowed_books - observed_books)
    unexpected_books = sorted(observed_books - allowed_books)
    if passage_count != 31_103 or len(observed_books) != 66 or excluded_rows:
        raise BuildError(
            "whole-Bible shadow source is not the expected canonical-66 inventory: "
            f"passages={passage_count}, books={len(observed_books)}, excluded={excluded_rows}"
        )
    report: dict[str, Any] = {
        "schema_version": "scripture_first_whole_bible_shadow_report.v1",
        "family_id": "scripture-first-biblical-chunking",
        "mode": "candidate_only_no_text_routing_shadow",
        "status": "hold_missing_marker_evidenced_form_observations",
        "source_inventory_path": COVERAGE_INVENTORY.relative_to(ROOT).as_posix(),
        "source_inventory_sha256": _sha256_file(COVERAGE_INVENTORY),
        "accounted_passage_count": passage_count,
        "canonical_book_count": len(observed_books),
        "missing_canonical_books": missing_books,
        "unexpected_or_noncanonical_books": unexpected_books,
        "noncanonical_default_scope_rows": excluded_rows,
        "lane_counts": dict(sorted(lane_counts.items())),
        "coverage_status_counts": dict(sorted(status_counts.items())),
        "risk_flag_counts": dict(sorted(flag_counts.items())),
        "source_surface_counts": dict(sorted(surface_counts.items())),
        "specialist_activation_counts": {},
        "specialist_activation_state": "not_activated_without_marker_evidenced_form",
        "writer_checker_disagreements": None,
        "writer_checker_disagreement_state": "not_measured_before_candidate_packet_run",
        "boundary_proposals_emitted": 0,
        "candidate_activations": 0,
        "chunk_outputs_changed": 0,
        "cross_form_rule_leakage_detected": False,
        "cross_form_rule_leakage_measurement_state": "router_contract_only",
        "regression_risk": "unmeasured_until_reviewed_identity_pilots_run",
        "holds": [
            "marker_evidenced_form_observations_not_present_in_coverage_inventory",
            "t475_source_marker_integrity_unresolved",
            "run_level_parent_assignment_resolution_required_before_pilots",
        ],
        "independent_review_status": "accepted_candidate_foundation_only",
        "gate_results": {
            "every_in_scope_passage_accounted_for": True,
            "no_noncanonical_record_in_default_scope": True,
            "no_candidate_activated_automatically": True,
            "no_chunk_output_changed": True,
            "candidate_boundary_trial_complete": False,
            "whole_bible_shadow_gate_passed": False,
        },
    }
    report["report_digest"] = _digest_record(report, "report_digest")
    return report


def build_dad_adaptation(
    catalog: dict[str, Any],
    reverse: dict[str, Any],
    pilot: dict[str, Any],
    shadow: dict[str, Any],
) -> dict[str, Any]:
    family = _load_yaml(FAMILY_DIR / "family.v1.yaml")
    family_version = family.get("family_version")
    if not isinstance(family_version, str) or not family_version:
        raise BuildError("family.v1.yaml must declare a non-empty family_version")
    constituent_hashes = []
    for name in CONSTITUENT_NAMES:
        path = FAMILY_DIR / name
        if not path.is_file():
            raise BuildError(f"missing family constituent: {name}")
        constituent_hashes.append({"path": path.relative_to(ROOT).as_posix(), "sha256": _sha256_file(path)})
    generated_hashes = [
        {"artifact": "knowledge_catalog", "digest": catalog["catalog_digest"]},
        {"artifact": "reverse_dependencies", "digest": reverse["reverse_dependency_digest"]},
        {"artifact": "controlled_pilot_routing_report", "digest": pilot["report_digest"]},
        {"artifact": "whole_bible_shadow_report", "digest": shadow["report_digest"]},
    ]
    adaptation: dict[str, Any] = {
        "schema_version": "dad.scripture_first_biblical_chunking_adaptation_candidate.v1",
        "family_id": "scripture-first-biblical-chunking",
        "family_version": family_version,
        "source_authority": "Logos",
        "portable_catalog_owner": "DAD",
        "status": "ineligible_hold",
        "eligible_for_dad_publication": False,
        "constituent_hashes": constituent_hashes,
        "generated_artifact_hashes": generated_hashes,
        "capabilities": [
            "scripture_first_observation",
            "marker_evidenced_form_routing",
            "candidate_boundary_alternatives",
            "anti_imputation_independent_review",
            "canonical_66_scope_guard",
            "resumable_whole_bible_candidate_campaign",
            "role_separated_review_with_independence_disclosure",
            "append_only_disagreement_and_appeal_docket",
            "validator_bound_book_completion_receipts",
            "provider_neutral_subagent_prompt_pack",
        ],
        "contains_scripture_text": False,
        "contains_source_rows": False,
        "contains_private_conversations": False,
        "contains_secrets": False,
        "contains_logos_authority": False,
        "dad_may_override_logos_governance": False,
        "dad_may_write_or_push_into_logos": False,
        "blockers": [
            "dad_candidate_family_framework_not_reviewed_and_merged",
            "dad_portfolio_registry_documentation_drift_unreconciled",
            "controlled_exegetical_pilots_not_run",
            "whole_bible_candidate_boundary_shadow_not_complete",
            "owner_activation_not_authorized",
        ],
    }
    adaptation["adaptation_digest"] = _digest_record(adaptation, "adaptation_digest")
    return adaptation


def build_outputs() -> dict[Path, dict[str, Any]]:
    catalog, reverse = build_knowledge_catalog()
    pilot = build_pilot_report()
    shadow = build_shadow_report()
    dad = build_dad_adaptation(catalog, reverse, pilot, shadow)
    return {
        KNOWLEDGE_CATALOG: catalog,
        REVERSE_DEPENDENCIES: reverse,
        PILOT_REPORT: pilot,
        SHADOW_REPORT: shadow,
        DAD_ADAPTATION: dad,
    }


def _write_or_check(outputs: dict[Path, dict[str, Any]], *, check: bool) -> None:
    failures: list[str] = []
    for path, value in outputs.items():
        expected = _stable_text(value)
        if check:
            try:
                actual = path.read_text(encoding="utf-8")
            except OSError:
                failures.append(f"missing generated artifact: {path.relative_to(ROOT).as_posix()}")
                continue
            if actual != expected:
                failures.append(f"stale generated artifact: {path.relative_to(ROOT).as_posix()}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected, encoding="utf-8", newline="\n")
    if failures:
        raise BuildError("; ".join(failures))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="write deterministic generated artifacts")
    mode.add_argument("--check", action="store_true", help="fail when generated artifacts are missing or stale")
    args = parser.parse_args()
    try:
        outputs = build_outputs()
        _write_or_check(outputs, check=args.check)
    except BuildError as exc:
        print(f"Scripture-first family catalog build failed: {exc}")
        return 1
    action = "validated" if args.check else "wrote"
    print(f"Scripture-first family catalog {action} {len(outputs)} payload-free artifacts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
