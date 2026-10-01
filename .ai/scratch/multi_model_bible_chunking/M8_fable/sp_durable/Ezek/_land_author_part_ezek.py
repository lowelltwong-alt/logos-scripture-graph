#!/usr/bin/env python3
"""Land one Ezekiel author-wave deliverable. It is written OUTSIDE the worktree (OW-11) and landed here with parity. The
steps: form check against its orders file, receipt, layer-C note, capture index.

This tool never edits a deliverable and never judges content. It proves FORM against the orders the controlling agent's
rulings produced:
  - every line is a JSON object with _op in replace | new_row | retire;
  - an emitted row has exactly the 22 fields plus _op, a legal unit_type and confidence, book Ezek, model_id M8_fable,
    non_authorizing true, a full span form, and writer_part = the part;
  - replace: the row is in the part, with decision_id, writer_decision_id, writer_attempt_id and chunk_index_in_book
    unchanged, and its span equals the ruled target_span (or the current span when none is ruled);
  - new_row: a provisional id from the orders, with span = target_span, chunk_index_in_book 0, and writer_attempt_id = the
    author's attempt id;
  - retire: exactly the retire list;
  - coverage: every ordered row carrying anything but `hold` is emitted or retired, and nothing unordered is emitted;
  - local tiling: the part, with the output applied, covers the part's verses exactly;
  - E-01: the normalizer dry-run over the landed rows reports 0 defects and 0 fixed.
A form defect lands as LANDED_WITH_FORM_DEFECTS with every defect named; the apply step refuses such a file.

FIXUP-1 mode (ezek_controlling_rulings_a1#e4 ruling FIXUP-1), when --orders names an m8_fixup_orders.v1 file: the deliverable
lands beside its orders under the orders' attempt id, its receipt goes to ezek_author_fixup_attempt_receipts.jsonl there
(lane ezek_author_fixup), any _op but replace is a defect, and a replace that changes span, unit_type, confidence or
parent_collection is a defect (FIXUP-1 (3)). --brief is required in this mode.

Usage: _land_author_part_ezek.py --part pNN --src <OUT file> --record <agent OW-8 final message .json>
       --tokens N --tool-uses N [--ordinal N]
       [--orders fixup1/orders_ezek_author_fixup_pNN_a1.json --brief <brief file under SP/Ezek> --model <ordered model>]
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EZ = Path(__file__).resolve().parent
SP = EZ.parent
CAMPAIGN = SP / "campaign"
AUTHOR = EZ / "author"
RECEIPTS = AUTHOR / "ezek_author_attempt_receipts.jsonl"
NOTES = EZ / "evidence_notes"
sys.path.insert(0, str(EZ / "tools"))
from ezek_lib import LAST_VERSE  # noqa: E402

FIELDS = ["decision_id", "book", "model_id", "chunk_index_in_book", "span", "boundary_rationale", "boundary_evidence_refs",
          "strongest_rejected_alternative", "literature_type_guess", "confidence", "strong_or_hebrew_tags_used",
          "wj_or_red_letter_considered", "frontier_flag_considered", "non_authorizing", "review_status", "parent_collection",
          "unit_type", "writer_part", "writer_decision_id", "writer_attempt_id", "observed_substrate_signals", "device_notes"]
UNIT_TYPES = {"vision_report", "commission_narrative", "sign_act", "judgment_oracle", "oracle_against_nation", "lament_qinah",
              "parable_allegory", "disputation_oracle", "salvation_oracle", "temple_measurement", "temple_law", "land_allotment"}
CONFIDENCE = {"high", "medium", "medium_low", "low"}
SPAN = re.compile(r"^Ezek\.(\d+)\.(\d+)-Ezek\.(\d+)\.(\d+)$")
FIXUP1_ORDERED_BY = "ezek_controlling_rulings_a1#e4 ruling FIXUP-1"
AGENT_LABEL = "%s author %s"
PRODUCER = "%s execution of the controlling agent's fix-up orders (%s)"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def verses(span):
    c1, v1, c2, v2 = map(int, SPAN.match(span).groups())
    out, c, v = [], c1, v1
    while (c, v) <= (c2, v2) and c in LAST_VERSE:
        out.append((c, v))
        c, v = (c, v + 1) if v < LAST_VERSE[c] else (c + 1, 1)
    return out


def resolve_ordinal(aid, record_xid, arg_ordinal):
    """(ordinal, None) or (None, reason). OW-11-k (2026-09-11): a defaulted --ordinal landed a deliverable under the wrong
    execution. The ordinal comes from the agent record's execution_id when --ordinal is omitted; disagreement, a foreign
    attempt, a malformed id, or absence of both sources is refused before anything is landed."""
    m = re.fullmatch(r"(.+)#e(\d+)", str(record_xid)) if record_xid else None
    if record_xid and (not m or m.group(1) != aid):
        return None, "the agent record names execution %r, which is not an execution of %s" % (record_xid, aid)
    rec_ord = int(m.group(2)) if m else None
    if arg_ordinal is None and rec_ord is None:
        return None, "no --ordinal given and the agent record names no execution_id; an explicit ordinal is required"
    if arg_ordinal is not None and rec_ord is not None and arg_ordinal != rec_ord:
        return None, "--ordinal %d disagrees with the agent record's execution %s; nothing landed" % (arg_ordinal, record_xid)
    return (arg_ordinal if arg_ordinal is not None else rec_ord), None


def wave_labels(orders):
    """(wave, ordered_by) for a fix-up orders file, from the file's own fields; the FIXUP-1 strings are the defaults when the
    fields are absent (ezek_controlling_rulings_a1#e9 ruling S2-ROUTING (5))."""
    return orders.get("wave") or "FIXUP-1", orders.get("ordered_by") or FIXUP1_ORDERED_BY


def selftest():
    aid = "ezek_author_fixup_p01_a1"
    vectors = [
        ("the ordinal is derived from the record when --ordinal is omitted", (aid, aid + "#e2", None), 2),
        ("an explicit ordinal agreeing with the record", (aid, aid + "#e2", 2), 2),
        ("REGRESSION OW-11-k: ordinal 1 against a #e2 record is refused", (aid, aid + "#e2", 1), None),
        ("no ordinal and no execution id in the record is refused", (aid, None, None), None),
        ("an explicit ordinal with a record that names no execution id", (aid, None, 1), 1),
        ("a record naming another attempt's execution is refused", (aid, "ezek_author_p01_a1#e1", None), None),
        ("a malformed execution id is refused", (aid, aid + "-e2", None), None),
    ]
    results = []
    for name, args, want in vectors:
        got, _why = resolve_ordinal(*args)
        results.append({"vector": name, "want": want, "got": got, "ok": got == want})
    # ezek_controlling_rulings_a1#e9 ruling S2-ROUTING (5): wave and ruling labels, both ways
    s2r = "ezek_controlling_rulings_a1#e9 ruling S2-ROUTING"
    for name, orders, want in [
            ("FIXUP-1 orders (no wave field) keep the FIXUP-1 labels", {"ordered_by": FIXUP1_ORDERED_BY}, ("FIXUP-1", FIXUP1_ORDERED_BY)),
            ("orders with neither field default to the FIXUP-1 labels", {}, ("FIXUP-1", FIXUP1_ORDERED_BY)),
            ("FIXUP-2 orders resolve their own wave and ruling", {"wave": "FIXUP-2", "ordered_by": s2r}, ("FIXUP-2", s2r))]:
        got = wave_labels(orders)
        results.append({"vector": name, "want": list(want), "got": list(got), "ok": got == want})
    w1, ob1 = wave_labels({"ordered_by": FIXUP1_ORDERED_BY})
    w2, ob2 = wave_labels({"wave": "FIXUP-2", "ordered_by": s2r})
    for name, got, want in [
            ("the FIXUP-1 agent label equals the old literal", AGENT_LABEL % (w1, "p06"), "FIXUP-1 author p06"),
            ("the FIXUP-1 producer equals the old literal", PRODUCER % (w1, ob1),
             "FIXUP-1 execution of the controlling agent's fix-up orders (ezek_controlling_rulings_a1#e4 ruling FIXUP-1)"),
            ("the FIXUP-2 agent label names FIXUP-2", AGENT_LABEL % (w2, "p08"), "FIXUP-2 author p08"),
            ("the FIXUP-2 producer names #e9", PRODUCER % (w2, ob2),
             "FIXUP-2 execution of the controlling agent's fix-up orders (ezek_controlling_rulings_a1#e9 ruling S2-ROUTING)")]:
        results.append({"vector": name, "want": want, "got": got, "ok": got == want})
    failed = [r for r in results if not r["ok"]]
    print(json.dumps({"selftest": "resolve_ordinal", "vectors": len(results), "failed": failed,
                      "verdict": "GREEN" if not failed else "RED"}, indent=1))
    return 1 if failed else 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", required=True)
    ap.add_argument("--src", required=True)
    ap.add_argument("--record", required=True)
    ap.add_argument("--tokens", type=int, required=True)
    ap.add_argument("--tool-uses", type=int, required=True)
    ap.add_argument("--ordinal", type=int, default=None,
                    help="derived from the agent record's execution_id when omitted; refused when it disagrees (OW-11-k)")
    ap.add_argument("--orders", help="an m8_fixup_orders.v1 file (FIXUP-1 mode); the author-wave orders path when omitted")
    ap.add_argument("--brief", help="the brief file under SP/Ezek the execution ran under; required in FIXUP-1 mode")
    ap.add_argument("--model", default="claude-sonnet-5", help="the model ORDERED at launch, as recorded")
    a = ap.parse_args()
    if a.orders:
        orders_p = Path(a.orders) if Path(a.orders).is_absolute() else EZ / a.orders
    else:
        orders_p = AUTHOR / ("orders_ezek_author_%s_a1.json" % a.part)
    orders = json.loads(orders_p.read_text(encoding="utf-8"))
    aid = orders["attempt_id"]
    fixup = orders.get("schema") == "m8_fixup_orders.v1"
    wave, ordered_by = wave_labels(orders)
    if fixup and (orders.get("part") != a.part or not a.brief):
        raise SystemExit("ABORT: %s orders for %s landed as %s, or no --brief given" % (wave, orders.get("part"), a.part))
    base_dir = orders_p.parent if fixup else AUTHOR
    receipts_p = (orders_p.parent / "ezek_author_fixup_attempt_receipts.jsonl") if fixup else RECEIPTS
    brief_p = (EZ / a.brief) if a.brief else EZ / "AUTHOR_BRIEF.md"
    rec = json.loads(Path(a.record).read_text(encoding="utf-8"))
    ordinal, why = resolve_ordinal(aid, rec.get("execution_id"), a.ordinal)
    if ordinal is None:
        print(json.dumps({"part": a.part, "verdict": "REFUSED", "why": why, "actions": []}, ensure_ascii=False, indent=1))
        return 1
    a.ordinal = ordinal
    xid = "%s#e%d" % (aid, a.ordinal)
    suffix = "" if a.ordinal == 1 else "_e%d" % a.ordinal
    dest = base_dir / (("%s%s.jsonl" % (aid, suffix)) if fixup else ("ezek_author_%s_a1%s.jsonl" % (a.part, suffix)))
    out = {"part": a.part, "execution_id": xid, "actions": [], "form_defects": []}
    defects = out["form_defects"]

    src = Path(a.src)
    if not src.is_file():
        out.update(verdict="NOT_LANDED")
        defects.append("source deliverable absent: %s" % src)
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 1
    if dest.is_file():
        if sha(dest) != sha(src):
            out.update(verdict="REFUSED")
            defects.append("%s already exists with DIFFERENT bytes; a landed deliverable is never replaced" % dest.name)
            print(json.dumps(out, ensure_ascii=False, indent=1))
            return 1
        out["actions"].append("already landed with identical bytes - no-op")
    else:
        shutil.copyfile(src, dest)
        assert sha(dest) == sha(src), "persist parity failure"
        out["actions"].append("landed from outside the worktree, parity verified")

    rows_p = SP / orders["sources"]["rows"]["path"]
    if sha(rows_p) != orders["sources"]["rows"]["sha256"]:
        defects.append("the rows file the orders were built on has changed since (%s)" % orders["sources"]["rows"]["path"])
    chain = [json.loads(l) for l in rows_p.read_text(encoding="utf-8").splitlines() if l.strip()]
    part_rows = {r["decision_id"]: r for r in chain if r["writer_part"] == a.part}
    entries = {e["decision_id"]: e for e in orders["rows_with_orders"]}
    target = {}
    for e in orders["rows_with_orders"]:
        for it in e["items"]:
            if it.get("op") == "replace" and it.get("target_span"):
                target[e["decision_id"]] = it["target_span"]
    new_ids = {n["provisional_decision_id"]: n for n in orders["new_rows"]}
    retire_ids = {x["decision_id"] for x in orders["retire"]}

    emitted, seen = [], {}
    for i, line in enumerate(dest.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            defects.append("line %d is not JSON: %s" % (i, exc))
            continue
        if not isinstance(obj, dict) or obj.get("_op") not in (("replace",) if fixup else ("replace", "new_row", "retire")):
            defects.append("line %d: _op missing or not %s" % (i, "replace (FIXUP-1 (3): no new or retired rows)" if fixup
                                                              else "replace|new_row|retire"))
            continue
        did = obj.get("decision_id")
        if did in seen:
            defects.append("line %d: %s emitted twice" % (i, did))
        seen[did] = obj["_op"]
        if obj["_op"] == "retire":
            if did not in retire_ids:
                defects.append("line %d: retire of %s, which the orders do not retire" % (i, did))
            continue
        keys = set(obj) - {"_op"}
        if keys != set(FIELDS):
            defects.append("line %d (%s): fields differ from the 22 (missing %s; extra %s)"
                           % (i, did, sorted(set(FIELDS) - keys), sorted(keys - set(FIELDS))))
        if obj.get("unit_type") not in UNIT_TYPES:
            defects.append("%s: unit_type %r not in the 12" % (did, obj.get("unit_type")))
        if obj.get("confidence") not in CONFIDENCE:
            defects.append("%s: confidence %r not allowed" % (did, obj.get("confidence")))
        if obj.get("book") != "Ezek" or obj.get("model_id") != "M8_fable" or obj.get("non_authorizing") is not True:
            defects.append("%s: book/model_id/non_authorizing not Ezek/M8_fable/true" % did)
        if obj.get("writer_part") != a.part:
            defects.append("%s: writer_part %r is not %s" % (did, obj.get("writer_part"), a.part))
        if not isinstance(obj.get("span"), str) or not SPAN.match(obj["span"]):
            defects.append("%s: span %r not in full form" % (did, obj.get("span")))
            continue
        for f in ("boundary_evidence_refs", "strong_or_hebrew_tags_used", "observed_substrate_signals"):
            if not (isinstance(obj.get(f), list) and all(isinstance(x, str) for x in obj[f])):
                defects.append("%s: %s is not a list of strings" % (did, f))
        for f in ("boundary_rationale", "strongest_rejected_alternative", "literature_type_guess", "device_notes"):
            if not isinstance(obj.get(f), str):
                defects.append("%s: %s is not one string" % (did, f))
        if re.search(r"\{[a-z_]+\}", json.dumps(obj, ensure_ascii=False)):
            defects.append("%s: an unexpanded {placeholder} remains" % did)
        if obj["_op"] == "replace":
            cur = part_rows.get(did)
            if cur is None:
                defects.append("%s: replace of a row not in %s" % (did, a.part))
                continue
            for f in ("writer_decision_id", "writer_attempt_id", "chunk_index_in_book") + (("unit_type", "confidence", "parent_collection") if fixup else ()):
                if obj.get(f) != cur.get(f):
                    defects.append("%s: %s changed (%r -> %r)" % (did, f, cur.get(f), obj.get(f)))
            want = target.get(did, cur["span"])
            if obj["span"] != want:
                defects.append("%s: span %s, ruled %s" % (did, obj["span"], want))
        else:
            n = new_ids.get(did)
            if n is None:
                defects.append("%s: new_row id is not a provisional id in the orders" % did)
                continue
            if obj["span"] != n["target_span"]:
                defects.append("%s: new row span %s, ruled %s" % (did, obj["span"], n["target_span"]))
            if obj.get("chunk_index_in_book") != 0 or obj.get("writer_attempt_id") != aid:
                defects.append("%s: a new row needs chunk_index_in_book 0 and writer_attempt_id %s" % (did, aid))
            if obj.get("writer_decision_id") != n["provisional_writer_decision_id"]:
                defects.append("%s: writer_decision_id %r, provisional %r" % (did, obj.get("writer_decision_id"),
                                                                              n["provisional_writer_decision_id"]))
        emitted.append(obj)

    must = {d for d, e in entries.items() if set(e["ops"]) - {"hold"}} | set(new_ids)
    missing = sorted(must - set(seen))
    if missing:
        defects.append("ordered but not emitted: %s" % ", ".join(missing))
    unordered = sorted(set(seen) - set(entries) - set(new_ids))
    if unordered:
        defects.append("emitted without an order: %s" % ", ".join(unordered))

    # local tiling: the part with this output applied covers exactly the part's verses
    applied = dict(part_rows)
    for obj in emitted:
        applied[obj["decision_id"]] = obj
    for d, op in seen.items():
        if op == "retire":
            applied.pop(d, None)
    want_v = sorted(v for r in part_rows.values() for v in verses(r["span"]))
    got_v = sorted(v for r in applied.values() if SPAN.match(r.get("span", "")) for v in verses(r["span"]))
    tiling = "PASS" if got_v == want_v else "FAIL"
    if tiling == "FAIL":
        dup = sorted({v for v in got_v if got_v.count(v) > 1})[:5]
        gap = sorted(set(want_v) - set(got_v))[:5]
        defects.append("local tiling FAIL (overlap e.g. %s; gap e.g. %s)" % (dup, gap))

    # E-01 over the landed rows (dry run; the normalizer writes nothing without --write). The copy it reads lives in a
    # system temporary directory, never under SP (ruling R7's control).
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / ("normcheck_%s.json" % a.part)
        tmp.write_text(json.dumps([{k: v for k, v in o.items() if k != "_op"} for o in emitted], ensure_ascii=False),
                       encoding="utf-8")
        proc = subprocess.run([sys.executable, str(EZ / "tools" / "normalize_hebrew_in_json.py"), str(tmp)],
                              capture_output=True, text=True, encoding="utf-8", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
        try:
            norm = json.loads(proc.stdout.strip().splitlines()[-1])
        except (IndexError, json.JSONDecodeError):
            norm = {}
            defects.append("E-01: the normalizer returned no report (exit %s): %s" % (proc.returncode, proc.stderr[-300:]))
    if norm.get("defect_count", 1) or norm.get("fixed", 1):
        defects.append("E-01: normalizer over the landed rows reports defects=%s fixed=%s" % (norm.get("defect_count"), norm.get("fixed")))

    status = "LANDED" if not defects else "LANDED_WITH_FORM_DEFECTS"
    # the agent record was read, and its execution id resolved against the landing, before anything landed (OW-11-k)
    summary = {"lines": len(seen), "replaced": sum(1 for o in seen.values() if o == "replace"),
               "new_rows": sum(1 for o in seen.values() if o == "new_row"), "retired": sum(1 for o in seen.values() if o == "retire"),
               "ordered_rows": len(must), "local_tiling": tiling,
               "normalizer": {k: norm.get(k) for k in ("ok", "qere", "fixed", "defect_count")}}
    out["summary"] = summary

    existing = set()
    if receipts_p.is_file():
        existing = {json.loads(l).get("execution_id") for l in receipts_p.read_text(encoding="utf-8").splitlines() if l.strip()}
    if xid in existing:
        out["actions"].append("receipt for %s already present - not appended twice" % xid)
    else:
        receipt = {
            "schema": "m8_attempt_receipt.v1", "lane": "ezek_author_fixup" if fixup else "ezek_author_wave", "book": "Ezek",
            "attempt_id": aid, "execution_id": xid, "execution_of": aid, "execution_ordinal": a.ordinal,
            "previous_execution_id": ("%s#e%d" % (aid, a.ordinal - 1)) if a.ordinal > 1 else None, "retry_of": None,
            "agent": (AGENT_LABEL % (wave, a.part)) if fixup else ("author %s" % a.part), "parent_agent_id": "orchestrator", "model": a.model,
            "model_actual": "UNAVAILABLE - the runtime exposed no effective-model record; never inferred",
            "effort": "ORDERED session default, NOT VERIFIED",
            "producer": ((PRODUCER % (wave, ordered_by))
                         if fixup else "author-wave execution of the controlling agent's work orders (ruling R2)"),
            "catcher": "SP/Ezek/_land_author_part_ezek.py (form, coverage, local tiling, E-01 only); a distinct checker "
                       "reviews the amended rows after the apply step",
            "role_separation": "the landing tool proves form only; it does not review content",
            "outcome": status, "recorded_at": datetime.now(timezone.utc).isoformat(),
            "brief": {"path": "Ezek/" + str(brief_p.relative_to(EZ)).replace("\\", "/"), "sha256": sha(brief_p)},
            "orders": {"path": "Ezek/" + str(orders_p.relative_to(EZ)).replace("\\", "/"), "sha256": sha(orders_p)},
            "deliverable_source": str(src), "output_file": "Ezek/" + str(dest.relative_to(EZ)).replace("\\", "/"), "output_sha256": sha(dest),
            "form_defects": defects, "landing_summary": summary,
            "tokens_reported": a.tokens, "tool_uses": a.tool_uses,
            "token_note": "runtime-reported subagent tokens for this execution",
            "unresolved_uncertainty": rec.get("unresolved_uncertainty", []),
            "e19_selfreported": rec.get("e19_selfreport") or "NOT REPORTED by the agent",
        }
        with receipts_p.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(receipt, ensure_ascii=False) + "\n")
        out["actions"].append("receipt appended for %s" % xid)

    NOTES.mkdir(exist_ok=True)
    note_p = NOTES / (xid.replace("#", "%23") + ".json")
    if note_p.is_file():
        out["actions"].append("evidence note already present - kept, never overwritten")
    else:
        note = {"attempt_id": aid, "execution_id": xid, "sources": rec.get("sources", []), "outcome": rec.get("outcome", {}),
                "verification": rec.get("verification", []), "unresolved_uncertainty": rec.get("unresolved_uncertainty", []),
                "items": rec.get("items", []), "cure_tests": rec.get("cure_tests", []),
                "flags_on_my_rows": rec.get("flags_on_my_rows"), "self_authored": True,
                "limit": "accountable work summary; not chain of thought and not independent proof. Built verbatim from "
                         "the agent's own OW-8 final message."}
        note_p.write_text(json.dumps(note, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
        out["actions"].append("evidence note written")

    subprocess.run([sys.executable, str(CAMPAIGN / "_capture_index.py"), "--book", "Ezek", "--write"],
                   capture_output=True, text=True, encoding="utf-8")
    chk = subprocess.run([sys.executable, str(CAMPAIGN / "_capture_index.py"), "--check"],
                         capture_output=True, text=True, encoding="utf-8")
    out["capture_index"] = json.loads(chk.stdout)["verdict"]
    out["verdict"] = status
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0 if status == "LANDED" else 2


if __name__ == "__main__":
    sys.exit(main())
