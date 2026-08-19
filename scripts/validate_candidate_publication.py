#!/usr/bin/env python3
"""Validate the tracked metadata-only candidate publication without source-history access."""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from scripts import build_candidate_publication as publication
except ImportError:  # pragma: no cover - direct script execution
    import build_candidate_publication as publication


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "config" / "publications" / "m7_sol_candidate_v1.json"
MANIFEST = ROOT / "docs" / "publications" / "m7-sol-candidate-v1" / "ARTIFACT_MANIFEST.json"
README = ROOT / "docs" / "publications" / "m7-sol-candidate-v1" / "README.md"


def validate_repository() -> dict[str, object]:
    contract = publication._load_json(CONTRACT)
    manifest = publication._load_json(MANIFEST)
    publication.validate_manifest_envelope(contract, manifest)
    try:
        readme = README.read_text(encoding="utf-8")
    except OSError as exc:
        raise publication.PublicationError("PUB-README", str(exc)) from exc
    required_text = [
        "66/66 book strategies",
        "1,178 candidate-map rows",
        "22/66 correctively rereviewed",
        "| Replay qualified | **no** |",
        "| Release qualified | **no** |",
        "metadata and hashes only",
        "M8",
        "correlated model voice",
        "automatic reviewed-gold promotion is forbidden",
    ]
    missing = [text for text in required_text if text not in readme]
    if missing:
        raise publication.PublicationError("PUB-README", f"missing required disclosure text: {missing}")
    forbidden_claims = [
        "M7 is release ready",
        "M7 and M8 have converged",
        "independent provider consensus",
        "66/66 correctively rereviewed",
    ]
    present = [text for text in forbidden_claims if text in readme]
    if present:
        raise publication.PublicationError("PUB-README-AUTHORITY", f"forbidden claim text: {present}")
    return {
        "status": "pass",
        "publication_id": contract["publication_id"],
        "manifest_digest": manifest["manifest_digest"],
        "immutable_pointer_count": len(manifest["inventory"]),
        "embedded_payload_bytes": manifest["selection_summary"]["payload_bytes_embedded"],
        "replay_qualified": manifest["coverage"]["replay_qualified"],
        "release_qualified": manifest["coverage"]["release_qualified"],
    }


def main() -> int:
    try:
        result = validate_repository()
    except publication.PublicationError as exc:
        print(f"Candidate publication validation failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
