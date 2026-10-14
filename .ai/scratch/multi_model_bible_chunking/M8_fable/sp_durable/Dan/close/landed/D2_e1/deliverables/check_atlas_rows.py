#!/usr/bin/env python3
"""Check Daniel's atlas candidate rows and dimensions record (close-gate item 22).

This checker imports nothing from the generator. It re-measures from the pinned inputs by its own means:
the two numberings are aligned by POSITION (the n-th verse of one witness is the n-th verse of the other),
not by the generator's zone arithmetic; the blind lanes' verdicts are re-read from the packets; every linkage
source is re-opened and must name both units; the routed items are re-read and tested with this file's own
convention words.

Usage: check_atlas_rows.py [--dan-root DIR] [--out-root DIR] [--selftest]
       writes deliverables/atlas_rows_check.v1.json under --out-root; exit 0 only when every check passes,
       every tamper of the self-test is caught, and the generator's --check prints DETERMINISTIC: MATCH.
No clock, no randomness, no directory scan.
"""
import copy
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PINS = {
    "rows_v1_final.jsonl": "783a0e9ac2c8fe4c942b3b8f7dd65efaefdb28f6fcb55fdde42b500a5c395e09",
    "close/dan_landed_outputs_manifest.v1.json": "316676f61170822036032027b1a635ff7a7ee1ad229318b56a7d267b3a1fe378",
    "fable_end_review/routed_items.v1.jsonl": "42efe601b731e212ba60bc9b19fd9b3199d86e8d5a152bb7571f8e956376b0d6",
    "Dan_oshb.txt": "8424e3630879c53a44530dee0b87e6c1a64f020619a3c3c0ac758a387a33b3a0",
    "Dan_web_clean.txt": "532fc0e391ac63777e1f57303213b3aaef4ce32071bede797a488bfcee5b6cfa",
}
RULING_PINS = {
    1: "541e3c1958d0bbf723d1537a0a00f62e16f207bf54d12ec11ae86f7d4bd9da30",
    2: "43ae72e748fe1e55be3103e826194672a3b317300ff413d690682697b121f940",
    3: "680b621d178e1f1c173204d504131c7c80f0de6a78bfe93dd52a10a060c318c0",
    4: "ff21977a7c635f5104c810053f773a5f7c74a03a548bdd39f16d1f04f7adc6e1",
    5: "a447f1412ca0e56d7ab55b31ed5c1edd3ce34898b4904a462d5b9b03e702f97d",
    6: "d1626dea516a88039fbc6124934994f973b99c7d1e615b4ce435e31feb646759",
    7: "0648ec2988fac5d25cb48026bf0ff4268674910c2c62dd684435b2bf8fbca9ef",
    8: "2e1877aa81f32b6e35d0154b5e196cc33393fe24c18a0c850cb38570b851f42c",
    9: "73a482ab17232319f3c4384cd57d56f5207423953538f1b56db12947605f7e13",
    10: "ef7a3e0028eca463fbe011e5c166b6ea38d825ded7abd12fc1a832413db9b85d",
    11: "54c547cdec3fe96e2a3ba000326c801e87dcd0c306bf21d3bd5cc6e141c71fc8",
    12: "8bc16d34306a990deeb39637e6314b5465da6865dbd647fb4b456a905a2285e1",
}
EXPECT_KEYS = ["model_id", "book", "span", "chunk_decision_id", "confidence", "observed_substrate_signals",
               "review_packet_final_state", "chunk_review_status", "candidate_hold_state", "non_authorizing",
               "concern_type", "why_low_confidence", "possible_downstream_risk", "suggested_reviewer",
               "proposed_atlas_action", "atlas_promotion_authority"]
PACKET = re.compile(r"/(rev_(LF|OL)_c\d\d|peer_g\d\d|p13_(OS|TB)|p13r7_(OS|TB)|rr(8|9|10)_(OS|TB)"
                    r"|dan_boss_audit\.v1|dan_boss_audit_b8_b14)\.json$")
