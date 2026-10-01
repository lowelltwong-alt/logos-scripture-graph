#!/usr/bin/env python3
"""Phase-0 toolkit smoke test for Jer (orchestrator only; artifacts removed
after). THREE clean rows must pass every validator - one identity-zone row
with a front-seam PE + paseq disclosure, one OFFSET-ZONE row (WEB 9:1-9:2 =
MT 8:23-9:1, mandatory duals), one ARAMAIC-ISLAND row (10:11-10:12 with the
island + both SAMEKHs disclosed) - and three deliberately-bad rows must be
caught on EVERY planted defect class, including the zone arms and the NEW
Jer Tier-0 classes: E-15a/b/c (quote-pairing coverage), E-16 (exclusivity
never tier-dampened), E-01 (NFD-degraded = HARD), E-02 (whole-chapter cap),
and the register classes (E-06 + E-18 residual arms). Full 22-field schema
on every row; wj_or_red_letter_considered carries the mandated fixed
sentence (the p4 ngram7 exclusion class). A separate arm proves the
check_atomic_isolation machinery (verdict logic, crosswalk verse fetch
DISCRIMINATING crosswalk from identity via the ammi share at the WEB 9:1
seam, p3 guarded output path) BEFORE it can matter. Hebrew is byte-spliced
from verse_map_oshb.json (never hand-typed); English from verse_map_web.json."""
from __future__ import annotations

import importlib
import io
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SPBOOK = TOOLS.parent
oshb = json.loads((TOOLS / "verse_map_oshb.json").read_text(encoding="utf-8"))
web = json.loads((TOOLS / "verse_map_web.json").read_text(encoding="utf-8"))
pm = json.loads((SPBOOK / "pmarks_Jer.json").read_text(encoding="utf-8"))


def webtxt(ref):
    return re.sub(r"\[fn [^\]]*\]", " ", web[ref]["text"]).strip()


heb_2_4 = oshb["Jer.2.4"]["text"]                    # identity-zone verse
heb_8_23 = oshb["Jer.8.23"]["text"]                  # zone seam verse (= WEB 9:1)
heb_10_11 = oshb["Jer.10.11"]["text"]                # THE ARAMAIC ISLAND
heb_5_26 = oshb["Jer.5.26"]["text"]                  # wrong-ref fixture
heb_2_2 = oshb["Jer.2.2"]["text"]                    # NFD-degradation fixture
web_2_4 = webtxt("Jer.2.4")
web_9_1 = webtxt("Jer.9.1")
web_9_2 = webtxt("Jer.9.2")
web_9_4 = webtxt("Jer.9.4")
web_10_11 = webtxt("Jer.10.11")
web_5_28 = webtxt("Jer.5.28")

# preconditions for the rows below (fail loudly if the data moves)
assert pm["marks"].get("Jer.2.3") == ["PE"], "smoke precondition: PE at MT 2:3"
assert pm["marks"].get("Jer.5.29") == ["SAMEKH"], "smoke precondition: SAMEKH at MT 5:29"
assert pm["marks"].get("Jer.10.10") == ["SAMEKH"], "smoke precondition: SAMEKH at MT 10:10"
assert pm["marks"].get("Jer.10.11") == ["SAMEKH"], "smoke precondition: SAMEKH at MT 10:11"
for k in ("Jer.2.2", "Jer.2.4", "Jer.2.5", "Jer.5.24", "Jer.5.25", "Jer.5.26",
          "Jer.5.28", "Jer.5.30", "Jer.8.22", "Jer.8.23", "Jer.9.1", "Jer.10.12"):
    assert not pm["marks"].get(k), f"smoke precondition: {k} must be mark-free"
assert pm["paseq"].get("Jer.2.5") == 1, "smoke precondition: paseq at MT 2:5"
assert not pm["paseq"].get("Jer.5.30"), "smoke precondition: 5:30 paseq-free"
for k in ("Jer.2.2", "Jer.2.4", "Jer.2.5", "Jer.5.26", "Jer.5.28", "Jer.5.30",
          "Jer.8.23", "Jer.9.1", "Jer.10.11", "Jer.10.12"):
    assert not pm["kq"].get(k), f"smoke precondition: {k} must be K/Q-free"
