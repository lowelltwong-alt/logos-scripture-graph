#!/usr/bin/env python3
"""Tier-0 atomic-isolation validator + scoped-mesh cluster builder (Eccl,
built at Phase 0 per the Prov close lesson a — BEFORE any writer launches —
with the p3 guarded output path from day 0).

STATUS: STAGED, NOT ARMED. The atomic unit_type set and the scoped-vs-full
mesh decision are OWNER-GATE questions for Eccl; ATOMIC_TYPES below is
pinned AFTER the gate (empty = every row goes to model review = full mesh).
The tool itself is smoke-tested at Phase 0 so the machinery is proven
before it can matter.

For every atomic-typed row in the combined draft corpus, deterministically
measures skeleton-tier content-token overlap with BOTH neighboring verses
(len>=2, stoplist-filtered — the same metric as the Phase-0 catchword
adjacency signal). Verdicts:
  machine_clean   — zero shared content tokens with either neighbor AND
                    confidence not in {low, medium_low}: the row's isolation
                    (the only model-review question specific to sentence
                    literature) is machine-verified; quote/refs/marks/
                    universals classes are covered by the standing suite.
  cohesion_live   — >=1 shared token with a neighbor: a cluster/merge rival
                    exists; model review REQUIRED.
Non-atomic rows and low/medium_low rows are always model-reviewed.

NON-IDENTITY NOTE: spans are WEB; neighbor verses are computed in WEB space
and each WEB verse's Hebrew is fetched via the eccl_lib crosswalk (the MT
text of WEB 5:1 is MT 4:17's).

Also emits the scoped review set: mandatory rows + a DETERMINISTIC stride
sample of machine_clean rows (15%, canonical order, fixed stride — no
randomness, fully auditable), grouped into review clusters of <=8 rows in
canonical order. CALIBRATION_ROWS (fixed pre-scoping calibration cluster,
if the gate orders one) are excluded from re-clustering.

Output (patch prov_tools_p3 pattern, day-0 here): the shared
SP/Eccl/review_scope.json is written ONLY when run against the full
canonical corpus; any other input writes a sibling artifact next to that
input, so subset runs can never clobber the orchestrator's plan.
Usage: check_atomic_isolation.py ../draft_rows_combined.jsonl
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from eccl_lib import BOOK, LAST_VERSE, SPBOOK, skeleton, web_to_mt

STOP = {"לא", "אל", "את", "על", "כי", "מן", "אם", "גם", "כל", "אשר", "הוא",
        "היא", "יש", "אין", "או", "פן", "בל", "לו", "לך", "בו", "בה", "מה",
        "זה", "זאת", "עם", "עד", "אך", "רק", "כן", "כה", "אף"}
# PINNED AT THE OWNER GATE — empty set = nothing machine-cleans = full mesh.
ATOMIC_TYPES: set[str] = set()
# Fixed calibration cluster row ids (gate-ordered, if any); excluded from
# re-clustering like Prov's c01.
CALIBRATION_ROWS: list[str] = []
SAMPLE_RATE = 0.15
SPAN = re.compile(r"^Eccl\.(\d+)\.(\d+)-Eccl\.(\d+)\.(\d+)$")
MAX_CH = max(LAST_VERSE)


def main() -> int:
    rows_path = Path(sys.argv[1]) if len(sys.argv) > 1 else SPBOOK / "draft_rows_combined.jsonl"
    oshb = {}
    for line in (SPBOOK / f"{BOOK}_oshb.txt").read_text(encoding="utf-8").splitlines():
        if "\t" in line:
            ref, text = line.split("\t", 1)
            oshb[ref] = skeleton(text)

    def toks(c, v):
        """Content tokens of WEB verse (c, v), fetched from the MT text via
        the crosswalk."""
        mt = web_to_mt(c, v)
        if mt is None:
            return set()
        return {x for x in oshb.get(f"{BOOK}.{mt[0]}.{mt[1]}", "").split()
                if len(x) >= 2 and x not in STOP}

    rows = [json.loads(l) for l in rows_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    verdicts = []
    mandatory = []
    clean = []
    for r in rows:
        rid = r["writer_decision_id"]
        m = SPAN.match(r["span"])
        c1, v1, c2, v2 = map(int, m.groups())
        lowc = r["confidence"] in ("low", "medium_low")
        if r["unit_type"] not in ATOMIC_TYPES:
            verdicts.append({"row": rid, "verdict": "model_review", "why": f"unit_type {r['unit_type']}"})
            mandatory.append(rid)
            continue
        prev = (c1, v1 - 1) if v1 > 1 else ((c1 - 1, LAST_VERSE.get(c1 - 1)) if c1 > 1 else None)
        nxt = (c2, v2 + 1) if v2 < LAST_VERSE.get(c2, 0) else ((c2 + 1, 1) if c2 < MAX_CH else None)
        shared_prev = sorted(toks(c1, v1) & toks(*prev)) if prev else []
        shared_next = sorted(toks(c2, v2) & toks(*nxt)) if nxt else []
        if lowc:
            verdicts.append({"row": rid, "verdict": "model_review", "why": f"confidence {r['confidence']}",
                             "shared_prev": shared_prev, "shared_next": shared_next})
            mandatory.append(rid)
        elif shared_prev or shared_next:
            verdicts.append({"row": rid, "verdict": "cohesion_live",
                             "shared_prev": shared_prev, "shared_next": shared_next})
            mandatory.append(rid)
        else:
            verdicts.append({"row": rid, "verdict": "machine_clean"})
            clean.append(rid)

    # deterministic stride sample of machine_clean rows (canonical order)
    if clean:
        n_sample = max(1, round(len(clean) * SAMPLE_RATE))
        stride = len(clean) / n_sample
        sample = [clean[int(i * stride)] for i in range(n_sample)]
    else:
        sample = []

    scoped = [r["writer_decision_id"] for r in rows
              if r["writer_decision_id"] in set(mandatory) | set(sample)]
    scoped_excl_cal = [rid for rid in scoped if rid not in CALIBRATION_ROWS]
    clusters = [{"id": f"c{i + 1 + (1 if CALIBRATION_ROWS else 0):02d}",
                 "row_ids": scoped_excl_cal[i * 8:(i + 1) * 8]}
                for i in range((len(scoped_excl_cal) + 7) // 8)]

    out = {
        "built": "Phase 0 staging (lesson a); ATOMIC_TYPES pinned at the owner gate",
        "armed": bool(ATOMIC_TYPES),
        "atomic_types": sorted(ATOMIC_TYPES),
        "corpus": rows_path.name,
        "rows_total": len(rows),
        "verdict_counts": {
            "model_review_form_or_lowconf": sum(1 for v in verdicts if v["verdict"] == "model_review"),
            "cohesion_live": sum(1 for v in verdicts if v["verdict"] == "cohesion_live"),
            "machine_clean": len(clean),
        },
        "sample": {"rate": SAMPLE_RATE, "method": "deterministic stride over canonical order",
                   "count": len(sample), "row_ids": sample},
        "calibration_fixed": CALIBRATION_ROWS,
        "scoped_rows_total": len(scoped),
        "clusters": clusters,
        "verdicts": verdicts,
    }
    # patch prov_tools_p3 pattern (day-0 here): the shared
    # SP/Eccl/review_scope.json is written ONLY when run against the full
    # canonical corpus; any other input writes a sibling artifact next to
    # that input, so subset runs can never clobber the orchestrator's plan.
    if rows_path.resolve() == (SPBOOK / "draft_rows_combined.jsonl").resolve():
        out_path = SPBOOK / "review_scope.json"
    else:
        out_path = rows_path.with_suffix(rows_path.suffix + ".review_scope.json")
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"rows": len(rows), "armed": bool(ATOMIC_TYPES),
                      **out["verdict_counts"],
                      "sample": len(sample), "scoped_total": len(scoped),
                      "clusters": len(clusters),
                      "out_path": out_path.name}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
