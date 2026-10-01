#!/usr/bin/env python3
"""REPAIR-2 step 3: the DISTINCT CHECK #e15 Q10 requires before any measured-false item becomes a repair.

#e15 Q10: "Each such finding becomes a REPAIR-2 item after a DISTINCT CHECK (the fact reproduced from the pinned
input by a self-contained script, C1 shape from #e14 Q3) - a finding that does not reproduce is a STOP for that
item, never a fallback to the reviewer's wording."

So every function below reads ONLY pinned inputs - the Hebrew witness, the English version, the marks record and
the device census - and never the rows and never a reviewer's text. Each returns what it MEASURED, and the verdict
REPRODUCES or DOES NOT REPRODUCE. Whether the false claim still stands in the ROW is a separate question, measured
against the rows after step 2 lands; this file settles only whether the fact behind each item is true.

A negative fact runs a positive control on the same reader (E-36): "no paseq in 8:14-18" is only evidence if the same
reader finds the paseq it should find at 8:1.
"""
import hashlib
import json
import sys
import unicodedata
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
PM, INV = EZ / "pmarks_Ezek.json", EZ / "ezek_device_inventory.v2.json"
OSHB, WEB = EZ / "Ezek_oshb.txt", EZ / "Ezek_web_clean.txt"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731

pm = json.loads(PM.read_text(encoding="utf-8"))
inv = json.loads(INV.read_text(encoding="utf-8"))


def read_tsv(p):
    out = {}
    for line in Path(p).read_text(encoding="utf-8").splitlines():
        if "\t" in line:
            k, t = line.split("\t", 1)
            out[k.strip()] = t.strip()
    return out


oshb = read_tsv(OSHB)
# THE ENGLISH VERSION IS READ THROUGH THE TOOLKIT'S OWN VERSE MAP. My first version parsed Ezek_web_clean.txt as
# tab-separated; it is a formatted text ("===== EZEK N =====", "[v] N ..."), so every WEB lookup came back EMPTY and
# item 2 reported a STOP on a true fact. load_verse_maps() returns (web, oshb) - WEB FIRST - and its "clean" field
# is the verse text without footnote marks.
sys.path.insert(0, str(EZ / "tools"))
import ezek_lib as LIB                                                         # noqa: E402
web = {k: v.get("clean", "") for k, v in LIB.load_verse_maps()[0].items()}


def bare(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if not unicodedata.combining(c) and c not in "\u05be\u05c0\u05c3\u05c6")


def cls(path):
    o = inv
    for k in path.split("/"):
        o = o[k]
    return list(o)


def V(c, v):
    return "Ezek.%d.%d" % (c, v)


def vkey(ref):
    """Numeric sort key for 'Ezek.C.V'. My first version sorted verse strings LEXICALLY, so 'Ezek.8.10' came before
    'Ezek.8.3' and two TRUE facts (items 1 and 13) were reported as STOPs."""
    _, c, v = ref.split(".")
    return (int(c), int(v))


def marks_in(ch):
    return {k: v for k, v in pm["marks"].items() if k.startswith("Ezek.%d." % ch)}


R = []


def item(n, row, claim, measured, reproduces, control=None):
    R.append({"item": n, "row": row, "claim_under_test": claim, "measured": measured,
              "positive_control": control, "verdict": "REPRODUCES" if reproduces else "DOES NOT REPRODUCE - STOP"})


# 1  P02-003: paseq in ch 8 = 8:1, 8:3, 8:6, 8:10; none in 8:14-18; a samekh on 8:14
p8 = sorted((v for v in pm["paseq"] if v.startswith("Ezek.8.")), key=vkey)
in_span = [v for v in p8 if 14 <= int(v.split(".")[2]) <= 18]
m814 = pm["marks"].get(V(8, 14))
item(1, "P02-003", "no paseq falls in 8:14-18; the only Masoretic item in the span is the samekh on 8:14",
     {"paseq_in_ch8": p8, "paseq_in_8_14_18": in_span, "marks_on_8_14": m814,
      "kq_in_8_14_18": [k for k in pm["kq"] if k.startswith("Ezek.8.") and 14 <= int(k.split(".")[2]) <= 18]},
     not in_span and m814 == ["SAMEKH"] and p8 == [V(8, 1), V(8, 3), V(8, 6), V(8, 10)],
     control={"the reader finds a paseq at 8:1": V(8, 1) in pm["paseq"]})

# 2  P03-019: the 18:29 note AGREES with BHS; the WEB 18:30 gloss extends to "says the Lord Yahweh"
n1829 = pm["notes_other"].get(V(18, 29)) or []
txt = " ".join(x.get("text", "") for x in n1829)
w1830 = web.get(V(18, 30), "")
item(2, "P03-019", "the 18:29 note is an AGREEMENT note ('same form as BHS'), not a note against BHS; and WEB 18:30 "
                   "carries 'says the Lord Yahweh', so a gloss of the utterance must extend to it",
     {"notes_other_18_29": txt, "web_18_30": w1830},
     ("same form as BHS" in txt) and ("says the Lord Yahweh" in w1830))

