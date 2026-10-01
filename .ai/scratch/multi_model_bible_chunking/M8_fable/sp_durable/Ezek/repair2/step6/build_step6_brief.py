#!/usr/bin/env python3
"""Generate REPAIR-2 step-6 SLICES, the SUBSTANCE file and the AUTHOR BRIEF (the A8 transport batch; two blind lanes).

The gate is step 5's v5 pointed at the step-6 worklist: claim accounting, English form, per-row delta, entry form
with clause 6 v2 qualifiers on any refs entry an item adds, and the whole suite. The substance the lanes need -
#e15 Q8 in full, #e12 A16, the A9/A16 weighing duty, CUT-RULE and precedence, the transport predicate and class
facts, and the recognition class facts - is carried verbatim with each source's exact location.

usage: python build_step6_brief.py [--probe]
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
SP = EZ.parent
PROBE = "--probe" in sys.argv
SCR = Path(r"C:\Users\lowel\AppData\Local\Temp\claude\C--Users-lowel-OneDrive-Desktop-Git-Projects-03-World-View"
           r"\910cbe15-396b-4a0e-82f6-8aa1e2edf1e4\scratchpad")
BASE = (SCR / "ezek_step6_probe") if PROBE else HERE
WL = BASE / "step6_worklist.v1.json"
GATE = EZ / "repair2" / "step5" / "check_candidate_v5.py"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
PROSE = ("boundary_rationale", "strongest_rejected_alternative", "device_notes", "literature_type_guess")

wl = json.loads(WL.read_text(encoding="utf-8"))
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
if sha(ROWS) != wl["rows_sha256"]:
    raise SystemExit("REFUSED: the rows changed since the step-6 worklist was built; rebuild it first")
rows = {r["decision_id"]: r for r in (json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip())}
e12 = json.loads((EZ / "ezek_controlling_agent_ruling_e12.v1.json").read_text(encoding="utf-8"))
e15 = json.loads((EZ / "ezek_controlling_agent_ruling_e15.v1.json").read_text(encoding="utf-8"))
inv = json.loads((EZ / "ezek_device_inventory.v2.json").read_text(encoding="utf-8"))
awb = (EZ / "AUTHOR_WAVE_BRIEF.v1.md").read_text(encoding="utf-8")


def between(start, end, label):
    a = awb.find(start)
    b = awb.find(end, a + len(start))
    if a < 0 or b < 0:
        raise SystemExit("REFUSED: could not extract %s from AUTHOR_WAVE_BRIEF.v1.md" % label)
    return {"id": label, "source": "Ezek/AUTHOR_WAVE_BRIEF.v1.md from line %d" % (awb[:a].count("\n") + 1),
            "verbatim": awb[a:b].strip()}


vt = inv["vision_transport"]
subst = [
    {"id": "#e15 Q8 (the ruling this step executes)", "source": "Ezek/ezek_controlling_agent_ruling_e15.v1.json q8_transport_class",
     "verbatim": e15["q8_transport_class"]},
    {"id": "A16", "source": "Ezek/ezek_controlling_agent_ruling_e12.v1.json rulings[A16_held_note_vs_disclosure].ruling",
     "verbatim": next(r["ruling"] for r in e12["rulings"] if r["class_id"].startswith("A16_"))},
    {"id": "A12 (a class is what its predicate defines)", "source": "Ezek/ezek_controlling_agent_ruling_e12.v1.json rulings[A12_device_class_membership].ruling",
     "verbatim": next(r["ruling"] for r in e12["rulings"] if r["class_id"].startswith("A12_"))},
    between("## 5. The A9/A16 weighing duty", "---", "A9/A16 weighing"),
    between("## 1. CUT-RULE", "---", "CUT-RULE and the precedence of a driver over a mark"),
    between("**CONF-CAL", "**The scale has exactly", "CONF-CAL (no grade is raised in this step)"),
    {"id": "the transport class", "source": "Ezek/ezek_device_inventory.v2.json vision_transport",
     "verbatim": {k: vt[k] for k in ("gloss", "predicate_consonantal_skeleton", "count_verses", "count_occurrences", "verses_mt", "tokens_per_verse")}},
    {"id": "the recognition classes behind peer_03's findings", "source": "Ezek/ezek_device_inventory.v2.json formulae",
     "verbatim": {k: {kk: inv["formulae"][k][kk] for kk in ("gloss", "count", "verses_mt") if kk in inv["formulae"][k]}
                  for k in ("recognition_family_64", "recognition_formula_2mp", "recognition_formula_2fp")}},
    {"id": "clause 6 v2 (face qualifier and seam pair on any warrant you add)", "source": "Ezek/ezek_controlling_agent_ruling_e15.v1.json q5_role_vocabulary.DEF_A4_ARGUED_clause_6_v2",
     "verbatim": e15["q5_role_vocabulary"]["DEF_A4_ARGUED_clause_6_v2"]},
]
subst_p = BASE / "step6_substance.v1.json"
subst_p.write_text(json.dumps({"schema": "ezek_repair2_step6_substance.v1", "entries": subst}, ensure_ascii=False, indent=1),
                   encoding="utf-8", newline="\n")

owed = {}
for it in wl["items"]:
    owed.setdefault(it["row"], []).append(it)
# two halves balanced by prose length (deterministic: size descending, then row id), two blind lanes per half
H = int(sys.argv[sys.argv.index("--half") + 1])
size = {r: sum(len(rows[r].get(f) or "") for f in PROSE) + len(json.dumps(owed[r], ensure_ascii=False)) for r in owed}
halves, tot = {1: [], 2: []}, {1: 0, 2: 0}
for r in sorted(owed, key=lambda x: (-size[x], x)):
    k = 1 if tot[1] <= tot[2] else 2
    halves[k].append(r)
    tot[k] += size[r]
owed = {r: owed[r] for r in halves[H]}
half_items = [i for r in owed for i in owed[r]]
sl = {r: {"row": r, "span": rows[r].get("span"), "confidence": rows[r].get("confidence"),
          "live_prose": {f: rows[r].get(f) for f in PROSE}, "refs": rows[r].get("boundary_evidence_refs"),
          "owed_items": owed[r]} for r in sorted(owed)}
slices_p = BASE / ("step6_slices_half%d.v1.json" % H)
slices_p.write_text(json.dumps({"schema": "ezek_repair2_step6_slices.v1", "half": H, "rows_sha256": wl["rows_sha256"], "rows": len(sl),
                                "items": len(half_items), "distinct_checks": wl["distinct_checks"],
                                "ruling_count_check": wl["ruling_count_check"], "slices": sl}, ensure_ascii=False, indent=1),
                    encoding="utf-8", newline="\n")

PINS = [
    (ROWS, "the live rows"),
    (slices_p, "YOUR ROWS: span, confidence, prose, refs, the owed items with their distinct checks as data"),
    (WL, "the worklist and the gate's scope"),
    (subst_p, "the substance you apply, verbatim from the records that define it"),
    (EZ / "ezek_controlling_agent_ruling_e15.v1.json", "the ruling (q8_transport_class governs this step)"),
    (EZ / "ezek_controlling_agent_ruling_e12.v1.json", "the source of A12 and A16"),
    (EZ / "AUTHOR_WAVE_BRIEF.v1.md", "the source of the weighing duty, CUT-RULE and CONF-CAL substance"),
    (GATE, "YOUR GATE (v5, run with the step-6 worklist)"),
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
    (EZ / "tools" / "ezek_lib.py", "imported by the gate"),
    (EZ / "tools" / "verse_map_web.json", "the English version by verse"),
    (EZ / "Ezek_oshb.txt", "the Hebrew witness (WLC/OSHB)"),
    (EZ / "pmarks_Ezek.json", "marks, K/Q, paseq, notes (single witness)"),
    (EZ / "ezek_device_inventory.v2.json", "the device census"),
    (EZ / "web_mt_offset_map.json", "the WEB/MT map"),
    (EZ / "reviews" / "peer_10.json", "peer_10's own words on its four held rows"),
    (EZ / "reviews" / "peer_03.json", "peer_03's own words and per-row readings"),
]
table, pins = ["| input | sha256 | what it is |", "|---|---|---|"], []
for p, what in PINS:
    if not Path(p).is_file():
        raise SystemExit("REFUSED: pinned input missing %s" % p)
    shown = str(p) if str(p).startswith(str(SCR)) else "SP\\" + str(Path(p).resolve().relative_to(SP))
    table.append("| `%s` | `%s` | %s |" % (shown, sha(p), what))
    pins.append("| `%s` | `%s` |" % (shown, sha(p)))
by_class = {}
for i in half_items:
    by_class[i["class"]] = by_class.get(i["class"], 0) + 1

B = r"""# REPAIR-2 STEP 6 - THE TRANSPORT BATCH AND THE ROUTED REPAIRS. Author brief, HALF %(half)d (two blind lanes)

