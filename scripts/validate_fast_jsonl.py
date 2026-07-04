#!/usr/bin/env python3
"""Fast JSONL validation wrapper with Rust dispatch and Python fallback."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = ROOT / "tools" / "logos_fast_validators" / "Cargo.toml"


def rust_command(args: argparse.Namespace) -> list[str]:
    cmd = [
        args.cargo_bin,
        "run",
        "--quiet",
        "--manifest-path",
        str(args.manifest_path),
        "--",
        "jsonl-scan",
        "--translation-id",
        args.translation_id,
    ]
    if args.require_canon:
        cmd.append("--require-canon")
    if args.summary_json:
        cmd.extend(["--summary-json", str(args.summary_json)])
    cmd.extend(str(Path(path)) for path in args.paths)
    return cmd


def python_command(args: argparse.Namespace) -> list[str]:
    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "validate_jsonl.py"),
        "--translation-id",
        args.translation_id,
    ]
    if args.require_canon:
        cmd.append("--require-canon")
    cmd.extend(str(Path(path)) for path in args.paths)
    return cmd


def relay(result: subprocess.CompletedProcess[str]) -> None:
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)


def run_command(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--translation-id", default="eng-web")
    parser.add_argument("--require-canon", action="store_true")
    parser.add_argument("--summary-json", type=Path)
    parser.add_argument("--manifest-path", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--cargo-bin", default="cargo")
    parser.add_argument("--python-fallback", action="store_true")
    parser.add_argument("--require-rust", action="store_true")
    parser.add_argument(
        "--compare-python",
        action="store_true",
        help="Run the Python validator too and fail if Rust/Python verdicts diverge.",
    )
    args = parser.parse_args(argv)

    if not args.manifest_path.exists():
        if args.require_rust:
            print(f"Missing Rust manifest: {args.manifest_path}", file=sys.stderr)
            return 1
        if args.python_fallback:
            print("Rust fast JSONL validator unavailable; using Python fallback.", file=sys.stderr)
            result = run_command(python_command(args))
            relay(result)
            return result.returncode
        print(f"Missing Rust manifest: {args.manifest_path}", file=sys.stderr)
        return 1

    try:
        rust_result = run_command(rust_command(args))
    except FileNotFoundError:
        if args.require_rust:
            print(f"Rust cargo binary not found: {args.cargo_bin}", file=sys.stderr)
            return 1
        if args.python_fallback:
            print("Rust cargo binary unavailable; using Python fallback.", file=sys.stderr)
            result = run_command(python_command(args))
            relay(result)
            return result.returncode
        print(f"Rust cargo binary not found: {args.cargo_bin}", file=sys.stderr)
        return 1

    relay(rust_result)
    if args.compare_python:
        python_result = run_command(python_command(args))
        if (rust_result.returncode == 0) != (python_result.returncode == 0):
            print("Rust/Python JSONL validator verdict mismatch.", file=sys.stderr)
            print("--- Python stdout ---", file=sys.stderr)
            print(python_result.stdout, file=sys.stderr)
            print("--- Python stderr ---", file=sys.stderr)
            print(python_result.stderr, file=sys.stderr)
            return 1
        print("Rust/Python JSONL validator verdict parity passed.")
    return rust_result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
