#!/usr/bin/env python3
"""Shared library for the Greek NT substrate toolkit (Tier-0, deterministic).

Modelled on sp_durable/Dan/tools/dan_lib.py (read, never edited): range-guarded ref handling, word-boundary
matching, ordered ellipsis-aware collation, a selftest that asserts the facts stated in prose. Nothing here is
copied from a Hebrew book's figures; every figure asserted by _selftest() was MEASURED from the staged bytes on
2026-09-29 (see ../README.md).

WITNESSES (see ../STAGING_RECEIPT.v1.json for pins, hashes and licences):
    web:  World English Bible, read-only from the repo's governed eng-web_usfm.zip (sha256 checked on load)
    rp:   Robinson-Pierpont Byzantine Textform v3.3.2, PRIMARY. MEASURED 2026-09-29: JOH.csv itself prints John
          7:53-8:11, and PA.csv (a separate form of the pericope whose editorial status is UNKNOWN here) differs from
          it in 11 of 12 verses; ACT.csv prints Acts 24:6 and 24:8 but not 24:7, which exists only in ACT24.csv (a
          longer 24:6-8). load_rp() keeps the main-file text, merges ONLY verses the main file lacks (RP_MERGED),
          and records separate-file readings that differ (RP_SEPARATE_DIFFERS). Nothing is chosen as preferred.
    sbl:  SBLGNT v1.2, SECONDARY (critical-text disclosure).
    Swete LXX is REFERENCE-ONLY and is never loaded as a verse witness here; swete_skeleton_shingles() exists only
    so the normalizer can detect Swete-sourced wording that must not enter rows (owner terms, 2026-09-29). It
    returns hashes, never text.

REFS: "<space>:<Book>.<ch>.<v>" with Book in BOOKS (e.g. web:John.7.53, rp:3John.1.14, sbl:3John.1.15). Ranges
"John.7.53-John.8.11" or "John.7.53-8.11". Every space is range-guarded against ITS OWN witness: a ref exists only
if that witness prints that verse. There is no arithmetic crosswalk: verse identity across witnesses is by
number, and existence is recorded per witness (crosswalk()).

TIERS (collate_greek): byte > nfc > accent_stripped > skeleton > none.
    byte             exact code points
    nfc              equal after Unicode NFC (e.g. oxia U+1F71 vs tonos U+03AC); an E-01-class degradation
    accent_stripped  NFD, acute/grave/circumflex (U+0300, U+0301, U+0340, U+0341, U+0342) removed; breathings,
                     diaeresis and iota subscript KEPT; recomposed NFC
    skeleton         every combining mark removed, casefolded, final sigma -> sigma, elision marks and punctuation
                     removed, whitespace collapsed
Fragments match IN ORDER and on word boundaries: at byte/nfc/accent_stripped no letter or combining mark may stand
beside a match; at skeleton no letter.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import unicodedata
import zipfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SUB = TOOLS.parent                                   # M8_fable/greek_substrate
REPO = SUB.parents[4]                                # worktree root
WEB_ZIP = REPO / "data/raw/bible/eng-web/usfm/eng-web_usfm.zip"
WEB_ZIP_SHA256 = "a745365f53ab95570e9c39a60a7d245ba10bbf6c863832006876b01ea8654f8e"
RECEIPT = SUB / "STAGING_RECEIPT.v1.json"

# ref token, WEB usfm code, RP csv stem, SBL file stem (SBL line prefix equals the stem)
BOOK_TABLE = [
    ("Matt", "MAT", "MAT", "Matt"), ("Mark", "MRK", "MAR", "Mark"), ("Luke", "LUK", "LUK", "Luke"),
    ("John", "JHN", "JOH", "John"), ("Acts", "ACT", "ACT", "Acts"), ("Rom", "ROM", "ROM", "Rom"),
    ("1Cor", "1CO", "1CO", "1Cor"), ("2Cor", "2CO", "2CO", "2Cor"), ("Gal", "GAL", "GAL", "Gal"),
    ("Eph", "EPH", "EPH", "Eph"), ("Phil", "PHP", "PHP", "Phil"), ("Col", "COL", "COL", "Col"),
    ("1Thess", "1TH", "1TH", "1Thess"), ("2Thess", "2TH", "2TH", "2Thess"), ("1Tim", "1TI", "1TI", "1Tim"),
    ("2Tim", "2TI", "2TI", "2Tim"), ("Titus", "TIT", "TIT", "Titus"), ("Phlm", "PHM", "PHM", "Phlm"),
    ("Heb", "HEB", "HEB", "Heb"), ("Jas", "JAS", "JAM", "Jas"), ("1Pet", "1PE", "1PE", "1Pet"),
    ("2Pet", "2PE", "2PE", "2Pet"), ("1John", "1JN", "1JO", "1John"), ("2John", "2JN", "2JO", "2John"),
    ("3John", "3JN", "3JO", "3John"), ("Jude", "JUD", "JUD", "Jude"), ("Rev", "REV", "REV", "Rev"),
]
BOOKS = [b[0] for b in BOOK_TABLE]
RP_SEPARATE = {"John": "PA.csv", "Acts": "ACT24.csv"}
SPACES = ("web", "rp", "sbl")

TONE = {"\u0300", "\u0301", "\u0340", "\u0341", "\u0342"}
ELISION = "\u02bc\u2019\u1fbd\u1fbf'"
REF = re.compile(r"\b(web|rp|sbl):(" + "|".join(sorted(map(re.escape, BOOKS), key=len, reverse=True)) +
                 r")\.(\d+)\.(\d+)(?:-(?:(?:\2)\.)?(\d+)(?:\.(\d+))?)?")
GREEK_RUN = re.compile(r"[\u0370-\u03ff\u1f00-\u1fff\u0300-\u036f\u02bc\u2019]+"
                       r"(?:[ ,.·;\u0387\u02bc\u2019]+[\u0370-\u03ff\u1f00-\u1fff][\u0370-\u03ff\u1f00-\u1fff"
                       r"\u0300-\u036f\u02bc\u2019]*)*")


class SubstrateError(RuntimeError):
    """A staged input is missing or differs from its pinned hash. Tools must fail closed on it."""


# ---------------------------------------------------------------- text tiers
def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def strip_accents(s: str) -> str:
    return nfc("".join(c for c in unicodedata.normalize("NFD", s) if c not in TONE))


def skeleton(s: str) -> str:
    d = unicodedata.normalize("NFD", s)
    d = "".join(c for c in d if unicodedata.category(c) != "Mn").casefold().replace("ς", "σ")
    d = "".join("" if c in ELISION else (" " if unicodedata.category(c)[0] in "PSZ" else c) for c in d)
    return re.sub(r"\s+", " ", d).strip()


def is_letter(ch: str) -> bool:
    return unicodedata.category(ch).startswith("L")


def is_mark(ch: str) -> bool:
    return unicodedata.category(ch) == "Mn"


def bounded_find(hay: str, needle: str, pos: int = 0, marks: bool = True) -> int:
    if not needle:
        return -1
    edge = (lambda ch: is_letter(ch) or is_mark(ch)) if marks else is_letter
    i = hay.find(needle, pos)
    while i != -1:
        j = i + len(needle)
        if (i == 0 or not edge(hay[i - 1])) and (j >= len(hay) or not edge(hay[j])):
            return i
        i = hay.find(needle, i + 1)
    return -1


TIERS = (("byte", lambda s: s), ("nfc", nfc), ("accent_stripped", strip_accents), ("skeleton", skeleton))
TIER_RANK = {t: i for i, (t, _) in enumerate(TIERS)} | {"none": len(TIERS)}


def collate_greek(quoted: str, source_text: str) -> str:
    frags = [f.strip() for f in re.split(r"…|\.\.\.", quoted) if f.strip()]
    if not frags:
        return "none"
    for tier, xf in TIERS:
        hay, pos, ok = xf(source_text), 0, True
        for n in (xf(f) for f in frags):
            i = bounded_find(hay, n, pos, tier != "skeleton")
            if i < 0:
                ok = False
                break
            pos = i + len(n)
        if ok:
            return tier
    return "none"


# ---------------------------------------------------------------- loaders
def _sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _clean_usfm(t: str) -> str:
    t = re.sub(r"\\f .*?\\f\*", " ", t, flags=re.S)
    t = re.sub(r"\\x .*?\\x\*", " ", t, flags=re.S)
    t = re.sub(r"\\\+?w ([^|\\]*)\|[^\\]*\\\+?w\*", r"\1", t)
    t = re.sub(r"\\[a-z0-9+]+\*?", " ", t)
    return re.sub(r"\s+", " ", t).strip()


_WEB_CACHE: dict | None = None


def load_web() -> dict[str, dict[tuple[int, int], str]]:
    """{Book: {(ch, v): clean English}} for the 27 NT books. Verse bridges (\\v 1-2) are keyed to EACH verse and
    flagged in WEB_BRIDGES. Raises SubstrateError if the zip hash drifts."""
    global _WEB_CACHE
    if _WEB_CACHE is not None:
        return _WEB_CACHE
    if not WEB_ZIP.is_file():
        raise SubstrateError(f"WEB zip missing: {WEB_ZIP}")
    raw = WEB_ZIP.read_bytes()
    if _sha256(raw) != WEB_ZIP_SHA256:
        raise SubstrateError("WEB zip sha256 differs from the pinned value")
    z = zipfile.ZipFile(io.BytesIO(raw))
    out: dict[str, dict[tuple[int, int], str]] = {}
    for book, code, _, _ in BOOK_TABLE:
        names = [n for n in z.namelist() if re.fullmatch(rf"\d\d-{code}eng-web\.usfm", n)]
        if len(names) != 1:
            raise SubstrateError(f"WEB member for {code}: {names}")
        text = z.read(names[0]).decode("utf-8-sig")
        verses: dict[tuple[int, int], str] = {}
        for chap in re.split(r"\\c (?=\d)", text)[1:]:
            ch = int(re.match(r"\d+", chap).group())
            for m in re.finditer(r"\\v (\d+)(?:-(\d+))?\s(.*?)(?=\\v \d|\Z)", chap, re.S):
                lo, hi = int(m.group(1)), int(m.group(2) or m.group(1))
                txt = _clean_usfm(m.group(3))
                for v in range(lo, hi + 1):
                    if not txt:                       # a \v marker carrying only a footnote (e.g. Rom 16:25)
                        WEB_EMPTY.add((book, ch, v))
                        continue
                    verses[(ch, v)] = txt
                    if hi != lo:
                        WEB_BRIDGES.add((book, ch, v))
        out[book] = verses
    _WEB_CACHE = out
    return out


WEB_BRIDGES: set[tuple[str, int, int]] = set()
WEB_EMPTY: set[tuple[str, int, int]] = set()          # verse markers with no text (not counted as existing)
RP_MERGED: dict[tuple[str, int, int], str] = {}      # (book, ch, v) -> separate file it came from
RP_SEPARATE_DIFFERS: dict[tuple[str, int, int], str] = {}   # main file prints the verse; separate file differs
RP_PARAGRAPH: set[tuple[str, int, int]] = set()      # verses whose RP text carries a pilcrow


def _read_csv(p: Path) -> list[tuple[int, int, str]]:
    if not p.is_file():
        raise SubstrateError(f"RP file missing: {p.name}")
    rows = list(csv.reader(io.StringIO(p.read_text(encoding="utf-8-sig"))))
    if rows[0] != ["chapter", "verse", "text"]:
        raise SubstrateError(f"RP header changed in {p.name}: {rows[0]}")
    return [(int(c), int(v), t) for c, v, t in rows[1:]]


_RP_CACHE: dict | None = None


def load_rp() -> dict[str, dict[tuple[int, int], str]]:
    """{Book: {(ch, v): Greek}}. Pilcrows are removed from the text and recorded in RP_PARAGRAPH. Verses from
    PA.csv / ACT24.csv are merged only where the main file lacks that verse (recorded in RP_MERGED); if the main
    file already carries one, the separate file's reading is NOT substituted (reported by crosswalk)."""
    global _RP_CACHE
    if _RP_CACHE is not None:
        return _RP_CACHE
    d = SUB / "byzantine_rp_PRIMARY"
    out = {}
    for book, _, stem, _ in BOOK_TABLE:
        vs = {}
        for c, v, t in _read_csv(d / f"{stem}.csv"):
            if "¶" in t:
                RP_PARAGRAPH.add((book, c, v))
            vs[(c, v)] = re.sub(r"\s+", " ", t.replace("¶", "")).strip()
        if book in RP_SEPARATE:
            for c, v, t in _read_csv(d / RP_SEPARATE[book]):
                t2 = re.sub(r"\s+", " ", t.replace("¶", "")).strip()
                if (c, v) not in vs:
                    vs[(c, v)] = t2
                    RP_MERGED[(book, c, v)] = RP_SEPARATE[book]
                elif vs[(c, v)] != t2:
                    RP_SEPARATE_DIFFERS[(book, c, v)] = RP_SEPARATE[book]
        out[book] = dict(sorted(vs.items()))
    _RP_CACHE = out
    return out


