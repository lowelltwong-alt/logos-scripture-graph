#!/usr/bin/env python3
"""CHECKER for the Ezekiel scholar record (close-gate item 20, OW-17).

Item 20 says "THE CHECKER PASSES: every landed packet represented, every high-severity finding present, every
cross-lane disagreement surfaced, and nothing asserted that is not in a packet." Each of those four is a
separate test here, plus two more the item's first bullet implies.

THE FOURTH TEST IS THE INTERESTING ONE. "Nothing asserted that is not in a packet" cannot be checked by reading
the prose and judging it - that would just be another opinion. It is checked structurally: the generator is a
PURE FUNCTION of the pinned records, so the checker RE-RUNS it into a temporary file and compares digests. If
the document is reproducible from the records alone, then every sentence in it either came from a record or is
one of the generator's own template strings, and those are enumerated in the document's last section for the
reader to inspect. A digest match therefore establishes the property; a mismatch means someone edited the
document by hand, which is exactly the thing this test exists to catch.

THE VOCABULARY TEST IS THE ONE MOST LIKELY TO FAIL, and it should be strict. A scholar record that leaks an
internal row identifier, an agent name, a rule code or a process noun is asking its reader to learn a private
apparatus before they can read an argument about Ezekiel.
"""
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
GEN = HERE / "gen_scholar_record.py"
DOC = Path(sys.argv[1]) if len(sys.argv) > 1 else (HERE / "EZEKIEL_SCHOLAR_RECORD.v2.md")
text = DOC.read_text(encoding="utf-8")

# the part of the document that is the apparatus's own disclosure list is EXCLUDED from the vocabulary test,
# because that section exists to quote the frame's own words back to the reader
# EXCLUDED from the vocabulary test, with reasons:
#  - the provenance table, because item 20 REQUIRES every landed record to be named; those filenames are the
#    evidence trail, not a leak
#  - the substitution table and the apparatus's own words, because both exist to show the reader the frame
# the heading is matched by SHAPE, not by its number: adding a section renumbers everything after it, and a
# hardcoded "## 6. Provenance" would silently make the vocabulary test cover the whole document - including the
# two tables that exist to show the reader the frame - and then pass for the wrong reason
m_prov = re.search(r"^## (\d+)\. Provenance$", text, re.M)
if not m_prov:
    raise SystemExit("no provenance heading found in %s: the vocabulary test has no defined scope" % DOC)
body = text[:m_prov.start()]

CAMPAIGN_VOCAB = [
    (r"\bP\d{2}-\d{3}\b", "an internal row identifier"),
    (r"\bOW-\d+", "an owner-directive code"),
    (r"\bE-\d{2}\b", "an error-ledger code"),
    (r"\bE13-\d+", "a queue identifier"),
    (r"\bpeer_\d+", "an agent name"),
    (r"\brev_(LF|OL)_c\d+", "a packet filename"),
    (r"\bDEF-A4-ARGUED\b", "an internal definition name"),
    (r"\bCUT-RULE\b|\bCONF-CAL\b", "an internal rule name"),
    (r"\bworklist\b", "a process noun"),
    (r"\bclose gate\b|\bclose-gate\b", "a process noun"),
    (r"\borchestrator\b", "a process role"),
    (r"\bsubagent\b|\blane blindness\b", "a process noun"),
    (r"\bTRIAGE-EZ-\d+|\bCWO-EZ-\d+|\bFIXUP-\d", "an internal ticket code"),
    (r"#e1[0-9]\b", "an internal execution reference"),
    (r"\bA4\b|\bA6-b\b|\bA9/A16\b|\bC2-amended\b", "an internal rule code"),
    (r"\bMARKS-3D\b|\bOSS-VOCAB\b", "an internal class name"),
    (r"\bsha256\b", "an implementation detail in prose"),
    # ---- added for v2, which quotes the second reading. Every pattern below was MEASURED in that wave's own
    # prose before it was banned here, so each one bans a token class that really occurs and would really leak;
    # none is a guess about what might be there. Together they are what makes the substitution table's claim
    # testable rather than asserted: if a substitution stops firing, the check fails.
    (r"\bS[1-6]-\d{3}\b|\bF-\d{3}\b", "an internal repair-item code"),
    (r"\bO-C2-\d{2}\b|\bO-\d{2}\b|\bM-\d{1,2}\b", "an internal repair-order code"),
    (r"\bRT-\d{2}\b|\bR17-[A-Z]\b|\bK[1-9]\b", "an internal ruling code"),
    (r"\btier-\d\b", "an internal tier code"),
    (r"\bNO_DEFECT\b|\bNO_ACTION\b|\bDISCHARGED\b|\bSTOP\b|\bGRADE_QUESTION\b|\bTWO_FACED\b",
     "a status enumeration a reader would have to learn"),
    (r"\bMEDIUM_LOW\b|\bmedium_low\b", "a grade value in its stored spelling"),
    (r"\bMEASURED\b|\bEXTRACTED\b|\bINFERRED\b|\bDISCLOSURE\b|\bWARRANT\b|\bINTERIOR\b|\bGREEN\b",
     "an internal enumeration value"),
    (r"\bobserved_substrate_signals\b|\bboundary_evidence_refs\b|\bboundary_rationale\b|\bdevice_notes\b",
     "a stored field name"),
    (r"\bstrongest_rejected_alternative\b|\bgrade_questions\b|\bexact_repair\b|\brefs_left_out\b",
     "a stored field name"),
    (r"\brows_v7_cwo24\b|\bk3_caps_plan\b|\bbook_strategy_Ezek\b", "an internal filename"),
]
vocab_hits = []
for pat, why in CAMPAIGN_VOCAB:
    for m in re.finditer(pat, body):
        ln = body[:m.start()].count("\n") + 1
        vocab_hits.append({"term": m.group(0), "why_banned": why, "line": ln,
                           "context": body[max(0, m.start() - 60):m.end() + 60].replace("\n", " ")})

