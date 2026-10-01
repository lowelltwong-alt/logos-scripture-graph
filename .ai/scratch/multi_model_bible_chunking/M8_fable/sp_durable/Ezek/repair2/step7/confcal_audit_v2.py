#!/usr/bin/env python3
"""CONF-CAL AUDIT MEMBER, v2 - the read-only view #e15 Q2 ordered, built once the face vocabulary exists.

THE ORDER (#e15 q2_confcal_high_limb.order_confcal_audit_sweep): "A read-only member (distinct from the authors and
from the refs member) derives, for every row: own-seam faces from inventory v2 + pmarks + the verse-final test over
the witness; rivals from WARRANT-rival tokens and the verse anchors of strongest_rejected_alternative; the CONF-CAL
limb that follows; and lists every row whose carried grade disagrees with the derived limb, with the disagreeing face
named. NO grade is changed by the member. Its list is the #e16 docket."

WHY v1 WAS NOT THAT MEMBER. v1 (session archive) read faces off six-word ref annotations and said so: 76 of 145 rows
"disagreed", which measured the annotations, not the grades. v2 derives every own-seam face from the census and the
witness bytes, never from a row's prose or annotations; the row's refs contribute only its rival SEAM PAIRS.

WHAT IS MEASURED AND WHAT NEEDS A READER - each face carries its tier:
  MEASURED  class membership (inventory v2, distinct-checked); marks at a seam (pmarks, single witness); the
            verse-final test on the consonantal skeleton (the verse ENDS on the close-role phrase)
  READER    CUT-RULE limb (a) - an addressee change - for a messenger or son-of-man onset whose limb (b) fails;
            #e14 Q2's refinement - a close formula followed in its verse only by a DEPENDENT completion grades as
            verse-final - which the strict skeleton test cannot see, so a mid-verse close is reported MID_VERSE with
            that caveat rather than weak; a scene change without a transport verb; the division plan's own direction.
A reader-dependent face WIDENS the derived limb to a range instead of being guessed. THE CENSUS IS NOT EVERY LICENSED
SIGNAL: refrains outside the counted classes, discourse turns, scene changes and "he said to me" are invisible here, so
a grade above the range is a docket QUESTION with its basis named ("census absence on the near face 2:7"), never a
finding that the grade is wrong. Marks and mid-verse formulae make no face.

usage: python confcal_audit_v2.py [--rows <rows.jsonl>] [--out <json>]
       python confcal_audit_v2.py --selftest
"""
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
EZ = HERE.parent.parent
sys.path.insert(0, str(EZ / "tools"))
import ezek_lib as LIB                                                         # noqa: E402


def _arg(n, d=None):
    return sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d


ROWS = Path(_arg("--rows", str(EZ / "repair" / "rows_v7_cwo24.jsonl")))
OUT = Path(_arg("--out", str(HERE / "confcal_audit.v2.json")))
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731
ORDERV = {"low": 0, "medium_low": 1, "medium": 2, "high": 3}


def skel(t):
    t = unicodedata.normalize("NFD", t).replace("־", " ")
    return " ".join("".join(ch for ch in t if "א" <= ch <= "ת" or ch == " ").split())


WIT, ORDER = {}, []
for line in (EZ / "Ezek_oshb.txt").read_text(encoding="utf-8").splitlines():
    if "\t" in line:
        ref, text = line.split("\t", 1)
        c, v = (int(x) for x in ref.strip().split(".")[1:3])
        WIT[(c, v)] = skel(text)
        ORDER.append((c, v))
POS = {cv: i for i, cv in enumerate(ORDER)}
inv = json.loads((EZ / "ezek_device_inventory.v2.json").read_text(encoding="utf-8"))
F = inv["formulae"]


def verses(lst):
    return {tuple(int(x) for x in r.split(".")[1:3]) for r in lst}


