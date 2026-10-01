#!/usr/bin/env python3
"""FINAL REMEDIATION WORKLIST v2: every owed correction after REPAIR-2 step 7, #e16, the second review and #e17, grouped by
row, on the re-tiled corpus. v1 (build_final_worklist.py) is kept unchanged; it predates #e17 and the re-tiling.

Classes, each read from the record that holds it:
  RETILE     the 8 rows #e17 wrote: rewrite whole from the ruling's ground, faces and tokens; the hard flags, mirror citations
             and refs the re-tiling left out travel as data
  S7DEF      step-7 reconciled defects (step7_reconciled.v2.json)
  S7OUT      step-7 readers' out-of-scope observations
  R6         step-6 adjudicators' routed corrections
  E16 / E17  the controlling agent's author orders, and mechanical orders the planner could not execute exactly
  GROUND     the applied grade moves (#e16 as settled by #e17): the prose states the ground of the grade it carries
  CONFCAL    CONF-CAL v4 finds the grade outside the range the faces derive: state the ruling's ground, or record a
             GRADE_QUESTION with the faces - never change a grade
  RIVALTOKEN a rival weighed in prose with no WARRANT-rival token (v4 missing_token)
  C4TOKEN    a 'he said to me' verse interior to the span with no WARRANT-rival token (#e17 T-5)
  REG        register flags on the row (book-wide member on the live rows)
  WEBQ, MARKSYM  web_quotes and mark_symmetry flags
An item on a row #e17 retired is carried to every new row made from it, marked so. Scope cut 3 (E13-111): a LOW defect
raised by ONE step-7 reader takes one author lane ('lanes': 'ONE'); every other item takes both blind lanes.
Universals member flags are NOT items (never a close criterion; the gate's completion measure does not read them).
Refuses if a hard flag sits on a row that is not a RETILE row, or if a source names a row the corpus does not carry.

usage: python build_final_worklist_v2.py
"""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
OUT = HERE / "final_worklist.v2.json"
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
BASIS = HERE / "suite_basis" / "rows_03327cf4.jsonl"
REP = Path(str(BASIS) + ".validator_report.json")
REC = EZ / "repair2" / "step7" / "step7_reconciled.v2.json"
R16 = EZ / "author" / "e16" / "ruling_e16.json"
R17 = EZ / "author" / "e17" / "ruling_e17.json"
PLAN = EZ / "repair2" / "e16" / "mechanical" / "plan.json"
RETILE = EZ / "repair2" / "e17" / "retile_e17.manifest.json"
CC4 = EZ / "repair2" / "step7" / "confcal_audit.v4.json"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
PID = re.compile(r"P\d\d-\d\d\d")
PROSE = ["boundary_rationale", "strongest_rejected_alternative", "device_notes", "literature_type_guess"]
REFS = "boundary_evidence_refs"

if sha(ROWS) != sha(BASIS):
    raise SystemExit("REFUSED: the suite basis is not the live rows; re-run the suite on a copy of the live rows")
rows_list = [json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip()]
rows = {r["decision_id"]: r for r in rows_list}
by_writer = {r["writer_decision_id"]: r["decision_id"] for r in rows_list}
rep = json.loads(REP.read_text(encoding="utf-8"))
man = json.loads(RETILE.read_text(encoding="utf-8"))
if man["postimage_sha256_measured_from_disk"] not in (sha(ROWS),) and man["postimage_sha256_measured_from_disk"] != "e6f74aea60208af4e8b2f933fafefb6701e634a56781942cc08be0f7909c31d9":
    raise SystemExit("REFUSED: the re-tiling manifest is not in this rows file's chain")
r16 = json.loads(R16.read_text(encoding="utf-8-sig"))
r17 = json.loads(R17.read_text(encoding="utf-8-sig"))
plan = json.loads(PLAN.read_text(encoding="utf-8"))
cc4 = json.loads(CC4.read_text(encoding="utf-8"))
if cc4["inputs"]["rows_sha256"] != sha(ROWS):
    raise SystemExit("REFUSED: CONF-CAL v4 was run on other rows; re-run it with --overwrite")

new_of = {}                                    # retired id -> new ids made from it
label_of = {}
for lab, v in man["new_row_ids"].items():
    label_of[v["decision_id"]] = lab
    for src in v["from"]:
        new_of.setdefault(src, []).append(v["decision_id"])
