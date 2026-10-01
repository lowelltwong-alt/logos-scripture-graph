#!/usr/bin/env python3
"""REPAIR-2 step 3 worklist: every measured-false item from every governing source, tested against the CURRENT rows.

SOURCES (#e15 repair2_batch_composition_and_sequence item 3, plus what later rounds carried into this step):
  Q10  - #e15's measured-false list; each fact distinct-checked in distinct_checks_q10.v1.json (13 of 13 reproduce)
  TRACE- the order-to-edit trace's PARTIAL and UNCLEAR items, re-run on the current rows
  CENS - the census-consistency member's flags, re-run on the current rows
  Q11  - the A4 residue: bare decimal verse references outside a list context (a4_extraction_gap.v1.json)
  L02  - author-wave lane 02's four out-of-worklist escalations (durable copy of its deliverable)
  ADJ  - the step-2 adjudication's carried obligations marked step 3
  CSW  - the citation sweep's two standing wrong-verse problems (P08-011, P10-008)

STATUS per item, MEASURED by a string test on the current row and never assumed:
  PRESENT     the claim or entry the order names still stands - the item is owed
  DISCHARGED  step 2 already removed it - recorded, not repeated
  READER      the order names no testable string - an author must read the row (never passed silently)
"""
import hashlib
import json
import re
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
HERE = Path(__file__).resolve().parent
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
rows = {r["decision_id"]: r for r in (json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip())}
PROSE = ("boundary_rationale", "strongest_rejected_alternative", "device_notes", "literature_type_guess")


def text(rid):
    return "\n".join(rows[rid].get(f) or "" for f in PROSE)


def refs(rid):
    return list(rows[rid].get("boundary_evidence_refs") or [])


def signals(rid):
    return rows[rid].get("observed_substrate_signals")


items = []


def add(src, rid, cls, order, test, fields, dcheck=None):
    """test: ('prose', substring) | ('ref', substring) | ('signal', key) | ('reader', None) | ('csw', None)"""
    kind, s = test
    if kind == "prose":
        status = "PRESENT" if s.lower() in text(rid).lower() else "DISCHARGED"
        evidence = s
    elif kind == "ref":
        hit = [e for e in refs(rid) if s.lower() in e.lower()]
        status, evidence = ("PRESENT", hit) if hit else ("DISCHARGED", s)
    elif kind == "signal":
        sg = json.dumps(signals(rid), ensure_ascii=False)
        status, evidence = ("PRESENT" if s in sg else "DISCHARGED"), s
    else:
        status, evidence = "READER", None
    items.append({"id": "S3-%03d" % (len(items) + 1), "source": src, "row": rid, "class": cls,
                  "order": order, "status": status, "tested": {"kind": kind, "for": evidence},
                  "fields": fields, "distinct_check": dcheck})


# ---- Q10 (distinct checks: distinct_checks_q10.v1.json items 1-13)
add("Q10-1", "P02-003", "prose_false", "8:14-18 carries no paseq and no K/Q; the only Masoretic item in the span is the samekh on 8:14",
    ("prose", "no paseq beyond the one already disclosed"), ["device_notes"], "Q10 dc 1")
add("Q10-2a", "P03-019", "prose_false", "the 18:29 note AGREES with BHS; rewrite 'against BHS'", ("prose", "against BHS"),
    ["device_notes", "boundary_rationale"], "Q10 dc 2")
add("Q10-2b", "P03-019", "quotation_extent", "extend the WEB 18:30 gloss to 'says the Lord Yahweh', which the Hebrew splice carries",
    ("reader", None), ["boundary_rationale"], "Q10 dc 2")
add("Q10-3", "P08-012", "prose_false", "36:16 is the FIFTH strict word-event seam since 33:1; 35:1 named", ("prose", "fourth and last"),
    ["boundary_rationale"], "Q10 dc 3")