ONSET_LICENSED = {
    "word-event formula": verses(F["word_event_formula"]["verses_mt"]) | verses(F["word_event_vayehi_any"]["verses_mt"])
                          | verses(F["word_event_hayah_any"]["verses_mt"]),
    "dateline": verses(inv["dated_oracles"]["verses_mt"]),
    "hand of YHWH": verses(F["hand_of_yhwh_upon_me"]["verses_mt"]),
    "set your face": verses(F["set_your_face"]["verses_mt"]),
    "transport": verses(inv["vision_transport"]["verses_mt"]),
}
ONSET_CUTRULE = {"messenger formula": verses(F["thus_says_the_lord_yhwh"]["verses_mt"]),
                 "son-of-man address": verses(F["son_of_man_address"]["verses_mt"])}
CLOSE = {"recognition": verses(F["recognition_family_64"]["verses_mt"]) | verses(F["recognition_formula"]["verses_mt"])
                        | verses(F["recognition_formula_2s"]["verses_mt"]) | verses(F["recognition_formula_2mp"]["verses_mt"])
                        | verses(F["recognition_formula_2fp"]["verses_mt"]) | verses(F["recognition_formula_adonai_variant"]["verses_mt"]),
         "utterance": verses(F["utterance_of_the_lord_yhwh"]["verses_mt"]) | verses(F["utterance_short_yhwh"]["verses_mt"]),
         "I YHWH have spoken": verses(F["i_am_yhwh_spoken"]["verses_mt"])}
FINAL = re.compile(r"(?:אני (?:אדני )?יהוה|אני יהוה דברתי(?: ועשיתי| ועשיתיו| בקנאתי)?|נאם (?:אדני )?יהוה)$")
pm = LIB.load_pmarks()


def marks_at(cv):
    ref = "Ezek.%d.%d" % cv
    out = []
    for key in ("marks", "section_marks"):
        m = pm.get(key)
        if isinstance(m, dict) and ref in m:
            out.append(m[ref])
    return out


def close_signal(cv):
    classes = [k for k, s in CLOSE.items() if cv in s]
    if not classes:
        return {"signal": "none"}
    if FINAL.search(WIT.get(cv, "")):
        return {"signal": "close", "classes": classes, "verse_final": "VERSE_FINAL", "tier": "MEASURED"}
    return {"signal": "mid_verse_close", "classes": classes, "verse_final": "MID_VERSE",
            "tier": "MEASURED strictly; READER - #e14 Q2's dependent-completion refinement may make it verse-final in effect"}


def onset_signal(cv, before):
    lic = [k for k, s in ONSET_LICENSED.items() if cv in s]
    if lic:
        return {"signal": "licensed", "classes": lic, "tier": "MEASURED"}
    cut = [k for k, s in ONSET_CUTRULE.items() if cv in s]
    if not cut:
        return {"signal": "none"}
    if before is not None and close_signal(before).get("verse_final") == "VERSE_FINAL":
        return {"signal": "licensed", "classes": cut, "licence": "CUT-RULE limb (b): the verse before ends verse-final on a close-role formula",
                "tier": "MEASURED"}
    return {"signal": "reader", "classes": cut, "licence": "limb (b) fails on the bytes; limb (a), an addressee change, needs a reader",
            "tier": "READER"}


def prev_cv(cv):
    i = POS[cv]
    return ORDER[i - 1] if i > 0 else None


def next_cv(cv):
    i = POS[cv]
    return ORDER[i + 1] if i + 1 < len(ORDER) else None


def to_mt(c, v):
    m = LIB.web_to_mt(c, v)
    return tuple(m) if m else (c, v)