retired = set(man["retired"])
items = []


def add(cls, row, order, data, source, lanes="TWO", refs=True):
    targets = [(row, None)]
    if row in retired:
        targets = [(n, row) for n in new_of[row]]
    for t, carried in targets:
        if t not in rows:
            raise SystemExit("REFUSED: %s names a row the corpus does not carry: %r" % (cls, t))
        items.append({"id": None, "class": cls, "row": t, "fields_hint": PROSE + ([REFS] if refs else []), "order": order,
                      "data": data, "source": source, "lanes": lanes, "status": "PENDING",
                      **({"carried_from_retired_row": carried} if carried else {})})


# ---- RETILE: one item per new row, with everything the re-tiling left for the authors
hard = {}
for p in rep["citation_sweep"]["problems"]:
    m = PID.match(p)
    hard.setdefault(m.group(0) if m else "?", []).append({"member": "citation_sweep", "problem": p})
for f in rep["role_tokens"].get("flags") or []:
    hard.setdefault(f["row"], []).append({"member": "role_tokens", **f})
outside = sorted(set(hard) - set(label_of))
if outside:
    raise SystemExit("REFUSED: hard flags on rows that are not re-tiled rows: %s" % outside)
mirror = {}
for c in rep["refs_mirror"].get("worklist_citations") or []:
    mirror.setdefault(c["decision_id"], []).append(c)
ro = {n["provisional_label"]: (o, n) for o in r17["retiling_orders"] for n in o["new_rows"]}
for did, lab in sorted(label_of.items()):
    o, n = ro[lab]
    add("RETILE", did,
        ("REWRITE THIS ROW WHOLE. The controlling agent re-tiled it (span, grade, unit type and collection are final). Its "
         "prose is a SEED: the boundary rationale is the ruling's ground verbatim, and the rejected alternative and device notes "
         "are the retired rows' texts joined, so they still argue seams this row no longer has. Write the row as one record "
         "of THIS span: onset and close faces as the ruling measured them, each interior rival the ruling names weighed and "
         "tokened, the device notes for the verses of this span only (every mark, paseq and K/Q disclosure kept for the "
         "verses it concerns). RE-MEASURE every face on the witness; the ruling's required tokens are orders of substance, "
         "not bytes: the hard flags below show that some of them put a mark on the verse AFTER it (a mark is recorded on "
         "the verse it follows) or give a later pair verse ':far' (it is ':near'); write them true. Claim accounting on "
         "this row is reported to the adjudicator, not enforced (the seed is not a reviewed claim set)."),
        {"ruling_new_row": n, "retiling_order": {k: o[k] for k in o if k != "new_rows"}, "retired_rows": [s for s in o["retire"]],
         "hard_flags_on_the_seed": hard.get(did, []), "mirror_citations_on_the_seed": mirror.get(did, []),
         "refs_left_out_by_the_retiling": [x for x in man["refs_left_out_as_invalid_on_the_new_span"] if x["new_row"] == did],
         "conditional_token_orders": [x for x in man["conditional_token_orders_for_authors"] if x["new_row"] == did]},
        "Ezek/author/e17/ruling_e17.json retiling_orders; Ezek/repair2/e17/retile_e17.manifest.json")

# ---- S7DEF / S7OUT
rec = json.loads(REC.read_text(encoding="utf-8"))
for d in rec["defects"]:
    one = d["agreement"] in ("A_ONLY", "B_ONLY") and d["max_severity"] == "LOW"
    add("S7DEF", d["row"],
        ("A step-7 reader found this %s defect (%s; raised by %s). RE-MEASURE against the witness first: repair what reproduces "
         "with the smallest change that makes the row true; NO_DEFECT with evidence what does not." %
         (d["item"], d["max_severity"], {"BOTH": "both readers", "A_ONLY": "one reader", "B_ONLY": "one reader"}[d["agreement"]])),
        {"item": d["item"], "agreement": d["agreement"], "severity": d["max_severity"], "reader_A": d["A"], "reader_B": d["B"]},
        "Ezek/repair2/step7/step7_reconciled.v2.json", lanes="ONE" if one else "TWO")
