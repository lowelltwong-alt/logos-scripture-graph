from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from scripts import validate_epistle_argument_theological_issue_dossier_queue as validator


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / ".ai" / "control" / "epistle_argument_theological_issue_dossier_queue.yaml"


def load_queue() -> dict:
    return yaml.safe_load(QUEUE.read_text(encoding="utf-8"))


def write_candidate(tmp_path: Path, data: dict) -> Path:
    candidate = tmp_path / "epistle_argument_theological_issue_dossier_queue.yaml"
    candidate.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return candidate


def test_epistle_argument_issue_queue_validates_current_repo() -> None:
    data = validator.validate_epistle_argument_theological_issue_dossier_queue()

    assert data["object_type"] == "epistle_argument_theological_issue_dossier_queue"
    assert data["scope"]["lane"] == "epistle_argument"
    assert data["authority"]["authorizes_doctrinal_system"] is False
    assert data["authority"]["authorizes_chunk_boundaries"] is False
    assert data["authority"]["authorizes_output_change"] is False


def test_queue_preserves_epistle_theological_options_without_selecting_systems() -> None:
    data = load_queue()
    policy = data["interpretive_preservation_policy"]

    assert validator.REQUIRED_PRESERVED_OPTIONS <= set(policy["preserved_orthodox_options"])
    assert "Calvinist or Arminian soteriology" in policy["not_selected_by_queue"]
    assert "covenant theology or dispensational theology" in policy["not_selected_by_queue"]
    assert "sacramental presence or memorial-only conclusions" in policy["not_selected_by_queue"]
    assert "Nicene/Chalcedonian" in policy["orthodox_boundary"]


def test_queue_records_existing_t352_packets_as_pending_dependencies() -> None:
    data = validator.validate_epistle_argument_theological_issue_dossier_queue()
    packet_state = data["existing_packet_state"]
    dossiers = {dossier["dossier_id"]: dossier for dossier in data["dossier_queue"]}

    assert packet_state["t352_packet_count"] == 4
    assert packet_state["packet_status_required"] == "pending_human_review"
    assert packet_state["reviewed_gold_promoted"] is False
    assert dossiers["EPH1_BLESSING_ELECTION_SEALING"]["existing_review_packet_dependency"] == "packet_eph1_3_14_argument_review"
    assert dossiers["ROM9_11_ISRAEL_ELECTION_MERCY"]["existing_review_packet_dependency"] == "packet_rom9_11_argument_review"
    assert dossiers["HEB7_10_PRIESTHOOD_COVENANT_SACRIFICE"]["existing_review_packet_dependency"] == "packet_heb7_10_priesthood_argument_review"
    assert dossiers["1COR8_10_CONSCIENCE_IDOL_FOOD_TABLE"]["existing_review_packet_dependency"] == "packet_1cor8_10_food_offered_to_idols_review"


def test_queue_records_future_epistle_research_cases() -> None:
    data = load_queue()
    dossiers = {dossier["dossier_id"]: dossier for dossier in data["dossier_queue"]}

    assert validator.REQUIRED_DOSSIERS <= set(dossiers)
    assert "Gal.3-Gal.4" in dossiers["GAL3_4_LAW_PROMISE_SEED_SONS"]["exact_passage_scope"]
    assert "Rom.7-Rom.8" in dossiers["ROM7_8_FLESH_SPIRIT_ASSURANCE"]["exact_passage_scope"]
    assert "Jas.2" in dossiers["JAMES2_FAITH_WORKS_JUSTIFICATION"]["exact_passage_scope"]
    assert "1Pet.3.18-1Pet.3.22" in dossiers["1PET3_SPIRITS_BAPTISM_SALVATION"]["exact_passage_scope"]
    assert "Jude.5-Jude.15" in dossiers["JUDE_NONCANONICAL_REFERENCES_JUDGMENT"]["exact_passage_scope"]


def test_queue_rejects_authorizing_doctrinal_system(tmp_path: Path) -> None:
    data = load_queue()
    data["authority"]["authorizes_doctrinal_system"] = True
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.EpistleIssueQueueError, match="authorizes_doctrinal_system must be false"):
        validator.validate_epistle_argument_theological_issue_dossier_queue(candidate)


def test_queue_rejects_missing_soteriology_option(tmp_path: Path) -> None:
    data = load_queue()
    data["interpretive_preservation_policy"]["preserved_orthodox_options"].remove(
        "arminian_or_wesleyan_election_readings"
    )
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.EpistleIssueQueueError, match="preserved_orthodox_options"):
        validator.validate_epistle_argument_theological_issue_dossier_queue(candidate)


def test_queue_rejects_existing_packet_without_reviewed_gold_non_authorization(tmp_path: Path) -> None:
    data = load_queue()
    data["dossier_queue"][0]["non_authorizations"].remove("reviewed_gold")
    candidate = write_candidate(tmp_path, data)

    with pytest.raises(validator.EpistleIssueQueueError, match="reviewed_gold"):
        validator.validate_epistle_argument_theological_issue_dossier_queue(candidate)
