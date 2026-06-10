"""Behavioral tests for scripts/agent/post_merge_verify.py.

These exercise the verification logic with a fake command runner so future agents
can rely on fail-closed behavior: unmerged PRs, unreachable commits, dirty trees,
and failing validation must all produce a FAIL verdict and a nonzero exit code.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "agent" / "post_merge_verify.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("post_merge_verify", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    # Register before exec so dataclasses (with `from __future__ import annotations`)
    # can resolve the module via sys.modules during class processing.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


pmv = _load_module()


MERGED_PR_JSON = json.dumps(
    {
        "number": 52,
        "title": "example",
        "state": "MERGED",
        "mergedAt": "2026-06-10T21:17:58Z",
        "mergeCommit": {"oid": "abc1234"},
        "statusCheckRollup": [],
    }
)


def _args(**over):
    base = {"pr": 52, "expected_commit": "abc1234", "next_task": None, "skip_pytest": False, "json": False}
    base.update(over)
    return argparse.Namespace(**base)


class FakeRunner:
    """Returns rc 0 for every command unless an override is registered by name."""

    def __init__(self, overrides=None, gh_stdout=MERGED_PR_JSON):
        self.overrides = overrides or {}
        self.gh_stdout = gh_stdout

    def __call__(self, name, command):
        if name == "gh pr view":
            rc, out, err = self.overrides.get(name, (0, self.gh_stdout, ""))
        else:
            rc, out, err = self.overrides.get(name, (0, "", ""))
        return pmv.CommandResult(name=name, command=command, returncode=rc, stdout=out, stderr=err)


def _patch_filesystem_gates(monkeypatch):
    monkeypatch.setattr(pmv, "check_path_absent", lambda path: pmv.CheckResult(str(path), True, "absent"))
    monkeypatch.setattr(pmv, "parse_yaml_files", lambda paths: pmv.CheckResult("YAML parse checks", True, "ok"))
    monkeypatch.setattr(pmv, "parse_jsonl_files", lambda paths: pmv.CheckResult("JSONL parse checks", True, "ok"))


def _run(monkeypatch, runner, args):
    _patch_filesystem_gates(monkeypatch)
    monkeypatch.setattr(pmv, "run_command", runner)
    return pmv.build_report(args)


# --- pure helpers -----------------------------------------------------------


def test_run_command_missing_binary_fails_closed():
    result = pmv.run_command("missing", ["definitely-not-a-real-binary-xyz", "--version"])
    assert result.returncode == 127
    assert result.passed is False
    assert result.stderr == "command not found: definitely-not-a-real-binary-xyz"


def test_mentions_task_is_token_bounded():
    assert pmv.mentions_task("next is T340B today", "T340B") is True
    assert pmv.mentions_task("next is T340B today", "T340") is False
    assert pmv.mentions_task("T340 then T341", "T340") is True


def test_next_task_state_statuses_and_prefix_safety(tmp_path, monkeypatch):
    monkeypatch.setattr(pmv, "ROOT", tmp_path)

    # nothing exists -> not_found
    assert pmv.next_task_state("T123B")["status"] == "not_found"

    # prose-only token mention -> ambiguous
    (tmp_path / "ROADMAP_STATE.yaml").write_text("notes: consider T123B later\n", encoding="utf-8")
    state = pmv.next_task_state("T123B")
    assert state["status"] == "ambiguous"
    assert state["mentioned_in"] == ["ROADMAP_STATE.yaml"]

    # exact task file -> found
    tasks = tmp_path / ".ai" / "tasks"
    tasks.mkdir(parents=True)
    (tasks / "T123B.task.yaml").write_text("id: T123B\n", encoding="utf-8")
    state = pmv.next_task_state("T123B")
    assert state["status"] == "found"
    assert state["task_file_exists"] is True

    # prefix id must not match the suffixed id anywhere
    assert pmv.next_task_state("T123")["status"] == "not_found"

    # detection is report-only and says so
    assert "does not authorize" in state["authorization_note"]


def test_missing_gh_fails_closed_with_clean_report(monkeypatch):
    runner = FakeRunner(overrides={"gh pr view": (127, "", "command not found: gh")})
    report, code = _run(monkeypatch, runner, _args())
    assert code == 1
    assert report["verdict"] == "FAIL"
    gh_checks = [c for c in report["pr_checks"] if c["name"] == "gh pr view"]
    assert gh_checks and not gh_checks[0]["passed"]
    assert "command not found: gh" in gh_checks[0]["detail"]
    # clean report and valid JSON, not a traceback
    assert "Traceback" not in pmv.format_text_report(report)
    json.dumps(report)


def test_status_checks_green_variants():
    assert pmv.status_checks_green([])[0] is True
    failing = [{"__typename": "CheckRun", "name": "validate", "status": "COMPLETED", "conclusion": "FAILURE"}]
    assert pmv.status_checks_green(failing)[0] is False
    passing = [{"__typename": "CheckRun", "name": "validate", "status": "COMPLETED", "conclusion": "SUCCESS"}]
    assert pmv.status_checks_green(passing)[0] is True
    status_fail = [{"__typename": "StatusContext", "context": "ci", "state": "FAILURE"}]
    assert pmv.status_checks_green(status_fail)[0] is False
    unknown = [{"__typename": "MysteryType", "name": "x"}]
    assert pmv.status_checks_green(unknown)[0] is False


def test_parse_pr_json_rejects_non_json_and_non_object():
    with pytest.raises(ValueError):
        pmv.parse_pr_json("not json")
    with pytest.raises(ValueError):
        pmv.parse_pr_json("[1, 2, 3]")


# --- build_report scenarios -------------------------------------------------


def test_build_report_passes_when_everything_green(monkeypatch):
    report, code = _run(monkeypatch, FakeRunner(), _args())
    assert code == 0
    assert report["verdict"] == "PASS"


def test_build_report_fails_closed_on_unmerged_pr(monkeypatch):
    open_pr = json.dumps({"number": 52, "title": "x", "state": "OPEN", "mergedAt": None, "mergeCommit": None, "statusCheckRollup": []})
    report, code = _run(monkeypatch, FakeRunner(gh_stdout=open_pr), _args())
    assert code == 1
    assert report["verdict"] == "FAIL"
    assert any(c["name"] == "PR state is MERGED" and not c["passed"] for c in report["pr_checks"])


def test_build_report_fails_when_expected_commit_unreachable(monkeypatch):
    runner = FakeRunner(overrides={"expected commit reachable": (1, "", "not an ancestor")})
    report, code = _run(monkeypatch, runner, _args())
    assert code == 1
    assert report["verdict"] == "FAIL"
    assert any("reachable from HEAD" in c["name"] and not c["passed"] for c in report["commit_checks"])


def test_build_report_fails_on_dirty_working_tree(monkeypatch):
    runner = FakeRunner(overrides={"git status --short": (0, " M somefile.py", "")})
    report, code = _run(monkeypatch, runner, _args())
    assert code == 1
    assert report["verdict"] == "FAIL"
    assert any(c["name"] == "git status --short clean" and not c["passed"] for c in report["state_checks"])


def test_build_report_fails_when_validation_command_fails(monkeypatch):
    runner = FakeRunner(overrides={"validate_all.py": (1, "", "gate failed")})
    report, code = _run(monkeypatch, runner, _args())
    assert code == 1
    assert report["verdict"] == "FAIL"


def test_build_report_marks_skipped_pytest_explicitly(monkeypatch):
    runner = FakeRunner()
    report, code = _run(monkeypatch, runner, _args(skip_pytest=True))
    assert code == 0
    assert report["pytest_skipped"] is True
    pytest_checks = [c for c in report["validation_checks"] if c["name"] == "pytest"]
    assert len(pytest_checks) == 1
    assert pytest_checks[0]["detail"] == "SKIPPED via --skip-pytest"
    text = pmv.format_text_report(report)
    assert "pytest: SKIPPED via --skip-pytest" in text
    assert "WARNING" in text


def test_pass_verdict_does_not_imply_next_task_authorization(monkeypatch):
    report, code = _run(monkeypatch, FakeRunner(), _args(next_task="T999ZZZ"))
    assert code == 0
    assert report["verdict"] == "PASS"
    # unknown next task does not flip the verdict (report-only) ...
    assert report["next_task"]["status"] == "not_found"
    # ... and the text report states non-authorization explicitly
    text = pmv.format_text_report(report)
    assert "does not authorize the next task" in text


def test_build_report_fails_when_merge_commit_missing(monkeypatch):
    no_merge = json.dumps({"number": 52, "title": "x", "state": "MERGED", "mergedAt": "t", "mergeCommit": None, "statusCheckRollup": []})
    report, code = _run(monkeypatch, FakeRunner(gh_stdout=no_merge), _args())
    assert code == 1
    assert any("merge commit" in c["name"] and not c["passed"] for c in report["commit_checks"])
