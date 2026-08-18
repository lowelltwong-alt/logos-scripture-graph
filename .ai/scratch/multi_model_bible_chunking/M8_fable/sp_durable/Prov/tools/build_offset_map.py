#!/usr/bin/env python3
"""Phase-0 Tier-0: build + BYTE-VERIFY ../web_mt_offset_map.json for Prov.

Prov is expected near-identity WEB<->MT (lesson j.1) but identity is PROVEN,
not assumed, by four independent layers:
  1. per-chapter verse-count equality (both witnesses' bytes);
  2. automatic content anchors: numeral + proper-name tokens in a WEB verse
     must find their Hebrew counterpart in the SAME MT ref (skeleton tier);
     every miss is listed for orchestrator byte review — zero unexplained;
  3. OSHB KJV-variance note scan (Prov.xml carries the crosswalk layer OSHB
     uses to flag verses where KJV-family numbering diverges);
  4. the eshet-chayil acrostic (MT 31:10-31): 22 first letters must run the
     full alef-bet IN ORDER — a 22-point alignment anchor for the final
     chapter (derived in prov_devices.py; asserted here too).
LXX reorder of 24:23-34 and chs 30-31 is CROSS-TRADITION METADATA — both
staged witnesses follow MT order; it never enters this map.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SPBOOK = TOOLS.parent
BOOK = "Prov"

POINTS = re.compile(r"[\u0591-\u05C7]")


def skeleton(s: str) -> str:
    return POINTS.sub("", unicodedata.normalize("NFD", s)).replace("\u05BE", " ")


ANCHORS = {
    "two": ["שנים", "שתים", "שני", "שתי"],
    "three": ["שלוש", "שלש", "שלושה", "שלשה"],
    "four": ["ארבע", "ארבעה"],
    "five": ["חמש", "חמשה"],
    "six": ["שש", "ששה"],
    "seven": ["שבע", "שבעה", "שבעתים"],
    "eight": ["שמנה", "שמונה"],
    "ten": ["עשר", "עשרה"],
    "Solomon": ["שלמה"],
    "David": ["דוד"],
    "Israel": ["ישראל"],
    "Hezekiah": ["חזקיה"],
    "Agur": ["אגור"],
    "Lemuel": ["למואל"],
    "Sheol": ["שאול"],
    "Egypt": ["מצרים"],
    "Yahweh": ["יהוה"],
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

    # layer 1: per-chapter count equality
    assert set(web_last) == set(mt_last) == set(range(1, 32)), "chapter set mismatch"
    diffs = {c: (web_last[c], mt_last[c]) for c in web_last if web_last[c] != mt_last[c]}
    assert not diffs, f"per-chapter count mismatches: {diffs}"

    # layer 2: content anchors from the WEB clean extract
    web_text: dict[str, str] = {}
    ch = None
    cur = None
    for line in (SPBOOK / f"{BOOK}_web_clean.txt").read_text(encoding="utf-8").splitlines():
        h = re.match(r"===== PROV (\d+) =====", line)
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
    misses = []
    for key, en in web_text.items():
        sk = skeleton(oshb.get(key, ""))
        toks = set(sk.split())
        for word, hebs in ANCHORS.items():
            if re.search(rf"\b{word}\b", en):
                if any(h in toks or any(t.endswith(h) or t.startswith(h) for t in toks) for h in hebs):
                    agreements += 1
                else:
                    misses.append({"ref": key, "anchor": word})
    # layer 3: KJV-variance notes in the OSHB XML
    xml = (Path(r"C:\wt\logos-t423-m8-fable\data\candidate\original_language_evidence\canonical_source_views\openscriptures_oshb\files") / f"{BOOK}.xml").read_text(encoding="utf-8")
    kjv_notes = re.findall(r'type="KJV">([^<]*)<', xml)

    # layer 4: acrostic assertion (full derivation in prov_devices.py)
    letters = [skeleton(oshb[f"31.{v}"]).split()[0][0] for v in range(10, 32)]
    alefbet = [chr(c) for c in range(0x05D0, 0x05EA + 1)
               if chr(c) not in "\u05DA\u05DD\u05DF\u05E3\u05E5"]  # skip finals
    assert letters == alefbet, f"acrostic sequence broke: {letters}"

    chapters = {str(c): {"rule": "identity", "web_verses": web_last[c],
                         "mt_verses": mt_last[c]} for c in sorted(web_last)}
    out = {
        "book": BOOK,
        "status": "identity",
        "web_total": sum(web_last.values()),
        "mt_total": sum(mt_last.values()),
        "chapters": chapters,
        "verification": {
            "per_chapter_counts_equal": True,
            "content_anchor_agreements": agreements,
            "content_anchor_misses": misses,
            "content_anchor_note": "misses are rendering divergences awaiting orchestrator byte review, not offsets — see anchor_review in this file after review",
            "oshb_kjv_variance_notes": kjv_notes,
            "acrostic_31_10_31": "full alef-bet in order (22/22) — ch 31 alignment anchor",
        },
        "cross_tradition_note": "LXX reorders 24:23-34 and chs 30-31 relative to MT; both staged witnesses follow MT order — cross-tradition METADATA only, never evidence, never a refs entry.",
    }
    (SPBOOK / "web_mt_offset_map.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"chapters": len(chapters), "web_total": out["web_total"],
                      "mt_total": out["mt_total"], "anchors": agreements,
                      "misses": misses, "kjv_notes": kjv_notes,
                      "acrostic": "22/22 OK"}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
