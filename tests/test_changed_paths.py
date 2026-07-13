from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from logos_validation import changed_paths as changed_paths_module
from logos_validation.changed_paths import PROFILE_LAYERS, get_changed_paths, parity_log_line

ROOT = Path(__file__).resolve().parent.parent
GOLDEN = ROOT / "tests/fixtures/changed_paths/golden-success.json"


def git(repo: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        capture_output=True,
        check=False,
    )
    if check and result.returncode:
        raise AssertionError(f"git {' '.join(args)} failed: {result.stderr}")
    return result.stdout.strip()


def write(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def commit(repo: Path, message: str) -> str:
    git(repo, "add", "-A")
    git(repo, "commit", "-m", message)
    return git(repo, "rev-parse", "HEAD")


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    target = tmp_path / "repo"
    target.mkdir()
    git(target, "init", "-b", "main")
    git(target, "config", "user.name", "Changed Paths Test")
    git(target, "config", "user.email", "changed-paths@example.invalid")
    write(target / "tracked.txt", "base\n")
    commit(target, "base")
    return target


@pytest.fixture
def layered_repo(repo: Path) -> Path:
    git(repo, "checkout", "-b", "feature")
    write(repo / "committed.txt", "committed\n")
    commit(repo, "feature commit")
    write(repo / "staged.txt", "staged\n")
    git(repo, "add", "staged.txt")
    write(repo / "tracked.txt", "unstaged\n")
    write(repo / "untracked.txt", "untracked\n")
    return repo


def local_result(repo: Path, profile: str = "local-full", **kwargs):
    return get_changed_paths(
        profile,
        "main",
        repo=repo,
        fetch=False,
        allow_stale=True,
        **kwargs,
    )


def test_four_layers_and_golden_contract(layered_repo: Path):
    result = local_result(layered_repo)
    assert result.ok
    actual = result.to_dict()
    actual["base"]["resolved_sha"] = "<sha>"
    actual["head_sha"] = "<sha>"
    expected = json.loads(GOLDEN.read_text(encoding="utf-8"))
    assert actual == expected


@pytest.mark.parametrize("profile", sorted(PROFILE_LAYERS))
def test_union_is_exact_union_of_profile_layers(layered_repo: Path, profile: str):
    result = local_result(layered_repo, profile)
    assert result.ok
    expected = sorted({path for layer in PROFILE_LAYERS[profile] for path in result.layers[layer]})
    assert result.union == expected


def test_ci_union_excludes_local_dirt(layered_repo: Path):
    result = local_result(layered_repo, "ci")
    assert result.union == ["committed.txt"]
    assert result.layers["untracked"] == ["untracked.txt"]


def test_parity_log_helper_is_deterministic_and_write_free(layered_repo: Path):
    result = local_result(layered_repo, "ci")
    line = parity_log_line("example-consumer", ["legacy-only.txt", "committed.txt"], result)
    payload = json.loads(line)
    assert line.endswith("\n")
    assert payload["schema_version"] == "changed-paths-parity.v1"
    assert payload["legacy_paths"] == ["committed.txt", "legacy-only.txt"]
    assert payload["engine_paths"] == ["committed.txt"]
    assert payload["only_legacy"] == ["legacy-only.txt"]
    assert payload["only_engine"] == []
    assert payload["matches"] is False
    assert not (layered_repo / "build/runtime_tmp/changed-paths-parity.jsonl").exists()


def test_parity_log_refuses_unnamed_consumer(layered_repo: Path):
    with pytest.raises(ValueError, match="consumer must be non-empty"):
        parity_log_line(" ", [], local_result(layered_repo, "ci"))


def test_staged_layer_uses_merge_base_not_stale_head(layered_repo: Path):
    legacy = git(layered_repo, "diff", "--cached", "--name-only", "HEAD").splitlines()
    assert legacy == ["staged.txt"]
    result = local_result(layered_repo, "pre-commit")
    assert result.layers["staged"] == ["committed.txt", "staged.txt"]


def test_rename_surfaces_both_paths_and_mapping(repo: Path):
    git(repo, "checkout", "-b", "rename")
    git(repo, "mv", "tracked.txt", "renamed.txt")
    commit(repo, "rename")
    result = local_result(repo, "ci")
    assert result.union == ["renamed.txt", "tracked.txt"]
    assert [item.to_dict() for item in result.renames] == [{"from": "tracked.txt", "to": "renamed.txt"}]


def test_stacked_branch_override_is_echoed(repo: Path):
    git(repo, "checkout", "-b", "stack-parent")
    write(repo / "parent.txt", "parent\n")
    commit(repo, "parent")
    git(repo, "checkout", "-b", "stack-child")
    write(repo / "child.txt", "child\n")
    commit(repo, "child")
    result = get_changed_paths("ci", "stack-parent", repo=repo, fetch=False, allow_stale=True)
    assert result.ok
    assert result.base["requested"] == "stack-parent"
    assert result.base["method"] == "override"
    assert result.union == ["child.txt"]


def test_local_slash_base_is_not_mistaken_for_remote(repo: Path, tmp_path: Path):
    remote = tmp_path / "origin.git"
    git(tmp_path, "init", "--bare", str(remote))
    git(repo, "remote", "add", "origin", str(remote))
    git(repo, "push", "origin", "main")
    git(repo, "checkout", "-b", "stack/parent")
    write(repo / "parent.txt", "parent\n")
    commit(repo, "parent")
    git(repo, "checkout", "-b", "stack/child")
    write(repo / "child.txt", "child\n")
    commit(repo, "child")
    result = get_changed_paths("ci", "stack/parent", repo=repo)
    assert result.ok, result.to_dict()
    assert result.base["method"] == "override"
    assert result.union == ["child.txt"]


def test_task_scope_classifies_only_dirty_paths(layered_repo: Path):
    result = local_result(layered_repo, "task-scope", scope_paths=["staged.txt", "tracked.txt"])
    assert result.ok
    assert result.out_of_scope_dirty == ["untracked.txt"]


def test_missing_scope_rules_are_explicit(layered_repo: Path):
    result = local_result(layered_repo, "task-scope")
    assert "scope paths not provided; out_of_scope_dirty was not classified" in result.warnings


def test_no_fetch_requires_explicit_stale_permission(repo: Path):
    result = get_changed_paths("ci", "main", repo=repo, fetch=False)
    assert not result.ok
    assert result.fail.code == "CP-STALE-NOT-ALLOWED"


def test_missing_base_fails_closed(repo: Path):
    result = get_changed_paths("ci", "missing", repo=repo, fetch=False, allow_stale=True)
    assert not result.ok
    assert result.fail.code == "CP-AMBIGUOUS-BASE"
    assert result.union == []


def test_same_named_branch_and_tag_is_ambiguous(repo: Path):
    git(repo, "branch", "collision")
    git(repo, "tag", "collision")
    result = get_changed_paths("ci", "collision", repo=repo, fetch=False, allow_stale=True)
    assert not result.ok
    assert result.fail.code == "CP-AMBIGUOUS-BASE"


@pytest.mark.parametrize("base", ["--help", "bad\nref", "bad\rref"])
def test_option_like_or_control_character_base_fails_before_git(repo: Path, base: str):
    result = get_changed_paths("ci", base, repo=repo, fetch=False, allow_stale=True)
    assert not result.ok
    assert result.fail.code == "CP-AMBIGUOUS-BASE"


def test_head_is_resolved_fresh_each_invocation(repo: Path):
    git(repo, "checkout", "-b", "feature")
    write(repo / "one.txt", "one\n")
    commit(repo, "one")
    first = local_result(repo, "ci")
    write(repo / "two.txt", "two\n")
    commit(repo, "two")
    second = local_result(repo, "ci")
    assert first.head_sha != second.head_sha
    assert second.union == ["one.txt", "two.txt"]


def test_merge_base_is_resolved_again_after_rebase(repo: Path):
    git(repo, "checkout", "-b", "feature")
    write(repo / "feature.txt", "feature\n")
    before_rebase = commit(repo, "feature")
    git(repo, "checkout", "main")
    write(repo / "main.txt", "main\n")
    commit(repo, "main advances")
    git(repo, "checkout", "feature")
    git(repo, "rebase", "main")
    result = local_result(repo, "ci")
    assert result.ok
    assert result.head_sha != before_rebase
    assert result.base["resolved_sha"] == git(repo, "rev-parse", "main")
    assert result.union == ["feature.txt"]


def test_cli_json_and_schema(layered_repo: Path):
    command = [
        sys.executable,
        "-m",
        "logos_validation.changed_paths",
        "--repo",
        str(layered_repo),
        "--profile",
        "local-full",
        "--base",
        "main",
        "--no-fetch",
        "--allow-stale",
    ]
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["engine_version"] == 1
    jsonschema = pytest.importorskip("jsonschema")
    schema = json.loads((ROOT / "schemas/changed-paths-output.schema.json").read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(payload)


def test_cli_failure_is_json_and_exit_two(repo: Path):
    command = [
        sys.executable,
        "-m",
        "logos_validation.changed_paths",
        "--repo",
        str(repo),
        "--profile",
        "ci",
        "--base",
        "missing",
        "--no-fetch",
        "--allow-stale",
    ]
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    assert result.returncode == 2
    assert json.loads(result.stdout)["fail"]["code"] == "CP-AMBIGUOUS-BASE"


def test_cli_null_separated_preserves_spaces(repo: Path):
    git(repo, "checkout", "-b", "feature")
    write(repo / "space name.txt", "value\n")
    commit(repo, "space path")
    command = [
        sys.executable,
        "-m",
        "logos_validation.changed_paths",
        "--repo",
        str(repo),
        "--profile",
        "ci",
        "--base",
        "main",
        "--no-fetch",
        "--allow-stale",
        "--null-separated",
    ]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, check=False)
    assert result.returncode == 0
    assert result.stdout == b"space name.txt\0"


def _build_shallow_remote(tmp_path: Path) -> Path:
    source = tmp_path / "source"
    source.mkdir()
    git(source, "init", "-b", "main")
    git(source, "config", "user.name", "Changed Paths Test")
    git(source, "config", "user.email", "changed-paths@example.invalid")
    write(source / "base.txt", "0\n")
    base_sha = commit(source, "base")
    for index in range(1, 6):
        write(source / "base.txt", f"{index}\n")
        commit(source, f"main {index}")
    git(source, "checkout", "-b", "feature", base_sha)
    write(source / "feature.txt", "feature\n")
    commit(source, "feature")
    bare = tmp_path / "remote.git"
    git(tmp_path, "clone", "--bare", str(source), str(bare))
    return bare


@pytest.fixture(scope="module")
def shallow_remote(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return _build_shallow_remote(tmp_path_factory.mktemp("changed-paths-shallow-remote"))


def test_shallow_clone_deepens_until_merge_base(
    tmp_path: Path,
    shallow_remote: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    shallow = tmp_path / "shallow"
    url = shallow_remote.resolve().as_uri()
    git(tmp_path, "clone", "--depth", "1", "--branch", "feature", url, str(shallow))
    fetches: list[dict[str, object]] = []
    real_fetch_base = changed_paths_module._fetch_base

    def record_fetch(*args, **kwargs):
        fetches.append(dict(kwargs))
        return real_fetch_base(*args, **kwargs)

    monkeypatch.setattr(changed_paths_module, "_fetch_base", record_fetch)
    result = get_changed_paths("ci", repo=shallow, deepen_by=10, deepen_rounds=2)
    assert result.ok, result.to_dict()
    assert result.base["method"] == "deepened"
    assert result.union == ["feature.txt"]
    assert git(shallow, "cat-file", "-e", "HEAD^") == ""
    assert any(
        call.get("deepen_by") == 10 and call.get("head_sha") == result.head_sha
        for call in fetches
    )


def test_shallow_clone_exhaustion_fails_closed(tmp_path: Path, shallow_remote: Path):
    shallow = tmp_path / "shallow-exhausted"
    url = shallow_remote.resolve().as_uri()
    git(tmp_path, "clone", "--depth", "1", "--branch", "feature", url, str(shallow))
    result = get_changed_paths("ci", repo=shallow, deepen_rounds=0)
    assert not result.ok
    assert result.fail.code == "CP-NO-MERGE-BASE"