_SBL_CACHE: dict | None = None


def load_sbl() -> dict[str, dict[tuple[int, int], str]]:
    global _SBL_CACHE
    if _SBL_CACHE is not None:
        return _SBL_CACHE
    d = SUB / "sblgnt_SECONDARY"
    out = {}
    for book, _, _, stem in BOOK_TABLE:
        p = d / f"{stem}.txt"
        if not p.is_file():
            raise SubstrateError(f"SBLGNT file missing: {p.name}")
        vs = {}
        for line in p.read_text(encoding="utf-8-sig").splitlines():
            m = re.match(rf"^{re.escape(stem)} (\d+):(\d+)\t(.*)$", line)
            if m:
                vs[(int(m.group(1)), int(m.group(2)))] = m.group(3).strip()
        if not vs:
            raise SubstrateError(f"SBLGNT file has no verse lines: {p.name}")
        out[book] = vs
    _SBL_CACHE = out
    return out


def load(space: str) -> dict[str, dict[tuple[int, int], str]]:
    return {"web": load_web, "rp": load_rp, "sbl": load_sbl}[space]()


def verse(space: str, book: str, ch: int, v: int) -> str | None:
    """Range-guarded: None if that witness does not print the verse."""
    return load(space).get(book, {}).get((ch, v))


