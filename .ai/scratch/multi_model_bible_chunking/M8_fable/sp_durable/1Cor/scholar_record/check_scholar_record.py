#!/usr/bin/env python3
"""CHECKER for a book's scholar record (close-gate item 20, OW-17). Book-agnostic (TE-7).

Item 20 asks that the checker pass on four things: every landed packet represented, every high-severity finding
present, every cross-lane disagreement surfaced, nothing asserted that is not in a packet. Each is a separate test
here, enumerated from the landed files by this script and not taken from the generator's own bookkeeping. It adds:
every routed open question present as open, with its count; byte-identical regeneration; the licence terms checked
against the book's own files.

"Nothing asserted that is not in a packet" is tested three ways, none of which reads the prose and judges it:
  (a) regeneration: the generator is re-run in memory and its bytes compared with the document on disk;
  (b) quotation trace: every quoted line must equal some string of a landed or pinned file after the printed
      substitution table is applied to it;
  (c) frame trace: every other line of the body must be an instance of a template the document itself prints.

The generator module is imported for its digest-checked loader, its substitution function, its reference
formatter and its entry-number finders. Those are shared on purpose and disclosed in the check record.

Usage: python -B check_scholar_record.py [--params FILE] [--book-root DIR] [--out-root DIR] [--check]
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
EXPECTED_SECTIONS = ["What made this book difficult", "How the division was examined, and what that does and does not establish",
                     "The disputes", "What changed", "The reviews, the adjudication and the audit",
                     "What remains open", "Provenance", "Licence and attribution", "Private terms replaced",
                     "The apparatus's own words"]
OUTSIDE_VOCABULARY_SCOPE = ["Provenance", "Private terms replaced", "The apparatus's own words"]

# The vocabulary a reader of the book should never have to learn. The positive-control count in the check record
# shows whether each pattern is live in this book's own landed prose. The parameter file adds book-level classes.
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
    (r"(?i)\bexecutions?\b|\bpeers?\b|\bprimaries\b|\blaunch(?:es|ed)?\b", "a process noun"),
    (r"(?i)\brr\d+\b|\bp13", "a stage code"),
]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def template_regex(t):
    return re.compile(re.escape(t).replace("%d", r"\d+").replace("%s", r".*"), re.S)


def run(params_path, book_root, out_root):
    spec = importlib.util.spec_from_file_location("gen_scholar_record", str(HERE / "gen_scholar_record.py"))
    gen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gen)
    leaves = gen.leaves
    P = gen.load_params(params_path)
    doc_bytes = (Path(out_root) / "scholar_record" / P["doc_name"]).read_bytes()
    text = doc_bytes.decode("utf-8")
    checks = []

    def check(name, passed, **detail):
        checks.append({"check": name, "passed": bool(passed), "detail": detail})

    # ---- regeneration
    b1, _ = gen.build(params_path, book_root)
    b2, _ = gen.build(params_path, book_root)
    check("regeneration_is_byte_identical", sha(b1) == sha(doc_bytes) and sha(b1) == sha(b2),
          on_disk=sha(doc_bytes), rebuilt_first=sha(b1), rebuilt_second=sha(b2), bytes=len(doc_bytes))
    check("lf_line_endings_only", b"\r" not in doc_bytes, carriage_returns=doc_bytes.count(b"\r"))

    # ---- the scripts hold no book
    held = {}
    for name in ("gen_scholar_record.py", "check_scholar_record.py"):
        b = (HERE / name).read_text(encoding="utf-8")
        held[name] = {t: b.count(t) for t in P["script_forbidden_tokens"] if b.count(t)}
        if re.search(r"\b[0-9a-f]{64}\b", b):
            held[name]["a sha256 literal"] = 1
    check("scripts_hold_no_book_specific_token", not any(held.values()), tokens_tested=P["script_forbidden_tokens"], found=held)

    # ---- sections and scope
    heads = re.findall(r"^## (\d+)\. (.+)$", text, re.M)
    check("sections_present_in_order", [h for _n, h in heads] == EXPECTED_SECTIONS and [int(n) for n, _h in heads] == list(range(1, len(heads) + 1)),
          found=[h for _n, h in heads])

    def section(n):
        m = re.search(r"^## %d\. .+$" % n, text, re.M)
        m2 = re.search(r"^## %d\. .+$" % (n + 1), text, re.M)
        return text[m.start():m2.start() if m2 else len(text)]

    before_9 = text[:re.search(r"^## 9\. ", text, re.M).start()]
    body = text[:re.search(r"^## 1\. ", text, re.M).start()]
    for i, name in enumerate(EXPECTED_SECTIONS, 1):
        if name not in OUTSIDE_VOCABULARY_SCOPE:
            body += section(i)

    # ---- own enumeration of the landed files
    inp = gen.Inputs(P, book_root)
    cl = gen.Cleaner(P, inp)
    rid_of = lambda x: (cl.row_of(x) or {}).get("decision_id")
    ids_in = lambda v: sorted({rid_of(x) for x in re.findall(P["row_id_regex"], v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)) if rid_of(x)})
    limit = P["max_rows_under_a_passage"]
    rank = P["severity_rank"]
    is_high = lambda s: rank.get(str(s).lower(), 0) == 3
    lanes = [k for k, _n in P["first_reading_lanes"]]
    first = {k: {} for k in lanes}
    raised = set()
    high = []                # (where, ids placed under, claim leaves)
    all_findings = []        # same, every new review finding
    counts = Counter()
    for e in inp.outputs:
        counts["manifest_outputs"] += 1
        counts["kind:" + e["kind"]] += 1
        if e["rel"] not in inp.landed:
            continue
        d = inp.landed[e["rel"]]
        if e["kind"] == "first_reading":
            lane = re.search(P["first_reading_lane_regex"], e["rel"]).group(1)
            for it in d.get("items", []):
                rid = rid_of(it["row_id"])
                first[lane][rid] = it
                counts["first_reading_findings"] += 1
                if str(it.get("verdict")).lower() != "support":
                    raised.add(rid)
                if is_high(it.get("severity")):
                    high.append((e["rel"], [rid], list(leaves(it.get("claim")))))
        elif e["kind"] == "gate_review":
            for f in d.get("new_findings", []):
                ids = ids_in(f.get("row_or_artifact", ""))
                placed = ids if 1 <= len(ids) <= limit else []
                raised.update(placed)
                counts["review_findings"] += 1
                all_findings.append((e["rel"], placed, list(leaves(f.get("claim")))))
                if is_high(f.get("severity")):
                    high.append((e["rel"], placed, list(leaves(f.get("claim")))))
            for s in d.get("seams", []):
                counts["review_seams"] += 1
                if s.get("verdict") != "accept" or s.get("findings"):
                    counts["review_seams_unaccepted_or_with_findings"] += 1
                    ids = ids_in(s.get("rows", []))
                    if 1 <= len(ids) <= limit:
                        raised.update(ids)
        elif e["kind"] in ("audit", "audit_supplement"):
            for it in d.get("rows", []):
                rid = rid_of(it["row"])
                if it.get("verdict") != "CONFIRM":
                    raised.add(rid)
                for fd in it.get("findings", []) or []:
                    counts["audit_findings"] += 1
                    raised.add(rid)
                    if is_high(fd.get("severity")):
                        high.append((e["rel"], [rid], list(leaves(fd.get("claim")))))
    rulings = []
    for rel, d in inp.rulings:
        for ru in d.get("rulings", []):
            counts["rulings"] += 1
            rulings.append(ru)
            ids = gen.ruling_ids(ru, cl)
            if 1 <= len(ids) <= limit:
                raised.update(ids)
    disagree = set()
    for r in inp.rows:
        rid = r["decision_id"]
        its = [first[k][rid] for k in lanes if rid in first[k]]
        vs = {str(i.get("verdict")).lower() for i in its}
        ch = {json.dumps(i.get("decision"), ensure_ascii=False, sort_keys=True) for i in its if str(i.get("verdict")).lower() == "challenge"}
        if len(vs) > 1 or (vs == {"challenge"} and len(ch) > 1):
            disagree.add(rid)
    raised |= disagree

    # ---- entries of section 3
    s3 = section(3)
    entries = {}
    for blk in re.split(r"(?m)^(?=### )", s3)[1:]:
        entries[blk.split("\n", 1)[0]] = blk
    ref_of = {r["decision_id"]: gen.full_ref(P, r["span"]) for r in inp.rows}
    entry_of = {}
    for rid, ref in ref_of.items():
        hits = [h for h in entries if h.startswith("### " + ref + " — ")]
        if len(hits) == 1:
            entry_of[rid] = hits[0]
    quiet_blk = [entries[h] for h in entries if h.startswith("### Passages on which")]
    quiet_refs = set()
    if quiet_blk:
        mq = re.search(r"no later finding: (.*)\.\n", quiet_blk[0])
        quiet_refs = set(mq.group(1).split("; ")) if mq else set()
        quiet_refs.discard("none")
    placed_once = all((rid in entry_of) != (ref_of[rid] in quiet_refs) for rid in ref_of)
    check("every_unit_placed_exactly_once", placed_once and len(entry_of) + len(quiet_refs) == len(inp.rows),
          units=len(inp.rows), dispute_entries=len(entry_of), quiet=len(quiet_refs))
    check("every_raised_passage_has_an_entry", raised == set(entry_of), raised=len(raised), entries=len(entry_of),
          missing=sorted(ref_of[x] for x in raised - set(entry_of)), unexpected=sorted(ref_of[x] for x in set(entry_of) - raised))

    # ---- item 20: every landed packet represented
    prov = section(7)
    missing = [e["path"] for e in inp.outputs if ("| %s | " % e["shown"]) not in prov or e["sha256"] not in prov]
    missing_nm = [x["listed_path"] for x in inp.manifest.get("not_matching", []) if x["sha256"] not in prov]
    quote_lines = [l[2:] for l in before_9.split("\n") if l.startswith("> ")]
    quote_set = set(quote_lines)
    unquoted = []
    S = set()
    for e in inp.outputs:
        if e["rel"] in inp.landed:
            own = {cl.clean(x) for x in leaves(inp.landed[e["rel"]])}
            S |= own
            if not (own & quote_set):
                unquoted.append(e["rel"])
    check("every_landed_packet_represented", not missing and not unquoted and not missing_nm,
          manifest_outputs=len(inp.outputs), named_in_provenance=len(inp.outputs) - len(missing), missing=missing,
          opened_and_quoted=len(inp.landed), opened_but_no_line_quoted=unquoted,
          by_kind={k[5:]: counts[k] for k in sorted(counts) if k.startswith("kind:")},
          listed_with_no_durable_file=len(inp.manifest.get("not_matching", [])), listed_with_no_durable_file_missing=missing_nm,
          note="files marked not opened are named with the manifest's digest only; they are represented by name, not by content")

    # ---- item 20: every high-severity finding present
    def present(placed, claims):
        want = [cl.clean(x) for x in claims]
        if not want:
            return False
        if placed:
            return all(all(("> " + w) in entries.get(entry_of.get(r, ""), "").split("\n") for w in want) for r in placed)
        return all(("> " + w) in section(5).split("\n") for w in want)
    hi_missing = [where for where, placed, claims in high if not present(placed, claims)]
    hi_heading = [ref_of[r] for _w, placed, _c in high for r in placed if r in entry_of and not entry_of[r].endswith("highest severity: high")]
    check("every_high_severity_finding_present", not hi_missing and not hi_heading, high_findings=len(high),
          by_reader_word_mapping=P["severity_mapping_text"], placed_under_a_passage=sum(1 for _w, p, _c in high if p),
          book_wide=sum(1 for _w, p, _c in high if not p), passages=sorted({ref_of[r] for _w, p, _c in high for r in p}),
          missing=hi_missing, heading_understated=hi_heading)
    rv_missing = [where for where, placed, claims in all_findings if not present(placed, claims)]
    check("every_review_finding_present", not rv_missing, review_findings=len(all_findings), missing=rv_missing)

    # ---- item 20: every cross-lane disagreement surfaced
    marker = "**The first readings disagreed here**"
    marked = {rid for rid, h in entry_of.items() if marker in entries[h]}
    check("every_cross_reading_disagreement_surfaced", marked == disagree,
          first_reading_disagreements=len(disagree), marked_in_document=len(marked),
          missing=sorted(ref_of[x] for x in disagree - marked), spurious=sorted(ref_of[x] for x in marked - disagree),
          note="a disagreement is a difference of verdict among the readings of one passage, or two or more challenges proposing different courses; no reconciling or paired later reading exists in this book's landed files")

    # ---- every dispute entry carries both sides and a resolution
    lacking = [h for rid, h in sorted(entry_of.items()) if "**Evidence on each side.**" not in entries[h] or "**Resolution.**" not in entries[h]
               or any(k not in entries[h] for k in P["required_lanes_in_a_dispute"])]
    check("every_dispute_entry_has_evidence_on_each_side_and_a_resolution", not lacking, entries=len(entry_of), lacking=lacking)

    # ---- every ruling present
    ru_missing = [ru.get("id") for ru in rulings if not any(cl.clean(x) in quote_set for x in leaves(ru.get("decision")))]
    check("every_ruling_present", not ru_missing, rulings=len(rulings), by_ruling=dict(sorted(Counter(ru.get("ruling") for ru in rulings).items())), missing=ru_missing)

    # ---- the open questions
    s6 = section(6)
    oq = [b for b in re.split(r"(?m)^(?=### )", s6)[1:] if b.startswith("### Open question ")]
    bad = []
    expected = P["expected_open_questions"]
    for i, it in enumerate(inp.routed, 1):
        blk = oq[i - 1] if i <= len(oq) else ""
        want = [cl.clean(x) for x in leaves([it.get("decision"), gen.order_value(it)])]
        if not blk.startswith("### Open question %d\n" % i) or "\nStatus: open.\n" not in blk or any(("> " + w) not in blk.split("\n") for w in want):
            bad.append(it.get("id"))
    check("open_questions_present_as_open", len(inp.routed) == expected == len(oq) and not bad
          and ("%d questions are carried open." % expected) in s6 and len(re.findall(r"(?m)^Status: open\.$", s6)) == len(oq),
          expected_in_params=expected, in_routed_file=len(inp.routed), in_document=len(oq), not_fully_rendered=bad,
          key_rows_in_provenance=sum(1 for i, it in enumerate(inp.routed, 1) if ("| %d | %s | " % (i, it.get("id"))) in prov))

    # ---- nothing asserted that is not in a packet: quotation trace and frame trace
    for rel, d in inp.rulings:
        S |= {cl.clean(x) for x in leaves(d)}
    for v in (inp.routed, inp.rows, inp.rows_manifest, inp.marks, inp.inventory, [gen.order_value(it) for it in inp.routed]):
        S |= {cl.clean(x) for x in leaves(v)}
    S |= {cl.clean(l) for l in inp.text(P["paths"]["strategy"]).splitlines()}
    untraced = [q for q in quote_lines if q not in S]
    check("every_quoted_line_traces_to_a_landed_or_pinned_string", not untraced, quoted_lines=len(quote_lines),
          distinct=len(quote_set), untraced=len(untraced), first_untraced=[u[:160] for u in untraced[:5]])
    tmpl = [l[2:] for l in section(10).split("\n") if l.startswith("- ")]
    rx = [template_regex(t) for t in tmpl]
    tset = set(tmpl)
    frame = [l for l in before_9.split("\n") if l and not l.startswith("> ") and not l.startswith("|")]
    off = [l for l in frame if l not in tset and not any(r.fullmatch(l) for r in rx)]
    table_in_body = sum(1 for l in body.split("\n") if l.startswith("|"))
    check("every_other_line_is_an_instance_of_a_printed_template", not off and table_in_body == 0, frame_lines=len(frame),
          templates_printed=len(tmpl), off_template=len(off), first_off=[u[:160] for u in off[:5]], table_lines_in_body=table_in_body)

    # ---- vocabulary
    raw = "\n".join(x for e in inp.outputs if e["rel"] in inp.landed for x in leaves(inp.landed[e["rel"]]))
    vocab = []
    total = 0
    gate = "".join("(?<!%s )" % re.escape(x) for x in P["gate_word_exempt_prefixes"])
    patterns = CAMPAIGN_VOCAB + [(gate + r"\bgates?\b", "a process noun (gate)")] + [tuple(x) for x in P["extra_vocabulary"]]
    for pat, what in patterns:
        hits = re.findall(pat, body)
        total += len(hits)
        vocab.append({"pattern": pat, "class": what, "hits_in_scope": len(hits), "first": [str(h)[:40] for h in hits[:3]],
                      "positive_control_hits_in_landed_prose": len(re.findall(pat, raw))})
    check("body_is_free_of_campaign_vocabulary", total == 0, scope="every section except " + ", ".join(OUTSIDE_VOCABULARY_SCOPE),
          chars_in_scope=len(body), patterns=len(patterns), hits=total, by_pattern=vocab,
          dead_patterns=[v["pattern"] for v in vocab if v["positive_control_hits_in_landed_prose"] == 0])

    # ---- the two disclosure tables and the licence section
    sub_rows = [l for l in section(9).split("\n") if l.startswith("| `")]
    check("substitution_table_and_template_list_present", len(sub_rows) == len(cl.table) and len(tmpl) > 0,
          substitution_rows=len(sub_rows), substitutions_in_generator=len(cl.table), templates=len(tmpl))
    s8 = section(8)
    s8q = {l[2:] for l in s8.split("\n") if l.startswith("> ")}
    terms = []
    for path in P["licence_traced"]:
        v = gen.lookup(inp, {}, path)
        terms.append({"from": path, "found_in_section": cl.clean(v) in s8q})
    lic_absent = [k for k in P["licence_required"] if k not in s8]
    lic_foreign = [k for k in P["licence_forbidden"] if k in s8]
    check("licence_and_attribution_taken_from_the_books_own_files", not lic_absent and not lic_foreign and all(t["found_in_section"] for t in terms),
          terms_traced=terms, required_absent=lic_absent, foreign_terms_present=lic_foreign,
          quoted_source_lines=sum(1 for l in s8.split("\n") if l.startswith("> ")))

    # ---- the frame statements of the parameter file that can be measured
    rounds = sorted({int(re.search(P["change_log_regex"], e["rel"]).group(1)) for e in inp.outputs if e["kind"] == "change_log"})
    read_on = sorted({str(d.get("rows_file")) for _e, d in inp.of_kind("first_reading")})
    read_bad = [x for x in read_on if not re.search(P["first_readings_rows_file_regex"], x)]
    check("book_specific_frame_statements_hold", rounds == P["revision_rounds_with_logs"] and not read_bad and read_on != [],
          rounds_with_a_log=rounds, rounds_stated=P["revision_rounds_with_logs"], first_readings_named_rows_files=len(read_on), not_matching_the_stated_revision=read_bad)

    # ---- informational, not gating: script runs against the witnesses
    wit = "\n".join(inp.text(rel) for rel in P["script_run_files"])
    runs = set()
    for q in quote_lines:
        for m in re.finditer(P["script_run_regex"], q):
            if len(m.group(0)) >= 8:
                runs.add(m.group(0))
    found = sum(1 for r in runs if r in wit)
    info = {"what": "distinct runs of %s script (8 characters or more) inside quoted lines, tested as exact substrings of the witness files" % P["script_run_label"],
            "runs": len(runs), "found_exactly": found, "not_found_exactly": len(runs) - found,
            "reading": "NOT a gate. A run not found exactly may be an elided, respaced or differently pointed citation; this count does not say any quotation is wrong or right."}

    failed = [c["check"] for c in checks if not c["passed"]]
    return {
        "schema": P["check_schema"],
        "book": P["book"],
        "document": {"name": P["doc_name"], "sha256": sha(doc_bytes), "bytes": len(doc_bytes), "lines": doc_bytes.count(b"\n")},
        "generator": {"name": "gen_scholar_record.py", "sha256": sha((HERE / "gen_scholar_record.py").read_bytes())},
        "checker": {"name": "check_scholar_record.py", "sha256": sha(Path(__file__).resolve().read_bytes())},
        "params": {"name": Path(params_path).name, "sha256": sha(Path(params_path).read_bytes())},
        "tier": "MEASURED by this script on the pinned and landed bytes; the landed files themselves are what their readers REPORTED",
        "counts": {k: counts[k] for k in sorted(counts)},
        "checks": checks,
        "checks_total": len(checks),
        "checks_passed": len(checks) - len(failed),
        "FAILED": failed,
        "VERDICT": "PASS" if not failed else "FAIL",
        "informational": {"script_runs": info, "entry_numbers_outside_the_final_set": sum(cl.unknown_ids.values())},
        "shared_with_the_generator": ["the digest-checked loader (Inputs)", "the substitution function (Cleaner.clean)", "the reference formatter (full_ref)", "the entry-number finder for rulings (ruling_ids)", "the decoder of routed orders (order_value)", "the parameter lookup (lookup)"],
        "what_a_pass_does_not_establish": [
            "It does not establish that any reader's sentence is true of the book. The checker traces sentences to files; it reads no original-language text and weighs no boundary.",
            "It does not establish independence. Every reading at every stage came from one model family, so agreement between readings is one voice.",
            "The vocabulary test bans the classes listed here, over every section except the three named in its detail, which by their purpose name files or print patterns. A private term of a class not listed would pass; the list was measured, not proven complete.",
            "The substitution function is shared with the generator, so a substitution that distorts a sentence distorts it identically in the trace test.",
            "Files the manifest lists but this build does not open (closing messages) are represented by name and listed digest only. Outputs the project's records list with no durable file are represented by listed digest only.",
            "The frame sentences are checked for shape, not for truth: a template in the parameter file that misdescribes a stage would pass.",
            "The licence test shows the terms are the book's own statements; it does not show they match each witness's own distribution.",
            "The first audit's overall verdict is reported in the record as it was given; a PASS here is not a pass of that audit.",
        ],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--params", default=str(HERE / "book_params.v1.json"))
    ap.add_argument("--book-root", default=str(HERE.parent))
    ap.add_argument("--out-root", default=None)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    out_root = a.out_root or a.book_root
    rec = run(a.params, a.book_root, out_root)
    b = (json.dumps(rec, ensure_ascii=False, indent=1, sort_keys=False) + "\n").encode("utf-8")
    target = Path(out_root) / "scholar_record" / json.loads(Path(a.params).read_bytes().decode("utf-8"))["check_name"]
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
