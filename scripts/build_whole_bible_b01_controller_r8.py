#!/usr/bin/env python3
"""Build a controller-observed, candidate-only B01 evidence scaffold.

This module intentionally does not dispatch a model and does not enable the
revision-7 campaign.  It creates an immutable source manifest before any role
assignment, then records controller-observed assignment/result events.  Agent
reports are supplied by an external provider adapter and contain observations
only; no source text is copied into the packet.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping

ROLES = (
    "original_language_translation_scout",
    "literary_form_scout",
    "canonical_relations_and_premortem_scout",
    "second_temple_rabbinic_context_scout",
)
_ID = re.compile(r"^[A-Za-z0-9._:-]+$")


def _canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical(value)).hexdigest()


def file_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _safe_id(value: str, field: str) -> str:
    if not isinstance(value, str) or len(value) < 8 or not _ID.fullmatch(value):
        raise ValueError(f"invalid {field}")
    return value


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _identity(execution_id: str, assignment_id: str, instance: str, role: str, provider: str) -> dict[str, str]:
    return {
        "execution_id": _safe_id(execution_id, "execution_id"),
        "assignment_id": _safe_id(assignment_id, "assignment_id"),
        "agent_instance_id": _safe_id(instance, "agent_instance_id"),
        "role_id": role,
        "provider_family": provider,
    }


@dataclass(frozen=True)
class ControllerRun:
    root: Path
    book: str
    run_id: str
    attempt_id: str
    controller_instance_id: str
    manifest_sha256: str
    source_ids: tuple[str, ...]

    @property
    def packet_dir(self) -> Path:
        return self.root / "packet"

    @property
    def events_dir(self) -> Path:
        return self.root / "controller_events"

    def _event(self, *, event_id: str, event_kind: str, execution_id: str, assignment_id: str, result_digest: str) -> Path:
        event = {
            "schema_version": "whole_bible_b01_controller_event.v1",
            "event_id": event_id,
            "event_kind": event_kind,
            "execution_id": execution_id,
            "assignment_id": assignment_id,
            "observed_at": _now(),
            "controller_instance_id": self.controller_instance_id,
            "input_manifest_sha256": self.manifest_sha256,
            "result_digest": result_digest,
            "candidate_only": True,
            "non_authorizing": True,
        }
        path = self.events_dir / f"{event_id}.json"
        if path.exists():
            if json.loads(path.read_text(encoding="utf-8")) != event:
                raise ValueError(f"event id collision: {event_id}")
            return path
        path.write_bytes(_canonical(event))
        return path

    def assign(self, role: str, *, provider_family: str = "provider-neutral") -> dict[str, str]:
        if role not in ROLES:
            raise ValueError(f"unsupported B01 role: {role}")
        assignment_id = f"asg-{self.run_id}-{role}"
        execution_id = f"exec-{self.run_id}-{role}"
        event_id = f"evt-{self.run_id}-{role}-assigned"
        self._event(event_id=event_id, event_kind="assignment_issued", execution_id=execution_id, assignment_id=assignment_id, result_digest=digest({"event": event_id}))
        return {"role_id": role, "assignment_id": assignment_id, "execution_id": execution_id, "assignment_event_id": event_id, "provider_family": provider_family}

    def record_result(self, assignment: Mapping[str, str], *, agent_instance_id: str, report: Mapping[str, Any], provider_family: str = "provider-neutral") -> Path:
        role = assignment["role_id"]
        _safe_id(agent_instance_id, "agent_instance_id")
        if role not in ROLES:
            raise ValueError("unsupported B01 role")
        required = {"observations", "uncertainties", "source_refs"}
        if set(report) != required or not report["observations"] or not report["source_refs"]:
            raise ValueError("role report must contain only observations, uncertainties, and source_refs")
        result_digest = digest(report)
        finished_id = f"evt-{self.run_id}-{role}-finished"
        received_id = f"evt-{self.run_id}-{role}-received"
        self._event(event_id=finished_id, event_kind="execution_finished", execution_id=assignment["execution_id"], assignment_id=assignment["assignment_id"], result_digest=result_digest)
        self._event(event_id=received_id, event_kind="result_received", execution_id=assignment["execution_id"], assignment_id=assignment["assignment_id"], result_digest=result_digest)
        doc = {
            "schema_version": "whole_bible_b01_role_report.v2", "kind": "role_report",
            "book": self.book, "run_id": self.run_id, "stage_attempt_id": self.attempt_id,
            "candidate_only": True, "non_authorizing": True,
            "identity": _identity(assignment["execution_id"], assignment["assignment_id"], agent_instance_id, role, provider_family),
            "controller_event_ids": [assignment["assignment_event_id"], finished_id, received_id],
            "input_manifest_sha256": self.manifest_sha256,
            **dict(report),
        }
        path = self.packet_dir / f"role-{role}.json"
        if path.exists() and json.loads(path.read_text(encoding="utf-8")) != doc:
            raise ValueError(f"non-idempotent result for role: {role}")
        path.write_bytes(_canonical(doc))
        return path


def prepare(*, root: Path, book: str, run_id: str, attempt_id: str, source_paths: Iterable[Path], controller_instance_id: str = "controller-r8-local") -> ControllerRun:
    """Freeze source IDs/digests and emit assignment-ready run state."""
    if not re.fullmatch(r"[A-Za-z0-9-]{2,12}", book):
        raise ValueError("invalid book")
    root = root.resolve(); root.mkdir(parents=True, exist_ok=True)
    source_rows = []
    for path in sorted((Path(p).resolve() for p in source_paths), key=lambda p: p.as_posix()):
        if not path.is_file():
            raise FileNotFoundError(path)
        source_id = path.as_posix().replace("/", "_").replace("\\", "_")
        source_rows.append({"source_id": source_id, "sha256": file_digest(path), "size": path.stat().st_size})
    if not source_rows:
        raise ValueError("at least one governed source is required")
    source_ids = tuple(row["source_id"] for row in source_rows)
    manifest_payload = {"book": book, "run_id": run_id, "stage_attempt_id": attempt_id, "sources": source_rows}
    manifest_sha = digest(manifest_payload)
    packet, events = root / "packet", root / "controller_events"
    packet.mkdir(exist_ok=True); events.mkdir(exist_ok=True)
    manifest = {
        "schema_version": "whole_bible_b01_input_manifest.v1", "kind": "input_manifest",
        "book": book, "run_id": run_id, "stage_attempt_id": attempt_id,
        "candidate_only": True, "non_authorizing": True,
        "identity": _identity(f"exec-{run_id}-controller", f"asg-{run_id}-controller", controller_instance_id, "controller", "provider-neutral"),
        "controller_event_ids": [f"evt-{run_id}-manifest"], "input_manifest_sha256": manifest_sha,
        "source_ids": list(source_ids), "source_digests": {row["source_id"]: row["sha256"] for row in source_rows},
    }
    manifest_path = packet / "input-manifest.json"
    if manifest_path.exists() and json.loads(manifest_path.read_text(encoding="utf-8")) != manifest:
        raise ValueError("immutable manifest collision")
    manifest_path.write_bytes(_canonical(manifest))
    run = ControllerRun(root, book, run_id, attempt_id, controller_instance_id, manifest_sha, source_ids)
    run._event(event_id=f"evt-{run_id}-manifest", event_kind="assignment_issued", execution_id=f"exec-{run_id}-controller", assignment_id=f"asg-{run_id}-controller", result_digest=manifest_sha)
    return run


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path); parser.add_argument("--book", required=True); parser.add_argument("--run-id", required=True); parser.add_argument("--attempt-id", required=True); parser.add_argument("sources", nargs="+", type=Path)
    args = parser.parse_args(argv)
    run = prepare(root=args.root, book=args.book, run_id=args.run_id, attempt_id=args.attempt_id, source_paths=args.sources)
    print(json.dumps({"manifest_sha256": run.manifest_sha256, "packet_dir": str(run.packet_dir), "events_dir": str(run.events_dir), "source_count": len(run.source_ids)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
