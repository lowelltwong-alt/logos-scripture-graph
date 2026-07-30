"""Compact direct semantic coverage for the additive T550 V3.2 policy."""

from __future__ import annotations

from copy import deepcopy
import importlib.util
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
CHECKS = ROOT / ".ai/scratch/multi_model_bible_chunking/M7_sol/checks"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


P = _load("t550_policy_v32_tests", CHECKS / "rematerialization_live_gate_policy_v3_2.py")
T = _load("t550_policy_v31_fixture_for_v32", ROOT / "tests/test_rematerialization_live_gate_policy_v3_1.py")

LEASE_ID = "lease_V32_0123456789abcdefghijklmnop"


def _retime(raw_doc: dict) -> None:
    checker = raw_doc["checker"]
    wall = checker["start_wall_utc"]
    mono = checker["start_monotonic_ns"]
    evidence = raw_doc["evidence"]
    for row in [
        *evidence["targets"],
        *evidence["sentinels"],
        *evidence["bounded_process_snapshot"]["rows"],
    ]:
        row["observation_wall_utc"] = wall
        row["observation_monotonic_ns"] = mono
    checker["checked_evidence_sha256"] = P.V31.digest_value(evidence)


def _topology(raw_doc: dict) -> dict:
    evidence = raw_doc["evidence"]
    env = evidence["environment"]
    parents = {row["parent_id"]: row for row in evidence["canonical_parents"]}
    chains = [
        {
            "parent_id": "model-root",
            "path_token": ".",
            "identities_from_model": [],
        },
        {
            "parent_id": "hos-book-chunks-parent",
            "path_token": "book_chunks/Hos",
            "identities_from_model": [
                T.identity(701, directory=True),
                deepcopy(parents["hos-book-chunks-parent"]["identity"]),
            ],
        },
        {
            "parent_id": "hos-receipts-parent",
            "path_token": "receipts",
            "identities_from_model": [
                deepcopy(parents["hos-receipts-parent"]["identity"])
            ],
        },
        {
            "parent_id": "hos-reviews-parent",
            "path_token": "reviews/Hos",
            "identities_from_model": [
                T.identity(702, directory=True),
                deepcopy(parents["hos-reviews-parent"]["identity"]),
            ],
        },
    ]
    keys = [
        env["volume_root_identity"],
        env["workspace_identity"],
        env["model_identity"],
    ]
    for chain in chains:
        keys.extend(chain["identities_from_model"])
    keys.extend(
        row["identity"]
        for row in [*evidence["targets"], *evidence["sentinels"]]
    )
    projection = [
        {"volume_serial": row["volume_serial"], "file_id": row["file_id"]}
        for row in keys
    ]
    return {
        "volume_serial": env["volume_serial"],
        "root_chain_from_volume": [
            deepcopy(env["volume_root_identity"]),
            deepcopy(env["workspace_identity"]),
            deepcopy(env["model_identity"]),
        ],
        "parent_chains": chains,
        "all_identity_keys_sha256": P.digest_value(projection),
    }


def _enumeration(raw_doc: dict) -> dict:
    opened = raw_doc["evidence"]["bounded_process_snapshot"]["rows"]
    rows = [
        {
            "ordinal": index,
            "pid": row["pid"],
            "parent_pid": row["parent_pid"],
            "creation_token": row["creation_token"],
            "normalized_name": row["normalized_name"],
        }
        for index, row in enumerate(opened, 1)
    ]
    return {
        "api_identity": P.ENUMERATION_API,
        "terminal_status": P.ENUMERATION_TERMINAL_STATUS,
        "raw_count": len(rows),
        "rows": rows,
        "rows_sha256": P.digest_value(rows),
        "derived_candidate_sha256": P.digest_value(rows),
        "opened_evidence_sha256": P.digest_value(opened),
    }


