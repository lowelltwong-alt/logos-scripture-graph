#!/usr/bin/env python3
"""The לכן-TURN MESSENGER ONSET CLASS: the evidence table #e16 needs to rule on three sites together.

THE ROUTED QUESTION. #e15 Q2 held a class question rather than deciding it per row: is a לכן-turn messenger
formula, standing with NO addressee change and NO verse-final close-role formula before it, a licensed onset (a
sub-onset the scale can rest a seam on) or a discourse turn inside one unit? Three rows depend on it and #e15
ordered them decided together in #e16: P03-012 at 17:19, the ch-20 site at 20:30, and P09-011 at 39:25. Its note
on P03-012 states the shape exactly: "the onset near face at 17:19 is a לכן-turn messenger formula with no
addressee change and no verse-final close before it - the class question routed at Q2; the grade holds at medium
pending that class decision."

WHAT THIS FILE IS. An evidence table, not a ruling. For each site it reports, from the pinned witnesses: the
verse's opening, the PRECEDING verse's ending and whether that ending is a close-role formula at the verse end,
the section marks standing on the preceding verse, both verses' inventory class memberships, and the row that
carries the seam with its current grade. #e16 decides; this makes the three comparable at a glance, which is
what a class decision needs and what three separate per-row readings could not give.

WHAT IT DOES NOT DECIDE, and why it says so. Whether the ADDRESSEE changes is a reading of the discourse, not a
byte test: the same hearers can be named by two titles, which is the precise ground on which #e15 overruled
P08-002's licence claim ("house of Israel" and "children of your people" are two titles for one audience). So
the addressee is reported as the title words each verse actually carries, MEASURED, with the identity question
left open and labelled. A table that resolved it by string comparison would be asserting the very thing the
class question asks.

THE FACES ARE NOT CROSSED. Each site is checked against the offset map's zone before any arithmetic: all three
sit outside WEB 20:45-49 / WEB ch 21 / MT ch 21, where the map declares identity numbering. Ch 20 is the zone's
own chapter, so 20:30 is verified individually rather than assumed from the chapter number.
"""
import hashlib
import json
import re
import unicodedata
from pathlib import Path

EZ = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking\M8_fable\sp_durable\Ezek")
HERE = Path(__file__).resolve().parent
OSHB = EZ / "Ezek_oshb.txt"
PM = EZ / "pmarks_Ezek.json"
INV = EZ / "ezek_device_inventory.v2.json"
ROWS = EZ / "repair" / "rows_v7_cwo24.jsonl"
OFF = EZ / "web_mt_offset_map.json"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()               # noqa: E731

text = {}
for line in OSHB.read_text(encoding="utf-8").splitlines():
    if "\t" not in line:
        continue
    ref, t = line.split("\t", 1)
    m = re.fullmatch(r"Ezek\.(\d+)\.(\d+)", ref)
    if m:
        text[(int(m.group(1)), int(m.group(2)))] = t.strip()

pm = json.loads(PM.read_text(encoding="utf-8"))
inv = json.loads(INV.read_text(encoding="utf-8"))
off = json.loads(OFF.read_text(encoding="utf-8"))
rows = [json.loads(l) for l in ROWS.read_text(encoding="utf-8").splitlines() if l.strip()]

ZONE_MT = {(21, v) for v in range(1, 38)}
ZONE_WEB = {(20, v) for v in range(45, 50)} | {(21, v) for v in range(1, 33)}


def bare(s):
    """Consonants only: accents and points removed, so a formula is matched on its skeleton."""
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if not unicodedata.combining(c) and c not in "\u05be\u05c0\u05c3\u05c6")


LAKHEN = "לכן"
MESSENGER = "כה אמר"                       # koh amar - the messenger formula's opening
CLOSE_FORMS = {
    "utterance of the Lord YHWH": "נאם אדני יהוה",
    "utterance of YHWH": "נאם יהוה",
    "I YHWH have spoken": "אני יהוה דברתי",
    "recognition (they/you shall know that I am YHWH)": "כי אני יהוה",
}
TITLES = {
    "house of Israel": "בית ישראל",
    "children of your people": "בני עמך",
    "son of man": "בן אדם",
    "mountains of Israel": "הרי ישראל",
    "Gog": "גוג",
    "the nations": "הגוים",
}


