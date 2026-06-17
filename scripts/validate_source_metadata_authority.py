#!/usr/bin/env python3
"""Validate that source metadata remains evidence, not authority."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Iterable

import yaml

ROOT = Path(__file__).resolve().parent.parent
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"
REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
HARNESS_ROADMAP = ROOT / ".ai" / "control" / "harness_upgrade_roadmap.yaml"
FRONT_DOOR = ROOT / "AI_FRONT_DOOR.md"
T343_TASK = ROOT / ".ai" / "tasks" / "T343.task.yaml"
T344_TASK = ROOT / ".ai" / "tasks" / "T344.task.yaml"
VALIDATOR_PATH = "scripts/validate_source_metadata_authority.py"

SCAN_ROOTS = (
    ROOT / "AI_FRONT_DOOR.md",
    ROOT / ".ai" / "control",
    ROOT / ".ai" / "tasks",
    ROOT / "docs" / "methodology",
    ROOT / "docs" / "roadmap",
    ROOT / "eval" / "chunking_gold",
    ROOT / "pipelines",
    ROOT / "registry",
)

TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".jsonl", ".py"}

REQUIRED_METADATA_TYPES = {
    "internal_cross_references",
    "strongs_style_word_numbers",
    "hebrew_greek_lexeme_tags",
    "footnotes",
    "alternate_readings",
    "section_headings",
    "paragraph_markers",
    "poetry_markers",
    "words_of_jesus_markers",
    "speaker_labels",
    "edition_formatting",
}

REQUIRED_FALSE_POLICY_KEYS = {
    "authorizes_scripture_truth",
    "authorizes_lexical_truth",
    "authorizes_intertext_truth",
    "authorizes_speaker_attribution",
    "authorizes_graph_edges",
    "authorizes_chunk_boundaries",
    "authorizes_output_change",
}

TASK_FALSE_FLAGS = {
    "source_metadata_authority_allowed",
    "internal_cross_reference_authority_allowed",
    "strongs_number_authority_allowed",
    "greek_lexical_rarity_authority_allowed",
}

FORBIDDEN_PATTERNS = (
    (re.compile(r"\bsource[_ -]?metadata[_ -]?authority[_ -]?allowed\s*:\s*true\b", re.I), "source metadata authority allowed"),
    (re.compile(r"\binternal[_ -]?cross[_ -]?reference[_ -]?authority[_ -]?allowed\s*:\s*true\b", re.I), "internal cross-reference authority allowed"),
    (re.compile(r"\bstrongs?[_ -]?number[_ -]?authority[_ -]?allowed\s*:\s*true\b", re.I), "Strong's-style number authority allowed"),
    (re.compile(r"\bgreek[_ -]?lexical[_ -]?rarity[_ -]?authority[_ -]?allowed\s*:\s*true\b", re.I), "Greek lexical rarity authority allowed"),
    (re.compile(r"\bauthorizes_(scripture_truth|lexical_truth|intertext_truth|speaker_attribution|graph_edges|chunk_boundaries|output_change)\s*:\s*true\b", re.I), "metadata authority policy set true"),
    (re.compile(r"\bmetadata[_ -]?driven[_ -]?boundary\s*:\s*true\b", re.I), "metadata-driven boundary enabled"),
    (re.compile(r"\bautomatic[_ -]?cross[_ -]?reference[_ -]?edge\s*:\s*true\b", re.I), "automatic cross-reference edge enabled"),
    (re.compile(r"\bautomatic[_ -]?strongs?[_ -]?lexical[_ -]?authority\s*:\s*true\b", re.I), "automatic Strong's lexical authority enabled"),
)


class SourceMetadataAuthorityError(ValueError):
    """Raised when source metadata is allowed to become authority."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise SourceMetadataAuthorityError(f"{_rel(path)}: not UTF-8 text: {exc}") from exc
    except OSError as exc:
        raise SourceMetadataAuthorityError(f"{_rel(path)}: unreadable: {exc}") from exc


def _read_yaml(path: Path) -> dict[str, Any]:
    text = _read_text(path)
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            text = parts[1] + "\n" + parts[2]
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise SourceMetadataAuthorityError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise SourceMetadataAuthorityError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _iter_scan_paths(roots: Iterable[Path] = SCAN_ROOTS) -> Iterable[Path]:
    for root in roots:
        if root.is_file():
            if root.suffix.lower() in TEXT_SUFFIXES:
                yield root
            continue
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
                yield path


def scan_forbidden_authority(paths: Iterable[Path]) -> None:
    for path in paths:
        text = _read_text(path)
        for pattern, label in FORBIDDEN_PATTERNS:
            match = pattern.search(text)
            if match:
                line = _line_number(text, match.start())
                raise SourceMetadataAuthorityError(f"{_rel(path)}:{line}: forbidden {label}")


