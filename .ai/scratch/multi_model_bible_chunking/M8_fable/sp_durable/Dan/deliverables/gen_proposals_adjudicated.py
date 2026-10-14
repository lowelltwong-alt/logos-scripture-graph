#!/usr/bin/env python3
"""Join Daniel's eight method-change proposals to their adjudications (close-gate item 23).

Reads the proposer's candidate file and the adjudicator's record, both landed and both pinned here by sha256, and
writes method_change_proposals.Dan.adjudicated.jsonl beside this tool: each proposal row unchanged except that
`adjudication` is filled from the adjudicator's record and `landed_in_version` names the method version that carries
an adopted text. It authors nothing: every value is copied. The proposer's bytes and the adjudicator's bytes are not
modified. Appending these rows to the campaign's shared proposal log is not done here.

Usage: gen_proposals_adjudicated.py [--check]
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DAN = HERE.parent
CAND = DAN / "close" / "landed" / "D3_e1" / "method_change_proposals.Dan.candidate.jsonl"
CAND_SHA = "3e236361de698bc39268949b8bcaa8267cd2eafc3fbcfeb745949419863d8a9f"
ADJ = DAN / "close" / "landed" / "D5_e1" / "method_change_adjudications.Dan.v1.json"
ADJ_SHA = "efc1b89b4a504618ef3efa23471aabfeaad4dd6dfb338f7f70eeca7516ba0cae"
OUT = HERE / "method_change_proposals.Dan.adjudicated.jsonl"
VERSION = "v7"
# The adjudicator's record carries no time of its own. This is the time the orchestrator's landing receipt was recorded.
LANDED_AT = "2026-10-13T16:32:13Z"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def build():
    cb, ab = CAND.read_bytes(), ADJ.read_bytes()
    if sha(cb) != CAND_SHA or sha(ab) != ADJ_SHA:
        sys.exit("FAIL: an input is not the bytes this tool pins")
    d = json.loads(ab.decode("utf-8"))
    adj = {a["proposal_id"]: a for a in d["adjudications"]}
    rows = [json.loads(ln) for ln in cb.decode("utf-8").splitlines() if ln.strip()]
    if [r["proposal_id"] for r in rows] != list(adj) or len(rows) != d["rates"]["proposed"]:
        sys.exit("FAIL: the proposals and the adjudications do not pair one to one in order")
    out = []
    for r in rows:
        if r["adjudication"] is not None or r["landed_in_version"] is not None:
            sys.exit("FAIL: %s was not unadjudicated in the candidate file" % r["proposal_id"])
        a = adj[r["proposal_id"]]
        r["adjudication"] = {
            "verdict": a["verdict"], "rating": a["rating"], "by": d["execution_id"], "at": LANDED_AT,
            "at_is": "the time the landing receipt was recorded; the adjudicator's record carries no time",
            "reasons": a["reasons"], "admissible": a["admissible"],
            "adopted_text_differs_from_proposal": a["adopted_text_differs_from_proposal"],
            "target_section_as_adopted": a["target_section"] if a["verdict"] == "ADOPT" else None,
            "model": d["model"], "grader_fallback": d["grader_fallback"],
            "record": "sp_durable/Dan/close/landed/D5_e1/method_change_adjudications.Dan.v1.json",
            "record_sha256": ADJ_SHA,
        }
        r["landed_in_version"] = VERSION if a["verdict"] == "ADOPT" else None
        out.append(json.dumps(r, ensure_ascii=False))
    return ("\n".join(out) + "\n").encode("utf-8")


def main():
    data = build()
    if "--check" in sys.argv:
        ok = OUT.is_file() and sha(OUT.read_bytes()) == sha(data)
        print("%s %s: %s" % (OUT.name, sha(data)[:16], "MATCH" if ok else "DIFFER"))
        sys.exit(0 if ok else 1)
    if OUT.is_file() and sha(OUT.read_bytes()) != sha(data):
        sys.exit("REFUSED: %s exists with other bytes" % OUT.name)
    OUT.write_bytes(data)
    print("%s sha256 %s rows %d" % (OUT.name, sha(data), data.count(b"\n")))


if __name__ == "__main__":
    main()
