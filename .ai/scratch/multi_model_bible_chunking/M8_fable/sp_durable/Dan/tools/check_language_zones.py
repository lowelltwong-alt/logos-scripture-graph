#!/usr/bin/env python3
"""Language-zone guard for Dan (FLAGS member; API parity with the Jer and Ezek members).

Dan carries ONE Aramaic island, entered MID-VERSE (../dan_language_zones.json, EXTRACTED from the OSHB morph codes;
dan_lib.py asserts every figure here):
    Hebrew  1:1 - 2:4 word 4     Aramaic  2:4 word 5 - 7:28     Hebrew  8:1 - 12:13
MT 2:4 is the only mixed verse (12 words; the switch falls before word 5: 2:4a Hebrew, 2:4b Aramaic). The island
contains both WEB/MT numbering zones (chapters 3-6), so a ref's language is the same in WEB and MT coordinates and
this guard never converts a ref. "Syrian" is a language label here because WEB 2:4 says "in the Syrian language".

Five arms. Arms 1-3 are the Jer member's, keyed on the zone map instead of one verse; arms 4 and 5 are new, because
a verse-granular tool cannot express the 2:4 boundary.
 1. ARAMAIC LABEL ON A HEBREW VERSE (review candidate): an "Aramaic" or "Syrian" label within 100 chars of a ref in
    1:1-2:3 or 8:1-12:13 (or a ref written Dan.2.4a). Aramaic-INFLUENCE discussion is legitimate (negative
    lookahead), and a field that ENGAGES the island (any island ref, 2:4 included) is exempt: discussing the
    language shift from a Hebrew neighbor is legitimate, labeling a Hebrew VERSE Aramaic is not.
 2. HEBREW LABEL ON AN ARAMAIC VERSE (review candidate): a "Hebrew" grammar label within 60 chars of a ref in
    2:5-7:28 (or Dan.2.4b), with no Aramaic word and no Hebrew-zone ref in the same window. "Hebrew Bible",
    "Hebrew canon" and "Hebrew Scripture(s)" name the corpus, not the language, and are exempt.
 3. ISLAND DISCLOSURE SYMMETRY (rows only): any ROW whose span covers an island verse (2:4-7:28) must say
    "Aramaic" somewhere in the row.
 4. MID-VERSE SWITCH DISCLOSURE (rows only): any ROW whose span covers 2:4 must disclose the switch, by a half
    token (2:4a / 2:4b / Dan.2.4a / Dan.2.4b) or the words mid-verse, switch or "word 5". A row whose span STARTS or
    ENDS at 2:4 must carry a half token: the boundary is inside the verse, and the row must say which half it means.
 5. MID-VERSE QUOTATION (string fields): a field that cites Dan.2.4 and quotes Hebrew-script words of MT 2:4 must
    say which half they come from. The words are located in the verse by consonantal skeleton, never typed: a bare
    Dan.2.4 cite with no half token or switch word is flagged, and a half token that contradicts the half the
    quoted words come from is flagged.
Output contract identical to the Jer and Ezek members: flag_count / flags / status; exit 1 on flags.
Usage: check_language_zones.py file1.json [more...]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dan_lib import (HEB_RUN, LAST_VERSE, MIXED_VERSES, MT_LAST_VERSE, SPBOOK, expand_ref_token, language_of,
                     skeleton)

REFPAT = re.compile(r"\bDan\.(\d+)\.(\d+)([ab](?![A-Za-z]))?")
ARAMAIC = re.compile(r"\bAramaic\b(?!\s*(?:-influenced|influence|ism|izing|coloring|colouring|loan))|\bSyrian\b")
ARAMAIC_WORD = re.compile(r"\bAramaic\b")
HEBREW_LABEL = re.compile(r"\bHebrew\b(?!\s+(?:Bible|canon|Scriptures?)\b)")
RANGE = re.compile(r"(?:oshb:|web:)?Dan\.\d+\.\d+(?:-(?:Dan\.)?\d+(?:\.\d+)?)?")
HALF = re.compile(r"(?:\bDan\.2\.4|(?<![\d:.])2:4)([ab])(?![A-Za-z])")
SWITCH = re.compile(r"\bmid-?verse\b|\bswitch|\bword 5\b", re.I)
BARE_2_4 = re.compile(r"\bDan\.2\.4(?![\dA-Za-z])")

# MT 2:4 words by skeleton, 1-based, with the half each falls in. Fail closed if the extract disagrees with the map.
_V24 = dict(l.split("\t", 1) for l in (SPBOOK / "Dan_oshb.txt").read_text(encoding="utf-8").splitlines())["Dan.2.4"]
_WORDS = [skeleton(w).replace(" ", "") for w in _V24.split(" ")]
_SWITCH = MIXED_VERSES[(2, 4)]["switch_before_word"][0]
if len(_WORDS) != MIXED_VERSES[(2, 4)]["words"] or len(set(_WORDS)) != len(_WORDS):
    raise SystemExit("REFUSED: MT 2:4 in Dan_oshb.txt does not split into the zone map's distinct words")
HALF_OF_WORD = {sk: ("a" if i < _SWITCH else "b") for i, sk in enumerate(_WORDS, start=1)}


def ref_language(c: int, v: int, half: str | None) -> str:
    if (c, v) == (2, 4) and half:
        return "Hebrew" if half == "a" else "Aramaic"
    return language_of(c, v)


def iter_strings(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from iter_strings(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from iter_strings(v, f"{path}[{i}]")
    elif isinstance(o, str):
        yield path, o


def load_any(p: Path):
    text = p.read_text(encoding="utf-8-sig")
    if p.suffix == ".jsonl":
        return [json.loads(l) for l in text.splitlines() if l.strip()]
    return json.loads(text)


def rows_of(data):
    if isinstance(data, list):
        return [r for r in data if isinstance(r, dict)]
    if isinstance(data, dict):
        if "decisions" in data:
            return [r for r in data["decisions"] if isinstance(r, dict)]
        return [v for v in data.values() if isinstance(v, dict)]
    return []


def quoted_halves(s: str) -> set[str]:
    """The halves of MT 2:4 that the field's Hebrew-script words come from (skeleton match, whole words only)."""
    out = set()
    for run in HEB_RUN.findall(s):
        for w in skeleton(run).split():
            if w in HALF_OF_WORD:
                out.add(HALF_OF_WORD[w])
    return out


