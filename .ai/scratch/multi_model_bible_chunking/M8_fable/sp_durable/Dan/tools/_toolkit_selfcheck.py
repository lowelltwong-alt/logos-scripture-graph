#!/usr/bin/env python3
"""Verify Daniel's Phase 0 artifacts against their bytes, against one another and against their Ezekiel counterparts,
and every factual claim in TOOLKIT.md against those artifacts.

WHY. The toolkit is the one document every lane reads and none of them re-derives, so a wrong number in it reaches
every brief and every row as though it were established. Daniel's Phase 0 was ported from Ezekiel's, and E-61 showed
that a port made from the predecessor's stage script silently drops what its FINAL artifacts carry. So this file:

1. audits file-set and top-level key parity two ways against Ezekiel's final artifacts. Every difference must be
   declared below with its reason. An undeclared difference fails, and so does a declaration that no longer matches a
   difference;
2. asserts the faces: verse_inventory.json is on the WEB face and the device inventory on the MT face;
3. re-derives the WEB/MT alignment from the two extracts' verse order and holds the offset map and the OSHB KJV-variance
   layer to it;
4. checks that no Daniel tool binds to an Ezekiel-only key;
5. runs E-65's floor: no Ezekiel-only integer fact in a Daniel string. It is a FLOOR, not a proof, because a list
   cannot show that no predecessor fact survived. The review lanes still owe E-65's item;
6. checks TOOLKIT.md's refs and pinned numbers against the artifacts. --artifacts-only skips this section, and the
   output then says the verdict covers only the artifacts.

Read-only. Exit 1 on any failure.
"""
import ast
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
BK = HERE.parent
EZ = BK.parent / "Ezek"
TK = HERE / "TOOLKIT.md"
EZ_TK = EZ / "tools" / "TOOLKIT.md"

# ---- declarations: every Daniel/Ezekiel difference, with its reason (E-61) ------------------------------------------

