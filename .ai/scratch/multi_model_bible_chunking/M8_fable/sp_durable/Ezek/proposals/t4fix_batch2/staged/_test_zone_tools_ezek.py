#!/usr/bin/env python3
"""Exhaustive and adversarial tests for the Ezek-specific arms of citation_sweep.py and check_marks.py.

1. PROPERTY (exhaustive): citation_sweep's zone predicates flag a verse if and only if the crosswalk moves it. Every
   WEB verse and every MT verse is tested against ezek_lib, so the predicates cannot drift from the verified map.
2. VECTORS: one fixture row per behaviour, run through each tool as a subprocess exactly as the suite runs it. Each
   vector asserts the presence or the absence of its own finding, matched by decision_id.
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
from ezek_lib import LAST_VERSE, MT_LAST_VERSE, mt_to_web, web_to_mt  # noqa: E402
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

# (decision_id, boundary_evidence_refs, expected problem substring or None for "no problem at all")
CS_VECTORS = [
    ("cs_puncta_41_20_ok", ["web:Ezek.41.20-Ezek.41.20 puncta extraordinaria (single-witness)"], None),
    ("cs_puncta_46_22_ok", ["oshb:Ezek.46.22-Ezek.46.22 puncta extraordinaria (single-witness)"], None),
    ("cs_puncta_40_20_bad", ["web:Ezek.40.20-Ezek.40.20 puncta extraordinaria (single-witness)"], "claims puncta extraordinaria"),
    ("cs_zone_bare_web_21_3", ["web:Ezek.21.3-Ezek.21.3"], "offset-zone ref lacks"),
    ("cs_zone_bare_web_20_45", ["web:Ezek.20.45-Ezek.20.45"], "offset-zone ref lacks"),
    ("cs_zone_bare_mt_21_8", ["oshb:Ezek.21.8-Ezek.21.8"], "offset-zone ref lacks"),
    ("cs_edge_web_20_44_ok", ["web:Ezek.20.44-Ezek.20.44"], None),
    ("cs_edge_web_22_1_ok", ["web:Ezek.22.1-Ezek.22.1"], None),
    ("cs_dual_ok", ["web:Ezek.21.3-Ezek.21.3 = oshb:Ezek.21.8"], None),
    ("cs_dual_bad", ["web:Ezek.21.3-Ezek.21.3 = oshb:Ezek.21.3"], "dual-cite arithmetic wrong"),
    ("cs_mt_qualifier_ok", ["web:Ezek.20.47-Ezek.20.47 (MT 21:3)"], None),
    ("cs_oshb_20_49_out_of_range", ["oshb:Ezek.20.49-Ezek.20.49"], "out of range for OSHB"),
    ("cs_small_letter", ["web:Ezek.1.1-Ezek.1.1 small nun (single-witness)"], "NO special-letter segs of any class"),
    ("cs_large_letter", ["web:Ezek.1.1-Ezek.1.1 large letter (single-witness)"], "NO special-letter segs of any class"),
    ("cs_qumran_siglum", ["web:Ezek.1.1-Ezek.1.1 per 4QEzek"], "cross-tradition material"),
    ("cs_masada_siglum", ["web:Ezek.1.1-Ezek.1.1 per MasEzek"], "cross-tradition material"),
    ("cs_selah", ["web:Ezek.1.1-Ezek.1.1 selah"], "NO selah exists"),
    ("cs_kq_in_zone_ok", ["oshb:Ezek.21.28-Ezek.21.28 = web:Ezek.21.23 ketiv/qere"], None),
]

# (decision_id, prose, rule id, expect the rule to fire)
CM_VECTORS = [
    ("cm_puncta_41_20_ok", "the puncta extraordinaria in oshb:Ezek.41.20 are a byte feature", "puncta_claim_in_ezek", False),
    ("cm_puncta_46_22_ok", "puncta extraordinaria at web:Ezek.46.22", "puncta_claim_in_ezek", False),
    ("cm_puncta_41_21_bad", "puncta extraordinaria at oshb:Ezek.41.21", "puncta_claim_in_ezek", True),
    ("cm_small_letter", "a small nun at oshb:Ezek.1.1", "small_letter_claim_in_jer", True),
    ("cm_selah", "selah at oshb:Ezek.1.1", "selah_claim_in_jer", True),
    ("cm_mark_type_ok", "a setumah follows oshb:Ezek.1.28", "paragraph_mark_claim", False),
    ("cm_mark_type_bad", "a petuchah follows oshb:Ezek.1.28", "paragraph_mark_claim", True),
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
# run time (never typed): MT 1:8's first note, split by kq_split.
from ezek_lib import kq_split, kq_split_bytes, load_pmarks  # noqa: E402

PM = load_pmarks()
OSHB = dict(l.split("\t", 1) for l in (HERE.parent / "Ezek_oshb.txt").read_text(encoding="utf-8").splitlines() if "\t" in l)
# D3: fixtures carry the Qere in the note's RAW bytes, which is what a correct row quotes and what the tools compare
QERE = kq_split_bytes(PM["kq"]["Ezek.1.8"][0], OSHB["Ezek.1.8"])[1].replace("/", "")
check("fixture: the MT 1:8 Qere is pointed and absent from the verse bytes, so the Qere tier is what gets tested",
      bool(QERE) and QERE not in OSHB["Ezek.1.8"], QERE)
FIRST = OSHB["Ezek.1.1"].split(" ")[0]
HEB_VECTORS = [
    ("cs_qere_disclosed_ok", "the Qere %s at oshb:Ezek.1.8 (ketiv/qere, single-witness)" % QERE, None),
    ("cs_qere_undisclosed", "the reading %s at oshb:Ezek.1.8" % QERE, "matches the Qere"),
    ("cs_verse_quote_ok", "%s opens oshb:Ezek.1.1" % FIRST, None),
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

# 4. REGRESSION - the first puncta arms flagged all 12 puncta mentions in the real rows, every one wrongly: negated
# disclosures ("no puncta ... inside this span") and correct disclosures citing a bare "41:20" or "46.22".
PUNCTA2_CS = [
    ("cs_puncta_negated_ok", ["web:Ezek.40.5-Ezek.40.5 (no puncta here)"], None),
    ("cs_puncta_denied_at_site", ["oshb:Ezek.41.20-Ezek.41.20 (no puncta)"], "denies puncta extraordinaria"),
    ("cs_puncta_range_ok", ["web:Ezek.41.1-Ezek.41.26 (puncta at 41:20, single-witness)"], None),
    # editorial-note tier: MT 3:20 carries an OSHB note on a ketib/qere relative to BHS; MT 5:2 carries nothing
    ("cs_kq_editorial_note_ok",
     ["oshb:Ezek.3.20-Ezek.3.20 (OSHB editorial note, single-witness: a ketiv/qere read with L against BHS)"], None),
    ("cs_kq_none_bad", ["oshb:Ezek.5.2-Ezek.5.2 (ketiv/qere, single-witness)"], "kq inventory has none"),
]
PUNCTA2_CM = [
    ("cm_puncta_negated_ok", "No K/Q, no paseq, no puncta and no zone-dual issue touches this span.",
     "Ezek.33.1-Ezek.33.20", {"puncta_claim_in_ezek": False, "false_puncta_absence_claim": False}),
    ("cm_puncta_absence_false", "No editorial note and no puncta extraordinaria fall inside this span.",
     "Ezek.41.15-Ezek.41.26", {"false_puncta_absence_claim": True, "puncta_claim_in_ezek": False}),
    ("cm_puncta_bare_number_ok", "Puncta extraordinaria disclosed at 41:20, single witness.", None,
     {"puncta_claim_in_ezek": False}),
    ("cm_puncta_dotted_number_ok", "MT 46.22 carries seven U+05C4 puncta-extraordinaria combining marks.", None,
     {"puncta_claim_in_ezek": False}),
    ("cm_kq_editorial_note_ok", "the editorial note at oshb:Ezek.3.20 records a ketiv/qere relative to BHS", None,
     {"kq_claim": False}),
    ("cm_kq_none_bad", "a ketiv/qere at oshb:Ezek.5.2", None, {"kq_claim": True}),
    # second-round regressions, both from the real rows: a distant "not" is no negation (P11-009), and a span
    # covering the site satisfies a positive claim whose number sits outside the window (P10-008)
    ("cm_puncta_distant_not_ok",
     "that is source-true, not degradation, and the NFD arm must treat U+05C4 as a legitimate combining mark.",
     "Ezek.46.19-Ezek.46.24", {"false_puncta_absence_claim": False, "puncta_claim_in_ezek": False}),
    ("cm_puncta_span_covers_site_ok", "five instances of the upper dot U+05C4, disclosed here single-witness",
     "Ezek.41.12-Ezek.41.20", {"puncta_claim_in_ezek": False}),
    ("cm_puncta_no_site_still_flags", "five instances of the upper dot U+05C4, disclosed here single-witness",
     "Ezek.40.1-Ezek.40.4", {"puncta_claim_in_ezek": True}),
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
# direct counterpart, so a later edit cannot quietly reopen what the review closed.
QERE2 = kq_split_bytes(PM["kq"]["Ezek.3.15"][0], OSHB["Ezek.3.15"])[1].replace("/", "")
check("fixture: MT 3:15 Qere differs from MT 1:8 Qere", bool(QERE2) and QERE2 != QERE and QERE2 not in OSHB["Ezek.3.15"], QERE2)
T1_CS = [
    ("cs_t1_01_wrong_number_in_covering_range", ["web:Ezek.41.1-Ezek.41.26 (puncta at 41:5, single-witness)"],
     "claims puncta extraordinaria"),
    ("cs_t1_03_double_negation_asserts_presence_ok", ["oshb:Ezek.41.20-Ezek.41.20 (not without puncta, single-witness)"], None),
    ("cs_negation_naming_a_site_fails", ["web:Ezek.41.1-Ezek.41.26 (no puncta at 41:20)"], "denies puncta extraordinaria"),
]
T1_CM = [
    ("cm_t1_02_wrong_number_span_covers_site", "the puncta extraordinaria sit at 41:5 in this span",
     "Ezek.41.12-Ezek.41.20", {"puncta_claim_in_ezek": True}),
    ("cm_t1_03_double_negation_ok", "this span is not without puncta extraordinaria at 41:20",
     "Ezek.41.12-Ezek.41.20", {"false_puncta_absence_claim": False, "puncta_claim_in_ezek": False}),
    ("cm_real_row_distant_next_verse_number_ok",
     "the word carrying the book's puncta extraordinaria -- five instances of the upper dot U+05C4, disclosed here "
     "single-witness -- a natural summary line before 41:21 returns to the measurements",
     "Ezek.41.12-Ezek.41.20", {"puncta_claim_in_ezek": False}),
]
T1_HEB = [
    # T1-04: the disclosure keyword must stand near THIS run, not merely somewhere in the field
    ("cs_t1_04_second_qere_rides_on_distant_disclosure",
     "the Qere %s at oshb:Ezek.1.8 (ketiv/qere, single-witness). %s The reading %s at oshb:Ezek.3.15."
     % (QERE, "Unrelated prose follows here to push the second quote far from the first disclosure keyword. " * 3, QERE2),
     "matches the Qere at oshb:Ezek.3.15"),
    # hard_gate 'unclear': a Qere cited at the WRONG verse is refused per verse by citation_sweep
    ("cs_qere_cited_at_wrong_verse_refused", "the Qere %s at oshb:Ezek.3.15 (ketiv/qere, single-witness)" % QERE,
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
    fp.write_text(json.dumps({"a": "x %s at oshb:Ezek.3.15" % QERE}, ensure_ascii=False), encoding="utf-8")
    proc = subprocess.run([sys.executable, str(HERE / "normalize_hebrew_in_json.py"), str(fp)],
                          capture_output=True, text=True, encoding="utf-8", env=ENV)
    nrep = json.loads(proc.stdout.strip().splitlines()[-1])
    check("normalize: the Qere tier is book-wide by design (per-verse binding is citation_sweep's, proven above)",
          nrep["defect_count"] == 0 and nrep.get("qere") == 1, nrep)

# 6. T2 REVIEW REGRESSIONS (ezek_toolkit_repair_review_t2_a1#e1) and D3 (raw note bytes) - the reviewer's own attacks,
# both directions, plus the non-canonical-note case T2 could not construct.
import unicodedata  # noqa: E402
from ezek_lib import kq_split_bytes  # noqa: E402

T2_CS = [
    ("cs_t2_01_decoy_site_number", ["web:Ezek.41.1-Ezek.41.26 (cf. 41:20; but the true puncta claim here is verse 41:5, single-witness)"],
     "claims puncta extraordinaria"),
    ("cs_t2_02_true_claim_near_nonsite_ok", ["web:Ezek.41.1-Ezek.41.26 (41:19 nearby; puncta extraordinaria stand at 41:20, single-witness)"], None),
    ("cs_t2_02_range_holding_site_ok", ["web:Ezek.41.1-Ezek.41.26 (puncta extraordinaria across 41:18-41:20, single-witness)"], None),
    ("cs_t2_03_distant_negation_denial", ["web:Ezek.41.1-Ezek.41.26 (the text absolutely does not under any reading carry puncta extraordinaria at 41:20, single-witness)"],
     "denies puncta extraordinaria"),
    ("cs_t2_05_mt_phrase_is_not_a_qualifier_ok", ["web:Ezek.5.2-Ezek.5.2 (MT 46.22 puncta extraordinaria, single-witness)"], None),
    ("cs_mixed_site_and_nonsite_ambiguous", ["web:Ezek.41.1-Ezek.41.26 (puncta extraordinaria at 41:20 and 41:21, single-witness)"], "ambiguous"),
]
T2_CM = [
    ("cm_t2_01_decoy_site_number", "cf. 41:20; but the true puncta claim here is verse 41:5", "Ezek.5.1-Ezek.5.4",
     {"puncta_claim_in_ezek": True}),
    ("cm_t2_03_distant_negation", "the text absolutely does not under any reading carry puncta extraordinaria at 41:20",
     "Ezek.41.12-Ezek.41.20", {"false_puncta_absence_claim": True}),
    ("cm_t2_02_true_claim_near_nonsite_ok", "41:19 nearby; puncta extraordinaria stand at 41:20", "Ezek.41.12-Ezek.41.20",
     {"puncta_claim_in_ezek": False, "false_puncta_absence_claim": False}),
]
NONCANON = next((ref, n) for ref, ns in PM["kq"].items() for n in ns
                if n != unicodedata.normalize("NFC", n) and kq_split_bytes(n, OSHB[ref])[1])
RAWQ = kq_split_bytes(NONCANON[1], OSHB[NONCANON[0]])[1].replace("/", "")
NFDQ = unicodedata.normalize("NFD", RAWQ)
check("fixture: a non-canonical note's raw Qere differs from its NFD form", RAWQ != NFDQ, NONCANON[0])
REF_NC = "oshb:" + NONCANON[0]
T2_HEB = [
    ("cs_t2_04_short_gap_second_qere", "the Qere %s at oshb:Ezek.1.8 (ketiv/qere, single-witness). A short gap. The reading %s at oshb:Ezek.3.15."
     % (QERE, QERE2), "matches the Qere at oshb:Ezek.3.15"),
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

# 7. CALENDAR-DATE arm (strategy section 10 as clarified by ruling G12(d); T1 widened scope item 2). The constants are
# asserted against the device inventory; then one fixture row per behaviour: row onsets, prose claims, ref annotations.
INV = json.loads((HERE.parent / "ezek_device_inventory.json").read_text(encoding="utf-8"))


def _pairs(keys):
    return {tuple(int(x) for x in k.split(".")[1:]) for k in keys}


check("calendar constants: CAL_DATE_PAIRS == inventory calendar_dates_not_datelines (4)",
      cs.CAL_DATE_PAIRS == _pairs(INV["calendar_dates_not_datelines"]["verses_mt"]) and len(cs.CAL_DATE_PAIRS) == 4,
      sorted(cs.CAL_DATE_PAIRS))
check("calendar constants: DATELINE_PAIRS == inventory dated_oracles (14)",
      cs.DATELINE_PAIRS == _pairs(INV["dated_oracles"]["verses_mt"]) and len(cs.DATELINE_PAIRS) == 14, sorted(cs.DATELINE_PAIRS))
check("calendar constants: 45:18 is the one calendar date a row may open on", cs.CAL_DATE_PAIRS - cs.CAL_NO_ONSET == {(45, 18)})
CAL_ROWS = [
    ("cal_onset_45_18_ok", {"span": "Ezek.45.18-Ezek.45.25", "boundary_rationale":
                            "the onset is the messenger formula at oshb:Ezek.45.18 after the samekh at 45:17; the date clause is not a dateline"}, None),
    ("cal_onset_45_19_ok", {"span": "Ezek.45.19-Ezek.45.25"}, None),
    ("cal_onset_45_20_bad", {"span": "Ezek.45.20-Ezek.45.25"}, "row opens at a calendar date with no formula (MT 45:20)"),
    ("cal_onset_45_21_bad", {"span": "Ezek.45.21-Ezek.45.24"}, "row opens at a calendar date with no formula (MT 45:21)"),
    ("cal_onset_45_25_bad", {"span": "Ezek.45.25-Ezek.45.25"}, "row opens at a calendar date with no formula (MT 45:25)"),
    ("cal_prose_claim_45_18_bad", {"boundary_rationale": "the dateline at 45:18 opens the festival calendar"}, "claims a dateline at MT 45:18"),
    ("cal_prose_number_first_bad", {"boundary_rationale": "Ezek.45.20 is a dateline"}, "claims a dateline at MT 45:20"),
    ("cal_prose_list_bad", {"boundary_rationale": "datelines at 40:1, 45:21 and 45:25"}, "claims a dateline at MT 45:21, MT 45:25"),
    ("cal_prose_double_negation_bad", {"boundary_rationale": "45:25 is not without a dateline"}, "claims a dateline at MT 45:25"),
    ("cal_prose_negated_ok", {"boundary_rationale": "45:18 is not a dateline, having no year word"}, None),
    ("cal_prose_non_dateline_ok", {"boundary_rationale": "the non-dateline calendar date at 45.21"}, None),
    ("cal_prose_real_dateline_ok", {"boundary_rationale": "the dateline at 40:1 opens the vision"}, None),
    ("cal_prose_other_clause_ok", {"boundary_rationale": "unlike the dateline at 40:1, the date at 45:18 carries no year word"}, None),
    ("cal_prose_unnumbered_ok", {"boundary_rationale": "the date clause fails the book's structural dateline test"}, None),
    ("cal_ref_bare_claim_bad", {"boundary_evidence_refs": ["oshb:Ezek.45.25-Ezek.45.25 (dateline; single-witness)"]}, "claims a dateline at MT 45:25"),
    ("cal_ref_numbered_claim_bad", {"boundary_evidence_refs": ["web:Ezek.45.17-Ezek.45.25 (dateline at 45:21)"]}, "claims a dateline at MT 45:21"),
    ("cal_ref_denial_ok", {"boundary_evidence_refs": ["oshb:Ezek.45.18-Ezek.45.18 (disclosure: not a dateline (no year word), single-witness)"]}, None),
    ("cal_ref_real_dateline_ok", {"boundary_evidence_refs": ["oshb:Ezek.40.1-Ezek.40.1 (dateline; single-witness)"]}, None),
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
# because the real-row vector cm_real_row_distant_next_verse_number_ok (section 4) pins a TRUE claim against the next
# verse's number - an implementation deviation from order (2), recorded for T4 and the controlling agent. The apposition
# and parenthesis forms of a dateline claim now bind (RED). GREEN controls keep a prior-clause negator, 'nonetheless',
# 'not without', true sites, and the other clause.
R4II_CS = [
    ("cs_r4ii_novel_a_paren_nonsite", ["web:Ezek.41.1-Ezek.41.26 puncta extraordinaria (41:5)"], "claims puncta extraordinaria"),
    ("cs_r4ii_novel_a2_distant_nonsite",
     ["web:Ezek.41.1-Ezek.41.26 puncta extraordinaria are recorded in this measured span by the single witness, standing at verse 41:5"],
     "claims puncta extraordinaria"),
    ("cs_r4ii_paren_site_ok", ["web:Ezek.41.1-Ezek.41.26 puncta extraordinaria (41:20, single-witness)"], None),
    ("cs_r4ii_distant_site_ok",
     ["web:Ezek.41.1-Ezek.41.26 puncta extraordinaria are recorded in this measured span by the single witness, standing at verse 41:20"],
     None),
]
R4II_CM = [
    ("cm_r4ii_novel_a_prose_paren_nonsite", "the puncta extraordinaria (41:5)", "Ezek.41.12-Ezek.41.20", {"puncta_claim_in_ezek": True}),
    ("cm_r4ii_novel_f_paren_nonsite", "the puncta extraordinaria (five dots at 41:5)", "Ezek.41.12-Ezek.41.20", {"puncta_claim_in_ezek": True}),
    ("cm_r4ii_paren_site_ok", "the puncta extraordinaria (five dots at 41:20)", "Ezek.41.12-Ezek.41.20",
     {"puncta_claim_in_ezek": False, "false_puncta_absence_claim": False}),
    ("cm_r4ii_prior_clause_negator_ok", "no paseq stands at 41:5; the puncta extraordinaria at 41:20 are in the verse bytes",
     "Ezek.41.12-Ezek.41.20", {"puncta_claim_in_ezek": False, "false_puncta_absence_claim": False}),
    ("cm_r4ii_nonetheless_ok", "nonetheless the puncta extraordinaria stand at 41:20", "Ezek.41.12-Ezek.41.20",
     {"puncta_claim_in_ezek": False, "false_puncta_absence_claim": False}),
    ("cm_r4ii_not_without_ok", "this verse is not without puncta extraordinaria at 41:20", "Ezek.41.12-Ezek.41.20",
     {"puncta_claim_in_ezek": False, "false_puncta_absence_claim": False}),
]
CAL1_ROWS = [
    ("cal1_apposition_bad", {"boundary_rationale": "the onset stands at 45:18, a dateline-grade onset"}, "claims a dateline at MT 45:18"),
    ("cal1_parenthesis_bad", {"boundary_rationale": "the dateline (45:18) opens the festival paragraph"}, "claims a dateline at MT 45:18"),
    ("cal1_apposition_negated_ok", {"boundary_rationale": "the onset stands at 45:18, not a dateline"}, None),
    ("cal1_own_clause_number_ok", {"boundary_rationale": "the samekh follows 45:17, the dateline at 40:1 is far behind"}, None),
    ("cal1_other_clause_kept_ok", {"boundary_rationale": "unlike the dateline at 40:1, the date at 45:18 carries no year word"}, None),
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
# T4-04: a true puncta ref needs single-witness disclosure, hyphenated or spaced.
T4_CS = [
    ("cs_t4_01_decoy_letter_id_ok",
     ["web:Ezek.41.1-Ezek.41.26 puncta extraordinaria (cross-referenced at row R4.5 in the ledger), single-witness"], None),
    ("cs_t4_01_dotted_ezek_ref_still_binds", ["web:Ezek.41.1-Ezek.41.26 puncta extraordinaria (Ezek.41.5, single-witness)"],
     "claims puncta extraordinaria"),
    ("cs_t4_03_puncta_denial_after_nonsite_ok",
     ["web:Ezek.41.1-Ezek.41.10 puncta extraordinaria would be expected at 41:5 but none stands"], None),
    ("cs_t4_03_puncta_denial_after_at_site",
     ["oshb:Ezek.41.20-Ezek.41.20 puncta extraordinaria would be expected here but none stands"], "denies puncta extraordinaria"),
    ("cs_t4_04_site_without_disclosure", ["web:Ezek.41.1-Ezek.41.26 puncta extraordinaria (41:20)"], "lacks single-witness disclosure"),
    ("cs_t4_04_spaced_single_witness_ok", ["web:Ezek.41.1-Ezek.41.26 puncta extraordinaria at 41:20, single witness"], None),
]
T4_CAL_ROWS = [
    ("cal_t4_03_apposition_denial_ok", {"boundary_rationale": "the unit opens at 45:18, where a dateline would be expected but none stands"}, None),
    ("cal_t4_03_parenthesis_denial_ok", {"boundary_rationale": "the dateline (45:18) would be expected but none stands"}, None),
    ("cal_t4_03_absent_at_clause_end_ok", {"boundary_rationale": "a dateline at 45:18 is absent"}, None),
    ("cal_t4_03_bare_later_no_stays_red", {"boundary_rationale": "the dateline at 45:18 opens no new year"}, "claims a dateline at MT 45:18"),
    ("cal_t4_03_none_of_stays_red", {"boundary_rationale": "the dateline at 45:18 but none of the festival dates"}, "claims a dateline at MT 45:18"),
    ("cal_t4_03_missing_not_final_stays_red", {"boundary_rationale": "the dateline at 45:18 is missing its year word"},
     "claims a dateline at MT 45:18"),
    ("cal_t4_03_denial_behind_comma_residual_red", {"boundary_rationale": "a dateline at 45:18 would be expected, though none stands"},
     "claims a dateline at MT 45:18"),
]
T4_CM = [
    ("cm_t4_01_decoy_letter_id_ok", "the puncta extraordinaria (cross-referenced at row R4.5 in the ledger)", "Ezek.41.12-Ezek.41.20",
     {"puncta_claim_in_ezek": False, "false_puncta_absence_claim": False}),
    ("cm_t4_03_denial_after_nonsite_ok", "puncta extraordinaria would be expected at 41:5 but none stands", "Ezek.41.1-Ezek.41.10",
     {"puncta_claim_in_ezek": False, "false_puncta_absence_claim": False}),
    ("cm_t4_03_denial_after_at_site_flags", "puncta extraordinaria would be expected at 41:20 but none stands", "Ezek.41.12-Ezek.41.20",
     {"false_puncta_absence_claim": True, "puncta_claim_in_ezek": False}),
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
    ("cs_e4_a2_positive_then_denial_nonsite_red",
     ["web:Ezek.41.1-Ezek.41.26 puncta extraordinaria stand at 41:5 but none is present in ch 46, single-witness"], "claims puncta extraordinaria"),
    ("cs_e4_a2_positive_then_denial_site_ok",
     ["web:Ezek.41.1-Ezek.41.26 puncta extraordinaria stand at 41:20 but none is present at 41:21, single-witness"], None),
    ("cs_e4_a3_mark_spaced_single_witness_ok", ["oshb:Ezek.1.28-Ezek.1.28 samekh (single witness)"], None),
    ("cs_e4_a3_paseq_spaced_single_witness_ok", ["oshb:Ezek.3.27-Ezek.3.27 paseq (count-only, single witness)"], None),
]
E4_CAL = [
    ("cal_e4_a2_positive_then_denial_red", {"boundary_rationale": "a dateline stands at 45:18 but none stands at 45:20"},
     "claims a dateline at MT 45:18 - a calendar"),
    ("cal_e4_a2_true_then_denial_ok", {"boundary_rationale": "the dateline at 40:1 opens the vision but none stands at 45:18"}, None),
]
E4_CM = [
    ("cm_e4_a1_copular_denial_at_field_end_flags",
     {"boundary_rationale": "puncta extraordinaria are absent", "device_notes": "the span is otherwise unremarkable",
      "span": "Ezek.41.12-Ezek.41.20"}, {"false_puncta_absence_claim": True}),
    ("cm_e4_a2_positive_then_denial_nonsite_flags",
     {"boundary_rationale": "puncta extraordinaria stand at 41:5 but none is present in ch 46", "span": "Ezek.41.12-Ezek.41.20"},
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

failed = [r for r in results if not r["ok"]]
print(json.dumps({"checks": len(results), "passed": len(results) - len(failed), "failed": failed,
                  "verdict": "GREEN" if not failed else "RED"}, ensure_ascii=False, indent=1))
raise SystemExit(1 if failed else 0)