BAD_BYTES = re.compile("[֐-׿יִ-ﭏ\"“”]")
BAD_CODE = re.compile(r"\bW\d+-\d+\b|\bE\d{1,2}\b|\bCWO\b|FIXUP|\bP13\b|\bOW-\d+|\.json", re.I)
MY_CONVENTION = re.compile(r"convention|\bclass\b|\brule\b|\bpolicy\b", re.I)
CLASSES = {"one_unit", "several_units", "one_book", "campaign_wide"}
VERDICTS = {"same_treatment", "real_distinction", "possible_inconsistency_unruled"}
ROUTED_PATH = "sp_durable/Dan/fable_end_review/routed_items.v1.jsonl"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def pinned(path, digest):
    b = path.read_bytes()
    if sha(b) != digest:
        raise SystemExit("REFUSED: %s moved since it was pinned" % path.name)
    return b


def lines(b):
    return [json.loads(x) for x in b.decode("utf-8").splitlines() if x.strip()]


def ids_in(o):
    t = json.dumps(o, ensure_ascii=False)
    return {"W%s-%03d" % (a, int(b)) for a, b in re.findall(r"\bW([1-9])-(\d{1,3})\b", t)}


def load_context(dan_root):
    m8 = dan_root.parent.parent
    c = {"m8": m8}
    c["rows"] = lines(pinned(dan_root / "rows_v1_final.jsonl", PINS["rows_v1_final.jsonl"]))
    c["routed"] = lines(pinned(dan_root / "fable_end_review" / "routed_items.v1.jsonl",
                               PINS["fable_end_review/routed_items.v1.jsonl"]))
    mt = []
    for ln in pinned(dan_root / "Dan_oshb.txt", PINS["Dan_oshb.txt"]).decode("utf-8").splitlines():
        k, _, t = ln.partition("\t")
        if re.match(r"Dan\.\d+\.\d+$", k):
            mt.append((k, len(t.split())))
    web, ch = [], None
    for ln in pinned(dan_root / "Dan_web_clean.txt", PINS["Dan_web_clean.txt"]).decode("utf-8").splitlines():
        m = re.match(r"===== DAN (\d+) =====", ln)
        if m:
            ch = m.group(1)
        m = re.match(r"\[v\] (\d+)\b", ln)
        if m and ch:
            web.append("Dan.%s.%s" % (ch, m.group(1)))
    c["mt"], c["web"] = mt, web
    man = json.loads(pinned(dan_root / "close" / "dan_landed_outputs_manifest.v1.json",
                            PINS["close/dan_landed_outputs_manifest.v1.json"]).decode("utf-8"))
    docs = {}
    for o in man["outputs"]:
        if PACKET.search("/" + o["path"]) and "final_message" not in o["path"]:
            docs[o["path"]] = json.loads(pinned(m8 / o["path"], o["sha256"]).decode("utf-8"))
    c["packets"] = dict(docs)
    c["rulings"] = {}
    for n, d in RULING_PINS.items():
        p = "sp_durable/Dan/review/dan_controlling_agent_rulings_E%d.v1.json" % n
        c["rulings"][p] = json.loads(pinned(m8 / p, d).decode("utf-8"))
    return c


