#!/usr/bin/env python3
"""Fast T423 chunk-map validation wrapper with Rust dispatch and Python fallback."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = ROOT / "tools" / "logos_fast_validators" / "Cargo.toml"
DEFAULT_CANON = ROOT / "config" / "canon" / "canonical_66_books.yaml"


def resolve_chunk_map_path(path: Path) -> Path:
    if path.is_dir():
        return path / "whole_bible_chunk_map.jsonl"
    return path


def infer_model_id(path: Path) -> str | None:
    model_root = path if path.is_dir() else path.parent
    manifest = model_root / "model_manifest.yaml"
    if not manifest.is_file():
        return None
    data: Any = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    if isinstance(data, dict) and data.get("model_id"):
        return str(data["model_id"])
    return None


def rust_command(args: argparse.Namespace, chunk_map_path: Path) -> list[str]:
    cmd = [
        args.cargo_bin,
        "run",
        "--quiet",
        "--manifest-path",
        str(args.manifest_path),
        "--",
        "chunk-map",
        "--canon",
        str(args.canon),
    ]
    if args.model_id:
        cmd.extend(["--model-id", args.model_id])
    if args.require_full_bible:
        cmd.append("--require-full-bible")
    for book in args.books:
        cmd.extend(["--book", book])
    if args.summary_json:
        cmd.extend(["--summary-json", str(args.summary_json)])
    cmd.append(str(chunk_map_path))
    return cmd


def python_command(args: argparse.Namespace, original_path: Path) -> list[str]:
    cmd = [
        sys.executable,
        "-m",
        "scripts.validate_whole_bible_chunk_map",
        str(original_path),
    ]
    if args.model_id:
        cmd.extend(["--model-id", args.model_id])
    if args.require_full_bible:
        cmd.append("--require-full-bible")
    for book in args.books:
        cmd.extend(["--book", book])
    return cmd


def relay(result: subprocess.CompletedProcess[str]) -> None:
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)


def run_command(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="whole_bible_chunk_map.jsonl or model folder")
    parser.add_argument("--model-id")
    parser.add_argument("--require-full-bible", action="store_true")
    parser.add_argument("--book", action="append", dest="books", default=[])
    parser.add_argument("--canon", type=Path, default=DEFAULT_CANON)
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

    original_path = args.path
    chunk_map_path = resolve_chunk_map_path(original_path)
    if not args.model_id:
        args.model_id = infer_model_id(original_path)

    if (args.python_fallback or args.compare_python) and args.canon.resolve() != DEFAULT_CANON.resolve():
        print(
            "Custom --canon is not supported with Python fallback/compare because "
            "scripts/validate_whole_bible_chunk_map.py uses the repo default canon config.",
            file=sys.stderr,
        )
        return 1

    if not args.manifest_path.exists():
        if args.require_rust:
            print(f"Missing Rust manifest: {args.manifest_path}", file=sys.stderr)
            return 1
        if args.python_fallback:
            print("Rust fast chunk-map validator unavailable; using Python fallback.", file=sys.stderr)
            result = run_command(python_command(args, original_path))
            relay(result)
            return result.returncode
        print(f"Missing Rust manifest: {args.manifest_path}", file=sys.stderr)
        return 1

    try:
        rust_result = run_command(rust_command(args, chunk_map_path))
    except FileNotFoundError:
        if args.require_rust:
            print(f"Rust cargo binary not found: {args.cargo_bin}", file=sys.stderr)
            return 1
        if args.python_fallback:
            print("Rust cargo binary unavailable; using Python fallback.", file=sys.stderr)
            result = run_command(python_command(args, original_path))
            relay(result)
            return result.returncode
        print(f"Rust cargo binary not found: {args.cargo_bin}", file=sys.stderr)
        return 1

    relay(rust_result)
    if args.compare_python:
        python_result = run_command(python_command(args, original_path))
        if (rust_result.returncode == 0) != (python_result.returncode == 0):
            print("Rust/Python chunk-map validator verdict mismatch.", file=sys.stderr)
            print("--- Python stdout ---", file=sys.stderr)
            print(python_result.stdout, file=sys.stderr)
            print("--- Python stderr ---", file=sys.stderr)
            print(python_result.stderr, file=sys.stderr)
            return 1
        print("Rust/Python chunk-map validator verdict parity passed.")
    return rust_result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
