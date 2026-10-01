#!/usr/bin/env python3
"""REPAIR-2 step-2 CANDIDATE GATE, v2. Read-only: builds candidate rows in memory and never writes the corpus.

WHAT v1 GOT WRONG, and why v2 exists. v1 (the gate both step-2 author lanes ran) filtered the mirror member's output
on a `mirrored` key the member never sets, so `x.get("mirrored", True)` was always true and its citation-mirroring
arm COULD NEVER FIRE. Both lanes' ALL_CLEAN certified the register arm only. Author lane B found it; ledger E-36
addendum, queue E13-99. The two lanes then answered the same broken gate in opposite ways - one wrote verses by
position, one named thirteen uncovered citations - and the pinned suite confirmed the duty is real: lane B's prose
takes refs_mirror GREEN -> FLAGS with exactly those thirteen items (E13-100).

WHAT v2 CHECKS, per proposed row:
  1. REGISTER - every class in tools/check_register.py over every content leaf, prose and refs alike.
  2. MIRRORING - tools/check_refs_mirror.analyze_row: its `items` list IS the argued citations no refs entry
     mirrors; any item, any orphan ref, any mirror-reading disagreement makes the row unclean.
  3. REFS ARE APPEND-ONLY IN STEP 2 - every live entry must survive unchanged and in order. Removing or rewording an
     entry is step 3 (measured-false) or step 4 (vocabulary) work, and doing it here would collide with them.
  4. EACH NEW ENTRY IS WELL-FORMED against the vocabulary PINNED TODAY: one face-prefixed reference (or the dual
     form inside the zone), exactly one bracketed token from the member's ROLE_VOCABULARY, NO face qualifier (clause
     6 v2 qualifiers are installed by step 4's sweep, which will pick these entries up), and an annotation of one to
     six words (the rotation rule).
  5. FACE (X2, #e15 Q5): an MT-borne device token (kq, mark, paseq, note, device) sits on the oshb: face; QUOTE on
     the web: face.
  6. THE ZONE: an entry touching WEB 20:45-49, WEB ch 21 or MT ch 21 must be DUAL, "web:... = oshb:...", and the
     pair must agree with the offset map's own web_to_mt, never with arithmetic.

A SELFTEST RUNS FIRST AND GATES EVERY VERDICT (E-36): fixtures include rows that MUST fail, taken from the real
lane-B proposal, so an arm that cannot fire refuses the run instead of passing it.

usage: python check_candidate_v2.py <proposal.json>     proposal = {"<row>": {"<field>": <text or list>}}
       python check_candidate_v2.py --selftest
"""
import json
import re
import sys
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
sys.path.insert(0, str(EZ / "tools"))
import check_register as CR                                                    # noqa: E402
import check_refs_mirror as CM                                                 # noqa: E402
import ezek_lib as LIB                                                         # noqa: E402

PROSE = ("boundary_rationale", "strongest_rejected_alternative", "device_notes", "literature_type_guess")
REFS = "boundary_evidence_refs"
VOCAB = tuple(CM.ROLE_VOCABULARY)
MT_BORNE = {"DISCLOSURE-kq", "DISCLOSURE-mark", "DISCLOSURE-paseq", "DISCLOSURE-note", "DISCLOSURE-device"}

REF = r"(oshb|web):Ezek\.(\d{1,2})\.(\d{1,3})(?:-Ezek\.(\d{1,2})\.(\d{1,3}))?"
ENTRY = re.compile(r"^" + REF + r"(?: = " + REF + r")? \[([A-Za-z-]+)(:[a-z]+)?\] (.+)$")
ZONE_WEB = {(20, v) for v in range(45, 50)} | {(21, v) for v in range(1, 33)}
ZONE_MT = {(21, v) for v in range(1, 38)}


def _verses(face, c1, v1, c2, v2):
    a = (int(c1), int(v1))
    b = (int(c2), int(v2)) if c2 else a
    return face, a, b


def _touches_zone(face, a, b):
    zone = ZONE_MT if face == "oshb" else ZONE_WEB
    if a[0] == b[0]:
        return any((a[0], v) in zone for v in range(a[1], b[1] + 1))
    return any(x in zone for x in (a, b)) or any(c in (20, 21) for c in range(a[0], b[0] + 1))