FILE_ABSENT = {  # an Ezekiel Phase 0 data file with no Daniel file of the same role
    "ezek_kjv_variance_crosscheck.json":
        "Daniel keeps this corroboration inside web_mt_offset_map.json (kjv_variance_crosscheck) with the raw OSHB "
        "layer in pmarks_Dan.json (kjv_variance); both are held to the byte alignment in section 3",
}
FILE_ADDED = {  # a Daniel Phase 0 file with no Ezekiel file of the same role
    "dan_language_zones.json": "Ezekiel is Hebrew throughout and has no Aramaic, so it has no zone map",
    "strategy_plan_Dan.json": "the machine-readable strategy plan beside book_strategy_Dan.md, checked by "
                              "_validate_strategy_dan.py; Ezekiel's strategy was markdown only",
}
KEYS = {  # file -> (Ezekiel-only keys, Daniel-only keys), each with its reason
    "web_mt_offset_map.json": (
        {"content_anchors": "hand transliterations that no tool reads; Daniel's evidence for the same need is "
                            "kjv_variance_crosscheck plus zone_pairs, and the authoring brief must name those (E-61 "
                            "correction)"},
        {"kjv_variance_crosscheck": "the OSHB KJV-variance corroboration, kept in the map instead of a separate file",
         "numbering_face": "the map states the campaign's row face"}),
    "pmarks_Dan.json": (
        {"aramaic_verses": "re-scoped as verses_with_any_aramaic_morph_including_notes; Ezekiel's list is empty",
         "morph_prefix_tally": "re-scoped as morph_prefix_tally_including_note_words, which counts note words",
         "arithmetic_anomalies_resolved": "Daniel has no anomaly to resolve; its computed facts are under arithmetic"},
        {"arithmetic": "the computed sof-pasuq and multi-mark facts, both empty for Daniel",
         "kjv_variance": "the raw OSHB KJV-variance layer keyed MT to English",
         "kjv_variance_note": "the provenance note for kjv_variance",
         "morph_prefix_tally_including_note_words": "re-scoped book fact: counts note words (E-61)",
         "source": "the OSHB source path and sha256",
         "verses_with_any_aramaic_morph_including_notes": "re-scoped book fact: counts note words (E-61)"}),
    "dan_stage_report.json": ({}, {"language": "the per-language summary; Ezekiel has one language"}),
    "verse_inventory.json": ({}, {}),
    "web_mt_verse_check.json": ({}, {}),
}
# The device inventory declares its Ezekiel-only keys in its own ezek_key_crosswalk; its Daniel-only keys are here.
DEV_ADDED = {
    "attribution": "the attribution terms of both witnesses, which travel with any quotation",
    "citation_sweep_constants": "the calendar-pair constants citation_sweep.py needs for Daniel, with their face",
    "date_family_patterns": "the year, month and day patterns per language, substring and anchored",
    "ezek_key_crosswalk": "this crosswalk itself: every Ezekiel key's Daniel disposition",
    "for_fable_end_review": "items held for Fable's end-of-campaign review (OW-28)",
    "inputs": "the sha256 of every input the inventory was built from",
    "language_switches": "the Hebrew/Aramaic switch points; Ezekiel has none",
    "month_or_day_substring_artifacts": "verses hit only by the month/day substring reading, recorded as non-dates",
    "month_or_day_word_not_a_date": "month or day words outside any dateline or calendar date",
    "numbering_face": "the inventory's declared face (MT)",
    "numbering_face_obligation_on_consumers": "what a consumer must assert before verse arithmetic (E-61)",
    "produced_by": "the attempt, execution, model and grader role that produced it (OW-25)",
    "self_assertions": "the builder's own checks, each with whether it holds",
    "web_format": "the WEB extract's shape facts",
}
AMENDED = {  # a Phase 0 output amended after staging; its pre-image must be kept (E-44)
    "verse_inventory.json": "amended by Dan/_declare_inventory_face_dan.py to declare the WEB face (E-61 fix 1)",
}
KEY_CONST_EXEMPT = {  # files allowed to carry an Ezekiel-only key as a string constant
    "_build_device_inventory_dan.py": "it writes ezek_key_crosswalk, which names the Ezekiel keys to declare them",
    Path(__file__).name: "its declarations name the Ezekiel keys",
}
# (file, number, the context that must stand in the same string with %d as the number, reason). Numbers are ints and
# contexts are templates so that this file's own strings carry no Ezekiel number and the file stays inside the scan.
E65_EXEMPT = [
    ("check_register.py", 134, "tier-[%d]", "a regex character class of tier numbers, not a count"),
]
EZEK_MENTION_ALLOWED = {  # Daniel JSON places allowed to name Ezekiel, each a deliberate comparison
    "dan_device_inventory.json": {"citation_sweep_constants", "datelines", "ezek_key_crosswalk", "formulae",
                                  "year_word_but_not_a_dateline"},
    "verse_inventory.json": {"numbering_face_basis"},
    "strategy_plan_Dan.json": {"for_fable_end_review"},  # a Fable item says Ezekiel's ruling does not carry over
}
def _n(x):
    return len(x) if isinstance(x, (list, dict)) else x


def _zone_lines(om):
    """The zone lines as TOOLKIT.md prints them, formatted from the offset map's own zone keys."""
    out = []
    for z in om["rule"]["zones"]:
        for k, v in z.items():
            if k.startswith("mt_") and isinstance(v, str) and v.startswith("= WEB "):
                a = k[3:].split("_to_")
                c, v1 = (int(x) for x in a[0].split("_"))
                v2 = int(a[1]) if len(a) > 1 else v1
                out.append("MT %d:%s %s" % (c, ("%d-%d" % (v1, v2)) if v2 != v1 else str(v1), v))
    return out


def _notes_other(pm):
    cls = Counter((e["type"], e["attrs"], e["text"]) for v in pm["notes_other"].values() for e in v)
    return sum(cls.values()), len(pm["notes_other"]), len(cls)


