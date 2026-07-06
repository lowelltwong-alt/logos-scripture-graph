#!/usr/bin/env python3
"""Fast word-token evidence-signal scan wrapper with Rust dispatch and Python fallback."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = ROOT / "tools" / "logos_fast_validators" / "Cargo.toml"


def rust_command(args: argparse.Namespace, summary_json: Path | None = None) -> list[str]:
    cmd = [
        args.cargo_bin,
        "run",
        "--quiet",
        "--manifest-path",
        str(args.manifest_path),
        "--",
        "word-token-signals",
        "--translation-id",
        args.translation_id,
    ]
    if summary_json is not None:
        cmd.extend(["--summary-json", str(summary_json)])
    elif args.summary_json:
        cmd.extend(["--summary-json", str(args.summary_json)])
    cmd.extend(str(Path(path)) for path in args.paths)
    return cmd


def relay(result: subprocess.CompletedProcess[str]) -> None:
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)


def run_command(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


def _strong_values(value: Any) -> list[str]:
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    if isinstance(value, list):
        values: list[str] = []
        for item in value:
            values.extend(_strong_values(item))
        return values
    return []


def _record_book(record: dict[str, Any]) -> str:
    value = str(record.get("book") or "")
    if value:
        return value.split(".", 1)[0]
    osis_ref = str(record.get("osis_ref") or "")
    return osis_ref.split(".", 1)[0] if osis_ref else ""


def build_python_summary(paths: list[Path], translation_id: str) -> tuple[dict[str, Any], list[str]]:
    failures: list[str] = []
    records = 0
    source_files: set[str] = set()
    translation_ids: set[str] = set()
    book_token_counts: Counter[str] = Counter()
    book_wj_token_counts: Counter[str] = Counter()
    books_with_wj: set[str] = set()
    wj_word_tokens = 0
    wj_token_runs = 0
    in_wj_run = False
    current_wj_book = ""
    tokens_with_strong = 0
    tokens_with_surface_text = 0
    tokens_with_nesting_context = 0
    strong_occurrences_total = 0
    strong_h_occurrences = 0
    strong_g_occurrences = 0
    strong_other_occurrences = 0

    for path in paths:
        if not path.is_file():
            failures.append(f"Missing word-token JSONL file: {path}")
            continue
        with path.open(encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as exc:
                    failures.append(f"{path}:{line_no}: invalid JSON: {exc}")
                    continue
                if not isinstance(record, dict):
                    failures.append(f"{path}:{line_no}: JSONL row is not an object")
                    continue
                records += 1
                actual_translation = str(record.get("translation_id") or "")
                if not actual_translation:
                    failures.append(f"{path}:{line_no}: missing translation_id")
                else:
                    translation_ids.add(actual_translation)
                    if actual_translation != translation_id:
                        failures.append(
                            f"{path}:{line_no}: translation_id {actual_translation} != expected {translation_id}"
                        )
                book = _record_book(record)
                if not book:
                    failures.append(f"{path}:{line_no}: missing book identity")
                else:
                    book_token_counts[book] += 1
                osis_ref = str(record.get("osis_ref") or "")
                if osis_ref.count(".") != 2:
                    failures.append(f"{path}:{line_no}: missing or malformed osis_ref")
                source_file = str(record.get("source_file") or "")
                if source_file:
                    source_files.add(source_file)
                if str(record.get("surface_text") or ""):
                    tokens_with_surface_text += 1
                nesting_context = record.get("nesting_context")
                if isinstance(nesting_context, list) and nesting_context:
                    tokens_with_nesting_context += 1
                is_wj = isinstance(nesting_context, list) and "wj" in nesting_context
                if is_wj:
                    wj_word_tokens += 1
                    if book:
                        books_with_wj.add(book)
                        book_wj_token_counts[book] += 1
                    if not in_wj_run or current_wj_book != book:
                        wj_token_runs += 1
                        current_wj_book = book
                    in_wj_run = True
                else:
                    in_wj_run = False
                    current_wj_book = ""

                strong_values: list[str] = []
                for key in ("strong", "strong_id", "strong_ids", "strongs"):
                    strong_values.extend(_strong_values(record.get(key)))
                if strong_values:
                    tokens_with_strong += 1
                for strong in strong_values:
                    strong_occurrences_total += 1
                    if strong.startswith("H"):
                        strong_h_occurrences += 1
                    elif strong.startswith("G"):
                        strong_g_occurrences += 1
                    else:
                        strong_other_occurrences += 1

    summary = {
        "validator": "logos_fast_validators word-token-signals",
        "status": "passed" if not failures else "failed",
        "files": len(paths),
        "records": records,
        "failures": len(failures),
        "translation_id": translation_id,
        "translation_ids_observed": sorted(translation_ids),
        "source_file_count": len(source_files),
        "book_count": len(book_token_counts),
        "book_token_counts": dict(sorted(book_token_counts.items())),
        "wj_word_tokens": wj_word_tokens,
        "wj_token_runs": wj_token_runs,
        "books_with_wj": sorted(books_with_wj),
        "book_wj_token_counts": dict(sorted(book_wj_token_counts.items())),
        "tokens_with_nesting_context": tokens_with_nesting_context,
        "tokens_with_surface_text": tokens_with_surface_text,
        "tokens_with_strong": tokens_with_strong,
        "strong_occurrences_total": strong_occurrences_total,
        "strong_h_occurrences": strong_h_occurrences,
        "strong_g_occurrences": strong_g_occurrences,
        "strong_other_occurrences": strong_other_occurrences,
        "non_authorizing": True,
        "no_text": True,
        "authority": "deterministic_word_token_signal_counts_only",
    }
    return summary, failures


def write_summary(path: Path | None, summary: dict[str, Any]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_python(args: argparse.Namespace, summary_json: Path | None = None) -> int:
    summary, failures = build_python_summary([Path(path) for path in args.paths], args.translation_id)
    write_summary(summary_json or args.summary_json, summary)
    if failures:
        print("PYTHON WORD-TOKEN SIGNAL SCAN FAILED")
        for failure in failures[:200]:
            print(f"- {failure}")
        if len(failures) > 200:
            print(f"- ... {len(failures) - 200} additional failures")
        return 1
    print(f"Python word-token signal scan passed for {summary['records']} record(s).")
    return 0


def _load_summary(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _summaries_match(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return left == right


def _compare_with_python(args: argparse.Namespace, rust_result: subprocess.CompletedProcess[str], rust_summary: Path) -> int:
    runtime_tmp = ROOT / "build" / "runtime_tmp"
    runtime_tmp.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="word-token-signals-", dir=runtime_tmp) as temp_dir:
        python_summary = Path(temp_dir) / "python_summary.json"
        python_code = run_python(args, python_summary)
        if (rust_result.returncode == 0) != (python_code == 0):
            print("Rust/Python word-token signal verdict mismatch.", file=sys.stderr)
            return 1
        rust_data = _load_summary(rust_summary)
        python_data = _load_summary(python_summary)
        if not _summaries_match(rust_data, python_data):
            print("Rust/Python word-token signal summary mismatch.", file=sys.stderr)
            print("--- Rust summary ---", file=sys.stderr)
            print(json.dumps(rust_data, indent=2, sort_keys=True), file=sys.stderr)
            print("--- Python summary ---", file=sys.stderr)
            print(json.dumps(python_data, indent=2, sort_keys=True), file=sys.stderr)
            return 1
    print("Rust/Python word-token signal parity passed.")
    return rust_result.returncode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--translation-id", default="eng-web")
    parser.add_argument("--summary-json", type=Path)
    parser.add_argument("--manifest-path", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--cargo-bin", default="cargo")
    parser.add_argument("--python-fallback", action="store_true")
    parser.add_argument("--require-rust", action="store_true")
    parser.add_argument(
        "--compare-python",
        action="store_true",
        help="Run the Python scanner too and fail if Rust/Python verdicts or summaries diverge.",
    )
    args = parser.parse_args(argv)

    if not args.manifest_path.exists():
        if args.require_rust:
            print(f"Missing Rust manifest: {args.manifest_path}", file=sys.stderr)
            return 1
        if args.python_fallback:
            print("Rust word-token signal scanner unavailable; using Python fallback.", file=sys.stderr)
            return run_python(args)
        print(f"Missing Rust manifest: {args.manifest_path}", file=sys.stderr)
        return 1

    runtime_tmp = ROOT / "build" / "runtime_tmp"
    runtime_tmp.mkdir(parents=True, exist_ok=True)
    compare_summary: Path | None = None
    if args.compare_python:
        compare_summary = runtime_tmp / "word_token_signals_rust_summary.json"

    try:
        rust_result = run_command(rust_command(args, compare_summary))
    except FileNotFoundError:
        if args.require_rust:
            print(f"Rust cargo binary not found: {args.cargo_bin}", file=sys.stderr)
            return 1
        if args.python_fallback:
            print("Rust cargo binary unavailable; using Python fallback.", file=sys.stderr)
            return run_python(args)
        print(f"Rust cargo binary not found: {args.cargo_bin}", file=sys.stderr)
        return 1

    relay(rust_result)
    if args.compare_python:
        assert compare_summary is not None
        return _compare_with_python(args, rust_result, compare_summary)
    return rust_result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
