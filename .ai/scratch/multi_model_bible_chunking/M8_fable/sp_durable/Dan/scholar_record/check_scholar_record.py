#!/usr/bin/env python3
"""CHECKER for the Daniel scholar record (close-gate item 20, OW-17). Ported in form from the Ezekiel checker.

Item 20 asks that the checker pass on four things: every landed packet represented, every high-severity finding
present, every cross-lane disagreement surfaced, nothing asserted that is not in a packet. Each is a separate
test here, enumerated from the landed files by this script and not taken from the generator's own bookkeeping.
The Daniel build adds: the open questions present as open, with their count; byte-identical regeneration.

"Nothing asserted that is not in a packet" is tested three ways, none of which reads the prose and judges it:
  (a) regeneration: the generator is re-run in memory and its bytes compared with the document on disk;
  (b) quotation trace: every quoted line must equal some string of a landed or pinned file after the printed
      substitution table is applied to it;
  (c) frame trace: every other line of the body must be an instance of a template the document itself prints.

The generator module is imported for three things only: its digest-checked loader, its substitution function
and its reference formatter. Those are shared on purpose and disclosed in the check record.

Usage: python -B check_scholar_record.py [--dan-root DIR] [--out-root DIR] [--check]
  --check  write nothing; recompute and compare with the check record on disk (exit 1 on a difference or FAIL)
"""
import argparse
import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
CHECK_NAME = "scholar_record_check.v1.json"
EXPECTED_OPEN_QUESTIONS = 46  # the build's own statement of how many questions are carried open
EXPECTED_SECTIONS = ["What made this book difficult", "How the division was examined, and what that does and does not establish",
                     "The disputes", "What changed", "The later re-readings, the adjudication and the audit",
                     "What remains open", "Provenance", "Licence and attribution", "Private terms replaced",
                     "The apparatus's own words"]

# The vocabulary a reader of Daniel should never have to learn. Each class was measured in Daniel's own landed
# prose (the positive-control count in the check record shows each pattern is live there).
CAMPAIGN_VOCAB = [
    (r"\bW\d{1,2}[-#]\d+", "an entry or revision-note identifier"),
    (r"\b[A-Za-z][A-Za-z0-9]*_[A-Za-z0-9_]+\b", "a field, file or key name"),
    (r"\b(?:MEASURED|EXTRACTED|TRANSCRIBED|REPORTED|INFERRED|ASSUMED|UNAVAILABLE|NOT_TESTABLE)\b", "an evidence-tier code"),
    (r"(?i)\btier(?:s|ed|ing)?\b", "the tier vocabulary"),
    (r"\b(?:CWO|TRIAGE|FIXUP|OW|SEAM|CLASS|GATE|RR\d+|S\d+|E\d*)-[A-Z0-9]", "an internal ticket or rule code"),
    (r"\b[EBPF]\d{1,2}\b", "a round, condition or finding code"),
    (r"\b(?:LF|OL|OS|TB)\b", "a reading's internal name"),
    (r"(?i)\blanes?\b", "a process noun (lane)"),
    (r"(?i)\brows?\b", "a process noun (row)"),
    (r"(?i)\bpackets?\b", "a process noun (packet)"),
    (r"(?i)\borchestrator|\bsub-?agents?\b", "a process role"),
    (r"(?i)\bfix-?ups?\d*\b", "a process noun (fix-up)"),
    (r"(?i)\bend[- ]review\b|\bcontrolling[- ]agent|\bboss\b", "a process stage or role"),
    (r"\bFable\b|\bOpus\b|\bClaude\b|\bclaude-", "a model or reviewer name"),
    (r"\bsha256\b|\b[0-9a-f]{64}\b", "an implementation detail in prose"),
    (r"\.(?:jsonl|json|py|md)\b|\bSP[\\/]", "a file name or path"),
    (r"#e\d", "an internal execution reference"),
    (r"(?i)\bthe brief\b|\bledger\b|\breceipts?\b|\bvalidators?\b|\bclose[- ]gate\b", "a process noun"),
    (r"(?<!king's )(?<!king’s )\bgates?\b", "a process noun (gate), outside the phrase the king's gate"),
    (r"(?i)\bexecutions?\b|\bpeers?\b|\bprimaries\b|\blaunch(?:es|ed)?\b", "a process noun"),
    (r"(?i)\brr\d+\b|\bp13", "a stage code"),
]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def leaves(v):
    if isinstance(v, str):
        if v.strip():
            yield v
    elif isinstance(v, dict):
        for k in v:
            yield from leaves(v[k])
    elif isinstance(v, list):
        for x in v:
            yield from leaves(x)


