#!/usr/bin/env python3
"""Validate Ezekiel's atlas deliverable against the pinned records, with a negative control (method record v6, ob 12).

WHAT IT ESTABLISHES, rather than asserts:
  - the rows carry EXACTLY the shared feed's 16 fields, and their controlled values are drawn from the vocabulary
    MEASURED in the shared feed at run time (never a hardcoded list);
  - every span is a shipped Ezekiel row and every confidence matches that row's RECORDED grade;
  - the selection is the stated rule as SET EQUALITY, not as a count (method record s11);
  - no witness bytes and no internal campaign code appear in any prose field;
  - every row held in the corpus is held in the feed, and no other row is, and every feed row mirrors its corpus
    row's review status, hold state and packet state (AMENDED 2026-09-23, v10 hold round, OW-30: the held set
    was the second reading's STOP/GRADE_QUESTION set, and the selection added it at any grade);
  - the three s15 dimensions stay separated: no hardness or score reaches the feed rows;
  - the dependency facts in the sidecar are re-measured HERE, independently of the generator.

Nothing is imported from gen_atlas_rows.py on purpose: a checker that reuses the generator's own helpers shares its
bugs and proves only self-consistency.

Usage: check_atlas_rows.py [--selftest]      writes atlas_rows_check.v1.json; exit 0 PASS, 1 FAIL."""
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent
ROWS_IN = EZ / "rows_v10_final.jsonl"  # v10 hold round 2026-09-23 (OW-30); was rows_v9_final.jsonl, and
# before that repair/rows_v7_cwo24.jsonl
FINAL = EZ / "author" / "final"
FEED = EZ.parent.parent / "atlas_candidate_feed.jsonl"
OUT_ROWS = HERE / "atlas_candidate_feed_rows.jsonl"
OUT_DIM = HERE / "Ezek_atlas_dimensions.v1.jsonl"
GEN = HERE / "gen_atlas_rows.py"

PROSE = ("why_low_confidence", "possible_downstream_risk", "concern_type", "span", "chunk_decision_id")
HEB = re.compile(r"[֐-׿]")
CODE = re.compile(r"\[WARRANT|\bP\d{2}-\d{3}\b|\btier-\d\b|\bS[1-6]-\d{3}\b|\bK\d\b|rows_v\d|\.jsonl\b|\bOW-\d+\b")
# 'book' and 'confidence' are deliberately NOT vocabulary-constrained against the shared feed. 'book' is an identity
# field - a new book is the point. 'confidence' would wrongly reject the one grade the widened referral rule exists to
# carry (a row recorded high that the second reading still refused to act on); it gets its own check below instead,
# and every grade is verified row-by-row against the shipped record in spans_and_grades_are_the_shipped_ones.
CONTROLLED = ("model_id", "review_packet_final_state", "chunk_review_status", "candidate_hold_state",
              "non_authorizing", "proposed_atlas_action", "atlas_promotion_authority", "suggested_reviewer")
JUDGED_WORDS = ("hardness", "score", "judged")


def jl(p):
    return [json.loads(l) for l in Path(p).read_text(encoding="utf-8").splitlines() if l.strip()]


def vref(s):
    m = re.match(r"Ezek\.(\d+)\.(\d+)$", s or "")
    return (int(m.group(1)), int(m.group(2))) if m else None


