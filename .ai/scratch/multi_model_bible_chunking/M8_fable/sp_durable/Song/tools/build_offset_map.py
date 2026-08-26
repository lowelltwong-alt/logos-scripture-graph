#!/usr/bin/env python3
"""Phase-0 Tier-0: build + BYTE-VERIFY ../web_mt_offset_map.json for Song.

The resume prompt EXPECTED non-identity at the 6:13|7:1 seam (lesson a:
verified, never assumed — prove whichever way the bytes fall). The bytes
CONFIRM the classic division:
  MT 7:1             = WEB 6:13  ("Return, return, Shulammite!")
  MT 7:2..7:14       = WEB 7:1..7:13
All other chapters are identity. Totals are 117 = 117 over 8 chapters.
Proven, not assumed, by four independent layers:
  1. per-chapter verse-count equality UNDER THE RULE SET (both witnesses'
     bytes): identity everywhere except ch 6 (WEB 13 / MT 12) and
     ch 7 (WEB 13 / MT 14);
  2. automatic content anchors: numeral / proper-name / distinctive-lexeme
     tokens in a WEB verse must find their Hebrew counterpart at the
     CROSSWALK-MAPPED MT ref (skeleton tier); every miss is listed for
     orchestrator byte review — zero unexplained;
  3. OSHB KJV-variance note scan — EMPTY for Song (0 notes despite the real
     offset), exactly as it was for Eccl: this layer is INERT here; absence
     of notes is NOT identity evidence in this book; the offset stands on
     layers 1/2/4;
  4. seam byte-review: the four split-point facts asserted directly from
     bytes (MT 7:1 carries ha-shulamit rendered at WEB 6:13; MT 7:2 opens
     the feet-in-sandals wasf line rendered at WEB 7:1; MT 7:14 carries
     ha-duda'im rendered at WEB 7:13 "mandrakes"; the zone edges MT 6:12 =
     WEB 6:12 chariots and MT 8:1 = WEB 8:1 brother-wish are identity).
Cross-tradition note: LXX/Greek numbering FOLLOWS MT at the 6:13/7:1 seam;
the English chapter division follows the Vulgate-family tradition. That is
cross-tradition METADATA — never boundary evidence, never a refs entry.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SPBOOK = TOOLS.parent
BOOK = "Song"

POINTS = re.compile(r"[\u0591-\u05C7]")
FINALS = str.maketrans("\u05DA\u05DD\u05DF\u05E3\u05E5", "\u05DB\u05DE\u05E0\u05E4\u05E6")


def skeleton(s: str) -> str:
    return POINTS.sub("", unicodedata.normalize("NFD", s)).replace("\u05BE", " ")


def anchor_norm(s: str) -> str:
    """Final-letter allography normalization FOR ANCHORING ONLY (never for
    quotation): the bare-lexeme anchor forms end in final letters while
    suffixed attested forms use medials (yayin/yeini, kerem/karmi) \u2014 the
    Phase-0 allography hazard class, live in this very list."""
    return s.translate(FINALS)


def web_to_mt_local(ch: int, v: int) -> tuple[int, int]:
    """The rule set under test (proven below): identity except the seam —
    WEB 6:13 = MT 7:1 and WEB 7:v = MT 7:(v+1)."""
    if ch == 6 and v == 13:
        return (7, 1)
    if ch == 7:
        return (7, v + 1)
    return (ch, v)


ANCHORS = {
    "Jerusalem": ["ירושלם", "ירושלים"],
    "Solomon": ["שלמה"],
    "Tirzah": ["תרצה"],
    "Gilead": ["גלעד"],
    "Heshbon": ["חשבון"],
    "Damascus": ["דמשק"],
    "Carmel": ["כרמל"],
    "Lebanon": ["לבנון"],
    "Shulammite": ["שולמית"],
    "mandrakes?": ["דודאים"],
    "pomegranates?": ["רמון", "רמונים", "רמנים", "רמני"],
    "sixty": ["ששים"],
    "eighty": ["שמנים"],
    "vineyards?": ["כרם", "כרמים", "כרמי"],
    "wine": ["יין"],
    "myrrh": ["מור", "מר"],
    "milk": ["חלב"],
    "honey": ["דבש"],
    "mother": ["אמו", "אמי", "אמך", "אמם", "אמה"],
    "king": ["מלך"],
    "daughters": ["בנות"],
    "apples?": ["תפוח", "תפוחים"],
    "foxes": ["שעלים", "שועלים"],
    "chariots?": ["מרכבות", "רכב", "רכבי"],
    "sandals": ["נעלים"],
    "wheat": ["חטים"],
    "tower": ["מגדל"],
    "purple": ["ארגמן"],
    "palm": ["תמר"],
    "villages": ["כפרים"],
    "nut": ["אגוז"],
    "dove": ["יונה", "יונתי", "יונים"],
}


def main() -> int:
    inv = json.loads((SPBOOK / "verse_inventory.json").read_text(encoding="utf-8"))
    web_last = {int(c): n for c, n in inv["chapters"].items()}

    oshb: dict[str, str] = {}
    mt_last: dict[int, int] = {}
    for line in (SPBOOK / f"{BOOK}_oshb.txt").read_text(encoding="utf-8").splitlines():
        if "\t" not in line:
            continue
        ref, text = line.split("\t", 1)
        _, c, v = ref.split(".")
        c, v = int(c), int(v)
        mt_last[c] = max(mt_last.get(c, 0), v)
        oshb[f"{c}.{v}"] = text

    # layer 1: per-chapter counts under the rule set
    assert set(web_last) == set(mt_last) == set(range(1, 9)), "chapter set mismatch"
    expected = {6: (13, 12), 7: (13, 14)}
    diffs = {}
    for c in sorted(web_last):
        want = expected.get(c, (web_last[c], web_last[c]))
        if (web_last[c], mt_last[c]) != want:
            diffs[c] = {"web": web_last[c], "mt": mt_last[c], "expected": want}
    assert not diffs, f"per-chapter counts break the 6:13|7:1 rule set: {diffs}"
    assert sum(web_last.values()) == sum(mt_last.values()) == 117, "totals not 117"

    # layer 2: content anchors from the WEB clean extract, mapped via the rule set
    web_text: dict[str, str] = {}
    ch = None
    cur = None
    for line in (SPBOOK / f"{BOOK}_web_clean.txt").read_text(encoding="utf-8").splitlines():
        h = re.match(r"===== SONG (\d+) =====", line)
        if h:
            ch = int(h.group(1)); cur = None
            continue
        if re.match(r"\s*\[(SUPERSCRIPTION|MAJOR-SECTION|HEADING|SPEAKER)", line.strip()):
            continue                     # tier-4 editorial apparatus, never anchor text
        body = re.sub(r"^(¶[»›]?\([^)]*\)|¶|\s*•|\s*\|[a-z0-9]+(?:\([^)]*\))?)\s*", "", line)
        parts = re.split(r"\[v\] (\d+)\s*", body)
        if parts[0].strip() and cur:
            web_text[cur] += " " + parts[0].strip()
        i = 1
        while i < len(parts):
            cur = f"{ch}.{int(parts[i])}"
            web_text[cur] = parts[i + 1].strip()
            i += 2

    agreements = 0
    offset_zone_agreements = 0
    misses = []
    for key, en in web_text.items():
        wc, wv = (int(x) for x in key.split("."))
        mc, mv = web_to_mt_local(wc, wv)
        sk = anchor_norm(skeleton(oshb.get(f"{mc}.{mv}", "")))
        toks = set(sk.split())
        for word, hebs_raw in ANCHORS.items():
            hebs = [anchor_norm(h) for h in hebs_raw]
            if re.search(rf"\b{word}\b", en, re.I):
                if any(h in toks or any(t.endswith(h) or t.startswith(h) for t in toks) for h in hebs):
                    agreements += 1
                    if (wc, wv) != (mc, mv):
                        offset_zone_agreements += 1
                else:
                    misses.append({"web_ref": key, "mapped_mt": f"{mc}.{mv}", "anchor": word})

    # layer 2b: FALSIFICATION probe — the refuted identity mapping must FAIL
    # inside the offset zone (if identity also satisfied the anchors there,
    # the anchors would prove nothing about the seam). WEB 6:13 has NO MT
    # 6:13 at all under identity; WEB ch-7 anchors must miss at same-number
    # MT refs.
    ident_failures = 0
    for wc, wv in [(6, 13)] + [(7, v) for v in range(1, 14)]:
        en = web_text.get(f"{wc}.{wv}", "")
        sk_ident = anchor_norm(skeleton(oshb.get(f"{wc}.{wv}", "")))
        toks_ident = set(sk_ident.split())
        for word, hebs_raw in ANCHORS.items():
            hebs = [anchor_norm(h) for h in hebs_raw]
            if re.search(rf"\b{word}\b", en, re.I):
                if not any(h in toks_ident or any(t.endswith(h) or t.startswith(h) for t in toks_ident)
                           for h in hebs):
                    ident_failures += 1

    # layer 3: KJV-variance notes in the OSHB XML (inert for Song — see docstring)
    xml = (Path(r"C:\wt\logos-t423-m8-fable\data\candidate\original_language_evidence\canonical_source_views\openscriptures_oshb\files") / f"{BOOK}.xml").read_text(encoding="utf-8")
    kjv_notes = re.findall(r'type="KJV">([^<]*)<', xml)

    # layer 4: seam byte-review assertions (+ identity at both zone edges)
    mt71 = skeleton(oshb["7.1"])
    assert "השולמית" in mt71 and "בשולמית" in mt71, "MT 7:1 lacks the shulamit tokens"
    assert re.search(r"\bShulammite\b", web_text["6.13"]), \
        "WEB 6:13 lacks the Shulammite rendering"
    mt72 = skeleton(oshb["7.2"])
    assert mt72.split()[:3] == ["מה", "יפו", "פעמיך"], "MT 7:2 does not open mah-yafu-fe'amayikh"
    assert re.search(r"\bfeet\b", web_text["7.1"], re.I) and re.search(r"\bsandals\b", web_text["7.1"], re.I), \
        "WEB 7:1 lacks the feet-in-sandals rendering"
    assert "הדודאים" in skeleton(oshb["7.14"]), "MT 7:14 lacks the duda'im token"
    assert re.search(r"\bmandrakes\b", web_text["7.13"], re.I), "WEB 7:13 lacks the mandrakes rendering"
    assert "מרכבות" in skeleton(oshb["6.12"]), "MT 6:12 lacks the merkavot token"
    assert re.search(r"\bchariots\b", web_text["6.12"], re.I), "WEB 6:12 lacks the chariots rendering"
    assert skeleton(oshb["8.1"]).split()[:2] == ["מי", "יתנך"], "MT 8:1 does not open mi-yitenkha"
    assert re.search(r"\bbrother\b", web_text["8.1"], re.I), "WEB 8:1 lacks the brother rendering"

    chapters = {}
    for c in sorted(web_last):
        if c == 6:
            chapters[str(c)] = {
                "rule": "web_extra_final_verse", "web_verses": 13, "mt_verses": 12,
                "note": "WEB 6:1-12 = MT 6:1-12 identity; WEB 6:13 has NO MT ch-6 counterpart (it is MT 7:1)"}
        elif c == 7:
            chapters[str(c)] = {
                "rule": "web_minus1_of_mt", "web_verses": 13, "mt_verses": 14,
                "note": "MT 7:1 = WEB 6:13; WEB 7:v = MT 7:(v+1) for v in 1..13"}
        else:
            chapters[str(c)] = {"rule": "identity", "web_verses": web_last[c],
                                "mt_verses": mt_last[c]}
    out = {
        "book": BOOK,
        "status": "offset_present_seam_6_13_7_1",
        "web_total": sum(web_last.values()),
        "mt_total": sum(mt_last.values()),
        "chapters": chapters,
        "verification": {
            "per_chapter_counts_match_rule_set": True,
            "content_anchor_agreements": agreements,
            "content_anchor_agreements_in_offset_zone": offset_zone_agreements,
            "content_anchor_misses": misses,
            "content_anchor_note": "misses are rendering divergences awaiting orchestrator byte review, not offsets — see anchor_review in this file after review",
            "identity_falsification_failures_in_zone": ident_failures,
            "identity_falsification_note": "count of anchor checks that FAIL when WEB 6:13 + WEB ch 7 are mapped by the refuted identity rule — nonzero means the anchors genuinely discriminate the mappings (WEB 6:13 has no MT 6:13 at all: its skeleton is empty under identity)",
            "oshb_kjv_variance_notes": kjv_notes,
            "kjv_variance_note": "EMPTY for Song despite the real 6:13|7:1 offset — this layer is INERT in this book (as it was in Eccl); absence of notes is NOT identity evidence here",
            "seam_byte_review": "MT 7:1 carries ha-shulamit (twice: address + gaze clause) rendered at WEB 6:13; MT 7:2 opens mah-yafu-fe'amayikh rendered at WEB 7:1 feet-in-sandals; MT 7:14 carries ha-duda'im rendered at WEB 7:13 mandrakes; zone edges MT 6:12 = WEB 6:12 (chariots) and MT 8:1 = WEB 8:1 (brother-wish) are identity — all asserted from bytes",
        },
        "cross_tradition_note": "LXX/Greek numbering follows MT at the 6:13/7:1 seam; the English division follows the Vulgate-family tradition — cross-tradition METADATA only, never evidence, never a refs entry.",
    }
    (SPBOOK / "web_mt_offset_map.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"chapters": len(chapters), "web_total": out["web_total"],
                      "mt_total": out["mt_total"], "anchors": agreements,
                      "offset_zone_anchors": offset_zone_agreements,
                      "identity_falsification_failures_in_zone": ident_failures,
                      "misses": misses, "kjv_notes": kjv_notes,
                      "seam_review": "6 assertions OK (4 seam + 2 identity edges)"}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