for s, v in rec["strides"].items():
    for lane in ("A", "B"):
        obs = v.get("outside_scope", {}).get(lane)
        flat = obs if isinstance(obs, list) else [x for vals in (obs or {}).values() for x in (vals if isinstance(vals, list) else [vals])]
        for o in flat:
            for rid in sorted(set(PID.findall(json.dumps(o, ensure_ascii=False)))):
                if rid in rows or rid in retired:
                    add("S7OUT", rid, "A step-7 reader observed this outside the changed fields. RE-MEASURE; repair what reproduces; NO_DEFECT with evidence otherwise.",
                        {"stride": s, "reader": lane, "observation": o}, "Ezek/repair2/step7/step7_reconciled.v2.json strides.%s.outside_scope" % s)

# ---- R6
for h in (1, 2):
    adj = EZ / "author" / "repair2_step6" / ("h%d_adjudication" % h) / "adjudication.json"
    for e in json.loads(adj.read_text(encoding="utf-8")).get("routed") or []:
        txt = json.dumps(e, ensure_ascii=False)
        if re.search(r"for #e16|to #e16|#e16:|class question|confidence observation", txt, re.I) and not re.search(r"exact repair|replace|->|-&gt;|add ", txt, re.I):
            continue
        for rid in sorted(set(PID.findall(txt))):
            if rid in rows or rid in retired:
                add("R6", rid, "ROUTED by a step-6 adjudicator with its repair, verbatim below. RE-MEASURE; make the repair if it reproduces; NO_DEFECT with evidence otherwise.",
                    {"routed_entry": e}, str(adj.relative_to(EZ)))

# ---- E16 / E17 author orders and routed mechanical orders
routed = {(r.get("id"), r.get("row")) for r in plan["routed_to_authors"] if r.get("id")}
voided = " | ".join(x for o in r17["retiling_orders"] for x in o.get("orders_voided_on_retired_rows") or [])
for tag, rr, src in (("E16", r16, "Ezek/author/e16/ruling_e16.json"), ("E17", r17, "Ezek/author/e17/ruling_e17.json")):
    for o in rr.get("orders_for_final_remediation") or []:
        kind = str(o.get("kind", "")).lower()
        for rid in sorted(set(PID.findall(str(o.get("row", ""))))):
            if kind == "author" or (o.get("id"), rid) in routed or (o.get("id"), o.get("row")) in routed:
                if rid not in rows and rid not in retired:
                    raise SystemExit("REFUSED: %s order %s names %s, which no rows file carries" % (tag, o.get("id"), rid))
                note = ("" if rid not in retired else
                        " This order was written for a row #e17 retired; the re-tiling order says of such orders: %s. Execute it "
                        "on this row only where it still applies to this span; NO_DEFECT with the reason otherwise." % voided[:900])
                add(tag, rid, "ORDERED by the controlling agent: execute exactly; STOP with evidence if the order cannot be made true." + note,
                    {"order": o, "was_mechanical_routed": kind != "author"}, src)

# ---- GROUND
for g in plan["grade_moves"]:
    if g["row"] in retired:
        continue
    add("GROUND", g["row"], ("The controlling agent moved this row's grade %s -> %s (applied). Make the prose state the ground of the grade "
                              "it carries, in the faces' own terms, and remove any sentence that argues the old grade: %s" % (g["from"], g["to"], g.get("ground"))),
        {"grade_move": g}, "Ezek/repair2/e16/mechanical/plan.json grade_moves", refs=False)

# ---- CONFCAL, RIVALTOKEN, C4TOKEN
decided = {g["row"] for g in plan["grade_moves"]} | {d["row"] for d in r17["grade_decisions"]} | set(label_of)
for x in cc4["rows_for_final"]:
    by_ruling = x["row"] in decided
    add("CONFCAL", x["row"],
        (("The grade (%s) was decided by the controlling agent, and the audit derives a different range from the faces. Make the "
          "prose state the ruling's ground in the faces' own terms (a plan naming that caps the grade, a disclosed guard). Never change the grade.")
         if by_ruling else
         ("The audit derives a range from the faces that does not contain the grade (%s). If a ground the row can state holds the "
          "grade (a plan naming, a guard, a disclosed reading), state it; if none does, record GRADE_QUESTION in discharge.json "
          "with the faces measured. Never change the grade.")) % x["grade"],
        {"audit": {k: x[k] for k in ("grade", "derived_range", "state", "disagreeing_faces", "onset_seam", "close_seam")}, "decided_by_ruling": by_ruling},
        "Ezek/repair2/step7/confcal_audit.v4.json rows_for_final", refs=False)
