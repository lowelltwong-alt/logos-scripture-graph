"""Form check of a FIXUP-9 re-review packet (Daniel). Form only; it never judges a verdict, a grade or a check answer.
Usage: python -B rr9_form_check.py DELIVERABLE LANE EXECUTION_ID"""
import json
import sys
from pathlib import Path

TIERS = {"MEASURED", "EXTRACTED", "TRANSCRIBED", "REPORTED", "INFERRED", "ASSUMED"}


def verify(doc, want, aid, xid, lane, rows_sha):
    p = []
    for k, v in (("attempt_id", aid), ("execution_id", xid), ("book", "Dan"), ("role", "rr9_" + lane)):
        if doc.get(k) != v:
            p.append("%s is %r, expected %r" % (k, doc.get(k), v))
    if (doc.get("rows_file") or {}).get("sha256") != rows_sha:
        p.append("rows_file.sha256 is not the pinned rows digest")
    if doc.get("records_reviewed") != want:
        p.append("records_reviewed is not exactly the extract's records in order")
    items = doc.get("items")
    if not isinstance(items, list) or not all(isinstance(i, dict) for i in items):
        return p + ["items is not a list of objects"], None
    if [i.get("record") for i in items] != want:
        p.append("items are not exactly one per record, in order")
    tally = {"supports": 0, "challenges": 0, "by_severity": {"high": 0, "medium": 0, "low": 0}}
    text = lambda v: isinstance(v, str) and bool(v.strip())  # noqa: E731

    def body(i, tag, need_sev):
        if need_sev and i.get("severity") not in ("high", "medium", "low"):
            p.append("%s: no severity of high/medium/low" % tag)
        for k in ("claim", "decision"):
            if not text(i.get(k)):
                p.append("%s: empty %s" % (tag, k))
        if i.get("tier") not in TIERS:
            p.append("%s: tier %r is not in the list" % (tag, i.get("tier")))
        ev = i.get("evidence")
        if not (isinstance(ev, list) and ev and all(text(e) for e in ev)):
            p.append("%s: evidence is not a non-empty list of strings" % tag)

    for i in items:
        v = i.get("verdict")
        if v not in ("support", "challenge"):
            p.append("%s: verdict %r" % (i.get("record"), v))
        if v == "challenge":
            tally["challenges"] += 1
            if i.get("severity") in tally["by_severity"]:
                tally["by_severity"][i["severity"]] += 1
        elif v == "support":
            tally["supports"] += 1
            if "severity" in i:
                p.append("%s: severity present on a support" % i.get("record"))
        body(i, i.get("record"), v == "challenge")
        if not isinstance(i.get("asks_row_change"), bool):
            p.append("%s: asks_row_change is not a boolean" % i.get("record"))
        if not text(i.get("bytes_read")):
            p.append("%s: bytes_read is not a non-empty string" % i.get("record"))
    xf = doc.get("extra_findings")
    if not isinstance(xf, list) or not all(isinstance(i, dict) for i in xf):
        p.append("extra_findings is not a list of objects")
    else:
        for n, i in enumerate(xf):
            body(i, "extra_findings[%d]" % n, True)
    s = doc.get("summary") or {}
    got = {"supports": s.get("supports"), "challenges": s.get("challenges"),
           "by_severity": {k: (s.get("by_severity") or {}).get(k, 0) for k in ("high", "medium", "low")}}
    if got != tally:
        p.append("summary %r does not equal the recomputed %r" % (got, tally))
    ck = doc.get("checks")
    if not isinstance(ck, dict):
        p.append("checks is not an object")
    else:
        ae = ck.get("after_text_equal")
        if not (isinstance(ae, list) and all(isinstance(t, dict) for t in ae) and [t.get("record") for t in ae] == want
                and all(isinstance(t.get("equal"), bool) and text(t.get("bytes_read")) for t in ae)):
            p.append("checks.after_text_equal is not one object per record in order, each with a boolean equal and bytes_read")
        for key, flag in (("w3_010_reason_not_under_mark_extracted", "holds"), ("w4_004_entry_agrees_with_verse_and_inventory", "agrees")):
            t = ck.get(key)
            if not (isinstance(t, dict) and isinstance(t.get(flag), bool) and text(t.get("bytes_read"))):
                p.append("checks.%s is not an object with a boolean %s and bytes_read" % (key, flag))
    if not text(doc.get("e19_selfreport")):
        p.append("no e19_selfreport")
    if not isinstance(doc.get("unresolved_uncertainty"), list):
        p.append("unresolved_uncertainty is not a list")
    if not doc.get("limit"):
        p.append("no limit")
    return p, tally


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    deliv, lane, xid = sys.argv[1:4]
    b = Path(deliv).read_bytes()
    ext = json.loads(Path(__file__).with_name("fixup9_changes_for_review.json").read_bytes().decode("utf-8"))
    probs = ["CR byte in the deliverable; write LF only"] if bytes([13]) in b else []
    try:
        doc = json.loads(b.decode("utf-8"))
    except ValueError as e:
        doc, probs = None, probs + ["deliverable is not JSON: %s" % e]
    tally = None
    if isinstance(doc, dict):
        more, tally = verify(doc, [r["record"] for r in ext["records"]], xid.split("#")[0], xid, lane, ext["applied_rows"]["sha256"])
        probs += more
    elif doc is not None:
        probs.append("deliverable is not an object")
    print(json.dumps({"form_problems": probs, "tally": tally}, ensure_ascii=False))