def classes_at(c, v):
    """Every inventory v2 class whose verse list names this MT verse."""
    found = []

    def walk(o, path):
        if isinstance(o, dict):
            for k, val in o.items():
                if isinstance(val, list) and val and all(isinstance(x, str) for x in val):
                    if ("Ezek.%d.%d" % (c, v)) in val or ("oshb:Ezek.%d.%d" % (c, v)) in val:
                        found.append((path + "/" + k).strip("/"))
                walk(val, path + "/" + str(k))
        elif isinstance(o, list):
            for i, val in enumerate(o):
                walk(val, "%s[%d]" % (path, i))
    walk(inv, "")
    return sorted(set(found))


def marks_on(c, v):
    m = pm.get("marks") or {}
    key = "Ezek.%d.%d" % (c, v)
    got = m.get(key)
    if got is None:
        return []
    return got if isinstance(got, list) else [got]


def row_for(c, v):
    """The row whose span contains this verse, by its OSIS endpoints."""
    out = []
    for r in rows:
        vs = re.findall(r"Ezek\.(\d+)\.(\d+)", str(r.get("span", "")))
        if not vs:
            continue
        a, b = (int(vs[0][0]), int(vs[0][1])), (int(vs[-1][0]), int(vs[-1][1]))
        if a <= (c, v) <= b:
            out.append({"row": r["decision_id"], "span": r.get("span"),
                        "confidence": r.get("confidence")})
    return out


# POSITIVE CONTROLS, run before the sites, because the finding at all three sites is a NEGATIVE - "no
# close-role formula in the preceding verse" - and a broken matcher produces the same negative. Each control is
# a measurement a ruling already made, so agreement proves the detector fires and disagreement would stop the
# run. This is the E-36 rule applied here: a check that found nothing must show what it can find.
CONTROLS = [((32, 16), "verse-final", "#e15 P07-008: 32:16 ends נאם אדני יהוה (verse-final)"),
            ((32, 32), "verse-final", "#e15 P07-008: 32:32 ends נאם אדני יהוה (verse-final)"),
            ((18, 9), "verse-final", "#e15 ch-18 table: 18:9 utterance VERSE-FINAL"),
            ((18, 23), "mid-verse", "#e15 ch-18 table: 18:23 utterance MID-verse, הלוא בשובו מדרכיו וחיה follows")]
controls, control_failures = [], []
for (c, v), want, src in CONTROLS:
    b = bare(text.get((c, v), ""))
    got, detail = "NONE", None
    for name, form in CLOSE_FORMS.items():
        pos = b.find(bare(form))
        if pos < 0:
            continue
        tail = b[pos + len(bare(form)):].strip()
        got = "verse-final" if not tail else "mid-verse"
        detail = {"formula": name, "words_after_it": len(tail.split()) if tail else 0}
    rec = {"verse": "oshb:Ezek.%d.%d" % (c, v), "the_ruling_measured": want, "this_detector_finds": got,
           "detail": detail, "source_of_the_expectation": src, "agrees": got == want}
    controls.append(rec)
    if not rec["agrees"]:
        control_failures.append(rec)
if control_failures:
    raise SystemExit("REFUSED: the close-formula detector disagrees with a measurement a ruling already made, "
                     "so its NEGATIVE findings at the three sites cannot be trusted: %r" % control_failures)

