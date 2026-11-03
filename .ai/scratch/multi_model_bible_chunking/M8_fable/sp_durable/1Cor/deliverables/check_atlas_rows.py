#!/usr/bin/env python3
"""Check a book's atlas candidate rows, dimensions record and sidecar (close-gate item 22).

Book-agnostic: every book-specific name, path, digest and word list comes from book_params.v1.json. This checker
imports nothing from the generators. It re-measures from the pinned inputs by its own means: the two numberings are
aligned by POSITION (the n-th verse of one witness is the n-th verse of the other), not by the generator's zone
arithmetic; lane verdicts, audit verdicts and severities are re-read from the packets; seam evidence is re-derived
from the marks file and the inventory; every linkage source is re-opened and must name both units; the open-question
sources are recounted; the routed items are tested with this file's own convention words.

Usage: check_atlas_rows.py [--params FILE] [--book-root DIR] [--out-root DIR] [--selftest] [--check]
       writes deliverables/<check file> under --out-root; exit 0 only when every check passes, every tamper of the
       self-test is caught, and both generators' --check match.
       --selftest  prints which check catches each tamper and writes nothing
       --check     rebuilds the record, compares bytes, writes nothing; the last line printed is MATCH or DIFFERS
No clock, no randomness, no directory scan.
"""
import copy
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
MY_CONVENTION = re.compile(r"convention|\bclass\b|\brule\b|\bpolicy\b", re.I)
CLASSES = {"one_unit", "several_units", "one_book", "campaign_wide"}
VERDICTS = {"same_treatment", "real_distinction", "possible_inconsistency_unruled"}
SIDE_FIELDS = ("concern_type", "why_low_confidence", "why_frontier_review_needed", "possible_downstream_risk",
               "suggested_reviewer", "proposed_atlas_action")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def lines(b):
    return [json.loads(x) for x in b.decode("utf-8").splitlines() if x.strip()]


def dump(objs):
    return "".join(json.dumps(o, ensure_ascii=False) + "\n" for o in objs).encode("utf-8")


class Ctx:
    pass


def ids_in(c, o):
    t = o if isinstance(o, str) else json.dumps(o, ensure_ascii=False)
    fmt = c.P["row_id_format"]
    out = {fmt % (a, int(b)) for a, b in c.rowref.findall(t)}
    for a, b, x, y in c.rowrange.findall(t):
        if a == x and int(b) <= int(y):
            out |= {fmt % (a, i) for i in range(int(b), int(y) + 1)}
    return out


def load_context(book_root, P):
    c = Ctx()
    c.P = P
    c.rowref = re.compile(P["row_ref_regex"])
    c.rowrange = re.compile(P["row_range_regex"])
    c.cref = re.compile(P["crossref_regex"])
    c.chap = re.compile(P["chapter_ref_regex"], re.I)
    m8 = book_root.parent.parent

    def pinned(rel):
        b = (book_root / rel).read_bytes()
        if sha(b) != P["pins"][rel]:
            raise SystemExit("REFUSED: %s moved since it was pinned" % rel)
        return b
    c.rows = lines(pinned(P["rows_file"]))
    c.routed = lines(pinned(P["routed_file"]))
    verse_key = re.compile(r"%s\.\d+\.\d+$" % re.escape(P["verse_prefix"]))
    primary = []
    for ln in pinned(P["witnesses"]["primary"]["file"]).decode("utf-8").splitlines():
        k, _, t = ln.partition("\t")
        if verse_key.match(k):
            primary.append((k, len(t.split())))
    w = P["witnesses"]["web"]
    head, vers = re.compile(w["chapter_header_regex"]), re.compile(w["verse_regex"])
    web, ch = [], None
    for ln in pinned(w["file"]).decode("utf-8").splitlines():
        m = head.match(ln)
        if m:
            ch = m.group(1)
        m = vers.match(ln)
        if m and ch:
            web.append("%s.%s.%s" % (P["verse_prefix"], ch, m.group(1)))
    c.primary, c.web = primary, web
    c.marks = json.loads(pinned(P["marks"]["file"]).decode("utf-8"))
    c.inventory = json.loads(pinned(P["inventory_file"]).decode("utf-8"))
    c.strategy = pinned(P["strategy_file"]).decode("utf-8").splitlines()
    man = json.loads(pinned(P["landed_manifest_file"]).decode("utf-8"))
    never = re.compile(P["never_open_name_regex"])
    c.packets, c.kind_of, c.lane_of = {}, {}, {}
    for o in sorted(man["outputs"], key=lambda o: o["path"]):
        name = o["path"].split("/")[-1]
        if never.search(name):
            continue
        for k in P["packet_kinds"]:
            m = re.match(k["name_regex"], name)
            if m:
                b = (m8 / o["path"]).read_bytes()
                if sha(b) != o["sha256"]:
                    raise SystemExit("REFUSED: %s moved since the manifest" % o["path"])
                c.packets[o["path"]] = json.loads(b.decode("utf-8"))
                c.kind_of[o["path"]] = k["kind"]
                c.lane_of[o["path"]] = m.groupdict().get("lane")
    c.rulings = {}
    for n in P["ruling_numbers"]:
        rel = P["ruling_path_format"] % n
        c.rulings[P["book_path_in_m8"] + rel] = ("E%d" % n, json.loads(pinned(rel).decode("utf-8")))
    return c


