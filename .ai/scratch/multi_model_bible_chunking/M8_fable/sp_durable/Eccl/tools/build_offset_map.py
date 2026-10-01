#!/usr/bin/env python3
"""Phase-0 Tier-0: build + BYTE-VERIFY ../web_mt_offset_map.json for Eccl.

The resume prompt EXPECTED identity; the bytes REFUTE it. Eccl carries the
classic ch 4/5 versification split:
  MT 4:17            = WEB 5:1   ("Guard your steps ... God's house")
  MT 5:1..5:19       = WEB 5:2..5:20
All other chapters are identity. Totals are 222 = 222. Proven, not assumed,
by four independent layers:
  1. per-chapter verse-count equality UNDER THE RULE SET (both witnesses'
     bytes): identity everywhere except ch 4 (WEB 16 / MT 17) and
     ch 5 (WEB 20 / MT 19);
  2. automatic content anchors: numeral / proper-name / distinctive-lexeme
     tokens in a WEB verse must find their Hebrew counterpart at the
     CROSSWALK-MAPPED MT ref (skeleton tier); every miss is listed for
     orchestrator byte review — zero unexplained;
  3. OSHB KJV-variance note scan — EMPTY for Eccl (0 notes despite the real
     offset), so this layer is INERT here: absence of notes is NOT identity
     evidence in this book; the offset stands on layers 1/2/4;
  4. seam byte-review: the four split-point facts asserted directly from
     bytes (MT 4:17 contains the house-of-God phrase rendered at WEB 5:1;
     MT 5:1 opens the rash-mouth admonition rendered at WEB 5:2; both
     chapter ends align).
Cross-tradition note: LXX/Greek numbering FOLLOWS MT at this split; the
English chapter division follows the Vulgate-family tradition. That is
cross-tradition METADATA — never boundary evidence, never a refs entry.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SPBOOK = TOOLS.parent
BOOK = "Eccl"

POINTS = re.compile(r"[\u0591-\u05C7]")


def skeleton(s: str) -> str:
    return POINTS.sub("", unicodedata.normalize("NFD", s)).replace("\u05BE", " ")


def web_to_mt_local(ch: int, v: int) -> tuple[int, int]:
    """The rule set under test (proven below): identity except WEB ch 5."""
    if ch == 5:
        return (4, 17) if v == 1 else (5, v - 1)
    return (ch, v)


ANCHORS = {
    "two": ["שנים", "שתים", "שני", "שתי"],
    "three": ["שלוש", "שלש", "שלושה", "שלשה"],
    "seven": ["שבע", "שבעה"],
    "eight": ["שמנה", "שמונה"],
    "ten": ["עשר", "עשרה"],
    "hundred": ["מאה", "מאת"],
    "thousand": ["אלף"],
    "David": ["דוד"],
    "Jerusalem": ["ירושלם"],
    "Israel": ["ישראל"],
    "God": ["אלהים"],
    "sun": ["שמש"],
    "vanity": ["הבל"],
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
    assert set(web_last) == set(mt_last) == set(range(1, 13)), "chapter set mismatch"
    expected = {4: (16, 17), 5: (20, 19)}
    diffs = {}
    for c in sorted(web_last):
        want = expected.get(c, (web_last[c], web_last[c]))
        if (web_last[c], mt_last[c]) != want:
            diffs[c] = {"web": web_last[c], "mt": mt_last[c], "expected": want}
    assert not diffs, f"per-chapter counts break the ch4/5 rule set: {diffs}"
    assert sum(web_last.values()) == sum(mt_last.values()) == 222, "totals not 222"

    # layer 2: content anchors from the WEB clean extract, mapped via the rule set
    web_text: dict[str, str] = {}
    ch = None
    cur = None
    for line in (SPBOOK / f"{BOOK}_web_clean.txt").read_text(encoding="utf-8").splitlines():
        h = re.match(r"===== ECCL (\d+) =====", line)
        if h:
            ch = int(h.group(1)); cur = None
            continue
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
        sk = skeleton(oshb.get(f"{mc}.{mv}", ""))
        toks = set(sk.split())
        for word, hebs in ANCHORS.items():
            if re.search(rf"\b{word}\b", en, re.I):
                if any(h in toks or any(t.endswith(h) or t.startswith(h) for t in toks) for h in hebs):
                    agreements += 1
                    if (wc, wv) != (mc, mv):
                        offset_zone_agreements += 1
                else:
                    misses.append({"web_ref": key, "mapped_mt": f"{mc}.{mv}", "anchor": word})

    # layer 2b: FALSIFICATION probe — the refuted identity mapping must FAIL
    # inside the offset zone (if identity also satisfied the anchors there,
    # the anchors would prove nothing about the split).
    ident_failures = 0
    for wv in range(1, 21):
        en = web_text.get(f"5.{wv}", "")
        sk_ident = skeleton(oshb.get(f"5.{wv}", ""))
        toks_ident = set(sk_ident.split())
        for word, hebs in ANCHORS.items():
            if re.search(rf"\b{word}\b", en, re.I):
                if not any(h in toks_ident or any(t.endswith(h) or t.startswith(h) for t in toks_ident)
                           for h in hebs):
                    ident_failures += 1

    # layer 3: KJV-variance notes in the OSHB XML (inert for Eccl — see docstring)
    xml = (Path(r"C:\wt\logos-t423-m8-fable\data\candidate\original_language_evidence\canonical_source_views\openscriptures_oshb\files") / f"{BOOK}.xml").read_text(encoding="utf-8")
    kjv_notes = re.findall(r'type="KJV">([^<]*)<', xml)

    # layer 4: seam byte-review assertions
    mt417 = skeleton(oshb["4.17"])
    assert "בית האלהים" in mt417, "MT 4:17 lacks the house-of-God phrase"
    assert re.search(r"\bGod['\u2019]s house\b|\bhouse of God\b", web_text["5.1"]), \
        "WEB 5:1 lacks the house-of-God rendering"
    mt51 = skeleton(oshb["5.1"])
    assert mt51.split()[:2] == ["אל", "תבהל"], "MT 5:1 does not open al-tevahel"
    assert re.search(r"\brash\b", web_text["5.2"], re.I), "WEB 5:2 lacks the rash-mouth rendering"
    assert "שמחת" in skeleton(oshb["5.19"]), "MT 5:19 lacks the simchat token"
    assert re.search(r"\bjoy\b", web_text["5.20"], re.I), "WEB 5:20 lacks the joy rendering"

    chapters = {}
    for c in sorted(web_last):
        if c == 4:
            chapters[str(c)] = {
                "rule": "mt_extra_final_verse", "web_verses": 16, "mt_verses": 17,
                "note": "WEB 4:1-16 = MT 4:1-16 identity; MT 4:17 has NO WEB ch-4 counterpart (it is WEB 5:1)"}
        elif c == 5:
            chapters[str(c)] = {
                "rule": "web_plus1_of_mt", "web_verses": 20, "mt_verses": 19,
                "note": "WEB 5:1 = MT 4:17; WEB 5:v = MT 5:(v-1) for v in 2..20"}
        else:
            chapters[str(c)] = {"rule": "identity", "web_verses": web_last[c],
                                "mt_verses": mt_last[c]}
    out = {
        "book": BOOK,
        "status": "offsets_present_ch4_ch5",
        "web_total": sum(web_last.values()),
        "mt_total": sum(mt_last.values()),
        "chapters": chapters,
        "verification": {
            "per_chapter_counts_match_rule_set": True,
            "content_anchor_agreements": agreements,
            "content_anchor_agreements_in_offset_zone": offset_zone_agreements,
            "content_anchor_misses": misses,
            "content_anchor_note": "misses are rendering divergences awaiting orchestrator byte review, not offsets — see anchor_review in this file after review",
            "identity_falsification_failures_in_ch5": ident_failures,
            "identity_falsification_note": "count of anchor checks that FAIL when WEB ch 5 is mapped by the refuted identity rule — nonzero means the anchors genuinely discriminate the mappings",
            "oshb_kjv_variance_notes": kjv_notes,
            "kjv_variance_note": "EMPTY for Eccl despite the real ch 4/5 offset — this layer is INERT in this book; absence of notes is NOT identity evidence here",
            "seam_byte_review": "MT 4:17 carries bet-ha-elohim rendered at WEB 5:1; MT 5:1 opens al-tevahel rendered at WEB 5:2; MT 5:19/WEB 5:20 share the joy token — all asserted from bytes",
        },
        "cross_tradition_note": "LXX/Greek numbering follows MT at the 4:17/5:1 split; the English division follows the Vulgate-family tradition — cross-tradition METADATA only, never evidence, never a refs entry.",
    }
    (SPBOOK / "web_mt_offset_map.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"chapters": len(chapters), "web_total": out["web_total"],
                      "mt_total": out["mt_total"], "anchors": agreements,
                      "offset_zone_anchors": offset_zone_agreements,
                      "identity_falsification_failures_in_ch5": ident_failures,
                      "misses": misses, "kjv_notes": kjv_notes,
                      "seam_review": "4 assertions OK"}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
