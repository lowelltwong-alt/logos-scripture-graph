#!/usr/bin/env python3
"""Diagnose the 8 Hebrew runs that are not byte-identical to the witness, and say which are mechanically fixable.

THE RULE, from the normalizer's own docstring: every maximal Hebrew run in a row must be a BYTE-IDENTICAL
substring of Ezek_oshb.txt standing on word boundaries. NFD-only differences are auto-replaced with the source's
bytes. These 8 survived that, so they differ in actual characters - they were hand-typed or mis-sliced. The
toolkit's instruction is blunt: "NEVER hand-type Hebrew - slice from verse_map_oshb.json."

WHY THIS MATTERS MORE THAN A FAILING CHECK. A Hebrew run in a row is a QUOTATION of the witness. If its bytes
are not the witness's bytes, the row asserts that the text reads something it does not - which is the same class
as the manufactured quotation lane 01 refused to write, arriving from the other direction. So each of these is
diagnosed rather than patched: what did the author intend, what does the witness actually carry, and is the
difference mechanical (accents, a final form, a Qere) or a wrong verse?

THE DIAGNOSIS IS PER-RUN AND REPORTS THE EVIDENCE, never a bare verdict. For each run it finds the best window
in the witness by consonantal skeleton, then names the exact character difference, so a reader can see whether
the fix is "use these bytes" or "this quote is from another verse".
"""
import json
import re
import sys
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(EZ / "tools"))

OSHB = (EZ / "Ezek_oshb.txt").read_text(encoding="utf-8")
vmap = json.loads((EZ / "tools" / "verse_map_oshb.json").read_text(encoding="utf-8"))
report = json.loads((EZ / "repair" / "rows_v7_cwo24.jsonl.validator_report.json").read_text(encoding="utf-8"))
DEFECTS = report["hebrew_normalize_dryrun"]["defects"]

POINTS = re.compile(r"[\u0591-\u05C7]")
FINALS = {"\u05DA": "\u05DB", "\u05DD": "\u05DE", "\u05DF": "\u05E0", "\u05E3": "\u05E4",
          "\u05E5": "\u05E6"}


def skel(s):
    """Consonantal skeleton: points and accents stripped, final forms folded, spaces collapsed."""
    s = POINTS.sub("", unicodedata.normalize("NFC", s))
    s = "".join(FINALS.get(c, c) for c in s)
    return " ".join(s.split())


# index the witness by verse, with skeletons
verses = {}
for k, v in vmap.items():
    txt = v.get("text") if isinstance(v, dict) else str(v)
    if txt:
        verses[k] = {"text": txt, "skel": skel(txt)}

out = []
for run in DEFECTS:
    r_sk = skel(run)
    exact_hits = [k for k, v in verses.items() if run in v["text"]]
    skel_hits = [k for k, v in verses.items() if r_sk and r_sk in v["skel"]]
    best = None
    if skel_hits:
        # for the first skeleton hit, find the witness window whose skeleton equals the run's, and show its bytes
        k = skel_hits[0]
        words = verses[k]["text"].split()
        n = len(r_sk.split())
        for i in range(len(words) - n + 1):
            w = " ".join(words[i:i + n])
            if skel(w) == r_sk:
                best = {"verse": k, "witness_bytes": w,
                        "identical": w == run,
                        "differs_only_in_points_or_accents": skel(w) == r_sk and w != run,
                        "char_diff": [(tag, run[i1:i2], w[j1:j2])
                                      for tag, i1, i2, j1, j2 in
                                      SequenceMatcher(None, run, w).get_opcodes() if tag != "equal"][:6]}
                break
    out.append({
        "run": run,
        "chars": len(run),
        "byte_identical_somewhere_in_the_witness": bool(exact_hits),
        "verses_containing_it_exactly": exact_hits[:4],
        "verses_containing_its_skeleton": skel_hits[:6],
        "skeleton_hit_count": len(skel_hits),
        "best_witness_window": best,
        "mechanically_fixable": bool(best and best["differs_only_in_points_or_accents"]),
        "diagnosis": (
            "FIXABLE: the witness carries this run with different points/accents; replace with the witness "
            "bytes" if (best and best["differs_only_in_points_or_accents"]) else
            "ALREADY EXACT somewhere - the normalizer's complaint is about word boundaries, not bytes"
            if exact_hits else
            "NOT IN THE WITNESS at any pointing: the skeleton does not occur, so this is not a quotation of "
            "this book and needs an author decision" if not skel_hits else
            "skeleton occurs but no window reproduces it as a unit - likely a run assembled across a word "
            "boundary or from two verses"),
    })

p = HERE / "hebrew_defect_diagnosis.v1.json"
p.write_text(json.dumps({"schema": "ezek_hebrew_defect_diagnosis.v1",
                         "rule": ("every Hebrew run must be a byte-identical substring of the witness on word "
                                  "boundaries; the toolkit says never hand-type Hebrew, slice from the verse "
                                  "map"),
                         "why_it_matters": ("a Hebrew run in a row is a QUOTATION. Bytes that are not the "
                                            "witness's bytes assert that the text reads something it does "
                                            "not."),
                         "defects": out}, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
for o in out:
    print("%-2d chars  skel_hits=%-3d exact=%-5s  %s"
          % (o["chars"], o["skeleton_hit_count"], o["byte_identical_somewhere_in_the_witness"],
             o["diagnosis"][:96]))
    print("     run: %s" % o["run"][:60])
    if o["best_witness_window"]:
        b = o["best_witness_window"]
        print("     witness %s: %s" % (b["verse"], b["witness_bytes"][:60]))
    print()
print("mechanically fixable: %d of %d" % (sum(1 for o in out if o["mechanically_fixable"]), len(out)))
