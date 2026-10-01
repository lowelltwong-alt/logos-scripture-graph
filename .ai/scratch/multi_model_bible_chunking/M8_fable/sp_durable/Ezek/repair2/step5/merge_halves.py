#!/usr/bin/env python3
"""Merge the two landed step-5 adjudications into ONE proposal and ONE claim-accounting file for the gate and harness.

Refuses unless: both adjudications have landed durably; their proposals touch disjoint rows; every proposed row
belongs to its own half's slices; and the claim accountings are keyed by rows of their own half. Writes
Ezek/author/repair2_step5/merged/{proposal.json, claim_accounting.json} and prints both digests.

usage: python merge_halves.py
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
A = EZ / "author" / "repair2_step5"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
props, accs, owned = {}, {}, {}
for h in (1, 2):
    d = A / ("h%d_adjudication" % h)
    for n in ("proposal.json", "adjudication.json"):
        if not (d / n).is_file():
            raise SystemExit("REFUSED: half %d adjudication has not landed (%s)" % (h, n))
    props[h] = json.loads((d / "proposal.json").read_text(encoding="utf-8"))
    accs[h] = json.loads((d / "adjudication.json").read_text(encoding="utf-8")).get("claim_accounting") or {}
    owned[h] = set(json.loads((HERE / ("step5_slices_half%d.v1.json" % h)).read_text(encoding="utf-8"))["slices"])
    stray = sorted(set(props[h]) - owned[h])
    if stray:
        raise SystemExit("REFUSED: half %d proposes rows outside its slices: %s" % (h, stray))
    stray_acc = sorted(set(accs[h]) - owned[h])
    if stray_acc:
        raise SystemExit("REFUSED: half %d accounts claims on rows outside its slices: %s" % (h, stray_acc))
overlap = sorted(set(props[1]) & set(props[2]))
if overlap:
    raise SystemExit("REFUSED: the halves' proposals overlap on %s" % overlap)
merged = dict(props[1], **props[2])
acc = dict(accs[1], **accs[2])
out = A / "merged"
out.mkdir(parents=True, exist_ok=True)
(out / "proposal.json").write_text(json.dumps(merged, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
(out / "claim_accounting.json").write_text(json.dumps({"claim_accounting": acc}, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"rows": len(merged), "rows_half1": len(props[1]), "rows_half2": len(props[2]),
                  "fields": sum(len(v) for v in merged.values()), "accounted_rows": len(acc),
                  "proposal_sha256": sha(out / "proposal.json"), "claim_accounting_sha256": sha(out / "claim_accounting.json")}, indent=1))
