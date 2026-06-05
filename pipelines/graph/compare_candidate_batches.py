#!/usr/bin/env python3
"""Compare candidate RelationshipObject batches from multiple agents."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def load_batch(path: Path) -> dict[tuple[str, str, str], dict[str, object]]:
    records: dict[tuple[str, str, str], dict[str, object]] = {}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            rec = json.loads(line)
            key = (str(rec.get("subject_id")), str(rec.get("predicate")), str(rec.get("object_id")))
            records[key] = rec
    return records


def compare_batches(paths: list[Path]) -> dict[str, object]:
    if len(paths) < 2:
        raise ValueError("compare_candidate_batches requires at least two input batches")
    by_agent: dict[str, dict[tuple[str, str, str], dict[str, object]]] = {p.as_posix(): load_batch(p) for p in paths}
    key_to_agents: dict[tuple[str, str, str], list[str]] = defaultdict(list)
    for agent, records in by_agent.items():
        for key in records:
            key_to_agents[key].append(agent)
    agreements = {key: sorted(agents) for key, agents in key_to_agents.items() if len(agents) >= 2}
    disagreements = {key: agents[0] for key, agents in key_to_agents.items() if len(agents) == 1}
    return {"by_agent": by_agent, "agreements": agreements, "disagreements": disagreements}


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")


def materialize_outputs(result: dict[str, object], out_dir: Path, report_path: Path) -> tuple[Path, Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    agreement_path = out_dir / "agreement.jsonl"
    disagreement_path = out_dir / "disagreement.jsonl"
    agreements: dict[tuple[str, str, str], list[str]] = result["agreements"]  # type: ignore[assignment]
    disagreements: dict[tuple[str, str, str], str] = result["disagreements"]  # type: ignore[assignment]
    agreement_rows = [
        {"subject_id": k[0], "predicate": k[1], "object_id": k[2], "agents": agents, "agent_count": len(agents)}
        for k, agents in sorted(agreements.items())
    ]
    disagreement_rows = [
        {"subject_id": k[0], "predicate": k[1], "object_id": k[2], "agent": agent}
        for k, agent in sorted(disagreements.items())
    ]
    write_jsonl(agreement_path, agreement_rows)
    write_jsonl(disagreement_path, disagreement_rows)
    by_agent: dict[str, dict[tuple[str, str, str], dict[str, object]]] = result["by_agent"]  # type: ignore[assignment]
    all_keys = set()
    for records in by_agent.values():
        all_keys.update(records)
    lines = [
        "# Candidate batch comparison",
        "",
        "## Per-agent counts",
        "",
        "| agent batch | candidates | overlap with any other | overlap % |",
        "|-------------|------------|------------------------|-----------|",
    ]
    agreement_keys = set(agreements)
    for agent, records in sorted(by_agent.items()):
        overlap = len(set(records) & agreement_keys)
        pct = (overlap / len(records) * 100) if records else 0.0
        lines.append(f"| `{agent}` | {len(records)} | {overlap} | {pct:.1f}% |")
    lines.extend([
        "",
        "## Summary",
        "",
        f"- Unique subject/predicate/object triples: {len(all_keys)}",
        f"- Agreement triples (>=2 agents): {len(agreement_rows)}",
        f"- Disagreement triples (single agent): {len(disagreement_rows)}",
        f"- Agreement JSONL: `{agreement_path.as_posix()}`",
        f"- Disagreement JSONL: `{disagreement_path.as_posix()}`",
        "",
        "## Agreement list",
        "",
        "| subject | predicate | object | agents |",
        "|---------|-----------|--------|--------|",
    ])
    for row in agreement_rows[:100]:
        lines.append(f"| {row['subject_id']} | {row['predicate']} | {row['object_id']} | {', '.join(row['agents'])} |")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return agreement_path, disagreement_path, report_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batches", nargs="+", help="Candidate JSONL batches to compare")
    parser.add_argument("--out-dir", default="build/discovery/comparison")
    parser.add_argument("--report", default="build/discovery/comparison.md")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = [Path(p) for p in args.batches]
    result = compare_batches(paths)
    agreement_path, disagreement_path, report_path = materialize_outputs(result, Path(args.out_dir), Path(args.report))
    print(f"Agreement set: {agreement_path}")
    print(f"Disagreement set: {disagreement_path}")
    print(f"Report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
