#!/usr/bin/env python3
"""Phase-0 toolkit smoke test for Song (orchestrator only; artifacts removed
after). Two clean rows must pass every validator; one deliberately-bad row
must be caught on EVERY planted defect class — including the offset-zone
classes (Song is a crosswalk book: MT 7:1 = WEB 6:13) and the p1/p2/p4
patch-lineage classes (full 22-field schema on every row per Prov close
lesson b; wj_or_red_letter_considered carries the mandated fixed sentence on
all rows — the p4 ngram7 exclusion class). A separate arm proves the
check_atomic_isolation machinery (verdict logic, crosswalk verse fetch
DISCRIMINATING crosswalk from identity, p3 guarded output path) BEFORE it
can matter. Hebrew is byte-spliced from verse_map_oshb.json (never
hand-typed); English is spliced from verse_map_web.json."""
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
pm = json.loads((SPBOOK / "pmarks_Song.json").read_text(encoding="utf-8"))


def webtxt(ref):
    return re.sub(r"\[fn [^\]]*\]", " ", web[ref]["text"]).strip()


heb_2_7 = oshb["Song.2.7"]["text"]                   # SAMEKH-bearing adjuration verse
heb_7_1 = oshb["Song.7.1"]["text"]                   # the seam verse (MT 7:1 = WEB 6:13)
heb_3_2 = oshb["Song.3.2"]["text"]                   # full pointed verse (wrong-ref fixture)
web_2_5 = webtxt("Song.2.5")
web_6_13 = webtxt("Song.6.13")
web_7_3 = webtxt("Song.7.3")
web_3_7 = webtxt("Song.3.7")

# preconditions for the rows below (fail loudly if the data moves)
assert pm["marks"].get("Song.2.7") == ["SAMEKH"], "smoke precondition: SAMEKH at MT 2:7"
assert pm["marks"].get("Song.8.10") == ["PE"], "smoke precondition: PE at MT 8:10"
assert pm["marks"].get("Song.3.5") == ["SAMEKH"], "smoke precondition: SAMEKH at MT 3:5 (absence-arm seam)"
for k in ("Song.2.1", "Song.2.4", "Song.2.5", "Song.2.6", "Song.3.4", "Song.3.6",
          "Song.6.12", "Song.7.1", "Song.7.2"):
    assert not pm["marks"].get(k), f"smoke precondition: {k} must be mark-free"
assert pm["kq"].get("Song.2.11"), "smoke precondition: K/Q at MT 2:11"
for k in ("Song.2.5", "Song.2.7", "Song.3.6", "Song.7.1", "Song.7.2"):
    assert not pm["kq"].get(k), f"smoke precondition: {k} must be K/Q-free"
assert not pm["paseq"].get("Song.3.6"), "smoke precondition: 3:6 paseq-free"

COMMON = {
    "book": "Song", "model_id": "M8_fable", "non_authorizing": True,
    "literature_type_guess": "lyric_poetry", "confidence": "high",
    "strong_or_hebrew_tags_used": False,
    "wj_or_red_letter_considered": "not applicable in the OT substrate",
    "frontier_flag_considered": False, "review_status": "draft",
    "observed_substrate_signals": ["adjuration_refrain.smoke_fixture"],
}

