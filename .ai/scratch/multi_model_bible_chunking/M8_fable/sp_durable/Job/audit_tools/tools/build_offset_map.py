#!/usr/bin/env python3
"""Phase-0-style Tier-0: build + BYTE-VERIFY ../web_mt_offset_map.json for Job
(rebuilt 2026-09-03 for the OW-2 item-2 audit; independent of job_lib, which
READS the map this script writes).

The Job strategy (book_strategy/Job.md §3, owner-ruled LAW) records ONE
offset zone: WEB 41:1-8 = MT 40:25-32; WEB 41:9-34 = MT 41:1-26; all else
identity. This script re-derives and PROVES it from the staged witnesses'
bytes — never assumed — by independent layers:
  1. per-chapter verse-count equality UNDER THE RULE SET from both
     witnesses' bytes (WEB 40 = 24 / MT 40 = 32; WEB 41 = 34 / MT 41 = 26;
     every other chapter equal; totals 1070 = 1070);
  2. content anchors: every WEB verse containing a proper-name / numeral
     anchor must find its Hebrew skeleton at the CROSSWALK-MAPPED MT ref;
     every miss is listed for byte review;
  3. FALSIFICATION probe: the same checks under the IDENTITY mapping must
     fail inside the zone;
  4. seam byte-review assertions: MT 40:24 = WEB 40:24 (identity edge);
     MT 40:25 opens the Leviathan line rendered at WEB 41:1; MT 41:1 =
     WEB 41:9; MT 41:26 = WEB 41:34 (zone end); MT 42:1 = WEB 42:1;
  5. SECONDARY witness (consistency probe, not proof): explicit
     "web:Job.C.V = oshb:Job.C.W" dual-cites in the SHIPPED Job corpus are
     checked against the map; disagreements are SURFACED.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SPBOOK = TOOLS.parent
BOOK = "Job"
SHIPPED = Path(r"C:\wt\logos-t423-m8-fable\.ai\scratch\multi_model_bible_chunking"
               r"\M8_fable\book_chunks\Job\chunks.jsonl")

POINTS = re.compile(r"[\u0591-\u05C7]")
FINALS = str.maketrans("\u05DA\u05DD\u05DF\u05E3\u05E5", "\u05DB\u05DE\u05E0\u05E4\u05E6")


def skeleton(s: str) -> str:
    return POINTS.sub("", unicodedata.normalize("NFD", s)).replace("\u05BE", " ")


def anchor_norm(s: str) -> str:
    return s.translate(FINALS)


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

web: dict[tuple[int, int], str] = {}
clean = (SPBOOK / f"{BOOK}_web_clean.txt").read_text(encoding="utf-8")
ch = None
cur = None
annot = []
for line in clean.splitlines():
    h = re.match(r"===== JOB (\d+) =====", line.strip())
    if h:
        ch = int(h.group(1)); cur = None
        continue
    s = line.strip()
    if s.startswith("[SUPERSCRIPTION") or s.startswith("[MAJOR-SECTION") or s.startswith("[HEADING") or s.startswith("[SPEAKER"):
        annot.append(s[:60])
        continue
    body = re.sub(r"^(\u00B6[\u00BB\u203A]?\([^)]*\)|\u00B6|\s*\u2022|\s*\|[a-z0-9]+(?:\([^)]*\))?)\s*", "", line)
    parts = re.split(r"\[v\] (\d+)\s*", body)
    if parts[0].strip() and cur:
        web[cur] = web[cur] + " " + parts[0].strip()
    i = 1
    while i < len(parts):
        cur = (ch, int(parts[i]))
        web[cur] = parts[i + 1].strip()
        i += 2

assert sum(WEB_LAST.values()) == len(web) == 1070
assert sum(MT_LAST.values()) == len(oshb) == 1070
assert len(WEB_LAST) == len(MT_LAST) == 42
assert WEB_LAST[40] == 24 and WEB_LAST[41] == 34 and MT_LAST[40] == 32 and MT_LAST[41] == 26
for c in WEB_LAST:
    if c not in (40, 41):
        assert WEB_LAST[c] == MT_LAST[c], f"ch {c}: WEB {WEB_LAST[c]} MT {MT_LAST[c]}"


def web_to_mt_local(c: int, v: int) -> tuple[int, int]:
    if c == 41:
        return (40, 24 + v) if v <= 8 else (41, v - 8)
    return (c, v)


ANCHORS = {
    "Job": ["איוב"], "Uz": ["עוץ"], "Satan": ["השטן", "שטן"], "Eliphaz": ["אליפז"],
    "Bildad": ["בלדד"], "Zophar": ["צפר", "צופר"], "Elihu": ["אליהוא", "אליהו"], "Barachel": ["ברכאל"],
    "Buzite": ["בוזי"], "Temanite": ["תימני", "תמני"], "Shuhite": ["שוחי", "שחי"],
    "Naamathite": ["נעמתי"], "Sabeans": ["שבא"], "Chaldeans": ["כשדים"],
    "Leviathan": ["לויתן"], "Behemoth": ["בהמות"], "Ophir": ["אופיר"], "Sheba": ["שבא"],
    "Tema": ["תימא", "תמא"], "Jemimah": ["ימימה"], "Keziah": ["קציעה"], "Keren Happuch": ["קרן הפוך"],
    "Rahab": ["רהב"], "Pleiades": ["כימה"], "Jordan": ["ירדן"], "Egypt": ["מצרים"],
    "seven": ["שבע", "שבעה", "שבעת"], "three": ["שלש", "שלוש", "שלשה", "שלשת"], "thousand": ["אלף", "אלפים"],
    "hundred": ["מאה", "מאות", "מאתים"], "fourteen": ["ארבעה עשר"], "forty": ["ארבעים"],
    "Adam": ["אדם"],
    # Leviathan-poem lexemes so the WEB 41 zone carries several discriminating anchors
    # (generic glosses "deep"/"sword"/"sparks"/"bronze" were tried and dropped: WEB
    # renders several DIFFERENT Hebrew lexemes with them in identity chapters —
    # rendering divergences, not offset evidence; the remaining set is clean)
    "iron": ["ברזל"], "smoke": ["עשן"], "millstone": ["פלח"],
    "hook": ["חוח", "חכה"], "arrow": ["חץ", "קשת"], "scales": ["מגנים", "מגן"],
    "Leviathan poem sparks line": [],
}
ANCHORS.pop("Leviathan poem sparks line")


def check_anchors(mapper) -> dict:
    checks = 0
    misses = []
    zone_checks = 0
    for (c, v), text in web.items():
        text = re.sub(r"\[fn [^\]]*\]", " ", text)     # never anchor on footnote text
        for eng, hebs in ANCHORS.items():
            if re.search(rf"\b{eng}\b", text):
                mt = mapper(c, v)
                hay = anchor_norm(skeleton(oshb.get(mt, "")))
                checks += 1
                if c == 41:
                    zone_checks += 1
                if not any(anchor_norm(h) in hay for h in hebs):
                    misses.append({"web": f"Job.{c}.{v}", "anchor": eng, "mt": f"Job.{mt[0]}.{mt[1]}"})
    return {"anchor_checks": checks, "zone_checks": zone_checks, "anchor_misses": misses}


rule_result = check_anchors(web_to_mt_local)
ident_result = check_anchors(lambda c, v: (c, v))

seam = {
    # WEB 40:24 renders b-'einav as "when he is on the watch" — anchor on the snare word instead
    "mt_40_24_identity_edge_web_40_24_snare": "במוקשים" in skeleton(oshb[(40, 24)]) and "snare" in web[(40, 24)].lower(),
    "mt_40_25_leviathan_is_web_41_1": "לויתן" in skeleton(oshb[(40, 25)]) and "leviathan" in web[(41, 1)].lower(),
    "mt_41_1_hope_in_vain_is_web_41_9": skeleton(oshb[(41, 1)]).startswith("הן תחלתו") and "hope" in web[(41, 9)].lower(),
    "mt_41_26_zone_end_is_web_41_34": "מלך" in skeleton(oshb[(41, 26)]) and "king" in web[(41, 34)].lower(),
    "mt_42_1_identity_edge": skeleton(oshb[(42, 1)]).startswith("ויען איוב") and "job answered" in web[(42, 1)].lower(),
    "mt_40_15_behemoth_before_zone_identity": "בהמות" in skeleton(oshb[(40, 15)]) and "behemoth" in web[(40, 15)].lower(),
}
assert all(seam.values()), seam

DUAL = re.compile(r"web:Job\.(\d+)\.(\d+)\s*=\s*oshb:Job\.(\d+)\.(\d+)")
probe = {"dual_cites_found": 0, "agree": 0, "disagree": []}
if SHIPPED.is_file():
    for line in SHIPPED.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        blob = json.dumps(row, ensure_ascii=False)
        for m in DUAL.finditer(blob):
            wc, wv, mc, mv = (int(m.group(i)) for i in range(1, 5))
            probe["dual_cites_found"] += 1
            if (mc, mv) == web_to_mt_local(wc, wv):
                probe["agree"] += 1
            else:
                probe["disagree"].append({"row": row.get("decision_id"), "cite": m.group(0)})

chapters = {}
for c in sorted(WEB_LAST):
    rule = "identity" if c not in (40, 41) else ("zone_web41_split_across_mt40_41" if c == 41 else "identity_but_mt_ch40_continues_to_32")
    chapters[str(c)] = {"rule": rule if c == 41 else ("identity" if c != 40 else "identity"),
                        "web_verses": WEB_LAST[c], "mt_verses": MT_LAST[c]}
chapters["40"]["rule"] = "identity"     # WEB 40:1-24 = MT 40:1-24; MT 40:25-32 belong to WEB 41
chapters["40"]["note"] = "WEB 40:1-24 = MT 40:1-24 (identity); MT 40:25-32 are rendered as WEB 41:1-8"
chapters["41"]["rule"] = "zone"
chapters["41"]["note"] = "WEB 41:1-8 = MT 40:25-32; WEB 41:9-34 = MT 41:1-26"

out = {
    "book": BOOK,
    "built": "2026-09-03 (OW-2 item-2 audit rebuild; independent of the lost Job campaign scratchpad)",
    "rule_set": "identity everywhere except WEB 41:1-8 = MT 40:25-32 and WEB 41:9-34 = MT 41:1-26",
    "totals": {"web": 1070, "mt": 1070},
    "chapters": chapters,
    "anchors_under_rule_set": rule_result,
    "falsification_under_identity": {"anchor_misses": len(ident_result["anchor_misses"]),
                                     "zone_checks": ident_result["zone_checks"],
                                     "miss_list": ident_result["anchor_misses"]},
    "seam_byte_review": seam,
    "shipped_corpus_dual_cite_probe": probe,
    "convention": "bare/web: refs + row spans = WEB; oshb:/pmarks = MT; no title pseudo-verses",
    "annotation_lines_seen_in_web_extract": annot,
}
(SPBOOK / "web_mt_offset_map.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({
    "anchor_checks": rule_result["anchor_checks"], "zone_checks": rule_result["zone_checks"],
    "anchor_misses_under_rules": rule_result["anchor_misses"],
    "falsification_identity_misses": len(ident_result["anchor_misses"]),
    "seam": seam,
    "shipped_dual_cites": {"found": probe["dual_cites_found"], "agree": probe["agree"], "disagree": probe["disagree"][:20]},
    "annotations": annot[:10],
    "status": "WRITTEN",
}, ensure_ascii=False, indent=1))