# 3  P08-012: strict word-event members from 33:1 = 33:1, 33:23, 34:1, 35:1, 36:16, 37:15, 38:1
we = cls("formulae/word_event_formula/verses_mt")
after = [v for v in we if (int(v.split(".")[1]), int(v.split(".")[2])) >= (33, 1)
         and (int(v.split(".")[1]), int(v.split(".")[2])) <= (38, 1)]
item(3, "P08-012", "36:16 is the FIFTH strict word-event seam from 33:1 (33:1, 33:23, 34:1, 35:1, 36:16), and 37:15 "
                   "and 38:1 follow",
     {"strict_word_event_33_1_to_38_1": after,
      "ordinal_of_36_16": (after.index(V(36, 16)) + 1) if V(36, 16) in after else None},
     after == [V(33, 1), V(33, 23), V(34, 1), V(35, 1), V(36, 16), V(37, 15), V(38, 1)])

# 4  P07-008: MT 32:17 names no MONTH ordinal (the day is the fifteenth "of the month")
t3217 = bare(oshb.get(V(32, 17), ""))
MONTHS = ["בראשון", "בשני", "בשלישי", "ברביעי", "בחמישי", "בששי", "בשביעי", "בשמיני", "בתשיעי", "בעשירי",
          "בעשתי עשר חדש", "בשנים עשר חדש", "בשני עשר חדש"]
found = [m for m in MONTHS if bare(m) in t3217]
item(4, "P07-008", "MT 32:17 names no month; a twelfth-month reading can only be INFERRED from 32:1",
     {"mt_32_17_consonants_head": " ".join(t3217.split()[:9]), "month_ordinal_terms_found": found,
      "mt_32_1_head": " ".join(bare(oshb.get(V(32, 1), "")).split()[:9])},
     not found and "לחדש" in t3217,
     control={"the same month-term reader finds a month in 32:1": bool([m for m in MONTHS
                                                                       if bare(m) in bare(oshb.get(V(32, 1), ""))])})

# 5  P06-001: MT 21:33 addresses Ammon, and it is a set-your-face-class context in the collection
t2133 = bare(oshb.get(V(21, 33), ""))
syf = cls("formulae/set_your_face/verses_mt")
item(5, "P06-001", "MT 21:33 (= WEB 21:28) addresses the children of Ammon, so 25:1-7 is not the book's first "
                   "foreign addressee; the set-your-face class has 9 verses",
     {"mt_21_33_names_ammon": "בני עמון" in t2133, "set_your_face_verses": syf},
     "בני עמון" in t2133 and len(syf) == 9)

# 6  P02-008: PE recorded on 11:1 (so it divides 11:1/11:2, interior); chapter 10 carries no mark
item(6, "P02-008", "the pe on 11:1 is interior to 10:18-11:13 and chapter 10 carries no mark at all",
     {"marks_on_11_1": pm["marks"].get(V(11, 1)), "marks_in_ch10": marks_in(10)},
     pm["marks"].get(V(11, 1)) == ["PE"] and not marks_in(10),
     control={"the reader finds marks in ch 11": sorted(marks_in(11))})

# 7  P09-010: marks in ch 39 only at 39:10, 39:16, 39:24, 39:29; none at 39:20; 39:23 in no class; 39:20 ends utterance
all_lists = []


