#!/usr/bin/env python3
"""EZEKIEL mark inventory (pmarks_Ezek.json) — parashah marks, paseq, K/Q, apparatus notes and the language layer,
all read from the OSHB XML bytes and keyed in MT numbering.

WHY THESE ARE INVENTORIED SEPARATELY. The staged MT text drops every <seg> with its content, so maqaf, paseq,
sof-pasuq, samekh and pe do not appear in Ezek_oshb.txt at all. That is the established convention and it is the
right one for running text — but the marks are exactly what a boundary argument reaches for, so they are counted
here instead of being lost. A reviewer who wants to argue a seam at a samekh must cite THIS file.

WHAT A MARK IS AND IS NOT. Samekh (setumah) and pe (petuchah) are the Masoretic paragraph divisions. They are
EVIDENCE about how the tradition read the text, and this campaign's rule is that they inform a boundary and never
decide one alone: they are a witness, not a verdict, and tier-4 translation formatting never drives a boundary at
all (E-23). A mark is recorded on the verse it FOLLOWS, because that is where the XML puts it.
"""
import collections
import json
import re
import sys
from pathlib import Path

SP = Path(__file__).resolve().parent
REPO = Path(r"C:\wt\logos-t423-m8-fable")
XML = REPO / "data/candidate/original_language_evidence/canonical_source_views/openscriptures_oshb/files/Ezek.xml"
BOOK = "Ezek"

SEG_NAME = {"x-samekh": "SAMEKH", "x-pe": "PE", "x-paseq": "PASEQ",
            "x-maqqef": "MAQQEF", "x-sof-pasuq": "SOF_PASUQ", "x-reversednun": "REVERSED_NUN"}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    raw = XML.read_text(encoding="utf-8")

    # split into verses, keeping each verse's full body so a seg can be attributed to the verse it follows
    parts = re.split(r'(<verse[^>]*osisID="Ezek\.\d+\.\d+"[^>]*>)', raw)
    marks, paseq, other_segs, kq, notes_other = {}, [], collections.Counter(), {}, {}
    morph_prefix = collections.Counter()
    aramaic = []
    seg_total = collections.Counter()
    cur = None
    for i, chunk in enumerate(parts):
        m = re.match(r'<verse[^>]*osisID="(Ezek\.\d+\.\d+)"', chunk)
        if m:
            cur = m.group(1)
            continue
        if cur is None:
            continue
        body = chunk.split("</chapter")[0]
        for t in re.findall(r'<seg type="([^"]+)"', body):
            seg_total[t] += 1
            name = SEG_NAME.get(t, t)
            if name in ("SAMEKH", "PE", "REVERSED_NUN"):
                marks.setdefault(cur, []).append(name)
            elif name == "PASEQ":
                paseq.append(cur)
            elif name not in ("MAQQEF", "SOF_PASUQ"):
                other_segs[name] += 1
        # EVERY note, typed or not. An earlier build required a type= attribute and silently dropped the
        # untyped ones - which lost the OSHB editors' punctuation note at Ezek 33:20 ("We read punctuation in L
        # differently from BHS"), a single-witness divergence and exactly the kind of site a row must disclose.
        # It surfaced only because that verse also has no sof-pasuq and the 1272-vs-1273 arithmetic did not close.
        for attrs, txt in re.findall(r"<note\b([^>]*)>(.*?)</note>", body, re.S):
            typ = (re.search(r'type="([^"]*)"', attrs) or [None, ""])[1] if 'type="' in attrs else ""
            plain = re.sub(r"<[^>]+>", "", txt).strip()
            if "variant" in typ.lower():
                kq.setdefault(cur, []).append(plain[:200])
            else:
                notes_other.setdefault(cur, []).append(
                    {"type": typ or "(untyped)", "attrs": attrs.strip(), "text": plain[:200]})
        for p in re.findall(r'morph="([A-Za-z])', body):
            morph_prefix[p] += 1
        if 'morph="A' in body:
            aramaic.append(cur)

    out = {
        "book": BOOK,
        "witness": "WLC (OSHB) - single witness; disclose on every citation",
        "numbering": ("MT != WEB in the ch 20/21 zone (MT 21:1-5 = WEB 20:45-49; MT 21:6-37 = WEB 21:1-32); "
                      "identity in every other chapter. Byte-proven in web_mt_offset_map.json. EVERY ref in this "
                      "file is MT."),
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
                       "so an intra-verse POSITION claim is unsourceable from Ezek_oshb.txt and must be read from "
                       "the XML by exact path. Listed once per occurrence, so a verse may repeat."),
        "paseq_tally": {"occurrences": len(paseq), "verses": len(set(paseq))},
        "other_segs": dict(other_segs),
        "other_segs_note": "seg types beyond the paragraph marks, paseq, maqqef and sof-pasuq",
        "seg_totals_in_xml": dict(seg_total),
        "kq": kq,
        "kq_note": ("Ketiv/Qere: the written form and the read form. A K/Q verse is a TEXTUAL-VARIANT site; a row "
                    "whose span covers one discloses it, and a boundary is never argued from the Qere alone."),
        "kq_tally": {"verses": len(kq), "notes": sum(len(v) for v in kq.values())},
        "notes_other": notes_other,
        "notes_other_note": ("non-variant OSHB notes (exegesis, alternative readings, punctuation divergences); "
                             "single-witness, disclose. UNTYPED notes are captured too and marked '(untyped)'."),
        "arithmetic_anomalies_resolved": {
            "sof_pasuq_1272_for_1273_verses": {
                "verse": "Ezek.33.20",
                "finding": ("this verse carries no x-sof-pasuq seg. In its place the OSHB editors wrote an "
                            "untyped note, 'We read punctuation in L differently from BHS.', followed directly "
                            "by the x-pe paragraph mark."),
                "status": ("a real source fact, not a parsing gap. Recorded as a single-witness punctuation "
                           "divergence; a row spanning Ezek 33:20 (MT) discloses it, and no boundary is argued "
                           "from the absent sof-pasuq."),
            },
            "184_marks_on_183_verses": {
                "verse": "Ezek.43.27",
                "finding": "carries two consecutive x-samekh segs in the XML",
                "status": "counted as two occurrences on one verse; the tallies are occurrences, the verse count "
                          "is verses, and the two never add together",
            },
        },
        "morph_prefix_tally": dict(morph_prefix),
        "aramaic_verses": aramaic,
        "language_note": ("morph prefix H = Hebrew, A = Aramaic. Ezekiel is Hebrew throughout unless this list is "
                          "non-empty; an Aramaic island would be a Tier-0 disclosure like Jeremiah's MT 10:11."),
    }
    (SP / f"pmarks_{BOOK}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                            encoding="utf-8", newline="\n")
    print(json.dumps({"verses_with_marks": len(marks), "marks_tally": out["marks_tally"],
                      "paseq": out["paseq_tally"], "kq": out["kq_tally"],
                      "other_segs": out["other_segs"], "seg_totals_in_xml": out["seg_totals_in_xml"],
                      "morph_prefix": dict(morph_prefix), "aramaic_verses": aramaic,
                      "notes_other_verses": len(notes_other)}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