def run_checks(c, feed_bytes, dims_bytes, side_bytes):
    P = c.P
    out = []

    def chk(cid, claim, bad):
        bad = list(bad)
        out.append({"id": cid, "claim": claim, "result": "PASS" if not bad else "FAIL",
                    "failures": len(bad), "first_failures": [str(x)[:160] for x in bad[:3]]})
    rows = c.rows
    by = {r["decision_id"]: r for r in rows}
    cid_of = {r["decision_id"]: P["cid_format"] % r["chunk_index_in_book"] for r in rows}
    by_cid = {cid_of[k]: r for k, r in by.items()}
    feed_text, dims_text = feed_bytes.decode("utf-8"), dims_bytes.decode("utf-8")
    chk("A1", "both outputs are LF-only UTF-8 with a final newline",
        [n for n, t in (("feed", feed_text), ("dims", dims_text)) if "\r" in t or not t.endswith("\n")])
    feed, dims = lines(feed_bytes), lines(dims_bytes)
    units = [d for d in dims if d.get("record") == "unit"]
    qs = [d for d in dims if d.get("record") == "open_question"]
    links = [d for d in dims if d.get("record") == "linkage"]
    chk("A2", "every feed row has exactly the shared-feed fields, in order",
        [f.get("chunk_decision_id") for f in feed if list(f.keys()) != P["feed_keys"]])
    want = {cid_of[r["decision_id"]] for r in rows if r["confidence"] in P["select_confidence"]}
    got = [f.get("chunk_decision_id") for f in feed]
    chk("A3", "feed rows are exactly the final rows graded in the selected set, once each",
        sorted(want ^ set(got)) + (["duplicate"] if len(got) != len(set(got)) else []))
    bad = []
    for f in feed:
        r = by_cid.get(f.get("chunk_decision_id"))
        if r is None:
            bad.append(f.get("chunk_decision_id"))
            continue
        if not (f["span"] == r["span"] and f["confidence"] == r["confidence"]
                and f["chunk_review_status"] == r["review_status"]
                and f["candidate_hold_state"] == r["candidate_hold_state"]
                and f["non_authorizing"] is True and f["atlas_promotion_authority"] == "none"
                and f["proposed_atlas_action"] == "consider_only" and f["model_id"] == P["model_id"]
                and f["book"] == P["book"] and f["observed_substrate_signals"] == (r.get("observed_substrate_signals") or [])):
            bad.append(f["chunk_decision_id"])
    chk("A4", "each feed row mirrors its corpus row: span, confidence, review state, the row's own hold, "
              "non-authorizing, no promotion authority", bad)
    bad_bytes = re.compile(P["witness_bytes_regex"] + "|" + P["quote_regex"])
    bad_code = re.compile(P["checker_bad_code_regex"], re.I)
    chk("A5", "no witness bytes, quotation mark or internal code in any feed prose field",
        [f["chunk_decision_id"] for f in feed
         for k in ("why_low_confidence", "possible_downstream_risk", "concern_type", "suggested_reviewer")
         if bad_bytes.search(str(f.get(k) or "")) or bad_code.search(str(f.get(k) or ""))])
    whys = [f.get("why_low_confidence") or "" for f in feed]
    chk("A6", "every why_low_confidence is non-empty and unique",
        [w[:60] for w in whys if not w.strip() or whys.count(w) > 1])
    unit_by_cid = {u.get("chunk_decision_id"): u for u in units}
    bad = []
    split = re.compile(P["sentence_split_regex"])
    for f in feed:
        r, u = by_cid.get(f.get("chunk_decision_id")), unit_by_cid.get(f.get("chunk_decision_id"))
        if r is None or u is None or (u.get("derivation") or {}).get("composed_not_derived"):
            continue
        src = " ".join((r.get(k) or "").replace("\n", " ") for k in ("device_notes", "boundary_rationale",
                                                                     "strongest_rejected_alternative"))
        for s in split.split(f["why_low_confidence"]):
            s = s.strip()
            if s.startswith("Recorded alternative: "):
                s = s[len("Recorded alternative: "):]
            if s and s not in src and s[:-1] not in src:
                bad.append("%s: %s" % (f["chunk_decision_id"], s[:80]))
    chk("A7", "every sentence of why_low_confidence is found verbatim in that row's own prose", bad)
    chk("A8", "no judged rating travels in the feed",
        [f["chunk_decision_id"] for f in feed if re.search(r"hardness|JUDGED|score", json.dumps(f))])
    # final state, from the audits themselves
    last = {}
    by_name = {p.split("/")[-1]: p for p in c.packets}
    for name in P["audit_order"]:
        for it in c.packets[by_name[name]].get("rows") or []:
            for k in ids_in(c, str(it.get("row"))):
                last[k] = it.get("verdict")
    fs = P["final_state"]

    def state(r):
        ok = (r["review_status"] == fs["requires_review_status"] and r["candidate_hold_state"] is None
              and last.get(r["decision_id"]) == fs["confirm_word"])
        return fs["accepted_value"] if ok else fs["other_value"]
    chk("A9", "review_packet_final_state equals a re-derivation from the row's status, its hold and the last audit "
              "verdict, on every feed row and every unit",
        [f.get("chunk_decision_id") for f in feed if f.get("chunk_decision_id") in by_cid
         and f.get("review_packet_final_state") != state(by_cid[f["chunk_decision_id"]])]
        + [u.get("chunk_decision_id") for u in units if u.get("chunk_decision_id") in by_cid
           and u["measured"]["review_packet_final_state"]["value"] != state(by_cid[u["chunk_decision_id"]])])

    # units
    chk("B1", "one unit record per final row", sorted(set(cid_of.values()) ^ {u.get("chunk_decision_id") for u in units})
        + (["count"] if len(units) != len(rows) else []))
    bad = []
    for u in units:
        j, m = u.get("judged") or {}, u.get("measured") or {}
        if not (j.get("tier") == "JUDGED_BY_RULE" and j.get("not_a_measurement") and j.get("rule")
                and "risk_rating_left_out" in j and j.get("risk_rating") is None
                and not ({"atlas_hardness", "score"} & set(m)) and isinstance(u.get("dependency"), dict)
                and u.get("in_feed") == (u.get("chunk_decision_id") in want)):
            bad.append(u.get("chunk_decision_id"))
    chk("B2", "measured, dependency and judged are separate blocks; the judged block is labelled a rule, and the "
              "risk rating is left out and said to be left out", bad)
    web, pri = c.web, c.primary
    pos = {v: i for i, v in enumerate(web)}
    bad, covered = [], []
    if len(web) != len(pri):
        bad.append("witness verse counts differ: %d vs %d" % (len(web), len(pri)))
    order = sorted(rows, key=lambda r: r["chunk_index_in_book"])
    unit_at = {}
    for r in order:
        a, _, b = r["span"].partition("-")
        u = unit_by_cid.get(cid_of[r["decision_id"]]) or {}
        if a not in pos or b not in pos or pos[a] > pos[b]:
            bad.append("span not on the numbering face: " + r["span"])
            continue
        covered.extend(range(pos[a], pos[b] + 1))
        for v in web[pos[a]:pos[b] + 1]:
            unit_at[v] = r["decision_id"]
        m = u.get("measured") or {}
        if (m.get("span_primary") != "%s-%s" % (pri[pos[a]][0], pri[pos[b]][0]) or m.get("verses") != pos[b] - pos[a] + 1
                or m.get("words_primary") != sum(w for _v, w in pri[pos[a]:pos[b] + 1])):
            bad.append("primary span or size differs for " + r["span"])
    if covered != list(range(len(web))):
        bad.append("the spans do not tile the book once each, in order")
    chk("B3", "every span exists on both witnesses, the spans tile the book, and each unit's primary span and size "
              "match an independent positional alignment of the two numberings", bad)
    seen = {}
    for p, d in c.packets.items():
        if c.kind_of[p] != "primary":
            continue
        for it in d.get("items") or []:
            k = sorted(ids_in(c, str(it.get("row_id"))))
            if k:
                seen.setdefault(k[0], {}).setdefault(c.lane_of[p], set()).add(str(it.get("verdict")).lower())
    bad = []
    for u in units:
        s = seen.get(u.get("internal_decision_id")) or {}
        mine = len({tuple(sorted(v)) for v in s.values()}) > 1
        if ((u.get("measured") or {}).get("contested_between_blind_lanes") or {}).get("verdicts_differ") != mine:
            bad.append(u.get("internal_decision_id"))
    chk("B4", "contested-between-blind-lanes equals an independent re-read of the lanes' verdicts", bad)
    chk("B5", "answerable-from-the-witnesses is one of three stated values, and left_out says what it means",
        [u.get("chunk_decision_id") for u in units
         if ((u.get("measured") or {}).get("answerable_from_the_witnesses") or {}).get("value")
         not in ("a_witness_limit_is_stated", "seam_evidence_present_in_the_witness_layers", "left_out")
         or not ((u.get("measured") or {}).get("answerable_from_the_witnesses") or {}).get("left_out_means")])
    chk("B6", "writer ids and decision ids are the same ids in two spellings (the sidecar keys on the former)",
        [r["decision_id"] for r in rows if ids_in(c, r["writer_decision_id"]) != {r["decision_id"]}])
    words = P["severity_words"]
    sev = {r: {w: 0 for w in words} for r in by}

    def land(r, s):
        if r in sev and s in sev[r]:
            sev[r][s] += 1
    for p, d in c.packets.items():
        kind = c.kind_of[p]
        if kind == "primary":
            for it in d.get("items") or []:
                if str(it.get("verdict")).lower() == "challenge":
                    for r in ids_in(c, str(it.get("row_id"))):
                        land(r, it.get("severity"))
        elif kind == "final_audit":
            for it in d.get("rows") or []:
                for r in ids_in(c, str(it.get("row"))):
                    for f in it.get("findings") or []:
                        if not f.get("already_routed"):
                            land(r, f.get("severity"))
        else:
            for it in d.get("new_findings") or []:
                for r in ids_in(c, str(it.get("row_or_artifact") or "")):
                    land(r, it.get("severity"))
    chk("B7", "severities landed equal an independent recount from the packets",
        [u.get("internal_decision_id") for u in units
         if (u.get("measured") or {}).get("severities_landed") != sev.get(u.get("internal_decision_id"))])
    excl = re.compile(P["device_family_excluded_regex"])
    dv = set()
    for f in c.inventory["formulae"].values():
        if not excl.search(str(f.get("family"))):
            for k in P["device_verse_keys"].values():
                dv |= set(f.get(k) or [])
    mk = set(c.marks[P["marks"]["counted_key"]])

    def ev(v, side):
        return v in dv or (v in mk and side == P["marks"]["counted_face"])
    bad = []
    for i, r in enumerate(order):
        u = unit_by_cid.get(cid_of[r["decision_id"]]) or {}
        rec = ((u.get("measured") or {}).get("seam_evidence") or {}).get("onset") or {}
        if i == 0:
            if rec.get("evidence_on_both_faces") is not None:
                bad.append(r["decision_id"])
            continue
        a = pri[pos[order[i - 1]["span"].partition("-")[2]]][0]
        b = pri[pos[r["span"].partition("-")[0]]][0]
        if rec.get("evidence_on_both_faces") != (ev(a, "left") and ev(b, "right")):
            bad.append(r["decision_id"])
    chk("B8", "onset seam evidence on both faces equals a re-derivation from the marks file and the inventory", bad)

    # open questions
    qid = [q.get("question_id") for q in qs]
    chk("C1", "every routed end-review item is an open-question record, once",
        sorted({"routed:" + r["id"] for r in c.routed} ^ {x for x in qid if str(x).startswith("routed:")})
        + (["duplicate"] if len(qid) != len(set(qid)) else []))
    routed_ids = [r["id"] for r in c.routed]
    strat = re.compile(P["strategy_open_regex"])
    expect = {
        "unresolved_in_packet": sum(len(d.get("unresolved_uncertainty") or []) for d in c.packets.values()),
        "unresolved_in_ruling": sum(len(d[1].get("unresolved_uncertainty") or []) for d in c.rulings.values()),
        "escalation_in_packet": sum(len(d.get("escalations") or []) for d in c.packets.values())
        + sum(len(d[1].get("escalations") or []) for d in c.rulings.values()),
        "device_inventory_end_review_item": len(c.inventory.get(P["inventory_open_key"]) or []),
        "strategy_line_for_end_review": sum(1 for ln in c.strategy if strat.search(ln)),
        "finding_routed_to_end_review": sum(
            1 for p, d in c.packets.items() if c.kind_of[p] == "spot_review" for f in d.get("new_findings") or []
            if str(f.get("route")) == P["end_review_route"]
            and not any(x == str(f.get("id")) or x.endswith("-" + str(f.get("id"))) for x in routed_ids))}
    chk("C2", "every unresolved entry, escalation, inventory end-review item, strategy line and end-review finding "
              "without a routed id is an open-question record",
        ["%s: %d sources, %d records" % (k, v, sum(1 for q in qs if q.get("kind") == k))
         for k, v in sorted(expect.items()) if v != sum(1 for q in qs if q.get("kind") == k)])
    chk("C3", "every open question carries one of the four blast-radius classes, labelled as assigned by rule",
        [q.get("question_id") for q in qs if (q.get("blast_radius") or {}).get("class") not in CLASSES
         or (q.get("blast_radius") or {}).get("tier") != "JUDGED_BY_RULE"])
    rt = {"routed:" + r["id"]: " ".join(str(r.get(k) or "") for k in ("id", "order", "decision")) for r in c.routed}
    chk("C4", "no convention question is filed as one unit (the record's own convention words, and this checker's "
              "own words over the routed items' text)",
        [q.get("question_id") for q in qs if q["blast_radius"]["class"] == "one_unit"
         and (q["measured"]["convention_words"] or q["measured"]["units_named_count"] != 1
              or MY_CONVENTION.search(rt.get(q["question_id"], "")))])
    chk("C5", "a question that names no unit is never filed as one unit or several units",
        [q.get("question_id") for q in qs if q["measured"]["units_named_count"] == 0
         and q["blast_radius"]["class"] in ("one_unit", "several_units")])
    chk("C6", "a routed item whose id names no unit is filed one_book or wider",
        [q.get("question_id") for q in qs if str(q.get("question_id")).startswith("routed:")
         and not c.rowref.search(q["question_id"]) and q["blast_radius"]["class"] in ("one_unit", "several_units")])

    # linkages
    def reach(o):
        t = o if isinstance(o, str) else json.dumps(o, ensure_ascii=False)
        out = set()
        pre = P["verse_prefix"]
        for a, b in c.cref.findall(t):
            k = "%s.%s.%s" % (pre, a, b)
            if k in unit_at:
                out.add(unit_at[k])
        for n in c.chap.findall(t):
            out |= {u for v, u in unit_at.items() if v.startswith("%s.%s." % (pre, n))}
        return out

    def at(doc, loc):
        m = re.match(r"(\w+)\[(\d+)\]$", loc)
        return doc[m.group(1)][int(m.group(2))]

    def question_object(p, loc):
        if loc.startswith("routed:"):
            if p != P["routed_path_in_m8"]:
                raise KeyError(p)
            return [{k: r.get(k) for k in ("id", "order", "decision")} for r in c.routed if "routed:" + r["id"] == loc][0]
        if loc.startswith("device_inventory#"):
            return at(c.inventory, loc.split("#")[1])
        if loc.startswith("strategy#line["):
            return c.strategy[int(re.search(r"\[(\d+)\]", loc).group(1)) - 1]
        tail = loc.split("#")[1].replace("unresolved[", "unresolved_uncertainty[")
        return at(c.packets[p] if p in c.packets else c.rulings[p][1], tail)

    def source_names(s, pair):
        p, loc, kind = s.get("path"), str(s.get("locator")), s.get("kind")
        try:
            if kind in ("named_inside_a_review_item_on_the_other_unit", "named_together_in_a_review_finding"):
                return set(pair) <= ids_in(c, at(c.packets[p], loc))
            if kind == "cross_reference_written_in_a_review_item":
                obj = at(c.packets[p], loc)
                named, cited = ids_in(c, obj), reach(obj)
                return (pair[0] in named and pair[1] in cited) or (pair[1] in named and pair[0] in cited)
            if kind == "named_together_in_a_controlling_ruling":
                label, doc = c.rulings[p]
                return any(set(pair) <= ids_in(c, e) for e in doc["rulings"] if loc == "%s:%s" % (label, e.get("id")))
            if kind == "named_together_in_an_open_question":
                obj = question_object(p, loc)
                return set(pair) <= (ids_in(c, obj) | reach(obj) | ids_in(c, loc))
        except (KeyError, IndexError, AttributeError, TypeError, ValueError):
            return False
        return False
    bad_src, bad_diff, bad_stmt = [], [], []
    for l in links:
        pair = l.get("pair") or []
        if len(pair) != 2 or not set(pair) <= set(by) or not l.get("sources") \
                or not all(source_names(s, pair) for s in l["sources"]):
            bad_src.append(pair)
            continue
        a, b = by[pair[0]], by[pair[1]]
        d = [f for f in ("confidence", "unit_type") if a[f] != b[f]]
        if l.get("differs_in") != d or l.get("treated_differently") != bool(d):
            bad_diff.append(pair)
        st = l.get("statement") or {}
        if st.get("verdict") not in VERDICTS or not st.get("basis") or (bool(d) == (st.get("verdict") == "same_treatment")) \
                or (st.get("basis") == "standing_after_controlling_ruling" and not st.get("ruling_entries_naming_both")):
            bad_stmt.append(pair)
    chk("D1", "every linkage is harvested from a named source: each source, re-opened at its locator, names both "
              "units (a cross-reference names one and cites a verse inside the other)", bad_src)
    chk("D2", "treated-differently equals a re-comparison of the two final rows", bad_diff)
    chk("D3", "every linked pair treated differently carries a statement (real distinction or possible "
              "inconsistency) with its basis; none is unremarked", bad_stmt)

    # sidecar
    side = lines(side_bytes)
    want_w = {r["writer_decision_id"] for r in rows if r["confidence"] in P["select_confidence"]}
    got_w = [s.get("writer_decision_id") for s in side]
    chk("E1", "the sidecar has exactly the selected rows, once each, and every required field is non-empty",
        sorted(want_w ^ set(got_w)) + (["duplicate"] if len(got_w) != len(set(got_w)) else [])
        + [s.get("writer_decision_id") for s in side for k in SIDE_FIELDS if not str(s.get(k) or "").strip()])
    side_whys = [s.get("why_low_confidence") or "" for s in side]
    chk("E2", "every sidecar why_low_confidence is unique and equals the atlas row's",
        [w[:60] for w in side_whys if side_whys.count(w) > 1]
        + [s.get("writer_decision_id") for s in side if s.get("why_low_confidence")
           not in {f.get("why_low_confidence") for f in feed}])
    return out


