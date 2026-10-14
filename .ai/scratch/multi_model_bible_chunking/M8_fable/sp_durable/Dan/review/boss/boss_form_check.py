"""Form check of the Daniel boss-audit packet. Tests FORM only; never a verdict.
  python -B boss_form_check.py DELIVERABLE EXECUTION_ID
Reads the deliverable and the applied rows file beside the pinned paths only. Prints {"form_problems": [...], "tally": {...}}."""
import hashlib
import json
import sys
from pathlib import Path

SP = Path(__file__).resolve().parents[3]
ROWS = SP / "Dan" / "fixup" / "draft_rows_fixup10_applied.jsonl"
TIERS = {"MEASURED", "EXTRACTED", "TRANSCRIBED", "REPORTED", "INFERRED", "ASSUMED"}
CV = {"MET", "NOT_MET", "NOT_TESTABLE"}
SEV = {"high", "medium", "low"}
BIDS = ["B%d" % i for i in range(1, 18)]


def s(x):
    return isinstance(x, str) and bool(x.strip())


def sl(x):
    return isinstance(x, list) and bool(x) and all(s(i) for i in x)


def verify(doc, row_ids, aid, xid, rows_sha):
    p = []
    if doc.get("attempt_id") != aid or doc.get("execution_id") != xid:
        p.append("attempt_id or execution_id is not %s / %s" % (aid, xid))
    if doc.get("book") != "Dan" or doc.get("role") != "boss_audit":
        p.append("book is not Dan or role is not boss_audit")
    rf = doc.get("rows_file")
    if not isinstance(rf, dict) or rf.get("sha256") != rows_sha:
        p.append("rows_file.sha256 is not the digest of the applied rows file")
    cs = doc.get("conditions")
    if not isinstance(cs, list) or [c.get("id") if isinstance(c, dict) else None for c in cs] != BIDS:
        p.append("conditions is not the 17 objects B1..B17 in order")
        cs = []
    for c in cs:
        if c.get("verdict") not in CV or c.get("tier") not in TIERS or not s(c.get("how")) or not sl(c.get("evidence")) or not s(c.get("bytes_read")):
            p.append("condition %s: verdict, tier, how, evidence (non-empty list of strings) or bytes_read (string) missing or malformed" % c.get("id"))
    rs = doc.get("rows")
    if not isinstance(rs, list) or [r.get("row") if isinstance(r, dict) else None for r in rs] != row_ids:
        p.append("rows is not one object per row of the applied file, in file order, keyed row")
        rs = []
    for r in rs:
        fs = r.get("findings")
        if r.get("verdict") not in ("CONFIRM", "RETURN") or not s(r.get("why")) or not isinstance(fs, list):
            p.append("row %s: verdict, why or findings (a list) missing or malformed" % r.get("row"))
            continue
        for f in fs:
            if not isinstance(f, dict) or f.get("severity") not in SEV or f.get("tier") not in TIERS or not s(f.get("field")) \
                    or not s(f.get("claim")) or not sl(f.get("evidence")) or "already_routed" not in f:
                p.append("row %s: a finding lacks field, severity, claim, tier, evidence (non-empty list) or already_routed (null or an id)" % r.get("row"))
        if r["verdict"] == "RETURN" and not s(r.get("work_order")):
            p.append("row %s: RETURN without work_order" % r.get("row"))
        if r["verdict"] == "CONFIRM" and r.get("work_order"):
            p.append("row %s: CONFIRM with a work_order" % r.get("row"))
    for k in ("reported_where_measured", "escalations", "verification_evidence", "unresolved_uncertainty", "parts_read"):
        if not isinstance(doc.get(k), list):
            p.append("%s is not a list" % k)
    for k in ("changes_made_or_no_change", "e19_selfreport", "limit"):
        if not s(doc.get(k)):
            p.append("%s is not a non-empty string" % k)
    tally = {"conditions": {v: sum(1 for c in cs if c.get("verdict") == v) for v in sorted(CV)},
             "rows": {v: sum(1 for r in rs if r.get("verdict") == v) for v in ("CONFIRM", "RETURN")},
             "findings": {v: sum(1 for r in rs for f in (r.get("findings") or []) if isinstance(f, dict) and f.get("severity") == v) for v in sorted(SEV)}}
    o = doc.get("overall")
    if not isinstance(o, dict) or o.get("verdict") not in ("CONFIRM", "RETURN"):
        p.append("overall.verdict is not CONFIRM or RETURN")
    elif cs and rs:
        want = "CONFIRM" if tally["conditions"]["MET"] == 17 and tally["rows"]["RETURN"] == 0 else "RETURN"
        if o["verdict"] != want:
            p.append("overall.verdict is %s but the conditions and rows of this packet give %s" % (o["verdict"], want))
        if o.get("conditions_met") != tally["conditions"]["MET"] or o.get("rows_confirm") != tally["rows"]["CONFIRM"] or o.get("rows_return") != tally["rows"]["RETURN"]:
            p.append("overall counts do not equal the counts of this packet's own conditions and rows")
    return p, tally


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    b = Path(sys.argv[1]).read_bytes()
    probs = ["CR byte in the deliverable"] if bytes([13]) in b else []
    rb = ROWS.read_bytes()
    ids = [json.loads(x)["writer_decision_id"] for x in rb.decode("utf-8").split("\n") if x]
    try:
        d = json.loads(b.decode("utf-8"))
    except ValueError as e:
        d, probs = None, probs + ["not JSON: %s" % e]
    t = None
    if isinstance(d, dict):
        pp, t = verify(d, ids, sys.argv[2].split("#")[0], sys.argv[2], hashlib.sha256(rb).hexdigest())
        probs += pp
    elif d is not None:
        probs.append("not an object")
    print(json.dumps({"form_problems": probs, "tally": t}))
