#!/usr/bin/env python3
"""Phase-0 Tier-0: build + BYTE-VERIFY ../web_mt_offset_map.json for Jer.

The resume prompt ordered the landscape PROBED, never assumed (Jer's
versification is famously divergent across TRADITIONS - LXX order/length -
but our two witnesses are WEB and MT, and cross-tradition divergence proves
nothing about THIS pair). The bytes settle it: EXACTLY ONE offset zone,
pure renumbering, NO split anywhere:

ZONE (chs 8-9) - pure renumbering:
  MT 8:23           = WEB 9:1   ("Oh that my head were waters ... spring of
                                  tears" - the weeping-prophet line)
  MT 9:1..9:25      = WEB 9:2..9:26
All other chapters are identity. Totals: WEB 1364 / MT 1364 over 52
chapters - EQUAL totals, which arithmetically EXCLUDES any Isa-zone-B-style
split (a split forces WEB > MT). Proven, not assumed, by four independent
layers:
  1. per-chapter verse-count equality UNDER THE RULE SET (both witnesses'
     bytes): identity everywhere except ch 8 (WEB 22 / MT 23) and ch 9
     (WEB 26 / MT 25);
  2. automatic content anchors: proper-name / distinctive-lexeme tokens in a
     WEB verse must find their Hebrew counterpart at the CROSSWALK-MAPPED MT
     ref (skeleton tier, finals-normalized FOR ANCHORING ONLY); every miss
     is listed for orchestrator byte review - zero unexplained;
  3. OSHB KJV-variance note scan - EMPTY for Jer (0 notes despite a real
     offset zone), the FOURTH book running (Eccl, Song, Isa, Jer): this
     layer is INERT; absence of notes is NOT identity evidence; the offset
     stands on layers 1/2/4;
  4. seam byte-review: seam facts asserted directly from bytes, plus
     identity at both zone edges (MT 8:22 = WEB 8:22 balm-in-Gilead;
     MT 10:1 = WEB 10:1 hear-the-word).
Cross-tradition note: LXX Jeremiah is ~1/8 shorter with the
oracles-against-nations block placed after 25:13 and re-ordered; 4QJer-b/d
attest a short Hebrew text type. That is cross-tradition METADATA - never
boundary evidence, never a refs entry - and does NOT touch the WEB/MT pair.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SPBOOK = TOOLS.parent
BOOK = "Jer"

POINTS = re.compile(r"[\u0591-\u05C7]")
FINALS = str.maketrans("\u05DA\u05DD\u05DF\u05E3\u05E5", "\u05DB\u05DE\u05E0\u05E4\u05E6")


def skeleton(s: str) -> str:
    return POINTS.sub("", unicodedata.normalize("NFD", s)).replace("\u05BE", " ")


def anchor_norm(s: str) -> str:
    """Final-letter allography normalization FOR ANCHORING ONLY (never for
    quotation) - the finals-normalized sweep discipline (E-11)."""
    return s.translate(FINALS)


def web_to_mt_local(ch: int, v: int) -> tuple[int, int]:
    """The rule set under test (proven below)."""
    if ch == 9:
        return (8, 23) if v == 1 else (9, v - 1)
    return (ch, v)


ANCHORS = {
    "Jeremiah": ["ירמיהו", "ירמיה"],       # BOTH spellings attested in Jer
    "Baruch": ["ברוך"],
    "Nebuchadnezzar|Nebuchadrezzar": ["נבוכדראצר", "נבוכדנאצר"],  # both attested
    "Zedekiah": ["צדקיהו", "צדקיה"],
    "Jehoiakim": ["יהויקים"],
    "Josiah": ["יאשיהו"],
    "Hananiah": ["חנניה"],
    "Pashhur": ["פשחור"],
    "Anathoth": ["ענתות"],
    "Gilead": ["גלעד"],
    "Euphrates": ["פרת"],
    "Chaldeans": ["כשדים"],
    "Babylon": ["בבל"],
    "Egypt": ["מצרים"],
    "Moab": ["מואב"],
    "Edom": ["אדום"],
    "Ammon": ["עמון"],
    "Damascus": ["דמשק"],
    "Hazor": ["חצור"],
    "Elam": ["עילם"],
    "Jerusalem": ["ירושלם"],
    "Zion": ["ציון"],
    "Israel": ["ישראל"],
    "Jacob": ["יעקב"],
    "Judah": ["יהודה"],
    "David": ["דוד"],
    "Rachel": ["רחל"],
    "Samaria": ["שמרון"],
    "Ephraim": ["אפרים"],
    "Yahweh": ["יהוה"],
    "heavens?": ["שמים", "השמים"],
    "potters?": ["יוצר", "היוצר"],
    "balm": ["צרי"],
    "tears": ["דמעה"],
    "wormwood": ["לענה"],
    "windows?": ["חלונינו"],
    "wilderness": ["מדבר", "במדבר"],
    "wine": ["יין"],
    "sword": ["חרב"],
    "famine": ["רעב"],
    "shepherds?": ["רעים", "הרעים", "רעי"],
}

# WEB verses whose numbering diverges from MT under the rule set (used by
# the falsification probes).
ZONE_WEB = [(9, v) for v in range(1, 27)]


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
    assert set(web_last) == set(mt_last) == set(range(1, 53)), "chapter set mismatch"
    expected = {8: (22, 23), 9: (26, 25)}
    diffs = {}
    for c in sorted(web_last):
        want = expected.get(c, (web_last[c], web_last[c]))
        if (web_last[c], mt_last[c]) != want:
            diffs[c] = {"web": web_last[c], "mt": mt_last[c], "expected": want}
    assert not diffs, f"per-chapter counts break the one-zone rule set: {diffs}"
    assert sum(web_last.values()) == 1364 and sum(mt_last.values()) == 1364, \
        "totals not 1364/1364 - the pure-renumbering accounting is broken"

    # layer 2: content anchors from the WEB clean extract, mapped via the rule set
    web_text: dict[str, str] = {}
    ch = None
    cur = None
    for line in (SPBOOK / f"{BOOK}_web_clean.txt").read_text(encoding="utf-8").splitlines():
        h = re.match(r"===== JER (\d+) =====", line)
        if h:
            ch = int(h.group(1)); cur = None
            continue
        if re.match(r"\s*\[(SUPERSCRIPTION|MAJOR-SECTION|HEADING|SPEAKER)", line.strip()):
            raise SystemExit("unexpected editorial apparatus line in Jer extract")
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

    # layer 2b: FALSIFICATION probes - the refuted identity mapping must FAIL
    # inside the offset zone.
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

    ident_failures_zone = ident_fail_count(ZONE_WEB)

    # layer 2c: NO-SPLIT DISCRIMINATOR - equal totals already exclude a split
    # arithmetically; additionally the zone's LAST verses align 1:1 (WEB 9:26's
    # nations list lives in MT 9:25 and MT 9:25 has no residual second WEB
    # verse - ch 10 opens at identity on both sides).
    mt925 = anchor_norm(skeleton(oshb["9.25"]))
    for tok in ("מצרים", "אדום", "מואב"):
        assert anchor_norm(tok) in mt925.split(), f"nations-list token {tok} missing from MT 9:25"
    assert re.search(r"\bEgypt\b", web_text["9.26"]) and \
        re.search(r"\bEdom\b", web_text["9.26"]) and \
        re.search(r"\bMoab\b", web_text["9.26"]), \
        "WEB 9:26 lacks the Egypt/Edom/Moab nations rendering"

    # layer 3: KJV-variance notes in the OSHB XML (inert for Jer - see docstring)
    xml = (Path(r"C:\wt\logos-t423-m8-fable\data\candidate\original_language_evidence\canonical_source_views\openscriptures_oshb\files") / f"{BOOK}.xml").read_text(encoding="utf-8")
    kjv_notes = re.findall(r'type="KJV">([^<]*)<', xml)

    # layer 4: seam byte-review assertions (the zone + both zone edges)
    mt823 = skeleton(oshb["8.23"])
    assert "ראשי" in mt823 and "מים" in mt823 and "דמעה" in mt823, \
        "MT 8:23 lacks the head/waters/tears tokens"
    assert re.search(r"\bhead were waters\b", web_text["9.1"], re.I) and \
        re.search(r"\btears\b", web_text["9.1"], re.I), \
        "WEB 9:1 lacks the head-were-waters/tears rendering"
    mt91 = skeleton(oshb["9.1"])
    assert mt91.split()[:2] == ["מי", "יתנני"], \
        "MT 9:1 does not open mi-yitteneni (lodging-place wish)"
    assert re.search(r"\blodging place\b", web_text["9.2"], re.I) and \
        re.search(r"\bwilderness\b", web_text["9.2"], re.I), \
        "WEB 9:2 lacks the lodging-place/wilderness rendering"
    mt920 = skeleton(oshb["9.20"])
    assert "בחלונינו" in mt920.split(), "MT 9:20 lacks be-challoneinu (our windows)"
    assert re.search(r"\bwindows\b", web_text["9.21"], re.I), \
        "WEB 9:21 lacks the windows rendering"
    mt916 = skeleton(oshb["9.16"])
    assert "למקוננות" in mt916.split(), "MT 9:16 lacks la-meqonenot (mourning women)"
    assert re.search(r"\bmourning women\b", web_text["9.17"], re.I), \
        "WEB 9:17 lacks the mourning-women rendering"
    # zone edges: identity on both sides
    mt822 = skeleton(oshb["8.22"])
    assert "בגלעד" in mt822.split() and "צרי" in anchor_norm(mt822), \
        "MT 8:22 lacks the balm-in-Gilead tokens"
    assert re.search(r"\bbalm in Gilead\b", web_text["8.22"], re.I), \
        "WEB 8:22 lacks the balm-in-Gilead rendering"
    mt101 = skeleton(oshb["10.1"])
    assert mt101.split()[0] == "שמעו" and "ישראל" in mt101.split(), \
        "MT 10:1 does not open shim'u ... beit Yisrael"
    assert re.search(r"\bHear the word\b", web_text["10.1"], re.I) and \
        re.search(r"\bIsrael\b", web_text["10.1"]), \
        "WEB 10:1 lacks the hear-the-word/Israel rendering"
    # the Aramaic island sits at IDENTITY numbering on both sides
    mt1011 = skeleton(oshb["10.11"])
    assert mt1011.split()[0] == "כדנה" and "ארעא" in anchor_norm(mt1011), \
        "MT 10:11 does not carry the Aramaic kidnah/ar'a tokens"
    assert re.search(r"\bgods\b", web_text["10.11"], re.I) and \
        re.search(r"\bperish\b", web_text["10.11"], re.I), \
        "WEB 10:11 lacks the gods-shall-perish rendering"

    chapters = {}
    for c in sorted(web_last):
        if c == 8:
            chapters[str(c)] = {
                "rule": "mt_extra_final_verse", "web_verses": 22, "mt_verses": 23,
                "note": "WEB 8:1-22 = MT 8:1-22 identity; MT 8:23 has NO WEB ch-8 counterpart (it is WEB 9:1)"}
        elif c == 9:
            chapters[str(c)] = {
                "rule": "web_plus1_of_mt", "web_verses": 26, "mt_verses": 25,
                "note": "WEB 9:1 = MT 8:23; WEB 9:v = MT 9:(v-1) for v in 2..26"}
        else:
            chapters[str(c)] = {"rule": "identity", "web_verses": web_last[c],
                                "mt_verses": mt_last[c]}
    out = {
        "book": BOOK,
        "status": "offsets_present_one_zone_8_23_9_1_pure_renumbering_no_split",
        "web_total": sum(web_last.values()),
        "mt_total": sum(mt_last.values()),
        "chapters": chapters,
        "verification": {
            "per_chapter_counts_match_rule_set": True,
            "content_anchor_agreements": agreements,
            "content_anchor_agreements_in_offset_zone": offset_zone_agreements,
            "content_anchor_misses": misses,
            "content_anchor_note": "misses are rendering divergences awaiting orchestrator byte review, not offsets - see anchor_review in this file after review",
            "identity_falsification_failures_zone": ident_failures_zone,
            "identity_falsification_note": ("count of anchor checks that FAIL when WEB ch 9 is mapped by the "
                                            "refuted identity rule - nonzero means the anchors genuinely "
                                            "discriminate the mappings (under identity WEB 9:26 has NO MT 9:26 "
                                            "at all)"),
            "no_split_discriminator": ("EQUAL totals (1364 = 1364) arithmetically exclude any split; the zone's "
                                       "last verses align 1:1 (WEB 9:26's Egypt/Edom/Moab nations list lives in "
                                       "MT 9:25; ch 10 opens at identity on both sides) - asserted from bytes"),
            "oshb_kjv_variance_notes": kjv_notes,
            "kjv_variance_note": "EMPTY for Jer despite a real offset zone - this layer is INERT (fourth book running: Eccl, Song, Isa, Jer); absence of notes is NOT identity evidence here",
            "seam_byte_review": ("MT 8:23 carries head/waters/tears rendered at WEB 9:1; MT 9:1 opens "
                                 "mi-yitteneni rendered at WEB 9:2 lodging-place; MT 9:16 carries la-meqonenot "
                                 "rendered at WEB 9:17 mourning-women; MT 9:20 carries be-challoneinu rendered "
                                 "at WEB 9:21 windows; MT 9:25 carries the Egypt/Edom/Moab list rendered at "
                                 "WEB 9:26; zone edges MT 8:22 = WEB 8:22 (balm-in-Gilead) and MT 10:1 = "
                                 "WEB 10:1 (hear-the-word) are identity; the Aramaic island MT 10:11 = WEB "
                                 "10:11 sits at identity numbering - all asserted from bytes"),
        },
        "cross_tradition_note": ("LXX Jeremiah is ~1/8 shorter with the oracles-against-nations block placed "
                                 "after 25:13 and internally re-ordered; 4QJer-b/d attest a short Hebrew text "
                                 "type. Cross-tradition METADATA only - never evidence, never a refs entry; "
                                 "the WEB/MT pair diverges ONLY at the chs 8-9 seam."),
    }
    (SPBOOK / "web_mt_offset_map.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"chapters": len(chapters), "web_total": out["web_total"],
                      "mt_total": out["mt_total"], "anchors": agreements,
                      "offset_zone_anchors": offset_zone_agreements,
                      "ident_failures_zone": ident_failures_zone,
                      "miss_count": len(misses),
                      "misses": misses,
                      "kjv_notes": len(kjv_notes),
                      "seam_review": "assertions OK (one-zone seam + both identity edges + nations-list tail + Aramaic island)"},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