def evaluate(rows_path, dims_path):
    res, failed = {}, []

    def check(name, ok, detail):
        res[name] = {"ok": bool(ok), "detail": str(detail)}
        if not ok:
            failed.append(name)

    feed_rows, dims = jl(rows_path), jl(dims_path)
    shipped = jl(ROWS_IN)
    shared = jl(FEED)
    by_span = {r["span"]: r for r in shipped}
    idx_of = {r["span"]: r.get("chunk_index_in_book") for r in shipped}

    stop, gq = set(), set()
    for k in range(1, 7):
        d = json.loads((FINAL / ("s%d_adjudication" % k) / "adjudication.json").read_text(encoding="utf-8"))
        for _iid, it in sorted((d.get("items") or {}).items()):
            if isinstance(it, dict):
                s = str(it.get("status", "")).split()[0] if it.get("status") else ""
                if s == "STOP":
                    stop.add(it.get("row") or "")
                elif s == "GRADE_QUESTION":
                    gq.add(it.get("row") or "")
    # AMENDED 2026-09-23 (v10 hold round, OW-30): a row is held exactly when its corpus row is held, and the selection
    # is low/medium_low only. The second reading's STOP/GRADE_QUESTION items no longer decide either; Fable's ruling
    # resolved each of them against the corpus (Ezek/fable_end_review/atlas_hold_ruling.v1.json).
    held_ids = {r["decision_id"] for r in shipped if r.get("candidate_hold_state") is not None}
    want = {r["span"] for r in shipped if str(r.get("confidence")) in ("low", "medium_low")}
    res["second_reading_items_no_longer_decide"] = {"ok": None, "detail":
        "DISCLOSED, not a failure: the second reading refused or grade-questioned %d rows; the corpus holds %d"
        % (len({r["decision_id"] for r in shipped if r["decision_id"] in stop | gq}), len(held_ids))}

    # The shared feed is itself heterogeneous: MEASURED 2026-09-21, 253 of its 384 rows carry 16 fields and 131 carry
    # 12 (an earlier generation lacking the four referral fields). The full form is the union, so that is the target -
    # taking row 0's keys would make the target depend on which generation happens to sort first.
    want_keys = set().union(*[set(r.keys()) for r in shared])
    bad_keys = [r.get("span") for r in feed_rows if set(r.keys()) != want_keys]
    check("schema_keys_exact", len(want_keys) == 16 and not bad_keys,
          "target is the feed's %d-field union; %d rows, %d off-schema: %s"
          % (len(want_keys), len(feed_rows), len(bad_keys), bad_keys[:3]))
    res["shared_feed_is_heterogeneous"] = {"ok": None, "detail":
        "DISCLOSED, not a failure: %s" % sorted({len(r) for r in shared})}

    vocab = {f: {json.dumps(r.get(f)) for r in shared} for f in CONTROLLED}
    novel = {f: sorted({json.dumps(r.get(f)) for r in feed_rows} - vocab[f]) for f in CONTROLLED}
    novel = {f: v for f, v in novel.items() if v}
    check("vocabulary_from_shared_feed", not novel, "values not seen in the shared feed: %s" % novel)
    new_concerns = sorted({r["concern_type"] for r in feed_rows} - {str(r.get("concern_type")) for r in shared})
    res["concern_types_new_to_the_feed"] = {"ok": None, "detail": "DISCLOSED, not a failure: %s" % new_concerns}

    books = {r.get("book") for r in feed_rows}
    check("book_is_this_book_and_new_to_the_feed",
          books == {"Ezek"} and "Ezek" not in {r.get("book") for r in shared},
          "rows carry %s; the shared feed's books are %s" % (sorted(books), sorted({r.get("book") for r in shared})))

    feed_grades = {json.dumps(r.get("confidence")) for r in shared}
    off = {r["span"]: r["confidence"] for r in feed_rows if json.dumps(r["confidence"]) not in feed_grades}
    referred = {r["span"] for r in shipped if r["decision_id"] in held_ids}
    check("off_vocabulary_grades_are_referred_rows", set(off) <= referred,
          "grades the shared feed has never carried: %s; all held in the corpus: %s"
          % (off, set(off) <= referred))

    unknown = [r["span"] for r in feed_rows if r["span"] not in by_span]
    mismatch = [r["span"] for r in feed_rows
                if r["span"] in by_span and r["confidence"] != by_span[r["span"]].get("confidence")]
    check("spans_and_grades_are_the_shipped_ones", not unknown and not mismatch,
          "unknown spans %s, grade mismatches %s" % (unknown[:3], mismatch[:3]))

    got = {r["span"] for r in feed_rows}
    check("selection_rule_is_set_equality", got == want,
          "selected %d, rule gives %d, missing %s, extra %s"
          % (len(got), len(want), sorted(want - got)[:3], sorted(got - want)[:3]))

    ids = [r["chunk_decision_id"] for r in feed_rows]
    id_bad = [r["span"] for r in feed_rows
              if r["chunk_decision_id"] != "M8-Ezek-%03d" % (idx_of.get(r["span"]) or 0)]
    check("ids_unique_and_derived_from_the_index", len(set(ids)) == len(ids) and not id_bad,
          "%d ids, %d distinct, %d not derived from chunk_index_in_book" % (len(ids), len(set(ids)), len(id_bad)))

    heb = [r["span"] for r in feed_rows if any(HEB.search(str(r.get(f) or "")) for f in PROSE)]
    quoted = [r["span"] for r in feed_rows
              if any(re.search(r"[\"“]", str(r.get(f) or "")) for f in PROSE)]
    check("no_witness_bytes_quoted", not heb and not quoted,
          "Hebrew in %s, quotation marks in %s" % (heb[:3], quoted[:3]))

    codes = {r["span"]: sorted({m.group(0) for f in PROSE for m in CODE.finditer(str(r.get(f) or ""))})
             for r in feed_rows}
    codes = {k: v for k, v in codes.items() if v}
    check("no_internal_codes_in_prose", not codes, "rows carrying internal codes: %s" % list(codes.items())[:3])

    held_spans = {r["span"] for r in shipped if r["decision_id"] in held_ids}
    held_marked = {r["span"] for r in feed_rows if r.get("candidate_hold_state")}
    deferred = {r["span"] for r in feed_rows if r.get("chunk_review_status") == "final_deferred_review"}
    check("held_rows_are_exactly_the_referred_ones", held_marked == held_spans == deferred,
          "held in the corpus %d, marked held %d, deferred %d, difference %s"
          % (len(held_spans), len(held_marked), len(deferred), sorted(held_marked ^ held_spans)[:3]))

    def unmirrored(r):
        c = by_span.get(r["span"])
        return c is None or (r.get("chunk_review_status"), r.get("candidate_hold_state"),
                             r.get("review_packet_final_state")) != (
            c.get("review_status"), c.get("candidate_hold_state"),
            "accepted_candidate" if c.get("candidate_hold_state") is None else "held_lower_confidence")
    off_corpus = [r["span"] for r in feed_rows if unmirrored(r)]
    check("feed_mirrors_the_corpus_hold", not off_corpus,
          "rows whose review status, hold state or packet state differ from the corpus row: %d %s"
          % (len(off_corpus), off_corpus[:3]))

    leak = [r["span"] for r in feed_rows
            if any(w in json.dumps(r).lower() for w in JUDGED_WORDS)]
    check("no_judgement_merged_into_the_feed", not leak, "rows carrying a judged rating: %s" % leak[:3])

    # Independent derivation check: every fragment of why_low_confidence must occur VERBATIM in the row's own
    # device_notes or strongest_rejected_alternative, unless the sidecar declares composed_not_derived. This is what
    # makes 'derived, never re-written' falsifiable rather than a claim in a README.
    why_by_id = {r["chunk_decision_id"]: r.get("why_low_confidence") or "" for r in feed_rows}
    composed, not_traced, short = [], [], 0
    for d in dims:
        row = by_span.get(d["span"], {})
        src = ((row.get("device_notes") or "") + " " + (row.get("strongest_rejected_alternative") or ""))
        src = re.sub(r"\s+", " ", src)
        if d.get("derivation", {}).get("composed_not_derived"):
            composed.append(d["chunk_decision_id"])
            continue
        txt = why_by_id.get(d["chunk_decision_id"], "").replace("Recorded alternative: ", "")
        for frag in [f.strip().rstrip(".;") for f in re.split(r"(?<=[.;]) ", txt) if f.strip()]:
            if len(frag) < 12:
                short += 1
            elif frag not in src:
                not_traced.append((d["chunk_decision_id"], frag[:60]))
    check("prose_traces_to_the_rows_own_words", not not_traced,
          "%d rows declare composed_not_derived; %d untraceable fragments %s; %d fragments too short to trace"
          % (len(composed), len(not_traced), not_traced[:2], short))

    dim_ids, feed_ids = {d["chunk_decision_id"] for d in dims}, set(ids)
    shape = [d["chunk_decision_id"] for d in dims
             if not (set(("measured", "dependency", "judged")) <= set(d)
                     and d["judged"].get("tier") == "JUDGED_BY_RULE" and d["judged"].get("rule")
                     and d["judged"].get("not_a_measurement"))]
    check("sidecar_pairs_and_separates", dim_ids == feed_ids and not shape,
          "%d sidecar rows, pairing %s, malformed %s" % (len(dims), dim_ids == feed_ids, shape[:3]))

    order = sorted(shipped, key=lambda r: r.get("chunk_index_in_book") or 0)
    nb = {}
    for i, r in enumerate(order):
        nb[r["span"]] = [s for s in (order[i - 1]["span"] if i else None,
                                     order[i + 1]["span"] if i + 1 < len(order) else None) if s]
    frame_n = {}
    for r in shipped:
        frame_n[r.get("parent_collection")] = frame_n.get(r.get("parent_collection"), 0) + 1
    wrong = []
    for d in dims:
        row = by_span.get(d["span"], {})
        a, b = vref(d["span"].partition("-")[0]), vref(d["span"].partition("-")[2])
        zone = 21 in (a[0] if a else 0, b[0] if b else 0) or a in ((20, 44), (22, 1)) or b in ((20, 44), (22, 1))
        if (d["dependency"]["neighbour_spans"] != nb.get(d["span"])
                or d["measured"]["in_numbering_divergence_zone"] != zone
                or d["dependency"]["units_sharing_this_frame"] != frame_n.get(row.get("parent_collection"))
                or d["measured"]["confidence_recorded"] != row.get("confidence")):
            wrong.append(d["chunk_decision_id"])
    check("dependency_facts_re_measured_here", not wrong, "%d sidecar rows disagree with a fresh measurement: %s"
          % (len(wrong), wrong[:3]))

    if Path(rows_path).resolve() == OUT_ROWS.resolve() and GEN.exists():
        p = subprocess.run([sys.executable, str(GEN), "--check"], capture_output=True, text=True, cwd=str(HERE))
        check("generated_deterministically", p.returncode == 0 and "MATCH" in p.stdout,
              (p.stdout.strip().splitlines() or ["no output"])[-1])
    else:
        res["generated_deterministically"] = {"ok": None, "detail": "SKIP: not the canonical pair"}
    return res, failed


