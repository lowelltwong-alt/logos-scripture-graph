#!/usr/bin/env python3
"""Build verse_map_web.json, verse_map_oshb.json, consonantal_index.json for
Jer (run ONCE by the orchestrator at staging; agents consume the JSONs).

Jer specifics vs the Isa builder:
  - NO editorial apparatus lines of ANY class in the WEB Jer extract
    (byte-verified at Phase 0: zero [SPEAKER]/[HEADING]/[SUPERSCRIPTION]/
    [MAJOR-SECTION] lines; 11 [fn ...] footnote sites remain inline and are
    stripped by norm_english) - the builder ASSERTS this stays true.
  - ONE-ZONE NON-IDENTITY numbering, NO split: MT 8:23 = WEB 9:1;
    MT 9:1-25 = WEB 9:2-26 (byte-proven; see build_offset_map.py). The
    round-trip audit is exact equality both directions - web_to_mt is
    INJECTIVE in Jer.
  - LANGUAGE layer LIVE: the single Aramaic verse MT 10:11 = WEB 10:11
    (identity numbering) is marked "Aramaic" in BOTH maps and in the
    consonantal index (byte-proven from morph codes at Phase 0).
  - Paragraph-continuation folding + the per-verse raw-vs-folded token audit
    (lesson M8-LOG-0002) are UNCHANGED - Jer carries extensive narrative
    prose (chs 26-29, 32-45, 52), so the fold machinery is expected LIVE.
"""
from __future__ import annotations

import json
import re
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from jer_lib import (BOOK, LAST_VERSE, MT_LAST_VERSE, SPBOOK, TOOLS,
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
        h = re.match(r"===== JER (\d+) =====", line)
        if h:
            ch = int(h.group(1)); cur = None; para_pending = False
            continue
        assert not re.match(r"\[(SUPERSCRIPTION|MAJOR-SECTION|HEADING|SPEAKER)", line.strip()), \
            f"unexpected structural annotation in Jer extract: {line[:60]}"
        body = line
        opened_para = False
        opened_poetry = 0
        m = re.match(r"^(¶[»›]?\([^)]*\)|¶|\s*•|\s*\|[a-z0-9]+(?:\([^)]*\))?)\s*(.*)$", line)
        if m:
            opened_para = line.lstrip().startswith("¶")
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
        if m and not body.strip() and len(parts) == 1 and line.lstrip().startswith("¶"):
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
        # MT 10:11 is identity-zone, so language_of applies at MT coords too
        entry = {"text": text, "language": language_of(c, v),
                 "web": f"{BOOK}.{w[0]}.{w[1]}" if w else None}
        out[ref] = entry
    return out


def main() -> int:
    web = build_web()
    oshb = build_oshb()
    assert len(web) == 1364, f"WEB fold produced {len(web)} verses"
    assert len(oshb) == 1364, f"OSHB map has {len(oshb)} verses"
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
    # seam + zone-edge assertions
    assert web_to_mt(9, 1) == (8, 23) and mt_to_web(8, 23) == (9, 1), "zone seam rule broken"
    assert web_to_mt(9, 26) == (9, 25) and mt_to_web(9, 25) == (9, 26), "zone tail rule broken"
    assert web_to_mt(8, 22) == (8, 22) and web_to_mt(10, 1) == (10, 1), "zone edge identity broken"
    # language layer assertions (the Aramaic island, identity numbering)
    assert web[f"{BOOK}.10.11"]["language"] == "Aramaic", "WEB 10:11 not marked Aramaic"
    assert oshb[f"{BOOK}.10.11"]["language"] == "Aramaic", "MT 10:11 not marked Aramaic"
    assert sum(1 for d in web.values() if d["language"] == "Aramaic") == 1, "Aramaic count != 1 in WEB map"
    assert sum(1 for d in oshb.values() if d["language"] == "Aramaic") == 1, "Aramaic count != 1 in OSHB map"
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
                      "round_trip": "OK (one-zone crosswalk, injective, range-guarded, both directions)",
                      "token_audit": f"PASS {len(raw_counts)}/{len(raw_counts)}",
                      "maqaf_codepoints_in_staged_oshb": maqaf_raw,
                      "verses_opening_poetry_lines": poetry_verses,
                      "continuation_paragraph_folds": para_folds,
                      "fold_verses": fold_verses,
                      "aramaic_verses": [k for k, d in oshb.items() if d["language"] == "Aramaic"],
                      "status": "OK"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