def template_regex(t):
    return re.compile(re.escape(t).replace("%d", r"\d+").replace("%s", r".*"), re.S)


def run(dan_root, out_root):
    spec = importlib.util.spec_from_file_location("gen_scholar_record", str(HERE / "gen_scholar_record.py"))
    gen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gen)
    doc_bytes = (Path(out_root) / "scholar_record" / gen.DOC_NAME).read_bytes()
    text = doc_bytes.decode("utf-8")
    checks = []

    def check(name, passed, **detail):
        checks.append({"check": name, "passed": bool(passed), "detail": detail})

    # ---- regeneration
    b1, _ = gen.build(dan_root)
    b2, _ = gen.build(dan_root)
    check("regeneration_is_byte_identical", sha(b1) == sha(doc_bytes) and sha(b1) == sha(b2),
          on_disk=sha(doc_bytes), rebuilt_first=sha(b1), rebuilt_second=sha(b2), bytes=len(doc_bytes))
    check("lf_line_endings_only", b"\r" not in doc_bytes, carriage_returns=doc_bytes.count(b"\r"))

    # ---- sections and scope
    heads = re.findall(r"^## (\d+)\. (.+)$", text, re.M)
    check("sections_present_in_order", [h for _n, h in heads] == EXPECTED_SECTIONS and [int(n) for n, _h in heads] == list(range(1, len(heads) + 1)),
          found=[h for _n, h in heads])
    m_prov = re.search(r"^## (\d+)\. Provenance$", text, re.M)
    if not m_prov:
        raise SystemExit("no provenance heading: the vocabulary test has no defined scope")
    body = text[:m_prov.start()]
    after = text[m_prov.start():]

    def section(n):
        m = re.search(r"^## %d\. .+$" % n, text, re.M)
        m2 = re.search(r"^## %d\. .+$" % (n + 1), text, re.M)
        return text[m.start():m2.start() if m2 else len(text)]

    # ---- own enumeration of the landed files
    inp = gen.Inputs(dan_root)
    cl = gen.Cleaner(inp)
    by_id = {}
    for r in inp.rows:
        by_id[r["decision_id"]] = r
        by_id[r["writer_decision_id"]] = r
    ids_in = lambda v: sorted({by_id[x]["decision_id"] for x in re.findall(r"W\d-\d{1,3}", v if isinstance(v, str) else json.dumps(v)) if x in by_id})
    first = {"LF": {}, "OL": {}}
    high, raised = set(), set()
    counts = Counter()
    for e in inp.outputs:
        counts["manifest_outputs"] += 1
        counts["kind:" + e["kind"]] += 1
        if e["rel"] not in inp.landed:
            continue
        d = inp.landed[e["rel"]]
        if e["kind"] == "first_reading":
            lane = "LF" if "/rev_LF_" in e["rel"] else "OL"
            for it in d.get("items", []):
                rid = by_id[it["row_id"]]["decision_id"]
                first[lane][rid] = it
                counts["first_reading_findings"] += 1
                if it.get("verdict") != "support":
                    raised.add(rid)
                if it.get("severity") == "high":
                    high.add(rid)
        elif e["kind"] == "reconciling":
            for it in d.get("items", []):
                rid = by_id[it["row_id"]]["decision_id"]
                counts["reconciling_findings"] += 1
                first.setdefault("PEER", {})[rid] = it
                if it.get("proposal_severity") == "high" or any(pf.get("severity") == "high" for pf in it.get("primary_findings", []) or []):
                    high.add(rid)
        elif e["kind"] == "rereading":
            for key in ("items", "extra_findings"):
                for it in d.get(key, []) or []:
                    counts["rereading_" + key] += 1
                    if key == "extra_findings" or it.get("verdict") != "support":
                        raised.update(ids_in(it.get("row", "")))
                    if it.get("severity") == "high":
                        high.update(ids_in(it.get("row", "")))
        elif e["kind"] == "audit":
            for it in d.get("rows", []):
                rid = by_id[it["row"]]["decision_id"]
                for fd in it.get("findings", []) or []:
                    counts["audit_findings"] += 1
                    raised.add(rid)
                    if fd.get("severity") == "high":
                        high.add(rid)
    peer = first.get("PEER", {})
    disagree = set()
    for r in inp.rows:
        rid = r["decision_id"]
        a, b = first["LF"].get(rid), first["OL"].get(rid)
        va, vb = (a or {}).get("verdict"), (b or {}).get("verdict")
        if va != vb or (va == "challenge" and a.get("decision") != b.get("decision")) or (peer.get(rid) or {}).get("lanes_disagreed") is True:
            disagree.add(rid)
    raised |= disagree

    # ---- entries of section 3
    s3 = section(3)
    entries = {}
    for blk in re.split(r"(?m)^(?=### )", s3)[1:]:
        entries[blk.split("\n", 1)[0]] = blk
    ref_of = {r["decision_id"]: gen.full_ref(r["span"]) for r in inp.rows}
    entry_of = {}
    for rid, ref in ref_of.items():
        hits = [h for h in entries if h.startswith("### " + ref + " — ")]
        if len(hits) == 1:
            entry_of[rid] = hits[0]
    quiet_blk = [entries[h] for h in entries if h.startswith("### Passages on which")]
    quiet_refs = set()
    if quiet_blk:
        mq = re.search(r"drew no later finding: (.*)\.\n", quiet_blk[0])
        quiet_refs = set(mq.group(1).split("; ")) if mq else set()
    placed_once = all((rid in entry_of) != (ref_of[rid] in quiet_refs) for rid in ref_of)
    check("every_unit_placed_exactly_once", placed_once and len(entry_of) + len(quiet_refs) == len(inp.rows),
          units=len(inp.rows), dispute_entries=len(entry_of), quiet=len(quiet_refs))
    check("every_raised_passage_has_an_entry", raised == set(entry_of), raised=len(raised), entries=len(entry_of),
          missing=sorted(ref_of[x] for x in raised - set(entry_of)), unexpected=sorted(ref_of[x] for x in set(entry_of) - raised))

    # ---- item 20: every landed packet represented
    prov = section(7)
    missing = [e["path"] for e in inp.outputs if ("| %s | " % (e["rel"] or e["name"])) not in prov or e["sha256"] not in prov]
    quote_lines = [l[2:] for l in text[:re.search(r"^## 9\. ", text, re.M).start()].split("\n") if l.startswith("> ")]
    quote_set = set(quote_lines)
    unquoted = []
    S = set()
    for e in inp.outputs:
        if e["rel"] in inp.landed:
            own = {cl.clean(x) for x in leaves(inp.landed[e["rel"]])}
            S |= own
            if not (own & quote_set):
                unquoted.append(e["rel"])
    check("every_landed_packet_represented", not missing and not unquoted,
          manifest_outputs=len(inp.outputs), named_in_provenance=len(inp.outputs) - len(missing), missing=missing,
          opened_and_quoted=len(inp.landed), opened_but_no_line_quoted=unquoted,
          by_kind={k[5:]: counts[k] for k in sorted(counts) if k.startswith("kind:")},
          note="files marked not opened are named with the manifest's digest only; they are represented by name, not by content")

    # ---- item 20: every high-severity finding present
    hi_missing = [ref_of[x] for x in sorted(high) if x not in entry_of or not entry_of[x].endswith("highest severity: high")]
    check("every_high_severity_finding_present", not hi_missing, passages_with_a_high_finding=len(high),
          passages=sorted(ref_of[x] for x in high), missing=hi_missing)

    # ---- item 20: every cross-lane disagreement surfaced
    marker = "**The first readings disagreed here**"
    marked = {rid for rid, h in entry_of.items() if marker in entries[h]}
    pairs = []
    stages = {}
    for e in inp.outputs:
        m = re.fullmatch(r"review/(\w+)/\1_(OS|TB)\.json", e["rel"] or "")
        if m:
            stages.setdefault(m.group(1), {})[m.group(2)] = {it.get("record"): it for it in inp.landed[e["rel"]].get("items", [])}
    s5 = section(5)
    pair_missing = []
    T = lambda s: s
    for st in sorted(stages):
        a, b = stages[st].get("OS", {}), stages[st].get("TB", {})
        for rec in sorted(set(a) | set(b), key=str):
            va = a[rec].get("verdict") if rec in a else "no finding"
            vb = b[rec].get("verdict") if rec in b else "no finding"
            if va != vb:
                pairs.append((st, rec))
                if gen.pair_line(cl, T, st, rec, a.get(rec) or b.get(rec), va, vb) not in s5.split("\n"):
                    pair_missing.append("%s %s" % (st, rec))
    check("every_cross_reading_disagreement_surfaced", marked == disagree and not pair_missing,
          first_reading_disagreements=len(disagree), marked_in_document=len(marked),
          missing=sorted(ref_of[x] for x in disagree - marked), spurious=sorted(ref_of[x] for x in marked - disagree),
          later_pair_disagreements=len(pairs), later_pair_missing=pair_missing)

    # ---- every dispute entry carries both sides and a resolution
    lacking = [h for rid, h in sorted(entry_of.items()) if "**Evidence on each side.**" not in entries[h] or "**Resolution.**" not in entries[h]
               or "Reading A" not in entries[h] or "Reading B" not in entries[h]]
    check("every_dispute_entry_has_evidence_on_each_side_and_a_resolution", not lacking, entries=len(entry_of), lacking=lacking)

    # ---- the open questions
    s6 = section(6)
    oq = re.split(r"(?m)^(?=### )", s6)[1:]
    oq = [b for b in oq if b.startswith("### Open question ")]
    bad = []
    for i, it in enumerate(inp.routed, 1):
        blk = oq[i - 1] if i <= len(oq) else ""
        want = [cl.clean(x) for x in leaves([it.get("decision"), it.get("order")])]
        if not blk.startswith("### Open question %d\n" % i) or "\nStatus: open.\n" not in blk or any(("> " + w) not in blk.split("\n") for w in want):
            bad.append(it.get("id"))
    check("open_questions_present_as_open", len(inp.routed) == EXPECTED_OPEN_QUESTIONS == len(oq) and not bad
          and ("%d questions are carried open." % EXPECTED_OPEN_QUESTIONS) in s6 and len(re.findall(r"(?m)^Status: open\.$", s6)) == len(oq),
          expected=EXPECTED_OPEN_QUESTIONS, in_routed_file=len(inp.routed), in_document=len(oq), not_fully_rendered=bad,
          key_rows_in_provenance=sum(1 for i, it in enumerate(inp.routed, 1) if ("| %d | %s | " % (i, it.get("id"))) in prov))

    # ---- nothing asserted that is not in a packet: quotation trace and frame trace
    for rel, d in inp.rulings:
        S |= {cl.clean(x) for x in leaves(d)}
    for v in (inp.routed, inp.rows, inp.rows_manifest, inp.pmarks, inp.inventory):
        S |= {cl.clean(x) for x in leaves(v)}
    S |= {" ".join(l.split()) for l in inp.text("book_strategy_Dan.md").splitlines()}
    S |= {" ".join(x.split()) for x in leaves(inp.pmarks)}
    untraced = [q for q in quote_lines if q not in S]
    check("every_quoted_line_traces_to_a_landed_or_pinned_string", not untraced, quoted_lines=len(quote_lines),
          distinct=len(quote_set), untraced=len(untraced), first_untraced=[u[:160] for u in untraced[:5]])
    tmpl = [l[2:] for l in section(10).split("\n") if l.startswith("- ")]
    rx = [template_regex(t) for t in tmpl]
    tset = set(tmpl)
    frame = [l for l in text[:re.search(r"^## 9\. ", text, re.M).start()].split("\n") if l and not l.startswith("> ") and not l.startswith("|")]
    off = [l for l in frame if l not in tset and not any(r.fullmatch(l) for r in rx)]
    table_in_body = sum(1 for l in body.split("\n") if l.startswith("|"))
    check("every_other_line_is_an_instance_of_a_printed_template", not off and table_in_body == 0, frame_lines=len(frame),
          templates_printed=len(tmpl), off_template=len(off), first_off=[u[:160] for u in off[:5]], table_lines_in_body=table_in_body)

    # ---- vocabulary
    raw = "\n".join(x for e in inp.outputs if e["rel"] in inp.landed for x in leaves(inp.landed[e["rel"]]))
    vocab = []
    total = 0
    for pat, what in CAMPAIGN_VOCAB:
        hits = re.findall(pat, body)
        total += len(hits)
        vocab.append({"pattern": pat, "class": what, "hits_in_body": len(hits), "first": [str(h)[:40] for h in hits[:3]],
                      "positive_control_hits_in_landed_prose": len(re.findall(pat, raw))})
    check("body_is_free_of_campaign_vocabulary", total == 0, body_chars=len(body), patterns=len(CAMPAIGN_VOCAB), hits=total, by_pattern=vocab,
          dead_patterns=[v["pattern"] for v in vocab if v["positive_control_hits_in_landed_prose"] == 0])

    # ---- the two disclosure tables and the licence section
    sub_rows = [l for l in section(9).split("\n") if l.startswith("| `")]
    check("substitution_table_and_template_list_present", len(sub_rows) == len(cl.table) and len(tmpl) > 0,
          substitution_rows=len(sub_rows), substitutions_in_generator=len(cl.table), templates=len(tmpl))
    s8 = section(8)
    check("licence_and_attribution_present_with_its_limit", all(k in s8 for k in ("Open Scriptures Hebrew Bible", "Westminster Leningrad Codex",
          "World English Bible", "public domain", "Creative Commons Attribution 4.0", "Daniel's own files do not state them")),
          quoted_source_lines=sum(1 for l in s8.split("\n") if l.startswith("> ")))

    # ---- informational, not gating: Hebrew-script runs against the witness
    wit = inp.text("Dan_oshb.txt")
    runs = set()
    for q in quote_lines:
        for m in re.finditer(r"[֐-׿][֐-׿ ־]*[֐-׿]", q):
            if len(m.group(0)) >= 8:
                runs.add(m.group(0))
    found = sum(1 for r in runs if r in wit)
    info = {"what": "distinct runs of Hebrew script (8 characters or more) inside quoted lines, tested as exact substrings of the Hebrew-Aramaic witness file",
            "runs": len(runs), "found_exactly": found, "not_found_exactly": len(runs) - found,
            "reading": "NOT a gate. A run not found exactly may be an elided, respaced or unpointed citation; this count does not say any quotation is wrong or right."}

    failed = [c["check"] for c in checks if not c["passed"]]
    return {
        "schema": "dan_scholar_record_check.v1",
        "book": "Dan",
        "document": {"name": gen.DOC_NAME, "sha256": sha(doc_bytes), "bytes": len(doc_bytes), "lines": doc_bytes.count(b"\n")},
        "generator": {"name": "gen_scholar_record.py", "sha256": sha((HERE / "gen_scholar_record.py").read_bytes())},
        "checker": {"name": "check_scholar_record.py", "sha256": sha(Path(__file__).resolve().read_bytes())},
        "tier": "MEASURED by this script on the pinned and landed bytes; the landed files themselves are what their readers REPORTED",
        "counts": {k: counts[k] for k in sorted(counts)},
        "checks": checks,
        "checks_total": len(checks),
        "checks_passed": len(checks) - len(failed),
        "FAILED": failed,
        "VERDICT": "PASS" if not failed else "FAIL",
        "informational": {"hebrew_script_runs": info, "entry_numbers_outside_the_final_set": sum(cl.unknown_ids.values())},
        "shared_with_the_generator": ["the digest-checked loader (Inputs)", "the substitution function (Cleaner.clean)", "the reference formatter (full_ref, pair_line)"],
        "what_a_pass_does_not_establish": [
            "It does not establish that any reader's sentence is true of Daniel. The checker traces sentences to files; it reads no Hebrew or Aramaic and weighs no boundary.",
            "It does not establish independence. Every reading at every stage came from one model family, so agreement between readings is one voice.",
            "The vocabulary test bans the classes listed here. A private term of a class not listed would pass; the list was measured, not proven complete.",
            "The substitution function is shared with the generator, so a substitution that distorts a sentence distorts it identically in the trace test.",
            "Files the manifest lists but this build was not permitted to open (closing messages, and revision logs held outside the tree) are represented by name and listed digest only.",
            "The licence terms are carried from the Ezekiel record's wording; Daniel's own files do not state them, and the checker tests only that the section says so.",
            "The audit's overall verdict is reported in the record as it was given; a PASS here is not a pass of that audit.",
        ],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dan-root", default=str(HERE.parent))
    ap.add_argument("--out-root", default=None)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    out_root = a.out_root or a.dan_root
    rec = run(a.dan_root, out_root)
    b = (json.dumps(rec, ensure_ascii=False, indent=1, sort_keys=False) + "\n").encode("utf-8")
    target = Path(out_root) / "scholar_record" / CHECK_NAME
    if a.check:
        same = target.read_bytes() == b
        print("%s: %s; record on disk %s; %d/%d checks" % (rec["VERDICT"], "FAILED " + ", ".join(rec["FAILED"]) if rec["FAILED"] else "no failure",
                                                           "IDENTICAL" if same else "DIFFERS", rec["checks_passed"], rec["checks_total"]))
        return 0 if (same and rec["VERDICT"] == "PASS") else 1
    target.write_bytes(b)
    print("%s %d/%d FAILED=%s record sha256 %s" % (rec["VERDICT"], rec["checks_passed"], rec["checks_total"], rec["FAILED"], sha(b)))
    return 0 if rec["VERDICT"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
