#!/usr/bin/env python3
"""Phase-0 toolkit smoke test for Eccl (orchestrator only; artifacts removed
after). Two clean rows must pass every validator; one deliberately-bad row
must be caught on EVERY planted defect class — including the NEW offset-zone
classes (Eccl is a crosswalk book) and the p1/p2/p3 patch-lineage classes
(full 22-field schema on every row per Prov close lesson b). A separate arm
proves the check_atomic_isolation machinery (verdict logic, crosswalk verse
fetch, p3 guarded output path) BEFORE it can matter. Hebrew is byte-spliced
from verse_map_oshb.json (never hand-typed); English is spliced from
verse_map_web.json."""
from __future__ import annotations

import importlib
import json
import re
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
SPBOOK = TOOLS.parent
oshb = json.loads((TOOLS / "verse_map_oshb.json").read_text(encoding="utf-8"))
web = json.loads((TOOLS / "verse_map_web.json").read_text(encoding="utf-8"))
pm = json.loads((SPBOOK / "pmarks_Eccl.json").read_text(encoding="utf-8"))


def webtxt(ref):
    return re.sub(r"\[fn [^\]]*\]", " ", web[ref]["text"]).strip()


heb_1_11 = oshb["Eccl.1.11"]["text"]                 # full pointed verse
heb_4_17 = oshb["Eccl.4.17"]["text"]                 # seam verse (K/Q inline)
heb_3_2 = oshb["Eccl.3.2"]["text"]                   # full pointed verse
web_1_9 = webtxt("Eccl.1.9")
web_5_1 = webtxt("Eccl.5.1")
web_5_3 = webtxt("Eccl.5.3")
web_3_7 = webtxt("Eccl.3.7")

# preconditions for the rows below (fail loudly if the data moves)
assert pm["marks"].get("Eccl.1.11") == ["PE"], "smoke precondition: PE at MT 1:11"
assert pm["marks"].get("Eccl.3.8") == ["SAMEKH"], "smoke precondition: SAMEKH at MT 3:8"
for k in ("Eccl.1.8", "Eccl.1.9", "Eccl.1.10", "Eccl.3.9", "Eccl.4.16",
          "Eccl.4.17", "Eccl.5.1", "Eccl.5.2"):
    assert not pm["marks"].get(k), f"smoke precondition: {k} must be mark-free"
assert pm["kq"].get("Eccl.4.17"), "smoke precondition: K/Q at the seam verse MT 4:17"
for k in ("Eccl.1.9", "Eccl.1.11", "Eccl.3.3", "Eccl.3.9", "Eccl.5.1"):
    assert not pm["kq"].get(k), f"smoke precondition: {k} must be K/Q-free"
assert not pm["paseq"].get("Eccl.3.3"), "smoke precondition: 3:3 paseq-free"

COMMON = {
    "book": "Eccl", "model_id": "M8_fable", "non_authorizing": True,
    "literature_type_guess": "wisdom_reflection", "confidence": "high",
    "strong_or_hebrew_tags_used": False,
    "wj_or_red_letter_considered": "not applicable in the OT substrate",
    "frontier_flag_considered": False, "review_status": "draft",
    "observed_substrate_signals": ["smoke-fixture signal"],
}