# ---- 1. every landed packet represented (by filename in the provenance table)
packets = sorted([p.name for p in (EZ / "reviews").glob("rev_LF_c*.json")]
                 + [p.name for p in (EZ / "reviews").glob("rev_OL_c*.json")]
                 + [p.name for p in (EZ / "reviews").glob("peer_*.json")])
missing_packets = [n for n in packets if ("`%s`" % n) not in text]

# ---- 2. every high-severity finding present
rows = [json.loads(l) for l in (EZ / "repair" / "rows_v7_cwo24.jsonl")
        .read_text(encoding="utf-8").splitlines() if l.strip()]
span_of = {r["decision_id"]: r.get("span", "") for r in rows}
# the same pinned earlier division the generator uses, for the identifiers the re-tiling dissolved. Without it
# this checker would look for a heading named by an identifier the document is right not to print, and would
# report a missing dispute that is in fact present under its passage.
PRIOR = EZ / "cure_runs" / "2026-09-14_after_s4" / "rows_v6_fixup3.jsonl"
span_before = {}
for line in PRIOR.read_text(encoding="utf-8").splitlines():
    if line.strip():
        r = json.loads(line)
        if r["decision_id"] not in span_of:
            span_before[r["decision_id"]] = r.get("span", "")


def ref(span):
    m = re.findall(r"Ezek\.(\d+)\.(\d+)", str(span))
    if not m:
        return str(span)
    (c1, v1), (c2, v2) = m[0], m[-1]
    if c1 == c2:
        return "Ezekiel %s:%s-%s" % (c1, v1, v2) if v1 != v2 else "Ezekiel %s:%s" % (c1, v1)
    return "Ezekiel %s:%s\u2013%s:%s" % (c1, v1, c2, v2)


high, lanes = [], defaultdict(dict)
for pat in ("rev_LF_c*.json", "rev_OL_c*.json"):
    for p in sorted((EZ / "reviews").glob(pat)):
        d = json.loads(p.read_text(encoding="utf-8"))
        lane = "LF" if "LF" in p.name else "OL"
        for it in d.get("items", []):
            if not isinstance(it, dict) or not it.get("row_id"):
                continue
            lanes[it["row_id"]][lane] = str(it.get("decision", ""))
            if str(it.get("severity", "")).lower() == "high":
                high.append((it["row_id"], p.name, str(it.get("claim", ""))[:70]))
def heading_for(rid):
    """The heading a dispute on this identifier must appear under: its passage in the present division, or - if
    the re-tiling dissolved the unit - its passage in the pinned earlier division."""
    return "### " + ref(span_of.get(rid) or span_before.get(rid) or rid)


missing_high = [h for h in high if heading_for(h[0]) not in text]

# ---- 3. every cross-lane disagreement surfaced
cross = [rid for rid, v in lanes.items() if len(set(v.values())) > 1]
missing_cross = [rid for rid in cross if heading_for(rid) not in text]

