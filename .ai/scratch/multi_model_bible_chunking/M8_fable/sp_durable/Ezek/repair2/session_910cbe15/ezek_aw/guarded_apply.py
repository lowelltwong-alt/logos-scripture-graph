#!/usr/bin/env python3
"""The guarded mutation harness for the Ezekiel author wave. Every row edit in this book goes through here.

WHAT IT GUARANTEES, and each guarantee is a defect this campaign has already paid for somewhere:

  * THE PREIMAGE IS PINNED. The rows file's digest must equal the caller's expected preimage before anything is
    read, and the postimage is measured and reported after. A mutation whose before-state is not pinned cannot
    be reasoned about afterwards.
  * EVERY EDIT NAMES ITS EXPECTED-BEFORE VALUE, exactly. An edit whose current value differs is REFUSED - not
    skipped, not forced - because the difference means the deliverable was written against different bytes.
  * NO EDIT MAY TOUCH A SEAM. span, osis_start, osis_end, decision_id and the writer identity fields are
    PROTECTED: an edit addressing one is refused even if the value is identical. The author wave has no
    authority to move a boundary, and the enforcement lives here rather than in a brief anyone can misread.
  * EXECUTED/ORDERED PARITY (E-18). The receipt carries both counts and they must be equal. A sweep that
    ordered 40 edits and executed 39 is a failure, and a harness that reports only "39 applied" hides it.
  * ATOMIC REPLACE with a read-back. The file is written to a temp path, re-parsed, counted, and only then
    replaced; then its digest is measured again from disk.
  * DRY RUN IS THE DEFAULT. Nothing mutates unless the caller passes apply=True. A harness whose default is to
    write is a harness that writes by accident.

WHAT IT DELIBERATELY DOES NOT DO. It does not judge content. It will happily install a sentence that is wrong,
because catching that is the spot wave's job and a tool that tried would encode a judgement it cannot audit.
"""
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"

# Fields no author-wave edit may address, for any reason.
PROTECTED = {"span", "osis_start", "osis_end", "decision_id", "book", "model_id", "chunk_index_in_book",
             "writer_part", "writer_decision_id", "writer_attempt_id", "parent_collection"}
CONFIDENCE_SCALE = {"high", "medium", "medium_low", "low"}


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    return sha_bytes(Path(p).read_bytes())


def load_rows(path=ROWS):
    return [json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]


def dump_rows(rows):
    """One JSON object per line, UTF-8, LF, key order preserved. The serialisation is fixed here so that an
    unrelated formatting difference can never masquerade as a content change in a digest comparison."""
    return "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows).encode("utf-8")


class Refused(Exception):
    pass


