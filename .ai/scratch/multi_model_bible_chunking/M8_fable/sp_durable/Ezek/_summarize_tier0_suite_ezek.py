#!/usr/bin/env python3
"""Orchestrator tool: a durable, digest-bound summary of the Tier-0 suite run over the Ezekiel draft rows.

Deterministic part: statuses, counts, finding classes by member and by writer part, and the digests of the report,
the view, the rows and every tool that produced it. Judgment part: the `orchestrator_observations` block, which
sorts finding classes into brief gaps, content defects and heuristic limits. That block is the orchestrator's
reading, NOT a ruling: on this HARD book the controlling agent rules on how the findings are routed.
Usage: _summarize_tier0_suite_ezek.py
"""
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EZ = Path(__file__).resolve().parent
REPORT = EZ / "writer" / "draft_rows_combined.suite_view.jsonl.validator_report.json"
VIEW = EZ / "writer" / "draft_rows_combined.suite_view.jsonl"
ROWS = EZ / "writer" / "draft_rows_combined.jsonl"
OUT = EZ / "writer" / "ezek_tier0_suite_summary.v1.json"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def norm(msg: str) -> str:
    m = re.sub(r"'[^']*'|\"[^\"]*\"", "'…'", msg)
    return re.sub(r"\d+", "N", m)[:110]


OBSERVATIONS = {
    "brief_gap": {
        "classes": ["has NO oshb: ref in its field", "non-Ezek or malformed ref",
                    "web_quotes e15 classes and 'curly quote with NO web: ref'"],
        "reading": ("Conventions the Tier-0 tools enforce but WRITER_BRIEF.md never stated, because the toolchain was "
                    "not staged when the writers ran: every Hebrew quote carries an oshb: ref in the same field; one "
                    "witness-prefixed ref per boundary_evidence_refs entry; WEB quotes in curly double quotes with an "
                    "inline web: ref, Hebrew spliced bare. The landing validator already proved byte truth for the "
                    "Hebrew, so most of these are form, not fabrication. Which form is canonical, and whether the "
                    "draft rows are repaired before or after primaries, is the controlling agent's call."),
    },
    "content_defect_candidates": {
        "classes": ["hebrew_normalize_dryrun defects", "cap_sweep failures", "ngram7 offending 7-grams",
                    "claims paseq but OSHB carries none", "parashah-mark ref lacks single-witness disclosure",
                    "does not collate against any nearby cited ref (a share of them)"],
        "reading": ("Findings that stand whatever the conventions: K/Q notes copied whole (ketiv and qere run together "
                    "as one string that is neither reading); pointed forms in neither the verse bytes nor the Qere "
                    "layer; two whole-chapter rows at medium confidence without the E-02 cap disclosure (p01-2 ch 2, "
                    "p02-4 ch 9); p03 boilerplate repeated across 11-12 rows; paseq cited at MT 5:2 (it stands at "
                    "5:1) and at MT 26:19 (none)."),
    },
    "heuristic_limits": {
        "classes": ["does not collate against any nearby cited ref (the rest)", "mark_symmetry kq_claim",
                    "universals", "register"],
        "reading": ("Window and nearest-ref heuristics bind a claim to the wrong verse where prose cites in another "
                    "form (bare 2:3, MT 46.22). Each item needs a reader; none is a verdict."),
    },
    "tool_defects_fixed_at_staging_before_this_run": [
        "norm_english stripped only [fn ...]; the Ezek extract writes a bare [fn] at 38 sites",
        "pm['paseq'] is a list in pmarks_Ezek.json; the Jer tools read a dict - converted in ezek_lib.load_pmarks",
        "no Qere tier in the normalizer or the Hebrew-binding arm, although the brief permits disclosed Qere quotes",
        "the first puncta arms raised 12 flags on 5 rows, every one wrong (negated disclosures, bare 41:20 / 46.22 "
        "numbers, spans covering the site, a distant 'not'); rewritten and regression-tested, 0 remain",
        "the K/Q claim arms ignored the OSHB editorial notes that record a ketib/qere relative to BHS",
        "the suite was first run without PYTHONIOENCODING=utf-8: four members (normalizer, web_quotes, universals, "
        "register) crashed on the Windows codec, and three more (citation_sweep, refs_mirror, check_marks) on the "
        "paseq and object-ref shapes",
    ],
}


