#!/usr/bin/env python3
"""Rust-accelerated wrapper for validate_canonical_66_scope.py."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable
DEFAULT_MANIFEST = ROOT / "tools" / "logos_fast_validators" / "Cargo.toml"
DEFAULT_CANON = ROOT / "config" / "canon" / "canonical_66_books.yaml"
PY_VALIDATOR = ROOT / "scripts" / "validate_canonical_66_scope.py"


class RustUnavailable(RuntimeError):
    """Raised when the Rust fast path cannot be invoked in this environment."""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl", nargs="*")
    parser.add_argument("--canon", type=Path, default=DEFAULT_CANON)
    parser.add_argument("--summary-json", type=Path)
    parser.add_argument("--manifest-path", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--cargo-bin", default="cargo")
    parser.add_argument("--python-fallback", action="store_true")
    parser.add_argument("--require-rust", action="store_true")
    parser.add_argument(
        "--compare-python",
        action="store_true",
        help="Run the original Python validator too and fail if verdicts diverge.",
    )
    return parser


def rust_cmd(args: argparse.Namespace) -> list[str]:
    cmd = [
        args.cargo_bin,
        "run",
        "--quiet",
        "--manifest-path",
        str(args.manifest_path),
        "--",
        "canonical-scope",
        "--canon",
        str(args.canon),
    ]
    if args.summary_json is not None:
        cmd.extend(["--summary-json", str(args.summary_json)])
    cmd.extend(str(Path(path)) for path in args.jsonl)
    return cmd


def python_cmd(args: argparse.Namespace) -> list[str]:
    return [PY, str(PY_VALIDATOR), *[str(Path(path)) for path in args.jsonl]]


def run_command(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)


def run_rust(args: argparse.Namespace) -> subprocess.CompletedProcess[str]:
    if not args.manifest_path.exists():
        raise RustUnavailable(f"Rust manifest not found: {args.manifest_path}")
    try:
        return run_command(rust_cmd(args))
    except FileNotFoundError as exc:
        raise RustUnavailable(f"{args.cargo_bin!r} was not found on PATH") from exc


def relay(result: subprocess.CompletedProcess[str]) -> None:
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        rust = run_rust(args)
    except RustUnavailable as exc:
        if args.require_rust or not args.python_fallback:
            print(f"Rust fast canonical-scope validation unavailable: {exc}", file=sys.stderr)
            return 127
        print(f"Rust fast canonical-scope validation unavailable; using Python fallback: {exc}", file=sys.stderr)
        py_result = run_command(python_cmd(args))
        relay(py_result)
        return py_result.returncode

    relay(rust)
    if args.compare_python:
        py_result = run_command(python_cmd(args))
        if py_result.returncode != rust.returncode:
            print("Rust/Python canonical-scope validator parity failed.", file=sys.stderr)
            print(f"- rust exit: {rust.returncode}", file=sys.stderr)
            print(f"- python exit: {py_result.returncode}", file=sys.stderr)
            relay(py_result)
            return 1
        if rust.returncode == 0:
            print("Rust/Python canonical-scope validator parity passed.")
    return rust.returncode


if __name__ == "__main__":
    raise SystemExit(main())