def apply_edits(edits, preimage_sha, sweep, ordered_count=None, apply=False, path=ROWS):
    """Apply a list of edits under the guard. Returns a receipt dict.

    An edit is {row_id, field, op, expected_before, value}:
      op "set"            - replace a string field; expected_before is the exact current value
      op "append_ref"      - append ONE entry to boundary_evidence_refs; expected_before is the current LIST
      op "set_confidence"  - like set, but the value must be on the four-value scale

    `ordered_count` is what the CALLER believes it ordered. If it disagrees with len(edits) the sweep is refused
    before anything is read - that disagreement is E-18's parity failure at its earliest detectable point.
    """
    p = Path(path)
    measured_pre = sha_file(p)
    if measured_pre != preimage_sha:
        raise Refused("preimage is %s, caller pinned %s. The deliverable was written against different bytes."
                      % (measured_pre, preimage_sha))
    if ordered_count is not None and ordered_count != len(edits):
        raise Refused("E-18 parity: caller ordered %d edits and handed me %d." % (ordered_count, len(edits)))

    rows = load_rows(p)
    by_id = {}
    for i, r in enumerate(rows):
        rid = r.get("decision_id")
        if rid in by_id:
            raise Refused("duplicate decision_id %r - the file is not addressable by row id" % rid)
        by_id[rid] = i

    # ---- validate EVERY edit before applying ANY of them
    problems = []
    for n, e in enumerate(edits):
        rid, field, op = e.get("row_id"), e.get("field"), e.get("op")
        if field in PROTECTED:
            problems.append((n, rid, field, "PROTECTED field - the author wave may not move a seam or an "
                                            "identity, and this is refused even when the value is unchanged"))
            continue
        if rid not in by_id:
            problems.append((n, rid, field, "no such row"))
            continue
        cur = rows[by_id[rid]].get(field)
        if op in ("set", "set_confidence"):
            if cur != e.get("expected_before"):
                problems.append((n, rid, field, "expected_before does not match the current value "
                                                "(current %r chars, expected %r chars)"
                                 % (len(str(cur)), len(str(e.get("expected_before"))))))
            if op == "set_confidence" and str(e.get("value")).lower() not in CONFIDENCE_SCALE:
                problems.append((n, rid, field, "%r is not on the four-value confidence scale"
                                 % e.get("value")))
        elif op == "append_ref":
            if field != "boundary_evidence_refs":
                problems.append((n, rid, field, "append_ref addresses boundary_evidence_refs only"))
            elif cur != e.get("expected_before"):
                problems.append((n, rid, field, "the refs list has changed since the deliverable was written "
                                                "(current %d entries, expected %d)"
                                 % (len(cur or []), len(e.get("expected_before") or []))))
            elif not isinstance(e.get("value"), str) or not e.get("value").strip():
                problems.append((n, rid, field, "append_ref takes one non-empty string entry"))
        else:
            problems.append((n, rid, field, "unknown op %r" % op))
    if problems:
        raise Refused("%d of %d edits failed validation; NOTHING was applied:\n%s"
                      % (len(problems), len(edits),
                         "\n".join("  [%d] %s.%s  %s" % pr for pr in problems[:20])))

    # ---- apply to an in-memory copy
    working = json.loads(json.dumps(rows))          # deep copy; the original stays for the diff count
    executed = 0
    touched_rows, touched_fields = set(), set()
    for e in edits:
        i = by_id[e["row_id"]]
        if e["op"] in ("set", "set_confidence"):
            working[i][e["field"]] = (str(e["value"]).lower() if e["op"] == "set_confidence" else e["value"])
        else:
            working[i][e["field"]] = list(working[i][e["field"]]) + [e["value"]]
        executed += 1
        touched_rows.add(e["row_id"])
        touched_fields.add(e["field"])

    # ---- independent verification: count fields that ACTUALLY differ, rather than trusting the loop
    diffs = 0
    for a, b in zip(rows, working):
        for k in set(a) | set(b):
            if a.get(k) != b.get(k):
                diffs += 1
    if executed != len(edits):
        raise Refused("E-18 parity: executed %d of %d ordered" % (executed, len(edits)))
    # one edit per (row, field) is the normal case; several appends to one refs list collapse to one field diff
    expected_field_diffs = len({(e["row_id"], e["field"]) for e in edits})
    if diffs != expected_field_diffs:
        raise Refused("the measured field-level difference is %d where %d distinct (row, field) pairs were "
                      "edited - an edit changed something it did not address, or changed nothing"
                      % (diffs, expected_field_diffs))
    # no protected field may differ, measured rather than assumed
    for a, b in zip(rows, working):
        for k in PROTECTED:
            if a.get(k) != b.get(k):
                raise Refused("a PROTECTED field changed: %s.%s" % (a.get("decision_id"), k))
    if len(working) != len(rows):
        raise Refused("row count changed: %d -> %d" % (len(rows), len(working)))

    out = dump_rows(working)
    receipt = {
        "sweep": sweep,
        "applied": bool(apply),
        "preimage_sha256": measured_pre,
        "postimage_sha256_computed": sha_bytes(out),
        "ordered": len(edits), "executed": executed,
        "executed_equals_ordered": executed == len(edits),
        "e18_parity_digits": "%d/%d" % (executed, len(edits)),
        "rows_in": len(rows), "rows_out": len(working),
        "rows_touched": len(touched_rows), "fields_touched": sorted(touched_fields),
        "measured_field_level_differences": diffs,
        "protected_fields_unchanged": True,
        "at": datetime.now(timezone.utc).isoformat(),
    }
    if not apply:
        receipt["note"] = ("DRY RUN. Nothing was written. The postimage digest above is what a real apply "
                           "would produce, so the caller can pin it in advance.")
        return receipt

    tmp = p.with_suffix(p.suffix + ".tmpGA")
    tmp.write_bytes(out)
    # read-back BEFORE replacing: re-parse and re-count from the temp file, not from memory
    back = load_rows(tmp)
    if len(back) != len(working) or json.dumps(back, sort_keys=True) != json.dumps(working, sort_keys=True):
        tmp.unlink()
        raise Refused("the written file does not re-parse to what was intended; nothing replaced")
    backup = p.with_suffix(p.suffix + ".pre_" + measured_pre[:12])
    if not backup.exists():
        shutil.copy2(p, backup)
    tmp.replace(p)
    receipt["postimage_sha256_measured_from_disk"] = sha_file(p)
    receipt["postimage_matches_computed"] = (receipt["postimage_sha256_measured_from_disk"]
                                             == receipt["postimage_sha256_computed"])
    receipt["preimage_backup"] = backup.name
    if not receipt["postimage_matches_computed"]:
        raise Refused("the file on disk does not match what was written")
    return receipt