def expand_ref(space: str, book: str, c1: int, v1: int, c2: int | None = None, v2: int | None = None):
    """[(c, v)] of verses that EXIST in the witness between the two ends, or None if either end does not exist
    in that witness or the range runs backwards (range ends are validated, never clamped)."""
    vs = load(space).get(book)
    if vs is None:
        return None
    end = (c2 if c2 is not None else c1, v2 if v2 is not None else v1)
    if (c1, v1) not in vs or end not in vs or end < (c1, v1):
        return None
    return [k for k in vs if (c1, v1) <= k <= end]


def parse_refs(text: str):
    """Yield (token, space, book, c1, v1, c2, v2) for every ref token in text."""
    for m in REF.finditer(text):
        sp, bk, c1, v1, a, b = m.groups()
        c1, v1 = int(c1), int(v1)
        if a is None:
            c2, v2 = c1, v1
        elif b is None:
            c2, v2 = c1, int(a)
        else:
            c2, v2 = int(a), int(b)
        yield m.group(0), sp, bk, c1, v1, c2, v2


def crosswalk(book: str) -> list[dict]:
    """One entry per verse number printed by ANY witness, in canonical order, with existence flags."""
    w, r, s = load_web()[book], load_rp()[book], load_sbl()[book]
    out = []
    for k in sorted(set(w) | set(r) | set(s)):
        e = {"ref": f"{book}.{k[0]}.{k[1]}", "web": k in w, "rp": k in r, "sbl": k in s}
        if (book, *k) in RP_MERGED:
            e["rp_separate_file"] = RP_MERGED[(book, *k)]
        if (book, *k) in RP_SEPARATE_DIFFERS:
            e["rp_separate_file_differs"] = RP_SEPARATE_DIFFERS[(book, *k)]
        if (book, *k) in WEB_BRIDGES:
            e["web_bridge"] = True
        out.append(e)
    for b, c, v in sorted(WEB_EMPTY):
        if b == book:
            e = next((x for x in out if x["ref"] == f"{book}.{c}.{v}"), None)
            if e is None:
                e = {"ref": f"{book}.{c}.{v}", "web": False, "rp": (c, v) in r, "sbl": (c, v) in s}
                out.append(e)
            e["web_empty_marker"] = True
    out.sort(key=lambda x: tuple(int(n) for n in x["ref"].split(".")[1:]))
    return out


