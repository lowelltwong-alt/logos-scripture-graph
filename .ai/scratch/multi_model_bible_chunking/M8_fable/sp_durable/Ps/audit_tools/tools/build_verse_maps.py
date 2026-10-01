#!/usr/bin/env python3
"""Build verse_map_web.json, verse_map_oshb.json, consonantal_index.json,
../ps119_letter_headers_web.json and ../editorial_headings_web.json for Ps
(run ONCE by the orchestrator at staging; agents consume the JSONs).

Ps specifics vs the Song builder:
  - [SUPERSCRIPTION: ...] lines are the WEB psalm TITLES for 116 psalms:
    each becomes the title pseudo-verse Ps.N.0 (text = the title; mt =
    "Ps.N.1" for shift1 / titled-identity psalms [where it is the PREFIX of
    MT v1 — flagged title_is_prefix_of_mt_v1] or "Ps.N.1-2" for shift2).
    Ps 119's 22 [SUPERSCRIPTION] markers are ACROSTIC LETTER HEADERS — WEB
    typography (owner-addendum tier 4): cataloged separately, keyed by the
    WEB verse each precedes; NEVER a title; Ps.119.0 does not exist.
  - [MAJOR-SECTION: BOOK n] lines are modern editorial book headings (tier
    4): cataloged in ../editorial_headings_web.json keyed by the WEB verse
    each precedes, with the tier-4 warning embedded.
  - The extractor renders the inline Selah as "[qs Selah]"; the verse map
    carries it as the WEB word "Selah" (content-preserving; the raw-vs-folded
    token audit proves parity).
  - NON-IDENTITY numbering per ../web_mt_offset_map.json (byte-proven by
    build_offset_map.py). The round-trip audit exercises the REAL crosswalk
    in both directions incl. the 62 shift psalms and the Ps 13 split.
  - Paragraph-continuation folding + the per-verse raw-vs-folded token audit
    (lesson M8-LOG-0002) are UNCHANGED.
"""
from __future__ import annotations

import json
import re
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from ps_lib import (BOOK, LAST_VERSE, MT_LAST_VERSE, PSALM_RULES, SPBOOK, TITLED,
                    TOOLS, language_of, mt_to_web, mt_to_web_all, nfd,
                    norm_english, skeleton, strip_accents, title_mt_refs,
                    web_to_mt, web_to_mt_all)


def build_web():
    raw = (SPBOOK / f"{BOOK}_web_clean.txt").read_text(encoding="utf-8")
    verses: dict[str, dict] = {}
    letter_headers: dict[str, list[str]] = {}
    editorial: dict[str, list[str]] = {}
    pending_letters: list[str] = []
    pending_editorial: list[str] = []
    ch = None
    cur = None
    para_pending = False
    for line in raw.splitlines():
        line = line.rstrip()
        if not line:
            continue
        h = re.match(r"===== PS (\d+) =====", line.strip())
        if h:
            ch = int(h.group(1)); cur = None; para_pending = False
            continue
        sup = re.match(r"\s*\[SUPERSCRIPTION:\s*(.*)\]\s*$", line)
        if sup:
            text = sup.group(1).strip()
            if ch == 119:
                pending_letters.append(text)
            else:
                assert ch in TITLED, f"title line in an untitled psalm {ch}"
                t = title_mt_refs(ch)
                rule = PSALM_RULES[ch]["rule"]
                key = f"{BOOK}.{ch}.0"
                assert key not in verses, f"second title line in Ps {ch}"
                verses[key] = {"text": text, "clean": None, "title": True,
                               "para_before": False, "continuation_paragraphs": 0,
                               "poetry_lines": 0, "language": language_of(ch, 0),
                               "mt": (f"{BOOK}.{t[0][0]}.{t[0][1]}" if len(t) == 1
                                      else f"{BOOK}.{t[0][0]}.{t[0][1]}-{t[-1][1]}"),
                               "title_is_prefix_of_mt_v1": rule == "identity",
                               "rule": rule}
            continue
        ms = re.match(r"\s*\[MAJOR-SECTION:\s*(.*)\]\s*$", line)
        if ms:
            pending_editorial.append(ms.group(1).strip())
            continue
        assert not re.match(r"\[(HEADING|SPEAKER)", line.strip()), \
            f"unexpected structural annotation in Ps extract: {line[:60]}"
        # the extractor renders the inline \qs marker as "[qs Selah.]" (the WEB
        # punctuation stays inside the marker): fold it to the plain WEB text so
        # the raw-vs-folded token audit compares like with like. EXTRACTOR GAP
        # (upstream checks/extract_book_inputs.py, recorded 2026-09-03): where
        # the Selah is wrapped in a NESTED \+w ...|strong="..."\+w* tag inside
        # \qs (14 Psalm verses), the raw markup leaks into the clean text —
        # strip the nested tag and the \qs pair here, then assert no backslash
        # markup survives in any verse.
        line = re.sub(r'\\\+?w\s+([^|\\]+)\|strong="[^"]*"\\\+?w\*', r"\1", line)
        line = re.sub(r"\\qs\s*([^\\]*?)\\qs\*", r"\1", line)
        line = re.sub(r"\[qs\s+([^\]]*?)\s*\]", r"\1", line)
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
            if pending_letters:
                letter_headers[cur] = pending_letters
                pending_letters = []
            if pending_editorial:
                editorial[cur] = pending_editorial
                pending_editorial = []
            opened_para = False; para_pending = False
            i += 2
        if m and not body.strip() and len(parts) == 1 and line.lstrip().startswith("¶"):
            para_pending = True
    assert not pending_letters and not pending_editorial, "trailing headings unattached"
    leaks = [k for k, v in verses.items() if "\\" in v["text"] or "[qs" in v["text"]]
    assert not leaks, f"USFM markup leaked into {len(leaks)} verses: {leaks[:5]}"
    for k, v in verses.items():
        v["clean"] = norm_english(v["text"])
    return verses, letter_headers, editorial