def _attestations(raw_doc: dict, sidecar: dict) -> list[dict]:
    evidence = raw_doc["evidence"]
    wall = raw_doc["checker"]["start_wall_utc"]
    mono = raw_doc["checker"]["start_monotonic_ns"]
    subjects: list[tuple[str, str, object]] = [
        ("environment", "environment", evidence["environment"]),
        ("effect", "effects", evidence["effects"]),
        ("system_snapshot", "enumeration", sidecar["enumeration"]),
        ("topology", "rooted_topology", sidecar["rooted_topology"]),
    ]
    subjects.extend(
        ("parent", row["parent_id"], row) for row in evidence["canonical_parents"]
    )
    subjects.extend(("target", row["target_id"], row) for row in evidence["targets"])
    subjects.extend(
        ("sentinel", row["sentinel_id"], row) for row in evidence["sentinels"]
    )
    subjects.extend(
        ("process", str(row["pid"]), row)
        for row in evidence["bounded_process_snapshot"]["rows"]
    )
    return [
        {
            "observation_class": kind,
            "subject_id": subject_id,
            "subject_sha256": P.digest_value(subject),
            "observation_wall_utc": (
                subject.get("observation_wall_utc", wall)
                if isinstance(subject, dict)
                else wall
            ),
            "observation_monotonic_ns": (
                subject.get("observation_monotonic_ns", mono)
                if isinstance(subject, dict)
                else mono
            ),
        }
        for kind, subject_id, subject in subjects
    ]


def _sidecar(raw_doc: dict, phase: str) -> dict:
    sidecar = {
        "schema_version": P.EVIDENCE_SCHEMA,
        "phase": phase,
        "lease_id": LEASE_ID,
        "boot_identity": raw_doc["evidence"]["boot"]["boot_identity"],
        "lease_start_wall_utc": T.iso(0),
        "lease_start_monotonic_ns": T.MONO,
        "rooted_topology": _topology(raw_doc),
        "enumeration": _enumeration(raw_doc),
        "observation_attestations": [],
        "continuity_sha256": T.sha(0),
        "candidate_only": True,
        "non_authorizing": True,
    }
    sidecar["observation_attestations"] = _attestations(raw_doc, sidecar)
    sidecar["continuity_sha256"] = P.digest_value(
        P._continuity_projection(raw_doc, sidecar)
    )
    return sidecar


def _prepare_fixture() -> dict:
    x = T.fixture()
    _retime(x["prepare_doc"])
    T.rebuild_prepare(x)
    sidecar = _sidecar(x["prepare_doc"], "prepare")
    sidecar_bytes = P.canonical_json_bytes(sidecar)
    return {
        **x,
        "prepare_sidecar": sidecar,
        "prepare_sidecar_bytes": sidecar_bytes,
        "prepare_sidecar_sha": P.digest_bytes(sidecar_bytes),
    }


def _prepare_kwargs(x: dict) -> dict:
    return {
        "static_allowlist_bytes": x["allowlist_bytes"],
        "expected_static_allowlist_sha256": P.STATIC_ALLOWLIST_SHA256,
        "component_lock_bytes": x["component_bytes"],
        "expected_component_lock_sha256": x["component_sha"],
        "execution_freeze_bytes": x["freeze_bytes"],
        "expected_execution_freeze_sha256": x["freeze_sha"],
        "expected_reviewed_release_sha256": x["freeze_doc"]["reviewed_release_sha256"],
        "raw_measurement_bytes": x["prepare_bytes"],
        "expected_raw_measurement_sha256": x["prepare_sha"],
        "capability_scope_projection": x["capability"],
        "expected_capability_reference_sha256": T.sha(600),
        "expected_phase": "prepare",
        "validation_wall_time_utc": T.iso(11),
        "validation_monotonic_ns": T.MONO + 11_000_000_000,
        "v3_2_evidence_bytes": x["prepare_sidecar_bytes"],
        "expected_v3_2_evidence_sha256": x["prepare_sidecar_sha"],
    }


