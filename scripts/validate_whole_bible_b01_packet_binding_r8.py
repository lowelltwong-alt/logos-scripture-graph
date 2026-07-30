#!/usr/bin/env python3
"""Additional revision-8 packet/manifest binding checks.

Kept as a separate gate so the selected revision-7 B00 validator is never
mutated. It composes the structural r8 validator and then checks the exact
input manifest and non-circular boss packet digest.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from scripts.validate_whole_bible_b01_typed_contract_r8 import B01R8Error, load, validate_packet_dir


def packet_digest(docs: dict[str, dict]) -> str:
    rows = {name: hashlib.sha256(json.dumps(doc, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest() for name, doc in docs.items() if doc.get("kind") != "boss_authorization"}
    return "sha256:" + hashlib.sha256(json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def validate(path: Path, *, book: str, run_id: str, attempt: str) -> dict:
    result = validate_packet_dir(path, book=book, run_id=run_id, attempt=attempt)
    docs = {p.name: load(p) for p in sorted(path.glob("*.json"))}
    manifest = next((d for d in docs.values() if d.get("kind") == "input_manifest"), None)
    boss = next((d for d in docs.values() if d.get("kind") == "boss_authorization"), None)
    if manifest is None or not manifest.get("source_ids"):
        raise B01R8Error("QF-16-B01-INPUT-CLOSURE: exact input manifest missing")
    if boss is None or boss.get("input_manifest_sha256") != manifest.get("input_manifest_sha256"):
        raise B01R8Error("QF-16-B01-INPUT-CLOSURE: manifest digest disagreement")
    if boss.get("packet_sha256") != packet_digest(docs):
        raise B01R8Error("QF-B01-BOSS: packet hash does not bind immutable evidence")
    result["packet_sha256"] = boss["packet_sha256"]
    result["source_count"] = len(manifest["source_ids"])
    return result


def main(argv=None) -> int:
    p = argparse.ArgumentParser(); p.add_argument("packet_dir", type=Path); p.add_argument("--book", required=True); p.add_argument("--run-id", required=True); p.add_argument("--attempt", required=True); a = p.parse_args(argv)
    try: print(json.dumps(validate(a.packet_dir, book=a.book, run_id=a.run_id, attempt=a.attempt), sort_keys=True))
    except B01R8Error as exc: print(str(exc)); return 1
    return 0


if __name__ == "__main__": raise SystemExit(main())