SITES = [(17, 19), (20, 30), (39, 25)]
report = []
for c, v in SITES:
    if (c, v) in ZONE_MT or (c, v) in ZONE_WEB:
        report.append({"site": "Ezek.%d.%d" % (c, v),
                       "REFUSED": ("this verse lies in the ch 20/21 zone, where WEB and MT do not number "
                                   "alike; it cannot be read as a single face and #e16 must be given the "
                                   "dual form")})
        continue
    onset, prev = text.get((c, v)), text.get((c, v - 1)) if v > 1 else None
    b_on, b_pv = bare(onset or ""), bare(prev or "")
    # does the PRECEDING verse END on a close-role formula? verse-final is the test, never mid-verse
    ends_on = []
    for name, form in CLOSE_FORMS.items():
        if not b_pv:
            continue
        pos = b_pv.find(bare(form))
        if pos < 0:
            continue
        tail = b_pv[pos + len(bare(form)):].strip()
        ends_on.append({"formula": name, "verse_final": tail == "",
                        "what_follows_it_in_the_verse": (prev[-len(tail) - 12:] if tail else ""),
                        "words_after_it": len(tail.split()) if tail else 0})
    report.append({
        "site": "Ezek.%d.%d" % (c, v),
        "numbering": ("outside the zone, so WEB and MT agree here by the offset map's identity rule"),
        "the_onset_verse": {
            "ref": "oshb:Ezek.%d.%d" % (c, v),
            "opening_words": " ".join((onset or "").split()[:7]),
            "opens_with_lakhen": b_on.startswith(LAKHEN),
            "carries_the_messenger_formula": bare(MESSENGER) in b_on,
            "messenger_at_word": (b_on.split().index(bare(MESSENGER).split()[0]) + 1
                                  if bare(MESSENGER).split()[0] in b_on.split() else None),
            "inventory_classes": classes_at(c, v),
            "titles_present": [n for n, t in TITLES.items() if bare(t) in b_on],
        },
        "the_verse_before": {
            "ref": "oshb:Ezek.%d.%d" % (c, v - 1),
            "closing_words": " ".join((prev or "").split()[-7:]),
            "close_role_formulae_found": ends_on,
            "ends_on_a_verse_final_close_role_formula": any(e["verse_final"] for e in ends_on),
            "marks_recorded_on_it": marks_on(c, v - 1),
            "inventory_classes": classes_at(c, v - 1),
            "titles_present": [n for n, t in TITLES.items() if bare(t) in b_pv],
        },
        "the_rows_that_carry_this_verse": row_for(c, v),
        "the_rows_that_carry_the_verse_before": row_for(c, v - 1),
    })

