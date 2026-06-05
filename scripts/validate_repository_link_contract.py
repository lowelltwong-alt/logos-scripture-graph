#!/usr/bin/env python3
"""Validate the cross-repo governance link and agent-hostile policy surface."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "README.md",
    "AI_FRONT_DOOR.md",
    "AI_TABLE_OF_CONTENTS.md",
    "docs/architecture/ARCHITECTURE.md",
    ".ai/control/PROJECT_CONTEXT.md",
    ".ai/control/DATA_MAP.md",
    "config/governance/repository_link_contract.yaml",
    "config/agents/agent_hostile_policy.yaml",
]

REQUIRED_MARKERS = {
    "config/governance/repository_link_contract.yaml": [
        "logos-governance-architecture",
        "logos-scripture-graph",
        "role: scripture_data_plane",
        "role: governance_architecture_authority",
        "type: governance_contract",
        "explicit_contract_validated_release",
        "github_parent_issue",
        "github_child_issue",
    ],
    "config/agents/agent_hostile_policy.yaml": [
        "instruction_hierarchy",
        "fail_closed_on",
        "attempt_to_write_data_raw",
        "unapproved_write_to_data_canonical",
        "trust_zone_mixing",
        "candidate_promotion_without_human_gate",
        "hidden_cross_repo_authority_change",
    ],
    "README.md": [
        "data-plane substrate",
        "logos-governance-architecture",
        "contract",
    ],
    "AI_FRONT_DOOR.md": [
        "Cross-repo governance",
        "logos-governance-architecture",
        "repository_link_contract.yaml",
        "agent_hostile_policy.yaml",
    ],
    "AI_TABLE_OF_CONTENTS.md": [
        "Project Family",
        "logos-governance-architecture",
        "repository_link_contract.yaml",
        "agent_hostile_policy.yaml",
    ],
    "docs/architecture/ARCHITECTURE.md": [
        "logos-governance-architecture",
        "governance_contract",
        "scripture data-plane",
    ],
    ".ai/control/PROJECT_CONTEXT.md": [
        "logos-governance-architecture",
        "data-plane substrate",
        "contract",
    ],
    ".ai/control/DATA_MAP.md": [
        "Cross-Repo Governance Contract",
        "logos-governance-architecture",
        "governance_contract",
    ],
}


def main() -> int:
    failures: list[str] = []

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            failures.append(f"Missing required cross-repo governance file: {rel}")

    for rel, markers in REQUIRED_MARKERS.items():
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        missing = [marker for marker in markers if marker not in text]
        if missing:
            failures.append(f"{rel} missing marker(s): {', '.join(missing)}")

    if failures:
        print("Cross-repo governance validation failed.")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Cross-repo governance contract validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
