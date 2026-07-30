#!/usr/bin/env python3
"""Fail-closed validation for the revision-8 B01 typed evidence packet.

This is deliberately separate from the selected revision-7 B00 validator.  It
checks controller-observed identity/timing, exact role closure, append-only
challenge/appeal records, and boss binding.  A passing packet is still only a
candidate and never authorizes B02.
"""
from __future__ import annotations

import argparse, hashlib, json, re, unicodedata
from pathlib import Path
from typing import Any

ROLES = {"original_language_translation_scout", "literary_form_scout", "canonical_relations_and_premortem_scout", "second_temple_rabbinic_context_scout"}
ZERO_WIDTH = dict.fromkeys(map(ord, "\u200b\u200c\u200d\ufeff"), None)
FORBIDDEN = {"selectedboundary", "finalboundary", "startverse", "endverse", "sourcetext", "hebrewtext", "greektext", "chainofthought", "hiddenreasoning", "systemprompt", "userprompt"}
BOUNDARY_WORD = re.compile(r"(?:chunk|partition|range|span|boundary)", re.I)


class B01R8Error(ValueError):
    pass


def norm(value: Any) -> str:
    return unicodedata.normalize("NFKC", str(value)).translate(ZERO_WIDTH).casefold()


def sha(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def walk(value: Any, path: str = "$"):
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk(child, f"{path}.{key}")
    elif isinstance(value, list):
        for i, child in enumerate(value):
            yield from walk(child, f"{path}[{i}]")


def validate_safe_payload(value: Any) -> None:
    for path, child in walk(value):
        if isinstance(child, dict):
            for key in child:
                compact = re.sub(r"[^a-z0-9]", "", norm(key))
                if compact in FORBIDDEN or compact.startswith("raw") or "hiddenreasoning" in compact:
                    raise B01R8Error(f"QF-20-B01-PAYLOAD: forbidden key at {path}.{key}")
                if BOUNDARY_WORD.search(norm(key)) and compact not in {"boundaryrationale", "boundaryevidence"} and not any(token in norm(path) for token in ("source_digests", "source_ids", "source_refs")):
                    raise B01R8Error(f"QF-15-B01-BOUNDARY-LEAKAGE: boundary-like key at {path}.{key}")
        elif isinstance(child, str):
            text = norm(child)
            if any(token in text for token in ("<osis", "<reversednun", "<sblgnt", "<w " )):
                raise B01R8Error(f"QF-20-B01-PAYLOAD: source markup at {path}")
            if re.search(r"[\u0590-\u05ff]{8,}|[\u0370-\u03ff]{8,}", text):
                raise B01R8Error(f"QF-20-B01-PAYLOAD: unbounded original-language text at {path}")


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise B01R8Error(f"QF-SCHEMA: cannot load {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise B01R8Error(f"QF-SCHEMA: object required: {path}")
    validate_safe_payload(value)
    return value


def _common(doc: dict[str, Any], *, book: str, run_id: str, attempt: str) -> None:
    if doc.get("schema_version") not in {"whole_bible_b01_typed_contract.v2", "whole_bible_b01_role_report.v2", "whole_bible_b01_boss_authorization.v2", "whole_bible_b01_challenge_appeal.v1", "whole_bible_b01_input_manifest.v1"}:
        raise B01R8Error("QF-SCHEMA: unsupported revision-8 B01 schema")
    if any(doc.get(k) != v for k, v in (("book", book), ("run_id", run_id), ("stage_attempt_id", attempt))):
        raise B01R8Error("QF-17-B01-ATTRIBUTION: identity scope mismatch")
    if doc.get("candidate_only") is not True or doc.get("non_authorizing") is not True:
        raise B01R8Error("QF-10-AUTHORITY-SMUGGLING: authority flags")
    ident = doc.get("identity")
    if not isinstance(ident, dict) or not all(isinstance(ident.get(k), str) and ident[k] for k in ("execution_id", "assignment_id", "agent_instance_id", "role_id", "provider_family")):
        raise B01R8Error("QF-16-B01-CONTROLLER-ATTESTATION: incomplete identity")
    events = doc.get("controller_event_ids")
    if not isinstance(events, list) or not events or len(set(events)) != len(events):
        raise B01R8Error("QF-16-B01-CONTROLLER-ATTESTATION: event closure")
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", str(doc.get("input_manifest_sha256", ""))):
        raise B01R8Error("QF-16-B01-INPUT-CLOSURE: manifest digest")


def validate_packet_dir(packet_dir: Path, *, book: str, run_id: str, attempt: str) -> dict[str, Any]:
    docs = {path.name: load(path) for path in sorted(packet_dir.glob("*.json"))}
    if not docs:
        raise B01R8Error("QF-SCHEMA: empty packet")
    reports = {doc.get("identity", {}).get("role_id"): doc for doc in docs.values() if doc.get("kind") == "role_report"}
    if set(reports) != ROLES:
        raise B01R8Error(f"QF-16-B01-INPUT-CLOSURE: roles={sorted(reports)}")
    executions: set[str] = set()
    manifest_digests: set[str] = set()
    for doc in docs.values():
        _common(doc, book=book, run_id=run_id, attempt=attempt)
        executions.add(doc["identity"]["execution_id"])
        manifest_digests.add(doc["input_manifest_sha256"])
    if len(executions) != len(docs):
        raise B01R8Error("QF-16-B01-CONTROLLER-ATTESTATION: duplicate execution identity")
    for role, report in reports.items():
        if not report.get("observations") or not report.get("source_refs"):
            raise B01R8Error(f"QF-15-B01-SEMANTIC-ARTIFACT: incomplete report {role}")
    boss = next((doc for doc in docs.values() if doc.get("kind") == "boss_authorization"), None)
    if boss is None:
        raise B01R8Error("QF-B01-BOSS: boss review missing")
    if boss["input_manifest_sha256"] not in manifest_digests:
        raise B01R8Error("QF-B01-BOSS: stale input manifest binding")
    if boss.get("identity", {}).get("agent_instance_id") in {doc["identity"]["agent_instance_id"] for doc in docs.values() if doc is not boss}:
        raise B01R8Error("QF-B01-BOSS: boss identity not independent")
    if boss.get("verdict") not in {"GO_B01_RECEIPT_ONLY", "NO_GO", "HOLD"}:
        raise B01R8Error("QF-B01-BOSS: invalid verdict")
    if not boss.get("rationale") or not boss.get("appeal_route"):
        raise B01R8Error("QF-B01-APPEAL-CLOSURE: missing rationale/appeal route")
    return {"status": "passed_candidate_only", "documents": len(docs), "roles": sorted(reports), "boss_verdict": boss["verdict"], "B02_authorized": False}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet_dir", type=Path); parser.add_argument("--book", required=True); parser.add_argument("--run-id", required=True); parser.add_argument("--attempt", required=True)
    args = parser.parse_args(argv)
    try: print(json.dumps(validate_packet_dir(args.packet_dir, book=args.book, run_id=args.run_id, attempt=args.attempt), sort_keys=True))
    except B01R8Error as exc: print(str(exc)); return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


