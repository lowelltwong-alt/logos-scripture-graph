#!/usr/bin/env python3
"""Generate the FINAL REMEDIATION slices, the substance file and one AUTHOR BRIEF per (slice, blind lane).

Slices: the owed rows of final_worklist.v2.json split into N slices balanced by size (live prose plus owed items, size
descending then row id - deterministic). Two blind Opus lanes per slice and one Fable adjudicator (OW-13, OW-19). Scope
cut 3 (E13-111): an item marked lanes ONE is given to lane A only; lane B's slice file omits it (and any row left empty).
The gate is v6: v5 with claim accounting reported, not enforced, on the eight re-tiled rows only.

usage: python build_final_brief.py --slices N --slice K --lane A|B
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
SP = EZ.parent
DELIV_ROOT = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
                  r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad\ezek_final")
WL = HERE / "final_worklist.v2.json"
GATE = HERE / "check_candidate_v6.py"
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
arg = lambda n: sys.argv[sys.argv.index(n) + 1]                                # noqa: E731
PROSE = ("boundary_rationale", "strongest_rejected_alternative", "device_notes", "literature_type_guess")
N, K, LANE = int(arg("--slices")), int(arg("--slice")), arg("--lane").upper()
if LANE not in ("A", "B") or not 1 <= K <= N:
    raise SystemExit("usage: --slices N --slice K --lane A|B")

wl = json.loads(WL.read_text(encoding="utf-8"))
if sha(ROWS) != wl["rows_sha256"]:
    raise SystemExit("REFUSED: the rows changed since the final worklist was built; rebuild it first")
rows = {r["decision_id"]: r for r in (json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip())}

# ---- substance, verbatim with locations (written once; identical bytes for every slice and lane)
r16 = json.loads((EZ / "author" / "e16" / "ruling_e16.json").read_text(encoding="utf-8-sig"))
r17 = json.loads((EZ / "author" / "e17" / "ruling_e17.json").read_text(encoding="utf-8-sig"))
e15 = json.loads((EZ / "ezek_controlling_agent_ruling_e15.v1.json").read_text(encoding="utf-8"))
e12 = json.loads((EZ / "ezek_controlling_agent_ruling_e12.v1.json").read_text(encoding="utf-8"))
awb = (EZ / "AUTHOR_WAVE_BRIEF.v1.md").read_text(encoding="utf-8")


def between(start, end, label):
    a = awb.find(start)
    b = awb.find(end, a + len(start))
    if a < 0 or b < 0:
        raise SystemExit("REFUSED: could not extract %s from AUTHOR_WAVE_BRIEF.v1.md" % label)
    return {"id": label, "source": "Ezek/AUTHOR_WAVE_BRIEF.v1.md from line %d" % (awb[:a].count("\n") + 1), "verbatim": awb[a:b].strip()}


subst = [
    {"id": "clause 6 v2 (face qualifier and seam pair on every warrant)", "source": "Ezek/ezek_controlling_agent_ruling_e15.v1.json q5_role_vocabulary.DEF_A4_ARGUED_clause_6_v2",
     "verbatim": e15["q5_role_vocabulary"]["DEF_A4_ARGUED_clause_6_v2"]},
    {"id": "C1 forward-merge rivals (:merge)", "source": "Ezek/author/e16/ruling_e16.json c1_forward_merge", "verbatim": r16["c1_forward_merge"]},
    {"id": "C2 merge pairing", "source": "Ezek/author/e16/ruling_e16.json c2_merge_pairing", "verbatim": r16["c2_merge_pairing"]},
    {"id": "C3 the therefore-turn", "source": "Ezek/author/e16/ruling_e16.json c3_lakhen_turn", "verbatim": r16["c3_lakhen_turn"]},
    {"id": "C4 said-to-me and transport inside a vision", "source": "Ezek/author/e16/ruling_e16.json c4_confcal_member", "verbatim": r16["c4_confcal_member"]},
    {"id": "the scale's application rules for this book", "source": "Ezek/author/e16/ruling_e16.json scale_application_rules_binding_for_ezekiel",
     "verbatim": r16["scale_application_rules_binding_for_ezekiel"]},
    {"id": "#e17 class rulings K1-K7", "source": "Ezek/author/e17/ruling_e17.json class_rulings", "verbatim": r17["class_rulings"]},
    {"id": "A16", "source": "Ezek/ezek_controlling_agent_ruling_e12.v1.json rulings[A16_held_note_vs_disclosure].ruling",
     "verbatim": next(r["ruling"] for r in e12["rulings"] if r["class_id"].startswith("A16_"))},
    between("## 5. The A9/A16 weighing duty", "---", "A9/A16 weighing"),
    between("## 1. CUT-RULE", "---", "CUT-RULE and the precedence of a driver over a mark"),
    between("**CONF-CAL", "**The scale has exactly", "CONF-CAL (no grade is moved in this step)"),
]
subst_p = HERE / "final_substance.v1.json"
data = json.dumps({"schema": "ezek_final_substance.v1", "entries": subst}, ensure_ascii=False, indent=1).encode("utf-8")
if subst_p.exists() and subst_p.read_bytes() != data:
    raise SystemExit("REFUSED: %s exists with different bytes (E-41); a running lane may pin it" % subst_p.name)
subst_p.write_bytes(data)

# ---- slices
owed = {}
for it in wl["items"]:
    owed.setdefault(it["row"], []).append(it)
size = {r: sum(len(rows[r].get(f) or "") for f in PROSE) + len(json.dumps(owed[r], ensure_ascii=False)) for r in owed}
parts, tot = {k: [] for k in range(1, N + 1)}, {k: 0 for k in range(1, N + 1)}
for r in sorted(owed, key=lambda x: (-size[x], x)):
    k = min(tot, key=lambda j: (tot[j], j))
    parts[k].append(r)
    tot[k] += size[r]
mine = {r: [i for i in owed[r] if LANE == "A" or i["lanes"] == "TWO"] for r in parts[K]}
mine = {r: v for r, v in mine.items() if v}
items = [i for v in mine.values() for i in v]
sl = {r: {"row": r, "span": rows[r]["span"], "confidence": rows[r]["confidence"], "unit_type": rows[r]["unit_type"],
          "live_prose": {f: rows[r].get(f) for f in PROSE}, "refs": rows[r].get("boundary_evidence_refs"), "owed_items": mine[r]}
      for r in sorted(mine)}
slices_p = HERE / ("final_slices_s%d_lane%s.v1.json" % (K, LANE))
slices_p.write_text(json.dumps({"schema": "ezek_final_slices.v1", "slice": K, "of": N, "lane": LANE, "rows_sha256": wl["rows_sha256"],
                                "rows": len(sl), "items": len(items), "slices": sl}, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
by_class = {}
for i in items:
    by_class[i["class"]] = by_class.get(i["class"], 0) + 1
DELIV = DELIV_ROOT / ("s%d_lane_%s" % (K, LANE.lower()))

PINS = [
    (ROWS, "the live rows"),
    (slices_p, "YOUR ROWS: span, grade, prose, refs and the owed items"),
    (WL, "the worklist (the gate's scope)"),
    (subst_p, "the substance you apply, verbatim from the records that define it"),
    (EZ / "author" / "e17" / "ruling_e17.json", "the controlling agent's latest ruling (re-tilings, grade decisions, orders)"),
    (EZ / "author" / "e16" / "ruling_e16.json", "the ruling before it (class rulings, orders)"),
    (EZ / "ezek_controlling_agent_ruling_e15.v1.json", "the ruling that set the role vocabulary and the register rule"),
    (GATE, "YOUR GATE (v6)"),
    (EZ / "repair2" / "step5" / "check_candidate_v5.py", "imported by the gate"),
    (EZ / "repair2" / "step4" / "check_candidate_v4.py", "imported by the gate"),
    (EZ / "repair2" / "step3" / "check_candidate_v3_1.py", "imported by the gate"),
    (EZ / "repair2" / "step3" / "check_candidate_v3.py", "imported by the gate"),
    (EZ / "repair2" / "step2_reconciliation" / "check_candidate_v2.py", "imported by the gate"),
    (EZ / "repair2" / "suite_delta.py", "imported by the gate"),
    (EZ / "tools" / "run_validator_suite.py", "run by the gate"),
    (EZ / "tools" / "check_register.py", "the register member"),
    (EZ / "tools" / "check_role_tokens.py", "the hard member that verifies every face qualifier and seam pair"),
    (EZ / "tools" / "role_tokens_phase.json", "that member's pinned phase"),
    (EZ / "tools" / "check_refs_mirror.py", "imported by the gate"),
    (EZ / "tools" / "check_web_quotes.py", "the quotation member"),
    (EZ / "tools" / "ezek_lib.py", "imported by the gate"),
    (HERE / ("final_extract_s%d.v1.json" % K), "YOUR WITNESS EXTRACT: every verse of your rows' spans with three verses of margin - the "
                                               "Hebrew line sliced from the witness, the WEB text, and the marks, paseq and K/Q on each verse. "
                                               "Work from this; the three files below are the sources it was sliced from and you open one only "
                                               "if a verse you need is absent here"),
    (EZ / "tools" / "verse_map_web.json", "the English version by verse (source of the extract; opening it costs your whole context)"),
    (EZ / "Ezek_oshb.txt", "the Hebrew witness (WLC/OSHB; source of the extract)"),
    (EZ / "pmarks_Ezek.json", "marks, K/Q, paseq, notes (single witness; source of the extract)"),
    (EZ / "ezek_device_inventory.v3.json", "the device census v3 (said-to-me, colophons, vision returns; additive over v2)"),
    (EZ / "ezek_device_inventory.v2.json", "the device census v2"),
    (EZ / "book_strategy_Ezek.md", "the division plan (sections 6-7 name cut sites and regions)"),
    (EZ / "web_mt_offset_map.json", "the WEB/MT map"),
]
table, pins = ["| input | sha256 | what it is |", "|---|---|---|"], []
for p, what in PINS:
    if not Path(p).is_file():
        raise SystemExit("REFUSED: pinned input missing %s" % p)
    shown = "SP\\" + str(Path(p).resolve().relative_to(SP))
    table.append("| `%s` | `%s` | %s |" % (shown, sha(p), what))
    pins.append("| `%s` | `%s` |" % (shown, sha(p)))

B = r"""# FINAL REMEDIATION - EZEKIEL. Author brief, SLICE %(k)d of %(n)d, blind lane %(lane)s