assert list(pm["other_segs"]) == ["Jer.39.13"], "smoke precondition: the one x-small site"
assert web["Jer.10.11"]["language"] == "Aramaic", "smoke precondition: island marked"

COMMON = {
    "book": "Jer", "model_id": "M8_fable", "non_authorizing": True,
    "literature_type_guess": "prophetic_oracle", "confidence": "high",
    "strong_or_hebrew_tags_used": False,
    "wj_or_red_letter_considered": "not applicable in the OT substrate",
    "frontier_flag_considered": False, "review_status": "draft",
    "observed_substrate_signals": ["oracle_frame.smoke_fixture"],
}

rows = [
    # clean row A: identity zone; front-seam PE at MT 2:3 + paseq at MT 2:5
    # disclosed; byte-spliced Hebrew bound to its cited ref; proper X-X span
    {
        **COMMON,
        "decision_id": "SMOKE-A", "chunk_index_in_book": 1,
        "span": "Jer.2.4-Jer.2.5",
        "parent_collection": "SMOKE Jer.1.1-Jer.52.34",
        "unit_type": "smoke_oracle",
        "writer_part": "p00", "writer_decision_id": "SMOKE-A",
        "writer_attempt_id": "smoke_jer_r1",
        "boundary_evidence_refs": [
            "web:Jer.2.4 = oshb:Jer.2.4",
            "oshb:Jer.2.3 (petuchah, single-witness)",
            "oshb:Jer.2.5 (paseq, single-witness)",
        ],
        "boundary_rationale": ("The summons opens the unit: “" + web_2_4 +
                               "” (web:Jer.2.4). The Hebrew runs " + heb_2_4 +
                               " (oshb:Jer.2.4). A petuchah stands at oshb:Jer.2.3 "
                               "(single-witness) on the unit's front seam. The paseq "
                               "count for oshb:Jer.2.5 is one (single-witness)."),
        "strongest_rejected_alternative": "A cut after web:Jer.2.4 was rejected; the fathers-question completes the summons pair.",
        "device_notes": "Frame site recorded from the byte inventories.",
    },
    # clean row B: OFFSET-ZONE row - WEB 9:1-9:2 spans MT 8:23-9:1; mandatory
    # duals correct; Hebrew spliced from the seam verse itself
    {
        **COMMON,
        "decision_id": "SMOKE-B", "chunk_index_in_book": 2,
        "span": "Jer.9.1-Jer.9.2",
        "parent_collection": "SMOKE Jer.1.1-Jer.52.34",
        "unit_type": "smoke_oracle",
        "writer_part": "p00", "writer_decision_id": "SMOKE-B",
        "writer_attempt_id": "smoke_jer_r1",
        "boundary_evidence_refs": [
            "web:Jer.9.1 = oshb:Jer.8.23",
            "web:Jer.9.2 = oshb:Jer.9.1",
        ],
        "boundary_rationale": ("The weeping wish opens the unit: “" + web_9_1 +
                               "” (web:Jer.9.1 = oshb:Jer.8.23). The Hebrew runs " +
                               heb_8_23 + " (oshb:Jer.8.23 = web:Jer.9.1). The "
                               "lodging-place wish follows: “" + web_9_2 +
                               "” (web:Jer.9.2 = oshb:Jer.9.1)."),
        "strongest_rejected_alternative": "Starting at web:Jer.9.2 was rejected; the tears-wish governs the wilderness-wish.",
        "device_notes": "Crosswalk duals verified against the offset map.",
    },
    # clean row C: THE ARAMAIC-ISLAND row - 10:11-10:12 with the island
    # disclosed, both SAMEKHs disclosed, pointed ARAMAIC spliced and bound
    {
        **COMMON,
        "decision_id": "SMOKE-C", "chunk_index_in_book": 3,
        "span": "Jer.10.11-Jer.10.12",
        "parent_collection": "SMOKE Jer.1.1-Jer.52.34",
        "unit_type": "smoke_oracle",
        "writer_part": "p00", "writer_decision_id": "SMOKE-C",
        "writer_attempt_id": "smoke_jer_r1",
        "boundary_evidence_refs": [
            "web:Jer.10.11",
            "oshb:Jer.10.11",
            "web:Jer.10.12",
            "oshb:Jer.10.10 (setumah, single-witness)",
            "oshb:Jer.10.11 (setumah, single-witness)",
        ],
        "boundary_rationale": ("The verse at web:Jer.10.11 is the book's single Aramaic "
                               "island: “" + web_10_11 + "” (web:Jer.10.11). The Aramaic "
                               "runs " + heb_10_11 + " (oshb:Jer.10.11). Setumah segs "
                               "stand at oshb:Jer.10.10 and oshb:Jer.10.11 "
                               "(single-witness each); the doxology at web:Jer.10.12 "
                               "resumes the surrounding language."),
        "strongest_rejected_alternative": "Binding web:Jer.10.11 to the idol satire behind it was rejected; the island's addressee-instruction faces the nations.",
        "device_notes": "Language-island site recorded from the morph-code inventory.",
    },
    # bad row 1: the omnibus - every legacy planted defect class + the new
    # E-15/E-16/E-01/register classes
    {
        **COMMON,
        "decision_id": "SMOKE-BAD", "chunk_index_in_book": 4,
        "span": "Jer.5.30",                                 # (1) not X-X form
        "parent_collection": "SMOKE Jer.1.1-Jer.52.34",
        "unit_type": "smoke_saying",
        "writer_part": "p00", "writer_decision_id": "SMOKE-BAD",
        "writer_attempt_id": "smoke_jer_r1",
        "boundary_evidence_refs": [
            # ORDER MATTERS (the documented Ezra window heuristic): the
            # setumah fixture leads, the SAMEKH-marked 5:29 large-mem fixture
            # goes LAST behind >120 chars of mark-free entries.
            "oshb:Jer.5.25 (setumah, single-witness)",      # (2) mark claim at markless verse
            "web:Jer.9.4 (MT 9:4)",                         # (3) MT qualifier wrong (expect 9:3)
            "web:Jer.2.1-Jer.2.99",                         # (4) range END out of range
            "LXX Jer 25:13 (4QJer-b order)",                # (5) cross-tradition in refs
            "web:Jer.5.0",                                  # (6) zero-verse pseudo-ref invalid
            "oshb:Jer.5.26 (selah)",                        # (7) selah fabrication in Jer
            "oshb:Jer.5.30 (paseq)",                        # (8) no paseq at 5:30 + no disclosure
            "oshb:Jer.5.28 (qere)",                         # (9) false K/Q claim
            "oshb:Jer.5.26 (small nun, single-witness)",    # (10) small letter off the one site
            "web:Jer.9.5",                                  # (11) offset-zone bare ref
            "web:Jer.9.3 = oshb:Jer.9.3",                   # (12) crosswalk dual wrong (expect 9:2)
            "oshb:Jer.5.29 (large mem, single-witness)",    # (13) large-letter fabrication
        ],
        "boundary_rationale": ("The book's only overturned-altar scene - no other "     # (14) universal, no digit
                               "chapter does this. There is no setumah anywhere "       # (15) false absence claim (SAMEKH at MT 5:29)
                               "in this span. Verse 27 confirms the arc, "              # (16) unmirrored bare verse
                               "and Jer.3.4 echoes it. The quoted line " +              # (17) unmirrored ref
                               heb_5_26 +                                               # (18) Hebrew bound to WRONG ref
                               " (oshb:Jer.5.22) proves it. The faded copy reads " +    # (19) E-01: NFD-degraded pointed Hebrew
                               unicodedata.normalize("NFD", heb_2_2) +
                               " (oshb:Jer.2.2) beside it. "
                               "Only this seam matches at byte tier against "           # (20) E-16: exclusivity + tier + ref, no digit
                               "oshb:Jer.2.2. "
                               "Jer.5.27 is in Aramaic here. "                          # (21) Aramaic label, wrong verse, field has no 10:11 ref
                               "The zone reads “" + web_9_4 +                           # (22) neighbor-only in offset zone
                               "” (web:Jer.9.3)."),
        "strongest_rejected_alternative": ("“" + web_5_28 + "” (web:Jer.5.24). "        # (23) WEB misquote, wrong ref
                                           "Also \"" + web_5_28 + "\" sits near "      # (24) E-15c: WEB text in straight quotes
                                           "web:Jer.5.28 undelimited."),
        "device_notes": ("The pair web:Jer.9.6 = oshb:Jer.9.6 anchors "                 # (25) prose dual arithmetic wrong (expect 9:5)
                         "the zone. That row handles the seam, and the cross-part "     # (26) register: positional + cross-part arms
                         "context lives in citation_sweep.py under P01-003. "           # (27) register: tool filename + decision id
                         "The Hebrew inside “" + heb_5_26 + "” breaks pairing. "        # (28) E-15b: Hebrew in curly quotes
                         "“This opening quote never closes"),                           # (29) E-15a: unclosed curly quote
    },
    # bad row 2: E-02 - a whole-chapter row (ch 45 = 5 vv) at high
    # confidence, no frontier flag, no cap disclosure
    {
        **COMMON,
        "decision_id": "SMOKE-CAP", "chunk_index_in_book": 5,
        "span": "Jer.45.1-Jer.45.5",
        "parent_collection": "SMOKE Jer.1.1-Jer.52.34",
        "unit_type": "smoke_oracle",
        "writer_part": "p00", "writer_decision_id": "SMOKE-CAP",
        "writer_attempt_id": "smoke_jer_r1",
        "boundary_evidence_refs": ["web:Jer.45.1"],
        "boundary_rationale": "The Baruch oracle stands alone between the Egypt narratives and the nations.",
        "strongest_rejected_alternative": "Attaching it to the ch-44 sermon was rejected.",
        "device_notes": "Personal-oracle site.",
    },
    # bad row 3: the island-disclosure symmetry arm + a Hebrew label on the
    # island - a span covering 10:11 with NO Aramaic word anywhere
    {
        **COMMON,
        "decision_id": "SMOKE-ISLE", "chunk_index_in_book": 6,
        "span": "Jer.10.10-Jer.10.13",
        "parent_collection": "SMOKE Jer.1.1-Jer.52.34",
        "unit_type": "smoke_oracle",
        "writer_part": "p00", "writer_decision_id": "SMOKE-ISLE",
        "writer_attempt_id": "smoke_jer_r1",
        "boundary_evidence_refs": ["web:Jer.10.10-Jer.10.13"],
        "boundary_rationale": ("The living-God confession runs to the doxology; the "
                               "Hebrew diction at Jer.10.11 carries the polemic "
                               "forward without a break."),
        "strongest_rejected_alternative": "A cut before web:Jer.10.12 was rejected.",
        "device_notes": "Doxology parallel recorded.",
    },
]

