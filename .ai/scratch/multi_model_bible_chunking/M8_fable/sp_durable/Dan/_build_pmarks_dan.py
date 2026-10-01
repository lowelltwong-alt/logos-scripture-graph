#!/usr/bin/env python3
"""DANIEL mark inventory (pmarks_Dan.json): parashah marks, paseq, K/Q, apparatus notes and the language layer, all
read from the OSHB XML bytes and keyed in MT numbering.

Adapted from Ezek/_build_pmarks_ezek.py. It makes three changes, and each is stated here:
  1. The OSHB KJV-variance notes (`KJV:Dan.c.v`) get their own key, `kjv_variance`, instead of sitting in
     notes_other. Daniel has 66 of them, and they are a numbering witness, not exegesis.
  2. The arithmetic anomalies are COMPUTED rather than written up by hand: the verses with no sof pasuq and the
     verses that carry more than one paragraph mark. A reader explains them from this list; the builder asserts
     nothing about why they occur.
  3. The language layer points to dan_language_zones.json, which is the word-level zone map. The morph-prefix tally
     here counts every morph in a verse body, NOTE WORDS INCLUDED, so it is larger than that file's main-text
     totals by exactly its note_word_totals.

WHY THESE ARE INVENTORIED SEPARATELY. The staged MT text drops every <seg> with its content, so maqaf, paseq, sof
pasuq, samekh and pe do not appear in Dan_oshb.txt at all. That is the right convention for running text. But the
marks are exactly what a boundary argument reaches for, so they are counted here rather than lost. A reviewer who
wants to argue a seam at a samekh must cite THIS file.

WHAT A MARK IS AND IS NOT. Samekh (setumah) and pe (petuchah) are the Masoretic paragraph divisions. They are
EVIDENCE of how the tradition read the text: they inform a boundary and never decide one alone, and tier-4
translation formatting never drives a boundary at all (E-23). A mark is recorded on the verse it FOLLOWS, because
that is where the XML puts it.
"""
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

SP = Path(__file__).resolve().parent
REPO = Path(r"C:\wt\logos-t423-m8-fable")
XML = REPO / "data/candidate/original_language_evidence/canonical_source_views/openscriptures_oshb/files/Dan.xml"
BOOK = "Dan"

SEG_NAME = {"x-samekh": "SAMEKH", "x-pe": "PE", "x-paseq": "PASEQ",
            "x-maqqef": "MAQQEF", "x-sof-pasuq": "SOF_PASUQ", "x-reversednun": "REVERSED_NUN"}