def collect(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "verses_mt" and isinstance(v, list):
                all_lists.append((path, v))
            else:
                collect(v, path + "/" + k)


collect(inv)
cls_3923 = [p for p, v in all_lists if V(39, 23) in v]
t3920 = bare(oshb.get(V(39, 20), ""))
item(7, "P09-010", "no mark stands on 39:20; MT 39:23 is in no census class; 39:20 ends on the utterance formula",
     {"marks_in_ch39": sorted(marks_in(39), key=vkey), "classes_containing_39_23": cls_3923,
      "mt_39_20_tail": " ".join(t3920.split()[-3:])},
     sorted(marks_in(39), key=vkey) == [V(39, 10), V(39, 16), V(39, 24), V(39, 29)] and not cls_3923
     and t3920.endswith("נאם אדני יהוה"))

# 8  P08-007: the K/Q entries at 35:9 and 35:12 - count the "/" separators
k359, k3512 = pm["kq"].get(V(35, 9)), pm["kq"].get(V(35, 12))
seps = {k: [e.count("/") for e in (v or [])] for k, v in ((V(35, 9), k359), (V(35, 12), k3512))}
item(8, "P08-007", "the K/Q entries at 35:9 and 35:12 carry ZERO separators, so 'with its separators stripped' "
                   "describes nothing",
     {"kq_35_9": k359, "kq_35_12": k3512, "separator_counts": seps,
      "reference_entry_with_separators": {V(1, 8): pm["kq"].get(V(1, 8))}},
     all(c == 0 for v in seps.values() for c in v) and bool(k359) and bool(k3512),
     control={"the counter finds separators in the 1:8 entry": [e.count("/") for e in pm["kq"].get(V(1, 8), [])]})

# 9  P02-018: recognition_formula_2fp counts exactly 13:21 and 13:23
r2fp = cls("formulae/recognition_formula_2fp/verses_mt")
item(9, "P02-018", "the 2fp recognition clauses are COUNTED - the census class holds exactly 13:21 and 13:23",
     {"recognition_formula_2fp": r2fp}, r2fp == [V(13, 21), V(13, 23)])

# 10 P10-014: no K/Q at 43:15; two notes_other at 43:15; K/Q at 43:16
item(10, "P10-014", "43:15 is not a K/Q verse (it carries two other notes); the span's K/Q verse is 43:16",
     {"kq_43_15": pm["kq"].get(V(43, 15)), "notes_other_43_15_count": len(pm["notes_other"].get(V(43, 15)) or []),
      "kq_43_16": pm["kq"].get(V(43, 16))},
     pm["kq"].get(V(43, 15)) is None and len(pm["notes_other"].get(V(43, 15)) or []) == 2
     and pm["kq"].get(V(43, 16)) is not None)

# 11 P11-007: a K/Q note stands on 46:15
item(11, "P11-007", "a K/Q note stands on the row's close verse 46:15",
     {"kq_46_15": pm["kq"].get(V(46, 15))}, pm["kq"].get(V(46, 15)) is not None)

# 12 transport class size
tr = cls("vision_transport/verses_mt")
item(12, "P02-001 and any row stating 'transport ... 20 verses'", "the transport class is 33 verses (46 occurrences); "
     "the strategy's closed 20 is a subset", {"transport_verses": len(tr),
     "strategy_list": len(cls("vision_transport/relation_to_the_strategy_closed_20/strategy_list"))},
     len(tr) == 33)

# 13 P06-005: marks at 26:6, 26:14, 26:18, 26:21
item(13, "P06-005", "chapter 26 carries marks at 26:6, 26:14, 26:18 and 26:21 - four marked units",
     {"marks_in_ch26": marks_in(26)}, sorted(marks_in(26), key=vkey) == [V(26, 6), V(26, 14), V(26, 18), V(26, 21)])

out = {
    "schema": "ezek_repair2_step3_distinct_checks.v1",
    "order": "#e15 Q10 - every measured-false finding is distinct-checked from the pinned input before it becomes a "
             "repair; a finding that does not reproduce is a STOP",
    "inputs": {"pmarks_sha256": sha(PM), "inventory_v2_sha256": sha(INV), "oshb_sha256": sha(OSHB),
               "web_sha256": sha(WEB)},
    "checked_here": len(R),
    "three_defects_in_this_check_fixed_before_its_verdict_was_trusted": [
        "verse lists were sorted as STRINGS, so Ezek.8.10 preceded Ezek.8.3 and items 1 and 13 read as STOPs on facts "
        "that are true",
        "the English version was parsed as tab-separated text, which it is not, so every WEB lookup was empty and item "
        "2 read as a STOP; it is now read through the toolkit's own verse map",
        "each STOP was examined against its MEASURED values before being recorded - the reviewer's fact was the last "
        "suspect, not the first"],
    "not_checked_here_and_why": {
        "14": "near/far inversions and WEB-faced MT devices (X2) - a refs-and-prose property measured on the ROWS "
              "after step 2, and the re-face half is step 4's mechanical sweep",
        "15": "three truncated quotations - measured against the ROWS' quoted text after step 2",
        "16": "lane 02's four out-of-worklist defects - named in that lane's escalations, to be extracted and each "
              "distinct-checked the same way",
        "17": "the 1-based inclusive digit convention - a property of row prose, measured after step 2"},
    "results": R,
    "tally": {"REPRODUCES": sum(1 for r in R if r["verdict"] == "REPRODUCES"),
              "STOP": sum(1 for r in R if r["verdict"] != "REPRODUCES")},
    "tier": "MEASURED from pinned inputs only; no row text and no reviewer wording was read",
}
p = Path(__file__).resolve().parent / "distinct_checks_q10.v1.json"
p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
print(json.dumps(out["tally"]))
for r in R:
    print("  %-3s %-9s %-26s %s" % (r["item"], r["row"][:9], r["verdict"][:26],
                                   json.dumps(r["positive_control"], ensure_ascii=False)[:70] if r["positive_control"] else ""))