def check_new_entry(e):
    """Return a list of problems for one NEW refs entry (empty list = well-formed)."""
    m = ENTRY.match(e)
    if not m:
        return ["not in the entry form '<face>:Ezek.C.V[-Ezek.C.V][ = <face>:Ezek.C.V[-...]] [TOKEN] annotation'"]
    g = m.groups()
    token, qual, note = g[10], g[11], g[12]
    probs = []
    if token not in VOCAB:
        probs.append("token [%s] is not in the pinned ROLE_VOCABULARY" % token)
    if qual:
        probs.append("face qualifier '%s' is step-4 work; step 2 installs the bare token and step 4's sweep "
                     "qualifies it" % qual)
    words = len(note.split())
    if not 1 <= words <= 6:
        probs.append("annotation has %d words; the rotation rule allows 1 to 6" % words)
    f1, a1, b1 = _verses(g[0], g[1], g[2], g[3], g[4])
    dual = g[5] is not None
    if _touches_zone(f1, a1, b1) or (dual and _touches_zone(*_verses(g[5], g[6], g[7], g[8], g[9]))):
        if not dual or g[0] != "web" or g[5] != "oshb":
            probs.append("the entry touches the ch 20/21 zone and must be DUAL in the form 'web:... = oshb:...'")
        else:
            f2, a2, b2 = _verses(g[5], g[6], g[7], g[8], g[9])
            if LIB.web_to_mt(*a1) != a2 or LIB.web_to_mt(*b1) != b2:
                probs.append("dual pair disagrees with the offset map: web %s-%s maps to %s-%s, entry says %s-%s"
                             % (a1, b1, LIB.web_to_mt(*a1), LIB.web_to_mt(*b1), a2, b2))
    else:
        if token in MT_BORNE and g[0] != "oshb":
            probs.append("an MT-borne device token [%s] sits on the oshb: face (X2)" % token)
        if token == "QUOTE" and g[0] != "web":
            probs.append("a [QUOTE] sits on the web: face (X2)")
    return probs


def check_row(live_row, fields):
    cand = dict(live_row)
    problems = []
    for f, v in fields.items():
        if f not in PROSE and f != REFS:
            problems.append({"field": f, "problem": "not a field step 2 may propose"})
            continue
        cand[f] = v
    if REFS in fields:
        new_list, old_list = list(fields[REFS] or []), list(live_row.get(REFS) or [])
        it = iter(new_list)
        if not all(any(x == y for y in it) for x in old_list):
            problems.append({"field": REFS, "problem": "a live entry was removed, reworded or reordered - refs are "
                             "APPEND-ONLY in step 2"})
        for e in new_list:
            if e in old_list:
                continue
            for p in check_new_entry(e):
                problems.append({"field": REFS, "entry": e, "problem": p})
    flags = CR.scan_row(cand, "candidate")
    a = CM.analyze_row(cand)
    unmirrored = [{"citation": x.get("citation"), "class": x.get("class"), "field": x.get("field"),
                   "raw": x.get("raw")} for x in (a.get("items") or [])]
    orphans, disagreements = a.get("orphan_refs") or [], a.get("mirror_reading_disagreements") or []
    clean = not (problems or flags or unmirrored or orphans or disagreements)
    return {"clean": clean, "form_problems": problems,
            "register_flags": [{"field": f["field"], "class": f["class"], "match": f["match"]} for f in flags],
            "unmirrored_argued_citations": unmirrored, "orphan_refs": orphans,
            "mirror_reading_disagreements": disagreements,
            "comparisons": {"register_classes_scanned": len(CR.CLASSES), "citations_read": a.get("citations_read"),
                            "refs_entries_checked": len(cand.get(REFS) or [])}}


def live_rows():
    return {r["decision_id"]: r for r in
            (json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip())}