out = TOOLS / "_smoke_rows.jsonl"
out.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows),
               encoding="utf-8")
proc = subprocess.run([sys.executable, str(TOOLS / "run_validator_suite.py"), str(out)],
                      capture_output=True, text=True, encoding="utf-8")
print(proc.stdout)
report = json.loads(out.with_suffix(".jsonl.validator_report.json").read_text(encoding="utf-8"))

expected = {
    "citation_sweep": ["span not in full X-X form", "dual-cite arithmetic wrong",
                       "claims setumah but the marks inventory", "claims selah",
                       "claims paseq", "single-witness", "range END out of range",
                       "ketiv/qere", "cross-tradition", "does not collate",
                       "always invalid", "claims a small letter", "claims a large letter",
                       "offset-zone ref lacks dual-cite/qualifier",
                       "MT qualifier wrong"],
    "mark_symmetry": ["selah_claim_in_jer", "paragraph_mark_claim",
                      "false_mark_absence_claim", "small_letter_claim_in_jer",
                      "large_letter_claim_in_jer", "kq_claim"],
    "refs_mirror": ["Jer.5.27", "Jer.3.4"],
    "universals": ["only"],
    "language_zones": ["aramaic_label_outside_10_11", "hebrew_label_on_10_11",
                       "aramaic_island_undisclosed"],
    "web_quotes": ["Jer.5.24", "e15a_curly_pairing_broken",
                   "e15b_hebrew_in_curly_quotes", "e15c_web_text_in_straight_quotes"],
    "cap_sweep": ["at confidence", "without frontier flag",
                  "cap disclosure missing"],
    "register": ["positional_row_reference", "cross_part_or_part_range",
                 "governance_tooling", "decision_id_in_prose"],
}
blob = {k: json.dumps(report.get(k, {}), ensure_ascii=False) for k in expected}
missed = [(k, pat) for k, pats in expected.items() for pat in pats
          if pat not in blob[k]]