# ------------------------------------------------------------------ simulating a whole PLAN before touching disk
def simulate_plan(sweeps, preimage_sha, path=ROWS):
    """Validate an ordered list of sweeps against each other WITHOUT writing anything.

    WHY THIS EXISTS. The sweeps run in the ruling's order, and an edit in a later sweep may legitimately expect
    the state an earlier sweep produced. Lane 01 reported exactly that: one row needs an A4 append (step 4) and
    an A6 repair (step 5) on the SAME refs list, so the A6 edit's expected_before is the original list PLUS the
    A4 entry. Validating each sweep against the pristine file would refuse it; validating the plan in order
    accepts it and would still catch a genuine mismatch.

    So the whole plan is replayed in memory first. Nothing reaches disk until every sweep validates in sequence,
    which means an ordering error costs a report rather than a half-applied corpus.

    `sweeps` is [(name, edits), ...] in execution order. Returns a per-sweep report plus the digest the plan
    would end at, so the caller can pin the postimage in advance.
    """
    p = Path(path)
    measured = sha_file(p)
    if measured != preimage_sha:
        raise Refused("preimage is %s, caller pinned %s" % (measured, preimage_sha))
    rows = load_rows(p)
    report = []
    for name, edits in sweeps:
        by_id = {r.get("decision_id"): i for i, r in enumerate(rows)}
        problems = []
        for n, e in enumerate(edits):
            rid, field, op = e.get("row_id"), e.get("field"), e.get("op")
            if field in PROTECTED:
                problems.append((n, rid, field, "PROTECTED field"))
                continue
            if rid not in by_id:
                problems.append((n, rid, field, "no such row"))
                continue
            cur = rows[by_id[rid]].get(field)
            if op in ("set", "set_confidence"):
                if cur != e.get("expected_before"):
                    problems.append((n, rid, field, "expected_before mismatch"))
                elif op == "set_confidence" and str(e.get("value")).lower() not in CONFIDENCE_SCALE:
                    problems.append((n, rid, field, "off-scale confidence %r" % e.get("value")))
            elif op == "append_ref":
                if cur != e.get("expected_before"):
                    problems.append((n, rid, field, "refs list mismatch (%d entries now, %d expected)"
                                     % (len(cur or []), len(e.get("expected_before") or []))))
            else:
                problems.append((n, rid, field, "unknown op %r" % op))
        if problems:
            report.append({"sweep": name, "ordered": len(edits), "validated": False,
                           "problems": [{"index": a, "row": b, "field": c, "why": d} for a, b, c, d in
                                        problems[:25]],
                           "problem_count": len(problems)})
            return {"ok": False, "sweeps": report,
                    "stopped_at": name,
                    "note": "the plan was NOT applied; simulation stops at the first sweep that fails so the "
                            "report describes one cause rather than a cascade"}
        # apply in memory, so the next sweep validates against this state
        for e in edits:
            i = by_id[e["row_id"]]
            if e["op"] in ("set", "set_confidence"):
                rows[i][e["field"]] = (str(e["value"]).lower() if e["op"] == "set_confidence" else e["value"])
            else:
                rows[i][e["field"]] = list(rows[i][e["field"]]) + [e["value"]]
        report.append({"sweep": name, "ordered": len(edits), "validated": True, "executed": len(edits),
                       "e18_parity_digits": "%d/%d" % (len(edits), len(edits)),
                       "rows_touched": len({e["row_id"] for e in edits}),
                       "fields_touched": sorted({e["field"] for e in edits}),
                       "digest_after_this_sweep": sha_bytes(dump_rows(rows))})
    return {"ok": True, "sweeps": report, "final_digest_if_applied": sha_bytes(dump_rows(rows)),
            "rows_out": len(rows),
            "note": "SIMULATION ONLY - nothing was written. Every sweep validated against the state its "
                    "predecessors would produce, so a later sweep may legitimately expect an earlier one's "
                    "output."}


