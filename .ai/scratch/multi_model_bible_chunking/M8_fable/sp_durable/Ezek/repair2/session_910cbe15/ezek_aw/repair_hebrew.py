#!/usr/bin/env python3
"""Replace hand-typed Hebrew with the witness's own bytes, sliced from THE VERSE THE FIELD CITES.

THE DEFECT, measured: eight Hebrew runs the wave inserted are not byte-identical to the witness. All eight
differ the same way - the authors wrote the consonants and vowels but omitted the ACCENTS (te'amim) the witness
carries, and one is fully unpointed with a non-final tsadi where the text has a final one. A Hebrew run in a row
is a QUOTATION, so bytes that are not the witness's bytes assert a reading the text does not have.

WHY THE VERSE MATTERS AND "THE FIRST MATCH" WOULD BE WRONG. My diagnosis found the skeleton of `לָכֵן` in 69
verses and of the messenger formula in 122. Accentuation depends on a word's position in its verse, so the
witness bytes for the same word differ between verses. Slicing from the first skeleton hit would replace a
hand-typed quotation with an ACCURATE QUOTATION OF THE WRONG VERSE - which is worse, because it would then pass
every check while attributing the wrong accents to the row's cited verse.

So each run is sliced from a verse the SAME FIELD cites. Where the field cites no verse, the run is left alone
and reported: that is the case the citation sweep separately flags as "no oshb: ref in its field", and it needs
an author to say which verse is meant. I will not guess a verse in order to clear a check.
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
PRE = "759a4094fbc6ef121e2bc4f5020bcd9841357f87279a1b7a9975ee39e9c1dee9"
vmap = json.loads((EZ / "tools" / "verse_map_oshb.json").read_text(encoding="utf-8"))

HEB_RUN = re.compile(r"[א-ת֑-ׇ]+(?:[ ־][א-ת֑-ׇ]+)*")
OSHB_REF = re.compile(r"oshb:Ezek\.(\d+)\.(\d+)(?:-(?:Ezek\.)?(\d+)(?:\.(\d+))?)?")
POINTS = re.compile(r"[֑-ׇ]")
FINALS = {"ך": "כ", "ם": "מ", "ן": "נ", "ף": "פ",
          "ץ": "צ"}
SKIP = {"boundary_evidence_refs"}          # refs entries are handled by their own arm


def skel(s):
    s = POINTS.sub("", unicodedata.normalize("NFC", s))
    s = "".join(FINALS.get(c, c) for c in s)
    return " ".join(s.split())


OSHB_TEXT = (EZ / "Ezek_oshb.txt").read_text(encoding="utf-8")

# ONLY the runs the normalizer itself reports as defects. My first pass treated any run not byte-present in the
# witness as needing repair, and produced 19 false positives - Qere forms like the K/Q read-forms, which the
# normalizer's own QERE TIER accepts because a Qere lives in the NOTE LAYER and never in the verse bytes. A
# repair script whose defect test is stricter than the checker's manufactures work and, worse, would have
# rewritten legitimate Qere citations into verse bytes that do not contain them.
_report = json.loads((EZ / "repair" / "rows_v7_cwo24.jsonl.validator_report.json").read_text(encoding="utf-8"))
DEFECT_RUNS = set(_report["hebrew_normalize_dryrun"]["defects"])
print("the normalizer names %d defect runs; only those are repaired" % len(DEFECT_RUNS))


def witness_window(run, verse_keys):
    """The witness's own bytes for `run`, sliced from one of `verse_keys`. Returns (bytes, verse) or None."""
    target = skel(run)
    if not target:
        return None
    for k in verse_keys:
        v = vmap.get(k)
        txt = (v.get("text") if isinstance(v, dict) else str(v)) if v else None
        if not txt:
            continue
        words = txt.split()
        n = len(target.split())
        for i in range(len(words) - n + 1):
            w = " ".join(words[i:i + n])
            if skel(w) == target:
                return w, k
    return None