# ---- 4. nothing asserted that is not in a packet, by reproducibility
with tempfile.TemporaryDirectory() as td:
    tmp = Path(td) / "regen.md"
    r = subprocess.run([sys.executable, str(GEN), str(tmp)], capture_output=True, text=True,
                       cwd=str(HERE), encoding="utf-8", errors="replace")
    regen_ok = r.returncode == 0 and tmp.is_file()
    regen_sha = hashlib.sha256(tmp.read_bytes()).hexdigest() if regen_ok else None
doc_sha = hashlib.sha256(DOC.read_bytes()).hexdigest()
reproducible = bool(regen_ok and regen_sha == doc_sha)

# ---- 5. the five sections item 20 names are all present and non-empty
SECTIONS = [r"^## \d+\. What made this book difficult$",
            r"^## \d+\. The disputes, the evidence on each side, and the resolution$",
            r"^## \d+\. The second, independent reading of every stated ground$",
            r"^## \d+\. What remains open$", r"^## \d+\. Provenance$",
            r"^## \d+\. Licence and attribution of the witnesses$"]
missing_sections = [s for s in SECTIONS if not re.search(s, text, re.M)]

# ---- 6. every dispute entry actually carries evidence on each side
# SCOPED TO THE DISPUTES SECTION. Section 5 also uses '### <passage>' headings, for the second reading of a
# passage, and those are not dispute entries and carry no two-sided evidence; testing them here would fail the
# document for being more complete.
m3 = re.search(r"^## \d+\. The disputes, the evidence on each side, and the resolution$", text, re.M)
m4 = re.search(r"^## \d+\. What changed as a result of the review$", text, re.M)
disputes_body = text[m3.start():m4.start()] if (m3 and m4) else body
entries = re.findall(r"^### (Ezekiel [^\n]+)$", disputes_body, re.M)
without_evidence = []
for e in entries:
    i = disputes_body.index("### " + e)
    j = disputes_body.find("\n### ", i + 1)
    block = disputes_body[i:j if j > 0 else len(disputes_body)]
    if "Evidence on each side" not in block:
        without_evidence.append(e)

# ---- 7. the second reading (section 5): its records named, its selected items present, its counts true
# WHY EACH OF THESE. Section 5 reports counts over 543 items and quotes only 8 of them. A reader cannot check
# that selection by reading the document, so it is checked here against the records: every one of the eighteen
# readings must be named with a digest, every item the reconciling reader refused to act on must appear under
# its passage, every passage where measurement found nothing to repair must be listed, and the counts the prose
# states must equal the counts the records hold. If a future edit quietly drops a refusal, this fails.
FINAL_DIR = EZ / "author" / "final"
ADOPTED_KEY = {1: "what_i_wrote", 2: "what_i_adopt", 3: "what_i_adopt", 4: "what_i_adopted",
               5: "adjudication", 6: "decision"}
final_names, final_items = [], []
for k in range(1, 7):
    for lane in ("a", "b"):
        p = FINAL_DIR / ("s%d_lane_%s" % (k, lane)) / "discharge.json"
        if p.is_file():
            final_names.append("%s/%s" % (p.parent.name, p.name))
    p = FINAL_DIR / ("s%d_adjudication" % k) / "adjudication.json"
    if not p.is_file():
        continue
    final_names.append("%s/%s" % (p.parent.name, p.name))
    d = json.loads(p.read_text(encoding="utf-8"))
    for iid, it in sorted((d.get("items") or {}).items()):
        if isinstance(it, dict):
            raw = str(it.get("status", "") or "").strip()
            final_items.append({"item": iid, "row": it.get("row") or "",
                                "status": raw.split()[0] if raw else ""})
missing_final_records = [n for n in final_names if ("`%s`" % n) not in text]
m5 = re.search(r"^## \d+\. The second, independent reading of every stated ground$", text, re.M)
m6 = re.search(r"^## \d+\. What remains open$", text, re.M)
second_body = text[m5.start():m6.start()] if (m5 and m6) else ""
refused_rows = sorted({i["row"] for i in final_items if i["status"] in ("STOP", "GRADE_QUESTION")})
nothing_rows = sorted({i["row"] for i in final_items if i["status"] == "NO_DEFECT"})
missing_refused = [rid for rid in refused_rows
                   if rid in span_of and ("### " + ref(span_of[rid])) not in second_body]