# ------------------------------------------------------------------ selftest, on synthetic rows only
def _selftest():
    import tempfile
    cases = []
    base = [{"decision_id": "T-001", "span": "Ezek.1.1-Ezek.1.5", "confidence": "high",
             "boundary_rationale": "original text", "boundary_evidence_refs": ["web:Ezek.1.1"]},
            {"decision_id": "T-002", "span": "Ezek.2.1-Ezek.2.3", "confidence": "low",
             "boundary_rationale": "second row", "boundary_evidence_refs": []}]
    d = Path(tempfile.mkdtemp())
    f = d / "t.jsonl"
    f.write_bytes(dump_rows(base))
    pin = sha_file(f)

    def run(edits, **kw):
        try:
            return apply_edits(edits, kw.pop("pin", pin), "selftest", path=f, **kw), None
        except Refused as ex:
            return None, str(ex)

    r, err = run([{"row_id": "T-001", "field": "boundary_rationale", "op": "set",
                   "expected_before": "original text", "value": "repaired text"}])
    cases.append(("a well-formed dry run validates and reports its postimage", r is not None and not r["applied"]
                  and r["e18_parity_digits"] == "1/1"))
    cases.append(("a dry run writes NOTHING", sha_file(f) == pin))

    r, err = run([{"row_id": "T-001", "field": "span", "op": "set",
                   "expected_before": "Ezek.1.1-Ezek.1.5", "value": "Ezek.1.1-Ezek.1.6"}])
    cases.append(("an edit addressing span is REFUSED (no seam moves)", r is None and "PROTECTED" in err))

    r, err = run([{"row_id": "T-001", "field": "span", "op": "set",
                   "expected_before": "Ezek.1.1-Ezek.1.5", "value": "Ezek.1.1-Ezek.1.5"}])
    cases.append(("an edit addressing span is refused even when the value is UNCHANGED",
                  r is None and "PROTECTED" in err))

    r, err = run([{"row_id": "T-001", "field": "boundary_rationale", "op": "set",
                   "expected_before": "text that is not there", "value": "x"}])
    cases.append(("a stale expected_before is REFUSED", r is None and "expected_before" in err))

    r, err = run([{"row_id": "T-001", "field": "boundary_rationale", "op": "set",
                   "expected_before": "original text", "value": "a"},
                  {"row_id": "T-999", "field": "boundary_rationale", "op": "set",
                   "expected_before": "x", "value": "b"}])
    cases.append(("one bad edit refuses the WHOLE batch, so a sweep is all-or-nothing",
                  r is None and "NOTHING was applied" in err))

    r, err = run([{"row_id": "T-001", "field": "confidence", "op": "set_confidence",
                   "expected_before": "high", "value": "medium_high"}])
    cases.append(("a confidence value off the four-value scale is REFUSED",
                  r is None and "four-value confidence scale" in err))

    r, err = run([{"row_id": "T-001", "field": "boundary_rationale", "op": "set",
                   "expected_before": "original text", "value": "x"}], ordered_count=5)
    cases.append(("an ordered/handed count mismatch is refused before anything is read (E-18)",
                  r is None and "parity" in err))

    r, err = run([{"row_id": "T-001", "field": "boundary_rationale", "op": "set",
                   "expected_before": "original text", "value": "x"}], pin="0" * 64)
    cases.append(("a wrong pinned preimage is refused", r is None and "preimage is" in err))

    r, err = run([{"row_id": "T-002", "field": "boundary_evidence_refs", "op": "append_ref",
                   "expected_before": [], "value": "web:Ezek.2.1-Ezek.2.3 [WARRANT-onset] onset span"}])
    cases.append(("a refs append to an empty list validates", r is not None and r["e18_parity_digits"] == "1/1"))

    r, err = run([{"row_id": "T-002", "field": "boundary_evidence_refs", "op": "append_ref",
                   "expected_before": ["something else"], "value": "x"}])
    cases.append(("a refs append whose list has moved is refused", r is None and "refs list has changed" in err))

    # a real apply, then the postimage read-back
    r, err = run([{"row_id": "T-001", "field": "boundary_rationale", "op": "set",
                   "expected_before": "original text", "value": "repaired text"},
                  {"row_id": "T-001", "field": "confidence", "op": "set_confidence",
                   "expected_before": "high", "value": "medium"}], apply=True)
    cases.append(("a real apply reports a postimage MEASURED FROM DISK that matches what it computed",
                  r is not None and r.get("postimage_matches_computed") is True))
    after = load_rows(f)
    cases.append(("and the bytes on disk carry the edit", after[0]["boundary_rationale"] == "repaired text"
                  and after[0]["confidence"] == "medium"))
    cases.append(("and the span is untouched", after[0]["span"] == "Ezek.1.1-Ezek.1.5"))
    cases.append(("and the preimage was preserved as a backup",
                  any(x.name.startswith("t.jsonl.pre_") for x in d.iterdir())))
    r2, err2 = run([{"row_id": "T-001", "field": "boundary_rationale", "op": "set",
                     "expected_before": "original text", "value": "again"}])
    cases.append(("re-applying the same deliverable after a successful apply is REFUSED (not idempotent by "
                  "accident)", r2 is None))

    w = max(len(n) for n, _ in cases)
    for n, ok in cases:
        print("  %s  %s" % ("PASS" if ok else "FAIL", n.ljust(w)))
    bad = [n for n, ok in cases if not ok]
    print("\nguarded_apply selftest: %d/%d passed" % (len(cases) - len(bad), len(cases)))
    shutil.rmtree(d, ignore_errors=True)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(_selftest())
