from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts import build_divine_capitalization_inventory as builder
from scripts import validate_divine_capitalization_inventory as validator

pytestmark = pytest.mark.generated_data(
    "data/canonical/translations/eng-web/word_tokens.jsonl"
)


@pytest.fixture(scope="module")
def built_inventory() -> dict:
    return builder.build_inventory()


def test_divine_capitalization_inventory_passes_current_repo() -> None:
    data = validator.validate_divine_capitalization_inventory()
    assert data["authority"]["authorizes_graph_edges"] is False
    assert data["authority"]["authorizes_chunk_boundaries"] is False


def test_inventory_builder_is_deterministic(built_inventory: dict) -> None:
    first = built_inventory
    second = builder.build_inventory()
    assert first == second


def test_inventory_records_required_token_variants(built_inventory: dict) -> None:
    data = built_inventory
    terms = {item["term_id"]: item for item in data["token_watch_terms"]}

    god_forms = {item["surface_form"] for item in terms["god"]["observed_variants"]}
    spirit_forms = {item["surface_form"] for item in terms["spirit"]["observed_variants"]}
    word_forms = {item["surface_form"] for item in terms["word"]["observed_variants"]}
    pronoun_forms = {item["surface_form"] for item in terms["his"]["observed_variants"]}

    assert {"God", "god", "GOD"} <= god_forms
    assert {"Spirit", "spirit"} <= spirit_forms
    assert {"Word", "word"} <= word_forms
    assert {"His", "his"} <= pronoun_forms


def test_inventory_records_required_phrase_variants(built_inventory: dict) -> None:
    data = built_inventory
    phrases = {item["phrase_id"]: item for item in data["phrase_watch_terms"]}

    holy_spirit = {item["surface_phrase"] for item in phrases["holy_spirit"]["observed_variants"]}
    son_of_man = {item["surface_phrase"] for item in phrases["son_of_man"]["observed_variants"]}
    alpha_omega = {item["surface_phrase"] for item in phrases["alpha_and_the_omega"]["observed_variants"]}

    assert "Holy Spirit" in holy_spirit
    assert {"Son of Man", "Son of man", "son of man"} <= son_of_man
    assert "Alpha and the Omega" in alpha_omega


def test_inventory_rejects_authorizing_policy(tmp_path: Path, built_inventory: dict) -> None:
    data = copy.deepcopy(built_inventory)
    data["authority"]["authorizes_graph_edges"] = True
    candidate = tmp_path / "inventory.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    with pytest.raises(validator.DivineCapitalizationInventoryError, match="authorizes_graph_edges"):
        validator.validate_divine_capitalization_inventory(candidate)


def test_inventory_rejects_stale_counts(tmp_path: Path, built_inventory: dict) -> None:
    data = copy.deepcopy(built_inventory)
    data["token_watch_terms"][0]["total_occurrences"] += 1
    candidate = tmp_path / "inventory.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    with pytest.raises(validator.DivineCapitalizationInventoryError, match="is stale"):
        validator.validate_divine_capitalization_inventory(candidate)
