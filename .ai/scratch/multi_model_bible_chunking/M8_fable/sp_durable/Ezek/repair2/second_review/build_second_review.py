#!/usr/bin/env python3
"""OW-6b(b): the SECOND INDEPENDENT FABLE REVIEW of the flagged regions - slices and brief (two blind Fable lanes).

WHICH ROWS, each set from its record:
  * the boss audit's section-7 flagged rows (ezek_boss_audit.v1.json rows whose sets name '(flagged)');
  * #e15 close clearance item 4's named items: the chapter-18 tiling (every row spanning ch 18), the 16:44-50 /
    16:44-58 seam (the rows spanning 16:44-58), the 37:1-14 rival (the row spanning 37:1), and the rows whose grades
    #e15 moved (q3 confidence_moves_by_this_ruling);
  * anything #e16 routes to the second review, when #e16 has landed.
ORDERING: this review runs after #e16 (so it reads the rulings) and BEFORE the final remediation batch, so its
findings are repaired in that one batch rather than a further round.
Each slice row carries the live row in full, its neighbours' spans and grades, and the rulings' named items on it.

usage: python build_second_review.py [--probe]
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
SP = EZ.parent
PROBE = "--probe" in sys.argv
SCR = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
           r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad")
BASE = (SCR / "ezek_second_review_probe") if PROBE else HERE
DELIV = SCR / "ezek_second_review"
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
E16 = EZ / "author" / "e16" / "ruling_e16.json"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
order = [json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip()]
rows = {r["decision_id"]: r for r in order}
idx = {r["decision_id"]: i for i, r in enumerate(order)}


def span(r):
    m = re.match(r"Ezek\.(\d+)\.(\d+)-Ezek\.(\d+)\.(\d+)$", r["span"])
    return (int(m.group(1)), int(m.group(2))), (int(m.group(3)), int(m.group(4)))


def overlapping(a, b):
    return [rid for rid, r in rows.items() if not (span(r)[1] < a or span(r)[0] > b)]


why = {}


def mark(rid, reason):
    why.setdefault(rid, []).append(reason)


boss = json.loads((EZ / "ezek_boss_audit.v1.json").read_text(encoding="utf-8"))
for r in boss["rows"]:
    if any("flagged" in s for s in r.get("sets") or []):
        mark(r["row_id"], "boss audit: section-7 flagged region")
e15 = json.loads((EZ / "ezek_controlling_agent_ruling_e15.v1.json").read_text(encoding="utf-8"))
for rid in [k for k, (a, b) in ((k, span(v)) for k, v in rows.items()) if a[0] <= 18 <= b[0]]:
    mark(rid, "#e15 close clearance 4: the chapter-18 tiling")
for rid in overlapping((16, 44), (16, 58)):
    mark(rid, "#e15 close clearance 4: the 16:44-50 / 16:44-58 seam")
for rid in overlapping((37, 1), (37, 14)):
    mark(rid, "#e15 close clearance 4: the 37:1-14 rival")
for rid in [k for k in (e15["q3_confidence_defects"].get("confidence_moves_by_this_ruling") or {}) if re.fullmatch(r"P\d\d-\d\d\d", k)]:
    mark(rid, "#e15 close clearance 4: a grade #e15 moved")
if E16.is_file():
    r16 = json.loads(E16.read_text(encoding="utf-8"))
    for e in (r16.get("routed_to_second_review") or []) + [x for x in (r16.get("escalations") or []) if "second" in json.dumps(x).lower()]:
        for rid in re.findall(r"P\d\d-\d\d\d", json.dumps(e, ensure_ascii=False)):
            if rid in rows:
                mark(rid, "#e16 routed to the second review: %s" % json.dumps(e, ensure_ascii=False)[:300])
elif not PROBE:
    raise SystemExit("REFUSED: #e16 has not landed; the second review reads its rulings (build with --probe only)")
sl = {}
for rid in sorted(why, key=lambda x: idx[x]):
    i = idx[rid]
    nb = {k: {"row": order[j]["decision_id"], "span": order[j]["span"], "confidence": order[j].get("confidence")}
          for k, j in (("previous", i - 1), ("next", i + 1)) if 0 <= j < len(order)}
    sl[rid] = {"why_in_scope": why[rid], "row": rows[rid], "neighbours": nb}
BASE.mkdir(parents=True, exist_ok=True)
slp = BASE / "second_review_slices.v1.json"
slp.write_text(json.dumps({"schema": "ezek_second_review_slices.v1", "rows_sha256": sha(ROWS), "e16_landed": E16.is_file(),
                           "rows": len(sl), "slices": sl}, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
PINS = [(ROWS, "the live rows"), (slp, "YOUR ROWS: each flagged row in full, why it is in scope, its neighbours"),
        (EZ / "book_strategy_Ezek.md", "the division plan v1 (its section 7 holds these regions)"),
        (EZ / "ezek_boss_audit.v1.json", "the boss audit (the section-7 flags)"),
        (EZ / "ezek_controlling_agent_ruling_e15.v1.json", "#e15 (close clearance item 4 names this review's items)"),
        (EZ / "ezek_controlling_agent_ruling_e14.v1.json", "#e14"), (EZ / "ezek_controlling_agent_ruling_e13.v1.json", "#e13 (CONF-CAL, CUT-RULE)"),
        (EZ / "ezek_controlling_agent_ruling_e12.v1.json", "#e12"),
        (EZ / "repair2" / "step7" / "confcal_audit.v2.json", "the CONF-CAL audit member's view"),
        (EZ / "ezek_device_inventory.v2.json", "the device census"), (EZ / "Ezek_oshb.txt", "the Hebrew witness (WLC/OSHB)"),
        (EZ / "pmarks_Ezek.json", "marks, K/Q, paseq, notes (single witness)"), (EZ / "tools" / "verse_map_web.json", "the English version by verse"),
        (EZ / "web_mt_offset_map.json", "the WEB/MT map")]
if E16.is_file():
    PINS.insert(5, (E16, "#e16 - the controlling agent's latest rulings; read before judging any class it decided"))
table, pins = ["| input | sha256 | what it is |", "|---|---|---|"], []
for p, what in PINS:
    if not Path(p).is_file():
        raise SystemExit("REFUSED: pinned input missing %s" % p)
    shown = str(p) if str(p).startswith(str(SCR)) else "SP\\" + str(Path(p).resolve().relative_to(SP))
    table.append("| `%s` | `%s` | %s |" % (shown, sha(p), what))
    pins.append("| `%s` | `%s` |" % (shown, sha(p)))
B = r"""# OW-6b(b) - SECOND INDEPENDENT FABLE REVIEW OF THE FLAGGED REGIONS - EZEKIEL (two blind lanes)