KJV = re.compile(r"^KJV:(Dan\.\d+\.\d+)$")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    raw_b = XML.read_bytes()
    raw = raw_b.decode("utf-8")

    # split into verses, keeping each verse's full body so a seg can be attributed to the verse it follows
    parts = re.split(r'(<verse[^>]*osisID="Dan\.\d+\.\d+"[^>]*>)', raw)
    marks, paseq, other_segs, kq, notes_other, kjv = {}, [], collections.Counter(), {}, {}, {}
    morph_prefix = collections.Counter()
    aramaic = []
    seg_total = collections.Counter()
    verses, no_sof_pasuq = [], []
    cur = None
    for chunk in parts:
        m = re.match(r'<verse[^>]*osisID="(Dan\.\d+\.\d+)"', chunk)
        if m:
            cur = m.group(1)
            verses.append(cur)
            continue
        if cur is None:
            continue
        body = chunk.split("</chapter")[0]
        types = re.findall(r'<seg type="([^"]+)"', body)
        if "x-sof-pasuq" not in types:
            no_sof_pasuq.append(cur)
        for t in types:
            seg_total[t] += 1
            name = SEG_NAME.get(t, t)
            if name in ("SAMEKH", "PE", "REVERSED_NUN"):
                marks.setdefault(cur, []).append(name)
            elif name == "PASEQ":
                paseq.append(cur)
            elif name not in ("MAQQEF", "SOF_PASUQ"):
                other_segs[name] += 1
        # EVERY note, typed or not (the Ezekiel lesson: an untyped punctuation note was once silently dropped)
        for attrs, txt in re.findall(r"<note\b([^>]*)>(.*?)</note>", body, re.S):
            typ = (re.search(r'type="([^"]*)"', attrs) or [None, ""])[1] if 'type="' in attrs else ""
            plain = re.sub(r"<[^>]+>", "", txt).strip()
            k = KJV.match(plain)
            if k and not typ:
                kjv[cur] = k.group(1)
            elif "variant" in typ.lower():
                kq.setdefault(cur, []).append(plain[:200])
            else:
                notes_other.setdefault(cur, []).append(
                    {"type": typ or "(untyped)", "attrs": attrs.strip(), "text": plain[:200]})
        for p in re.findall(r'morph="([A-Za-z])', body):
            morph_prefix[p] += 1
        if 'morph="A' in body:
            aramaic.append(cur)

    multi_mark = {v: ms for v, ms in marks.items() if len(ms) > 1}
    out = {
        "book": BOOK,
        "source": {"path": str(XML.relative_to(REPO)).replace("\\", "/"), "sha256": hashlib.sha256(raw_b).hexdigest()},
        "witness": "WLC (OSHB) - single witness; disclose on every citation",
        "numbering": ("MT != WEB in two zones (MT 3:31-33 = WEB 4:1-3 and MT 4:1-34 = WEB 4:4-37; MT 6:1 = WEB 5:31 "
                      "and MT 6:2-29 = WEB 6:1-28); identity in every other chapter. Byte-proven in "
                      "web_mt_offset_map.json. EVERY ref in this file is MT."),
        "marks": marks,
        "marks_note": ("SAMEKH = setumah (closed section), PE = petuchah (open section), recorded on the verse the "
                       "mark FOLLOWS. Masoretic paragraph evidence: it informs a boundary and never decides one "
                       "alone, and translation formatting never drives a boundary at all (E-23)."),
        "marks_tally": {"SAMEKH": sum(v.count("SAMEKH") for v in marks.values()),
                        "PE": sum(v.count("PE") for v in marks.values()),
                        "REVERSED_NUN": sum(v.count("REVERSED_NUN") for v in marks.values()),
                        "verses_carrying_a_mark": len(marks)},
        "paseq": paseq,
        "paseq_note": ("paseq (U+05C0) is a disjunctive stroke inside a verse. COUNT-ONLY: the extract drops segs, "
                       "so an intra-verse POSITION claim is unsourceable from Dan_oshb.txt and must be read from "
                       "the XML by exact path. Listed once per occurrence, so a verse may repeat."),
        "paseq_tally": {"occurrences": len(paseq), "verses": len(set(paseq))},
        "other_segs": dict(other_segs),
        "other_segs_note": "seg types beyond the paragraph marks, paseq, maqqef and sof-pasuq",
        "seg_totals_in_xml": dict(seg_total),
        "kq": kq,
        "kq_note": ("Ketiv/Qere: the written form and the read form. A K/Q verse is a TEXTUAL-VARIANT site; a row "
                    "whose span covers one discloses it, and a boundary is never argued from the Qere alone."),
        "kq_tally": {"verses": len(kq), "notes": sum(len(v) for v in kq.values())},
        "kjv_variance": kjv,
        "kjv_variance_note": ("untyped OSHB notes of the exact form KJV:Dan.c.v, keyed MT -> English; the numbering "
                              "witness that web_mt_offset_map.json cross-checks"),
        "notes_other": notes_other,
        "notes_other_note": ("non-variant, non-KJV OSHB notes (exegesis, alternative readings, punctuation "
                             "divergences); single-witness, disclose. UNTYPED notes are captured and marked "
                             "'(untyped)'."),
        "arithmetic": {
            "verses_in_xml": len(verses),
            "sof_pasuq_absent_verses": no_sof_pasuq,
            "verses_with_more_than_one_mark": multi_mark,
            "note": ("computed, not explained: each listed verse is a source fact to be read from the XML, and a row "
                     "spanning one discloses it; no boundary is argued from an absent sof pasuq"),
        },
        "morph_prefix_tally_including_note_words": dict(morph_prefix),
        "verses_with_any_aramaic_morph_including_notes": aramaic,
        "language_note": ("morph prefix H = Hebrew, A = Aramaic. The word-level zone map, main text only, is "
                          "dan_language_zones.json: Aramaic from MT 2:4 word 5 to 7:28, with a mid-verse switch at "
                          "2:4. The lists here include apparatus words and are a cross-check, not the zone map."),
    }
    (SP / f"pmarks_{BOOK}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n",
                                            encoding="utf-8", newline="\n")
    print(json.dumps({"verses_in_xml": len(verses), "verses_with_marks": len(marks), "marks_tally": out["marks_tally"],
                      "paseq": out["paseq_tally"], "kq": out["kq_tally"], "kjv_variance_notes": len(kjv),
                      "other_segs": out["other_segs"], "seg_totals_in_xml": out["seg_totals_in_xml"],
                      "morph_prefix_incl_notes": dict(morph_prefix),
                      "aramaic_verses_incl_notes": len(aramaic),
                      "aramaic_first_last": [aramaic[0], aramaic[-1]] if aramaic else None,
                      "sof_pasuq_absent": no_sof_pasuq, "multi_mark": multi_mark,
                      "notes_other": {v: [n["type"] + ": " + n["text"][:60] for n in ns] for v, ns in notes_other.items()}},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