def run_checks(c, feed_bytes, dims_bytes):
    out = []

    def chk(cid, claim, bad):
        bad = list(bad)
        out.append({"id": cid, "claim": claim, "result": "PASS" if not bad else "FAIL",
                    "failures": len(bad), "first_failures": [str(x)[:160] for x in bad[:3]]})
    rows = c["rows"]
    by = {r["decision_id"]: r for r in rows}
    cid_of = {r["decision_id"]: "M8-Dan-%03d" % r["chunk_index_in_book"] for r in rows}
    by_cid = {cid_of[k]: r for k, r in by.items()}
    feed_text, dims_text = feed_bytes.decode("utf-8"), dims_bytes.decode("utf-8")
    chk("A1", "both outputs are LF-only UTF-8 with a final newline",
        [n for n, t in (("feed", feed_text), ("dims", dims_text)) if "\r" in t or not t.endswith("\n")])
    feed, dims = lines(feed_bytes), lines(dims_bytes)
    units = [d for d in dims if d.get("record") == "unit"]
    qs = [d for d in dims if d.get("record") == "open_question"]
    links = [d for d in dims if d.get("record") == "linkage"]
    chk("A2", "every feed row has exactly the 16 shared-feed fields, in order",
        [f.get("chunk_decision_id") for f in feed if list(f.keys()) != EXPECT_KEYS])
    want = {cid_of[r["decision_id"]] for r in rows if r["confidence"] in ("low", "medium_low")}
    got = [f.get("chunk_decision_id") for f in feed]
    chk("A3", "feed rows are exactly the final rows graded low or medium_low, once each",
        sorted(want ^ set(got)) + (["duplicate"] if len(got) != len(set(got)) else []))
    bad = []
    for f in feed:
        r = by_cid.get(f.get("chunk_decision_id"))
        if r is None:
            bad.append(f.get("chunk_decision_id"))
            continue
        if not (f["span"] == r["span"] and f["confidence"] == r["confidence"]
                and f["chunk_review_status"] == r["review_status"] and f["candidate_hold_state"] is None
                and r["candidate_hold_state"] is None and f["review_packet_final_state"] == "accepted_candidate"
                and f["non_authorizing"] is True and f["atlas_promotion_authority"] == "none"
                and f["proposed_atlas_action"] == "consider_only" and f["model_id"] == "M8_fable"
                and f["book"] == "Dan" and f["observed_substrate_signals"] == (r.get("observed_substrate_signals") or [])):
            bad.append(f["chunk_decision_id"])
    chk("A4", "each feed row mirrors its corpus row: span, confidence, review state, null hold, accepted_candidate, "
              "non-authorizing, no promotion authority", bad)
    chk("A5", "no witness bytes, quotation mark or internal code in any feed prose field",
        [f["chunk_decision_id"] for f in feed
         for k in ("why_low_confidence", "possible_downstream_risk", "concern_type", "suggested_reviewer")
         if BAD_BYTES.search(str(f.get(k) or "")) or BAD_CODE.search(str(f.get(k) or ""))])
    whys = [f.get("why_low_confidence") or "" for f in feed]
    chk("A6", "every why_low_confidence is non-empty and unique",
        [w[:60] for w in whys if not w.strip() or whys.count(w) > 1])
    unit_by_cid = {u.get("chunk_decision_id"): u for u in units}
    bad = []
    for f in feed:
        r, u = by_cid.get(f.get("chunk_decision_id")), unit_by_cid.get(f.get("chunk_decision_id"))
        if r is None or u is None or (u.get("derivation") or {}).get("composed_not_derived"):
            continue
        src = " ".join((r.get(k) or "").replace("\n", " ") for k in ("device_notes", "strongest_rejected_alternative"))
        for s in re.split(r"(?<=[.;])\s+", f["why_low_confidence"]):
            s = s.strip()
            if s.startswith("Recorded alternative: "):
                s = s[len("Recorded alternative: "):]
            if s and s not in src and s[:-1] not in src:
                bad.append("%s: %s" % (f["chunk_decision_id"], s[:80]))
    chk("A7", "every sentence of why_low_confidence is found verbatim in that row's own prose", bad)
    chk("A8", "no judged rating travels in the feed",
        [f["chunk_decision_id"] for f in feed if re.search(r"hardness|JUDGED|score", json.dumps(f))])

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
    # numbering, by position
    web, mt = c["web"], c["mt"]
    pos = {v: i for i, v in enumerate(web)}
    bad, covered = [], []
    if len(web) != len(mt):
        bad.append("witness verse counts differ: %d vs %d" % (len(web), len(mt)))
    for r in sorted(rows, key=lambda r: r["chunk_index_in_book"]):
        a, _, b = r["span"].partition("-")
        u = unit_by_cid.get(cid_of[r["decision_id"]]) or {}
        if a not in pos or b not in pos or pos[a] > pos[b]:
            bad.append("span not on the WEB face: " + r["span"])
            continue
        covered.extend(range(pos[a], pos[b] + 1))
        m = u.get("measured") or {}
        if (m.get("span_mt") != "%s-%s" % (mt[pos[a]][0], mt[pos[b]][0]) or m.get("verses") != pos[b] - pos[a] + 1
                or m.get("words_mt") != sum(w for _v, w in mt[pos[a]:pos[b] + 1])):
            bad.append("MT span or size differs for " + r["span"])
    if covered != list(range(len(web))):
        bad.append("the spans do not tile the book once each, in order")
    chk("B3", "every span exists on both witnesses, the spans tile the book, and each unit's MT span and size match "
              "an independent positional alignment of the two numberings", bad)
    # contested, independently
    seen = {}
    for p, d in c["packets"].items():
        m = re.search(r"/rev_(LF|OL)_c\d\d\.json$", p)
        if not m:
            continue
        for it in d.get("items") or []:
            k = sorted(ids_in(it.get("row_id")))
            if k:
                seen.setdefault(k[0], {}).setdefault(m.group(1), set()).add(it.get("verdict"))
    bad = []
    for u in units:
        s = seen.get(u.get("internal_decision_id")) or {}
        mine = bool(s.get("LF") and s.get("OL") and s["LF"] != s["OL"])
        if ((u.get("measured") or {}).get("contested_between_blind_lanes") or {}).get("verdicts_differ") != mine:
            bad.append(u.get("internal_decision_id"))
    chk("B4", "contested-between-blind-lanes equals an independent re-read of the two lanes' verdicts", bad)
    chk("B5", "answerable-from-the-witnesses is one of three stated values, and left_out says what it means",
        [u.get("chunk_decision_id") for u in units
         if ((u.get("measured") or {}).get("answerable_from_the_witnesses") or {}).get("value")
         not in ("a_witness_limit_is_stated", "seam_evidence_present_in_the_witness_layers", "left_out")
         or not ((u.get("measured") or {}).get("answerable_from_the_witnesses") or {}).get("left_out_means")])
    chk("B6", "writer ids and decision ids are the same ids in two spellings (the sidecar keys on the former)",
        [r["decision_id"] for r in rows if ids_in(r["writer_decision_id"]) != {r["decision_id"]}])

    # open questions
    qid = [q.get("question_id") for q in qs]
    chk("C1", "every routed end-review item is an open-question record, once",
        sorted({"routed:" + r["id"] for r in c["routed"]} ^ {x for x in qid if str(x).startswith("routed:")})
        + (["duplicate"] if len(qid) != len(set(qid)) else []))
    n_uu = sum(len(d.get("unresolved_uncertainty") or []) for d in list(c["packets"].values()) + list(c["rulings"].values()))
    chk("C2", "every unresolved entry of every landed packet and ruling is an open-question record",
        [] if n_uu == sum(1 for x in qid if not str(x).startswith("routed:")) else
        ["%d entries, %d records" % (n_uu, sum(1 for x in qid if not str(x).startswith("routed:")))])
    chk("C3", "every open question carries one of the four blast-radius classes, labelled as assigned by rule",
        [q.get("question_id") for q in qs if (q.get("blast_radius") or {}).get("class") not in CLASSES
         or (q.get("blast_radius") or {}).get("tier") != "JUDGED_BY_RULE"])
    rt = {"routed:" + r["id"]: " ".join(str(r.get(k) or "") for k in ("id", "order", "decision")) for r in c["routed"]}
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
         and not re.search(r"W\d-\d", q["question_id"]) and q["blast_radius"]["class"] in ("one_unit", "several_units")])

    # linkages
    def source_names(s, pair):
        p, loc, kind = s.get("path"), str(s.get("locator")), s.get("kind")
        try:
            if kind == "named_inside_a_review_item_on_the_other_unit":
                m = re.match(r"(\w+)\[(\d+)\]$", loc)
                obj = c["packets"][p][m.group(1)][int(m.group(2))]
            elif kind == "named_together_in_a_controlling_ruling":
                obj = [e for e in c["rulings"][p]["rulings"] if loc == "%s:%s" % (re.search(r"_(E\d+)\.v1", p).group(1), e.get("id"))]
                obj = obj[0]
            elif loc.startswith("routed:"):
                obj = [{k: r.get(k) for k in ("order", "decision")} for r in c["routed"] if "routed:" + r["id"] == loc][0]
                if p != ROUTED_PATH:
                    return False
            else:
                i = int(re.search(r"#unresolved\[(\d+)\]$", loc).group(1))
                obj = (c["packets"].get(p) or c["rulings"][p])["unresolved_uncertainty"][i]
        except (KeyError, IndexError, AttributeError, TypeError):
            return False
        return set(pair) <= ids_in(obj)
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
    chk("D1", "every linkage is harvested from a packet: each source, re-opened at its locator, names both units", bad_src)
    chk("D2", "treated-differently equals a re-comparison of the two final rows", bad_diff)
    chk("D3", "every linked pair treated differently carries a statement (real distinction or possible "
              "inconsistency) with its basis; none is unremarked", bad_stmt)
    return out