def selftest():
    live = live_rows()
    lane_b = json.loads((EZ / "author" / "repair2_step2" / "lane_b" / "proposal.json").read_text(encoding="utf-8"))
    b = lane_b["P08-002"]
    cases = []
    r = check_row(live["P08-002"], b)
    cases.append(("lane B's P08-002 prose without refs MUST be unclean on mirroring (the arm v1 could not fire)",
                  (not r["clean"]) and any("33.21" in str(x["citation"]) for x in r["unmirrored_argued_citations"])))
    fixed = dict(b, boundary_evidence_refs=list(live["P08-002"][REFS]) + ["oshb:Ezek.33.21 [ANCHOR] dateline past this close"])
    r2 = check_row(live["P08-002"], fixed)
    cases.append(("the same prose plus a well-formed entry covering 33:21 clears THAT citation",
                  not any("33.21" in str(x["citation"]) for x in r2["unmirrored_argued_citations"])
                  and not r2["form_problems"]))
    bad_q = dict(fixed, boundary_evidence_refs=list(live["P08-002"][REFS]) + ["oshb:Ezek.33.21 [WARRANT-close:far] dateline past close"])
    cases.append(("a face qualifier in step 2 is refused", any("step-4" in p["problem"] for p in check_row(live["P08-002"], bad_q)["form_problems"])))
    removed = dict(fixed, boundary_evidence_refs=list(live["P08-002"][REFS])[1:])
    cases.append(("removing a live entry is refused", any("APPEND-ONLY" in p["problem"] for p in check_row(live["P08-002"], removed)["form_problems"])))
    long_note = {REFS: list(live["P08-002"][REFS]) + ["oshb:Ezek.33.21 [ANCHOR] a dateline that opens the next unit here"]}
    cases.append(("an annotation over six words is refused", any("1 to 6" in p["problem"] for p in check_row(live["P08-002"], long_note)["form_problems"])))
    face = {REFS: list(live["P08-003"][REFS]) + ["web:Ezek.33.20 [DISCLOSURE-mark] pe behind the dateline"]}
    cases.append(("an MT-borne device on the web: face is refused", any("X2" in p["problem"] for p in check_row(live["P08-003"], face)["form_problems"])))
    zone_single = {REFS: list(live["P04-008"][REFS]) + ["web:Ezek.21.7 [ANCHOR] preceding verse content only"]}
    cases.append(("a zone entry that is not dual is refused", any("DUAL" in p["problem"] for p in check_row(live["P04-008"], zone_single)["form_problems"])))
    mt7 = LIB.web_to_mt(21, 7)
    zone_ok = {REFS: list(live["P04-008"][REFS]) + ["web:Ezek.21.7 = oshb:Ezek.%d.%d [ANCHOR] preceding verse content only" % mt7]}
    cases.append(("a correctly mapped dual zone entry is accepted", not check_row(live["P04-008"], zone_ok)["form_problems"]))
    zone_bad = {REFS: list(live["P04-008"][REFS]) + ["web:Ezek.21.7 = oshb:Ezek.21.7 [ANCHOR] preceding verse content only"]}
    cases.append(("a dual pair computed by arithmetic instead of the map is refused", any("offset map" in p["problem"] for p in check_row(live["P04-008"], zone_bad)["form_problems"])))
    reg = {"device_notes": "the samekh is disclosed under A10 at this seam"}
    cases.append(("a bare rule id in prose is a register flag", any(f["class"] == "bare_rule_id" for f in check_row(live["P08-003"], reg)["register_flags"])))
    denom = check_row(live["P08-003"], {})
    cases.append(("a live row is checked with a nonzero denominator", denom["comparisons"]["citations_read"] and denom["comparisons"]["refs_entries_checked"]))
    failed = [n for n, ok in cases if not ok]
    print(json.dumps({"selftest_cases": len(cases), "failed": failed}, indent=1))
    return 1 if failed else 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    if selftest():
        raise SystemExit("REFUSED: the gate's selftest failed, so no verdict is computed (E-36)")
    prop = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    live = live_rows()
    report = {}
    for rid, fields in prop.items():
        report[rid] = {"clean": False, "form_problems": [{"problem": "no such row"}]} if rid not in live else check_row(live[rid], fields)
    all_clean = bool(report) and all(r["clean"] for r in report.values())
    print(json.dumps({"rows_checked": len(report), "ALL_CLEAN": all_clean,
                      "rows_unclean": sorted(k for k, v in report.items() if not v["clean"]),
                      "per_row": report}, ensure_ascii=False, indent=1))
    return 0 if all_clean else 1


if __name__ == "__main__":
    raise SystemExit(main())
