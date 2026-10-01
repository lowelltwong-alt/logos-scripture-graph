#!/usr/bin/env python3
"""Phase-0-style Tier-0: build + BYTE-VERIFY ../web_mt_offset_map.json for Ps
(rebuilt 2026-09-03 for the OW-2 item-2 audit; independent of ps_lib, which
READS the map this script writes).

The Ps strategy (book_strategy/Ps.md §3, owner-ruled LAW) records the rule
set: 87 identity / 58 shift+1 / 4 shift+2 (51, 52, 54, 60) / Ps 13 split.
This script re-derives and PROVES it from the staged witnesses' bytes —
never assumed — by independent layers:
  1. per-psalm verse-count difference (MT - WEB) in {0, 1, 2} from both
     witnesses' bytes -> identity / shift1 / shift2; the equal-count Ps 13
     is classified SPLIT only after three byte tests hold (WEB 13 carries a
     title line; MT 13:1 is title-shaped [lamnatseach..le-David, no body
     content]; MT 13:6 carries BOTH the trust-clause and the sing-clause
     that WEB renders as 13:5 and 13:6);
  2. title-presence consistency: every shift psalm carries a WEB
     [SUPERSCRIPTION] line; the counted-title arithmetic 58*1 + 4*2 = 66 =
     MT total - WEB total;
  3. content anchors: every WEB verse containing "Selah" must map to an MT
     verse carrying the word-bound token סלה, and vice versa; every WEB
     verse containing a proper-name anchor must find its Hebrew skeleton at
     the CROSSWALK-MAPPED MT ref; every miss is listed for byte review;
  4. FALSIFICATION probe: the same anchor checks under the IDENTITY mapping
     must fail massively (if they did not, the rule set would be
     unsupported);
  5. seam byte-review assertions at MT 1:1 / 3:1-2 / 13:6 / 51:1-3 / 60:1-3;
  6. SECONDARY witness (consistency probe, not proof): every explicit
     "web:Ps.C.V = oshb:Ps.C.W" dual-cite in the SHIPPED Ps corpus
     (book_chunks/Ps/chunks.jsonl, M8's own evidence) is checked against the
     map; disagreements are SURFACED (they are either a map error or a
     shipped defect — the audit lane decides).
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SPBOOK = TOOLS.parent
BOOK = "Ps"
SHIPPED = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking"
               r"\M8_fable\book_chunks\Ps\chunks.jsonl")

POINTS = re.compile(r"[\u0591-\u05C7]")
FINALS = str.maketrans("\u05DA\u05DD\u05DF\u05E3\u05E5", "\u05DB\u05DE\u05E0\u05E4\u05E6")


def skeleton(s: str) -> str:
    return POINTS.sub("", unicodedata.normalize("NFD", s)).replace("\u05BE", " ")


def anchor_norm(s: str) -> str:
    """Final-letter allography normalization FOR ANCHORING ONLY (never for
    quotation)."""
    return s.translate(FINALS)


# ---------------------------------------------------------------- witnesses
inv = json.loads((SPBOOK / "verse_inventory.json").read_text(encoding="utf-8"))
WEB_LAST = {int(c): n for c, n in inv["chapters"].items()}

oshb: dict[tuple[int, int], str] = {}
MT_LAST: dict[int, int] = {}
for line in (SPBOOK / f"{BOOK}_oshb.txt").read_text(encoding="utf-8").splitlines():
    if "\t" not in line:
        continue
    ref, text = line.split("\t", 1)
    _, c, v = ref.split(".")
    c, v = int(c), int(v)
    MT_LAST[c] = max(MT_LAST.get(c, 0), v)
    oshb[(c, v)] = text

# WEB verse texts + title lines from the clean extract (minimal parser)
web: dict[tuple[int, int], str] = {}
titled: set[int] = set()
ps119_markers = 0
clean = (SPBOOK / f"{BOOK}_web_clean.txt").read_text(encoding="utf-8")
ch = None
cur = None
for line in clean.splitlines():
    h = re.match(r"===== PS (\d+) =====", line.strip())
    if h:
        ch = int(h.group(1)); cur = None
        continue
    s = line.strip()
    if s.startswith("[SUPERSCRIPTION"):
        if ch == 119:
            ps119_markers += 1
        else:
            titled.add(ch)
        continue
    if s.startswith("[MAJOR-SECTION") or s.startswith("[HEADING") or s.startswith("[SPEAKER"):
        continue
    body = re.sub(r"^(\u00B6[\u00BB\u203A]?\([^)]*\)|\u00B6|\s*\u2022|\s*\|[a-z0-9]+(?:\([^)]*\))?)\s*", "", line)
    body = body.replace("[qs Selah]", "Selah")
    parts = re.split(r"\[v\] (\d+)\s*", body)
    if parts[0].strip() and cur:
        web[cur] = web[cur] + " " + parts[0].strip()
    i = 1
    while i < len(parts):
        cur = (ch, int(parts[i]))
        web[cur] = parts[i + 1].strip()
        i += 2

assert sum(WEB_LAST.values()) == len(web) == 2461, (len(web), sum(WEB_LAST.values()))
assert sum(MT_LAST.values()) == len(oshb) == 2527, (len(oshb), sum(MT_LAST.values()))
assert len(WEB_LAST) == len(MT_LAST) == 150
assert ps119_markers == 22, ps119_markers
assert len(titled) == 116, len(titled)

# ---------------------------------------------------------------- layer 1+2: rules from counts
rules: dict[int, dict] = {}
for c in sorted(WEB_LAST):
    diff = MT_LAST[c] - WEB_LAST[c]
    assert diff in (0, 1, 2), f"Ps {c}: MT-WEB difference {diff} outside the known rule set"
    rules[c] = {"rule": {0: "identity", 1: "shift1", 2: "shift2"}[diff],
                "web_verses": WEB_LAST[c], "mt_verses": MT_LAST[c],
                "titled": c in titled}

# Ps 13: equal counts, but the strategy law records a SPLIT — prove it from bytes
sk13_1 = skeleton(oshb[(13, 1)])
sk13_6 = skeleton(oshb[(13, 6)])
split_tests = {
    "web_13_titled": 13 in titled,
    "mt_13_1_title_shaped": sk13_1.split() == ["למנצח", "מזמור", "לדוד"],
    "mt_13_6_carries_trust_clause": "בטחתי" in sk13_6,          # WEB 13:5 "I trust"
    "mt_13_6_carries_sing_clause": "אשירה" in sk13_6,          # WEB 13:6 "I will sing"
    "web_13_5_is_trust": "trust" in web[(13, 5)].lower(),
    "web_13_6_is_sing": "sing" in web[(13, 6)].lower(),
}
assert all(split_tests.values()), split_tests
rules[13]["rule"] = "split13"

for c, r in rules.items():
    if r["rule"] in ("shift1", "shift2", "split13"):
        assert r["titled"], f"Ps {c}: shift rule without a WEB title line"
counts = {k: sum(1 for r in rules.values() if r["rule"] == k)
          for k in ("identity", "shift1", "shift2", "split13")}
assert counts == {"identity": 87, "shift1": 58, "shift2": 4, "split13": 1}, counts
assert sorted(c for c, r in rules.items() if r["rule"] == "shift2") == [51, 52, 54, 60]
assert counts["shift1"] * 1 + counts["shift2"] * 2 == 66 == 2527 - 2461
titled_identity = sorted(c for c, r in rules.items() if r["titled"] and r["rule"] == "identity")
# strategy §2a: "in the other 53 titled psalms the title is the PREFIX of MT v1"
# (116 titles = 58 shift1 + 4 shift2 + 1 split [Ps 13] + 53 titled identity)
assert len(titled_identity) == 53, len(titled_identity)
assert len(titled) == 58 + 4 + 1 + 53 == 116


def web_to_mt_rule(c: int, v: int, rule_of=None) -> tuple[int, int]:
    r = (rule_of or rules)[c]["rule"] if rule_of is not False else "identity"
    if r == "identity":
        return (c, v)
    if r == "shift1":
        return (c, v + 1)
    if r == "shift2":
        return (c, v + 2)
    if r == "split13":
        return (13, v + 1) if v <= 4 else (13, 6)
    raise ValueError(r)


# ---------------------------------------------------------------- layer 3: anchors
ANCHORS = {
    "Jerusalem": ["ירושלם", "ירושלים"], "Zion": ["ציון"], "Israel": ["ישראל"],
    "Jacob": ["יעקב"], "Egypt": ["מצרים"], "Moses": ["משה"], "Aaron": ["אהרן"],
    "Judah": ["יהודה"], "Ephraim": ["אפרים"], "Manasseh": ["מנשה"],
    "Lebanon": ["לבנון"], "Bashan": ["בשן"], "Jordan": ["ירדן"], "Sinai": ["סיני"],
    "Moab": ["מואב"], "Philistia": ["פלשת"], "Babylon": ["בבל"], "Amalek": ["עמלק"],
    "Melchizedek": ["מלכי צדק"], "Abraham": ["אברהם"], "Joseph": ["יוסף", "יהוסף"],
    "Hermon": ["חרמון"], "Tabor": ["תבור"], "Meribah": ["מריבה"],
    "Zebulun": ["זבולן", "זבלון"], "Naphtali": ["נפתלי"], "Benjamin": ["בנימן", "בנימין"],
    "Gilead": ["גלעד"], "Tarshish": ["תרשיש"], "Sheba": ["שבא"], "Midian": ["מדין"],
    "Sisera": ["סיסרא"], "Sihon": ["סיחון", "סיחן"], "Zoan": ["צען"],
    "Succoth": ["סכות"], "Assyria": ["אשור"], "Gebal": ["גבל"], "Ammon": ["עמון"],
    "Kedar": ["קדר"], "Edom": ["אדום", "אדם"], "David": ["דוד", "דויד"],
    "seventy": ["שבעים"], "forty": ["ארבעים"], "thousand": ["אלף", "אלפים"],
}


def check_anchors(mapper) -> dict:
    checks = 0
    misses = []
    for (c, v), text in web.items():
        text = re.sub(r"\[fn [^\]]*\]", " ", text)     # never anchor on footnote text
        for eng, hebs in ANCHORS.items():
            if re.search(rf"\b{eng}\b", text):
                mt = mapper(c, v)
                hay = anchor_norm(skeleton(oshb.get(mt, "")))
                checks += 1
                if not any(anchor_norm(h) in hay for h in hebs):
                    misses.append({"web": f"Ps.{c}.{v}", "anchor": eng, "mt": f"Ps.{mt[0]}.{mt[1]}"})
    # Selah both directions (word-bound)
    selah_checks = 0
    selah_misses = []
    web_selah = {(c, v) for (c, v), t in web.items() if re.search(r"\bSelah\b", t)}
    mt_selah = {k for k, t in oshb.items() if "סלה" in skeleton(t).split()}
    for (c, v) in sorted(web_selah):
        selah_checks += 1
        if mapper(c, v) not in mt_selah:
            selah_misses.append({"web": f"Ps.{c}.{v}", "mt": "Ps.%d.%d" % mapper(c, v)})
    mapped = {mapper(c, v) for (c, v) in web_selah}
    for k in sorted(mt_selah):
        selah_checks += 1
        if k not in mapped:
            selah_misses.append({"mt": f"Ps.{k[0]}.{k[1]}", "web": "none"})
    return {"anchor_checks": checks, "anchor_misses": misses,
            "selah_web_verses": len(web_selah), "selah_mt_verses": len(mt_selah),
            "selah_checks": selah_checks, "selah_misses": selah_misses}


rule_result = check_anchors(lambda c, v: web_to_mt_rule(c, v))
ident_result = check_anchors(lambda c, v: (c, v))

# ---------------------------------------------------------------- layer 5: seam byte review
seam = {
    "mt_1_1_opens_ashrei_untitled_identity": skeleton(oshb[(1, 1)]).startswith("אשרי") and 1 not in titled,
    "mt_3_1_is_title_mizmor_ledavid": skeleton(oshb[(3, 1)]).startswith("מזמור לדוד"),
    "mt_3_2_is_web_3_1_adversaries": "מה רבו צרי" in skeleton(oshb[(3, 2)]) and "adversaries" in web[(3, 1)],
    "mt_51_1_2_title_51_3_is_web_51_1_have_mercy": skeleton(oshb[(51, 1)]).startswith("למנצח")
        and "נתן הנביא" in skeleton(oshb[(51, 2)]) and skeleton(oshb[(51, 3)]).startswith("חנני")
        and web[(51, 1)].lower().startswith("have mercy"),
    "mt_60_1_2_title_60_3_is_web_60_1_rejected": skeleton(oshb[(60, 1)]).startswith("למנצח")
        and "אלהים זנחתנו" in skeleton(oshb[(60, 3)]) and "rejected" in web[(60, 1)].lower(),
    "mt_13_6_double_half": split_tests["mt_13_6_carries_trust_clause"] and split_tests["mt_13_6_carries_sing_clause"],
    "mt_119_1_untitled_identity_ashrei": skeleton(oshb[(119, 1)]).startswith("אשרי") and 119 not in titled,
}
assert all(seam.values()), seam

# ---------------------------------------------------------------- layer 6: shipped-corpus dual-cite probe
DUAL = re.compile(r"web:Ps\.(\d+)\.(\d+)\s*=\s*oshb:Ps\.(\d+)\.(\d+)(?:-(\d+))?")
probe = {"dual_cites_found": 0, "agree": 0, "disagree": []}
if SHIPPED.is_file():
    for line in SHIPPED.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        blob = json.dumps(row, ensure_ascii=False)
        for m in DUAL.finditer(blob):
            wc, wv, mc, mv, mv2 = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), m.group(5)
            probe["dual_cites_found"] += 1
            if wv == 0:
                # the title spans MT v1 (or vv1-2 in the four +2 psalms): a title cite may
                # name either title verse or the pair (e.g. web:Ps.51.0 = oshb:Ps.51.2 for
                # the Bathsheba clause, which sits in MT 51:2)
                want = [(wc, 1), (wc, 2)] if rules[wc]["rule"] == "shift2" else [(wc, 1)]
                got = [(mc, mv)] + ([(mc, int(mv2))] if mv2 else [])
                ok = wc in titled and all(g in want for g in got)
            else:
                ok = (mc, mv) == web_to_mt_rule(wc, wv)
            if ok:
                probe["agree"] += 1
            else:
                probe["disagree"].append({"row": row.get("decision_id"), "cite": m.group(0)})

# ---------------------------------------------------------------- write
out = {
    "book": BOOK,
    "built": "2026-09-03 (OW-2 item-2 audit rebuild; independent of the lost Ps campaign scratchpad)",
    "rule_set": ("identity | shift1 (WEB v = MT v+1; MT v1 = WEB title Ps.N.0) | "
                 "shift2 (WEB v = MT v+2; MT vv1-2 = WEB title; psalms 51, 52, 54, 60) | "
                 "split13 (WEB 13:1-4 = MT 13:2-5; WEB 13:5 AND 13:6 = MT 13:6; MT 13:1 = WEB title)"),
    "totals": {"web": 2461, "mt": 2527, "counted_title_verses": 66, "web_titled_psalms": 116,
               "titled_identity_psalms": 53, "ps119_letter_markers_not_titles": 22},
    "rule_counts": counts,
    "chapters": {str(c): rules[c] for c in sorted(rules)},
    "ps13_split_byte_tests": split_tests,
    "anchors_under_rule_set": rule_result,
    "falsification_under_identity": {"anchor_misses": len(ident_result["anchor_misses"]),
                                     "selah_misses": len(ident_result["selah_misses"]),
                                     "anchor_checks": ident_result["anchor_checks"]},
    "seam_byte_review": seam,
    "shipped_corpus_dual_cite_probe": probe,
    "convention": "bare/web: refs + row spans = WEB; oshb:/pmarks = MT; web:Ps.N.0 = the title pseudo-verse",
}
(SPBOOK / "web_mt_offset_map.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({
    "rule_counts": counts,
    "anchor_checks": rule_result["anchor_checks"],
    "anchor_misses_under_rules": len(rule_result["anchor_misses"]),
    "anchor_miss_list": rule_result["anchor_misses"][:40],
    "selah": {"web": rule_result["selah_web_verses"], "mt": rule_result["selah_mt_verses"],
              "misses": rule_result["selah_misses"]},
    "falsification_identity": out["falsification_under_identity"],
    "seam": seam,
    "shipped_dual_cites": {"found": probe["dual_cites_found"], "agree": probe["agree"],
                           "disagree": probe["disagree"][:20]},
    "status": "WRITTEN",
}, ensure_ascii=False, indent=1))