missing_nothing = [rid for rid in nothing_rows
                   if rid in span_of and ref(span_of[rid]) not in second_body]
stated = {int(x) for x in re.findall(r"\b(\d{1,4})\b", second_body.split("### ")[0])}
counts_true = {"readings": len(final_names) in stated, "items": len(final_items) in stated}

checks = [
    ("every landed review record appears in the provenance table",
     not missing_packets, {"packets": len(packets), "missing": missing_packets}),
    ("every high-severity finding's passage has an entry",
     not missing_high, {"high_findings": len(high), "missing": [h[0] for h in missing_high]}),
    ("every passage where the two independent readings differed has an entry",
     not missing_cross, {"cross_lane_disagreements": len(cross), "missing": missing_cross}),
    ("the document is REPRODUCIBLE from the records alone, which is how 'nothing asserted that is not in a "
     "record' is established rather than asserted",
     reproducible, {"document_sha256": doc_sha, "regenerated_sha256": regen_sha,
                    "generator_exit": r.returncode,
                    "generator_stderr_tail": (r.stderr or "")[-300:] if not reproducible else ""}),
    ("every section item 20 names is present", not missing_sections, {"missing": missing_sections}),
    ("every dispute entry carries evidence on each side",
     not without_evidence, {"entries": len(entries), "without_evidence": without_evidence[:10]}),
    ("no campaign vocabulary leaks into the body (the provenance table, the substitution table and the "
     "apparatus's own words are excluded, with reasons given in the source)",
     not vocab_hits, {"hits": len(vocab_hits), "sample": vocab_hits[:15]}),
    ("the substitution table that de-privatises quoted prose is present, so a reader can invert it, and the "
     "table of seam repairs beside it",
     bool(re.search(r"^## \d+\. Private terms replaced in quoted prose$", text, re.M))
     and "| internal code | replaced by |" in text and "| seam | repaired to |" in text, {}),
    ("every one of the second reading's records is named with its digest",
     not missing_final_records, {"records": len(final_names), "missing": missing_final_records}),
    ("every item the reconciling reader refused to act on appears in the second reading's section, under its "
     "passage",
     not missing_refused, {"refusals": len(refused_rows), "missing": missing_refused}),
    ("every passage where measurement found nothing to repair is named there",
     not missing_nothing, {"units": len(nothing_rows), "missing": missing_nothing}),
    ("the counts that section states are the counts its records hold",
     all(counts_true.values()), {"stated_true": counts_true, "readings": len(final_names),
                                 "items": len(final_items)}),
]
failed = [c[0] for c in checks if not c[1]]
out = {
    "schema": "ezek_scholar_record_check.v2",
    "document": {"path": str(DOC), "sha256": doc_sha, "bytes": DOC.stat().st_size,
                 "lines": len(text.splitlines())},
    "generator": {"path": str(GEN), "sha256": hashlib.sha256(GEN.read_bytes()).hexdigest()},
    "checks": [{"check": n, "passed": ok, "detail": d} for n, ok, d in checks],
    "checks_passed": len(checks) - len(failed), "checks_total": len(checks),
    "FAILED": failed,
    "VERDICT": "PASS" if not failed else "FAIL",
    "what_a_pass_does_not_establish": ("that the reviewers were RIGHT. This checker establishes that the "
                                       "document faithfully and completely represents what they recorded. "
                                       "Whether their readings of the Hebrew are correct is what the "
                                       "post-flight audit against the primary sources is for."),
}
# named after the document checked, so v1's record is not overwritten by a run against v2
_stem = re.sub(r"^EZEKIEL_SCHOLAR_RECORD\.", "", DOC.stem)
(HERE / ("scholar_record_check.%s.json" % (_stem if re.fullmatch(r"v\d+", _stem) else "adhoc"))).write_text(
    json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
w = max(len(n) for n, _, _ in checks)
for n, ok, d in checks:
    print("  %s  %s" % ("PASS" if ok else "FAIL", n[:100]))
print()
print(json.dumps({k: out[k] for k in ("checks_passed", "checks_total", "FAILED", "VERDICT")}, indent=1))
if vocab_hits:
    print()
    print("campaign-vocabulary hits: %d" % len(vocab_hits))
    seen = set()
    for h in vocab_hits:
        if h["term"] in seen:
            continue
        seen.add(h["term"])
        print("   %-18s %-34s line %d" % (h["term"], h["why_banned"], h["line"]))
raise SystemExit(1 if failed else 0)