def _validate_prepare(x: dict | None = None) -> dict:
    x = x or _prepare_fixture()
    return P.validate_live_gate_policy_v3_2(**_prepare_kwargs(x))


def _publish_fixture() -> dict:
    x = _prepare_fixture()
    base_prepare = P.V31.validate_live_gate_policy_v3_1(
        **{
            key: value
            for key, value in _prepare_kwargs(x).items()
            if not key.startswith(("v3_2_", "expected_v3_2_"))
        }
    )
    base_prepare_bytes = P.V31.canonical_json_bytes(base_prepare)
    base_prepare_sha = P.V31.digest_bytes(base_prepare_bytes)
    prepare_result = _validate_prepare(x)
    prepare_result_bytes = P.canonical_json_bytes(prepare_result)
    prepare_result_sha = P.digest_bytes(prepare_result_bytes)
    publish_doc = T.raw(
        "publish",
        x["component_doc"],
        x["component_sha"],
        x["freeze_doc"],
        x["freeze_sha"],
        offset=20,
        prepare_raw_sha=x["prepare_sha"],
        prepare_result_sha=base_prepare_sha,
    )
    _retime(publish_doc)
    publish_bytes = P.V31.canonical_json_bytes(publish_doc)
    publish_sidecar = _sidecar(publish_doc, "publish")
    publish_sidecar_bytes = P.canonical_json_bytes(publish_sidecar)
    return {
        **x,
        "base_prepare_sha": base_prepare_sha,
        "prepare_result": prepare_result,
        "prepare_result_bytes": prepare_result_bytes,
        "prepare_result_sha": prepare_result_sha,
        "publish_doc": publish_doc,
        "publish_bytes": publish_bytes,
        "publish_sha": P.digest_bytes(publish_bytes),
        "publish_sidecar": publish_sidecar,
        "publish_sidecar_bytes": publish_sidecar_bytes,
        "publish_sidecar_sha": P.digest_bytes(publish_sidecar_bytes),
    }


def _publish_kwargs(x: dict) -> dict:
    kwargs = _prepare_kwargs(x)
    kwargs.update(
        {
            "expected_phase": "publish",
            "raw_measurement_bytes": x["publish_bytes"],
            "expected_raw_measurement_sha256": x["publish_sha"],
            "validation_wall_time_utc": T.iso(31),
            "validation_monotonic_ns": T.MONO + 31_000_000_000,
            "v3_2_evidence_bytes": x["publish_sidecar_bytes"],
            "expected_v3_2_evidence_sha256": x["publish_sidecar_sha"],
            "prepare_raw_measurement_bytes": x["prepare_bytes"],
            "independently_expected_prepare_raw_sha256": x["prepare_sha"],
            "prepare_result_bytes": x["prepare_result_bytes"],
            "independently_expected_prepare_result_sha256": x["prepare_result_sha"],
            "prepare_v3_2_evidence_bytes": x["prepare_sidecar_bytes"],
            "independently_expected_prepare_v3_2_evidence_sha256": x[
                "prepare_sidecar_sha"
            ],
        }
    )
    return kwargs


def _rebuild_sidecar(x: dict, phase: str) -> None:
    key = f"{phase}_sidecar"
    raw = x[f"{phase}_doc"]
    sidecar = x[key]
    sidecar["observation_attestations"] = _attestations(raw, sidecar)
    sidecar["continuity_sha256"] = P.digest_value(
        P._continuity_projection(raw, sidecar)
    )
    x[f"{key}_bytes"] = P.canonical_json_bytes(sidecar)
    x[f"{key}_sha"] = P.digest_bytes(x[f"{key}_bytes"])


def _rejects(call, text: str) -> None:
    try:
        call()
    except P.LiveGatePolicyV32Error as exc:
        assert text.casefold() in str(exc).casefold(), str(exc)
    else:
        raise AssertionError(f"expected V3.2 rejection containing {text!r}")


