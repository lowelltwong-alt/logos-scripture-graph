#!/usr/bin/env python3
"""Run deterministic post-merge verification for a merged pull request."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
PY = sys.executable

PROTECTED_PATHS = [
    "data/raw/**",
    "data/canonical/**",
    "data/derived/**",
    "pipelines/chunking/chunker.py",
    "pipelines/chunking/orchestrator.py",
    "pipelines/chunking/evaluate_chunks.py",
    "pipelines/chunking/leaderboard.py",
    "pipelines/chunking/skills/**",
    "registry/chunking/**",
    "eval/chunking_runs/**",
    "eval/LEADERBOARD.md",
]


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str


@dataclass
class CommandResult:
    name: str
    command: list[str]
    returncode: int
    stdout: str
    stderr: str

    @property
    def passed(self) -> bool:
        return self.returncode == 0


def run_command(name: str, command: list[str]) -> CommandResult:
    try:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    except FileNotFoundError:
        # Missing executable (e.g. gh or git absent) must fail closed with a clean
        # report line, not an uncaught traceback that hides the verdict.
        return CommandResult(
            name=name,
            command=command,
            returncode=127,
            stdout="",
            stderr=f"command not found: {command[0]}",
        )
    return CommandResult(
        name=name,
        command=command,
        returncode=result.returncode,
        stdout=result.stdout.strip(),
        stderr=result.stderr.strip(),
    )


def check_path_absent(path: Path) -> CheckResult:
    return CheckResult(
        name=f"{path.relative_to(ROOT)} absent",
        passed=not path.exists(),
        detail="absent" if not path.exists() else "present",
    )


def parse_pr_json(stdout: str) -> dict[str, Any]:
    try:
        value = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise ValueError(f"gh pr view did not return JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("gh pr view JSON root was not an object")
    return value


def status_checks_green(status_rollup: list[dict[str, Any]]) -> tuple[bool, str]:
    if not status_rollup:
        return True, "no GitHub status checks reported"

    failures: list[str] = []
    summaries: list[str] = []
    for item in status_rollup:
        name = str(item.get("name") or item.get("context") or item.get("__typename") or "unknown")
        typename = item.get("__typename")
        if typename == "CheckRun":
            status = item.get("status")
            conclusion = item.get("conclusion")
            summaries.append(f"{name}: {status}/{conclusion}")
            if status != "COMPLETED" or conclusion not in {"SUCCESS", "SKIPPED", "NEUTRAL"}:
                failures.append(f"{name} is {status}/{conclusion}")
        elif typename == "StatusContext":
            state = item.get("state")
            summaries.append(f"{name}: {state}")
            if state not in {"SUCCESS", "SKIPPED"}:
                failures.append(f"{name} is {state}")
        else:
            summaries.append(f"{name}: unrecognized status type {typename}")
            failures.append(f"{name} has unrecognized status type {typename}")
    return not failures, "; ".join(failures or summaries)


def parse_yaml_files(paths: list[Path]) -> CheckResult:
    parsed = 0
    for path in paths:
        with path.open("r", encoding="utf-8") as handle:
            yaml.safe_load(handle)
        parsed += 1
    return CheckResult("YAML parse checks", True, f"parsed {parsed} YAML file(s)")


def parse_jsonl_files(paths: list[Path]) -> CheckResult:
    details: list[str] = []
    for path in paths:
        count = 0
        with path.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, 1):
                if line.strip():
                    try:
                        json.loads(line)
                    except json.JSONDecodeError as exc:
                        raise ValueError(f"{path}:{line_no}: invalid JSONL: {exc}") from exc
                    count += 1
        details.append(f"{path.relative_to(ROOT)}={count}")
    return CheckResult("JSONL parse checks", True, "; ".join(details))


def all_task_yaml_paths() -> list[Path]:
    task_root = ROOT / ".ai" / "tasks"
    return sorted(task_root.glob("*.task.yaml"))


def task_in_roadmap_state(task_id: str) -> bool:
    state_path = ROOT / "ROADMAP_STATE.yaml"
    if not state_path.exists():
        return False
    state = yaml.safe_load(state_path.read_text(encoding="utf-8")) or {}

    def walk(value: Any) -> bool:
        if isinstance(value, dict):
            if value.get("id") == task_id:
                return True
            return any(walk(v) for v in value.values())
        if isinstance(value, list):
            return any(walk(item) for item in value)
        return False

    return walk(state)


def mentions_task(text: str, task_id: str) -> bool:
    """Token-bounded match so ``T340`` does not falsely match ``T340B``."""
    return re.search(rf"\b{re.escape(task_id)}\b", text) is not None


def next_task_state(task_id: str | None) -> dict[str, Any]:
    """Report-only next-task presence. Detection never authorizes implementation."""
    if not task_id:
        return {"provided": False, "status": "not requested"}

    task_file = ROOT / ".ai" / "tasks" / f"{task_id}.task.yaml"
    handoff_file = ROOT / ".ai" / "handoffs" / task_id / "handoff.md"
    status_paths = [
        ROOT / "ROADMAP_STATE.yaml",
        ROOT / ".ai" / "control" / "PROJECT_STATUS.md",
        ROOT / ".ai" / "control" / "current_focus.yaml",
    ]
    mentions = [
        str(path.relative_to(ROOT))
        for path in status_paths
        if path.exists() and mentions_task(path.read_text(encoding="utf-8"), task_id)
    ]
    roadmap_found = task_in_roadmap_state(task_id)

    # Exact authorization surfaces (task file / handoff / roadmap id field) -> found.
    # Token-bounded prose mentions alone -> ambiguous. Nothing at all -> not_found.
    if task_file.exists() or handoff_file.exists() or roadmap_found:
        status = "found"
    elif mentions:
        status = "ambiguous"
    else:
        status = "not_found"

    return {
        "provided": True,
        "task_id": task_id,
        "task_file_exists": task_file.exists(),
        "handoff_exists": handoff_file.exists(),
        "roadmap_state_field_found": roadmap_found,
        "mentioned_in": mentions,
        "status": status,
        "authorization_note": "report-only: presence does not authorize implementation",
    }


def append_command_checks(checks: list[CheckResult], commands: list[CommandResult]) -> None:
    for command in commands:
        detail_parts = []
        if command.stdout:
            detail_parts.append(command.stdout)
        if command.stderr:
            detail_parts.append(f"stderr: {command.stderr}")
        checks.append(
            CheckResult(
                command.name,
                command.passed,
                "\n".join(detail_parts) if detail_parts else f"exit {command.returncode}",
            )
        )


def format_text_report(report: dict[str, Any]) -> str:
    lines = [
        "# Post-Merge Verification Report",
        "",
        f"Final verdict: {report['verdict']}",
        "",
        "## Main Status",
        report["main_status"],
        "",
        "## PR Status",
        report["pr_status"],
        "",
        "## PR Checks",
    ]
    lines.extend(f"- {item['name']}: {'PASS' if item['passed'] else 'FAIL'} - {item['detail']}" for item in report["pr_checks"])
    lines.extend(
        [
            "",
            "## Commit Reachability",
        ]
    )
    lines.extend(f"- {item['name']}: {'PASS' if item['passed'] else 'FAIL'} - {item['detail']}" for item in report["commit_checks"])
    lines.extend(
        [
            "",
            "## Working Tree And Merge/Rebase State",
        ]
    )
    lines.extend(f"- {item['name']}: {'PASS' if item['passed'] else 'FAIL'} - {item['detail']}" for item in report["state_checks"])
    lines.extend(["", "## Validation Results"])
    for item in report["validation_checks"]:
        if item["name"] == "pytest" and item["detail"].startswith("SKIPPED"):
            lines.append(f"- pytest: {item['detail']}")
            continue
        status = "PASS" if item["passed"] else "FAIL"
        suffix = f" - {item['detail']}" if not item["passed"] else ""
        lines.append(f"- {item['name']}: {status}{suffix}")
    if report.get("pytest_skipped"):
        lines.append("> WARNING: full pytest gate was SKIPPED via --skip-pytest; this verdict does not cover the test suite.")
    lines.extend(["", "## Next Task State", json.dumps(report["next_task"], indent=2)])
    lines.append("> Next-task detection is report-only. A PASS verdict verifies the merge; it does not authorize the next task, output-changing work, reviewed-gold promotion, or skill lifecycle promotion.")
    lines.extend(["", "## Protected-Path Reminder"])
    lines.extend(f"- {path}" for path in report["protected_paths"])
    return "\n".join(lines)


def build_report(args: argparse.Namespace) -> tuple[dict[str, Any], int]:
    commands: list[CommandResult] = [
        run_command("git fetch origin", ["git", "fetch", "origin"]),
        run_command("git checkout main", ["git", "checkout", "main"]),
        run_command("git pull --ff-only origin main", ["git", "pull", "--ff-only", "origin", "main"]),
    ]
    setup_checks: list[CheckResult] = []
    append_command_checks(setup_checks, commands)

    status = run_command("git status --short", ["git", "status", "--short"])
    setup_checks.append(
        CheckResult(
            "git status --short clean",
            status.passed and not status.stdout,
            status.stdout or "clean",
        )
    )

    state_checks = [
        *setup_checks,
        check_path_absent(ROOT / ".git" / "MERGE_HEAD"),
        check_path_absent(ROOT / ".git" / "rebase-merge"),
        check_path_absent(ROOT / ".git" / "rebase-apply"),
    ]

    pr_view = run_command(
        "gh pr view",
        [
            "gh",
            "pr",
            "view",
            str(args.pr),
            "--json",
            "number,title,state,mergedAt,mergeCommit,statusCheckRollup",
        ],
    )
    pr_status = "unavailable"
    pr_json: dict[str, Any] = {}
    pr_checks: list[CheckResult] = [
        CheckResult("gh pr view", pr_view.passed, pr_view.stdout or pr_view.stderr or f"exit {pr_view.returncode}")
    ]
    if pr_view.passed:
        try:
            pr_json = parse_pr_json(pr_view.stdout)
            pr_checks.append(CheckResult("PR state is MERGED", pr_json.get("state") == "MERGED", str(pr_json.get("state"))))
            green, detail = status_checks_green(pr_json.get("statusCheckRollup") or [])
            pr_checks.append(CheckResult("GitHub status checks green", green, detail))
            merge_commit = (pr_json.get("mergeCommit") or {}).get("oid")
            pr_status = (
                f"#{pr_json.get('number')} {pr_json.get('title')} - state={pr_json.get('state')}, "
                f"mergedAt={pr_json.get('mergedAt')}, mergeCommit={merge_commit or 'none'}"
            )
        except ValueError as exc:
            pr_checks.append(CheckResult("Parse PR JSON", False, str(exc)))

    commit_checks: list[CheckResult] = []
    expected = run_command(
        "expected commit reachable",
        ["git", "merge-base", "--is-ancestor", args.expected_commit, "HEAD"],
    )
    commit_checks.append(
        CheckResult(
            f"expected commit {args.expected_commit} reachable from HEAD",
            expected.passed,
            "reachable" if expected.passed else expected.stderr or expected.stdout or f"exit {expected.returncode}",
        )
    )
    merge_commit_oid = (pr_json.get("mergeCommit") or {}).get("oid")
    if merge_commit_oid:
        merge_commit = run_command(
            "merge commit reachable",
            ["git", "merge-base", "--is-ancestor", merge_commit_oid, "HEAD"],
        )
        commit_checks.append(
            CheckResult(
                f"merge commit {merge_commit_oid} reachable from HEAD",
                merge_commit.passed,
                "reachable" if merge_commit.passed else merge_commit.stderr or merge_commit.stdout or f"exit {merge_commit.returncode}",
            )
        )
    else:
        commit_checks.append(CheckResult("merge commit reachable from HEAD", False, "merge commit unavailable from PR JSON"))

    validation_commands: list[CommandResult] = [
        run_command("validate_canonical_66_scope.py", [PY, str(ROOT / "scripts" / "validate_canonical_66_scope.py")]),
        run_command("qa_canonical_corpus.py", [PY, str(ROOT / "scripts" / "qa_canonical_corpus.py")]),
        run_command("validate_all.py", [PY, str(ROOT / "scripts" / "validate_all.py")]),
    ]
    if not args.skip_pytest:
        validation_commands.append(run_command("pytest", [PY, "-m", "pytest", "-q"]))
    validation_commands.append(run_command("git diff --check", ["git", "diff", "--check"]))

    validation_checks: list[CheckResult] = []
    append_command_checks(validation_checks, validation_commands)
    if args.skip_pytest:
        # Surface the skip explicitly so a PASS verdict can never silently hide
        # that the full test gate was not run. passed=True because skipping is an
        # allowed mode, but the report and JSON make the gap unmistakable.
        validation_checks.append(CheckResult("pytest", True, "SKIPPED via --skip-pytest"))
    try:
        validation_checks.append(parse_yaml_files([ROOT / "ROADMAP_STATE.yaml", *all_task_yaml_paths()]))
    except Exception as exc:  # pragma: no cover - reports exact local parse failure
        validation_checks.append(CheckResult("YAML parse checks", False, str(exc)))
    try:
        validation_checks.append(
            parse_jsonl_files(
                [
                    ROOT / ".ai" / "control" / "roadmap_events.jsonl",
                    ROOT / ".ai" / "control" / "handoff_ledger.jsonl",
                ]
            )
        )
    except Exception as exc:  # pragma: no cover - reports exact local parse failure
        validation_checks.append(CheckResult("JSONL parse checks", False, str(exc)))

    all_checks = [*state_checks, *pr_checks, *commit_checks, *validation_checks]
    passed = all(check.passed for check in all_checks)
    main_head = run_command("git rev-parse HEAD", ["git", "rev-parse", "--short", "HEAD"])
    report = {
        "verdict": "PASS" if passed else "FAIL",
        "main_status": f"HEAD={main_head.stdout or 'unknown'}; working tree={status.stdout or 'clean'}",
        "pr_status": pr_status,
        "state_checks": [asdict(check) for check in state_checks],
        "pr_checks": [asdict(check) for check in pr_checks],
        "commit_checks": [asdict(check) for check in commit_checks],
        "validation_checks": [asdict(check) for check in validation_checks],
        "pytest_skipped": bool(args.skip_pytest),
        "next_task": next_task_state(args.next_task),
        "protected_paths": PROTECTED_PATHS,
    }
    return report, 0 if passed else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pr", required=True, type=int, help="Merged GitHub pull request number to verify")
    parser.add_argument("--expected-commit", required=True, help="Short or full commit SHA expected on main")
    parser.add_argument("--next-task", help="Optional next task id to look for in roadmap/control state")
    parser.add_argument("--skip-pytest", action="store_true", help="Skip the full python -m pytest -q gate")
    parser.add_argument("--json", action="store_true", help="Emit the verification report as JSON")
    args = parser.parse_args(argv)

    report, code = build_report(args)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_text_report(report))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