TOOLKIT_PINS = [  # (claim, predicate over the loaded data); every figure is formatted from the data, never typed
    ("TOOLKIT.md states the verse and chapter totals",
     lambda d: "%d verses / %d chapters" % (d["inv"]["total_verses"], len(d["inv"]["chapters"])) in d["text"]),
    ("TOOLKIT.md states all four offset zones",
     lambda d: len(_zone_lines(d["om"])) == 4 and all(z in d["text"] for z in _zone_lines(d["om"]))),
    ("TOOLKIT.md carries the Tier-0 offset-zone rule verbatim",
     lambda d: d["om"]["rule"]["tier0_disclosure"] in d["text"]),
    ("TOOLKIT.md states the KJV-variance crosscheck",
     lambda d: "%d notes, %d of them" % (_n(d["om"]["kjv_variance_crosscheck"]["notes"]),
                                         _n(d["om"]["kjv_variance_crosscheck"]["notes_inside_zones"])) in d["text"]
     and "%d disagreements" % _n(d["om"]["kjv_variance_crosscheck"]["disagreements"]) in d["text"]),
    ("TOOLKIT.md names kjv_variance_crosscheck and zone_pairs, never content_anchors",
     lambda d: "kjv_variance_crosscheck" in d["text"] and "zone_pairs" in d["text"]
     and "content_anchors" not in d["text"]),
    ("TOOLKIT.md states the main-text word totals by language",
     lambda d: "%s Aramaic, %s Hebrew" % ("{:,}".format(d["lz"]["word_totals"]["A"]),
                                          "{:,}".format(d["lz"]["word_totals"]["H"])) in d["text"]),
    ("TOOLKIT.md states the per-verse language tally",
     lambda d: "%d Hebrew, %d Aramaic and %d mixed" % tuple(Counter(d["lz"]["verse_language"].values())[k]
                                                             for k in ("H", "A", "mixed")) in d["text"]),
    ("TOOLKIT.md states the parashah marks",
     lambda d: "%d samekh (setumah) + %d pe (petuchah) = %d mark occurrences over %d verses" % (
         d["pm"]["marks_tally"]["SAMEKH"], d["pm"]["marks_tally"]["PE"],
         d["pm"]["marks_tally"]["SAMEKH"] + d["pm"]["marks_tally"]["PE"],
         d["pm"]["marks_tally"]["verses_carrying_a_mark"]) in d["text"]),
    ("TOOLKIT.md states the paseq tally",
     lambda d: "Paseq: %d segs over %d verses" % (d["pm"]["paseq_tally"]["occurrences"],
                                                   d["pm"]["paseq_tally"]["verses"]) in d["text"]),
    ("TOOLKIT.md states the ketiv/qere tally",
     lambda d: "Ketiv/qere: %d notes over %d verses" % (d["pm"]["kq_tally"]["notes"],
                                                         d["pm"]["kq_tally"]["verses"]) in d["text"]),
    ("TOOLKIT.md states the OSHB editorial-note tally",
     lambda d: "%d notes over %d verses**, in %d classes" % _notes_other(d["pm"]) in d["text"]),
    ("TOOLKIT.md states sof-pasuq and maqaf seg totals",
     lambda d: "sof-pasuq: %d for %d verses" % (d["pm"]["seg_totals_in_xml"]["x-sof-pasuq"],
                                                d["inv"]["total_verses"]) in d["text"]
     and "maqaf: %s segs in the XML" % "{:,}".format(d["pm"]["seg_totals_in_xml"]["x-maqqef"]) in d["text"]),
    ("TOOLKIT.md states the dateline count",
     lambda d: "%d DATELINES" % d["dev"]["datelines"]["count"] in d["text"]),
    ("TOOLKIT.md states the WEB extract line count",
     lambda d: "WEB extract, %d lines" % len((BK / "Dan_web_clean.txt").read_text(encoding="utf-8").splitlines())
     in d["text"]),
    ("TOOLKIT.md carries no Ezekiel-only number (E-65)",
     lambda d: not [t for t in NUM.findall(d["text"]) if int(t.replace(",", "")) in d["want"]]),
]

NUM = re.compile(r"(?<![\w.:])\d{1,3}(?:,\d{3})+(?!\w)|(?<![\w.:,])\d+(?![\w:,]|\.\d)")


def _j(p):
    return json.loads(p.read_text(encoding="utf-8"))


