#!/usr/bin/env python3
"""Generate a no-context audit brief for a branch or PR review."""
from __future__ import annotations

import argparse
import datetime as dt
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT_ROOT = ROOT / ".ai" / "audits" / "reports"


def run_git(args: list[str]) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.STDOUT).strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        return f"UNAVAILABLE: {exc}"


def optional_file(path: str) -> str:
    target = ROOT / path
    return path if target.exists() else f"{path} (missing)"


def changed_files(base_ref: str) -> str:
    merge_base = run_git(["merge-base", "HEAD", base_ref])
    if merge_base.startswith("UNAVAILABLE"):
        committed = merge_base
    else:
        committed = run_git(["diff", "--name-status", f"{merge_base}...HEAD"]) or "(none)"
    staged = run_git(["diff", "--cached", "--name-status"]) or "(none)"
    unstaged = run_git(["diff", "--name-status"]) or "(none)"
    untracked = run_git(["ls-files", "--others", "--exclude-standard"]) or "(none)"
    return "\n".join(
        [
            "[committed-vs-base]",
            committed,
            "",
            "[staged]",
            staged,
            "",
            "[unstaged]",
            unstaged,
            "",
            "[untracked]",
            untracked,
        ]
    )


def build_brief(task_id: str, base_ref: str, pr: str | None) -> str:
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    branch = run_git(["branch", "--show-current"])
    status = run_git(["status", "-sb"])
    head = run_git(["rev-parse", "HEAD"])
    merge_base = run_git(["merge-base", "HEAD", base_ref])
    diff = changed_files(base_ref)
    pr_line = pr or "not provided"

    required_reads = [
        "AI_FRONT_DOOR.md",
        ".ai/audits/README.md",
        ".ai/audits/NO_CONTEXT_REVIEW_PROTOCOL.md",
        ".ai/control/audit_surface_map.yaml",
        "ROADMAP_STATE.yaml",
        ".ai/control/PROJECT_STATUS.md",
        ".ai/control/current_focus.yaml",
        f".ai/tasks/{task_id}.task.yaml",
        f".ai/handoffs/{task_id}/handoff.md",
        ".ai/control/roadmap_events.jsonl",
        ".ai/control/handoff_ledger.jsonl",
        ".ai/control/harness_upgrade_roadmap.yaml",
        ".ai/control/chunking_theological_decision_register.yaml",
        ".ai/control/governance_memory_durability_policy.yaml",
        ".ai/control/owner_decision_projection_policy.yaml",
        ".ai/control/bible_chunking_readiness_map.yaml",
    ]

    validations = [
        "python scripts/validate_audit_surface_map.py",
        "python scripts/validate_chunking_agent_preflight.py",
        "python scripts/validate_chunking_theological_decision_register.py",
        "python scripts/validate_governance_memory_durability.py",
        "python scripts/validate_owner_decision_projection_policy.py",
        "python scripts/validate_bible_chunking_readiness_map.py",
        "python scripts/validate_all.py",
        "python -m pytest -q",
    ]

    reads_block = "\n".join(f"- {optional_file(path)}" for path in required_reads)
    validation_block = "\n".join(f"- `{cmd}`" for cmd in validations)

    return f"""# No-Context Audit Brief

## Review Target

- generated_at: {now}
- task_id: {task_id}
- branch: {branch}
- base_ref: {base_ref}
- merge_base: {merge_base}
- head: {head}
- pr: {pr_line}

## Worktree State

```text
{status}
```

## Changed Files

```text
{diff}
```

## Required Read Order

{reads_block}

## Required Validation

{validation_block}

## Red-Team Focus

- Prove every claim from repo files, git/PR state, logs, handoffs, decision registers, readiness maps, review packets, and validation output.
- Treat chat-only claims as unproven.
- Verify that pending packets or owner-selection dockets are not treated as reviewed gold.
- Verify that raw/canonical/generated chunk/evaluator/vector/edge surfaces were not touched without explicit authorization.
- Verify that theological downstream decisions are recorded in the decision register.
- Verify that the decision register remains protected and discoverable, and that any projected owner-pattern decision includes a conflict scan.
- Verify that no source metadata, cross-reference, Strong's-style number, Greek lexical rarity, heading, footnote, WJ marker, or formatting becomes hidden authority.
- Check `.ai/control/harness_upgrade_roadmap.yaml`; if this review reveals a repeated manual check or likely future failure mode, update the roadmap or record why no harness is needed.

## Report Location

Write findings to `.ai/audits/reports/` using `.ai/audits/templates/REVIEW_REPORT_TEMPLATE.md`.
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--base-ref", default="origin/main")
    parser.add_argument("--pr", default=None)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--print", action="store_true", dest="print_brief")
    args = parser.parse_args(argv)

    brief = build_brief(args.task_id, args.base_ref, args.pr)
    if args.output:
        output = (ROOT / args.output).resolve() if not args.output.is_absolute() else args.output.resolve()
        report_root = REPORT_ROOT.resolve()
        if report_root not in output.parents and output != report_root:
            print(
                f"ERROR: output must be under {report_root}",
                file=sys.stderr,
            )
            return 2
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(brief, encoding="utf-8")
        print(output.relative_to(ROOT))
    if args.print_brief or not args.output:
        print(brief)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