def seam(near_kind, near_cv, far_cv, row_first_or_last):
    if near_kind == "onset":
        near = onset_signal(near_cv, far_cv)
        far = {"signal": "BOOK_EDGE"} if far_cv is None else close_signal(far_cv)
        if far.get("signal") == "none" and far_cv is not None:
            o = onset_signal(far_cv, prev_cv(far_cv))
            far = o if o["signal"] == "licensed" else far
    else:
        near = close_signal(near_cv)
        far = {"signal": "BOOK_EDGE"} if far_cv is None else onset_signal(far_cv, near_cv)
    def cls(sig):
        return {"licensed": "L", "close": "L", "BOOK_EDGE": "L", "mid_verse_close": "W", "reader": "R"}.get(sig.get("signal"), "N")
    n, f = cls(near), cls(far)
    # the scale's limbs, face by face; every combination the scale does not place is named, never forced
    if n == "L":
        state = {"L": "TWO_FACED", "N": "NEAR_ONLY"}.get(f, "READER_FAR")
    elif n == "W":
        state = "WEAK_NEAR" if f == "N" else "READER_NEAR_REFINEMENT"
    elif n == "R":
        state = "READER_NEAR_LIMB_A"
    else:
        state = "FAR_ONLY" if f != "N" else "NO_SIGNAL"
    return {"near_class": n, "far_class": f, "near": dict(near, verse_mt="%d:%d" % near_cv),
            "far": dict(far, verse_mt=("%d:%d" % far_cv) if far_cv else None),
            "marks_near": marks_at(near_cv), "marks_far": marks_at(far_cv) if far_cv else [], "state": state}


PAIR = re.compile(r"(?<![\d.:])(\d{1,2})[.:](\d{1,3})/(\d{1,2})[.:](\d{1,3})(?![\d])")


