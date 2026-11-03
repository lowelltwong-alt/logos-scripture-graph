"""Build the landing row (m8_attempt_receipt.v1 completion) of one 1Cor primary lane from the deliverable's bytes plus
notification facts. Derived from P/cor_w/make_ctl_landing.py (same row shape); the checks are the primary brief's
deliverable contract (SP/1Cor/review/PRIMARY_BRIEF.template.md), MEASURED here:
  one JSON object, no CR; every top-level key; attempt, execution, book, role and cluster equal the brief's; the rows
  digest equals the round's pin; rows_reviewed and the items' row_ids each equal the cluster's rows exactly once;
  verdict in {support, challenge}; severity in {high, medium, low} present exactly on a challenge; a non-empty claim; a
  tier from the brief's list; a non-empty evidence list; summary equals the recount; exactly one triage answer per id;
  every Greek-script phrase (Greek words joined by single spaces) in any string is an exact substring of the RP or SBLGNT
  witness (raw bytes, or the verse texts joined by a space for a cross-verse run). A phrase found only after NFC
  normalisation is listed as a warning, not a problem. A failing deliverable is still landed and the row records each
  failure. notification_time is stamped by this script's clock.

usage: make_primary_landing.py --lane OL --cluster c01 --agent-id ID --tokens N --tool-uses N --duration-ms N
       --outcome TEXT --summary TEXT [--note TEXT ...] --out FILE
"""
import argparse
import datetime
import hashlib
import json
import re
import unicodedata
from pathlib import Path

P = Path("C:/Users/lowel/AppData/Local/Temp/claude/C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View/"
         "af84b702-d913-4495-8e57-252cf7894c63/scratchpad")  # worker deliverables stay here until landed
BK = Path("C:/wt/logos-t423-m8-fable/.ai/scratch/multi_model_bible_chunking/M8_fable/sp_durable/1Cor")
ROWS_SHA = "75933a142375d8736ae71cdcc7f0e0b9052c36ea4ac4b87ccacf676ae50c6fbe"
PLAN_SHA = "a393f453f58d956b6d0951b513416f6678b0a78f445a796254f43ee718a17101"
KEYS = ("attempt_id", "execution_id", "book", "role", "cluster", "model_ordered", "rows_file", "artifacts_reviewed",
        "rows_reviewed", "items", "triage_answers", "summary", "unresolved_uncertainty", "e19_selfreport", "limit")
TIERS = {"MEASURED", "EXTRACTED", "TRANSCRIBED", "REPORTED", "INFERRED", "ASSUMED"}
SEV = {"high", "medium", "low"}
TIDS = ["TRIAGE-1COR-01", "TRIAGE-1COR-02"]
GW = r"[\u0370-\u03FF\u1F00-\u1FFF][\u0370-\u03FF\u1F00-\u1FFF\u0300-\u036F\u0342-\u0345\u2019\u02BC]*"
GPH = re.compile(GW + r"(?: " + GW + r")*")
ap = argparse.ArgumentParser()
for k in ("--lane", "--cluster", "--agent-id", "--outcome", "--summary", "--out"):
    ap.add_argument(k, required=True)
for k in ("--tokens", "--tool-uses", "--duration-ms"):
    ap.add_argument(k, required=True, type=int)
ap.add_argument("--note", action="append", default=[])
ap.add_argument("--file", help="fixture tests only: check this deliverable instead of the lane's OUT path")
a = ap.parse_args()
h = lambda b: hashlib.sha256(b).hexdigest()
pb = (BK / "review_clusters.json").read_bytes()
if h(pb) != PLAN_SHA:
    raise SystemExit("REFUSED: the cluster plan digest differs from the pin")
plan = json.loads(pb.decode("utf-8"))
cl = {c["id"]: c for c in plan["clusters"]}[a.cluster]
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
tag = "%s_%s" % (a.lane, a.cluster)
att = "cor_primary_%s_a1" % tag.lower()
eid = att + "#e1"
out_dir = P / "cor_prim" / (tag + "_e1")
f = Path(a.file) if a.file else out_dir / ("final_%s_e1.json" % tag)
problems, warnings, d, b = [], [], None, b""
if f.is_file() and not a.file:  # the scratchpad is not durable (2026-10-31 purge): keep the landed bytes beside the receipts
    (BK / "review" / "primaries" / "finals").mkdir(exist_ok=True)
    (BK / "review" / "primaries" / "finals" / f.name).write_bytes(f.read_bytes())
if not f.is_file():
    problems.append("deliverable absent")
else:
    b = f.read_bytes()
    if b"\r" in b:
        problems.append("CR bytes %d" % b.count(b"\r"))
    try:
        d = json.loads(b.decode("utf-8"))
    except ValueError as e:
        problems.append("not JSON: %s" % e)
wit = {}
for w in ("rp", "sbl"):
    t = (BK / ("1Cor_%s.txt" % w)).read_text(encoding="utf-8")
    joined = " ".join(x.split("\t", 1)[1] for x in t.splitlines() if "\t" in x)
    wit[w] = (t, joined, unicodedata.normalize("NFC", t + "\n" + joined))


def strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values():
            yield from strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from strings(v)