def swete_skeleton_shingles(n: int = 5) -> set[str]:
    """sha1 hashes of every n-word skeleton shingle in the staged Swete files (reference-only isolation arm).
    Returns hashes only; no Swete wording leaves this function."""
    out: set[str] = set()
    d = SUB / "swete_lxx_REFERENCE_ONLY"
    files = sorted(d.glob("*.xml"))
    if not files:
        raise SubstrateError("Swete reference files missing")
    for p in files:
        t = p.read_text(encoding="utf-8")
        body = t[t.find("<body"):] if "<body" in t else t
        body = re.sub(r"<note.*?</note>", " ", body, flags=re.S)
        words = skeleton(re.sub(r"<[^>]+>", " ", body)).split()
        for i in range(len(words) - n + 1):
            out.add(hashlib.sha1(" ".join(words[i:i + n]).encode("utf-8")).hexdigest())
    return out


def nt_skeleton_shingles(n: int = 5) -> set[str]:
    out: set[str] = set()
    for sp in ("rp", "sbl"):
        for vs in load(sp).values():
            words = skeleton(" ".join(vs.values())).split()
            for i in range(len(words) - n + 1):
                out.add(hashlib.sha1(" ".join(words[i:i + n]).encode("utf-8")).hexdigest())
    return out


def verify_staged() -> list[str]:
    """Re-hash every staged file against STAGING_RECEIPT.v1.json. Returns problems (empty = clean)."""
    problems = []
    if not RECEIPT.is_file():
        return ["STAGING_RECEIPT.v1.json missing"]
    rec = json.loads(RECEIPT.read_text(encoding="utf-8"))
    for s in rec["sets"]:
        if s.get("status") != "staged":
            problems.append(f"set {s['set']} not staged")
            continue
        for f in s["files"]:
            p = SUB / s["folder"] / f["name"]
            if not p.is_file():
                problems.append(f"missing {s['folder']}/{f['name']}")
            elif _sha256(p.read_bytes()) != f["sha256"]:
                problems.append(f"sha256 drift {s['folder']}/{f['name']}")
    return problems