rows = GA.load_rows()
edits, fixed, unfixable = [], [], []
for r in rows:
    rid = r["decision_id"]
    newvals = {}
    for field, val in list(r.items()):
        if field in SKIP or not isinstance(val, str):
            continue
        runs = [m.group(0) for m in HEB_RUN.finditer(val)]
        if not runs:
            continue
        # every verse this FIELD cites, in citation order
        keys = []
        for m in OSHB_REF.finditer(val):
            c1, v1 = int(m.group(1)), int(m.group(2))
            c2 = int(m.group(3)) if m.group(3) else c1
            v2 = int(m.group(4)) if m.group(4) else (int(m.group(3)) if m.group(3) and not m.group(4) else v1)
            if m.group(3) and not m.group(4):
                c2, v2 = c1, int(m.group(3))
            for ch in range(c1, c2 + 1):
                for vv in range(v1 if ch == c1 else 1, (v2 if ch == c2 else 200) + 1):
                    k = "Ezek.%d.%d" % (ch, vv)
                    if k in vmap and k not in keys:
                        keys.append(k)
                    if ch == c2 and vv >= v2:
                        break
        out = val
        for run in runs:
            if run not in DEFECT_RUNS:
                continue                                    # not a run the checker objects to
            if run in OSHB_TEXT:
                continue                                    # already byte-identical to the witness
            if not keys:
                unfixable.append({"row": rid, "field": field, "run": run[:60],
                                  "why": "the field cites no oshb: verse, so the verse this quotes cannot be "
                                         "determined mechanically; an author must name it"})
                continue
            w = witness_window(run, keys)
            if not w:
                unfixable.append({"row": rid, "field": field, "run": run[:60],
                                  "cited_verses": keys[:6],
                                  "why": "no verse this field cites carries this run at any pointing"})
                continue
            bytes_, verse = w
            out = out.replace(run, bytes_)
            fixed.append({"row": rid, "field": field, "from": run[:60], "to": bytes_[:60], "verse": verse})
        if out != val:
            newvals[field] = out
    for field, out in newvals.items():
        edits.append({"row_id": rid, "field": field, "op": "set", "expected_before": r[field], "value": out,
                      "sweep": "disclosures",
                      "why": "hand-typed Hebrew replaced with the witness's own bytes, sliced from a verse this "
                             "field cites"})

print(json.dumps({"runs_repaired": len(fixed), "rows_edited": len({e['row_id'] for e in edits}),
                  "edits": len(edits),
                  "runs_left_alone_needing_an_author": len(unfixable),
                  "repaired_by_verse": dict(Counter(f["verse"] for f in fixed))}, indent=1))
print()
for f in fixed:
    print("  %-9s %-30s %s -> %s" % (f["row"], f["field"], f["from"][:26], f["to"][:30]))
print()
for u in unfixable:
    print("  UNFIXABLE %-9s %-30s %s | %s" % (u["row"], u["field"], u["run"][:26], u["why"][:70]))

(HERE / "hebrew_repair.v1.json").write_text(
    json.dumps({"repaired": fixed, "needing_an_author": unfixable}, ensure_ascii=False, indent=1),
    encoding="utf-8", newline="\n")

if not edits:
    raise SystemExit(0)
sim = GA.simulate_plan([("hebrew", edits)], PRE)
print()
print(json.dumps({"simulation_ok": sim["ok"], "final": sim.get("final_digest_if_applied")}, indent=1))
if not sim["ok"] or "--apply" not in sys.argv:
    print("\n(simulation only; pass --apply to mutate)")
    raise SystemExit(0 if sim["ok"] else 1)

RECEIPTS = EZ / "author" / "ezek_author_wave_sweep_receipts.jsonl"
rec = GA.apply_edits(edits, PRE, "author_wave_hebrew_byte_repair", ordered_count=len(edits), apply=True)
rec["what_this_was"] = ("hand-typed Hebrew replaced with the witness's own bytes, each run sliced from a verse "
                        "the SAME FIELD cites. No run was sliced from an arbitrary verse: the same word carries "
                        "different accents in different verses, so a first-match slice would have produced an "
                        "accurate quotation of the WRONG verse and passed every check.")
rec["runs_repaired"] = len(fixed)
rec["runs_left_for_an_author"] = len(unfixable)
with RECEIPTS.open("a", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
print(json.dumps({k: rec[k] for k in ("sweep", "e18_parity_digits", "rows_touched", "runs_repaired",
                                      "runs_left_for_an_author", "preimage_sha256",
                                      "postimage_sha256_measured_from_disk")}, indent=1))