out = {
    "schema": "ezek_lakhen_onset_class.v1",
    "for": "#e16",
    "the_routed_question": (
        "is a לכן-turn messenger formula, with NO addressee change and NO verse-final close-role formula "
        "before it, a licensed onset the scale may rest a seam on, or a discourse turn inside one unit? #e15 Q2 "
        "held the class and ordered the three sites decided together."),
    "why_a_class_and_not_three_readings": (
        "the three rows carry the same shape at three places; deciding them one at a time is how the corpus "
        "ended up with one grade resting on a mark alone and another on a formula that stands mid-verse. A "
        "shared seam weighs the same from both sides, and a shared SHAPE should weigh the same at all three "
        "sites unless something distinguishes them - which this table is built to show."),
    "what_this_is_not": ("a ruling, and not an addressee analysis. Whether the addressee CHANGES is a reading "
                         "of the discourse, not a byte test: the same hearers can be named by two titles, "
                         "which is exactly the ground on which #e15 overruled P08-002's licence claim. The "
                         "titles each verse carries are reported MEASURED; their identity is left to #e16."),
    "the_cut_rule_limbs_this_bears_on": (
        "a messenger formula is a sub-onset when (a) the addressee changes, or (b) the verse immediately "
        "before ENDS on a close-role formula - verse-final, not mid-verse. A mark alone never satisfies limb "
        "(b). So limb (b) is decidable from the bytes and is measured here; limb (a) is not."),
    "inputs": {"oshb": OSHB.name, "oshb_sha256": sha(OSHB),
               "marks": PM.name, "marks_sha256": sha(PM),
               "census": INV.name, "census_sha256": sha(INV),
               "rows": ROWS.name, "rows_sha256": sha(ROWS),
               "offset_map_sha256": sha(OFF)},
    "note_on_mark_direction": "a mark is recorded ON the verse it FOLLOWS, which is how the marks below read",
    "positive_controls_for_the_close_formula_detector": {
        "why": ("the finding at all three sites is a NEGATIVE, and a broken matcher produces the same "
                "negative. Each control is a measurement a ruling already made; the run refuses if one "
                "disagrees."),
        "controls": controls,
        "all_agree": not control_failures,
    },
    "the_shape_the_three_sites_share": {
        "lakhen_plus_messenger_at_all_three": True,
        "limb_b_fails_at_all_three": ("MEASURED: 17:18 ends לא ימלט, 20:29 ends עד היום הזה, 39:24 ends "
                                      "ואסתר פני מהם - none is a close-role formula, verse-final or "
                                      "otherwise. #e15's own P09-011 ground says the same of 39:24, "
                                      "independently reproduced here."),
        "the_marks_differ": "a SAMEKH stands on 17:18 and on 39:24; nothing stands on 20:29",
        "and_a_mark_alone_never_satisfies_limb_b": "so the marks cannot rescue the licence at any site",
        "the_only_open_variable_is_limb_a": ("the addressee. 20:30 and 39:25 name בית ישראל in the onset "
                                             "verse; 17:19 names no title. Whether that is a CHANGE of "
                                             "addressee is the reading #e16 must make, and #e15's P08-002 "
                                             "holding is the nearest precedent: two titles for one audience "
                                             "inside one speech do not satisfy limb (a)."),
        "the_grades_these_rows_carry_today_are_not_uniform": ("P03-012 medium, P04-003 medium_low, P09-011 "
                                                              "medium - three grades on one shape, which is "
                                                              "the argument for a class ruling rather than "
                                                              "three readings"),
    },
    "WHAT_THIS_CLASS_DECISION_ACTUALLY_REACHES": {
        "measured": ("all three לכן verses are their row's FIRST verse, and in each case the preceding row "
                     "ends at the verse immediately before: 17:19 opens P03-012 where P03-011 ends at 17:18; "
                     "20:30 opens P04-003 where P04-002 ends at 20:29; 39:25 opens P09-011 where P09-010 ends "
                     "at 39:24."),
        "so_the_question_is_not_only_about_grades": (
            "these are three CUTS the corpus actually made. If a לכן-turn messenger formula with no addressee "
            "change and no verse-final close behind it is NOT a licensed onset, then three shipped seams rest "
            "on an unlicensed onset - which is a SPAN question in three places, not a confidence question. "
            "#e15 routed the class expecting it to settle grades; the measurement shows it reaches further."),
        "and_that_is_beyond_a_confidence_ruling": (
            "span questions in flagged regions are the OW-6b(b) second Fable review's business, and chs 17, "
            "20-21 and 38-39 are all named §7 regions. So the honest disposition is: #e16 decides the CLASS "
            "and the three grades; if it decides the turn is unlicensed, the three seams go to the OW-6b(b) "
            "review with this table as their input, exactly as the ch-18 tiling question was routed."),
        "the_nearest_precedent_cuts_against_the_licence": (
            "#e15 overruled P08-002's licence claim on the ground that two titles for one audience inside one "
            "speech do not satisfy limb (a), and it resolved that a mark-only close does NOT satisfy limb (b) "
            "(#e13 P09-011). Both limbs are what these three sites depend on, and both readings, applied here, "
            "point the same way - which is a reason for #e16 to be explicit rather than for me to anticipate "
            "it."),
        "tier": "the seam positions and the adjacent rows are MEASURED; the consequence for spans is INFERRED "
                "from the ruling's own limbs and is labelled as such",
    },
    "sites": report,
    "tier": "MEASURED: the bytes, the formula positions, the marks, the class memberships and the grades. The "
            "addressee question is left OPEN, not inferred.",
}
p = HERE / "lakhen_onset_class.v1.json"
p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
for s in report:
    if "REFUSED" in s:
        print("  %s  REFUSED: %s" % (s["site"], s["REFUSED"][:90]))
        continue
    o, b = s["the_onset_verse"], s["the_verse_before"]
    print("=== %s   rows: %s" % (s["site"], ", ".join("%s (%s)" % (r["row"], r["confidence"])
                                                      for r in s["the_rows_that_carry_this_verse"])))
    print("    lakhen=%-5s messenger=%-5s  titles=%s" % (o["opens_with_lakhen"],
                                                         o["carries_the_messenger_formula"],
                                                         o["titles_present"]))
    print("    before: verse-final close? %-5s  marks=%-14s titles=%s"
          % (b["ends_on_a_verse_final_close_role_formula"], b["marks_recorded_on_it"], b["titles_present"]))
    for e in b["close_role_formulae_found"]:
        print("        %-46s verse_final=%-5s words_after=%d"
              % (e["formula"], e["verse_final"], e["words_after_it"]))
print("\nwritten:", p.name, sha(p)[:16])
