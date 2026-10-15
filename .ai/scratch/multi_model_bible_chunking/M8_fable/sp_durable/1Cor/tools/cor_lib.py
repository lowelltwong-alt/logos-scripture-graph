#!/usr/bin/env python3
"""Shared library for the 1Cor verification toolkit (Tier-0, deterministic). Orchestrator-written; PROTECTED.

Every agent brief points here. USE these tools; do NOT rebuild them.

EVERY FACT IN THIS DOCSTRING IS ASSERTED BY _selftest() BELOW against the staged Phase-0 artifacts and the Greek
substrate. Run `python -B cor_lib.py`: it exits non-zero if any statement here has drifted from the data.

LINEAGE. The interface follows Dan/tools/dan_lib.py, so a Daniel tool can be REBOUND to 1Cor rather than rewritten
from nothing. This is a Greek rebinding, not a token swap. The Hebrew-only parts of dan_lib have no counterpart here:
HEB_RUN, POINTS, ACCENTS, the K/Q splitter, the language zones and the paseq/parashah apparatus. The Greek text
functions (nfc, strip_accents, skeleton, is_letter, is_mark, bounded_find, collate_greek) are greek_lib's own,
re-exported unchanged; there is exactly one Greek normalization in the campaign, and it lives in
greek_substrate/tools/greek_lib.py.

WITNESSES (OW-31): Byzantine Robinson-Pierpont (rp) is PRIMARY, SBLGNT (sbl) is SECONDARY, WEB is the English face.
Swete's LXX is reference-only and is never loaded here.

NUMBERING - identity. WEB, RP and SBLGNT print the same 437 verses in 16 chapters, verse for verse
(../web_greek_verse_check.json and ../web_greek_offset_map.json, MEASURED from greek_lib.crosswalk()). There is no
offset zone, no split verse and no title pseudo-verse. web_to_greek() and greek_to_web() are still RANGE-GUARDED and
return None outside the book; use them, never hand-assume. web_to_mt, mt_to_web, mt_to_web_all, MT_LAST_VERSE and
PSALM_RULES exist for API parity with the Hebrew Bible tools: "mt" means the Greek face here, and every chapter's
rule is "identity".

REFS. Bare refs are `1Cor.C.V`; ranges `1Cor.C.V-1Cor.C.V` or `1Cor.C.V-V`. A witness prefix (web:, rp:, sbl:) may
precede a ref and does not change its numbers.

APPARATUS (../pmarks_1Cor.json, every ref WEB = Greek):
    RP paragraph starts (pilcrows)   35, of which 31 are also WEB paragraph starts
    WEB paragraph starts             87, plus one mid-verse WEB paragraph break inside 9:12
    SBLGNT variant-site verses       220 (inline critical signs U+2E00-U+2E05; 419 signs in all)
    RP/SBLGNT wording differs        218 verses, after greek_lib.skeleton
    WEB footnote markers             16 over 13 verses
Edition paragraphing is evidence, never a driver; a variant site is disclosed, never argued from alone.

SBLGNT SIGLA. The staged SBLGNT text keeps its inline critical signs byte for byte. They are not Greek words. At the
byte, nfc and accent_stripped tiers they stay in the haystack, so a quotation that runs ACROSS a sign reaches only the
skeleton tier against SBLGNT (skeleton turns the signs into spaces). A quotation that sits wholly inside or wholly
outside a signed span is unaffected. Quote RP as the primary; quote SBLGNT with its signs, or claim skeleton.

WEB TEXT. ../1Cor_web_clean.txt carries `[v] N text` lines under `===== 1COR C =====` headers, `¶` paragraph lines,
poetry continuation lines (` |q1 `, ` |q2 `) and one mid-verse `¶ ` continuation (9:12). load_web_clean() folds each
continuation into its verse; the result equals greek_lib.load_web()["1Cor"] verse for verse under norm_english.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SPBOOK = TOOLS.parent                       # SP/1Cor
SP = SPBOOK.parent                          # sp_durable
GREEK_TOOLS = SP.parent / "greek_substrate" / "tools"
BOOK = "1Cor"
sys.path.insert(0, str(GREEK_TOOLS))
import greek_lib as g  # noqa: E402

from greek_lib import bounded_find, collate_greek, is_letter, is_mark, nfc, skeleton, strip_accents  # noqa: E402,F401

_inv = json.loads((SPBOOK / "verse_inventory.json").read_text(encoding="utf-8"))
LAST_VERSE = {int(c): n for c, n in _inv["chapters"].items()}
TOTAL_VERSES = sum(LAST_VERSE.values())          # 437

_check = json.loads((SPBOOK / "web_greek_verse_check.json").read_text(encoding="utf-8"))
GREEK_LAST_VERSE = {int(c): p["rp"] for c, p in _check["per_chapter"].items()}
GREEK_TOTAL_VERSES = sum(GREEK_LAST_VERSE.values())
MT_LAST_VERSE = GREEK_LAST_VERSE                 # API parity: the Greek face
MT_TOTAL_VERSES = GREEK_TOTAL_VERSES
PSALM_RULES = {c: {"rule": "identity", "web_verses": LAST_VERSE[c], "mt_verses": GREEK_LAST_VERSE[c]}
               for c in sorted(LAST_VERSE)}
SPLIT_MT = None
SPLIT_WEB: list = []

REF = re.compile(r"(?<![\w.])(?:(web|rp|sbl):)?1Cor\.(\d+)\.(\d+)\b")
SIGLA = "⸀⸁⸂⸃⸄⸅"
SPACES = ("web", "rp", "sbl")


def web_to_greek(ch: int, v: int) -> tuple[int, int] | None:
    """WEB (ch, v) -> Greek (ch, v). Identity in 1Cor; range-guarded: None outside the book."""
    if ch not in LAST_VERSE or not (1 <= v <= LAST_VERSE[ch]):
        return None
    return (ch, v)


def greek_to_web(ch: int, v: int) -> tuple[int, int] | None:
    """Greek (ch, v) -> WEB (ch, v). Identity in 1Cor; range-guarded."""
    if ch not in GREEK_LAST_VERSE or not (1 <= v <= GREEK_LAST_VERSE[ch]):
        return None
    return (ch, v)


web_to_mt = web_to_greek                         # API parity with the Hebrew Bible tools
mt_to_web = greek_to_web


def mt_to_web_all(ch: int, v: int) -> list[tuple[int, int]]:
    """Every WEB verse a Greek verse maps to: exactly one everywhere in 1Cor (API parity)."""
    w = greek_to_web(ch, v)
    return [w] if w else []


def language_of(ch: int, v: int) -> str:
    """'Greek' for every verse of the book, None outside it (API parity; 1Cor has no language zone)."""
    return "Greek" if web_to_greek(ch, v) else None


def bounded_in(needle: str, hay: str, marks: bool = True) -> bool:
    return bounded_find(hay, needle, 0, marks) != -1


def collate(quoted: str, source_text: str) -> str:
    """greek_lib.collate_greek, unchanged: 'byte' | 'nfc' | 'accent_stripped' | 'skeleton' | 'none'. Ellipsis-aware,
    fragments in order, word-bounded. Against SBLGNT read the SIGLA note in the module docstring."""
    return collate_greek(quoted, source_text)


def expand_ref_token(tok: str, last_verse: dict[int, int] | None = None) -> list[tuple[int, int]]:
    """'1Cor.2.7', '1Cor.2.7-1Cor.3.5', '1Cor.8.1-13', each optionally prefixed web:/rp:/sbl: -> [(c, v), ...].
    Identity numbering, so one verse space serves every witness. Range ends are CLAMPED to real verses, as in
    dan_lib; [] for a token that is not a 1Cor ref."""
    lv = last_verse or LAST_VERSE
    m = re.match(r"^(?:(?:web|rp|sbl):)?1Cor\.(\d+)\.(\d+)(?:-(?:1Cor\.)?(\d+)(?:\.(\d+))?)?$", tok.strip())
    if not m:
        return []
    c1, v1 = int(m.group(1)), int(m.group(2))
    if m.group(3) is None:
        return [(c1, v1)]
    if m.group(4) is None:
        c2, v2 = c1, int(m.group(3))
    else:
        c2, v2 = int(m.group(3)), int(m.group(4))
    out = []
    for c in range(c1, c2 + 1):
        lo = max(v1 if c == c1 else 1, 1)
        hi = min(v2 if c == c2 else lv.get(c, 0), lv.get(c, 0))
        out.extend((c, v) for v in range(lo, hi + 1))
    return out


def ref(ch: int, v: int) -> str:
    return "1Cor.%d.%d" % (ch, v)


def _read_tsv(name: str) -> dict[tuple[int, int], str]:
    out = {}
    for line in (SPBOOK / name).read_text(encoding="utf-8").splitlines():
        key, text = line.split("\t", 1)
        b, c, v = key.split(".")
        if b != BOOK:
            raise ValueError("foreign key %r in %s" % (key, name))
        out[(int(c), int(v))] = text
    return out


def load_web_clean() -> dict[tuple[int, int], str]:
    """{(c, v): WEB text} from ../1Cor_web_clean.txt, continuation lines folded into their verse with one space and
    their markers (`|q1`, `|q2`, a leading `¶ `) removed. [fn] markers are KEPT; norm_english() removes them."""
    out, ch, last = {}, None, None
    for line in (SPBOOK / "1Cor_web_clean.txt").read_text(encoding="utf-8").split("\n"):
        if line.startswith("===== 1COR "):
            ch = int(line.split()[2])
        elif line.startswith("[v] "):
            n, text = line[4:].split(" ", 1)
            last = (ch, int(n))
            out[last] = text.strip()
        elif line in ("", "¶"):
            continue
        else:
            text = line.strip()
            for mark in ("|q1", "|q2", "¶"):
                if text.startswith(mark):
                    text = text[len(mark):].strip()
            if text:
                out[last] = out[last] + " " + text
    return out


def load_witnesses() -> dict[str, dict[tuple[int, int], str]]:
    """{'web': ..., 'rp': ..., 'sbl': ...}, each {(c, v): text} from the staged Phase-0 files (byte-faithful to the
    substrate; asserted by _selftest)."""
    return {"web": load_web_clean(), "rp": _read_tsv("1Cor_rp.txt"), "sbl": _read_tsv("1Cor_sbl.txt")}


def load_pmarks() -> dict:
    """../pmarks_1Cor.json as stored. Every key is a WEB ref, which is also the Greek ref."""
    return json.loads((SPBOOK / "pmarks_1Cor.json").read_text(encoding="utf-8"))


def norm_english(s: str) -> str:
    """Normalize English for quote comparison: typographic quotes, apostrophes and dashes to ASCII, footnote markers
    ([fn] and [fn ...]) removed, whitespace collapsed."""
    s = re.sub(r"\[fn(?: [^\]]*)?\]", " ", s)
    s = (s.replace("“", '"').replace("”", '"')
          .replace("‘", "'").replace("’", "'")
          .replace("—", "-").replace("–", "-"))
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def web_quote_found(quoted: str, verse_texts: list[str]) -> bool:
    """Ellipsis-aware verbatim membership of an English quote in folded WEB text."""
    hay = norm_english(" ".join(verse_texts))
    frags = [norm_english(f) for f in re.split(r"…|\.\.\.", quoted)]
    frags = [f for f in frags if f]
    pos = 0
    for f in frags:
        i = hay.find(f, pos)
        if i < 0:
            return False
        pos = i + len(f)
    return bool(frags)


# API parity names a ported tool imports (orchestrator amendment 2026-10-14, proposed by lane T2,
# cor_p0_toolport_t2_a1). GREEK_RUN is greek_lib's; it also matches U+2019, so a tool that masks Greek runs in English
# prose must spare a lone apostrophe itself (the ported tools do; a library-level change is a Greek-lane question).
from greek_lib import GREEK_RUN  # noqa: E402,F401  (the counterpart of dan_lib.HEB_RUN)


def load_verse_maps():
    """API parity with dan_lib.load_verse_maps: (web, rp), each keyed "1Cor.C.V". web values carry "text" and
    "clean" (both the load_web_clean() text: 1 Corinthians has no separate raw WEB layer here); rp values carry
    "text" and "web" (the identity WEB ref)."""
    web = {f"{BOOK}.{c}.{v}": {"text": t, "clean": t} for (c, v), t in load_web_clean().items()}
    rp = {f"{BOOK}.{c}.{v}": {"text": t, "web": f"{BOOK}.{c}.{v}"} for (c, v), t in _read_tsv(f"{BOOK}_rp.txt").items()}
    return web, rp

def _selftest() -> int:
    """Assert every fact in the module docstring. Exit non-zero on any drift."""
    sys.stdout.reconfigure(encoding="utf-8")
    checks = []
    w = load_witnesses()
    pm = load_pmarks()
    stage = json.loads((SPBOOK / "1cor_stage_report.json").read_text(encoding="utf-8"))
    omap = json.loads((SPBOOK / "web_greek_offset_map.json").read_text(encoding="utf-8"))
    keys = [(c, v) for c in sorted(LAST_VERSE) for v in range(1, LAST_VERSE[c] + 1)]

    def k(r):
        return tuple(int(x) for x in r.split(".")[1:])

    # ---- staged bytes and numbering ----
    checks.append(("staged outputs match the stage report's digests",
                   all(hashlib.sha256((SPBOOK / n).read_bytes()).hexdigest() == o["sha256"]
                       for n, o in stage["outputs"].items())))
    checks.append(("16 chapters, 437 verses on every face",
                   len(LAST_VERSE) == 16 and TOTAL_VERSES == 437 and GREEK_TOTAL_VERSES == 437
                   and all(len(w[s]) == 437 for s in SPACES)))
    checks.append(("WEB, RP and SBLGNT print the same verses in every chapter",
                   all(p["web"] == p["rp"] == p["sbl"] == LAST_VERSE[int(c)] for c, p in _check["per_chapter"].items())
                   and _check["divergent_chapters"] == [] and _check["verses_not_in_all_three"] == []
                   and all(sorted(w[s]) == keys for s in SPACES)))
    checks.append(("the offset map declares identity throughout with no zone",
                   omap["identity_throughout"] is True and omap["zones"] == []))
    checks.append(("every chapter's rule is identity", all(r["rule"] == "identity" for r in PSALM_RULES.values())))
    checks.append(("crosswalk round-trips every verse",
                   all(web_to_greek(*x) == x and greek_to_web(*x) == x and mt_to_web_all(*x) == [x] for x in keys)))
    checks.append(("out-of-range refs return None",
                   web_to_greek(17, 1) is None and web_to_greek(1, 0) is None and web_to_greek(1, 32) is None
                   and greek_to_web(16, 25) is None and language_of(16, 25) is None and language_of(13, 1) == "Greek"))
    crosswalk_ok = all(e["web"] and e["rp"] and e["sbl"] for e in g.crosswalk(BOOK))
    checks.append(("greek_lib.crosswalk(1Cor) has every verse in all three witnesses",
                   crosswalk_ok and len(g.crosswalk(BOOK)) == 437))
    checks.append(("staged RP equals greek_lib.load_rp() byte for byte", w["rp"] == g.load_rp()[BOOK]))
    checks.append(("staged SBLGNT equals greek_lib.load_sbl() byte for byte", w["sbl"] == g.load_sbl()[BOOK]))
    gw = g.load_web()[BOOK]
    checks.append(("load_web_clean() equals greek_lib.load_web() under norm_english on every verse",
                   all(norm_english(w["web"][x]) == norm_english(gw[x]) for x in keys)))

    # ---- apparatus ----
    t = pm["tally"]
    checks.append(("RP pilcrows 35, of which 31 are WEB paragraph starts",
                   len(pm["rp_paragraph_starts"]) == 35 == t["rp_paragraph_starts"]
                   and len(set(pm["rp_paragraph_starts"]) & set(pm["web_paragraph_starts"])) == 31
                   == t["rp_and_web_agree_on_start"]
                   and stage["rp"]["pilcrow_verses"] == pm["rp_paragraph_starts"]))
    raw_web = (SPBOOK / "1Cor_web_clean.txt").read_text(encoding="utf-8").split("\n")
    checks.append(("WEB 87 paragraph starts plus one mid-verse break inside 9:12",
                   len(pm["web_paragraph_starts"]) == 87 and raw_web.count("¶") == 87
                   and pm["web_paragraph_midverse"] == ["1Cor.9.12"]
                   and sum(1 for x in raw_web if x.startswith("¶ ")) == 1))
    signs = {c: sum(t_.count(c) for t_ in w["sbl"].values()) for c in SIGLA}
    carrying = {x for x, t_ in w["sbl"].items() if any(c in t_ for c in SIGLA)}
    checks.append(("SBLGNT sigla U+2E00-U+2E05: 419 signs over 220 verses, as the stage report measured",
                   sum(signs.values()) == 419
                   and {"U+%04X" % ord(c): n for c, n in signs.items()} == stage["sbl"]["apparatus_sigla_MEASURED"]["chars"]
                   and len(carrying) == 220 == len(pm["sbl_variant_sites"])
                   and {k(r) for r in pm["sbl_variant_sites"]} == carrying))
    diff = {x for x in keys if skeleton(w["rp"][x]) != skeleton(w["sbl"][x])}
    checks.append(("RP and SBLGNT wording differ in 218 verses after skeleton",
                   len(diff) == 218 and {k(r) for r in pm["rp_sbl_differences"]} == diff))
    fn = {x: w["web"][x].count("[fn]") for x in keys if "[fn]" in w["web"][x]}
    checks.append(("WEB [fn] 16 markers over 13 verses, and norm_english removes every one",
                   sum(fn.values()) == 16 and len(fn) == 13 and {"1Cor.%d.%d" % x: n for x, n in fn.items()}
                   == pm["web_footnote_verses"] and not any("[fn" in norm_english(t_) for t_ in w["web"].values())))

    # ---- refs ----
    checks.append(("expand_ref_token: single, cross-chapter, same-chapter shorthand, prefixed, clamped, foreign",
                   expand_ref_token("1Cor.13.1") == [(13, 1)]
                   and expand_ref_token("1Cor.1.30-1Cor.2.2") == [(1, 30), (1, 31), (2, 1), (2, 2)]
                   and expand_ref_token("rp:1Cor.14.33-36") == [(14, 33), (14, 34), (14, 35), (14, 36)]
                   and expand_ref_token("1Cor.16.20-40") == [(16, v) for v in range(20, 25)]
                   and expand_ref_token("2Cor.1.1") == [] and expand_ref_token("Dan.1.1") == []))
    checks.append(("REF reads prefixed and bare refs and refuses 2Cor/11Cor",
                   [m.group(0) for m in REF.finditer("sbl:1Cor.14.34 and 1Cor.7.1; 2Cor.1.1 11Cor.1.1")]
                   == ["sbl:1Cor.14.34", "1Cor.7.1"]))

    # ---- collation (greek_lib's, re-exported) ----
    rp11, sbl11 = w["rp"][(1, 1)], w["sbl"][(1, 1)]
    checks.append(("collate is a thin wrapper that delegates to greek_lib.collate_greek",
                   collate is not collate_greek and collate_greek is g.collate_greek and
                   collate(rp11, rp11) == collate_greek(rp11, rp11) == "byte"))
    checks.append(("a quote inside an SBLGNT signed span is byte; one across a sign reaches only skeleton",
                   "⸂Χριστοῦ Ἰησοῦ⸃" in sbl11
                   and collate("Χριστοῦ Ἰησοῦ", sbl11) == "byte"
                   and collate("ἀπόστολος Χριστοῦ", sbl11) == "skeleton"))
    checks.append(("a fragment that starts inside a word does not collate at any tier",
                   collate("πόστολος", rp11) == "none"))
    checks.append(("an ellipsis of whole words collates in order, and not out of order",
                   collate("Παῦλος … ἀπόστολος", rp11) == "byte" and collate("ἀπόστολος … Παῦλος", rp11) == "none"))
    checks.append(("an unaccented whole word collates at accent_stripped",
                   collate(strip_accents("θελήματος"), rp11) == "accent_stripped"))
    checks.append(("web_quote_found: verbatim with typographic quotes, footnote-insensitive, ordered ellipsis",
                   web_quote_found("Paul, called to be an apostle of Jesus Christ through", [w["web"][(1, 1)]])
                   and web_quote_found("Paul … Sosthenes", [w["web"][(1, 1)]])
                   and not web_quote_found("Sosthenes … Paul", [w["web"][(1, 1)]])
                   and not web_quote_found("", [w["web"][(1, 1)]])))

    failed = [n for n, ok in checks if not ok]
    print(json.dumps({"module": "cor_lib", "checks": len(checks), "passed": len(checks) - len(failed),
                      "failed": failed, "verdict": "GREEN" if not failed else "RED"}, ensure_ascii=False, indent=1))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(_selftest())