def test_green_prepare_and_publish_remain_machine_only() -> None:
    prepare = _validate_prepare()
    publish = P.validate_live_gate_policy_v3_2(**_publish_kwargs(_publish_fixture()))
    for result, phase in ((prepare, "prepare"), (publish, "publish")):
        assert result["schema_version"] == P.RESULT_SCHEMA
        assert result["phase"] == phase
        assert result["governed_member_count"] == 13
        assert result["replacement_count"] == 8
        assert result["guard_only_count"] == 5
        assert result["effect_authorized"] is False
        assert result["publication_authorized"] is False
        assert result["canonical_execution_blocked"] is True


def test_every_observation_class_after_checker_is_rejected() -> None:
    for observation_class in (
        "target",
        "sentinel",
        "process",
        "parent",
        "environment",
        "effect",
        "system_snapshot",
        "topology",
    ):
        x = _prepare_fixture()
        row = next(
            item
            for item in x["prepare_sidecar"]["observation_attestations"]
            if item["observation_class"] == observation_class
        )
        row["observation_wall_utc"] = T.iso(8)
        row["observation_monotonic_ns"] = T.MONO + 8_000_000_000
        x["prepare_sidecar_bytes"] = P.canonical_json_bytes(x["prepare_sidecar"])
        x["prepare_sidecar_sha"] = P.digest_bytes(x["prepare_sidecar_bytes"])
        _rejects(lambda: _validate_prepare(x), "checker interval")


def test_cross_volume_and_file_parent_alias_are_rejected() -> None:
    x = _prepare_fixture()
    x["prepare_sidecar"]["rooted_topology"]["parent_chains"][1][
        "identities_from_model"
    ][0]["volume_serial"] = 88
    _rebuild_sidecar(x, "prepare")
    _rejects(lambda: _validate_prepare(x), "cross-volume")

    x = _prepare_fixture()
    target_identity = deepcopy(x["prepare_doc"]["evidence"]["targets"][0]["identity"])
    target_identity["is_directory"] = True
    target_identity["attributes"] = 16
    x["prepare_sidecar"]["rooted_topology"]["parent_chains"][1][
        "identities_from_model"
    ][0] = target_identity
    _rebuild_sidecar(x, "prepare")
    _rejects(lambda: _validate_prepare(x), "identity alias")


def test_full_enumeration_api_terminal_count_digest_and_omission_are_rejected() -> None:
    mutations = (
        ("api_identity", "fake-api", "API"),
        ("terminal_status", "SUCCESS", "terminal"),
        ("raw_count", 3, "count"),
        ("rows_sha256", T.sha(9), "digest"),
    )
    for key, value, message in mutations:
        x = _prepare_fixture()
        x["prepare_sidecar"]["enumeration"][key] = value
        _rebuild_sidecar(x, "prepare")
        _rejects(lambda: _validate_prepare(x), message)
    x = _prepare_fixture()
    enumeration = x["prepare_sidecar"]["enumeration"]
    enumeration["rows"].pop()
    enumeration["raw_count"] = 1
    enumeration["rows_sha256"] = P.digest_value(enumeration["rows"])
    enumeration["derived_candidate_sha256"] = P.digest_value(enumeration["rows"])
    _rebuild_sidecar(x, "prepare")
    _rejects(lambda: _validate_prepare(x), "every derived candidate")


def test_opened_process_access_exit_reuse_and_ambiguity_remain_rejected() -> None:
    for key, value, message in (
        ("process_handle_access", "ACCESS_DENIED", "access"),
        ("liveness_status", "EXITED", "exit"),
        ("creation_token", "", "creation"),
    ):
        x = _prepare_fixture()
        row = x["prepare_doc"]["evidence"]["bounded_process_snapshot"]["rows"][0]
        row[key] = value
        T.rebuild_prepare(x)
        x["prepare_sidecar"] = _sidecar(x["prepare_doc"], "prepare")
        x["prepare_sidecar_bytes"] = P.canonical_json_bytes(x["prepare_sidecar"])
        x["prepare_sidecar_sha"] = P.digest_bytes(x["prepare_sidecar_bytes"])
        _rejects(lambda: _validate_prepare(x), message)


