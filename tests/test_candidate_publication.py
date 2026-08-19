from __future__ import annotations

import copy
import gzip
import hashlib
import io
import json
import subprocess
import tarfile

import pytest

from scripts import build_candidate_publication as builder
from scripts import validate_candidate_publication as validator


def _contract() -> dict:
    return builder._load_json(validator.CONTRACT)


def _manifest() -> dict:
    return builder._load_json(validator.MANIFEST)


def _resign(manifest: dict) -> None:
    unsigned = copy.deepcopy(manifest)
    unsigned.pop("manifest_digest", None)
    manifest["manifest_digest"] = f"sha256:{hashlib.sha256(builder._canonical_json(unsigned)).hexdigest()}"


def test_tracked_candidate_publication_is_valid_and_held() -> None:
    result = validator.validate_repository()

    assert result["status"] == "pass"
    assert result["immutable_pointer_count"] == 279
    assert result["embedded_payload_bytes"] == 0
    assert result["replay_qualified"] is False
    assert result["release_qualified"] is False


def test_contract_schema_forbids_payload_or_release_claims() -> None:
    contract = _contract()
    contract["licensing"]["selected_payloads_embedded"] = True

    with pytest.raises(builder.PublicationError, match="PUB-SCHEMA"):
        builder.validate_contract(contract)


def test_candidate_map_book_set_must_equal_pinned_canonical_allowlist() -> None:
    expected = [f"Book{index:02d}" for index in range(66)]
    observed = set(expected)
    observed.remove("Book65")
    observed.add("BookTypo")

    with pytest.raises(builder.PublicationError, match="PUB-MAP-CANONICAL-BOOKS.*Book65.*BookTypo"):
        builder._require_exact_canonical_book_set(observed, expected)


def test_manifest_rejects_m8_or_other_forbidden_path() -> None:
    contract = _contract()
    manifest = _manifest()
    manifest["inventory"][0]["path"] = ".ai/scratch/multi_model_bible_chunking/M8_fable/model_manifest.yaml"
    manifest["inventory"][0]["classification"] = builder._classify(manifest["inventory"][0]["path"])
    manifest["inventory"] = sorted(manifest["inventory"], key=lambda item: item["path"])
    _resign(manifest)

    with pytest.raises(builder.PublicationError, match="PUB-MANIFEST-PATH"):
        builder.validate_manifest_envelope(contract, manifest)


def test_manifest_rejects_embedded_payload() -> None:
    contract = _contract()
    manifest = _manifest()
    manifest["inventory"][0]["payload_embedded"] = True
    _resign(manifest)

    with pytest.raises(builder.PublicationError, match="PUB-MANIFEST-PAYLOAD"):
        builder.validate_manifest_envelope(contract, manifest)


@pytest.mark.parametrize(
    ("mutate", "error_code"),
    [
        (lambda manifest: manifest["status"].__setitem__("release_qualified", True), "PUB-MANIFEST-CONTRACT"),
        (lambda manifest: manifest["coverage"].__setitem__("candidate_map_rows", 1179), "PUB-MANIFEST-COVERAGE"),
        (lambda manifest: manifest.__setitem__("publication_revision", "1.0.1"), "PUB-MANIFEST-CONTRACT"),
    ],
)
def test_manifest_rejects_resigned_contract_or_coverage_drift(mutate, error_code: str) -> None:
    contract = _contract()
    manifest = _manifest()
    mutate(manifest)
    _resign(manifest)

    with pytest.raises(builder.PublicationError, match=error_code):
        builder.validate_manifest_envelope(contract, manifest)


def test_manifest_rejects_resigned_extra_nonselected_path() -> None:
    contract = _contract()
    manifest = _manifest()
    manifest["inventory"].append(
        {
            "path": "docs/not-selected.md",
            "git_blob": "0" * 40,
            "sha256": "sha256:" + "0" * 64,
            "bytes": 0,
            "classification": "governance_or_provenance_pointer",
            "payload_embedded": False,
        }
    )
    manifest["inventory"] = sorted(manifest["inventory"], key=lambda item: item["path"])
    manifest["selection_summary"]["selected_pointer_count"] += 1
    _resign(manifest)

    with pytest.raises(builder.PublicationError, match="PUB-MANIFEST-MEMBERSHIP"):
        builder.validate_manifest_envelope(contract, manifest)


def test_manifest_rejects_resigned_malformed_hash_binding() -> None:
    contract = _contract()
    manifest = _manifest()
    manifest["inventory"][0]["sha256"] = "sha256:not-a-digest"
    _resign(manifest)

    with pytest.raises(builder.PublicationError, match="PUB-MANIFEST-ITEM"):
        builder.validate_manifest_envelope(contract, manifest)


def test_metadata_package_is_deterministic_and_contains_no_selected_payload(tmp_path) -> None:
    contract = _contract()
    manifest = _manifest()
    first_path, first_digest = builder.package_metadata(contract, manifest, tmp_path / "a")
    second_path, second_digest = builder.package_metadata(contract, manifest, tmp_path / "b")

    assert first_digest == second_digest
    assert first_path.read_bytes() == second_path.read_bytes()
    with gzip.GzipFile(fileobj=io.BytesIO(first_path.read_bytes()), mode="rb") as stream:
        with tarfile.open(fileobj=stream, mode="r") as archive:
            names = archive.getnames()
    assert names == [
        "m7-sol-candidate-v1/ARTIFACT_MANIFEST.json",
        "m7-sol-candidate-v1/PUBLICATION_CONTRACT.json",
        "m7-sol-candidate-v1/README.md",
    ]
    assert not any(".ai/scratch" in name for name in names)


def test_progress_and_failure_history_remain_separate() -> None:
    manifest = _manifest()
    coverage = manifest["coverage"]
    limitations = {item["limitation_id"]: item for item in manifest["known_limitations"]}

    assert coverage["book_strategy_records"] == 66
    assert coverage["candidate_map_books"] == 66
    assert coverage["candidate_map_rows"] == 1178
    assert coverage["corrective_review_completed"] == 22
    assert limitations["psalm-template-and-midpoint-history"]["state"] == "historical_repaired"
    assert limitations["psalm-active-holds"]["state"] == "active_hold"
    assert limitations["correlated-reviewer-mesh"]["state"] == "unproven"


def test_immutable_source_replay_when_commit_is_available() -> None:
    contract = _contract()
    available = subprocess.run(
        ["git", "cat-file", "-e", f"{contract['source']['commit_sha']}^{{commit}}"],
        cwd=builder.ROOT,
        check=False,
        capture_output=True,
    ).returncode == 0
    if not available:
        pytest.skip("immutable M7 source commit is not present in this checkout")

    rebuilt = builder.build_manifest(contract)
    assert rebuilt == _manifest()