TAMPERS = ["drop_feed_row", "hold_a_row", "hebrew_in_prose", "duplicate_why", "extra_feed_field",
           "untraceable_sentence", "flip_contested", "wrong_mt_span", "convention_as_one_unit",
           "drop_routed_question", "routed_process_item_narrowed", "linkage_without_source", "linkage_wrong_source", "unremarked_divergence"]


def tamper(name, feed, dims):
    feed, dims = copy.deepcopy(feed), copy.deepcopy(dims)
    units = [d for d in dims if d["record"] == "unit"]
    qs = [d for d in dims if d["record"] == "open_question"]
    links = [d for d in dims if d["record"] == "linkage"]
    diff = [l for l in links if l["treated_differently"]]
    if name == "drop_feed_row":
        feed.pop(0)
    elif name == "hold_a_row":
        feed[0]["candidate_hold_state"] = "held"
    elif name == "hebrew_in_prose":
        feed[0]["why_low_confidence"] += " א"
    elif name == "duplicate_why":
        feed[1]["why_low_confidence"] = feed[0]["why_low_confidence"]
    elif name == "extra_feed_field":
        feed[0]["atlas_hardness"] = "high"
    elif name == "untraceable_sentence":
        feed[0]["why_low_confidence"] += " This sentence was never written in the row and should not pass."
    elif name == "flip_contested":
        m = units[0]["measured"]["contested_between_blind_lanes"]
        m["verdicts_differ"] = not m["verdicts_differ"]
    elif name == "wrong_mt_span":
        units[5]["measured"]["span_mt"] = "Dan.1.1-Dan.1.1"
    elif name == "convention_as_one_unit":
        q = [q for q in qs if q["measured"]["convention_words"]][0]
        q["blast_radius"]["class"] = "one_unit"
    elif name == "drop_routed_question":
        dims.remove([q for q in qs if q["question_id"].startswith("routed:")][0])
    elif name == "routed_process_item_narrowed":
        q = [q for q in qs if q["question_id"].startswith("routed:") and not re.search(r"W\d-\d", q["question_id"])][0]
        q["blast_radius"]["class"] = "several_units"
        q["measured"]["units_named_count"] = 2
    elif name == "linkage_without_source":
        links[0]["sources"] = []
    elif name == "linkage_wrong_source":
        links[0]["pair"] = [links[0]["pair"][0], [u["internal_decision_id"] for u in units
                                                  if u["internal_decision_id"] not in links[0]["pair"]
                                                  and u["internal_decision_id"] not in
                                                  {x for l in links if links[0]["pair"][0] in l["pair"] for x in l["pair"]}][0]]
    elif name == "unremarked_divergence":
        diff[0]["statement"] = {}
    return feed, dims