def test_same_lease_boot_whole_duration_and_interphase_skew_are_rejected() -> None:
    x = _publish_fixture()
    x["publish_sidecar"]["lease_id"] = "other_V32_0123456789abcdefghijklmnop"
    _rebuild_sidecar(x, "publish")
    _rejects(
        lambda: P.validate_live_gate_policy_v3_2(**_publish_kwargs(x)),
        "same opaque lease",
    )
    x = _publish_fixture()
    x["publish_sidecar"]["boot_identity"] = T.sha(999)
    _rebuild_sidecar(x, "publish")
    _rejects(
        lambda: P.validate_live_gate_policy_v3_2(**_publish_kwargs(x)), "boot"
    )
    x = _prepare_fixture()
    kwargs = _prepare_kwargs(x)
    kwargs["validation_wall_time_utc"] = T.iso(121)
    kwargs["validation_monotonic_ns"] = T.MONO + 121_000_000_000
    _rejects(lambda: P.validate_live_gate_policy_v3_2(**kwargs), "whole-lease")
    x = _publish_fixture()
    kwargs = _publish_kwargs(x)
    kwargs["validation_wall_time_utc"] = T.iso(41)
    _rejects(lambda: P.validate_live_gate_policy_v3_2(**kwargs), "whole-lease")


def test_numeric_float_bool_negative_and_overflow_are_rejected() -> None:
    for value in (2.0, True, -1, P.MAX_INTEGER + 1):
        x = _prepare_fixture()
        x["prepare_sidecar"]["enumeration"]["raw_count"] = value
        x["prepare_sidecar_bytes"] = P.canonical_json_bytes(x["prepare_sidecar"])
        x["prepare_sidecar_sha"] = P.digest_bytes(x["prepare_sidecar_bytes"])
        _rejects(lambda: _validate_prepare(x), "strict integer")
    x = _prepare_fixture()
    x["prepare_doc"]["evidence"]["targets"][0]["size_bytes"] = 4.0
    T.rebuild_prepare(x)
    _rejects(lambda: _validate_prepare(x), "strict integer")


def test_canonical_continuity_hash_and_prepare_result_substitution_are_rejected() -> None:
    x = _prepare_fixture()
    x["prepare_sidecar"]["continuity_sha256"] = T.sha(123)
    x["prepare_sidecar_bytes"] = P.canonical_json_bytes(x["prepare_sidecar"])
    x["prepare_sidecar_sha"] = P.digest_bytes(x["prepare_sidecar_bytes"])
    _rejects(lambda: _validate_prepare(x), "continuity")

    x = _publish_fixture()
    x["prepare_result"]["effect_authorized"] = True
    x["prepare_result_bytes"] = P.canonical_json_bytes(x["prepare_result"])
    x["prepare_result_sha"] = P.digest_bytes(x["prepare_result_bytes"])
    _rejects(
        lambda: P.validate_live_gate_policy_v3_2(**_publish_kwargs(x)),
        "does not recompute",
    )


def test_v31_allowlist_sizes_graph_executables_and_authorization_stay_frozen() -> None:
    assert P.STATIC_ALLOWLIST_SHA256 == (
        "a3e18ac151a4d0fb51afc282874e873f2c3344b5aab858bc5da1d1e2acec4a80"
    )
    x = _prepare_fixture()
    x["component_doc"]["artifact_graph"]["nodes"].append(
        {
            "artifact_id": "extra",
            "artifact_type": "extra",
            "sha256": T.sha(4),
            "depends_on": [],
        }
    )
    T.rebuild_component(x)
    kwargs = _prepare_kwargs(x)
    _rejects(lambda: P.validate_live_gate_policy_v3_2(**kwargs), "extra or missing")
