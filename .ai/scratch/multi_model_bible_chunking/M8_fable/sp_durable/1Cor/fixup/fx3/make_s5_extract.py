#!/usr/bin/env python3
"""Build 1Cor/review/tool_fixes/s5_receipt_extract.v1.json: whitelisted fields of the review receipts from the round-4
landing to the last row, with every (path, digest) pair classed against the bytes now on disk.

A launch row loses its runtime id, its message file and its OUT directory; a completion keeps its checks and outputs. A
pair is match, crlf_form (ledger E-73), superseded (a later row of the same tool records the bytes now on disk) or drift.
Run once all six FIXUP-3 parts have landed and been applied, after the coverage report row, before the S5 brief is built.
usage: make_s5_extract.py FIRST_LINE
"""
import datetime
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
BK = HERE.parents[1]
SP = BK.parent
R = BK / "review"
REC = R / "1cor_review_attempt_receipts.jsonl"
OUT = R / "tool_fixes" / "s5_receipt_extract.v1.json"
DROP = {"agent_id", "parent_agent_id", "launch_message", "output_dir", "agent", "effort", "tokens_unit_note"}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def pairs(v, out):
    if isinstance(v, dict):
        p = v.get("path")
        for k in ("sha256", "after_sha256"):
            if isinstance(p, str) and isinstance(v.get(k), str):
                out.append((p, v[k]))
        for x, y in (("brief", "brief_sha256"), ("installed_path", "output_sha256")):
            if isinstance(v.get(x), str) and isinstance(v.get(y), str):
                out.append((v[x], v[y]))
        for x in v.values():
            pairs(x, out)
    elif isinstance(v, list):
        for x in v:
            pairs(x, out)


def main():
    first = int(sys.argv[1])
    lines = [x for x in REC.read_text(encoding="utf-8").splitlines() if x.strip()]
    rows = []
    for n, x in enumerate(lines, 1):
        if n >= first:
            r = json.loads(x)
            rows.append(dict({k: v for k, v in r.items() if k not in DROP}, receipt_line=n))
    got = []
    pairs(rows, got)
    uniq = sorted(set(got))
    classes = []
    counts = {}
    for path, want in uniq:
        f = SP / path[len("sp_durable/"):] if path.startswith("sp_durable/") else None
        if f is None or not f.is_file():
            c = "not_on_disk"
        else:
            b = f.read_bytes()
            lf = b.replace(b"\r\n", b"\n")
            if sha(b) == want:
                c = "match"
            elif sha(lf.replace(b"\n", b"\r\n")) == want:
                c = "crlf_form"
            elif any(p == path and sha(b) == s for p, s in uniq):
                c = "superseded"
            else:
                c = "drift"
        counts[c] = counts.get(c, 0) + 1
        classes.append({"path": path, "sha256": want, "class": c})
    d = {"schema": "m8_receipt_extract.v1", "book": "1Cor",
         "source": {"path": "sp_durable/1Cor/review/" + REC.name, "sha256": sha(REC.read_bytes()), "lines": [first, len(lines)]},
         "whitelist": {"dropped_keys": sorted(DROP)},
         "built_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "built_by": "1Cor/fixup/fx3/make_s5_extract.py",
         "rows": rows, "orchestrator_measured": {"pairs": len(uniq), "counts": counts, "classes": classes}}
    OUT.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"rows": len(rows), "pairs": len(uniq), "counts": counts, "sha256": sha(OUT.read_bytes())}))


main()