rows = [
    # clean row A: identity zone; SAMEKH at MT 2:7 disclosed; optional dual
    # correct; byte-spliced Hebrew bound to its cited ref; proper X-X span;
    # full schema incl. range-shaped parent_collection (p1 skip class)
    {
        **COMMON,
        "decision_id": "SMOKE-A", "chunk_index_in_book": 1,
        "span": "Song.2.5-Song.2.7",
        "parent_collection": "SMOKE Song.1.1-Song.8.14",
        "unit_type": "smoke_lyric",
        "writer_part": "p00", "writer_decision_id": "SMOKE-A",
        "writer_attempt_id": "smoke_song_r1",
        "boundary_evidence_refs": [
            "web:Song.2.5 = oshb:Song.2.5",
            "oshb:Song.2.7 (setumah, single-witness)",
        ],
        "boundary_rationale": ("The faintness plea opens the unit: “" + web_2_5 +
                               "” (web:Song.2.5). The adjuration closes it: " +
                               heb_2_7 + " (oshb:Song.2.7); a setumah stands at "
                               "oshb:Song.2.7 (single-witness), closing the unit."),
        "strongest_rejected_alternative": "A cut after web:Song.2.6 was rejected; the adjuration completes the embrace scene.",
        "device_notes": "Refrain bracket recorded from the byte inventories.",
    },
    # clean row B: THE OFFSET-ZONE row — WEB 6:13-7:1 spans MT 7:1-7:2;
    # mandatory duals correct; Hebrew spliced from the seam verse itself
    {
        **COMMON,
        "decision_id": "SMOKE-B", "chunk_index_in_book": 2,
        "span": "Song.6.13-Song.7.1",
        "parent_collection": "SMOKE Song.1.1-Song.8.14",
        "unit_type": "smoke_lyric",
        "writer_part": "p00", "writer_decision_id": "SMOKE-B",
        "writer_attempt_id": "smoke_song_r1",
        "boundary_evidence_refs": [
            "web:Song.6.13 = oshb:Song.7.1",
            "web:Song.7.1 = oshb:Song.7.2",
        ],
        "boundary_rationale": ("The return-call opens the exchange: “" + web_6_13 +
                               "” (web:Song.6.13 = oshb:Song.7.1). The Hebrew runs " +
                               heb_7_1 + " (oshb:Song.7.1). The sandal-line answer "
                               "follows at web:Song.7.1 (MT 7:2)."),
        "strongest_rejected_alternative": "Starting at web:Song.7.1 was rejected; the call and the gaze question govern the answer.",
        "device_notes": "Crosswalk duals verified against the offset map.",
    },
    # bad row: every planted defect class, one row
    {
        **COMMON,
        "decision_id": "SMOKE-BAD", "chunk_index_in_book": 3,
        "span": "Song.3.6",                                 # (1) not X-X form
        "parent_collection": "SMOKE Song.1.1-Song.8.14",
        "unit_type": "smoke_saying",
        "writer_part": "p00", "writer_decision_id": "SMOKE-BAD",
        "writer_attempt_id": "smoke_song_r1",
        "boundary_evidence_refs": [
            # order matters: the setumah fixture must sit >120 chars from the
            # device_notes prose pair, whose crosswalk reading could otherwise
            # satisfy the dual-reading mark check (window heuristic)
            "web:Song.7.3 = oshb:Song.7.3",                 # (2) crosswalk dual wrong
            "web:Song.2.1-Song.2.99",                       # (6) range END out of range
            "LXX Song 2:1",                                 # (8) cross-tradition in refs
            "web:Song.5.0",                                 # (9) zero-verse pseudo-ref invalid
            "oshb:Song.3.6 (setumah, single-witness)",      # (3) mark claim at markless verse
            "oshb:Song.2.1 (selah)",                        # (4) selah fabrication in Song
            "oshb:Song.3.6 (paseq)",                        # (5) no paseq at 3:6 + no disclosure
            "oshb:Song.3.6 (qere)",                         # (7) false K/Q claim
            "oshb:Song.3.4 (small nun, single-witness)",    # (10) special-letter fabrication
            "web:Song.7.5",                                 # (11) offset-zone bare ref
            "web:Song.7.2 (MT 7:2)",                        # (12) MT qualifier wrong (expect 7:3)
        ],
        "boundary_rationale": ("The book's only incense-column scene — no other "  # (13) universal, no digit
                               "chapter does this. There is no setumah anywhere "  # (21) false absence claim (seam MT 3:5)
                               "in this span. Verse 7 confirms the arc, "          # (14) unmirrored bare verse
                               "and Song.4.2 echoes it. The quoted line " +        # (15) unmirrored ref
                               heb_3_2 +                                           # (16) Hebrew bound to WRONG ref
                               " (oshb:Song.3.5) proves it. Song.3.2 is in "
                               "Aramaic here. The zone reads “" + web_7_3 +        # (17) Aramaic label
                               "” (web:Song.7.2)."),                               # (18) neighbor-only in offset zone
        "strongest_rejected_alternative": "“" + web_3_7 + "” (web:Song.3.4)",      # (19) WEB misquote, wrong ref
        "device_notes": ("The pair web:Song.7.6 = oshb:Song.7.6 anchors "          # (20) prose dual arithmetic wrong
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
    "mark_symmetry": ["selah_claim_in_song", "paragraph_mark_claim",
                      "false_mark_absence_claim", "special_letter_claim_in_song",
                      "kq_claim"],
    "refs_mirror": ["Song.3.7", "Song.4.2"],
    "universals": ["only"],
    "language_zones": ["aramaic_label"],
    "web_quotes": ["Song.3.4"],
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
        "Song.7.6" not in blob["citation_sweep"]:
    extra_missed.append(("citation_sweep", "prose dual-cite crosswalk arm"))
if report["web_quotes"].get("neighbor_only_warn_count", 0) < 1:
    extra_missed.append(("web_quotes", "offset-zone neighbor-only warn arm"))

# ---- check_atomic_isolation machinery arm (verdicts + crosswalk + p3) ----
at_rows = [
    {"writer_decision_id": "AT-1", "span": "Song.2.16-Song.2.16",
     "unit_type": "test_atomic", "confidence": "high"},         # cohesion_live (shares dodi with 2:17)
    {"writer_decision_id": "AT-2", "span": "Song.5.9-Song.5.9",
     "unit_type": "test_atomic", "confidence": "high"},         # machine_clean expected
    {"writer_decision_id": "AT-3", "span": "Song.7.9-Song.7.9",
     "unit_type": "test_atomic", "confidence": "high"},         # crosswalk proof: MT 7:10 & MT 7:11 share le-dodi (identity would find NO share)
    {"writer_decision_id": "AT-4", "span": "Song.7.1-Song.7.1",
     "unit_type": "other_type", "confidence": "high"},          # model_review (form)
    {"writer_decision_id": "AT-5", "span": "Song.5.10-Song.5.10",
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
    atomic_problems.append("p3 GUARD BROKEN: subset run touched SP/Song/review_scope.json")

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
if v["AT-1"]["verdict"] != "cohesion_live" or "דודי" not in v["AT-1"].get("shared_next", []):
    atomic_problems.append(f"AT-1 expected cohesion_live via dodi: {v['AT-1']}")
if v["AT-2"]["verdict"] != "machine_clean":
    atomic_problems.append(f"AT-2 expected machine_clean: {v['AT-2']}")
if v["AT-4"]["verdict"] != "model_review" or v["AT-5"]["verdict"] != "model_review":
    atomic_problems.append("AT-4/AT-5 expected model_review")
# crosswalk proof: WEB 7:9's tokens come from MT 7:10 and share le-dodi with
# its next neighbor WEB 7:10 (= MT 7:11); the identity mapping (MT 7:9 vs MT
# 7:10) shares NOTHING — this share only exists through the crosswalk.
at3 = v["AT-3"]
if at3["verdict"] != "cohesion_live" or "לדודי" not in at3.get("shared_next", []):
    atomic_problems.append(f"AT-3 crosswalk fetch wrong: {at3}")
if shared_plan.exists() != plan_before:
    atomic_problems.append("p3 GUARD BROKEN on armed run")

# ---- collate crosswalk CLI arm: bare WEB ref 6:13 must byte-match MT 7:1 ----
proc3 = subprocess.run([sys.executable, str(TOOLS / "collate.py"),
                        "--ref", "Song.6.13", "--quote", heb_7_1],
                       capture_output=True, text=True, encoding="utf-8")
col = json.loads(proc3.stdout)
collate_ok = col.get("tier") == "byte" and "7.1" in col.get("mt_window", "")

verdict = ("PASS" if not missed and not clean_hit and not extra_missed
           and not atomic_problems and collate_ok else "FAIL")
print(json.dumps({"planted_defects_missed": missed + extra_missed,
                  "clean_rows_flagged_by": clean_hit,
                  "atomic_isolation_problems": atomic_problems,
                  "collate_crosswalk_cli": col,
                  "verdict": verdict},
                 ensure_ascii=False, indent=1))