def report(rows_path, dims_path):
    res, failed = evaluate(rows_path, dims_path)
    run = sum(1 for v in res.values() if v["ok"] is not None)
    return {"schema": "ezek_atlas_rows_check.v1",
            "rows": Path(rows_path).name, "rows_sha256": hashlib.sha256(Path(rows_path).read_bytes()).hexdigest(),
            "dimensions_sha256": hashlib.sha256(Path(dims_path).read_bytes()).hexdigest(),
            "input_rows_sha256": hashlib.sha256(ROWS_IN.read_bytes()).hexdigest(),
            "row_count": len(jl(rows_path)), "checks_passed": run - len(failed), "checks_run": run,
            "FAILED": failed, "checks": res, "VERDICT": "PASS" if not failed else "FAIL"}, failed


def tamper_hebrew(rows):
    rows[0]["why_low_confidence"] += " א"
    return rows


def tamper_code(rows):
    rows[1]["why_low_confidence"] += " See P03-003."
    return rows


def tamper_span(rows):
    rows[2]["span"] = "Ezek.99.1-Ezek.99.2"
    return rows


def tamper_unhold(rows):
    for r in rows:
        if r.get("candidate_hold_state"):
            r["candidate_hold_state"] = None
            break
    return rows


def tamper_packet_state(rows):
    r = next((x for x in rows if x.get("candidate_hold_state")), rows[0])
    r["review_packet_final_state"] = ("accepted_candidate" if r["review_packet_final_state"] == "held_lower_confidence"
                                      else "held_lower_confidence")
    return rows