summ, greek = None, {"phrases": 0, "found_raw": 0, "found_nfc_only": 0, "missing": 0}
if isinstance(d, dict):
    problems += ["missing key %s" % k for k in KEYS if k not in d]
    want = {"attempt_id": att, "execution_id": eid, "book": "1Cor", "role": "primary_" + a.lane, "cluster": a.cluster}
    problems += ["%s %r" % (k, d.get(k)) for k, v in want.items() if d.get(k) != v]
    if not isinstance(d.get("rows_file"), dict) or d["rows_file"].get("sha256") != ROWS_SHA:
        problems.append("rows_file.sha256 is not the round's pin")
    if sorted(d.get("rows_reviewed") or []) != sorted(cl["row_ids"]):
        problems.append("rows_reviewed differs from the cluster")
    items = d.get("items") if isinstance(d.get("items"), list) else []
    rid = [i.get("row_id") if isinstance(i, dict) else None for i in items]
    problems += ["no item for %s" % r for r in cl["row_ids"] if r not in rid]
    problems += ["item for a row outside the cluster: %r" % r for r in rid if r not in cl["row_ids"]]
    problems += ["%d items for %s" % (rid.count(r), r) for r in sorted(set(rid), key=str) if rid.count(r) > 1]
    rec = {"supports": 0, "challenges": 0, "by_severity": {"high": 0, "medium": 0, "low": 0}}
    for i in items:
        if not isinstance(i, dict):
            problems.append("an item is not an object")
            continue
        r, v = i.get("row_id"), i.get("verdict")
        if v == "support":
            rec["supports"] += 1
            if "severity" in i:
                problems.append("%s: severity on a support" % r)
        elif v == "challenge":
            rec["challenges"] += 1
            if i.get("severity") in SEV:
                rec["by_severity"][i["severity"]] += 1
            else:
                problems.append("%s: severity %r on a challenge" % (r, i.get("severity")))
        else:
            problems.append("%s: verdict %r" % (r, v))
        if not (isinstance(i.get("claim"), str) and i["claim"].strip()):
            problems.append("%s: empty claim" % r)
        if i.get("tier") not in TIERS:
            problems.append("%s: tier %r" % (r, i.get("tier")))
        if not (isinstance(i.get("evidence"), list) and i["evidence"]):
            problems.append("%s: empty evidence" % r)
    summ = rec
    if d.get("summary") != rec:
        problems.append("summary %r differs from the recount %r" % (d.get("summary"), rec))
    ta = [t.get("id") if isinstance(t, dict) else None for t in (d.get("triage_answers") or [])]
    if sorted(ta, key=str) != TIDS:
        problems.append("triage_answers ids %r" % ta)
    for s in strings(d):
        for ph in GPH.findall(s):
            greek["phrases"] += 1
            if any(ph in raw or ph in jn for raw, jn, _ in wit.values()):
                greek["found_raw"] += 1
            elif any(unicodedata.normalize("NFC", ph) in nf for _, _, nf in wit.values()):
                greek["found_nfc_only"] += 1
                warnings.append("Greek phrase found only after NFC: %s" % ph)
            else:
                greek["missing"] += 1
                problems.append("Greek phrase not in RP or SBLGNT: %s" % ph)
elif d is not None:
    problems.append("not one JSON object")
work = sorted(p.name for p in (out_dir / "work").iterdir()) if (out_dir / "work").is_dir() else []
row = {
    "schema": "m8_attempt_receipt.v1", "record_kind": "completion", "book": "1Cor",
    "attempt_id": att, "amends_execution_id": eid, "lane": "primary_%s" % tag,
    "agent_id": a.agent_id, "model_ordered": "claude-opus-5-5",
    "model_actual": "UNAVAILABLE (the notification does not report the served model)",
    "model_actual_tier": "UNAVAILABLE", "grader_role": "grader_fallback (OW-25)",
    "outcome": a.outcome, "notification_time": NOW + " (the orchestrator's read of the notification, measured by this "
    "script's clock when the landing row was built; an upper bound; the notification carried no time)",
    "tokens_notification_unit": a.tokens,
    "tokens_spend_unit": "UNAVAILABLE (the notification reports subagent_tokens only)",
    "token_note": "subagent_tokens from the completion notification; OW-28 tracked, not enforced",
    "tool_uses": a.tool_uses, "duration_ms": a.duration_ms, "out_dir": str(out_dir).replace("\\", "/"),
    "outputs": ([{"path": str(f).replace("\\", "/"), "sha256": h(b)}] if b else []),
    "result_summary": a.summary,
    "orchestrator_verification": {
        "method": "make_primary_landing.py: JSON parse, schema keys, identity fields, rows digest, one item per cluster "
                  "row (%d rows of %s), verdict/severity/claim/tier/evidence, summary recount, triage ids, Greek "
                  "phrases against both witnesses, CR count (MEASURED)" % (len(cl["row_ids"]), a.cluster),
        "problems": problems, "warnings": warnings, "summary_recount": summ, "greek_phrases": greek},
    "for_fable_end_review": a.note,
    "working_files_count": len(work), "working_files_manifest": work,
    "lane_verdict": ("LANDED_FORM_OK (form only; the findings are candidate claims for the next controlling round)"
                     if not problems else "LANDED_WITH_FORM_PROBLEMS"),
}
Path(a.out).write_text(json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({"row_built": eid, "problems": problems[:12], "n_problems": len(problems), "warnings": len(warnings),
                  "summary": summ, "greek": greek, "work_files": len(work)}, ensure_ascii=False))
