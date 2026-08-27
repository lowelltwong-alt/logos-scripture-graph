#!/usr/bin/env python3
"""Phase-0 toolkit smoke test for Isa (orchestrator only; artifacts removed
after). THREE clean rows must pass every validator — one identity-zone, one
ZONE-A (renumbering) row, one ZONE-B (SPLIT) row spanning WEB 63:19-64:2 —
and one deliberately-bad row must be caught on EVERY planted defect class,
including both offset-zone arms, the SPLIT-dual arm, and the p1/p2/p4
patch-lineage classes (full 22-field schema on every row per Prov close
lesson b; wj_or_red_letter_considered carries the mandated fixed sentence on
all rows — the p4 ngram7 exclusion class). A separate arm proves the
check_atomic_isolation machinery (verdict logic, crosswalk verse fetch
DISCRIMINATING crosswalk from identity via the MT 9:5|9:6 המשרה share, the
SPLIT-pair marker, p3 guarded output path) BEFORE it can matter. Hebrew is
byte-spliced from verse_map_oshb.json (never hand-typed); English is spliced
from verse_map_web.json."""
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
pm = json.loads((SPBOOK / "pmarks_Isa.json").read_text(encoding="utf-8"))


def webtxt(ref):
    return re.sub(r"\[fn [^\]]*\]", " ", web[ref]["text"]).strip()


heb_5_24 = oshb["Isa.5.24"]["text"]                  # identity-zone verse
heb_8_23 = oshb["Isa.8.23"]["text"]                  # zone-A seam verse (= WEB 9:1)
heb_63_19 = oshb["Isa.63.19"]["text"]                # THE SPLIT VERSE (= WEB 63:19 + 64:1)
heb_5_26 = oshb["Isa.5.26"]["text"]                  # wrong-ref fixture
web_5_24 = webtxt("Isa.5.24")
web_9_1 = webtxt("Isa.9.1")
web_9_2 = webtxt("Isa.9.2")
web_64_1 = webtxt("Isa.64.1")
web_9_4 = webtxt("Isa.9.4")
web_5_28 = webtxt("Isa.5.28")

# preconditions for the rows below (fail loudly if the data moves)
assert pm["marks"].get("Isa.5.23") == ["SAMEKH"], "smoke precondition: SAMEKH at MT 5:23"
assert pm["marks"].get("Isa.5.30") == ["PE"], "smoke precondition: PE at MT 5:30"
for k in ("Isa.5.24", "Isa.5.25", "Isa.5.26", "Isa.5.28", "Isa.8.22", "Isa.8.23",
          "Isa.9.1", "Isa.63.18", "Isa.63.19", "Isa.64.1"):
    assert not pm["marks"].get(k), f"smoke precondition: {k} must be mark-free"
assert pm["kq"].get("Isa.9.2") and pm["kq"].get("Isa.9.6"), "smoke precondition: K/Q at MT 9:2 + 9:6"
for k in ("Isa.5.24", "Isa.5.26", "Isa.5.28", "Isa.5.30", "Isa.8.23", "Isa.9.1",
          "Isa.63.19", "Isa.64.1"):
    assert not pm["kq"].get(k), f"smoke precondition: {k} must be K/Q-free"
assert not pm["paseq"].get("Isa.5.30"), "smoke precondition: 5:30 paseq-free"
assert pm["other_segs"] == {"Isa.44.14": ["x-small:ן"]}, "smoke precondition: the one x-small site"

COMMON = {
    "book": "Isa", "model_id": "M8_fable", "non_authorizing": True,
    "literature_type_guess": "prophetic_oracle", "confidence": "high",
    "strong_or_hebrew_tags_used": False,
    "wj_or_red_letter_considered": "not applicable in the OT substrate",
    "frontier_flag_considered": False, "review_status": "draft",
    "observed_substrate_signals": ["oracle_frame.smoke_fixture"],
}

