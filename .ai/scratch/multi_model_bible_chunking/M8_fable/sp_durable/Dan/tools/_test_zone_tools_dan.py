#!/usr/bin/env python3
"""Exhaustive and adversarial tests for the Dan-specific arms of citation_sweep.py and check_marks.py.

Ported by Dan/tools/_adapt_tools_dan.py from _test_zone_tools_ezek.py: every section keeps its number there, and every
vector carries an 'L:' comment that names its source vector id ('ported') or says 'created' (written for Dan).
1. PROPERTY (exhaustive): citation_sweep's zone predicates, which state Dan's four zones on their face, flag a verse if
   and only if the crosswalk moves it. Every WEB verse and every MT verse is tested against dan_lib, so the predicates
   cannot drift from the verified map.
2. VECTORS: one fixture row per behaviour, run through each tool as a subprocess exactly as the suite runs it. Each
   vector asserts the presence or the absence of its own finding, matched by decision_id. Dan has no puncta site, so a
   ported vector whose claim was TRUE at a source-book site is its negative here (the claim is RED), and a ported
   denial at a site is a true denial (GREEN). Every Hebrew and Aramaic form is derived from the verse or note bytes at
   run time, never typed; every WEB form is sliced from Dan_web_clean.txt at run time.
Writes only to a temporary directory. Exit 1 on any failure.
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from dan_lib import LAST_VERSE, MT_LAST_VERSE, mt_to_web, web_to_mt  # noqa: E402
import citation_sweep as cs  # noqa: E402

results = []


def check(name, ok, detail=None):
    entry = {"check": name, "ok": bool(ok)}
    if not ok and detail:
        entry["detail"] = detail
    results.append(entry)


bad_web = [(c, v) for c in LAST_VERSE for v in range(1, LAST_VERSE[c] + 1)
           if cs.web_pairs_in_offset_zone([(c, v)]) != (web_to_mt(c, v) != (c, v))]
bad_mt = [(c, v) for c in MT_LAST_VERSE for v in range(1, MT_LAST_VERSE[c] + 1)
          if cs.mt_pairs_in_offset_zone([(c, v)]) != (mt_to_web(c, v) != (c, v))]
check("web zone predicate == crosswalk non-identity, all %d WEB verses" % sum(LAST_VERSE.values()), not bad_web, bad_web[:5])
check("mt zone predicate == crosswalk non-identity, all %d MT verses" % sum(MT_LAST_VERSE.values()), not bad_mt, bad_mt[:5])
# L: created
ZW = [(c, v) for c in LAST_VERSE for v in range(1, LAST_VERSE[c] + 1) if cs.web_pairs_in_offset_zone([(c, v)])]
ZM = [(c, v) for c in MT_LAST_VERSE for v in range(1, MT_LAST_VERSE[c] + 1) if cs.mt_pairs_in_offset_zone([(c, v)])]
check("zones: the predicates hold 66 WEB and 66 MT verses, and each WEB zone verse maps into the MT zone",
      len(ZW) == 66 and len(ZM) == 66 and all(cs.mt_pairs_in_offset_zone([web_to_mt(*p)]) for p in ZW), [len(ZW), len(ZM)])

# (decision_id, boundary_evidence_refs, expected problem substring or None for "no problem at all")
def xx(kind, c, v, tail=""):
    """A single-verse X-X ref, built where a literal would name a verse the other face lacks (the adapter reads the
    bare end of an oshb: range on the WEB face) or a deliberately out-of-range verse."""
    return "%s:Dan.%d.%d-Dan.%d.%d%s" % (kind, c, v, c, v, tail)


ZDUAL = [((4, 2), (3, 32)), ((4, 10), (4, 7)), ((5, 31), (6, 1)), ((6, 10), (6, 11))]   # one (WEB, MT) pair per zone
ZWRONG = [(4, 2), (4, 10), (5, 30), (6, 10)]   # a wrong MT reading per zone (MT 5:31 does not exist, so zone 3 uses 5:30)
# L: created
check("fixture: each zone pair follows the crosswalk; each wrong reading does not, and exists on the MT face",
      all(web_to_mt(*w) == m and m != b and 1 <= b[1] <= MT_LAST_VERSE[b[0]] for (w, m), b in zip(ZDUAL, ZWRONG)))
CS_VECTORS = [
    # L: ported=cs_puncta_41_20_ok | negative: U+05C4 stands in no Dan verse, so the claim is RED
    ("cs_puncta_web_4_20_red", ["web:Dan.4.20-Dan.4.20 puncta extraordinaria (single-witness)"], "claims puncta extraordinaria"),
    # L: ported=cs_puncta_46_22_ok | negative, as above
    ("cs_puncta_oshb_8_22_red", ["oshb:Dan.8.22-Dan.8.22 puncta extraordinaria (single-witness)"], "claims puncta extraordinaria"),
    # L: ported=cs_puncta_40_20_bad
    ("cs_puncta_web_1_20_bad", ["web:Dan.1.20-Dan.1.20 puncta extraordinaria (single-witness)"], "claims puncta extraordinaria"),
    # L: ported=cs_zone_bare_web_21_3
    ("cs_zone_bare_web_4_5", ["web:Dan.4.5-Dan.4.5"], "offset-zone ref lacks"),
    # L: ported=cs_zone_bare_web_20_45 | the first verse of a WEB zone
    ("cs_zone_bare_web_4_1", ["web:Dan.4.1-Dan.4.1"], "offset-zone ref lacks"),
    # L: ported=cs_zone_bare_mt_21_8
    ("cs_zone_bare_mt_4_2", ["oshb:Dan.4.2-Dan.4.2"], "offset-zone ref lacks"),
    # L: created | every other zone, bare, on both faces
    ("cs_dan_zone_bare_web_5_31", ["web:Dan.5.31-Dan.5.31"], "offset-zone ref lacks"),
    ("cs_dan_zone_bare_web_6_28", ["web:Dan.6.28-Dan.6.28"], "offset-zone ref lacks"),
    ("cs_dan_zone_bare_mt_3_31", [xx("oshb", 3, 31)], "offset-zone ref lacks"),
    ("cs_dan_zone_bare_mt_6_1", ["oshb:Dan.6.1-Dan.6.1"], "offset-zone ref lacks"),
    ("cs_dan_zone_bare_mt_6_29", [xx("oshb", 6, 29)], "offset-zone ref lacks"),
    # L: ported=cs_edge_web_20_44_ok | the last WEB verse before a zone
    ("cs_edge_web_3_30_ok", ["web:Dan.3.30-Dan.3.30"], None),
    # L: ported=cs_edge_web_22_1_ok | the first WEB verse after the last zone
    ("cs_edge_web_7_1_ok", ["web:Dan.7.1-Dan.7.1"], None),
    # L: created | the other edges
    ("cs_dan_edge_web_5_30_ok", ["web:Dan.5.30-Dan.5.30"], None),
    ("cs_dan_edge_mt_3_30_ok", ["oshb:Dan.3.30-Dan.3.30"], None),
    ("cs_dan_edge_mt_5_30_ok", ["oshb:Dan.5.30-Dan.5.30"], None),
    ("cs_dan_edge_mt_7_1_ok", ["oshb:Dan.7.1-Dan.7.1"], None),
    # L: ported=cs_dual_ok | zone 2
    ("cs_dual_ok", ["web:Dan.4.10-Dan.4.10 = oshb:Dan.4.7"], None),
    # L: ported=cs_dual_bad | zone 2
    ("cs_dual_bad", ["web:Dan.4.10-Dan.4.10 = oshb:Dan.4.10"], "dual-cite arithmetic wrong"),
    # L: ported=cs_mt_qualifier_ok
    ("cs_mt_qualifier_ok", ["web:Dan.4.5-Dan.4.5 (MT 4:2)"], None),
    # L: ported=cs_oshb_20_49_out_of_range | a WEB verse the MT face lacks
    ("cs_oshb_4_35_out_of_range", [xx("oshb", 4, MT_LAST_VERSE[4] + 1)], "out of range for OSHB"),
    # L: created | the converse
    ("cs_dan_web_3_31_out_of_range", [xx("web", 3, LAST_VERSE[3] + 1)], "out of range for WEB"),
    # L: ported=same
    ("cs_small_letter", ["web:Dan.1.1-Dan.1.1 small nun (single-witness)"], "NO special-letter segs of any class"),
    ("cs_large_letter", ["web:Dan.1.1-Dan.1.1 large letter (single-witness)"], "NO special-letter segs of any class"),
    ("cs_qumran_siglum", ["web:Dan.1.1-Dan.1.1 per 4QDan"], "cross-tradition material"),
    ("cs_masada_siglum", ["web:Dan.1.1-Dan.1.1 per MasDan"], "cross-tradition material"),
    # L: created | Daniel's own non-MT witnesses (CROSS re-pointed)
    ("cs_dan_papyrus_siglum", ["web:Dan.1.1-Dan.1.1 per 6QpapDan"], "cross-tradition material"),
    ("cs_dan_theodotion", ["web:Dan.3.23-Dan.3.23 per Theodotion"], "cross-tradition material"),
    ("cs_dan_greek_addition", ["web:Dan.3.23-Dan.3.23 cf. the Prayer of Azariah"], "cross-tradition material"),
    # L: ported=same
    ("cs_selah", ["web:Dan.1.1-Dan.1.1 selah"], "NO selah exists"),
    # L: ported=cs_kq_in_zone_ok | MT 4:9 = WEB 4:12 carries K/Q inside zone 2
    ("cs_kq_in_zone_ok", ["oshb:Dan.4.9-Dan.4.9 = web:Dan.4.12 ketiv/qere"], None),
]
# L: created | one right and one wrong dual for zones 1, 3 and 4 (zone 2 is cs_dual_ok / cs_dual_bad), and the MT-first form
for _i in (1, 3, 4):
    (_wc, _wv), (_mc, _mv) = ZDUAL[_i - 1]
    CS_VECTORS.append(("cs_dan_zone%d_dual_ok" % _i, [xx("web", _wc, _wv, " = oshb:Dan.%d.%d" % (_mc, _mv))], None))
    CS_VECTORS.append(("cs_dan_zone%d_dual_bad" % _i, [xx("web", _wc, _wv, " = oshb:Dan.%d.%d" % ZWRONG[_i - 1])],
                       "dual-cite arithmetic wrong"))
CS_VECTORS.append(("cs_dan_zone4_dual_mt_first_ok", ["oshb:Dan.6.11-Dan.6.11 = web:Dan.6.10"], None))

# (decision_id, prose, rule id, expect the rule to fire)
CM_VECTORS = [
    # L: ported=cm_puncta_41_20_ok | negative: no Dan site
    ("cm_puncta_oshb_4_20_red", "the puncta extraordinaria in oshb:Dan.4.20 are a byte feature", "puncta_claim_in_ezek", True),
    # L: ported=cm_puncta_46_22_ok | negative
    ("cm_puncta_web_6_22_red", "puncta extraordinaria at web:Dan.6.22", "puncta_claim_in_ezek", True),
    # L: ported=cm_puncta_41_21_bad
    ("cm_puncta_oshb_1_21_bad", "puncta extraordinaria at oshb:Dan.1.21", "puncta_claim_in_ezek", True),
    # L: ported=same
    ("cm_small_letter", "a small nun at oshb:Dan.1.1", "small_letter_claim_in_jer", True),
    ("cm_selah", "selah at oshb:Dan.1.1", "selah_claim_in_jer", True),
    # L: ported=same | MT 1:28 (SAMEKH) re-pointed to MT 3:12 (SAMEKH; neither neighbour carries PE)
    ("cm_mark_type_ok", "a setumah follows oshb:Dan.3.12", "paragraph_mark_claim", False),
    ("cm_mark_type_bad", "a petuchah follows oshb:Dan.3.12", "paragraph_mark_claim", True),
    # L: created | a PE verse, both readings
    ("cm_dan_mark_pe_ok", "a petuchah follows oshb:Dan.5.12", "paragraph_mark_claim", False),
    ("cm_dan_mark_pe_as_samekh_bad", "a setumah follows oshb:Dan.5.12", "paragraph_mark_claim", True),
]


ENV = dict(os.environ, PYTHONIOENCODING="utf-8")   # tools print Hebrew; the Windows console codec cannot


def run(tool, rows_path):
    out = subprocess.run([sys.executable, str(HERE / tool), str(rows_path)],
                         capture_output=True, text=True, encoding="utf-8", env=ENV)
    return json.loads(out.stdout)


with tempfile.TemporaryDirectory() as td:
    cs_rows = Path(td) / "cs_vectors.jsonl"
    cs_rows.write_text("\n".join(json.dumps({"decision_id": d, "boundary_evidence_refs": refs}, ensure_ascii=False)
                                 for d, refs, _ in CS_VECTORS), encoding="utf-8")
    rep = run("citation_sweep.py", cs_rows)
    for did, _, expect in CS_VECTORS:
        mine = [p for p in rep["problems"] if p.startswith(did + ":")]
        if expect is None:
            check("citation_sweep %s: no problem" % did, not mine, mine)
        else:
            check("citation_sweep %s: %r" % (did, expect), any(expect in p for p in mine), mine)

    cm_rows = Path(td) / "cm_vectors.jsonl"
    cm_rows.write_text("\n".join(json.dumps({"decision_id": d, "boundary_rationale": prose}, ensure_ascii=False)
                                 for d, prose, _, _ in CM_VECTORS), encoding="utf-8")
    rep = run("check_marks.py", cm_rows)
    for did, _, rule, fires in CM_VECTORS:
        mine = [f for f in rep["flags"] if f.get("decision_id") == did and f.get("rule") == rule]
        check("check_marks %s: %s %s" % (did, rule, "fires" if fires else "silent"), bool(mine) == fires, mine)

# 3. QERE TIER - citation_sweep's Hebrew-binding arm and the normalizer. The Qere is derived from the note layer at
# run time (never typed): MT 8:11's first note (Hebrew), split by kq_split_bytes; for Dan the Aramaic MT 2:5 and the
# mixed verse MT 2:4 are added.
from dan_lib import collate_hebrew, kq_split, kq_split_bytes, language_of, load_pmarks, strip_accents  # noqa: E402

PM = load_pmarks()
OSHB = dict(l.split("\t", 1) for l in (HERE.parent / "Dan_oshb.txt").read_text(encoding="utf-8").splitlines() if "\t" in l)
# D3: fixtures carry the Qere in the note's RAW bytes, which is what a correct row quotes and what the tools compare
# L: ported | the source's MT 1:8 Qere re-pointed to MT 8:11 (MT 1:8 carries no K/Q in Dan)
QERE = kq_split_bytes(PM["kq"]["Dan.8.11"][0], OSHB["Dan.8.11"])[1].replace("/", "")
check("fixture: the MT 8:11 Qere is pointed and absent from the verse bytes, so the Qere tier is what gets tested",
      bool(QERE) and QERE not in OSHB["Dan.8.11"], QERE)
FIRST = OSHB["Dan.1.1"].split(" ")[0]
# L: created
QERE_A = kq_split_bytes(PM["kq"]["Dan.2.5"][0], OSHB["Dan.2.5"])[1].replace("/", "")
W24 = OSHB["Dan.2.4"].split(" ")
ARAM24 = " ".join(W24[4:6])
check("fixture: MT 2:5 is Aramaic and its Qere is absent from its bytes; MT 2:4 has 12 words and its words 5-6 "
      "(Aramaic) do not collate against MT 2:5",
      language_of(2, 5) == "Aramaic" and bool(QERE_A) and QERE_A not in OSHB["Dan.2.5"] and len(W24) == 12
      and collate_hebrew(ARAM24, OSHB["Dan.2.5"]) == "none", [language_of(2, 5), len(W24)])
HEB_VECTORS = [
    # L: ported=same | re-pointed to MT 8:11
    ("cs_qere_disclosed_ok", "the Qere %s at oshb:Dan.8.11 (ketiv/qere, single-witness)" % QERE, None),
    ("cs_qere_undisclosed", "the reading %s at oshb:Dan.8.11" % QERE, "matches the Qere"),
    # L: ported=same
    ("cs_verse_quote_ok", "%s opens oshb:Dan.1.1" % FIRST, None),
    # L: created | the Aramaic Qere tier and the mixed verse
    ("cs_dan_aramaic_qere_disclosed_ok", "the Qere %s at oshb:Dan.2.5 (ketiv/qere, single-witness)" % QERE_A, None),
    ("cs_dan_aramaic_qere_undisclosed", "the reading %s at oshb:Dan.2.5" % QERE_A, "matches the Qere"),
    ("cs_dan_mixed_2_4_hebrew_words_ok", "%s opens oshb:Dan.2.4" % " ".join(W24[:2]), None),
    ("cs_dan_mixed_2_4_aramaic_words_ok", "the Aramaic %s (oshb:Dan.2.4)" % ARAM24, None),
    ("cs_dan_mixed_2_4_words_at_wrong_verse", "the Aramaic %s (oshb:Dan.2.5)" % ARAM24, "does not collate"),
]
with tempfile.TemporaryDirectory() as td:
    hp = Path(td) / "heb_vectors.jsonl"
    hp.write_text("\n".join(json.dumps({"decision_id": d, "boundary_rationale": prose}, ensure_ascii=False)
                            for d, prose, _ in HEB_VECTORS), encoding="utf-8")
    rep = run("citation_sweep.py", hp)
    for did, _, expect in HEB_VECTORS:
        mine = [p for p in rep["problems"] if p.startswith(did + ":")]
        if expect is None:
            check("citation_sweep %s: no problem" % did, not mine, mine)
        else:
            check("citation_sweep %s: %r" % (did, expect), any(expect in p for p in mine), mine)
    for label, payload, want_defects, want_qere in (
            ("normalize: a Qere is accepted and counted under qere", {"a": "x %s y" % QERE}, 0, 1),
            ("normalize: a pointed run in neither the verse bytes nor the Qere layer stays a defect",
             {"b": QERE + "תָ"}, 1, 0)):
        fp = Path(td) / ("norm_%d.json" % want_defects)
        fp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        proc = subprocess.run([sys.executable, str(HERE / "normalize_hebrew_in_json.py"), str(fp)],
                              capture_output=True, text=True, encoding="utf-8", env=ENV)
        nrep = json.loads(proc.stdout.strip().splitlines()[-1])
        check(label, nrep["defect_count"] == want_defects and nrep.get("qere", 0) == want_qere, nrep)

# 4. REGRESSION - the source book's first puncta arms flagged all 12 puncta mentions in its real rows, every one
# wrongly: negated disclosures and correct disclosures citing a bare site number. Dan has no site, so each ported
# vector whose claim was TRUE at a site is its negative here (a positive claim is RED; a denial is true and GREEN).
PUNCTA2_CS = [
    # L: ported=same
    ("cs_puncta_negated_ok", ["web:Dan.1.5-Dan.1.5 (no puncta here)"], None),
    # L: ported=cs_puncta_denied_at_site | negative: no Dan verse carries puncta, so the denial is true
    ("cs_puncta_denied_true_ok", ["oshb:Dan.8.20-Dan.8.20 (no puncta)"], None),
    # L: ported=cs_puncta_range_ok | negative
    ("cs_puncta_range_red", ["web:Dan.8.1-Dan.8.26 (puncta at 8:20, single-witness)"], "claims puncta extraordinaria"),
    # L: ported=cs_kq_editorial_note_ok | MT 3:20 re-pointed to MT 2:29: an OSHB note on a ketib/qere, no kq entry
    ("cs_kq_editorial_note_ok",
     ["oshb:Dan.2.29-Dan.2.29 (OSHB editorial note, single-witness: a ketiv/qere read with L against BHS)"], None),
    # L: ported=cs_kq_none_bad | MT 5:2 re-pointed to MT 1:2, which carries no K/Q and no note
    ("cs_kq_none_bad", ["oshb:Dan.1.2-Dan.1.2 (ketiv/qere, single-witness)"], "kq inventory has none"),
]
PUNCTA2_CM = [
    # L: ported=same
    ("cm_puncta_negated_ok", "No K/Q, no paseq, no puncta and no zone-dual issue touches this span.",
     "Dan.1.5-Dan.1.20", {"puncta_claim_in_ezek": False, "false_puncta_absence_claim": False}),
    # L: ported=cm_puncta_absence_false | negative: the absence claim is true in Dan
    ("cm_puncta_absence_true_ok", "No editorial note and no puncta extraordinaria fall inside this span.",
     "Dan.8.15-Dan.8.26", {"false_puncta_absence_claim": False, "puncta_claim_in_ezek": False}),
    # L: ported=cm_puncta_bare_number_ok | negative
    ("cm_puncta_bare_number_red", "Puncta extraordinaria disclosed at 8:20, single witness.", None,
     {"puncta_claim_in_ezek": True}),
    # L: ported=cm_puncta_dotted_number_ok | negative
    ("cm_puncta_dotted_number_red", "MT 8.22 carries seven U+05C4 puncta-extraordinaria combining marks.", None,
     {"puncta_claim_in_ezek": True}),
    # L: ported=same | MT 3:20 re-pointed to MT 2:29
    ("cm_kq_editorial_note_ok", "the editorial note at oshb:Dan.2.29 records a ketiv/qere relative to BHS", None,
     {"kq_claim": False}),
    # L: ported=same | MT 5:2 re-pointed to MT 1:2
    ("cm_kq_none_bad", "a ketiv/qere at oshb:Dan.1.2", None, {"kq_claim": True}),
    # second-round regressions from the source book's real rows: a distant "not" is no negation (P11-009), and a span
    # covering a site satisfied a positive claim whose number sat outside the window (P10-008). With no Dan site
    # both claims are positive and RED.
    # L: ported=cm_puncta_distant_not_ok | negative: the distant "not" still does not negate
    ("cm_puncta_distant_not_red",
     "that is source-true, not degradation, and the NFD arm must treat U+05C4 as a legitimate combining mark.",
     "Dan.8.19-Dan.8.24", {"false_puncta_absence_claim": False, "puncta_claim_in_ezek": True}),
    # L: ported=cm_puncta_span_covers_site_ok | negative: no span covers a site
    ("cm_puncta_span_covers_no_site_red", "five instances of the upper dot U+05C4, disclosed here single-witness",
     "Dan.8.12-Dan.8.20", {"puncta_claim_in_ezek": True}),
    # L: ported=same
    ("cm_puncta_no_site_still_flags", "five instances of the upper dot U+05C4, disclosed here single-witness",
     "Dan.1.1-Dan.1.4", {"puncta_claim_in_ezek": True}),
]
with tempfile.TemporaryDirectory() as td:
    p2 = Path(td) / "cs_puncta2.jsonl"
    p2.write_text("\n".join(json.dumps({"decision_id": d, "boundary_evidence_refs": refs}) for d, refs, _ in PUNCTA2_CS),
                  encoding="utf-8")
    rep = run("citation_sweep.py", p2)
    for did, _, expect in PUNCTA2_CS:
        mine = [p for p in rep["problems"] if p.startswith(did + ":")]
        if expect is None:
            check("citation_sweep %s: no problem" % did, not mine, mine)
        else:
            check("citation_sweep %s: %r" % (did, expect), any(expect in p for p in mine), mine)
    p3 = Path(td) / "cm_puncta2.jsonl"
    lines = []
    for d, prose, span, _ in PUNCTA2_CM:
        row = {"decision_id": d, "boundary_rationale": prose}
        if span:
            row["span"] = span
        lines.append(json.dumps(row))
    p3.write_text("\n".join(lines), encoding="utf-8")
    rep = run("check_marks.py", p3)
    for d, _, _, expect in PUNCTA2_CM:
        for rule, fires in expect.items():
            mine = [f for f in rep["flags"] if f.get("decision_id") == d and f.get("rule") == rule]
            check("check_marks %s: %s %s" % (d, rule, "fires" if fires else "silent"), bool(mine) == fires, mine)

# 5. T1 REVIEW REGRESSIONS (ezek_toolkit_review_t1_a1#e2, 2026-09-10) - each vector is the reviewer's own attack or its
# direct counterpart, so a later edit cannot quietly reopen what the review closed. Dan: with no site, every presence
# claim is RED and every denial GREEN; the second Qere is the Aramaic MT 2:5.
# L: ported | the source's MT 3:15 Qere re-pointed to MT 2:5 (Aramaic)
QERE2 = kq_split_bytes(PM["kq"]["Dan.2.5"][0], OSHB["Dan.2.5"])[1].replace("/", "")
check("fixture: MT 2:5 Qere differs from MT 8:11 Qere, and the MT 8:11 Qere does not collate against MT 2:5",
      bool(QERE2) and QERE2 != QERE and QERE2 not in OSHB["Dan.2.5"] and collate_hebrew(QERE, OSHB["Dan.2.5"]) == "none", QERE2)
T1_CS = [
    # L: ported=same
    ("cs_t1_01_wrong_number_in_covering_range", ["web:Dan.8.1-Dan.8.26 (puncta at 8:5, single-witness)"],
     "claims puncta extraordinaria"),
    # L: ported=cs_t1_03_double_negation_asserts_presence_ok | negative: the double negation asserts presence, RED in Dan
    ("cs_t1_03_double_negation_asserts_presence_red", ["oshb:Dan.8.20-Dan.8.20 (not without puncta, single-witness)"],
     "claims puncta extraordinaria"),
    # L: ported=cs_negation_naming_a_site_fails | negative: a denial naming a verse is true in Dan
    ("cs_negation_naming_a_verse_ok", ["web:Dan.8.1-Dan.8.26 (no puncta at 8:20)"], None),
]
T1_CM = [
    # L: ported=same
    ("cm_t1_02_wrong_number_span_covers_site", "the puncta extraordinaria sit at 8:5 in this span",
     "Dan.8.12-Dan.8.20", {"puncta_claim_in_ezek": True}),
    # L: ported=cm_t1_03_double_negation_ok | negative
    ("cm_t1_03_double_negation_red", "this span is not without puncta extraordinaria at 8:20",
     "Dan.8.12-Dan.8.20", {"false_puncta_absence_claim": False, "puncta_claim_in_ezek": True}),
    # L: ported=cm_real_row_distant_next_verse_number_ok | negative
    ("cm_real_row_distant_next_verse_number_red",
     "the word carrying the book's puncta extraordinaria -- five instances of the upper dot U+05C4, disclosed here "
     "single-witness -- a natural summary line before 8:21 returns to the measurements",
     "Dan.8.12-Dan.8.20", {"puncta_claim_in_ezek": True}),
]
T1_HEB = [
    # T1-04: the disclosure keyword must stand near THIS run, not merely somewhere in the field
    # L: ported=same | the source's MT 1:8 / 3:15 re-pointed to MT 8:11 / 2:5
    ("cs_t1_04_second_qere_rides_on_distant_disclosure",
     "the Qere %s at oshb:Dan.8.11 (ketiv/qere, single-witness). %s The reading %s at oshb:Dan.2.5."
     % (QERE, "Unrelated prose follows here to push the second quote far from the first disclosure keyword. " * 3, QERE2),
     "matches the Qere at oshb:Dan.2.5"),
    # hard_gate 'unclear': a Qere cited at the WRONG verse is refused per verse by citation_sweep
    # L: ported=same
    ("cs_qere_cited_at_wrong_verse_refused", "the Qere %s at oshb:Dan.2.5 (ketiv/qere, single-witness)" % QERE,
     "does not collate"),
]
with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "t1_cs.jsonl"
    p.write_text("\n".join(json.dumps({"decision_id": d, "boundary_evidence_refs": refs}) for d, refs, _ in T1_CS), encoding="utf-8")
    rep = run("citation_sweep.py", p)
    for did, _, expect in T1_CS:
        mine = [x for x in rep["problems"] if x.startswith(did + ":")]
        check("citation_sweep %s: %s" % (did, "no problem" if expect is None else repr(expect)),
              (not mine) if expect is None else any(expect in x for x in mine), mine)
    p = Path(td) / "t1_cm.jsonl"
    p.write_text("\n".join(json.dumps({"decision_id": d, "boundary_rationale": prose, "span": span})
                           for d, prose, span, _ in T1_CM), encoding="utf-8")
    rep = run("check_marks.py", p)
    for d, _, _, expect in T1_CM:
        for rule, fires in expect.items():
            mine = [f for f in rep["flags"] if f.get("decision_id") == d and f.get("rule") == rule]
            check("check_marks %s: %s %s" % (d, rule, "fires" if fires else "silent"), bool(mine) == fires, mine)
    p = Path(td) / "t1_heb.jsonl"
    p.write_text("\n".join(json.dumps({"decision_id": d, "boundary_rationale": prose}, ensure_ascii=False)
                           for d, prose, _ in T1_HEB), encoding="utf-8")
    rep = run("citation_sweep.py", p)
    for did, _, expect in T1_HEB:
        mine = [x for x in rep["problems"] if x.startswith(did + ":")]
        check("citation_sweep %s: %r" % (did, expect), any(expect in x for x in mine), mine)
    fp = Path(td) / "norm_cross_verse.json"
    fp.write_text(json.dumps({"a": "x %s at oshb:Dan.3.15" % QERE}, ensure_ascii=False), encoding="utf-8")
    proc = subprocess.run([sys.executable, str(HERE / "normalize_hebrew_in_json.py"), str(fp)],
                          capture_output=True, text=True, encoding="utf-8", env=ENV)
    nrep = json.loads(proc.stdout.strip().splitlines()[-1])
    check("normalize: the Qere tier is book-wide by design (per-verse binding is citation_sweep's, proven above)",
          nrep["defect_count"] == 0 and nrep.get("qere") == 1, nrep)

# 6. T2 REVIEW REGRESSIONS (ezek_toolkit_repair_review_t2_a1#e1) and D3 (raw note bytes) - the reviewer's own attacks,
# both directions, plus the non-canonical-note case T2 could not construct.
import unicodedata  # noqa: E402
from dan_lib import kq_split_bytes  # noqa: E402

T2_CS = [
    # L: ported=same
    ("cs_t2_01_decoy_site_number", ["web:Dan.8.1-Dan.8.26 (cf. 8:20; but the true puncta claim here is verse 8:5, single-witness)"],
     "claims puncta extraordinaria"),
    # L: ported=cs_t2_02_true_claim_near_nonsite_ok | negative
    ("cs_t2_02_claim_near_other_number_red", ["web:Dan.8.1-Dan.8.26 (8:19 nearby; puncta extraordinaria stand at 8:20, single-witness)"],
     "claims puncta extraordinaria"),
    # L: ported=cs_t2_02_range_holding_site_ok | negative
    ("cs_t2_02_range_red", ["web:Dan.8.1-Dan.8.26 (puncta extraordinaria across 8:18-8:20, single-witness)"],
     "claims puncta extraordinaria"),
    # L: ported=cs_t2_03_distant_negation_denial | negative: the distant negation is a true denial in Dan
    ("cs_t2_03_distant_negation_true_ok",
     ["web:Dan.8.1-Dan.8.26 (the text absolutely does not under any reading carry puncta extraordinaria at 8:20, single-witness)"], None),
    # L: ported=cs_t2_05_mt_phrase_is_not_a_qualifier_ok | negative for its puncta half
    ("cs_t2_05_mt_phrase_puncta_red", ["web:Dan.5.2-Dan.5.2 (MT 8.22 puncta extraordinaria, single-witness)"], "claims puncta extraordinaria"),
    # L: created | the qualifier half of the source vector: an unclosed 'MT n.m' phrase is no numbering qualifier
    ("cs_dan_t2_05_mt_phrase_is_not_a_qualifier_ok", ["web:Dan.5.2-Dan.5.2 (MT 8.22 is cited for comparison only)"], None),
    # L: ported=cs_mixed_site_and_nonsite_ambiguous | negative: with no site no clause can mix, so the claim is RED
    ("cs_mixed_two_numbers_red", ["web:Dan.8.1-Dan.8.26 (puncta extraordinaria at 8:20 and 8:21, single-witness)"], "claims puncta extraordinaria"),
]
T2_CM = [
    # L: ported=same
    ("cm_t2_01_decoy_site_number", "cf. 8:20; but the true puncta claim here is verse 8:5", "Dan.5.1-Dan.5.4",
     {"puncta_claim_in_ezek": True}),
    # L: ported=cm_t2_03_distant_negation | negative: a true denial
    ("cm_t2_03_distant_negation_true_ok", "the text absolutely does not under any reading carry puncta extraordinaria at 8:20",
     "Dan.8.12-Dan.8.20", {"false_puncta_absence_claim": False, "puncta_claim_in_ezek": False}),
    # L: ported=cm_t2_02_true_claim_near_nonsite_ok | negative
    ("cm_t2_02_claim_near_other_number_red", "8:19 nearby; puncta extraordinaria stand at 8:20", "Dan.8.12-Dan.8.20",
     {"puncta_claim_in_ezek": True, "false_puncta_absence_claim": False}),
]
NONCANON = next((ref, n) for ref, ns in PM["kq"].items() for n in ns
                if n != unicodedata.normalize("NFC", n) and kq_split_bytes(n, OSHB[ref])[1])
RAWQ = kq_split_bytes(NONCANON[1], OSHB[NONCANON[0]])[1].replace("/", "")
NFDQ = unicodedata.normalize("NFD", RAWQ)
check("fixture: a non-canonical note's raw Qere differs from its NFD form", RAWQ != NFDQ, NONCANON[0])
REF_NC = "oshb:" + NONCANON[0]
T2_HEB = [
    # L: ported=same | the source's MT 1:8 / 3:15 re-pointed to MT 8:11 / 2:5
    ("cs_t2_04_short_gap_second_qere", "the Qere %s at oshb:Dan.8.11 (ketiv/qere, single-witness). A short gap. The reading %s at oshb:Dan.2.5."
     % (QERE, QERE2), "matches the Qere at oshb:Dan.2.5"),
    # L: ported=same
    ("cs_d3_raw_noncanonical_qere_ok", "the Qere %s at %s (ketiv/qere, single-witness)" % (RAWQ, REF_NC), None),
]
with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "t2_cs.jsonl"
    p.write_text("\n".join(json.dumps({"decision_id": d, "boundary_evidence_refs": refs}) for d, refs, _ in T2_CS), encoding="utf-8")
    rep = run("citation_sweep.py", p)
    for did, _, expect in T2_CS:
        mine = [x for x in rep["problems"] if x.startswith(did + ":")]
        check("citation_sweep %s: %s" % (did, "no problem" if expect is None else repr(expect)),
              (not mine) if expect is None else any(expect in x for x in mine), mine)
    p = Path(td) / "t2_cm.jsonl"
    p.write_text("\n".join(json.dumps({"decision_id": d, "boundary_rationale": prose, "span": span}) for d, prose, span, _ in T2_CM),
                 encoding="utf-8")
    rep = run("check_marks.py", p)
    for d, _, _, expect in T2_CM:
        for rule, fires in expect.items():
            mine = [f for f in rep["flags"] if f.get("decision_id") == d and f.get("rule") == rule]
            check("check_marks %s: %s %s" % (d, rule, "fires" if fires else "silent"), bool(mine) == fires, mine)
    p = Path(td) / "t2_heb.jsonl"
    p.write_text("\n".join(json.dumps({"decision_id": d, "boundary_rationale": prose}, ensure_ascii=False) for d, prose, _ in T2_HEB)
                 + "\n" + json.dumps({"decision_id": "cs_d3_nfd_form_of_noncanonical_qere_refused",
                                      "boundary_rationale": "the Qere %s at %s (ketiv/qere, single-witness)" % (NFDQ, REF_NC)},
                                     ensure_ascii=False), encoding="utf-8")
    rep = run("citation_sweep.py", p)
    for did, _, expect in T2_HEB:
        mine = [x for x in rep["problems"] if x.startswith(did + ":")]
        check("citation_sweep %s: %s" % (did, "no problem" if expect is None else repr(expect)),
              (not mine) if expect is None else any(expect in x for x in mine), mine)
    nfd_did = "cs_d3_nfd_form_of_noncanonical_qere_refused"
    refused = [x for x in rep["problems"] if x.startswith(nfd_did + ":")] + [x for x in rep.get("nfd_degraded", []) if x.startswith(nfd_did + ":")]
    check("citation_sweep %s: the NFD form is not accepted as the Qere" % nfd_did, bool(refused), refused)
    for label, payload, want_qere in (("normalize D3: the raw bytes of a non-canonical Qere are accepted", {"a": "x %s y" % RAWQ}, 1),
                                      ("normalize D3: the NFD form of that Qere is not accepted as a Qere", {"b": "x %s y" % NFDQ}, 0)):
        fp = Path(td) / ("norm_d3_%d.json" % want_qere)
        fp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        proc = subprocess.run([sys.executable, str(HERE / "normalize_hebrew_in_json.py"), str(fp)],
                              capture_output=True, text=True, encoding="utf-8", env=ENV)
        nrep = json.loads(proc.stdout.strip().splitlines()[-1])
        ok = nrep.get("qere", 0) == want_qere and (nrep["defect_count"] == 0 if want_qere else (nrep["defect_count"] + nrep.get("fixed", 0)) >= 1)
        check(label, ok, nrep)

# 7. CALENDAR-DATE arm. The constants are asserted against dan_device_inventory.json (face MT): its
# citation_sweep_constants, and its datelines and calendar_dates_not_datelines entries (the source keys dated_oracles
# and calendar_dates_not_datelines, as the inventory's ezek_key_crosswalk maps them). CAL_NO_ONSET is EMPTY in Dan,
# so no onset vector can fail: each ported onset vector that expected a refusal is its negative here.
INV = json.loads((HERE.parent / "dan_device_inventory.json").read_text(encoding="utf-8"))
CSC = INV["citation_sweep_constants"]


def _pairs(keys):
    return {tuple(int(x) for x in k.split(".")[1:]) for k in keys}


# L: ported | re-pointed to the Dan inventory and its counts; the face checks are created
check("calendar constants: the inventory and its constants are on the MT face", INV["numbering_face"] == "MT" and CSC["face"] == "MT",
      [INV.get("numbering_face"), CSC.get("face")])
check("calendar constants: CAL_DATE_PAIRS == inventory calendar_dates_not_datelines (count %s)" % INV["calendar_dates_not_datelines"]["count"],
      cs.CAL_DATE_PAIRS == _pairs(INV["calendar_dates_not_datelines"]["verses_mt"]) == {tuple(p) for p in CSC["CAL_DATE_PAIRS"]}
      and len(cs.CAL_DATE_PAIRS) == int(INV["calendar_dates_not_datelines"]["count"]), sorted(cs.CAL_DATE_PAIRS))
check("calendar constants: DATELINE_PAIRS == inventory datelines (count %s)" % INV["datelines"]["count"],
      cs.DATELINE_PAIRS == _pairs(INV["datelines"]["verses_mt"]) == {tuple(p) for p in CSC["DATELINE_PAIRS"]}
      and len(cs.DATELINE_PAIRS) == int(INV["datelines"]["count"]), sorted(cs.DATELINE_PAIRS))
check("calendar constants: CAL_NO_ONSET is empty, as the inventory records, so every calendar date may open a row",
      cs.CAL_NO_ONSET == {tuple(p) for p in CSC["CAL_NO_ONSET"]} == set() and cs.CAL_DATE_PAIRS - cs.CAL_NO_ONSET == cs.CAL_DATE_PAIRS)
check("calendar constants: no pair falls in a numbering zone, so the WEB-face numbers equal the MT-face ones",
      all(web_to_mt(*p) == p and mt_to_web(*p) == p for p in cs.CAL_DATE_PAIRS | cs.DATELINE_PAIRS))
CAL_ROWS = [
    # L: ported=cal_onset_45_18_ok | the calendar date MT 10:4 opens a row, its rationale denying a dateline
    ("cal_onset_10_4_ok", {"span": "Dan.10.4-Dan.10.21", "boundary_rationale":
                           "the onset follows the petuchah at 10:3; the date clause at oshb:Dan.10.4 is not a dateline"}, None),
    # L: ported=cal_onset_45_19_ok
    ("cal_onset_10_5_ok", {"span": "Dan.10.5-Dan.10.21"}, None),
    # L: ported=cal_onset_45_20_bad | negative: CAL_NO_ONSET is empty, so a bare calendar-date onset passes
    ("cal_onset_10_4_no_formula_ok", {"span": "Dan.10.4-Dan.10.9"}, None),
    # L: ported=cal_onset_45_21_bad | negative, on the web:-prefixed span form
    ("cal_onset_web_10_4_ok", {"span": "web:Dan.10.4-Dan.10.21"}, None),
    # L: ported=cal_onset_45_25_bad | negative, a single-verse span
    ("cal_onset_10_4_single_ok", {"span": "Dan.10.4-Dan.10.4"}, None),
    # L: created | a calendar date as a row onset, argued in the rationale and denied as a dateline
    ("cal_dan_calendar_date_onset_ok", {"span": "Dan.10.4-Dan.10.21", "boundary_rationale":
                                        "the unit opens at the calendar date 10:4 (month and day, no year word), not a dateline"}, None),
    # L: ported=cal_prose_claim_45_18_bad
    ("cal_prose_claim_10_4_bad", {"boundary_rationale": "the dateline at 10:4 opens the vision"}, "claims a dateline at MT 10:4"),
    # L: ported=same | the source's calendar dates re-pointed to MT 10:4 and its real datelines to MT 9:1, 9:2 and 10:1
    ("cal_prose_number_first_bad", {"boundary_rationale": "Dan.10.4 is a dateline"}, "claims a dateline at MT 10:4"),
    ("cal_prose_list_bad", {"boundary_rationale": "datelines at 9:1, 9:2 and 10:4"}, "claims a dateline at MT 10:4"),
    ("cal_prose_double_negation_bad", {"boundary_rationale": "10:4 is not without a dateline"}, "claims a dateline at MT 10:4"),
    ("cal_prose_negated_ok", {"boundary_rationale": "10:4 is not a dateline, having no year word"}, None),
    ("cal_prose_non_dateline_ok", {"boundary_rationale": "the non-dateline calendar date at 10.4"}, None),
    ("cal_prose_real_dateline_ok", {"boundary_rationale": "the dateline at 10:1 opens the vision"}, None),
    ("cal_prose_other_clause_ok", {"boundary_rationale": "unlike the dateline at 10:1, the date at 10:4 carries no year word"}, None),
    ("cal_prose_unnumbered_ok", {"boundary_rationale": "the date clause fails the book's structural dateline test"}, None),
    ("cal_ref_bare_claim_bad", {"boundary_evidence_refs": ["oshb:Dan.10.4-Dan.10.4 (dateline; single-witness)"]}, "claims a dateline at MT 10:4"),
    ("cal_ref_numbered_claim_bad", {"boundary_evidence_refs": ["web:Dan.10.2-Dan.10.9 (dateline at 10:4)"]}, "claims a dateline at MT 10:4"),
    ("cal_ref_denial_ok", {"boundary_evidence_refs": ["oshb:Dan.10.4-Dan.10.4 (disclosure: not a dateline (no year word), single-witness)"]}, None),
    ("cal_ref_real_dateline_ok", {"boundary_evidence_refs": ["oshb:Dan.10.1-Dan.10.1 (dateline; single-witness)"]}, None),
    # L: created | a ref covering a real dateline and the calendar date, naming no number, passes; the WEB face binds too
    ("cal_dan_ref_covers_dateline_and_date_ok", {"boundary_evidence_refs": ["web:Dan.10.1-Dan.10.4 (dateline; single-witness)"]}, None),
    ("cal_dan_ref_web_face_bad", {"boundary_evidence_refs": ["web:Dan.10.4-Dan.10.4 (dateline; single-witness)"]}, "claims a dateline at MT 10:4"),
]
with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "cal_cs.jsonl"
    p.write_text("\n".join(json.dumps(dict({"decision_id": d}, **fields), ensure_ascii=False) for d, fields, _ in CAL_ROWS),
                 encoding="utf-8")
    rep = run("citation_sweep.py", p)
    for did, _, expect in CAL_ROWS:
        mine = [x for x in rep["problems"] if x.startswith(did + ":")]
        check("citation_sweep %s: %s" % (did, "no problem" if expect is None else repr(expect)),
              (not mine) if expect is None else any(expect in x for x in mine), mine)

# 8. R4(ii) AND CAL-1 CHANGES (ezek_controlling_rulings_a1#e3): a verse number in a parenthetical opening directly after
# the mention's clause now binds the claim in both tools, and a ref annotation's number binds at any distance (RED vectors
# NOVEL-A ref and prose, NOVEL-A2 ref distance, NOVEL-F prose parenthetical). The prose arm keeps its 60-character reach,
# because the real-row vector cm_real_row_distant_next_verse_number_ok (section 5 of the source) pinned a TRUE claim
# against the next verse's number - an implementation deviation from order (2), recorded for T4 and the controlling
# agent. The apposition and parenthesis forms of a dateline claim now bind (RED). GREEN controls keep a prior-clause
# negator, 'nonetheless', 'not without', true sites, and the other clause. Dan has no site, so the site controls are
# negatives here; the message shows that the number bound ('names a verse that carries none').
R4II_CS = [
    # L: ported=same
    ("cs_r4ii_novel_a_paren_nonsite", ["web:Dan.8.1-Dan.8.26 puncta extraordinaria (8:5)"], "claims puncta extraordinaria"),
    ("cs_r4ii_novel_a2_distant_nonsite",
     ["web:Dan.8.1-Dan.8.26 puncta extraordinaria are recorded in this measured span by the single witness, standing at verse 8:5"],
     "claims puncta extraordinaria"),
    # L: ported=cs_r4ii_paren_site_ok | negative
    ("cs_r4ii_paren_number_red", ["web:Dan.8.1-Dan.8.26 puncta extraordinaria (8:20, single-witness)"], "names a verse that carries none"),
    # L: ported=cs_r4ii_distant_site_ok | negative
    ("cs_r4ii_distant_number_red",
     ["web:Dan.8.1-Dan.8.26 puncta extraordinaria are recorded in this measured span by the single witness, standing at verse 8:20"],
     "names a verse that carries none"),
]
R4II_CM = [
    # L: ported=same
    ("cm_r4ii_novel_a_prose_paren_nonsite", "the puncta extraordinaria (8:5)", "Dan.8.12-Dan.8.20", {"puncta_claim_in_ezek": True}),
    ("cm_r4ii_novel_f_paren_nonsite", "the puncta extraordinaria (five dots at 8:5)", "Dan.8.12-Dan.8.20", {"puncta_claim_in_ezek": True}),
    # L: ported=cm_r4ii_paren_site_ok | negative
    ("cm_r4ii_paren_number_red", "the puncta extraordinaria (five dots at 8:20)", "Dan.8.12-Dan.8.20",
     {"puncta_claim_in_ezek": True, "false_puncta_absence_claim": False}),
    # L: ported=cm_r4ii_prior_clause_negator_ok | negative: the prior-clause negator still does not negate
    ("cm_r4ii_prior_clause_negator_red", "no paseq stands at 8:5; the puncta extraordinaria at 8:20 are in the verse bytes",
     "Dan.8.12-Dan.8.20", {"puncta_claim_in_ezek": True, "false_puncta_absence_claim": False}),
    # L: ported=cm_r4ii_nonetheless_ok | negative
    ("cm_r4ii_nonetheless_red", "nonetheless the puncta extraordinaria stand at 8:20", "Dan.8.12-Dan.8.20",
     {"puncta_claim_in_ezek": True, "false_puncta_absence_claim": False}),
    # L: ported=cm_r4ii_not_without_ok | negative
    ("cm_r4ii_not_without_red", "this verse is not without puncta extraordinaria at 8:20", "Dan.8.12-Dan.8.20",
     {"puncta_claim_in_ezek": True, "false_puncta_absence_claim": False}),
]
CAL1_ROWS = [
    # L: ported=same | the source's MT 45:18 re-pointed to MT 10:4, its real dateline to MT 10:1
    ("cal1_apposition_bad", {"boundary_rationale": "the onset stands at 10:4, a dateline-grade onset"}, "claims a dateline at MT 10:4"),
    ("cal1_parenthesis_bad", {"boundary_rationale": "the dateline (10:4) opens the vision"}, "claims a dateline at MT 10:4"),
    ("cal1_apposition_negated_ok", {"boundary_rationale": "the onset stands at 10:4, not a dateline"}, None),
    ("cal1_own_clause_number_ok", {"boundary_rationale": "the unit opens at 10:4, the dateline at 10:1 is close behind"}, None),
    ("cal1_other_clause_kept_ok", {"boundary_rationale": "unlike the dateline at 10:1, the date at 10:4 carries no year word"}, None),
]
with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "r4ii_cs.jsonl"
    p.write_text("\n".join(json.dumps({"decision_id": d, "boundary_evidence_refs": refs}) for d, refs, _ in R4II_CS)
                 + "\n" + "\n".join(json.dumps(dict({"decision_id": d}, **f), ensure_ascii=False) for d, f, _ in CAL1_ROWS),
                 encoding="utf-8")
    rep = run("citation_sweep.py", p)
    for did, _, expect in R4II_CS + CAL1_ROWS:
        mine = [x for x in rep["problems"] if x.startswith(did + ":")]
        check("citation_sweep %s: %s" % (did, "no problem" if expect is None else repr(expect)),
              (not mine) if expect is None else any(expect in x for x in mine), mine)
    p = Path(td) / "r4ii_cm.jsonl"
    p.write_text("\n".join(json.dumps({"decision_id": d, "boundary_rationale": prose, "span": span}) for d, prose, span, _ in R4II_CM),
                 encoding="utf-8")
    rep = run("check_marks.py", p)
    for d, _, _, expect in R4II_CM:
        for rule, fires in expect.items():
            mine = [f for f in rep["flags"] if f.get("decision_id") == d and f.get("rule") == rule]
            check("check_marks %s: %s %s" % (d, rule, "fires" if fires else "silent"), bool(mine) == fires, mine)

# 9. T4 FINDINGS - the batched edit proposed to ezek_controlling_rulings_a1#e4 (installed only after its ruling, then a
# fresh distinct review). T4-01: digits that follow a letter ('R4.5') are an id, not a verse. T4-03: a closed set of
# denials LATER in the clause denies, read through a parenthetical; a bare later 'no', 'none of' and a non-final
# 'is missing' do not, and a denial behind a comma stays outside the clause (a disclosed residual, pinned RED).
# T4-04: a true puncta ref needs single-witness disclosure, hyphenated or spaced; with no Dan site that branch cannot
# be reached, so its two vectors are negatives.
T4_CS = [
    # L: ported=cs_t4_01_decoy_letter_id_ok | negative: RED, and the message shows R4.5 was read as no verse number
    ("cs_t4_01_decoy_letter_id_red",
     ["web:Dan.8.1-Dan.8.26 puncta extraordinaria (cross-referenced at row R4.5 in the ledger), single-witness"], "the ref covers no site"),
    # L: ported=cs_t4_01_dotted_ezek_ref_still_binds
    ("cs_t4_01_dotted_dan_ref_still_binds", ["web:Dan.8.1-Dan.8.26 puncta extraordinaria (Dan.8.5, single-witness)"],
     "names a verse that carries none"),
    # L: ported=same
    ("cs_t4_03_puncta_denial_after_nonsite_ok",
     ["web:Dan.8.1-Dan.8.10 puncta extraordinaria would be expected at 8:5 but none stands"], None),
    # L: ported=cs_t4_03_puncta_denial_after_at_site | negative: the later denial is true in Dan
    ("cs_t4_03_puncta_denial_after_true_ok",
     ["oshb:Dan.8.20-Dan.8.20 puncta extraordinaria would be expected here but none stands"], None),
    # L: ported=cs_t4_04_site_without_disclosure | negative: no site, so the claim is RED before disclosure is judged
    ("cs_t4_04_number_without_disclosure_red", ["web:Dan.8.1-Dan.8.26 puncta extraordinaria (8:20)"], "claims puncta extraordinaria"),
    # L: ported=cs_t4_04_spaced_single_witness_ok | negative
    ("cs_t4_04_spaced_single_witness_red", ["web:Dan.8.1-Dan.8.26 puncta extraordinaria at 8:20, single witness"], "claims puncta extraordinaria"),
]
T4_CAL_ROWS = [
    # L: ported=same | the source's MT 45:18 re-pointed to MT 10:4
    ("cal_t4_03_apposition_denial_ok", {"boundary_rationale": "the unit opens at 10:4, where a dateline would be expected but none stands"}, None),
    ("cal_t4_03_parenthesis_denial_ok", {"boundary_rationale": "the dateline (10:4) would be expected but none stands"}, None),
    ("cal_t4_03_absent_at_clause_end_ok", {"boundary_rationale": "a dateline at 10:4 is absent"}, None),
    ("cal_t4_03_bare_later_no_stays_red", {"boundary_rationale": "the dateline at 10:4 opens no new year"}, "claims a dateline at MT 10:4"),
    ("cal_t4_03_none_of_stays_red", {"boundary_rationale": "the dateline at 10:4 but none of the other dates"}, "claims a dateline at MT 10:4"),
    ("cal_t4_03_missing_not_final_stays_red", {"boundary_rationale": "the dateline at 10:4 is missing its year word"},
     "claims a dateline at MT 10:4"),
    ("cal_t4_03_denial_behind_comma_residual_red", {"boundary_rationale": "a dateline at 10:4 would be expected, though none stands"},
     "claims a dateline at MT 10:4"),
]
T4_CM = [
    # L: ported=cm_t4_01_decoy_letter_id_ok | negative
    ("cm_t4_01_decoy_letter_id_red", "the puncta extraordinaria (cross-referenced at row R4.5 in the ledger)", "Dan.8.12-Dan.8.20",
     {"puncta_claim_in_ezek": True, "false_puncta_absence_claim": False}),
    # L: ported=same
    ("cm_t4_03_denial_after_nonsite_ok", "puncta extraordinaria would be expected at 8:5 but none stands", "Dan.8.1-Dan.8.10",
     {"puncta_claim_in_ezek": False, "false_puncta_absence_claim": False}),
    # L: ported=cm_t4_03_denial_after_at_site_flags | negative: a true denial
    ("cm_t4_03_denial_after_true_ok", "puncta extraordinaria would be expected at 8:20 but none stands", "Dan.8.12-Dan.8.20",
     {"false_puncta_absence_claim": False, "puncta_claim_in_ezek": False}),
]
with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "t4_cs.jsonl"
    p.write_text("\n".join(json.dumps({"decision_id": d, "boundary_evidence_refs": refs}) for d, refs, _ in T4_CS)
                 + "\n" + "\n".join(json.dumps(dict({"decision_id": d}, **f), ensure_ascii=False) for d, f, _ in T4_CAL_ROWS),
                 encoding="utf-8")
    rep = run("citation_sweep.py", p)
    for did, _, expect in T4_CS + T4_CAL_ROWS:
        mine = [x for x in rep["problems"] if x.startswith(did + ":")]
        check("citation_sweep %s: %s" % (did, "no problem" if expect is None else repr(expect)),
              (not mine) if expect is None else any(expect in x for x in mine), mine)
    p = Path(td) / "t4_cm.jsonl"
    p.write_text("\n".join(json.dumps({"decision_id": d, "boundary_rationale": prose, "span": span}) for d, prose, span, _ in T4_CM),
                 encoding="utf-8")
    rep = run("check_marks.py", p)
    for d, _, _, expect in T4_CM:
        for rule, fires in expect.items():
            mine = [f for f in rep["flags"] if f.get("decision_id") == d and f.get("rule") == rule]
            check("check_marks %s: %s %s" % (d, rule, "fires" if fires else "silent"), bool(mine) == fires, mine)

# 9b. #e4 AMENDMENTS to TOOLFIX-1 (ezek_controlling_rulings_a1#e4 rulings TOOLFIX-1, T4-03, T4-04). A1: the copular denial's
# clause end may be a newline. A2: a coordinated denial with a verse number and no expectation modal before it does not deny;
# the mention is judged on the numbers before the denial. A3: mark and paseq refs accept 'single witness' spaced.
E4_CS = [
    # L: ported=same
    ("cs_e4_a2_positive_then_denial_nonsite_red",
     ["web:Dan.8.1-Dan.8.26 puncta extraordinaria stand at 8:5 but none is present in ch 9, single-witness"], "claims puncta extraordinaria"),
    # L: ported=cs_e4_a2_positive_then_denial_site_ok | negative: the number before the denial names a verse without puncta
    ("cs_e4_a2_positive_then_denial_red",
     ["web:Dan.8.1-Dan.8.26 puncta extraordinaria stand at 8:20 but none is present at 8:21, single-witness"], "names a verse that carries none"),
    # L: ported=same | the source's MT 1:28 (SAMEKH) re-pointed to MT 3:12 (SAMEKH), its paseq verse to MT 3:2 (paseq)
    ("cs_e4_a3_mark_spaced_single_witness_ok", ["oshb:Dan.3.12-Dan.3.12 samekh (single witness)"], None),
    ("cs_e4_a3_paseq_spaced_single_witness_ok", ["oshb:Dan.3.2-Dan.3.2 paseq (count-only, single witness)"], None),
]
E4_CAL = [
    # L: ported=same | the source's MT 45:18 re-pointed to MT 10:4, its real dateline to MT 10:1
    ("cal_e4_a2_positive_then_denial_red", {"boundary_rationale": "a dateline stands at 10:4 but none stands at 10:5"},
     "claims a dateline at MT 10:4 - a calendar"),
    ("cal_e4_a2_true_then_denial_ok", {"boundary_rationale": "the dateline at 10:1 opens the vision but none stands at 10:4"}, None),
]
E4_CM = [
    # L: ported=cm_e4_a1_copular_denial_at_field_end_flags | negative: the copular denial at the field end is true
    ("cm_e4_a1_copular_denial_true_ok",
     {"boundary_rationale": "puncta extraordinaria are absent", "device_notes": "the span is otherwise unremarkable",
      "span": "Dan.8.12-Dan.8.20"}, {"false_puncta_absence_claim": False, "puncta_claim_in_ezek": False}),
    # L: ported=same
    ("cm_e4_a2_positive_then_denial_nonsite_flags",
     {"boundary_rationale": "puncta extraordinaria stand at 8:5 but none is present in ch 9", "span": "Dan.8.12-Dan.8.20"},
     {"puncta_claim_in_ezek": True}),
]
with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "e4_cs.jsonl"
    p.write_text("\n".join([json.dumps({"decision_id": d, "boundary_evidence_refs": refs}, ensure_ascii=False) for d, refs, _ in E4_CS]
                           + [json.dumps(dict({"decision_id": d}, **f), ensure_ascii=False) for d, f, _ in E4_CAL]), encoding="utf-8")
    rep = run("citation_sweep.py", p)
    for did, _, expect in E4_CS + E4_CAL:
        mine = [x for x in rep["problems"] if x.startswith(did + ":")]
        check("citation_sweep %s: %s" % (did, "no problem" if expect is None else repr(expect)),
              (not mine) if expect is None else any(expect in x for x in mine), mine)
    p = Path(td) / "e4_cm.jsonl"
    p.write_text("\n".join(json.dumps(dict({"decision_id": d}, **f), ensure_ascii=False) for d, f, _ in E4_CM), encoding="utf-8")
    rep = run("check_marks.py", p)
    for d, _, expect in E4_CM:
        for rule, fires in expect.items():
            mine = [fl for fl in rep["flags"] if fl.get("decision_id") == d and fl.get("rule") == rule]
            check("check_marks %s: %s %s" % (d, rule, "fires" if fires else "silent"), bool(mine) == fires, mine)

# 10b. TOOLFIX-2 per ezek_controlling_rulings_a1#e4 ruling TOOLFIX-2 (b). Local helpers keep this file runnable against
# the tools that predate the edit, so its vectors can be shown to discriminate.
import unicodedata  # noqa: E402


def _mk10(ch):
    return unicodedata.category(ch) == "Mn"


def _lt10(ch):
    return "\u05d0" <= ch <= "\u05ea"


def _bnd10(needle, hay, marks=True):
    edge = (lambda ch: _lt10(ch) or _mk10(ch)) if marks else _lt10
    i = hay.find(needle)
    while i != -1:
        j = i + len(needle)
        if (i == 0 or not edge(hay[i - 1])) and (j >= len(hay) or not edge(hay[j])):
            return True
        i = hay.find(needle, i + 1)
    return False


def _skel10(s):
    return "".join(ch for ch in s if not _mk10(ch))


JOINED10 = " | ".join(OSHB.values())
SKEL10 = _skel10(JOINED10)


def _cases10():
    found = {}
    for key, verse in OSHB.items():
        for w in verse.split(" "):
            letters = [i for i, ch in enumerate(w) if _lt10(ch)]
            if len(letters) < 5:
                continue
            if "end" not in found and _mk10(w[-1]):
                k = len(w)
                while k and _mk10(w[k - 1]):
                    k -= 1
                if not _bnd10(w[:k], JOINED10):
                    found["end"] = (key, w, w[:k])
            if "start" not in found:
                rest = w[letters[1]:]
                if not _bnd10(rest, JOINED10):
                    found["start"] = (key, w, rest)
            if "root" not in found:
                sk = _skel10(w)
                inner = sk[1:-1]
                if len(inner) >= 3 and not _bnd10(inner, SKEL10, marks=False):
                    found["root"] = (key, w, inner)
            if len(found) == 3:
                return found
    return found


C10 = _cases10()
check("fixture: word-boundary cases found in the bytes (end, start, root)", set(C10) == {"end", "start", "root"}, sorted(C10))
# L: ported | the source's MT 7:2 K/Q re-pointed to MT 2:10 (Aramaic; its Qere carries an accent, so the accent-stripped
# form is a distinct pointed run). The source vector's typed ketiv and gloss are dropped: the ketiv kq_split_bytes
# returns for MT 2:10 does not collate against the verse (measured 'none'), so it would make the vector fire for
# another reason than the stripped Qere.
Q72b = kq_split_bytes(PM["kq"]["Dan.2.10"][0], OSHB["Dan.2.10"])[1].replace("/", "")
Q72b_STRIPPED = strip_accents(Q72b)
check("fixture: the MT 2:10 Qere is absent from the verse bytes; its accent-stripped form differs and is absent too",
      bool(Q72b) and Q72b not in OSHB["Dan.2.10"] and Q72b_STRIPPED != Q72b and Q72b_STRIPPED not in OSHB["Dan.2.10"], Q72b)
W11b = OSHB["Dan.1.1"].split(" ")
OTHER12b = next(w for w in OSHB["Dan.1.2"].split(" ") if len([ch for ch in w if _lt10(ch)]) >= 3 and w not in OSHB["Dan.1.1"])
# L: ported | the source's MT 1:28 (SAMEKH) re-pointed to MT 3:12, its MT 33:16 (K/Q) to MT 9:5, its MT 40:1-4 to MT 8:1-4
UNMARKED1 = next(v for v in range(2, 12) if not PM["marks"].get("Dan.3.%d" % v) and not PM["kq"].get("Dan.3.%d" % v))
NOMARK_CH = next((c for c in sorted(MT_LAST_VERSE) if not any(k.startswith("Dan.%d." % c) for k in PM["marks"])), None)
NEXT_MARK = next(((int(k.split(".")[1]), int(k.split(".")[2])) for k in sorted(PM["marks"], key=lambda k: (int(k.split(".")[1]), int(k.split(".")[2])))
                  if NOMARK_CH and int(k.split(".")[1]) > NOMARK_CH), None)
check("fixture: MT 3:12 carries SAMEKH, MT 3:%d carries no mark and no K/Q" % UNMARKED1, "SAMEKH" in PM["marks"].get("Dan.3.12", []), UNMARKED1)
check("fixture: a chapter with no parashah mark exists, followed by a marked verse", NOMARK_CH is not None and NEXT_MARK is not None,
      [NOMARK_CH, NEXT_MARK])
check("fixture: MT 9:5 carries a K/Q note and MT 8:1-4 carry no K/Q and no editorial note",
      bool(PM["kq"].get("Dan.9.5")) and not any(PM["kq"].get("Dan.8.%d" % v) or PM.get("notes_other", {}).get("Dan.8.%d" % v)
                                                for v in range(1, 5)))
# L: created | WEB slices for the check_web_quotes vectors, cut from Dan_web_clean.txt at run time
import re  # noqa: E402
WEBT, _ch = {}, None
for _line in (HERE.parent / "Dan_web_clean.txt").read_text(encoding="utf-8").splitlines():
    _m = re.match(r"^===== DAN (\d+) =====$", _line)
    if _m:
        _ch = int(_m.group(1))
        continue
    _m = re.match(r"^\[v\] (\d+) (.*)$", _line)
    if _m and _ch:
        WEBT[(_ch, int(_m.group(1)))] = _m.group(2)
WQ_PLAIN_REF = next(k for k, t in sorted(WEBT.items()) if k[0] >= 2 and "[fn]" not in t and not re.search("[“”‘’]", t))
WQ_PLAIN = " ".join(WEBT[WQ_PLAIN_REF].split(" ")[:6]).rstrip(",;:.")
WQ_APOS_REF = next(k for k, t in sorted(WEBT.items()) if "’s " in t and "[fn]" not in t and not re.search("[“”‘]", t))
_w = WEBT[WQ_APOS_REF].split(" ")
_j = next(i for i, x in enumerate(_w) if "’s" in x)
WQ_APOS = " ".join(_w[max(0, _j - 1):_j + 3]).rstrip(",;:.")
check("fixture: WEB slices come from Dan_web_clean.txt, one [v] line per WEB verse, and each slice stands in its verse",
      len(WEBT) == sum(LAST_VERSE.values()) and WQ_PLAIN in WEBT[WQ_PLAIN_REF] and WQ_APOS in WEBT[WQ_APOS_REF],
      [len(WEBT), WQ_PLAIN_REF, WQ_APOS_REF])
S10B_CS_REFS = [
    # L: ported=same | re-pointed to MT 2:10; the accent-stripped Qere is derived, not typed
    ("cs_tf2b_s1_06_accent_stripped_qere_in_ref",
     ["oshb:Dan.2.10 (K/Q, checked before quoting: qere %s)" % Q72b_STRIPPED], "does not collate against its own ref"),
    ("cs_tf2b_s1_06_raw_qere_in_ref_ok", ["oshb:Dan.2.10 (K/Q: qere %s)" % Q72b], None),
    ("cs_tf2b_s1_06_undisclosed_qere_in_ref", ["oshb:Dan.2.10 (the reading %s)" % Q72b], "matches the Qere of its own ref"),
    # L: ported=same
    ("cs_tf2b_s1_06_own_verse_words_ok", ["oshb:Dan.1.1 (%s %s)" % (W11b[1], W11b[2])], None),
    ("cs_tf2b_s1_06_other_verse_words", ["oshb:Dan.1.1 (%s)" % OTHER12b], "does not collate against its own ref"),
    ("cs_tf2b_s1_06_named_other_ref_does_not_rebind", ["oshb:Dan.1.1 (cf. oshb:Dan.1.2 %s)" % OTHER12b], "does not collate against its own ref"),
]
S10B_CS_PROSE = [
    ("cs_tf2b_s1_07_cut_at_word_end", "the splice %s (oshb:%s) closes the unit" % (C10["end"][2], C10["end"][0]), "does not collate against any nearby cited ref"),
    ("cs_tf2b_s1_07_cut_at_word_start", "the splice %s (oshb:%s) closes the unit" % (C10["start"][2], C10["start"][0]), "does not collate against any nearby cited ref"),
    ("cs_tf2b_s1_07_root_inside_word", "the root %s (oshb:%s) recurs" % (C10["root"][2], C10["root"][0]), "does not collate against any nearby cited ref"),
    ("cs_tf2b_s1_07_whole_word_ok", "the splice %s (oshb:%s) closes the unit" % (C10["end"][1], C10["end"][0]), None),
]
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
S10B_CM = [
    # L: ported=same | the source's MT 1:28 re-pointed to MT 3:12 (SAMEKH), MT 33:16 to MT 9:5, MT 40:1-4 to MT 8:1-4
    ("cm_tf2b_s1_22_cv_form_own_clause_ok",
     {"boundary_rationale": "a setumah is recorded after 3:12; the unit then turns at oshb:Dan.3.%d" % UNMARKED1}, {"paragraph_mark_claim": False}),
    ("cm_tf2b_s1_22_mt_form_type_mismatch_flags", {"boundary_rationale": "a petuchah is recorded after MT 3:12"}, {"paragraph_mark_claim": True}),
    ("cm_tf2b_s1_22_absence_named_unmarked_verse_ok",
     {"boundary_rationale": "no setumah stands after 3:%d" % UNMARKED1, "span": "Dan.3.1-Dan.3.12"}, {"false_mark_absence_claim": False}),
    ("cm_tf2b_s1_22_absence_named_marked_verse_flags",
     {"boundary_rationale": "no setumah stands after 3:12", "span": "Dan.3.1-Dan.3.13"}, {"false_mark_absence_claim": True}),
    # L: created | the span above runs one verse past 3:12 because the installed Dan check_marks drops the row's own last
    # verse from a named absence claim (MARKS-3D, the close seam); this vector pins that drop
    ("cm_dan_s1_22_absence_named_close_seam_ok",
     {"boundary_rationale": "no setumah stands after 3:12", "span": "Dan.3.1-Dan.3.12"}, {"false_mark_absence_claim": False}),
    ("cm_tf2b_s1_22_absence_chapter_named_ok",
     {"boundary_rationale": "chapter %s carries no parashah mark" % NOMARK_CH,
      "span": "Dan.%s.1-Dan.%s.%s" % (NOMARK_CH, NEXT_MARK[0] if NEXT_MARK else 0, NEXT_MARK[1] if NEXT_MARK else 0)}, {"false_mark_absence_claim": False}),
    ("cm_tf2b_s1_22_negated_kq_near_dotted_ref_ok",
     {"boundary_rationale": "No K/Q or editorial note touches oshb:Dan.8.1-4", "span": "Dan.8.1-Dan.8.4"},
     {"kq_claim": False, "false_kq_absence_claim": False}),
    ("cm_tf2b_s1_22_negated_kq_named_verse_flags", {"boundary_rationale": "no K/Q stands at 9:5"}, {"false_kq_absence_claim": True}),
    ("cm_tf2b_s1_22_kq_claim_cv_form_flags", {"boundary_rationale": "the qere at 3:%d is disclosed" % UNMARKED1}, {"kq_claim": True}),
]
with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "tf2b_cs.jsonl"
    p.write_text("\n".join([json.dumps({"decision_id": d, "boundary_evidence_refs": refs}, ensure_ascii=False) for d, refs, _ in S10B_CS_REFS]
                           + [json.dumps({"decision_id": d, "boundary_rationale": prose}, ensure_ascii=False) for d, prose, _ in S10B_CS_PROSE]),
                 encoding="utf-8")
    rep = run("citation_sweep.py", p)
    for did, _, expect in S10B_CS_REFS + S10B_CS_PROSE:
        mine = [x for x in rep["problems"] if x.startswith(did + ":")]
        check("citation_sweep %s: %s" % (did, "no problem" if expect is None else repr(expect)),
              (not mine) if expect is None else any(expect in x for x in mine), mine)
    for label, payload, want in (("normalize tf2b S1-07: a run cut at its word's end is a defect", {"a": "x %s y" % C10["end"][2]}, 1),
                                 ("normalize tf2b S1-07: a run cut at its word's start is a defect", {"b": "x %s y" % C10["start"][2]}, 1),
                                 ("normalize tf2b S1-07: an unpointed root inside a word is a defect", {"c": "x %s y" % C10["root"][2]}, 1),
                                 ("normalize tf2b S1-07: the whole word stays byte-true", {"d": "x %s y" % C10["end"][1]}, 0)):
        fp = Path(td) / ("tf2b_norm_%s.json" % list(payload)[0])
        fp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        proc = subprocess.run([sys.executable, str(HERE / "normalize_hebrew_in_json.py"), str(fp)],
                              capture_output=True, text=True, encoding="utf-8", env=ENV)
        nrep = json.loads(proc.stdout.strip().splitlines()[-1])
        check(label, nrep["defect_count"] == want, nrep)
    p = Path(td) / "tf2b_reg.jsonl"
    p.write_text("\n".join(json.dumps(dict({"decision_id": d}, **fields), ensure_ascii=False) for d, fields, _ in S10B_REG), encoding="utf-8")
    rep = run("check_register.py", p)
    for d, _, cls in S10B_REG:
        mine = [fl for fl in rep["flags"] if fl.get("decision_id") == d]
        check("check_register %s: %s" % (d, cls or "no flag of any class"), (not mine) if cls is None else any(fl.get("class") == cls for fl in mine), mine)
    # L: ported=same | the source vectors quoted the source book's WEB; these quote Dan's WEB, sliced at run time
    p = Path(td) / "tf2b_wq.jsonl"
    p.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in (
        {"decision_id": "wq_tf2b_s1_10_unequal", "boundary_rationale": "“%s (web:Dan.%d.%d)." % ((WQ_PLAIN,) + WQ_PLAIN_REF)},
        {"decision_id": "wq_tf2b_s1_10_balanced_ok", "boundary_rationale": "“%s” (web:Dan.%d.%d)." % ((WQ_PLAIN,) + WQ_PLAIN_REF)},
        {"decision_id": "wq_tf2b_s1_10_apostrophes_ok", "boundary_rationale": "%s (web:Dan.%d.%d)." % ((WQ_APOS,) + WQ_APOS_REF)})),
        encoding="utf-8")
    rep = run("check_web_quotes.py", p)
    for d, fires in (("wq_tf2b_s1_10_unequal", True), ("wq_tf2b_s1_10_balanced_ok", False), ("wq_tf2b_s1_10_apostrophes_ok", False)):
        mine = [fl for fl in rep["flags"] if "e15d" in str(fl.get("issue")) and fl.get("decision_id") == d]
        check("check_web_quotes %s: e15d %s" % (d, "fires" if fires else "silent"), bool(mine) == fires, rep["flags"])
    p = Path(td) / "tf2b_cm.jsonl"
    p.write_text("\n".join(json.dumps(dict({"decision_id": d}, **f), ensure_ascii=False) for d, f, _ in S10B_CM), encoding="utf-8")
    rep = run("check_marks.py", p)
    for d, _, expect in S10B_CM:
        for rule, fires in expect.items():
            mine = [fl for fl in rep["flags"] if fl.get("decision_id") == d and fl.get("rule") == rule]
            check("check_marks %s: %s %s" % (d, rule, "fires" if fires else "silent"), bool(mine) == fires, mine)

# 10c. TOOLFIX-2 re-stage per ezek_controlling_rulings_a1#e5 (NEWCLASS-TF2-1, FLAGS-TF2-1, REG-TF2-1). Every Hebrew form
# is derived from the verse bytes at run time and never typed.


def _let10c(s):
    return "".join(ch for ch in s if _lt10(ch))


# L: ported | the source's MT 12:20 / 17:12 pair re-pointed to MT 1:1 / 7:27, found by code over the bytes
W1220C = [w for w in OSHB["Dan.1.1"].split(" ")
          if len(_let10c(w)) >= 5 and any(_let10c(w)[1:] == _let10c(x) for x in OSHB["Dan.7.27"].split(" "))]
check("fixture 10c: exactly one MT 1:1 word is a whole MT 7:27 word plus one leading letter", len(W1220C) == 1, W1220C)
WHOLE10C = _let10c(W1220C[0]) if W1220C else ""
BARE10C = WHOLE10C[1:]
S10C_CS_PROSE = [
    # L: ported=same | re-pointed to MT 1:1 / 7:27
    ("cs_e5_nc_proclitic_stripped_label_refused", "the %s recognition family (oshb:Dan.1.1)" % BARE10C,
     "does not collate against any nearby cited ref"),
    ("cs_e5_nc_whole_word_label_ok", "the %s recognition family (oshb:Dan.1.1)" % WHOLE10C, None),
    ("cs_e5_nc_bare_form_at_bare_verse_ok", "the %s form (oshb:Dan.7.27)" % BARE10C, None),
]
S10C_REG = [
    # L: ported=same | the source's range numbers re-pointed to Dan ranges that exist (9:24-26, 11.1-45, a 45-verse row)
    ("reg_e5_prior_range_reading", {"device_notes": "keeping the prior 9:24-26 reading"}, "author_wave_register_s1_05"),
    ("reg_e5_former_hyphenated_span", {"device_notes": "its former nineteen-verse span"}, "author_wave_register_s1_05"),
    ("reg_e5_former_two_words_span", {"device_notes": "the former single 11.1-45 span"}, "author_wave_register_s1_05"),
    ("reg_e5_last_of_underscored_rows", {"device_notes": "the last of three land_allotment rows"}, "author_wave_register_s1_05"),
    ("reg_e5_previously_held_as", {"device_notes": "ground previously held as one 45-verse row"}, "author_wave_register_s1_05"),
    ("reg_e5_green_former_kings_ok", {"device_notes": "the former kings"}, None),
    ("reg_e5_green_last_of_the_gates_ok", {"device_notes": "the last of the gates"}, None),
    ("reg_e5_green_rows_of_chambers_ok", {"device_notes": "one of three rows of chambers"}, None),
    ("reg_e5_green_previously_held_by_ok", {"device_notes": "the land previously held by Judah"}, None),
    ("reg_e5_green_prior_verse_ok", {"device_notes": "the prior verse"}, None),
]
S10C_CM = [
    # L: ported=same | re-pointed: PE at MT 5:12 before MT 5:13; no mark at MT 1:3-10; PE at the chapter end MT 8:27
    # before MT 9:1; one K/Q in WEB 2:10-16 (MT 2:10) and in WEB 1:1-7 (MT 1:4); MT 1:5-7 clean of every device
    ("cm_e5_w1_mark_before_onset_ok", {"boundary_rationale": "a petuchah closes the row immediately before the fresh word-event at oshb:Dan.5.13",
                                       "span": "Dan.5.9-Dan.5.12"}, [("paragraph_mark_claim", False)]),
    ("cm_e5_w1_no_mark_at_n_or_n_minus_1_flags", {"boundary_rationale": "a petuchah follows oshb:Dan.1.10"}, [("paragraph_mark_claim", True)]),
    ("cm_e5_w1_type_never_conflated_flags", {"boundary_rationale": "a setumah closes the row immediately before oshb:Dan.5.13"},
     [("paragraph_mark_claim", True)]),
    ("cm_e5_w1_chapter_crossing_ok", {"boundary_rationale": "a petuchah closes the preceding row immediately before the fresh word-event at oshb:Dan.9.1"},
     [("paragraph_mark_claim", False)]),
    ("cm_e5_w2_adjacent_negator_flags", {"device_notes": "No K/Q note touches this span", "span": "Dan.2.10-Dan.2.16"},
     [("false_kq_absence_claim", ("keys", ["Dan.2.10"]))]),
    ("cm_e5_w2_distant_negator_silent", {"boundary_rationale": "a boundary is never argued from any of these Qere readings", "span": "Dan.9.4-Dan.9.19"},
     [("false_kq_absence_claim", False), ("kq_claim", False)]),
    ("cm_e5_w2_two_words_between_silent", {"boundary_rationale": "not the whole-verse ketiv/qere concatenation", "span": "Dan.7.10-Dan.7.27"},
     [("false_kq_absence_claim", False), ("kq_claim", False)]),
    ("cm_e5_w2_no_other_undisclosed_flags", {"device_notes": "no other K/Q note touches this row", "span": "Dan.1.1-Dan.1.7"},
     [("false_kq_absence_claim", ("keys", ["Dan.1.4"]))]),
    ("cm_e5_w2_no_other_disclosed_silent", {"boundary_rationale": "the K/Q at 1:4 is a form variant", "device_notes": "no other K/Q note touches this row",
                                            "span": "Dan.1.1-Dan.1.7"}, [("false_kq_absence_claim", False), ("kq_claim", False)]),
    ("cm_e5_w5_negator_heads_list_ok", {"boundary_rationale": "No parashah, K/Q or editorial note touches 1:5-1:7", "span": "Dan.1.5-Dan.1.7"},
     [("kq_claim", False), ("false_kq_absence_claim", False)]),
    ("cm_e5_w5_negator_heads_list_flags", {"boundary_rationale": "No parashah, K/Q or editorial note touches 2:10-2:16", "span": "Dan.2.10-Dan.2.16"},
     [("false_kq_absence_claim", True)]),
    ("cm_e5_w5_clause_not_a_list_flags", {"boundary_rationale": "No parashah stands here, K/Q at 3:%d is disclosed" % UNMARKED1}, [("kq_claim", True)]),
    ("cm_e5_w6_no_pe_or_samekh_true_silent", {"boundary_rationale": "the close has no Masoretic mark at all (no pe or samekh follows 1:10)",
                                              "span": "Dan.1.4-Dan.1.10"},
     [("paragraph_mark_claim", False), ("false_mark_absence_claim", ("no_scope", "named_interior"))]),
    # the installed Dan check_marks labels every named mark-absence scope 'named_interior' (MARKS-3D); 'named' is its K/Q label
    ("cm_e5_w6_no_samekh_false_flags", {"boundary_rationale": "no samekh mark follows 3:12"}, [("false_mark_absence_claim", ("scope", "named_interior"))]),
]


def _cm10c_ok(mine, want):
    if want is True:
        return bool(mine)
    if want is False:
        return not mine
    kind, val = want
    if kind == "keys":
        return any(fl.get("kq_mt_keys") == val for fl in mine)
    if kind == "scope":
        return any(fl.get("scope") == val for fl in mine)
    return not any(fl.get("scope") == val for fl in mine)


with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "tf2c_cs.jsonl"
    p.write_text("\n".join(json.dumps({"decision_id": d, "boundary_rationale": prose}, ensure_ascii=False) for d, prose, _ in S10C_CS_PROSE),
                 encoding="utf-8")
    rep = run("citation_sweep.py", p)
    for did, _, expect in S10C_CS_PROSE:
        mine = [x for x in rep["problems"] if x.startswith(did + ":")]
        check("citation_sweep %s: %s" % (did, "no problem" if expect is None else repr(expect)),
              (not mine) if expect is None else any(expect in x for x in mine), mine)
    p = Path(td) / "tf2c_reg.jsonl"
    p.write_text("\n".join(json.dumps(dict({"decision_id": d}, **fields), ensure_ascii=False) for d, fields, _ in S10C_REG), encoding="utf-8")
    rep = run("check_register.py", p)
    for d, _, cls in S10C_REG:
        mine = [fl for fl in rep["flags"] if fl.get("decision_id") == d]
        check("check_register %s: %s" % (d, cls or "no flag of any class"), (not mine) if cls is None else any(fl.get("class") == cls for fl in mine), mine)
    p = Path(td) / "tf2c_cm.jsonl"
    p.write_text("\n".join(json.dumps(dict({"decision_id": d}, **f), ensure_ascii=False) for d, f, _ in S10C_CM), encoding="utf-8")
    rep = run("check_marks.py", p)
    for d, _, expects in S10C_CM:
        for rule, want in expects:
            mine = [fl for fl in rep["flags"] if fl.get("decision_id") == d and fl.get("rule") == rule]
            check("check_marks %s: %s %s" % (d, rule, ("fires" if want else "silent") if isinstance(want, bool) else "%s=%s" % want),
                  _cm10c_ok(mine, want), mine)

failed = [r for r in results if not r["ok"]]
print(json.dumps({"checks": len(results), "passed": len(results) - len(failed), "failed": failed,
                  "verdict": "GREEN" if not failed else "RED"}, ensure_ascii=False, indent=1))
raise SystemExit(1 if failed else 0)
