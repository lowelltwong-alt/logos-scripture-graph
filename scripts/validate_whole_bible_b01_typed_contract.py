#!/usr/bin/env python3
"""Fail-closed, provider-neutral checks for the future B01 typed packet.

This validator is intentionally independent of the selected revision-7 B00
receipt code.  It validates shape and binding rules; it does not authorize B02.
"""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from pathlib import Path
from typing import Any

ROLES = {
    "original_language_translation_scout",
    "literary_form_scout",
    "canonical_relations_and_premortem_scout",
    "second_temple_rabbinic_context_scout",
}
FORBIDDEN = {"chunk", "chunkmap", "selectedboundary", "finalboundary", "hebrewtext", "greektext", "sourcetext", "chainofthought", "hiddenreasoning", "systemprompt", "userprompt"}
ZERO_WIDTH = dict.fromkeys(map(ord, "\u200b\u200c\u200d\ufeff"), None)


class B01ContractError(ValueError):
    pass


def norm(value: Any) -> str:
    return unicodedata.normalize("NFKC", str(value)).translate(ZERO_WIDTH).casefold()


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _walk(obj: Any, path: str = "$"):
    yield path, obj
    if isinstance(obj, dict):
        for key, value in obj.items():
            yield from _walk(value, f"{path}.{key}")
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            yield from _walk(value, f"{path}[{i}]")


def validate_payload(payload: Any) -> None:
    strings: list[str] = []
    for path, value in _walk(payload):
        if isinstance(value, dict):
            for key in value:
                compact = re.sub(r"[^a-z0-9]", "", norm(key))
                if compact in FORBIDDEN or "chunk" in compact and compact not in {"chunking"}:
                    raise B01ContractError(f"QF-20-B01-PAYLOAD: forbidden key at {path}.{key}")
        elif isinstance(value, str):
            strings.append(norm(value))
    joined = " ".join(strings)
    if any(token in joined for token in ("<osis", "<reversednun", "<sblgnt")):
        raise B01ContractError("QF-20-B01-PAYLOAD: source markup")
    if re.search(r"[\u0590-\u05ff]{8,}|[\u0370-\u03ff]{8,}", joined):
        raise B01ContractError("QF-20-B01-PAYLOAD: unbounded original-language text")


def validate_packet(packet: dict[str, Any], *, manifest: dict[str, str], role_reports: dict[str, dict[str, Any]],
                    synthesis: dict[str, Any], redteam: dict[str, Any], boss: dict[str, Any]) -> None:
    required = {"schema_version", "kind", "book", "run_id", "stage_attempt_id", "candidate_only", "non_authorizing", "identity", "payload"}
    if set(packet) != required or packet["schema_version"] != "whole_bible_b01_typed_contract.v1":
        raise B01ContractError("QF-SCHEMA: typed packet shape")
    if packet["candidate_only"] is not True or packet["non_authorizing"] is not True:
        raise B01ContractError("QF-10-AUTHORITY-SMUGGLING: packet authority flags")
    validate_payload(packet["payload"])
    if set(role_reports) != ROLES:
        raise B01ContractError("QF-16-B01-INPUT-CLOSURE: exact role set required")
    ids = []
    for role, report in role_reports.items():
        if not isinstance(report.get("payload"), dict) or not report["payload"].get("observations"):
            raise B01ContractError(f"QF-16-B01-ROLE-REPORT: empty report {role}")
        validate_payload(report["payload"])
        ids.append(report["identity"].get("execution_id"))
    if len(set(ids)) != len(ids):
        raise B01ContractError("QF-16-B01-CONTROLLER-ATTESTATION: duplicate execution identity")
    if not synthesis.get("payload", {}).get("role_report_artifact_ids"):
        raise B01ContractError("QF-16-B01-ROLE-REPORT: synthesis lacks role lineage")
    if not redteam.get("payload", {}).get("findings"):
        raise B01ContractError("QF-15-B01-SEMANTIC-ARTIFACT: empty red-team findings")
    for item, label in ((synthesis, "synthesis"), (redteam, "redteam"), (boss, "boss")):
        validate_payload(item.get("payload", {}))
    boss_payload = boss.get("payload", {})
    if boss_payload.get("input_manifest_sha256") not in set(manifest.values()):
        raise B01ContractError("QF-B01-BOSS: stale input manifest binding")
    if boss_payload.get("verdict") not in {"GO_B01_RECEIPT_ONLY", "NO_GO"}:
        raise B01ContractError("QF-B01-BOSS: invalid verdict")
    identities = [r.get("identity", {}) for r in role_reports.values()] + [synthesis.get("identity", {}), redteam.get("identity", {})]
    if boss.get("identity") in identities:
        raise B01ContractError("QF-B01-BOSS: boss identity not independent")
    if not boss_payload.get("dissent") or not boss_payload.get("appeal_route"):
        raise B01ContractError("QF-B01-APPEAL-CLOSURE: dissent and appeal route required")


if __name__ == "__main__":
    print("B01 typed contract validator loaded; B01 materialization remains disabled.")
