#!/usr/bin/env python3
"""Repair every flagged Hebrew run as a WHOLE RUN, sliced from the verse that actually carries it, and ensure
that verse is cited in the same field.

A DEFECT I CREATED, fixed here. My first Hebrew pass replaced SUBSTRINGS. The run `וְאַתָּה בֶן אָדָם` was
unaccented; I had also queued a replacement for the shorter run `וְאַתָּה`, and the shorter pattern matched
INSIDE the longer phrase. The result was a hybrid - accented first word, unaccented remainder - which is a worse
artifact than what I started with, because it looks like witness bytes for one word and is not witness bytes for
the phrase. The unit of a quotation repair is the WHOLE RUN, and runs must be processed longest-first so a
shorter one cannot eat into a longer one.

THE TWO CHECKS THIS MUST SATISFY, and they are different:
  * the normalizer wants every Hebrew run to be byte-identical to the witness on word boundaries;
  * the citation sweep wants every Hebrew run to COLLATE against an oshb: ref in the SAME FIELD.
So a repair that only fixes the bytes can still fail the sweep, and one that only adds a ref can still fail the
normalizer. Both are handled per run: slice the witness's bytes AND make sure the field cites the verse they
came from.

WHERE I STOP. If a run's skeleton occurs in no verse this row's span touches, I do not go hunting the book for a
verse to attribute it to - that would be choosing a citation to satisfy a checker. Those are reported for an
author.
"""
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import guarded_apply as GA                                                     # noqa: E402

HERE = Path(__file__).resolve().parent
EZ = GA.EZ
PRE = "fbc401e0dfbb6083c753aece4c41582cf28d041fd8bf0133012209416a3cc587"
vmap = json.loads((EZ / "tools" / "verse_map_oshb.json").read_text(encoding="utf-8"))
rep = json.loads((EZ / "repair" / "rows_v7_cwo24.jsonl.validator_report.json").read_text(encoding="utf-8"))

HEB_RUN = re.compile(r"[א-ת֑-ׇ]+(?:[ ־][א-ת֑-ׇ]+)*")
OSHB_REF = re.compile(r"oshb:Ezek\.(\d+)\.(\d+)")
SPAN = re.compile(r"Ezek\.(\d+)\.(\d+)")
POINTS = re.compile(r"[֑-ׇ]")
FINALS = {"ך": "כ", "ם": "מ", "ן": "נ", "ף": "פ", "ץ": "צ"}


def skel(s):
    s = POINTS.sub("", unicodedata.normalize("NFC", s))
    s = "".join(FINALS.get(c, c) for c in s)
    return " ".join(s.split())


# every run the two checks object to, as a set of (row, field) -> runs
flagged = {}
for x in rep["citation_sweep"]["problems"]:
    m = re.match(r"(P\d\d-\d\d\d): Hebrew quote '([^']+)'… in row\.(\w+)", x)
    if m:
        flagged.setdefault((m.group(1), m.group(3)), set()).add(m.group(2))
DEFECT_RUNS = set(rep["hebrew_normalize_dryrun"]["defects"])

verses = {}
for k, v in vmap.items():
    t = (v.get("text") if isinstance(v, dict) else str(v)) or ""
    if t:
        verses[k] = t


def find_window(run):
    """Every (verse, witness-bytes) whose whole-word window matches this run's skeleton."""
    target = skel(run)
    n = len(target.split())
    hits = []
    for k, t in verses.items():
        w = t.split()
        for i in range(len(w) - n + 1):
            cand = " ".join(w[i:i + n])
            if skel(cand) == target:
                hits.append((k, cand))
                break
    return hits


