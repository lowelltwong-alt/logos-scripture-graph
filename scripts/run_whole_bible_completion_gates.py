#!/usr/bin/env python3
"""Execute the exact completion gates without a shell and write immutable evidence."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from scripts import whole_bible_replay_evidence as core


def run_gates(*, book: str, run_id: str, attempt_id: str, campaign_path: Path = core.DEFAULT_CAMPAIGN, model_root: Path = core.DEFAULT_MODEL_ROOT, root: Path = core.ROOT, allow_test_roots: bool = False) -> Path:
    core.validate_authoritative_runtime_paths(campaign_path=campaign_path, model_root=model_root, root=root, allow_test_roots=allow_test_roots)
    if not core.SAFE_ID.fullmatch(run_id) or not core.SAFE_ID.fullmatch(attempt_id):
        raise core.ReplayEvidenceError("QF-SCHEMA", "unsafe gate run identity")
    campaign = core.load_json(campaign_path)
    job = core.campaign_job(campaign, book)
    expected = core.expected_completion_gate_argv(book=book, run_id=run_id)
    directory = core.run_dir(model_root, book, run_id)
    evidence_directory = directory / "gate_evidence" / attempt_id
    records = []
    for gate_id, declared_argv in expected.items():
        actual_argv = [sys.executable, *declared_argv[1:]] if declared_argv[0] == "python" else list(declared_argv)
        completed = subprocess.run(actual_argv, cwd=root, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, check=False)
        if completed.returncode != 0:
            detail = completed.stderr.decode("utf-8", errors="replace")[-2000:]
            raise core.ReplayEvidenceError("QF-GATE", f"{gate_id} failed with {completed.returncode}: {detail}")
        if not completed.stdout:
            raise core.ReplayEvidenceError("QF-GATE", f"{gate_id} emitted no stdout evidence")
        evidence = evidence_directory / f"{gate_id}.stdout"
        with core.exclusive_lock(model_root / "state"):
            core.atomic_write(evidence, completed.stdout, immutable=True)
        normalized = core.repo_relative(evidence, root)
        if not core.job_path_authorized(normalized, job, run_id=run_id):
            raise core.ReplayEvidenceError("QF-09-FORBIDDEN-EFFECT", f"gate evidence outside job allowlist: {normalized}")
        digest = core.digest_file(evidence)
        records.append({
            "gate_id": gate_id,
            "argv": declared_argv,
            "exit_code": 0,
            "status": "passed",
            "evidence_path": normalized,
            "evidence_sha256": digest,
            "stdout_sha256": digest,
        })
    bundle = {
        "schema_version": "whole_bible_completion_gate_bundle.v1",
        "book": book,
        "run_id": run_id,
        "gates": records,
        "contains_scripture_text": False,
        "contains_source_rows": False,
        "non_authorizing": True,
    }
    output = directory / "completion_gate_bundles" / f"{attempt_id}.json"
    with core.exclusive_lock(model_root / "state"):
        core.atomic_write(output, core.canonical_bytes(bundle), immutable=True)
    core.validate_completion_gate_bundle(output, book=book, run_id=run_id, root=root)
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--book", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--attempt-id", required=True)
    args = parser.parse_args(argv)
    try:
        path = run_gates(book=args.book, run_id=args.run_id, attempt_id=args.attempt_id)
    except core.ReplayEvidenceError as exc:
        print(f"Completion gate execution failed: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote immutable completion gate bundle: {core.repo_relative(path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())