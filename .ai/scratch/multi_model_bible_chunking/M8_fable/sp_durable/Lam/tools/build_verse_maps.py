#!/usr/bin/env python3
"""Build verse_map_web.json, verse_map_oshb.json, consonantal_index.json for
Lam (run ONCE by the orchestrator at staging; agents consume the JSONs).

Lam specifics: IDENTITY numbering (no zone, no split); Hebrew throughout; the acrostic spine of chs 1-4 is pinned from bytes into verse_map_oshb (acrostic_letter / acrostic_position) and acrostic_spine.json; paragraph-continuation folding + the raw-vs-folded token audit unchanged.
"""
from __future__ import annotations

import json
import re
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from lam_lib import (BOOK, LAST_VERSE, MT_LAST_VERSE, SPBOOK, TOOLS,
                     language_of, mt_to_web, mt_to_web_all, nfd, norm_english,
                     skeleton, strip_accents, web_to_mt)


def build_web():
    raw = (SPBOOK / f"{BOOK}_web_clean.txt").read_text(encoding="utf-8")
    verses: dict[str, dict] = {}
    ch = None
    cur = None
    para_pending = False
    for line in raw.splitlines():
        line = line.rstrip()
        if not line:
            continue
        h = re.match(r"===== LAM (\d+) =====", line)
        if h:
            ch = int(h.group(1)); cur = None; para_pending = False
            continue
        assert not re.match(r"\[(SUPERSCRIPTION|MAJOR-SECTION|HEADING|SPEAKER)", line.strip()), \
            f"unexpected structural annotation in Lam extract: {line[:60]}"
        body = line
        opened_para = False
        opened_poetry = 0
        m = re.match(r"^(Â¶[Â»â€º]?\([^)]*\)|Â¶|\s*â€¢|\s*\|[a-z0-9]+(?:\([^)]*\))?)\s*(.*)$", line)
        if m:
            opened_para = line.lstrip().startswith("Â¶")
            if re.match(r"^\s*\|q[123]", line):
                opened_poetry = 1
            body = m.group(2)
        parts = re.split(r"\[v\] (\d+)\s*", body)
        if parts[0].strip() and cur:
            verses[cur]["text"] += " " + parts[0].strip()
            if opened_para:
                verses[cur]["continuation_paragraphs"] += 1
            if opened_poetry:
                verses[cur]["poetry_lines"] += 1
        elif not parts[0].strip() and opened_para and len(parts) > 1:
            para_pending = True
        i = 1
        while i < len(parts):
            v = int(parts[i]); text = parts[i + 1].strip()
            cur = f"{BOOK}.{ch}.{v}"
            mt = web_to_mt(ch, v)
            entry = {"text": text, "para_before": opened_para or para_pending,
                     "continuation_paragraphs": 0,
                     "poetry_lines": opened_poetry if i == 1 else 0,
                     "language": language_of(ch, v),
                     "mt": f"{BOOK}.{mt[0]}.{mt[1]}" if mt else None}
            verses[cur] = entry
            opened_para = False; para_pending = False
            i += 2
        if m and not body.strip() and len(parts) == 1 and line.lstrip().startswith("Â¶"):
            para_pending = True
    for k, v in verses.items():
        v["clean"] = norm_english(v["text"])
    return verses


def build_oshb():
    out: dict[str, dict] = {}
    for line in (SPBOOK / f"{BOOK}_oshb.txt").read_text(encoding="utf-8").splitlines():
        if "\t" not in line:
            continue
        ref, text = line.split("\t", 1)
        _, c, v = ref.split(".")
        c, v = int(c), int(v)
        w = mt_to_web(c, v)
        entry = {"text": text, "language": language_of(c, v),
                 "web": f"{BOOK}.{w[0]}.{w[1]}" if w else None}
        out[ref] = entry
    return out