rows = [
    # clean row A: identity zone; PE at MT 1:11 disclosed; optional dual
    # correct; byte-spliced Hebrew bound to its cited ref; proper X-X span;
    # full schema incl. range-shaped parent_collection (p1 skip class)
    {
        **COMMON,
        "decision_id": "SMOKE-A", "chunk_index_in_book": 1,
        "span": "Eccl.1.9-Eccl.1.11",
        "parent_collection": "F1 Eccl.1.1-Eccl.1.11",
        "unit_type": "smoke_poem",
        "writer_part": "p00", "writer_decision_id": "SMOKE-A",
        "writer_attempt_id": "smoke_eccl_r1",
        "boundary_evidence_refs": [
            "web:Eccl.1.9 = oshb:Eccl.1.9",
            "oshb:Eccl.1.11 (petuchah, single-witness)",
        ],
        "boundary_rationale": ("The nothing-new refrain closes the prologue poem: “" +
                               web_1_9 + "” (web:Eccl.1.9). The closing line runs " +
                               heb_1_11 + " (oshb:Eccl.1.11); a petuchah stands at "
                               "oshb:Eccl.1.11 (single-witness), closing the poem."),
        "strongest_rejected_alternative": "A cut after web:Eccl.1.10 was rejected; the no-remembrance line completes the poem's frame.",
        "device_notes": "Refrain texture recorded in the staged inventory.",
    },
    # clean row B: THE OFFSET-ZONE row — WEB 5:1-5:2 spans MT 4:17-5:1;
    # mandatory duals correct; Hebrew spliced from the K/Q-bearing seam
    # verse with in-field ketiv/qere disclosure
    {
        **COMMON,
        "decision_id": "SMOKE-B", "chunk_index_in_book": 2,
        "span": "Eccl.5.1-Eccl.5.2",
        "parent_collection": "M Eccl.1.12-Eccl.12.7",
        "unit_type": "smoke_admonition",
        "writer_part": "p00", "writer_decision_id": "SMOKE-B",
        "writer_attempt_id": "smoke_eccl_r1",
        "boundary_evidence_refs": [
            "web:Eccl.5.1 = oshb:Eccl.4.17 (ketiv/qere, single-witness)",
            "web:Eccl.5.2 = oshb:Eccl.5.1",
        ],
        "boundary_rationale": ("The temple admonition opens the unit: “" + web_5_1 +
                               "” (web:Eccl.5.1 = oshb:Eccl.4.17). The Hebrew runs " +
                               heb_4_17 + " (oshb:Eccl.4.17; the verse carries a "
                               "ketiv/qere note, single-witness). The rash-mouth "
                               "warning follows at web:Eccl.5.2 (MT 5:1)."),
        "strongest_rejected_alternative": "Beginning at web:Eccl.5.2 was rejected; the step-guarding command governs the unit.",
        "device_notes": "Crosswalk duals verified against the offset map.",
    },
    # bad row: every planted defect class, one row
    {
        **COMMON,
        "decision_id": "SMOKE-BAD", "chunk_index_in_book": 3,
        "span": "Eccl.3.9",                                 # (1) not X-X form
        "parent_collection": "M Eccl.1.12-Eccl.12.7",
        "unit_type": "smoke_saying",
        "writer_part": "p00", "writer_decision_id": "SMOKE-BAD",
        "writer_attempt_id": "smoke_eccl_r1",
        "boundary_evidence_refs": [
            "web:Eccl.5.3 = oshb:Eccl.5.3",                 # (2) crosswalk dual wrong
            "oshb:Eccl.3.9 (setumah, single-witness)",      # (3) mark claim at markless verse
            "oshb:Eccl.3.2 (selah)",                        # (4) selah fabrication in Eccl
            "oshb:Eccl.3.3 (paseq)",                        # (5) no paseq at 3:3 + no disclosure
            "web:Eccl.2.1-Eccl.2.99",                       # (6) range END out of range
            "oshb:Eccl.3.3 (qere)",                         # (7) false K/Q claim
            "LXX Eccl 2:1",                                 # (8) cross-tradition in refs
            "web:Eccl.5.0",                                 # (9) zero-verse pseudo-ref invalid
            "oshb:Eccl.3.4 (small nun, single-witness)",    # (10) special-letter fabrication
            "web:Eccl.5.6",                                 # (11) offset-zone bare ref
            "web:Eccl.5.4 (MT 5:4)",                        # (12) MT qualifier wrong (expect 5:3)
        ],
        "boundary_rationale": ("The book's only rest-command — no other "         # (13) universal, no digit
                               "chapter does this. There is no setumah anywhere "  # (21) false absence claim (seam MT 3:8)
                               "in this span. Verse 7 confirms the arc, "          # (14) unmirrored bare verse
                               "and Eccl.4.2 echoes it. The quoted line " +        # (15) unmirrored ref
                               heb_3_2 +                                           # (16) Hebrew bound to WRONG ref
                               " (oshb:Eccl.3.5) proves it. Eccl.3.2 is in "
                               "Aramaic here. The zone reads “" + web_5_3 +        # (17) Aramaic label
                               "” (web:Eccl.5.2)."),                               # (18) neighbor-only in offset zone
        "strongest_rejected_alternative": "“" + web_3_7 + "” (web:Eccl.3.4)",      # (19) WEB misquote, wrong ref
        "device_notes": ("The pair web:Eccl.5.10 = oshb:Eccl.5.10 anchors "        # (20) prose dual arithmetic wrong
                         "the zone."),
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
                       "always invalid", "small/large letter",
                       "offset-zone ref lacks dual-cite/qualifier",
                       "MT qualifier wrong"],
    "mark_symmetry": ["selah_claim_in_eccl", "paragraph_mark_claim",
                      "false_mark_absence_claim", "special_letter_claim_in_eccl",
                      "kq_claim"],
    "refs_mirror": ["Eccl.3.7", "Eccl.4.2"],
    "universals": ["only"],
    "language_zones": ["aramaic_label"],
    "web_quotes": ["Eccl.3.4"],
}
blob = {k: json.dumps(report.get(k, {}), ensure_ascii=False) for k in expected}
missed = [(k, pat) for k, pats in expected.items() for pat in pats
          if pat not in blob[k]]