add("Q10-4", "P07-008", "prose_false", "MT 32:17 names no month; the twelfth-month reading is INFERRED from 32:1", ("prose", "month 12"),
    ["boundary_rationale", "device_notes"], "Q10 dc 4")
add("Q10-5", "P06-001", "prose_false", "narrow 'the book's first foreign addressee'; MT 21:33 (= WEB 21:28) addresses Ammon",
    ("prose", "first foreign addressee"), ["boundary_rationale", "strongest_rejected_alternative"], "Q10 dc 5")
add("Q10-6", "P02-008", "prose_false", "the pe on 11:1 is interior; remove 'A pe follows this very verse' and the superlative",
    ("prose", "A pe follows this very verse"), ["boundary_rationale"], "Q10 dc 6")
add("Q10-7", "P09-010", "prose_false", "no mark on 39:20: remove '-plus-mark' from the onset ground", ("prose", "refrain-plus-mark"),
    ["boundary_rationale", "device_notes"], "Q10 dc 7")
add("Q10-8", "P08-007", "prose_false", "the K/Q entries at 35:9 and 35:12 carry no separators; rewrite 'with its separators stripped'",
    ("prose", "separators stripped"), ["device_notes"], "Q10 dc 8")
add("Q10-9", "P02-018", "prose_stale", "the 2fp recognition clauses are COUNTED (13:21, 13:23); restate and re-weigh the sentence resting on 'outside either counted sweep'",
    ("prose", "outside the two counted recognition families"), ["device_notes"], "Q10 dc 9")
add("Q10-10", "P10-014", "prose_false", "43:15 is not a K/Q verse (two other notes); the span's K/Q verse is 43:16", ("reader", None),
    ["device_notes", "boundary_rationale"], "Q10 dc 10")
add("Q10-11", "P11-007", "disclosure_missing", "add the K/Q disclosure at the row's close verse 46:15", ("reader", None),
    ["device_notes", "boundary_evidence_refs"], "Q10 dc 11")
for rid in sorted(r for r in rows if re.search(r"transport[^.;]{0,80}\b20\b", text(r), re.I)):
    add("Q10-12", rid, "census_stale", "the transport class is 33 verses (46 occurrences); the strategy's closed 20 is a subset",
        ("prose", re.search(r"transport[^.;]{0,80}\b20\b", text(rid), re.I).group(0)), ["boundary_rationale", "device_notes"],
        "Q10 dc 12")
add("Q10-13", "P06-005", "count_mismatch", "four marked units (marks at 26:6, 26:14, 26:18, 26:21) with three ranges listed - reconcile",
    ("reader", None), ["boundary_rationale", "device_notes"], "Q10 dc 13")
for rid in ("P01-006", "P08-003", "P10-001", "P09-009", "P11-001", "P11-013"):
    add("Q10-14", rid, "near_far_inversion", "near/far inversions in prose (lane 02's list; 'far face closes the allotment'); the re-facing of MT devices is step 4",
        ("reader", None), ["boundary_rationale", "strongest_rejected_alternative"], "reader")
for rid, v in (("P10-008", "41:22"), ("P10-005", "41:26"), ("P01-002", "40:38")):
    add("Q10-15", rid, "quotation_truncated", "the quotation at %s stops where the witness stops agreeing with the gloss - conform the gloss to the witness or extend the quotation" % v,
        ("reader", None), ["boundary_rationale", "device_notes"], "reader")
for rid in ("P01-013", "P02-016", "P08-002", "P02-020"):
    add("Q10-17", rid, "digit_convention", "character positions stated 1-based inclusive (the 0-based half-open convention is retired)",
        ("reader", None), ["boundary_rationale", "strongest_rejected_alternative", "device_notes"], "reader")

# ---- L02 (lane 02's out-of-worklist escalations)
add("L02-P02-006", "P02-006", "prose_false", "the wheel vocabulary recurs outside 10:6-17 and 1:15-21 (the stem on 15 verses incl. 3:13, 10:19, 11:22, 23:43; galgal on 5 incl. 23:24, 26:10) - the distinctness claim does not reproduce",
    ("prose", "does not recur outside"), ["strongest_rejected_alternative"], "to distinct-check before writing")