rows = GA.load_rows()
edits, fixed, left = [], [], []
for r in rows:
    rid = r["decision_id"]
    own = set()
    ms = SPAN.findall(str(r.get("span", "")))
    if ms:
        (c1, v1), (c2, v2) = (int(ms[0][0]), int(ms[0][1])), (int(ms[-1][0]), int(ms[-1][1]))
        for ch in range(c1, c2 + 1):
            for vv in range(1, 201):
                k = "Ezek.%d.%d" % (ch, vv)
                if k in verses and (ch > c1 or vv >= v1) and (ch < c2 or vv <= v2):
                    own.add(k)
    for field in ("boundary_rationale", "strongest_rejected_alternative", "device_notes",
                  "literature_type_guess"):
        val = r.get(field)
        if not isinstance(val, str):
            continue
        want = flagged.get((rid, field), set())
        runs_here = [m.group(0) for m in HEB_RUN.finditer(val)]
        # the runs to repair: those the sweep flagged, plus any the normalizer flagged, in THIS field
        todo = [x for x in runs_here if x in want or x in DEFECT_RUNS
                or any(x.startswith(w) or w.startswith(x) for w in want)]
        if not todo:
            continue
        # LONGEST FIRST, so a shorter run cannot eat into a longer one - the bug this file exists to fix
        todo = sorted(set(todo), key=len, reverse=True)
        out = val
        cited = {"Ezek.%s.%s" % (a, b) for a, b in OSHB_REF.findall(val)}
        add_refs = []
        for run in todo:
            hits = find_window(run)
            if not hits:
                left.append({"row": rid, "field": field, "run": run[:50],
                             "why": "no verse carries this run at any pointing"})
                continue
            # prefer a verse the field already cites, then one inside the row's own span
            pick = next((h for h in hits if h[0] in cited), None) \
                or next((h for h in hits if h[0] in own), None)
            if pick is None:
                left.append({"row": rid, "field": field, "run": run[:50],
                             "candidate_verses": [h[0] for h in hits[:5]],
                             "why": "the run occurs only outside this row's span and the field cites none of "
                                    "its verses, so choosing one would be picking a citation to satisfy a "
                                    "checker; an author must say which verse is meant"})
                continue
            verse, bytes_ = pick
            if run != bytes_:
                out = out.replace(run, bytes_)
            if verse not in cited:
                add_refs.append(verse)
                cited.add(verse)
            fixed.append({"row": rid, "field": field, "run": run[:40], "verse": verse,
                          "bytes_changed": run != bytes_, "ref_added": verse in add_refs})
        if add_refs:
            out = out.rstrip()
            tail = " (" + ", ".join("oshb:%s" % v for v in add_refs) + ")"
            out = (out[:-1] + tail + ".") if out.endswith(".") else (out + tail)
        if out != val:
            edits.append({"row_id": rid, "field": field, "op": "set", "expected_before": val, "value": out,
                          "sweep": "disclosures",
                          "why": "Hebrew run(s) replaced with the witness's own bytes as WHOLE RUNS and the "
                                 "verse they came from cited in the same field"})

print(json.dumps({"runs_repaired": len(fixed), "edits": len(edits),
                  "rows": len({e["row_id"] for e in edits}),
                  "refs_added": sum(1 for f in fixed if f["ref_added"]),
                  "bytes_rewritten": sum(1 for f in fixed if f["bytes_changed"]),
                  "left_for_an_author": len(left)}, indent=1))
for f in fixed:
    print("  %-9s %-30s %-26s <- %s%s" % (f["row"], f["field"], f["run"][:24], f["verse"],
                                          " +ref" if f["ref_added"] else ""))
for x in left:
    print("  LEFT %-9s %-28s %-24s %s" % (x["row"], x["field"], x["run"][:22], x["why"][:74]))

(HERE / "hebrew_repair.v2.json").write_text(json.dumps({"repaired": fixed, "left": left},
                                                       ensure_ascii=False, indent=1),
                                            encoding="utf-8", newline="\n")
if not edits:
    raise SystemExit(0)
sim = GA.simulate_plan([("hebrew2", edits)], PRE)
print()
print(json.dumps({"simulation_ok": sim["ok"], "final": sim.get("final_digest_if_applied")}, indent=1))
if not sim["ok"] or "--apply" not in sys.argv:
    print("\n(simulation only; pass --apply to mutate)")
    raise SystemExit(0 if sim["ok"] else 1)
RECEIPTS = EZ / "author" / "ezek_author_wave_sweep_receipts.jsonl"
rec = GA.apply_edits(edits, PRE, "author_wave_hebrew_repair_pass2", ordered_count=len(edits), apply=True)
rec["what_this_was"] = ("whole-run Hebrew repair: each flagged run replaced with the witness's own bytes and "
                        "the verse it came from cited in the same field. Runs processed LONGEST FIRST because "
                        "my first pass replaced substrings and produced a hybrid with an accented first word "
                        "and an unaccented remainder.")
rec["runs_repaired"] = len(fixed)
rec["left_for_an_author"] = len(left)
with RECEIPTS.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
print(json.dumps({k: rec[k] for k in ("sweep", "e18_parity_digits", "rows_touched", "runs_repaired",
                                      "left_for_an_author", "postimage_sha256_measured_from_disk")}, indent=1))
