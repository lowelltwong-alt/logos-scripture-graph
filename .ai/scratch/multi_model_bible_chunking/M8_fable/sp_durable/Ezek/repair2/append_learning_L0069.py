#!/usr/bin/env python3
"""L-0069: the refreshed metrics file's summary counter reads 0 refusals while its own histogram reads 5."""
import hashlib
import json
from pathlib import Path

M8 = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable")
LOG = M8 / "orchestration_learning_log.v1.jsonl"

row = {
    "schema": "m8_orchestration_learning.v1", "date": "2026-09-21", "book": "Ezek", "id": "L-0069",
    "stage": "bookkeeping", "element": "metric_classifier_coverage",
    "observation": ("The OW-14 metrics refresh DID ingest the five refused Fable dispatches - source "
                    "sp_durable/Ezek/ezek_close_audit_attempt_receipts.jsonl at sha 5e2e8e51, 5 receipts, and the "
                    "by_model_ordered histogram for claude-fable-5-1 shows 'FAILED AT LAUNCH': 5. But the adjacent "
                    "summary counter refused_no_deliverable reads 0 for that model, because the counter keys on a "
                    "different outcome string than the one launch refusals are receipted with. Both numbers sit in "
                    "the same file: a reader of the summary sees zero refusals, a reader of the histogram sees five."),
    "recommendation": ("Widen the refused_no_deliverable classifier in sp_durable/campaign/_orchestration_metrics.py "
                       "to include launch-time refusals, and bump the metrics schema when doing so, because "
                       "reclassifying changes every historical number the file reports. NOT done here: the file was "
                       "refreshed minutes earlier, and silently changing a classifier between two refreshes of the "
                       "same schema version would make two versions disagree with no recorded reason. Generated "
                       "files are not hand-edited; the generator is authoritative."),
    "verdict": "PROPOSED - defer to the book-close metrics version bump",
    "metric": "1 summary counter undercounts 5 receipted launch refusals; histogram is correct",
    "evidence_refs": ["orchestration_metrics.v1.json@1337016a4b5dc7d790404b640a7fae8e5cde59672c82f44307923f0049bb6416",
                      "ezek_close_audit_attempt_receipts.jsonl@5e2e8e51", "E-49", "OW-18"],
    "supersedes": None,
}

pre = LOG.read_bytes()
if b'"L-0069"' in pre:
    print("L-0069 already present - not appended again")
else:
    with LOG.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    if not LOG.read_bytes().startswith(pre):
        raise SystemExit("INTEGRITY FAILURE: the learning log was not appended to")
print(json.dumps({"total_rows": len([l for l in LOG.read_text(encoding="utf-8").splitlines() if l.strip()]),
                  "sha256": hashlib.sha256(LOG.read_bytes()).hexdigest()}, indent=1))