Attempt `ezek_final_s%(k)d_lane_%(lanel)s_a1`, execution `ezek_final_s%(k)d_lane_%(lanel)s_a1#e1`. You are ONE OF TWO BLIND
LANES on this slice; a Fable adjudicator reconciles you with the other lane, whose work you never see. Every other slice has
its own lanes. This is the last authoring pass before the book's final check. Your slice: %(rows)d rows, %(items)d owed
items: %(by_class)s. %(lanenote)s

## The item classes (each item carries its order and its data; read the order, then the data)

- **RETILE** - a row the controlling agent re-tiled. Span, grade, unit type and collection are FINAL. Its prose is a seed
  (the ruling's ground verbatim, and the retired rows' rejected-alternative and device texts joined), so it still argues
  seams the row no longer has. REWRITE the row whole as one record of this span, from the ruling's ground, faces and
  required tokens (in the item's data) and the witness. The hard flags on the seed travel with the item: the ruling's
  tokens place some marks on the verse AFTER the mark (a mark is recorded on the verse it FOLLOWS) and give one later pair
  verse ':far' (it is ':near'). Write them true. Keep every mark, paseq and K/Q disclosure for the verses of this span.
  The gate REPORTS the anchors you remove from a seed to the adjudicator instead of requiring accounting.
- **S7DEF / S7OUT / R6** - a defect a reader found, an out-of-scope observation, a routed repair. RE-MEASURE on the witness
  first; repair what reproduces with the smallest change that makes the row true; NO_DEFECT with evidence otherwise.
- **E16 / E17** - an order of the controlling agent: execute it exactly; STOP with evidence if it cannot be made true. An
  order carried from a retired row applies only where it still applies to this span.
- **GROUND** - the grade was moved by the controlling agent: make the prose state the ground of the grade it carries in
  the faces' own terms, and remove any sentence that argues the old grade.
- **CONFCAL** - the audit derives a range from the faces that does not hold the grade. State the ground that holds it (a
  plan naming, a guard, a disclosed reading) or record GRADE_QUESTION with the faces. NEVER change a grade.
- **RIVALTOKEN / C4TOKEN** - a rival weighed in prose with no WARRANT-rival entry, or a 'he said to me' verse inside a
  vision interior to the span with none: add the entry (qualifier by side; the pair as the annotation's first token;
  ':merge' when the rival contests this row's own seam) with the ground that holds the row, or reword where the pair is
  not in fact weighed.
- **REG / WEBQ / MARKSYM** - member flags: state the substance instead of a label; put five or more WEB words in double
  curly quotes with an in-field web: reference; make a mark claim true to the apparatus.

**No grade, span, identity or signals change.** A grade you believe wrong is a GRADE_QUESTION, never an edit.

## Rules for what you may write

- **Change no claim beyond an item's order.** The gate extracts every face reference, verse number, Hebrew run, evidence
  tier word, count and curly-quoted English from a row's prose; anything your edit removes must be ACCOUNTED FOR in
  discharge.json under `claim_accounting[row]` as `{"anchor": <exact string the gate prints>, "why": ...}` (RETILE rows:
  reported, not required).
- **Refs:** add or re-gloss the entries an item needs; each new entry takes a ROLE token and, on a WARRANT, a verified
  face qualifier (a seam pair first on a rival). Every argued citation is mirrored by a refs entry with a ROLE token.
  MT-borne devices sit on the oshb: face; English quotations on the web: face.
- **Quotations:** five or more consecutive WEB words are a quotation whatever the delimiter: double curly quotes and an
  in-field web: reference; a run that is only the WEB's fixed rendering of a counted device is exempt.
- **Marks:** recorded on the verse they FOLLOW; every mark, paseq or puncta mention carries "single-witness". **Hebrew:**
  never hand-typed - SLICED from the witness or the live row. **Categorical claims:** unsourced means absent from BOTH
  pinned inputs. **The zone:** MT 21:1-5 = WEB 20:45-49 and MT 21:6-37 = WEB 21:1-32; an entry touching it is written on
  BOTH faces. **Rotation:** no 7-gram in more than a handful of rows; vary repeated statements.
- **The register rule:** a row is a scholar-facing record - no rule ids, ruling numbers, file or tool names, digests,
  record, census, plan, inventory or worklist names, scale labels ('tier-1'), review or wave talk, repair narration. State
  substance; name the witness and its layers; "(sweep: N verses)" is the one sanctioned count shorthand. **Read back as
  English** every field you change after your final edit, and record `read_back: true` per item only then.

## Budget and token economy (owner directive; binding)

The owner has set a hard token line for this book and it is close, and a measured audit showed where the cost really
goes: every file you pull into context is re-read on every one of your later tool calls. So:

- **Work from your extract and your slice file.** Do NOT open the live rows file, the worklist, or the three witness
  sources unless a verse you need is missing from your extract - the gate reads the rows and the worklist for you.
- **Build your proposal in ONE pass**: assemble it with a single script that writes proposal.json and discharge.json,
  rather than many small edits.
- **Run the gate when your proposal is complete** - twice at most: once to see the verdict, once after fixing what it
  reports. If a third run is truly needed, say why in `limit`.
- Measure only what an item rests on; do not re-review fields no item names; never print a whole file into your context.

## Pinned inputs

%(table)s

Pin rows for the pre-launch check:

%(pins)s

## Your gate

`python -B <SP>\Ezek\repair2\final\check_candidate_v6.py %(deliv)s\proposal.json --work %(deliv)s\gate_work --discharge %(deliv)s\discharge.json --worklist <SP>\Ezek\repair2\final\final_worklist.v2.json`

Run until ALL_CLEAN is true. It checks the per-row delta, claim accounting, new English-form problems, the entry form of
every added refs entry, and the WHOLE pinned suite with no hard member allowed to gain a flag.

## Outputs - write early and rewrite at every stage (E-29); digest after the final write

1. `%(deliv)s\proposal.json` - `{"<row>": {"<field>": <full new value>}}`, only changed fields; refs as FULL lists.
2. `%(deliv)s\discharge.json` - `items`: per item id (F-nnn) `status` DISCHARGED | NO_DEFECT | STOP | GRADE_QUESTION,
   `what_i_wrote` or `evidence`, `read_back`; top-level `claim_accounting`, `grade_questions`, `gate`,
   `what_i_could_not_verify`, `e19_selfreport`, `limit`.

## Hard stops

Write only in your own directory; never modify the corpus or a pinned file; no git, receipts or registry; never list,
glob or search directories - open the exact paths above. Escalate rather than write: any seam move, any grade you believe
wrong, a pinned input that contradicts itself, a digest that differs from the table.
""" % {"k": K, "n": N, "lane": LANE, "lanel": LANE.lower(), "rows": len(sl), "items": len(items),
       "by_class": ", ".join("%s %d" % kv for kv in sorted(by_class.items())),
       "lanenote": ("Items marked `\"lanes\": \"ONE\"` (a low-severity defect one earlier reader raised) are assigned to you alone; the adjudicator reads your work on them directly."
                    if LANE == "A" else "Some low-severity items on this slice are assigned to the other lane only; they are not in your file."),
       "table": "\n".join(table), "pins": "\n".join(pins), "deliv": str(DELIV)}
out = HERE / ("FINAL_AUTHOR_BRIEF_S%d_%s.md" % (K, LANE))
out.write_text(B, encoding="utf-8", newline="\n")
DELIV.mkdir(parents=True, exist_ok=True)
print(json.dumps({"slice": K, "lane": LANE, "brief": out.name, "brief_sha256": sha(out), "rows": len(sl), "items": len(items),
                  "slice_sizes_all": {k: len(v) for k, v in parts.items()}, "slices_sha256": sha(slices_p), "substance_sha256": sha(subst_p)}, indent=1))