clean_hit = []
for k in expected:
    # word-boundary match - "SMOKE-B" must not match "SMOKE-BAD"
    if re.search(r"SMOKE-[ABC]\b", blob[k]):
        clean_hit.append(k)

extra_missed = []
if report["citation_sweep"].get("prose_pair_problem_count", 0) < 1 or \
        "Jer.9.6" not in blob["citation_sweep"]:
    extra_missed.append(("citation_sweep", "prose dual-cite crosswalk arm"))
if report["web_quotes"].get("neighbor_only_warn_count", 0) < 1:
    extra_missed.append(("web_quotes", "offset-zone neighbor-only warn arm"))
if report["citation_sweep"].get("nfd_degraded_count", 0) < 1:
    extra_missed.append(("citation_sweep", "E-01 nfd_degraded detection"))
if not report["summary"].get("nfd_hard_e01"):
    extra_missed.append(("suite", "E-01 nfd-degraded must set the HARD arm"))
if report["summary"].get("hard_status") != "RED":
    extra_missed.append(("suite", "hard_status must be RED on the planted file"))
if report["universals"].get("e16_exclusivity_undampened", 0) < 1:
    extra_missed.append(("universals", "E-16 exclusivity-undampened counter"))

# ---- check_atomic_isolation machinery arm (verdicts + crosswalk + p3) ----
# dynamic machine-clean candidate: first ch-3-7 single verse with zero
# stoplist-filtered skeleton shares with either neighbor
sys.path.insert(0, str(TOOLS))
jl = importlib.import_module("jer_lib")
cai = importlib.import_module("check_atomic_isolation")
osh_sk = {}
for line in (SPBOOK / "Jer_oshb.txt").read_text(encoding="utf-8").splitlines():
    if "\t" in line:
        ref, text = line.split("\t", 1)
        osh_sk[ref] = jl.skeleton(text)


