#!/usr/bin/env python3
"""Compare candidate connection batches from multiple agents."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Iterable


def iter_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def agent_name(path: Path, record: dict[str, Any]) -> str:
    provenance = record.get("provenance") or {}
    created_by = str(provenance.get("created_by") or "")
    if ":" in created_by:
        return created_by.rsplit(":", 1)[-1]
    if created_by:
        return created_by
    return path.stem


def edge_key(record: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(record.get("subject_id")),
        str(record.get("predicate")),
        str(record.get("object_id")),
    )


def compare_batches(paths: list[Path]) -> dict[str, Any]:
    by_key: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    per_agent = Counter()
    for path in paths:
        for record in iter_jsonl(path):
            agent = agent_name(path, record)
            wrapped = {"agent": agent, "path": str(path), "record": record}
            by_key[edge_key(record)].append(wrapped)
            per_agent[agent] += 1

    agreements = []
    disagreements = []
    for key, proposals in sorted(by_key.items()):
        agents = sorted({proposal["agent"] for proposal in proposals})
        best = max(proposals, key=lambda proposal: proposal["record"].get("confidence", 0))
        item = {
            "subject_id": key[0],
            "predicate": key[1],
            "object_id": key[2],
            "agents": agents,
            "agent_count": len(agents),
            "proposal_count": len(proposals),
            "highest_confidence": best["record"].get("confidence", 0),
            "evidence_refs": sorted(
                {
                    evidence
                    for proposal in proposals
                    for evidence in proposal["record"].get("evidence_refs", [])
                }
            ),
        }
        if len(agents) >= 2:
            agreements.append(item)
        else:
            disagreements.append(item)

    return {
        "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "input_files": [str(path) for path in paths],
        "per_agent_counts": dict(sorted(per_agent.items())),
        "total_unique_edges": len(by_key),
        "agreement_count": len(agreements),
        "disagreement_count": len(disagreements),
        "agreements": sorted(
            agreements,
            key=lambda item: (-item["agent_count"], -item["highest_confidence"], item["subject_id"], item["predicate"], item["object_id"]),
        ),
        "disagreements": sorted(
            disagreements,
            key=lambda item: (-item["highest_confidence"], item["subject_id"], item["predicate"], item["object_id"]),
        ),
    }


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")


def write_report(path: Path, comparison: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Candidate Batch Comparison",
        "",
        f"- Generated: `{comparison['created_at']}`",
        f"- Input files: **{len(comparison['input_files'])}**",
        f"- Unique edges: **{comparison['total_unique_edges']}**",
        f"- Agreements: **{comparison['agreement_count']}**",
        f"- Disagreements: **{comparison['disagreement_count']}**",
        "",
        "## Per-Agent Counts",
        "",
        "| Agent | Candidates |",
        "|---|---:|",
    ]
    for agent, count in comparison["per_agent_counts"].items():
        lines.append(f"| `{agent}` | {count} |")
    lines.extend(["", "## Agreement Set", ""])
    if comparison["agreements"]:
        lines.append("| Edge | Agents | Confidence |")
        lines.append("|---|---|---:|")
        for item in comparison["agreements"][:50]:
            edge = f"{item['subject_id']} {item['predicate']} {item['object_id']}"
            lines.append(f"| `{edge}` | {', '.join(item['agents'])} | {item['highest_confidence']} |")
    else:
        lines.append("_No agreements across two or more agents._")
    lines.extend(["", "## Disagreement Set (Top 50)", ""])
    if comparison["disagreements"]:
        lines.append("| Edge | Agent | Confidence |")
        lines.append("|---|---|---:|")
        for item in comparison["disagreements"][:50]:
            edge = f"{item['subject_id']} {item['predicate']} {item['object_id']}"
            lines.append(f"| `{edge}` | {', '.join(item['agents'])} | {item['highest_confidence']} |")
    else:
        lines.append("_No single-agent-only edges._")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("batches", nargs="+", help="Candidate JSONL batch paths")
    parser.add_argument("--agreement-out", default="build/discovery/agreement.jsonl")
    parser.add_argument("--disagreement-out", default="build/discovery/disagreement.jsonl")
    parser.add_argument("--report", default="build/discovery/comparison.md")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    paths = [Path(path) for path in args.batches]
    if len(paths) < 2:
        print("Need at least two candidate batches to compare.")
        return 1
    missing = [str(path) for path in paths if not path.exists()]
    if missing:
        print("Missing batch file(s): " + ", ".join(missing))
        return 1
    comparison = compare_batches(paths)
    write_jsonl(Path(args.agreement_out), comparison["agreements"])
    write_jsonl(Path(args.disagreement_out), comparison["disagreements"])
    write_report(Path(args.report), comparison)
    print(
        f"Wrote {comparison['agreement_count']} agreements and "
        f"{comparison['disagreement_count']} disagreements."
    )
    print(f"Wrote report to {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
