#!/usr/bin/env python3
"""Exhaustive and adversarial tests for the 1Cor arms of citation_sweep.py (and the register and WEB-quote checks).

Ported from the predecessor book's zone test by _adapt_tools_1cor.py with the extra spec of lane T1. Every section
keeps its number there; every vector carries an 'L:' comment naming its source vector id ('ported') or saying 'created'
(written for 1Cor). The check_marks and normalizer parts are deferred to the marks lane (DEFERRED_TO_MARKS_LANE below).
1. PROPERTY (exhaustive): the zone predicates state on their face that no verse is in a zone, for every verse of all
   three spaces (web:, rp:, sbl:), and the range-guarded crosswalk is the identity inside the book and None outside it.
2. VECTORS: one fixture row per behaviour, run through the tool as a subprocess exactly as the suite runs it, matched by
   decision_id. 1Cor has no Hebrew device of any class, so a ported vector whose claim was TRUE in the source book is its
   negative here (RED), and a ported denial is a true denial (GREEN). Every Greek form is sliced from 1Cor_rp.txt or
   1Cor_sbl.txt and every WEB form from 1Cor_web_clean.txt at run time, never typed.
Writes only to a temporary directory. Exit 1 on any failure.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
BOOK = HERE.parent
sys.path.insert(0, str(HERE))
from cor_lib import (GREEK_LAST_VERSE, LAST_VERSE, SIGLA, collate, greek_to_web, load_pmarks,  # noqa: E402
                     load_web_clean, web_to_greek)
import citation_sweep as cs  # noqa: E402

results = []
DEFERRED_TO_MARKS_LANE = ["CM_VECTORS (section 2)", "PUNCTA2_CM (4)", "T1_CM (5)", "T2_CM (6)", "R4II_CM (8)",
                          "T4_CM (9)", "E4_CM (9b)", "S10B_CM (10b)", "S10C_CM (10c)",
                          "normalize_hebrew_in_json.py vectors (3, 5, 6, 10b)"]


def check(name, ok, detail=None):
    entry = {"check": name, "ok": bool(ok)}
    if not ok and detail:
        entry["detail"] = detail
    results.append(entry)


def tsv(name):
    """verse key -> text, sliced byte-exact from a pinned witness file."""
    out = {}
    for line in (BOOK / name).read_text(encoding="utf-8").splitlines():
        k, t = line.split("\t", 1)
        c, v = k.split(".")[1:]
        out[(int(c), int(v))] = t
    return out


RP, SBL = tsv("1Cor_rp.txt"), tsv("1Cor_sbl.txt")
WEB = load_web_clean()   # 1Cor_web_clean.txt, '[fn]' markers kept

# 1. PROPERTY (exhaustive). L: ported=section 1 | the zone predicates against the crosswalk, now over three spaces
SPACES = {"web": LAST_VERSE, "rp": GREEK_LAST_VERSE, "sbl": GREEK_LAST_VERSE}
for kind, space in SPACES.items():
    verses = [(c, v) for c in space for v in range(1, space[c] + 1)]
    pred = cs.web_pairs_in_offset_zone if kind == "web" else cs.greek_pairs_in_offset_zone
    moved = [p for p in verses if (web_to_greek(*p) if kind == "web" else greek_to_web(*p)) != p]
    zoned = [p for p in verses if pred([p])]
    check("%s: no zone and an identity crosswalk, all %d verses" % (kind, len(verses)),
          len(verses) == 437 and len(space) == 16 and not moved and not zoned, [len(verses), moved[:3], zoned[:3]])
check("zone predicates state no zone on their face (no crosswalk call)",
      all(not ({"web_to_greek", "greek_to_web"} & set(f.__code__.co_names))
          for f in (cs.web_pairs_in_offset_zone, cs.greek_pairs_in_offset_zone)))
outside = [(17, 1), (1, 0), (1, LAST_VERSE[1] + 1), (16, LAST_VERSE[16] + 1)]
check("crosswalk is range-guarded: None outside the book", all(web_to_greek(*p) is None and greek_to_web(*p) is None
                                                               for p in outside))
check("witness facts: RP and SBLGNT 437 verses each, same keys as WEB, 0 Hebrew letters",
      len(RP) == len(SBL) == 437 and set(RP) == set(SBL) == set(WEB)
      and not any(re.search("[\u0590-\u05ff]", t) for t in list(RP.values()) + list(SBL.values())))
check("pmarks: 13 WEB footnote verses", len(load_pmarks()["web_footnote_verses"]) == 13)


def xx(kind, c, v, tail=""):
    """A single-verse X-X ref, built where a literal would name a verse 1Cor lacks."""
    return "%s:1Cor.%d.%d-1Cor.%d.%d%s" % (kind, c, v, c, v, tail)


# Greek fixtures, sliced by code. L: created
RP_Q = " ".join(RP[(10, 23)].split()[:3]).rstrip(",.;·")                 # RP 10:23 opens with three words that carry 'moi'
_sw = SBL[(10, 23)].split(" ")
_k = next(i for i, w in enumerate(_sw) if cs.SIGLA_RE.search(w))
_k2 = next(i for i, w in enumerate(_sw) if i > 0 and cs.SIGLA_RE.search(w))   # a sign inside the span
SBL_Q = " ".join(_sw[_k:_k + 2]).rstrip(",.;·")              # SBLGNT 10:23 opens without 'moi'
SIG_Q = " ".join(_sw[_k2 - 1:_k2 + 2]).rstrip(",.;·")         # a span with an SBLGNT critical sign inside it
NOSIG_Q = cs.SIGLA_RE.sub("", SIG_Q)
RP24 = " ".join(RP[(10, 24)].split()[:3]).rstrip(",.;·")
NFD_Q = unicodedata.normalize("NFD", RP_Q)
ACC_Q = unicodedata.normalize("NFC", "".join(ch for ch in NFD_Q if ch not in "̀́͂"))   # accents only
SKEL_Q = unicodedata.normalize("NFC", "".join(ch for ch in NFD_Q if not unicodedata.combining(ch)))
_w3 = RP_Q.split(" ")[2]
CUT_END = " ".join(RP_Q.split(" ")[:2] + [_w3[:-1]])
CUT_START = RP_Q[1:]
ROOT_IN = _w3[1:-1]
check("fixtures: tiers of the sliced Greek forms are as the vectors need",
      [collate(RP_Q, RP[(10, 23)]), collate(RP_Q, SBL[(10, 23)]), collate(SBL_Q, SBL[(10, 23)]),
       collate(SBL_Q, RP[(10, 23)]), collate(SIG_Q, SBL[(10, 23)]), collate(NOSIG_Q, SBL[(10, 23)]),
       collate(NFD_Q, RP[(10, 23)]), collate(ACC_Q, RP[(10, 23)]), collate(SKEL_Q, RP[(10, 23)])]
      == ["byte", "none", "byte", "none", "byte", "skeleton", "nfc", "accent_stripped", "skeleton"],
      [RP_Q, SBL_Q, SIG_Q])
HEB3 = "\u05d3\u05d1\u05e8"   # a three-letter Hebrew word built by escape (no aleph: aleph is also a manuscript siglum)
PAPYRUS = "\U0001d513" + "46"

# 2. VECTORS (decision_id, boundary_evidence_refs, expected problem substring or None for "no problem at all")
CS_VECTORS = [
    # L: ported=cs_puncta_web_4_20_red | no puncta site in 1Cor: the claim stays RED
    ("cs_puncta_web_4_20_red", ["web:1Cor.4.20-1Cor.4.20 puncta extraordinaria (single-witness)"], "claims puncta extraordinaria"),
    # L: ported=cs_puncta_oshb_8_22_red | re-pointed to the rp: space, 8:12
    ("cs_puncta_rp_8_12_red", ["rp:1Cor.8.12-1Cor.8.12 puncta extraordinaria (single-witness)"], "claims puncta extraordinaria"),
    # L: ported=cs_puncta_web_1_20_bad
    ("cs_puncta_web_1_20_bad", ["web:1Cor.1.20-1Cor.1.20 puncta extraordinaria (single-witness)"], "claims puncta extraordinaria"),
    # L: ported=cs_zone_bare_web_4_5 | negative: no zone, so a bare ref needs no disclosure
    ("cs_no_zone_bare_web_4_5_ok", ["web:1Cor.4.5-1Cor.4.5"], None),
    # L: ported=cs_zone_bare_web_4_1 | negative
    ("cs_no_zone_bare_web_4_1_ok", ["web:1Cor.4.1-1Cor.4.1"], None),
    # L: ported=cs_zone_bare_mt_4_2 | negative, re-pointed to rp:
    ("cs_no_zone_bare_rp_4_2_ok", ["rp:1Cor.4.2-1Cor.4.2"], None),
    # L: ported=cs_dan_zone_bare_web_5_31 | negative; 5:13 is the chapter's last verse in 1Cor
    ("cs_no_zone_bare_web_5_13_ok", ["web:1Cor.5.13-1Cor.5.13"], None),
    # L: ported=cs_dan_zone_bare_web_6_28 | negative; 6:20 is the chapter's last verse in 1Cor
    ("cs_no_zone_bare_web_6_20_ok", ["web:1Cor.6.20-1Cor.6.20"], None),
    # L: ported=cs_dan_zone_bare_mt_3_31 | negative, sbl:; 3:23 is the chapter's last verse in 1Cor
    ("cs_no_zone_bare_sbl_3_23_ok", ["sbl:1Cor.3.23-1Cor.3.23"], None),
    # L: ported=cs_dan_zone_bare_mt_6_1 | negative, rp:
    ("cs_no_zone_bare_rp_6_1_ok", ["rp:1Cor.6.1-1Cor.6.1"], None),
    # L: ported=cs_dan_zone_bare_mt_6_29 | negative, sbl:
    ("cs_no_zone_bare_sbl_6_20_ok", ["sbl:1Cor.6.20-1Cor.6.20"], None),
    # L: ported=cs_edge_web_3_30_ok | re-pointed to 3:23
    ("cs_edge_web_3_23_ok", ["web:1Cor.3.23-1Cor.3.23"], None),
    # L: ported=cs_edge_web_7_1_ok
    ("cs_edge_web_7_1_ok", ["web:1Cor.7.1-1Cor.7.1"], None),
    # L: ported=cs_dan_edge_web_5_30_ok | re-pointed to 5:13
    ("cs_edge_web_5_13_ok", ["web:1Cor.5.13-1Cor.5.13"], None),
    # L: ported=cs_dan_edge_mt_3_30_ok | re-pointed to rp:1Cor.3.23
    ("cs_edge_rp_3_23_ok", ["rp:1Cor.3.23-1Cor.3.23"], None),
    # L: ported=cs_dan_edge_mt_5_30_ok | re-pointed to sbl:1Cor.5.13
    ("cs_edge_sbl_5_13_ok", ["sbl:1Cor.5.13-1Cor.5.13"], None),
    # L: ported=cs_dan_edge_mt_7_1_ok | rp:
    ("cs_edge_rp_7_1_ok", ["rp:1Cor.7.1-1Cor.7.1"], None),
    # L: ported=cs_dual_ok | identity: the right pairing is the same verse
    ("cs_dual_ok", ["web:1Cor.4.10-1Cor.4.10 = rp:1Cor.4.10"], None),
    # L: ported=cs_dual_bad | the source book's zone pairing is wrong arithmetic here
    ("cs_dual_bad", ["web:1Cor.4.10-1Cor.4.10 = rp:1Cor.4.9"], "dual-cite arithmetic wrong"),
    # L: created | the sbl: and the reverse dual forms
    ("cs_dual_sbl_ok", ["web:1Cor.15.3-1Cor.15.3 = sbl:1Cor.15.3"], None),
    ("cs_dual_sbl_bad", ["web:1Cor.15.3-1Cor.15.3 = sbl:1Cor.15.4"], "dual-cite arithmetic wrong"),
    ("cs_dual_reverse_ok", ["rp:1Cor.11.2-1Cor.11.2 = web:1Cor.11.2"], None),
    ("cs_dual_reverse_bad", ["sbl:1Cor.11.2-1Cor.11.2 = web:1Cor.11.3"], "dual-cite arithmetic wrong"),
    # L: ported=cs_mt_qualifier_ok | the MT qualifier re-pointed to RP and SBL
    ("cs_rp_qualifier_ok", ["web:1Cor.4.5-1Cor.4.5 (RP 4:5)"], None),
    # L: created
    ("cs_sbl_qualifier_bad", ["web:1Cor.4.5-1Cor.4.5 (SBL 4:6)"], "Greek qualifier wrong"),
    ("cs_web_qualifier_ok", ["rp:1Cor.4.5-1Cor.4.5 (WEB 4:5)"], None),
    ("cs_web_qualifier_bad", ["sbl:1Cor.4.5-1Cor.4.5 (WEB 4.4)"], "WEB qualifier wrong"),
    ("cs_greek_qualifier_on_rp_bad", ["rp:1Cor.4.5-1Cor.4.5 (SBL 4:5)"], "Greek qualifier on a non-web ref"),
    # L: ported=cs_oshb_4_35_out_of_range | rp: space
    ("cs_rp_out_of_range", [xx("rp", 4, GREEK_LAST_VERSE[4] + 1)], "out of range for RP"),
    # L: created
    ("cs_sbl_out_of_range", [xx("sbl", 16, GREEK_LAST_VERSE[16] + 1)], "out of range for SBL"),
    # L: ported=cs_dan_web_3_31_out_of_range
    ("cs_web_3_out_of_range", [xx("web", 3, LAST_VERSE[3] + 1)], "out of range for WEB"),
    # L: created | chapter, verse 0 and range END guards in each space
    ("cs_chapter_17_bad", ["rp:1Cor.%d.1" % (len(GREEK_LAST_VERSE) + 1)], "chapter out of range"),
    ("cs_verse_0_bad", ["web:1Cor.%d.%d" % (1, 0)], "always invalid"),
    ("cs_range_end_bad", ["sbl:1Cor.10.1-%d" % (GREEK_LAST_VERSE[10] + 1)], "range END out of range"),
    ("cs_range_backwards_bad", ["web:1Cor.10.5-1Cor.10.2"], "range END precedes start"),
    # L: ported=cs_small_letter | fabrication class
    ("cs_small_letter", ["web:1Cor.1.1-1Cor.1.1 small nun (single-witness)"], "NO special-letter segs of any class"),
    # L: ported=cs_large_letter | fabrication class
    ("cs_large_letter", ["web:1Cor.1.1-1Cor.1.1 large letter (single-witness)"], "NO special-letter segs of any class"),
    # L: created | denials pass
    ("cs_small_letter_denied_ok", ["web:1Cor.1.1-1Cor.1.1 (no small letter)"], None),
    ("cs_selah_denied_ok", ["rp:1Cor.1.1-1Cor.1.1 (no selah)"], None),
    # L: ported=cs_qumran_siglum | cross-tradition: a papyrus by number
    ("cs_papyrus_number", ["web:1Cor.1.1-1Cor.1.1 per P46"], "cross-tradition material"),
    # L: ported=cs_masada_siglum | a majuscule by name
    ("cs_majuscule_name", ["rp:1Cor.1.1-1Cor.1.1 per Codex Sinaiticus"], "cross-tradition material"),
    # L: ported=cs_dan_papyrus_siglum | the papyrus symbol
    ("cs_papyrus_symbol", ["web:1Cor.1.1-1Cor.1.1 per " + PAPYRUS], "cross-tradition material"),
    # L: ported=cs_dan_theodotion | a version
    ("cs_version_vulgate", ["web:1Cor.3.23-1Cor.3.23 per the Vulgate"], "cross-tradition material"),
    # L: ported=cs_dan_greek_addition | another critical edition
    ("cs_edition_na28", ["web:1Cor.3.23-1Cor.3.23 cf. NA28"], "cross-tradition material"),
    # L: created | the Septuagint (Swete is reference-only, OW-35), a majuscule number and symbol, a minuscule
    ("cs_lxx", ["web:1Cor.15.32-1Cor.15.32 the LXX wording"], "cross-tradition material"),
    ("cs_swete", ["rp:1Cor.15.54-1Cor.15.54 per Swete"], "cross-tradition material"),
    ("cs_ga_number", ["sbl:1Cor.14.34-1Cor.14.35 order of 06"], "cross-tradition material"),
    ("cs_aleph_symbol", ["sbl:1Cor.13.3-1Cor.13.3 ℵ reads otherwise"], "cross-tradition material"),
    ("cs_minuscule", ["rp:1Cor.13.3-1Cor.13.3 per minuscule 1739"], "cross-tradition material"),
    ("cs_own_witness_ok", ["rp:1Cor.13.3-1Cor.13.3 (Byzantine Textform; SBLGNT differs)"], None),
    # L: ported=cs_selah | fabrication class
    ("cs_selah", ["web:1Cor.1.1-1Cor.1.1 selah"], "NO selah exists"),
    # L: ported=cs_kq_in_zone_ok | the claim is RED (no 1Cor note layer); its denial passes
    ("cs_kq_dual_red", ["rp:1Cor.4.9-1Cor.4.9 = web:1Cor.4.9 ketiv/qere"], "claims ketiv/qere"),  # fab
    ("cs_kq_dual_denied_ok", ["rp:1Cor.4.9-1Cor.4.9 = web:1Cor.4.9 (no ketiv/qere)"], None),  # fab
    # L: created | a petuchah claim and its denial; a Hebrew run in a ref
    ("cs_petuchah_red", ["rp:1Cor.7.1-1Cor.7.1 petuchah before the verse"], "claims petuchah"),
    ("cs_petuchah_denied_ok", ["rp:1Cor.7.1-1Cor.7.1 (no petuchah precedes the verse)"], None),
    ("cs_hebrew_in_ref_red", ["rp:1Cor.14.21-1Cor.14.21 " + HEB3], "Hebrew run in ref entry"),
]
# L: created | the identity dual loop over every chapter's last verse (the source looped over its zones)
for c in GREEK_LAST_VERSE:
    last = GREEK_LAST_VERSE[c]
    CS_VECTORS.append(("cs_dual_last_%d_ok" % c, ["web:1Cor.%d.%d = rp:1Cor.%d.%d" % (c, last, c, last)], None))
    CS_VECTORS.append(("cs_dual_last_%d_bad" % c, ["web:1Cor.%d.%d = sbl:1Cor.%d.%d" % (c, last, c, last - 1)],
                       "dual-cite arithmetic wrong"))

ENV = dict(os.environ, PYTHONIOENCODING="utf-8")   # tools print Greek; the Windows console codec cannot
TD = tempfile.TemporaryDirectory()


def run(tool, rows_path):
    out = subprocess.run([sys.executable, str(HERE / tool), str(rows_path)],
                         capture_output=True, text=True, encoding="utf-8", env=ENV)
    return json.loads(out.stdout)


def sweep(rows, tag):
    """Run citation_sweep on rows written to the temporary directory (never on the frozen rows)."""
    p = Path(TD.name) / ("%s.jsonl" % tag)
    p.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows), encoding="utf-8")
    return run("citation_sweep.py", p)


def expect_rows(rep, vectors, key="problems"):
    for did, _, expect in vectors:
        mine = [p for p in rep[key] if p.startswith(did + ":")]
        check("citation_sweep %s: %s" % (did, "no problem" if expect is None else repr(expect)),
              (not mine) if expect is None else any(expect in p for p in mine), mine)


rep = sweep([{"decision_id": d, "boundary_evidence_refs": r} for d, r, _ in CS_VECTORS], "cs_vectors")
expect_rows(rep, CS_VECTORS)
# L: created | prose-only cross-tradition names are metadata and pass
rep = sweep([{"decision_id": "cs_cross_prose_only_ok", "boundary_rationale": "P46 and the Vulgate agree; the LXX of "
              "Isaiah lies behind the quotation (Swete, reference-only)", "boundary_evidence_refs": ["rp:1Cor.15.54"]}],
            "cs_cross_prose")
expect_rows(rep, [("cs_cross_prose_only_ok", None, None)])
# L: created | each regex on a positive and a negative
for name, rx, pos, neg in (
        ("CROSS", cs.CROSS, "per Codex Vaticanus", "per the Robinson-Pierpont Byzantine Textform"),
        ("CROSS number", cs.CROSS, "order of 06", "rp:1Cor.1.10"),
        ("TOPIC_MARKER", cs.TOPIC_MARKER, "a topic marker", "a non-topic-marker turn"),
        ("TOPIC_MARKER Greek", cs.TOPIC_MARKER, SBL[(7, 1)][:8], SBL[(8, 4)][:5]),
        ("GREEK_QUOTE", cs.GREEK_QUOTE, RP_Q, "Paul writes"),
        ("GREEK_REF", cs.GREEK_REF, "rp:1Cor.10.23", "web:1Cor.10.23"),
        ("SIGLA_RE", cs.SIGLA_RE, SIG_Q, NOSIG_Q),
        ("HEB_RUN", cs.HEB_RUN, HEB3, RP_Q),
        ("MARK_WORD", cs.MARK_WORD, "a petuchah", "a paragraph"),
        ("KQ_WORD", cs.KQ_WORD, "a ketiv", "a variant"),  # fab
        ("PASEQ_WORD", cs.PASEQ_WORD, "a paseq", "a pause"),  # fab
        ("SELAH", cs.SELAH, "selah", "Sela's"),
        ("REVERSED_NUN", cs.REVERSED_NUN, "a reversed nun", "a reversed order"),
        ("LARGE_LETTER", cs.LARGE_LETTER, "a large letter", "a large majuscule"),
        ("SMALL_LETTER", cs.SMALL_LETTER, "a small nun", "a small minuscule"),
        ("PUNCTA", cs.PUNCTA, "puncta extraordinaria", "punctuation"),
        ("SINGLE_WITNESS", cs.SINGLE_WITNESS, "single witness", "two witnesses")):
    check("regex %s: positive %r matches, negative %r does not" % (name, pos[:20], neg[:20]),
          bool(rx.search(pos)) and not rx.search(neg))

# 3. QUOTE TIER (the source's note-layer tier, re-pointed to the Greek quote binding). Prose fields.
HEB_VECTORS = [
    # L: ported=cs_verse_quote_ok | a Greek quote at byte tier at its rp: ref
    ("cs_verse_quote_ok", "“%s” (rp:1Cor.10.23) opens the unit" % RP_Q, None),
    # L: ported=cs_dan_mixed_2_4_words_at_wrong_verse | the same quote at a wrong verse
    ("cs_words_at_wrong_verse", "“%s” (rp:1Cor.10.24) opens the unit" % RP_Q, "does not collate against any nearby cited ref"),
    # L: created | 10:23: RP has 'moi', SBLGNT does not; each quote bound to each witness
    ("cs_1023_rp_quote_at_sbl_red", "“%s” (sbl:1Cor.10.23)" % RP_Q, "does not collate against any nearby cited ref"),
    ("cs_1023_sbl_quote_at_sbl_ok", "“%s” (sbl:1Cor.10.23)" % SBL_Q, None),
    ("cs_1023_sbl_quote_at_rp_red", "“%s” (rp:1Cor.10.23)" % SBL_Q, "does not collate against any nearby cited ref"),
    # L: ported=cs_qere_disclosed_ok | re-pointed: an SBLGNT quote that carries its critical signs
    ("cs_sbl_with_sigla_ok", "“%s” (sbl:1Cor.10.23)" % SIG_Q, None),
    # L: ported=cs_qere_undisclosed | re-pointed: the same quote without its signs passes and is listed
    ("cs_sbl_without_sigla_listed", "“%s” (sbl:1Cor.10.23)" % NOSIG_Q, None),
    # L: created | a quote with SBLGNT signs bound to rp: is RED
    ("cs_sigla_at_rp_red", "“%s” (rp:1Cor.10.23)" % SIG_Q, "does not collate against any nearby cited ref"),
    # L: created | the overclaim tiers are RED; a web: ref never binds
    ("cs_accent_stripped_red", "“%s” (rp:1Cor.10.23)" % ACC_Q, "tier accent_stripped"),
    ("cs_skeleton_red", "“%s” (rp:1Cor.10.23)" % SKEL_Q, "tier skeleton"),
    ("cs_greek_with_web_ref_only_red", "“%s” (web:1Cor.10.23)" % RP_Q, "has NO rp:/sbl: ref in its field"),
    # L: ported=cs_dan_aramaic_qere_disclosed_ok | disabled: 1Cor has no Aramaic and no Qere; the 10:23 vectors above
    #    take its place
    # L: ported=cs_dan_aramaic_qere_undisclosed | disabled for the same reason
    # L: ported=cs_dan_mixed_2_4_hebrew_words_ok | re-pointed: two quotes in one field, each at its own ref
    ("cs_two_quotes_own_refs_ok", "“%s” (rp:1Cor.10.23); then “%s” (rp:1Cor.10.24)" % (RP_Q, RP24), None),
    # L: ported=cs_dan_mixed_2_4_aramaic_words_ok | re-pointed to the sbl: witness
    ("cs_sbl_quote_ok", "“%s” (sbl:1Cor.10.23) closes it" % SBL_Q, None),
]
rep = sweep([{"decision_id": d, "boundary_rationale": t} for d, t, _ in HEB_VECTORS], "quote_tier")
expect_rows(rep, HEB_VECTORS)
check("cs_sbl_without_sigla_listed: in sbl_sigla_stripped",
      any(x.startswith("cs_sbl_without_sigla_listed:") for x in rep["sbl_sigla_stripped"]), rep["sbl_sigla_stripped"])
check("cs_sbl_with_sigla_ok: not in sbl_sigla_stripped",
      not any(x.startswith("cs_sbl_with_sigla_ok:") for x in rep["sbl_sigla_stripped"]))

# 4. REGRESSION (puncta and the note layer)
PUNCTA2_CS = [
    # L: ported=cs_puncta_negated_ok
    ("cs_puncta_negated_ok", ["web:1Cor.1.5-1Cor.1.5 (no puncta here)"], None),
    # L: ported=cs_puncta_denied_true_ok | rp:1Cor.8.10
    ("cs_puncta_denied_true_ok", ["rp:1Cor.8.10-1Cor.8.10 (no puncta)"], None),
    # L: ported=cs_puncta_range_red | 8:1-13, 8:10
    ("cs_puncta_range_red", ["web:1Cor.8.1-1Cor.8.13 (puncta at 8:10, single-witness)"], "claims puncta extraordinaria"),
    # L: ported=cs_kq_editorial_note_ok | negative: 1Cor has no editorial note layer, so the claim is RED
    ("cs_kq_editorial_note_red", ["rp:1Cor.2.9-1Cor.2.9 (editorial note, single-witness: a ketiv/qere read)"], "claims ketiv/qere"),  # fab
    # L: ported=cs_kq_none_bad
    ("cs_kq_none_bad", ["rp:1Cor.1.2-1Cor.1.2 (ketiv/qere, single-witness)"], "claims ketiv/qere"),  # fab
]
# 5. T1 REVIEW REGRESSIONS
T1_CS = [
    # L: ported=cs_t1_01_wrong_number_in_covering_range
    ("cs_t1_01_wrong_number_in_covering_range", ["web:1Cor.8.1-1Cor.8.13 (puncta at 8:5, single-witness)"],
     "claims puncta extraordinaria"),
    # L: ported=cs_t1_03_double_negation_asserts_presence_red
    ("cs_t1_03_double_negation_asserts_presence_red", ["rp:1Cor.8.10-1Cor.8.10 (not without puncta, single-witness)"],
     "claims puncta extraordinaria"),
    # L: ported=cs_negation_naming_a_verse_ok
    ("cs_negation_naming_a_verse_ok", ["web:1Cor.8.1-1Cor.8.13 (no puncta at 8:10)"], None),
]
# 6. T2 REVIEW REGRESSIONS
T2_CS = [
    # L: ported=cs_t2_01_decoy_site_number
    ("cs_t2_01_decoy_site_number", ["web:1Cor.8.1-1Cor.8.13 (cf. 8:10; but the true puncta claim here is verse 8:5, single-witness)"],
     "claims puncta extraordinaria"),
    # L: ported=cs_t2_02_claim_near_other_number_red
    ("cs_t2_02_claim_near_other_number_red", ["web:1Cor.8.1-1Cor.8.13 (8:9 nearby; puncta extraordinaria stand at 8:10, single-witness)"],
     "claims puncta extraordinaria"),
    # L: ported=cs_t2_02_range_red
    ("cs_t2_02_range_red", ["web:1Cor.8.1-1Cor.8.13 (puncta extraordinaria across 8:8-8:10, single-witness)"],
     "claims puncta extraordinaria"),
    # L: ported=cs_t2_03_distant_negation_true_ok
    ("cs_t2_03_distant_negation_true_ok",
     ["web:1Cor.8.1-1Cor.8.13 (the text absolutely does not under any reading carry puncta extraordinaria at 8:10, single-witness)"], None),
    # L: ported=cs_t2_05_mt_phrase_puncta_red | the phrase re-pointed to 'RP 8.12'
    ("cs_t2_05_rp_phrase_puncta_red", ["web:1Cor.5.2-1Cor.5.2 (RP 8.12 puncta extraordinaria, single-witness)"], "claims puncta extraordinaria"),
    # L: ported=cs_dan_t2_05_mt_phrase_is_not_a_qualifier_ok
    ("cs_t2_05_rp_phrase_is_not_a_qualifier_ok", ["web:1Cor.5.2-1Cor.5.2 (RP 8.12 is cited for comparison only)"], None),
    # L: ported=cs_mixed_two_numbers_red
    ("cs_mixed_two_numbers_red", ["web:1Cor.8.1-1Cor.8.13 (puncta extraordinaria at 8:10 and 8:11, single-witness)"], "claims puncta extraordinaria"),
]
# 8. R4 (ii)
R4II_CS = [
    # L: ported=cs_r4ii_novel_a_paren_nonsite
    ("cs_r4ii_novel_a_paren_nonsite", ["web:1Cor.8.1-1Cor.8.13 puncta extraordinaria (8:5)"], "claims puncta extraordinaria"),
    # L: ported=cs_r4ii_novel_a2_distant_nonsite
    ("cs_r4ii_novel_a2_distant_nonsite",
     ["web:1Cor.8.1-1Cor.8.13 puncta extraordinaria are recorded in this measured span by the single witness, standing at verse 8:5"],
     "claims puncta extraordinaria"),
    # L: ported=cs_r4ii_paren_number_red
    ("cs_r4ii_paren_number_red", ["web:1Cor.8.1-1Cor.8.13 puncta extraordinaria (8:10, single-witness)"], "names a verse that carries none"),
    # L: ported=cs_r4ii_distant_number_red
    ("cs_r4ii_distant_number_red",
     ["web:1Cor.8.1-1Cor.8.13 puncta extraordinaria are recorded in this measured span by the single witness, standing at verse 8:10"],
     "names a verse that carries none"),
]
# 9. T4 FINDINGS
T4_CS = [
    # L: ported=cs_t4_01_decoy_letter_id_red
    ("cs_t4_01_decoy_letter_id_red",
     ["web:1Cor.8.1-1Cor.8.13 puncta extraordinaria (cross-referenced at row R4.5 in the ledger), single-witness"], "the ref covers no site"),
    # L: ported=cs_t4_01_dotted_dan_ref_still_binds
    ("cs_t4_01_dotted_ref_still_binds", ["web:1Cor.8.1-1Cor.8.13 puncta extraordinaria (1Cor.8.5, single-witness)"],
     "names a verse that carries none"),
    # L: ported=cs_t4_03_puncta_denial_after_nonsite_ok
    ("cs_t4_03_puncta_denial_after_nonsite_ok",
     ["web:1Cor.8.1-1Cor.8.10 puncta extraordinaria would be expected at 8:5 but none stands"], None),
    # L: ported=cs_t4_03_puncta_denial_after_true_ok
    ("cs_t4_03_puncta_denial_after_true_ok",
     ["rp:1Cor.8.10-1Cor.8.10 puncta extraordinaria would be expected here but none stands"], None),
    # L: ported=cs_t4_04_number_without_disclosure_red
    ("cs_t4_04_number_without_disclosure_red", ["web:1Cor.8.1-1Cor.8.13 puncta extraordinaria (8:10)"], "claims puncta extraordinaria"),
    # L: ported=cs_t4_04_spaced_single_witness_red
    ("cs_t4_04_spaced_single_witness_red", ["web:1Cor.8.1-1Cor.8.13 puncta extraordinaria at 8:10, single witness"], "claims puncta extraordinaria"),
]
# 9b. E4
E4_CS = [
    # L: ported=cs_e4_a2_positive_then_denial_nonsite_red
    ("cs_e4_a2_positive_then_denial_nonsite_red",
     ["web:1Cor.8.1-1Cor.8.13 puncta extraordinaria stand at 8:5 but none is present in ch 9, single-witness"], "claims puncta extraordinaria"),
    # L: ported=cs_e4_a2_positive_then_denial_red
    ("cs_e4_a2_positive_then_denial_red",
     ["web:1Cor.8.1-1Cor.8.13 puncta extraordinaria stand at 8:10 but none is present at 8:11, single-witness"], "names a verse that carries none"),
    # L: ported=cs_e4_a3_mark_spaced_single_witness_ok | negative: no 1Cor witness carries a paragraph mark
    ("cs_e4_a3_mark_spaced_single_witness_red", ["rp:1Cor.3.12-1Cor.3.12 samekh (single witness)"], "claims samekh"),  # fab
    # L: ported=cs_e4_a3_paseq_spaced_single_witness_ok | negative: no 1Cor witness carries a paseq
    ("cs_e4_a3_paseq_spaced_single_witness_red", ["rp:1Cor.3.2-1Cor.3.2 paseq (count-only, single witness)"], "claims paseq"),  # fab
]
REF_SETS = PUNCTA2_CS + T1_CS + T2_CS + R4II_CS + T4_CS + E4_CS
rep = sweep([{"decision_id": d, "boundary_evidence_refs": r} for d, r, _ in REF_SETS], "ref_sets")
expect_rows(rep, REF_SETS)

# 5/6 (the note-layer binding regressions, re-pointed to the Greek binding). Prose fields.
T1_HEB = [
    # L: ported=cs_t1_04_second_qere_rides_on_distant_disclosure | re-pointed: the second quote binds to its own ref
    ("cs_t1_04_second_quote_binds_own_ref", "“%s” (rp:1Cor.10.23). Later, “%s” (rp:1Cor.10.24)." % (RP_Q, RP_Q),
     "does not collate against any nearby cited ref"),
    # L: ported=cs_qere_cited_at_wrong_verse_refused | 1Cor binds to the ONE nearest ref, so a right ref further off
    #    in another sentence does not rescue it
    ("cs_quote_cited_at_wrong_verse_refused",
     "The unit turns at rp:1Cor.10.23. Its next verse reads “%s” (rp:1Cor.10.25)." % RP24, "bound to rp:1Cor.10.25"),
]
T2_HEB = [
    # L: ported=cs_t2_04_short_gap_second_qere | two quotes a short gap apart, each at its own ref
    ("cs_t2_04_short_gap_second_quote", "“%s” (rp:1Cor.10.23), “%s” (rp:1Cor.10.24)" % (RP_Q, RP24), None),
    # L: ported=cs_d3_raw_noncanonical_qere_ok | an NFD copy is copy degradation, not a problem
    ("cs_d3_nfd_quote_degraded", "“%s” (rp:1Cor.10.23)" % NFD_Q, None),
]
rep = sweep([{"decision_id": d, "boundary_rationale": t} for d, t, _ in T1_HEB + T2_HEB], "heb_regressions")
expect_rows(rep, T1_HEB + T2_HEB)
check("cs_d3_nfd_quote_degraded: in nfd_degraded",
      any(x.startswith("cs_d3_nfd_quote_degraded:") for x in rep["nfd_degraded"]), rep["nfd_degraded"])

# 7. DEVICES (the source's calendar section, re-pointed). Every constant against the pinned inventory, with counts.
INV = json.loads((BOOK / "1cor_device_inventory.json").read_text(encoding="utf-8"))
CSC = INV["citation_sweep_constants"]


def _pairs(key):
    return frozenset(tuple(p) for p in CSC[key])


PAIR_KEYS = sorted(k for k in CSC if k.endswith("_PAIRS"))
check("inventory: 19 *_PAIRS keys", len(PAIR_KEYS) == 19, PAIR_KEYS)
for k in PAIR_KEYS:
    fam = k[:-len("_PAIRS")]
    got = (cs.FRAME_IN_BODY_PAIRS if k == "FRAME_IN_BODY_PAIRS" else cs.DEVICE_SBL_ONLY_PAIRS.get(fam[:-len("_SBL_ONLY")])
           if fam.endswith("_SBL_ONLY") else cs.DEVICE_PAIRS.get(fam))
    check("device constant %s == inventory (%d)" % (k, len(_pairs(k))), got == _pairs(k), sorted(got or []))
COUNTS = {"TOPIC_MARKER_PAIRS": 6, "BARE_PERI_SENTENCE_START_PAIRS": 1, "DISCLOSURE_PAIRS": 5, "APPEAL_PAIRS": 3,
          "TRADITION_PAIRS": 4, "PRAISE_PAIRS": 3, "SLOGAN_PAIRS": 2, "FRAME_PAIRS": 7, "THANKSGIVING_PAIRS": 3,
          "FRAME_IN_BODY_PAIRS": 1}
check("device counts at the port", all(len(_pairs(k)) == n for k, n in COUNTS.items())
      and all(not CSC[k] for k in PAIR_KEYS if k.endswith("_SBL_ONLY_PAIRS")),
      {k: len(_pairs(k)) for k in PAIR_KEYS})
check("TOPIC_MARKER_PAIRS: 7:1, 7:25, 8:1, 12:1, 16:1, 16:12",
      cs.TOPIC_MARKER_PAIRS == {(7, 1), (7, 25), (8, 1), (12, 1), (16, 1), (16, 12)})
check("DEVICE_NO_ONSET is EMPTY (count 0) and equals the inventory", cs.DEVICE_NO_ONSET == _pairs("DEVICE_NO_ONSET") == set())
check("FRAME_edges: opening_before 1:10, closing_from 16:19; FRAME_IN_BODY 10:32 lies between them",
      cs.FRAME_EDGES == {k: tuple(v) for k, v in CSC["FRAME_edges"].items()} == {"opening_before": (1, 10), "closing_from": (16, 19)}
      and cs.FRAME_IN_BODY_PAIRS == {(10, 32)})
check("only TOPIC_MARKER carries a claim arm", cs.DEVICE_CLAIM_FAMILIES == ("TOPIC_MARKER",))
SBL81 = SBL[(8, 1)].split(" ")
PERI_DE = " ".join(SBL81[:2])
CAL_ROWS = [
    # L: ported=cal_onset_10_4_ok | a unit opening at a topic marker: the onset arm never fires (DEVICE_NO_ONSET empty)
    ("cal_onset_7_1_ok", {"span": "1Cor.7.1-1Cor.7.24", "boundary_rationale": "the onset is the topic marker at 7:1"}, None),
    # L: ported=cal_onset_10_5_ok
    ("cal_onset_7_2_ok", {"span": "1Cor.7.2-1Cor.7.24"}, None),
    # L: ported=cal_onset_10_4_no_formula_ok
    ("cal_onset_7_1_no_formula_ok", {"span": "1Cor.7.1-1Cor.7.9"}, None),
    # L: ported=cal_onset_web_10_4_ok
    ("cal_onset_web_7_1_ok", {"span": "web:1Cor.7.1-1Cor.7.24"}, None),
    # L: ported=cal_onset_10_4_single_ok
    ("cal_onset_7_1_single_ok", {"span": "1Cor.7.1-1Cor.7.1"}, None),
    # L: ported=cal_dan_calendar_date_onset_ok | re-pointed: a unit opening at the bare peri sentence start 8:4
    ("cal_bare_peri_onset_ok", {"span": "1Cor.8.4-1Cor.8.13", "boundary_rationale": "the unit opens at 8:4, not a topic marker"}, None),
    # L: ported=cal_prose_claim_10_4_bad
    ("cal_prose_claim_7_2_bad", {"boundary_rationale": "the topic marker at 7:2 opens the unit"}, "claims a topic marker at 7:2"),
    # L: ported=cal_prose_number_first_bad
    ("cal_prose_number_first_bad", {"boundary_rationale": "1Cor.7.2 is a topic marker"}, "claims a topic marker at 7:2"),
    # L: ported=cal_prose_list_bad | 8:4 is BARE_PERI_SENTENCE_START, not TOPIC_MARKER
    ("cal_prose_list_bad", {"boundary_rationale": "topic markers at 7:1, 7:25 and 8:4"}, "claims a topic marker at 8:4"),
    # L: ported=cal_prose_double_negation_bad
    ("cal_prose_double_negation_bad", {"boundary_rationale": "7:2 is not without a topic marker"}, "claims a topic marker at 7:2"),
    # L: ported=cal_prose_negated_ok
    ("cal_prose_negated_ok", {"boundary_rationale": "7:2 is not a topic marker, having no peri de"}, None),
    # L: ported=cal_prose_non_dateline_ok
    ("cal_prose_non_topic_marker_ok", {"boundary_rationale": "the non-topic-marker transition at 7.2"}, None),
    # L: ported=cal_prose_real_dateline_ok
    ("cal_prose_real_topic_marker_ok", {"boundary_rationale": "the topic marker at 16:12 opens the unit"}, None),
    # L: ported=cal_prose_other_clause_ok
    ("cal_prose_other_clause_ok", {"boundary_rationale": "unlike the topic marker at 7:1, the turn at 7:2 carries no peri de"}, None),
    # L: ported=cal_prose_unnumbered_ok
    ("cal_prose_unnumbered_ok", {"boundary_rationale": "the turn fails the letter's structural topic-marker test"}, None),
    # L: ported=cal_ref_bare_claim_bad
    ("cal_ref_bare_claim_bad", {"boundary_evidence_refs": ["rp:1Cor.7.2-1Cor.7.2 (topic marker; single-witness)"]}, "claims a topic marker at 7:2"),
    # L: ported=cal_ref_numbered_claim_bad
    ("cal_ref_numbered_claim_bad", {"boundary_evidence_refs": ["web:1Cor.7.1-1Cor.7.9 (topic marker at 7:2)"]}, "claims a topic marker at 7:2"),
    # L: ported=cal_ref_denial_ok
    ("cal_ref_denial_ok", {"boundary_evidence_refs": ["rp:1Cor.7.2-1Cor.7.2 (disclosure: not a topic marker (no peri de), single-witness)"]}, None),
    # L: ported=cal_ref_real_dateline_ok
    ("cal_ref_real_topic_marker_ok", {"boundary_evidence_refs": ["sbl:1Cor.12.1-1Cor.12.1 (topic marker; single-witness)"]}, None),
    # L: ported=cal_dan_ref_covers_dateline_and_date_ok
    ("cal_ref_covers_marker_and_other_ok", {"boundary_evidence_refs": ["web:1Cor.7.1-1Cor.7.2 (topic marker; single-witness)"]}, None),
    # L: ported=cal_dan_ref_web_face_bad
    ("cal_ref_web_face_bad", {"boundary_evidence_refs": ["web:1Cor.7.2-1Cor.7.2 (topic marker; single-witness)"]}, "claims a topic marker at 7:2"),
    # L: created | a topic-marker claim inside and outside TOPIC_MARKER_PAIRS, with the Greek formula sliced from SBLGNT 8:1
    ("cal_greek_formula_inside_ok", {"boundary_rationale": "“%s” (sbl:1Cor.8.1) is the topic marker at 8:1" % PERI_DE}, None),
    ("cal_greek_formula_outside_bad", {"boundary_rationale": "the formula %s is a topic marker at 8:4" % PERI_DE}, "claims a topic marker at 8:4"),
    ("cal_peri_de_inside_ok", {"boundary_rationale": "peri de at 16:1 opens the collection"}, None),
    ("cal_peri_de_outside_bad", {"boundary_rationale": "peri de at 15:1 opens the gospel unit"}, "claims a topic marker at 15:1"),
]
# 8. CAL-1 (the apposition and parenthesis readings)
CAL1_ROWS = [
    # L: ported=cal1_apposition_bad
    ("cal1_apposition_bad", {"boundary_rationale": "the onset stands at 7:2, a topic-marker onset"}, "claims a topic marker at 7:2"),
    # L: ported=cal1_parenthesis_bad
    ("cal1_parenthesis_bad", {"boundary_rationale": "the topic marker (7:2) opens the unit"}, "claims a topic marker at 7:2"),
    # L: ported=cal1_apposition_negated_ok
    ("cal1_apposition_negated_ok", {"boundary_rationale": "the onset stands at 7:2, not a topic marker"}, None),
    # L: ported=cal1_own_clause_number_ok
    ("cal1_own_clause_number_ok", {"boundary_rationale": "the unit opens at 7:2, the topic marker at 7:1 is close behind"}, None),
    # L: ported=cal1_other_clause_kept_ok
    ("cal1_other_clause_kept_ok", {"boundary_rationale": "unlike the topic marker at 7:1, the turn at 7:2 carries no formula"}, None),
]
# 9. T4 (the closed-set denials)
T4_CAL_ROWS = [
    # L: ported=cal_t4_03_apposition_denial_ok
    ("cal_t4_03_apposition_denial_ok", {"boundary_rationale": "the unit opens at 7:2, where a topic marker would be expected but none stands"}, None),
    # L: ported=cal_t4_03_parenthesis_denial_ok
    ("cal_t4_03_parenthesis_denial_ok", {"boundary_rationale": "the topic marker (7:2) would be expected but none stands"}, None),
    # L: ported=cal_t4_03_absent_at_clause_end_ok
    ("cal_t4_03_absent_at_clause_end_ok", {"boundary_rationale": "a topic marker at 7:2 is absent"}, None),
    # L: ported=cal_t4_03_bare_later_no_stays_red
    ("cal_t4_03_bare_later_no_stays_red", {"boundary_rationale": "the topic marker at 7:2 opens no new topic"}, "claims a topic marker at 7:2"),
    # L: ported=cal_t4_03_none_of_stays_red
    ("cal_t4_03_none_of_stays_red", {"boundary_rationale": "the topic marker at 7:2 but none of the other turns"}, "claims a topic marker at 7:2"),
    # L: ported=cal_t4_03_missing_not_final_stays_red
    ("cal_t4_03_missing_not_final_stays_red", {"boundary_rationale": "the topic marker at 7:2 is missing its particle"},
     "claims a topic marker at 7:2"),
    # L: ported=cal_t4_03_denial_behind_comma_residual_red
    ("cal_t4_03_denial_behind_comma_residual_red", {"boundary_rationale": "a topic marker at 7:2 would be expected, though none stands"},
     "claims a topic marker at 7:2"),
]
# 9b. E4
E4_CAL = [
    # L: ported=cal_e4_a2_positive_then_denial_red
    ("cal_e4_a2_positive_then_denial_red", {"boundary_rationale": "a topic marker stands at 7:2 but none stands at 7:3"},
     "claims a topic marker at 7:2"),
    # L: ported=cal_e4_a2_true_then_denial_ok
    ("cal_e4_a2_true_then_denial_ok", {"boundary_rationale": "the topic marker at 7:1 opens the unit but none stands at 7:2"}, None),
]
DEV_ROWS = CAL_ROWS + CAL1_ROWS + T4_CAL_ROWS + E4_CAL
# L: created | the onset arm never fires: one row opening at every verse of the book
ONSETS = [("dev_onset_%d_%d" % (c, v), {"span": "1Cor.%d.%d-1Cor.%d.%d" % (c, v, c, v)}, None)
          for c in LAST_VERSE for v in range(1, LAST_VERSE[c] + 1)]
rep = sweep([dict({"decision_id": d}, **f) for d, f, _ in DEV_ROWS + ONSETS], "devices")
expect_rows(rep, DEV_ROWS)
check("device onset arm silent at all 437 onsets", not [p for p in rep["problems"] if p.startswith("dev_onset_")],
      [p for p in rep["problems"] if p.startswith("dev_onset_")][:3])

# 10b. TOOLFIX (ref-entry binding, word bounds, register, WEB quotes)
RP_Q24 = RP24
S10B_CS_REFS = [
    # L: ported=cs_tf2b_s1_06_accent_stripped_qere_in_ref | an accent-stripped quote in a ref entry is RED
    ("cs_tf2b_s1_06_accent_stripped_in_ref", ["rp:1Cor.10.23-1Cor.10.23 %s" % ACC_Q], "does not collate against its own ref"),
    # L: ported=cs_tf2b_s1_06_raw_qere_in_ref_ok | a byte quote in its own ref entry
    ("cs_tf2b_s1_06_byte_quote_in_ref_ok", ["rp:1Cor.10.23-1Cor.10.23 %s" % RP_Q], None),
    # L: ported=cs_tf2b_s1_06_undisclosed_qere_in_ref | a sign-free SBLGNT quote in its sbl: entry passes and is listed
    ("cs_tf2b_s1_06_sign_free_in_ref", ["sbl:1Cor.10.23-1Cor.10.23 %s" % NOSIG_Q], None),
    # L: ported=cs_tf2b_s1_06_own_verse_words_ok | words of a verse inside the entry's range
    ("cs_tf2b_s1_06_own_verse_words_ok", ["rp:1Cor.10.22-1Cor.10.24 %s" % RP_Q24], None),
    # L: ported=cs_tf2b_s1_06_other_verse_words
    ("cs_tf2b_s1_06_other_verse_words", ["rp:1Cor.10.23-1Cor.10.23 %s" % RP_Q24], "does not collate against its own ref"),
    # L: ported=cs_tf2b_s1_06_named_other_ref_does_not_rebind
    ("cs_tf2b_s1_06_named_other_ref_does_not_rebind", ["rp:1Cor.10.23-1Cor.10.23 (cf. rp:1Cor.10.24) %s" % RP_Q24],
     "does not collate against its own ref"),
    # L: created | Greek in a web: entry never binds
    ("cs_greek_in_web_entry_red", ["web:1Cor.10.23-1Cor.10.23 %s" % RP_Q], "a web: ref never binds"),
]
S10B_CS_PROSE = [
    # L: ported=cs_tf2b_s1_07_cut_at_word_end
    ("cs_tf2b_s1_07_cut_at_word_end", "the turn “%s” (rp:1Cor.10.23)" % CUT_END, "does not collate"),
    # L: ported=cs_tf2b_s1_07_cut_at_word_start
    ("cs_tf2b_s1_07_cut_at_word_start", "the turn “%s” (rp:1Cor.10.23)" % CUT_START, "does not collate"),
    # L: ported=cs_tf2b_s1_07_root_inside_word
    ("cs_tf2b_s1_07_root_inside_word", "the turn “%s” (rp:1Cor.10.23)" % ROOT_IN, "does not collate"),
    # L: ported=cs_tf2b_s1_07_whole_word_ok
    ("cs_tf2b_s1_07_whole_word_ok", "the turn “%s” (rp:1Cor.10.23)" % RP_Q, None),
]
rep = sweep([{"decision_id": d, "boundary_evidence_refs": r} for d, r, _ in S10B_CS_REFS]
            + [{"decision_id": d, "boundary_rationale": t} for d, t, _ in S10B_CS_PROSE], "tf2b_cs")
expect_rows(rep, S10B_CS_REFS + S10B_CS_PROSE)
check("cs_tf2b_s1_06_sign_free_in_ref: in sbl_sigla_stripped",
      any(x.startswith("cs_tf2b_s1_06_sign_free_in_ref:") for x in rep["sbl_sigla_stripped"]), rep["sbl_sigla_stripped"])
# L: ported=S10B_REG | every register vector verbatim: the register words are book-neutral prose
S10B_REG = [
    ("reg_tf2b_originally_drafted", {"strongest_rejected_alternative": "the span as originally drafted ran to 7:27"}, "author_wave_register_s1_05"),
    ("reg_tf2b_former_span", {"device_notes": "the former span held one refrain"}, "author_wave_register_s1_05"),
    ("reg_tf2b_prior_reading", {"device_notes": "keeping the prior paragraph reading"}, "author_wave_register_s1_05"),
    ("reg_tf2b_correction_earlier", {"device_notes": "a correction to an earlier grouping"}, "author_wave_register_s1_05"),
    ("reg_tf2b_next_row", {"boundary_rationale": "the onset of the next row's unit"}, "author_wave_register_s1_05"),
    ("reg_tf2b_row_after", {"boundary_rationale": "the row after this unit closes on the refrain"}, "author_wave_register_s1_05"),
    ("reg_tf2b_last_of_rows", {"device_notes": "the last of three rows"}, "author_wave_register_s1_05"),
    ("reg_tf2b_strategy_s", {"device_notes": "matches the strategy's own naming"}, "author_wave_register_s1_05"),
    ("reg_tf2b_order_s", {"device_notes": "rather than the order's own ceiling"}, "author_wave_register_s1_05"),
    ("reg_tf2b_posture", {"device_notes": "held under the flagged-region posture"}, "author_wave_register_s1_05"),
    ("reg_tf2b_officially_inventoried", {"device_notes": "a messenger formula, officially inventoried"}, "author_wave_register_s1_05"),
    ("reg_tf2b_ends_the_part", {"device_notes": "the utterance formula ends the part"}, "author_wave_register_s1_05"),
    ("reg_tf2b_the_part_s", {"device_notes": "the part's close"}, "author_wave_register_s1_05"),
    ("reg_tf2b_green_part_of_the_court_ok", {"boundary_rationale": "the measuring covers part of the court"}, None),
    ("reg_tf2b_green_order_of_the_gates_ok", {"boundary_rationale": "the order of the gates follows the court"}, None),
]
# 10c. TOOLFIX (register, second wave)
S10C_REG = [
    # L: ported=reg_e5_prior_range_reading | 9:24-26 exists in 1Cor
    ("reg_e5_prior_range_reading", {"device_notes": "keeping the prior 9:24-26 reading"}, "author_wave_register_s1_05"),
    # L: ported=reg_e5_former_hyphenated_span
    ("reg_e5_former_hyphenated_span", {"device_notes": "its former nineteen-verse span"}, "author_wave_register_s1_05"),
    # L: ported=reg_e5_former_two_words_span | re-pointed to a 1Cor range (11.17-34)
    ("reg_e5_former_two_words_span", {"device_notes": "the former single 11.17-34 span"}, "author_wave_register_s1_05"),
    # L: ported=reg_e5_last_of_underscored_rows
    ("reg_e5_last_of_underscored_rows", {"device_notes": "the last of three land_allotment rows"}, "author_wave_register_s1_05"),
    # L: ported=reg_e5_previously_held_as | re-pointed: an 18-verse row
    ("reg_e5_previously_held_as", {"device_notes": "ground previously held as one 18-verse row"}, "author_wave_register_s1_05"),
    # L: ported=reg_e5_green_* (five GREEN controls, verbatim)
    ("reg_e5_green_former_kings_ok", {"device_notes": "the former kings"}, None),
    ("reg_e5_green_last_of_the_gates_ok", {"device_notes": "the last of the gates"}, None),
    ("reg_e5_green_rows_of_chambers_ok", {"device_notes": "one of three rows of chambers"}, None),
    ("reg_e5_green_previously_held_by_ok", {"device_notes": "the land previously held by Judah"}, None),
    ("reg_e5_green_prior_verse_ok", {"device_notes": "the prior verse"}, None),
]
# L: ported=section 10c S10C_CS_PROSE (cs_e5_nc_*) | disabled: those vectors test a proclitic-stripped Hebrew label
#    against a Hebrew text; 1Cor has no Hebrew text, and the word-bound Greek vectors of 10b cover the same seam
p = Path(TD.name) / "reg.jsonl"
p.write_text("\n".join(json.dumps(dict({"decision_id": d}, **f), ensure_ascii=False) for d, f, _ in S10B_REG + S10C_REG),
             encoding="utf-8")
rep = run("check_register.py", p)
for d, _, cls in S10B_REG + S10C_REG:
    mine = [fl for fl in rep["flags"] if fl.get("decision_id") == d]
    check("check_register %s: %s" % (d, cls or "no flag of any class"),
          (not mine) if cls is None else any(fl.get("class") == cls for fl in mine), mine)


# L: ported=same | WEB slices for the check_web_quotes vectors, cut from 1Cor_web_clean.txt at run time
def web_words(p, n=6):
    return " ".join(WEB[p].split()[:n]).rstrip(",.;:")


PLAIN_P = next(p for p in sorted(WEB) if not re.search("[‘’“”]|\\[fn\\]", WEB[p]))
APOS_P = next(p for p in sorted(WEB) if "’" in WEB[p] and not re.search("[“”]|\\[fn\\]", WEB[p]))
WQ_PLAIN = web_words(PLAIN_P)
_aw = WEB[APOS_P].split()
_ai = next(i for i, w in enumerate(_aw) if "’" in w)
WQ_APOS = "“%s”" % " ".join(_aw[max(0, _ai - 2):_ai + 3]).rstrip(",.;:")
p = Path(TD.name) / "wq.jsonl"
p.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in (
    {"decision_id": "wq_tf2b_s1_10_unequal", "boundary_rationale": "“%s (web:1Cor.%d.%d)." % ((WQ_PLAIN,) + PLAIN_P)},
    {"decision_id": "wq_tf2b_s1_10_balanced_ok", "boundary_rationale": "“%s” (web:1Cor.%d.%d)." % ((WQ_PLAIN,) + PLAIN_P)},
    {"decision_id": "wq_tf2b_s1_10_apostrophes_ok", "boundary_rationale": "%s (web:1Cor.%d.%d)." % ((WQ_APOS,) + APOS_P)})),
    encoding="utf-8")
rep = run("check_web_quotes.py", p)
for d, fires in (("wq_tf2b_s1_10_unequal", True), ("wq_tf2b_s1_10_balanced_ok", False), ("wq_tf2b_s1_10_apostrophes_ok", False)):
    mine = [fl for fl in rep["flags"] if "e15d" in str(fl.get("issue")) and fl.get("decision_id") == d]
    check("check_web_quotes %s: e15d %s" % (d, "fires" if fires else "silent"), bool(mine) == fires, rep["flags"])

# L: created | the WEB footnote quote WARN (the predecessor's note-layer WEB-quote warn, re-pointed)
FN = sorted(tuple(int(x) for x in k.split(".")[1:]) for k in load_pmarks()["web_footnote_verses"])
FN_P = next(p for p in FN if WEB[p].find("[fn]") > 40)
NOFN_P = PLAIN_P
fn_q = web_words(FN_P, 5)
FNROWS = [("fn_quote_undisclosed_warn", "“%s” (web:1Cor.%d.%d)" % ((fn_q,) + FN_P), True),
          ("fn_quote_disclosed_ok", "“%s” (web:1Cor.%d.%d; the WEB footnote is noted)" % ((fn_q,) + FN_P), False),
          ("fn_quote_plain_verse_ok", "“%s” (web:1Cor.%d.%d)" % ((WQ_PLAIN,) + NOFN_P), False)]
rep = sweep([{"decision_id": d, "boundary_rationale": t} for d, t, _ in FNROWS], "fn_quotes")
for d, _, fires in FNROWS:
    mine = [w for w in rep["web_footnote_quote_warns"] if w.startswith(d + ":")]
    check("web footnote warn %s: %s" % (d, "fires" if fires else "silent"), bool(mine) == fires and not
          [x for x in rep["problems"] if x.startswith(d + ":")], [mine, rep["problems"]])
check("web footnote fixture: %d:%d is a footnote verse and %d:%d is not" % (FN_P + NOFN_P), FN_P in FN and NOFN_P not in FN)

TD.cleanup()
failed = [r for r in results if not r["ok"]]
print(json.dumps({"checks": len(results), "failed": len(failed), "failures": failed[:40],
                  "deferred_to_marks_lane": DEFERRED_TO_MARKS_LANE}, ensure_ascii=False, indent=1))
sys.exit(1 if failed else 0)