def content_toks(c, v):
    mt = jl.web_to_mt(c, v)
    return {x for x in osh_sk.get(f"Jer.{mt[0]}.{mt[1]}", "").split()
            if len(x) >= 2 and x not in cai.STOP}


clean_candidate = None
for c in range(3, 8):
    for v in range(2, jl.LAST_VERSE[c]):
        if not (content_toks(c, v) & content_toks(c, v - 1)) and \
                not (content_toks(c, v) & content_toks(c, v + 1)):
            clean_candidate = (c, v)
            break
    if clean_candidate:
        break
assert clean_candidate, "no machine-clean candidate found in chs 3-7"

# crosswalk discrimination precondition: the ammi share at the seam exists
# ONLY through the crosswalk (WEB 9:1 = MT 8:23 shares ammi with WEB 9:2 =
# MT 9:1); under the refuted identity mapping (MT 9:1 vs MT 9:2) it is absent
ammi = "עמי"
assert ammi in (content_toks(9, 1) & content_toks(9, 2)), \
    "seam ammi share missing through the crosswalk"
ident_share = ({x for x in osh_sk["Jer.9.1"].split() if len(x) >= 2 and x not in cai.STOP}
               & {x for x in osh_sk["Jer.9.2"].split() if len(x) >= 2 and x not in cai.STOP})
assert ammi not in ident_share, "ammi unexpectedly shared under identity - discrimination lost"

at_rows = [
    {"writer_decision_id": "AT-1", "span": "Jer.2.1-Jer.2.1",
     "unit_type": "test_atomic", "confidence": "high"},         # cohesion_live (lemor share)
    {"writer_decision_id": "AT-2",
     "span": f"Jer.{clean_candidate[0]}.{clean_candidate[1]}-Jer.{clean_candidate[0]}.{clean_candidate[1]}",
     "unit_type": "test_atomic", "confidence": "high"},         # machine_clean
    {"writer_decision_id": "AT-3", "span": "Jer.9.1-Jer.9.1",
     "unit_type": "test_atomic", "confidence": "high"},         # crosswalk proof (ammi share)
    {"writer_decision_id": "AT-4", "span": "Jer.36.1-Jer.36.1",
     "unit_type": "other_type", "confidence": "high"},          # model_review (form)
    {"writer_decision_id": "AT-5", "span": "Jer.30.5-Jer.30.5",
     "unit_type": "test_atomic", "confidence": "medium_low"},   # model_review (confidence)
]
at_path = TOOLS / "_smoke_atomic_rows.jsonl"
at_path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in at_rows),
                   encoding="utf-8")