TAMPERS = ["drop_feed_row", "hold_a_row", "witness_bytes_in_prose", "duplicate_why", "extra_feed_field",
           "untraceable_sentence", "wrong_final_state", "flip_contested", "wrong_primary_span", "severity_count",
           "flip_seam_evidence", "convention_as_one_unit", "drop_routed_question", "drop_inventory_question",
           "routed_process_item_narrowed", "linkage_without_source", "linkage_wrong_source", "unremarked_divergence",
           "sidecar_missing_row", "sidecar_duplicate_why"]


def tamper(c, name, feed, dims, side):
    P = c.P
    feed, dims, side = copy.deepcopy(feed), copy.deepcopy(dims), copy.deepcopy(side)
    units = [d for d in dims if d["record"] == "unit"]
    qs = [d for d in dims if d["record"] == "open_question"]
    links = [d for d in dims if d["record"] == "linkage"]
    diff = [l for l in links if l["treated_differently"]]
    if name == "drop_feed_row":
        feed.pop(0)
    elif name == "hold_a_row":
        feed[0]["candidate_hold_state"] = "held"
    elif name == "witness_bytes_in_prose":
        feed[0]["why_low_confidence"] += " " + P["tamper_witness_char"]
    elif name == "duplicate_why":
        feed[1]["why_low_confidence"] = feed[0]["why_low_confidence"]
    elif name == "extra_feed_field":
        feed[0]["atlas_hardness"] = "high"
    elif name == "untraceable_sentence":
        feed[0]["why_low_confidence"] += " This sentence was never written in the row and should not pass."
    elif name == "wrong_final_state":
        feed[0]["review_packet_final_state"] = P["final_state"]["other_value"]
    elif name == "flip_contested":
        m = units[0]["measured"]["contested_between_blind_lanes"]
        m["verdicts_differ"] = not m["verdicts_differ"]
    elif name == "wrong_primary_span":
        units[5]["measured"]["span_primary"] = "%s.1.1-%s.1.1" % (P["verse_prefix"], P["verse_prefix"])
    elif name == "severity_count":
        units[0]["measured"]["severities_landed"][P["severity_words"][0]] += 1
    elif name == "flip_seam_evidence":
        o = units[1]["measured"]["seam_evidence"]["onset"]
        o["evidence_on_both_faces"] = not o["evidence_on_both_faces"]
    elif name == "convention_as_one_unit":
        q = [q for q in qs if q["measured"]["convention_words"]][0]
        q["blast_radius"]["class"] = "one_unit"
    elif name == "drop_routed_question":
        dims.remove([q for q in qs if q["question_id"].startswith("routed:")][0])
    elif name == "drop_inventory_question":
        dims.remove([q for q in qs if q["kind"] == "device_inventory_end_review_item"][0])
    elif name == "routed_process_item_narrowed":
        q = [q for q in qs if q["question_id"].startswith("routed:") and not c.rowref.search(q["question_id"])][0]
        q["blast_radius"]["class"] = "several_units"
        q["measured"]["units_named_count"] = 2
    elif name == "linkage_without_source":
        links[0]["sources"] = []
    elif name == "linkage_wrong_source":
        partners = {x for l in links if links[0]["pair"][0] in l["pair"] for x in l["pair"]}
        links[0]["pair"] = [links[0]["pair"][0], [u["internal_decision_id"] for u in units
                                                  if u["internal_decision_id"] not in partners][0]]
    elif name == "unremarked_divergence":
        diff[0]["statement"] = {}
    elif name == "sidecar_missing_row":
        side.pop(0)
    elif name == "sidecar_duplicate_why":
        side[1]["why_low_confidence"] = side[0]["why_low_confidence"]
    return feed, dims, side


