#!/usr/bin/env python3
"""Validate the divine-name/title capitalization inventory."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_divine_capitalization_inventory import OUTPUT, build_inventory

REGISTER = ROOT / ".ai" / "control" / "chunking_theological_decision_register.yaml"
PREFLIGHT = ROOT / ".ai" / "control" / "chunking_agent_preflight.yaml"

REQUIRED_FALSE_AUTHORITY = {
    "authorizes_divine_identity",
    "authorizes_trinitarian_relation",
    "authorizes_christology",
    "authorizes_pneumatology",
    "authorizes_speaker_attribution",
    "authorizes_lexical_truth",
    "authorizes_graph_edges",
    "authorizes_chunk_boundaries",
    "authorizes_retrieval_truth",
    "authorizes_output_change",
}

REQUIRED_NON_AUTHORIZATIONS = {
    "capitalization_driven_divine_identity",
    "capitalization_driven_trinitarian_relation",
    "capitalization_driven_christology",
    "capitalization_driven_pneumatology",
    "capitalization_driven_speaker_attribution",
    "capitalization_driven_graph_edge",
    "capitalization_driven_chunk_boundary",
    "capitalization_driven_retrieval_truth",
    "capitalization_driven_output_change",
    "strong_number_driven_lexical_truth",
    "pronoun_capitalization_as_referent_identity",
}

REQUIRED_TOKEN_VARIANTS = {
    "god": {"God", "god", "GOD"},
    "lord": {"Lord", "lord", "LORD"},
    "spirit": {"Spirit", "spirit"},
    "father": {"Father", "father"},
    "son": {"Son", "son"},
    "word": {"Word", "word"},
    "christ": {"Christ"},
    "messiah": {"Messiah"},
    "he": {"He", "he"},
    "his": {"His", "his"},
}

REQUIRED_PHRASE_VARIANTS = {
    "holy_spirit": {"Holy Spirit"},
    "son_of_god": {"Son of God"},
    "son_of_man": {"Son of Man", "Son of man", "son of man"},
    "word_of_god": {"Word of God", "word of God"},
    "lord_god": {"Lord God"},
    "lamb_of_god": {"Lamb of God"},
    "alpha_and_the_omega": {"Alpha and the Omega"},
    "first_and_the_last": {"First and the Last", "first and the last"},
    "beginning_and_the_end": {"Beginning and the End"},
}


class DivineCapitalizationInventoryError(ValueError):
    """Raised when the capitalization inventory is missing, stale, or authorizing."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
        if text.startswith("---\n"):
            parts = text.split("---\n", 2)
            if len(parts) == 3:
                text = parts[1] + "\n" + parts[2]
        data = yaml.safe_load(text)
    except (OSError, yaml.YAMLError) as exc:
        raise DivineCapitalizationInventoryError(f"{_rel(path)}: YAML unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise DivineCapitalizationInventoryError(f"{_rel(path)}: expected a YAML mapping")
    return data


def _variant_forms(entry: dict[str, Any], key: str) -> set[str]:
    variants = entry.get("observed_variants")
    if not isinstance(variants, list):
        raise DivineCapitalizationInventoryError(f"{entry.get('term_id') or entry.get('phrase_id')}: variants must be a list")
    return {str(item.get(key)) for item in variants if isinstance(item, dict)}


def _validate_non_authorizing(data: dict[str, Any], path: Path) -> None:
    if data.get("object_type") != "divine_capitalization_inventory":
        raise DivineCapitalizationInventoryError(f"{_rel(path)}: object_type must be divine_capitalization_inventory")
    if data.get("trust_zone") != "canonical":
        raise DivineCapitalizationInventoryError(f"{_rel(path)}: trust_zone must be canonical")
    if data.get("lifecycle_status") != "active":
        raise DivineCapitalizationInventoryError(f"{_rel(path)}: lifecycle_status must be active")
    authority = data.get("authority")
    if not isinstance(authority, dict):
        raise DivineCapitalizationInventoryError(f"{_rel(path)}: authority must be a mapping")
    if authority.get("records_source_observations") is not True:
        raise DivineCapitalizationInventoryError(f"{_rel(path)}: authority.records_source_observations must be true")
    if authority.get("may_surface_for_review") is not True:
        raise DivineCapitalizationInventoryError(f"{_rel(path)}: authority.may_surface_for_review must be true")
    for key in REQUIRED_FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise DivineCapitalizationInventoryError(f"{_rel(path)}: authority.{key} must be false")
    missing_non_auth = sorted(REQUIRED_NON_AUTHORIZATIONS - set(data.get("non_authorizations", [])))
    if missing_non_auth:
        raise DivineCapitalizationInventoryError(f"{_rel(path)}: missing non_authorizations {missing_non_auth}")


def _validate_required_observations(data: dict[str, Any], path: Path) -> None:
    token_terms = {
        str(item.get("term_id")): item
        for item in data.get("token_watch_terms", [])
        if isinstance(item, dict)
    }
    phrase_terms = {
        str(item.get("phrase_id")): item
        for item in data.get("phrase_watch_terms", [])
        if isinstance(item, dict)
    }
    for term_id, required_forms in REQUIRED_TOKEN_VARIANTS.items():
        entry = token_terms.get(term_id)
        if not isinstance(entry, dict):
            raise DivineCapitalizationInventoryError(f"{_rel(path)}: missing token watch term {term_id}")
        observed = _variant_forms(entry, "surface_form")
        missing = sorted(required_forms - observed)
        if missing:
            raise DivineCapitalizationInventoryError(f"{_rel(path)}: token term {term_id} missing forms {missing}")
        if int(entry.get("total_occurrences", 0)) <= 0:
            raise DivineCapitalizationInventoryError(f"{_rel(path)}: token term {term_id} must have observations")
    for phrase_id, required_forms in REQUIRED_PHRASE_VARIANTS.items():
        entry = phrase_terms.get(phrase_id)
        if not isinstance(entry, dict):
            raise DivineCapitalizationInventoryError(f"{_rel(path)}: missing phrase watch term {phrase_id}")
        observed = _variant_forms(entry, "surface_phrase")
        missing = sorted(required_forms - observed)
        if missing:
            raise DivineCapitalizationInventoryError(f"{_rel(path)}: phrase term {phrase_id} missing forms {missing}")
        if int(entry.get("total_occurrences", 0)) <= 0:
            raise DivineCapitalizationInventoryError(f"{_rel(path)}: phrase term {phrase_id} must have observations")


def _validate_inventory_is_current(data: dict[str, Any], path: Path) -> None:
    expected = build_inventory()
    if data != expected:
        raise DivineCapitalizationInventoryError(
            f"{_rel(path)} is stale; run python scripts/build_divine_capitalization_inventory.py --write"
        )


def _validate_governed_links() -> None:
    register = _read_yaml(REGISTER)
    decisions = register.get("decisions")
    if not isinstance(decisions, list):
        raise DivineCapitalizationInventoryError(f"{_rel(REGISTER)}: decisions must be a list")
    cd018 = next((item for item in decisions if isinstance(item, dict) and item.get("decision_id") == "CD-018"), None)
    if not isinstance(cd018, dict):
        raise DivineCapitalizationInventoryError(f"{_rel(REGISTER)}: missing CD-018")
    for validator in (
        "scripts/validate_divine_capitalization_inventory.py",
        "tests/test_divine_capitalization_inventory.py",
    ):
        if validator not in cd018.get("validators", []):
            raise DivineCapitalizationInventoryError(f"{_rel(REGISTER)}: CD-018 validators missing {validator}")
    preflight = _read_yaml(PREFLIGHT)
    reading_paths = {
        str(item.get("path"))
        for item in preflight.get("mandatory_reading", [])
        if isinstance(item, dict)
    }
    if ".ai/control/divine_capitalization_inventory.yaml" not in reading_paths:
        raise DivineCapitalizationInventoryError(f"{_rel(PREFLIGHT)}: inventory must be mandatory reading")


def validate_divine_capitalization_inventory(path: Path = OUTPUT) -> dict[str, Any]:
    data = _read_yaml(path)
    _validate_non_authorizing(data, path)
    _validate_required_observations(data, path)
    _validate_inventory_is_current(data, path)
    _validate_governed_links()
    return data


def main() -> int:
    try:
        validate_divine_capitalization_inventory()
    except DivineCapitalizationInventoryError as exc:
        print(f"Divine capitalization inventory validation failed: {exc}", file=sys.stderr)
        return 1
    print("Divine capitalization inventory validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