for rid, pairs in cc4["missing_token_rows"].items():
    add("RIVALTOKEN", rid, ("The prose weighs a rival at %s with no WARRANT-rival refs entry. Add one per pair (face qualifier by side, the pair "
                            "as the annotation's first token, ':merge' when the rival contests this row's own seam), or reword the prose "
                            "if the pair is not in fact weighed." % ", ".join(pairs)), {"pairs": pairs}, "Ezek/repair2/step7/confcal_audit.v4.json missing_token_rows")
for rid, pairs in cc4["c4_missing_token_rows"].items():
    add("C4TOKEN", rid, ("'He said to me' at the head of a verse inside a vision is a licensed onset, whoever speaks. At %s it stands inside "
                         "this row with no token: weigh it - a WARRANT-rival:near entry on the pair and the ground that holds the row "
                         "(one clause of device notes, the strongest rival in the rejected-alternative field)." % ", ".join(pairs)),
        {"pairs": pairs}, "#e16 C4 / #e17 K4 and T-5; Ezek/repair2/step7/confcal_audit.v4.json c4_missing_token_rows")

# ---- REG, WEBQ, MARKSYM (from the suite on the live rows)
reg = {}
for f in rep["register"].get("flags") or []:
    rid = by_writer.get(f["decision_id"], f["decision_id"])
    reg.setdefault(rid, []).append({k: f[k] for k in ("field", "class", "match", "context")})
for rid, fl in reg.items():
    add("REG", rid, ("Register flags on this row, listed below: state the substance the flagged words point at and name the witness "
                     "and its layers instead of a scale label, rule, record, file or classification value ('(sweep: N verses)' is the one "
                     "sanctioned count shorthand; evidence-tier scale labels such as 'tier-1' are barred). Change no claim."),
        {"flags": fl}, "register member on the live rows")
for f in rep["web_quotes"].get("flags") or []:
    m = re.match(r"^\[(\d+)\]\.(\w+)", f.get("path", ""))
    if not m:
        raise SystemExit("REFUSED: a web_quotes flag whose path is not '[row index].field': %r" % f.get("path"))
    add("WEBQ", rows_list[int(m.group(1))]["decision_id"], ("Five or more consecutive WEB words stand without the quotation convention: "
                                                            "put them in double curly quotes with an in-field web: reference, or reword."),
        {"web_quotes_flag": f}, "web_quotes member on the live rows")
for f in rep["mark_symmetry"].get("flags") or []:
    add("MARKSYM", f["decision_id"], "The mark-symmetry member flags this claim against the marks apparatus. RE-MEASURE; make the claim true; NO_DEFECT with evidence otherwise.",
        {"mark_symmetry_flag": f}, "mark_symmetry member on the live rows")

for n, it in enumerate(items, 1):
    it["id"] = "F-%03d" % n
by_class = Counter(i["class"] for i in items)
by_row = Counter(i["row"] for i in items)
two_rows = sorted({i["row"] for i in items if i["lanes"] == "TWO"})
out = {"schema": "ezek_final_remediation_worklist.v2", "rows_sha256": sha(ROWS),
       "inputs": {"suite_report_sha256": sha(REP), "step7_reconciled_sha256": sha(REC), "e16_sha256": sha(R16), "e17_sha256": sha(R17),
                  "plan_sha256": sha(PLAN), "retile_manifest_sha256": sha(RETILE), "confcal_v4_sha256": sha(CC4)},
       "scope_cut_3": "items with lanes ONE are given to lane A only; lane B's worklist view omits them",
       "not_items": {"universals_member_flags": rep["universals"].get("flag_count")},
       "items_by_class": dict(by_class), "rows_owed": len(by_row), "rows_owed_by_both_lanes": len(two_rows),
       "distinct_checks": [], "ruling_count_check": {}, "items": items}
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps({"items": len(items), "items_by_class": dict(by_class), "lanes": dict(Counter(i["lanes"] for i in items)),
                  "rows_owed": len(by_row), "rows_owed_by_both_lanes": len(two_rows), "rows_not_owed": sorted(set(rows) - set(by_row)),
                  "rows_with_most_items": by_row.most_common(8), "sha256": sha(OUT)}, indent=1))