rows = [
    # clean row A: identity zone; front-seam SAMEKH at MT 5:23 disclosed;
    # byte-spliced Hebrew bound to its cited ref; proper X-X span; full
    # schema incl. range-shaped parent_collection (p1 skip class)
    {
        **COMMON,
        "decision_id": "SMOKE-A", "chunk_index_in_book": 1,
        "span": "Isa.5.24-Isa.5.25",
        "parent_collection": "SMOKE Isa.1.1-Isa.66.24",
        "unit_type": "smoke_oracle",
        "writer_part": "p00", "writer_decision_id": "SMOKE-A",
        "writer_attempt_id": "smoke_isa_r1",
        "boundary_evidence_refs": [
            "web:Isa.5.24 = oshb:Isa.5.24",
            "oshb:Isa.5.23 (setumah, single-witness)",
        ],
        "boundary_rationale": ("The fire-judgment line opens the unit: “" + web_5_24 +
                               "” (web:Isa.5.24). The Hebrew runs " + heb_5_24 +
                               " (oshb:Isa.5.24). A setumah stands at oshb:Isa.5.23 "
                               "(single-witness), the seam before this unit."),
        "strongest_rejected_alternative": "A cut after web:Isa.5.24 was rejected; the outstretched-hand line completes the judgment pair.",
        "device_notes": "Refrain site recorded from the byte inventories.",
    },
    # clean row B: ZONE-A row — WEB 9:1-9:2 spans MT 8:23-9:1; mandatory
    # duals correct; Hebrew spliced from the seam verse itself
    {
        **COMMON,
        "decision_id": "SMOKE-B", "chunk_index_in_book": 2,
        "span": "Isa.9.1-Isa.9.2",
        "parent_collection": "SMOKE Isa.1.1-Isa.66.24",
        "unit_type": "smoke_oracle",
        "writer_part": "p00", "writer_decision_id": "SMOKE-B",
        "writer_attempt_id": "smoke_isa_r1",
        "boundary_evidence_refs": [
            "web:Isa.9.1 = oshb:Isa.8.23",
            "web:Isa.9.2 = oshb:Isa.9.1",
        ],
        "boundary_rationale": ("The gloom-reversal opens the unit: “" + web_9_1 +
                               "” (web:Isa.9.1 = oshb:Isa.8.23). The Hebrew runs " +
                               heb_8_23 + " (oshb:Isa.8.23 = web:Isa.9.1). The "
                               "light-line follows: “" + web_9_2 +
                               "” (web:Isa.9.2 = oshb:Isa.9.1)."),
        "strongest_rejected_alternative": "Starting at web:Isa.9.2 was rejected; the reversal line governs the light-line.",
        "device_notes": "Crosswalk duals verified against the offset map.",
    },
    # clean row C: THE SPLIT-ZONE row — WEB 63:19-64:2 spans MT 63:19 (BOTH
    # halves) + MT 64:1; mandatory duals correct incl. the second-half dual
    {
        **COMMON,
        "decision_id": "SMOKE-C", "chunk_index_in_book": 3,
        "span": "Isa.63.19-Isa.64.2",
        "parent_collection": "SMOKE Isa.1.1-Isa.66.24",
        "unit_type": "smoke_oracle",
        "writer_part": "p00", "writer_decision_id": "SMOKE-C",
        "writer_attempt_id": "smoke_isa_r1",
        "boundary_evidence_refs": [
            "web:Isa.63.19 = oshb:Isa.63.19",
            "web:Isa.64.1 = oshb:Isa.63.19",
            "web:Isa.64.2 = oshb:Isa.64.1",
        ],
        "boundary_rationale": ("The tear-the-heavens plea stands at “" + web_64_1 +
                               "” (web:Isa.64.1 = oshb:Isa.63.19, the second half of "
                               "the split verse). The Hebrew runs " + heb_63_19 +
                               " (oshb:Isa.63.19 = web:Isa.63.19); the split verse "
                               "spans both WEB halves, and the fire-simile follows at "
                               "web:Isa.64.2 (MT 64:1)."),
        "strongest_rejected_alternative": "A cut between web:Isa.63.19 and web:Isa.64.1 was rejected; the plea continues the same MT verse.",
        "device_notes": "Split-verse duals verified against the offset map.",
    },
    # bad row: every planted defect class, one row
    {
        **COMMON,
        "decision_id": "SMOKE-BAD", "chunk_index_in_book": 4,
        "span": "Isa.5.30",                                 # (1) not X-X form
        "parent_collection": "SMOKE Isa.1.1-Isa.66.24",
        "unit_type": "smoke_saying",
        "writer_part": "p00", "writer_decision_id": "SMOKE-BAD",
        "writer_attempt_id": "smoke_isa_r1",
        "boundary_evidence_refs": [
            # ORDER MATTERS (the documented Ezra window heuristic, hit again
            # here at Phase 0): the setumah fixture must sit >120 chars from
            # the device_notes prose pair, whose Isa.9.6 token is a genuinely
            # SAMEKH-marked MT verse that would satisfy the dual-reading mark
            # check — so the setumah entry goes LAST, behind >120 chars of
            # mark-free entries.
            "web:Isa.9.4 (MT 9:4)",                         # (2) MT qualifier wrong (expect 9:3)
            "web:Isa.2.1-Isa.2.99",                         # (3) range END out of range
            "LXX Isa 2:1",                                  # (4) cross-tradition in refs
            "web:Isa.5.0",                                  # (5) zero-verse pseudo-ref invalid
            "oshb:Isa.5.25 (selah)",                        # (7) selah fabrication in Isa
            "oshb:Isa.5.30 (paseq)",                        # (8) no paseq at 5:30 + no disclosure
            "oshb:Isa.5.28 (qere)",                         # (9) false K/Q claim
            "oshb:Isa.5.26 (small nun, single-witness)",    # (10) small letter off the one site
            "oshb:Isa.5.29 (large mem, single-witness)",    # (11) large-letter fabrication
            "web:Isa.9.5",                                  # (12) offset-zone bare ref
            "web:Isa.9.3 = oshb:Isa.9.3",                   # (13) crosswalk dual wrong (expect 9:2)
            "oshb:Isa.63.19 = web:Isa.63.18",               # (14) SPLIT dual wrong (expect 63:19 or 64:1)
            "oshb:Isa.5.24 (setumah, single-witness)",      # (6) mark claim at markless verse
        ],
        "boundary_rationale": ("The book's only overturned-vineyard scene — no other "  # (15) universal, no digit
                               "chapter does this. There is no setumah anywhere "       # (16) false absence claim (PE at MT 5:30)
                               "in this span. Verse 27 confirms the arc, "              # (17) unmirrored bare verse
                               "and Isa.3.4 echoes it. The quoted line " +              # (18) unmirrored ref (ch 3: outside the clamped ch-2 range's coverage)
                               heb_5_26 +                                               # (19) Hebrew bound to WRONG ref
                               " (oshb:Isa.5.22) proves it. The qere reading at "
                               "Isa.5.28 alters it. Isa.5.27 is in Aramaic here. "      # (20) Aramaic label
                               "The zone reads “" + web_9_4 +                           # (21) neighbor-only in offset zone
                               "” (web:Isa.9.3)."),
        "strongest_rejected_alternative": "“" + web_5_28 + "” (web:Isa.5.24)",          # (22) WEB misquote, wrong ref
        "device_notes": ("The pair web:Isa.9.6 = oshb:Isa.9.6 anchors "                 # (23) prose dual arithmetic wrong
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
                       "always invalid", "claims a small letter", "claims a large letter",
                       "offset-zone ref lacks dual-cite/qualifier",
                       "MT qualifier wrong", "web:Isa.63.19 or web:Isa.64.1"],
    "mark_symmetry": ["selah_claim_in_isa", "paragraph_mark_claim",
                      "false_mark_absence_claim", "small_letter_claim_in_isa",
                      "large_letter_claim_in_isa", "kq_claim"],
    "refs_mirror": ["Isa.5.27", "Isa.3.4"],
    "universals": ["only"],
    "language_zones": ["aramaic_label"],
    "web_quotes": ["Isa.5.24"],
}
blob = {k: json.dumps(report.get(k, {}), ensure_ascii=False) for k in expected}
missed = [(k, pat) for k, pats in expected.items() for pat in pats
          if pat not in blob[k]]
clean_hit = []
for k in ("citation_sweep", "mark_symmetry", "refs_mirror", "universals",
          "language_zones", "web_quotes"):
    # word-boundary match — "SMOKE-B" must not match "SMOKE-BAD"
    if re.search(r"SMOKE-[ABC]\b", blob[k]):
        clean_hit.append(k)

# offset-zone arm assertions beyond the pattern lists
extra_missed = []
if report["citation_sweep"].get("prose_pair_problem_count", 0) < 1 or \
        "Isa.9.6" not in blob["citation_sweep"]:
    extra_missed.append(("citation_sweep", "prose dual-cite crosswalk arm"))
if report["web_quotes"].get("neighbor_only_warn_count", 0) < 1:
    extra_missed.append(("web_quotes", "offset-zone neighbor-only warn arm"))

# ---- check_atomic_isolation machinery arm (verdicts + crosswalk + split + p3) ----
at_rows = [
    {"writer_decision_id": "AT-1", "span": "Isa.5.4-Isa.5.4",
     "unit_type": "test_atomic", "confidence": "high"},         # cohesion_live (identity zone)
    {"writer_decision_id": "AT-2", "span": "Isa.5.9-Isa.5.9",
     "unit_type": "test_atomic", "confidence": "high"},         # machine_clean expected
    {"writer_decision_id": "AT-3", "span": "Isa.9.6-Isa.9.6",
     "unit_type": "test_atomic", "confidence": "high"},         # crosswalk proof: MT 9:5 & MT 9:6 share המשרה (identity finds NO share)
    {"writer_decision_id": "AT-4", "span": "Isa.36.1-Isa.36.1",
     "unit_type": "other_type", "confidence": "high"},          # model_review (form)
    {"writer_decision_id": "AT-5", "span": "Isa.40.3-Isa.40.3",
     "unit_type": "test_atomic", "confidence": "medium_low"},   # model_review (confidence)
    {"writer_decision_id": "AT-6", "span": "Isa.63.19-Isa.63.19",
     "unit_type": "test_atomic", "confidence": "high"},         # SPLIT-pair marker: next neighbor WEB 64:1 = same MT verse
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
        un.get("model_review_form_or_lowconf") != 6:
    atomic_problems.append(f"unarmed run wrong: {un}")
if not sibling.exists():
    atomic_problems.append("p3 sibling artifact missing")
if shared_plan.exists() != plan_before:
    atomic_problems.append("p3 GUARD BROKEN: subset run touched SP/Isa/review_scope.json")

# armed in-process run: verdict logic + crosswalk fetch + split marker
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
if v["AT-1"]["verdict"] != "cohesion_live" or not (
        v["AT-1"].get("shared_prev") or v["AT-1"].get("shared_next")):
    atomic_problems.append(f"AT-1 expected cohesion_live with a share: {v['AT-1']}")
if v["AT-2"]["verdict"] != "machine_clean":
    atomic_problems.append(f"AT-2 expected machine_clean: {v['AT-2']}")
if v["AT-4"]["verdict"] != "model_review" or v["AT-5"]["verdict"] != "model_review":
    atomic_problems.append("AT-4/AT-5 expected model_review")
# crosswalk proof: WEB 9:6's tokens come from MT 9:5 and share ha-misrah with
# its next neighbor WEB 9:7 (= MT 9:6); the identity mapping (MT 9:6 vs MT
# 9:7) shares NOTHING — this share only exists through the crosswalk.
at3 = v["AT-3"]
if at3["verdict"] != "cohesion_live" or "המשרה" not in at3.get("shared_next", []):
    atomic_problems.append(f"AT-3 crosswalk fetch wrong: {at3}")
# split marker: WEB 63:19's next neighbor is WEB 64:1 = the SAME MT verse —
# the share is by construction and must be routed to model_review with the
# split reason, never silent cohesion
at6 = v["AT-6"]
if at6["verdict"] != "model_review" or "split" not in at6.get("why", ""):
    atomic_problems.append(f"AT-6 split marker wrong: {at6}")
if shared_plan.exists() != plan_before:
    atomic_problems.append("p3 GUARD BROKEN on armed run")

# ---- collate crosswalk CLI arms: bare WEB refs in BOTH zones ----
proc3 = subprocess.run([sys.executable, str(TOOLS / "collate.py"),
                        "--ref", "Isa.9.1", "--quote", heb_8_23],
                       capture_output=True, text=True, encoding="utf-8")
col_a = json.loads(proc3.stdout)
proc4 = subprocess.run([sys.executable, str(TOOLS / "collate.py"),
                        "--ref", "Isa.64.1", "--quote", heb_63_19],
                       capture_output=True, text=True, encoding="utf-8")
col_b = json.loads(proc4.stdout)
collate_ok = (col_a.get("tier") == "byte" and "8.23" in col_a.get("mt_window", "")
              and col_b.get("tier") == "byte" and "63.19" in col_b.get("mt_window", ""))

verdict = ("PASS" if not missed and not clean_hit and not extra_missed
           and not atomic_problems and collate_ok else "FAIL")
print(json.dumps({"planted_defects_missed": missed + extra_missed,
                  "clean_rows_flagged_by": clean_hit,
                  "atomic_isolation_problems": atomic_problems,
                  "collate_crosswalk_cli_zone_a": col_a,
                  "collate_crosswalk_cli_zone_b_split": col_b,
                  "verdict": verdict},
                 ensure_ascii=False, indent=1))