def audit_row(r):
    m = re.match(r"Ezek\.(\d+)\.(\d+)-Ezek\.(\d+)\.(\d+)$", r["span"])
    first, last = to_mt(int(m.group(1)), int(m.group(2))), to_mt(int(m.group(3)), int(m.group(4)))
    onset = seam("onset", first, prev_cv(first), first)
    close = seam("close", last, next_cv(last), last)
    rivals, unpaired = {}, []
    for e in r.get("boundary_evidence_refs") or []:
        if "[WARRANT-rival" not in e:
            continue
        note = e.split("]", 1)[1].strip()
        pm_ = PAIR.match(note)
        if pm_:
            rivals.setdefault((to_mt(int(pm_.group(1)), int(pm_.group(2))), to_mt(int(pm_.group(3)), int(pm_.group(4)))), set()).add("token")
        else:
            unpaired.append(e)
    for pm_ in PAIR.finditer(r.get("strongest_rejected_alternative") or ""):
        a = to_mt(int(pm_.group(1)), int(pm_.group(2)))
        b = to_mt(int(pm_.group(3)), int(pm_.group(4)))
        rivals.setdefault((a, b), set()).add("rejected-alternative prose")
    rv = []
    for (a, b), src in sorted(rivals.items()):
        if a not in POS or b not in POS or POS[b] != POS[a] + 1:
            rv.append({"seam": "%d:%d/%d:%d" % (a + b), "from": sorted(src), "state": "NOT_ADJACENT_OR_UNKNOWN"})
            continue
        if not (POS[first] < POS[b] <= POS[last]):
            rv.append({"seam": "%d:%d/%d:%d" % (a + b), "from": sorted(src), "state": "OUTSIDE_THE_SPAN (an own seam or a merge)"})
            continue
        o = onset_signal(b, a)
        c = close_signal(a)
        st = ("TWO_FACED" if o["signal"] == "licensed" and c.get("verse_final") == "VERSE_FINAL" else
              "LICENSED" if o["signal"] == "licensed" else "READER" if o["signal"] == "reader" else "UNLICENSED")
        rv.append({"seam": "%d:%d/%d:%d" % (a + b), "from": sorted(src), "onset_side": o, "close_side": c, "state": st})
    bars_high = [x for x in rv if x["state"] in ("TWO_FACED", "LICENSED")]
    reader_rivals = [x for x in rv if x["state"] == "READER"]
    L, ML, M, H = 0, 1, 2, 3
    # each seam state maps to the RANGE of limbs the scale's words allow; a reader-dependent face widens the range
    # rather than being guessed. NO_SIGNAL reaches medium_low because a discourse turn without a formula and a region
    # the division plan holds are both medium_low and both invisible to this member. FAR_ONLY is capped below medium
    # because MEDIUM and HIGH both require a licensed near-face signal on each seam; low or medium_low is a reader's call.
    RANGE = {"TWO_FACED": (H, H), "NEAR_ONLY": (M, M), "WEAK_NEAR": (ML, ML), "NO_SIGNAL": (L, ML), "FAR_ONLY": (L, ML),
             "READER_FAR": (M, H), "READER_NEAR_REFINEMENT": (ML, H)}

    def seam_range(s):
        if s["state"] != "READER_NEAR_LIMB_A":
            return RANGE[s["state"]]
        licensed_max = {"L": H, "N": M}.get(s["far_class"], H)
        licensed_min = {"L": H, "N": M}.get(s["far_class"], M)
        return (L, max(licensed_max, ML)) if licensed_min else (L, licensed_max)

    ranges = [seam_range(onset), seam_range(close)]
    lo, hi = min(x[0] for x in ranges), min(x[1] for x in ranges)
    if bars_high:
        hi, lo = min(hi, M), min(lo, M)
    if (reader_rivals or unpaired) and hi == H:
        lo = min(lo, M)
    names = ["low", "medium_low", "medium", "high"]
    grade = str(r.get("confidence"))
    if grade not in ORDERV:
        state = "UNDERDETERMINED"
    elif ORDERV[grade] > hi:
        state = "GRADE_ABOVE_DERIVED"
    elif ORDERV[grade] < lo:
        state = "GRADE_BELOW_DERIVED"
    else:
        state = "CONSISTENT" if lo == hi else "WITHIN_READER_RANGE"
    capping = [("onset seam", onset), ("close seam", close)]
    disagreeing = []
    def basis(s):
        if s["state"] in ("FAR_ONLY", "NO_SIGNAL"):
            return ("CENSUS ABSENCE on the near face %s: the census records no licensed onset or close there; a reader must "
                    "name a signal the census does not list (a refrain, a discourse turn, a scene change, 'he said to me') "
                    "or the grade exceeds its evidence" % s["near"].get("verse_mt"))
        if s["state"] == "NEAR_ONLY":
            return ("CENSUS ABSENCE on the far face %s: a reader must name a far-face signal the census does not list, "
                    "or the seam is one-faced" % s["far"].get("verse_mt"))
        if s["state"] == "WEAK_NEAR":
            return ("STRICT VERSE-FINAL TEST at %s: the close formula is not verse-final on the skeleton; #e14 Q2's "
                    "dependent-completion refinement, which a reader applies, may lift it" % s["near"].get("verse_mt"))
        return "reader-dependent face"

    if state == "GRADE_ABOVE_DERIVED":
        disagreeing = [{"face": "%s %s" % (n, s["state"]), "caps_at": names[seam_range(s)[1]], "basis": basis(s)}
                       for n, s in capping if seam_range(s)[1] < ORDERV[grade]] + \
                      [{"face": "rival %s %s" % (x["seam"], x["state"]), "caps_at": "medium",
                        "basis": "MEASURED: the rival's onset side carries a licensed signal (a rival that is licensed or two-faced bars high)"}
                       for x in bars_high if ORDERV[grade] > M]
    elif state == "GRADE_BELOW_DERIVED":
        disagreeing = [{"face": "%s %s" % (n, s["state"]), "at_least": names[seam_range(s)[0]],
                        "basis": "MEASURED PRESENCE of census signals; a grade may still be held below by a stated reason "
                                 "(the division plan's direction, a guard) and no grade is raised unasked"} for n, s in capping]
    return {"row": r["decision_id"], "span_web": r["span"], "span_mt": "%d:%d-%d:%d" % (first + last), "grade": grade,
            "derived_range": [names[lo], names[hi]], "state": state, "disagreeing_faces": disagreeing,
            "onset_seam": onset, "close_seam": close, "rivals": rv, "unpaired_rival_tokens": unpaired,
            "reader_needed": [n for n, s in capping if s["state"] in ("READER_FAR", "READER_NEAR_REFINEMENT", "READER_NEAR_LIMB_A", "FAR_ONLY", "NO_SIGNAL")]
                             + ["rival " + x["seam"] for x in reader_rivals] + (["unpaired rival tokens"] if unpaired else [])}


