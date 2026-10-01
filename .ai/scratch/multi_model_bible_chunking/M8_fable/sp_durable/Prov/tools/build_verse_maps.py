#!/usr/bin/env python3
"""Build verse_map_web.json, verse_map_oshb.json, consonantal_index.json for Prov
(run ONCE by the orchestrator at staging; agents consume the JSONs).

Prov specifics vs the Ps builder:
  - NO titles, superscriptions, acrostic stanza headers, or [MAJOR-SECTION]
    banners exist in the WEB Prov extract (asserted); the collection headers
    (1:1, 10:1, 22:17, 24:23, 25:1, 30:1, 31:1) are ordinary counted verses.
  - Identity numbering both directions (byte-proven; see build_offset_map.py);
    the round-trip audit still runs range-guarded via prov_lib.
  - Paragraph-continuation folding + the per-verse raw-vs-folded token audit
    (lesson M8-LOG-0002) are UNCHANGED — the folding hazard class does not
    depend on the book.
"""
from __future__ import annotations

import json
import re
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from prov_lib import (BOOK, LAST_VERSE, MT_LAST_VERSE, SPBOOK, TOOLS,
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
        h = re.match(r"===== PROV (\d+) =====", line)
        if h:
            ch = int(h.group(1)); cur = None; para_pending = False
            continue
        assert not re.match(r"\[(SUPERSCRIPTION|MAJOR-SECTION|HEADING|SPEAKER)", line.strip()), \
            f"unexpected structural annotation in Prov extract: {line[:60]}"
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
            verses[cur] = {"text": text, "para_before": opened_para or para_pending,
                           "continuation_paragraphs": 0,
                           "poetry_lines": opened_poetry if i == 1 else 0,
                           "language": language_of(ch, v),
                           "mt": f"{BOOK}.{mt[0]}.{mt[1]}" if mt else None}
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
        out[ref] = {"text": text, "language": "Hebrew",
                    "web": f"{BOOK}.{w[0]}.{w[1]}" if w else None}
    return out


def main() -> int:
    web = build_web()
    oshb = build_oshb()
    assert len(web) == 915, f"WEB fold produced {len(web)} verses"
    assert len(oshb) == 915, f"OSHB map has {len(oshb)} verses"
    for c, last in LAST_VERSE.items():
        for v in range(1, last + 1):
            assert f"{BOOK}.{c}.{v}" in web, f"missing WEB {c}.{v}"
    for c, last in MT_LAST_VERSE.items():
        for v in range(1, last + 1):
            assert f"{BOOK}.{c}.{v}" in oshb, f"missing OSHB {c}.{v}"
    # identity round-trip audit, range-guarded
    for c, last in LAST_VERSE.items():
        for v in range(1, last + 1):
            mt = web_to_mt(c, v)
            assert mt == (c, v), f"web_to_mt broke identity at {c}.{v}"
            assert mt_to_web_all(*mt) == [(c, v)], f"round-trip fail {c}.{v}"
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
    poetry_verses = sum(1 for d in web.values() if d["poetry_lines"])
    para_folds = sum(d["continuation_paragraphs"] for d in web.values())
    print(json.dumps({"web_verses": len(web), "oshb_verses": len(oshb),
                      "round_trip": "OK (identity, range-guarded)",
                      "token_audit": f"PASS {len(raw_counts)}/{len(raw_counts)}",
                      "verses_opening_poetry_lines": poetry_verses,
                      "continuation_paragraph_folds": para_folds,
                      "status": "OK"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