def tamper_drop(rows):
    return rows[:-1]


def tamper_judged(rows):
    rows[3]["atlas_hardness"] = "high"
    return rows


def tamper_rewrite(rows):
    rows[4]["why_low_confidence"] = "The unit reads awkwardly to me and I have restated its reason freely here."
    return rows


TAMPERS = [("prose_traces_to_the_rows_own_words", tamper_rewrite), ("no_witness_bytes_quoted", tamper_hebrew), ("no_internal_codes_in_prose", tamper_code),
           ("spans_and_grades_are_the_shipped_ones", tamper_span),
           ("held_rows_are_exactly_the_referred_ones", tamper_unhold),
           ("feed_mirrors_the_corpus_hold", tamper_packet_state),
           ("selection_rule_is_set_equality", tamper_drop), ("no_judgement_merged_into_the_feed", tamper_judged)]


def selftest():
    clean, failed = report(OUT_ROWS, OUT_DIM)
    ok = not failed
    print("clean deliverable: %s (%d/%d)%s" % (clean["VERDICT"], clean["checks_passed"], clean["checks_run"],
                                               "" if ok else "  FAILED=%s" % failed))
    tmp = Path(tempfile.mkdtemp(prefix="atlascheck_"))
    shutil.copy2(OUT_DIM, tmp / OUT_DIM.name)
    base = jl(OUT_ROWS)
    for want, fn in TAMPERS:
        rows = fn(json.loads(json.dumps(base)))
        p = tmp / "tamper.jsonl"
        p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
        _, got = report(p, tmp / OUT_DIM.name)
        hit = want in got
        ok = ok and hit
        print("  %-42s %s  (failed: %s)" % (want, "CAUGHT" if hit else "MISSED", ",".join(got) or "none"))
    shutil.rmtree(tmp, ignore_errors=True)
    print("SELFTEST: %s" % ("PASS - the clean deliverable passes and every tampering is caught" if ok else "FAIL"))
    return ok


def main():
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    out, failed = report(OUT_ROWS, OUT_DIM)
    (HERE / "atlas_rows_check.v1.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n",
                                                   encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("rows", "row_count", "checks_passed", "checks_run", "FAILED", "VERDICT")},
                     indent=1))
    for k, v in out["checks"].items():
        print("  %-44s %s  %s" % (k, {True: "PASS", False: "FAIL", None: "SKIP"}[v["ok"]], v["detail"][:100]))
    sys.exit(0 if not failed else 1)


if __name__ == "__main__":
    main()