You are ONE OF TWO BLIND FABLE REVIEWERS reading the same %(rows)d rows; you never see the other. On a HARD book the
owner's directive requires "a second, independent Fable review of the flagged regions" before the close. You REVIEW:
you write nothing to any row. Your findings are repaired in the final remediation batch or ruled on by the
controlling agent.

## For every row, judge the BOUNDARY DECISION, not only the prose

1. **seams** - is each seam of this row where the text's signals put it? Read the Hebrew witness at both faces of both
   seams; weigh the strongest rival the row names and any it does not. A seam you believe wrong is an ESCALATION with
   its evidence (the controlling agent decides; nothing moves silently).
2. **grade** - does the confidence follow CONF-CAL on the faces as measured (a licensed text signal on each near face;
   a text signal on the far face; a licensed or two-faced rival bars high; marks and mid-verse formulae make no face)?
   State what each face carries; say KEEP or the grade the evidence supports, with the faces named.
3. **the named item** - where the slice says why the row is in scope (the chapter-18 tiling, the 16:44-50/16:44-58
   seam, the 37:1-14 rival, a grade #e15 moved), answer that question directly.
4. **claims** - any claim in the row that is false against the witness, the marks or the census, with the exact
   repair; C2-amended - unsourced means absent from BOTH pinned inputs; a mark is recorded on the verse it FOLLOWS.
5. **the scholar reads this** - the register rule: a row is a scholar-facing record; flag any rule id, record name or
   repair narration; English quotations need double curly quotes and a web: reference (A6-b exempts a counted
   device's fixed rendering); refs follow DEF-A4-ARGUED with a ROLE token, a verified face qualifier and seam pair;
   "single-witness" on any mark, paseq or puncta mention; Hebrew SLICED from the witness, never typed; in the zone
   (MT 21:1-5 = WEB 20:45-49) entries on BOTH faces; rotation - no 7-gram in more than a handful of rows, at least 4
   distinct formulations.

## Pinned inputs

%(table)s

Pin rows for the pre-launch check:

%(pins)s

## Output - write early, rewrite at every stage (E-29), digest after the final write

`review.json`: `per_row` {row: {seams, grade, named_item, claims, register - each {verdict OK|DEFECT|ESCALATE|QUESTION,
evidence, tier, exact_repair}}}, `escalations`, `grade_findings` [{row, from, supported, faces}], `cross_row_patterns`,
`what_i_could_not_verify`, `e19_selfreport`, `limit`.

## Hard stops

Write only in your own directory; never modify the corpus or a pinned file; no git, receipts or registry. A digest that
differs from the table: record both and stop.
""" % {"rows": len(sl), "table": "\n".join(table), "pins": "\n".join(pins)}
out = BASE / "SECOND_REVIEW_BRIEF.md"
out.write_text(B, encoding="utf-8", newline="\n")
if not PROBE:
    for lane in ("lane_a", "lane_b"):
        (DELIV / lane).mkdir(parents=True, exist_ok=True)
print(json.dumps({"probe": PROBE, "rows": len(sl), "by_reason": {k: sum(1 for v in why.values() if any(k in x for x in v)) for k in ("boss audit", "chapter-18", "16:44", "37:1-14", "grade #e15", "#e16")},
                  "slices_bytes": slp.stat().st_size, "brief_sha256": sha(out), "slices_sha256": sha(slp)}, indent=1))