def _sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _cv(ref):
    """'Dan.4.1', 'web:Dan.4.1' or 'oshb:Dan.4.1' -> (4, 1)."""
    c, v = ref.split(":")[-1].split(".")[1:]
    return int(c), int(v)


def _strings(v, path, out):
    if isinstance(v, dict):
        for k, x in v.items():
            _strings(x, path + [str(k)], out)
    elif isinstance(v, list):
        for x in v:
            _strings(x, path, out)
    elif isinstance(v, str):
        out.append((path, v))


def _ints(v, out):
    if isinstance(v, dict):
        for x in v.values():
            _ints(x, out)
    elif isinstance(v, list):
        for x in v:
            _ints(x, out)
    elif isinstance(v, int) and not isinstance(v, bool):
        out.add(v)


def _consts(p):
    return [n.value for n in ast.walk(ast.parse(p.read_text(encoding="utf-8")))
            if isinstance(n, ast.Constant) and isinstance(n.value, str)]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    artifacts_only = "--artifacts-only" in sys.argv
    checks = []

    def ck(name, ok):
        checks.append((name, bool(ok)))

    inv, om, vc = _j(BK / "verse_inventory.json"), _j(BK / "web_mt_offset_map.json"), _j(BK / "web_mt_verse_check.json")
    pm, dev = _j(BK / "pmarks_Dan.json"), _j(BK / "dan_device_inventory.json")
    lz, st = _j(BK / "dan_language_zones.json"), _j(BK / "dan_stage_report.json")
    oshb_lines = (BK / "Dan_oshb.txt").read_text(encoding="utf-8").splitlines()
    oshb = dict(l.split("\t", 1) for l in oshb_lines)
    web_order, ch = [], 0
    for l in (BK / "Dan_web_clean.txt").read_text(encoding="utf-8").splitlines():
        if l.startswith("===== DAN "):
            ch = int(l.split()[2])
        elif l.startswith("[v] "):
            web_order.append((ch, int(l.split()[1])))
    mt_order = [_cv(l.split("\t", 1)[0]) for l in oshb_lines]

    # 1. file-set and key parity, two ways, against Ezekiel's FINAL artifacts --------------------------------------
    ez_table = re.findall(r"^\| `\.\./([^`]+)`", EZ_TK.read_text(encoding="utf-8"), re.M)
    ck("Ezekiel's toolkit data-file table was read (%d files)" % len(ez_table), len(ez_table) >= 5)
    dan_files = sorted(p.name for p in BK.iterdir() if p.is_file() and p.suffix in (".json", ".txt", ".usfm"))

    def to_dan(n):
        return n.replace("Ezek", "Dan").replace("ezek_", "dan_")

    for n in ez_table:
        if n in FILE_ABSENT:
            ck("declared absence %s still has no Daniel file" % n, to_dan(n) not in dan_files)
        else:
            ck("Ezekiel data file %s has a Daniel counterpart" % n, to_dan(n) in dan_files)
    ez_names = {to_dan(n) for n in ez_table}
    for n in dan_files:
        if n in FILE_ADDED:
            ck("declared addition %s still has no Ezekiel counterpart" % n,
               not (EZ / n.replace("dan_", "ezek_").replace("Dan", "Ezek")).exists())
        else:
            ck("Daniel file %s has an Ezekiel counterpart" % n,
               n in ez_names or (EZ / n.replace("dan_", "ezek_").replace("_Dan", "_Ezek")).exists())
    for n in sorted(set(FILE_ABSENT) - set(ez_table)):
        ck("declared absence %s is in Ezekiel's table" % n, False)

    ez_only_keys = set()
    pairs = dict(KEYS)
    pairs["dan_device_inventory.json"] = None
    for n, decl in sorted(pairs.items()):
        d = _j(BK / n)
        e = _j(EZ / n.replace("dan_", "ezek_").replace("_Dan", "_Ezek"))
        eo, do = set(e) - set(d), set(d) - set(e)
        ez_only_keys |= eo
        if decl is None:
            rows = d["ezek_key_crosswalk"]["top_level"]
            named = {r["ezek_key"] for r in rows if r.get("reason")}
            ck("%s: every Ezekiel-only key has a crosswalk row with a reason" % n, eo <= named)
            xw_dan = {str(r["dan_key"]).split(".")[0] for r in rows if r["dan_key"]}
            ck("%s: every Daniel-only key is declared here or is a crosswalk target%s" % (
                n, (" (undeclared %s)" % sorted(do - set(DEV_ADDED) - xw_dan)) if do - set(DEV_ADDED) - xw_dan
                else ""), not (do - set(DEV_ADDED) - xw_dan))
            ck("%s: no stale Daniel-only declaration%s" % (
                n, (" (%s)" % sorted(set(DEV_ADDED) - do)) if set(DEV_ADDED) - do else ""), set(DEV_ADDED) <= do)
        else:
            ck("%s: Ezekiel-only keys are exactly the declared ones %s" % (n, sorted(eo)), eo == set(decl[0]))
            ck("%s: Daniel-only keys are exactly the declared ones %s" % (n, sorted(do)), do == set(decl[1]))

    # 2. faces ----------------------------------------------------------------------------------------------------
    ck('verse_inventory.json numbering_face == "WEB"', inv["numbering_face"] == "WEB")
    ck('dan_device_inventory.json numbering_face == "MT"', dev["numbering_face"] == "MT")
    ck("the offset map names WEB as the row face", om["numbering_face"].startswith("WEB"))
    web_pc = Counter(c for c, _ in web_order)
    mt_pc = Counter(c for c, _ in mt_order)
    ck("verse_inventory chapters equal the WEB extract's own counts",
       {int(k): v for k, v in inv["chapters"].items()} == dict(web_pc))
    ck("web_mt_verse_check per_chapter equals both extracts' own counts",
       all(vc["per_chapter"][str(c)] == {"web": web_pc[c], "mt": mt_pc[c]} for c in range(1, 13)))
    ck("divergent chapters are exactly 3, 4, 5 and 6", vc["divergent_chapters"] == [3, 4, 5, 6]
       and [c for c in range(1, 13) if web_pc[c] != mt_pc[c]] == [3, 4, 5, 6])
    ck("357 verses in each witness, 12 chapters", len(web_order) == len(mt_order) == len(oshb) == 357
       and inv["total_verses"] == 357 and len(inv["chapters"]) == 12)
    ck("device inventory MT per-chapter counts equal the MT extract",
       {int(k): v for k, v in dev["totals"]["verses_per_chapter_mt"].items()} == dict(mt_pc))

    # 3. the alignment, re-derived from verse order ----------------------------------------------------------------
    align = dict(zip(mt_order, web_order))
    moved = {m: w for m, w in align.items() if m != w}
    ck("MT refs are unique and WEB refs are unique", len(set(mt_order)) == len(set(web_order)) == 357)
    ck("66 verses are renumbered, all inside MT chapters 3, 4 and 6",
       len(moved) == 66 and {m[0] for m in moved} == {3, 4, 6})
    kv = {_cv(k): _cv(v) for k, v in pm["kjv_variance"].items()}
    ck("every OSHB KJV-variance note agrees with the order alignment (%d)" % len(kv),
       len(kv) == 66 and all(align.get(m) == w for m, w in kv.items()))
    ck("the KJV-variance notes cover exactly the renumbered verses", set(kv) == set(moved))
    ck("every zone_pairs endpoint agrees with the order alignment",
       all(align.get(_cv(z["mt"])) == _cv(z["web"]) for z in om["zone_pairs"]))
    xc = om["kjv_variance_crosscheck"]
    ck("the map's KJV cross-check is 66/66 with no disagreement",
       xc["notes"] == xc["notes_inside_zones"] == 66 and xc["disagreements"] == [])
    ck("offset map verdict GREEN with no problems", om["verification"]["verdict"] == "GREEN"
       and om["verification"]["problems"] == [])
    ck("offset map totals equal at 357", om["totals"] == {"web": 357, "mt": 357, "equal": True})

    # provenance and drift
    src = st["sources"]["oshb_xml"]["sha256"]
    ck("one OSHB source hash across stage report, pmarks, zones and the map's cross-check",
       pm["source"]["sha256"] == lz["source"]["sha256"] == xc["source_sha256"] == src)
    for n, rec in sorted(st["outputs"].items()):
        cur = _sha(BK / n)
        if n in AMENDED:
            pre = BK / ("%s.pre_%s" % (n, rec["sha256"][:12]))
            ck("%s amended after staging and its pre-image kept (E-44)" % n,
               cur != rec["sha256"] and pre.is_file() and _sha(pre) == rec["sha256"])
        else:
            ck("%s unchanged since staging" % n, cur == rec["sha256"])
    for n, h in sorted(dev["inputs"].items()):
        p = BK / n
        pre = BK / ("%s.pre_%s" % (n, h[:12]))
        ck("device-inventory input %s is the current file or its kept pre-image" % n,
           p.is_file() and (_sha(p) == h or (n in AMENDED and pre.is_file() and _sha(pre) == h)))

    # language arithmetic
    wt, nt = lz["word_totals"], lz["note_word_totals"]
    ck("pmarks morph tally = zone word totals + note word totals, per language",
       pm["morph_prefix_tally_including_note_words"] == {k: wt.get(k, 0) + nt.get(k, 0) for k in set(wt) | set(nt)})
    runs = lz["runs"]
    ck("three language runs H, A, H whose words sum to the word totals",
       [r["lang"] for r in runs] == ["H", "A", "H"] and sum(r["words"] for r in runs) == sum(wt.values()))
    ck("the run boundaries are the device inventory's switch points",
       [(r["start"].split()[0], int(r["start"].split()[1][1:])) for r in runs[1:]]
       == [(s["mt"], s["word_index"]) for s in dev["language_switches"]])
    ck("every device-inventory self-assertion holds", all(a["holds"] for a in dev["self_assertions"]))

    # parashah and segs
    seg, mk = pm["seg_totals_in_xml"], pm["marks_tally"]
    ck("sof-pasuq on all 357 verses", seg["x-sof-pasuq"] == 357 and pm["arithmetic"]["sof_pasuq_absent_verses"] == [])
    ck("seg totals equal the mark and paseq tallies", seg["x-pe"] == mk["PE"] and seg["x-samekh"] == mk["SAMEKH"]
       and seg["x-paseq"] == pm["paseq_tally"]["occurrences"])
    ck("no verse carries more than one mark", pm["arithmetic"]["verses_with_more_than_one_mark"] == {}
       and mk["verses_carrying_a_mark"] == mk["PE"] + mk["SAMEKH"] + mk["REVERSED_NUN"] == len(pm["marks"]))
    # paseq is one ref per occurrence, so its length is the occurrence count and its distinct refs the verse count
    ck("paseq and K/Q tallies equal their own lists", pm["paseq_tally"]["occurrences"] == len(pm["paseq"])
       and pm["paseq_tally"]["verses"] == len(set(pm["paseq"]))
       and pm["kq_tally"]["verses"] == len(pm["kq"]) and pm["kq_tally"]["notes"] == sum(map(len, pm["kq"].values())))

    # extract hygiene (the same convention the Ezekiel extract states)
    joined = "".join(oshb.values())
    for name, cp in (("maqaf U+05BE", "־"), ("paseq U+05C0", "׀"), ("sof-pasuq U+05C3", "׃"),
                     ("puncta U+05C4", "ׄ"), ("lower dot U+05C5", "ׅ"), ("morpheme /", "/"),
                     ("stray >", ">")):
        ck("no %s in the MT extract" % name, joined.count(cp) == 0)

    # 4. no Daniel tool binds to an Ezekiel-only key ----------------------------------------------------------------
    pys = sorted(HERE.glob("*.py")) + sorted(BK.glob("*.py"))
    for p in pys:
        if p.name in KEY_CONST_EXEMPT:
            continue
        bad = sorted(set(_consts(p)) & ez_only_keys)
        ck("%s carries no Ezekiel-only key%s" % (p.name, (" (has %s)" % bad) if bad else ""), not bad)
    ck("dan_lib.py binds to the Daniel morph key", "morph_prefix_tally_including_note_words"
       in _consts(HERE / "dan_lib.py"))

    # 5. E-65 floor: no Ezekiel-only integer fact in a Daniel string -------------------------------------------------
    ez_ints, dan_ints = set(), set()
    for n in ez_table + ["ezek_stage_report.json"]:
        if n.endswith(".json"):
            _ints(_j(EZ / n), ez_ints)
    for p in BK.glob("*.json"):
        _ints(_j(p), dan_ints)
    want = {x for x in ez_ints - dan_ints if x >= 100}
    ck("the E-65 floor has Ezekiel facts to look for (%d)" % len(want), len(want) >= 5)
    exempt_used = []
    for p in sorted(BK.glob("*.json")):
        ss = []
        _strings(_j(p), [], ss)
        hits = sorted({t for _, v in ss for t in NUM.findall(v) if int(t.replace(",", "")) in want})
        ck("%s carries no Ezekiel-only number%s" % (p.name, (" (has %s)" % hits) if hits else ""), not hits)
        places = {path[0] for path, v in ss if "Ezek" in v and path}
        allowed = EZEK_MENTION_ALLOWED.get(p.name, set())
        ck("%s names Ezekiel only in declared places%s" % (p.name, (" (also %s)" % sorted(places - allowed))
                                                           if places - allowed else ""), places <= allowed)
    for p in pys:
        hits = []
        for v in _consts(p):
            for t in NUM.findall(v):
                if int(t.replace(",", "")) not in want:
                    continue
                ex = [e for e in E65_EXEMPT if e[0] == p.name and str(e[1]) == t and (e[2] % e[1]) in v]
                (exempt_used if ex else hits).append(t)
        ck("%s emits no Ezekiel-only number%s" % (p.name, (" (has %s)" % sorted(set(hits))) if hits else ""), not hits)
    ck("every E-65 exemption is still used", len(set(exempt_used)) == len(E65_EXEMPT))

    # 6. TOOLKIT.md claims ------------------------------------------------------------------------------------------
    exempt = []
    if not artifacts_only:
        ck("TOOLKIT.md exists", TK.is_file())
        text = TK.read_text(encoding="utf-8") if TK.is_file() else ""
        ck("TOOLKIT.md pins at least one claim", bool(TOOLKIT_PINS))
        data = dict(inv=inv, om=om, vc=vc, pm=pm, dev=dev, lz=lz, st=st, oshb=oshb, text=text, want=want)
        for claim, pred in TOOLKIT_PINS:
            ck(claim, pred(data))
        quoted = set()
        for line in text.splitlines():
            for q in re.findall(r'"([^"]*)"', line):
                quoted.update(re.findall(r"MT (\d+):(\d+)", q))
        for m in re.finditer(r"MT (\d+):(\d+)", text):
            if m.groups() in quoted:
                exempt.append("MT %s:%s (quoted counter-example, not an assertion)" % m.groups())
                continue
            ck("named ref MT %s:%s exists" % m.groups(), "Dan.%s.%s" % m.groups() in oshb)
        webset = set(web_order)
        for m in re.finditer(r"(oshb|web):(\w+)\.(\d+)\.(\d+)", text):
            face, bk, c, v = m.groups()
            if bk != "Dan":
                exempt.append("%s:%s.%s.%s (another book, book-qualified)" % (face, bk, c, v))
                continue
            ok = ("Dan.%s.%s" % (c, v) in oshb) if face == "oshb" else ((int(c), int(v)) in webset)
            ck("named ref %s:Dan.%s.%s exists" % (face, c, v), ok)

    failed = [n for n, ok in checks if not ok]
    print(json.dumps({"checks": len(checks), "passed": len(checks) - len(failed), "failed": failed,
                      "scope": "artifacts_only" if artifacts_only else "full",
                      "declared": {"files": len(FILE_ABSENT) + len(FILE_ADDED),
                                   "keys": sum(len(a) + len(b) for a, b in KEYS.values()) + len(DEV_ADDED),
                                   "amended": len(AMENDED), "e65_exempt": len(E65_EXEMPT)},
                      "exempt_refs": sorted(set(exempt)),
                      "verdict": "GREEN" if not failed else "RED"}, ensure_ascii=False, indent=1))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