def arg(flag):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else None


def main():
    params = Path(arg("--params") or HERE / "book_params.v1.json")
    book_root = Path(arg("--book-root") or HERE.parent)
    out_root = Path(arg("--out-root") or book_root)
    raw = params.read_bytes()
    P = json.loads(raw.decode("utf-8"))
    c = load_context(book_root, P)
    fp, dp, sp = (out_root / "deliverables" / P["outputs"]["feed"], out_root / "deliverables" / P["outputs"]["dimensions"],
                  out_root / P["outputs"]["sidecar"])
    fb, db, sb = fp.read_bytes(), dp.read_bytes(), sp.read_bytes()
    checks = run_checks(c, fb, db, sb)
    failed = [x["id"] for x in checks if x["result"] != "PASS"]
    selftest = {}
    for name in TAMPERS:
        f2, d2, s2 = tamper(c, name, lines(fb), lines(db), lines(sb))
        selftest[name] = [x["id"] for x in run_checks(c, dump(f2), dump(d2), dump(s2)) if x["result"] != "PASS"]
    if "--selftest" in sys.argv:
        for name in TAMPERS:
            print("selftest %-30s %s" % (name, "caught by " + ",".join(selftest[name]) if selftest[name] else "NOT CAUGHT"))
        missed = [n for n in TAMPERS if not selftest[n]]
        print("SELFTEST: %s" % ("PASS" if not missed and not failed else "FAIL"))
        sys.exit(0 if not missed and not failed else 1)
    common = ["--params", str(params), "--book-root", str(book_root), "--out-root", str(out_root), "--check"]
    last = {}
    for script in ("gen_atlas_rows.py", "gen_sidecars.py"):
        g = subprocess.run([sys.executable, "-B", str(HERE / script)] + common, capture_output=True, text=True, encoding="utf-8")
        last[script] = {"exit": g.returncode, "last_line": (g.stdout.strip().splitlines() or [""])[-1]}
    gen_ok = last["gen_atlas_rows.py"]["last_line"] == "DETERMINISTIC: MATCH" and last["gen_sidecars.py"]["last_line"] == "MATCH"
    dims = lines(db)
    ok = not failed and all(selftest.values()) and gen_ok
    rec = {"schema": P["schemas"]["check"], "book": P["book"], "overall": "PASS" if ok else "FAIL",
           "params_sha256": sha(raw),
           "checked": {fp.name: sha(fb), dp.name: sha(db), sp.name: sha(sb)},
           "inputs_sha256": dict(sorted(P["pins"].items())),
           "packets_reopened": len(c.packets),
           "counts": {"feed_rows": len(lines(fb)), "units": sum(1 for d in dims if d["record"] == "unit"),
                      "open_questions": sum(1 for d in dims if d["record"] == "open_question"),
                      "linkages": sum(1 for d in dims if d["record"] == "linkage"),
                      "linkages_treated_differently": sum(1 for d in dims if d["record"] == "linkage" and d["treated_differently"])},
           "checks": checks,
           "selftest": {"what": "each tamper is applied in memory to a copy of the outputs; a tamper that no check "
                                "catches fails the run", "caught_by": selftest},
           "generator_check": last,
           "tier": "MEASURED by this checker; it shares no code with the generator, but it was written by the same "
                   "builder on the same model family, so it is not independent review",
           "limit": "The checker proves form, mirroring, tracing and harvest. It cannot prove that a rule-assigned "
                    "class or statement is the right reading; those are labelled JUDGED_BY_RULE."}
    data = (json.dumps(rec, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    target = out_root / "deliverables" / P["outputs"]["check"]
    for x in checks:
        if x["result"] != "PASS":
            print("FAIL %s %s %s" % (x["id"], x["failures"], x["first_failures"]))
    print("checks %d  failed %d  tampers %d  uncaught %d  generators %s"
          % (len(checks), len(failed), len(TAMPERS), sum(1 for v in selftest.values() if not v),
             [v["last_line"] for _k, v in sorted(last.items())]))
    if "--check" in sys.argv:
        try:
            on = sha(target.read_bytes())
        except FileNotFoundError:
            on = "ABSENT"
        print("%-34s on_disk %s  rebuilt %s" % (target.name, on[:12], sha(data)[:12]))
        print("MATCH" if ok and on == sha(data) else "DIFFERS")
        sys.exit(0 if ok and on == sha(data) else 1)
    target.write_bytes(data)
    print("ATLAS ROWS CHECK: %s" % ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
