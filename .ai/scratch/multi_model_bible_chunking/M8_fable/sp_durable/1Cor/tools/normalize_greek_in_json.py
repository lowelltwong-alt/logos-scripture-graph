#!/usr/bin/env python3
"""normalize_greek_in_json.py - 1Cor (T3 port of the predecessor's normalize_hebrew_in_json.py: its file walk, output
line and --write path are kept; its tiers are replaced by Greek ones modelled on
greek_substrate/tools/normalize_greek_in_json.py).

Every Greek run (cor_lib.GREEK_RUN, at least MIN_LEN letters) in every string value at any depth of every row is
looked for in the two Greek witnesses, 1Cor_rp.txt and 1Cor_sbl.txt, word-bounded at letter and mark edges
(S1-07: cor_lib.bounded_in). Tiers, first match wins:
  ok            the run's bytes stand in RP or SBLGNT. RP and SBLGNT differ at many verses; both readings are
                legitimate, and ok_sources says which witness carried each run (RP is tried first)
  fixed         only the run's NFC form stands there (E-01: the suite treats fixed > 0 as HARD). --write replaces
                each such run with its NFC form, preferring RP; nothing else in the file changes
  sbl_unsigned  the run stands in SBLGNT only once SBLGNT's critical signs are removed: SBLGNT wording quoted
                across an interior sign without disclosing it. Counted, not a defect; the row's own sign
                disclosure is check_marks' business
  mention       the run carries NO tone mark (greek_lib.TONE) and its accent-stripped form stands in a witness's
                accent-stripped text: a deliberate unaccented mention. Skeleton is never accepted: it casefolds,
                drops elision and turns punctuation and the critical signs into spaces
  defect        anything else: a mis-accented run, a run cut inside a witness word, or wording in neither witness
A quote that carries critical signs is split at them by GREEK_RUN, and each side is judged alone. There is no
Qere-style tier: 1Cor is a Greek book with no K/Q layer.
Fail closed: a witness verse whose letters and marks are not NFC stops the run (punctuation singletons such as
U+037E are tolerated: letters_nfc) (status ERROR, exit 2); so does any argument naming a
witness file, refused before anything is read, so --write can never touch a witness.

Usage: normalize_greek_in_json.py [--write] rows.jsonl|file.json ...
Prints one JSON line per file: {file, mode, ok, fixed, sbl_unsigned, mention, ok_sources, defects, defect_count};
exits 1 on any defect.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

FREEZE = Path(__file__).resolve().parent
MIN_LEN = 2   # lesson f (Ps close): the standard re-splice cure runs MIN_LEN=2
sys.path.insert(0, str(FREEZE))
import cor_lib  # noqa: E402
from cor_lib import GREEK_RUN, SIGLA, bounded_in, nfc, strip_accents  # noqa: E402   S1-07: word-bounded at every tier
from greek_lib import TONE  # noqa: E402   (importable once cor_lib has put greek_substrate/tools on the path)

BOOKDIR = cor_lib.SPBOOK
WITNESSES = ("1Cor_rp.txt", "1Cor_sbl.txt", "1Cor_web_clean.txt")
SIGN_RE = re.compile("[" + SIGLA + "]")


def refused_args(args):
    """Every argument that names a witness file, by name (case-folded) or by resolved path."""
    names = {w.casefold() for w in WITNESSES}
    paths = {(BOOKDIR / w).resolve() for w in WITNESSES}
    return [a for a in args if Path(a).name.casefold() in names or Path(a).resolve() in paths]


def letters_nfc(t: str) -> bool:
    """NFC everywhere except a canonical-singleton punctuation code point (U+037E GREEK QUESTION MARK, which NFC
    turns into ';', stands in 5 SBLGNT verses: 5:13, 6:19, 7:18, 7:21, 7:27). Runs are letters, so it never sits inside one."""
    t2 = "".join(nfc(ch) if unicodedata.category(ch)[0] == "P" else ch for ch in t)
    return nfc(t2) == t2


def build_index():
    """The two witnesses, verse texts joined by one space (a run may cross a verse boundary). Fails closed on a
    witness verse that is not NFC."""
    idx = {}
    for sp in ("rp", "sbl"):
        verses = cor_lib._read_tsv("1Cor_%s.txt" % sp)
        bad = sorted("%d.%d" % k for k, t in verses.items() if not letters_nfc(t))
        if bad:
            raise ValueError("1Cor_%s.txt: %d verse(s) not NFC, first %s" % (sp, len(bad), bad[0]))
        idx[sp] = " ".join(verses[k] for k in sorted(verses))
    idx["sbl_unsigned"] = re.sub(r" {2,}", " ", SIGN_RE.sub("", idx["sbl"]))
    idx["rp_stripped"] = strip_accents(idx["rp"])
    idx["sbl_stripped"] = strip_accents(idx["sbl_unsigned"])
    return idx


def greek_letters(s: str) -> int:
    return sum(1 for ch in s if ch.isalpha() and ("Ͱ" <= ch <= "Ͽ" or "ἀ" <= ch <= "῿"))


def classify(run: str, idx) -> tuple[str, str | None]:
    """(tier, source) for one run; source is 'rp' or 'sbl' for ok and fixed, else None."""
    for sp in ("rp", "sbl"):
        if bounded_in(run, idx[sp]):
            return "ok", sp
    n = nfc(run)
    if n != run:
        for sp in ("rp", "sbl"):
            if bounded_in(n, idx[sp]):
                return "fixed", sp
    if bounded_in(n, idx["sbl_unsigned"]):
        return "sbl_unsigned", None
    has_tone = any(ch in TONE for ch in unicodedata.normalize("NFD", run))
    if not has_tone:
        s = strip_accents(n)
        if bounded_in(s, idx["rp_stripped"]) or bounded_in(s, idx["sbl_stripped"]):
            return "mention", None
    if has_tone and (bounded_in(strip_accents(n), idx["rp_stripped"])
                     or bounded_in(strip_accents(n), idx["sbl_stripped"])):
        return "defect:accent_mismatch", None
    if n in idx["rp"] or n in idx["sbl"] or n in idx["sbl_unsigned"]:
        return "defect:cut_inside_a_witness_word", None
    return "defect:in_neither_witness", None


def fix_string(s: str, idx, stats, defects) -> str:
    out, pos = [], 0
    for m in GREEK_RUN.finditer(s):
        run = m.group(0)
        lead = len(run) - len(run.lstrip("’ʼ ,.·;·"))
        run = run[lead:]
        if greek_letters(run) < MIN_LEN:
            continue
        tier, src = classify(run, idx)
        if tier.startswith("defect"):
            defects.append("%s %r" % (tier.split(":", 1)[1], run[:60]))
            continue
        stats[tier] += 1
        if tier == "ok":
            stats["ok_sources"][src] += 1
        elif tier == "fixed":
            stats["ok_sources"]["fixed_from_" + src] += 1
            out.append(s[pos:m.start() + lead])
            out.append(nfc(run))
            pos = m.end()
    out.append(s[pos:])
    return "".join(out)


def walk(o, idx, stats, defects):
    if isinstance(o, list):
        return [walk(x, idx, stats, defects) for x in o]
    if isinstance(o, dict):
        return {k: walk(v, idx, stats, defects) for k, v in o.items()}
    if isinstance(o, str):
        return fix_string(o, idx, stats, defects)
    return o


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    args = [a for a in sys.argv[1:] if a != "--write"]
    write = "--write" in sys.argv
    refused = refused_args(args)
    if refused:
        print(json.dumps({"status": "ERROR", "refused": refused,
                          "error": "a witness file is never an input to the normalizer"}, ensure_ascii=False))
        return 2
    try:
        idx = build_index()
    except (OSError, ValueError) as e:
        print(json.dumps({"status": "ERROR", "error": str(e)[:300]}, ensure_ascii=False))
        return 2
    any_defects = False
    for f in args:
        p = Path(f)
        text = p.read_text(encoding="utf-8-sig")
        is_jsonl = p.suffix == ".jsonl"
        if is_jsonl:
            data = [json.loads(l) for l in text.splitlines() if l.strip()]
        else:
            data = json.loads(text)
        stats = {"ok": 0, "fixed": 0, "sbl_unsigned": 0, "mention": 0,
                 "ok_sources": {"rp": 0, "sbl": 0, "fixed_from_rp": 0, "fixed_from_sbl": 0}}
        defects: list[str] = []
        new = walk(data, idx, stats, defects)
        if write and stats["fixed"]:
            if is_jsonl:
                p.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in new) + "\n",
                             encoding="utf-8")
            else:
                p.write_text(json.dumps(new, indent=1, ensure_ascii=False), encoding="utf-8")
        print(json.dumps({"file": p.name, "mode": "write" if write else "dry-run",
                          **stats, "defects": defects[:15], "defect_count": len(defects)},
                         ensure_ascii=False))
        any_defects = any_defects or bool(defects)
    return 1 if any_defects else 0


if __name__ == "__main__":
    sys.exit(main())