shared_plan = SPBOOK / "review_scope.json"
plan_before = shared_plan.exists()

# unarmed subprocess run: everything model_review; sibling artifact only (p3)
proc2 = subprocess.run([sys.executable, str(TOOLS / "check_atomic_isolation.py"),
                        str(at_path)], capture_output=True, text=True, encoding="utf-8")
un = json.loads(proc2.stdout)
sibling = at_path.with_suffix(at_path.suffix + ".review_scope.json")
atomic_problems = []
if un.get("armed") is not False or un.get("machine_clean") != 0 or \
        un.get("model_review_form_or_lowconf") != 5:
    atomic_problems.append(f"unarmed run wrong: {un}")
if not sibling.exists():
    atomic_problems.append("p3 sibling artifact missing")
if shared_plan.exists() != plan_before:
    atomic_problems.append("p3 GUARD BROKEN: subset run touched SP/Jer/review_scope.json")

# armed in-process run: verdict logic + crosswalk fetch
cai.ATOMIC_TYPES = {"test_atomic"}
old_argv = sys.argv
sys.argv = ["check_atomic_isolation.py", str(at_path)]
buf = io.StringIO()
old_stdout = sys.stdout
sys.stdout = buf
try:
    cai.main()
finally:
    sys.stdout = old_stdout
    sys.argv = old_argv
armed = json.loads(sibling.read_text(encoding="utf-8"))
v = {x["row"]: x for x in armed["verdicts"]}
if v["AT-1"]["verdict"] != "cohesion_live" or not (
        v["AT-1"].get("shared_prev") or v["AT-1"].get("shared_next")):
    atomic_problems.append(f"AT-1 expected cohesion_live with a share: {v['AT-1']}")
if v["AT-2"]["verdict"] != "machine_clean":
    atomic_problems.append(f"AT-2 expected machine_clean: {v['AT-2']}")
if v["AT-4"]["verdict"] != "model_review" or v["AT-5"]["verdict"] != "model_review":
    atomic_problems.append("AT-4/AT-5 expected model_review")
at3 = v["AT-3"]
if at3["verdict"] != "cohesion_live" or ammi not in at3.get("shared_next", []):
    atomic_problems.append(f"AT-3 crosswalk fetch wrong (want ammi in shared_next): {at3}")
if shared_plan.exists() != plan_before:
    atomic_problems.append("p3 GUARD BROKEN on armed run")

# ---- collate crosswalk CLI arms: bare WEB zone ref + the Aramaic island ----
proc3 = subprocess.run([sys.executable, str(TOOLS / "collate.py"),
                        "--ref", "Jer.9.1", "--quote", heb_8_23],
                       capture_output=True, text=True, encoding="utf-8")
col_a = json.loads(proc3.stdout)
proc4 = subprocess.run([sys.executable, str(TOOLS / "collate.py"),
                        "--ref", "Jer.10.11", "--quote", heb_10_11],
                       capture_output=True, text=True, encoding="utf-8")
col_b = json.loads(proc4.stdout)
collate_ok = (col_a.get("tier") == "byte" and "8.23" in col_a.get("mt_window", "")
              and col_b.get("tier") == "byte" and col_b.get("language") == "Aramaic")

verdict = ("PASS" if not missed and not clean_hit and not extra_missed
           and not atomic_problems and collate_ok else "FAIL")
print(json.dumps({"planted_defects_missed": missed + extra_missed,
                  "clean_rows_flagged_by": clean_hit,
                  "atomic_isolation_problems": atomic_problems,
                  "machine_clean_candidate": f"Jer.{clean_candidate[0]}.{clean_candidate[1]}",
                  "collate_crosswalk_cli_zone": col_a,
                  "collate_aramaic_island": col_b,
                  "verdict": verdict},
                 ensure_ascii=False, indent=1))