You are ONE OF TWO BLIND LANES on half %(half)d; a Fable adjudicator reconciles you with the other lane, whose work
you never see. The other half has its own two lanes. Your half: %(rows)d rows, %(items)d owed items: %(by_class)s.
Some classes below may have no item in your half.

## What this step executes - #e15 Q8, carried verbatim in the substance file

The transport class is what its STATED predicate defines: 33 verses / 46 occurrences, a strict superset of an older
closed list of 20. The orchestrator ran every membership two ways before issuing an item - the census list and an
independent scan of the witness bytes with the stated predicate - and both agree book-wide (33/33; recognition family
64/64, 2mp 21/21, 2fp 2/2). The results travel with each item as data; you rely on them, and re-derive any you doubt.

- **REL10** - peer_10's four transport rows, held while the class was undefined. Each verse IS a member. A reading
  that depended on its being inside the class stands; one that depended on its being outside fails. The row may name
  the verse a transport verse of the counted class, stated as "(sweep: 33 verses / 46 occurrences)".
- **REL03** - peer_03's four findings resting on recognition memberships that now have pinned lists. Score each
  finding against the row AS IT STANDS NOW: repair what still stands; NO_DEFECT with evidence where an earlier repair
  already cured it.
- **A16** - seven interior transport verses are now licensed rivals and must be WEIGHED: the strongest rival stays in
  the rejected-alternative field; any further live candidate is disclosed in one clause of device_notes as weighed and
  not taken, naming the device, with the guard or ground that holds the row ("a row under three verses is held only
  for a complete word-event unit" is the over-split guard's substance). A weighing is argued, so its verse is
  mirrored by a refs entry: `[WARRANT-rival:near]` or `:far` with the seam pair as the annotation's first token.
- **A16-DISCLOSE** - the ruling carries MT 37:2 to a disclosure (a one-verse remainder): confirm the row discloses it
  as a device the boundary does not rest on (`[DISCLOSURE-device]`); weigh nothing.
- **ONSET5** - five rows whose onset verse is a transport verse MAY name that licensed driver (with a
  `[WARRANT-onset:near]` entry if it is argued). Optional: NO_DEFECT is complete where naming adds nothing.
- **STALE20** - a "20" figure for the transport class; correct it to the counted class.
- **REG6** - a register flag on any row: state the substance the flagged words point at and name the witness and its
  layers ("this witness", "the K/Q apparatus at MT 33:13") instead of a record, file, list label or classification
  label; "(sweep: N verses)" is the one sanctioned count shorthand. Change no claim.
- **ROUTED5** - what the register prose pass's adjudicators routed onward: a claim two authors or an adjudicator
  measured false outside that pass, or a repair that sat in a refs entry the pass held read-only. The routed entry
  travels verbatim. RE-MEASURE before writing: repair what reproduces (the smallest change that makes the claim true),
  NO_DEFECT with evidence what does not, STOP what needs a ruling. A repair here is a claim correction, so account
  for every anchor it removes exactly as for any other edit.

**No grade moves in this step.** If a weighing makes you believe a confidence limb rises or falls, record it as an
observation for the confidence audit; never write it.

## Rules for what you may write

- **Change no claim beyond an item's order.** The gate extracts every face reference, verse number, Hebrew run,
  evidence-tier word, count and curly-quoted English from a row's prose; anything your edit removes must be ACCOUNTED
  FOR in discharge.json under `claim_accounting[row]` as `{"anchor": <exact string the gate prints>, "why": ...}`.
- **Refs:** you may ADD or re-gloss the entries an item needs; each new entry takes a ROLE token and, on a WARRANT,
  a verified face qualifier (and a seam pair on a rival). DEF-A4-ARGUED: every argued citation is mirrored by a refs
  entry carrying a ROLE token. MT-borne devices sit on the oshb: face; English quotations on the web: face.
- **Quotations:** five or more consecutive WEB words are a quotation whatever the delimiter and take double curly
  quotes and an in-field web: reference; a run that is nothing but the WEB's fixed rendering of a counted device is
  exempt (A6-b).
- **The mark convention:** a mark is recorded on the verse it FOLLOWS. A mark, paseq or puncta mention carries
  "single-witness". **Hebrew:** never hand-type it - SLICED from the witness or the live row. **Categorical claims:**
  C2-amended - unsourced means absent from BOTH pinned inputs. **The zone:** MT 21:1-5 = WEB 20:45-49 and MT 21:6-37 =
  WEB 21:1-32; an entry touching it is written on BOTH faces, mapped by the offset map. **Rotation:** no 7-gram in
  more than a handful of rows, at least 4 distinct formulations for repeated statements - seven weighings must not
  read as one template.
- **The register rule:** a row is a scholar-facing record - no rule ids, ruling numbers, file or tool names,
  digests, record/census/plan/inventory names, review or wave talk, repair narration. State substance; name the
  witness and its layers; "(sweep: N verses)" is the one sanctioned count shorthand. **Read back as English** every
  field you change, after your final edit, and record `read_back: true` per item only then.
- No grade, span, identity or signals change. A false only-ground is a STOP, never a substitution.

## Pinned inputs

%(table)s

Pin rows for the pre-launch check:

%(pins)s

## Your gate

`python -B <SP>\Ezek\repair2\step5\check_candidate_v5.py <your dir>\proposal.json --work <your ABSOLUTE dir>\gate_work --discharge <your dir>\discharge.json --worklist %(wl)s`

It checks the per-row delta, the claim accounting, new English-form problems, the entry form of every added refs
entry (clause 6 v2 qualifiers included), and the WHOLE pinned suite - including the hard role_tokens member, which
verifies every face qualifier and seam pair - with no hard member allowed to gain a flag.

## Outputs - write early and rewrite at every stage (E-29); digest after the final write

1. `proposal.json` - `{"<row>": {"<field>": <full new value>}}`, only changed fields; refs as FULL lists.
2. `discharge.json` - per item id (S6-nnn): `status` DISCHARGED | NO_DEFECT | STOP, `what_i_wrote` or `evidence`,
   `read_back`, `facts_reproduced` with tiers; top-level `claim_accounting`, `confidence_observations`, `gate`,
   `what_i_could_not_verify`, `e19_selfreport`, `limit`.

## Hard stops

Write only in your own directory; never modify the corpus or a pinned file; no git, receipts or registry. Escalate
rather than write: any seam move, any grade you believe wrong, a pinned input that contradicts itself, a digest that
differs from the table.
""" % {"half": H, "rows": len(sl), "items": len(half_items), "by_class": ", ".join("%s %d" % kv for kv in sorted(by_class.items())),
       "table": "\n".join(table), "pins": "\n".join(pins),
       "wl": (str(WL) if PROBE else "<SP>\\Ezek\\repair2\\step6\\step6_worklist.v1.json")}
out = BASE / ("STEP6_AUTHOR_BRIEF_HALF%d.md" % H)
out.write_text(B, encoding="utf-8", newline="\n")
print(json.dumps({"half": H, "brief": str(out), "brief_sha256": sha(out), "rows": len(sl), "items": len(half_items),
                  "slices_sha256": sha(slices_p), "substance_sha256": sha(subst_p)}, indent=1))