def selftest():
    cases = [
        ("13:14 recognition is VERSE_FINAL", close_signal((13, 14)).get("verse_final") == "VERSE_FINAL"),
        ("29:9 recognition is MID_VERSE (the #e14 Q2 weak shape)", close_signal((29, 9)).get("verse_final") == "MID_VERSE"),
        ("36:23 is MID_VERSE on the strict test, with the refinement caveat", "READER" in close_signal((36, 23)).get("tier", "")),
        ("6:1 word-event onset is licensed", onset_signal((6, 1), (5, 17))["signal"] == "licensed"),
        ("a verse with no class is no signal", onset_signal((1, 5), (1, 4))["signal"] == "none" and close_signal((1, 5))["signal"] == "none"),
        ("zone: WEB 20:45 is MT 21:1", to_mt(20, 45) == (21, 1)),
        ("the witness is on MT numbering (21:37 exists, 20:49 does not)", (21, 37) in POS and (20, 49) not in POS),
        ("census sets are non-empty (E-36)", all(ONSET_LICENSED.values()) and all(CLOSE.values()) and all(ONSET_CUTRULE.values())),
    ]
    failed = [n for n, ok in cases if not ok]
    print(json.dumps({"selftest_cases": len(cases), "failed": failed}, indent=1))
    return 1 if failed else 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    if selftest():
        raise SystemExit("REFUSED: selftest failed (E-36)")
    rows = [json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip()]
    out_rows = [audit_row(r) for r in rows]
    if len(out_rows) != 145:
        raise SystemExit("REFUSED: audited %d rows, expected 145" % len(out_rows))
    tally = Counter(x["state"] for x in out_rows)
    seam_states = Counter(s for x in out_rows for s in (x["onset_seam"]["state"], x["close_seam"]["state"]))
    out = {"schema": "ezek_confcal_audit.v2", "order": "#e15 q2_confcal_high_limb.order_confcal_audit_sweep",
           "inputs": {"rows": str(ROWS), "rows_sha256": sha(ROWS), "inventory_sha256": sha(EZ / "ezek_device_inventory.v2.json"),
                      "witness_sha256": sha(EZ / "Ezek_oshb.txt")},
           "what_this_is_not": "a verdict and never a grade change; #e16 rules",
           "tiers": "class membership, marks and the strict verse-final test are MEASURED; CUT-RULE limb (a), the #e14 Q2 "
                    "dependent-completion refinement, scene change without a transport verb and the division plan's direction "
                    "are READER, and a limb that turns on one is UNDERDETERMINED",
           "tally": dict(tally), "seam_states": dict(seam_states),
           "rows_for_e16": [x for x in out_rows if x["state"] in ("GRADE_ABOVE_DERIVED", "GRADE_BELOW_DERIVED")],
           "rows_needing_a_reader": [{"row": x["row"], "grade": x["grade"], "reader_needed": x["reader_needed"]} for x in out_rows if x["state"] == "WITHIN_READER_RANGE"],
           "all": out_rows}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    print(json.dumps({"rows_audited": len(out_rows), "tally": dict(tally), "seam_states": dict(seam_states),
                      "rows_for_e16": len(out["rows_for_e16"]), "out": str(OUT), "sha256": sha(OUT)}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
