#!/usr/bin/env python3
"""_test_marks_tools_1cor.py - T3 (cor_p0_toolport_t3_a1#e3) test of the three 1Cor ports: check_marks.py,
normalize_greek_in_json.py and run_validator_suite.py (static checks only; the suite is run on its own).

Every Greek fixture is sliced from 1Cor_rp.txt / 1Cor_sbl.txt by code at run time, and every verse fixture is chosen
from pmarks_1Cor.json by code, so nothing Greek and no site is typed here. Each vector is labelled 'ported' (with its
lineage in the predecessor test, Dan/tools/_test_zone_tools_dan.py) or 'created'.

Usage: _test_marks_tools_1cor.py [--tools-dir DIR] [--manifest OUT.json]
  --tools-dir  the directory holding the tools under test (default: this file's directory). cor_lib, greek_lib and the
               1Cor data always come from this file's directory and its parent (PYTHONPATH), so a deliberately broken
               copy of a tool can be tested alone.
  --manifest   write the full result (vectors, figures, parity, files read) to this JSON file.
Prints one JSON summary; exits 1 on any failed check.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import tokenize
import unicodedata
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
BOOKDIR = HERE.parent
sys.path.insert(0, str(HERE))
import cor_lib  # noqa: E402
from cor_lib import GREEK_RUN, LAST_VERSE, SIGLA, bounded_in, nfc, strip_accents  # noqa: E402
from greek_lib import TONE  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--tools-dir", default=None)
ap.add_argument("--manifest", default=None)
A = ap.parse_args()
TOOLS = Path(A.tools_dir).resolve() if A.tools_dir else HERE
ENV = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1", PYTHONPATH=str(HERE))
CM, NORM, SUITE = "check_marks.py", "normalize_greek_in_json.py", "run_validator_suite.py"
DANTEST = "Dan/tools/_test_zone_tools_dan.py"

RESULTS: list[dict] = []


def check(name, ok, detail=None):
    RESULTS.append({"name": name, "ok": bool(ok), **({} if ok else {"detail": str(detail)[:300]})})


def run(tool, *args, cwd=None):
    return subprocess.run([sys.executable, "-B", str(TOOLS / tool), *map(str, args)], capture_output=True,
                          text=True, encoding="utf-8", env=ENV, cwd=cwd)


# ---------------------------------------------------------------- data and fixture verses (chosen by code)
pm = json.loads((BOOKDIR / "pmarks_1Cor.json").read_text(encoding="utf-8"))
RP = set(pm["rp_paragraph_starts"])
WEBS = set(pm["web_paragraph_starts"])
WEB = WEBS | set(pm["web_paragraph_midverse"])
SBL = set(pm["sbl_variant_sites"])
ALLV = [(c, v) for c in sorted(LAST_VERSE) for v in range(1, LAST_VERSE[c] + 1)]


def key(c, v):
    return "1Cor.%d.%d" % (c, v)


def nxt(c, v):
    return (c, v + 1) if v < LAST_VERSE[c] else ((c + 1, 1) if c + 1 in LAST_VERSE else None)


def ks(p):
    return key(*p) if p else None


def cv(p):
    return "%d:%d" % p


def cvd(p):
    return "%d.%d" % p


def first(pred, what):
    for p in ALLV:
        if pred(*p):
            return p
    raise SystemExit(json.dumps({"status": "ERROR", "error": "no fixture verse for " + what}))


def none_in(s, c, lo, hi):
    return all(key(c, v) not in s for v in range(lo, hi + 1))


rp_only = first(lambda c, v: key(c, v) in RP and key(c, v) not in WEB and ks(nxt(c, v)) not in WEB, "rp_only")
web_only = first(lambda c, v: key(c, v) in WEBS and key(c, v) not in RP and ks(nxt(c, v)) not in RP, "web_only")
quiet = first(lambda c, v: all(x not in RP | WEB | SBL for x in (key(c, v), ks(nxt(c, v)))), "quiet")
w1_start = first(lambda c, v: key(c, v) not in RP and ks(nxt(c, v)) in RP, "w1_start")
sbl_site = first(lambda c, v: key(c, v) in SBL, "sbl_site")
sbl_w1 = first(lambda c, v: key(c, v) not in SBL and ks(nxt(c, v)) in SBL, "sbl_w1")
rp_int = first(lambda c, v: key(c, v) in RP and v >= 3 and v + 3 <= LAST_VERSE[c]
               and none_in(RP, c, v - 2, v - 1) and none_in(RP, c, v + 1, v + 3), "rp_interior")
web_int = first(lambda c, v: key(c, v) in WEBS and v >= 2 and v + 2 <= LAST_VERSE[c]
                and none_in(RP, c, v - 1, v + 2), "web_interior")
q_span = first(lambda c, v: v + 5 <= LAST_VERSE[c] and none_in(RP, c, v, v + 5), "quiet_span")
SPAN_RP = "%s-%s" % (key(rp_int[0], rp_int[1] - 2), key(rp_int[0], rp_int[1] + 2))
SPAN_WEB = "%s-%s" % (key(web_int[0], web_int[1] - 1), key(web_int[0], web_int[1] + 1))
SPAN_Q = "%s-%s" % (key(*q_span), key(q_span[0], q_span[1] + 4))
FIXTURES = {"rp_only": key(*rp_only), "web_only": key(*web_only), "quiet": key(*quiet), "w1_start": key(*w1_start),
            "sbl_site": key(*sbl_site), "sbl_w1": key(*sbl_w1), "span_rp_interior": SPAN_RP,
            "span_web_interior": SPAN_WEB, "span_quiet": SPAN_Q}

# ---------------------------------------------------------------- check_marks vectors
VEC: list[dict] = []


def cmv(section, lineage, text, expect, span=None, ref=None):
    vid = "t3cm_%03d" % (len(VEC) + 1)
    row = {"decision_id": vid, "boundary_rationale": text}
    if span:
        row["span"] = span
    VEC.append({"id": vid, "section": section, "ref": ref or span or "", "lineage": lineage,
                "text_source": "synthetic prose (no witness text)", "tool": CM, "row": row, "expect": expect})


C = "created"
cmv("typed claims", C, "RP pilcrow at %s opens the unit." % cv(rp_only), {"paragraph_mark_claim": False}, ref=key(*rp_only))
cmv("typed claims", C, "WEB paragraph at %s opens the unit." % cv(rp_only), {"paragraph_mark_claim": True}, ref=key(*rp_only))
cmv("typed claims", C, "WEB paragraph at %s opens the unit." % cv(web_only), {"paragraph_mark_claim": False}, ref=key(*web_only))
cmv("typed claims", C, "RP pilcrow at %s opens the unit." % cv(web_only), {"paragraph_mark_claim": True}, ref=key(*web_only))
cmv("typed claims", C, "A pilcrow stands at %s." % cv(web_only), {"paragraph_mark_claim": True}, ref=key(*web_only))
cmv("typed claims", C, "SBL critical sign at %s." % cv(sbl_site), {"paragraph_mark_claim": False}, ref=key(*sbl_site))
cmv("W1 keying", C, "SBL critical sign at %s." % cv(sbl_w1), {"paragraph_mark_claim": True}, ref=key(*sbl_w1))
cmv("W1 keying", C, "RP pilcrow at %s." % cv(w1_start), {"paragraph_mark_claim": False}, ref=key(*w1_start))
cmv("typed claims", C, "RP pilcrow at %s." % cv(quiet), {"paragraph_mark_claim": True}, ref=key(*quiet))
mid = tuple(int(x) for x in pm["web_paragraph_midverse"][0].split(".")[1:])
cmv("typed claims", C, "WEB paragraph at %s (mid-verse)." % cv(mid), {"paragraph_mark_claim": False}, ref=key(*mid))
cmv("symmetry", C, "RP pilcrow at %s opens the second paragraph." % cv(rp_int),
    {"mark_symmetry_gap": False, "paragraph_mark_claim": False}, span=SPAN_RP)
cmv("symmetry", C, "The argument turns here.", {"mark_symmetry_gap": True}, span=SPAN_RP)
cmv("typed absence", C, "No pilcrow stands in this span.", {"false_mark_absence_claim": True}, span=SPAN_RP)
cmv("typed absence", C, "No pilcrow stands in this span.",
    {"false_mark_absence_claim": False, "mark_symmetry_gap": False}, span=SPAN_WEB)
cmv("typed absence", C, "No WEB paragraph stands in this span.", {"false_mark_absence_claim": True}, span=SPAN_WEB)
cmv("typed absence", C, "No pilcrow stands in this span.",
    {"false_mark_absence_claim": False, "mark_symmetry_gap": False}, span=SPAN_Q)
cmv("typed absence", C, "No petuchah or setumah stands in this span.",
    {"false_mark_absence_claim": False, "paragraph_mark_claim": False}, span=SPAN_Q)
q, qd = cv(quiet), cvd(quiet)
H = "Hebrew arms (empty in 1Cor)"
cmv(H, C, "A petuchah follows %s." % q, {"paragraph_mark_claim": True}, ref=key(*quiet))
cmv(H, C, "A setumah stands here.", {"paragraph_mark_claim": True})
cmv(H, C, "The ketiv at %s differs from the qere." % q, {"kq_claim": True}, ref=key(*quiet))
cmv(H, C, "No K/Q touches this span.", {"kq_claim": False, "false_kq_absence_claim": False}, span=SPAN_Q)
cmv(H, C, "The puncta extraordinaria sit at %s." % q, {"puncta_claim_in_ezek": True}, ref=key(*quiet))
cmv(H, C, "No puncta stand in this span.", {"puncta_claim_in_ezek": False, "false_puncta_absence_claim": False},
    span=SPAN_Q)
cmv(H, C, "A small nun stands at %s." % q, {"small_letter_claim_in_jer": True}, ref=key(*quiet))
cmv(H, C, "Selah closes the unit.", {"selah_claim_in_jer": True})
cmv(H, C, "An inverted nun stands at %s." % q, {"nonexistent_seg_claim_in_jer": True}, ref=key(*quiet))
cmv(H, C, "A paseq at %s divides the clause." % q, {"paseq_false_presence": True}, ref=key(*quiet))
P = "ported: " + DANTEST
cmv("ported §2", P + " §2 lines 124-140 (cm_puncta_oshb_*_red)", "The puncta at rp:1Cor.%s mark the verse." % qd,
    {"puncta_claim_in_ezek": True}, ref=key(*quiet))
cmv("ported §2", P + " §2 lines 124-140 (cm_small_letter)", "a small nun at rp:1Cor.%s" % qd,
    {"small_letter_claim_in_jer": True}, ref=key(*quiet))
cmv("ported §2", P + " §2 lines 124-140 (cm_selah)", "The selah here closes the unit.", {"selah_claim_in_jer": True})
cmv("ported §2", P + " §2 lines 124-140 (mark type setumah; 1Cor has no PE/SAMEKH layer, so RED)",
    "a setumah follows %s" % qd, {"paragraph_mark_claim": True}, ref=key(*quiet))
cmv("ported §4", P + " §4 lines 244-275 (negated_ok)",
    "No K/Q, no paseq, no puncta and no zone-dual issue touches this span.",
    {"kq_claim": False, "false_kq_absence_claim": False, "paseq_false_presence": False,
     "puncta_claim_in_ezek": False, "false_puncta_absence_claim": False}, span=SPAN_Q)
cmv("ported §4", P + " §4 lines 244-275 (dotted_number_red)", "MT %s carries seven U+05C4 marks." % qd,
    {"puncta_claim_in_ezek": True}, ref=key(*quiet))
cmv("ported §4", P + " §4 lines 244-275 (kq_editorial_note_ok; polarity flipped: the note route is closed in 1Cor)",
    "the editorial note at %s records a ketiv/qere relative to BHS" % q, {"kq_claim": True}, ref=key(*quiet))
cmv("ported §4", P + " §4 lines 244-275 (span_covers_no_site_red)", "The puncta in this span carry the point.",
    {"puncta_claim_in_ezek": True}, span=SPAN_Q)
cmv("ported §5", P + " §5 lines 318-330 (t1_02)", "the puncta extraordinaria sit at %s in this span" % q,
    {"puncta_claim_in_ezek": True}, span=SPAN_Q)
# every site of every type, one row each (created): each type accepted at its own sites; RP never taken from WEB
for k in sorted(RP):
    cmv("every RP start", C, "RP pilcrow at %s." % k.split(".", 1)[1].replace(".", ":"), {"paragraph_mark_claim": False}, ref=k)
for k in sorted(WEB):
    cmv("every WEB start", C, "WEB paragraph at %s." % k.split(".", 1)[1].replace(".", ":"), {"paragraph_mark_claim": False}, ref=k)
for k in sorted(SBL):
    cmv("every SBL site", C, "SBL critical sign at %s." % k.split(".", 1)[1].replace(".", ":"), {"paragraph_mark_claim": False}, ref=k)
for c_, v_ in ALLV:
    if key(c_, v_) in WEBS and key(c_, v_) not in RP and ks(nxt(c_, v_)) not in RP:
        cmv("WEB-only start is no RP claim", C, "RP pilcrow at %d:%d." % (c_, v_), {"paragraph_mark_claim": True},
            ref=key(c_, v_))

# ---------------------------------------------------------------- normalizer fixtures (sliced by code)
RPV = cor_lib._read_tsv("1Cor_rp.txt")
SBLV = cor_lib._read_tsv("1Cor_sbl.txt")
rp_j = " ".join(RPV[k] for k in sorted(RPV))
sbl_j = " ".join(SBLV[k] for k in sorted(SBLV))
sbl_u = re.sub(r" {2,}", " ", re.sub("[" + SIGLA + "]", "", sbl_j))
rp_s, sbl_s = strip_accents(rp_j), strip_accents(sbl_u)
WORD = re.compile(r"[^\s,.;·:·()\[\]" + SIGLA + "]+")


def nfd(s):
    return unicodedata.normalize("NFD", s)


def tone(s):
    return any(ch in TONE for ch in nfd(s))


def pure(s):
    return all(ch == " " or ch.isalpha() or unicodedata.category(ch) == "Mn" for ch in s)


def one_run(s):
    ms = list(GREEK_RUN.finditer(s))
    return len(ms) == 1 and ms[0].group(0) == s


def windows(verses, n):
    for k in sorted(verses):
        ws = WORD.findall(verses[k])
        for i in range(len(ws) - n + 1):
            cand = " ".join(ws[i:i + n])
            if cand in verses[k] and pure(cand) and one_run(cand):
                yield k, cand


def pick(gen, what):
    for k, s in gen:
        return k, s
    raise SystemExit(json.dumps({"status": "ERROR", "error": "no witness fixture for " + what}))


def nowhere(s):
    return not (bounded_in(s, rp_j) or bounded_in(s, sbl_j) or bounded_in(s, sbl_u))


k_rp, rp_run = pick(((k, w) for k, w in windows(RPV, 3) if nfd(w) != w and tone(w)), "rp_run")
k_sbl, sbl_run = pick(((k, w) for k, w in windows(SBLV, 2) if not bounded_in(w, rp_j) and bounded_in(w, sbl_j)), "sbl_run")


def _unsigned():
    pat = re.compile(r"([^\s" + SIGLA + r",.;·:·]+)\s*[" + SIGLA + r"]+\s*([^\s" + SIGLA + r",.;·:·]+)")
    for k in sorted(SBLV):
        for m in pat.finditer(SBLV[k]):
            cand = m.group(1) + " " + m.group(2)
            if pure(cand) and one_run(cand) and nfc(cand) == cand and not bounded_in(cand, rp_j) \
                    and not bounded_in(cand, sbl_j) and bounded_in(cand, sbl_u):
                yield k, cand


k_uns, uns_run = pick(_unsigned(), "sbl_unsigned")
check("fixture: the sbl_unsigned run has an NFD form that differs from it (K2-D9 vector n09)", nfd(uns_run) != uns_run,
      uns_run)
k_men, men_run = pick(((k, strip_accents(w)) for k, w in windows(RPV, 2)
                       if not tone(strip_accents(w)) and strip_accents(w) != w and nowhere(strip_accents(w))
                       and bounded_in(strip_accents(w), rp_s) and one_run(strip_accents(w))), "mention")


def _accent():
    for k, w in windows(RPV, 2):
        d = nfd(w)
        if "́" in d:
            m = nfc(d.replace("́", "̀", 1))
            if tone(m) and nowhere(m) and bounded_in(strip_accents(m), rp_s) and one_run(m):
                yield k, m


k_acc, acc_run = pick(_accent(), "accent_mismatch")


def _cut():
    for k, w in windows(RPV, 1):
        c_ = w[1:]
        if len(w) >= 6 and tone(c_) and one_run(c_) and nowhere(c_) and not bounded_in(strip_accents(c_), rp_s) \
                and not bounded_in(strip_accents(c_), sbl_s) and c_ in rp_j:
            yield k, c_


k_cut, cut_run = pick(_cut(), "cut")
NEITHER = "ξυζξυζ ψωψω"
NV = [  # (id, section, lineage, text_source, value, expect)
    ("n01", "tiers", C, "1Cor_rp.txt %d:%d" % k_rp, rp_run, {"ok": 1, "fixed": 0, "defect_count": 0, "src.rp": 1}),
    ("n02", "tiers", C, "1Cor_sbl.txt %d:%d" % k_sbl, sbl_run, {"ok": 1, "defect_count": 0, "src.sbl": 1}),
    ("n03", "tiers", P + " §6 lines 452-460 (D3, NFD half; the Qere half is disabled)",
     "1Cor_rp.txt %d:%d, NFD" % k_rp, nfd(rp_run), {"ok": 0, "fixed": 1, "defect_count": 0, "src.fixed_from_rp": 1}),
    ("n04", "tiers", C, "1Cor_sbl.txt %d:%d, sign removed" % k_uns, uns_run,
     {"ok": 0, "sbl_unsigned": 1, "defect_count": 0}),
    ("n05", "tiers", C, "1Cor_rp.txt %d:%d, accent-stripped" % k_men, men_run, {"mention": 1, "defect_count": 0}),
    ("n06", "defects", C, "1Cor_rp.txt %d:%d, acute made grave" % k_acc, acc_run,
     {"defect_count": 1, "kind": "accent_mismatch"}),
    ("n07", "defects", P + " §10b lines 877-886 (S1-07 word-bounded presence)", "1Cor_rp.txt %d:%d, first letter cut" % k_cut,
     cut_run, {"defect_count": 1, "kind": "cut_inside_a_witness_word"}),
    ("n08", "defects", C, "synthetic", NEITHER, {"defect_count": 1, "kind": "in_neither_witness"}),
    ("n09", "defects", C + " (K2-D9: an NFD copy across a critical sign is E-01, not the counted tier)",
     "1Cor_sbl.txt %d:%d, sign removed, NFD" % k_uns, nfd(uns_run),
     {"sbl_unsigned": 0, "defect_count": 1, "kind": "nfd_across_a_critical_sign"}),
]
DISABLED = [
    {"lineage": P + " §3 lines 217-226", "what": "Qere accepted / pointed-run tier", "reason": "1Cor has no K/Q layer; there is no Qere tier"},
    {"lineage": P + " §5 lines 366-372", "what": "Qere across a verse boundary", "reason": "no Qere tier"},
    {"lineage": P + " §6 lines 452-460", "what": "raw-byte Qere (D3 Qere half)", "reason": "no Qere tier; the NFD half is ported as n03"},
]
for vid, sec, lin, src, val, exp in NV:
    VEC.append({"id": vid, "section": sec, "ref": src, "lineage": lin, "text_source": src, "tool": NORM,
                "row": {"decision_id": vid, "quote": val}, "expect": exp})

# ---------------------------------------------------------------- run the tools
with tempfile.TemporaryDirectory() as td:
    td = Path(td)
    cm_rows = td / "cm_vectors.jsonl"
    cm_rows.write_text("\n".join(json.dumps(v["row"], ensure_ascii=False) for v in VEC if v["tool"] == CM) + "\n",
                       encoding="utf-8")
    p = run(CM, cm_rows)
    try:
        rep = json.loads(p.stdout)
    except json.JSONDecodeError:
        rep = None
    check("check_marks: one JSON object", isinstance(rep, dict), (p.stdout[-300:], p.stderr[-300:]))
    flags = rep.get("flags", []) if isinstance(rep, dict) else []
    by = {}
    for f in flags:
        by.setdefault(f.get("decision_id"), set()).add(f.get("rule"))
    for v in VEC:
        if v["tool"] != CM:
            continue
        for rule, fires in v["expect"].items():
            got = rule in by.get(v["id"], set())
            check("check_marks %s [%s] %s: %s %s" % (v["id"], v["section"], v["ref"], rule,
                                                      "fires" if fires else "silent"),
                  got == fires, sorted(by.get(v["id"], set())))
    files = []
    for vid, *_rest in NV:
        f = td / (vid + ".json")
        f.write_text(json.dumps([next(v["row"] for v in VEC if v["id"] == vid)], ensure_ascii=False), encoding="utf-8")
        files.append(f)
    p = run(NORM, *files)
    outs = {}
    for line in p.stdout.splitlines():
        try:
            o = json.loads(line)
            outs[o.get("file")] = o
        except json.JSONDecodeError:
            pass
    check("normalizer: one JSON line per file", len(outs) == len(files), (p.stdout[-300:], p.stderr[-300:]))
    for vid, sec, lin, src, val, exp in NV:
        o = outs.get(vid + ".json", {})
        for k_, want in exp.items():
            if k_ == "kind":
                got = bool(o.get("defects")) and o["defects"][0].startswith(want + " ")
                check("normalizer %s [%s]: defect kind %s" % (vid, src, want), got, o.get("defects"))
            elif k_.startswith("src."):
                check("normalizer %s [%s]: ok_sources.%s == %s" % (vid, src, k_[4:], want),
                      o.get("ok_sources", {}).get(k_[4:]) == want, o.get("ok_sources"))
            else:
                check("normalizer %s [%s]: %s == %s" % (vid, src, k_, want), o.get(k_) == want, o)
    # --write: only the fixed run changes
    wf = td / "write_case.json"
    wf.write_text(json.dumps([{"decision_id": "w01", "quote": nfd(rp_run), "note": "kept as written"}],
                             ensure_ascii=False), encoding="utf-8")
    p = run(NORM, "--write", wf)
    back = json.loads(wf.read_text(encoding="utf-8"))
    check("normalizer --write: the NFD run becomes the RP bytes", back[0]["quote"] == rp_run, back[0]["quote"][:40])
    check("normalizer --write: LF line ends only, no CR byte (K2-D5, E-73)", b"\r" not in wf.read_bytes())
    check("normalizer --write: other fields untouched", back[0]["note"] == "kept as written"
          and back[0]["decision_id"] == "w01", back[0])
    # witness refusal, by resolved path and by case-folded name
    for arg in (BOOKDIR / "1Cor_rp.txt", td / "1COR_SBL.TXT"):
        p = run(NORM, arg)
        try:
            o = json.loads(p.stdout)
        except json.JSONDecodeError:
            o = {}
        check("normalizer refuses witness argument %s" % arg.name, p.returncode == 2 and o.get("refused"), p.stdout[-200:])
VEC.append({"id": "w01", "section": "write path", "ref": "1Cor_rp.txt %d:%d" % k_rp, "lineage": C,
            "text_source": "1Cor_rp.txt %d:%d, NFD" % k_rp, "tool": NORM})
VEC.append({"id": "r01", "section": "witness refusal", "ref": "1Cor_rp.txt / 1COR_SBL.TXT", "lineage": C,
            "text_source": "path only (never read)", "tool": NORM})

# ---------------------------------------------------------------- data and identity
check("verse count 437", sum(LAST_VERSE.values()) == 437, sum(LAST_VERSE.values()))
bad_id = [p_ for p_ in ALLV if not (cor_lib.web_to_greek(*p_) == p_ and cor_lib.greek_to_web(*p_) == p_
                                    and cor_lib.mt_to_web_all(*p_) == [p_] and cor_lib.web_to_mt(*p_) == p_)]
check("identity readings over every verse (web_to_greek, greek_to_web, mt_to_web_all, web_to_mt)", not bad_id, bad_id[:5])
P_SINGLE = sorted("%s %d:%d" % (n_, *k_) for n_, vs_ in (("rp", RPV), ("sbl", SBLV)) for k_, t_ in vs_.items() if nfc(t_) != t_)
check("witness letters and marks are NFC (RP, SBL); punctuation singletons only: %s" % P_SINGLE,
      all(nfc(x) == x for x in ("".join(nfc(ch) if unicodedata.category(ch)[0] == "P" else ch for ch in t_)
                                for t_ in list(RPV.values()) + list(SBLV.values()))))
web_text = (BOOKDIR / "1Cor_web_clean.txt").read_text(encoding="utf-8")
heb = [n for n, t in (("rp", rp_j), ("sbl", sbl_j), ("web", web_text)) if re.search("[֐-׿]", t)]
check("no Hebrew code point (U+0590-U+05FF) in any witness", not heb, heb)
check("pmarks counts (RP 35, WEB 87 + 1 mid-verse, SBL 220)",
      (len(RP), len(WEBS), len(pm["web_paragraph_midverse"]), len(SBL)) == (35, 87, 1, 220),
      (len(RP), len(WEBS), len(SBL)))

# ---------------------------------------------------------------- static scans of the tools
LINEAGE_LINE = re.compile(r"\bDan\b|Daniel|Ezek|\bJer\b|\bIsa\b|\bPs\b|S1-\d|\bE-\d|#e\d|\bT\d-|\bR4|\bK2\b|\bD\d\b|"
                          r"\bW\d\b|lineage|predecessor|OW-\d|TOOLFIX|FLAGS-|ruling", re.I)
MEASURED = {437, 35, 87, 220}
parity, read_by, figures, sha = {}, {}, [], {}
for tool in (CM, NORM, SUITE):
    src = (TOOLS / tool).read_bytes()
    sha[tool] = hashlib.sha256(src).hexdigest()
    text = src.decode("utf-8")
    tree = ast.parse(text)
    used = set()
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
            if node.module == "cor_lib":
                used |= {a.name for a in node.names}
        elif isinstance(node, ast.Import):
            imports |= {a.name for a in node.names}
        elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == "cor_lib":
            used.add(node.attr)
    missing = sorted(n for n in used if not hasattr(cor_lib, n))
    parity[tool] = {"cor_lib_names_used": sorted(used), "missing": missing}
    check("%s: every cor_lib name it uses exists" % tool, not missing, missing)
    check("%s: no dan_lib import" % tool, "dan_lib" not in imports, sorted(imports))
    consts = {n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str)}
    read_by[tool] = sorted(s for s in consts if re.fullmatch(r"[\w%.-]+\.(?:json|jsonl|txt|tsv)", s))
    lines = text.splitlines()
    for tok in tokenize.generate_tokens(io.StringIO(text).readline):
        if tok.type == tokenize.NUMBER:
            nums, emitted = [tok.string], False
        elif tok.type == tokenize.STRING:
            nums, emitted = re.findall(r"(?<![\w.])\d{2,}(?![\w])", tok.string), True
        else:
            continue
        for s in nums:
            try:
                n = int(s)
            except ValueError:
                continue
            if n < 10:
                continue
            line = lines[tok.start[0] - 1]
            cls = "lineage" if LINEAGE_LINE.search(line) else ("cor_measured" if n in MEASURED else "neither")
            action = {"lineage": "keep: ruling id or history", "cor_measured": "keep: measured 1Cor figure"}.get(
                cls, "keep: code constant (window/limit), not a book figure" if not emitted else "review")
            figures.append({"tool": tool, "line": tok.start[0], "number": n, "class": cls, "emitted": emitted,
                            "action": action})
    check("%s: no predecessor verse total 357 in any string" % tool,
          not any(f["number"] == 357 and f["emitted"] and f["tool"] == tool for f in figures))
suite_consts = {n.value for n in ast.walk(ast.parse((TOOLS / SUITE).read_text(encoding="utf-8")))
                if isinstance(n, ast.Constant) and isinstance(n.value, str)}
check("suite runs normalize_greek_in_json.py, not the Hebrew normalizer",
      "normalize_greek_in_json.py" in suite_consts and "normalize_hebrew_in_json.py" not in suite_consts)
check("suite has no language_zones member", "check_language_zones.py" not in suite_consts)
check("suite sums the Greek tier keys", {"sbl_unsigned", "mention", "fixed", "defect_count"} <= suite_consts)
# K2-D6: a Python child started without -B caches cor_lib's bytecode inside SP
check("suite starts every member with -B (K2-D6)", "-B" in suite_consts)
no_b = [f.name for f in sorted(TOOLS.glob("*.py")) if not f.name.startswith("_adapt_")
        and re.search(r"sys\.executable,\s*str\(", f.read_text(encoding="utf-8"))]
check("no tool starts a Python child without -B (K2-D6)", not no_b, no_b)
# K2-D3: the brief checker must discover every member the suite registers, by run( or run_each(
suite_members = {k.value for d in ast.walk(ast.parse((TOOLS / SUITE).read_text(encoding="utf-8")))
                 if isinstance(d, ast.Dict) for k, v in zip(d.keys, d.values)
                 if isinstance(k, ast.Constant) and isinstance(v, ast.Call)
                 and getattr(v.func, "id", "") in ("run", "run_each")}
with tempfile.TemporaryDirectory() as td2:
    no_duty = Path(td2) / "no_duty.md"
    no_duty.write_bytes(b"a brief that names no duty\n")
    p = run("check_brief_vs_suite.py", no_duty)
listed = set(re.findall(r"^  .{14} (\w+)", p.stdout, re.M))
check("brief checker lists every suite member (K2-D3)", suite_members and suite_members <= listed,
      sorted(suite_members - listed))
check("brief checker maps greek_normalize_dryrun to a duty (K2-D3)",
      re.search(r"^  DUTY MISSING\s+greek_normalize_dryrun ", p.stdout, re.M), p.stdout[-400:])
read_by["cor_lib.py (shared)"] = sorted({n.value for n in ast.walk(ast.parse((HERE / "cor_lib.py").read_text(encoding="utf-8")))
                                        if isinstance(n, ast.Constant) and isinstance(n.value, str)
                                        and re.fullmatch(r"[\w%.-]+\.(?:json|jsonl|txt|tsv)", n.value)})

passed = sum(r["ok"] for r in RESULTS)
failed = [r for r in RESULTS if not r["ok"]]
if A.manifest:
    Path(A.manifest).write_text(json.dumps({
        "tools_dir": str(TOOLS), "tool_sha256": sha, "fixtures": FIXTURES,
        "vectors": [{k: v[k] for k in ("id", "section", "ref", "lineage", "text_source", "tool")} for v in VEC],
        "disabled": DISABLED, "cor_lib_parity": parity, "files_read_by_tool": read_by,
        "predecessor_figures": figures, "results": RESULTS}, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({"tools_dir": str(TOOLS), "checks": len(RESULTS), "passed": passed, "failed": len(failed),
                  "vectors": len(VEC), "ported": sum(v["lineage"].startswith("ported") for v in VEC),
                  "failures": failed[:40]}, ensure_ascii=False))
sys.exit(1 if failed else 0)