def build_oshb():
    out: dict[str, dict] = {}
    for line in (SPBOOK / f"{BOOK}_oshb.txt").read_text(encoding="utf-8").splitlines():
        if "\t" not in line:
            continue
        ref, text = line.split("\t", 1)
        _, c, v = ref.split(".")
        c, v = int(c), int(v)
        w = mt_to_web(c, v)
        ws = mt_to_web_all(c, v)
        out[ref] = {"text": text, "language": "Hebrew",
                    "web": f"{BOOK}.{w[0]}.{w[1]}" if w else None,
                    "web_all": [f"{BOOK}.{a}.{b}" for a, b in ws]}
    return out


def main() -> int:
    web, letter_headers, editorial = build_web()
    oshb = build_oshb()
    titles = [k for k, d in web.items() if d.get("title")]
    body = {k for k in web if not web[k].get("title")}
    assert len(body) == 2461, f"WEB fold produced {len(body)} body verses"
    assert len(titles) == 116, f"{len(titles)} title pseudo-verses"
    assert len(oshb) == 2527, f"OSHB map has {len(oshb)} verses"
    assert sum(len(v) for v in letter_headers.values()) == 22, "Ps 119 letter headers != 22"
    for c, last in LAST_VERSE.items():
        for v in range(1, last + 1):
            assert f"{BOOK}.{c}.{v}" in web, f"missing WEB {c}.{v}"
        assert (f"{BOOK}.{c}.0" in web) == (c in TITLED), f"title presence mismatch Ps {c}"
    for c, last in MT_LAST_VERSE.items():
        for v in range(1, last + 1):
            assert f"{BOOK}.{c}.{v}" in oshb, f"missing OSHB {c}.{v}"
    # crosswalk round-trip audit, range-guarded, BOTH directions + titles + the split
    for c, last in LAST_VERSE.items():
        for v in range(1, last + 1):
            mt = web_to_mt(c, v)
            assert mt is not None, f"web_to_mt None at WEB {c}.{v}"
            assert (c, v) in mt_to_web_all(*mt), f"round-trip fail WEB {c}.{v} -> MT {mt}"
        if c in TITLED:
            t = web_to_mt_all(c, 0)
            assert t == title_mt_refs(c) and t, f"title map fail Ps {c}"
    for c, last in MT_LAST_VERSE.items():
        for v in range(1, last + 1):
            w = mt_to_web(c, v)
            assert w is not None, f"mt_to_web None at MT {c}.{v}"
            assert (c, v) in web_to_mt_all(*w), f"round-trip fail MT {c}.{v} -> WEB {w}"
    assert web_to_mt(3, 1) == (3, 2) and mt_to_web(3, 1) == (3, 0) and mt_to_web(3, 2) == (3, 1)
    assert web_to_mt(51, 1) == (51, 3) and web_to_mt_all(51, 0) == [(51, 1), (51, 2)] and mt_to_web(51, 2) == (51, 0)
    assert web_to_mt(13, 4) == (13, 5) and web_to_mt(13, 5) == (13, 6) and web_to_mt(13, 6) == (13, 6)
    assert mt_to_web_all(13, 6) == [(13, 5), (13, 6)] and mt_to_web(13, 1) == (13, 0)
    assert web_to_mt(1, 1) == (1, 1) and web_to_mt(119, 1) == (119, 1) and web_to_mt(119, 0) is None
    assert web_to_mt(98, 0) == (98, 1) and web_to_mt(98, 1) == (98, 1)   # titled identity (p22 erratum psalm)
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
            bodyt = re.sub(r'\\f \+ .*?\\f\*', ' ', tok, flags=re.S)
            bodyt = re.sub(r'\|strong="[^"]*"', ' ', bodyt)
            bodyt = re.sub(r'\\\+?[a-z0-9]+\*?', ' ', bodyt)
            key = f"{BOOK}.{chp}.{vs}"
            raw_counts[key] = raw_counts.get(key, 0) + len(re.findall(r"[A-Za-z]+", bodyt))
    mismatch = []
    for key, want in raw_counts.items():
        got_text = re.sub(r"\[fn [^\]]*\]", " ", web[key]["text"])
        got = len(re.findall(r"[A-Za-z]+", got_text))
        if got != want:
            mismatch.append({"verse": key, "raw": want, "folded": got})
    assert not mismatch, f"token audit fail ({len(mismatch)}): {mismatch[:5]}"
    # title text audit: every \d line's alphabetic tokens must equal the Ps.N.0 text's
    dl = {}
    chp = None
    for l in raw_usfm.splitlines():
        mc = re.match(r'\\c (\d+)', l)
        if mc:
            chp = int(mc.group(1)); continue
        if l.startswith("\\d ") and chp != 119:
            t = re.sub(r'\\f \+ .*?\\f\*', ' ', l[3:], flags=re.S)
            t = re.sub(r'\|strong="[^"]*"', ' ', t)
            t = re.sub(r'\\\+?[a-z0-9]+\*?', ' ', t)
            dl[chp] = dl.get(chp, 0) + len(re.findall(r"[A-Za-z]+", t))
    for c, want in dl.items():
        got = len(re.findall(r"[A-Za-z]+", re.sub(r"\[fn [^\]]*\]", " ", web[f"{BOOK}.{c}.0"]["text"])))
        assert got == want, f"title token audit fail Ps {c}: raw {want} folded {got}"
    assert set(dl) == TITLED, "\\d lines vs titled psalms mismatch"
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
    warn4 = ("WEB apparatus — MODERN EDITORIAL typography (owner addendum tier 4). "
             "NEVER boundary evidence, NEVER counterevidence by absence. Cataloged ONLY "
             "so claims can be audited against leaning on them. Keys = the WEB verse "
             "each heading immediately precedes.")
    (SPBOOK / "ps119_letter_headers_web.json").write_text(json.dumps({
        "book": BOOK, "tier": 4,
        "warning": "Ps 119 acrostic LETTER HEADERS (WEB typography; MT has no headers — the "
                   "letters are the verses' own initials). NEVER call them superscriptions. " + warn4,
        "headings_before_web_verse": letter_headers}, ensure_ascii=False, indent=1), encoding="utf-8")
    (SPBOOK / "editorial_headings_web.json").write_text(json.dumps({
        "book": BOOK, "tier": 4,
        "warning": "WEB [MAJOR-SECTION: BOOK n] lines — modern editorial five-book headings. " + warn4,
        "headings_before_web_verse": editorial}, ensure_ascii=False, indent=1), encoding="utf-8")
    maqaf_raw = (SPBOOK / f"{BOOK}_oshb.txt").read_text(encoding="utf-8").count("\u05BE")
    poetry_verses = sum(1 for k, d in web.items() if d.get("poetry_lines") and not d.get("title"))
    para_folds = sum(d["continuation_paragraphs"] for d in web.values())
    print(json.dumps({"web_body_verses": len(body), "web_title_pseudo_verses": len(titles),
                      "oshb_verses": len(oshb),
                      "round_trip": "OK (per-psalm crosswalk, range-guarded, both directions, titles + Ps 13 split)",
                      "token_audit": f"PASS {len(raw_counts)}/{len(raw_counts)} + {len(dl)} titles",
                      "maqaf_codepoints_in_staged_oshb": maqaf_raw,
                      "verses_opening_poetry_lines": poetry_verses,
                      "continuation_paragraph_folds": para_folds,
                      "ps119_letter_headers": sum(len(v) for v in letter_headers.values()),
                      "editorial_book_headings": sum(len(v) for v in editorial.values()),
                      "status": "OK"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
