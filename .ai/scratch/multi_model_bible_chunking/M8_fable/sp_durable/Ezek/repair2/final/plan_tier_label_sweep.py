#!/usr/bin/env python3
"""Plan the TIER-LABEL deletion sweep (#e16: 'Evidence-tier labels tier-1/3/4 are strategy scale labels and are BARRED').
Plan only; the proposal is applied by apply_proposal.py after the suite judges the candidate.

A label is removed ONLY by one of the fixed rules below, each of which leaves a sentence that says what it said without the
scale word (the noun after the label already names the evidence, or the single-witness disclosure stays). Every other
occurrence is left in place and listed for the final remediation authors - a mechanical sweep never rewrites a claim.

usage: python plan_tier_label_sweep.py [--selftest]
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
FIELDS = ("boundary_rationale", "strongest_rejected_alternative", "device_notes", "literature_type_guess", "boundary_evidence_refs")
RULES = [
    (re.compile(r"\(tier-3, single-witness\)"), "(single-witness)"),
    (re.compile(r"single-witness, tier-3\)"), "single-witness)"),
    (re.compile(r"\btier-3,? single-witness"), "single-witness"),
    (re.compile(r"\btier-1 (formula|sign-act|address device|vision onset|vision transport|transport-verb)"), r"\1"),
    (re.compile(r"\btier-4 (texture|translation layout)"), r"\1"),
    (re.compile(r"\btier-4 paragraphing"), "WEB paragraphing"),
    (re.compile(r"; tier-3 disclosure, not deciding"), "; a disclosure, not deciding"),
]
LABEL = re.compile(r"\btier[- ]\d\b")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731


def sweep_text(t):
    n = 0
    for pat, rep in RULES:
        t, k = pat.subn(rep, t)
        n += k
    return t, n


def selftest():
    cases = [("(tier-3, single-witness)", "(single-witness)"), ("pe follows, tier-3 single-witness; device", "pe follows, single-witness; device"),
             ("disclosure: tier-1 formula (sweep: 7 verses)", "disclosure: formula (sweep: 7 verses)"),
             ("[ANCHOR] tier-4 paragraphing, texture only", "[ANCHOR] WEB paragraphing, texture only"),
             ("would read tier-4 translation structure as tier-1 evidence", "would read tier-4 translation structure as tier-1 evidence"),
             ("a clean tier-1 onset", "a clean tier-1 onset"), ("disclosure: tier-1 (sweep: 93 verses)", "disclosure: tier-1 (sweep: 93 verses)")]
    failed = [(a, sweep_text(a)[0]) for a, want in cases if sweep_text(a)[0] != want]
    print(json.dumps({"selftest_cases": len(cases), "failed": failed}, ensure_ascii=False, indent=1))
    return 1 if failed else 0


if "--selftest" in sys.argv:
    raise SystemExit(selftest())
if selftest():
    raise SystemExit("REFUSED: selftest failed (E-36)")
rows = [json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip()]
proposal, left, removed = {}, [], 0
for r in rows:
    for f in FIELDS:
        v = r.get(f)
        if isinstance(v, list):
            new = []
            for i, e in enumerate(v):
                t, n = sweep_text(e)
                removed += n
                new.append(t)
                left += [{"row": r["decision_id"], "field": "%s[%d]" % (f, i), "label": m.group(0), "context": t[max(0, m.start() - 60):m.end() + 60]} for m in LABEL.finditer(t)]
            if new != v:
                proposal.setdefault(r["decision_id"], {})[f] = new
        elif isinstance(v, str):
            t, n = sweep_text(v)
            removed += n
            left += [{"row": r["decision_id"], "field": f, "label": m.group(0), "context": t[max(0, m.start() - 60):m.end() + 60]} for m in LABEL.finditer(t)]
            if t != v:
                proposal.setdefault(r["decision_id"], {})[f] = t
out = HERE / "tier_label_sweep"
out.mkdir(exist_ok=True)
(out / "proposal.json").write_text(json.dumps(proposal, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
(out / "left_for_authors.json").write_text(json.dumps({"rows_sha256": sha(ROWS), "labels_left": left}, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"rows_sha256": sha(ROWS), "labels_removed": removed, "rows_in_proposal": len(proposal), "labels_left_for_authors": len(left),
                  "proposal_sha256": sha(out / "proposal.json")}, indent=1))