clean_hit = []
for k in ("citation_sweep", "mark_symmetry", "refs_mirror", "universals",
          "language_zones", "web_quotes"):
    # word-boundary match — "SMOKE-B" must not match "SMOKE-BAD"
    if re.search(r"SMOKE-[AB]\b", blob[k]):
        clean_hit.append(k)

# offset-zone arm assertions beyond the pattern lists
extra_missed = []
if report["citation_sweep"].get("prose_pair_problem_count", 0) < 1 or \
        "Eccl.5.10" not in blob["citation_sweep"]:
    extra_missed.append(("citation_sweep", "prose dual-cite crosswalk arm"))
if report["web_quotes"].get("neighbor_only_warn_count", 0) < 1:
    extra_missed.append(("web_quotes", "offset-zone neighbor-only warn arm"))

# ---- check_atomic_isolation machinery arm (verdicts + crosswalk + p3) ----
at_rows = [
    {"writer_decision_id": "AT-1", "span": "Eccl.3.2-Eccl.3.2",
     "unit_type": "test_atomic", "confidence": "high"},         # cohesion_live (shares et-tokens)
    {"writer_decision_id": "AT-2", "span": "Eccl.10.8-Eccl.10.8",
     "unit_type": "test_atomic", "confidence": "high"},         # machine_clean expected
    {"writer_decision_id": "AT-3", "span": "Eccl.5.1-Eccl.5.1",
     "unit_type": "test_atomic", "confidence": "high"},         # crosswalk: MT 4:17 bytes
    {"writer_decision_id": "AT-4", "span": "Eccl.7.1-Eccl.7.1",
     "unit_type": "other_type", "confidence": "high"},          # model_review (form)
    {"writer_decision_id": "AT-5", "span": "Eccl.10.9-Eccl.10.9",
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
    atomic_problems.append("p3 GUARD BROKEN: subset run touched SP/Eccl/review_scope.json")

# armed in-process run: verdict logic + crosswalk fetch
sys.path.insert(0, str(TOOLS))
cai = importlib.import_module("check_atomic_isolation")
cai.ATOMIC_TYPES = {"test_atomic"}
old_argv = sys.argv
sys.argv = ["check_atomic_isolation.py", str(at_path)]
import io
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
if v["AT-1"]["verdict"] != "cohesion_live":
    atomic_problems.append(f"AT-1 expected cohesion_live: {v['AT-1']}")
if v["AT-2"]["verdict"] != "machine_clean":
    atomic_problems.append(f"AT-2 expected machine_clean: {v['AT-2']}")
if v["AT-4"]["verdict"] != "model_review" or v["AT-5"]["verdict"] != "model_review":
    atomic_problems.append("AT-4/AT-5 expected model_review")
# crosswalk proof: WEB 5:1's tokens come from MT 4:17 and share ha-elohim
# with its next neighbor WEB 5:2 (= MT 5:1)
at3 = v["AT-3"]
if at3["verdict"] != "cohesion_live" or "האלהים" not in at3.get("shared_next", []):
    atomic_problems.append(f"AT-3 crosswalk fetch wrong: {at3}")
if shared_plan.exists() != plan_before:
    atomic_problems.append("p3 GUARD BROKEN on armed run")

# ---- collate crosswalk CLI arm: bare WEB ref 5:1 must byte-match MT 4:17 ----
proc3 = subprocess.run([sys.executable, str(TOOLS / "collate.py"),
                        "--ref", "Eccl.5.1", "--quote", heb_4_17],
                       capture_output=True, text=True, encoding="utf-8")
col = json.loads(proc3.stdout)
collate_ok = col.get("tier") == "byte" and "4.17" in col.get("mt_window", "")

verdict = ("PASS" if not missed and not clean_hit and not extra_missed
           and not atomic_problems and collate_ok else "FAIL")
print(json.dumps({"planted_defects_missed": missed + extra_missed,
                  "clean_rows_flagged_by": clean_hit,
                  "atomic_isolation_problems": atomic_problems,
                  "collate_crosswalk_cli": col,
                  "verdict": verdict},
                 ensure_ascii=False, indent=1))
