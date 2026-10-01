#!/usr/bin/env python3
"""Merge the landed FINAL REMEDIATION adjudications into ONE proposal and ONE claim-accounting file for the gate and harness.

Refuses unless: every slice named has landed durably; the proposals touch disjoint rows; every proposed row belongs to its
own slice (lane A's slice file carries all of the slice's rows); and claim accountings are keyed by rows of their own slice.
Writes Ezek/author/final/merged/{proposal.json, claim_accounting.json}; refuses to overwrite different bytes (E-41).

usage: python merge_final_slices.py --slices 1,2,3,4,5,6
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
A = EZ / "author" / "final"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
KS = [int(x) for x in sys.argv[sys.argv.index("--slices") + 1].split(",")]
merged, acc, seen = {}, {}, {}
for k in KS:
    d = A / ("s%d_adjudication" % k)
    for n in ("proposal.json", "adjudication.json"):
        if not (d / n).is_file():
            raise SystemExit("REFUSED: slice %d adjudication has not landed (%s)" % (k, n))
    prop = json.loads((d / "proposal.json").read_text(encoding="utf-8"))
    ca = json.loads((d / "adjudication.json").read_text(encoding="utf-8")).get("claim_accounting") or {}
    owned = set(json.loads((HERE / ("final_slices_s%d_laneA.v1.json" % k)).read_text(encoding="utf-8"))["slices"])
    stray = sorted(set(prop) - owned) + sorted(set(ca) - owned)
    if stray:
        raise SystemExit("REFUSED: slice %d proposes or accounts rows outside its slice: %s" % (k, stray))
    clash = sorted(set(prop) & set(merged))
    if clash:
        raise SystemExit("REFUSED: slice %d overlaps slice %s on %s" % (k, [seen[r] for r in clash], clash))
    for r in prop:
        seen[r] = k
    merged.update(prop)
    acc.update(ca)
out = A / "merged"
out.mkdir(parents=True, exist_ok=True)
for name, obj in (("proposal.json", merged), ("claim_accounting.json", {"claim_accounting": acc})):
    data = json.dumps(obj, ensure_ascii=False, indent=1).encode("utf-8")
    p = out / name
    if p.exists() and p.read_bytes() != data:
        raise SystemExit("REFUSED: %s exists with different bytes (E-41)" % p)
    p.write_bytes(data)
print(json.dumps({"slices": KS, "rows": len(merged), "fields": sum(len(v) for v in merged.values()), "accounted_rows": len(acc),
                  "proposal_sha256": sha(out / "proposal.json"), "claim_accounting_sha256": sha(out / "claim_accounting.json")}, indent=1))