def main() -> int:
    r = json.loads(REPORT.read_text(encoding="utf-8"))
    members = {}
    for name, v in r.items():
        if name == "summary" or not isinstance(v, dict):
            continue
        n = next((v[k] for k in ("flag_count", "defect_count") if k in v), None)
        if n is None and isinstance(v.get("problems"), list):
            n = len(v["problems"])
        if n is None and isinstance(v.get("failures"), list):
            n = len(v["failures"])
        if n is None and isinstance(v.get("offending_7grams"), list):
            n = len(v["offending_7grams"])
        members[name] = {"status": v.get("status") or ("RED" if v.get("defect_count") else "GREEN"), "count": n}

    cs = r["citation_sweep"]["problems"]
    cs_classes = collections.Counter(norm(p.split(": ", 1)[1]) for p in cs)
    cs_parts = collections.Counter(p.split(":", 1)[0].split("-")[0].lower() for p in cs)
    cs_rows = collections.Counter(p.split(":", 1)[0] for p in cs)

    def classes(items, *keys):
        c = collections.Counter()
        for it in items:
            c[next((str(it[k])[:90] for k in keys if isinstance(it, dict) and k in it), "unclassified")] += 1
        return dict(c.most_common())

    tools = sorted((EZ / "tools").glob("*.py"))
    out = {
        "schema": "m8_tier0_suite_summary.v1", "book": "Ezek", "built_by": "orchestrator (claude-opus-5)",
        "inputs": {
            "rows": {"path": "writer/draft_rows_combined.jsonl", "sha256": sha(ROWS)},
            "suite_view": {"path": "writer/draft_rows_combined.suite_view.jsonl", "sha256": sha(VIEW),
                           "why": "three parts wrote object refs; see draft_rows_combined.suite_view.manifest.json"},
            "report": {"path": REPORT.relative_to(EZ).as_posix(), "sha256": sha(REPORT)},
            "tools": {p.name: sha(p) for p in tools},
        },
        "run": {"command": "PYTHONIOENCODING=utf-8 python tools/run_validator_suite.py writer/draft_rows_combined.suite_view.jsonl",
                "summary": r["summary"]},
        "members": members,
        "citation_sweep": {"problems": len(cs), "by_class": dict(cs_classes.most_common()),
                           "by_part": dict(sorted(cs_parts.items())), "rows_with_most": dict(cs_rows.most_common(12))},
        "hebrew_normalize": {k: r["hebrew_normalize_dryrun"].get(k) for k in ("ok", "qere", "fixed", "mention", "defect_count")}
        | {"defects_listed": r["hebrew_normalize_dryrun"].get("defects"),
           "note": "the tool lists the first 15 of defect_count; the rest need a run over the rows"},
        "cap_sweep": {k: r["cap_sweep"].get(k) for k in ("whole_chapter_rows", "failures")},
        "ngram7": {"offending_7grams": r["ngram7"].get("offending_7grams")},
        "mark_symmetry_rules": dict(collections.Counter(f["rule"] for f in r["mark_symmetry"]["flags"])),
        "web_quotes_classes": classes(r["web_quotes"]["flags"], "issue", "class", "rule"),
        "universals_classes": classes(r["universals"]["flags"], "claim"),
        "register_classes": classes(r["register"]["flags"], "class"),
        "orchestrator_observations": OBSERVATIONS,
        "limit": "a deterministic tally plus the orchestrator's reading; it rules on nothing",
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    print(json.dumps({"written": OUT.relative_to(EZ).as_posix(), "sha256": sha(OUT), "members": members,
                      "citation_sweep_by_part": out["citation_sweep"]["by_part"]}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