def validate_preflight_policy(path: Path = PREFLIGHT) -> None:
    data = _read_yaml(path)
    metadata_types = data.get("non_authorizing_metadata_types")
    if not isinstance(metadata_types, list):
        raise SourceMetadataAuthorityError(f"{_rel(path)}: non_authorizing_metadata_types must be a list")
    missing_types = sorted(REQUIRED_METADATA_TYPES - {str(item) for item in metadata_types})
    if missing_types:
        raise SourceMetadataAuthorityError(f"{_rel(path)}: missing metadata types {missing_types}")

    policy = data.get("metadata_authority_policy")
    if not isinstance(policy, dict):
        raise SourceMetadataAuthorityError(f"{_rel(path)}: metadata_authority_policy must be a mapping")
    if policy.get("may_preserve_as_evidence") is not True:
        raise SourceMetadataAuthorityError(f"{_rel(path)}: metadata must remain preservable as evidence")
    if policy.get("may_surface_for_review") is not True:
        raise SourceMetadataAuthorityError(f"{_rel(path)}: metadata must remain surfaceable for review")
    for key in REQUIRED_FALSE_POLICY_KEYS:
        if policy.get(key) is not False:
            raise SourceMetadataAuthorityError(f"{_rel(path)}: metadata_authority_policy.{key} must be false")

    future_requirements = data.get("future_output_changing_use_requires")
    if not isinstance(future_requirements, list):
        raise SourceMetadataAuthorityError(f"{_rel(path)}: future_output_changing_use_requires must be a list")
    for requirement in ("owner_review", "reviewed_gold_or_equivalent_governed_evidence", "non_target_identity_proof"):
        if requirement not in future_requirements:
            raise SourceMetadataAuthorityError(f"{_rel(path)}: missing future requirement {requirement}")


def validate_task_flags(paths: Iterable[Path] = (T343_TASK, T344_TASK)) -> None:
    for path in paths:
        data = _read_yaml(path)
        auth = data.get("authorization")
        if not isinstance(auth, dict):
            raise SourceMetadataAuthorityError(f"{_rel(path)}: authorization must be a mapping")
        for flag in TASK_FALSE_FLAGS:
            if auth.get(flag) is not False:
                raise SourceMetadataAuthorityError(f"{_rel(path)}: authorization.{flag} must be false")


def validate_decision_register(path: Path = REGISTER) -> None:
    data = _read_yaml(path)
    decisions = data.get("decisions")
    if not isinstance(decisions, list):
        raise SourceMetadataAuthorityError(f"{_rel(path)}: decisions must be a list")
    cd015 = next((item for item in decisions if isinstance(item, dict) and item.get("decision_id") == "CD-015"), None)
    if not isinstance(cd015, dict):
        raise SourceMetadataAuthorityError(f"{_rel(path)}: missing CD-015 source metadata decision")
    decision_text = str(cd015.get("decision", ""))
    for phrase in (
        "do not automatically authorize Scripture truth",
        "lexical truth",
        "intertext claims",
        "speaker attribution",
        "graph edges",
        "chunk boundaries",
        "output changes",
    ):
        if phrase not in decision_text:
            raise SourceMetadataAuthorityError(f"{_rel(path)}: CD-015 decision missing phrase {phrase!r}")
    for non_authorization in (
        "automatic_cross_reference_edge",
        "automatic_strongs_lexical_authority",
        "metadata_driven_output_change",
    ):
        if non_authorization not in cd015.get("non_authorizations", []):
            raise SourceMetadataAuthorityError(f"{_rel(path)}: CD-015 missing {non_authorization}")
    if VALIDATOR_PATH not in cd015.get("validators", []):
        raise SourceMetadataAuthorityError(f"{_rel(path)}: CD-015 validators must include {VALIDATOR_PATH}")


def validate_harn_006(path: Path = HARNESS_ROADMAP) -> None:
    data = _read_yaml(path)
    candidates = data.get("candidate_harnesses")
    if not isinstance(candidates, list):
        raise SourceMetadataAuthorityError(f"{_rel(path)}: candidate_harnesses must be a list")
    harn = next((item for item in candidates if isinstance(item, dict) and item.get("harness_id") == "HARN-006"), None)
    if not isinstance(harn, dict):
        raise SourceMetadataAuthorityError(f"{_rel(path)}: missing HARN-006")
    if harn.get("status") != "implemented_v1":
        raise SourceMetadataAuthorityError(f"{_rel(path)}: HARN-006.status must be implemented_v1")
    implemented = harn.get("implemented_surfaces")
    if not isinstance(implemented, list) or VALIDATOR_PATH not in implemented:
        raise SourceMetadataAuthorityError(f"{_rel(path)}: HARN-006 implemented_surfaces must include {VALIDATOR_PATH}")
    for non_authorization in (
        "metadata_driven_boundary",
        "automatic_cross_reference_edge",
        "automatic_strongs_lexical_authority",
    ):
        if non_authorization not in harn.get("non_authorizations", []):
            raise SourceMetadataAuthorityError(f"{_rel(path)}: HARN-006 missing {non_authorization}")


def validate_front_door(path: Path = FRONT_DOOR) -> None:
    text = _read_text(path)
    for phrase in (
        "Source metadata is evidence, not authority",
        VALIDATOR_PATH,
        "internal cross-references",
        "Strong's-style word numbers",
    ):
        if phrase not in text:
            raise SourceMetadataAuthorityError(f"{_rel(path)}: missing source-metadata phrase {phrase!r}")


def validate_source_metadata_authority() -> None:
    validate_preflight_policy()
    validate_task_flags()
    validate_decision_register()
    validate_harn_006()
    validate_front_door()
    scan_forbidden_authority(_iter_scan_paths())


def main() -> int:
    try:
        validate_source_metadata_authority()
    except SourceMetadataAuthorityError as exc:
        print(f"Source metadata authority validation failed: {exc}", file=sys.stderr)
        return 1
    print("Source metadata authority validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
