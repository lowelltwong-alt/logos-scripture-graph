#!/usr/bin/env python3
"""Run pytest in timeout-aware segments and persist local runtime hints.

This runner is for local/agent use when a normal pytest run hangs or times out.
It records timeout hints under `.pytest_cache/logos_pytest_runtime_hints.json`.
The next run uses those hints to isolate likely timeout tests first, so one known
bad test does not repeatedly hang the entire suite.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STATE = ROOT / ".pytest_cache" / "logos_pytest_runtime_hints.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_hints(path: Path) -> dict:
    if not path.exists():
        return {"version": 1, "tests": {}, "segments": []}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"version": 1, "tests": {}, "segments": [], "previous_state_unreadable": True}


def save_hints(path: Path, hints: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(hints, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parse_collected_nodeids(stdout: str) -> list[str]:
    nodeids: list[str] = []
    for raw in stdout.splitlines():
        line = raw.strip()
        if not line or line.startswith("<") or line.startswith("="):
            continue
        if line.endswith(" selected") or " collected" in line:
            continue
        if line.startswith("tests/") or line.startswith("tests\\"):
            nodeids.append(line.replace("\\", "/"))
    return nodeids


def collect_nodeids(pytest_args: list[str], timeout_seconds: int) -> list[str]:
    cmd = [sys.executable, "-m", "pytest", "--collect-only", "-q", *pytest_args]
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "pytest collection failed")
    return parse_collected_nodeids(proc.stdout)


def order_nodeids(nodeids: list[str], hints: dict) -> list[str]:
    test_hints = hints.get("tests", {})
    suspect = [n for n in nodeids if test_hints.get(n, {}).get("likely_timeout")]
    normal = [n for n in nodeids if n not in suspect]
    return suspect + normal


def segment_nodeids(nodeids: list[str], hints: dict, max_segment_size: int) -> list[list[str]]:
    ordered = order_nodeids(nodeids, hints)
    test_hints = hints.get("tests", {})
    segments: list[list[str]] = []
    current: list[str] = []
    current_module: str | None = None

    for nodeid in ordered:
        module = nodeid.split("::", 1)[0]
        if test_hints.get(nodeid, {}).get("likely_timeout"):
            if current:
                segments.append(current)
                current = []
                current_module = None
            segments.append([nodeid])
            continue
        if current and (module != current_module or len(current) >= max_segment_size):
            segments.append(current)
            current = []
        current.append(nodeid)
        current_module = module

    if current:
        segments.append(current)
    return segments


def timeout_for_segment(segment: list[str], hints: dict, default_timeout: int) -> int:
    tests = hints.get("tests", {})
    suggested = default_timeout
    for nodeid in segment:
        item = tests.get(nodeid, {})
        if item.get("likely_timeout") and item.get("last_timeout_seconds"):
            suggested = min(suggested, max(5, int(item["last_timeout_seconds"])))
        elif item.get("last_duration_seconds"):
            suggested = max(suggested, min(default_timeout * 3, int(item["last_duration_seconds"] * 3) + 5))
    return suggested


def mark_timeout(hints: dict, segment: list[str], timeout_seconds: int, elapsed: float) -> None:
    tests = hints.setdefault("tests", {})
    for nodeid in segment:
        item = tests.setdefault(nodeid, {})
        item.update(
            {
                "likely_timeout": True,
                "last_timeout_seconds": timeout_seconds,
                "last_elapsed_before_timeout_seconds": round(elapsed, 3),
                "last_started_at": utc_now(),
                "next_run_hint": "run isolated first; split parent segment before retrying full suite",
            }
        )


def mark_success(hints: dict, segment: list[str], elapsed: float) -> None:
    tests = hints.setdefault("tests", {})
    per_test = elapsed / max(1, len(segment))
    for nodeid in segment:
        item = tests.setdefault(nodeid, {})
        item.update(
            {
                "likely_timeout": False,
                "last_duration_seconds": round(per_test, 3),
                "last_passed_at": utc_now(),
            }
        )


def run_segment(segment: list[str], hints: dict, timeout_seconds: int) -> int:
    started = time.monotonic()
    hints["active_segment"] = {
        "nodeids": segment,
        "timeout_seconds": timeout_seconds,
        "started_at": utc_now(),
    }
    save_hints(DEFAULT_STATE, hints)
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", *segment],
            cwd=ROOT,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        elapsed = time.monotonic() - started
        mark_timeout(hints, segment, timeout_seconds, elapsed)
        hints.pop("active_segment", None)
        return 124

    elapsed = time.monotonic() - started
    if proc.returncode == 0:
        mark_success(hints, segment, elapsed)
    hints.pop("active_segment", None)
    return proc.returncode


def run_segments(segments: list[list[str]], hints: dict, default_timeout: int) -> int:
    overall = 0
    for index, segment in enumerate(segments, 1):
        timeout_seconds = timeout_for_segment(segment, hints, default_timeout)
        print(f"[pytest-guarded] segment {index}/{len(segments)} size={len(segment)} timeout={timeout_seconds}s")
        code = run_segment(segment, hints, timeout_seconds)
        save_hints(DEFAULT_STATE, hints)
        if code == 124 and len(segment) > 1:
            midpoint = max(1, len(segment) // 2)
            print("[pytest-guarded] timeout; splitting segment for isolation")
            split_code = run_segments([segment[:midpoint], segment[midpoint:]], hints, timeout_seconds)
            overall = split_code or overall or code
        elif code != 0:
            overall = code if overall == 0 else overall
    return overall


def main() -> int:
    global DEFAULT_STATE

    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout-seconds", type=int, default=60)
    parser.add_argument("--collect-timeout-seconds", type=int, default=60)
    parser.add_argument("--max-segment-size", type=int, default=10)
    parser.add_argument("--state", default=str(DEFAULT_STATE))
    parser.add_argument("pytest_args", nargs="*")
    args = parser.parse_args()

    DEFAULT_STATE = Path(args.state)

    hints = load_hints(DEFAULT_STATE)
    nodeids = collect_nodeids(args.pytest_args, args.collect_timeout_seconds)
    if not nodeids:
        print("No pytest tests collected.")
        return 1
    segments = segment_nodeids(nodeids, hints, args.max_segment_size)
    hints["last_collection"] = {
        "collected_at": utc_now(),
        "test_count": len(nodeids),
        "segment_count": len(segments),
    }
    save_hints(DEFAULT_STATE, hints)
    return run_segments(segments, hints, args.timeout_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