add("L02-P02-016", "P02-016", "prose_stale", "the 13:9 close is still described on the superseded basis (device_notes and the 13:9 refs entry); D3 counts the adonai-form recognition",
    ("prose", "deliberately not tagged"), ["device_notes", "boundary_evidence_refs"], "inventory v2 adonai variant list")

# ---- TRACE (re-run on current rows)
tr = json.loads((HERE / "order_to_edit_trace.v1.json").read_text(encoding="utf-8"))
for k in ("PARTIAL", "UNCLEAR"):
    for x in tr.get(k, []):
        add("TRACE-" + k, x["row"], "order_undischarged", x["order"], ("reader", None), ["per the order"], "order-to-edit trace")

# ---- CENS (re-run on current rows)
cc = json.loads((HERE / "census_consistency.v1.json").read_text(encoding="utf-8"))
for f in cc["flags"]:
    if any(i["row"] == f["row"] and i["class"] == "census_stale" for i in items):
        continue
    add("CENS", f["row"], "census_figure", "figure %s: %s - context: %s" % (f["figure"], f["why"], f["context"][:140]),
        ("reader", None), [f["field"]], "census v2")

# ---- ADJ (step-2 adjudication carried obligations marked step 3)
adj = json.loads((EZ / "repair2" / "step2_reconciliation" / "adjudication_a1" / "adjudication.json").read_text(encoding="utf-8"))
for rid, r in (adj.get("rows") or {}).items():
    for c in r.get("carried_obligations") or []:
        if str(c.get("step")) == "3":
            add("ADJ", rid, "carried_from_step2", c["what"], ("reader", None), ["boundary_evidence_refs or observed_substrate_signals or prose"], "adjudication a1")

# ---- CSW (the citation sweep's standing problems)
add("CSW", "P08-011", "wrong_verse_hebrew", "the Hebrew run 'גויך' in boundary_rationale does not collate against any nearby cited reference - attribute it to its true verse or remove",
    ("reader", None), ["boundary_rationale", "boundary_evidence_refs"], "citation_sweep")
add("CSW", "P10-008", "wrong_verse_hebrew", "the Hebrew run 'וַיּוֹצִאֵ֗נִי' in boundary_rationale does not collate against any nearby cited reference - attribute it to its true verse or remove",
    ("reader", None), ["boundary_rationale", "boundary_evidence_refs"], "citation_sweep")

# ---- Q11 residue
gap = json.loads((EZ / "a4_extraction_gap.v1.json").read_text(encoding="utf-8"))
for c in gap["candidates_NOT_in_a_list_context_for_a_human_read"]:
    add("Q11", c["row"], "bare_decimal_anchor", "a bare dotted verse reference '%s' with no OSIS token before it: if it is an argued anchor, rewrite it to an explicit oshb:/web:Ezek.C.V form and mirror it; if not, leave it (context: %s)" % (c["token"], c["context"][:110]),
        ("prose", c["token"]), [c["field"], "boundary_evidence_refs"], "reader")

from collections import Counter
out = {"schema": "ezek_repair2_step3_worklist.v1", "rows_sha256": sha(ROWS), "items": items,
       "tally_by_status": dict(Counter(i["status"] for i in items)),
       "tally_by_source": dict(Counter(i["source"].split("-")[0] for i in items)),
       "rows_touched": sorted({i["row"] for i in items if i["status"] != "DISCHARGED"}),
       "tier": "status MEASURED by string tests on the current rows; READER items carry no pass"}
p = HERE / "step3_worklist.v1.json"
p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({k: out[k] for k in ("tally_by_status", "tally_by_source")}, indent=1),
      "\nrows with owed items:", len(out["rows_touched"]))
for i in items:
    if i["status"] == "DISCHARGED":
        print("  DISCHARGED by step 2:", i["id"], i["row"], i["source"])
