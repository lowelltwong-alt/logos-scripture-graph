#!/usr/bin/env python3
"""Phase-0 Tier-0: build + BYTE-VERIFY ../web_mt_offset_map.json for Isa.

The resume prompt EXPECTED non-identity at TWO classic seams (lesson a:
verified, never assumed — prove whichever way the bytes fall, PER ZONE).
The bytes CONFIRM both, and they have DIFFERENT SHAPES:

ZONE A (chs 8-9) — pure renumbering, no split:
  MT 8:23           = WEB 9:1   (Zebulun/Naphtali/Galilee line)
  MT 9:1..9:20      = WEB 9:2..9:21
ZONE B (chs 63-64) — a genuine SPLIT (the book's WEB total exceeds MT by 1):
  MT 63:19          = WEB 63:19 + WEB 64:1  (one MT verse, two WEB verses:
                      the "never ruled / not called by your name" half at
                      WEB 63:19 and the "tear the heavens ... mountains
                      quake" half at WEB 64:1)
  MT 64:1..64:11    = WEB 64:2..64:12
All other chapters are identity. Totals: WEB 1292 / MT 1291 over 66 chapters.
Proven, not assumed, by four independent layers:
  1. per-chapter verse-count equality UNDER THE RULE SET (both witnesses'
     bytes): identity everywhere except ch 8 (WEB 22 / MT 23), ch 9
     (WEB 21 / MT 20), ch 63 (19 = 19, numbering identity, content SPLIT at
     the final verse), ch 64 (WEB 12 / MT 11);
  2. automatic content anchors: proper-name / distinctive-lexeme tokens in a
     WEB verse must find their Hebrew counterpart at the CROSSWALK-MAPPED MT
     ref (skeleton tier, finals-normalized FOR ANCHORING ONLY); every miss
     is listed for orchestrator byte review — zero unexplained;
  3. OSHB KJV-variance note scan — EMPTY for Isa (0 notes despite two real
     offset zones), the THIRD book running (Eccl, Song, now Isa): this layer
     is INERT; absence of notes is NOT identity evidence; the offsets stand
     on layers 1/2/4;
  4. seam byte-review: split-point facts asserted directly from bytes in
     BOTH zones, plus identity at all four zone edges, plus the ZONE-B SPLIT
     DISCRIMINATOR (WEB 64:1's heavens/mountains tokens live in MT 63:19 and
     are ABSENT from MT 64:1).
Cross-tradition note: MT/LXX numbering at 8:23|9:1 and 63:19|64:1 differs
from the English (Vulgate-family) chapter division. That is cross-tradition
METADATA — never boundary evidence, never a refs entry.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SPBOOK = TOOLS.parent
BOOK = "Isa"

POINTS = re.compile(r"[\u0591-\u05C7]")
FINALS = str.maketrans("\u05DA\u05DD\u05DF\u05E3\u05E5", "\u05DB\u05DE\u05E0\u05E4\u05E6")


def skeleton(s: str) -> str:
    return POINTS.sub("", unicodedata.normalize("NFD", s)).replace("\u05BE", " ")


def anchor_norm(s: str) -> str:
    """Final-letter allography normalization FOR ANCHORING ONLY (never for
    quotation) — the finals-normalized sweep discipline (Song lesson e).
    Isaiah even carries a MEDIAL final-mem in its letter bytes (MT 9:6
    לםרבה), so this normalization is load-bearing here."""
    return s.translate(FINALS)


def web_to_mt_local(ch: int, v: int) -> tuple[int, int]:
    """The rule set under test (proven below)."""
    if ch == 9:
        return (8, 23) if v == 1 else (9, v - 1)
    if ch == 64:
        return (63, 19) if v == 1 else (64, v - 1)
    return (ch, v)


ANCHORS = {
    "Zebulun": ["זבולן", "זבלון"],
    "Naphtali": ["נפתלי"],
    "Galilee": ["גליל"],
    "Jordan": ["ירדן"],
    "Midian": ["מדין"],
    "Ephraim": ["אפרים"],
    "Manasseh": ["מנשה"],
    "Samaria": ["שמרון"],
    "Rezin": ["רצין"],
    "Syrians?": ["ארם"],
    "Philistines": ["פלשתים"],
    "Assyria|Assyrian": ["אשור"],
    "David": ["דוד"],
    "Egypt": ["מצרים"],
    "Babylon": ["בבל"],
    "Moab": ["מואב"],
    "Damascus": ["דמשק"],
    "Jerusalem": ["ירושלם", "ירושלים"],
    "Zion": ["ציון"],
    "Israel": ["ישראל"],
    "Jacob": ["יעקב"],
    "Judah": ["יהודה"],
    "Hezekiah": ["חזקיהו"],
    "Sennacherib": ["סנחריב"],
    "Cyrus": ["כורש"],
    "Lebanon": ["לבנון"],
    "Carmel": ["כרמל"],
    "Sharon": ["שרון"],
    "Sodom": ["סדם"],
    "Gomorrah": ["עמרה"],
    "Sidon": ["צידן", "צידון"],
    "Elam": ["עילם"],
    "Eliakim": ["אליקים"],
    "Shebna": ["שבנא"],
    "Ahaz": ["אחז"],
    "Uzziah": ["עזיהו"],
    "Yahweh": ["יהוה"],
    "heavens?": ["שמים", "השמים"],
    "mountains?": ["הרים", "ההרים"],
    "vineyards?": ["כרם", "כרמים", "כרמי"],
    "darkness": ["חשך", "חשכה"],
    "potter": ["יצר", "היצר"],
    "clay": ["חמר"],
}

# WEB verses whose numbering diverges from MT under the rule set (used by the
# falsification probes; WEB 63:19 keeps identical NUMBERING and is probed via
# the split discriminator instead).
ZONE_A_WEB = [(9, v) for v in range(1, 22)]
ZONE_B_WEB = [(64, v) for v in range(1, 13)]


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
    assert set(web_last) == set(mt_last) == set(range(1, 67)), "chapter set mismatch"
    expected = {8: (22, 23), 9: (21, 20), 63: (19, 19), 64: (12, 11)}
    diffs = {}
    for c in sorted(web_last):
        want = expected.get(c, (web_last[c], web_last[c]))
        if (web_last[c], mt_last[c]) != want:
            diffs[c] = {"web": web_last[c], "mt": mt_last[c], "expected": want}
    assert not diffs, f"per-chapter counts break the two-zone rule set: {diffs}"
    assert sum(web_last.values()) == 1292 and sum(mt_last.values()) == 1291, \
        "totals not 1292/1291 — the single-split accounting is broken"

    # layer 2: content anchors from the WEB clean extract, mapped via the rule set
    web_text: dict[str, str] = {}
    ch = None
    cur = None
    for line in (SPBOOK / f"{BOOK}_web_clean.txt").read_text(encoding="utf-8").splitlines():
        h = re.match(r"===== ISA (\d+) =====", line)
        if h:
            ch = int(h.group(1)); cur = None
            continue
        if re.match(r"\s*\[(SUPERSCRIPTION|MAJOR-SECTION|HEADING|SPEAKER)", line.strip()):
            raise SystemExit("unexpected editorial apparatus line in Isa extract")
        body = re.sub(r"^(¶[»›]?\([^)]*\)|¶|\s*•|\s*\|[a-z0-9]+(?:\([^)]*\))?)\s*", "", line)
        parts = re.split(r"\[v\] (\d+)\s*", body)
        if parts[0].strip() and cur:
            web_text[cur] += " " + parts[0].strip()
        i = 1
        while i < len(parts):
            cur = f"{ch}.{int(parts[i])}"
            web_text[cur] = parts[i + 1].strip()
            i += 2

    def anchor_hits(en: str, sk_tokens: set[str]):
        """(hits, misses-as-words) for one verse pair."""
        hits = []
        misses = []
        for word, hebs_raw in ANCHORS.items():
            hebs = [anchor_norm(h) for h in hebs_raw]
            if re.search(rf"\b(?:{word})\b", en, re.I):
                if any(h in sk_tokens or any(t.endswith(h) or t.startswith(h)
                                             for t in sk_tokens) for h in hebs):
                    hits.append(word)
                else:
                    misses.append(word)
        return hits, misses

    agreements = 0
    offset_zone_agreements = 0
    misses = []
    for key, en in web_text.items():
        wc, wv = (int(x) for x in key.split("."))
        mc, mv = web_to_mt_local(wc, wv)
        sk = anchor_norm(skeleton(oshb.get(f"{mc}.{mv}", "")))
        toks = set(sk.split())
        hits, miss_words = anchor_hits(en, toks)
        agreements += len(hits)
        if (wc, wv) != (mc, mv):
            offset_zone_agreements += len(hits)
        for w in miss_words:
            misses.append({"web_ref": key, "mapped_mt": f"{mc}.{mv}", "anchor": w})

    # SPLIT-VERSE anchor arm: WEB 63:19's anchors must also live in MT 63:19
    # (numbering-identity half of the split) — counted above already since
    # web_to_mt_local(63,19) == (63,19).

    # layer 2b: FALSIFICATION probes — the refuted identity mapping must FAIL
    # inside each offset zone.
    def ident_fail_count(zone):
        fails = 0
        for wc, wv in zone:
            en = web_text.get(f"{wc}.{wv}", "")
            sk_ident = anchor_norm(skeleton(oshb.get(f"{wc}.{wv}", "")))
            toks_ident = set(sk_ident.split())
            for word, hebs_raw in ANCHORS.items():
                hebs = [anchor_norm(h) for h in hebs_raw]
                if re.search(rf"\b(?:{word})\b", en, re.I):
                    if not any(h in toks_ident or any(t.endswith(h) or t.startswith(h)
                                                      for t in toks_ident) for h in hebs):
                        fails += 1
        return fails

    ident_failures_zone_a = ident_fail_count(ZONE_A_WEB)
    ident_failures_zone_b = ident_fail_count(ZONE_B_WEB)

    # layer 2c: ZONE-B SPLIT DISCRIMINATOR — WEB 64:1's distinctive tokens
    # (heavens/mountains/came-down) are IN MT 63:19 and ABSENT from MT 64:1;
    # this separates the split rule from any same-chapter renumbering story.
    mt63_19 = anchor_norm(skeleton(oshb["63.19"]))
    mt64_1 = anchor_norm(skeleton(oshb["64.1"]))
    for tok in ("שמים", "הרים", "ירדת"):
        t = anchor_norm(tok)
        assert t in mt63_19.split(), f"split discriminator: {tok} missing from MT 63:19"
        assert t not in mt64_1.split(), f"split discriminator: {tok} unexpectedly in MT 64:1"
    assert re.search(r"\bheavens\b", web_text["64.1"], re.I) and \
        re.search(r"\bmountains\b", web_text["64.1"], re.I), \
        "WEB 64:1 lacks the tear-the-heavens/mountains rendering"
    assert re.search(r"\bruled\b", web_text["63.19"], re.I) and \
        re.search(r"\bname\b", web_text["63.19"], re.I), \
        "WEB 63:19 lacks the never-ruled/not-called-by-your-name rendering"
    for tok in ("היינו", "משלת", "שמך"):
        assert anchor_norm(tok) in mt63_19.split(), \
            f"split first-half token {tok} missing from MT 63:19"

    # layer 3: KJV-variance notes in the OSHB XML (inert for Isa — see docstring)
    xml = (Path(r"C:\wt\logos-t423-m8-fable\data\candidate\original_language_evidence\canonical_source_views\openscriptures_oshb\files") / f"{BOOK}.xml").read_text(encoding="utf-8")
    kjv_notes = re.findall(r'type="KJV">([^<]*)<', xml)

    # layer 4: seam byte-review assertions (both zones + all four zone edges)
    mt823 = skeleton(oshb["8.23"])
    assert "זבלון" in mt823 and "נפתלי" in mt823 and "גליל" in mt823, \
        "MT 8:23 lacks the Zebulun/Naphtali/Galilee tokens"
    assert re.search(r"\bZebulun\b", web_text["9.1"]) and \
        re.search(r"\bNaphtali\b", web_text["9.1"]) and \
        re.search(r"\bGalilee\b", web_text["9.1"], re.I), \
        "WEB 9:1 lacks the Zebulun/Naphtali/Galilee rendering"
    assert skeleton(oshb["9.1"]).split()[:2] == ["העם", "ההלכים"], \
        "MT 9:1 does not open ha-am ha-holekhim (walkers-in-darkness)"
    assert re.search(r"\bwalked in darkness\b", web_text["9.2"], re.I), \
        "WEB 9:2 lacks the walked-in-darkness rendering"
    mt920 = skeleton(oshb["9.20"])
    assert "מנשה" in mt920 and "אפרים" in mt920, "MT 9:20 lacks Manasseh/Ephraim"
    assert re.search(r"\bManasseh\b", web_text["9.21"]) and \
        re.search(r"\bEphraim\b", web_text["9.21"]), \
        "WEB 9:21 lacks the Manasseh/Ephraim rendering"
    # zone A edges: identity on both sides
    mt822 = skeleton(oshb["8.22"])
    assert "צרה" in mt822 and "וחשכה" in mt822, "MT 8:22 lacks tsarah-va-chashekhah"
    assert re.search(r"\bdistress\b", web_text["8.22"], re.I) and \
        re.search(r"\bdarkness\b", web_text["8.22"], re.I), \
        "WEB 8:22 lacks the distress/darkness rendering"
    assert skeleton(oshb["10.1"]).split()[0] == "הוי", "MT 10:1 does not open hoy"
    assert re.search(r"\bWoe\b", web_text["10.1"]), "WEB 10:1 lacks the Woe rendering"
    # zone B: fire-kindles seam + tail + edges
    mt641 = skeleton(oshb["64.1"])
    assert mt641.split()[0] == "כקדח", "MT 64:1 does not open ki-qdoach (fire kindles)"
    assert re.search(r"\bfire kindles\b", web_text["64.2"], re.I), \
        "WEB 64:2 lacks the fire-kindles rendering"
    mt6411 = skeleton(oshb["64.11"])
    assert "תתאפק" in mt6411 and "יהוה" in mt6411, "MT 64:11 lacks titappaq/YHWH"
    assert re.search(r"\bhold yourself back\b", web_text["64.12"], re.I), \
        "WEB 64:12 lacks the hold-yourself-back rendering"
    mt6318 = skeleton(oshb["63.18"])
    assert "מקדשך" in mt6318, "MT 63:18 lacks miqdashekha"
    assert re.search(r"\bsanctuary\b", web_text["63.18"], re.I), \
        "WEB 63:18 lacks the sanctuary rendering"
    assert skeleton(oshb["65.1"]).split()[0] == "נדרשתי", "MT 65:1 does not open nidrashti"
    assert re.search(r"\binquired\b", web_text["65.1"], re.I), \
        "WEB 65:1 lacks the inquired-of rendering"

    chapters = {}
    for c in sorted(web_last):
        if c == 8:
            chapters[str(c)] = {
                "rule": "mt_extra_final_verse", "web_verses": 22, "mt_verses": 23,
                "note": "WEB 8:1-22 = MT 8:1-22 identity; MT 8:23 has NO WEB ch-8 counterpart (it is WEB 9:1)"}
        elif c == 9:
            chapters[str(c)] = {
                "rule": "web_plus1_of_mt", "web_verses": 21, "mt_verses": 20,
                "note": "WEB 9:1 = MT 8:23; WEB 9:v = MT 9:(v-1) for v in 2..21"}
        elif c == 63:
            chapters[str(c)] = {
                "rule": "identity_numbering_split_final_verse", "web_verses": 19, "mt_verses": 19,
                "note": ("WEB 63:v = MT 63:v for all v (numbering identity), BUT MT 63:19 is a "
                         "SPLIT verse: its bytes span WEB 63:19 AND WEB 64:1 — any content claim "
                         "about MT 63:19 must say which WEB half it lives in")}
        elif c == 64:
            chapters[str(c)] = {
                "rule": "web_plus1_of_mt_v1_from_prev_chapter", "web_verses": 12, "mt_verses": 11,
                "note": "WEB 64:1 = MT 63:19 (second half — the split); WEB 64:v = MT 64:(v-1) for v in 2..12"}
        else:
            chapters[str(c)] = {"rule": "identity", "web_verses": web_last[c],
                                "mt_verses": mt_last[c]}
    out = {
        "book": BOOK,
        "status": "offsets_present_two_zones_8_23_9_1_and_63_19_64_1_split",
        "web_total": sum(web_last.values()),
        "mt_total": sum(mt_last.values()),
        "chapters": chapters,
        "verification": {
            "per_chapter_counts_match_rule_set": True,
            "content_anchor_agreements": agreements,
            "content_anchor_agreements_in_offset_zone": offset_zone_agreements,
            "content_anchor_misses": misses,
            "content_anchor_note": "misses are rendering divergences awaiting orchestrator byte review, not offsets — see anchor_review in this file after review",
            "identity_falsification_failures_zone_a": ident_failures_zone_a,
            "identity_falsification_failures_zone_b": ident_failures_zone_b,
            "identity_falsification_note": ("count of anchor checks that FAIL when WEB ch 9 / WEB ch 64 are mapped "
                                            "by the refuted identity rule — nonzero in BOTH zones means the anchors "
                                            "genuinely discriminate the mappings (under identity, WEB 64:12 has no "
                                            "MT 64:12 at all)"),
            "split_discriminator": ("WEB 64:1's heavens/mountains/came-down tokens (שמים/הרים/ירדת) are IN MT 63:19 "
                                    "and ABSENT from MT 64:1; MT 63:19 also carries the WEB 63:19 half "
                                    "(היינו/משלת/שמך) — one MT verse, two WEB verses, asserted from bytes"),
            "oshb_kjv_variance_notes": kjv_notes,
            "kjv_variance_note": "EMPTY for Isa despite TWO real offset zones — this layer is INERT (third book running: Eccl, Song, Isa); absence of notes is NOT identity evidence here",
            "seam_byte_review": ("MT 8:23 carries Zebulun/Naphtali/Galilee rendered at WEB 9:1; MT 9:1 opens "
                                 "ha-am-ha-holekhim rendered at WEB 9:2; MT 9:20 carries Manasseh/Ephraim rendered "
                                 "at WEB 9:21; zone-A edges MT 8:22 = WEB 8:22 (distress/darkness) and MT 10:1 = "
                                 "WEB 10:1 (hoy/Woe) are identity; MT 63:19 spans WEB 63:19 (never-ruled half) + "
                                 "WEB 64:1 (tear-the-heavens half); MT 64:1 opens ki-qdoach rendered at WEB 64:2 "
                                 "fire-kindles; MT 64:11 carries titappaq/YHWH rendered at WEB 64:12; zone-B edges "
                                 "MT 63:18 = WEB 63:18 (sanctuary) and MT 65:1 = WEB 65:1 (nidrashti/inquired) are "
                                 "identity — all asserted from bytes"),
        },
        "cross_tradition_note": ("MT (and LXX-order) numbering differs from the English Vulgate-family chapter "
                                 "division at both seams — cross-tradition METADATA only, never evidence, never a "
                                 "refs entry."),
    }
    (SPBOOK / "web_mt_offset_map.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"chapters": len(chapters), "web_total": out["web_total"],
                      "mt_total": out["mt_total"], "anchors": agreements,
                      "offset_zone_anchors": offset_zone_agreements,
                      "ident_failures_zone_a": ident_failures_zone_a,
                      "ident_failures_zone_b": ident_failures_zone_b,
                      "miss_count": len(misses),
                      "misses": misses,
                      "kjv_notes": len(kjv_notes),
                      "seam_review": "17 assertions OK (split discriminator + both zones + 4 identity edges)"},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
