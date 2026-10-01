"""Check a brief's deliverable schema against the landing validator that will judge the deliverable, and refuse on disagreement.

The control this implements (learning log L-0018): a brief's deliverable schema and the landing tool's validator are two statements of one
contract. S4's brief was copied from S3's template and launched with four keys validate_s4 refuses - cwo23_pairs for cwo_ez_23_pairs,
mark_sample for mark_disclosures, a flat cwo_recomputed for cwo_recomputed.residuals, and p04_008_readback.verdict as accept|defect where
cured|not_cured is required. The template was right for its own job and wrong for the next one. Nothing caught it; the execution was already
running when a human read of the validator found it.

WHAT IT CHECKS, mechanically and without judgment:
  - TOP-LEVEL KEYS. Every `d.get("<key>")` in the validator's own function body is a key the deliverable must carry. Each must appear as a
    key in the brief's deliverable schema block. A missing one is a REFUSAL - that is exactly the cwo23_pairs and mark_sample class.
  - NESTED ACCESSES, reported not enforced. The validator's other `.get("<name>")` calls (residuals, p03, others, runs, shapes, ...) are
    listed so the orchestrator reads them against the schema by eye. They cannot be bound mechanically to a parent key without parsing the
    validator's data flow, and this tool does not pretend to: it says what it checked and what it only reported.
  - LITERAL SETS. Allowed-value tuples the validator compares against (cured|not_cured and the like) are printed beside the keys they are
    tested on where the line makes that plain, again as a report.

The brief's schema block is the first fenced block after its '## Deliverable' heading. Keys are taken as every "name": in that block, which
is a superset - a key the brief carries at any depth counts as present, so this tool under-reports rather than over-refuses.

Exit 1 when a required top-level key is missing from the brief, so a builder can make this a hard stop before launch.

Usage: check_brief_schema_vs_validator.py --brief <brief.md> --validator <_land_rulings_and_t1.py> --job s4
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def validator_body(text, job):
    m = re.search(r"^def validate_%s\(.*?$" % re.escape(job), text, re.M)
    if not m:
        raise SystemExit("ABORT: the validator has no validate_%s function" % job)
    start = m.start()
    nxt = re.search(r"^def \w+\(", text[m.end():], re.M)
    return text[start:m.end() + nxt.start()] if nxt else text[start:]


def brief_schema_block(text):
    i = text.find("## Deliverable")
    if i < 0:
        raise SystemExit("ABORT: the brief has no '## Deliverable' heading")
    j = text.find("```", i)
    k = text.find("```", j + 3)
    if j < 0 or k < 0:
        raise SystemExit("ABORT: the brief's deliverable section has no fenced schema block")
    return text[j + 3:k]


ap = argparse.ArgumentParser()
ap.add_argument("--brief", required=True)
ap.add_argument("--validator", required=True)
ap.add_argument("--job", required=True)
a = ap.parse_args()

vtext = Path(a.validator).read_text(encoding="utf-8")
btext = Path(a.brief).read_text(encoding="utf-8")
body = validator_body(vtext, a.job)
block = brief_schema_block(btext)

required = sorted(set(re.findall(r'\bd\.get\("([A-Za-z0-9_]+)"', body)))
nested = sorted(set(re.findall(r'\.get\("([A-Za-z0-9_]+)"', body)) - set(required))
in_brief = set(re.findall(r'"([A-Za-z0-9_]+)"\s*:', block))
missing = [k for k in required if k not in in_brief]
present = [k for k in required if k in in_brief]
nested_missing = [k for k in nested if k not in in_brief]
literals = sorted({t for t in re.findall(r'\(\s*"cured",\s*"not_cured"[^)]*\)|\(\s*"accept",\s*"defect"\s*\)', body)})

report = {
    "schema": "m8_brief_schema_check.v1", "job": a.job,
    "brief": {"path": str(a.brief), "sha256": sha(a.brief)[:16]},
    "validator": {"path": str(a.validator), "sha256": sha(a.validator)[:16], "function": "validate_%s" % a.job},
    "checked": {"required_top_level_keys": len(required), "present_in_brief": len(present), "missing_from_brief": missing},
    "reported_not_enforced": {
        "nested_keys_the_validator_reads": nested,
        "nested_keys_absent_from_the_brief_block": nested_missing,
        "why": "a nested name cannot be bound to its parent key without following the validator's data flow; read these by eye",
        "allowed_value_tuples_seen": literals},
    "verdict": "REFUSED" if missing else "AGREES_ON_TOP_LEVEL_KEYS",
    "limit": ("top-level key NAMES only. A key present under the right name but the wrong shape - a flat dict where the validator wants a "
              "sub-dict, or an allowed-value set the brief states differently - is NOT caught here and is what the nested report is for."),
}
print(json.dumps(report, ensure_ascii=False, indent=1))
sys.exit(1 if missing else 0)