def dump(objs):
    return "".join(json.dumps(o, ensure_ascii=False) + "\n" for o in objs).encode("utf-8")


def main():
    dan_root, out_root = HERE.parent, None
    for flag in ("--dan-root", "--out-root"):
        if flag in sys.argv:
            v = Path(sys.argv[sys.argv.index(flag) + 1])
            if flag == "--dan-root":
                dan_root = v
            else:
                out_root = v
    out_root = out_root or dan_root
    c = load_context(dan_root)
    fb = (out_root / "deliverables" / "atlas_candidate_feed_rows.jsonl").read_bytes()
    db = (out_root / "deliverables" / "Dan_atlas_dimensions.v1.jsonl").read_bytes()
    checks = run_checks(c, fb, db)
    failed = [x["id"] for x in checks if x["result"] != "PASS"]
    if "--selftest" in sys.argv:
        missed = []
        for name in TAMPERS:
            f2, d2 = tamper(name, lines(fb), lines(db))
            caught = [x["id"] for x in run_checks(c, dump(f2), dump(d2)) if x["result"] != "PASS"]
            print("selftest %-26s %s" % (name, "caught by " + ",".join(caught) if caught else "NOT CAUGHT"))
            if not caught:
                missed.append(name)
        print("SELFTEST: %s" % ("PASS" if not missed and not failed else "FAIL"))
        sys.exit(0 if not missed and not failed else 1)
    selftest = {}
    for name in TAMPERS:
        f2, d2 = tamper(name, lines(fb), lines(db))
        selftest[name] = [x["id"] for x in run_checks(c, dump(f2), dump(d2)) if x["result"] != "PASS"]
    gen = subprocess.run([sys.executable, "-B", str(HERE / "gen_atlas_rows.py"), "--dan-root", str(dan_root),
                          "--out-root", str(out_root), "--check"], capture_output=True, text=True, encoding="utf-8")
    gen_last = (gen.stdout.strip().splitlines() or [""])[-1]
    dims = lines(db)
    ok = not failed and all(selftest.values()) and gen.returncode == 0 and gen_last == "DETERMINISTIC: MATCH"
    rec = {"schema": "dan_atlas_rows_check.v1", "book": "Dan", "overall": "PASS" if ok else "FAIL",
           "checked": {"atlas_candidate_feed_rows.jsonl": sha(fb), "Dan_atlas_dimensions.v1.jsonl": sha(db)},
           "inputs_sha256": dict(sorted(PINS.items())),
           "ruling_inputs_sha256": {"E%d" % n: d for n, d in sorted(RULING_PINS.items())},
           "packets_reopened": len(c["packets"]),
           "counts": {"feed_rows": len(lines(fb)), "units": sum(1 for d in dims if d["record"] == "unit"),
                      "open_questions": sum(1 for d in dims if d["record"] == "open_question"),
                      "linkages": sum(1 for d in dims if d["record"] == "linkage"),
                      "linkages_treated_differently": sum(1 for d in dims if d["record"] == "linkage" and d["treated_differently"])},
           "checks": checks,
           "selftest": {"what": "each tamper is applied in memory to a copy of the outputs; a tamper that no check "
                                "catches fails the run", "caught_by": selftest},
           "generator_check": {"exit": gen.returncode, "last_line": gen_last},
           "tier": "MEASURED by this checker; it shares no code with the generator, but it was written by the same "
                   "builder on the same model family, so it is not independent review",
           "limit": "The checker proves form, mirroring, tracing and harvest. It cannot prove that a rule-assigned "
                    "class or statement is the right reading; those are labelled JUDGED_BY_RULE."}
    (out_root / "deliverables" / "atlas_rows_check.v1.json").write_bytes(
        (json.dumps(rec, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    for x in checks:
        if x["result"] != "PASS":
            print("FAIL %s %s %s" % (x["id"], x["failures"], x["first_failures"]))
    print("checks %d  failed %d  tampers %d  uncaught %d  generator %s"
          % (len(checks), len(failed), len(TAMPERS), sum(1 for v in selftest.values() if not v), gen_last))
    print("ATLAS ROWS CHECK: %s" % ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
