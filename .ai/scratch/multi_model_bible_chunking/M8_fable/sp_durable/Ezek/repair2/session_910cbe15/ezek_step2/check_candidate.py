#!/usr/bin/env python3
"""Check CANDIDATE prose against the live gates WITHOUT touching the corpus. Read-only.

WHY THIS EXISTS. My brief for the author wave was written from the orders and never checked against the suite;
three checks that the brief called GREEN went RED, and one duty was not merely omitted but CONTRADICTED. The cure
is to put the GATE in the author's hands, so prose arrives already clean instead of arriving and then being
measured. This tool is that gate, applied to a proposal in memory.

USAGE
  python check_candidate.py my_proposal.json

  where my_proposal.json is {"P08-003": {"boundary_rationale": "...", "device_notes": "..."}, ...}
  Only the fields you name are replaced; everything else in the row is the live text.

WHAT IT REPORTS, per row and per field: every register class that fires (with the matched substring and its
context), and the refs-mirror and citation-mirror verdicts for the row. A proposal with flags is not finished.
It NEVER writes to the corpus - it builds a copy in memory and scans that.
"""
import json
import sys
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
sys.path.insert(0, str(EZ / "tools"))
import check_register as CR                                                    # noqa: E402
import check_refs_mirror as CM                                                 # noqa: E402

PROSE = ("boundary_rationale", "strongest_rejected_alternative", "device_notes", "literature_type_guess")


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    prop = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    live = {r["decision_id"]: r for r in
            (json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip())}
    report, clean = {}, True
    for rid, fields in prop.items():
        if rid not in live:
            report[rid] = {"ERROR": "no such row"}
            clean = False
            continue
        cand = dict(live[rid])
        unknown = [f for f in fields if f not in cand]
        for f, v in fields.items():
            cand[f] = v
        flags = CR.scan_row(cand, "candidate")
        row_rep = {"register_flags": len(flags),
                   "flags": [{"field": f["field"], "class": f["class"], "match": f["match"],
                              "context": f["context"]} for f in flags]}
        if unknown:
            row_rep["FIELDS_NOT_ON_THIS_ROW"] = unknown
        try:
            a = CM.analyze_row(cand)
            # REPORT THE KEYS THE MEMBER ACTUALLY RETURNS. My first version filtered on a guessed key list and
            # printed an EMPTY section for a sound row - a check that reports nothing is worse than no check,
            # because it reads as a pass. Non-empty lists are carried in full; empty ones are stated as 0.
            summary = {}
            for k, v in a.items():
                if k == "decision_id":
                    continue
                if isinstance(v, list):
                    summary[k] = v if v else 0
                else:
                    summary[k] = v
            row_rep["refs_and_citations"] = summary
            unmirrored = [x for x in (a.get("items") or []) if not x.get("mirrored", True)]
            if unmirrored:
                row_rep["UNMIRRORED_CITATIONS"] = unmirrored
                clean = False
            if a.get("orphan_refs") or a.get("mirror_reading_disagreements"):
                clean = False
        except Exception as exc:                                               # pragma: no cover
            row_rep["refs_and_citations"] = {"ERROR": "%s: %s" % (type(exc).__name__, exc)}
        if flags or unknown:
            clean = False
        report[rid] = row_rep
    print(json.dumps({"rows_checked": len(prop),
                      "ALL_CLEAN": clean,
                      "total_register_flags": sum(r.get("register_flags", 0) for r in report.values()),
                      "per_row": report}, ensure_ascii=False, indent=1))
    return 0 if clean else 1


if __name__ == "__main__":
    raise SystemExit(main())