def main() -> int:
    web = build_web()
    oshb = build_oshb()
    assert len(web) == 154, f"WEB fold produced {len(web)} verses"
    assert len(oshb) == 154, f"OSHB map has {len(oshb)} verses"
    for c, last in LAST_VERSE.items():
        for v in range(1, last + 1):
            assert f"{BOOK}.{c}.{v}" in web, f"missing WEB {c}.{v}"
    for c, last in MT_LAST_VERSE.items():
        for v in range(1, last + 1):
            assert f"{BOOK}.{c}.{v}" in oshb, f"missing OSHB {c}.{v}"
    # crosswalk round-trip audit, range-guarded, both directions (INJECTIVE)
    for c, last in LAST_VERSE.items():
        for v in range(1, last + 1):
            mt = web_to_mt(c, v)
            assert mt is not None, f"web_to_mt None at WEB {c}.{v}"
            assert mt_to_web(*mt) == (c, v), \
                f"round-trip fail WEB {c}.{v} -> MT {mt} -> {mt_to_web(*mt)}"
    for c, last in MT_LAST_VERSE.items():
        for v in range(1, last + 1):
            webs = mt_to_web_all(c, v)
            assert len(webs) == 1, f"injectivity broken at MT {c}.{v}: {webs}"
            assert web_to_mt(*webs[0]) == (c, v), \
                f"round-trip fail MT {c}.{v} -> WEB {webs[0]} -> {web_to_mt(*webs[0])}"
    # identity assertions (Lam: WEB == MT everywhere; API parity functions are the identity)
    assert web_to_mt(1, 1) == (1, 1) and mt_to_web(5, 22) == (5, 22), "identity crosswalk broken"
    assert web_to_mt(3, 66) == (3, 66) and web_to_mt(6, 1) is None and web_to_mt(3, 67) is None, "range guard broken"
    # language layer: Hebrew throughout (0 Aramaic codes byte-proven at Phase 0)
    assert all(d["language"] == "Hebrew" for d in web.values()), "non-Hebrew label in WEB map"
    assert all(d["language"] == "Hebrew" for d in oshb.values()), "non-Hebrew label in OSHB map"
    # ACROSTIC SPINE pinned from bytes: first consonant of every verse
    import unicodedata as _ud
    _pts = re.compile(r"[\u0591-\u05C7]")
    def _first(ref):
        s = _pts.sub("", _ud.normalize("NFD", oshb[ref]["text"])).strip()
        return s[0]
    STD = "\u05d0\u05d1\u05d2\u05d3\u05d4\u05d5\u05d6\u05d7\u05d8\u05d9\u05db\u05dc\u05de\u05e0\u05e1\u05e2\u05e4\u05e6\u05e7\u05e8\u05e9\u05ea"
    REV = STD.replace("\u05e2\u05e4", "\u05e4\u05e2")
    assert len(STD) == 22 and len(REV) == 22
    ch1 = "".join(_first(f"{BOOK}.1.{v}") for v in range(1, 23))
    ch2 = "".join(_first(f"{BOOK}.2.{v}") for v in range(1, 23))
    ch4 = "".join(_first(f"{BOOK}.4.{v}") for v in range(1, 23))
    ch3 = [_first(f"{BOOK}.3.{v}") for v in range(1, 67)]
    ch5 = "".join(_first(f"{BOOK}.5.{v}") for v in range(1, 23))
    assert ch1 == STD, "ch 1 acrostic (standard ayin-pe order) moved: " + ch1
    assert ch2 == REV and ch4 == REV, "ch 2/4 acrostic (pe-ayin order) moved"
    assert all(len(set(ch3[i:i + 3])) == 1 for i in range(0, 66, 3)) and "".join(ch3[::3]) == REV, "ch 3 triple acrostic (pe-ayin order) moved"
    assert ch5 != STD and ch5 != REV, "ch 5 unexpectedly acrostic"
    acrostic = {"1": {"order": "standard (ayin before pe)", "letters": ch1}, "2": {"order": "reversed (pe before ayin)", "letters": ch2},
                "3": {"order": "reversed (pe before ayin), triple", "letters": "".join(ch3)}, "4": {"order": "reversed (pe before ayin)", "letters": ch4},
                "5": {"order": "NOT acrostic (22 verses)", "letters": ch5}}
    for ref, d in oshb.items():
        c, v = int(ref.split(".")[1]), int(ref.split(".")[2])
        d["acrostic_letter"] = _first(ref) if c in (1, 2, 3, 4) else None
        d["acrostic_position"] = ((v - 1) // (3 if c == 3 else 1) + 1) if c in (1, 2, 3, 4) else None
    (TOOLS / "acrostic_spine.json").write_text(json.dumps(acrostic, ensure_ascii=False, indent=1), encoding="utf-8")
    # per-verse token audit: folded WEB map vs raw USFM (alphabetic tokens)
    raw_usfm = (SPBOOK / f"{BOOK}_web.usfm").read_text(encoding="utf-8")
    raw_counts: dict[str, int] = {}
    kept = [l for l in raw_usfm.splitlines()
            if not re.match(r'\\(s\d?|r|d|sp|ms\d?|mr)\b', l)]
    chp = None
    vs = None
    for tok in re.split(r'(\\c \d+|\\v \d+)', "\n".join(kept)):
        mc = re.match(r'\\c (\d+)', tok or '')
        if mc:
            chp = int(mc.group(1)); vs = None; continue
        mv = re.match(r'\\v (\d+)', tok or '')
        if mv:
            vs = int(mv.group(1)); continue
        if chp and vs:
            body = re.sub(r'\\f \+ .*?\\f\*', ' ', tok, flags=re.S)
            body = re.sub(r'\|strong="[^"]*"', ' ', body)
            body = re.sub(r'\\\+?[a-z0-9]+\*?', ' ', body)
            key = f"{BOOK}.{chp}.{vs}"
            raw_counts[key] = raw_counts.get(key, 0) + len(re.findall(r"[A-Za-z]+", body))
    mismatch = []
    for key, want in raw_counts.items():
        got_text = re.sub(r"\[fn [^\]]*\]", " ", web[key]["text"])
        got = len(re.findall(r"[A-Za-z]+", got_text))
        if got != want:
            mismatch.append({"verse": key, "raw": want, "folded": got})
    assert not mismatch, f"token audit fail ({len(mismatch)}): {mismatch[:5]}"
    cons = {ref: {"skeleton": skeleton(d["text"]),
                  "accent_stripped": strip_accents(d["text"]),
                  "nfd": nfd(d["text"]),
                  "language": d["language"]}
            for ref, d in oshb.items()}
    (TOOLS / "verse_map_web.json").write_text(
        json.dumps(web, ensure_ascii=False, indent=1), encoding="utf-8")
    (TOOLS / "verse_map_oshb.json").write_text(
        json.dumps(oshb, ensure_ascii=False, indent=1), encoding="utf-8")
    (TOOLS / "consonantal_index.json").write_text(
        json.dumps(cons, ensure_ascii=False, indent=1), encoding="utf-8")
    maqaf_raw = (SPBOOK / f"{BOOK}_oshb.txt").read_text(encoding="utf-8").count("\u05BE")
    poetry_verses = sum(1 for d in web.values() if d["poetry_lines"])
    para_folds = sum(d["continuation_paragraphs"] for d in web.values())
    fold_verses = sorted(k for k, d in web.items() if d["continuation_paragraphs"])
    print(json.dumps({"web_verses": len(web), "oshb_verses": len(oshb),
                      "round_trip": "OK (identity, range-guarded, both directions)",
                      "token_audit": f"PASS {len(raw_counts)}/{len(raw_counts)}",
                      "maqaf_codepoints_in_staged_oshb": maqaf_raw,
                      "verses_opening_poetry_lines": poetry_verses,
                      "continuation_paragraph_folds": para_folds,
                      "fold_verses": fold_verses,
                      "aramaic_verses": [k for k, d in oshb.items() if d["language"] == "Aramaic"], "acrostic_spine": "pinned (acrostic_spine.json)",
                      "status": "OK"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