# ---------------------------------------------------------------- selftest
def _selftest() -> int:
    fails = []

    def check(cond, msg):
        if not cond:
            fails.append(msg)

    # tier functions (constructed strings, not witness figures)
    check(collate_greek("λόγος", "ὁ λόγος ἦν") == "byte", "byte tier")
    check(collate_greek("λόγος", "ὁ λο\u0301γος ἦν") == "nfc", "nfc tier (decomposed acute)")
    check(collate_greek("\u1f00\u03b3\u03b1\u03c0\u1f71\u03c9", "ἀγαπάω") == "nfc", "nfc tier (oxia vs tonos)")
    check(collate_greek("λογος", "ὁ λόγος ἦν") == "accent_stripped", "accent_stripped tier")
    check(collate_greek("ο λογοσ", "Ὁ λόγος") == "skeleton", "skeleton tier (breathing, case, final sigma)")
    check(collate_greek("λόγ", "ὁ λόγος") == "none", "word boundary refuses a partial word")
    check(collate_greek("ἦν … λόγος", "ὁ λόγος ἦν") == "none", "fragments must be in order")
    check(skeleton("κατʼ ὄνομα.") == "κατ ονομα", "skeleton drops elision mark and punctuation")
    check(strip_accents("ἀγαπητῷ") == nfc("ἀγαπητῳ"), "accent_stripped keeps breathing and iota subscript")
    try:
        web, rp, sbl = load_web(), load_rp(), load_sbl()
    except SubstrateError as e:
        print(json.dumps({"status": "RED", "selftest": "greek_lib", "fails": [str(e)]}))
        return 1
    # MEASURED facts on the fixture books (2026-09-29, see README)
    check(len(web["3John"]) == 14 and len(rp["3John"]) == 14 and len(sbl["3John"]) == 15, "3John verse counts")
    check((1, 15) in sbl["3John"] and (1, 15) not in rp["3John"], "3John 1:15 is SBL-only")
    check(len(web["Phlm"]) == len(rp["Phlm"]) == len(sbl["Phlm"]) == 25, "Phlm 25 verses in all three")
    check(set(RP_MERGED) == {("Acts", 24, 7)}, "only Acts 24:7 is merged from a separate RP file")
    check(sum(1 for k in RP_SEPARATE_DIFFERS if k[0] == "John") == 11 and ("John", 8, 8) not in RP_SEPARATE_DIFFERS,
          "JOH.csv prints John 7:53-8:11 itself; PA.csv differs in 11 of its 12 verses")
    check((7, 53) in sbl["John"] and (7, 53) in rp["John"], "RP and SBLGNT v1.2 both print John 7:53")
    check(("Rom", 16, 25) in WEB_EMPTY and (16, 25) not in web["Rom"], "WEB Rom 16:25 is an empty marker")
    check(WEB_EMPTY == {("Acts", 8, 37), ("Acts", 15, 34), ("Acts", 24, 7), ("Luke", 17, 36), ("Rom", 16, 25)},
          "WEB NT has exactly five empty (footnote-only) verse markers")
    check(all((8, 37) not in d for d in (web["Acts"], rp["Acts"], sbl["Acts"])), "Acts 8:37 printed by none")
    check(RP_MERGED.get(("Acts", 24, 7)) == "ACT24.csv", "Acts 24:7 merged from ACT24.csv")
    check(verse("rp", "3John", 1, 15) is None and expand_ref("rp", "3John", 1, 1, 1, 15) is None,
          "range guard: an end that the witness does not print is refused, never clamped")
    check(expand_ref("web", "Phlm", 1, 3, 1, 1) is None, "backward range refused")
    check(collate_greek("Ὁ πρεσβύτερος Γαΐῳ", rp["3John"][(1, 1)]) == "byte", "RP 3John 1:1 byte collate")
    check(("3John", 1, 2) in RP_PARAGRAPH and "¶" not in rp["3John"][(1, 2)], "pilcrow recorded and removed")
    status = "GREEN" if not fails else "RED"
    print(json.dumps({"status": status, "selftest": "greek_lib", "fails": fails}, ensure_ascii=False))
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(_selftest())