def main() -> int:
    flags = []
    for f in sys.argv[1:]:
        name = Path(f).name
        data = load_any(Path(f))
        for path, s in iter_strings(data):
            refs = [(int(m.group(1)), int(m.group(2)), m.group(3), m) for m in REFPAT.finditer(s)]
            engages = any(ref_language(c, v, None) != "Hebrew" for c, v, _h, _m in refs)
            for c, v, half, m in refs:
                lang = ref_language(c, v, half)
                ctx = s[max(0, m.start() - 100):m.end() + 100]
                # arm 1
                if lang == "Hebrew" and ARAMAIC.search(ctx) and not engages:
                    flags.append({"file": name, "path": path, "issue": "aramaic_label_on_hebrew_verse",
                                  "note": ("review candidate - Dan's Aramaic is 2:4b-7:28 only; discussing the "
                                           "island from a Hebrew neighbor is legitimate, labeling a Hebrew VERSE "
                                           "Aramaic is not"),
                                  "ref": m.group(0), "context": ctx[:160]})
                # arm 2
                if lang == "Aramaic":
                    lo, hi = max(0, m.start() - 60), m.end() + 60
                    near = s[lo:hi]
                    hebrew_ref_near = any(lo <= m2.start() < hi and ref_language(c2, v2, h2) == "Hebrew"
                                          for c2, v2, h2, m2 in refs)
                    if HEBREW_LABEL.search(near) and not ARAMAIC_WORD.search(near) and not hebrew_ref_near:
                        flags.append({"file": name, "path": path, "issue": "hebrew_label_on_aramaic_verse",
                                      "note": ("review candidate - 2:4b-7:28 is ARAMAIC (byte-proven from the "
                                               "morph codes); a Hebrew grammar label on it is wrong"),
                                      "ref": m.group(0), "context": near[:160]})
            # arm 5
            if BARE_2_4.search(s):
                halves = quoted_halves(s)
                stated = {h for h in HALF.findall(s)}
                if halves and not stated and not SWITCH.search(s):
                    flags.append({"file": name, "path": path, "issue": "mid_verse_quote_half_unstated",
                                  "note": ("the field cites Dan.2.4 and quotes words of MT 2:4 from half(s) %s "
                                           "without saying which half (2:4a Hebrew, 2:4b Aramaic)"
                                           % "+".join(sorted(halves))),
                                  "context": s[:160]})
                elif halves and stated and not halves <= stated:
                    flags.append({"file": name, "path": path, "issue": "mid_verse_quote_half_mismatch",
                                  "note": ("the quoted MT 2:4 words come from half(s) %s but the field states %s"
                                           % ("+".join(sorted(halves)), "+".join(sorted(stated)))),
                                  "context": s[:160]})
        # arms 3 and 4 (rows with spans only)
        for row in rows_of(data):
            span = row.get("span")
            if not isinstance(span, str):
                continue
            pairs = []
            for m in RANGE.finditer(span):
                tok = m.group(0)
                space = MT_LAST_VERSE if tok.startswith("oshb:") else LAST_VERSE
                pairs.extend(expand_ref_token(tok.split(":", 1)[-1], space))
            if not pairs:
                continue
            whole = json.dumps(row, ensure_ascii=False)
            rid = row.get("decision_id", row.get("chunk_id", "?"))
            if any(language_of(c, v) != "Hebrew" for c, v in pairs) and not ARAMAIC_WORD.search(whole):
                flags.append({"file": name, "decision_id": rid, "issue": "aramaic_island_undisclosed",
                              "note": "row span covers the Aramaic island (2:4b-7:28) with no Aramaic disclosure",
                              "span": span})
            if (2, 4) in pairs:
                boundary = pairs[0] == (2, 4) or pairs[-1] == (2, 4)
                if boundary and not HALF.search(whole):
                    flags.append({"file": name, "decision_id": rid, "issue": "mid_verse_boundary_half_unstated",
                                  "note": ("row span starts or ends at 2:4, where the language switches before "
                                           "word 5; the row must say which half it means (2:4a / 2:4b)"),
                                  "span": span})
                elif not boundary and not (HALF.search(whole) or SWITCH.search(whole)):
                    flags.append({"file": name, "decision_id": rid, "issue": "mid_verse_switch_undisclosed",
                                  "note": ("row span covers 2:4, where Hebrew gives way to Aramaic before word 5, "
                                           "and never discloses the mid-verse switch"),
                                  "span": span})
    print(json.dumps({"flag_count": len(flags), "flags": flags,
                      "status": "GREEN" if not flags else "FLAGS"},
                     ensure_ascii=False, indent=1))
    return 1 if flags else 0


if __name__ == "__main__":
    raise SystemExit(main())
