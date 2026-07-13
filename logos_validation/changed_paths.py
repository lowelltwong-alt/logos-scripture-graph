"""Canonical, fail-closed Git changed-path discovery.

This module is additive in LSG-O2A: existing consumers keep their legacy logic
until later shadow/parity migrations explicitly adopt this engine.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from fnmatch import fnmatch
from pathlib import Path
from typing import Iterable, Sequence

ENGINE_VERSION = 1
DEFAULT_BASE = "origin/main"
DEFAULT_DEEPEN_BY = 200
DEFAULT_DEEPEN_ROUNDS = 3

PROFILE_LAYERS = {
    "ci": ("committed",),
    "pre-commit": ("committed", "staged"),
    "task-scope": ("committed", "staged", "unstaged", "untracked"),
    "local-full": ("committed", "staged", "unstaged", "untracked"),
}


@dataclass(frozen=True, order=True)
class Rename:
    """A rename or copy reported by Git."""

    from_path: str
    to_path: str

    def to_dict(self) -> dict[str, str]:
        return {"from": self.from_path, "to": self.to_path}


@dataclass(frozen=True)
class Failure:
    """Machine-readable fail-closed result."""

    code: str
    message: str


@dataclass
class ChangedPaths:
    """Versioned result returned by the engine and serialized by the CLI."""

    profile: str
    base: dict[str, str | None]
    head_sha: str | None
    fetched: bool
    layers: dict[str, list[str]] = field(
        default_factory=lambda: {
            "committed": [],
            "staged": [],
            "unstaged": [],
            "untracked": [],
        }
    )
    renames: list[Rename] = field(default_factory=list)
    union: list[str] = field(default_factory=list)
    out_of_scope_dirty: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    fail: Failure | None = None
    engine_version: int = ENGINE_VERSION

    @property
    def ok(self) -> bool:
        return self.fail is None

    def to_dict(self) -> dict[str, object]:
        value = asdict(self)
        value["renames"] = [rename.to_dict() for rename in self.renames]
        return value


def parity_log_line(consumer: str, legacy_paths: Iterable[str], result: ChangedPaths) -> str:
    """Return one deterministic JSONL shadow-parity record without writing it.

    LSG-O2B consumers may append this line to their task-local parity log while
    both legacy and engine paths are active. LSG-O2A itself has no consumers.
    """

    if not consumer.strip():
        raise ValueError("consumer must be non-empty")
    legacy = sorted({path.replace("\\", "/") for path in legacy_paths if path})
    engine = sorted(set(result.union))
    failure = asdict(result.fail) if result.fail is not None else None
    record = {
        "schema_version": "changed-paths-parity.v1",
        "consumer": consumer,
        "engine_version": result.engine_version,
        "profile": result.profile,
        "base_requested": result.base.get("requested"),
        "base_sha": result.base.get("resolved_sha"),
        "head_sha": result.head_sha,
        "engine_fail": failure,
        "legacy_paths": legacy,
        "engine_paths": engine,
        "only_legacy": sorted(set(legacy) - set(engine)),
        "only_engine": sorted(set(engine) - set(legacy)),
        "matches": failure is None and legacy == engine,
    }
    return json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n"


class GitCommandError(RuntimeError):
    """Internal Git command failure with safe diagnostics."""

    def __init__(self, args: Sequence[str], stderr: str, returncode: int):
        self.args_run = tuple(args)
        self.stderr = stderr.strip()
        self.returncode = returncode
        detail = self.stderr or f"git exited {returncode}"
        super().__init__(f"git {' '.join(args)}: {detail}")


def _failure(profile: str, base: str, code: str, message: str, *, fetched: bool = False) -> ChangedPaths:
    return ChangedPaths(
        profile=profile,
        base={"requested": base, "resolved_sha": None, "method": None},
        head_sha=None,
        fetched=fetched,
        fail=Failure(code=code, message=message),
    )


def _git(repo: Path, args: Sequence[str], *, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except (FileNotFoundError, OSError) as exc:
        raise GitCommandError(args, str(exc), 127) from exc
    if check and result.returncode != 0:
        raise GitCommandError(args, result.stderr.decode("utf-8", errors="replace"), result.returncode)
    return result


def _text(result: subprocess.CompletedProcess[bytes]) -> str:
    return result.stdout.decode("utf-8", errors="replace").strip()


def _rev_parse(repo: Path, ref: str) -> str | None:
    result = _git(repo, ["rev-parse", "--verify", f"{ref}^{{commit}}"], check=False)
    stderr = result.stderr.decode("utf-8", errors="replace").lower()
    if result.returncode != 0 or "ambiguous" in stderr:
        return None
    value = _text(result)
    return value if len(value) == 40 else None


def _merge_base(repo: Path, base: str) -> str | None:
    result = _git(repo, ["merge-base", base, "HEAD"], check=False)
    if result.returncode != 0:
        return None
    value = _text(result)
    return value if len(value) == 40 else None


def _remote_and_branch(repo: Path, base: str) -> tuple[str, str] | None:
    if "/" not in base or base.startswith("refs/"):
        return None
    remote, branch = base.split("/", 1)
    if not remote or not branch:
        return None
    remotes = set(_text(_git(repo, ["remote"], check=False)).splitlines())
    if remote not in remotes:
        return None
    if _git(repo, ["check-ref-format", f"refs/heads/{branch}"], check=False).returncode != 0:
        return None
    return remote, branch


def _fetch_base(
    repo: Path,
    base: str,
    *,
    deepen_by: int | None = None,
    head_sha: str | None = None,
) -> None:
    remote_branch = _remote_and_branch(repo, base)
    if remote_branch is None:
        remote_branch = ("origin", "main")
    remote, branch = remote_branch
    args = ["fetch", "--quiet"]
    if deepen_by is not None:
        args.append(f"--deepen={deepen_by}")
    refspec = f"+refs/heads/{branch}:refs/remotes/{remote}/{branch}"
    args.extend([remote, refspec])
    if head_sha is not None:
        # An explicit base refspec fetches only that ref. Request the exact,
        # already-validated HEAD object too so newer Git versions deepen both
        # sides of a prospective merge base without guessing a branch name or
        # creating a temporary local ref.
        args.append(head_sha)
    _git(repo, args)


def _parse_name_status(raw: bytes) -> tuple[list[str], list[Rename]]:
    tokens = [token.decode("utf-8") for token in raw.split(b"\0") if token]
    paths: list[str] = []
    renames: list[Rename] = []
    index = 0
    while index < len(tokens):
        status = tokens[index]
        index += 1
        if status.startswith(("R", "C")):
            if index + 1 >= len(tokens):
                raise ValueError(f"malformed name-status stream after {status}")
            source, target = tokens[index], tokens[index + 1]
            index += 2
            paths.extend((source, target))
            renames.append(Rename(source, target))
        else:
            if index >= len(tokens):
                raise ValueError(f"malformed name-status stream after {status}")
            paths.append(tokens[index])
            index += 1
    return sorted(set(paths)), sorted(set(renames))


def _diff(repo: Path, args: Sequence[str]) -> tuple[list[str], list[Rename]]:
    result = _git(repo, ["diff", "--name-status", "-z", "--find-renames", *args])
    try:
        return _parse_name_status(result.stdout)
    except ValueError as exc:
        raise GitCommandError(["diff", *args], str(exc), 2) from exc


def _untracked(repo: Path) -> list[str]:
    result = _git(repo, ["ls-files", "--others", "--exclude-standard", "-z"])
    try:
        return sorted({token.decode("utf-8") for token in result.stdout.split(b"\0") if token})
    except UnicodeDecodeError as exc:
        raise GitCommandError(["ls-files", "--others"], f"path is not valid UTF-8: {exc}", 2) from exc


def _base_request_is_safe(base: str) -> bool:
    return bool(base) and not base.startswith("-") and not any(character in base for character in "\0\r\n")


def _matches_scope(path: str, rules: Iterable[str]) -> bool:
    normalized = path.replace("\\", "/")
    for raw_rule in rules:
        rule = raw_rule.replace("\\", "/").removeprefix("./")
        if "*" in rule and fnmatch(normalized, rule):
            return True
        if rule.endswith("/") and normalized.startswith(rule):
            return True
        if normalized == rule:
            return True
    return False


def get_changed_paths(
    profile: str,
    base: str | None = None,
    *,
    repo: str | Path = ".",
    fetch: bool = True,
    allow_stale: bool = False,
    scope_paths: Iterable[str] | None = None,
    deepen_by: int = DEFAULT_DEEPEN_BY,
    deepen_rounds: int = DEFAULT_DEEPEN_ROUNDS,
) -> ChangedPaths:
    """Compute four independent Git layers and compose a named profile.

    A non-null ``result.fail`` is a validation failure. Callers must not treat it
    as an empty changed set.
    """

    requested_base = base or DEFAULT_BASE
    if profile not in PROFILE_LAYERS:
        return _failure(profile, requested_base, "CP-UNKNOWN-PROFILE", f"unknown profile: {profile}")
    if not _base_request_is_safe(requested_base):
        return _failure(
            profile,
            requested_base,
            "CP-AMBIGUOUS-BASE",
            "base ref is empty, option-like, or contains control characters",
        )
    if not fetch and not allow_stale:
        return _failure(
            profile,
            requested_base,
            "CP-STALE-NOT-ALLOWED",
            "--no-fetch requires explicit --allow-stale",
        )
    if deepen_by <= 0 or deepen_rounds < 0:
        return _failure(profile, requested_base, "CP-INVALID-OPTION", "deepen values must be non-negative")

    repo_path = Path(repo).resolve()
    warnings: list[str] = []
    fetched = False
    try:
        if _git(repo_path, ["rev-parse", "--is-inside-work-tree"], check=False).returncode != 0:
            return _failure(profile, requested_base, "CP-NOT-A-REPOSITORY", f"not a Git repository: {repo_path}")

        if fetch:
            try:
                _fetch_base(repo_path, requested_base)
                fetched = True
            except GitCommandError as exc:
                return _failure(profile, requested_base, "CP-FETCH-FAILED", str(exc))
        else:
            warnings.append("base ref was not fetched; stale resolution explicitly allowed")

        if _rev_parse(repo_path, requested_base) is None:
            return _failure(
                profile,
                requested_base,
                "CP-AMBIGUOUS-BASE",
                f"base ref is missing or ambiguous: {requested_base}",
                fetched=fetched,
            )

        head_sha = _rev_parse(repo_path, "HEAD")
        if head_sha is None:
            return _failure(profile, requested_base, "CP-GIT-ERROR", "HEAD is not a commit", fetched=fetched)

        merge_base = _merge_base(repo_path, requested_base)
        method = "override" if requested_base != DEFAULT_BASE else "merge-base"
        if merge_base is None:
            shallow = _text(_git(repo_path, ["rev-parse", "--is-shallow-repository"], check=False)) == "true"
            if shallow and fetch:
                for _ in range(deepen_rounds):
                    try:
                        _fetch_base(
                            repo_path,
                            requested_base,
                            deepen_by=deepen_by,
                            head_sha=head_sha,
                        )
                    except GitCommandError:
                        break
                    merge_base = _merge_base(repo_path, requested_base)
                    if merge_base is not None:
                        method = "deepened"
                        break
            if merge_base is None:
                return ChangedPaths(
                    profile=profile,
                    base={"requested": requested_base, "resolved_sha": None, "method": None},
                    head_sha=head_sha,
                    fetched=fetched,
                    warnings=warnings,
                    fail=Failure("CP-NO-MERGE-BASE", f"no merge-base for {requested_base} and HEAD"),
                )

        committed, committed_renames = _diff(repo_path, [f"{merge_base}..HEAD"])
        staged, staged_renames = _diff(repo_path, ["--cached", merge_base])
        unstaged, unstaged_renames = _diff(repo_path, [])
        untracked = _untracked(repo_path)
        layers = {
            "committed": committed,
            "staged": staged,
            "unstaged": unstaged,
            "untracked": untracked,
        }
        selected = PROFILE_LAYERS[profile]
        union = sorted({path for layer in selected for path in layers[layer]})
        renames = sorted(set(committed_renames + staged_renames + unstaged_renames))

        out_of_scope_dirty: list[str] = []
        if profile == "task-scope":
            if scope_paths is None:
                warnings.append("scope paths not provided; out_of_scope_dirty was not classified")
            else:
                index_vs_head, _ = _diff(repo_path, ["--cached", "HEAD"])
                dirty = sorted(set(index_vs_head + unstaged + untracked))
                rules = tuple(scope_paths)
                out_of_scope_dirty = [path for path in dirty if not _matches_scope(path, rules)]

        return ChangedPaths(
            profile=profile,
            base={"requested": requested_base, "resolved_sha": merge_base, "method": method},
            head_sha=head_sha,
            fetched=fetched,
            layers=layers,
            renames=renames,
            union=union,
            out_of_scope_dirty=out_of_scope_dirty,
            warnings=warnings,
        )
    except GitCommandError as exc:
        return _failure(profile, requested_base, "CP-GIT-ERROR", str(exc), fetched=fetched)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", required=True, choices=sorted(PROFILE_LAYERS))
    parser.add_argument("--base", default=None)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    output = parser.add_mutually_exclusive_group()
    output.add_argument("--json", action="store_true", help="emit the versioned JSON contract (default)")
    output.add_argument("--null-separated", action="store_true", help="emit successful union paths separated by NUL")
    parser.add_argument("--no-fetch", action="store_true")
    parser.add_argument("--allow-stale", action="store_true")
    parser.add_argument("--scope", action="append", default=None, help="allowed task-scope path or prefix; repeatable")
    parser.add_argument("--deepen-by", type=int, default=DEFAULT_DEEPEN_BY)
    parser.add_argument("--deepen-rounds", type=int, default=DEFAULT_DEEPEN_ROUNDS)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    result = get_changed_paths(
        args.profile,
        args.base,
        repo=args.repo,
        fetch=not args.no_fetch,
        allow_stale=args.allow_stale,
        scope_paths=args.scope,
        deepen_by=args.deepen_by,
        deepen_rounds=args.deepen_rounds,
    )
    if args.null_separated and result.ok:
        sys.stdout.buffer.write(b"\0".join(path.encode("utf-8") for path in result.union))
        if result.union:
            sys.stdout.buffer.write(b"\0")
    else:
        print(json.dumps(result.to_dict(), sort_keys=True, separators=(",", ":")))
    return 0 if result.ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
